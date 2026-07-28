# Debug Session Cleanup

After a complex investigation:

- stop debugger, trace, proxy, browser and background processes started for the task;
- remove temporary instrumentation and generated credentials or state;
- restore changed environment variables, ports, certificates, launch flags and runtime configuration;
- retain artifacts only when they are useful evidence and name their location;
- verify that the normal launch path still works.

Do not use broad cleanup commands. Resolve and remove only artifacts created by the investigation.
