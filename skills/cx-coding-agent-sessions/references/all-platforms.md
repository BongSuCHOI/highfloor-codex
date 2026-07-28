# Cross-Platform Session Stores

The finder probes known roots before parsing. Add nonstandard locations with repeated `--root`.

| Platform key | Typical Unix/macOS store |
|---|---|
| `codex` | `$CODEX_HOME`, `~/.codex` |
| `claude` | `~/.claude` |
| `senpi` | `~/.senpi/agent`, `~/.pi/agent` |
| `opencode` | `$OPENCODE_HOME`, `~/.opencode`, `~/.local/share/opencode` |
| `openclaw` | `~/.openclaw/agents/*/sessions` |
| `droid` | `~/.factory/sessions/*/*.jsonl` |
| `amp` | `~/.local/share/amp/threads/T-*.json` |
| `gemini`, `kimi`, `qwen` | product directories under `~/.gemini`, `~/.kimi`, `~/.qwen` |
| `roo-code`, `kilo-code`, `cline`, `kodu` | corresponding VS Code `globalStorage` task/database paths |
| `cursor-cli` | `~/.cursor/chats`, `~/.cursor/prompt_history.json` |
| `aider` | project-local `.aider.chat.history.md`; pass the project with `--root` |
| `kilo-cli`, `hermes`, `goose`, `crush`, `zed`, `kiro` | known product roots probed by the scanner |

Windows defaults use `%USERPROFILE%` or `%APPDATA%`; pass `--root` when the product is installed elsewhere.

Usage-only telemetry such as token accounting, OTEL rows or provider-retagging data is not a transcript source and is excluded unless it can reconstruct prompts.

## Evidence rule

Normalized previews locate candidates. Use `read` or the raw result `path` for exact prompts, tool calls and claims. Child transcripts are hidden from search by default; add `--include-subagents` when delegated work may contain the evidence.
