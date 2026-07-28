#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
# --- How to run ---
# uv run --isolated python "<skill-root>/scripts/find-agent-sessions.py" list --limit 20
# uv run --isolated python "<skill-root>/scripts/find-agent-sessions.py" search "commit" --from 7d
# uv run --isolated python "<skill-root>/scripts/find-agent-sessions.py" get <session-id>
from __future__ import annotations

import sys
import runpy
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))


if __name__ == "__main__":
    _ = runpy.run_module("agent_sessions.cli", run_name="__main__")
