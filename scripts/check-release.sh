#!/bin/sh

set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"

command -v python3 >/dev/null 2>&1 || {
  printf 'error: python3 is required for release validation\n' >&2
  exit 1
}

python3 "$ROOT/scripts/check_release.py"
