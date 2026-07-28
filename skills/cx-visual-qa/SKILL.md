---
name: cx-visual-qa
description: "Verify rendered web, mobile or terminal UI changes with current, sufficient, scope-proportional evidence. Use for screenshot or pixel comparison, reference fidelity, responsive and interaction states, design-system compliance, CJK wrapping, clipping, overflow and final visual PASS, FAIL, or NOT_PROVEN judgments."
---

# Visual QA

Judge only the rendered surface affected by the change. A blocking defect fails that surface.

## Process

1. Enumerate affected routes, tabs, modal/menu states, scroll regions, themes, breakpoints, slides or terminal states.
2. Reuse sufficient current evidence when the relevant source, rendered state, viewport, theme, and criterion have not changed. Otherwise capture after the last relevant edit. Broad changes need full affected-surface coverage; small changes need only the relevant surface.
3. Use available browser tools or `$cx-browser-automation` for web interaction and capture. Preserve text and ANSI evidence for TUI work.
4. Check functional/design-system and visual-fidelity concerns in one focused pass for small changes. Split passes only when the surface is broad or reference-sensitive.
5. Report `PASS`, `FAIL`, or `NOT_PROVEN` with blocking issues or proof gaps first and evidence paths.

Load `references/visual-contract.md` for evidence semantics and `references/review-checklist.md` for concrete defect lenses.

## Helpers

- Image diff and TUI utilities: `scripts/visual-qa.mjs`
- Terminal evidence: `scripts/terminal_visual_qa.mjs`

The helpers run directly with Node.js and have no npm package dependency. If `node` is missing, propose the exact installation command. Preserve capture, dimension, parsing and comparison failures as their real failure type.

## Blocking defects

- `FAIL`: an observed rendered surface contains unreadable or clipped text, broken CJK semantic wrapping in the changed area, overlap, an affected responsive or interaction defect, or a violation of the active design-system contract.
- `NOT_PROVEN`: required coverage is missing or stale, or a browser, tool, session, permission, capture, or access problem prevents observation.
- `PASS`: every required affected surface is observed with sufficient evidence and no blocking defect is found.
