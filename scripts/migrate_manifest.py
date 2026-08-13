#!/usr/bin/env python3
"""Migrate a repo-to-resume manifest from schema 1.0 to 1.1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from validate_manifest import validate_manifest


def _artifact_candidates(manifest: dict[str, Any]) -> dict[str, str]:
    artifacts = manifest.get("current_artifacts")
    return artifacts if isinstance(artifacts, dict) else {}


def migrate(manifest: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    if manifest.get("schema_version") != "1.0":
        raise ValueError("only schema_version 1.0 can be migrated")

    warnings: list[str] = []
    migrated = json.loads(json.dumps(manifest, ensure_ascii=False))
    migrated["schema_version"] = "1.1"
    migrated["current_artifacts"] = _artifact_candidates(migrated)
    migrated["code_mutation"] = {"authorized": False, "scope": []}

    project = migrated.get("project")
    if not isinstance(project, dict):
        project = {}
        migrated["project"] = project
    if not project.get("name"):
        project["name"] = "unknown-project"
        warnings.append("project.name was missing and needs user confirmation")

    for chain in migrated.get("business_chains", []):
        chain.setdefault("code_locations", [])
        if not chain.get("consumer"):
            chain["consumer"] = "待确认"
            warnings.append(f"{chain.get('id', 'chain')}.consumer needs confirmation")

    for task in migrated.get("enhancement_tasks", []):
        task.setdefault("solution_options", ["待补充"])
        task.setdefault("execution_steps", ["待补充"])
        task.setdefault("failure_injection", ["待补充"])
        task.setdefault("validation_methods", ["待补充"])
        task.setdefault("completion_evidence", [])
        task.setdefault("interview_gate", ["待补充"])

    for claim in migrated.get("claims", []):
        claim.setdefault("is_core", True)
        normalized_ids = []
        for evidence_id in claim.get("evidence_ids", []):
            match = str(evidence_id).split("-")[-1]
            normalized_ids.append(f"EVIDENCE-{match}" if match.isdigit() else str(evidence_id))
        claim["evidence_ids"] = normalized_ids

    for evidence in migrated.get("evidence", []):
        evidence_id = str(evidence.get("id", ""))
        suffix = evidence_id.split("-")[-1]
        if suffix.isdigit():
            evidence["id"] = f"EVIDENCE-{suffix}"

    migrated.setdefault("grill_results", [])
    migrated.setdefault("learning_gaps", [])
    migrated.setdefault("risk_flags", [])
    migrated.setdefault("quality_status", "TRAINING_REQUIRED")
    return migrated, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        source = json.loads(args.manifest.read_text(encoding="utf-8"))
        migrated, warnings = migrate(source)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Migration failed: {exc}", file=sys.stderr)
        return 2

    errors = validate_manifest(migrated)
    if errors:
        print("Migration produced a manifest that still needs repair:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    args.output.write_text(json.dumps(migrated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest migrated to: {args.output}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
