# Upstream attribution

Codex conversion of `slopslap` by vibedesignlab.

- Upstream package: `slopslap`
- Upstream plugin version: `1.3.0`
- Source archive used for this local conversion: `slopslap`
- License: MIT; see `UPSTREAM_LICENSE.txt`

Codex-specific changes replace Claude plugin discovery, `${CLAUDE_PLUGIN_ROOT}`, fixed five-agent concurrency, automatic Git operations, background report serving, and hard-coded Playwright resolution. Taxonomy, reference corpus, matrix data, inspection areas, and core scripts remain vendored for later comparison.

## Optional Gesso checker

- Upstream repository: [`Gesso-Build/skills`](https://github.com/Gesso-Build/skills)
- Inspected source commit: `ab68f1878dd5f19ac8dee9d55d2f4313060cac83`
- Runtime package: `@gessobuild/anti-slop@0.4.2`
- License: MIT; see the upstream repository license
- Relationship: `runtime invocation` and `research reference`

Highfloor independently documents a pinned, check-only JSON pass for
self-contained rendered HTML. It treats checker issues as candidates and
execution gaps as incomplete evidence. In an observed v0.4.2 smoke check, JSON
did not surface an external-stylesheet coverage gap, so the runtime contract
requires inspecting the HTML and skipping or bounding that case first. No Gesso
source, rule corpus, prevention prompt, baseline CSS, or auto-fix implementation
is bundled. Automatic fixes were deliberately excluded because they can
rewrite intentional content, semantics, styling, and accessibility.
