# Ghidra

Use Ghidra for authorized static analysis when symbols or source are unavailable.

1. Import the exact binary and choose the correct architecture/loader.
2. Let analysis complete, then begin from strings, imports, exports, entry points or a located crash address.
3. Follow cross-references and rename functions/variables only when evidence supports the meaning.
4. Treat decompiler output as a reconstruction; verify calling convention, data width and control flow in disassembly.

Record image base and offsets so findings map back to runtime addresses.
