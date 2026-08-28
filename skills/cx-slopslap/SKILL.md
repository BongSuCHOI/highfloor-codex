---
name: cx-slopslap
description: "Audit and remove statistical AI-slop from web and product UI using a vendored taxonomy, static candidate scanner, five-area contract and optional transform corpus. Use only when the user explicitly requests de-slopping, removal of an AI-looking UI, Slopslap, or removal of statistically common AI UI patterns. Do not auto-apply for general UI improvement, spacing, grid, color, typography, or redesign requests."
---

# Slopslap

Remove UI slop while preserving product meaning, intentional design, accessibility and project rules. Taxonomy matches are candidates, not automatic proof.

## Modes

- **Audit**: inspect and report; do not edit.
- **Reductive**: default repair mode. Prefer delete, flatten, simplify, then replace.
- **Transform**: only when AI-slop removal is explicit and a redesign direction is already approved. Use `$cx-design-director` to establish that direction, then apply this skill's constraints within it.

## Workflow

1. Read project rules, existing `DESIGN.md`, the current diff, affected UI and product content.
2. Define the affected surface and preserve copy, hierarchy, order, interactions and intentional brand elements.
3. Run the candidate scanner against explicit paths:

   ```bash
   node "<skill-root>/scripts/scan-slop-signals.mjs" <target-path> --json
   ```

   Treat `coverage.complete: false`, a non-empty `detectorErrors` array, or
   exit code `2` as incomplete evidence, not a clean scan.

4. Evaluate the areas in `references/inspection-areas.md`: A decorative slop, B layout/containers/media, C spacing, D typography, E color/contrast.
5. For a small surface, evaluate locally in one focused pass. For broad work, order repairs A → B → C → D → E because structural changes can invalidate later findings.
6. For each actionable finding, record the problem, located evidence, prescription, measurable check and area. Scanner hits are not proof.
7. In Audit mode, stop after findings and an optional report. In repair modes, apply only accepted findings and verify the changed surface once with the nearest relevant check.
8. Route broad redesign direction to `$cx-design-director`, rendered judgment to `$cx-visual-qa`, and browser interaction to `$cx-browser-automation`.

### Optional rendered-HTML cross-check

When a self-contained rendered or exported HTML file exists, an explicit
de-slopping task may add this pinned check-only pass. Inspect the file first:
if it loads CSS through `<link rel="stylesheet">` or `@import`, skip this pass
or mark its CSS coverage `NOT_PROVEN` because v0.4.2 JSON does not report that
gap.

```bash
npx -y @gessobuild/anti-slop@0.4.2 check <rendered-html> --json
```

Use its issues as another candidate list, not a verdict. Keep `[advisory]`
issues advisory and judge every other issue against product intent,
accessibility, project rules, and current rendered evidence. A nonzero exit,
malformed JSON, or checker or rule error is incomplete evidence, never zero
findings.

Do not run `fix`, `fix --write`, or copy its baseline CSS. Those operations can
rewrite intentional UI, copy, semantics, and accessibility without the local
judgment this skill requires.

## Optional artifacts and corpus

For broad work or a requested artifact, write `.codex/slopslap/<run>/findings.md` and optionally build a self-contained report:

```bash
node "<skill-root>/scripts/build-findings-report.mjs" <findings-dir> <report/index.html> --target "<label>" [--verifyDir <verify-dir>]
```

Use these deterministic resources:

- Candidate scanner: `scripts/scan-slop-signals.mjs`
- Scanner regression test: `scripts/scan-slop-signals.test.mjs`
- Taxonomy: `assets/data/aiSlopTaxonomyData.js`
- Quantitative lookup: `scripts/fetch-references.mjs`
- Transform directions: `scripts/fetch-answer.mjs`
- Matrix contract: `references/matrix-schema.md`

Project tokens and the existing component system outrank vendored values. Do not copy matrix screenshots, third-party layouts, logos, copy or brand assets into the target project.

Corpus regeneration and reference recapture are maintenance operations, not normal use. Follow `references/maintenance.md` only when the user asks to update the vendored corpus.

## Guardrails

- Preserve domain content, accessibility behavior and intentional brand decisions.
- Do not delete semantic content or imagery merely to reduce a pattern count.
- Do not perform unrelated cleanup or repeat equivalent checks.
- Keep provenance in `references/upstream-attribution.md` and `references/UPSTREAM_LICENSE.txt`.
