# TLS Transport Capability

`curl_cffi` can align common browser TLS and HTTP fingerprints for ordinary public HTTP requests. This may avoid false bot classification caused by a non-browser client fingerprint, but it does not solve JavaScript challenges, CAPTCHA, authentication, IP reputation or behavioral checks.

Use only profiles supported by the pinned package and engine. Do not rotate identities, inject cookies, add proxy infrastructure or introduce alternative impersonation libraries during a normal fetch. If the public request still reaches a challenge, follow the browser boundary or stop.
