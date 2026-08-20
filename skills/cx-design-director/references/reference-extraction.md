# Reference Extraction

Convert a screenshot, live URL, generated concept or inspiration set into first-party design decisions.

## Extract

- Geometry: grid, regions, alignment, density, whitespace and responsive transformations.
- Type: roles, scale, measure, weight contrast and mixed-script behavior.
- Color and depth: semantic surfaces, contrast pairs, borders, shadows and overlays.
- Components: anatomy, variants, interaction states and content constraints.
- Motion: trigger, purpose, duration, easing and reduced-motion equivalent.
- Assets: subject, crop, hierarchy and role; record provenance.

## Evidence lanes

Keep four statement types distinct:

- **Observed reference fact:** directly present in the inspected DOM, CSS,
  rendered state or supplied image. Record the relevant surface, state,
  breakpoint or theme.
- **Inferred reference behavior:** plausible but not directly observed. State
  the evidence and the inference separately.
- **New first-party decision:** a project-owned semantic token, component rule
  or responsive choice created while translating the reference. Do not present
  it as extracted source behavior.
- **Unresolved gap:** a relevant state, breakpoint, theme, interaction, motion
  rule, asset source or token chain that was not inspected or cannot yet be
  supported.

For machine-extracted CSS, preserve the raw declaration, resolved value and
`var()` chain together with the selector, stylesheet and theme or media scope
when available. Keep conflicting scoped declarations separate. Leave an
unresolved chain as a gap instead of flattening it into a canonical value.

## Do not copy

Do not reproduce third-party logos, proprietary illustrations, brand copy, hidden source code or a design corpus. Translate useful relationships into project-owned tokens and components. Do not invent an observed value or alias; a new semantic alias is allowed only as an explicit first-party decision mapped to supported source values.

## Selection

- Prefer a small set with explicit roles: one structural reference and, only when needed, one type, motion or interaction reference.
- Identify contradictions before implementation.
- When working from a live URL, capture only the pages, breakpoints and states relevant to the requested surface.
- Distinguish observed facts from inferred behavior.
- When a direction or moodboard must represent the product's actual work,
  content, or media, inventory the relevant first-party sources before creating
  stand-ins. Generated concepts may explore treatment; they do not establish
  which source material is representative.

Before a screenshot or generated concept directs implementation, resolve the
first-party semantic order, region responsibilities, scroll ownership,
constraints and responsive transformation. A reference may propose those
decisions but cannot silently override an active project contract. A generated
image demonstrates a visual possibility; it does not prove usability,
accessibility, brand fit or implementation feasibility.

The extracted contract should be detailed enough to implement without
repeatedly reopening every reference. Readiness means the relevant evidence is
sufficient and material gaps are visible; it does not require pretending the
entire source system was observed.
