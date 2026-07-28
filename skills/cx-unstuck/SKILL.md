---
name: cx-unstuck
description: "Break planning, product, architecture, or implementation-strategy deadlock by challenging the failed approach and producing bounded alternatives. Use when the same approach has failed repeatedly, constraints conflict, progress stalls, or the user asks for another angle. Use cx-debugging first for unresolved runtime failures; do not trigger a persona fan-out or replace evidence with brainstorming."
---

# Unstuck

Change the frame only after identifying why the current approach is stuck. Produce a small decision surface, not an idea dump.

## Method

- Use lateral thinking to challenge the frame or assumption that keeps reproducing the deadlock, not merely to generate more variants of the same approach.
- Apply only the useful perspective—researcher, contrarian, simplifier, architect, or another evidence-backed lens—without role-play or mandatory persona fan-out.
- Diverge into a few materially different paths, then converge with constraints, downsides, and the smallest discriminating experiment.
- Creative alternatives remain advisory until the user approves any required contract change.

## Hard floor

- State the problem, current approach, constraints, failed attempts, and available evidence before proposing alternatives.
- Do not repeat a failed approach without new evidence.
- Mark which assumption each alternative challenges and which constraints it preserves or risks.
- Do not disguise a contract change as an implementation workaround.
- Route unresolved runtime causes to `$cx-debugging` before strategic reframing.

## Workflow

1. Reconstruct the stuck point and distinguish runtime failure, missing fact, conflicting requirement, oversized scope, and structural recurrence.
2. Stop and use `$cx-debugging` when cause isolation is still the real task.
3. Select only the useful lens or lenses:
   - **Researcher** for a missing external or repository fact.
   - **Contrarian** for a repeated or untested assumption.
   - **Simplifier** for oversized scope or unnecessary coupling.
   - **Architect** for a structural problem that recurs across local fixes.
4. Produce at most three materially different alternatives. For each include:
   - challenged assumption;
   - preserved and endangered constraints;
   - smallest discriminating experiment or decision;
   - main downside.
5. Recommend one only when evidence supports it. Otherwise expose the decision cleanly.
6. Record rejected approaches so the originating workflow does not cycle back without new evidence.
7. Return to the originating workflow. If the choice changes the approved contract, require a `$cx-interview` amendment before implementation.

## Adaptive freedom

- Use a better reasoning method than the named lenses when it produces a clearer bounded decision.
- Combine lenses without role-play or subagent fan-out.
- Produce one alternative when only one credible path exists.
- Expand beyond three alternatives only when the user explicitly asks for broad ideation.

## Chains

- Runtime symptom or unknown cause → `$cx-debugging`.
- Missing current external fact → `$cx-ultraresearch`.
- Approved goal, constraint, non-goal, or outcome changes → `$cx-interview`.
- Chosen implementation path exceeds the current surface → `$cx-scope-check`.

Load `references/reframing-lenses.md` for lens selection, output shape, and simulations. Load `references/upstream.md` only for provenance or maintenance work.
