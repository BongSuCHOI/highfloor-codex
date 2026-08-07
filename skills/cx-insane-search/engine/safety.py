"""SSRF guard and DNS pinning data for the agent-facing fetcher.

Every curl sink must resolve through :func:`resolve_public_target`, fail closed,
and pin the returned addresses into the actual connection. Redirect hops are
resolved independently by the transport.
"""
from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass
from urllib.parse import urljoin, urlsplit, urlunsplit

ALLOWED_SCHEMES = {"http", "https"}
DEFAULT_MAX_REDIRECTS = 10


def allow_private_default() -> bool:
    """Compatibility helper: production fetches never permit private targets."""
    return False


def _ip_blocked(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return True
    mapped = getattr(ip, "ipv4_mapped", None)
    if mapped is not None:
        ip = mapped
    # ``ipaddress.is_global`` describes reachability, not safe public-unicast
    # eligibility: Python classifies multicast ranges such as 224.0.0.0/4 and
    # ff00::/8 as global. They are never valid agent-facing fetch targets.
    return not ip.is_global or ip.is_multicast


@dataclass(frozen=True)
class ResolvedTarget:
    scheme: str
    host: str
    port: int
    ips: tuple[str, ...]
    request_url: str
    ip_literal: bool = False

    def curl_resolve_entries(self) -> list[str]:
        """Return CURLOPT_RESOLVE entries that bind this host to checked IPs."""
        if self.ip_literal:
            return []
        addresses = [f"[{ip}]" if ":" in ip else ip for ip in self.ips]
        return [f"{self.host}:{self.port}:{','.join(addresses)}"]


def resolve_public_target(
    url: str,
    allow_private: bool = False,
) -> tuple[ResolvedTarget | None, str]:
    """Resolve an HTTP(S) URL and reject every non-global result.

    ``allow_private`` exists only for pure classifier tests. Public fetch paths
    never pass it through.
    """
    try:
        parsed = urlsplit(url)
    except Exception as exc:
        return None, f"parse_error:{type(exc).__name__}"

    scheme = parsed.scheme.lower()
    if scheme not in ALLOWED_SCHEMES:
        return None, f"scheme:{scheme or 'none'}"
    if parsed.username is not None or parsed.password is not None:
        return None, "userinfo_not_allowed"

    raw_host = parsed.hostname
    if not raw_host:
        return None, "no_host"
    if "%" in raw_host:
        return None, "scoped_host_not_allowed"
    try:
        host = raw_host.rstrip(".").encode("idna").decode("ascii").lower()
    except (UnicodeError, ValueError):
        return None, "invalid_host"
    if not host:
        return None, "no_host"
    try:
        port = parsed.port or (443 if scheme == "https" else 80)
    except ValueError:
        return None, "invalid_port"

    try:
        literal = ipaddress.ip_address(host)
    except ValueError:
        literal = None
    url_host = f"[{host}]" if literal is not None and literal.version == 6 else host
    default_port = 443 if scheme == "https" else 80
    netloc = url_host if port == default_port else f"{url_host}:{port}"
    request_url = urlunsplit((scheme, netloc, parsed.path, parsed.query, ""))
    if literal is not None:
        ip = str(literal)
        if not allow_private and _ip_blocked(ip):
            return None, f"ip_blocked:{ip}"
        return ResolvedTarget(
            scheme, host, port, (ip,), request_url, ip_literal=True
        ), (
            "allow_private" if allow_private else "public_ip"
        )

    try:
        infos = socket.getaddrinfo(
            host,
            port,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
    except Exception as exc:
        return None, f"resolve_failed:{type(exc).__name__}"
    resolved_ips: set[str] = set()
    for info in infos:
        if not info[4]:
            continue
        raw_ip = str(info[4][0]).split("%", 1)[0]
        try:
            resolved_ips.add(str(ipaddress.ip_address(raw_ip)))
        except ValueError:
            return None, f"resolve_invalid_ip:{raw_ip}"
    ips = tuple(sorted(resolved_ips))
    if not ips:
        return None, "resolve_empty"
    if not allow_private:
        blocked = [ip for ip in ips if _ip_blocked(ip)]
        if blocked:
            return None, f"resolves_non_global:{host}->{blocked[0]}"
    return ResolvedTarget(scheme, host, port, ips, request_url), (
        "allow_private" if allow_private else "public"
    )


def classify_url(url: str, allow_private: bool = False) -> tuple[bool, str]:
    """Return ``(is_safe, reason)`` using the same fail-closed resolver."""
    target, reason = resolve_public_target(url, allow_private=allow_private)
    return target is not None, reason


def location_of(resp) -> str | None:
    """Case-insensitive Location header from a curl_cffi/requests response."""
    try:
        headers = {k.lower(): v for k, v in dict(getattr(resp, "headers", {}) or {}).items()}
        return headers.get("location")
    except Exception:
        return None


def is_redirect(resp) -> bool:
    try:
        return int(getattr(resp, "status_code", 0) or 0) in (301, 302, 303, 307, 308)
    except Exception:
        return False


def resolve_redirect(base_url: str, location: str) -> str:
    return urljoin(base_url, location)
