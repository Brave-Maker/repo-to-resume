#!/usr/bin/env python3
"""Install this repository as portable, self-contained Agent Skills."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COLLECTION_PATH = ROOT / "skill-collection.json"
MARKER_NAME = ".repo-to-resume-package.json"
RUNTIME_SCRIPTS = ("migrate_manifest.py", "validate_manifest.py")


def load_collection() -> dict:
    collection = json.loads(COLLECTION_PATH.read_text(encoding="utf-8"))
    if collection.get("name") != "repo-to-resume":
        raise ValueError("skill-collection.json has an unexpected collection name")
    skills = collection.get("skills")
    if not isinstance(skills, list) or not skills:
        raise ValueError("skill-collection.json must declare at least one skill")
    return collection


def select_skills(collection: dict, requested: list[str]) -> list[dict]:
    by_name = {item["name"]: item for item in collection["skills"]}
    if not requested:
        return list(collection["skills"])
    unknown = sorted(set(requested) - set(by_name))
    if unknown:
        raise ValueError(f"unknown skill name(s): {', '.join(unknown)}")
    return [by_name[name] for name in requested]


def read_frontmatter_name(skill_path: Path) -> str:
    text = skill_path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\nname:\s*([^\r\n]+)\r?\n", text)
    if not match:
        raise ValueError(f"invalid SKILL.md frontmatter: {skill_path}")
    return match.group(1).strip()


def build_package(item: dict, destination: Path, collection: dict) -> None:
    source = (ROOT / item["path"]).resolve()
    source_skill = source / "SKILL.md"
    if not source_skill.is_file():
        raise FileNotFoundError(f"missing SKILL.md for {item['name']}: {source_skill}")
    if read_frontmatter_name(source_skill) != item["name"]:
        raise ValueError(f"folder/frontmatter mismatch for {item['name']}")

    destination.mkdir(parents=True)
    skill_text = source_skill.read_text(encoding="utf-8")
    if source != ROOT:
        skill_text = skill_text.replace("../../references/", "references/")
        skill_text = skill_text.replace("../../SKILL.md", "references/root-workflow.md")
    (destination / "SKILL.md").write_text(skill_text, encoding="utf-8")

    shutil.copytree(ROOT / "references", destination / "references")
    scripts_dir = destination / "scripts"
    scripts_dir.mkdir()
    for name in RUNTIME_SCRIPTS:
        shutil.copy2(ROOT / "scripts" / name, scripts_dir / name)
    shutil.copy2(ROOT / "LICENSE", destination / "LICENSE")

    if item["name"] == "resume-pipeline":
        shutil.copy2(ROOT / "SKILL.md", destination / "references" / "root-workflow.md")

    marker = {
        "collection": collection["name"],
        "collection_version": collection["version"],
        "skill": item["name"],
        "source": str(ROOT),
    }
    (destination / MARKER_NAME).write_text(
        json.dumps(marker, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def managed_package(path: Path, expected_skill: str) -> bool:
    marker_path = path / MARKER_NAME
    if not marker_path.is_file():
        return False
    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    return marker.get("collection") == "repo-to-resume" and marker.get("skill") == expected_skill


def preflight(target: Path, skills: list[dict], replace: bool, uninstall: bool) -> None:
    if target.exists() and not target.is_dir():
        raise ValueError(f"target is not a directory: {target}")
    for item in skills:
        destination = target / item["name"]
        if not destination.exists():
            continue
        if not managed_package(destination, item["name"]):
            raise ValueError(
                f"refusing to modify unmanaged destination: {destination}. "
                "Move it aside or choose another --target."
            )
        if not replace and not uninstall:
            raise ValueError(f"already installed: {destination}; pass --replace to update it")


def install(target: Path, skills: list[dict], collection: dict, replace: bool) -> None:
    target.mkdir(parents=True, exist_ok=True)
    preflight(target, skills, replace=replace, uninstall=False)
    with tempfile.TemporaryDirectory(prefix="repo-to-resume-install-") as temp_root:
        staging = Path(temp_root)
        for item in skills:
            build_package(item, staging / item["name"], collection)
        for item in skills:
            destination = target / item["name"]
            if destination.exists():
                shutil.rmtree(destination)
            shutil.move(str(staging / item["name"]), str(destination))
            print(f"installed {item['name']} -> {destination}")


def uninstall(target: Path, skills: list[dict]) -> None:
    preflight(target, skills, replace=False, uninstall=True)
    for item in skills:
        destination = target / item["name"]
        if destination.exists():
            shutil.rmtree(destination)
            print(f"removed {item['name']} -> {destination}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install repo-to-resume into any Agent Skills-compatible directory."
    )
    parser.add_argument("--target", required=True, type=Path, help="Destination skills directory")
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Install one named skill; repeat as needed. Defaults to the full collection.",
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--replace", action="store_true", help="Replace packages installed by this script")
    action.add_argument("--uninstall", action="store_true", help="Remove packages installed by this script")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    collection = load_collection()
    skills = select_skills(collection, args.skill)
    target = args.target.expanduser().resolve()
    if args.uninstall:
        uninstall(target, skills)
    else:
        install(target, skills, collection, replace=args.replace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
