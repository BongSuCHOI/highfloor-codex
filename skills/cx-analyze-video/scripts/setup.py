#!/usr/bin/env python3
"""Read-only preflight and explicit config scaffolding for cx-analyze-video."""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path


sys.dont_write_bytecode = True
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from config import CONFIG_DIR, CONFIG_FILE, get_config  # noqa: E402


MEDIA_BINARIES = ("ffmpeg", "ffprobe")
URL_BINARIES = ("yt-dlp",)
ENV_TEMPLATE = """# cx-analyze-video dedicated configuration
# Never copy project-local secrets into this file automatically.

GROQ_API_KEY=
OPENAI_API_KEY=

# transcript | efficient | balanced | token-burner
CX_ANALYZE_VIDEO_DETAIL=balanced
"""


def missing_binaries(*, local_only: bool = False) -> list[str]:
    required = MEDIA_BINARIES if local_only else MEDIA_BINARIES + URL_BINARIES
    return [name for name in required if shutil.which(name) is None]


def read_config_key(name: str) -> str | None:
    value = os.environ.get(name)
    if value and value.strip():
        return value.strip()
    if not CONFIG_FILE.is_file():
        return None
    try:
        if CONFIG_FILE.stat().st_mode & 0o044:
            print(
                f"[cx-analyze-video] warning: {CONFIG_FILE} is readable by other users; "
                f"run `chmod 600 {CONFIG_FILE}`",
                file=sys.stderr,
            )
        for line in CONFIG_FILE.read_text(encoding="utf-8").splitlines():
            raw = line.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue
            key, _, candidate = raw.partition("=")
            if key.strip() != name:
                continue
            candidate = candidate.strip()
            if (
                len(candidate) >= 2
                and candidate[0] in ("'", '"')
                and candidate[-1] == candidate[0]
            ):
                candidate = candidate[1:-1]
            return candidate or None
    except OSError:
        return None
    return None


def api_backend() -> str | None:
    if read_config_key("GROQ_API_KEY"):
        return "groq"
    if read_config_key("OPENAI_API_KEY"):
        return "openai"
    return None


def status(*, local_only: bool = False) -> dict[str, object]:
    missing = missing_binaries(local_only=local_only)
    backend = api_backend()
    config = get_config()
    return {
        "status": "ready" if not missing else "needs_install",
        "can_proceed": not missing,
        "missing_binaries": missing,
        "whisper_backend": backend,
        "has_api_key": backend is not None,
        "config_file": str(CONFIG_FILE),
        "detail": config["detail"],
        "platform": platform.system(),
        "source_scope": "local" if local_only else "url_or_local",
        "external_upload_default": "disabled",
    }


def install_instructions(missing: list[str]) -> str:
    needed = set(missing)
    system = platform.system()
    lines = ["Missing runtime binaries: " + ", ".join(missing)]
    if system == "Darwin":
        packages = []
        if needed.intersection({"ffmpeg", "ffprobe"}):
            packages.append("ffmpeg")
        if "yt-dlp" in needed:
            packages.append("yt-dlp")
        lines.append("Suggested command: brew install " + " ".join(packages))
    elif system == "Linux":
        if needed.intersection({"ffmpeg", "ffprobe"}):
            lines.append("ffmpeg/ffprobe: sudo apt install ffmpeg")
        if "yt-dlp" in needed:
            lines.append("yt-dlp: pipx install yt-dlp")
    elif system == "Windows":
        if needed.intersection({"ffmpeg", "ffprobe"}):
            lines.append("ffmpeg/ffprobe: winget install Gyan.FFmpeg")
        if "yt-dlp" in needed:
            lines.append("yt-dlp: winget install yt-dlp.yt-dlp")
    else:
        lines.append("Install the listed binaries with the platform package manager.")
    lines.append("No installer was run. Obtain user approval before executing a command above.")
    return "\n".join(lines)


def init_config() -> int:
    if CONFIG_FILE.exists():
        print(f"Config already exists; left unchanged: {CONFIG_FILE}")
        return 0
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(ENV_TEMPLATE, encoding="utf-8")
    CONFIG_FILE.chmod(0o600)
    print(f"Created config template: {CONFIG_FILE}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="Silent readiness check")
    group.add_argument("--json", action="store_true", help="Print structured status")
    group.add_argument(
        "--instructions",
        action="store_true",
        help="Print install guidance without installing anything",
    )
    group.add_argument(
        "--init-config",
        action="store_true",
        help="Create a dedicated 0600 config template without writing secrets",
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Check only local-file requirements; yt-dlp is not required",
    )
    args = parser.parse_args()

    if args.init_config:
        return init_config()

    current = status(local_only=args.local)
    if args.json:
        json.dump(current, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0
    if args.check:
        if current["can_proceed"]:
            return 0
        print(install_instructions(current["missing_binaries"]), file=sys.stderr)
        return 2

    if current["can_proceed"]:
        print("Runtime binaries are available. External Whisper upload remains disabled by default.")
        return 0
    print(install_instructions(current["missing_binaries"]))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
