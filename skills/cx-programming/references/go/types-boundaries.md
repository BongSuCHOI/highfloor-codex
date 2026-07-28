# Go Types and Boundaries

- Separate transport/storage shapes from domain values when their nullability, naming or lifecycle differs.
- Design zero values deliberately: useful, invalid-but-detectable or hidden behind a constructor.
- Use pointers for optionality, identity or mutation only when those semantics are intended.
- Use named types or constructors when they prevent material identity/unit mistakes.
- Accept small interfaces at the consuming boundary; avoid speculative interfaces for one implementation.
- Use generics when one algorithm or container genuinely applies across types without erasing domain meaning.

Validate untrusted input at the boundary and keep internal values as strong as the domain requires.
