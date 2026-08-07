#!/usr/bin/env python3
"""U7 tests — SSRF / redirect guard. Offline & deterministic.

Run:  python3 engine/tests/test_u7.py
"""
from __future__ import annotations

import os
import sys
from types import SimpleNamespace
from unittest.mock import patch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))

from engine.safety import classify_url  # noqa: E402
from engine.transport import SessionPool          # noqa: E402
from engine.phase0 import _canonical_youtube_url, _cffi_get, _detect, route  # noqa: E402


def t_classify_blocks_internal():
    blocked = [
        "http://127.0.0.1/",
        "http://169.254.169.254/latest/meta-data/",   # cloud metadata
        "http://10.0.0.1/",
        "http://192.168.1.1/admin",
        "http://172.16.0.1/",
        "http://[::1]/",
        "http://0.0.0.0/",
        "http://224.0.0.1/",                          # IPv4 multicast
        "http://[ff02::1]/",                          # IPv6 multicast
        "ftp://example.com/",                          # scheme
        "file:///etc/passwd",                          # scheme
        "http://localhost/",                           # resolves to loopback
    ]
    for u in blocked:
        ok, reason = classify_url(u, allow_private=False)
        assert not ok, f"should block {u} (got ok, reason={reason})"
    print(f"  ✓ blocks {len(blocked)} internal/metadata/scheme targets")


def t_classify_allows_public():
    for u in ["https://1.1.1.1/", "http://8.8.8.8/"]:   # public IP literals (no DNS)
        ok, reason = classify_url(u, allow_private=False)
        assert ok, f"should allow public {u} ({reason})"
    print("  ✓ allows public IP literals")


def t_allow_private_optin():
    ok, _ = classify_url("http://127.0.0.1:8080/", allow_private=True)
    assert ok, "allow_private=True must permit loopback"
    print("  ✓ allow_private=True opt-in permits loopback (local testing)")


def t_dns_failure_and_empty_fail_closed():
    with patch("engine.safety.socket.getaddrinfo", side_effect=OSError("offline")):
        ok, reason = classify_url("https://public.test/")
        assert not ok and reason.startswith("resolve_failed:"), (ok, reason)
    with patch("engine.safety.socket.getaddrinfo", return_value=[]):
        ok, reason = classify_url("https://public.test/")
        assert not ok and reason == "resolve_empty", (ok, reason)
    print("  ✓ DNS failure and empty answers fail closed")


def t_mixed_public_private_dns_fails_closed():
    answers = [
        (2, 1, 6, "", ("1.1.1.1", 443)),
        (2, 1, 6, "", ("127.0.0.1", 443)),
    ]
    with patch("engine.safety.socket.getaddrinfo", return_value=answers):
        ok, reason = classify_url("https://mixed.test/")
    assert not ok and reason.startswith("resolves_non_global:"), (ok, reason)
    print("  ✓ one non-global A/AAAA answer blocks the whole target")


def t_request_blocks_localhost_by_default():
    p = SessionPool()
    resp, err = p.request("http://127.0.0.1:9/", impersonate="chrome")  # no fetch happens
    assert resp is None and err and err.startswith("ssrf_blocked"), (resp, err)
    print(f"  ✓ POOL.request blocks loopback pre-fetch: {err}")


def t_request_cannot_enable_private_targets():
    p = SessionPool()
    response, error = p.request(
        "http://127.0.0.1:9/",
        impersonate="chrome",
        allow_private=True,
    )
    assert response is None and error == "ssrf_blocked:private_targets_disabled"
    print("  ✓ production request path cannot opt into private targets")


def t_warmup_reuses_guarded_transport():
    pool = SessionPool()
    entry = SimpleNamespace(warmed=False)
    calls = []
    pool.get = lambda host, impersonate: entry

    def guarded_request(url, **kwargs):
        calls.append((url, kwargs))
        return _FakeResp(200), None

    pool.request = guarded_request
    ok = pool.warmup(
        "example.com",
        "chrome",
        "https://example.com/",
        timeout=7,
    )
    assert ok and entry.warmed
    assert calls == [
        ("https://example.com/", {"impersonate": "chrome", "timeout": 7})
    ], calls
    print("  ✓ root warmup reuses the guarded redirect transport")


class _FakeResp:
    def __init__(self, status, headers=None):
        self.status_code = status
        self.headers = headers or {}
        self.text = "ok"


def t_redirect_to_metadata_blocked():
    def do_get(u, _target):
        if "start" in u:
            return _FakeResp(302, {"Location": "http://169.254.169.254/latest/meta-data/"})
        return _FakeResp(200)
    resp, err = SessionPool._fetch_following(
        do_get, "https://1.1.1.1/start", False, 5
    )
    assert resp is None and err and err.startswith("ssrf_redirect_blocked"), (resp, err)
    print(f"  ✓ redirect into metadata IP blocked: {err}")


def t_safe_redirect_followed():
    hops = {"n": 0}
    def do_get(u, _target):
        hops["n"] += 1
        if "start" in u:
            return _FakeResp(302, {"Location": "http://1.1.1.1/landing"})  # public
        return _FakeResp(200)
    resp, err = SessionPool._fetch_following(
        do_get, "https://8.8.8.8/start", False, 5
    )
    assert err is None and resp is not None and resp.status_code == 200, (resp, err)
    assert hops["n"] == 2, hops
    print(f"  ✓ safe redirect to public IP followed ({hops['n']} hops → 200)")


def t_too_many_redirects():
    def do_get(u, _target):
        return _FakeResp(302, {"Location": "http://1.1.1.1/loop"})
    resp, err = SessionPool._fetch_following(
        do_get, "http://1.1.1.1/loop", False, 3
    )
    assert resp is None and err == "too_many_redirects", (resp, err)
    print("  ✓ redirect loop capped (too_many_redirects)")


def t_request_pins_checked_dns_and_disables_env_proxy():
    captured = {}

    class FakeSession:
        def __init__(self, **kwargs):
            captured["session_kwargs"] = kwargs
            self.curl_options = {}
            self.cookies = SimpleNamespace(set=lambda *args, **kwargs: None)

        def get(self, url, **kwargs):
            captured["resolve"] = list(self.curl_options.get("RESOLVE", []))
            captured["request_kwargs"] = kwargs
            response = _FakeResp(200)
            response.url = url
            response.primary_ip = "1.1.1.1"
            return response

        def close(self):
            pass

    fake_curl = SimpleNamespace(
        CurlOpt=SimpleNamespace(RESOLVE="RESOLVE"),
        requests=SimpleNamespace(Session=FakeSession),
    )
    answers = [(2, 1, 6, "", ("1.1.1.1", 443))]
    with patch.dict(sys.modules, {"curl_cffi": fake_curl}):
        with patch("engine.safety.socket.getaddrinfo", return_value=answers) as resolver:
            response, error = SessionPool().request(
                "https://public.test/path",
                impersonate="chrome",
            )
    assert error is None and response is not None, error
    assert captured["session_kwargs"]["trust_env"] is False
    assert captured["request_kwargs"]["allow_redirects"] is False
    assert captured["resolve"] == ["public.test:443:1.1.1.1"], captured
    assert resolver.call_count == 1, resolver.call_count
    print("  ✓ checked DNS is pinned into curl; implicit environment proxy is disabled")


def t_phase0_rejects_spoof_hosts_and_open_redirect_shape():
    rejected = [
        "https://reddit.com.evil.example/r/test",
        "https://evilreddit.com/r/test",
        "https://notyoutube.com/watch?v=dQw4w9WgXcQ",
        "https://youtube.com.evil.example/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/redirect?q=http://127.0.0.1/",
    ]
    assert all(_detect(url) is None for url in rejected), rejected
    assert _canonical_youtube_url(
        "https://youtu.be/dQw4w9WgXcQ"
    ) == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    with patch("engine.phase0.subprocess.run", side_effect=AssertionError("must not run")):
        assert route("https://www.youtube.com/redirect?q=http://127.0.0.1/") is None
    print("  ✓ spoof hosts and YouTube open-redirect shape stay out of Phase 0")


def t_phase0_http_uses_guarded_pool():
    response = _FakeResp(200)
    response.url = "https://1.1.1.1/"
    with patch(
        "engine.transport.POOL.request",
        return_value=(response, None),
    ) as request:
        assert _cffi_get("https://1.1.1.1/") is response
    assert request.call_args.args == ("https://1.1.1.1/",)
    assert request.call_args.kwargs["impersonate"] == "safari"
    print("  ✓ Phase 0 HTTP routes through the guarded pool")


ALL = [
    ("classify_blocks_internal", t_classify_blocks_internal),
    ("classify_allows_public", t_classify_allows_public),
    ("allow_private_optin", t_allow_private_optin),
    ("dns_failure_and_empty_fail_closed", t_dns_failure_and_empty_fail_closed),
    ("mixed_public_private_dns_fails_closed", t_mixed_public_private_dns_fails_closed),
    ("request_blocks_localhost_by_default", t_request_blocks_localhost_by_default),
    ("request_cannot_enable_private_targets", t_request_cannot_enable_private_targets),
    ("warmup_reuses_guarded_transport", t_warmup_reuses_guarded_transport),
    ("redirect_to_metadata_blocked", t_redirect_to_metadata_blocked),
    ("safe_redirect_followed", t_safe_redirect_followed),
    ("too_many_redirects", t_too_many_redirects),
    ("request_pins_checked_dns_and_disables_env_proxy", t_request_pins_checked_dns_and_disables_env_proxy),
    ("phase0_rejects_spoof_hosts_and_open_redirect_shape", t_phase0_rejects_spoof_hosts_and_open_redirect_shape),
    ("phase0_http_uses_guarded_pool", t_phase0_http_uses_guarded_pool),
]


def main() -> int:
    p = f = 0
    for name, fn in ALL:
        try:
            print(f"[{name}]")
            fn()
            p += 1
        except AssertionError as e:
            f += 1
            print(f"  ✗ FAIL: {e}")
        except Exception as e:
            f += 1
            print(f"  ✗ ERROR: {type(e).__name__}: {e}")
    print(f"\n{p} passed, {f} failed")
    return 0 if f == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
