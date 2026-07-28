# CJK and Mixed-Script Typography

Use this for Korean, Japanese, Chinese or mixed CJK/Latin interfaces.

## Type roles

Define display, heading, body, label, caption, code and numeric roles. Choose families with compatible perceived size, stroke weight and baseline behavior rather than matching names alone.

## Readability

- Keep body measure and line height appropriate to the actual script and viewport.
- Verify real glyph coverage for Korean/CJK, punctuation, symbols and numerals.
- Avoid synthetic weight where the font does not provide the intended weight.
- Reserve display treatment for short text; body and controls prioritize recognition.
- Use tabular numerals only where aligned numeric comparison needs them.

## Semantic wrapping

Inspect the rendered result, not only CSS:

- Do not leave Korean particles, endings or short units stranded from the phrase they qualify.
- Keep English product names, versions, numbers, units and citations readable as meaningful groups.
- Avoid manual line breaks that fail at another width.
- Check headings, buttons, table cells, badges, form labels, error messages and source links at affected breakpoints.

Clipping, overlap or broken semantic wrapping in the changed surface is a blocking visual defect.
