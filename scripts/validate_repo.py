#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
HANGUL_RE = re.compile(r"[가-힣]")
LOCAL_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HTML_SRC_RE = re.compile(r"""<(?:img|source)\b[^>]*\bsrc=["']([^"']+)["']""")
MACHINE_HOME_RE = re.compile(
    r"(?<![A-Za-z0-9._:-])/(?:Users|home)/"
    r"[A-Za-z0-9._-]+(?:/|$)",
    re.MULTILINE,
)
OPENAI_INTERFACE_RE = re.compile(
    r'''^  (?P<key>display_name|short_description|default_prompt): '''
    r'''(?P<quote>["'])(?P<value>.*)(?P=quote)$'''
)

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def read_manifest(path: Path) -> list[str]:
    if not path.is_file():
        fail(f"missing manifest: {path.relative_to(ROOT)}")
        return []

    entries: list[str] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        entry = raw.strip()
        if not entry:
            fail(f"{path.relative_to(ROOT)}:{line_number}: blank manifest entry")
            continue
        if not NAME_RE.fullmatch(entry) or "/" in entry or ".." in entry:
            fail(f"{path.relative_to(ROOT)}:{line_number}: unsafe entry {entry!r}")
            continue
        entries.append(entry)

    if len(entries) != len(set(entries)):
        fail(f"{path.relative_to(ROOT)}: duplicate entries")
    if entries != sorted(entries):
        fail(f"{path.relative_to(ROOT)}: entries must be sorted")
    return entries


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        fail(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return {}

    try:
        end = lines.index("---", 1)
    except ValueError:
        fail(f"{path.relative_to(ROOT)}: unterminated YAML frontmatter")
        return {}

    values: dict[str, str] = {}
    for raw in lines[1:end]:
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def validate_skills() -> None:
    manifest_path = ROOT / "manifest" / "skills.txt"
    entries = read_manifest(manifest_path)
    skills_root = ROOT / "skills"

    discovered = sorted(
        path.name
        for path in skills_root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    if entries != discovered:
        fail(
            "skill manifest mismatch: "
            f"manifest={entries!r}, discovered={discovered!r}"
        )

    for entry in entries:
        if not entry.startswith("cx-"):
            fail(f"skill manifest entry must use the cx- namespace: {entry!r}")
        skill_file = skills_root / entry / "SKILL.md"
        if not skill_file.is_file():
            fail(f"missing skill entry point: {skill_file.relative_to(ROOT)}")
            continue
        frontmatter = parse_frontmatter(skill_file)
        if frontmatter.get("name") != entry:
            fail(
                f"{skill_file.relative_to(ROOT)}: frontmatter name "
                f"{frontmatter.get('name')!r} must equal directory {entry!r}"
            )
        if not frontmatter.get("description"):
            fail(f"{skill_file.relative_to(ROOT)}: missing frontmatter description")

        openai_config = skill_file.parent / "agents" / "openai.yaml"
        if not openai_config.is_file():
            fail(f"{entry}: missing agents/openai.yaml")
            continue

        openai_lines = openai_config.read_text(encoding="utf-8").splitlines()
        if not openai_lines or openai_lines[0] != "interface:":
            fail(
                f"{openai_config.relative_to(ROOT)}: "
                "must start with an interface mapping"
            )

        interface: dict[str, str] = {}
        for line_number, raw in enumerate(
            openai_lines, 1
        ):
            match = OPENAI_INTERFACE_RE.fullmatch(raw)
            if not match:
                continue
            key = match.group("key")
            if key in interface:
                fail(
                    f"{openai_config.relative_to(ROOT)}:{line_number}: "
                    f"duplicate interface key {key!r}"
                )
            interface[key] = match.group("value")

        for key in ("display_name", "short_description", "default_prompt"):
            if not interface.get(key, "").strip():
                fail(
                    f"{openai_config.relative_to(ROOT)}: missing quoted, "
                    f"non-empty interface.{key}"
                )

        display_name = interface.get("display_name", "")
        if display_name and not display_name.startswith("CX "):
            fail(
                f"{openai_config.relative_to(ROOT)}: interface.display_name "
                "must start with 'CX '"
            )

        for key in ("display_name", "short_description", "default_prompt"):
            if not interface.get(key, "").isascii():
                fail(
                    f"{openai_config.relative_to(ROOT)}: interface.{key} "
                    "must use ASCII English interface text"
                )

        short_description = interface.get("short_description", "")
        if short_description and not 25 <= len(short_description) <= 64:
            fail(
                f"{openai_config.relative_to(ROOT)}: "
                "interface.short_description must be 25-64 characters"
            )

        if f"${entry}" not in interface.get("default_prompt", ""):
            fail(
                f"{openai_config.relative_to(ROOT)}: interface.default_prompt "
                f"must mention ${entry}"
            )


def validate_agents() -> None:
    manifest_path = ROOT / "manifest" / "agents.txt"
    entries = read_manifest(manifest_path)
    agents_root = ROOT / "agents"
    discovered = sorted(path.name for path in agents_root.glob("*.toml"))

    if entries != discovered:
        fail(
            "agent manifest mismatch: "
            f"manifest={entries!r}, discovered={discovered!r}"
        )

    seen_names: set[str] = set()
    for entry in entries:
        path = agents_root / entry
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            fail(f"{path.relative_to(ROOT)}: invalid TOML: {exc}")
            continue

        for key in (
            "name",
            "description",
            "model",
            "developer_instructions",
        ):
            value = data.get(key)
            if not isinstance(value, str) or not value.strip():
                fail(f"{path.relative_to(ROOT)}: missing non-empty {key!r}")

        reasoning_effort = data.get("model_reasoning_effort")
        if reasoning_effort not in {
            "low",
            "medium",
            "high",
            "xhigh",
            "max",
            "ultra",
        }:
            fail(
                f"{path.relative_to(ROOT)}: unsupported "
                f"model_reasoning_effort {reasoning_effort!r}"
            )

        name = data.get("name")
        if isinstance(name, str):
            if name != path.stem:
                fail(
                    f"{path.relative_to(ROOT)}: name {name!r} "
                    f"must match filename stem {path.stem!r}"
                )
            if name in seen_names:
                fail(f"{path.relative_to(ROOT)}: duplicate agent name {name!r}")
            seen_names.add(name)

        sandbox_mode = data.get("sandbox_mode")
        if sandbox_mode not in {"read-only", "workspace-write"}:
            fail(
                f"{path.relative_to(ROOT)}: unsupported sandbox_mode "
                f"{sandbox_mode!r}"
            )


def validate_required_files() -> None:
    required = [
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.yml",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/workflows/validate.yml",
        "AGENTS.md",
        "CHANGELOG.md",
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "LICENSE",
        "README.md",
        "README_KR.md",
        "SECURITY.md",
        "SUPPORT.md",
        "THIRD_PARTY_NOTICES.md",
        "VERSION",
        "assets/highfloor-codex-banner.png",
        "docs/AGENT_CATALOG.md",
        "docs/ARCHITECTURE.md",
        "docs/INSTALLATION.md",
        "docs/RELEASING.md",
        "docs/WORKFLOWS.md",
        "install.sh",
        "scripts/check-release.sh",
        "scripts/check_release.py",
        "skills/CX_MIGRATION_MANIFEST.md",
        "skills/CX_SKILLS.md",
        "skills/CX_SKILL_CATALOG.md",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            fail(f"missing required file: {relative}")

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
        fail(f"VERSION is not semantic-version shaped: {version!r}")


def validate_repository_hygiene() -> None:
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts:
            continue
        if path.is_symlink():
            fail(f"symlink committed: {relative}")
            continue
        if path.name in {".DS_Store", "Thumbs.db", "__pycache__"}:
            fail(f"generated artifact committed: {relative}")
        if path.is_file() and path.suffix in {".pyc", ".pyo"}:
            fail(f"generated artifact committed: {relative}")

        if not path.is_file():
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        match = MACHINE_HOME_RE.search(content)
        if match:
            fail(
                f"machine-specific absolute home path in {relative}: "
                f"{match.group(0)!r}"
            )

        if path.suffix.lower() == ".md":
            if path.name != "README_KR.md" and HANGUL_RE.search(content):
                fail(f"Korean text outside README_KR.md: {relative}")
            validate_markdown_links(path, content)


def validate_markdown_links(path: Path, content: str) -> None:
    targets = LOCAL_LINK_RE.findall(content) + HTML_SRC_RE.findall(content)
    for target in targets:
        target = target.strip()
        if (
            not target
            or target.startswith(("#", "http://", "https://", "mailto:"))
            or "://" in target
        ):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        if target.startswith("~"):
            fail(f"{path.relative_to(ROOT)}: non-repository link {target!r}")
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            fail(f"{path.relative_to(ROOT)}: link escapes repository {target!r}")
            continue
        if not resolved.exists():
            fail(f"{path.relative_to(ROOT)}: broken local link {target!r}")


def main() -> int:
    validate_required_files()
    validate_skills()
    validate_agents()
    validate_repository_hygiene()

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Repository validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    skill_count = len((ROOT / "manifest" / "skills.txt").read_text().splitlines())
    agent_count = len((ROOT / "manifest" / "agents.txt").read_text().splitlines())
    print(f"Repository validation passed: {skill_count} skills, {agent_count} agents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
