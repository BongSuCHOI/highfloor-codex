# Python Runtime Debugging

## Establish identity

Confirm the interpreter, virtual environment, working directory, import path and installed project actually used by the failing command. A correct source file does not prove that runtime imported it.

## Select evidence

- Test failure: rerun the smallest test with useful traceback and captured output disabled only when needed.
- Async hang/leak: inspect task ownership, cancellation and pending tasks before adding arbitrary timeouts.
- Live process: use `debugpy` only when attach/startup control is needed and permitted.
- CPU or wall-time issue: choose sampling, deterministic profiling or tracing according to the question.
- Memory growth: distinguish retained objects from allocator/process behavior before changing code.

Preserve exception chains and inspect the boundary where an error changes type or loses context. Reuse the project's environment when imports and plugins matter; use isolated one-off tooling only for external analysis.
