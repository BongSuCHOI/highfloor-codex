# Browser Rendering Boundary

Use browser fallback only when a public page is a JavaScript shell and the same content should be available without authentication.

The engine's browser template is a bounded fetch route. For interactive navigation, state inspection or evidence capture, use `$cx-browser-automation`.

Do not inject cookies, extract a logged-in profile, solve challenges, alter anti-bot scripts or continue past login, paywall, CAPTCHA, private-network or permission gates. A browser-rendered challenge page is still a failure.
