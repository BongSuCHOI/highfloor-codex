# Security Policy

## Supported versions

Until `1.0.0`, security fixes target the latest tagged release and `main`.
After `1.0.0`, this table will identify supported release lines.

| Version | Supported |
|---|---|
| latest release | yes |
| `main` | yes, pre-release |
| older releases | best effort |

## Reporting a vulnerability

Use GitHub's private vulnerability reporting for this repository when enabled:

```text
Security tab → Report a vulnerability
```

If private reporting is not yet enabled, contact the maintainer through a
private channel listed on the GitHub profile. Do not include exploit details,
affected user paths, tokens, or private logs in a public issue.

Include:

- affected version or commit;
- operating system and shell;
- installation method and selected destination;
- minimal reproduction;
- impact and reachable trust boundary;
- whether secrets or arbitrary files are exposed;
- suggested mitigation if known.

Please allow a reasonable coordinated-disclosure window before publication.

## Security scope

High-priority reports include:

- installer path traversal or command injection;
- deletion or overwrite outside exact managed targets;
- unsafe archive extraction or source confusion;
- untrusted repository content gaining unintended execution;
- secrets or session data committed or exposed by bundled tools;
- a skill instruction that bypasses authentication, authorization, paywalls,
  CAPTCHA, private networks, or explicit user authority;
- license/provenance tampering that misrepresents executable content.

Ordinary prompt quality, unavailable models, unsupported product surfaces, and
expected permissions prompts are generally support issues unless they create a
concrete security boundary failure.

## Installer trust

Piping a remote script to a shell transfers execution trust to the selected
repository and ref. The safer default for sensitive environments is:

1. clone or download a release;
2. verify the tag and review `install.sh`;
3. run `--dry-run`;
4. install locally.

The installer does not request elevated privileges, modify system directories,
or install dependencies.
