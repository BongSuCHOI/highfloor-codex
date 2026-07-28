---
name: cx-programming
description: "Apply non-obvious Python, TypeScript, Go or Rust guidance at typing, validation, async/concurrency, resource, error, FFI or toolchain boundaries. Use when language-specific failure modes matter; do not load for routine syntax or when project conventions already decide the approach."
---

# Programming

Load only the language card needed for the current decision. Project conventions and dependencies win.

## Priority

1. Follow the nearest project `AGENTS.md`, manifest, architecture and style.
2. Reuse existing dependencies and patterns.
3. Load only the reference needed for the current failure mode.
4. Prefer the smallest implementation that satisfies observable behavior.

## Reference routing

- Python: `references/python/README.md`
- TypeScript: `references/typescript/README.md`
- Go: `references/go/README.md`
- Rust: `references/rust/README.md`

Reference recommendations are decision support, not reasons to replace an established stack or upgrade dependencies.

## Implementation and verification

- Inspect call sites and trust boundaries before changing behavior.
- Use strict types where they reduce material invalid states; avoid ceremony that adds no safety.
- Add or update tests when behavior changes or regression risk warrants it.
- Follow project verification first; otherwise run the closest relevant test, typecheck, lint or build.
- Do not repeat equivalent verification.

For behavior-preserving refactors, state the behavior that must remain unchanged, trace affected callers and boundaries, and use characterization coverage only when risk justifies it. Preview syntax-aware bulk rewrites and inspect the resulting diff. Do not combine a refactor with dependency upgrades or unrelated cleanup.

## Helper

`scripts/python/new-script.py` creates a no-overwrite PEP 723 script skeleton. Run it with `uv run --isolated`. If the default `uv` cache fails specifically with a sandbox permission error, retry once with `UV_CACHE_DIR=/tmp/codex-uv-cache`; do not relabel package resolution, network, script, or target failures as cache failures. If `uv` is missing, state why it is needed and propose the exact installation command. Preserve normal helper failures as execution errors.

Use `ast-grep` only when syntax-aware matching materially improves on `rg`. If it is missing, continue safely when practical or propose the exact installation command and wait for approval.
