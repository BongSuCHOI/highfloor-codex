# Repository Architecture

## Project state and direction

Highfloor is currently a Codex skill and custom-agent kit. It is not yet an
agent harness. The repository starts with components that are useful on their
own while keeping a clear direction for a future runtime.

Anything built under the Highfloor name should preserve the same design test:

- maintain a small hard floor for authority, evidence, safety, cost, and
  provenance;
- guide less capable models with clear positive actions rather than a maze of
  prohibitions;
- leave stronger models room to reason beyond the default path;
- ask for human judgment where authority or consequences materially change,
  not at every harmless intermediate step.

## Distribution units

Highfloor contains two runtime units:

1. **Skills** — directories whose required entry point is `SKILL.md`.
2. **Custom agents** — TOML definitions with `name`, `description`, and
   `developer_instructions`.

Repository governance, catalogs, CI, and artwork are not installed into the
runtime directories.

## Source-to-runtime mapping

```text
skills/cx-*/  ───────────────→ $CODEX_HOME/skills/cx-*
agents/*.toml ───────────────→ $CODEX_HOME/agents/*.toml

manifest/*.txt
      │
      ├── defines exact ownership
      ├── drives validation
      ├── drives install/update
      └── is copied into install state for uninstall
```

## Why manifests instead of directory synchronization?

A user's skills and agents directories are shared extension surfaces. Deleting
or mirroring the whole directory would turn a package update into an ownership
violation. Plain-text manifests make the managed set:

- inspectable before execution;
- reviewable in pull requests;
- usable by install, update, doctor, uninstall, tests, and CI;
- independent of unrelated local entries.

## Why one installer?

Separate install and update scripts tend to diverge. Highfloor models both as
reconciliation from a selected source state. The `update` action is an explicit
alias, not a second code path.

## Why no plugin package yet?

Codex plugins are a strong distribution mechanism for reusable extensions, but
the current kit also distributes personal custom-agent TOML definitions.
The first release keeps ownership across the skills and agents surfaces visible
through a reviewable installer.

A future plugin or harness release should be additive and separately versioned
unless its distribution contract can represent both runtime units without
changing their semantics. Runtime routing, intervention, recovery, and approval
mechanisms belong to that future layer; the philosophy above already governs
how they should be judged.

## Governance layers

| Layer | Owner |
|---|---|
| Repository contribution rules | root `AGENTS.md`, `CONTRIBUTING.md` |
| Release procedure | `docs/RELEASING.md` |
| CX family architecture and migration | `skills/CX_SKILLS.md` |
| Runtime behavior | each `SKILL.md` or agent TOML |
| Distribution ownership | `manifest/*.txt`, `install.sh` |
| License and provenance | `LICENSE`, `THIRD_PARTY_NOTICES.md`, per-skill references |
| Verification | `scripts/validate_repo.py`, `scripts/test-install.sh`, CI |

## Compatibility policy

Names are public interfaces:

- skill directory name must match skill frontmatter `name`;
- agent filename stem should match agent `name`;
- renamed or removed entries require migration guidance and a major version
  unless the item was never released.

Runtime contracts may evolve compatibly when triggers, permission boundaries,
and owned artifacts remain stable. Material behavior changes belong in the
changelog.
