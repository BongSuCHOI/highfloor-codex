# FastAPI and Async SQLAlchemy Boundaries

Use only when the project already selects these libraries.

- Create request/unit-of-work scoped `AsyncSession` ownership; do not share one session across concurrent tasks.
- Make transaction ownership explicit and avoid hidden commits in reusable repository functions.
- Prevent implicit database I/O during serialization. Select eager loading or explicit queries for data needed after the session boundary.
- Translate persistence objects into response/domain shapes at a deliberate boundary.
- Handle cancellation and rollback so a disconnected request does not leave ambiguous work.
- Use the real database dialect when the behavior depends on constraints, isolation, SQL syntax or driver semantics.

Do not replace the project's dependency injection, migration or validation stack with boilerplate from this reference.
