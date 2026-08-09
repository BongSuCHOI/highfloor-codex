#!/bin/sh

set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
TEST_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/highfloor-install-test.XXXXXX")"
TEST_HOME="$TEST_ROOT/home"
TEST_CODEX="$TEST_ROOT/codex"
TEST_SKILLS="$TEST_ROOT/skills"
TEST_AGENTS="$TEST_ROOT/agents"
STATE_ROOT="$TEST_CODEX/highfloor-codex"

cleanup() {
  rm -rf "$TEST_ROOT"
}
trap cleanup EXIT HUP INT TERM

mkdir -p "$TEST_HOME" "$TEST_CODEX" "$TEST_SKILLS" "$TEST_AGENTS"

HOME="$TEST_HOME" \
CODEX_HOME="$TEST_CODEX" \
"$ROOT/install.sh" install \
  --skills-dir "$TEST_SKILLS" \
  --agents-dir "$TEST_AGENTS" \
  --global-instructions keep

while IFS= read -r entry || [ -n "$entry" ]; do
  [ -f "$TEST_SKILLS/$entry/SKILL.md" ] || {
    printf 'missing installed skill: %s\n' "$entry" >&2
    exit 1
  }
done < "$ROOT/manifest/skills.txt"

while IFS= read -r entry || [ -n "$entry" ]; do
  [ -f "$TEST_AGENTS/$entry" ] || {
    printf 'missing installed agent: %s\n' "$entry" >&2
    exit 1
  }
done < "$ROOT/manifest/agents.txt"

mkdir -p "$TEST_SKILLS/user-skill"
: > "$TEST_SKILLS/user-skill/SKILL.md"
: > "$TEST_AGENTS/user-agent.toml"

printf '\n# local mutation\n' >> "$TEST_SKILLS/cx-interview/SKILL.md"

HOME="$TEST_HOME" \
CODEX_HOME="$TEST_CODEX" \
"$ROOT/install.sh" update \
  --skills-dir "$TEST_SKILLS" \
  --agents-dir "$TEST_AGENTS" \
  --global-instructions keep

cmp -s "$ROOT/skills/cx-interview/SKILL.md" "$TEST_SKILLS/cx-interview/SKILL.md" || {
  printf 'managed skill was not reconciled\n' >&2
  exit 1
}

[ -f "$TEST_SKILLS/user-skill/SKILL.md" ] || {
  printf 'unrelated skill was removed\n' >&2
  exit 1
}
[ -f "$TEST_AGENTS/user-agent.toml" ] || {
  printf 'unrelated agent was removed\n' >&2
  exit 1
}

find "$STATE_ROOT/backups" -path '*/skills/cx-interview/SKILL.md' -type f \
  | grep -q . || {
    printf 'changed managed skill was not backed up\n' >&2
    exit 1
  }

printf '# existing user instructions\n' > "$TEST_CODEX/AGENTS.md"

HOME="$TEST_HOME" \
CODEX_HOME="$TEST_CODEX" \
"$ROOT/install.sh" update \
  --skills-dir "$TEST_SKILLS" \
  --agents-dir "$TEST_AGENTS" \
  --global-instructions replace \
  > "$TEST_ROOT/global-replace.log"

cmp -s "$ROOT/CODEX_AGENTS.md" "$TEST_CODEX/AGENTS.md" || {
  printf 'explicit global instructions replacement failed\n' >&2
  exit 1
}

grep -Fq 'Creating temporary global instructions backup' \
  "$TEST_ROOT/global-replace.log" || {
    printf 'global instructions replacement did not create a temporary backup\n' >&2
    exit 1
  }
grep -Fq 'Removing verified temporary global instructions backup' \
  "$TEST_ROOT/global-replace.log" || {
    printf 'global instructions replacement was not verified before cleanup\n' >&2
    exit 1
  }
if find "$STATE_ROOT/backups" -path '*/instructions/AGENTS.md' -type f \
  | grep -q .; then
  printf 'successful global instructions replacement retained its temporary backup\n' >&2
  exit 1
fi

printf '# preserved without a terminal\n' > "$TEST_CODEX/AGENTS.md"

HOME="$TEST_HOME" \
CODEX_HOME="$TEST_CODEX" \
"$ROOT/install.sh" update \
  --skills-dir "$TEST_SKILLS" \
  --agents-dir "$TEST_AGENTS" \
  > "$TEST_ROOT/non-interactive-install.log"

grep -Fqx '# preserved without a terminal' "$TEST_CODEX/AGENTS.md" || {
  printf 'default non-interactive mode changed global instructions\n' >&2
  exit 1
}
grep -Fq 'use --global-instructions replace to opt in' \
  "$TEST_ROOT/non-interactive-install.log" || {
    printf 'default non-interactive mode did not explain its safe fallback\n' >&2
    exit 1
  }

printf '# preserved after explicit keep\n' > "$TEST_CODEX/AGENTS.md"

HOME="$TEST_HOME" \
CODEX_HOME="$TEST_CODEX" \
"$ROOT/install.sh" update \
  --skills-dir "$TEST_SKILLS" \
  --agents-dir "$TEST_AGENTS" \
  --global-instructions keep

grep -Fqx '# preserved after explicit keep' "$TEST_CODEX/AGENTS.md" || {
  printf 'global instructions keep mode changed the target\n' >&2
  exit 1
}

HOME="$TEST_HOME" CODEX_HOME="$TEST_CODEX" "$ROOT/install.sh" doctor

HOME="$TEST_HOME" CODEX_HOME="$TEST_CODEX" "$ROOT/install.sh" uninstall

while IFS= read -r entry || [ -n "$entry" ]; do
  [ ! -e "$TEST_SKILLS/$entry" ] || {
    printf 'managed skill survived uninstall: %s\n' "$entry" >&2
    exit 1
  }
done < "$ROOT/manifest/skills.txt"

while IFS= read -r entry || [ -n "$entry" ]; do
  [ ! -e "$TEST_AGENTS/$entry" ] || {
    printf 'managed agent survived uninstall: %s\n' "$entry" >&2
    exit 1
  }
done < "$ROOT/manifest/agents.txt"

[ -f "$TEST_SKILLS/user-skill/SKILL.md" ] || {
  printf 'unrelated skill did not survive uninstall\n' >&2
  exit 1
}
[ -f "$TEST_AGENTS/user-agent.toml" ] || {
  printf 'unrelated agent did not survive uninstall\n' >&2
  exit 1
}

grep -Fqx '# preserved after explicit keep' "$TEST_CODEX/AGENTS.md" || {
  printf 'uninstall changed optional global instructions\n' >&2
  exit 1
}

FRESH_HOME="$TEST_ROOT/fresh-home"
FRESH_CODEX="$FRESH_HOME/.codex"
mkdir -p "$FRESH_HOME"

HOME="$FRESH_HOME" CODEX_HOME= "$ROOT/install.sh" install

[ -f "$FRESH_CODEX/skills/cx-interview/SKILL.md" ] || {
  printf 'default install did not use the CODEX_HOME skills path\n' >&2
  exit 1
}
[ -f "$FRESH_CODEX/agents/planner.toml" ] || {
  printf 'default install did not use the CODEX_HOME agents path\n' >&2
  exit 1
}
[ -f "$FRESH_CODEX/AGENTS.md" ] || {
  printf 'default global instructions install did not create AGENTS.md\n' >&2
  exit 1
}
cmp -s "$ROOT/CODEX_AGENTS.md" "$FRESH_CODEX/AGENTS.md" || {
  printf 'installed global instructions differ from CODEX_AGENTS.md\n' >&2
  exit 1
}

for state_file in version ref skills-dir agents-dir skills.txt agents.txt; do
  [ -f "$FRESH_CODEX/highfloor-codex/$state_file" ] || {
    printf 'default install did not record state file: %s\n' "$state_file" >&2
    exit 1
  }
done

HOME="$FRESH_HOME" CODEX_HOME= "$ROOT/install.sh" uninstall

[ -f "$FRESH_CODEX/AGENTS.md" ] || {
  printf 'uninstall removed optional global instructions\n' >&2
  exit 1
}

printf 'Installer lifecycle test passed.\n'
