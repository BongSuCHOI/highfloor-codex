# Python Async and Concurrency

- Every created task needs an owner that awaits, cancels or deliberately detaches it with observable failure handling.
- Cancellation is part of the API. Clean up resources in `finally` or an async context manager and do not swallow cancellation accidentally.
- Place timeouts at an owning boundary; avoid stacking unrelated timeout policies across layers.
- Use shielding only for the smallest operation that must finish despite caller cancellation.
- Do not run blocking file, CPU or synchronous client work on the event loop.
- Limit concurrency where the downstream resource has a real capacity.

Use `asyncio`, AnyIO or a framework task group according to the repository. Do not introduce a concurrency abstraction solely for stylistic consistency.
