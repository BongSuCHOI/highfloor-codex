# Upstream provenance

## Primary adaptation source

- Upstream: `Q00/ouroboros`
- Snapshot: `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d`
- Relevant sources: `README.ko.md`, `skills/interview/SKILL.md`, `skills/seed/SKILL.md`, `skills/brownfield/SKILL.md`, `skills/auto/SKILL.md`
- License: MIT; see `LICENSE.upstream.txt`

Borrowed concepts:

- Socratic clarification and visible ambiguity tracks
- code facts before user questions
- explicit restatement and approval before execution
- acceptance-oriented specification
- assumption provenance
- Double Diamond-style divergence and convergence inside specification discovery

## Research refresh

- Reference: `Yeachan-Heo/gajae-code`
- Tag: `v0.12.0`
- Commit: `4e927cca7e6dda31d715957a2ecfbcbc4e62869a`
- Relevant sources: `deep-interview/SKILL.md`, `deep-interview-ambiguity.ts`, `deep-interview-stage.ts`
- License: MIT
- Relationship: `research reference`; no GJC source or wording is bundled

Independently absorbed ideas:

- conditionally confirm the top-level shape of multi-surface requests before deep questioning;
- treat readiness as non-monotonic when later answers contradict earlier decisions;
- require explicit review when a proposed contract removes, merges, or substitutes a confirmed material item.

## Method source additions

- Reference: [`mattpocock/skills`](https://github.com/mattpocock/skills)
- Inspected commit: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- Relevant sources: `skills/productivity/grilling/SKILL.md`,
  `skills/engineering/grill-with-docs/SKILL.md`,
  `skills/engineering/improve-codebase-architecture/SKILL.md`
- License: MIT; see `LICENSES/MIT-mattpocock-skills.txt` at the repository root
  and the bundled copy `LICENSE.mattpocock-skills.txt` in this directory
- Relationship: `modified derivative` (condensed); retains upstream method
  structure and terminology where noted; no executable source is bundled

Absorbed ideas (condensed):

- batch currently answerable material questions into numbered rounds with a
  recommended answer each, while dependency-blocked questions wait for later
  rounds;
- offer durable decision records, such as an ADR or glossary entry, when a
  load-bearing rejection reason would otherwise be re-litigated by a future
  session.

Deliberately not migrated:

- the fixed design-tree/frontier-empty completion rule, which conflicts with
  this skill's material-unknown readiness boundary;
- alias skills and any automatic documentation side effects during
  questioning.

## Specification-synthesis research reference

- Reference: `mattpocock/skills`
- Commit: `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`
- Relevant source: `skills/engineering/to-spec/SKILL.md`
- License: MIT
- Relationship: `research reference`; no source or wording is bundled

Independently absorbed idea:

- when the current conversation and project evidence already resolve material
  decisions, synthesize them into the contract without replaying an interview;
  ask only about a genuine surviving fork.

Deliberate changes:

- combine interview and seed into one compact task-contract skill;
- remove Ouroboros and GJC MCP/CLI, state, HUD, event-store, staged-transition, and product-specific behavior;
- remove mandatory panels, numeric ambiguity authority or deterministic score floor, fixed ontology and hash manifest, and iterative or persisted persona loops;
- preserve the interview's Socratic and divergence/convergence method without importing Ouroboros's full execution engine;
- preserve topology and reduction checks as conditional scaffolds rather than mandatory ceremony;
- preserve an adaptive ceiling so stronger models may compress or extend the scaffold while meeting the hard floor.

The Ouroboros-derived implementation remains independently worded; the
condensed Matt Pocock material above is a modified derivative as recorded.
Preserve this provenance record if the skill is redistributed.
