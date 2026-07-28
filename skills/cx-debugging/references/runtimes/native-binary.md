# Native Binary Debugging

Use only for authorized binaries and local artifacts.

## Triage

1. Fingerprint format, architecture, signing, build ID and interpreter/loader.
2. Check symbols, linked libraries and whether the binary is stripped or packed.
3. Determine whether the failure is load-time, startup, protocol, memory, concurrency or environment-related.
4. Prefer dynamic observation when the binary can run safely; use static analysis when execution is unavailable or unsafe.

Typical evidence includes `file`, platform dependency tools, symbol tables, crash reports, core dumps and debugger backtraces. Resolve the exact binary path before analysis.

Do not modify system trust stores, proxies, signing state or the binary merely to gain observability without explicit authorization. Do not patch a binary as part of diagnosis unless the user asks for a modification and the change is understood.
