# Rust Unsafe and FFI Discipline

Prefer a safe API. Each `unsafe` block must state:

- the exact invariant required;
- why it holds at this location;
- who maintains it over time;
- how the safe wrapper prevents callers from violating it.

Check pointer validity, alignment, initialization, aliasing, lifetime, provenance, layout and thread-safety as applicable. At FFI boundaries, define ownership, allocation/free pairing, unwind behavior, nullability, encoding and ABI/layout assumptions.

## Select the closest tool

| Tool | Best for |
|---|---|
| Miri | interpreter-detectable UB in supported Rust code |
| Sanitizer | memory/thread issues in compiled executions |
| Loom | modeled concurrency interleavings |
| Fuzzing | input-space and parser/state-machine exploration |

These tools cover different failure classes. Run only applicable tools and retain ordinary tests for the safe public contract.
