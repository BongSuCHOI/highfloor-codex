# Partial Runtime Evidence

Use this when the exact failure cannot be reproduced or the target runtime cannot be attached.

## Evidence order

Prefer the strongest available layer:

1. Exact runtime reproduction.
2. Recorded logs, traces, requests, state snapshots or crash artifacts from the failing run.
3. Same build/configuration in a close environment.
4. Source and configuration path analysis.
5. Static artifact or binary inspection.

State which layer supports each conclusion. Do not turn a plausible source path into a confirmed runtime cause.

## Useful discrimination

- Check executable, working directory, environment, build ID and configuration identity.
- Separate absent evidence from evidence that contradicts a hypothesis.
- Look for a prediction unique to the suspected cause.
- Request one additional artifact only when it would materially change the conclusion.

Report confidence and the missing observation that would confirm or falsify the diagnosis.
