---
name: cx-debugging
description: "Diagnose runtime bugs, crashes, hangs, wrong behavior, silent failures, debugger sessions and binary behavior using scoped reproduction and evidence that distinguishes plausible causes. Do not use for routine code review, requirement clarification, planned refactoring, or an acceptance verdict; use cx-acceptance-qa for the verdict and this skill only when a failure needs cause isolation."
---

# Debugging

Diagnose before fixing unless the user explicitly requests implementation.

## Choose the smallest investigation

- For a direct local symptom, reproduce once, inspect the nearest evidence and state the cause.
- For an unclear, intermittent or multi-layer failure, record the exact runtime/build identity, form distinguishable hypotheses and collect only evidence that separates them.
- When execution is blocked, use `references/methodology/partial-runtime-evidence.md` and state the confidence limit.

Confirm a root cause by showing that it predicts the failure or that changing the suspected condition changes the result. If asked to fix, make the smallest change and run the closest regression check. Remove temporary instrumentation, restore modified runtime state and report remaining uncertainty. Use a journal only for repeated rounds or multiple temporary artifacts.

If the same exact symptom remains after the proposed fix, treat the previous
cause or its claimed scope as incomplete. Reproduce that counterexample under
the same runtime identity, revise the distinguishable hypotheses, and gather
new separating evidence before changing another parameter or stacking another
fix.

## Runtime references

Load only the matching runtime card:

- Python: `references/runtimes/python.md`
- Node.js, Bun, Deno: `references/runtimes/node.md`
- Go: `references/runtimes/go.md`
- Rust: `references/runtimes/rust.md`
- Native binary: `references/runtimes/native-binary.md`
- Bundled JavaScript binary: `references/runtimes/bundled-js-binary.md`

Use `references/methodology/cleanup.md` after a complex session with temporary processes, files or debugger settings.

## Specialist tools

Route browser-only reproduction to `$cx-browser-automation`. Use LLDB/GDB for native processes and load `references/tools/ghidra.md`, `pwndbg.md` or `pwntools.md` only when that capability is warranted and authorized.

For one-off Python tools, prefer pinned `uv run --with` or `uvx`; for one-off Node CLIs, prefer pinned `npx`. Reuse the repository environment when the debugger must import the target project. Do not install tools globally. If a required runtime, debugger, OS package or browser binary is missing, explain the capability and propose the exact platform command. Preserve attach, symbol, permission, target-process and script failures as their real failure type.
