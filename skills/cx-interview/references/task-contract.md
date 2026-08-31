# Task Contract

Use the smallest structure that preserves intent and makes completion observable. YAML is a presentation format, not a runtime requirement.

## Core shape

```yaml
goal: One observable outcome

constraints:
  - A hard boundary that implementation must preserve

non_goals:
  - A tempting adjacent outcome that is explicitly excluded

acceptance_criteria:
  - outcome: A user-visible or externally observable result
    verification: The evidence that would prove it

unknowns:
  - question: A material unresolved decision
    status: MISSING | CONFLICTING | BLOCKED

assumptions:
  - text: A provisional belief
    source: user | code | project-doc | research | inference | default
    evidence: Exact path, source, or reason
```

Add actors, data, permissions, rollout, compatibility, risk, or operations only when the task needs them. Do not require an ontology for ordinary work.

## Persistent execution extension

Add this only when the user selects or is considering a Codex Goal and the work
will continue across material stages:

```yaml
persistent_execution:
  terminal_artifact: The observable artifact or state that ends the objective
  required_gates:
    - outcome: A required intermediate state on the path to the artifact
      verification: Evidence that closes this gate
      status: OPEN | BLOCKED | CLOSED
  blocking_boundaries:
    - Missing authority, dependency, environment, credential, or external state
```

The extension keeps execution live without turning activity into success. It
does not add scope, authorize blocked work, or require every implementation
detail to be planned in advance. Omit it for an ordinary bounded task.

## Decision ledger

Track material entries with:

```text
value
status: CONFIRMED | INFERRED | DEFAULTED | MISSING | CONFLICTING | BLOCKED
source
evidence
```

`INFERRED` and `DEFAULTED` never become `CONFIRMED` merely because they look safe. A user may approve them explicitly.

## Coverage and reduction

Use this scaffold only when the request spans multiple materially distinct surfaces.

- Enumerate and confirm the top-level shape before questioning one surface in depth. Mark each surface `ACTIVE`, `DEFERRED`, or `OUT_OF_SCOPE`.
- Use stable item IDs only when they materially improve traceability; do not impose a fixed ontology on ordinary work.
- Account for every confirmed material item in the proposed contract. Additions and clarifications need no separate ceremony.
- If the proposal removes, merges, or replaces a confirmed item, show the old item and its proposed removal or substitution, then obtain explicit user approval.
- Treat readiness as non-monotonic. A later answer, contradiction, or changed fact can reopen a previously settled item.
- Approval of a reduction or substitution changes only the contract. It does not authorize implementation.

## Readiness

A contract is ready when:

- the goal identifies one coherent outcome;
- constraints and non-goals expose important boundaries;
- each required acceptance criterion is independently valuable and has a plausible verification path;
- every confirmed material item remains represented or has an explicitly approved reduction or substitution;
- no material entry remains `MISSING`, `CONFLICTING`, or `BLOCKED`;
- assumptions are visible with provenance;
- the user approves the complete contract.

Do not block on optional detail that can be safely decided during implementation without changing observable scope.

## Question policy

Ask the question with the highest expected effect on goal, architecture, cost, risk, or acceptance. Prefer one question. Combine questions only when the answers remain independently visible.

Resolve decisions and claims from the appropriate authority or evidence owner:

| Question | Default authority / evidence owner |
|---|---|
| Exact project fact | Repository code, configuration, or documentation |
| Current external fact | Current research or an authoritative external source |
| Product direction, preference, trade-off, or non-goal | Authorized stakeholder |
| End-user need or behavior claim | Direct user evidence, analytics, research, support evidence, or another credible empirical source; otherwise hypothesis |
| Implementation detail inside the approved boundary | Model or implementer |
| High-consequence external action | Explicit authorized human or role |

Authority to choose a direction and evidence that a factual claim is true are
different dimensions. A stakeholder may knowingly authorize a hypothesis; that
does not promote the hypothesis to observed evidence.

When a product-problem claim materially affects the contract, optionally record:

```yaml
problem_evidence:
  - claim: ""
    status: observed | supported | hypothesis
    source: ""
    contract_impact: ""
```

Do not require this block for ordinary implementation work.

## Batched questioning (optional scaffold)

Use the one-question default for a single decisive unknown. When several
independent material decisions are already answerable, batch them instead of
walking one at a time:

- Sketch a small decision tree: each material decision may hang off earlier
  answers. A question is askable now when its prerequisites are settled.
- Ask every currently askable question in one numbered round, each with a
  recommended answer, then wait for the user's answers.
- A question that depends on an answer still open in this round belongs to a
  later round. After each round, recompute what became askable and continue.
- Readiness rules do not change: the contract closes when no material entry
  remains `MISSING`, `CONFLICTING`, or `BLOCKED`. Optional implementation
  detail never blocks readiness, and an unasked optional question is not a
  gap.

## Durable decision records

The interview records intent; it does not edit repository documentation on its
own authority. When the user settles or rejects a decision with a load-bearing
reason that a future session would otherwise re-litigate, offer to record that
decision in the repository's decision documentation, for example an ADR under
`docs/adr/` or a domain glossary entry. Perform the write only after explicit
user approval, and skip ephemeral or self-evident reasons.

## Exit recommendation

Recommend exactly one option and attach `(Recommended)` to its label. The user retains final control.

### Implement now

Recommend when work is bounded, prerequisites exist, risk is ordinary, and completion is plausible in the current task. A plan may still be created internally.

### Save contract

Recommend when the user requested planning or handoff, prerequisites or authority are missing, or implementation should deliberately wait.

### Start Codex Goal

Recommend when work spans multiple independent workstreams, repositories, services, migrations, deployment or monitoring, or likely multiple tasks or sessions. A recommendation is not permission to create a Goal; wait for explicit user selection.

Before this recommendation, make the terminal artifact and required gates
observable. If a material gate cannot yet be defined because intent or
authority is unresolved, recommend saving the contract instead.

## Simulation: greenfield alarm app

Input:

```text
I want an alarm app, but the idea is vague.
```

Evidence and interview:

```text
Q1 platform → macOS menu-bar app
Q2 source → Google Calendar
Q3 key outcome → notify five minutes before meetings
Q4 boundaries → no mobile sync, no calendar mutation
```

Contract:

```yaml
goal: Notify the user on macOS five minutes before Google Calendar meetings
constraints:
  - Read-only calendar access
  - Background operation
non_goals:
  - Mobile application
  - Calendar creation or editing
acceptance_criteria:
  - outcome: The user can connect and disconnect one calendar account
    verification: Account state and token removal are observed
  - outcome: A notification appears five minutes before a meeting
    verification: A controlled near-future event produces a macOS notification
unknowns: []
assumptions: []
```

Exit:

```text
Implement now (Recommended) — one app, bounded integration, observable criteria
Save contract
Start Codex Goal
```

## Simulation: unclear brownfield improvement

Input:

```text
This service feels bad. Improve it.
```

Do not invent the problem. Inspect the current flow, separate observed facts from product hypotheses, use analytics or research when available, present a small decision set, and obtain the user's chosen outcome before drafting the contract.
