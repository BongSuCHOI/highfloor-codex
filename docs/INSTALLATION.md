# Installation and Updates

This document describes the installer contract, destination selection, updates,
recovery, and removal.

## Trust choices

Choose the installation method that matches the machine:

| Method | Best for | Trade-off |
|---|---|---|
| Clone, inspect, run | Production, shared, or security-sensitive machines | More steps; strongest reviewability |
| Pinned release URL | Reproducible personal installation | Must select and update a tag |
| `main` URL | Fast evaluation of the latest repository | Content can change between runs |
| Local archive or clone | Offline or restricted environment | You own source transfer and integrity |

Review-first:

```sh
git clone https://github.com/BongSuCHOI/highfloor-codex.git
cd highfloor-codex
git checkout v0.2.0
less install.sh
./install.sh
```

Pinned remote:

```sh
curl -fsSL https://raw.githubusercontent.com/BongSuCHOI/highfloor-codex/v0.2.0/install.sh \
  | HIGHFLOOR_REF=v0.2.0 sh
```

Latest remote:

```sh
curl -fsSL https://raw.githubusercontent.com/BongSuCHOI/highfloor-codex/main/install.sh | sh
```

## Actions

```text
install     Install or reconcile all manifest entries.
update      Alias for install; useful for intent and documentation.
doctor      Verify that every recorded managed entry still exists.
uninstall   Back up and remove only recorded managed entries.
```

The same implementation performs install and update. This prevents the initial
installation and later reconciliation from drifting into different behavior.

## Options

```text
--repo OWNER/REPO
--ref BRANCH_OR_TAG_OR_COMMIT
--skills-dir PATH
--agents-dir PATH
--global-instructions ask|replace|keep
--dry-run
-h, --help
```

When an option must pass through a shell pipe, place it after `sh -s --`:

```sh
curl -fsSL https://raw.githubusercontent.com/BongSuCHOI/highfloor-codex/main/install.sh \
  | sh -s -- update --dry-run
```

## Environment variables

| Variable | Purpose | Default |
|---|---|---|
| `CODEX_HOME` | Codex configuration root | `$HOME/.codex` |
| `HIGHFLOOR_REPO` | Remote GitHub source | `BongSuCHOI/highfloor-codex` |
| `HIGHFLOOR_REF` | Remote branch, tag, or commit | `main` |
| `HIGHFLOOR_SKILLS_DIR` | Explicit skills destination | `$CODEX_HOME/skills` |
| `HIGHFLOOR_AGENTS_DIR` | Explicit agents destination | `$CODEX_HOME/agents` |
| `HIGHFLOOR_GLOBAL_INSTRUCTIONS` | Global instruction policy: `ask`, `replace`, or `keep` | `ask` |
| `HIGHFLOOR_STATE_DIR` | Install state and backup root | `$CODEX_HOME/highfloor-codex` |

Example with a fork:

```sh
curl -fsSL https://raw.githubusercontent.com/your-name/highfloor-codex/main/install.sh \
  | HIGHFLOOR_REPO=your-name/highfloor-codex HIGHFLOOR_REF=main sh
```

## Default destinations

The installer uses one predictable Codex root:

```text
skills: $CODEX_HOME/skills
agents: $CODEX_HOME/agents
optional instructions: $CODEX_HOME/AGENTS.md
```

With the default `CODEX_HOME`, those paths are `~/.codex/skills` and
`~/.codex/agents`. The installer does not use `$HOME/.agents/skills` unless you
explicitly pass that path through `--skills-dir` or
`HIGHFLOOR_SKILLS_DIR`. If your Codex build uses another location, override it
explicitly.

## Optional global instructions

`CODEX_AGENTS.md` is the portable repository source for Codex global
instructions. Install and update handle `$CODEX_HOME/AGENTS.md` according to
`--global-instructions`:

- `ask` (default): install when the target is absent; when a different regular
  file exists, ask through the controlling terminal before replacement;
- `replace`: install or replace without prompting, using a temporary backup for
  an existing regular file;
- `keep`: do not create or change the target.

An identical target is left alone. In default `ask` mode, a non-interactive
conflict preserves the existing file and prints the explicit opt-in command.
Symlinks and other non-regular targets are preserved in `ask` mode and rejected
in `replace` mode.

Examples:

```sh
./install.sh update --global-instructions keep
./install.sh update --global-instructions replace
```

For a pipeline:

```sh
curl -fsSL https://raw.githubusercontent.com/BongSuCHOI/highfloor-codex/main/install.sh \
  | sh -s -- update --global-instructions replace
```

This copy is an explicit user-level configuration choice, not a manifest-owned
runtime entry. `doctor` does not judge its content and `uninstall` does not
remove or restore it. A replacement is compared with `CODEX_AGENTS.md` after
copying. Its temporary `instructions/AGENTS.md` backup is deleted only after
that verification succeeds. Copy or verification failure restores and verifies
the previous file before reporting the error. The backup remains only when that
rollback or subsequent backup cleanup cannot finish safely.

## Skill-specific runtimes

The Highfloor installer copies skill source; it does not install system or
project dependencies.

- `cx-analyze-video` requires Python 3.11+, `ffmpeg`, and `ffprobe`. Public URLs
  also require `yt-dlp`; local video files do not. Its setup script reports
  missing binaries and suggestions but never runs an installer.
- `cx-understand-codebase` requires Node.js 22+ and `npx`. On first use, its
  runtime wrapper resolves pinned `pnpm@10.6.2` packages from the vendored
  frozen lockfile into
  `${XDG_CACHE_HOME:-$HOME/.cache}/highfloor/cx-understand-codebase/<revision>`.
  It never adds packages to the analyzed repository or installer-managed skill
  source. Set `HIGHFLOOR_UNDERSTAND_RUNTIME_DIR` to an explicit absolute path
  when a different cache location is required.

The installer does not own or remove this optional runtime cache. Run
`<skill>/scripts/prepare-runtime.sh path` to resolve the exact active path before
performing a separate cache cleanup.

Network, registry, cache, and build failures remain explicit runtime errors.
They are not treated as proof that Node.js or another dependency is absent.

## Ownership boundary

Only entries in these files are lifecycle-managed:

- `manifest/skills.txt`
- `manifest/agents.txt`

The optional global-instruction copy described above is not added to either
manifest. The installer never synchronizes an entire user directory. For each
manifest entry it:

1. validates the entry name;
2. compares the source and installed target;
3. skips an identical target;
4. creates a temporary backup for a conflicting target;
5. replaces and verifies only that exact target;
6. removes the temporary backup after success, or restores it after failure.

For a skill, the exact target is the whole named skill directory. A difference
in one internal file causes that directory to be replaced and verified as a
unit. Custom agents are compared, replaced, and verified as individual TOML
files. A verified replacement retains only the repository version; a failed
replacement restores the previous installed copy.

When a release removes a previously managed entry, update backs up and removes
that exact retired entry. Removing an entry from the repository manifest does
not preserve the installed copy as unmanaged content. There is no per-entry
opt-out in the current installer. Keep local variants in a fork or under a
different namespace. Unrelated siblings remain untouched.

## Backups and state

The default state root is:

```text
$CODEX_HOME/highfloor-codex/
├── agents-dir
├── agents.txt
├── backups/
│   └── YYYYMMDDTHHMMSSZ-PID/
│       ├── agents/                # removal backup or failed rollback recovery
│       ├── instructions/          # retained only when rollback cannot finish
│       │   └── AGENTS.md
│       └── skills/                # removal backup or failed rollback recovery
├── ref
├── skills-dir
├── skills.txt
└── version
```

Temporary replacement backups for managed skills, agents, and optional global
instructions are removed after content verification. Copy or verification
failure restores the prior target and then removes the verified rollback copy.
A backup remains only if rollback or backup cleanup cannot finish safely.

Retired-entry and uninstall backups are not pruned automatically because those
operations intentionally remove their targets. Users may remove those old
timestamped backups after inspection. Backups created by older installer
versions are also left untouched because the state does not record whether each
one came from replacement, retirement, or uninstall.

The state directory is not a third install destination. It records the
installed version and source ref, the two destinations, and the exact
manifests used by `doctor`, later updates, and uninstall. Timestamped backups
normally remain there only for retired entries and uninstall removals.

## Updates

From a clone:

```sh
git pull --ff-only
./install.sh update
./install.sh doctor
```

From a release:

```sh
curl -fsSL https://raw.githubusercontent.com/BongSuCHOI/highfloor-codex/v0.2.0/install.sh \
  | HIGHFLOOR_REF=v0.2.0 sh -s -- update
```

Changing the selected source ref does not change the destination. If you try to
change a destination while recorded state exists, the installer stops. Run
uninstall first, then install to the new path. This avoids orphaning managed
entries in an old location.

For every name in the new manifest, update compares the installed entry with
the selected repository ref. An identical entry is left alone. A different
entry is replaced and verified through a temporary backup transaction. Success
deletes the backup; copy or verification failure restores the prior installed
copy and reports the rollback. An entry that appeared in the previous recorded
manifest but no longer appears in the new one is backed up and removed. Files
outside the recorded manifests are not touched.
Global instructions follow the separate `ask`, `replace`, or `keep` choice and
remain outside recorded uninstall ownership.

## Offline installation

Copy or extract a reviewed repository release to the target machine, then:

```sh
cd highfloor-codex
./install.sh --dry-run
./install.sh
```

When a complete local repository is detected beside `install.sh`, no network
request is made.

## Doctor

```sh
./install.sh doctor
```

`doctor` verifies the recorded presence of every managed skill `SKILL.md` and
agent TOML file. It does not claim that a specific Codex product surface has
loaded or successfully executed them; that requires observing the host after a
restart.

## Uninstall

```sh
./install.sh uninstall --dry-run
./install.sh uninstall
```

Uninstall:

- reads the recorded destinations and manifests;
- backs up existing managed entries;
- removes only those exact entries;
- retains install state and backups.

It leaves `$CODEX_HOME/AGENTS.md` unchanged even when the installer previously
copied or replaced it.

To restore an entry, copy it from the latest timestamped backup into the
recorded destination.

## Troubleshooting

### Skills do not appear

1. Run `./install.sh doctor`.
2. Check the printed skills destination.
3. Restart Codex.
4. Confirm your Codex build's personal-skills directory.
5. Reinstall with `--skills-dir` if the host uses another path.

### Agents do not appear

1. Confirm files exist under `${CODEX_HOME:-$HOME/.codex}/agents`.
2. Restart Codex.
3. Check whether your Codex surface supports custom agents.
4. Verify that the configured model names are available to the account.

### A local customization was replaced

The previous target should exist under:

```text
${CODEX_HOME:-$HOME/.codex}/highfloor-codex/backups/<timestamp>/
```

Restore the desired file, then keep the customization in a fork or use a
different local name so future managed updates do not own it.

### Remote install fails

The installer fails closed on `curl` or archive errors. Check network access,
repository visibility, `HIGHFLOOR_REPO`, and `HIGHFLOOR_REF`. It does not fall
back to an unrelated source.
