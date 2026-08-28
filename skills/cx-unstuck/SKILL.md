---
name: cx-unstuck
description: "Break planning, product, architecture, or implementation-strategy deadlock by identifying the load-bearing failed assumption and its cheapest discriminating experiment before producing bounded alternatives. Use when the same approach has failed repeatedly, constraints conflict, progress stalls, or the user asks for another angle. Use cx-debugging first for unresolved runtime failures; do not trigger a persona fan-out or replace evidence with brainstorming."
---

# Unstuck

Change the frame only after identifying why the current approach is stuck. Produce a small decision surface, not an idea dump.

## Method

- Collapse the deadlock to the one load-bearing assumption whose failure would make the current approach untenable, then find the cheapest experiment or decision that can discriminate it.
- Use lateral thinking to challenge the frame that keeps reproducing the deadlock, not merely to generate more variants of the same approach.
- Apply only the useful perspective—researcher, contrarian, simplifier, architect, or another evidence-backed lens—without role-play or mandatory persona fan-out.
- Add alternatives only when the first discriminating result does not already resolve the path. Keep the output centered on one root, not a checklist of objections.
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
3. Identify the load-bearing assumption that must hold for the current approach to work. Collapse related objections to the single root whose failure makes the others secondary.
4. Define the cheapest discriminating experiment or decision for that root. Execute it when it is safe, authorized, and cheaper than expanding the plan; otherwise report the exact check and required authority or evidence.
5. If the result already selects or kills the approach, return that conclusion without manufacturing alternatives. Otherwise select only the useful lens or lenses:
   - **Researcher** for a missing external or repository fact.
   - **Contrarian** for a repeated or untested assumption.
   - **Simplifier** for oversized scope or unnecessary coupling.
   - **Architect** for a structural problem that recurs across local fixes.
6. Produce at most two materially different alternatives. For each include:
   - challenged assumption;
   - preserved and endangered constraints;
   - evidence expected from the discriminating experiment or decision;
   - main downside.
7. Recommend one only when evidence supports it. Otherwise expose the decision cleanly.
8. Record rejected approaches so the originating workflow does not cycle back without new evidence.
9. Return to the originating workflow. If the choice changes the approved contract, require a `$cx-interview` amendment before implementation.

## Adaptive freedom

- Use a better reasoning method than the named lenses when it produces a clearer bounded decision.
- Combine lenses without role-play or subagent fan-out.
- Return only the root and discriminating experiment when alternatives would add no decision value.
- Expand beyond two alternatives only when the user explicitly asks for broad ideation.

## Chains

- Runtime symptom or unknown cause → `$cx-debugging`.
- Missing current external fact → `$cx-ultraresearch`.
- Approved goal, constraint, non-goal, or outcome changes → `$cx-interview`.
- Chosen implementation path exceeds the current surface → `$cx-scope-check`.

Load `references/reframing-lenses.md` for lens selection, output shape, and simulations. Load `references/upstream.md` only for provenance or maintenance work.
