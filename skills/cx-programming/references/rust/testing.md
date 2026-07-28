# Rust Testing

- Use property tests for invariants, round trips, parsers and state transitions with a broad input space.
- Use snapshots for stable structured output where a reviewed diff is meaningful.
- Keep examples small enough that failures identify the violated rule.
- Reuse existing project tools; do not add proptest, insta or a new runner for a local assertion that ordinary tests cover.
- For async and concurrency behavior, control time and synchronization instead of relying on sleeps.
- For `unsafe`, test the safe wrapper's observable contract and select a specialized tool only for its applicable failure class.

Update snapshots deliberately and inspect the semantic diff before acceptance.
