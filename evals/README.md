# Evaluation Evidence

`evals/` stores public evaluation structure and post-run evidence for Highfloor.
The canonical policy is [`docs/EVALUATION.md`](../docs/EVALUATION.md).

## What belongs here

- schemas for task-set metadata and published result records;
- integrity identifiers and provenance for frozen task sets;
- public reports after a campaign;
- enough environment and comparison metadata to audit a claim.

## What does not belong here

Do not commit the next unpublished held-out task payloads, expected answers,
private fixtures, or evaluator secrets into the checkout visible to the system
under test. Keep those in an external evaluation workspace. Before a campaign,
record the task-set identifier and integrity hash. After publication, rotate the
next hold-out if the old payload becomes visible.

A public report is evidence only for the scope it actually measured. Absence of
a public report means repository evidence is not linked; it does not prove that
private or historical evaluation never occurred.

## Structural validation

Run:

```sh
python3 scripts/validate_evals.py
```

The validator checks repository-local structure and published JSON records. It
does not call models, compute quality scores, or decide that a component is
valuable.
