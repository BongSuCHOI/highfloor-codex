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

## Layout responsibility

- Name the main spatial problem before choosing a layout technique. Keep brand,
  typography, color and decoration from becoming accidental layout constraints.
- Separate viewport-owned structure from component-local adaptation. Use
  viewport breakpoints when the page responsibility changes; prefer intrinsic
  sizing or container queries when only a component's available space changes.
- Name the scroll owner for each axis and the region, if any, allowed to stay
  fixed or sticky. Add nested scrolling only when the task requires independent
  navigation of both regions.
- Preserve semantic source, reading and focus order when regions rearrange. Do
  not use visual ordering to conceal an incoherent document structure.
- Distinguish task-critical regions from supporting or replaceable regions so a
  responsive transformation never removes the path to the primary outcome.
- Keep sizing, overflow, sticky anchors and change points explicit enough that
  an implementer can explain which constraint owns each behavior.

For a broad or layout-sensitive change, declare only the stress inputs that can
materially affect the contract: empty, short, long or unbroken content; narrow
and wide component containers; relevant direction or writing mode; and scroll
top, middle or end. Rendered verdict ownership remains with `cx-visual-qa`.

## Accessibility and content

- Make the next action and current state visible.
- Keep labels concrete and consistent; labels must work without placeholders.
- Errors state what happened and how to recover.
- Empty states explain the missing content and the first useful action.
- Preserve keyboard access, focus order, target size, zoom/reflow and non-color feedback.
- Treat permanent, temporary and situational limitations as real constraints, not decorative personas.

Use familiar component primitives unless a different interaction materially improves the task.
