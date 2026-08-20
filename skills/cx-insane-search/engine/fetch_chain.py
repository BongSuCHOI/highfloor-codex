"""Single entrypoint: insane-search generic fetch chain.

    from engine import fetch
    result = fetch("https://example.com/path", success_selectors=["article"])

Public contract:
  * One function: `fetch(url, ...) -> FetchResult`.
  * Internal structure preserved as explicit phases so tests & debug logs
    can target each stage: probe → validate → detect → plan → execute → report.
  * `FetchResult.trace` exposes every attempt (transform × impersonate ×
    referer × executor) — callers can diagnose without re-running.

v2 scheduler (multi-AI review 2026-06-21):
  * `_build_plan` materializes the whole grid then orders it for DIVERSITY —
    one representative per TLS family across both URL transforms first, so a
    small attempt budget still touches every family/transform instead of
    burning out on the Safari family.
  * `tls_impersonate_avoid` entries are DEPRIORITIZED (moved last), never
    deleted — they are still attempted in exhaustive mode.
  * `max_attempts=None` (new default) means EXHAUSTIVE — run the full plan,
    honouring R6. A numeric cap is a *budget*, and exhaustion vs budget vs
    early-terminal is reported via `stop_reason` / `grid_exhausted`.
  * Jitter sleeps only on a CONTINUING (failed) attempt, never before a
    successful return.
  * `SUSPECT_OK` (abck unresolved / soft block) is NON-terminal: kept as
    best-effort, but the grid keeps searching for real proof.

No site-specific branching. Site knowledge enters only via:
  * `success_selectors` (caller-supplied positive proof)
  * `user_hint` (optional runtime hints; never persisted by this module)
"""
from __future__ import annotations

import os
import random
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Optional

from .content_safety import ContentSafetyReport, analyze_untrusted_content, wrap_untrusted_content
from .validators import Verdict, validate, TERMINAL_NONSUCCESS
from .waf_detector import detect, load_profile, _load_profiles, last_load_error
from .url_transforms import iter_transformed


_OK_VALUES = (Verdict.STRONG_OK.value, Verdict.WEAK_OK.value)
_TERMINAL_NONSUCCESS_VALUES = frozenset(v.value for v in TERMINAL_NONSUCCESS)


# --- Referer strategies (name → function of original URL) --------------------
def _self_root(url: str) -> str:
    from urllib.parse import urlsplit
    p = urlsplit(url)
    return f"{p.scheme}://{p.netloc}/"


REFERER_STRATEGIES = {
    "self_root": _self_root,
    "google_search": lambda _url: "https://www.google.com/",
    "none": lambda _url: "",
}


# --- Attempt & result schema -------------------------------------------------
@dataclass
class Attempt:
    phase: str                       # probe | grid | fallback
    executor: str                    # curl_cffi | playwright_real_chrome | ...
    url: str
    url_transform: str               # original | mobile_subdomain | ...
    impersonate: Optional[str]       # safari | chrome | ... | None (non-curl)
    referer: str
    status: int = 0
    body_size: int = 0
    verdict: str = ""
    reasons: list[str] = field(default_factory=list)
    elapsed_s: float = 0.0
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class FetchResult:
    ok: bool
    content: str = ""
    requested_url: str = ""
    final_url: str = ""
    retrieved_at: str = ""
    verdict: str = ""
    profile_used: Optional[str] = None
    trace: list[Attempt] = field(default_factory=list)
    summary: str = ""
    # v2 scheduler diagnostics
    planned_attempts: int = 0
    executed_attempts: int = 0
    grid_exhausted: bool = False
    stop_reason: str = ""            # success | exhausted | budget | <terminal verdict> | error
    # Failure gate (R6): when ok=False these tell the caller it is NOT finished —
    # which escalation routes the engine could not perform itself remain to try.
    untried_routes: list[str] = field(default_factory=list)
    # Compatibility field for existing JSON consumers. New host-facing code
    # should use the neutral `must_invoke_browser_automation` property.
    must_invoke_playwright_mcp: bool = False
    content_trust: str = ""
    prompt_injection_risk: str = ""
    prompt_injection_signals: list[str] = field(default_factory=list)
    untrusted_content_boundary: dict[str, str] = field(default_factory=dict)
    # Content-rescue metadata: `content` stays the raw fetched text unless a
    # rescue path fired — PDF bodies become pypdf-extracted text, SPA shells
    # whose visible text is thinner than their JSON-LD articleBody get the
    # articleBody, and a Playwright render can contribute its innerText
    # (render-merge). `extraction_source` says which path produced `content`
    # (raw | pdf | json_ld | raw_disabled | *+inner_text | ...).
    extraction_quality: float = 0.0
    extraction_source: str = ""
    extraction_meta: dict = field(default_factory=dict)
    retrieval_phase: str = ""
    retrieval_executor: str = ""
    limitations: list[str] = field(default_factory=list)
    runtime_warnings: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        report = analyze_untrusted_content(self.content, source_url=self.final_url)
        if not self.content_trust:
            self.content_trust = report.content_trust
        if not self.prompt_injection_risk:
            self.prompt_injection_risk = report.prompt_injection_risk
        if not self.prompt_injection_signals:
            self.prompt_injection_signals = list(report.prompt_injection_signals)
        if not self.untrusted_content_boundary:
            self.untrusted_content_boundary = dict(report.untrusted_content_boundary)

    def to_untrusted_text(self) -> str:
        report = ContentSafetyReport(
            content_trust=self.content_trust,
            prompt_injection_risk=self.prompt_injection_risk,
            prompt_injection_signals=list(self.prompt_injection_signals),
            untrusted_content_boundary={
                "begin": self.untrusted_content_boundary["begin"],
                "end": self.untrusted_content_boundary["end"],
            },
        )
        return wrap_untrusted_content(self.content, report=report, source_url=self.final_url)

    @property
    def must_invoke_browser_automation(self) -> bool:
        return self.must_invoke_playwright_mcp

    def to_evidence_dict(self) -> dict:
        """Retrieval-only metadata for a research source record."""
        content_role = (
            "diagnostic_only"
            if not self.ok
            else (
                "candidate_with_limitations"
                if self.verdict == Verdict.WEAK_OK.value
                else "published_source_candidate"
            )
        )
        completeness = (
            self.extraction_quality
            if (
                self.extraction_source
                and self.extraction_meta.get("completeness_measured") is not False
            )
            else None
        )
        return {
            "schema_version": 1,
            "requested_url": self.requested_url,
            "final_url": self.final_url,
            "retrieved_at": self.retrieved_at,
            "ok": self.ok,
            "content_role": content_role,
            "retrieval_verdict": self.verdict,
            "stop_reason": self.stop_reason,
            "untried_routes": list(self.untried_routes),
            "retrieval_route": {
                "phase": self.retrieval_phase,
                "executor": self.retrieval_executor,
                "fallback_used": self.retrieval_phase == "fallback",
                "profile_used": self.profile_used,
            },
            "extraction": {
                "method": self.extraction_source,
                "completeness_heuristic": completeness,
                "limitations": list(self.limitations),
            },
            "content_trust": self.content_trust,
            "prompt_injection_risk": self.prompt_injection_risk,
            "source_quality": "not_evaluated",
            "claim_confidence": "not_evaluated",
            "runtime_warnings": list(self.runtime_warnings),
        }

    def to_dict(self, *, include_content: bool = False) -> dict:
        payload = {
            "ok": self.ok,
            "requested_url": self.requested_url,
            "final_url": self.final_url,
            "retrieved_at": self.retrieved_at,
            "verdict": self.verdict,
            "profile_used": self.profile_used,
            "trace": [a.to_dict() for a in self.trace],
            "summary": self.summary,
            "content_length": len(self.content),
            "planned_attempts": self.planned_attempts,
            "executed_attempts": self.executed_attempts,
            "grid_exhausted": self.grid_exhausted,
            "stop_reason": self.stop_reason,
            "untried_routes": self.untried_routes,
            "must_invoke_browser_automation": self.must_invoke_browser_automation,
            "must_invoke_playwright_mcp": self.must_invoke_playwright_mcp,
            "content_trust": self.content_trust,
            "prompt_injection_risk": self.prompt_injection_risk,
            "prompt_injection_signals": self.prompt_injection_signals,
            "untrusted_content_boundary": self.untrusted_content_boundary,
            "extraction_quality": self.extraction_quality,
            "extraction_source": self.extraction_source,
            "extraction_meta": self.extraction_meta,
            "retrieval_phase": self.retrieval_phase,
            "retrieval_executor": self.retrieval_executor,
            "limitations": self.limitations,
            "runtime_warnings": self.runtime_warnings,
            "evidence": self.to_evidence_dict(),
        }
        if include_content:
            payload["untrusted_content"] = self.to_untrusted_text()
        return payload

    def to_research_handoff_dict(self) -> dict:
        """Compact single-fetch payload for the ultraresearch composition."""
        return {
            "evidence": self.to_evidence_dict(),
            "untrusted_content": self.to_untrusted_text(),
        }


# --- Content rescue extraction -----------------------------------------------
# Deliberately narrow scope: the raw body REMAINS `content` for ordinary HTML
# successes. A rescue path replaces it only where the raw body is unusable for
# an LLM, and only when the rescue demonstrably carries MORE text than the raw
# body's visible text — the gate that keeps a teaser (JSON-LD description)
# from beating a full article:
#   * PDF bodies (magic bytes / content-type, re-guarded) → pypdf text
#   * SPA shells whose visible text is thinner than their JSON-LD articleBody
#   * Playwright render-merge: rendered innerText wins over a thinner body
# pypdf is an optional import; every path degrades to the raw text.
import io as _io
import json as _json
import re as _re

try:
    from pypdf import PdfReader as _PdfReader
except ImportError:
    _PdfReader = None

_JSONLD_MIN_CHARS = 100          # an articleBody shorter than this is a teaser
_INNER_TEXT_MIN_CHARS = 200      # innerText shorter than this never wins


def _quality_score(md: str) -> float:
    """Crude 0..1 extraction-quality heuristic: length + sentence density."""
    if not md:
        return 0.0
    length_s = min(len(md) / 3000.0, 1.0)
    sentences = len(_re.findall(r"[.!?。…]\s", md)) + 1
    words = max(len(md.split()), 1)
    struct_s = min(sentences / (words / 18.0 + 1), 1.0)
    return round(max(0.0, min(1.0, 0.6 * length_s + 0.4 * struct_s)), 2)


def _visible_text(html: str) -> str:
    """Body text after stripping script/style/markup — the length yardstick
    every rescue path must beat before it may replace the raw body."""
    t = _re.sub(r"(?is)<(script|style|noscript|svg|template)[^>]*>.*?</\1>", " ", html)
    t = _re.sub(r"(?s)<[^>]+>", " ", t)
    return _re.sub(r"\s+", " ", t).strip()


def _extract_json_ld_text(html: str) -> str:
    """Pull articleBody / description from <script type=application/ld+json>."""
    out: list[str] = []
    for m in _re.finditer(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            html, _re.I | _re.S):
        try:
            data = _json.loads(m.group(1))
            if isinstance(data, list):
                data = data[0] if data else {}
            if isinstance(data, dict):
                t = (data.get("@type") or "")
                if t in ("Article", "NewsArticle", "BlogPosting") or "articleBody" in data:
                    body = data.get("articleBody") or data.get("description") or ""
                    if body:
                        out.append(body)
        except Exception:
            pass
    return "\n\n".join(out)


def _extract_pdf(body: bytes, url: str) -> tuple[str, str, float, str]:
    """Returns (title, text, quality, error_code). error_code is "" on success.
    Caps at 80 pages to keep token budget sane; reports pdf_no_text_layer for
    scanned PDFs (so the caller knows rendering will not help either)."""
    if _PdfReader is None:
        return "", "", 0.0, "pypdf_missing"
    try:
        reader = _PdfReader(_io.BytesIO(body))
        title = ""
        try:
            if reader.metadata and reader.metadata.title:
                title = str(reader.metadata.title)[:300]
        except Exception:
            pass
        pages: list[str] = []
        for page in reader.pages[:80]:
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                pages.append("")
        text = "\n\n".join(p for p in pages if p).strip()
        if not text:
            return title, "", 0.0, "pdf_no_text_layer"
        return title, text, _quality_score(text), ""
    except Exception as e:
        return "", "", 0.0, f"pdf_error:{type(e).__name__}"


def _looks_like_pdf(resp, final_url: str) -> bool:
    """Detect PDF by magic bytes OR explicit content-type OR .pdf URL.
    Covers the case where a server serves a PDF with text/html content-type."""
    body = getattr(resp, "content", None)
    if isinstance(body, (bytes, bytearray)) and len(body) >= 5 and bytes(body[:5]) == b"%PDF-":
        return True
    try:
        ctype = (dict(getattr(resp, "headers", {}) or {}).get("content-type", "") or "").lower()
    except Exception:
        ctype = ""
    if "pdf" in ctype:
        return True
    return final_url.lower().split("?")[0].endswith(".pdf")


class _PWResp:
    """Minimal response shim so a Playwright fallback's HTML can run through
    the same rescue-extraction path as a curl response."""
    def __init__(self, text: str, url: str, headers: Optional[dict] = None):
        self.text = text
        self.content = text.encode("utf-8", "ignore") if text else b""
        self.url = url
        self.status_code = 200
        self.headers = headers or {"content-type": "text/html"}


def _extract_response(resp, final_url: str, inner_text: str = "") -> tuple[str, str, float, dict]:
    """Returns (title, content, quality, meta); meta = {source, error,
    inner_text_used}. The raw body wins by default — see the module-block
    comment for when a rescue path may replace it."""
    if _looks_like_pdf(resp, final_url):
        body = getattr(resp, "content", None)
        if isinstance(body, (bytes, bytearray)) and body:
            # Re-guard: a .pdf URL can serve plain HTML — only hand pypdf a
            # body that really is a PDF (magic bytes or explicit content-type).
            ctype_pdf = False
            try:
                ctype_pdf = "pdf" in (dict(getattr(resp, "headers", {}) or {})
                                      .get("content-type", "") or "").lower()
            except Exception:
                pass
            if bytes(body[:5]) == b"%PDF-" or ctype_pdf:
                title, text, quality, err = _extract_pdf(bytes(body), final_url)
                if text:
                    return title, text, quality, {"source": "pdf", "error": err or "",
                                                  "inner_text_used": False}
                return title, f"[PDF binary, {len(body)} bytes; extractor={err or 'ok'}]", \
                       0.0, {"source": "pdf", "error": err, "inner_text_used": False}

    text = getattr(resp, "text", "") or ""
    if not text:
        body = getattr(resp, "content", None)
        if isinstance(body, (bytes, bytearray)) and body:
            return "", f"[{len(body)} bytes; binary]", 0.0, \
                   {"source": "raw_binary", "error": "no_text_body", "inner_text_used": False}
        return "", "", 0.0, {"source": "empty", "error": "empty_body",
                             "inner_text_used": False}

    title = ""
    m = _re.search(r"<title[^>]*>(.*?)</title>", text, _re.I | _re.S)
    if m:
        title = _re.sub(r"\s+", " ", m.group(1)).strip()[:300]

    visible = _visible_text(text)
    content, source, quality = text, "raw", _quality_score(visible)

    jsonld = _extract_json_ld_text(text)
    if len(jsonld) > _JSONLD_MIN_CHARS and len(jsonld) > len(visible):
        content, source, quality = jsonld, "json_ld", _quality_score(jsonld)

    # Render-merge: compare innerText against the VISIBLE text length (not the
    # raw markup length — markup would always win the comparison and disable
    # the merge).
    inner = (inner_text or "").strip()
    chosen_len = len(visible) if source == "raw" else len(content)
    inner_used = False
    if inner and len(inner) > max(chosen_len, _INNER_TEXT_MIN_CHARS):
        content, quality = inner, _quality_score(inner)
        source = source + "+inner_text"
        inner_used = True
    return title, content, quality, {"source": source, "error": "",
                                     "inner_text_used": inner_used}


def _maybe_extract(resp, final_url: str, *, enable_extraction: bool,
                   inner_text: str = "") -> tuple[str, str, float, dict]:
    """Run rescue extraction when enabled; otherwise raw text + consistent meta."""
    if not enable_extraction:
        return "", getattr(resp, "text", "") or "", 0.0, \
               {"source": "raw_disabled", "error": "", "inner_text_used": False}
    return _extract_response(resp, final_url, inner_text=inner_text)


# --- curl_cffi probe executor ------------------------------------------------
def _curl_probe(
    url: str, *, impersonate: str, referer: str, timeout: int = 20,
    enable_retry: bool = False,
) -> tuple[Any, Optional[str]]:
    """Returns (response, error_str). response may be None on exception.

    Routes through the guarded SessionPool so checked DNS addresses are pinned
    into curl while cookies and warm connections can be reused for the same
    host, identity, and address set.
    """
    from .transport import POOL
    return POOL.request(url, impersonate=impersonate, referer=referer, timeout=timeout,
                        max_retries=2 if enable_retry else 0)


def _run_attempt(
    url: str,
    *,
    transform_name: str,
    impersonate: str,
    referer_name: str,
    success_selectors: Optional[list[str]],
    known_bad_sizes: Optional[list[int]],
    timeout: int,
    phase: str,
    enable_retry: bool = False,
) -> tuple[Attempt, Any]:
    """Execute one curl_cffi attempt and produce an Attempt record."""
    referer_url = REFERER_STRATEGIES.get(referer_name, REFERER_STRATEGIES["none"])(url)
    t0 = time.time()
    resp, err = _curl_probe(url, impersonate=impersonate, referer=referer_url, timeout=timeout,
                            enable_retry=enable_retry)
    elapsed = round(time.time() - t0, 3)

    att = Attempt(
        phase=phase,
        executor="curl_cffi",
        url=url,
        url_transform=transform_name,
        impersonate=impersonate,
        referer=referer_name,
        elapsed_s=elapsed,
    )

    if err or resp is None:
        att.error = err or "no response"
        att.verdict = Verdict.UNKNOWN.value
        return att, None

    vr = validate(resp, success_selectors=success_selectors, known_bad_sizes=known_bad_sizes)
    att.status = vr.status
    att.body_size = vr.body_size
    att.verdict = vr.verdict.value
    att.reasons = vr.reasons
    return att, resp


# --- Diversity planner -------------------------------------------------------
@dataclass(frozen=True)
class _Cand:
    profile_id: str
    transform: str
    url: str
    impersonate: str
    referer: str
    known_bad_sizes: Optional[tuple]


_FAMILIES = ("safari_ios", "safari", "chrome_android", "chrome", "edge", "firefox")


def _family(tls: str) -> str:
    for fam in _FAMILIES:
        if tls.startswith(fam):
            return fam
    return tls


def _is_mobile_tls(t: str) -> bool:
    return ("ios" in t) or ("android" in t)


def _plan_for_profile(
    url: str, profile_id: str, profile: dict, device_class: str
) -> list[_Cand]:
    from .transport import filter_available, select_available

    groups: list[list[str]] = [
        filter_available(list(group))
        for group in (
            profile.get("tls_impersonate_candidates")
            or [["safari", "chrome"]]
        )
    ]
    avoid = set(profile.get("tls_impersonate_avoid") or [])
    referer_order = list(profile.get("referer_strategies") or ["self_root"])
    transform_order = list(profile.get("url_transform_order") or ["original"])
    kb = profile.get("known_bad_sizes") or None
    known_bad = tuple(kb) if kb else None

    # device_class shaping (fixes desktop/mobile drift)
    if device_class == "mobile":
        groups = [[t for t in g if _is_mobile_tls(t)] for g in groups]
        for extra in ("mobile_subdomain", "am_prefix"):
            if extra not in transform_order:
                transform_order.append(extra)
    elif device_class == "desktop":
        groups = [[t for t in g if not _is_mobile_tls(t)] for g in groups]
        transform_order = [t for t in transform_order if t not in ("mobile_subdomain", "am_prefix")] or ["original"]

    # deprioritize (not delete) avoid targets within each family group
    def _reorder(g: list[str]) -> list[str]:
        return [t for t in g if t not in avoid] + [t for t in g if t in avoid]

    groups = [_reorder(g) for g in groups if g]
    if not groups:
        defaults = (
            ["safari_ios", "chrome_android", "chrome"]
            if device_class == "mobile"
            else ["safari", "chrome", "firefox"]
        )
        fallback = select_available(defaults)
        if fallback is None:
            return []
        groups = [[fallback]]

    transforms = iter_transformed(url, transform_order) or [("original", url)]

    # Diversity ordering: vary FAMILY fastest, then TRANSFORM, then version
    # DEPTH, then REFERER. A small budget thus touches every family/transform
    # before exhausting one family's old versions.
    max_depth = max(len(g) for g in groups)
    cands: list[_Cand] = []
    seen: set[tuple] = set()
    for ref in referer_order:
        for depth in range(max_depth):
            for (t_name, t_url) in transforms:
                for g in groups:
                    if depth >= len(g):
                        continue
                    imp = g[depth]
                    key = (t_url, imp, ref)
                    if key in seen:
                        continue
                    seen.add(key)
                    cands.append(_Cand(profile_id, t_name, t_url, imp, ref, known_bad))
    return cands


def _build_plan(
    url: str,
    hits: list,
    profiles: dict,
    device_class: str,
    probe_impersonate: str,
    probe_referer: str,
    priority: Optional[dict] = None,
) -> list[_Cand]:
    """Materialize a diversity-ordered candidate plan across the top profiles.

    Profiles are round-robin interleaved so a confident #1 profile cannot
    starve #2/#3. The probe combo is removed (already executed).

    `priority` (U5 self-learning): a previously-successful route
    ``{"transform","impersonate","referer"}`` for this host — the matching
    candidate is moved to the FRONT so a known-good route is retried first."""
    per: list[list[_Cand]] = []
    for hit in hits[:3]:
        pid = getattr(hit, "profile_id", None) or "unknown_challenge"
        prof = load_profile(pid, profiles=profiles)
        per.append(_plan_for_profile(url, pid, prof, device_class))

    probe_key = (url, probe_impersonate, probe_referer)
    merged: list[_Cand] = []
    seen: set[tuple] = set()
    i = 0
    while any(i < len(p) for p in per):
        for p in per:
            if i < len(p):
                c = p[i]
                key = (c.url, c.impersonate, c.referer)
                if key == probe_key or key in seen:
                    continue
                seen.add(key)
                merged.append(c)
        i += 1

    if priority:
        front = [c for c in merged if c.transform == priority.get("transform")
                 and c.impersonate == priority.get("impersonate")
                 and c.referer == priority.get("referer")]
        if front:
            rest = [c for c in merged if c not in front]
            merged = front + rest
    return merged


# --- Public entrypoint: self-learning wrapper (U5) ---------------------------
def _winning_route(result: FetchResult) -> Optional[dict]:
    """Extract the curl route that produced the OK result, from the trace.

    Only probe/grid curl wins are learnable: Phase 0 always runs first anyway,
    and a browser win carries no reusable curl identity."""
    for att in reversed(result.trace):
        if (att.verdict in _OK_VALUES and att.phase in ("probe", "grid")
                and att.executor == "curl_cffi" and att.impersonate):
            return {
                "transform": att.url_transform,
                "impersonate": att.impersonate,
                "referer": att.referer,
                "phase": att.phase,
            }
    return None


def _finalize_result(
    result: FetchResult,
    requested_url: str,
    runtime_warnings: Optional[list[str]] = None,
) -> FetchResult:
    result.requested_url = requested_url
    if not result.retrieved_at:
        result.retrieved_at = datetime.now(timezone.utc).isoformat()
    if runtime_warnings:
        result.runtime_warnings.extend(
            warning for warning in runtime_warnings if warning not in result.runtime_warnings
        )

    selected: Optional[Attempt] = None
    if result.ok:
        for attempt in reversed(result.trace):
            if attempt.verdict in _OK_VALUES:
                selected = attempt
                break
    if selected is None and result.trace:
        selected = result.trace[-1]
    if selected is not None:
        result.retrieval_phase = selected.phase
        result.retrieval_executor = selected.executor

    if result.verdict == Verdict.WEAK_OK.value:
        result.limitations.append("weak_ok requires inspection of the retrieved content")
    if not result.ok and result.untried_routes:
        result.limitations.append("reported retrieval routes remain untried")
    return result


def fetch(
    url: str,
    *,
    success_selectors: Optional[list[str]] = None,
    device_class: str = "auto",
    user_hint: Optional[dict] = None,
    timeout: int = 25,
    max_attempts: Optional[int] = None,
    max_browser_attempts: int = 2,
    enable_playwright: bool = False,
    enable_phase0: bool = True,
    enable_learning: Optional[bool] = None,
    enable_extraction: bool = True,
    enable_retry: bool = True,
) -> FetchResult:
    """Public entrypoint — the generic grid wrapped with per-host self-learning.

    1. Before fetching, look up the route that last succeeded for this host and
       promote it: it becomes the probe identity AND the front of the grid.
    2. After fetching, record the winning route; or, if a learned route was
       promoted and the run hit a REAL block, strike it (evicted after two
       consecutive strikes — see `learning.py`).

    Persistent learning is off by default. Enable it explicitly with
    ``enable_learning=True`` or ``INSANE_LEARN=1``. Storage failures remain
    non-fatal and are exposed through ``FetchResult.runtime_warnings``.

    Local Playwright subprocess fallback is disabled at this public boundary:
    its browser egress cannot guarantee the same DNS pinning as the guarded
    transport. Use the returned browser-automation handoff instead.

    ``enable_extraction`` (default True) turns on content-rescue extraction:
    PDF bodies come back as pypdf-extracted text, and thin SPA shells fall back
    to JSON-LD articleBody / rendered innerText. Ordinary HTML successes keep
    the raw body — check ``FetchResult.extraction_source`` ("raw" = untouched).

    ``enable_retry`` (default True) retries transient statuses (429/502/503/
    504) on the PROBE attempt with exponential backoff, honouring a numeric
    ``Retry-After``. Grid attempts never retry — a failing grid must not
    multiply sleeps across dozens of candidates."""
    priority: Optional[dict] = None
    learned_existed = False
    runtime_warnings: list[str] = []
    uh = dict(user_hint or {})
    learning_active = False
    try:
        from . import learning
        learning_active = (
            learning.enabled() if enable_learning is None else enable_learning
        )
        if learning_active:
            priority = learning.lookup(url, device_class)
            if priority:
                learned_existed = True
                uh.setdefault("impersonate_first", priority.get("impersonate"))
                uh.setdefault("referer_strategy", priority.get("referer"))
    except Exception:
        priority = None

    if enable_playwright:
        runtime_warnings.append(
            "local Playwright fallback was disabled; use the browser-automation handoff"
        )
    result = _fetch_core(
        url, success_selectors=success_selectors, device_class=device_class,
        user_hint=uh, timeout=timeout, max_attempts=max_attempts,
        max_browser_attempts=max_browser_attempts,
        enable_playwright=False, enable_phase0=enable_phase0,
        priority=priority,
        enable_extraction=enable_extraction, enable_retry=enable_retry,
    )

    try:
        from . import learning
        if learning_active:
            warning = None
            if result.ok:
                win = _winning_route(result)
                if win:
                    warning = learning.record_success(url, device_class, win)
            elif learned_existed:
                warning = learning.record_failure(
                    url, device_class,
                    penalize=learning.is_real_failure(result.stop_reason))
            if warning:
                runtime_warnings.append(warning)
    except Exception:
        runtime_warnings.append("persistent learning update failed")

    return _finalize_result(result, url, runtime_warnings)


# --- Main entrypoint ---------------------------------------------------------
def _fetch_core(
    url: str,
    *,
    success_selectors: Optional[list[str]] = None,
    device_class: str = "auto",      # "auto" | "desktop" | "mobile"
    user_hint: Optional[dict] = None,
    timeout: int = 25,
    max_attempts: Optional[int] = None,   # None = exhaustive (R6); int = budget
    max_browser_attempts: int = 2,
    enable_playwright: bool = False,
    enable_phase0: bool = True,
    priority: Optional[dict] = None,      # U5: learned route to retry first
    enable_extraction: bool = True,
    enable_retry: bool = True,
) -> FetchResult:
    """Fetch `url` using the generic diversity grid.

    max_attempts
        None (default) → run the whole plan (exhaustive, honours R6).
        int → TOTAL curl-attempt budget (probe included). On budget exit the
        result reports `stop_reason="budget"`, `grid_exhausted=False`, so
        callers never mistake a truncated run for a true exhaustive failure.
    """
    user_hint = user_hint or {}
    profiles = _load_profiles()
    trace: list[Attempt] = []
    last_resp = None
    last_attempt: Optional[Attempt] = None
    best_suspect: Optional[tuple] = None   # (resp, attempt)
    profile_used: Optional[str] = None

    _jmin = int(os.environ.get("INSANE_JITTER_MS_MIN", "150"))
    _jmax = int(os.environ.get("INSANE_JITTER_MS_MAX", "400"))

    def _jitter():
        time.sleep(random.uniform(_jmin / 1000.0, _jmax / 1000.0))

    # Surface profile-loader failures as a diagnostic trace entry (not counted
    # as a network attempt).
    load_err = last_load_error()
    if load_err:
        trace.append(Attempt(
            phase="probe", executor="profile_loader", url=url,
            url_transform="original", impersonate=None, referer="",
            verdict=Verdict.UNKNOWN.value, error=f"profiles_fallback: {load_err}",
        ))

    # -------- Phase 0: official public-API router (R5; site-aware, sanctioned) --
    # For recognised platforms (Reddit/X/YouTube/...) try the official no-auth
    # endpoint BEFORE the generic grid. This is the *enforced* version of the
    # old agent-driven SKILL snippets — the agent can no longer skip it, which
    # is what made Reddit/X look "blocked" (grid 403'd .json; nobody tried .rss).
    if enable_phase0:
        try:
            from .phase0 import route as _phase0_route
            p0 = _phase0_route(url, timeout=timeout)
        except Exception as e:  # router must never break the generic chain
            p0 = None
            trace.append(Attempt(
                phase="phase0", executor="phase0", url=url, url_transform="original",
                impersonate=None, referer="", verdict=Verdict.UNKNOWN.value,
                error=f"{type(e).__name__}:{str(e)[:120]}",
            ))
        if p0 is not None:
            for a in p0["attempts"]:
                trace.append(Attempt(
                    phase="phase0", executor=a["route"], url=url, url_transform="-",
                    impersonate=None, referer="",
                    status=a.get("status", 0), body_size=a.get("bytes", 0),
                    verdict=(Verdict.STRONG_OK.value if a["ok"] else Verdict.BLOCKED.value),
                    reasons=[a["note"]] if a.get("note") else [],
                ))
            if p0["ok"]:
                phase0_method = (
                    "yt_dlp_metadata"
                    if p0["route"] == "yt-dlp"
                    else f"phase0_{str(p0['route']).replace('-', '_')}"
                )
                return FetchResult(
                    ok=True, content=p0["content"], final_url=p0["final_url"],
                    verdict=Verdict.STRONG_OK.value,
                    profile_used=f"phase0:{p0['platform']}", trace=trace,
                    summary=f"Phase 0 official route: {p0['platform']}:{p0['route']}",
                    stop_reason="success",
                    extraction_source=phase0_method,
                    extraction_quality=0.0,
                    extraction_meta={"completeness_measured": False},
                    limitations=[
                        "Phase 0 did not measure extraction completeness"
                    ],
                )
            # Recognised platform but every official route failed → fall through
            # to the generic grid (don't give up; R6).

    # -------- Phase 1: probe -------------------------------------------------
    base_impersonate = user_hint.get("impersonate_first") or (
        "safari_ios" if device_class == "mobile" else "safari")
    from .transport import select_available
    supported_impersonate = select_available(
        [base_impersonate, "chrome", "safari", "firefox"]
    )
    if supported_impersonate is not None:
        base_impersonate = supported_impersonate
    base_referer = user_hint.get("referer_strategy") or "self_root"

    # Root warmup (deep URLs only): let a WAF sensor set a resolved cookie on
    # the probe identity's session before the deep request — the classic
    # first-hit rejection fix. Skipped when the target already IS the root.
    try:
        from .transport import POOL, pool_enabled, _host_of, _root_of
        if pool_enabled():
            _root = _root_of(url)
            if _root != url:
                POOL.warmup(_host_of(url), base_impersonate, _root, timeout=min(timeout, 15))
    except Exception:
        pass

    curl_attempts = 0
    # Transient-status retry fires on the PROBE only: retrying each of the
    # dozens of grid candidates as well would multiply backoff sleeps into a
    # tens-of-seconds failure path.
    probe_attempt, probe_resp = _run_attempt(
        url, transform_name="original", impersonate=base_impersonate,
        referer_name=base_referer, success_selectors=success_selectors,
        known_bad_sizes=None, timeout=timeout, phase="probe",
        enable_retry=enable_retry,
    )
    trace.append(probe_attempt)
    curl_attempts += 1
    if probe_resp is not None:
        last_resp, last_attempt = probe_resp, probe_attempt
        if probe_attempt.verdict in _OK_VALUES:
            return _build_result(probe_resp, probe_attempt, trace, profile_used=None,
                                 planned=0, executed=curl_attempts,
                                 grid_exhausted=False, stop_reason="success",
                                 enable_extraction=enable_extraction)
        if probe_attempt.verdict == Verdict.SUSPECT_OK.value:
            best_suspect = (probe_resp, probe_attempt)
        elif probe_attempt.verdict in _TERMINAL_NONSUCCESS_VALUES:
            return _give_up(trace, profile_used, last_resp, last_attempt, best_suspect,
                            planned=0, executed=curl_attempts, grid_exhausted=False,
                            stop_reason=probe_attempt.verdict)

    # -------- Phase 2: detect + plan + execute ------------------------------
    if last_resp is not None:
        hits = detect(last_resp, profiles=profiles)
    else:
        hits = [type("H", (), {"profile_id": "unknown_challenge", "confidence": 0.1,
                               "signals": ["no_probe_response"]})()]
    profile_used = hits[0].profile_id if hits else None

    plan = _build_plan(url, hits, profiles, device_class, base_impersonate,
                       base_referer, priority=priority)
    planned = len(plan)
    grid_exhausted = False
    stop_reason = ""

    for cand in plan:
        if max_attempts is not None and curl_attempts >= max_attempts:
            stop_reason = "budget"
            break
        att, resp = _run_attempt(
            cand.url, transform_name=cand.transform, impersonate=cand.impersonate,
            referer_name=cand.referer, success_selectors=success_selectors,
            known_bad_sizes=list(cand.known_bad_sizes) if cand.known_bad_sizes else None,
            timeout=timeout, phase="grid",
        )
        trace.append(att)
        curl_attempts += 1
        if resp is not None:
            last_resp, last_attempt = resp, att
            if att.verdict in _OK_VALUES:
                return _build_result(resp, att, trace, profile_used=cand.profile_id,
                                     planned=planned, executed=curl_attempts,
                                     grid_exhausted=False, stop_reason="success",
                                     enable_extraction=enable_extraction)
            if att.verdict == Verdict.SUSPECT_OK.value and best_suspect is None:
                best_suspect = (resp, att)
            if att.verdict in _TERMINAL_NONSUCCESS_VALUES:
                stop_reason = att.verdict
                break
        # continuing → polite jitter (only on non-terminal failure)
        _jitter()
    else:
        grid_exhausted = True
        stop_reason = "exhausted"

    # If a terminal-nonsuccess (404/auth/429) stopped us, browser won't help.
    skip_browser = stop_reason in _TERMINAL_NONSUCCESS_VALUES

    # -------- Phase 3: Playwright fallback ----------------------------------
    if enable_playwright and not skip_browser:
        browser_used = 0
        try:
            from .executor import run_playwright_fallback
            fb_profile = load_profile(profile_used or "unknown_challenge", profiles=profiles)
            fb_order = fb_profile.get("fallback_when_challenge") or ["playwright_real_chrome"]
            for fb_name in fb_order:
                if fb_name == "curl_grid_exhaust":
                    continue
                if browser_used >= max_browser_attempts:
                    break
                pw_attempt, pw_content = run_playwright_fallback(
                    url, profile_id=profile_used or "unknown_challenge",
                    success_selectors=success_selectors, device_class=device_class,
                    force_executor=fb_name, timeout=timeout if timeout and timeout > 30 else 90,
                )
                trace.append(pw_attempt)
                browser_used += 1
                if pw_attempt.verdict in _OK_VALUES:
                    # Render-merge: the executor stashes the rendered innerText
                    # on the attempt; the rescue gate keeps whichever of
                    # (visible body text, innerText) carries more text.
                    pw_inner = getattr(pw_attempt, "_inner_text", "") or ""
                    _t, pw_out, pw_q, pw_meta = _maybe_extract(
                        _PWResp(pw_content, pw_attempt.url), pw_attempt.url,
                        enable_extraction=enable_extraction, inner_text=pw_inner)
                    return FetchResult(
                        ok=True, content=pw_out, final_url=pw_attempt.url,
                        verdict=pw_attempt.verdict, profile_used=profile_used,
                        trace=trace,
                        summary=f"Playwright fallback succeeded via {fb_name} "
                                f"(content={pw_meta.get('source')}, q={pw_q})",
                        planned_attempts=planned, executed_attempts=curl_attempts,
                        grid_exhausted=grid_exhausted, stop_reason="success",
                        extraction_quality=pw_q,
                        extraction_source=pw_meta.get("source", ""),
                        extraction_meta=pw_meta,
                    )
                if pw_attempt.verdict == Verdict.SUSPECT_OK.value and best_suspect is None:
                    best_suspect = (None, pw_attempt)
        except ImportError:
            trace.append(Attempt(
                phase="fallback", executor="playwright", url=url,
                url_transform="original", impersonate=None, referer="",
                verdict=Verdict.UNKNOWN.value, error="executor module not available"))
        except Exception as e:
            trace.append(Attempt(
                phase="fallback", executor="playwright", url=url,
                url_transform="original", impersonate=None, referer="",
                verdict=Verdict.UNKNOWN.value, error=f"{type(e).__name__}:{str(e)[:200]}"))

    # -------- Give up, return best we have ----------------------------------
    return _give_up(trace, profile_used, last_resp, last_attempt, best_suspect,
                    planned=planned, executed=curl_attempts,
                    grid_exhausted=grid_exhausted, stop_reason=stop_reason or "exhausted")


def _untried_routes(stop_reason, grid_exhausted) -> tuple[list[str], bool]:
    """Failure gate (R6): name the escalation routes the engine itself could not
    perform, so the caller never mistakes give-up for "everything was tried".

    Returns (untried_routes, must_invoke_browser_automation).
    """
    routes: list[str] = []
    # 429 is TRANSIENT, not a wall — exclude it from terminal so the gate still
    # surfaces backoff/MCP instead of telling the agent to give up (the exact
    # premature-failure this hardening exists to prevent).
    rate_limited = stop_reason == Verdict.RATE_LIMITED.value
    # Terminal non-success (404 / auth / paywall) → a real wall; nothing else helps.
    terminal = stop_reason in _TERMINAL_NONSUCCESS_VALUES and not rate_limited
    if terminal:
        return routes, False

    if rate_limited:
        routes.append("rate-limited (429) — transient: back off a few seconds then retry; a different TLS family or Playwright MCP often clears it. Do NOT hammer the grid.")
    # Budget cut → the curl grid itself was not finished (skip for 429: don't hammer).
    elif stop_reason == "budget" or not grid_exhausted:
        routes.append("generic-grid: NOT exhausted — re-run fetch() with max_attempts=None")

    # A gated page that survived the curl grid → the real browser is the next
    # escalation, and Playwright MCP must be driven from the AGENT session
    # (the engine can only spawn local Node Chrome, which Cloudflare-class
    # challenges often detect). So MCP is, by construction, an untried route here.
    must_mcp = True
    routes.append(
        "playwright_mcp (run from the agent session): browser_navigate → "
        "browser_network_requests → catch /api,/graphql,*.json internal endpoint → "
        "re-fetch that API URL with the bundled `scripts/run.sh`; or use browser_snapshot for rendered HTML"
    )
    routes.append("user_hint retry: fetch(url, user_hint={'impersonate_first': 'safari_ios'|'chrome', 'referer_strategy': 'none'}) and/or device_class='mobile'")
    return routes, must_mcp


def _give_up(trace, profile_used, last_resp, last_attempt, best_suspect,
             *, planned, executed, grid_exhausted, stop_reason) -> FetchResult:
    """Return the most honest failure result, preferring suspect content."""
    untried, must_mcp = _untried_routes(stop_reason, grid_exhausted)
    if best_suspect is not None:
        s_resp, s_att = best_suspect
        content = getattr(s_resp, "text", "") if s_resp is not None else ""
        return FetchResult(
            ok=False, content=content or "",
            final_url=str(getattr(s_resp, "url", s_att.url)) if s_resp is not None else s_att.url,
            verdict=s_att.verdict, profile_used=profile_used, trace=trace,
            summary=_format_summary(trace, profile_used, stop_reason),
            planned_attempts=planned, executed_attempts=executed,
            grid_exhausted=grid_exhausted, stop_reason=stop_reason,
            untried_routes=untried, must_invoke_playwright_mcp=must_mcp,
        )
    return FetchResult(
        ok=False,
        content=getattr(last_resp, "text", "") if last_resp is not None else "",
        final_url=str(getattr(last_resp, "url", url_of(last_attempt))) if last_resp is not None else url_of(last_attempt),
        verdict=last_attempt.verdict if last_attempt else Verdict.UNKNOWN.value,
        profile_used=profile_used, trace=trace,
        summary=_format_summary(trace, profile_used, stop_reason),
        planned_attempts=planned, executed_attempts=executed,
        grid_exhausted=grid_exhausted, stop_reason=stop_reason,
        untried_routes=untried, must_invoke_playwright_mcp=must_mcp,
    )


def url_of(attempt: Optional[Attempt]) -> str:
    return attempt.url if attempt else ""


def fetch_many(urls: list[str], **kwargs) -> list[FetchResult]:
    """Fetch many URLs, reusing the per-host SessionPool across calls.

    The first URL of a host may pay for warmup / browser bootstrap; later URLs
    of the SAME host reuse the winning session's cookies + connection, which is
    where R7-style bulk collection gets its throughput. Ordering by host keeps
    the warm session hot."""
    by_host: dict[str, list[int]] = {}
    for i, u in enumerate(urls):
        from .transport import _host_of
        by_host.setdefault(_host_of(u), []).append(i)
    results: list[Optional[FetchResult]] = [None] * len(urls)
    for _host, idxs in by_host.items():
        for i in idxs:
            results[i] = fetch(urls[i], **kwargs)
    return [r for r in results if r is not None]


def _build_result(resp, attempt: Attempt, trace: list[Attempt], profile_used: Optional[str],
                  *, planned: int, executed: int, grid_exhausted: bool, stop_reason: str,
                  enable_extraction: bool = True) -> FetchResult:
    final_url = str(getattr(resp, "url", attempt.url))
    _t, content, quality, meta = _maybe_extract(
        resp, final_url, enable_extraction=enable_extraction)
    return FetchResult(
        ok=True,
        content=content,
        final_url=final_url,
        verdict=attempt.verdict,
        profile_used=profile_used,
        trace=trace,
        summary=f"{attempt.executor} {attempt.impersonate} + {attempt.url_transform} + "
                f"referer:{attempt.referer} → {attempt.verdict} "
                f"(content={meta.get('source')}, q={quality})",
        planned_attempts=planned, executed_attempts=executed,
        grid_exhausted=grid_exhausted, stop_reason=stop_reason,
        extraction_quality=quality,
        extraction_source=meta.get("source", ""),
        extraction_meta=meta,
    )


# WAF profiles known to typically gate HTML but leave internal JSON APIs
# (relatively) open. R7 hint surfaces an API-first route.
_R7_ELIGIBLE_PROFILES = frozenset({
    "akamai_bot_manager", "cloudflare_turnstile", "datadome_probable",
    "perimeterx_human", "f5_big_ip", "aws_waf",
})

R7_HINT = (
    "💡 R7 API-first 권장: WAF가 HTML 경로를 차단 중. "
    "Playwright MCP 사용 → browser_navigate → browser_network_requests "
    "→ `/api/`·`/graphql`·`\\.json` 필터로 내부 엔드포인트 탐지 → "
    "해당 URL을 bundled `scripts/run.sh <API_URL>`로 재호출. 대부분 API 레이어는 "
    "WAF 방어가 얕아 curl_cffi만으로 수집됨."
)


def _format_summary(trace: list[Attempt], profile: Optional[str], stop_reason: str = "") -> str:
    n = len(trace)
    verdicts = [a.verdict for a in trace]
    challenge_count = sum(1 for v in verdicts if v == Verdict.CHALLENGE.value)
    base = (
        f"failed after {n} attempts; profile={profile}; stop={stop_reason}; "
        f"verdicts={','.join(v for v in verdicts[:5])}" + ("..." if n > 5 else "")
    )
    if profile in _R7_ELIGIBLE_PROFILES and challenge_count >= 3:
        return base + "\n" + R7_HINT
    return base
