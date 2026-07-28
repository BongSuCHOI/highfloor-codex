# Motion

Use motion only when it explains change, origin/destination, available action, success/failure or priority.

Conservative starting ranges:

- Micro feedback: 100–180 ms
- Control/state transition: 160–260 ms
- Page/panel transition: 220–360 ms
- Rare emphasis: up to 600 ms

Treat these as starting points, not fixed acceptance criteria. Prefer responsive easing, and prefer transform/opacity over layout-thrashing properties.

Define reduced-motion behavior for every material animation. Replace large movement, parallax, repeated pulses and forced smooth scrolling with opacity, color, outline or immediate state changes. Motion must not hide content, delay primary actions or carry information that disappears when animation is disabled.
