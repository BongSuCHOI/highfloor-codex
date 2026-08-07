"""Opt-in, bounded route-learning store.

Records which fetch route (impersonate × referer × url-transform × phase) last
SUCCEEDED for a host, so the next visit promotes it to the probe / front of the
grid instead of rediscovering it from scratch. The store is bounded and
self-pruning so it can never grow without limit:

  * eviction on failure — a learned route that fails on a REAL block
    (`exhausted` / `challenge` / `blocked`) earns a strike; after
    ``EVICT_AFTER_FAILS`` consecutive real failures the entry is deleted.
    Transient outcomes (429 rate-limit, network/unknown error, budget cut) and
    URL-level outcomes (404/401) never strike — they are not the route's fault.
  * TTL — an entry unused for ``TTL_DAYS`` is pruned the next time the store is
    loaded (default 30 days).
  * cap — at most ``MAX_ENTRIES`` (default 500); on overflow the
    least-recently-used entries are dropped.

Persistent learning is disabled by default. When explicitly enabled, hostnames
are stored as non-secret hashes and the file is written with mode ``0600``.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone, timedelta
from typing import Optional
from urllib.parse import urlsplit

SCHEMA_VERSION = 1
TTL_DAYS = int(os.environ.get("INSANE_LEARN_TTL_DAYS", "30"))
MAX_ENTRIES = int(os.environ.get("INSANE_LEARN_MAX", "500"))
EVICT_AFTER_FAILS = 2

# stop_reason values that mean the access ROUTE genuinely failed (→ strike).
# Everything else (rate_limited / unknown / budget / auth_required / not_found /
# success / "") is transient or URL-level and never strikes the route.
PENALIZE_REASONS = frozenset({"exhausted", "challenge", "blocked"})


def enabled() -> bool:
    return os.environ.get("INSANE_LEARN", "0").lower() in ("1", "true", "yes")


def default_path() -> str:
    p = os.environ.get("INSANE_LEARNED_PATH")
    if p:
        return p
    return os.path.join(os.path.expanduser("~"), ".insane_search", "learned.json")


def is_real_failure(stop_reason: str) -> bool:
    """True when `stop_reason` means the route itself was blocked (→ strike)."""
    return (stop_reason or "") in PENALIZE_REASONS


def key_for(url: str, device_class: str) -> str:
    host = (urlsplit(url).hostname or "").lower()
    dev = "mobile" if device_class == "mobile" else "desktop"
    digest = hashlib.sha256(host.encode("utf-8", "ignore")).hexdigest()
    return f"h1:{digest}::{dev}"


def _normalize_store_key(key: str) -> str:
    if key.startswith("h1:"):
        return key
    host, separator, device = key.rpartition("::")
    if not separator:
        host, device = key, "desktop"
    digest = hashlib.sha256(host.lower().encode("utf-8", "ignore")).hexdigest()
    normalized_device = "mobile" if device == "mobile" else "desktop"
    return f"h1:{digest}::{normalized_device}"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _parse(ts: str) -> Optional[datetime]:
    try:
        dt = datetime.fromisoformat(ts)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def _prune(data: dict, now: Optional[datetime] = None) -> dict:
    """Drop TTL-expired entries, then enforce the LRU cap. Pure (in-memory)."""
    now = now or _now()
    cutoff = now - timedelta(days=TTL_DAYS)
    kept = {}
    for k, v in data.items():
        lu = _parse(v.get("last_used", "")) if isinstance(v, dict) else None
        if lu is None or lu >= cutoff:
            kept[k] = v
    if len(kept) > MAX_ENTRIES:
        # keep the MAX_ENTRIES most-recently-used
        ordered = sorted(
            kept.items(),
            key=lambda kv: _parse(kv[1].get("last_used", "")) or now,
            reverse=True,
        )
        kept = dict(ordered[:MAX_ENTRIES])
    return kept


def load(path: Optional[str] = None) -> dict:
    """Load the store, pruning TTL-expired + over-cap entries in memory.

    Pruning is not persisted here (write-on-read is wasteful); the next
    `record_*` save writes the pruned set back, so the file converges."""
    path = path or default_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if not isinstance(raw, dict):
            return {}
        if "schema_version" in raw and raw.get("schema_version") != SCHEMA_VERSION:
            return {}
        if raw.get("schema_version") == SCHEMA_VERSION:
            entries = raw.get("entries")
            if not isinstance(entries, dict):
                return {}
            data = entries
        else:
            data = raw
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    normalized = {
        _normalize_store_key(str(key)): value
        for key, value in data.items()
        if isinstance(value, dict)
    }
    return _prune(normalized)


def save(data: dict, path: Optional[str] = None) -> Optional[str]:
    using_default_path = path is None and not os.environ.get("INSANE_LEARNED_PATH")
    path = path or default_path()
    temp_path = ""
    try:
        directory = os.path.dirname(path) or "."
        os.makedirs(directory, mode=0o700, exist_ok=True)
        if using_default_path:
            os.chmod(directory, 0o700)
        normalized = {
            _normalize_store_key(str(key)): value
            for key, value in data.items()
            if isinstance(value, dict)
        }
        fd, temp_path = tempfile.mkstemp(prefix=".learned.", dir=directory, text=True)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(
                {"schema_version": SCHEMA_VERSION, "entries": normalized},
                handle,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        os.chmod(temp_path, 0o600)
        os.replace(temp_path, path)
        temp_path = ""
        os.chmod(path, 0o600)
        return None
    except OSError as exc:
        if temp_path:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
        return f"persistent learning save failed:{type(exc).__name__}"


def lookup(url: str, device_class: str, path: Optional[str] = None,
           data: Optional[dict] = None) -> Optional[dict]:
    """Return the learned route dict for this host, or None."""
    data = load(path) if data is None else data
    entry = data.get(key_for(url, device_class))
    if isinstance(entry, dict):
        route = entry.get("route")
        if isinstance(route, dict):
            return route
    return None


def record_success(url: str, device_class: str, route: dict,
                   path: Optional[str] = None) -> Optional[str]:
    """Upsert the winning route for this host (resets the failure strike)."""
    data = load(path)
    k = key_for(url, device_class)
    now = _now().isoformat()
    raw = data.get(k)
    entry = raw if isinstance(raw, dict) else {}
    same = entry.get("route") == route
    data[k] = {
        "route": route,
        "wins": int(entry.get("wins", 0)) + 1 if same else 1,
        "consecutive_fails": 0,
        "last_used": now,
        "last_success": now,
    }
    return save(_prune(data), path)


def record_failure(url: str, device_class: str, penalize: bool,
                   path: Optional[str] = None) -> Optional[str]:
    """Record that the learned route did not win this run.

    `penalize=True` (a real block) strikes the entry and deletes it after
    EVICT_AFTER_FAILS consecutive strikes. `penalize=False` (transient / URL
    issue) just refreshes `last_used` so an actively-retried host is not
    TTL-pruned. No-op when nothing was learned for this host."""
    data = load(path)
    k = key_for(url, device_class)
    entry = data.get(k)
    if not isinstance(entry, dict):
        return None
    if penalize:
        entry["consecutive_fails"] = int(entry.get("consecutive_fails", 0)) + 1
        entry["last_used"] = _now().isoformat()
        if entry["consecutive_fails"] >= EVICT_AFTER_FAILS:
            del data[k]
    else:
        entry["last_used"] = _now().isoformat()
    return save(_prune(data), path)
