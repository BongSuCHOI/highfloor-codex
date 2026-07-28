# Rust Types and State

- Use a newtype when it prevents a real unit, identity or validation mistake.
- Use enums for materially closed state and make invalid transitions explicit.
- Use type-state when compile-time transition enforcement benefits callers enough to justify API complexity.
- Prefer a runtime state machine when states are dynamic, persisted, data-driven or need uniform storage.
- Use sealed traits only when downstream implementation would break an invariant or compatibility plan.

Do not encode every business rule in the type system. Optimize for clear ownership and caller behavior, not maximum generic sophistication.
