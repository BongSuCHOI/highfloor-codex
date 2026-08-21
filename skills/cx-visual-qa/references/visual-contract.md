# Visual Evidence Contract

- Currency: evidence must represent the current relevant source and rendered state. Reuse it when source, state, viewport, theme, and criterion are unchanged; otherwise recapture after the final relevant edit.
- Recapture bound: do not repeat an equivalent capture round on an unchanged
  surface more than once after fixes. A new relevant edit resets currency and
  requires fresh evidence; otherwise report `NOT_PROVEN` rather than
  re-capturing without cause.
- Coverage: include every changed route/state/breakpoint required to exercise the request, but do not expand into unrelated screens.
- Fidelity: compare against the active first-party design contract and any explicit reference.
- Reproducibility: record viewport, theme, state and artifact path when they affect the result.
- Claim boundary: a screenshot or image diff can establish a rendered fact. It
  does not by itself prove task success, usability, accessibility or brand fit;
  use evidence that directly addresses those claims.
- Verdict:
  - `PASS` only when every required affected surface is observed and no blocking defect remains.
  - `FAIL` only when the observed rendered surface demonstrates a blocking product defect.
  - `NOT_PROVEN` when missing, stale, inaccessible, or failed evidence collection prevents a verdict.

Pixel similarity is supporting evidence, not the sole verdict. Explain expected dynamic differences and investigate material unexpected differences.
