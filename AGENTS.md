# Repository Instructions

These instructions apply to all work in this repository. They are contributor
and maintainer rules for Highfloor for Codex; they are not intended to become a
user's global Codex instructions.

## Project intent

Highfloor currently distributes the Codex skills and custom agents used by its
maintainer. Its long-term direction is a harness built on the same philosophy.
Do not describe the current repository as a finished harness.

Preserve the governing model:

- **Hard Floor:** preserve the minimum guarantees for authority, scope,
  evidence, safety, cost, and provenance.
- **Soft Scaffold:** when guidance is needed, show the smallest useful path of
  positive actions, defaults, stops, and fallbacks.
- **Open Ceiling:** stronger reasoning may compress, replace, or extend the
  path while preserving the hard floor.
- **Human judgment at meaningful boundaries:** keep people in control of intent,
  risk, irreversible actions, and final accountability without making every
  harmless intermediate step wait for approval.

Wording, methods, and detailed criteria may evolve with evidence and model
capability. Treat `Hard Floor → Soft Scaffold → Open Ceiling` and
`Raise the floor. Keep the ceiling open.` as the stable backbone unless a
change explicitly reopens the project's governing philosophy.

Prefer clear desired behavior over exhaustive prohibition lists. Keep true
trust-boundary prohibitions short and explicit.

## Change boundaries

- Keep skill directory names, skill frontmatter names, custom agent names, and
  agent filenames stable unless the change explicitly includes a migration.
- Treat every `SKILL.md` as a runtime contract. Do not casually rewrite trigger,
  non-trigger, permission, stop, fallback, or evidence boundaries.
- Follow [`skills/CX_SKILLS.md`](skills/CX_SKILLS.md) before creating,
  modifying, evaluating, integrating, renaming, migrating, or deleting a
  `cx-*` skill.
- Preserve component-level upstream, modification, and license notices.
- Never imply that the root MIT license relicenses third-party or derivative
  content.
- Do not add generated caches, secrets, session logs, local absolute paths, or
  machine-specific artifacts.

## Installer invariants

- The installer owns only entries listed in `manifest/skills.txt` and
  `manifest/agents.txt`.
- It must preserve unrelated user skills and agents.
- Replaced or removed managed entries must be backed up first.
- Destination paths must be explicit, validated, and overrideable.
- Remote installation must use HTTPS, fail closed on download errors, and avoid
  executing files from outside the selected repository archive.
- `update` must be idempotent and use the same reconciliation path as
  `install`.
- `uninstall` must remove only recorded managed entries and retain recoverable
  backups.

## Documentation

- English is canonical for repository Markdown except `README_KR.md`.
- Keep `README.md` and `README_KR.md` semantically aligned when user-facing
  behavior changes.
- Preserve exact code, commands, config keys, API fields, paths, and error text.
- Distinguish current Codex documentation, observed host compatibility, project
  policy, and inference.
- Use repository-relative links. Do not commit `/Users/...` paths.

## Verification

Use the smallest evidence set that proves the change:

```sh
./scripts/validate.sh
./scripts/test-install.sh
```

Run both for installer, manifest, layout, agent, skill-frontmatter, or release
changes. For a narrow documentation-only edit, the repository validator is
usually sufficient.

For a release, follow [`docs/RELEASING.md`](docs/RELEASING.md).
`validate.sh` includes the release consistency check; do not bypass it by
updating only `VERSION` or the tag.

Do not claim `PASS` for behavior that was not observed. Use `NOT_PROVEN` when a
required host or external state is unavailable.

## Contribution discipline

- Keep changes focused and explain why behavior changed.
- Add or update tests for installer and validator behavior.
- Update `CHANGELOG.md` for user-visible changes.
- Do not add dependencies when the standard shell or Python library is enough.
- Do not combine unrelated cleanup with a functional change.
- Security-sensitive findings follow `SECURITY.md`, not public issue threads.
