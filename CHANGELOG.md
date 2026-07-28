# Changelog

All notable changes to Highfloor for Codex will be documented here.

The project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
