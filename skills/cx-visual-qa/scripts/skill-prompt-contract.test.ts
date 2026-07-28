import { describe, expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { join } from "node:path"

const skillText = readFileSync(join(import.meta.dir, "..", "SKILL.md"), "utf8")

describe("cx-visual-qa prompt contract", () => {
	test("requires current sufficient evidence and scoped surface coverage", () => {
		expect(skillText).toContain("Reuse sufficient current evidence")
		expect(skillText).toContain("Enumerate affected")
		expect(skillText).toContain("Broad changes need full affected-surface coverage")
	})

	test("routes browser capture through the Codex browser skill", () => {
		expect(skillText).toContain("$cx-browser-automation")
	})

	test("treats CJK semantic wrapping as blocking", () => {
		expect(skillText).toContain("CJK semantic wrapping")
		expect(skillText).toContain("FAIL")
	})

	test("separates observed defects from missing proof", () => {
		expect(skillText).toContain("`NOT_PROVEN`")
		expect(skillText).toContain("capture, or access problem prevents observation")
	})
})
