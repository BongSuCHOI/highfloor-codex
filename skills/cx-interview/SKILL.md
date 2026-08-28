---
name: cx-interview
description: "Clarify materially ambiguous product, feature, workflow, or brownfield improvement requests into an approved task contract, or synthesize an already-resolved conversation into that contract without restarting discovery. Use when the user asks for an interview, requirements, a specification, help deciding what to build, asks you to grill or stress-test an idea, plan, or design, or when unresolved goals, constraints, non-goals, acceptance criteria, or product decisions would materially change the result. Do not use for a narrow already-specified edit, pure diagnosis, or a decision already settled by project rules."
---

# Interview

Create the minimum approved contract needed for implementation. When the
material decisions already exist in the conversation and project evidence,
synthesize them without replaying discovery.

## Method

- Use Socratic questions to expose hidden assumptions and make a vague purpose concrete; ask what the desired thing is before prescribing how to build it.
- For requests with multiple material surfaces, establish the top-level shape before probing one thread deeply; diverge only across materially different ambiguity threads, then converge through restatement.
- Treat clarity as non-monotonic: later answers or evidence may reopen an earlier decision. Use repository and external evidence as facts about the current world, not as substitutes for user product decisions.
- The interview clarifies and records intent. It does not implement the result or silently convert model assumptions into requirements.

## Hard floor

- Distinguish user decisions, exact code or document facts, external evidence, model inference, and defaults.
- Inspect available project evidence before asking the user factual brownfield questions.
- Never promote an inference, hypothesis, or safe-looking default into a confirmed requirement.
- Keep material unknowns and conflicts visible.
- Require user approval before treating the task contract as implementation authority.
- Reopen approval when a proposed change alters the goal, constraints, non-goals, or observable outcomes.
- Do not silently drop, merge, or replace a previously confirmed material item. Show the proposed reduction or substitution and obtain explicit approval; that approval does not authorize implementation.

## Workflow

1. Classify the request as greenfield, brownfield, or mixed. Read the nearest project rules and relevant current state.
2. Choose the minimum mode:
   - **Clarification:** material decisions remain unresolved, so build the decision ledger and ask only questions whose answers change the result.
   - **Synthesis:** the conversation and project evidence already resolve the material decisions, so recover them into the ledger, verify current brownfield facts, and ask only about a genuine surviving fork. Do not restart the interview to refill a template.
3. Build or recover a decision ledger covering goal, users or actors, constraints, non-goals, outcomes, verification, unknowns, and assumptions with provenance. If the request spans multiple material surfaces, enumerate the top-level shape and mark each surface active, deferred, or out of scope before deep questioning.
4. Resolve exact facts from code, configuration, documentation, or current research. Label product hypotheses as hypotheses.
5. In clarification mode, prefer the highest-impact unresolved decision and one question at a time; when several independent material decisions are pending, use the batched-round scaffold in `references/task-contract.md`. In synthesis mode, proceed silently when the available evidence resolves the item.
6. Draft a task contract using `references/task-contract.md`. Keep optional sections optional.
7. Close only when no material item remains `MISSING`, `CONFLICTING`, or `BLOCKED` and every confirmed material item is represented or has an explicitly approved reduction or substitution. Then present the complete contract for explicit approval.
8. After approval, recommend one exit based on scope and explain why:
   - **Implement now (Recommended)** for bounded work likely to finish in the current task.
   - **Save contract (Recommended)** when the user requested planning or execution prerequisites are missing.
   - **Start Codex Goal (Recommended)** for multi-workstream, multi-repository, migration, deployment, monitoring, or multi-session work.
9. Before recommending a Codex Goal, add the optional persistent-execution block from the task-contract reference when terminal-artifact and gate visibility will materially improve continued execution.
10. Never create a Codex Goal from the recommendation alone. Wait for the user to select it. If the user selects implementation, continue in the same task and create a plan only when complexity warrants one.

## Adaptive freedom

- Use the question sequence as a scaffold, not a script.
- Combine related questions when their decisions remain distinct and the result is easier to answer.
- Skip questions already answered by authoritative evidence.
- Add domain-specific contract fields when they improve execution without replacing the core goal, boundary, outcome, and verification fields.
- Prefer a short, sharp contract over a ceremonial PRD.

## Chains

- Route broad UI or product-flow discovery to `$cx-design-director`, then return with evidence and decisions.
- Route current external comparisons or contested facts to `$cx-ultraresearch`, then return with sourced options.
- After approval: implementation may invoke `$cx-scope-check` on a drift trigger, `$cx-unstuck` on a genuine deadlock, and `$cx-acceptance-qa` for final proof.

Load `references/task-contract.md` for the contract schema, readiness rules, batched questioning scaffold, durable decision records, exit recommendation, and examples. Load `references/upstream.md` only for provenance or maintenance work.
