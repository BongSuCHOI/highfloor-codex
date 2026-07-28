# Python Decision Router

Use project Python/version, packaging, typing and test conventions first.

- Task lifetime, cancellation, timeouts or sync/async boundaries: `async-concurrency.md`
- Boundary and domain type selection: `typing-boundaries.md`
- Exceptions, cleanup and resource ownership: `errors-resources.md`
- FastAPI with async SQLAlchemy: `fastapi-sqlalchemy-async.md`
- Standalone PEP 723 scripts: `uv-scripts.md`

Do not blanket-ban `Any`, `object`, `cast`, broad exceptions, `asyncio` or a data library. Locate the boundary and explain the risk. Parse untrusted input once at the appropriate boundary using the project's existing parser or the standard library when sufficient.
