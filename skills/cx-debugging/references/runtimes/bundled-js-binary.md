# Bundled JavaScript Binary

Use when a CLI or desktop executable embeds or bundles JavaScript.

## Identify the bundle

- Resolve the executable and launcher chain.
- Distinguish a script wrapper, SEA/snapshot, pkg/nexe-style archive, Electron asar and ordinary minified bundle.
- Record runtime/version clues, archive boundaries and source-map availability.
- Compare the artifact actually launched with the repository build output.

## Investigation

Prefer official extraction or archive tooling for the identified format. Preserve the original artifact and work on a copy when extraction changes files. Search recovered sources for error text, command names, configuration keys and protocol messages before deminifying everything.

Static recovery may show possible control flow but not the live branch, environment or state. Confirm runtime claims with logs, tracing, a debugger or a controlled input when possible.
