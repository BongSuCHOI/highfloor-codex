# Go Testing

- Use table tests when cases share meaningful setup and assertions; do not force unrelated scenarios into one table.
- Use `httptest` at HTTP boundaries when it exercises routing, headers or serialization that unit calls would miss.
- Make concurrency tests deterministic with explicit synchronization rather than sleeps.
- Use the race detector when the changed path is concurrent and the platform supports it.
- Use leak checks only for code that owns long-lived goroutines or shutdown.
- Use the real database dialect when constraints, isolation or SQL behavior are under test.

Follow the repository's package and naming conventions. Select the nearest test that proves the changed behavior.
