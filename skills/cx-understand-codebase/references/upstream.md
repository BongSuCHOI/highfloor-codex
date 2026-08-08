# Upstream provenance

## Source

- Project: [`Egonex-AI/Understand-Anything`](https://github.com/Egonex-AI/Understand-Anything)
- Inspected commit: `fe8c5bc591716aafd79b4765549328f08ef5a52e`
- Upstream plugin version: `2.9.4`
- License: MIT
- Copyright: `Copyright (c) 2026 Yuxiang Lin`
- Copyright: `Copyright (c) 2026 Infinite Universe, Inc.`
- License copy: [`LICENSE.upstream.txt`](LICENSE.upstream.txt)

## Relationship

`cx-understand-codebase` is a modified derivative and Codex-native distribution of
the upstream codebase-analysis workflow. It retains:

- deterministic file scanning, language detection, ignore handling, tree-sitter
  import extraction, semantic batching, graph merging, test-link normalization,
  and fingerprint generation;
- the upstream specialist prompts for scanning, file analysis, assembly review,
  architecture, tours, graph review, and domain extraction;
- the `KnowledgeGraph` node/edge/layer/tour schema;
- the React interactive dashboard and read-only token-gated local viewer;
- pinned workspace packages and `pnpm-lock.yaml` needed to build the analysis
  and viewer runtime.

Highfloor modifications:

- replace Claude slash-command routing with one `$cx-understand-codebase` skill and
  action words (`analyze`, `dashboard`, `ask`, `explain`, `diff`, `onboard`,
  `domain`);
- keep the requested Codex worktree as the target instead of redirecting to the
  main checkout;
- treat all target project content as untrusted data for every worker;
- remove automatic hooks and post-commit updates;
- use pinned `npx --yes pnpm@10.6.2` plus the frozen lockfile, with runtime
  dependencies isolated in a source-versioned user cache so generated files do
  not mutate the installer-managed skill;
- carry one pre-resolved target/data path through workers, quote runtime paths,
  and write untrusted JSON through the host editor instead of shell interpolation;
- always exclude persistent `.ua/` and legacy `.understand-anything/` outputs
  from source scans;
- replace a per-run inline graph-validator script with the bundled
  `scripts/validate-graph.mjs`;
- separate complete and partial artifacts so failed coverage cannot advance
  freshness metadata or auto-launch the dashboard;
- keep the viewer local on `127.0.0.1`, token-gated, and `--no-open` by default;
- replace user-facing viewer slash-command hints and omit the unrelated bundled
  demo graph;
- normalize machine-specific example paths for portable repository validation;
- compress repeated orchestration while preserving phase artifacts and failure
  boundaries.

Upstream Figma and external knowledge-base workflows are not exposed by this
skill because the requested scope is codebase and harness understanding. Their
runtime is not needed for the retained analysis/dashboard vertical slice.

## Vendored grammar artifacts

The retained upstream runtime includes its existing Dart and Swift tree-sitter
WASM workspace packages. Their `BUILD.md`, package metadata, Swift grammar pin,
and Swift MIT license remain beside the artifacts. The Dart package records
`tree-sitter-dart@1.0.0` (publisher `amaanq`, MIT); the Swift package records
`alex-pinkus/tree-sitter-swift` at
`d42e9bb24646c4dbf1f5ec476a35b96d817da448` (MIT).
