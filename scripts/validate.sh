#!/bin/sh

set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"

command -v python3 >/dev/null 2>&1 || {
  printf 'error: python3 is required for repository validation\n' >&2
  exit 1
}

sh -n "$ROOT/install.sh"
python3 "$ROOT/scripts/validate_repo.py"
"$ROOT/scripts/check-release.sh"
