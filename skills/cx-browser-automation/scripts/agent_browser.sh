#!/usr/bin/env bash
set -euo pipefail

if ! command -v node >/dev/null 2>&1 || ! command -v npx >/dev/null 2>&1; then
  echo "Error: Node.js and npx are required for the isolated agent-browser runner." >&2
  echo "Suggested install: brew install node (macOS/Homebrew) or use the official Node.js installer." >&2
  exit 127
fi

exec npx --yes agent-browser@0.29.1 "$@"
