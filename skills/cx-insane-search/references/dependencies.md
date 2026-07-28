# Dependency Boundary

`scripts/run.sh` executes the engine with pinned requirements in an isolated uv environment:

```bash
uv run --isolated \
  --with-requirements <skill-root>/engine/requirements-core.txt \
  --with-requirements <skill-root>/engine/requirements-optional.txt \
  python -m engine "<URL>"
```

Core packages provide HTTP/TLS transport, HTML selectors and WAF profile parsing. Optional packages provide PDF and feed recovery. Versions live in the two requirement files and are the source of truth.

`yt-dlp` runs through pinned `uvx`. Local browser fallback reads exact package versions from `engine/templates/package.json` and resolves them through `npx`. These runners reuse uv/npm caches but do not inspect global Python/npm packages or create a project `.venv` or `node_modules`.

If `uv`, `node` or `npx` is absent, explain why it is needed and propose the exact installation command. Propose a browser binary download only after the runtime reports a missing executable. Preserve package-resolution, network, navigation, selector, authentication and WAF failures as distinct failure types.
