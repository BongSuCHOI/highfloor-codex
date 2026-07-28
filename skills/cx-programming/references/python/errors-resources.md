# Python Errors and Resources

- Catch an exception where the code can add context, recover, translate it for a boundary or guarantee cleanup.
- Preserve the causal chain with `raise ... from exc` when translating.
- Catch a broad exception only at an owning boundary such as a worker loop, CLI entrypoint or request adapter, then preserve diagnostics.
- Use return values for expected alternatives when that makes the caller contract clearer; use exceptions for failure paths that interrupt normal flow.
- Own files, sessions, locks and transports with context managers where possible.
- If cleanup can fail, decide whether it replaces, joins or is reported alongside the primary failure.

Avoid mandatory custom exception hierarchies. Reuse the project's public error contract.
