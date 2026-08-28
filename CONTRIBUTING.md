# Contributing

Thank you for helping improve Highfloor for Codex.

## Before opening a change

- Search existing issues and pull requests.
- Read the root `AGENTS.md`.
- For any `cx-*` skill change, read `skills/CX_SKILLS.md`.
- Identify whether the change affects runtime behavior, distribution,
  documentation, provenance, or only formatting.
- For a proposed skill, identify the ownership gap, held-out task, maintenance
  surfaces, and existing behavior it replaces or cannot reuse. `NO_CHANGE` is
  the correct outcome when the proposal adds no unique value.
- Open an issue first for new skills, new agents, renames, removals, installer
  ownership changes, or license-boundary changes.

Small corrections and focused bug fixes may go directly to a pull request.

## Development setup

No dependency installation is required for the core repository checks.

```sh
git clone https://github.com/BongSuCHOI/highfloor-codex.git
cd highfloor-codex
./scripts/validate.sh
./scripts/test-install.sh
```

Repository validation requires Python 3.11+ because it uses the standard
library's `tomllib`. Runtime installation itself requires only POSIX shell and
standard system tools.

## Change types

### Skill changes

Describe:

- owned artifact or decision;
- trigger and non-trigger;
- method and evidence contract;
- stop and fallback conditions;
- permissions and destructive boundaries;
- relationship to adjacent skills;
- upstream source, license, and modification status;
- context, routing, catalog, installer, documentation, test, and upstream
  maintenance cost.

Keep `SKILL.md` concise enough for progressive disclosure. Put deep method,
examples, and provenance in `references/` when appropriate.

### Agent changes

Preserve one narrow role. The filename stem and `name` should match. Explain:

- why delegation is useful;
- read/write authority;
- expected inputs and output;
- stop condition;
- chosen model and reasoning effort;
- overlap with existing agents.

### Installer changes

Preserve these invariants:

- exact manifest ownership;
- unrelated user entries remain untouched;
- conflicts and retired managed entries are backed up;
- update and install share reconciliation;
- uninstall removes only recorded managed entries;
- path changes fail safely;
- remote download failures stop installation.

Update `scripts/test-install.sh` for behavior changes.

### Documentation changes

English Markdown is canonical except `README_KR.md`. Keep the two READMEs
semantically aligned for user-facing behavior. Preserve exact technical
identifiers and use repository-relative links.

## Pull requests

A pull request should contain:

- a concise problem statement;
- the chosen change and why it is the smallest sufficient one;
- scope and non-goals;
- verification evidence;
- license/provenance impact;
- migration or rollback notes when behavior changes.

Keep unrelated cleanup out of the same pull request.

## Commit messages

Use imperative, scoped subjects:

```text
installer: keep managed destinations under CODEX_HOME
docs: explain event-driven workflow routing
agents: add database migration handoff boundary
skills(cx-debugging): clarify stop condition
```

The body should explain why when the reason is not obvious from the diff.
Conventional Commits are welcome but not required.

## Merge policy

- Pull requests require passing repository validation.
- Runtime-contract, installer, security, or license changes should receive
  maintainer review.
- Squash merge is the default for ordinary changes.
- Merge commits are reserved for release branches or intentionally meaningful
  multi-commit history.
- Rebase merge may be used for a clean series whose individual commits are each
  reviewable and useful.

## Version and changelog

Update `CHANGELOG.md` for user-visible changes. Maintainers update `VERSION`
during release preparation:

- patch: compatible fixes and documentation;
- minor: compatible capabilities and new entries;
- major: incompatible names, ownership, contracts, or license boundaries.

The complete maintainer sequence, licensing audit, migration review, tag
procedure, and publication check are in
[`docs/RELEASING.md`](docs/RELEASING.md).

## Provenance

Do not paste a third-party skill, prompt, dataset, script, or substantial text
without:

1. the exact upstream project and version/commit when known;
2. the upstream license;
3. a bundled license copy when redistribution requires it;
4. a modification notice;
5. an entry in `THIRD_PARTY_NOTICES.md`.

When provenance cannot be proven, do not publish the component as original.
Pure research references that contribute no copied source or wording remain in
the applicable per-skill provenance and migration manifest; do not present them
as redistributed components.

## Reporting security issues

Do not open a public issue for a vulnerability. Follow `SECURITY.md`.
