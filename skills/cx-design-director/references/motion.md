# Motion

Use motion only when it explains change, origin/destination, available action, success/failure or priority.

Before implementation, identify the trigger, expected frequency, purpose,
source and destination, stable states, cancellation behavior and reduced-motion
equivalent. A rare narrative transition and a repeatedly used control should
not inherit the same motion merely because they share a component.

Conservative starting ranges:

- Micro feedback: 100–180 ms
- Control/state transition: 160–260 ms
- Page/panel transition: 220–360 ms
- Rare emphasis: up to 600 ms

Treat these as starting points, not fixed acceptance criteria. Prefer responsive easing, and prefer transform/opacity over layout-thrashing properties.

Define reduced-motion behavior for every material animation. Replace large movement, parallax, repeated pulses and forced smooth scrolling with opacity, color, outline or immediate state changes. Motion must not hide content, delay primary actions or carry information that disappears when animation is disabled.

## Interaction continuity

- Keep the before and after states, semantic order, focus and recovery path
  coherent.
- Exercise repeated input, interruption, reversal, cancellation and rapid state
  changes when the interaction permits them. Continue from the current visible
  state rather than jumping back to a stale origin or locking input.
- Preserve a usable resting state when animation fails, is disabled or ends
  early.

Do not reject or approve motion from a universal duration, easing, scale value,
API or CSS property alone. Performance, device behavior and accessibility
claims require evidence from the corresponding environment; code inspection
can establish only the implemented path.
