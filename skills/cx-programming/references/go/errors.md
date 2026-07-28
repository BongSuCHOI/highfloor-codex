# Go Errors

- Wrap with `%w` when callers must retain `errors.Is` or `errors.As` behavior.
- Add context once where it becomes useful; avoid repeating the same operation name through every layer.
- Translate to stable API/CLI errors at the owning boundary.
- Log once where the code owns operational or user reporting.
- Reserve panic for broken invariants or startup conditions the process cannot continue from; do not use it for routine caller errors.
- If cleanup fails, decide whether to join, replace or report it alongside the primary error.

Do not require a custom error type when sentinel or wrapped errors already satisfy the caller contract.
