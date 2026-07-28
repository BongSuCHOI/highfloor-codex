# Rust Async and Tokio

Use only when the project selects Tokio or compatible concepts apply.

- Every spawned task needs ownership: await its handle, cancel it or deliberately detach it with failure observability.
- Define shutdown order and what happens to in-flight work.
- Place timeouts at an owning boundary and preserve the underlying error/cancellation distinction.
- Move blocking CPU or synchronous I/O off async worker threads.
- Do not hold a synchronous lock guard across `.await`.
- Make cancellation safety explicit for operations that mutate shared or external state.
- Use paused time in tests when it makes timer behavior deterministic.

Do not add a runtime abstraction when the existing executor already defines the contract.
