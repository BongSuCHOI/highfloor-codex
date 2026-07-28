#!/bin/sh

set -eu

PROJECT_NAME="highfloor-codex"
DEFAULT_REPO="BongSuCHOI/highfloor-codex"
DEFAULT_REF="main"

ACTION="install"
DRY_RUN=0
REPO="${HIGHFLOOR_REPO:-$DEFAULT_REPO}"
REF="${HIGHFLOOR_REF:-$DEFAULT_REF}"
CODEX_ROOT="${CODEX_HOME:-$HOME/.codex}"
STATE_ROOT="${HIGHFLOOR_STATE_DIR:-$CODEX_ROOT/$PROJECT_NAME}"
SKILLS_DIR="${HIGHFLOOR_SKILLS_DIR:-$CODEX_ROOT/skills}"
AGENTS_DIR="${HIGHFLOOR_AGENTS_DIR:-$CODEX_ROOT/agents}"
TEMP_ROOT=""
BACKUP_ROOT=""
SOURCE_ROOT=""

usage() {
  cat <<'EOF'
Highfloor for Codex installer

Usage:
  install.sh [install|update|doctor|uninstall] [options]

Actions:
  install      Install or reconcile managed skills and agents (default).
  update       Alias for install; fetches the selected ref when run remotely.
  doctor       Verify the recorded installation.
  uninstall    Back up and remove only Highfloor-managed entries.

Options:
  --repo OWNER/REPO     GitHub repository used by remote installs.
  --ref REF             Branch, tag, or commit to install.
  --skills-dir PATH     Override the skills destination.
  --agents-dir PATH     Override the custom agents destination.
  --dry-run             Print mutations without applying them.
  -h, --help            Show this help.

Environment:
  CODEX_HOME
  HIGHFLOOR_REPO
  HIGHFLOOR_REF
  HIGHFLOOR_SKILLS_DIR
  HIGHFLOOR_AGENTS_DIR
  HIGHFLOOR_STATE_DIR

Destination policy:
  Custom agents default to "$CODEX_HOME/agents".
  Skills default to "$CODEX_HOME/skills".
  Pass --skills-dir or --agents-dir to choose another location explicitly.
EOF
}

log() {
  printf '%s\n' "$*"
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

cleanup() {
  if [ -n "$TEMP_ROOT" ] && [ -d "$TEMP_ROOT" ]; then
    rm -rf "$TEMP_ROOT"
  fi
}

trap cleanup EXIT HUP INT TERM

run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    printf '+'
    for arg in "$@"; do
      printf ' %s' "$arg"
    done
    printf '\n'
  else
    "$@"
  fi
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || die "required command not found: $1"
}

validate_entry_name() {
  case "$1" in
    ""|.*|*/*|*..*) die "unsafe manifest entry: $1" ;;
    *[!A-Za-z0-9._-]*) die "unsafe manifest entry: $1" ;;
  esac
}

read_value_file() {
  if [ -f "$1" ]; then
    sed -n '1p' "$1"
  fi
}

ensure_destination_compatibility() {
  recorded_skills="$(read_value_file "$STATE_ROOT/skills-dir")"
  recorded_agents="$(read_value_file "$STATE_ROOT/agents-dir")"

  if [ -n "$recorded_skills" ] && [ "$recorded_skills" != "$SKILLS_DIR" ]; then
    die "existing install uses skills directory '$recorded_skills'; uninstall before changing it"
  fi
  if [ -n "$recorded_agents" ] && [ "$recorded_agents" != "$AGENTS_DIR" ]; then
    die "existing install uses agents directory '$recorded_agents'; uninstall before changing it"
  fi
}

ensure_backup_root() {
  if [ -z "$BACKUP_ROOT" ]; then
    stamp="$(date -u '+%Y%m%dT%H%M%SZ')-$$"
    BACKUP_ROOT="$STATE_ROOT/backups/$stamp"
    run mkdir -p "$BACKUP_ROOT/skills" "$BACKUP_ROOT/agents"
  fi
}

backup_directory() {
  ensure_backup_root
  run cp -R "$1" "$BACKUP_ROOT/skills/$2"
}

backup_file() {
  ensure_backup_root
  run cp "$1" "$BACKUP_ROOT/agents/$2"
}

resolve_local_source() {
  script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" 2>/dev/null && pwd || true)"
  if [ -n "$script_dir" ] &&
     [ -f "$script_dir/VERSION" ] &&
     [ -f "$script_dir/manifest/skills.txt" ] &&
     [ -f "$script_dir/manifest/agents.txt" ] &&
     [ -d "$script_dir/skills" ] &&
     [ -d "$script_dir/agents" ]; then
    SOURCE_ROOT="$script_dir"
    return 0
  fi
  return 1
}

download_source() {
  require_command curl
  require_command tar

  TEMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/highfloor-codex.XXXXXX")"
  archive="$TEMP_ROOT/source.tar.gz"
  url="https://codeload.github.com/$REPO/tar.gz/$REF"

  log "Downloading $REPO@$REF"
  curl -fsSL "$url" -o "$archive" || die "download failed: $url"
  tar -xzf "$archive" -C "$TEMP_ROOT" || die "could not extract downloaded archive"

  SOURCE_ROOT="$(find "$TEMP_ROOT" -mindepth 1 -maxdepth 1 -type d -print | sed -n '1p')"
  [ -n "$SOURCE_ROOT" ] || die "downloaded archive did not contain a repository directory"
}

resolve_source() {
  if ! resolve_local_source; then
    download_source
  fi
}

validate_source() {
  source_root="$1"
  [ -f "$source_root/VERSION" ] || die "source is missing VERSION"
  [ -f "$source_root/manifest/skills.txt" ] || die "source is missing manifest/skills.txt"
  [ -f "$source_root/manifest/agents.txt" ] || die "source is missing manifest/agents.txt"
  [ -d "$source_root/skills" ] || die "source is missing skills/"
  [ -d "$source_root/agents" ] || die "source is missing agents/"
}

reconcile_removed_skills() {
  new_manifest="$1"
  old_manifest="$STATE_ROOT/skills.txt"
  [ -f "$old_manifest" ] || return 0

  while IFS= read -r entry || [ -n "$entry" ]; do
    [ -n "$entry" ] || continue
    validate_entry_name "$entry"
    if ! grep -Fqx "$entry" "$new_manifest"; then
      target="$SKILLS_DIR/$entry"
      if [ -e "$target" ] || [ -L "$target" ]; then
        log "Removing retired managed skill: $entry"
        backup_directory "$target" "$entry"
        run rm -rf "$target"
      fi
    fi
  done < "$old_manifest"
}

reconcile_removed_agents() {
  new_manifest="$1"
  old_manifest="$STATE_ROOT/agents.txt"
  [ -f "$old_manifest" ] || return 0

  while IFS= read -r entry || [ -n "$entry" ]; do
    [ -n "$entry" ] || continue
    validate_entry_name "$entry"
    if ! grep -Fqx "$entry" "$new_manifest"; then
      target="$AGENTS_DIR/$entry"
      if [ -e "$target" ] || [ -L "$target" ]; then
        log "Removing retired managed agent: $entry"
        backup_file "$target" "$entry"
        run rm -f "$target"
      fi
    fi
  done < "$old_manifest"
}

install_skills() {
  source_root="$1"
  manifest="$source_root/manifest/skills.txt"

  reconcile_removed_skills "$manifest"
  run mkdir -p "$SKILLS_DIR"

  while IFS= read -r entry || [ -n "$entry" ]; do
    [ -n "$entry" ] || continue
    validate_entry_name "$entry"
    source_path="$source_root/skills/$entry"
    target="$SKILLS_DIR/$entry"
    [ -d "$source_path" ] || die "manifest skill does not exist: $entry"
    [ ! -L "$source_path" ] || die "manifest skill cannot be a symlink: $entry"
    if find "$source_path" -type l -print | grep -q .; then
      die "manifest skill contains a symlink: $entry"
    fi

    if [ ! -L "$target" ] &&
       [ -d "$target" ] &&
       diff -qr "$source_path" "$target" >/dev/null 2>&1; then
      log "Unchanged skill: $entry"
      continue
    fi

    if [ -e "$target" ] || [ -L "$target" ]; then
      log "Backing up existing skill: $entry"
      backup_directory "$target" "$entry"
      run rm -rf "$target"
    fi

    log "Installing skill: $entry"
    run cp -R "$source_path" "$target"
  done < "$manifest"
}

install_agents() {
  source_root="$1"
  manifest="$source_root/manifest/agents.txt"

  reconcile_removed_agents "$manifest"
  run mkdir -p "$AGENTS_DIR"

  while IFS= read -r entry || [ -n "$entry" ]; do
    [ -n "$entry" ] || continue
    validate_entry_name "$entry"
    source_path="$source_root/agents/$entry"
    target="$AGENTS_DIR/$entry"
    [ -f "$source_path" ] || die "manifest agent does not exist: $entry"
    [ ! -L "$source_path" ] || die "manifest agent cannot be a symlink: $entry"

    if [ ! -L "$target" ] &&
       [ -f "$target" ] &&
       cmp -s "$source_path" "$target"; then
      log "Unchanged agent: $entry"
      continue
    fi

    if [ -e "$target" ] || [ -L "$target" ]; then
      log "Backing up existing agent: $entry"
      backup_file "$target" "$entry"
    fi

    log "Installing agent: $entry"
    run cp "$source_path" "$target"
  done < "$manifest"
}

write_state() {
  source_root="$1"
  version="$(sed -n '1p' "$source_root/VERSION")"

  run mkdir -p "$STATE_ROOT"
  if [ "$DRY_RUN" -eq 1 ]; then
    log "+ write $STATE_ROOT/version = $version"
    log "+ write $STATE_ROOT/ref = $REF"
    log "+ write $STATE_ROOT/skills-dir = $SKILLS_DIR"
    log "+ write $STATE_ROOT/agents-dir = $AGENTS_DIR"
    log "+ copy installation manifests into $STATE_ROOT"
    return
  fi

  printf '%s\n' "$version" > "$STATE_ROOT/version"
  printf '%s\n' "$REF" > "$STATE_ROOT/ref"
  printf '%s\n' "$SKILLS_DIR" > "$STATE_ROOT/skills-dir"
  printf '%s\n' "$AGENTS_DIR" > "$STATE_ROOT/agents-dir"
  cp "$source_root/manifest/skills.txt" "$STATE_ROOT/skills.txt"
  cp "$source_root/manifest/agents.txt" "$STATE_ROOT/agents.txt"
}

install_all() {
  ensure_destination_compatibility
  resolve_source
  source_root="$SOURCE_ROOT"
  validate_source "$source_root"
  version="$(sed -n '1p' "$source_root/VERSION")"

  log "Installing Highfloor for Codex $version"
  install_skills "$source_root"
  install_agents "$source_root"
  write_state "$source_root"

  log ""
  log "Skills: $SKILLS_DIR"
  log "Agents: $AGENTS_DIR"
  [ -z "$BACKUP_ROOT" ] || log "Backup: $BACKUP_ROOT"
  log "Restart Codex to refresh discovered skills and agents."
}

doctor() {
  [ -d "$STATE_ROOT" ] || die "no installation state found at $STATE_ROOT"
  skills_dir="$(read_value_file "$STATE_ROOT/skills-dir")"
  agents_dir="$(read_value_file "$STATE_ROOT/agents-dir")"
  [ -n "$skills_dir" ] || die "installation state is missing skills-dir"
  [ -n "$agents_dir" ] || die "installation state is missing agents-dir"

  failures=0
  while IFS= read -r entry || [ -n "$entry" ]; do
    [ -n "$entry" ] || continue
    validate_entry_name "$entry"
    if [ ! -f "$skills_dir/$entry/SKILL.md" ]; then
      printf 'missing skill: %s\n' "$skills_dir/$entry" >&2
      failures=$((failures + 1))
    fi
  done < "$STATE_ROOT/skills.txt"

  while IFS= read -r entry || [ -n "$entry" ]; do
    [ -n "$entry" ] || continue
    validate_entry_name "$entry"
    if [ ! -f "$agents_dir/$entry" ]; then
      printf 'missing agent: %s\n' "$agents_dir/$entry" >&2
      failures=$((failures + 1))
    fi
  done < "$STATE_ROOT/agents.txt"

  if [ "$failures" -ne 0 ]; then
    die "doctor found $failures missing managed entries"
  fi

  log "Highfloor installation is healthy."
  log "Version: $(read_value_file "$STATE_ROOT/version")"
  log "Skills: $skills_dir"
  log "Agents: $agents_dir"
}

uninstall_all() {
  [ -d "$STATE_ROOT" ] || die "no installation state found at $STATE_ROOT"
  SKILLS_DIR="$(read_value_file "$STATE_ROOT/skills-dir")"
  AGENTS_DIR="$(read_value_file "$STATE_ROOT/agents-dir")"
  [ -n "$SKILLS_DIR" ] || die "installation state is missing skills-dir"
  [ -n "$AGENTS_DIR" ] || die "installation state is missing agents-dir"

  while IFS= read -r entry || [ -n "$entry" ]; do
    [ -n "$entry" ] || continue
    validate_entry_name "$entry"
    target="$SKILLS_DIR/$entry"
    if [ -e "$target" ] || [ -L "$target" ]; then
      backup_directory "$target" "$entry"
      log "Removing skill: $entry"
      run rm -rf "$target"
    fi
  done < "$STATE_ROOT/skills.txt"

  while IFS= read -r entry || [ -n "$entry" ]; do
    [ -n "$entry" ] || continue
    validate_entry_name "$entry"
    target="$AGENTS_DIR/$entry"
    if [ -e "$target" ] || [ -L "$target" ]; then
      backup_file "$target" "$entry"
      log "Removing agent: $entry"
      run rm -f "$target"
    fi
  done < "$STATE_ROOT/agents.txt"

  log ""
  log "Removed Highfloor-managed skills and agents."
  [ -z "$BACKUP_ROOT" ] || log "Backup: $BACKUP_ROOT"
  log "Installation state and backups remain at $STATE_ROOT."
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    install|update|doctor|uninstall)
      ACTION="$1"
      shift
      ;;
    --repo)
      [ "$#" -ge 2 ] || die "--repo requires a value"
      REPO="$2"
      shift 2
      ;;
    --ref)
      [ "$#" -ge 2 ] || die "--ref requires a value"
      REF="$2"
      shift 2
      ;;
    --skills-dir)
      [ "$#" -ge 2 ] || die "--skills-dir requires a value"
      SKILLS_DIR="$2"
      shift 2
      ;;
    --agents-dir)
      [ "$#" -ge 2 ] || die "--agents-dir requires a value"
      AGENTS_DIR="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown argument: $1"
      ;;
  esac
done

case "$ACTION" in
  install|update) install_all ;;
  doctor) doctor ;;
  uninstall) uninstall_all ;;
esac
