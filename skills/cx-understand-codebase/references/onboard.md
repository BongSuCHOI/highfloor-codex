# Onboarding and handoff guide

Turn a complete graph plus current source checks into a learning path.

1. Resolve the exact project/data directory, require a complete graph, and
   check freshness. Label stale sections rather than hiding them.
2. Read project metadata, layers, guided tour, file-level nodes, entry points,
   and the highest-complexity nodes. Avoid loading function/class detail until a
   tour step needs it.
3. Verify the main entry point, runtime boundary, and two or three critical
   flows against current source.
4. Produce:
   - project purpose and confirmed runtime surfaces;
   - architectural layers and key files;
   - a dependency-ordered guided tour;
   - important concepts and business flows;
   - complexity/risk hotspots;
   - known gaps, stale coverage, and questions for the prior owner.
5. Keep generated guidance in the conversation unless the user asks to save it.
   Writing `docs/ONBOARDING.md` is a separate source change and must preserve the
   target repository's documentation contract.
