# Evidence Contract

Use this contract in working context for high-stakes or citation-heavy work.
Materialize `sources.jsonl` and `claims.jsonl` only when the user requests a
durable report or evidence artifact.

## Source record

```json
{
  "id": "src_001",
  "url": "https://example.com/report",
  "title": "Report title",
  "publisher": "Publisher",
  "lineage_id": "publisher-or-originating-dataset",
  "source_type": "primary|official|paper|report|journalism|commentary",
  "observed_at": "2026-07-30T00:00:00+00:00",
  "valid_at": "2026-07-30",
  "access": null
}
```

`lineage_id` represents ownership, authorship, or originating data. Two domains
that repeat the same press release, wire story, study, or dataset share a
lineage. `access` may contain the exact retrieval-only envelope returned by
`$cx-insane-search`; it never establishes how well the source supports a
particular claim. Use `lineage_id="unknown"` when provenance cannot be
established, and do not count two unknown-lineage sources as independent
without affirmative evidence.

## Material claim record

```json
{
  "id": "claim_001",
  "text": "Material proposition stated in the answer",
  "risk": "normal|high",
  "status": "supported|unresolved|refuted",
  "evidence": [
    {
      "source_id": "src_001",
      "directness": "direct|indirect",
      "authority": "high|medium|low",
      "freshness": "fit|limited|stale",
      "methodology": "adequate|limited|unknown",
      "conflict_of_interest": "none_seen|present|unknown",
      "retrieval_completeness": "complete|partial|unknown"
    }
  ],
  "evidence_basis": "direct_authority|triangulated|execution_observation",
  "countersearch": {
    "required": false,
    "query_or_method": "",
    "result": "not_run|no_material_conflict|conflict_found"
  },
  "conflicts": [],
  "scope_note": ""
}
```

Each evidence assessment is claim-relative; do not turn it into a permanent
grade for the source. Use `supported` only when the cited evidence directly
supports the claim at the stated scope. Use `unresolved` for missing evidence,
partial retrieval, relevant conflict, or insufficiently independent support.
Use `refuted` when stronger evidence contradicts the proposition.

Execution proves only the observed behavior in the recorded environment. It
does not establish general product behavior, future behavior, or source
credibility.

## Mechanical checks

If artifacts are created, mechanically check only what a deterministic process
can establish:

- every line parses as JSON;
- source and claim IDs are unique;
- every `evidence[].source_id` exists;
- timestamps and status values have the expected form;
- a `supported` claim has at least one evidence link.

Do not label these checks a truth validator, signature, or factual
verification. Human and model judgment still own source assessment, conflict
resolution, citation placement in the report, and final accountability.
