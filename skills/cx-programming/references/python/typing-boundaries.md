# Python Typing Boundaries

Choose a representation from runtime needs:

| Need | Typical choice |
|---|---|
| Static mapping shape, no runtime behavior | `TypedDict` |
| Owned value with behavior/defaults | dataclass |
| Runtime parsing/serialization already using Pydantic | Pydantic model |
| Structural caller capability | `Protocol` |
| Distinct identity over a primitive | `NewType` or a small wrapper |
| Closed named values | enum or literal union |

Use discriminated variants when callers must handle a genuinely closed state set. Narrow `object` or `unknown` input with predicates before use. A `cast` records an assumption but performs no runtime validation; keep it next to the evidence for that assumption.

Prefer types supported by the project's minimum Python version. Do not add a runtime model or wrapper when a plain value communicates the contract safely.
