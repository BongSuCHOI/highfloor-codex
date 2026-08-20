# Codex Sessions

Codex has two useful surfaces:

- `$CODEX_HOME/state_*.sqlite` stores thread metadata.
- `$CODEX_HOME/sessions/**/rollout-*.jsonl` and archived rollout files store event transcripts.

Use the broad finder for Codex discovery:

```bash
uv run --isolated python "<skill-root>/scripts/find-agent-sessions.py" list --platform codex --limit 10
uv run --isolated python "<skill-root>/scripts/find-agent-sessions.py" search "deploy" --platform codex
uv run --isolated python "<skill-root>/scripts/find-agent-sessions.py" search --query "deploy" --query "token usage" --platform codex --workers 32
uv run --isolated python "<skill-root>/scripts/find-agent-sessions.py" get <session-id> --platform codex
```

Important filters: `--from`, `--to`, `--cwd`, `--model`,
`--reasoning-effort`, `--root`, `--limit`, `--include-subagents`, and
`--include-internal`. Model and effort filters match any recorded value in the
ordered session history. When old SQLite rows do not contain that history, the
finder reads their rollout lazily after applying date and cwd filters; narrow a
large store with those filters when possible.

Codex list and search results hide internal host sessions such as
`codex-auto-review`, built-in review, and memory-consolidation side threads by
default. The payload reports `excluded_internal_count`; use
`--include-internal` when those traces are themselves evidence. Direct
`read <session-id>` remains available regardless of the default filter.

## Spawned (subagent) threads

Codex subagent threads are ordinary rows in `threads` with their own rollout files. Two linkage sources:

- `thread_spawn_edges(parent_thread_id, child_thread_id, status)` — authoritative parent→child table.
- `threads.source` — `cli` / `exec` / `vscode` for user-started threads, or JSON for spawned ones:
  - `{"subagent": "review"}`, `{"subagent": "memory_consolidation"}` — built-in side threads.
  - `{"subagent": {"thread_spawn": {"parent_thread_id": "...", "depth": 1, "agent_nickname": "Tesla", "agent_role": "explorer"}}}` — collab/multi-agent spawns (depth can exceed 1: children spawn grandchildren).

`threads` also carries `agent_nickname`, `agent_role`, `model`, `first_user_message`, `tokens_used`. Without the SQLite DB, the same linkage is in each rollout file's first line: `type: "session_meta"` whose `payload` has `id`, `cwd`, `model_provider`, `forked_from_id`, and the same `source.subagent.thread_spawn` object.

The finder maps these to `parent_id` and `agent = "nickname (role)"`; `get <parent-thread-id>` lists children under `subagents`, and `get <child-thread-id>` returns the child's rollout events.

Codex rollout events may change model or reasoning effort during a task. The
finder preserves ordered, deduplicated `models` and `reasoning_efforts` arrays
and labels each result as `root`, `subagent`, or `internal`. These fields expose
recorded settings and available reasoning summaries; they do not reconstruct
hidden chain of thought.
