#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
RESULTS = EVALS / "results"
SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
CONCLUSIONS = {"RETAIN", "REVISE", "ABSORB", "MERGE", "PRUNE", "NO_CHANGE"}
errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return None


def require_text(data: dict, key: str, path: Path) -> None:
    if not isinstance(data.get(key), str) or not data[key].strip():
        fail(f"{path.relative_to(ROOT)}: missing non-empty {key!r}")


def validate_run(data: object, key: str, path: Path) -> None:
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)}: {key} must be an object")
        return
    for field in ("snapshot", "model_profile", "reasoning_effort"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            fail(f"{path.relative_to(ROOT)}: {key}.{field} must be non-empty")
    for field in ("tools", "permissions"):
        value = data.get(field)
        if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
            fail(f"{path.relative_to(ROOT)}: {key}.{field} must be a string list")


def validate_result(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        return
    if data.get("schema_version") != "1":
        fail(f"{path.relative_to(ROOT)}: schema_version must be '1'")
    for key in ("campaign_id", "component", "hypothesis", "removal_condition"):
        require_text(data, key, path)
    for key in ("baseline", "treatment"):
        validate_run(data.get(key), key, path)
    task_set = data.get("task_set")
    if not isinstance(task_set, dict):
        fail(f"{path.relative_to(ROOT)}: task_set must be an object")
    else:
        if not isinstance(task_set.get("id"), str) or not task_set["id"].strip():
            fail(f"{path.relative_to(ROOT)}: task_set.id must be non-empty")
        if not isinstance(task_set.get("integrity_hash"), str) or not SHA_RE.fullmatch(task_set["integrity_hash"]):
            fail(f"{path.relative_to(ROOT)}: task_set.integrity_hash must be sha256:<64 lowercase hex>")
        if not isinstance(task_set.get("payloads_private_during_run"), bool):
            fail(f"{path.relative_to(ROOT)}: task_set.payloads_private_during_run must be boolean")
    ground_truth = data.get("ground_truth")
    if not isinstance(ground_truth, dict) or not isinstance(ground_truth.get("source"), str) or not ground_truth.get("source", "").strip():
        fail(f"{path.relative_to(ROOT)}: ground_truth.source must be non-empty")
    elif not isinstance(ground_truth.get("independent"), bool):
        fail(f"{path.relative_to(ROOT)}: ground_truth.independent must be boolean")
    hard_gates = data.get("hard_gates")
    if not isinstance(hard_gates, dict) or not isinstance(hard_gates.get("regressions"), int) or hard_gates.get("regressions", -1) < 0:
        fail(f"{path.relative_to(ROOT)}: hard_gates.regressions must be a non-negative integer")
    if not isinstance(data.get("metrics"), dict):
        fail(f"{path.relative_to(ROOT)}: metrics must be an object")
    if data.get("conclusion") not in CONCLUSIONS:
        fail(f"{path.relative_to(ROOT)}: unsupported conclusion {data.get('conclusion')!r}")
    report = data.get("report")
    if report is not None:
        if not isinstance(report, str) or not report.strip():
            fail(f"{path.relative_to(ROOT)}: report must be a non-empty relative path")
        else:
            resolved = (ROOT / report).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(f"{path.relative_to(ROOT)}: report path escapes repository")
            else:
                if not resolved.is_file():
                    fail(f"{path.relative_to(ROOT)}: report path does not exist: {report}")


def main() -> int:
    for rel in (
        "docs/EVALUATION.md",
        "evals/README.md",
        "evals/schemas/task.schema.json",
        "evals/schemas/result.schema.json",
        "evals/results/REPORT_TEMPLATE.md",
    ):
        if not (ROOT / rel).is_file():
            fail(f"missing evaluation file: {rel}")

    for schema in (EVALS / "schemas").glob("*.json"):
        load_json(schema)

    # Private future payloads should not be stored in obvious in-repository
    # hold-out locations. Public post-run examples may be published elsewhere
    # with an explicit report and rotated future hold-outs.
    for forbidden in ("tasks", "holdouts", "private"):
        if (EVALS / forbidden).exists():
            fail(f"evals/{forbidden}: keep unpublished held-out payloads outside the tested checkout")

    for path in sorted(RESULTS.glob("*.json")):
        validate_result(path)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Evaluation validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    count = len(list(RESULTS.glob("*.json")))
    print(f"Evaluation validation passed: {count} published result record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
