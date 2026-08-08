# Visual Review Checklist

Inspect only applicable lenses:

- Hierarchy: primary task/action, scan order and density.
- Layout: alignment, spacing rhythm, named scroll ownership, container logic and stable responsive transformation.
- Components: anatomy, variants, hover/focus/disabled/loading/empty/error states.
- Type: role consistency, measure, weight, truncation and semantic CJK/Latin wrapping.
- Color: contrast, state distinction, non-color feedback and theme behavior.
- Media: crop, aspect ratio, loading/fallback and provenance-sensitive use.
- Motion: purpose, repeated input, interruption, reversal or cancellation,
  reduced-motion behavior and layout stability.
- Accessibility: focus visibility/order, zoom/reflow, target size and readable labels.
- Defects: clipping, overlap, overflow, broken stacking, stale data and missing state coverage.
- Applicable stress: empty, short, long or unbroken content; component-local
  narrow and wide containers independent of viewport; relevant direction or
  writing mode; focus transitions; and scroll top, middle or end for sticky and
  overflow behavior.

Report located evidence and impact rather than a subjective numeric score.
Do not expand a small change into this full matrix; exercise only conditions
that can change the affected contract or expose the claimed behavior.
