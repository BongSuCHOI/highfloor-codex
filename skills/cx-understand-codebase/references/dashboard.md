# Interactive dashboard

Launch the vendored Understand Anything viewer for a completed local graph.

## Preconditions

1. Resolve the exact project directory; do not redirect a worktree.
2. Prefer legacy `.understand-anything/` only when it already exists; otherwise
   use `.ua/`.
3. Require `knowledge-graph.json` and `meta.json.analysisStatus == "complete"`.
   Do not launch a partial or failed graph automatically.

## Start

Resolve `SKILL_DIR` to the directory containing the active `SKILL.md`, then
start this command in a managed long-running terminal session:

```bash
sh "<SKILL_DIR>/scripts/serve-dashboard.sh" "<project-directory>"
```

Optional port:

```bash
sh "<SKILL_DIR>/scripts/serve-dashboard.sh" "<project-directory>" --port 5173
```

The wrapper prepares the pinned dashboard runtime with the frozen upstream
lockfile, then runs the vendored read-only viewer with `--no-open`.

Capture the exact line:

```text
Dashboard URL: http://127.0.0.1:<PORT>/?token=<TOKEN>
```

Return the full tokenized URL and graph path. Never omit `?token=...`, bind to
`0.0.0.0`, publish the port, or print the token anywhere except the user-facing
handoff for this local task.

## Security properties

The upstream viewer retained here:

- binds to `127.0.0.1` only;
- requires a random token for every graph and source-data endpoint;
- serves source only for paths already present in the graph;
- rejects absolute paths, traversal, binary files, and source files over 1 MB;
- strips absolute project paths from graph responses;
- exposes a read-only UI.

Treat the viewer as a local development server. Keep the terminal session ID so
it can be stopped later. Do not kill unrelated Node or Vite processes.
