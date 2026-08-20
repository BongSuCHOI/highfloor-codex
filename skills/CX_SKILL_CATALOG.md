# CX Skill Catalog

- Snapshot date: 2026-08-19
- Canonical catalog: `skills/CX_SKILL_CATALOG.md`
- Runtime contracts: `skills/cx-*/SKILL.md`
- Governance: `skills/CX_SKILLS.md`
- Inventory and history: `skills/CX_MIGRATION_MANIFEST.md`

## 1. Document responsibility

This document is the routing catalog for the current `cx-*` skills. It
summarizes every skill through the same five fields:

- **Owns:** the unique result for which the skill is responsible
- **Trigger:** the state or request that warrants use
- **Non-trigger:** the state in which it should not be used
- **Method:** the core principle that determines behavior
- **Routes:** adjacent owners and paths for reusing evidence

This summary is not the runtime contract. Follow the linked `SKILL.md` for
detailed triggers, workflow, scripts, and fallbacks.

## 2. Quick routing

| Current need | Primary owner |
|---|---|
| Analyze a public or local video from timestamped visual and spoken evidence | `cx-analyze-video` |
| Turn an ambiguous product, feature, or improvement request into an approved contract | `cx-interview` |
| Reframe a repeatedly failed planning, product, or architecture strategy | `cx-unstuck` |
| Interact with and capture a real browser | `cx-browser-automation` |
| Find a prior coding-agent task or transcript | `cx-coding-agent-sessions` |
| Isolate the cause of a runtime failure | `cx-debugging` |
| Direct a broad UI, redesign, design-system, or product-flow change | `cx-design-director` |
| Read public content blocked through ordinary access | `cx-insane-search` |
| Handle a non-obvious Python, TypeScript, Go, or Rust boundary | `cx-programming` |
| Compare current work with an approved contract for semantic scope | `cx-scope-check` |
| Detect and remove explicitly requested AI slop | `cx-slopslap` |
| Perform explicitly requested deep, source-backed research | `cx-ultraresearch` |
| Map and explore an unfamiliar codebase or agent harness | `cx-understand-codebase` |
| Issue a formal AC, QA, release, or handoff verdict | `cx-acceptance-qa` |
| Issue the final visual verdict for rendered UI | `cx-visual-qa` |

## 3. Common composition

### Task Contract / Plan / Codex Goal

| Concept | Question | Role |
|---|---|---|
| Task Contract | What counts as success? | goal, boundary, outcome, verification |
| Plan | How should the work be executed? | stages, files, dependencies, order |
| Codex Goal | How long should the objective remain active? | persistent execution and long-running objective |

Typical flow:

```text
materially ambiguous request
→ cx-interview
→ user-approved Task Contract
→ Plan when complexity warrants it
→ implementation
→ risk-proportional basic verification
→ cx-acceptance-qa only when a formal verdict is needed
```

`cx-scope-check` and `cx-unstuck` are not fixed stages. They enter only when
their drift or genuine-deadlock triggers occur. Create a Codex Goal only when
the user explicitly selects long-running objective tracking. Persistent work
keeps one terminal artifact and its required gates visible; the Goal preserves
the objective but does not redefine success or justify adjacent expansion.

## 4. Skill cards

### `cx-acceptance-qa`

Runtime contract: [`SKILL.md`](cx-acceptance-qa/SKILL.md)

- **Owns:** a formal `PASS`, `FAIL`, or `NOT_PROVEN` verdict connecting explicit
  acceptance criteria to current evidence.
- **Trigger:** formal proof is needed for QA, release, handoff, Task Contract
  verification, or a behavior-bearing artifact.
- **Non-trigger:** a small change already proven by basic verification, cause
  diagnosis, or the final verdict for rendered UI alone.
- **Method:** treat each AC as an observable promise and prove it with the
  smallest sufficient mechanical, observable, and semantic evidence matched
  to the relevant failure topology.
- **Routes:** UI verdict → `cx-visual-qa`; interaction →
  `cx-browser-automation`; failure cause → `cx-debugging`; specification gap →
  `cx-interview`.

### `cx-analyze-video`

Runtime contract: [`SKILL.md`](cx-analyze-video/SKILL.md)

- **Owns:** a timestamped answer that separates visual, spoken, combined, and
  inferred evidence from a public URL or local video file.
- **Trigger:** a YouTube or other public video, local media file, screen
  recording, named moment, or comparison between what is shown and said needs
  analysis.
- **Non-trigger:** ordinary webpage interaction, login-gated media, or the final
  rendered-product UI verdict.
- **Method:** align independent frame and transcript lanes, begin with the
  smallest useful coverage, and treat external transcription as an explicit
  per-video privacy and cost boundary.
- **Routes:** page/session interaction → `cx-browser-automation`; final product
  UI verdict → `cx-visual-qa`; runtime failure cause → `cx-debugging`.

### `cx-browser-automation`

Runtime contract: [`SKILL.md`](cx-browser-automation/SKILL.md)

- **Owns:** real browser navigation, interaction, accessibility snapshots,
  screenshots, traces, and state reproduction.
- **Trigger:** a real page, form, browser state, logged-in session, or capture
  is required.
- **Non-trigger:** final visual-quality judgment, cookie extraction or
  injection, or bypassing CAPTCHA, paywalls, or permissions.
- **Method:** choose the browser surface that matches required session state and
  prioritize user-driven login and evidence capture.
- **Routes:** final judgment of captured rendered evidence → `cx-visual-qa`.

### `cx-coding-agent-sessions`

Runtime contract: [`SKILL.md`](cx-coding-agent-sessions/SKILL.md)

- **Owns:** discovery of Codex, Claude, OpenCode, Senpi, and other coding-agent
  sessions and transcripts.
- **Trigger:** a prior task, exact prompt, session ID, child task, or historical
  work evidence must be recovered.
- **Non-trigger:** semantic interpretation of the current diff, ordinary
  repository search, or a low-stakes conversation where memory is sufficient.
- **Method:** use the bundled finder first, hide host-internal traces from
  ordinary results, expose recorded model and reasoning-effort history for
  evaluation, and treat the raw transcript path as the source of truth for
  exact claims.
- **Routes:** recovered contracts can be consumed by `cx-scope-check` or
  `cx-interview`; this skill does not issue a drift verdict.

### `cx-debugging`

Runtime contract: [`SKILL.md`](cx-debugging/SKILL.md)

- **Owns:** cause isolation for crashes, hangs, wrong behavior, silent failures,
  debugger sessions, and binary behavior.
- **Trigger:** a runtime symptom exists and evidence is needed to distinguish
  plausible causes.
- **Non-trigger:** routine review, requirement clarification, a planned
  refactor, or an acceptance verdict.
- **Method:** use the smallest reproduction and discriminating hypotheses to
  test whether the cause predicts the failure; if the exact symptom survives a
  fix, reopen the cause or scope before stacking another change.
- **Routes:** browser-only reproduction → `cx-browser-automation`; formal
  verdict → `cx-acceptance-qa`.

### `cx-design-director`

Runtime contract: [`SKILL.md`](cx-design-director/SKILL.md)

- **Owns:** broad product UI direction, redesign, design-system extraction, and
  end-to-end UX structure.
- **Trigger:** the visual language, layout grammar, component pattern, or
  product flow changes materially.
- **Non-trigger:** a small style, copy, or single-component edit, or a request
  limited to AI-slop removal.
- **Method:** prefer the existing first-party system and translate references
  into tokens, geometry, states, responsiveness, and accessibility contracts;
  restoration preserves the approved composition, behavior, and tuned
  parameters unless that boundary is reopened.
- **Routes:** interaction → `cx-browser-automation`; rendered verdict →
  `cx-visual-qa`; explicit AI-slop constraint → `cx-slopslap`.

### `cx-insane-search`

Runtime contract: [`SKILL.md`](cx-insane-search/SKILL.md)

- **Owns:** alternate access paths for public content when ordinary web access
  fails.
- **Trigger:** `402`, `403`, WAF, empty or JS-only HTML, broken markup, or a
  degraded URL on a supported platform.
- **Non-trigger:** ordinary search, login, paywall, CAPTCHA, private network,
  deleted content, or permission-gated content.
- **Method:** use built-in web access first, then use the pinned, DNS-guarded
  engine. Keep persistent learning off unless explicitly requested and preserve
  its retrieval-only evidence envelope.
- **Routes:** use `cx-browser-automation` when real rendered interaction is
  required; pass `--evidence-json` once when `cx-ultraresearch` needs
  blocked-source content and access metadata.

### `cx-interview`

Runtime contract: [`SKILL.md`](cx-interview/SKILL.md)

- **Owns:** a user-approved Task Contract for a materially ambiguous idea,
  feature, workflow, or brownfield improvement.
- **Trigger:** goal, actor, constraint, non-goal, outcome, AC, or product
  decision could materially change the result.
- **Non-trigger:** an already specified narrow edit, pure diagnosis, or a
  decision already settled by project rules.
- **Method:** expose hidden assumptions through Socratic questions; for
  materially multi-surface requests, confirm top-level coverage before
  converging through restatement, explicit review of reductions, and approval;
  persistent contracts may name the terminal artifact and required gates.
- **Routes:** UI/product-flow discovery → `cx-design-director`; external
  comparison → `cx-ultraresearch`; implementation drift, deadlock, or formal
  proof → the corresponding owner.

### `cx-programming`

Runtime contract: [`SKILL.md`](cx-programming/SKILL.md)

- **Owns:** Python, TypeScript, Go, and Rust boundaries involving typing,
  validation, concurrency, resources, errors, FFI, and toolchains.
- **Trigger:** a non-obvious language-specific failure mode affects an
  implementation decision.
- **Non-trigger:** routine syntax, generic advice, or a case already decided by
  project convention.
- **Method:** prefer project conventions and dependencies, then load only the
  one language card needed for the current boundary.
- **Routes:** runtime cause → `cx-debugging`; completion proof → ordinary
  risk-matched verification or `cx-acceptance-qa`.

### `cx-scope-check`

Runtime contract: [`SKILL.md`](cx-scope-check/SKILL.md)

- **Owns:** semantic drift classification between an approved Task Contract and
  current changes.
- **Trigger:** an explicit drift check, resume, compaction, handoff, major phase,
  or unexpected dependency, API, schema, or surface change.
- **Non-trigger:** every turn, file-count growth alone, or legitimate
  implementation detail that preserves the contract.
- **Method:** use specification-as-contract as the baseline and compare outcome,
  constraint, and authority meaning rather than lexical distance.
- **Routes:** amendment → `cx-interview`; missing history →
  `cx-coding-agent-sessions`; proof gap → `cx-acceptance-qa`; environment
  mismatch → `cx-debugging`.

### `cx-slopslap`

Runtime contract: [`SKILL.md`](cx-slopslap/SKILL.md)

- **Owns:** an explicitly requested statistical AI-slop audit and removal.
- **Trigger:** requests for de-slopping, removing an “AI look,” Slopslap, or
  common AI UI patterns.
- **Non-trigger:** generic UI improvement, spacing, grid, color, typography, or
  broad redesign alone.
- **Method:** treat taxonomy and scanner hits only as candidates, preserve
  product meaning, and prefer reductive repair.
- **Routes:** redesign direction → `cx-design-director`; interaction →
  `cx-browser-automation`; rendered verdict → `cx-visual-qa`.

### `cx-ultraresearch`

Runtime contract: [`SKILL.md`](cx-ultraresearch/SKILL.md)

- **Owns:** explicit deep, source-backed, citation-heavy, multi-source
  investigation.
- **Trigger:** the user explicitly requests research, deep research,
  evidence-based investigation, or careful comparison.
- **Non-trigger:** an ordinary current-fact lookup, a simple web question, or
  reading one accessible page.
- **Method:** define only the necessary evidence axes, keep claim-relative
  source and material-claim maps, distinguish source lineage from domain, and
  classify claims as `supported`, `unresolved`, or `refuted`; distinguish
  direct measurement, first-principles bounds, transferred estimates, and
  scenarios for material quantitative claims.
- **Routes:** blocked public URL → `cx-insane-search`; real page interaction or
  rendered state → `cx-browser-automation`; apply the evidence contract in
  context for high-stakes or citation-heavy work, but materialize durable
  artifacts only when requested.

### `cx-understand-codebase`

Runtime contract: [`SKILL.md`](cx-understand-codebase/SKILL.md)

- **Owns:** a reusable evidence-backed architecture knowledge graph, learning
  path, and optional token-gated local interactive dashboard.
- **Trigger:** repository onboarding, handoff, unfamiliar codebase study, agent
  harness architecture tracing, graph refresh, change impact, or a graph-backed
  explanation is requested.
- **Non-trigger:** a narrow source lookup, runtime root-cause diagnosis, or a
  formal acceptance verdict.
- **Method:** establish deterministic file/import structure before semantic
  synthesis, preserve partial work without advancing freshness, and verify
  decisive graph claims against current source.
- **Routes:** exact prior-task recovery → `cx-coding-agent-sessions`; runtime
  cause → `cx-debugging`; formal completion proof → `cx-acceptance-qa`.

### `cx-unstuck`

Runtime contract: [`SKILL.md`](cx-unstuck/SKILL.md)

- **Owns:** bounded alternatives for a planning, product, architecture, or
  implementation-strategy deadlock.
- **Trigger:** repeated failure of the same approach, conflicting constraints,
  structural stagnation, or a request for a different perspective.
- **Non-trigger:** a runtime failure whose cause is not yet isolated or broad
  ideation without a genuine deadlock.
- **Method:** use lateral thinking to change the frame reproducing the deadlock,
  then reconverge through small discriminating experiments.
- **Routes:** runtime cause → `cx-debugging`; missing current fact →
  `cx-ultraresearch`; contract change → `cx-interview`; expanded surface →
  `cx-scope-check`.

### `cx-visual-qa`

Runtime contract: [`SKILL.md`](cx-visual-qa/SKILL.md)

- **Owns:** the final visual `PASS`, `FAIL`, or `NOT_PROVEN` for affected
  rendered web, mobile, slide, terminal, or TUI surfaces.
- **Trigger:** screenshot or pixel comparison, responsive or interaction state,
  reference fidelity, design-system conformance, CJK wrapping, clipping, or
  overflow judgment.
- **Non-trigger:** source-only review, browser manipulation itself, or inferring
  a product failure without evidence.
- **Method:** reuse current sufficient evidence or recapture only affected
  surfaces, and separate product defects from proof failures.
- **Routes:** browser state and capture → `cx-browser-automation`; cause
  isolation → `cx-debugging`.

## 5. Catalog maintenance

- Add only the same five fields for a new skill.
- Do not copy workflows, simulations, commands, or schemas into the catalog.
- Move an oversized summary into its `SKILL.md` or a reference.
- Update the routing table and card together when renaming, merging, or
  deprecating.
- Keep the live inventory aligned with `CX_MIGRATION_MANIFEST.md`.
