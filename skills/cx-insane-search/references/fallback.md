# Fallback Decisions

Use the engine trace instead of repeating every route manually.

1. Prefer a documented public endpoint or feed for the identified platform.
2. Try ordinary public HTML through the generic fetch chain.
3. Use Jina Reader or structured metadata when they can represent the same public page.
4. Use local browser rendering only for a public JavaScript shell whose content is available without login or challenge bypass.
5. Stop on authentication, permission, paywall, CAPTCHA, deleted/private content, SSRF rejection or a real not-found response.

If `grid_exhausted=false`, an exhaustive run may try remaining implemented routes. If `untried_routes` is non-empty, attempt only those routes. Escalate browser interaction to `$cx-browser-automation`; do not add an unimplemented route merely because a reference mentions it.
