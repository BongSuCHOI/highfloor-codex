# pwntools

Use pwntools as a deterministic process or protocol harness for authorized reproduction.

Useful roles:

- launch a process with exact arguments/environment;
- capture binary-safe input/output;
- replay a minimal protocol sequence;
- attach a debugger at a controlled point;
- parse addresses or structured binary fields.

Keep the harness scoped to the failure. Do not turn diagnosis into an exploit recipe or remote target interaction outside the user's authorization.
