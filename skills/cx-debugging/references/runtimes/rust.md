# Rust Runtime Debugging

Confirm Cargo workspace/package, feature set, profile, target, executable and environment.

## Evidence choices

- Enable `RUST_BACKTRACE` and project logging when stack/context is sufficient.
- Use LLDB/GDB when inspecting native state, panics across FFI or optimized behavior.
- Inspect spawned-task ownership, cancellation and blocking sections for async hangs.
- Check lock scope and whether a synchronous guard crosses `.await`.
- Select Miri, sanitizers, Loom or fuzzing only for the failure class they can expose.

Debug builds improve symbols and stepping, but reproduce the relevant release profile when optimization, layout, timing or undefined behavior may matter.
