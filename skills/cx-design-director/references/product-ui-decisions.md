# Product UI Decisions

Choose structure from user tasks and information relationships, not from a preferred visual style.

## Page and flow selection

- Dashboard: overview and prioritization; provide paths to detail rather than placing every control on one surface.
- List/table: repeated comparable data; preserve sorting, filtering, selection and empty/loading/error states.
- Detail: one entity with clear primary and secondary actions.
- Form/wizard: use one page when decisions are independent and visible; use steps when order, validation or cognitive load requires it.
- Settings: group by user mental model and make persistence feedback explicit.
- Master-detail or split view: useful when users repeatedly compare a collection with one selected item.
- Feed/timeline: appropriate when recency and sequence are the main organizing principles.

Map the full task flow, including entry, success, empty, loading, partial failure, permission denial, destructive confirmation and recovery.

## Layout and responsive transformation

- Give each region a role: navigation, primary work, secondary context or feedback.
- Use containers only when they express grouping or hierarchy.
- Prefer stable alignment and readable measures over arbitrary card grids.
- At narrow widths, decide what stacks, becomes a drawer/sheet, scrolls, collapses or moves to a separate route.
- Preserve task order and action reachability across breakpoints.

## Accessibility and content

- Make the next action and current state visible.
- Keep labels concrete and consistent; labels must work without placeholders.
- Errors state what happened and how to recover.
- Empty states explain the missing content and the first useful action.
- Preserve keyboard access, focus order, target size, zoom/reflow and non-color feedback.
- Treat permanent, temporary and situational limitations as real constraints, not decorative personas.

Use familiar component primitives unless a different interaction materially improves the task.
