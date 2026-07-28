# Corpus Maintenance

Use only when the user asks to update the vendored reference corpus.

Regenerate quantitative data with pinned packages in npm's cache:

```bash
bash "<skill-root>/scripts/run-node-deps.sh" gen-references
```

Recapture an authorized public reference:

```bash
bash "<skill-root>/scripts/run-node-deps.sh" capture-reference <url> <outDir> --id <unit-id>
```

If `node` or `npx` is missing, propose the exact Node.js installation command. If Playwright reports a missing browser executable, propose the exact pinned browser download and wait for approval. Do not reinterpret navigation, selector, authentication or script failures as dependencies, and do not bypass login, CAPTCHA, paywall, private network or permission gates.

Update provenance and license records with the corpus. Captured screenshots are internal evidence and must not be copied into target projects.
