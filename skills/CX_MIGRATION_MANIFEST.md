# CX Skills Migration Manifest

- Updated: 2026-07-28
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

Current live `cx-*` skills: 13.

- `cx-acceptance-qa`
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
- `cx-unstuck`
- `cx-visual-qa`

## 3. Upstream provenance and redistribution

Relationships follow the licensing governance in `CX_SKILLS.md`.

| Skill | Upstream | Source pin | Relationship | License | Local evidence |
|---|---|---|---|---|---|
| `cx-acceptance-qa` | `Q00/ouroboros` | `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d` | `independently worded` | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-browser-automation` | `microsoft/playwright-cli`; runtime: `vercel-labs/agent-browser@0.29.1` | Playwright commit `NOT_PROVEN`; agent-browser source not bundled | `modified derivative`; `runtime invocation` | Apache-2.0 | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-coding-agent-sessions` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/coding-agent-sessions` | source archive `4.14.0`; commit `NOT_PROVEN` | `modified derivative` with retained byte-identical files | Sustainable Use License 1.0 | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-debugging` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/debugging` | source archive `4.14.0`; commit `NOT_PROVEN` | `modified derivative` | Sustainable Use License 1.0 | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-design-director` | current local references; optional `ibelick/ui-skills@0.2.4` | external CLI content not bundled | original content; `runtime invocation` | original content license; UI Skills MIT | `references/upstream.md` |
| `cx-insane-search` | `fivetaku/insane-search` | source snapshot `NOT_PROVEN` | `modified derivative`; engine and tests retained | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-interview` | `Q00/ouroboros` | `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d` | `independently worded` | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-programming` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/programming` | source archive `4.14.0`; commit `NOT_PROVEN` | `modified derivative` | Sustainable Use License 1.0 | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-scope-check` | `Q00/ouroboros` | `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d` | `independently worded` | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-slopslap` | `vibedesignlab/slopslap` | plugin version `1.3.0`; commit `NOT_PROVEN` | `modified derivative`; taxonomy, data, references, scripts retained | MIT | `references/upstream-attribution.md`, `references/UPSTREAM_LICENSE.txt` |
| `cx-ultraresearch` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/ulw-research` | source archive `4.14.0`; commit `NOT_PROVEN` | `modified derivative` | Sustainable Use License 1.0 | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-unstuck` | `Q00/ouroboros` | `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d` | `independently worded` | MIT | `references/upstream.md`, `references/LICENSE.upstream.txt` |
| `cx-visual-qa` | `code-yeongyu/oh-my-openagent`, `packages/shared-skills/skills/visual-qa` | source archive `4.14.0`; commit `NOT_PROVEN` | `modified derivative` with retained byte-identical files | Sustainable Use License 1.0 | `references/upstream.md`, `references/LICENSE.upstream.txt` |

Distribution boundary:

- The public CX bundle is mixed-license.
- Original content may use the repository's root license.
- Third-party and derivative material remains under the license named above.
- `oh-my-openagent` derivatives may be distributed only free of charge for non-commercial purposes and must retain the Sustainable Use License terms and prominent modification notice.
- `code-yeongyu/lazycodex` and `Yeachan-Heo/gajae-code` were research/comparison references, not current redistribution sources.

## 4. 2026-07-28 additions and normalization

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

## 5. 2026-07-22 restructure

- Renamed `cx-visual-qa-strict` to `cx-visual-qa`.
- Replaced copied third-party design trees with six original references.
- Added optional UI Skills lookup without vendoring its content.
- Curated `cx-programming` into language decision cards and an isolated Python helper.
- Retained `cx-insane-search` engine/tests while rewriting public-content boundaries.
- Condensed browser, session, debugging, slopslap, and ultraresearch hot paths.
- Absorbed generic refactor and implementation-neutral anti-slop rules into retained owners.

## 6. Removed from live root

- `cx-ultimate-browsing` — deleted by the user on 2026-07-28; stale routes removed
- `cx-refactor`
- `cx-remove-ai-slops`
- `cx-review-work`
- `cx-start-work`
- `cx-ulw-plan`

Managed/plugin skills outside the `cx-*` namespace are out of scope.

## 7. Synchronization

Canonical public files live under this repository's `skills/` directory.
Installed copies are generated runtime artifacts and must not be treated as the
authoring source.
