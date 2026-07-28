# Workflow Recipes

These recipes show composition, not a mandatory lifecycle. Route by the current
state and stop when the owned outcome is complete.

## Concepts

| Concept | Question it answers | Owner |
|---|---|---|
| Task Contract | What does success mean? | `cx-interview` when ambiguity is material |
| Plan | How should approved work be sequenced? | Codex Plan or `planner` |
| Goal | Should the objective remain active across continued work? | Codex Goal, only when the user explicitly chooses it |
| Scope verdict | Does current work still match the contract? | `cx-scope-check` |
| Acceptance verdict | Do current artifacts prove the criteria? | `cx-acceptance-qa` |

## Recipe A: Product request with unclear boundaries

Use when actor, outcome, constraints, non-goals, or acceptance behavior could
change the implementation materially.

1. Run `cx-interview` until the remaining unknowns no longer change the
   result, then obtain the user's approval of the Task Contract.
2. Follow one of the skill's three recommended exits: implement now, save the
   contract, or start a Codex Goal for persistent multi-stage work.
3. If implementation begins now, use `explorer` to find current ownership or
   `architect` to examine a material boundary only when needed.
4. Create a Codex Plan or use `planner` only when complexity makes sequencing
   useful.
5. Implement and run the closest check that proves the changed behavior.
6. Use `cx-acceptance-qa` only when a handoff or release needs a formal verdict.

Do not create a Goal unless the user explicitly chooses persistent tracking.

## Recipe B: Narrow, already-specified edit

1. Read the nearest project rules and inspect the exact target.
2. Implement the requested change directly.
3. Run the nearest check that matches the change's risk.
4. Stop when that evidence proves the request.

Do not add `cx-interview`, planning, multiple reviewers, or formal acceptance
when the task is already clear and low risk.

## Recipe C: Runtime bug

1. Choose one diagnostic owner. Use `cx-debugging` in the current task, or
   delegate to `debugger` when a noisy investigation benefits from isolation.
2. Build the smallest reproduction that still shows the failure.
3. List the plausible causes and collect evidence that distinguishes them.
4. State the cause only when the evidence proves where the failure begins.
5. If the user requested a fix, make the smallest change that addresses the
   proven cause.
6. Run a focused regression check that would detect the failure if it returned.

For browser-only symptoms, use `browser-debugger` or
`cx-browser-automation` for reproduction. `cx-visual-qa` owns only the final
rendered visual verdict, not runtime cause.

## Recipe D: Broad UI redesign

1. Use `cx-design-director` to establish the direction from the existing
   design system and first-party references.
2. Use `cx-browser-automation` only when the current product must be observed
   or operated in a browser.
3. Implement the approved direction.
4. Use `accessibility-tester` when interaction or semantics changed.
5. Use `cx-visual-qa` to judge the result from current rendered evidence.

If the request is specifically about common AI UI patterns, add
`cx-slopslap` as a constraint owner. Do not use it as a generic redesign phase.

## Recipe E: Deep research

1. Use `cx-ultraresearch` after the user explicitly requests deep research.
2. Define the questions and evidence needed to answer them.
3. Use `docs-researcher` for a separate API or version question that requires
   authoritative documentation.
4. Use `research-analyst` only when an independent comparison will improve the
   evidence.
5. Use `cx-insane-search` only when ordinary access cannot read a relevant
   public page.
6. Stop when the available evidence is sufficient to answer the questions.

Separate documentation claims, code evidence, observed runtime behavior, and
inference.

## Recipe F: Resume after lost context

1. Use `cx-coding-agent-sessions` to recover the exact prior task or
   transcript.
2. Identify the approved Task Contract and recorded decisions.
3. Run `cx-scope-check` if current work may have crossed the contract's
   boundary.
4. Continue when the contract still fits. Return to `cx-interview` only when a
   material change needs user approval.

Do not treat remembered paraphrases as authoritative when the raw transcript is
available.

## Recipe G: High-risk infrastructure or data change

1. Begin from an approved Task Contract.
2. Use `explorer` or `architect` to establish ownership and material
   boundaries.
3. Ask `risk-reviewer` to identify the consequences that change the execution
   plan.
4. Assign implementation to `infra-engineer`, `database-engineer`, or
   `data-engineer`, whichever owns the change.
5. Add `security-reviewer` or `reliability-reviewer` only when that boundary
   materially changed.
6. Prove the rollback or recovery path.
7. Run formal acceptance only when release authority requires it.

Assign write ownership precisely. Reviewers remain read-only and should not
silently implement fixes.

## Recipe H: Release preparation

1. Follow [`docs/RELEASING.md`](RELEASING.md) and close the version,
   changelog, licensing, and migration decisions.
2. Run `./scripts/validate.sh` and `./scripts/test-install.sh`.
3. Use `reviewer` for material code changes.
4. Add a security or reliability specialist only when the release changed
   that boundary.
5. Use `technical-writer` when release notes or migration guidance need a
   dedicated pass.
6. Use `cx-acceptance-qa` only when the release process requires a formal
   verdict against the checklist.

The release verdict must distinguish locally proven behavior from external host
state that remains `NOT_PROVEN`.

## Anti-patterns

- Running every skill because it exists.
- Delegating the same question to multiple agents without independent evidence
  value.
- Treating a Plan as permission to expand scope.
- Treating a Goal as the definition of success.
- Asking `cx-acceptance-qa` to diagnose a failure.
- Asking `cx-visual-qa` to infer UI quality from source alone.
- Using `cx-insane-search` before ordinary public web access fails.
- Running `cx-slopslap` on any UI task without an explicit slop-removal request.
- Re-verifying an unchanged fact with equivalent tools.
