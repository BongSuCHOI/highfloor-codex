# Research Handoff

`FetchResult.to_evidence_dict()` describes retrieval, not truth. The CLI exposes
the same object under `evidence`.

```json
{
  "schema_version": 1,
  "requested_url": "https://example.com/article",
  "final_url": "https://example.com/article",
  "retrieved_at": "2026-07-30T00:00:00+00:00",
  "ok": true,
  "content_role": "published_source_candidate",
  "retrieval_verdict": "strong_ok",
  "stop_reason": "success",
  "untried_routes": [],
  "retrieval_route": {
    "phase": "grid",
    "executor": "curl_cffi",
    "fallback_used": false,
    "profile_used": null
  },
  "extraction": {
    "method": "raw",
    "completeness_heuristic": 0.82,
    "limitations": []
  },
  "content_trust": "untrusted_public_web",
  "prompt_injection_risk": "none",
  "source_quality": "not_evaluated",
  "claim_confidence": "not_evaluated",
  "runtime_warnings": []
}
```

Hard boundaries:

- `retrieval_verdict` reports access validation only.
- `extraction.completeness_heuristic` measures text recovery characteristics,
  not source credibility or factual accuracy.
- A `null` completeness heuristic means that the selected route did not measure
  it; use the accompanying method and limitations instead.
- `prompt_injection_risk="none"` does not make content trusted.
- `$cx-ultraresearch` owns source quality, independence, contradiction, and
  claim-support judgments.

Use `--evidence-json` when the caller needs both content and metadata. It emits
only `evidence` and `untrusted_content`, with the content wrapped for LLM
context. The broader `--json --include-content` form remains available for
diagnostics.

If `evidence.ok=false`, `content_role` is `diagnostic_only`: do not treat the
challenge or error body as published-source evidence. A `weak_ok` result uses
`candidate_with_limitations`; inspect `extraction.limitations` before using the
content. Reuse both values from one successful call; do not repeat the fetch
just to populate a research source map.
