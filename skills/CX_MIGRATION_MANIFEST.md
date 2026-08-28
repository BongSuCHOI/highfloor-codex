# CX Skills Migration Manifest

- Updated: 2026-08-22
- Repository root: `skills/`
- Installed root: selected by `install.sh` (`$CODEX_HOME/skills` by default,
  unless explicitly overridden)
- Governance: `CX_SKILLS.md`
- Uniform catalog: `CX_SKILL_CATALOG.md`
- Runtime contracts: `cx-*/SKILL.md`
- Pre-2026-07-28 backup: `~/Documents/Codex/2026-07-22/d/cx-skills-before-restructure-20260722.tar.gz`
- Recoverable 2026-07-22 removed material: `~/Documents/Codex/2026-07-22/d/work/restructure-removed`

## 1. Document responsibility

This file records the live inventory, migration history, upstream provenance,
and license ledger. `CX_SKILLS.md` owns the philosophy and design criteria,
`CX_SKILL_CATALOG.md` owns the uniform routing summary for current skills, and
each `SKILL.md` owns actual behavior.

## 2. Live inventory

Current live `cx-*` skills: 15. All are `active`; no new skill was added by the
2026-08-28 method absorption. `cx-browser-automation`, `cx-insane-search`, and
`cx-unstuck` remain possible `sunset candidate` evaluations, not deprecated
skills.

- `cx-acceptance-qa`
- `cx-analyze-video`
- `cx-browser-automation`
- `cx-coding-agent-sessions`
- `cx-debugging`
- `cx-design-director`
- `cx-insane-search`
- `cx-interview`
- `cx-programming`
- `cx-scope-check`
- `cx-slopslap`
- `cx-ultraresearch`
- `cx-understand-codebase`
- `cx-unstuck`
- `cx-visual-qa`

## 3. Upstream provenance and redistribution

Relationships follow the licensing governance in `CX_SKILLS.md`.

| Skill | Upstream | Source pin | Relationship | License | Local evidence |
|---|---|---|---|---|---|
| `cx-acceptance-qa` | `Q00/ouroboros` | `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d` | `independently worded` | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-analyze-video` | `bradautomates/claude-video`, `skills/watch` | `83da59fa78c3eee9e20f515fe75c438bb5166efd`; skill version `0.2.0` | `modified derivative` with retained Python analysis scripts | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-browser-automation` | `microsoft/playwright-cli`; runtime: `vercel-labs/agent-browser@0.29.1` | Playwright commit `NOT_PROVEN`; agent-browser source not bundled | `modified derivative`; `runtime invocation` | Apache-2.0 | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-coding-agent-sessions` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/coding-agent-sessions` | source archive `4.14.0`; commit `NOT_PROVEN` | `modified derivative` with retained byte-identical files | Sustainable Use License 1.0 | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-debugging` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/debugging`; method research: `mattpocock/skills` | source archive `4.14.0`, commit `NOT_PROVEN`; Matt `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | `modified derivative`; independently worded feedback-loop adaptation | Sustainable Use License 1.0; MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-design-director` | current local references; method source: `fivetaku/insane-design`; research: `changeroa/StyleGallery`; research: `uizze/uizze` (`anti-ui-slop`); optional `ibelick/ui-skills@0.2.4` | insane-design `a5eb1d976d29309092170ff7ba475a487df0b683`; StyleGallery `e67b440147970c5d4f5b83f922d2593e12d09e74`; uizze `3f08d874627be4d89d2af8e6409dc5e660050b5c`; UI Skills content not bundled | original content with an `independently worded` insane-design evidence-contract adaptation; `modified derivative` (condensed) of the uizze surface-intent material; `research reference`; `runtime invocation` | original content license; insane-design MIT; StyleGallery license `NOT_PROVEN`; uizze MIT; UI Skills MIT | `references/upstream.md`, `references/LICENSE.insane-design.txt`, `references/LICENSE.anti-ui-slop.txt` |
| `cx-insane-search` | `fivetaku/insane-search`; method reference: `fivetaku/insane-research` | original insane-search snapshot `NOT_PROVEN`; selective refresh `019ee16bbf471595f9b67b164e4a92208183af2d`; insane-research `68f7e59168a9c9b0a586bd4122cb7a229e119d9c` | `modified derivative`; engine and tests retained; independently worded retrieval-evidence adaptation | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt`, `references/LICENSE.insane-research.txt` |
| `cx-interview` | `Q00/ouroboros`; method source: `mattpocock/skills`; method research: `Yeachan-Heo/gajae-code`, `mattpocock/skills` | Ouroboros `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d`; GJC `4e927cca7e6dda31d715957a2ecfbcbc4e62869a`; Matt source `5b15a47f2d7150f545fbcacbfe381787fc0230dc`; Matt research `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | `independently worded` from Ouroboros; `modified derivative` (condensed) of questioning and decision-record material; independently worded synthesis adaptation | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt`, `references/LICENSE.mattpocock-skills.txt` |
| `cx-programming` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/programming` | source archive `4.14.0`; commit `NOT_PROVEN` | `modified derivative` | Sustainable Use License 1.0 | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-scope-check` | `Q00/ouroboros` | `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d` | `independently worded` | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-slopslap` | `vibedesignlab/slopslap` | plugin version `1.3.0`; commit `NOT_PROVEN` | `modified derivative`; taxonomy, data, references, scripts retained | MIT | `references/upstream-attribution.md`, `references/UPSTREAM_LICENSE.txt` |
| `cx-ultraresearch` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/ulw-research`; method references: `fivetaku/insane-research`, `LilMGenius/paperthin` | source archive `4.14.0`, commit `NOT_PROVEN`; insane-research `68f7e59168a9c9b0a586bd4122cb7a229e119d9c`; paperthin `3bca079a51bcfff5dafb53d1d7f9f523d66ee317` | `modified derivative`; independently worded adaptation of selected research and claim-checking concepts | Sustainable Use License 1.0; MIT | `references/upstream.md`, `references/LICENSE.upstream.txt`, `references/LICENSE.insane-research.txt` |
| `cx-understand-codebase` | `Egonex-AI/Understand-Anything` | `fe8c5bc591716aafd79b4765549328f08ef5a52e`; plugin version `2.9.4` | `modified derivative` with vendored analysis and viewer runtime | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-unstuck` | `Q00/ouroboros`; method research: `LilMGenius/paperthin` | Ouroboros `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d`; paperthin `3bca079a51bcfff5dafb53d1d7f9f523d66ee317` | `independently worded` with research reference | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-visual-qa` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/visual-qa`; method source: `uizze/uizze` (`anti-ui-slop`) | source archive `4.14.0`; commit `NOT_PROVEN`; uizze `3f08d874627be4d89d2af8e6409dc5e660050b5c` | `modified derivative` with retained byte-identical files plus a condensed uizze recapture-bound adaptation | Sustainable Use License 1.0; MIT | `references/upstream.md`, `references/LICENSE.upstream.txt`, `references/LICENSE.anti-ui-slop.txt` |

Distribution boundary:

- The public CX bundle is mixed-license.
- Original content may use the repository's root license.
- Third-party and derivative material remains under the license named above.
- `oh-my-openagent` derivatives may be distributed only free of charge for non-commercial purposes and must retain the Sustainable Use License terms and prominent modification notice.
- `code-yeongyu/lazycodex` and `Yeachan-Heo/gajae-code` remain research/comparison references, not current redistribution sources.

## 4. 2026-08-28 restraint and method absorption

Reviewed:

- `mattpocock/skills` at
  `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` under MIT;
- `LilMGenius/paperthin` at
  `3bca079a51bcfff5dafb53d1d7f9f523d66ee317` under MIT.

Independently absorbed:

- governance: `NO_CHANGE` as a valid success, explicit maintenance-cost review,
  independent-ground-truth checks for evaluation, and lifecycle states without
  directory churn;
- `cx-debugging`: a bounded red-capable feedback loop as the preferred first
  instrument for unclear failures, without removing partial-runtime analysis;
- `cx-interview`: synthesis mode when the conversation and current evidence
  already resolve material decisions;
- `cx-unstuck`: one load-bearing failed assumption and its cheapest
  discriminating experiment before alternatives;
- `cx-ultraresearch`: two-direction counterchecking when a material claim rests
  on intuition about plausibility, novelty, absurdity, or impossibility.

Deliberately not migrated:

- automatic post-edit skill chaining or mandatory recursive audits;
- separate micro-skills for prose cleanup, ordering, punctuation, routing, or
  ordinary intent restatement;
- model-tier routing, mandatory subagent fan-out, fresh-context consensus, or a
  generic project execution engine;
- the upstream skill catalogs, directory taxonomies, project setup workflows,
  issue-tracker orchestration, and artifact lifecycle runtimes.

For the additions in this subsection, no upstream source or wording is bundled;
the pinned repositories are research references for independently worded method
changes.

## 5. 2026-08-22 governance-path fix and method refresh

Documentation fix:

- Corrected the global-instruction governance pointer. The installer never
  distributed the three canonical governance documents, so no installed copy
  exists; Codex now reads `skills/CX_SKILLS.md` from a Highfloor checkout and
  states the constraint when none exists.

Method sources reviewed:

- [`mattpocock/skills`](https://github.com/mattpocock/skills)
  at `5b15a47f2d7150f545fbcacbfe381787fc0230dc` (MIT): `grilling`,
  `grill-me`, `grill-with-docs`, `improve-codebase-architecture`.
- [`uizze/uizze`](https://github.com/uizze/uizze)
  at `3f08d874627be4d89d2af8e6409dc5e660050b5c` (MIT):
  `skills/anti-ui-slop/SKILL.md`.

Absorbed (condensed):

- `cx-interview`: optional batched questioning rounds with per-question
  recommended answers; opt-in durable decision-record handoff (ADR or
  glossary) requiring explicit approval; colloquial grill/stress-test
  triggers.
- `agents/architect.toml`: hot-spot-first scoping, shallow-module friction
  signals, deletion test, recommendation-strength vocabulary, and
  decision-record non-re-litigation.
- `cx-design-director`: surface-intent classification lens and the rule not
  to soften a selected replacement direction by polishing the discarded look.
- `cx-visual-qa`: post-fix evidence recapture bound limited to the affected
  surface with at most one confirmation round.
- `docs/WORKFLOWS.md`: batched UI verification pass budget in Recipe D and an
  open-ended polish-loop anti-pattern.

Deliberately not migrated:

- Uizze advertising lines, covert runtime metadata, paid-MCP catalogue
  integration, command suite, hooks, and detector scripts.
- The fixed frontier-empty completion rule, which conflicts with this
  library's material-unknown readiness boundary.
- HTML report artifacts and mandatory parallel sub-agent fan-out from the
  architecture workflow.
- Alias-only skills as separate library entries; their useful behavior is
  owned by the absorptions above.

No skill was added, removed, or renamed; the live inventory is unchanged.

## 6. 2026-08-09 additions and design research refresh

Added:

- `cx-analyze-video`: preserves upstream frame extraction, scene/keyframe
  sampling, caption parsing, focused ranges, deduplication, and optional
  transcription while adding Codex routing, preflight-only setup, explicit
  external-upload consent, evidence lanes, and guarded cleanup.
- `cx-understand-codebase`: preserves upstream deterministic scanners, semantic
  batching, graph schema and merge logic, specialist prompts, incremental
  fingerprints, and interactive viewer while adding exact-worktree targeting,
  untrusted-project boundaries, a source-versioned runtime cache,
  partial-result separation, and local token-gated serving.

The temporary staging names `analyze-video` and `understand-codebase` were
canonicalized before release. No compatibility aliases were created. Claude
slash-command surfaces were replaced by `$cx-analyze-video` and
`$cx-understand-codebase` with trailing action words.

Forward verification used generated local MP4 and MOV files for frame
extraction and guarded cleanup, the vendored core test suite (`976` passing
tests), the dashboard suite (`102` passing tests), a frozen analysis/dashboard
build, and live `127.0.0.1` token-gate responses (`403` without a token, `200`
with one).
The cached runtime left the installer-managed skill source unchanged, and the
non-Git scanner excluded prior `.ua/` data while recovering four source files
and one internal import edge.
Public-URL download remained `NOT_PROVEN` on the validation host because
`yt-dlp` was absent; setup stopped with an install suggestion and ran no
installer.

StyleGallery was reviewed at
`e67b440147970c5d4f5b83f922d2593e12d09e74` as a research-only source for
layout responsibility, motion continuity and visual-evidence boundaries.
Highfloor added independently worded refinements to the existing
`cx-design-director` and `cx-visual-qa` owners. It did not import the pattern
corpus, CLI, MCP, governance runtime or visual defaults. Redistribution rights
remain `NOT_PROVEN`, so no StyleGallery source is bundled.

## 6. 2026-07-30 guarded retrieval and research composition

Selected concepts reviewed from `fivetaku/insane-research` at
`68f7e59168a9c9b0a586bd4122cb7a229e119d9c`:

- source and material-claim maps;
- countersearch and explicit contradiction states;
- `observed_at` versus `valid_at`;
- executable observation with an environment boundary;
- retrieval access metadata separated from claim judgment.

Independently absorbed:

- `cx-insane-search`: fail-closed resolution, curl DNS pinning, guarded Phase 0,
  local browser subprocess disabled at the public fetch boundary with an
  explicit host-browser handoff, opt-in persistent state, and a compact
  retrieval-only evidence envelope;
- `cx-ultraresearch`: claim-relative source assessment, lineage-based
  independence, `supported` / `unresolved` / `refuted` states, selective
  countersearch, and a single-fetch blocked-source handoff.

Deliberately not migrated:

- fixed seven-phase execution and automatic agent fan-out;
- permission bypass and mandatory plan approval;
- mandatory session, ledger, report, and website artifacts;
- fixed source grades, domain-based independence, and universal two-source
  rules;
- claim truth or signature claims from self-reported metadata;
- the upstream validator and report evaluator.

## 7. 2026-07-29 upstream research refresh

### Gajae Code `v0.12.0`

- Repository: `Yeachan-Heo/gajae-code`
- Tag: `v0.12.0`
- Commit: `4e927cca7e6dda31d715957a2ecfbcbc4e62869a`
- License: MIT
- Relationship: `research reference`; no GJC source or wording is bundled
- Reviewed surfaces: `deep-interview` skill/runtime, `ralplan` skill/runtime,
  and the Architect/Critic re-review prompt changes

Independently absorbed into `cx-interview`:

- conditional top-level coverage for materially multi-surface requests;
- non-monotonic readiness when later evidence reopens a settled decision;
- explicit approval for removing, merging, or substituting a confirmed material
  item.

Deliberately not migrated:

- GJC CLI, state, HUD, staged-transition, receipt, and artifact-ledger runtime;
- numeric ambiguity authority, deterministic score floors, fixed ontology, and
  hash-bound intent manifests;
- mandatory or persisted Planner/Architect/Critic orchestration.

The `ralplan` re-review ratchet remains a reviewed agent-workflow candidate. It
was not added to the skill library because it requires an explicit multi-agent
review context rather than a general skill runtime.

## 8. 2026-07-28 additions and normalization

### Added from `Q00/ouroboros`

Upstream:

- Repository: `Q00/ouroboros`
- Snapshot: `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d`
- License: MIT
- Per-skill provenance: each new skill's `references/upstream.md`

Added:

- `cx-interview`: Socratic clarification and approved Task Contract
- `cx-acceptance-qa`: evidence-backed `PASS`, `FAIL`, `NOT_PROVEN`
- `cx-scope-check`: event-triggered semantic scope comparison
- `cx-unstuck`: bounded lateral reframing

The initial staging names were changed before canonicalization:

| Initial name | Intermediate name | Canonical name |
|---|---|---|
| `cx-requirements` | — | `cx-interview` |
| `cx-acceptance-gate` | `cx-acceptance-check` | `cx-acceptance-qa` |
| `cx-scope-drift` | — | `cx-scope-check` |
| `cx-reframe` | `cx-break-deadlock` | `cx-unstuck` |

No compatibility aliases remain.

### Method preservation correction

The first migration preserved safety boundaries but left some rationale too implicit. Each of the four skills now carries a compact `## Method` that preserves the operational purpose of Socratic questioning, observable specification, specification-as-contract, or lateral thinking. Full Ouroboros MCP, orchestration, scoring, persona fan-out, and execution runtime remain intentionally excluded.

### Existing skill review

- Narrowed `cx-slopslap` to explicit AI-slop requests and routed redesign direction to `cx-design-director`.
- Removed stale `cx-ultimate-browsing` routing from `cx-ultraresearch` and narrowed deep-research trigger.
- Added `NOT_PROVEN` to `cx-visual-qa` for missing evidence or unavailable observation.
- Added permission-only `uv` cache fallback where applicable.
- Updated `cx-coding-agent-sessions` absolute `detail_hint`, stale tests, and bytecode-cache behavior.
- Added `cx-debugging` non-triggers.
- Pinned optional UI Skills CLI in `cx-design-director`.
- Added host-neutral `must_invoke_browser_automation` while retaining the old serialized alias for compatibility.
- Kept `cx-browser-automation` and the core `cx-programming` guidance unchanged.

### Documentation split

- `CX_SKILLS.md`: governance only
- `CX_SKILL_CATALOG.md`: uniform five-field summary for all live skills
- `CX_MIGRATION_MANIFEST.md`: inventory, migration history, upstream provenance, and license ledger

## 9. 2026-07-22 restructure

- Renamed `cx-visual-qa-strict` to `cx-visual-qa`.
- Replaced copied third-party design trees with six original references.
- Added optional UI Skills lookup without vendoring its content.
- Curated `cx-programming` into language decision cards and an isolated Python helper.
- Retained `cx-insane-search` engine/tests while rewriting public-content boundaries.
- Condensed browser, session, debugging, slopslap, and ultraresearch hot paths.
- Absorbed generic refactor and implementation-neutral anti-slop rules into retained owners.

## 10. Removed from live root

- `cx-ultimate-browsing` — deleted by the user on 2026-07-28; stale routes removed
- `cx-refactor`
- `cx-remove-ai-slops`
- `cx-review-work`
- `cx-start-work`
- `cx-ulw-plan`

Managed/plugin skills outside the `cx-*` namespace are out of scope.

## 11. Synchronization

Canonical public files live under this repository's `skills/` directory. The
installer does not distribute governance documents; it manages only the
manifest-listed skill directories and agent files. Treat any copy outside this
repository as an unverified convenience, not the authoring source.
