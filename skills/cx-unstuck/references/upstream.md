# Upstream provenance

- Upstream: `Q00/ouroboros`
- Snapshot: `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d`
- Relevant source: `skills/unstuck/SKILL.md`
- License: MIT; see `LICENSE.upstream.txt`

Borrowed concepts:

- challenge assumptions when progress stalls;
- use lateral thinking to change the frame rather than repeat the stalled approach;
- select different reasoning lenses for different failure shapes;
- return concrete alternatives, disagreements, and a recommendation.

Deliberate changes:

- remove mandatory MCP routing, hidden dispatch payloads, and multi-agent persona fan-out;
- bound the result to a small decision surface;
- route runtime cause-finding to `cx-debugging`;
- treat lenses as optional scaffolding so stronger models may use a better reasoning method.

This implementation is independently worded. Preserve this provenance record if the skill is redistributed.

## Method research reference

- Reference: `LilMGenius/paperthin`
- Commit: `3bca079a51bcfff5dafb53d1d7f9f523d66ee317`
- Relevant source: `skills/depth/hate/SKILL.md`
- License: MIT
- Relationship: `research reference`; no source or wording is bundled

Independently absorbed idea:

- collapse a stalled plan to one load-bearing failed assumption and identify
  the cheapest experiment that can discriminate it before multiplying
  alternatives.
