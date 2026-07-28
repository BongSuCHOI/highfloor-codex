# TypeScript Types and Boundaries

- Values crossing JSON, storage, environment, DOM or third-party boundaries begin as `unknown` unless a trusted API contract proves otherwise.
- Narrow or parse once, then pass typed values inward.
- Runtime schemas and TypeScript types solve different problems; use the repository's existing validator rather than mandating one library.
- Use discriminated unions and exhaustive handling when the state space is materially closed.
- Use `satisfies` when checking shape while preserving useful inference.
- Use branded/opaque types only when mixing same-shaped identities or units is a real risk.
- Keep assertions adjacent to the invariant that makes them safe.

Prefer ordinary object and function types when additional machinery does not remove an invalid state.
