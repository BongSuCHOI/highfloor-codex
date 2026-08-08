# Change-impact analysis

Map an explicit diff or the current working tree onto the existing knowledge
graph. This action diagnoses impact; it does not modify source.

1. Resolve the exact target/data directory and complete graph.
2. Determine the comparison boundary from the request. Without another stated
   boundary, use staged, unstaged, and untracked working-tree files. Do not
   silently guess a PR base branch.
3. Validate graph freshness. A stale graph may still provide historical context,
   but label missing current nodes and relationships.
4. Match changed paths to file, function, class, config, document, service,
   pipeline, table, schema, resource, and endpoint nodes.
5. Follow one-hop incoming and outgoing edges. Expand another hop only when a
   confirmed call/dependency path makes it material.
6. Report direct components, affected components, layers, cross-layer edges,
   complexity hotspots, and specific review/test risks. Graph degree alone is
   not proof of runtime impact.
7. Write `$UA_DIR/diff-overlay.json` atomically with:

   ```json
   {
     "version": "1.0.0",
     "baseBranch": "<explicit boundary or working-tree>",
     "generatedAt": "<ISO timestamp>",
     "changedFiles": [],
     "changedNodeIds": [],
     "affectedNodeIds": []
   }
   ```

Start the dashboard only when the user asks to visualize the overlay.
