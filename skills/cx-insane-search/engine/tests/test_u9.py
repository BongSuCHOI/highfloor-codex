#!/usr/bin/env python3
"""U9 regression tests — pinned yt-dlp invocation through uvx.

Deterministic and network-free. Locks in that the YouTube Phase-0 route
resolves the exact `yt-dlp` version through uvx and never probes global Python
or a globally installed console script.

Run:  python3 engine/tests/test_u9.py
"""
from __future__ import annotations

import os
import sys
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)

from engine import phase0  # noqa: E402


def t_uses_pinned_uvx_command() -> None:
    with mock.patch.object(phase0.shutil, "which", return_value="/usr/bin/uvx"):
        argv = phase0._ytdlp_argv()
    assert argv == ["/usr/bin/uvx", "yt-dlp@2026.07.04"], argv
    print("  ✓ uvx → pinned yt-dlp command")


def t_none_when_neither_available() -> None:
    with mock.patch.object(phase0.shutil, "which", return_value=None):
        argv = phase0._ytdlp_argv()
    assert argv is None, argv
    print("  ✓ truly missing → None")


def t_youtube_route_reports_not_installed_without_subprocess() -> None:
    def _boom(*a, **k):
        raise AssertionError("subprocess.run must not run when yt-dlp is unavailable")
    with mock.patch.object(phase0, "_ytdlp_argv", return_value=None), \
         mock.patch("engine.safety.resolve_public_target", return_value=(object(), "public")), \
         mock.patch.object(phase0.subprocess, "run", _boom):
        out = phase0._youtube(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            timeout=5,
        )
    assert out["ok"] is False, out
    assert out["attempts"] and out["attempts"][-1]["note"] == "uvx not available", out["attempts"]
    print("  ✓ unavailable → uvx note, subprocess not invoked")


def t_youtube_route_uses_resolved_argv() -> None:
    captured = {}

    class _P:
        returncode = 0
        stdout = '{"title": "x"}'
        stderr = ""

    def _fake_run(cmd, *a, **k):
        captured["cmd"] = cmd
        return _P()

    with mock.patch.object(phase0, "_ytdlp_argv", return_value=["/usr/bin/uvx", "yt-dlp@2026.07.04"]), \
         mock.patch("engine.safety.resolve_public_target", return_value=(object(), "public")), \
         mock.patch.object(phase0.subprocess, "run", _fake_run):
        out = phase0._youtube("https://youtu.be/dQw4w9WgXcQ", timeout=5)
    assert out["ok"] is True, out
    assert captured["cmd"][:2] == ["/usr/bin/uvx", "yt-dlp@2026.07.04"], captured["cmd"]
    assert captured["cmd"][2:] == [
        "--dump-json",
        "--skip-download",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    ], captured["cmd"]
    print("  ✓ resolved argv is passed through to subprocess with the yt-dlp flags")


ALL = [
    ("uses_pinned_uvx_command", t_uses_pinned_uvx_command),
    ("none_when_neither_available", t_none_when_neither_available),
    ("youtube_route_reports_not_installed_without_subprocess", t_youtube_route_reports_not_installed_without_subprocess),
    ("youtube_route_uses_resolved_argv", t_youtube_route_uses_resolved_argv),
]


def main() -> int:
    p = f = 0
    for name, fn in ALL:
        try:
            print(f"[{name}]")
            fn()
            p += 1
        except AssertionError as e:
            f += 1
            print(f"  ✗ FAIL: {e}")
        except Exception as e:
            f += 1
            print(f"  ✗ ERROR: {type(e).__name__}: {e}")
    print(f"\n{p} passed, {f} failed")
    return 0 if f == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
