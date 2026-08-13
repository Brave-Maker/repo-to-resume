#!/usr/bin/env python3
"""Validate repo-to-resume manifest semantics without third-party packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


MODES = {
    "REAL_INTERNSHIP",
    "WEAK_INTERNSHIP",
    "SELF_PROJECT",
    "PROJECT_MIGRATION",
    "EXISTING_RESUME",
    "UNDERSTAND_ONLY",
}
QUALITY_STATUSES = {
    "BLOCKED",
    "TRAINING_REQUIRED",
    "REVIEW_REQUIRED",
    "INTERVIEW_READY",
}
ARTIFACT_KEYS = {
    "project_analysis",
    "business_chains",
    "contribution_map",
    "enhancement_plan",
    "resume",
    "resume_clean",
    "claim_grill_report",
    "learning_path",
    "learning_interactive",
    "interview_scripts",
    "interview_report",
    "quality_gate_report",
}
UNDERSTAND_REQUIRED = {
    "project_analysis",
    "business_chains",
    "learning_path",
    "quality_gate_report",
}
UNDERSTAND_FORBIDDEN = {
    "contribution_map",
    "enhancement_plan",
    "resume",
    "resume_clean",
    "claim_grill_report",
    "interview_scripts",
    "interview_report",
}
FULL_REQUIRED = {
    "project_analysis",
    "business_chains",
    "contribution_map",
    "resume",
    "claim_grill_report",
    "learning_path",
    "interview_scripts",
    "quality_gate_report",
}
TOP_LEVEL_REQUIRED = {
    "schema_version",
    "mode",
    "current_artifacts",
    "code_mutation",
    "project",
    "business_chains",
    "contributions",
    "enhancement_tasks",
    "claims",
    "evidence",
    "grill_results",
    "learning_gaps",
    "risk_flags",
    "quality_status",
}
TOP_LEVEL_ALLOWED = TOP_LEVEL_REQUIRED | {"auto_confirmed"}
DEFAULT_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "references" / "evidence-manifest.schema.json"


def _json_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def _resolve_ref(root_schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported external schema reference: {ref}")
    current: Any = root_schema
    for raw_part in ref[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        current = current[part]
    if not isinstance(current, dict):
        raise ValueError(f"schema reference is not an object: {ref}")
    return current


def _validate_schema_node(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str,
) -> list[str]:
    if "$ref" in schema:
        return _validate_schema_node(value, _resolve_ref(root_schema, schema["$ref"]), root_schema, path)

    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type and not _json_type_matches(value, expected_type):
        return [f"{path} must be {expected_type}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path} must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path} must be one of {schema['enum']}")

    for child in schema.get("allOf", []):
        errors.extend(_validate_schema_node(value, child, root_schema, path))
    if "if" in schema:
        condition_errors = _validate_schema_node(value, schema["if"], root_schema, path)
        branch = schema.get("then") if not condition_errors else schema.get("else")
        if branch:
            errors.extend(_validate_schema_node(value, branch, root_schema, path))

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}.{key} is required")
        properties = schema.get("properties", {})
        for key, item in value.items():
            if key in properties:
                errors.extend(_validate_schema_node(item, properties[key], root_schema, f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}.{key} is not allowed")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path} must contain at least {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path} must contain at most {schema['maxItems']} items")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in value]
            if len(encoded) != len(set(encoded)):
                errors.append(f"{path} must contain unique items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(_validate_schema_node(item, item_schema, root_schema, f"{path}[{index}]"))

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path} is shorter than {schema['minLength']} characters")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append(f"{path} does not match {schema['pattern']}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path} must be >= {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path} must be <= {schema['maximum']}")
    return errors


def validate_structure(data: dict[str, Any], schema_path: Path = DEFAULT_SCHEMA_PATH) -> list[str]:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"schema read failed: {exc}"]
    if not isinstance(schema, dict):
        return ["schema root must be an object"]
    try:
        return _validate_schema_node(data, schema, schema, "$")
    except (KeyError, TypeError, ValueError) as exc:
        return [f"schema evaluation failed: {exc}"]


def _duplicates(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def _objects(data: dict[str, Any], key: str, errors: list[str]) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list):
        errors.append(f"{key} must be an array")
        return []
    if not all(isinstance(item, dict) for item in value):
        errors.append(f"{key} must contain only objects")
        return []
    return value


def _ids(items: list[dict[str, Any]], key: str, errors: list[str]) -> set[str]:
    values = [item.get("id") for item in items]
    if not all(isinstance(value, str) and value for value in values):
        errors.append(f"{key} contains an object without a non-empty id")
    string_values = [value for value in values if isinstance(value, str)]
    duplicates = _duplicates(string_values)
    if duplicates:
        errors.append(f"{key} contains duplicate ids: {', '.join(sorted(duplicates))}")
    return set(string_values)


def _check_references(
    items: list[dict[str, Any]],
    field: str,
    targets: set[str],
    label: str,
    errors: list[str],
) -> None:
    for item in items:
        value = item.get(field)
        if value not in targets:
            errors.append(f"{label} {item.get('id', '<unknown>')} has dangling {field}: {value}")


def _safe_artifact_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    has_drive = re.match(r"^[A-Za-z]:", normalized) is not None
    return (
        not path.is_absolute()
        and not has_drive
        and not normalized.startswith("//")
        and ".." not in path.parts
        and bool(path.parts)
    )


def validate_manifest(
    data: dict[str, Any],
    analysis_dir: Path | None = None,
    require_artifacts: bool = False,
) -> list[str]:
    errors: list[str] = validate_structure(data)
    missing = sorted(TOP_LEVEL_REQUIRED - data.keys())
    if missing:
        errors.append(f"missing top-level fields: {', '.join(missing)}")
    unknown = sorted(set(data) - TOP_LEVEL_ALLOWED)
    if unknown:
        errors.append(f"unknown top-level fields: {', '.join(unknown)}")

    if data.get("schema_version") != "1.1":
        errors.append("schema_version must equal 1.1")
    mode = data.get("mode")
    if mode not in MODES:
        errors.append(f"invalid mode: {mode}")
    if data.get("quality_status") not in QUALITY_STATUSES:
        errors.append(f"invalid quality_status: {data.get('quality_status')}")

    artifacts = data.get("current_artifacts")
    if not isinstance(artifacts, dict):
        errors.append("current_artifacts must be an object")
        artifacts = {}
    unknown_artifacts = sorted(set(artifacts) - ARTIFACT_KEYS)
    if unknown_artifacts:
        errors.append(f"unknown current_artifacts keys: {', '.join(unknown_artifacts)}")
    for key, value in artifacts.items():
        if not isinstance(value, str) or not _safe_artifact_path(value):
            errors.append(f"current_artifacts.{key} must be a safe relative path")
            continue
        if analysis_dir is not None and not (analysis_dir / value).is_file():
            errors.append(f"current_artifacts.{key} points to a missing file: {value}")

    if mode == "UNDERSTAND_ONLY":
        forbidden = sorted(UNDERSTAND_FORBIDDEN & set(artifacts))
        if forbidden:
            errors.append(f"UNDERSTAND_ONLY contains forbidden artifacts: {', '.join(forbidden)}")
        required = UNDERSTAND_REQUIRED
    else:
        required = FULL_REQUIRED
    if require_artifacts:
        missing_artifacts = sorted(required - set(artifacts))
        if missing_artifacts:
            errors.append(f"missing required current artifacts: {', '.join(missing_artifacts)}")

    mutation = data.get("code_mutation")
    if not isinstance(mutation, dict):
        errors.append("code_mutation must be an object")
        mutation = {}
    authorized = mutation.get("authorized")
    scope = mutation.get("scope")
    if not isinstance(authorized, bool):
        errors.append("code_mutation.authorized must be boolean")
    if not isinstance(scope, list) or not all(isinstance(item, str) and item for item in scope):
        errors.append("code_mutation.scope must be an array of non-empty strings")
        scope = []
    if authorized:
        if not scope:
            errors.append("authorized code mutation requires at least one scope")
        if not mutation.get("reason") or not mutation.get("authorized_at"):
            errors.append("authorized code mutation requires reason and authorized_at")
    elif scope:
        errors.append("unauthorized code mutation must have an empty scope")

    chains = _objects(data, "business_chains", errors)
    contributions = _objects(data, "contributions", errors)
    tasks = _objects(data, "enhancement_tasks", errors)
    claims = _objects(data, "claims", errors)
    evidence = _objects(data, "evidence", errors)
    grill_results = _objects(data, "grill_results", errors)
    learning_gaps = _objects(data, "learning_gaps", errors)
    risk_flags = _objects(data, "risk_flags", errors)

    chain_ids = _ids(chains, "business_chains", errors)
    _ids(contributions, "contributions", errors)
    task_ids = _ids(tasks, "enhancement_tasks", errors)
    claim_ids = _ids(claims, "claims", errors)
    evidence_ids = _ids(evidence, "evidence", errors)

    _check_references(contributions, "chain_id", chain_ids, "contribution", errors)
    _check_references(tasks, "chain_id", chain_ids, "enhancement task", errors)
    _check_references(claims, "chain_id", chain_ids, "claim", errors)
    _check_references(grill_results, "claim_id", claim_ids, "grill result", errors)
    _check_references(learning_gaps, "claim_id", claim_ids, "learning gap", errors)

    for task in tasks:
        for claim_id in task.get("claim_ids", []):
            if claim_id not in claim_ids:
                errors.append(f"enhancement task {task.get('id')} has dangling claim_id: {claim_id}")
        if task.get("mode") == "IMPLEMENTED" and not authorized:
            errors.append(f"enhancement task {task.get('id')} requires code mutation authorization")

    for contribution in contributions:
        linked = contribution.get("evidence_ids", [])
        dangling = sorted(set(linked) - evidence_ids) if isinstance(linked, list) else []
        if dangling:
            errors.append(
                f"contribution {contribution.get('id')} has dangling evidence_ids: {', '.join(dangling)}"
            )

    for claim in claims:
        claim_id = claim.get("id", "<unknown>")
        linked = claim.get("evidence_ids")
        if not isinstance(linked, list):
            errors.append(f"claim {claim_id} evidence_ids must be an array")
            continue
        dangling = sorted(set(linked) - evidence_ids)
        if dangling:
            errors.append(f"claim {claim_id} has dangling evidence_ids: {', '.join(dangling)}")
        if claim.get("status") == "READY" and not linked:
            errors.append(f"READY claim {claim_id} must have evidence")
        repair_task = claim.get("repair_task_id")
        if repair_task and repair_task not in task_ids:
            errors.append(f"claim {claim_id} has dangling repair_task_id: {repair_task}")

    for flag in risk_flags:
        claim_id = flag.get("claim_id")
        if claim_id is not None and claim_id not in claim_ids:
            errors.append(f"risk flag has dangling claim_id: {claim_id}")

    grill_by_claim = {item.get("claim_id"): item for item in grill_results}
    if data.get("quality_status") == "INTERVIEW_READY":
        if not any(claim.get("is_core") for claim in claims):
            errors.append("INTERVIEW_READY requires at least one core claim")
        for claim in claims:
            if not claim.get("is_core"):
                continue
            if claim.get("status") != "READY":
                errors.append(f"INTERVIEW_READY core claim {claim.get('id')} must have status READY")
            result = grill_by_claim.get(claim.get("id"))
            if not result or result.get("status") not in {"YELLOW", "GREEN"}:
                errors.append(f"INTERVIEW_READY core claim {claim.get('id')} lacks a passing grill result")
            if claim.get("risk") == "HIGH" and (not result or result.get("rounds", 0) < 2):
                errors.append(f"INTERVIEW_READY high-risk claim {claim.get('id')} needs two grill rounds")
            if claim.get("source_type") in {"BORROWED_CONTEXT", "NARRATIVE_FILL"}:
                completed = any(
                    claim.get("id") in task.get("claim_ids", [])
                    and task.get("status") == "COMPLETED"
                    and task.get("mode") in {"IMPLEMENTED", "REPRODUCED", "DESIGNED"}
                    for task in tasks
                )
                if not completed:
                    errors.append(
                        f"INTERVIEW_READY high-risk claim {claim.get('id')} lacks a completed validation task"
                    )

    core_red = any(
        claim.get("is_core") and claim.get("grill_status") == "RED" for claim in claims
    )
    if core_red and data.get("quality_status") != "BLOCKED":
        errors.append("a core RED claim requires quality_status BLOCKED")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--analysis-dir", type=Path)
    parser.add_argument("--require-artifacts", action="store_true")
    args = parser.parse_args()

    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Manifest read failed: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("Manifest root must be an object", file=sys.stderr)
        return 2

    errors = validate_manifest(data, args.analysis_dir, args.require_artifacts)
    if errors:
        print(f"Manifest validation failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Manifest validation passed: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
