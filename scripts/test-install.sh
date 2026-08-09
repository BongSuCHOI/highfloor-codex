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

REAL_CP="$(command -v cp)"
FAIL_BIN="$TEST_ROOT/fail-bin"
mkdir -p "$FAIL_BIN"
printf '%s\n' \
  '#!/bin/sh' \
  'if [ "$#" -eq 3 ] && [ "$1" = "-R" ] &&' \
  '   [ "$2" = "$HIGHFLOOR_TEST_FAIL_SOURCE" ] &&' \
  '   [ "$3" = "$HIGHFLOOR_TEST_FAIL_TARGET" ]; then' \
  '  exit 73' \
  'fi' \
  'if [ "$#" -eq 2 ] &&' \
  '   [ "$1" = "$HIGHFLOOR_TEST_FAIL_SOURCE" ] &&' \
  '   [ "$2" = "$HIGHFLOOR_TEST_FAIL_TARGET" ]; then' \
  '  exit 73' \
  'fi' \
  'exec "$HIGHFLOOR_TEST_REAL_CP" "$@"' \
  > "$FAIL_BIN/cp"
chmod +x "$FAIL_BIN/cp"

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
  --global-instructions keep \
  > "$TEST_ROOT/skill-replace.log"

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

grep -Fq 'Creating temporary skill backup: cx-interview' \
  "$TEST_ROOT/skill-replace.log" || {
    printf 'managed skill replacement did not create a temporary backup\n' >&2
    exit 1
  }
grep -Fq 'Removing verified temporary skill backup: cx-interview' \
  "$TEST_ROOT/skill-replace.log" || {
    printf 'managed skill replacement did not clean its temporary backup\n' >&2
    exit 1
  }
if find "$STATE_ROOT/backups" -path '*/skills/cx-interview' -print \
  | grep -q .; then
  printf 'successful managed skill replacement retained its temporary backup\n' >&2
  exit 1
fi

printf '\n# local agent mutation\n' >> "$TEST_AGENTS/planner.toml"

HOME="$TEST_HOME" \
CODEX_HOME="$TEST_CODEX" \
"$ROOT/install.sh" update \
  --skills-dir "$TEST_SKILLS" \
  --agents-dir "$TEST_AGENTS" \
  --global-instructions keep \
  > "$TEST_ROOT/agent-replace.log"

cmp -s "$ROOT/agents/planner.toml" "$TEST_AGENTS/planner.toml" || {
  printf 'managed agent was not reconciled\n' >&2
  exit 1
}
grep -Fq 'Creating temporary agent backup: planner.toml' \
  "$TEST_ROOT/agent-replace.log" || {
    printf 'managed agent replacement did not create a temporary backup\n' >&2
    exit 1
  }
grep -Fq 'Removing verified temporary agent backup: planner.toml' \
  "$TEST_ROOT/agent-replace.log" || {
    printf 'managed agent replacement did not clean its temporary backup\n' >&2
    exit 1
  }
if find "$STATE_ROOT/backups" -path '*/agents/planner.toml' -print \
  | grep -q .; then
  printf 'successful managed agent replacement retained its temporary backup\n' >&2
  exit 1
fi

printf '\n# rollback skill sentinel\n' >> "$TEST_SKILLS/cx-interview/SKILL.md"

if HOME="$TEST_HOME" \
  CODEX_HOME="$TEST_CODEX" \
  PATH="$FAIL_BIN:$PATH" \
  HIGHFLOOR_TEST_REAL_CP="$REAL_CP" \
  HIGHFLOOR_TEST_FAIL_SOURCE="$ROOT/skills/cx-interview" \
  HIGHFLOOR_TEST_FAIL_TARGET="$TEST_SKILLS/cx-interview" \
  "$ROOT/install.sh" update \
    --skills-dir "$TEST_SKILLS" \
    --agents-dir "$TEST_AGENTS" \
    --global-instructions keep \
    > "$TEST_ROOT/skill-rollback.log" 2>&1; then
  printf 'forced managed skill replacement failure unexpectedly succeeded\n' >&2
  exit 1
fi

grep -Fq '# rollback skill sentinel' \
  "$TEST_SKILLS/cx-interview/SKILL.md" || {
    printf 'failed managed skill replacement did not restore the prior copy\n' >&2
    exit 1
  }
grep -Fq 'skill copy failed; restored previous skill: cx-interview' \
  "$TEST_ROOT/skill-rollback.log" || {
    printf 'managed skill rollback was not reported\n' >&2
    exit 1
  }
if find "$STATE_ROOT/backups" -path '*/skills/cx-interview' -print \
  | grep -q .; then
  printf 'verified managed skill rollback retained its temporary backup\n' >&2
  exit 1
fi

printf '\n# rollback agent sentinel\n' >> "$TEST_AGENTS/planner.toml"

if HOME="$TEST_HOME" \
  CODEX_HOME="$TEST_CODEX" \
  PATH="$FAIL_BIN:$PATH" \
  HIGHFLOOR_TEST_REAL_CP="$REAL_CP" \
  HIGHFLOOR_TEST_FAIL_SOURCE="$ROOT/agents/planner.toml" \
  HIGHFLOOR_TEST_FAIL_TARGET="$TEST_AGENTS/planner.toml" \
  "$ROOT/install.sh" update \
    --skills-dir "$TEST_SKILLS" \
    --agents-dir "$TEST_AGENTS" \
    --global-instructions keep \
    > "$TEST_ROOT/agent-rollback.log" 2>&1; then
  printf 'forced managed agent replacement failure unexpectedly succeeded\n' >&2
  exit 1
fi

grep -Fq '# rollback agent sentinel' "$TEST_AGENTS/planner.toml" || {
  printf 'failed managed agent replacement did not restore the prior copy\n' >&2
  exit 1
}
grep -Fq 'agent copy failed; restored previous agent: planner.toml' \
  "$TEST_ROOT/agent-rollback.log" || {
    printf 'managed agent rollback was not reported\n' >&2
    exit 1
  }
if find "$STATE_ROOT/backups" -path '*/agents/planner.toml' -print \
  | grep -q .; then
  printf 'verified managed agent rollback retained its temporary backup\n' >&2
  exit 1
fi

printf '# existing user instructions\n' > "$TEST_CODEX/AGENTS.md"

if HOME="$TEST_HOME" \
  CODEX_HOME="$TEST_CODEX" \
  PATH="$FAIL_BIN:$PATH" \
  HIGHFLOOR_TEST_REAL_CP="$REAL_CP" \
  HIGHFLOOR_TEST_FAIL_SOURCE="$ROOT/CODEX_AGENTS.md" \
  HIGHFLOOR_TEST_FAIL_TARGET="$TEST_CODEX/AGENTS.md" \
  "$ROOT/install.sh" update \
    --skills-dir "$TEST_SKILLS" \
    --agents-dir "$TEST_AGENTS" \
    --global-instructions replace \
    > "$TEST_ROOT/global-rollback.log" 2>&1; then
  printf 'forced global instructions replacement failure unexpectedly succeeded\n' >&2
  exit 1
fi

grep -Fqx '# existing user instructions' "$TEST_CODEX/AGENTS.md" || {
  printf 'failed global instructions replacement did not restore the prior copy\n' >&2
  exit 1
}
grep -Fq 'global instructions copy failed; restored previous global instructions' \
  "$TEST_ROOT/global-rollback.log" || {
    printf 'global instructions rollback was not reported\n' >&2
    exit 1
  }
if find "$STATE_ROOT/backups" -path '*/instructions/AGENTS.md' -type f \
  | grep -q .; then
  printf 'verified global instructions rollback retained its temporary backup\n' >&2
  exit 1
fi

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

find "$STATE_ROOT/backups" -path '*/skills/cx-interview/SKILL.md' -type f \
  | grep -q . || {
    printf 'uninstall did not retain a recoverable managed skill backup\n' >&2
    exit 1
  }
find "$STATE_ROOT/backups" -path '*/agents/planner.toml' -type f \
  | grep -q . || {
    printf 'uninstall did not retain a recoverable managed agent backup\n' >&2
    exit 1
  }

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
