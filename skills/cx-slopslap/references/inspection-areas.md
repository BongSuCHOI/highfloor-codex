# Slopslap Area Inspection and Execution Rules (SSOT)

When broad work is delegated, each inspector or executor reads **only their
area section**. For small work, the current Codex selects the necessary sections
and handles them in one pass. The authoritative source for what counts as slop
and how to escape it is the tell/escape data in
`<skill-root>/assets/data/aiSlopTaxonomyData.js`. The rules below are the
area-specific judgment and execution contract layered on top.

Common principle: **“AI output statistically fails this way, so mechanically
enforce this response.”** Classify by one measurable trigger rather than
qualitative judgment. Derive values as a target-derived unit times a fixed
multiplier, not arbitrary fixed pixels.

---

## Area A · Mechanical removal of representative AI slop (first sweep; execution order 1)

**Character:** Areas B–E measure and derive values. Area A is the first sweep
that **deletes or flattens on sight without measurement or derivation**. Compare
every instance against the checklist and remove the most representative
decorative tells AI adds reflexively: decoration the content never requested.
This is not subjective. A match to a statistical slop pattern—reflexive
repetition, global overuse, or content-independent decoration—must be executed.
Execution means deleting the node or style and cleaning orphaned CSS. **Copy,
information, and content body are immutable; remove decoration only.**

Record “match/no match” for every item A1–A8 in the findings so omissions cannot
remain silent. One intentional brand-identity instance, such as one focal glow
or one identity-defining hero gradient, is not a tell. The tell is reflexive
repetition, global overuse, or content-independent decoration.

- **A1. Overline, eyebrow, and kicker.** Delete an overline when any condition
  below applies; inspect every overline:

  1. The text restates or is a subset of the title immediately below.
  2. It is a topic or kicker label above a one-off section or heading with no
     repeated siblings (`≤1`).
  3. It is a pure number or index with no functional anchor such as contents,
     steps, or pagination links.
  4. An all-caps eyebrow or pill eyebrow satisfies conditions 1–3.

  **Keep only when** it belongs to at least two repeated sibling blocks **and**
  contains a category or sequence value absent from each title. When retained,
  its distance from the title must exceed the title's line-height wrap gap.
  Connect this to Area C `hug` and record the value in findings.
  SSOT: `numbered-overline-fetish`, `all-caps-eyebrow`,
  `pill-eyebrow-badge`.

- **A2. Floating gradient orb or neon blob.** Delete purely decorative,
  content-free orb/blob nodes: absolute placement plus gradient or blurred fill
  with zero information. SSOT: `floating-gradient-orb`,
  `octane-blob-neon`.
- **A3. Mesh/aurora background and global glow.** Remove decorative mesh or
  aurora background layers. Remove glow box shadows repeated across three or
  more elements and flatten the surfaces. One intentional focal instance is
  exempt. SSOT: `mesh-aurora-background`, `everywhere-glow`.
- **A4. Glassmorphism surface.** Replace a surface combining
  `backdrop-filter: blur` with a translucent background by an opaque solid
  surface. SSOT: `glassmorphism-default`.
- **A5. Soft-shadow overuse.** Remove uniform soft box shadows placed on most
  cards or surfaces without a functional basis. Express emphasis through
  figure-ground: luminance, scale, and space. Mechanical trigger: most surfaces
  share the same soft shadow. SSOT: `ubiquitous-soft-shadow`.
- **A6. Gradient text.** Replace gradient text fill
  (`background-clip:text` plus gradient) with a solid color. SSOT:
  `gradient-text`.
- **A7. Emoji icons, navigation, and overuse.** Remove emojis used as icons,
  bullets, or navigation, or replace them with text labels or real icons.
  Remove excessive decorative emojis inside sentences. SSOT:
  `emoji-icon-navigation`, `emoji-overuse`.
- **A8. Decorative dots, sparkles, and meaningless charts.** Remove decorative
  dots unrelated to state, AI-branding sparkles, and charts or graphs that
  contain no data. SSOT: `decorative-status-dots`, `sparkle-ai-branding`,
  `meaningless-decorative-chart`.

**Boundary with E (color):** A removes or flattens the decorative object itself:
orb, mesh, glow, glass, and gradient text. E disciplines the palette of what
remains: hue role, semantics, and contrast math. A commits first, so E sees the
surface after decoration has been removed. Decorative gradients and glow belong
to A; brand accents, state colors, and contrast belong to E.

## Area B · Layout, containers, and images (execution order 2)

The order is the decision tree. A decision above constrains the steps below.

1. **Choose the type first.** Storytelling, USP, or showcase landing pages with
   a conceptual hero use a **fluid viewport division**: hero/scenes may be
   `100vh` with viewport-scaled breathing room. Dense apps, data, and dashboards
   use fixed or contained layouts. **Fluid does not mean expanding content.**
   Preserve content size inside a cell and change alignment only.

   **`100vh` is a measurement, not a declaration.** Measure whether the total
   content height—font, line count, padding, and gaps, or a rendered
   measurement—fits the viewport. If it overflows, it is not a viewport scene:
   reduce internal spacing/scale or remove `100vh`. Natural image size is the
   most frequent overflow cause, so cap it.
   SSOT: `layout-type-misfit`, `undecided-layout-type`.

   - **1b. BOLD gate: does a rough, low-density style produce the identity?**
     Make this judgment **once** at the upstream type-selection stage and pass
     `BOLD=on/off` downstream, especially to C. Downstream areas must not
     reassess it; they only consume the flag. This isolates the decision and
     prevents context load and disagreement.

     Set `BOLD=on` only when both AND conditions are true:

     - **a. At least three repeated rough-style vocabularies:** thick solid
       border (`≥3px`, dark/black); hard box shadow (offset `≥4px`, **zero
       blur**); flat saturated primary fill; extremely large bold typography
       (oversized/900 headline); zero or extreme radius.
     - **b. Content whose style benefits from low density—judge generously
       toward on.** AI often cannot tolerate whitespace and fills it with
       unnecessary density. Do not switch off merely because it looks busy.
       `off` means genuine functional density that cannot be low-density: data
       tables, dashboards, long real-data lists, forms/builders/segments,
       settings panels, and similar interactive or data-dense surfaces.
       Card grids, multiple text blocks, and three-column feature cards count as
       low density; their visible density is usually unnecessary AI filling,
       not a content requirement. If a substantial part of the page is hero,
       statement, or whitespace-led, treat it as low density. Resolve boundary
       cases to on.

     Condition a remains mandatory. Without rough-style vocabulary, use
     `BOLD=off` regardless of b; do not enlarge a screen that lacks the style.
     When a is present, judge b generously toward on. The prior STACKBOX void
     failure came from doubling spacing indiscriminately, not from b. Area C
     1-neo and the B scaling rules already constrain this: even with on, grow
     elements and surfaces first while preserving adjacent-gap and dead-void
     guards.

     - **`BOLD=on`: scale decisively.** Increase UI, button, and icon size;
       border and hard shadow; internal surface padding; and spacing/padding.
       Low density makes large space part of the style rather than a void.
       Adjacent elements require `gap ≥ hard-shadow offset` so shadows do not
       collide. Values remain derived rather than eyeballed, and focal
       isolation remains intact. Area C consumes the flag for spacing scale.
     - **`BOLD=off`:** use all ordinary area rules without enlargement.
       SSOT: `layout-type-misfit`.

2. **Module.** Column boundaries come only from harmonic divisions of a shared
   module: halves, thirds, quarters. They need not form one line across the
   entire page; for example, top `1:1` and bottom `0.5:0.5:1` are valid. Random
   misalignment is the defect. Replace content-fit random rows with equal rows
   such as `repeat(N, 1fr)`. SSOT: `undisciplined-grid`.

   - **2a. Derive widths; prohibit fixed/content-fit drift.** Containers,
     columns, and cells must derive from a shared module such as harmonic
     division or a max-width token. Independent fixed pixels or content-fit
     widths that differ by section break balance. Derive width from one scale,
     just as spacing is derived. Mechanical trigger: sibling or adjacent
     content containers have different max widths or column widths, such as
     mixed `900`, `1120`, and `auto`. Unify them under one page-measure token or
     harmonic multiples. Do not let content length determine cell width; use
     grid tracks such as `1fr` or harmonic ratios.

   - **2b. Match content measure to information density; prohibit an overly
     narrow measure.** A common AI pattern leaves generous side margins while
     compressing content width below what its information density requires.
     Multi-column cards, feature grids, and tables become cramped while margins
     remain wide. **Whitespace frames content; it must not crush it.**
     Mechanical trigger: container max width is narrower than the contained
     density requires—for example, a three- or four-column card/feature grid
     with measure `≤900`, or content occupies so little of the viewport that
     side margins exceed it. Widen the measure to fit density. A prose-only
     column with a readable `45–75em` measure is exempt; narrow is correct.
     Judge by density—column and element count—not screen size alone.
     SSOT: `undisciplined-grid` for underived width and
     `layout-type-misfit` for density/width mismatch.

   - **2c. Align series UI mapped from arrays.** For repeated series identified
     during content constantization—lists, cards, steps, pricing tiers, feature
     items—anchor each bullet, number, or icon to the first text-line baseline.
     **Do not vertically center with `top:50%` or `align-items:center`.** On
     multi-line items this misaligns markers and makes the series jump. Place
     marker `top` at approximately the center of the first line (`0.5lh`) or use
     flex `align-items:baseline`/`flex-start`. Keep marker size, indentation, and
     number width aligned; pad digits and right-align numbers. Mechanical
     trigger: a series list/card marker uses `top:50%` or centered alignment
     while item text has variable line count. SSOT: `undisciplined-grid`.

3. **Minimum containers.** The following is a mechanical comparison list, not a
   judgment. Execute every match:

   - **3a. Box in box always flattens.** When a container with any surface
     property—border, background fill, box shadow, or radius—directly wraps a
     child with any surface property, the surface is duplicated. Remove the
     inner surface regardless of claimed role. Convert children into rows with
     top lines or dividers plus spacing. Keep at most one surface layer per
     group. This replaces the strict “ghost wrapper” definition that let nested
     surfaces pass. Example: when a panel with background/border contains
     option boxes with background/border, remove option-box surfaces and use
     bordered rows.
   - **3b. Delete ghost wrappers.** Unwrap a single-child wrapper that contributes
     no grid/flex, spacing, background, border, or semantics.
   - **3c. Never use a colored left border.** It is a representative AI-slop
     pattern. Remove it even if it seems useful, and create emphasis through
     figure-ground: luminance, scale, and space.
   - **3d. Unify surface color.** Terminals and code blocks use one color for the
     background and horizontal scrollbar, including `scrollbar-color` and
     WebKit styling.
   - **3e. Do not overuse containers; surfaces only when necessary.** Use
     background, border, radius, or shadow only to distinguish a real
     information group. Do not wrap every simple list item, row, or short
     sentence in a box; bullet/text rows, hairline separators, and spacing are
     sufficient. In particular, do not turn each series item into a card unless
     it is an independently dense information unit containing title, body,
     metadata, and action. Otherwise strip the surface and use separator rows.
     Mechanical trigger: every item in a series array has a surface while its
     content is only a short sentence or one to two fields. Rule 3a removes
     surfaces inside surfaces; 3e removes surfaces that were never needed.

   SSOT: `meaningless-container-nesting`, `colored-left-border-cards`. Record
   “match/no match” for every item in findings.

4. **Image guard.** Never render above natural dimensions: zero upscaling. When
   one image does not fit a repeated series format, do not stretch it or mask the
   mismatch with whitespace; reductively remove the odd image.

## Area C · Spacing (execution order 3)

- **AI statistic:** almost always overcrowded with no hierarchical grouping;
  overline, title, and body gaps become identical blobs.
- **1. Derive the base unit from target character, not fixed pixels.**
  Editorial, magazine, storytelling, and USP landing pages use a large base
  (`24–32`). General information or marketing pages use medium-large
  (`20–24`). Only dense apps, dashboards, and data use a small base (`8–14`).
  Default toward generosity.
- **1-neo. Consume the BOLD flag. Do not reassess it here.** Area B 1b has
  already decided. With `BOLD=on`, scale spacing and padding decisively upward:
  choose a generous derived base and raise the ladder. In a confirmed
  low-density rough style, large space is the style rather than a void. With
  `BOLD=off`, ignore this item and use ordinary base derivation.

  The density judgment belongs only to the upstream AND gate because enlarging
  spacing alone on a dense screen creates dead voids, as in the STACKBOX
  failure. Area C only consumes the flag, avoiding duplicated and inconsistent
  judgments.

  - **Prevent hard-shadow collisions:** adjacent hard-shadow elements such as
    side-by-side buttons require `gap ≥ shadow offset + allowance`. Increase the
    gap when the shadow grows.
  - Preserve focal isolation and tight grouping. Continue to derive the base
    and ladder; **do not double the base merely because a style is
    neobrutalist.** Content determines density. Ignore mood alone.

- **2. Fix the multipliers.** Every space equals `base × fixed multiplier`:
  - `hug` (overline → title) = `0.25 × base`, but floor it above the title's
    line-height wrap gap;
  - `within` (title → body) = `1×`;
  - `action` (body → CTA) = `2×`;
  - `component` (block ↔ block) = `4×`;
  - `section` (section ↔ section) = `8×`.
- **3. Be decisive.** Choose a generous base because AI overcrowding is the
  default assumption.
- **4. Isolate the focal group: Gestalt rule one.** Whitespace is a frame around
  a coherent focal group, not a wedge that breaks it apart. Keep a hero's
  eyebrow, headline, description, and CTA as a tight `hug`/`within` unit, then
  isolate it with generous outer margin. Do not uniformly expand gaps between
  focal elements until the group disperses. Do not create dead voids: huge
  purposeless gaps below a CTA or between sections are defects, not isolation.
  Section spacing may be generous without becoming vacuum. Check whether the
  composition looks complete. Expand gutters and row gaps in text-heavy areas.
- SSOT: `unscaled-spacing-ladder`, `unpartitioned-space`. Never eyeball spacing;
  derive it from the declared ladder.

## Area D · Typography (execution order 4)

- **AI statistic:** one headline word becomes serif italic, or font families are
  mixed randomly without role.
- **a. Always remove italic.** Delete every `font-style: italic` with no
  exceptions.
- **b. Judge fonts through a family-to-role map.** The signal is not the number
  of families but **role bijection**: if every family owns one role and every
  role uses one family—serif for all display, mono for all labels, sans for all
  body—the system is orderly and should remain, even with three families.
  Unify only when one family jumps randomly between roles or one role mixes
  multiple families. Create hierarchy through size, weight, and spacing rather
  than font replacement.
- **Do not overshoot.** “Always use one family” and “unify whenever there are
  three or more” both destroy intentional role-fixed systems.
- SSOT: `italic-serif-accent`, `monospace-body-aesthetic`.

## Area E · Color (execution order 5)

- **AI statistic:** saturated color is scattered across sibling and qualitative
  content while accessibility contrast is ignored.
- **a. Define semantic roles first.** Recognize only brand, CTA, and real states
  such as error, warning, and success as color roles.
- **b. Demote every color outside those roles to a neutral tone scale.**
- **c. Reallocate for accessibility contrast.** Adjust luminance so approved
  role colors pass WCAG against the background, including `4.5:1` for body text.
- Sweep orphaned color variables and classes during execution.
  SSOT: `decorative-semantic-color`, `rainbow-status-list`,
  `iridescent-palette`.

---

## Findings schema (all areas)

Each inspector records every item in `findings-<area>.md`:

```yaml
- id: <SSOT id or area slug>
  problem: <one line>
  evidence: <static measurement: file:line or calculated value such as contrast x:1, divider x%, font role map>
  prescription: <mechanical change: what to change to which value, including derived base and multiplier>
  check: <predicate measured from source as true/false; make satisfaction decidable by grep or value comparison, for example: "scrollbar-color exists in .code pre and uses --code-bg/border", "hero max-width references var(--measure)", "font-style:italic has zero matches". Do not write completed/incomplete state; recompute the check from source every time.>
  execution_order: A|B|C|D|E
```

**Checklist equals evaluation function; never assert state.** A finding must not
declare “complete” or “not applicable.” It carries a `check` predicate, and the
executor or re-inspector measures that predicate from source every time:
true means already satisfied and skipped; false means execute.

Do not trust text saying “complete.” Reusing old findings or changing target
state makes such records stale; the missed terminal scrollbar color was this
failure. The executor applies prescriptions only for false checks. The
re-inspector measures the same check again in source or rendering and records
true/false rather than a subjective verdict. Broad independent areas may be
delegated to Codex workers. The current Codex evaluates and executes a small
scope directly. In either case, never pass based only on an implementer's
completion statement; recompute the `check` from source.
