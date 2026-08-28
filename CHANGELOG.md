# Changelog

All notable changes to Highfloor for Codex will be documented here.

The project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- Rebuilt the portable `CODEX_AGENTS.md` around the maintainer's proven
  outcome-driven contract: a binding intent gate, end-to-end execution,
  proportional verification, deterministic test guidance, manual QA, explicit
  failure recovery, and an observable stop. Merged Highfloor's authority,
  scope, `NOT_PROVEN`, and provenance floor once, resolved test and delegation
  conflicts, and generalized host-specific tool names into portable capability
  guidance. Skill governance and search or UI routing remain owned by
  capability discovery or explicit user direction instead of the global file.
- Added managed `default` and `worker` custom-agent overrides at
  `gpt-5.6-luna` / `xhigh`, preserving the user's `config.toml` while making
  Highfloor's fallback profile portable through install, update, doctor, and
  uninstall. Rebalanced `reviewer` to `gpt-5.6-terra` / `high`,
  `technical-writer` to `gpt-5.6-terra` / `medium`, and `test-engineer` to
  `gpt-5.6-luna` / `xhigh`; other specialist profiles retain their existing
  model and reasoning settings.
- Strengthened the portable instructions and existing CX contracts around
  constraint-preserving fallbacks, terminal artifacts and critical gates for
  persistent work, failure-topology evidence, repeated-symptom diagnosis,
  destructive-cleanup proof, restoration fidelity, first-party source use,
  and quantitative evidence basis. Runtime routing remains based on task
  state, evidence, risk, and execution conditions rather than model names.
- Extended `cx-coding-agent-sessions` with recorded model and reasoning-effort
  history, `--reasoning-effort`, root/subagent/internal labels, default
  filtering of host-internal sessions with `excluded_internal_count`, and lazy
  rollout hydration when older SQLite metadata is stale. The finder now keeps
  the rollout's first `session_meta.payload.id` authoritative so inherited
  parent metadata cannot collapse child sessions into the root.
- Hardened `cx-insane-search` challenge classification with identifier-boundary
  matching, decisive Cloudflare structure markers, large-document soft-mention
  handling, and filtering against the installed `curl_cffi` impersonation set;
  recorded the exact selective-refresh commit without mislabeling the original
  conversion snapshot.
- Strengthened `cx-design-director` reference extraction with explicit lanes
  for observed facts, inferred behavior, new first-party decisions and
  unresolved gaps, including scoped CSS declaration and variable-chain
  provenance. The selected `fivetaku/insane-design` method source is pinned and
  licensed without importing its runtime or corpus.
- Fixed the portable governance pointer: global instructions now read
  `skills/CX_SKILLS.md` from a Highfloor repository checkout and state the
  constraint when no checkout exists, instead of referencing an installed path
  that install-managed setups never create. Corrected the governance
  document's claim about installed copies to match installer behavior.
- Added optional batched questioning rounds with per-question recommended
  answers and an opt-in durable decision-record handoff to `cx-interview`,
  and recorded grill/stress-test triggers in its description.
- Compressed hot-spot-first scoping, shallow-module friction signals, the
  deletion test, Strong/Worth exploring/Speculative grading, domain-vocabulary
  seam naming, and decision-record non-re-litigation into the `architect`
  agent's instructions.
- Added surface-intent classification and a no-polish-on-discarded-direction
  rule to `cx-design-director`, a post-fix evidence recapture bound to
  `cx-visual-qa`, and a batched UI verification pass budget plus an
  open-ended polish-loop anti-pattern to the workflow recipes.
- Recorded `mattpocock/skills` and `uizze/uizze` (`anti-ui-slop`) as pinned
  method sources whose selected concepts are condensed into existing owners
  (modified derivative), with MIT license texts bundled at the repository root
  and inside each affected skill; no executable upstream source is
  redistributed.

## [0.2.0] - 2026-08-10

This is a compatible minor release from `0.1.0`. It adds two skills without
removing or renaming existing managed skills or agents. Existing installations
can update in place; global-instruction synchronization remains optional and
conflict-aware.

### Added

- Added `CODEX_AGENTS.md` as a portable English reference for the
  maintainer's global Codex instructions while keeping repository runtime
  rules in `AGENTS.md`.
- Added `cx-analyze-video`, adapted from `bradautomates/claude-video`, for
  timestamp-aligned frame and caption analysis with explicit external-upload
  consent and guarded cleanup.
- Added `cx-understand-codebase`, adapted from `Egonex-AI/Understand-Anything`,
  with deterministic scanning, an evidence-backed architecture graph, and a
  token-gated local interactive dashboard.

### Changed

- Standardized every `cx-*` skill's UI metadata on an English `CX ...` display
  name, 25–64 character English short description, and English `$cx-*` default
  prompt, with canonical governance and validator coverage to prevent drift.
- Added conflict-aware optional synchronization from `CODEX_AGENTS.md` to
  `$CODEX_HOME/AGENTS.md`: install when absent, prompt before replacing an
  existing file, preserve it in non-interactive mode, verify accepted
  replacements before deleting their temporary backups, restore the previous
  file after replacement failure, and leave it outside `doctor` and `uninstall`
  ownership.
- Made managed skill and agent replacement transactional: verify the repository
  copy, discard the temporary backup after success, and automatically restore
  the previous installed copy after copy or verification failure. Persistent
  backups remain limited to retirement, uninstall, or failed rollback and
  cleanup recovery.
- Added a conditional Art Direction Loop to `cx-design-director` for producing
  and converging on a few materially distinct, feasible visual directions
  without imposing exploration on restoration, small polish or already-decided
  first-party systems.
- Strengthened `cx-design-director` and `cx-visual-qa` with independently
  worded layout ownership, interaction-continuity, stress-coverage and visual
  claim boundaries after a research-only review of `changeroa/StyleGallery`;
  no StyleGallery corpus, CLI or MCP is bundled.
- Integrated the four `multica-ai/andrej-karpathy-skills` guidance concepts
  into the existing implementation sections of `CODEX_AGENTS.md` and the
  maintainer's synchronized global instructions without adding duplicate rules.
- Standardized imported Claude slash-command surfaces on Codex skill invocation:
  `$cx-analyze-video` and `$cx-understand-codebase` with trailing action words.
- Canonicalized both new skills under the `cx-*` namespace before release;
  their temporary staging names have no compatibility aliases.
- Kept `cx-understand-codebase` runtime artifacts out of installer-managed skill
  source by preparing its pinned workspace in a source-versioned user cache.
- Excluded persistent `.ua/` and legacy `.understand-anything/` artifacts from
  codebase scans so previous analysis cannot become source evidence.
- Excluded local `.git` metadata from repository hygiene scanning while keeping
  generated artifacts and machine-specific paths in repository content blocked.
- Strengthened repository validation for the `cx-*` namespace,
  `agents/openai.yaml`, exact catalog cards, live inventory counts, and
  per-skill provenance coverage.
- Separated the README language selector from its section navigation.
- Strengthened `cx-interview` with conditional multi-surface coverage,
  non-monotonic readiness, and explicit approval for removing or substituting
  confirmed requirements; recorded Gajae Code `v0.12.0` as a research-only
  provenance refresh.
- Hardened `cx-insane-search` with fail-closed DNS resolution, curl address
  pinning, guarded redirects and Phase 0 routes, local browser execution
  disabled at the public fetch boundary with an explicit host-browser handoff,
  opt-in persistent state, and a compact single-fetch retrieval evidence
  handoff.
- Strengthened `cx-ultraresearch` with claim-relative source assessment,
  lineage-based independence, selective countersearch, explicit
  `supported` / `unresolved` / `refuted` states, and lightweight composition
  with `cx-insane-search`; recorded `fivetaku/insane-research` as a selected
  method source without importing its fixed orchestration or validators.

## [0.1.0] - 2026-07-28

First public release.

### Added

- Public repository structure and governance.
- Unified install, update, doctor, and uninstall script.
- English and Korean project documentation.
- Repository, skill, agent, manifest, and installer validation.
- Release consistency validation and a maintainer release checklist.
- GitHub issue forms, pull-request template, and CI.
- README banner and open-source community policies.

### Changed

- Moved installable CX skills under `skills/`.
- Expanded the root license scope for original project content while preserving
  component-level upstream licenses.
- Standardized repository Markdown on English, with Korean in `README_KR.md`.
- Restored the canonical slogan, goal, and
  `Hard Floor → Soft Scaffold → Open Ceiling` philosophy in the README.
- Added the project's positive-guardrail and human-judgment principles, with a
  clear distinction between the current kit and its future harness direction.
- Clarified that the philosophy's details may evolve while
  `Hard Floor → Soft Scaffold → Open Ceiling` remains its stable backbone.
- Reworked the README around plain-language orientation, quick installation,
  skills, agents, and composable workflows.
- Added the project's origin, human-led model-assisted design process, and the
  domain-knowledge boundary for high-quality automation.
- Rewrote skill, agent, and workflow summaries as short complete sentences and
  aligned the interview workflow with its three actual exit choices.
- Restored compact workflow diagrams while retaining plain-language actions
  and the interview skill's three real exits.
- Added a concise upstream-to-Highfloor adaptation map for every current skill
  family while keeping exact provenance in the existing detailed records.
- Standardized default installation under `$CODEX_HOME/skills` and
  `$CODEX_HOME/agents`, with explicit state, backup, update, and retirement
  semantics.
- Promoted the selected v3 banner direction to the canonical README asset.
- Generalized local-path validation so it detects arbitrary macOS and Linux
  home directories instead of one maintainer username.

### Removed

- Generated Python cache files and machine-specific metadata.
