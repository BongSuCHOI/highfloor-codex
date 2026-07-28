# Structured Endpoint Discovery

Use a structured endpoint only when it represents the same public resource and is discoverable from documentation, page markup or network activity.

Common candidates:

- a public `.json` representation;
- RSS or Atom;
- oEmbed;
- documented REST or GraphQL queries that require no private credential;
- a public page's own same-origin data request.

Do not guess credentials, register for keys automatically, replay authenticated headers or crawl unrelated API surfaces. Validate response content rather than treating HTTP 200 as success.
