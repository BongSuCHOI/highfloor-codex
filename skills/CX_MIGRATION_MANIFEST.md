# CX Skills Migration Manifest

- Updated: 2026-08-09
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

Current live `cx-*` skills: 15.

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
| `cx-debugging` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/debugging` | source archive `4.14.0`; commit `NOT_PROVEN` | `modified derivative` | Sustainable Use License 1.0 | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-design-director` | current local references; method source: `fivetaku/insane-design`; research: `changeroa/StyleGallery`; optional `ibelick/ui-skills@0.2.4` | insane-design `a5eb1d976d29309092170ff7ba475a487df0b683`; StyleGallery `e67b440147970c5d4f5b83f922d2593e12d09e74`; UI Skills content not bundled | original content with an `independently worded` evidence-contract adaptation; `research reference`; `runtime invocation` | original content license; insane-design MIT; StyleGallery license `NOT_PROVEN`; UI Skills MIT | `references/upstream.md`, `references/LICENSE.insane-design.txt` |
| `cx-insane-search` | `fivetaku/insane-search`; method reference: `fivetaku/insane-research` | original insane-search snapshot `NOT_PROVEN`; selective refresh `019ee16bbf471595f9b67b164e4a92208183af2d`; insane-research `68f7e59168a9c9b0a586bd4122cb7a229e119d9c` | `modified derivative`; engine and tests retained; independently worded retrieval-evidence adaptation | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt`, `references/LICENSE.insane-research.txt` |
| `cx-interview` | `Q00/ouroboros` | `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d` | `independently worded` | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-programming` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/programming` | source archive `4.14.0`; commit `NOT_PROVEN` | `modified derivative` | Sustainable Use License 1.0 | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-scope-check` | `Q00/ouroboros` | `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d` | `independently worded` | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-slopslap` | `vibedesignlab/slopslap` | plugin version `1.3.0`; commit `NOT_PROVEN` | `modified derivative`; taxonomy, data, references, scripts retained | MIT | `references/upstream-attribution.md`, `references/UPSTREAM_LICENSE.txt` |
| `cx-ultraresearch` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/ulw-research`; method reference: `fivetaku/insane-research` | source archive `4.14.0`, commit `NOT_PROVEN`; insane-research `68f7e59168a9c9b0a586bd4122cb7a229e119d9c` | `modified derivative`; independently worded adaptation of selected research-method concepts | Sustainable Use License 1.0; MIT | `references/upstream.md`, `references/LICENSE.upstream.txt`, `references/LICENSE.insane-research.txt` |
| `cx-understand-codebase` | `Egonex-AI/Understand-Anything` | `fe8c5bc591716aafd79b4765549328f08ef5a52e`; plugin version `2.9.4` | `modified derivative` with vendored analysis and viewer runtime | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-unstuck` | `Q00/ouroboros` | `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d` | `independently worded` | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-visual-qa` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/visual-qa` | source archive `4.14.0`; commit `NOT_PROVEN` | `modified derivative` with retained byte-identical files | Sustainable Use License 1.0 | `references/upstream.md`, `references/LICENSE.upstream.txt` |

Distribution boundary:

- The public CX bundle is mixed-license.
- Original content may use the repository's root license.
- Third-party and derivative material remains under the license named above.
- `oh-my-openagent` derivatives may be distributed only free of charge for non-commercial purposes and must retain the Sustainable Use License terms and prominent modification notice.
- `code-yeongyu/lazycodex` and `Yeachan-Heo/gajae-code` remain research/comparison references, not current redistribution sources.

## 4. 2026-08-09 additions and design research refresh

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

## 5. 2026-07-30 guarded retrieval and research composition

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

## 6. 2026-07-29 upstream research refresh

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

## 7. 2026-07-28 additions and normalization

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

## 8. 2026-07-22 restructure

- Renamed `cx-visual-qa-strict` to `cx-visual-qa`.
- Replaced copied third-party design trees with six original references.
- Added optional UI Skills lookup without vendoring its content.
- Curated `cx-programming` into language decision cards and an isolated Python helper.
- Retained `cx-insane-search` engine/tests while rewriting public-content boundaries.
- Condensed browser, session, debugging, slopslap, and ultraresearch hot paths.
- Absorbed generic refactor and implementation-neutral anti-slop rules into retained owners.

## 9. Removed from live root

- `cx-ultimate-browsing` — deleted by the user on 2026-07-28; stale routes removed
- `cx-refactor`
- `cx-remove-ai-slops`
- `cx-review-work`
- `cx-start-work`
- `cx-ulw-plan`

Managed/plugin skills outside the `cx-*` namespace are out of scope.

## 10. Synchronization

Canonical public files live under this repository's `skills/` directory.
Installed copies are generated runtime artifacts and must not be treated as the
authoring source.
