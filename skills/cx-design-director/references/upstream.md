# Source and dependency provenance

The current design references in this skill are locally authored. Copied third-party design trees used during earlier experimentation were removed in the 2026-07-22 restructure.

Optional external invocation:

- Tool: `ibelick/ui-skills@0.2.4`
- Relationship: `runtime invocation`
- Source content bundled: no
- Upstream license: MIT

This record does not claim that the local design references are derived from UI Skills. It records the optional external dependency boundary only.

Research comparison:

- Project: [`changeroa/StyleGallery`](https://github.com/changeroa/StyleGallery)
- Inspected commit: `e67b440147970c5d4f5b83f922d2593e12d09e74`
- Relationship: `research reference`; no source, pattern corpus, CLI or MCP is bundled
- License: `NOT_PROVEN`; the inspected root had no `LICENSE` file and its
  `package.json` declared no project license

Highfloor independently words its layout-responsibility, motion-continuity and
visual-evidence refinements. The comparison does not make StyleGallery a
runtime dependency or a source of visual defaults.

Selected method source:

- Project: [`fivetaku/insane-design`](https://github.com/fivetaku/insane-design)
- Inspected commit: `a5eb1d976d29309092170ff7ba475a487df0b683`
- Relationship: `independently worded`
- License: MIT; see `LICENSE.insane-design.txt`

Highfloor independently adapted only the evidence-separation ideas relevant to
reference extraction: source provenance for extracted tokens, raw and resolved
CSS-variable chains, scoped declarations, and explicit known gaps. No parser,
apply or verification runtime, report corpus, templates, screenshots, brand
data, generated examples, command surface or upstream wording is bundled.
