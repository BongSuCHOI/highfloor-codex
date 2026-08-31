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

## Runtime / governance evidence

<!-- Complete only when this PR changes routing, instructions, skills, agents,
or workflow behavior. Leave as not applicable for ordinary docs/format fixes. -->

- Baseline:
- Treatment:
- Held-out / independent evidence:
- Decision or failure gap addressed:
- Why `NO_CHANGE` / absorption is insufficient:
- Added routing / context / coordination cost:
- Kill or rollback condition:

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
