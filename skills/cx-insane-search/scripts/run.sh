#!/usr/bin/env bash
set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_ROOT"

if ! command -v uv >/dev/null 2>&1; then
  printf '%s\n' 'Error: uv is required to run cx-insane-search in an isolated environment.' >&2
  printf '%s\n' 'Suggested install: brew install uv (macOS/Homebrew) or use the official uv installer.' >&2
  exit 127
fi

run_engine() {
  uv run --isolated \
    --with-requirements "$SKILL_ROOT/engine/requirements-core.txt" \
    --with-requirements "$SKILL_ROOT/engine/requirements-optional.txt" \
    python -m engine "$@"
}

ERROR_LOG="$(mktemp "${TMPDIR:-/tmp}/cx-insane-search-uv.XXXXXX")"
cleanup() {
  rm -f "$ERROR_LOG"
}
trap cleanup EXIT

set +e
run_engine "$@" 2>"$ERROR_LOG"
STATUS=$?
set -e

if [[ "$STATUS" -eq 0 ]]; then
  exit 0
fi

cat "$ERROR_LOG" >&2

if [[ -z "${UV_CACHE_DIR:-}" ]] \
  && grep -Fq "Failed to initialize cache" "$ERROR_LOG" \
  && grep -Eq "Operation not permitted|Permission denied" "$ERROR_LOG"; then
  printf '%s\n' 'uv default cache is unavailable in this sandbox; retrying once with UV_CACHE_DIR=/tmp/codex-uv-cache.' >&2
  UV_CACHE_DIR=/tmp/codex-uv-cache run_engine "$@"
  exit $?
fi

exit "$STATUS"
