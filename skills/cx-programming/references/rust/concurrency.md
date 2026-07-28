# Rust Concurrency

- Treat `Send` and `Sync` errors as information about ownership, not obstacles to silence with `unsafe`.
- Keep lock scope small and define poisoning/recovery behavior where applicable.
- Choose channels from message ownership, backpressure and shutdown requirements.
- Use atomics only with a stated synchronization invariant; default ordering is not a substitute for reasoning.
- Avoid blocking while holding a lock or inside async executor work.
- Use Loom only for small synchronization models whose interleavings need exploration.

Prefer ownership transfer and message passing when they simplify invariants, but follow the project's established model.
