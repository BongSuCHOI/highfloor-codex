# Agent Browser

Run commands through the pinned wrapper:

```bash
bash <skill-root>/scripts/agent_browser.sh open <url>
bash <skill-root>/scripts/agent_browser.sh snapshot -i
bash <skill-root>/scripts/agent_browser.sh click @e1
```

## Interaction loop

1. Open or navigate.
2. Run `snapshot -i` to obtain current element refs.
3. Interact with refs using `click`, `fill`, `press`, `select`, `check` or `upload`.
4. Re-snapshot after navigation, modal/menu changes, async replacement or a stale-ref error.
5. Capture only the screenshot, console, network or trace evidence required by the task.

Use `<command> --help` for uncommon commands instead of loading a full command catalog.

## Sessions and state

- Use a named `--session` to isolate unrelated workflows.
- Reuse an already authenticated user-controlled browser when the task depends on visible login state.
- If login is required, let the user complete credentials, MFA, CAPTCHA or security prompts.
- Store authentication state only when the user requests it, keep it out of source control and remove it after use when no longer needed.
- Do not print secrets, extract cookies from an unrelated profile or inject copied cookies into a new session.

Treat refs as ephemeral page state, not durable selectors.
