# Evidence Contract

## Evidence strength

Prefer the strongest practical evidence that directly proves the claim:

1. Current observed behavior or state with valid provenance after the final relevant change
2. Focused automated test exercising the behavior
3. Mechanical build, type, schema, or static check
4. Source inspection or diff reasoning
5. Plan, log claim, or model assertion

Lower evidence may support a verdict only when the criterion itself is static. A successful command message does not prove its claimed side effect.

## Evidence validity and reuse

Evidence remains current when the relevant artifact, criterion, environment, configuration, and observed state have not changed since collection and its provenance can be identified.

- Reuse current, relevant, and sufficient evidence.
- Rerun only when a relevant input changed, provenance is unclear, coverage is insufficient, or the criterion requires a new observation.
- Do not replace direct current evidence merely to produce a newer timestamp.
- Mark evidence stale when a relevant change can invalidate its claim.

## Per-criterion record

```yaml
criterion: The required outcome
status: PASS | FAIL | NOT_PROVEN
evidence:
  - command: Exact command, if any
    result: Exit status and relevant output
  - artifact: Exact file, response, screenshot, or state
    observation: What was directly observed
limitations:
  - Unobserved surface or environmental limit
```

## Verdict rules

- `PASS`: direct evidence establishes the required outcome.
- `FAIL`: direct evidence contradicts the required outcome or a required mechanical gate fails.
- `NOT_PROVEN`: evidence is absent, stale, indirect, blocked, or covers only part of the criterion.

Overall:

```text
any FAIL        → FAIL
else any NOT_PROVEN → NOT_PROVEN
else             → PASS
```

Do not average criteria. Do not convert uncertainty into a numeric score.

## Scope-proportional paths

### Small documentation or configuration change

- inspect affected content;
- run the closest format or parse check;
- inspect the relevant diff;
- stop.

### Code behavior

- run the nearest regression test;
- exercise the changed behavior when practical;
- inspect the resulting state, not only stdout.

### API

- send a representative request;
- observe status, payload, persistent effect, and a relevant rejection path.

### UI

- use browser automation for interaction and capture;
- route rendered judgment to `$cx-visual-qa`;
- reuse its current and sufficient evidence when the rendered state has not changed.

### External or unavailable environment

- verify local and static claims;
- mark the unavailable requirement `NOT_PROVEN`;
- state the exact missing authority, environment, credential, or state.

## Simulation: invite-link feature

```text
AC1 owner creates an expiring invite link
  Evidence: POST request returns 201 with URL and expiry
  Evidence: persisted invite row matches expiry
  Status: PASS

AC2 member cannot create a link
  Evidence: member request returns 403
  Status: PASS

AC3 invite joins the team
  Evidence: route code and unit test exist
  Limitation: no database runtime available
  Status: NOT_PROVEN

Overall: NOT_PROVEN
```

The model may choose a better evidence path. It may not claim overall `PASS` while AC3 remains unobserved.
