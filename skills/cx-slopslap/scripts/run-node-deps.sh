#!/usr/bin/env bash
set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v node >/dev/null 2>&1 || ! command -v npx >/dev/null 2>&1; then
  echo "Error: Node.js and npx are required for cx-slopslap's optional Node tools." >&2
  echo "Suggested install: brew install node (macOS/Homebrew) or use the official Node.js installer." >&2
  exit 127
fi

mode="${1:-}"
if [[ -z "$mode" ]]; then
  echo "Usage: run-node-deps.sh <gen-references|capture-reference> [args...]" >&2
  exit 2
fi
shift

quoted_args=""
if (( $# > 0 )); then
  printf -v quoted_args ' %q' "$@"
fi

case "$mode" in
  gen-references)
    script="$SKILL_ROOT/scripts/gen-reference-data.mjs"
    printf -v command 'NODE_PATH="$(dirname "$(dirname "$(command -v tailwindcss)")")" node %q%s' "$script" "$quoted_args"
    exec npx --yes \
      --package=tailwindcss@3.4.19 \
      --package=@radix-ui/colors@3.0.0 \
      -c "$command"
    ;;
  capture-reference)
    script="$SKILL_ROOT/scripts/capture-reference.mjs"
    printf -v command 'NODE_PATH="$(dirname "$(dirname "$(command -v playwright)")")" node %q%s' "$script" "$quoted_args"
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 exec npx --yes \
      --package=playwright@1.61.1 \
      -c "$command"
    ;;
  *)
    echo "Unknown mode: $mode" >&2
    exit 2
    ;;
esac
