# Changelog

All notable changes to Highfloor for Codex will be documented here.

The project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
