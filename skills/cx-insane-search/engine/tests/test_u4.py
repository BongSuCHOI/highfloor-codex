#!/usr/bin/env python3
"""U4 tests — SessionPool, root warmup, browser→curl cookie bridge.

Offline unit tests + a couple of benign online checks (example.com). Run:
    python3 engine/tests/test_u4.py
"""
from __future__ import annotations

import os
import sys
import inspect
import tempfile
from unittest.mock import patch

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ""))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))

from engine.transport import SessionPool, _host_of, _root_of  # noqa: E402
from engine.executor import _parse_envelope, _profile_dir_for  # noqa: E402
from engine.fetch_chain import fetch  # noqa: E402


def t_host_and_root_helpers():
    assert _host_of("https://www.x.com/a/b?q=1") == "www.x.com"
    assert _root_of("https://www.x.com/a/b?q=1") == "https://www.x.com/"
    print("  ✓ host/root helpers")


def t_session_reuse_same_key():
    p = SessionPool()
    e1 = p.get("www.x.com", "safari")
    e2 = p.get("www.x.com", "safari")
    e3 = p.get("www.x.com", "chrome")
    if e1 is None:
        print("  ⚠ curl_cffi unavailable — skipped reuse check")
        return
    assert e1 is e2, "same (host,impersonate) must reuse entry"
    assert e1 is not e3, "different impersonate must be separate session"
    assert p.stats()["sessions"] == 2, p.stats()
    print(f"  ✓ session reuse (same key→same, diff impersonate→new): {p.stats()}")


def t_inject_cookies_then_present():
    p = SessionPool()
    ok = p.inject_cookies("www.x.com", "chrome",
                          [{"name": "cf_clearance", "value": "abc", "domain": "www.x.com"}],
                          user_agent="UA/1.0")
    ent = p.get("www.x.com", "chrome")
    if ent is None:
        print("  ⚠ curl_cffi unavailable — skipped cookie inject check")
        return
    assert ok, "inject should report success"
    assert ent.injected_ua == "UA/1.0"
    names = {c.name for c in ent.session.cookies.jar}
    assert "cf_clearance" in names, names
    print(f"  ✓ injected cookies present on session: {sorted(names)}")


def t_parse_envelope_json():
    env = '{"html":"<h1>hi</h1>","finalUrl":"https://x/p","status":200,' \
          '"cookies":[{"name":"a","value":"b"}],"userAgent":"UA"}'
    html, final, status, cookies, ua, automation, inner_text = _parse_envelope(env, "https://x/q")
    assert html == "<h1>hi</h1>" and final == "https://x/p" and status == 200
    assert cookies and cookies[0]["name"] == "a" and ua == "UA"
    assert inner_text == "", f"innerText should default to '' (got {inner_text!r})"
    print("  ✓ envelope JSON parsed (innerText backward-compat default '')")


def t_parse_envelope_raw_html_fallback():
    html, final, status, cookies, ua, automation, inner_text = _parse_envelope(
        "<html>raw</html>", "https://x/q")
    assert html == "<html>raw</html>" and final == "https://x/q" and status == 200
    assert cookies == [] and ua is None
    assert inner_text == ""
    print("  ✓ raw-HTML fallback (non-JSON stdout, innerText default '')")


def t_browser_state_is_process_scoped_and_fallback_default_off():
    with patch.dict(
        os.environ,
        {
            key: value
            for key, value in os.environ.items()
            if key not in {"INSANE_PERSIST_BROWSER_PROFILE", "INSANE_BROWSER_PROFILE_PATH"}
        },
        clear=True,
    ):
        first = _profile_dir_for("https://example.com/a", "playwright_real_chrome")
        second = _profile_dir_for("https://example.com/b", "playwright_real_chrome")
    assert first == second
    assert "cx-insane-search-pw-" in first, first
    assert "/.insane_pw/" not in first, first
    assert inspect.signature(fetch).parameters["enable_playwright"].default is False

    with tempfile.TemporaryDirectory() as persistent_root:
        with patch.dict(
            os.environ,
            {
                "INSANE_PERSIST_BROWSER_PROFILE": "1",
                "INSANE_BROWSER_PROFILE_PATH": persistent_root,
            },
            clear=False,
        ):
            persistent = _profile_dir_for(
                "https://example.com/a", "playwright_real_chrome"
            )
        assert persistent.startswith(persistent_root), persistent
    print("  ✓ browser profile is process-scoped; local fallback defaults off")


def t_warmup_once_guard_online():
    p = SessionPool()
    first = p.warmup("example.com", "safari", "https://example.com/", timeout=15)
    second = p.warmup("example.com", "safari", "https://example.com/", timeout=15)
    ent = p.get("example.com", "safari")
    if ent is None:
        print("  ⚠ curl_cffi unavailable — skipped warmup check")
        return
    # first may be True (network) or False (offline); second must be False (guard).
    assert second is False, "warmup must be idempotent"
    assert ent.warmed is True
    print(f"  ✓ warmup once-guard (first={first}, second={second})")


def t_fetch_many_reuses_pool_online():
    from engine import transport
    from engine.fetch_chain import fetch_many
    transport.POOL.reset()
    results = fetch_many(
        ["https://example.com/", "https://example.com/index.html"],
        success_selectors=["h1", "p"], timeout=15, max_attempts=2, enable_playwright=False,
    )
    st = transport.POOL.stats()
    assert len(results) == 2
    # Same host → should not spawn a separate session per URL per identity.
    assert st["sessions"] <= 2, st
    oks = sum(1 for r in results if r.ok)
    print(f"  ✓ fetch_many reused pool: stats={st}, ok={oks}/2")


ALL = [
    ("host_and_root_helpers", t_host_and_root_helpers),
    ("session_reuse_same_key", t_session_reuse_same_key),
    ("inject_cookies_then_present", t_inject_cookies_then_present),
    ("parse_envelope_json", t_parse_envelope_json),
    ("parse_envelope_raw_html_fallback", t_parse_envelope_raw_html_fallback),
    (
        "browser_state_is_process_scoped_and_fallback_default_off",
        t_browser_state_is_process_scoped_and_fallback_default_off,
    ),
    ("warmup_once_guard_online", t_warmup_once_guard_online),
    ("fetch_many_reuses_pool_online", t_fetch_many_reuses_pool_online),
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
