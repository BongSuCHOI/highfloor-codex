# Art Direction

Use this branch to discover and select a visual direction, not to add a second
design system or a mandatory redesign ceremony.

## Short-circuit first

Skip exploration when the active first-party contract, an approved reference or
a restoration target already answers the visual question. Use one direction
when uncertainty is narrow. Produce two or three alternatives only when a
material choice remains.

## Minimal loop

1. Frame the target: product outcome, audience, real content, current brand
   assets, implementation constraints, desired character and explicitly
   unwanted impressions.
2. Select a small reference set with declared roles. Use
   `reference-extraction.md` to turn it into observations; do not accumulate a
   style corpus or treat popularity as product fit.
3. Create genuinely different direction cards. Each card states its visual
   thesis, typography, composition and density, color roles, image or material
   treatment, motion character, signature element and primary trade-off.
4. When visual comparison is necessary, render one representative surface per
   direction with the same content, state and viewport. Generated concepts are
   exploration artifacts, not implementation or accessibility evidence.
5. Check feasibility before selection: semantic order, layout and scroll
   responsibility, component reuse, responsive behavior, content resilience,
   asset provenance, motion fallback and accessibility constraints.
6. Converge at the meaningful boundary. Ask the user to select when the choice
   changes visual identity; when selection authority was delegated, choose from
   the product contract and state the decisive trade-off.
7. Materialize only the selected direction through
   `design-system-contract.md`. Record rejected alternatives only when their
   rejection prevents a likely future contradiction.
8. Implement the smallest representative vertical slice, then route current
   rendered fidelity to `cx-visual-qa`.

## Direction quality

Judge a direction from evidence and fit rather than a generic beauty score:

- product and brand fit;
- hierarchy, legibility and task clarity;
- distinctiveness without decorative inconsistency;
- behavior under real, sparse and dense content;
- responsive and implementation feasibility;
- accessible states and reduced-motion behavior;
- reference and asset provenance.

Do not make alternatives that differ only in color, radius or adjectives. Do
not let an image concept silently replace content structure, interaction logic
or the active first-party contract. Stop exploring once one feasible direction
clearly satisfies the target and further variants would not change the choice.
