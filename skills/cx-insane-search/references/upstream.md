# Upstream provenance and modification notice

This skill is a modified Codex conversion of `fivetaku/insane-search`.

- Upstream: `fivetaku/insane-search`
- Source archive used by the original conversion: `insane-search-main`
- Original conversion commit: `NOT_PROVEN`
- Selective refresh reviewed at: `019ee16bbf471595f9b67b164e4a92208183af2d`
- License: MIT; see `LICENSE.upstream.txt`

Prominent modification notice:

- adapted discovery and execution instructions for Codex;
- rewrote public-content, permission, paywall, login, CAPTCHA, and private-network boundaries;
- retained and modified upstream engine and test material;
- added Codex-specific fallback routing and dependency guidance;
- selectively incorporated identifier-boundary challenge detection, decisive
  Cloudflare structural markers, large-document soft-mention handling, and
  installed `curl_cffi` target filtering from the reviewed refresh.

The refresh did not import automatic dependency installation, protocol-stealth
browser execution, default persistent observation logging, site-specific or
internal endpoint routes, or the upstream's broader runtime and artifact
surface. Highfloor's guarded DNS transport, public-content boundary, opt-in
persistence, and host-browser handoff remain authoritative.

The 2026-07 hardening and research handoff also consulted
`fivetaku/insane-research` at
`68f7e59168a9c9b0a586bd4122cb7a229e119d9c` (MIT; see
`LICENSE.insane-research.txt`). Its access-metadata separation informed the
independently worded retrieval evidence envelope. The fixed research
orchestration, agent fan-out, claim validator, evaluator, and artifact layout
were not copied into this skill.
