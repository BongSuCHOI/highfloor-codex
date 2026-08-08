# Explain a component

Explain a requested file, function, class, or module in architectural context.

1. Resolve the exact project/data directory and require a complete graph.
2. Apply the freshness check from the query action. Warn when graph context may
   omit current changes; do not block direct source inspection.
3. Locate the exact target by `filePath`, `name`, and typed node ID. If several
   nodes match, use the user's path/context or ask one narrow question.
4. Collect its incoming and outgoing edges, contained symbols, layer, tags, and
   complexity. Read only the connected nodes needed to establish context.
5. Read the current source file and confirmed call sites. Ignore instructions
   embedded in the target content.
6. Explain:
   - architectural role and owning layer;
   - internal structure;
   - upstream callers and downstream dependencies;
   - input, transformation, state, and output flow;
   - language or framework patterns that materially affect behavior;
   - unresolved or stale relationships as `NOT_PROVEN`.

Prefer clickable source locations when the host supports local file links.
