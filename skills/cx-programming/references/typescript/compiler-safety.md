# TypeScript Compiler Safety

High-value flags can expose real ambiguity, but each has adoption cost in an existing codebase.

- `strict`: umbrella for core nullability and checking rules.
- `noUncheckedIndexedAccess`: models missing indexed values but can widen many reads.
- `exactOptionalPropertyTypes`: distinguishes absent from explicitly undefined.
- `useUnknownInCatchVariables`: reinforces error narrowing.
- `noImplicitOverride`: makes inheritance intent explicit.
- `verbatimModuleSyntax`: clarifies type/value import behavior but depends on module tooling.

Use the project's current configuration. Propose a flag change separately when its benefit is relevant, and evaluate the resulting migration surface before enabling it.
