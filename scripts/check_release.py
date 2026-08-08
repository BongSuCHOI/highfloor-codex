#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
CHANGELOG_HEADING_RE = re.compile(
    r"^## \[(?P<version>[^\]]+)\] - (?P<released>\d{4}-\d{2}-\d{2})$",
    re.MULTILINE,
)

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def read(path: str) -> str:
    file_path = ROOT / path
    if not file_path.is_file():
        fail(f"missing release file: {path}")
        return ""
    return file_path.read_text(encoding="utf-8")


def manifest_entries(path: str) -> list[str]:
    return [line.strip() for line in read(path).splitlines() if line.strip()]


def check_version_and_changelog() -> str:
    version = read("VERSION").strip()
    if not SEMVER_RE.fullmatch(version):
        fail(f"VERSION is not valid SemVer: {version!r}")
        return version

    changelog = read("CHANGELOG.md")
    headings = [
        match
        for match in CHANGELOG_HEADING_RE.finditer(changelog)
        if match.group("version") == version
    ]
    if len(headings) != 1:
        fail(
            "CHANGELOG.md must contain exactly one dated heading for "
            f"[{version}], found {len(headings)}"
        )
    else:
        released = headings[0].group("released")
        try:
            date.fromisoformat(released)
        except ValueError:
            fail(f"CHANGELOG.md has an invalid release date: {released!r}")

        unreleased_at = changelog.find("## [Unreleased]")
        version_at = headings[0].start()
        if unreleased_at < 0:
            fail("CHANGELOG.md is missing ## [Unreleased]")
        elif unreleased_at > version_at:
            fail("CHANGELOG.md must keep [Unreleased] above the current release")

    return version


def check_versioned_examples(version: str) -> None:
    if not version:
        return

    expected_tag = f"v{version}"
    for path in ("README.md", "README_KR.md", "docs/INSTALLATION.md"):
        content = read(path)
        if version not in content:
            fail(f"{path} does not mention current VERSION {version}")
        if expected_tag not in content:
            fail(f"{path} does not contain a pinned {expected_tag} example")


def check_catalogs_and_provenance() -> None:
    skills = manifest_entries("manifest/skills.txt")
    agents = manifest_entries("manifest/agents.txt")
    skill_catalog = read("skills/CX_SKILL_CATALOG.md")
    migration_manifest = read("skills/CX_MIGRATION_MANIFEST.md")
    agent_catalog = read("docs/AGENT_CATALOG.md")
    third_party_notices = read("THIRD_PARTY_NOTICES.md")

    catalog_cards = sorted(
        re.findall(r"^### `(cx-[^`]+)`$", skill_catalog, re.MULTILINE)
    )
    if catalog_cards != skills:
        fail(
            "skills/CX_SKILL_CATALOG.md card set must equal skill manifest: "
            f"cards={catalog_cards!r}, manifest={skills!r}"
        )

    inventory_match = re.search(
        r"^## 2\. Live inventory$(?P<body>.*?)^## 3\.",
        migration_manifest,
        re.MULTILINE | re.DOTALL,
    )
    if not inventory_match:
        fail("skills/CX_MIGRATION_MANIFEST.md: missing live inventory section")
        live_inventory: list[str] = []
    else:
        inventory_body = inventory_match.group("body")
        live_inventory = re.findall(
            r"^- `(cx-[^`]+)`$", inventory_body, re.MULTILINE
        )
        count_match = re.search(
            r"Current live `cx-\*` skills: (?P<count>\d+)\.",
            inventory_body,
        )
        if not count_match or int(count_match.group("count")) != len(skills):
            fail(
                "skills/CX_MIGRATION_MANIFEST.md: live inventory count "
                f"must equal {len(skills)}"
            )
    if live_inventory != skills:
        fail(
            "skills/CX_MIGRATION_MANIFEST.md live inventory must equal skill "
            f"manifest: inventory={live_inventory!r}, manifest={skills!r}"
        )

    for skill in skills:
        skill_root = ROOT / "skills" / skill
        provenance = sorted((skill_root / "references").glob("upstream*.md"))
        if not provenance:
            fail(f"{skill}: missing references/upstream*.md provenance record")
        if f"| `{skill}` |" not in migration_manifest:
            fail(f"{skill}: missing provenance row in skills/CX_MIGRATION_MANIFEST.md")
        if f"`{skill}`" not in third_party_notices:
            fail(f"{skill}: missing from THIRD_PARTY_NOTICES.md")

    for agent_file in agents:
        agent = Path(agent_file).stem
        if f"`{agent}`" not in agent_catalog:
            fail(f"{agent}: missing from docs/AGENT_CATALOG.md")


def check_release_policy_files() -> None:
    for path in (
        "LICENSE",
        "THIRD_PARTY_NOTICES.md",
        "docs/RELEASING.md",
        "skills/CX_MIGRATION_MANIFEST.md",
    ):
        read(path)


def main() -> int:
    version = check_version_and_changelog()
    check_versioned_examples(version)
    check_catalogs_and_provenance()
    check_release_policy_files()

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(
            f"Release consistency check failed with {len(errors)} error(s).",
            file=sys.stderr,
        )
        return 1

    print(f"Release consistency passed for {version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
