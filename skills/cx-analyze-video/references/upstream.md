# Upstream provenance

## Source

- Project: [`bradautomates/claude-video`](https://github.com/bradautomates/claude-video)
- Inspected commit: `83da59fa78c3eee9e20f515fe75c438bb5166efd`
- Upstream skill version: `0.2.0`
- License: MIT
- Copyright: `Copyright (c) 2026 Bradley Bonanno`
- License copy: [`LICENSE.upstream.txt`](LICENSE.upstream.txt)

## Relationship

`cx-analyze-video` is a modified derivative of upstream `skills/watch`. It retains
the frame extraction, duration-aware budgets, keyframe and scene selection,
near-duplicate removal, caption parsing, focused ranges, transcript-cue frames,
and pure-stdlib Groq/OpenAI Whisper clients.

Highfloor modifications:

- replace Claude `/watch`, `Read`, and `AskUserQuestion` assumptions with the
  Codex-native `$cx-analyze-video` invocation and host image inspection;
- remove automatic Homebrew installation and make setup preflight-only;
- require explicit authorization before any Whisper audio upload;
- enforce the same authorization inside the transcription helper, including
  direct CLI use;
- stop reading project-local `.env` files for transcription keys and use a
  dedicated Highfloor config path;
- allow ordered caption-language selection with `--subtitle-langs`;
- add guarded cleanup for only marked auto-created temp directories;
- prevent Python bytecode caches from mutating the installed managed skill;
- separate visual, spoken, combined, inferred, and `NOT_PROVEN` evidence;
- reduce unnecessary long-video frame use through a staged detail policy.

Claude plugin metadata, SessionStart hooks, release packaging, and the
upstream `/watch` slash-command surface are not redistributed because they do
not participate in the Codex skill runtime.
