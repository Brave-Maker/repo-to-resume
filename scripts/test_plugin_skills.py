#!/usr/bin/env python3
"""Deterministic checks for the multi-skill plugin surface."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED = {
    "claim-grill",
    "contribution-mapper",
    "experience-enhancer",
    "interview-script",
    "mock-interview",
    "project-analyzer",
    "project-learning",
    "resume-auditor",
    "resume-pipeline",
    "resume-writer",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def frontmatter(text: str, path: Path) -> tuple[str, str]:
    match = re.match(
        r"\A---\r?\nname:\s*([^\r\n]+)\r?\ndescription:\s*([^\r\n]+)\r?\n---",
        text,
    )
    if not match:
        fail(f"invalid frontmatter: {path}")
    return match.group(1).strip(), match.group(2).strip()


def main() -> int:
    manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if manifest.get("name") != "repo-to-resume" or manifest.get("skills") != "./skills/":
        fail("plugin manifest does not expose ./skills/")

    folders = {path.name for path in SKILLS.iterdir() if path.is_dir()}
    if folders != EXPECTED:
        fail(f"skill folders differ: missing={sorted(EXPECTED - folders)}, extra={sorted(folders - EXPECTED)}")

    seen_names: set[str] = set()
    for folder in sorted(folders):
        skill_dir = SKILLS / folder
        skill_path = skill_dir / "SKILL.md"
        agent_path = skill_dir / "agents" / "openai.yaml"
        prompts_path = skill_dir / "test-prompts.json"
        for required in (skill_path, agent_path, prompts_path):
            if not required.is_file():
                fail(f"missing required skill resource: {required}")

        name, description = frontmatter(skill_path.read_text(encoding="utf-8"), skill_path)
        if name != folder:
            fail(f"folder/frontmatter mismatch: {folder} != {name}")
        if name in seen_names:
            fail(f"duplicate skill name: {name}")
        seen_names.add(name)
        if not description or len(description) > 1024:
            fail(f"invalid description length: {name}")

        agent_text = agent_path.read_text(encoding="utf-8")
        if f"${name}" not in agent_text:
            fail(f"default prompt does not invoke ${name}: {agent_path}")

        prompts = json.loads(prompts_path.read_text(encoding="utf-8"))
        if not isinstance(prompts, list) or len(prompts) < 3:
            fail(f"{name} must have at least three test prompts")
        ids = [item.get("id") for item in prompts if isinstance(item, dict)]
        if len(ids) != len(prompts) or len(set(ids)) != len(ids):
            fail(f"{name} test prompt ids must be present and unique")
        for item in prompts:
            if not item.get("prompt") or not item.get("expected"):
                fail(f"{name} has an incomplete test prompt")

    orchestrator = (SKILLS / "resume-pipeline" / "SKILL.md").read_text(encoding="utf-8")
    for name in sorted(EXPECTED - {"resume-pipeline"}):
        if f"`${name}`" not in orchestrator and f"`${name}`" not in orchestrator.replace("$", ""):
            fail(f"resume-pipeline route table does not mention ${name}")

    print(f"Plugin skill contracts: {len(EXPECTED)} skills passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
