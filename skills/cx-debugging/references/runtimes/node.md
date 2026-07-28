# Node.js, Bun and Deno Runtime Debugging

Confirm the actual launcher, runtime/version, module mode, working directory, environment and built artifact. Do not assume Node-specific flags work in Bun or Deno.

## Evidence choices

- Use the runtime's inspector when breakpoints, heap or CPU profiles answer the question.
- Verify source maps point to the artifact actually running.
- For event-loop delay or hangs, inspect active handles, pending promises, timers and blocking synchronous work.
- For unhandled failures, preserve the original stack and the boundary that created or translated the promise.
- For bundled output, use `bundled-js-binary.md`.

Start with application logs and a minimal reproduction before enabling broad trace categories. Treat package resolution, ESM/CJS and duplicate-runtime issues as identity problems until proven otherwise.
