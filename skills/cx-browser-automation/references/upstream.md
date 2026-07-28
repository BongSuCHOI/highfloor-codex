# Upstream provenance and modification notice

This skill contains modified material derived from Microsoft Playwright CLI.

- Upstream: `microsoft/playwright-cli`
- Relevant source: `skills/playwright-cli/SKILL.md`
- Source branch used by the earlier conversion: `main`
- Exact source commit: `NOT_PROVEN`
- License: Apache License 2.0; see `LICENSE.upstream.txt`

Prominent modification notice:

- adapted the Playwright CLI skill for Codex routing and permission boundaries;
- replaced upstream-oriented setup with local wrapper and reference guides;
- separated browser interaction from final visual verdict ownership.

The skill also invokes `vercel-labs/agent-browser@0.29.1` as an external runtime dependency. Agent Browser source is not bundled here. Its upstream license is Apache License 2.0.
