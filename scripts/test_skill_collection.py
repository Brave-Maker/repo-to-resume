#!/usr/bin/env python3
"""Deterministic checks for the portable Agent Skills collection."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COLLECTION_PATH = ROOT / "skill-collection.json"
EXPECTED = {
    "repo-to-resume",
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


def validate_package(skill_dir: Path) -> None:
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.is_file():
        fail(f"missing SKILL.md: {skill_path}")
    text = skill_path.read_text(encoding="utf-8")
    name, description = frontmatter(text, skill_path)
    if name != skill_dir.name:
        fail(f"folder/frontmatter mismatch: {skill_dir.name} != {name}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        fail(f"invalid Agent Skills name: {name}")
    if not description or len(description) > 1024:
        fail(f"invalid description length: {name}")
    if "../../" in text:
        fail(f"non-portable parent reference remains: {skill_path}")
    for relative in re.findall(r"(?:references|scripts)/[a-z0-9._-]+", text):
        if not (skill_dir / relative).is_file():
            fail(f"missing packaged resource: {skill_dir / relative}")


def main() -> int:
    forbidden_host_files = [
        ROOT / ".codex-plugin" / "plugin.json",
        ROOT / "agents" / "openai.yaml",
    ]
    forbidden_host_files.extend((ROOT / "skills").glob("*/agents/openai.yaml"))
    remaining = [str(path) for path in forbidden_host_files if path.is_file()]
    if remaining:
        fail(f"host-specific packaging remains: {remaining}")

    collection = json.loads(COLLECTION_PATH.read_text(encoding="utf-8"))
    names = [item.get("name") for item in collection.get("skills", [])]
    if set(names) != EXPECTED or len(names) != len(EXPECTED):
        fail("skill-collection.json does not expose the expected unique skills")

    source_folders = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    if source_folders != EXPECTED - {"repo-to-resume"}:
        fail("source skill folders differ from skill-collection.json")
    for folder in sorted(source_folders):
        prompts_path = ROOT / "skills" / folder / "test-prompts.json"
        prompts = json.loads(prompts_path.read_text(encoding="utf-8"))
        if not isinstance(prompts, list) or len(prompts) < 3:
            fail(f"{folder} must have at least three test prompts")

    with tempfile.TemporaryDirectory(prefix="repo-to-resume-skills-") as temp_root:
        target = Path(temp_root) / ".agents" / "skills"
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "install_skills.py"), "--target", str(target)],
            check=True,
            capture_output=True,
            text=True,
        )
        installed = {path.name for path in target.iterdir() if path.is_dir()}
        if installed != EXPECTED:
            fail(f"installed skill set differs: {sorted(installed)}")
        for skill_dir in sorted(target.iterdir()):
            validate_package(skill_dir)

        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "install_skills.py"),
                "--target",
                str(target),
                "--replace",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        unmanaged_target = Path(temp_root) / "unmanaged" / "skills"
        unmanaged_skill = unmanaged_target / "project-analyzer"
        unmanaged_skill.mkdir(parents=True)
        (unmanaged_skill / "SKILL.md").write_text("user-owned\n", encoding="utf-8")
        refused = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "install_skills.py"),
                "--target",
                str(unmanaged_target),
                "--skill",
                "project-analyzer",
                "--replace",
            ],
            capture_output=True,
            text=True,
        )
        if refused.returncode == 0 or not (unmanaged_skill / "SKILL.md").is_file():
            fail("installer overwrote an unmanaged same-name skill")

        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "install_skills.py"),
                "--target",
                str(target),
                "--uninstall",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        if any(target.iterdir()):
            fail("uninstall left managed skill packages behind")

    print(f"Agent Skills collection contracts: {len(EXPECTED)} skills passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
