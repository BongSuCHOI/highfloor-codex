# Dependency Boundary

`scripts/run.sh` executes the engine with pinned requirements in an isolated uv environment:

```bash
uv run --isolated \
  --with-requirements <skill-root>/engine/requirements-core.txt \
  --with-requirements <skill-root>/engine/requirements-optional.txt \
  python -m engine "<URL>"
```

Core packages provide HTTP/TLS transport, HTML selectors and WAF profile
parsing. Optional packages provide PDF and feed recovery. Versions live in the
two requirement files and are the source of truth.

`yt-dlp` runs through pinned `uvx`. These runners reuse the uv cache but do not
inspect global Python packages or create a project `.venv`.

The retained local browser templates are not reachable from the public fetch
entrypoint because they cannot preserve its DNS-pinning and subresource-egress
boundary. Route rendered-page work to browser automation supplied by the host;
do not install Node.js or a browser for this engine path.

If `uv` is absent, explain why it is needed and propose the exact installation
command. Preserve package-resolution, network, navigation, selector,
authentication and WAF failures as distinct failure types.
