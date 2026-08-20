"""Per-host curl_cffi Session pool + root warmup + browser→curl cookie bridge.

Why (multi-AI review 2026-06-21):
  * v1 issued a brand-new `curl_cffi.requests.get()` per attempt, so cookies
    set by a WAF (e.g. an Akamai `_abck` sensor or a CF `cf_clearance`) and
    the warm TLS/connection were thrown away between attempts and between
    pages of the same host. That caps both success rate (sensor cookies never
    mature) and throughput (handshake per request).
  * A browser fallback that punches through a JS challenge produces exactly the
    cookies + User-Agent a plain HTTP client needs — but v1 discarded them
    (`_FakeResp` kept only HTML). The bridge here lets one expensive browser
    pass convert into cheap curl_cffi throughput (the FlareSolverr pattern).

No-Site-Name Rule: the transport has no site-specific branches, and persistent
learning hashes host keys.
"""
from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Optional
from urllib.parse import urlsplit


@lru_cache(maxsize=1)
def available_impersonates() -> Optional[frozenset[str]]:
    """Return targets supported by the installed curl_cffi, when inspectable."""
    try:
        from curl_cffi import requests as cffi_requests
        from curl_cffi.requests.impersonate import REAL_TARGET_MAP
        return frozenset(browser.value for browser in cffi_requests.BrowserType) | frozenset(
            REAL_TARGET_MAP.keys()
        )
    except Exception:
        return None


def filter_available(targets: list[str]) -> list[str]:
    """Remove known-unsupported targets without failing on older runtimes."""
    available = available_impersonates()
    if available is None:
        return targets
    return [target for target in targets if target in available]


def select_available(targets: list[str]) -> Optional[str]:
    """Choose a supported target, preserving order and a visible fallback."""
    if not targets:
        return None
    available = available_impersonates()
    if available is None:
        return targets[0]
    for target in targets:
        if target in available:
            return target
    return min(available) if available else None


# Transient statuses worth an in-place retry on the SAME identity — rotating
# to a different TLS family does not help rate-limit / gateway recovery, but
# the same warm session a moment later often succeeds.
_RETRY_STATUSES = frozenset({429, 502, 503, 504})
_RETRY_BASE_DELAY = 1.5       # seconds; backoff = base * (factor ** attempt)
_RETRY_FACTOR = 2.0
_RETRY_SLEEP_CAP = 10.0       # ceiling on TOTAL retry sleep per request


def _host_of(url: str) -> str:
    return (urlsplit(url).hostname or "unknown").lower()


def _root_of(url: str) -> str:
    p = urlsplit(url)
    return f"{p.scheme}://{p.netloc}/"


def _cookie_matches_host(cookie: dict, host: str) -> bool:
    domain = str(cookie.get("domain") or host).lower().lstrip(".").rstrip(".")
    normalized_host = host.lower().rstrip(".")
    if not domain:
        return False
    if normalized_host == domain:
        return True
    return "." in domain and normalized_host.endswith(f".{domain}")


@dataclass
class _Entry:
    session: Any
    resolved_ips: tuple[str, ...] = ()
    warmed: bool = False
    injected_ua: Optional[str] = None
    requests_made: int = 0


@dataclass
class SessionPool:
    """Pool keyed by scheme, host, port, curl identity, and checked IP set."""
    _entries: dict = field(default_factory=dict)
    _cookie_seeds: dict = field(default_factory=dict)
    _lock: Any = field(default_factory=threading.Lock)

    def _key(
        self,
        host: str,
        impersonate: str,
        resolved_ips: tuple[str, ...] = (),
        scheme: str = "",
        port: int = 0,
    ) -> tuple:
        return (scheme, host, port, impersonate, resolved_ips)

    def get(
        self,
        host: str,
        impersonate: str,
        resolved_ips: tuple[str, ...] = (),
        scheme: str = "",
        port: int = 0,
    ) -> Optional[_Entry]:
        """Return (creating if needed) the pool entry, or None if curl_cffi
        is unavailable."""
        key = self._key(host, impersonate, resolved_ips, scheme, port)
        with self._lock:
            ent = self._entries.get(key)
            if ent is not None:
                return ent
            try:
                from curl_cffi import requests as cffi_requests
            except ImportError:
                return None
            try:
                sess = cffi_requests.Session(
                    impersonate=impersonate,
                    trust_env=False,
                )
            except Exception:
                return None
            ent = _Entry(session=sess, resolved_ips=resolved_ips)
            seed = self._cookie_seeds.get((host, impersonate))
            if seed:
                cookies, user_agent = seed
                self._apply_cookie_seed(ent, host, cookies, user_agent)
            self._entries[key] = ent
            return ent

    def warmup(self, host: str, impersonate: str, root_url: str, timeout: int = 15) -> bool:
        """Hit the site root once per (host, impersonate) so a WAF sensor can
        set a resolved session cookie before the real (deep) request. Idempotent."""
        ent = self.get(host, impersonate)
        if ent is None or ent.warmed:
            return False
        if _host_of(root_url).rstrip(".") != host.lower().rstrip("."):
            ent.warmed = True   # don't retry a blocked root
            return False
        ent.warmed = True  # mark first to avoid duplicate warmups under race
        response, error = self.request(
            root_url,
            impersonate=impersonate,
            timeout=timeout,
        )
        return response is not None and error is None

    def inject_cookies(self, host: str, impersonate: str,
                       cookies: list[dict], user_agent: Optional[str] = None) -> bool:
        """Seed a session with cookies harvested by a real browser. Subsequent
        requests on this (host, impersonate) reuse the browser-cleared state."""
        filtered = [c for c in cookies or [] if _cookie_matches_host(c, host)]
        if not filtered and not user_agent:
            return False
        with self._lock:
            self._cookie_seeds[(host, impersonate)] = (filtered, user_agent)
            entries = [
                ent for key, ent in self._entries.items()
                if key[1] == host and key[3] == impersonate
            ]
        if not entries:
            ent = self.get(host, impersonate)
            entries = [ent] if ent is not None else []
        ok = False
        for ent in entries:
            ok = self._apply_cookie_seed(ent, host, filtered, user_agent) or ok
        return ok

    @staticmethod
    def _apply_cookie_seed(
        ent: _Entry,
        host: str,
        cookies: list[dict],
        user_agent: Optional[str],
    ) -> bool:
        ok = False
        for c in cookies:
            name = c.get("name")
            value = c.get("value")
            if not name:
                continue
            try:
                ent.session.cookies.set(name, value, domain=c.get("domain") or host)
                ok = True
            except Exception:
                try:
                    ent.session.cookies.set(name, value)
                    ok = True
                except Exception:
                    continue
        if user_agent:
            ent.injected_ua = user_agent
            ok = True
        return ok

    def request(self, url: str, *, impersonate: str, referer: str = "",
                timeout: int = 25, extra_headers: Optional[dict] = None,
                allow_private: Optional[bool] = None,
                max_redirects: Optional[int] = None,
                max_retries: int = 0) -> tuple[Any, Optional[str]]:
        """GET via the pooled session (cookie + connection reuse), with an SSRF
        guard: the initial URL and EVERY redirect hop are validated against the
        non-global-address block-list and pinned before being fetched.

        ``max_retries`` > 0 retries transient statuses (429/502/503/504) on the
        SAME identity with exponential backoff before the caller sees the
        response. A numeric ``Retry-After`` header overrides the backoff delay;
        total retry sleep is capped (see ``_retry_transient``). Default 0 —
        callers opt in per request so a failing grid never multiplies sleeps."""
        from . import safety
        if allow_private:
            return None, "ssrf_blocked:private_targets_disabled"
        allow_private = False
        if max_redirects is None:
            max_redirects = safety.DEFAULT_MAX_REDIRECTS

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        if referer:
            headers["Referer"] = referer
        if extra_headers:
            headers.update(extra_headers)

        def _do_get(current_url, target):
            ent = self.get(
                target.host,
                impersonate,
                target.ips,
                scheme=target.scheme,
                port=target.port,
            )
            if ent is None:
                raise RuntimeError("curl_cffi not installed or impersonate unavailable")
            try:
                from curl_cffi import CurlOpt
            except ImportError:
                raise RuntimeError("curl_cffi not installed")
            resolve_entries = target.curl_resolve_entries()
            if resolve_entries:
                ent.session.curl_options[CurlOpt.RESOLVE] = resolve_entries
            else:
                ent.session.curl_options.pop(CurlOpt.RESOLVE, None)
            request_headers = dict(headers)
            if ent.injected_ua:
                request_headers.setdefault("User-Agent", ent.injected_ua)
            response = ent.session.get(
                current_url,
                headers=request_headers,
                timeout=timeout,
                allow_redirects=False,
            )
            ent.requests_made += 1
            primary_ip = str(getattr(response, "primary_ip", "") or "")
            if primary_ip:
                import ipaddress
                primary_ip = primary_ip.split("%", 1)[0]
                try:
                    primary_ip = str(ipaddress.ip_address(primary_ip))
                except ValueError:
                    raise RuntimeError(f"connection_ip_invalid:{primary_ip}")
                if safety._ip_blocked(primary_ip) or primary_ip not in target.ips:
                    raise RuntimeError(f"connection_ip_mismatch:{primary_ip}")
            return response

        return self._fetch_following(_do_get, url, allow_private, max_redirects,
                                     max_retries=max_retries)

    @staticmethod
    def _fetch_following(do_get, url: str, allow_private: bool, max_redirects: int,
                         *, max_retries: int = 0) -> tuple[Any, Optional[str]]:
        """Resolve, pin, and fetch each redirect hop independently.

        Only the FIRST attempt on the original URL gets the transient-status
        retry loop; redirect hops are distinct URLs and are not retried."""
        from . import safety
        cur = url
        first = True
        for _ in range(max_redirects + 1):
            target, reason = safety.resolve_public_target(cur, allow_private=allow_private)
            if target is None:
                prefix = "ssrf_blocked" if first else "ssrf_redirect_blocked"
                return None, f"{prefix}:{reason}"
            try:
                if first and max_retries > 0:
                    resp = _retry_transient(
                        lambda current: do_get(current, target),
                        target.request_url,
                        max_retries,
                    )
                else:
                    resp = do_get(target.request_url, target)
                first = False
            except Exception as e:
                return None, f"{type(e).__name__}:{str(e)[:200]}"
            if safety.is_redirect(resp):
                loc = safety.location_of(resp)
                if not loc:
                    return resp, None     # redirect w/o Location → return as-is
                nxt = safety.resolve_redirect(target.request_url, loc)
                cur = nxt
                continue
            return resp, None
        return None, "too_many_redirects"

    def stats(self) -> dict:
        with self._lock:
            return {
                "sessions": len(self._entries),
                "warmed": sum(1 for e in self._entries.values() if e.warmed),
                "requests": sum(e.requests_made for e in self._entries.values()),
            }

    def reset(self) -> None:
        with self._lock:
            for e in self._entries.values():
                try:
                    e.session.close()
                except Exception:
                    pass
            self._entries.clear()
            self._cookie_seeds.clear()


# Process-wide pool. INSANE_NO_SESSION_POOL disables optional warmup and
# cookie-bridge reuse; guarded requests still use a target-pinned session.
POOL = SessionPool()


def pool_enabled() -> bool:
    return os.environ.get("INSANE_NO_SESSION_POOL", "") not in ("1", "true", "yes")


def _retry_after_seconds(resp) -> Optional[float]:
    """Numeric Retry-After header value, or None (absent / HTTP-date form)."""
    headers = getattr(resp, "headers", None) or {}
    try:
        raw = headers.get("Retry-After") or headers.get("retry-after")
    except Exception:
        return None
    if not raw:
        return None
    try:
        return max(0.0, float(str(raw).strip()))
    except ValueError:
        return None


def _retry_transient(do_get, url: str, max_attempts: int,
                     retry_statuses: frozenset = _RETRY_STATUSES,
                     base: float = _RETRY_BASE_DELAY,
                     factor: float = _RETRY_FACTOR,
                     sleep_cap: float = _RETRY_SLEEP_CAP) -> Any:
    """Call ``do_get(url)`` up to ``max_attempts + 1`` times. On a transient
    status (429/502/503/504) sleep, then retry the SAME identity — the warm
    session and cookies are exactly what a rate-limiter wants to see again.

    A numeric ``Retry-After`` header overrides the exponential backoff for
    that attempt. Total sleep across all retries is capped at ``sleep_cap``
    seconds so a huge or hostile Retry-After cannot stall the caller. Returns
    the last response; the caller classifies the verdict."""
    resp = do_get(url)
    slept = 0.0
    for attempt in range(max_attempts):
        if resp is None:
            break
        status = getattr(resp, "status_code", 0) or 0
        if status not in retry_statuses:
            break
        if slept >= sleep_cap:
            break
        delay = base * (factor ** attempt)
        ra = _retry_after_seconds(resp)
        if ra is not None:
            delay = ra
        delay = min(delay, sleep_cap - slept)
        time.sleep(delay)
        slept += delay
        resp = do_get(url)
    return resp
