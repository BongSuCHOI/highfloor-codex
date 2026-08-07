# Upstream provenance and modification notice

This skill is a modified Codex conversion of `fivetaku/insane-search`.

- Upstream: `fivetaku/insane-search`
- Source archive used by the conversion: `insane-search-main`
- Exact source commit: `NOT_PROVEN`
- License: MIT; see `LICENSE.upstream.txt`

Prominent modification notice:

- adapted discovery and execution instructions for Codex;
- rewrote public-content, permission, paywall, login, CAPTCHA, and private-network boundaries;
- retained and modified upstream engine and test material;
- added Codex-specific fallback routing and dependency guidance.

The 2026-07 hardening and research handoff also consulted
`fivetaku/insane-research` at
`68f7e59168a9c9b0a586bd4122cb7a229e119d9c` (MIT; see
`LICENSE.insane-research.txt`). Its access-metadata separation informed the
independently worded retrieval evidence envelope. The fixed research
orchestration, agent fan-out, claim validator, evaluator, and artifact layout
were not copied into this skill.
