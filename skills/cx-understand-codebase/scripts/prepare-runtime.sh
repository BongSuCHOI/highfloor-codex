#!/bin/sh

set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SKILL_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
VENDORED_ROOT="$SKILL_DIR/vendor/understand-anything-plugin"
PNPM_VERSION="10.6.2"
RUNTIME_REVISION="fe8c5bc591716aafd79b4765549328f08ef5a52e-highfloor-20260809"
MODE="${1:-analysis}"
STAGING_ROOT=""

fail() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

if [ -n "${XDG_CACHE_HOME:-}" ]; then
  CACHE_ROOT="$XDG_CACHE_HOME"
elif [ -n "${HOME:-}" ]; then
  CACHE_ROOT="$HOME/.cache"
else
  fail "HOME or XDG_CACHE_HOME is required to resolve the runtime cache"
fi

RUNTIME_ROOT="${HIGHFLOOR_UNDERSTAND_RUNTIME_DIR:-$CACHE_ROOT/highfloor/cx-understand-codebase/$RUNTIME_REVISION}"
case "$RUNTIME_ROOT" in
  /*) ;;
  *) fail "runtime cache path must be absolute: $RUNTIME_ROOT" ;;
esac
if [ "$RUNTIME_ROOT" = "/" ] ||
   { [ -n "${HOME:-}" ] && [ "$RUNTIME_ROOT" = "$HOME" ]; }; then
  fail "refusing broad runtime cache path: $RUNTIME_ROOT"
fi
[ ! -L "$RUNTIME_ROOT" ] ||
  fail "refusing symlink runtime cache path: $RUNTIME_ROOT"

cleanup_staging() {
  if [ -n "$STAGING_ROOT" ] && [ -d "$STAGING_ROOT" ]; then
    rm -rf -- "$STAGING_ROOT"
  fi
}
trap cleanup_staging 0 1 2 15

ensure_runtime_source() {
  marker="$RUNTIME_ROOT/.highfloor-runtime-source"
  if [ -f "$marker" ]; then
    recorded="$(sed -n '1p' "$marker")"
    [ "$recorded" = "$RUNTIME_REVISION" ] ||
      fail "runtime cache source mismatch at $RUNTIME_ROOT"
    return
  fi

  [ ! -e "$RUNTIME_ROOT" ] ||
    fail "incomplete runtime cache at $RUNTIME_ROOT; inspect and remove that exact directory before retrying"
  [ -f "$VENDORED_ROOT/pnpm-lock.yaml" ] || fail "vendored runtime lockfile is missing"
  [ -f "$VENDORED_ROOT/package.json" ] || fail "vendored runtime package.json is missing"

  runtime_parent="$(dirname -- "$RUNTIME_ROOT")"
  mkdir -p "$runtime_parent"
  STAGING_ROOT="$(mktemp -d "$runtime_parent/.prepare.XXXXXX")" ||
    fail "could not create runtime staging directory under $runtime_parent"
  cp -R "$VENDORED_ROOT/." "$STAGING_ROOT/"
  printf '%s\n' "$RUNTIME_REVISION" > "$STAGING_ROOT/.highfloor-runtime-source"
  [ ! -e "$RUNTIME_ROOT" ] || fail "runtime cache appeared during preparation: $RUNTIME_ROOT"
  mv "$STAGING_ROOT" "$RUNTIME_ROOT"
  STAGING_ROOT=""
}

require_node_runtime() {
  command -v node >/dev/null 2>&1 || fail "Node.js >= 22 is required"
  command -v npx >/dev/null 2>&1 || fail "npx is required for pinned pnpm execution"

  NODE_MAJOR="$(node -p 'Number(process.versions.node.split(".")[0])')"
  [ "$NODE_MAJOR" -ge 22 ] || fail "Node.js >= 22 is required; found $(node --version)"
}

run_pnpm() {
  npx --yes "pnpm@$PNPM_VERSION" "$@"
}

prepare_analysis() {
  if [ ! -d "$RUNTIME_ROOT/node_modules/.pnpm" ] ||
     [ ! -d "$RUNTIME_ROOT/node_modules/graphology" ]; then
    (
      cd "$RUNTIME_ROOT"
      run_pnpm install --frozen-lockfile --filter '@understand-anything/skill...'
    )
  fi

  if [ ! -f "$RUNTIME_ROOT/packages/core/dist/index.js" ]; then
    (
      cd "$RUNTIME_ROOT"
      run_pnpm --filter '@understand-anything/core' build
    )
  fi
}

prepare_dashboard() {
  if [ ! -d "$RUNTIME_ROOT/node_modules/.pnpm" ] ||
     [ ! -d "$RUNTIME_ROOT/packages/dashboard/node_modules" ]; then
    (
      cd "$RUNTIME_ROOT"
      run_pnpm install --frozen-lockfile
    )
  fi

  if [ ! -f "$RUNTIME_ROOT/packages/viewer/dist/index.html" ] ||
     [ ! -f "$RUNTIME_ROOT/packages/viewer/bin/dist/staleness.js" ]; then
    (
      cd "$RUNTIME_ROOT"
      run_pnpm --filter 'understand-anything-viewer' build
    )
  fi
}

case "$MODE" in
  path)
    printf '%s\n' "$RUNTIME_ROOT"
    ;;
  --check|check)
    printf 'runtime_root=%s\n' "$RUNTIME_ROOT"
    printf 'source_ready=%s\n' "$([ -f "$RUNTIME_ROOT/.highfloor-runtime-source" ] && printf true || printf false)"
    printf 'node=%s\n' "$(command -v node >/dev/null 2>&1 && node --version || printf missing)"
    printf 'npx=%s\n' "$(command -v npx >/dev/null 2>&1 && npx --version || printf missing)"
    printf 'analysis_ready=%s\n' "$([ -f "$RUNTIME_ROOT/packages/core/dist/index.js" ] && printf true || printf false)"
    printf 'dashboard_ready=%s\n' "$([ -f "$RUNTIME_ROOT/packages/viewer/dist/index.html" ] && printf true || printf false)"
    ;;
  analysis)
    require_node_runtime
    ensure_runtime_source
    prepare_analysis
    printf 'Understand Anything analysis runtime ready.\n'
    ;;
  dashboard)
    require_node_runtime
    ensure_runtime_source
    prepare_dashboard
    printf 'Understand Anything dashboard runtime ready.\n'
    ;;
  *)
    fail "usage: prepare-runtime.sh [analysis|dashboard|check|path]"
    ;;
esac
