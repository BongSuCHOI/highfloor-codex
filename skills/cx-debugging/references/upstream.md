# Upstream provenance and modification notice

This skill is a condensed and modified derivative of an Oh My OpenAgent shared skill.

- Upstream: `code-yeongyu/oh-my-openagent`
- Relevant source: `packages/shared-skills/skills/debugging`
- Source archive version: `4.14.0`
- Exact source commit: `NOT_PROVEN`
- License: Sustainable Use License 1.0; see `LICENSE.upstream.txt`
- Relationship: `modified derivative`

Prominent modification notice:

- condensed the upstream workflow into a cause-first Codex debugging contract;
- added current trigger, non-trigger, evidence, and stop boundaries;
- removed upstream runtime-specific orchestration.

Redistribution is limited by the upstream Sustainable Use License. Copies may be provided only free of charge for non-commercial purposes.

## Method research reference

- Reference: `mattpocock/skills`
- Commit: `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`
- Relevant source: `skills/engineering/diagnosing-bugs/SKILL.md`
- License: MIT
- Relationship: `research reference`; no source or wording is bundled

Independently absorbed idea:

- treat a bounded, red-capable feedback loop for the reported symptom as the
  preferred first instrument for unclear runtime failures, while preserving a
  partial-runtime path when execution is unavailable.
