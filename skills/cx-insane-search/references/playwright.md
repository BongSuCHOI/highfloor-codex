# Browser Rendering Boundary

Use host-provided browser automation only when a permitted public page is a
JavaScript shell and the same content should be available without
authentication.

The public engine path does not launch its retained local browser templates.
Those templates cannot guarantee the guarded HTTP transport's DNS pinning or
block hostile private-network subresources. A failure result instead sets
`must_invoke_browser_automation=true`.

For interactive navigation, state inspection, or evidence capture, use
`$cx-browser-automation`. Keep its result separate from the engine's retrieval
verdict.

Do not inject cookies, extract a logged-in profile, solve challenges, alter
anti-bot scripts, or continue past login, paywall, CAPTCHA, private-network, or
permission gates. A browser-rendered challenge page is still a failure.
