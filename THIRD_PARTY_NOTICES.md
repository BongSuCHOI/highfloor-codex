# Third-Party Notices

This notice identifies redistributed, adapted, derivative, invoked, and
research-reference material in this repository. Component-level provenance
files under `skills/cx-*/references/` are authoritative for individual skills.

This collection is mixed-license. The root license applies only to original
Highfloor content not otherwise identified below. It does not relicense any
third-party or derivative component.

## Redistribution matrix

| Skills | Upstream | Relationship | License | License copy |
|---|---|---|---|---|
| `cx-acceptance-qa`, `cx-interview`, `cx-scope-check`, `cx-unstuck` | `Q00/ouroboros` at `2dec0dbd01bb5b2243ea138af9d91f3583b92c5d` | independently worded adaptations with preserved method provenance | MIT | `LICENSES/MIT-Q00-ouroboros.txt` |
| `cx-browser-automation` | `microsoft/playwright-cli` | modified derivative | Apache-2.0 | `LICENSES/Apache-2.0-microsoft-playwright-cli.txt` |
| `cx-coding-agent-sessions`, `cx-debugging`, `cx-programming`, `cx-ultraresearch`, `cx-visual-qa` | `code-yeongyu/oh-my-openagent`, source archive version `4.14.0`, exact commit `NOT_PROVEN` | modified derivatives | Sustainable Use License 1.0 | `LICENSES/SUL-1.0-oh-my-openagent.txt` |
| `cx-insane-search` | `fivetaku/insane-search`, exact commit `NOT_PROVEN` | modified derivative | MIT | `LICENSES/MIT-fivetaku-insane-search.txt` |
| `cx-insane-search`, `cx-ultraresearch` | `fivetaku/insane-research` at `68f7e59168a9c9b0a586bd4122cb7a229e119d9c` | independently worded adaptations of selected access-evidence and research-method concepts | MIT | `LICENSES/MIT-fivetaku-insane-research.txt` |
| `cx-slopslap` | `vibedesignlab/slopslap` version `1.3.0`, exact commit `NOT_PROVEN` | modified derivative with vendored taxonomy, data, references, and scripts | MIT | `LICENSES/MIT-vibedesignlab-slopslap.txt` |

## Modification notices

### Microsoft Playwright CLI

`cx-browser-automation` adapts the Playwright CLI skill for Codex routing and permission boundaries, adds local wrappers and reference guides, and separates browser interaction from final visual verdict ownership.

Copyright (c) Microsoft Corporation.

### Oh My OpenAgent

The following are modified copies or derivatives:

- `cx-coding-agent-sessions`
- `cx-debugging`
- `cx-programming`
- `cx-ultraresearch`
- `cx-visual-qa`

They were condensed, reorganized, or adapted for Codex. Some session and visual QA files remain byte-identical to the source archive. The Sustainable Use License permits redistribution only free of charge for non-commercial purposes. The full terms accompany this collection.

### Insane Search

`cx-insane-search` adapts `fivetaku/insane-search` for Codex, rewrites public-content and permission boundaries, and retains modified engine and test material.

Copyright (c) 2026 fivetaku.

### Insane Research

`cx-insane-search` and `cx-ultraresearch` adapt selected concepts from
`fivetaku/insane-research`: retrieval metadata separation, working source and
claim maps, countersearch, contradiction states, and temporal evidence. The
fixed orchestration, automatic agent fan-out, permission bypass, mandatory
artifacts, claim validator, and report evaluator are not included.

Copyright (c) 2026 fivetaku.

### Slopslap

`cx-slopslap` converts `vibedesignlab/slopslap` for Codex and modifies host discovery, concurrency, Git behavior, report serving, and browser resolution while retaining upstream taxonomy and implementation material.

Copyright (c) 2026 groovelb.

### Ouroboros

The four Ouroboros-derived skills preserve method provenance while excluding the upstream MCP, orchestration, scoring, persona fan-out, and execution runtime. Their current wording is independent.

Copyright (c) 2025 Q00.

## External runtime invocations

The following tools are referenced or invoked but their source code is not bundled:

- `vercel-labs/agent-browser@0.29.1` — Apache License 2.0
- `ibelick/ui-skills@0.2.4` — MIT License

They are recorded for dependency provenance and are not classified as redistributed source.

## Research references not redistributed

The following projects informed comparison, historical research, or the broader
coding-agent design context. No current bundled skill or agent is classified as
copied from them:

- `code-yeongyu/lazycodex`
- `Yeachan-Heo/gajae-code`
- `can1357/oh-my-pi`

They are acknowledgements, not claims of endorsement or runtime dependency.

## OpenAI references

The repository follows OpenAI's public Codex documentation for skills,
repository `AGENTS.md`, and custom-agent configuration. OpenAI software, model
weights, trademarks, documentation, and examples are not redistributed by this
notice. Highfloor for Codex is independent and unofficial.
