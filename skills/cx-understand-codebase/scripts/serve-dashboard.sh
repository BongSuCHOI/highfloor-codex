#!/bin/sh

set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SKILL_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"

[ "$#" -ge 1 ] || {
  printf 'usage: serve-dashboard.sh <project-dir> [--port N]\n' >&2
  exit 2
}

PROJECT_DIR="$(CDPATH= cd -- "$1" 2>/dev/null && pwd -P)" || {
  printf 'error: project directory not found: %s\n' "$1" >&2
  exit 2
}
shift

if [ -f "$PROJECT_DIR/.ua/knowledge-graph.json" ]; then
  DATA_DIR="$PROJECT_DIR/.ua"
elif [ -f "$PROJECT_DIR/.understand-anything/knowledge-graph.json" ]; then
  DATA_DIR="$PROJECT_DIR/.understand-anything"
else
  printf 'error: no knowledge graph found under %s\n' "$PROJECT_DIR" >&2
  exit 2
fi

if [ -f "$DATA_DIR/meta.json" ]; then
  ANALYSIS_STATUS="$(node -e '
    const fs = require("node:fs");
    const meta = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
    process.stdout.write(typeof meta.analysisStatus === "string" ? meta.analysisStatus : "");
  ' "$DATA_DIR/meta.json")" || {
    printf 'error: invalid graph metadata: %s\n' "$DATA_DIR/meta.json" >&2
    exit 2
  }
  if [ -n "$ANALYSIS_STATUS" ] && [ "$ANALYSIS_STATUS" != "complete" ]; then
    printf 'error: dashboard requires a complete graph; analysisStatus=%s\n' "$ANALYSIS_STATUS" >&2
    exit 2
  fi
fi

"$SCRIPT_DIR/prepare-runtime.sh" dashboard
RUNTIME_ROOT="$("$SCRIPT_DIR/prepare-runtime.sh" path)"

exec node "$RUNTIME_ROOT/packages/viewer/bin/viewer.mjs" \
  "$PROJECT_DIR" \
  --no-open \
  "$@"
