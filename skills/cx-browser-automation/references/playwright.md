# Playwright CLI

Run the pinned CLI through:

```bash
bash <skill-root>/scripts/playwright_cli.sh open https://example.com
bash <skill-root>/scripts/playwright_cli.sh snapshot
bash <skill-root>/scripts/playwright_cli.sh click e3
```

## Core loop

1. Open the page, using `--headed` when visible state matters.
2. Snapshot before referring to element IDs.
3. Interact with the latest IDs.
4. Snapshot again after navigation or substantial DOM changes.
5. Use `console`, `network`, `tracing-start` and `tracing-stop` only when they answer the active question.

Useful commands include `fill`, `type`, `press`, `hover`, `select`, `upload`, `screenshot`, `tab-new`, `tab-list` and `tab-select`. Use the wrapper's `--help` for the current syntax rather than relying on a copied catalog.

Prefer the repository's existing browser command when it already owns session or fixture setup. Do not create Playwright test files unless the user requests durable tests.
