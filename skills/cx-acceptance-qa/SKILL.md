---
name: cx-acceptance-qa
description: "Verify completed or claimed work against explicit acceptance criteria using scope-proportional mechanical and observed evidence. Use for QA, release or handoff approval, task-contract verification, or whenever a behavior-bearing artifact must be proven. Do not run a second audit after equivalent evidence already proves the same claim; route rendered UI judgment to cx-visual-qa and unresolved failure diagnosis to cx-debugging."
---

# Acceptance QA

Prove the requested outcome with the smallest sufficient evidence set. Do not replace evidence with a confidence score.

## Method

- Treat acceptance criteria as observable promises from the approved specification, not as implementation steps or a subjective quality score.
- First establish what must be true, then gather the smallest current evidence that can prove or contradict it.
- Prefer acting verification and observed effects over optimistic source reading or success messages.
- Separate a demonstrated product failure (`FAIL`) from an unavailable or insufficient proof path (`NOT_PROVEN`).

## Hard floor

- Resolve the artifact, approved contract or quality bar, and affected surface before judging.
- Attach current, relevant, and sufficient evidence to every acceptance criterion.
- Reuse sufficient evidence when the relevant artifact, criterion, environment, and state have not changed; do not rerun it only to make it newer.
- Prefer observed behavior over source text, plans, screenshots of logs, or claimed success.
- Return `NOT_PROVEN` when required behavior cannot be observed or evidence is missing.
- Mechanical failure cannot be overruled by semantic optimism.
- Do not repeat equivalent tests, builds, reviews, or visual checks.

## Workflow

1. Recover explicit acceptance criteria from the approved task contract, user request, or nearest project rules. Ask only if the missing quality bar would materially change the verdict.
2. Design the minimum evidence path:
   - **Mechanical**: nearest relevant test, typecheck, lint, build, schema, or diff check.
   - **Observable**: actual command effect, file, API response, persisted state, interaction, or rendered surface.
   - **Semantic**: whether the observed evidence satisfies the criterion's meaning.
   - **Failure topology**: when behavior depends on state, thresholds, asynchronous downstream work, repetition, runtime identity, or cleanup footprint, select the smallest partition that could materially change the verdict.
3. Reuse qualifying evidence from the current state. Otherwise execute the applicable path with bounded commands. Record command, result, artifact path, observation, and any validity limitation.
4. Map each criterion to `PASS`, `FAIL`, or `NOT_PROVEN`. Keep the verdict within the states and failure paths actually covered; a passing happy path does not prove a broader behavior claim.
5. Set the overall verdict:
   - `PASS` only when every required criterion passes.
   - `FAIL` when any required criterion is contradicted by evidence.
   - `NOT_PROVEN` when none fail but at least one lacks sufficient evidence.
6. Report blocking items first, then the evidence map and one next action. Do not fix failures unless the user also requested implementation.

## Adaptive freedom

- Choose stronger or cheaper evidence than the scaffold when it proves the same claim.
- Add adversarial probes when risk or the implementation shape warrants them.
- Omit irrelevant stages. A documentation-only change may need a focused content and diff check; a behavior-bearing API needs observation.
- Do not use numeric scores or model majority as default authority.

## Chains

- Use `$cx-visual-qa` for final rendered web, mobile, slide, or terminal UI judgment; reuse its result rather than repeating capture.
- Use `$cx-browser-automation` to drive browser state and capture evidence.
- Use `$cx-debugging` when a failed criterion needs cause isolation.
- Return specification gaps to `$cx-interview`; do not silently rewrite the contract during evaluation.

Load `references/evidence-contract.md` for evidence strength, verdict rules, artifact examples, and simulations. Load `references/upstream.md` only for provenance or maintenance work.
