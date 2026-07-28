## Problem

<!-- What concrete problem or failure mode does this change address? -->

## Change

<!-- What changed, and why is this the smallest sufficient solution? -->

## Scope and non-goals

<!-- State important boundaries and intentionally excluded work. -->

## Verification

<!-- Include exact focused commands and observed results. -->

- [ ] `./scripts/validate.sh`
- [ ] `./scripts/test-install.sh` when installer, manifest, skill, agent, or release behavior changed
- [ ] Required behavior not observed is labeled `NOT_PROVEN`

## Runtime and migration impact

<!-- Names, triggers, authority, paths, update behavior, rollback, compatibility. -->

## Provenance and license

<!-- State no impact, or list source/version/license/modification notice changes. -->

## Checklist

- [ ] I read the root `AGENTS.md`.
- [ ] I read `skills/CX_SKILLS.md` if a `cx-*` skill changed.
- [ ] I preserved unrelated user and repository changes.
- [ ] I updated `CHANGELOG.md` for user-visible behavior.
- [ ] English docs are canonical and `README_KR.md` remains aligned where relevant.
- [ ] No secrets, private transcripts, caches, or local absolute paths were added.
