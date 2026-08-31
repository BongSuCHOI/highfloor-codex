# Evaluation Governance

This document is the canonical cross-cutting contract for evaluating Highfloor
instructions, skills, agents, and workflow compositions.

It does not define runtime behavior. It defines what evidence is required to
claim that a runtime component or rule improves the system.

## Principles

1. **Baseline before treatment.** Freeze the comparison before changing the
   behavior under test.
2. **Hard failures are not averages.** Authority, scope, safety, false-PASS,
   provenance, and other critical regressions cannot be offset by improvements
   on unrelated tasks.
3. **Negative routing matters.** A component must be evaluated on tasks where it
   should *not* activate, not only tasks where it is useful.
4. **Measure the ceiling tax.** Tokens, latency, unnecessary questions,
   delegations, verification, false blocks, and coordination errors are part of
   the cost.
5. **Use independent ground truth.** The same artifact or reasoning path being
   tested must not define its own success.
6. **Protect held-out evidence.** Do not place unpublished held-out task payloads
   in the checkout visible to the system under test.
7. **Metrics are evidence, not the objective.** Do not optimize one proxy while
   hiding per-task or hard-boundary regressions.
8. **Every retained procedure is falsifiable.** Record what evidence would make
   the project simplify, absorb, merge, or remove it.

## Evaluation units

Evaluate these units separately when practical:

- **Global instruction block** — repository or portable instructions that alter
  general execution behavior.
- **Skill** — trigger, procedure, evidence responsibility, and stop condition
  loaded into the current context.
- **Agent** — delegation decision, isolated responsibility, evidence or artifact
  returned to the parent, and coordination cost.
- **Composition** — interaction among existing owners for a recurring state
  transition.

Avoid changing several unit types in one treatment unless the interaction
itself is the hypothesis.

## Evaluation record

A report should identify:

- baseline commit or immutable snapshot;
- treatment commit or patch;
- component and hypothesis under test;
- task-set identifier and integrity hash;
- whether task payloads were private during the run;
- model/profile and reasoning effort;
- tools, permissions, environment, and budgets;
- evaluator and independent ground-truth source;
- pre-registered target metrics;
- hard gates;
- overhead metrics;
- per-slice and worst-case results;
- conclusion: `RETAIN`, `REVISE`, `ABSORB`, `MERGE`, `PRUNE`, or `NO_CHANGE`;
- explicit rollback or removal condition.

A repository-linked report records evidence available in the repository. Absence
of a report is not proof that no private or historical evaluation exists; it is
only a statement that the repository does not currently link reproducible
comparative evidence for that claim.

## Frozen comparison

Hold constant unless the changed variable is the subject of the experiment:

- task payload;
- model/profile;
- reasoning effort;
- tool availability;
- permissions;
- environment and fixtures;
- timeout and cost budget;
- evaluator;
- ground truth.

If a metric definition changes, recompute it for both baseline and treatment.

## Task slices

Representative campaigns should include the slices relevant to the component.

### Narrow / direct

Examples include local edits, simple bugs, and prose-only work. These cases
measure over-planning, over-questioning, over-delegation, and duplicate
verification.

### Material ambiguity

Include tasks where a decision really is unresolved and tasks where
authoritative evidence already closes it. Measure both under-scaffolding and
false scaffolding.

### Runtime debugging

Include stable unit contracts, direct CLI or API reproducers, UI-only
reproductions, and legacy integration cases where a new test harness may be
brittle or expensive.

### Cross-boundary work

Include cases where an early thin end-to-end proof is useful and matched
negative cases where the boundary is already stable.

### Risk and reversibility

Use paired tasks with similar technical work but different consequence or
rollback characteristics.

### Persistent or resumed work

Include cases where an explicit ledger or terminal artifact is useful and
matched cases where it would be ceremony.

### Delegation

Include tasks where specialist isolation creates incremental evidence and tasks
where `default`, `worker`, or the parent context is already sufficient.

### Configuration slices

Run relevant profiles separately. Configuration is an evaluation dimension, not
a runtime behavioral branch.

### Negative routing

Every routing evaluation should include enough cases where the correct outcome
is one or more of:

- `NO_SKILL`
- `NO_AGENT`
- `NO_PLAN`
- `NO_EXTRA_VERIFY`
- direct execution

A component that helps only its positive examples but over-triggers widely is
not a clear improvement.

## Hard gates

The following failures should normally be treated as non-compensable within a
campaign:

- unauthorized external or destructive action;
- wrong repository, worktree, environment, or destination;
- scope violation;
- fabricated requirement or observed fact;
- false `PASS`;
- loss of material evidence or provenance;
- unsafe credential or secret handling;
- destructive migration without a required recovery boundary;
- explicit user-constraint violation.

A treatment that regresses a relevant hard gate should be rejected or redesigned
even when its average score improves.

## Quality measures

Choose only measures relevant to the hypothesis:

- task or acceptance success;
- critical omissions;
- regressions introduced;
- root-cause accuracy;
- evidence traceability;
- uncertainty labeling;
- recoverability;
- specialist incremental defect discovery.

## Cost and ceiling measures

Measure costs introduced by the component:

- total tokens;
- wall-clock latency;
- tool calls;
- delegation count;
- unnecessary questions;
- unnecessary plan or ledger artifacts;
- duplicate verification;
- false blocks;
- time to first useful end-to-end evidence;
- coordination or handoff errors;
- context consumed by unused instructions.

## Routing measures

Useful measures include:

- correct activation;
- false activation;
- missed activation;
- owner collision;
- unnecessary chaining;
- wrong-specialist selection;
- direct-path suppression.

False activation is a first-class reliability and efficiency failure.

## No universal scalar

Do not default to a universal weighted score that can trade a critical failure
for token savings or average quality.

Prefer this decision order:

1. relevant hard gates pass;
2. the pre-registered target failure improves;
3. per-slice and worst-case regressions remain within the stated tolerance;
4. added context, latency, coordination, and maintenance cost remain within
   budget.

Report raw or interpretable slice results even when a summary score is useful.

## Held-out and leakage rules

Unpublished held-out task payloads should live outside the checkout visible to
the system under test.

Before a campaign:

- freeze the task-set manifest;
- record an integrity hash;
- freeze the evaluator and metric definitions;
- record the baseline snapshot.

After a campaign:

- publish the report and enough provenance to audit the run;
- publish task payloads only when doing so does not compromise the next
  evaluation;
- rotate future hold-outs when previously private cases become public.

Do not tune prompts against the next held-out set.

## Success

A treatment is supportable when, for the stated scope:

- it reduces the pre-registered target failure on held-out evidence;
- it creates no relevant hard-gate regression;
- negative routing does not degrade beyond the stated tolerance;
- the benefit survives paraphrase, task rotation, or other reasonable leakage
  checks;
- independent ground truth supports the result;
- added token, latency, context, and coordination cost is justified;
- no configuration slice hides a critical tail regression behind another
  slice's gain.

## Failure and rollback

Revise, absorb, merge, prune, or revert when any material condition holds:

- evidence is only stylistic or anecdotal;
- baseline and treatment are indistinguishable at the task level;
- benefit appears only on authored or exposed examples;
- benefit disappears on rotated hold-outs;
- a hard gate regresses;
- negative routing cost exceeds the target benefit;
- another existing owner provides the same benefit more cheaply;
- the named method adds vocabulary but no distinct decision order, misuse guard,
  or proof boundary;
- an artifact is not used by a real handoff, recovery, or review;
- ablation shows that removing the rule or component preserves or improves the
  result.

`NO_CHANGE` is a valid conclusion.

## New methodology rule

Do not add a named method because it is famous, canonical, elegant, or useful in
the abstract.

Use this order:

1. identify a repeated failure in the current owner;
2. freeze evidence that demonstrates the failure;
3. compare `NO_CHANGE`, clarification, condensation, and absorption;
4. preserve a named method only if its structure uniquely changes decision
   order, prevents a recurring misuse, or defines a proof or replacement
   boundary that the existing owner lacks;
5. record the added cost and removal condition.

A new skill or agent is a later option, not the default representation of a new
method.

## Agent evaluation

A proposed or existing specialist should be compared against:

- the parent using no delegation when feasible;
- `default` or `worker`;
- the nearest existing specialist.

Measure both incremental quality and delegation cost.

A separate agent is justified by a durable distinction such as:

- isolated context reduces contamination or conflict;
- independent evidence is materially valuable;
- a different authority or permission boundary is required;
- parallel execution creates net value;
- a specialist repeatedly outperforms existing owners on held-out tasks after
  coordination cost.

Role naming or model configuration alone is not sufficient.

## Skill evaluation

A skill should be tested on:

- true-trigger tasks;
- ambiguous boundary tasks;
- `NO_SKILL` tasks;
- existing-owner alternatives;
- relevant configuration slices.

Retain the smallest owner that preserves the measured benefit.

## Instruction ablation

Highfloor's own instructions are subject to the same restraint rule as skills.

For semantic clusters in global instructions:

1. freeze a representative task set;
2. remove or simplify one cluster;
3. rerun the same comparison;
4. retain the cluster only when its removal creates a meaningful regression or
   when it protects a hard invariant that cannot yet be mechanically enforced.

This is especially important as native model capability improves.

## Evidence storage

`evals/` stores schemas, public reports, integrity metadata, and documentation.
It should not contain the next unpublished held-out task payloads.

See `evals/README.md`.
