---
name: cx-coding-agent-sessions
description: "Find, inspect and summarize local coding-agent sessions across Codex, Claude, OpenCode, Senpi and supported transcript stores. Use for exact session recall, prior-work evidence, child-session discovery and transcript lookup."
---

# Coding Agent Sessions

Use the bundled finder before answering session-history questions from memory. When a platform is named, read its storage reference only if location or linkage details are needed.

## Platform references

| Platform | Reference |
|---|---|
| Codex | `references/codex.md` |
| Claude | `references/claude.md` |
| OpenCode | `references/opencode.md` |
| Senpi | `references/senpi.md` |
| Other or unknown | `references/all-platforms.md` |

## Search and read

Unless the user supplied an exact path, begin with the finder:

```bash
uv run --isolated python "<skill-root>/scripts/find-agent-sessions.py" list --limit 20
uv run --isolated python "<skill-root>/scripts/find-agent-sessions.py" find --query "deploy" --query "token usage" --from 7d
uv run --isolated python "<skill-root>/scripts/find-agent-sessions.py" read <session-id>
```

Resolve `<skill-root>` to this skill's actual absolute path. For vague recall, use a few discriminative aliases, repository names, exact errors, IDs or Korean/English variants with repeated `--query`. Narrow with `--platform`, `--cwd`, `--model`, `--from` and `--to`; add `--include-subagents` when delegated work may contain the only evidence. Run the result's absolute-path `detail_hint` or `read` command before ad hoc filesystem digging.

`list` and `find` hide child sessions by default but report `subagent_count`; `read` shows the child tree. The finder normalizes formats, while each result's raw `path` remains the source of truth for exact claims.

The finder uses only the Python standard library. Run it with `uv run --isolated`. If the default `uv` cache fails specifically with a sandbox permission error, retry once with `UV_CACHE_DIR=/tmp/codex-uv-cache`; do not relabel package resolution, network, script, or target failures as cache failures. If `uv` is missing, propose the exact installation command and wait for approval. Treat ordinary finder failures as execution errors, not missing dependencies.
