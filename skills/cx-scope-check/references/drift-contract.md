# Drift Contract

## Baseline

Prefer:

1. approved task contract and amendments;
2. explicit current user request;
3. current project plan and closest rules;
4. prior task history recovered through `$cx-coding-agent-sessions`.

State when the baseline is incomplete. Do not reconstruct user intent from model memory alone.

## Evidence inputs

- changed and untracked files;
- manifest, lockfile, dependency, and runtime changes;
- public API, schema, migration, and persistent-state changes;
- external calls, deployment, publication, or permission changes;
- accepted, removed, or unverified criteria;
- approved plan and current work state.

## Classification

### HARD_VIOLATION

- violates a hard constraint;
- implements an explicit non-goal;
- performs an external or destructive action without required authority;
- changes a compatibility or security boundary the contract freezes.

### SCOPE_REVIEW

- adds a new user-visible outcome;
- adds a repository, service, dependency class, migration, or operational workstream not implied by the contract;
- changes API or schema semantics;
- substitutes a materially different architecture with new trade-offs.

### NOT_PROVEN

- drops or weakens an acceptance criterion;
- claims preservation without evidence;
- cannot recover the approved baseline;
- lacks verification for a relevant changed surface.

### ON_TRACK

- internal refactoring preserves observable behavior and boundaries;
- additional files are necessary implementation detail;
- a dependency is already authorized or clearly implied by the approved architecture;
- changed wording preserves the same semantic outcome.

## Non-signals

Do not declare drift from these alone:

- file count;
- line count;
- renamed local symbols;
- a different implementation order;
- lexical distance between contract and code;
- model confidence.

## Simulation

Contract:

```text
Goal: owner creates a copyable invite link
Constraint: no email provider
Non-goal: RBAC redesign
```

Current changes:

```text
+ invite token table
+ owner permission check
+ SMTP provider
+ generalized RBAC engine
```

Verdict:

```text
HARD_VIOLATION
- SMTP provider violates "no email provider"

SCOPE_REVIEW
- generalized RBAC engine implements an explicit non-goal

ON_TRACK
- invite token table and owner permission check support approved outcomes
```

Recovery: remove the violating work or request a contract amendment. Do not silently normalize the contract to fit the implementation.
