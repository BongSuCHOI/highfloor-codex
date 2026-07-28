# Upstream provenance

- Upstream: `Q00/ouroboros`
- Snapshot: `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d`
- Relevant sources: `skills/qa/SKILL.md`, `skills/evaluate/SKILL.md`
- License: MIT; see `LICENSE.upstream.txt`

Borrowed concepts:

- define the quality bar before judgment;
- treat specification acceptance criteria as observable promises;
- mechanical checks before semantic evaluation;
- execute and observe behavior instead of trusting output text;
- escalate only when cheaper evidence cannot resolve the claim.

Deliberate changes:

- replace numeric scores and iterative QA sessions with `PASS`, `FAIL`, and `NOT_PROVEN`;
- remove mandatory multi-model consensus and Ouroboros session coupling;
- enforce scope-proportional verification and reuse existing `cx-*` owners;
- allow stronger models to select superior evidence paths without weakening verdict semantics.

This implementation is independently worded. Preserve this provenance record if the skill is redistributed.
