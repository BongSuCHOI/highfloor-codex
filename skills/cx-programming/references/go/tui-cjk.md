# Go TUI and CJK

Verify framework APIs against the version in the active module.

- Distinguish bytes, runes, grapheme clusters and terminal display cells.
- Cursor movement, selection and truncation must use the unit required by the UI, not raw byte length.
- Test wide CJK glyphs, combining marks, emoji and mixed CJK/Latin strings.
- Preserve IME composition behavior; avoid treating every key event as committed text.
- Handle terminal resize and minimum dimensions without clipping primary actions.
- Wrap on semantic or grapheme-safe boundaries and verify the rendered cell grid.

Use deterministic model/update tests for state and a rendered grid or ANSI artifact when visual alignment matters.
