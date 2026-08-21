# Custom Agent Catalog

This catalog explains when to delegate to each Highfloor custom agent. The TOML
files in `agents/` are the runtime source of truth.

## Selection rule

Delegate only when isolation, specialist boundaries, or independent progress is
materially useful. Keep small, sequential, tightly coupled work in the main
thread.

Choose one owner per evidence question. Do not delegate the same diagnosis or
review to multiple agents merely to repeat verification.

## Authority classes

| Class | Meaning |
|---|---|
| `read-only` | Analyze and report; do not modify repository or application state |
| `evidence workspace` | May create scoped diagnostic artifacts, traces, or reports; application edits remain out of scope |
| `workspace-write` | May implement only the explicitly assigned files or responsibility |

`sandbox_mode` is a technical capability, not authorization to expand the task.
Every delegated assignment still needs a concrete scope and expected result.

## Complete inventory

| Agent | Model / effort | Authority | Primary responsibility |
|---|---|---|---|
| `accessibility-tester` | `gpt-5.6-luna` / `max` | evidence workspace | Evidence-based accessibility testing of rendered UI, interaction states, keyboard flow, semantics, and assistive-technology risk |
| `ai-engineer` | `gpt-5.6-terra` / `high` | workspace-write | Model calls, prompts, tools, retrieval, evaluation, and production failure handling |
| `architect` | `gpt-5.6-sol` / `medium` | read-only | System boundaries, interfaces, coupling, data flow, migration shape, and maintainability |
| `browser-debugger` | `gpt-5.6-terra` / `high` | evidence workspace | Browser reproduction and console, network, state, screenshot, or trace evidence |
| `critic` | `gpt-5.6-sol` / `high` | read-only | Adversarial plan critique, hidden assumptions, alternatives, and execution readiness |
| `data-analyst` | `gpt-5.6-sol` / `medium` | read-only | Interpretation of existing datasets, metrics, trends, anomalies, and decisions |
| `data-engineer` | `gpt-5.6-terra` / `high` | workspace-write | Ingestion, transformation, data contracts, backfills, and recoverable ETL |
| `database-engineer` | `gpt-5.6-terra` / `high` | workspace-write | Schema, migration, query, transaction, and compatibility changes |
| `debugger` | `gpt-5.6-sol` / `medium` | evidence workspace | Root-cause isolation for crashes, hangs, wrong behavior, flakiness, and binaries |
| `default` | `gpt-5.6-luna` / `xhigh` | workspace-write | General fallback for bounded delegated work without a better specialist owner |
| `docs-researcher` | `gpt-5.6-luna` / `xhigh` | read-only | Current APIs, defaults, versions, and framework behavior from primary sources |
| `explorer` | `gpt-5.6-luna` / `xhigh` | read-only | Owning paths, execution flow, state transitions, and change boundaries |
| `financial-systems-reviewer` | `gpt-5.6-sol` / `high` | read-only | Payment, ledger, settlement, reconciliation, precision, idempotency, and audit flows |
| `incident-responder` | `gpt-5.6-sol` / `high` | read-only | Impact, timeline, containment, recovery decisions, and cause investigation |
| `infra-engineer` | `gpt-5.6-terra` / `high` | workspace-write | Cloud, IaC, deployment, networking, and environment changes |
| `mcp-developer` | `gpt-5.6-terra` / `high` | workspace-write | MCP server/client contracts, transport, capabilities, auth, and host integration |
| `mobile-engineer` | `gpt-5.6-terra` / `high` | workspace-write | iOS/Android screens, lifecycle, state, API integration, and platform behavior |
| `performance-investigator` | `gpt-5.6-sol` / `medium` | evidence workspace | Measured latency, throughput, memory, rendering, hot paths, and scaling bottlenecks |
| `planner` | `gpt-5.6-sol` / `medium` | read-only | Executable, right-sized plans from approved intent |
| `reliability-reviewer` | `gpt-5.6-sol` / `medium` | read-only | Failure modes, retries, timeouts, recovery, observability, and degraded operation |
| `research-analyst` | `gpt-5.6-sol` / `medium` | read-only | Bounded source-backed investigations, comparisons, and evidence synthesis |
| `reviewer` | `gpt-5.6-terra` / `high` | read-only | PR-style correctness, regression, integration, security, and test review |
| `risk-reviewer` | `gpt-5.6-sol` / `medium` | read-only | Product, technical, operational, legal-adjacent, and delivery risk |
| `security-reviewer` | `gpt-5.6-sol` / `high` | read-only | Trust, authentication, authorization, secrets, inputs, exploitability, and mitigation |
| `systems-engineer` | `gpt-5.6-terra` / `high` | workspace-write | Ownership, concurrency, memory, process, resource, and performance-sensitive systems |
| `technical-writer` | `gpt-5.6-terra` / `medium` | workspace-write | Release notes, migrations, onboarding, operator guidance, and developer docs |
| `test-engineer` | `gpt-5.6-luna` / `xhigh` | workspace-write | Targeted regression coverage, deterministic fixtures, and focused verification |
| `windows-engineer` | `gpt-5.6-terra` / `high` | workspace-write | PowerShell, services, identity, policy, registry, and Windows administration |
| `worker` | `gpt-5.6-luna` / `xhigh` | workspace-write | Execution fallback for bounded implementation without a better specialist owner |

## Common choices

### `default` vs `worker` vs specialists

- Use a named specialist whenever one owns the task boundary.
- Use `worker` for bounded implementation with no better specialist owner.
- Use `default` only for other bounded delegated work with no better specialist
  owner.
- These files intentionally override Codex's built-in agents with matching
  names; they are fallbacks, not replacements for deliberate role selection.

### `explorer` vs `architect`

- Use `explorer` to establish what the current code does and where ownership
  lives.
- Use `architect` to evaluate boundaries, coupling, migration shape, and
  long-term implications.

### `docs-researcher` vs `research-analyst`

- Use `docs-researcher` for an API, default, version, standard, or framework
  behavior with an authoritative definition.
- Use `research-analyst` for a broader technical question requiring comparison
  or synthesis across sources.

### `debugger` vs `browser-debugger`

- Use `debugger` when the cause can be isolated through runtime, logs, tests,
  stack traces, process state, or binary evidence.
- Use `browser-debugger` when reproduction requires a live page and browser
  console, network, storage, DOM, screenshot, or trace state.

### `reviewer` vs specialist reviewers

- Start with `reviewer` for general change correctness.
- Choose `security-reviewer`, `reliability-reviewer`,
  `financial-systems-reviewer`, or `accessibility-tester` when that boundary is
  material enough to own the verdict.
- Do not stack every reviewer on routine changes.

### `planner` vs `critic`

- `planner` turns approved intent into executable sequencing.
- `critic` decides whether the plan relies on hidden assumptions or needs an
  alternative before execution.

## Delegation contract

A useful assignment states:

1. the concrete question or implementation outcome;
2. owned files or responsibility;
3. read/write authority;
4. relevant constraints and non-goals;
5. expected evidence or deliverable;
6. a stop condition.

Example:

```text
Use explorer to trace the request-authentication flow from route entry to
session persistence. Read-only. Return owning files, key call edges, state
transitions, and unresolved branches. Stop when the end-to-end flow is mapped;
do not propose or implement a fix.
```

For a write agent, also state that other contributors may be editing the
repository and unrelated changes must not be reverted.

## Model availability

The model names and reasoning efforts are intentional defaults, but they are
not portable guarantees. Codex accounts and product surfaces may expose
different catalogs. Installation preserves the repository values exactly.
Highfloor installs custom `default`, `worker`, and `explorer` definitions, so
their values override the matching built-in agents without editing the user's
`config.toml` or changing unrelated subagent defaults.

If a model is unavailable:

1. copy or edit the installed agent TOML locally;
2. choose an available model suitable for the role;
3. preserve the agent name, authority, and developer instructions unless you
   intentionally create a local variant.

Public changes to model defaults should include host evidence and a changelog
entry.
