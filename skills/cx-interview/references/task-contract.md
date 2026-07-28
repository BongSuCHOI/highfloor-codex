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

## Decision ledger

Track material entries with:

```text
value
status: CONFIRMED | INFERRED | DEFAULTED | MISSING | CONFLICTING | BLOCKED
source
evidence
```

`INFERRED` and `DEFAULTED` never become `CONFIRMED` merely because they look safe. A user may approve them explicitly.

## Readiness

A contract is ready when:

- the goal identifies one coherent outcome;
- constraints and non-goals expose important boundaries;
- each required acceptance criterion is independently valuable and has a plausible verification path;
- no material entry remains `MISSING`, `CONFLICTING`, or `BLOCKED`;
- assumptions are visible with provenance;
- the user approves the complete contract.

Do not block on optional detail that can be safely decided during implementation without changing observable scope.

## Question policy

Ask the question with the highest expected effect on goal, architecture, cost, risk, or acceptance. Prefer one question. Combine questions only when the answers remain independently visible.

Resolve facts from authoritative sources:

```text
Exact project fact       → inspect code/config/docs
Current external fact    → research
Product preference       → user
Trade-off or non-goal    → user
Implementation detail    → model, inside approved boundaries
```

## Exit recommendation

Recommend exactly one option and attach `(Recommended)` to its label. The user retains final control.

### Implement now

Recommend when work is bounded, prerequisites exist, risk is ordinary, and completion is plausible in the current task. A plan may still be created internally.

### Save contract

Recommend when the user requested planning or handoff, prerequisites or authority are missing, or implementation should deliberately wait.

### Start Codex Goal

Recommend when work spans multiple independent workstreams, repositories, services, migrations, deployment or monitoring, or likely multiple tasks or sessions. A recommendation is not permission to create a Goal; wait for explicit user selection.

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
