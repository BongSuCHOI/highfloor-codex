# Reframing Lenses

Use lenses as optional prompts, not personas or authorities.

## Selection

### Researcher

Use when one missing fact could decide the path.

Ask:

- What do we claim without evidence?
- What smallest repository inspection, experiment, or current source resolves it?

### Contrarian

Use when the same assumption survives repeated failure.

Ask:

- What if the central assumption is false?
- Are we solving the wrong problem or preserving a false constraint?

### Simplifier

Use when scope, coupling, or verification surface is too large.

Ask:

- Which approved outcome creates most value?
- What can be removed without violating the contract?

### Architect

Use when local fixes recur because ownership or boundaries are wrong.

Ask:

- Which boundary produces the repeated failure?
- Would a different ownership or state transition remove the class of failure?

## Alternative shape

```yaml
alternative: Concrete path
challenged_assumption: What this path disputes
preserves:
  - Approved constraint or outcome
risks:
  - Constraint, cost, compatibility, or uncertainty
discriminating_step: Smallest experiment or user decision
downside: Primary trade-off
```

Generate at most three alternatives by default. Record tried and rejected approaches.

## Simulation: conflicting alarm-app constraints

Stuck point:

```text
The user wants automatic email invitations but prohibits any email provider.
```

Reframe:

```text
Challenged assumption:
Invitation must mean automatic email delivery.

Alternative A:
Generate a 24-hour copyable invite link.
Preserves: no external email provider
Test: verify link creation, expiry, and joining
Downside: operator must deliver the link

Alternative B:
Display a short invite code for manual delivery.
Preserves: no external service and smallest implementation
Test: verify one-time code redemption
Downside: weaker user convenience
```

If either choice changes an approved outcome, return to `$cx-interview` for amendment and approval.

## Simulation: repeated implementation strategy

If three local patches fail because state ownership is split across client and server, choose the Architect lens. Do not brainstorm more local patches. Propose one boundary change and one discriminating characterization test. Use `$cx-debugging` first if the actual failure mechanism remains unknown.
