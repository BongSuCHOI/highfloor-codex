# Go Runtime Debugging

Confirm module/workspace, build tags, target architecture, binary identity and launch arguments.

## Tool selection

- Use Delve to launch, attach or inspect a core only when breakpoints and goroutine state are needed.
- Use the race detector when the changed path can execute concurrently and a race is plausible.
- Use goroutine dumps for hangs, deadlocks and leaked work.
- Use `pprof` for CPU, heap, allocation, block or mutex questions; capture only the relevant profile.
- Use execution tracing for scheduler and latency questions that profiles cannot answer.

Optimized binaries can make local variables and stepping misleading. Reproduce with an appropriate debug build when possible, but do not replace the production build identity when the bug may depend on optimization or tags.
