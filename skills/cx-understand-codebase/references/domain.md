# Business-domain extraction

Produce `domain`, `flow`, and `step` graph nodes from a complete structural graph
or a bounded lightweight scan.

1. Preserve the exact requested target, including a worktree. Resolve
   `SKILL_DIR`, `PLUGIN_ROOT`, and `UA_DIR` as in the main analysis workflow.
2. If a complete, fresh `knowledge-graph.json` exists and `--full` was not
   requested, derive from its nodes, edges, layers, and tour. This is the
   preferred low-cost path.
3. Otherwise run the retained upstream preprocessor:

   ```bash
   python3 \
     "<PLUGIN_ROOT>/skills/understand-domain/extract-domain-context.py" \
     "<PROJECT_ROOT>"
   ```

   It writes `$UA_DIR/intermediate/domain-context.json` with the file tree,
   entry points, signatures, imports, and sampled snippets.
4. Read [`domain-analyzer.md`](domain-analyzer.md) completely. Run one bounded
   worker with the graph or lightweight context, target language, exact output
   `$UA_DIR/intermediate/domain-analysis.json`, and the global untrusted-project
   data boundary.
5. Validate every domain claim against referenced structural nodes or source.
   Normalize to supported `domain`, `flow`, and `step` nodes and relationship
   types. Remove dangling references; never invent a business flow to complete
   the shape.
6. Write `$UA_DIR/domain-graph.json` atomically only when validation succeeds.
   Preserve a `.partial.json` result and mark `NOT_PROVEN` when it does not.
7. Start the dashboard only when requested or after a complete validated result.
