# TypeScript Errors

- Catch values as `unknown` and narrow before reading fields.
- Translate errors at API, job, CLI or UI boundaries while retaining the original `cause` when supported.
- Use exceptions when failure unwinds normal control flow; use a Result-like value when expected alternatives are part of frequent caller logic.
- Do not log the same failure at every layer. Log at the boundary that owns user or operational reporting.
- Preserve stable public error codes separately from implementation messages.

Follow existing framework error handlers and avoid introducing a parallel hierarchy for a local change.
