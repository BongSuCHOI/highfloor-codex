---
name: cx-scope-check
description: "Compare current changes and decisions with an approved task contract to detect unapproved scope, constraint, non-goal, dependency, API or schema, and acceptance-coverage drift. Use for explicit drift checks, after resume, compaction, or handoff, at major phases of long work, or when changes exceed the expected surface. Do not run on every turn or treat legitimate implementation detail as drift."
---

# Scope Check

Compare approved intent with current reality. Report drift without reverting or expanding scope.

## Method

- Treat the approved specification as an execution contract: goal, constraints, non-goals, authority, and observable outcomes are the baseline until the user approves an amendment.
- Detect semantic drift, not textual distance. More files or a different implementation are not drift when the approved behavior and boundaries remain intact.
- Preserve legitimate implementation freedom while making unauthorized outcome, dependency, interface, or authority changes visible.
- A scope check reports and routes a decision; it does not silently revise the contract or mutate the work.

## Hard floor

- Use the approved task contract as the primary baseline. If absent, use the explicit user request and project plan, and state that the basis is weaker.
- Treat constraint violations, implemented non-goals, and unauthorized external actions as hard violations.
- Surface requirement or scope changes for user approval.
- Do not classify necessary internal implementation detail as drift when it preserves the approved observable contract.
- Do not use lexical similarity or a single numeric drift score as authority.

## Workflow

1. Reconstruct the baseline: goal, constraints, non-goals, acceptance criteria, approved amendments, expected surfaces, and execution authority.
2. Inspect current reality: changed files, manifests and dependencies, API or schema changes, persistent state, external effects, plan state, and acceptance coverage.
3. Compare semantics and classify findings:
   - `HARD_VIOLATION`: an approved constraint, non-goal, or authority boundary is violated.
   - `SCOPE_REVIEW`: a new outcome, dependency, interface, workstream, or behavior needs approval.
   - `NOT_PROVEN`: an approved criterion or preservation claim lacks evidence.
   - `ON_TRACK`: changes remain within the contract, including legitimate implementation detail.
4. Cite the exact contract item and current evidence for each finding.
5. Recommend the smallest recovery: return to approved scope, request a contract amendment, or collect missing evidence.
6. Never edit, revert, or broaden the work solely because this skill found drift.

## Adaptive freedom

- Use stronger semantic comparison than the checklist when available.
- Ignore file-count growth by itself; judge whether observable scope or risk changed.
- Add domain-specific drift classes when they map back to an approved boundary.
- Stop after the affected contract surface is covered.

## Chains

- Use `$cx-coding-agent-sessions` only when the original contract or approved amendment must be recovered from prior task history.
- Return proposed contract changes to `$cx-interview` for explicit amendment and approval.
- Use `$cx-acceptance-qa` when drift is resolved but acceptance coverage remains unproven.
- Use `$cx-debugging` when apparent drift may instead be a runtime or environment mismatch.

Load `references/drift-contract.md` for classification rules, non-examples, evidence inputs, and simulations. Load `references/upstream.md` only for provenance or maintenance work.
