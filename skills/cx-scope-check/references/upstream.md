# Upstream provenance

- Upstream: `Q00/ouroboros`
- Snapshot: `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d`
- Relevant sources: `skills/status/SKILL.md`, `src/ouroboros/observability/drift.py`
- License: MIT; see `LICENSE.upstream.txt`

Borrowed concept:

- treat the original specification as the execution baseline, compare current reality with it, and expose goal, constraint, and concept drift.

Deliberate changes:

- replace lexical Jaccard distance and weighted numeric thresholds with evidence-backed semantic categories;
- add explicit non-goal, dependency, API/schema, authority, and acceptance-coverage checks;
- make the skill event-triggered rather than continuously intrusive;
- preserve stronger-model judgment for semantic equivalence while keeping hard boundaries non-negotiable.

This implementation is independently worded. Preserve this provenance record if the skill is redistributed.
