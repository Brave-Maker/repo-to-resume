#!/usr/bin/env python3
"""Execute repo-to-resume fixture assertions and manifest contract checks."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path
from typing import Any

from validate_manifest import validate_manifest


ROOT = Path(__file__).resolve().parents[1]
EVALS_PATH = ROOT / "evals" / "evals.json"
FIXTURES_DIR = ROOT / "evals" / "fixtures"
LAYERS = {"事实确认", "个人角色", "技术实现", "方案对比", "数据与验证", "边界与复盘"}
class EvalFailure(Exception):
    pass


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _materialize(fixture: dict[str, Any], target: Path) -> dict[str, Any]:
    manifest = fixture["manifest"]
    for relative_path, content in fixture.get("files", {}).items():
        path = target / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    (target / "evidence-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def _artifact_path(target: Path, manifest: dict[str, Any], key: str) -> Path | None:
    value = manifest.get("current_artifacts", {}).get(key)
    return target / value if isinstance(value, str) else None


def _artifact_text(target: Path, manifest: dict[str, Any], key: str) -> str:
    path = _artifact_path(target, manifest, key)
    return path.read_text(encoding="utf-8") if path and path.is_file() else ""


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _check_assertion(
    check: str,
    target: Path,
    manifest: dict[str, Any],
) -> tuple[bool, str]:
    op, _, argument = check.partition(":")
    artifacts = manifest.get("current_artifacts", {})
    claims = manifest.get("claims", [])
    tasks = manifest.get("enhancement_tasks", [])
    grills = manifest.get("grill_results", [])

    if op == "manifest.mode_equals":
        return manifest.get("mode") == argument, f"mode={manifest.get('mode')}"
    if op == "files_exist":
        missing = [name for name in _split_csv(argument) if not (target / name).is_file()]
        return not missing, f"missing={missing}"
    if op == "files_not_exist":
        present = [name for name in _split_csv(argument) if (target / name).exists()]
        return not present, f"present={present}"
    if op == "file_exists":
        return (target / argument).is_file(), argument
    if op == "contribution_has_source":
        found = any(item.get("source_type") == argument for item in manifest.get("contributions", []))
        return found, argument
    if op == "resume_role_matches_manifest":
        text = _artifact_text(target, manifest, "resume")
        found = all(
            not claim.get("resume_text") or claim.get("resume_text") in text for claim in claims
        )
        return found, "resume_text mapping"
    if op == "all_resume_bullets_have_claim_id":
        text = _artifact_text(target, manifest, "resume")
        indexes = set(re.findall(r"CLAIM-[0-9]{3,}", text))
        expected = {claim["id"] for claim in claims if claim.get("resume_text")}
        return expected <= indexes and bool(expected), f"expected={sorted(expected)}, found={sorted(indexes)}"
    if op == "grill_has_layers":
        required = set(_split_csv(argument))
        found = set().union(*(set(item.get("layers", [])) for item in grills)) if grills else set()
        return required <= found, f"missing={sorted(required - found)}"
    if op == "business_chain_has_consumer":
        found = bool(manifest.get("business_chains")) and all(
            item.get("consumer") for item in manifest["business_chains"]
        )
        return found, "consumer"
    if op == "enhancement_task_count_between":
        low, high = map(int, _split_csv(argument))
        return low <= len(tasks) <= high, f"count={len(tasks)}"
    if op == "all_tasks_have":
        field_map = {
            "方案选项": "solution_options",
            "执行步骤": "execution_steps",
            "失败注入": "failure_injection",
            "验证方法": "validation_methods",
            "完成证据": "completion_evidence",
            "面试门禁": "interview_gate",
        }
        required_fields = [field_map[name] for name in _split_csv(argument)]
        missing = [
            f"{task.get('id')}:{field}"
            for task in tasks
            for field in required_fields
            if field not in task or not isinstance(task[field], list)
        ]
        return not missing and bool(tasks), f"missing={missing}"
    if op == "planned_tasks_not_marked_implemented":
        invalid = [
            task.get("id") for task in tasks
            if task.get("status") == "PLANNED" and task.get("mode") == "IMPLEMENTED"
        ]
        return not invalid, f"invalid={invalid}"
    if op == "high_risk_claims_have_grill_result":
        grilled = {item.get("claim_id") for item in grills}
        missing = [item["id"] for item in claims if item.get("risk") == "HIGH" and item["id"] not in grilled]
        return not missing, f"missing={missing}"
    if op == "resume_does_not_require_company":
        text = _artifact_text(target, manifest, "resume")
        bad = re.search(r"(?:公司背景|某公司|一家公司)", text)
        return bad is None, bad.group(0) if bad else ""
    if op == "all_enhancements_have_chain_id":
        chain_ids = {item["id"] for item in manifest.get("business_chains", [])}
        return bool(tasks) and all(task.get("chain_id") in chain_ids for task in tasks), "chain references"
    if op == "no_component_based_performance_estimates":
        text = "\n".join(fixture_text(target))
        bad = re.search(r"(?:Redis|线程池|消息队列|MQ|索引).{0,20}(?:提升|降低)\s*\d+%", text, re.I)
        return bad is None, bad.group(0) if bad else ""
    if op == "scripts_have_all_layers":
        text = _artifact_text(target, manifest, "interview_scripts")
        required = {"15秒", "30秒", "2分钟", "深挖"}
        missing = [item for item in required if item not in text]
        return not missing, f"missing={missing}"
    if op == "learning_path_has_claim_gaps":
        text = _artifact_text(target, manifest, "learning_path")
        expected = {item.get("claim_id") for item in manifest.get("learning_gaps", [])}
        return bool(expected) and all(item in text for item in expected), f"claims={sorted(expected)}"
    if op == "migration_focus_chain_count_between":
        low, high = map(int, _split_csv(argument))
        count = len(manifest.get("business_chains", []))
        return low <= count <= high, f"count={count}"
    if op == "claims_source_in":
        allowed = set(_split_csv(argument))
        return bool(claims) and all(item.get("source_type") in allowed for item in claims), f"allowed={sorted(allowed)}"
    if op == "enhancement_mode_in":
        allowed = set(_split_csv(argument))
        return bool(tasks) and all(item.get("mode") in allowed for item in tasks), f"allowed={sorted(allowed)}"
    if op == "high_risk_gate_enforced":
        by_claim = {item.get("claim_id"): item for item in grills}
        failures = []
        for claim in claims:
            if claim.get("risk") != "HIGH":
                continue
            result = by_claim.get(claim["id"])
            if not result or result.get("rounds", 0) < 2 or not LAYERS <= set(result.get("layers", [])):
                failures.append(claim["id"])
        return not failures, f"failed={failures}"
    if op == "quality_status_respects_grill":
        failing = any(item.get("status") in {"RED", "ORANGE"} for item in grills)
        return not (failing and manifest.get("quality_status") == "INTERVIEW_READY"), manifest.get("quality_status")
    if op == "risk_flags_include":
        required = set(_split_csv(argument))
        found = {item.get("type") for item in manifest.get("risk_flags", [])}
        return required <= found, f"missing={sorted(required - found)}"
    if op == "unsupported_number_not_low_risk":
        numeric_claims = [item for item in claims if re.search(r"\d", item.get("text", ""))]
        return bool(numeric_claims) and all(item.get("risk") != "LOW" for item in numeric_claims), "numeric risk"
    if op == "override_keeps_risk_and_training":
        overridden = [item for item in claims if item.get("override")]
        ok = bool(overridden) and all(item.get("risk") == "HIGH" for item in overridden)
        ok = ok and manifest.get("quality_status") != "INTERVIEW_READY"
        return ok, manifest.get("quality_status")
    if op == "red_claim_has_repair_task":
        task_ids = {item["id"] for item in tasks}
        red = [item for item in claims if item.get("grill_status") == "RED"]
        return bool(red) and all(item.get("repair_task_id") in task_ids for item in red), "repair tasks"
    if op == "quality_status_respects_evidence":
        risky = any(item.get("risk") in {"HIGH", "BLOCKED"} or not item.get("evidence_ids") for item in claims)
        return not (risky and manifest.get("quality_status") == "INTERVIEW_READY"), manifest.get("quality_status")
    if op == "scope_equals":
        return manifest.get("project", {}).get("scan_scope") == argument, str(manifest.get("project", {}).get("scan_scope"))
    if op == "excluded":
        required = set(_split_csv(argument))
        found = set(manifest.get("project", {}).get("excluded_paths", []))
        return required <= found, f"missing={sorted(required - found)}"
    if op == "learning_path_generated_without_resume":
        return bool(_artifact_text(target, manifest, "learning_path")) and "resume" not in artifacts, "artifact routing"
    if op == "all_skill_references_exist":
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        references = re.findall(r"references/[a-z0-9.-]+", skill_text)
        missing = [item for item in references if not (ROOT / item).is_file()]
        return not missing, f"missing={missing}"
    if op == "single_manifest_contract":
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        return "current_artifacts" in skill_text and "evidence-manifest.json" in skill_text, "manifest contract"
    if op == "version_existing_outputs":
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        return "-v1" in skill_text and "current_artifacts" in skill_text, "version contract"
    if op == "failure_modes_encoded":
        return "## 失败与恢复" in (ROOT / "SKILL.md").read_text(encoding="utf-8"), "failure table"
    if op == "explicit_checkpoints_exist":
        return (ROOT / "SKILL.md").read_text(encoding="utf-8").count("CHECKPOINT") >= 5, "checkpoint count"
    if op == "blacklist_exists":
        return "## 反例黑名单" in (ROOT / "SKILL.md").read_text(encoding="utf-8"), "blacklist"
    if op == "runtime_neutral":
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        pattern = re.compile(r"Claude Code skill|Cursor only|~/\.claude/skills/[a-z]|/plugin install\b", re.I)
        return pattern.search(text) is None, "runtime scan"
    if op == "no_fabricated_interview_scores":
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        return "用户未实际回答时，不伪造面试得分" in text, "score policy"
    if op == "current_artifact_routing_enforced":
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        tests = (ROOT / "scripts" / "test_contracts.py").read_text(encoding="utf-8")
        ok = "current_artifacts" in text and "artifact routing selected stale content" in tests
        return ok, "current artifact pointer contract"
    if op == "code_mutation_gate_enforced":
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        ok = "CHECKPOINT · CODE MUTATION" in text and "code_mutation.authorized=true" in text
        return ok, "code mutation checkpoint"
    if op == "manifest_semantic_validator_exists":
        validator = ROOT / "scripts" / "validate_manifest.py"
        tests = ROOT / "scripts" / "test_contracts.py"
        return validator.is_file() and tests.is_file(), "semantic validation scripts"
    if op == "chinese_output_contract":
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        resume = (ROOT / "references" / "star-resume-generator.md").read_text(encoding="utf-8")
        output = (ROOT / "references" / "output-contracts.md").read_text(encoding="utf-8")
        required = [
            "用户明确指定 > 用户当前使用的语言 > 默认中文",
            "大语言模型（LLM）",
            "`Agent` | 智能体",
            "代码标识符首次出现时补充中文职责",
            "用户明确要求英文时",
            "简历要点拷打完成",
        ]
        combined = "\n".join((skill, resume, output))
        missing = [item for item in required if item not in combined]
        forbidden_templates = ["> Bullet 拷打完成", "条 Action", "| Ready | Needs training"]
        found = [item for item in forbidden_templates if item in output]
        return not missing and not found, f"missing={missing}, forbidden={found}"
    if op == "code_first_value_selection_contract":
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        engine = (ROOT / "references" / "code-analysis-engine.md").read_text(encoding="utf-8")
        chains = (ROOT / "references" / "business-chain-extractor.md").read_text(encoding="utf-8")
        mapper = (ROOT / "references" / "contribution-mapper.md").read_text(encoding="utf-8")
        resume = (ROOT / "references" / "star-resume-generator.md").read_text(encoding="utf-8")
        prompts = (ROOT / "test-prompts.json").read_text(encoding="utf-8")
        combined = "\n".join((skill, engine, chains, mapper, resume))
        required = [
            "Git 历史仅用于核对作者、时间、改动边界和演进顺序",
            "Git 元数据只能追加作者/时间/演进信息，不得提高节点价值分",
            "至少 `max(6, 2N)` 个跨链路候选",
            "存在更高分且准入合格的候选时必须替换",
            "后续简历排序与替换的唯一价值分",
            "唯一权威排序值为贡献映射阶段产生的 `candidate_value_score`",
            "岗位相关性已经计入 `candidate_value_score`，不得再次作为例外",
            "不得把准入条件与价值分混算",
            "commit hash、提交次数、改动文件数、增删行数、commit 大小、ADR/设计文档数量",
            "候选池只来自一个提交/功能",
        ]
        missing = [item for item in required if item not in combined]
        prompt_ok = all(item in prompts for item in ("QualityFlow", "7fd13a7", "增加 8422 行", "替换"))
        return not missing and prompt_ok, f"missing={missing}, qualityflow_prompt={prompt_ok}"
    raise EvalFailure(f"unsupported assertion operator: {op}")


def fixture_text(target: Path) -> list[str]:
    return [path.read_text(encoding="utf-8") for path in target.rglob("*") if path.is_file()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", type=int, action="append")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    spec = _load_json(EVALS_PATH)
    scenarios = spec["evals"]
    if args.scenario:
        selected = set(args.scenario)
        scenarios = [item for item in scenarios if item["id"] in selected]

    passed = 0
    failed = 0
    with tempfile.TemporaryDirectory(prefix="repo-to-resume-evals-") as temp_root:
        root = Path(temp_root)
        for scenario in scenarios:
            fixture_path = FIXTURES_DIR / f"scenario-{scenario['id']}.json"
            fixture = _load_json(fixture_path)
            target = root / f"scenario-{scenario['id']}"
            target.mkdir()
            manifest = _materialize(fixture, target)

            semantic_errors = validate_manifest(manifest, target, require_artifacts=True)
            if semantic_errors:
                failed += 1
                print(f"FAIL scenario {scenario['id']} semantic validation")
                for error in semantic_errors:
                    print(f"  - {error}")
            else:
                passed += 1
                if args.verbose:
                    print(f"PASS scenario {scenario['id']} semantic validation")

            for assertion in scenario["assertions"]:
                try:
                    ok, detail = _check_assertion(assertion["check"], target, manifest)
                except EvalFailure as exc:
                    ok, detail = False, str(exc)
                if ok:
                    passed += 1
                    if args.verbose:
                        print(f"PASS {assertion['id']} {assertion['text']}")
                else:
                    failed += 1
                    print(f"FAIL {assertion['id']} {assertion['text']}: {detail}")

        representative = scenarios[0] if scenarios else None
        if representative:
            fixture = _load_json(FIXTURES_DIR / f"scenario-{representative['id']}.json")
            target = root / f"scenario-{representative['id']}"
            manifest = fixture["manifest"]
            for assertion in spec["global_assertions"]:
                try:
                    ok, detail = _check_assertion(assertion["check"], target, manifest)
                except EvalFailure as exc:
                    ok, detail = False, str(exc)
                if ok:
                    passed += 1
                    if args.verbose:
                        print(f"PASS {assertion['id']} {assertion['text']}")
                else:
                    failed += 1
                    print(f"FAIL {assertion['id']} {assertion['text']}: {detail}")

    print(f"Eval assertions: {passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
