# Repository Architecture

## Project state and direction

Highfloor is currently a Codex skill and custom-agent kit. It is not yet an
agent harness. The repository starts with components that are useful on their
own while keeping a clear direction for a future runtime.

Anything built under the Highfloor name should preserve the same design test:

- maintain a small hard floor for authority, evidence, safety, cost, and
  provenance;
- adapt scaffolding to task state, evidence, risk, and execution conditions;
  model names and reasoning-effort labels remain evaluation dimensions, not
  runtime branches;
- guide uncertain or under-specified work with clear positive actions rather
  than a maze of prohibitions;
- remove or compress procedure when its owned question is already closed by
  authoritative evidence or an equal-or-stronger proof;
- ask for human judgment where authority or consequences materially change,
  not at every harmless intermediate step;
- treat `NO_CHANGE` as a successful result when no necessary improvement
  exists, and prefer absorbing or pruning behavior over growing the catalog.


## Operational semantics

Highfloor distinguishes four runtime concepts:

- **Skill** — a task-state procedure or evidence method loaded into the current
  reasoning context. A skill owns how to close one class of unresolved question.
- **Agent** — a delegated execution, isolation, or authority boundary. An agent
  owns a separated responsibility and returns evidence or an artifact to the
  parent thread.
- **Workflow** — a compositional example that connects owners for a recurring
  state transition. It is not a mandatory lifecycle.
- **Model profile** — a resource configuration attached to a role. Selecting a
  role may select a different model or reasoning effort, but model identity does
  not change the role's behavioral contract or Hard Floor.

## Hard Floor implementation levels

A floor requirement can be:

1. **declarative** — expressed as an instruction;
2. **mechanically enforced** — constrained by permissions, sandboxing, schemas,
   budgets, path boundaries, or approval capabilities;
3. **evidentially verified** — checked from observable results.

The current kit necessarily relies on declarative constraints in places. A
future harness should move high-consequence constraints toward mechanical
enforcement and independent verification where practical. Do not call a prose
rule mechanically enforced merely because it uses mandatory language.

## Controller complexity

Add runtime variety only for recurring task-state, authority, isolation, or
evidence distinctions that materially change behavior. More skills or agents
are not inherently better; unnecessary variety increases routing, context, and
coordination error. When two owners remain distinguishable in prose but not in
held-out outcomes, prefer the smaller controller.

## Distribution units

Highfloor contains two runtime units:

1. **Skills** — directories whose required entry point is `SKILL.md`.
2. **Custom agents** — TOML definitions with `name`, `description`, and
   `developer_instructions`.

Repository governance, catalogs, CI, and artwork are not installed into the
runtime directories.

`CODEX_AGENTS.md` is a portable instruction source, not a third managed runtime
unit. The installer may copy it to `$CODEX_HOME/AGENTS.md` when no target exists
or after explicit conflict approval. `doctor` and `uninstall` do not own that
user-level file.

## Source-to-runtime mapping

```text
skills/*/     ───────────────→ $CODEX_HOME/skills/*
agents/*.toml ───────────────→ $CODEX_HOME/agents/*.toml
CODEX_AGENTS.md ── optional ─→ $CODEX_HOME/AGENTS.md

manifest/*.txt
      │
      ├── defines exact ownership
      ├── drives validation
      ├── drives install/update
      └── is copied into install state for uninstall
```

The manifest ownership arrows apply only to skills and custom agents. Optional
global-instruction synchronization is conflict-aware, uses a temporary backup
until replacement verification succeeds, rolls back on failure, and is
intentionally excluded from recorded uninstall ownership. Managed skill and
agent replacements use the same verified temporary-backup boundary; persistent
backups are reserved for removals or incomplete rollback and cleanup recovery.

The managed agent set intentionally includes `default`, `worker`, and
`explorer`. Codex gives matching custom definitions precedence over its
built-in agents, so Highfloor can distribute portable fallback and exploration
profiles through the normal manifest lifecycle. The installer does not edit
`config.toml` or replace the user's unrelated global subagent defaults.

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
| CX family architecture and migration only | `skills/CX_SKILLS.md` |
| Runtime behavior | each `SKILL.md` or agent TOML |
| Distribution ownership | `manifest/*.txt`, `install.sh` |
| License and provenance | `LICENSE`, `THIRD_PARTY_NOTICES.md`, per-skill references |
| Comparative evaluation | `docs/EVALUATION.md`, `evals/` |
| Repository verification | `scripts/validate_repo.py`, `scripts/validate_evals.py`, `scripts/test-install.sh`, CI |

The CX portfolio records `incubating`, `active`, `sunset candidate`, and
deprecated states in `skills/CX_MIGRATION_MANIFEST.md`. Maturity does not move
or rename a runtime directory. A candidate becomes active only after it proves
a unique owner and held-out benefit; a native capability or adjacent owner may
instead absorb the useful method and leave the inventory unchanged.

## Compatibility policy

Names are public interfaces:

- skill directory name must match skill frontmatter `name`;
- agent filename stem should match agent `name`;
- renamed or removed entries require migration guidance and a major version
  unless the item was never released.

Runtime contracts may evolve compatibly when triggers, permission boundaries,
and owned artifacts remain stable. Material behavior changes belong in the
changelog.

Skill-specific runtime ownership remains explicit. `cx-analyze-video` uses host
`ffmpeg`/`ffprobe` and URL-only `yt-dlp`; external transcription is an explicit
per-video privacy and cost boundary. `cx-understand-codebase` vendors its pinned
source and lockfile in the skill, prepares resolved packages in a
source-versioned user cache, and writes only `.ua/` or an existing legacy
`.understand-anything/` directory in the analyzed target. Runtime artifacts
therefore do not mutate either the analyzed repository or installer-managed
skill source.
