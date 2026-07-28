# Go Concurrency

- Every goroutine needs a bounded lifetime, termination path and result/error owner.
- The caller that creates cancellation normally owns calling it; propagate `context.Context` across blocking boundaries.
- The sender that owns production normally closes a channel. Receivers should not close a shared producer channel.
- Do not hold a lock while performing blocking I/O or sending to an uncontrolled channel.
- Size buffers from a known burst/backpressure policy, not to hide a deadlock.
- Define shutdown order for producers, consumers and resources.

Use `errgroup`, worker pools or raw goroutines according to existing project patterns. Run race or leak-sensitive verification only when the changed behavior makes those failures plausible.
