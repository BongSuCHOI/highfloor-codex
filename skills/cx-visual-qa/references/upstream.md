# Upstream provenance and modification notice

This skill is a modified derivative of an Oh My OpenAgent shared skill.

- Upstream: `code-yeongyu/oh-my-openagent`
- Relevant source: `packages/shared-skills/skills/visual-qa`
- Source archive version: `4.14.0`
- Exact source commit: `NOT_PROVEN`
- License: Sustainable Use License 1.0; see `LICENSE.upstream.txt`
- Relationship: `modified derivative` with retained byte-identical scripts

Prominent modification notice:

- adapted the upstream visual QA workflow for Codex routing and scope-proportional evidence;
- added explicit `NOT_PROVEN`, browser-owner separation, and current-evidence reuse;
- retained upstream terminal and image inspection implementation material where noted by file comparison.

Additional method source:

- Reference: [`uizze/uizze`](https://github.com/uizze/uizze), `anti-ui-slop`
  skill
- Inspected commit: `3f08d874627be4d89d2af8e6409dc5e660050b5c`
- License: MIT; see `LICENSES/MIT-uizze-uizze.txt` at the repository root and
  the bundled copy `LICENSE.anti-ui-slop.txt` in this directory
- Relationship: `modified derivative` (condensed); retains upstream method
  structure and terminology where noted; no executable source is bundled

Absorbed idea (condensed): bound post-fix evidence recapture to the affected
surface with at most one confirmation round. This does not change the
Sustainable Use License obligations that govern this skill's derivative
material.

Redistribution is limited by the upstream Sustainable Use License. Copies may be provided only free of charge for non-commercial purposes.
