#!/usr/bin/env python3
"""Delete only an auto-created cx-analyze-video temp directory."""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path


MARKER = ".highfloor-cx-analyze-video-workdir"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: cleanup.py <work-dir>", file=sys.stderr)
        return 2

    candidate = Path(sys.argv[1]).expanduser()
    if candidate.is_symlink():
        print(f"refusing symlink: {candidate}", file=sys.stderr)
        return 2

    resolved = candidate.resolve()
    temp_root = Path(tempfile.gettempdir()).resolve()
    if resolved.parent != temp_root or not resolved.name.startswith("watch-"):
        print(f"refusing non-watch temp directory: {resolved}", file=sys.stderr)
        return 2
    if not (resolved / MARKER).is_file():
        print(f"refusing unmarked directory: {resolved}", file=sys.stderr)
        return 2

    shutil.rmtree(resolved)
    print(f"removed cx-analyze-video work directory: {resolved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
