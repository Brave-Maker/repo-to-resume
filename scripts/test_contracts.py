#!/usr/bin/env python3
"""Negative contract tests for manifest validation and artifact routing."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from run_evals import _artifact_text
from validate_manifest import validate_manifest


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals" / "fixtures"


def load_scenario(number: int) -> dict:
    return json.loads((FIXTURES / f"scenario-{number}.json").read_text(encoding="utf-8"))["manifest"]


def expect_error(name: str, manifest: dict, needle: str) -> None:
    errors = validate_manifest(manifest)
    if not any(needle in error for error in errors):
        raise AssertionError(f"{name}: expected error containing {needle!r}, got {errors}")


def main() -> int:
    migration = load_scenario(4)
    dangling = copy.deepcopy(migration)
    dangling["claims"][0]["evidence_ids"] = ["EVIDENCE-999"]
    expect_error("dangling evidence", dangling, "dangling evidence_ids")

    empty_ready = copy.deepcopy(migration)
    empty_ready["claims"][0]["status"] = "READY"
    empty_ready["claims"][0]["evidence_ids"] = []
    expect_error("ready without evidence", empty_ready, "READY claim")

    unauthorized = copy.deepcopy(migration)
    unauthorized["enhancement_tasks"][0]["mode"] = "IMPLEMENTED"
    unauthorized["enhancement_tasks"][0]["status"] = "IN_PROGRESS"
    expect_error("unauthorized mutation", unauthorized, "code mutation authorization")

    understand = load_scenario(6)
    forbidden = copy.deepcopy(understand)
    forbidden["current_artifacts"]["resume"] = "resume.md"
    expect_error("understand-only resume", forbidden, "forbidden artifacts")

    stale = copy.deepcopy(migration)
    stale["current_artifacts"]["resume"] = "resume-v2.md"
    with tempfile.TemporaryDirectory(prefix="repo-to-resume-contract-") as temp_root:
        errors = validate_manifest(stale, Path(temp_root), require_artifacts=True)
    if not any("resume-v2.md" in error and "missing file" in error for error in errors):
        raise AssertionError(f"stale artifact pointer was accepted: {errors}")

    unsafe = copy.deepcopy(migration)
    unsafe["current_artifacts"]["resume"] = "../resume.md"
    expect_error("artifact traversal", unsafe, "safe relative path")

    drive_path = copy.deepcopy(migration)
    drive_path["current_artifacts"]["resume"] = "C:/outside/resume.md"
    expect_error("artifact drive path", drive_path, "safe relative path")

    unknown_field = copy.deepcopy(migration)
    unknown_field["unexpected"] = True
    expect_error("unknown top-level field", unknown_field, "not allowed")

    malformed_task = copy.deepcopy(migration)
    del malformed_task["enhancement_tasks"][0]["validation_methods"]
    expect_error("missing task field", malformed_task, "validation_methods is required")

    dangling_contribution = copy.deepcopy(migration)
    dangling_contribution["contributions"][0]["evidence_ids"] = ["EVIDENCE-999"]
    expect_error("dangling contribution evidence", dangling_contribution, "contribution CONTRIBUTION-001")

    false_ready = copy.deepcopy(migration)
    false_ready["quality_status"] = "INTERVIEW_READY"
    expect_error("interview ready claim state", false_ready, "must have status READY")

    routed = copy.deepcopy(migration)
    routed["current_artifacts"]["resume"] = "resume-v1.md"
    with tempfile.TemporaryDirectory(prefix="repo-to-resume-routing-") as temp_root:
        target = Path(temp_root)
        (target / "resume.md").write_text("OLD", encoding="utf-8")
        (target / "resume-v1.md").write_text("CURRENT", encoding="utf-8")
        selected = _artifact_text(target, routed, "resume")
    if selected != "CURRENT":
        raise AssertionError(f"artifact routing selected stale content: {selected!r}")

    core_red = copy.deepcopy(migration)
    core_red["claims"][0]["grill_status"] = "RED"
    core_red["quality_status"] = "TRAINING_REQUIRED"
    expect_error("core red status", core_red, "quality_status BLOCKED")

    print("Contract tests: 13 passed, 0 failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
