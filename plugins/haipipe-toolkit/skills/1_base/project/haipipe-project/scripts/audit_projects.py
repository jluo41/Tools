#!/usr/bin/env python3
"""Audit the haipipe-project/v1 contract at Project-root depth, plus cowork/ topic folders.

A path below a Project (a Block, Job, Task or Run) goes to ladder.py; --deep adds its counts."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Iterable


SCHEMA = "haipipe-project/v1"
PROFILES = {"research", "software", "hybrid"}
GIT_MODES = {"workspace", "submodule"}
STATES = {"active", "paused", "archived"}
WORLD_DIRS = {
    "tasks",
    "discoveries",
    "cowork",        # coordination text + project Boards; diagram/ retired 261003 (declared debt)
    "papers",
    "insights",      # older register-kind <Dataset>-InsightBoard/ (new Insight work: a tasks/ Block)
    "designs",
    "labelings",     # labeling Blocks; a Job is one dataset with one label (JL 261005)
    "external",      # applications/ is legacy since 261001: migration debt, not a world
}
CODE_DIRS = {"src", "tests", "scripts", "configs", "docs", "platforms"}
# cowork/bNN_<topic>/ Blocks: a fixed top, the rest in Jobs (JL 261004; haipipe-cowork 0.2.0)
COWORK_BLOCK_DIRS = {"studio", "reports", "_old"}
COWORK_JOB_DIRS = {"design", "materials", "emails", "meetings", "_old"}
COWORK_BLOCK = re.compile(r"b\d{2}_[a-z0-9]+(?:_[a-z0-9]+)*")
COWORK_JOB = re.compile(r"j\d{2}_[a-z0-9]+(?:_[a-z0-9]+)*")


@dataclass
class Manifest:
    values: dict[str, str]
    migration: dict[str, object]


@dataclass
class Result:
    project: Path
    profile: str
    git_mode: str
    state: str
    errors: list[str]
    debts: list[str]

    @property
    def status(self) -> str:
        if self.errors:
            return "failed"
        if self.debts:
            return "debt"
        return "ok"


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def read_manifest(path: Path) -> Manifest:
    values: dict[str, str] = {}
    migration: dict[str, object] = {"legacy_paths": []}
    section = ""
    list_key = ""

    for raw in path.read_text(encoding="utf-8").splitlines():
        content = raw.split("#", 1)[0].rstrip()
        if not content.strip():
            continue
        indent = len(content) - len(content.lstrip())
        stripped = content.strip()

        if indent == 0 and ":" in stripped:
            key, value = stripped.split(":", 1)
            value = value.strip()
            if value:
                values[key] = unquote(value)
                section = ""
            else:
                section = key
            list_key = ""
            continue

        if section == "migration" and indent >= 2:
            if stripped.startswith("- ") and list_key == "legacy_paths":
                migration["legacy_paths"].append(unquote(stripped[2:]))
                continue
            if ":" in stripped:
                key, value = stripped.split(":", 1)
                value = value.strip()
                if key == "legacy_paths":
                    list_key = key
                else:
                    migration[key] = unquote(value)
                    list_key = ""

    return Manifest(values=values, migration=migration)


def observed_git_mode(project: Path) -> str:
    return "submodule" if (project / ".git").is_file() else "workspace"


def cowork_topic_findings(cowork: Path) -> list[str]:
    """Each cowork/bNN_<topic>/ Block: board.md (board-kind: cowork-block), only studio/, reports/,
    _old/ and jNN_<job>/ Jobs at its top, and each Job a jNN_<job>.md page (job-kind: cowork-job)
    with only the Job folder names inside. An old N-<Topic>/ folder is a finding (haipipe-cowork)."""
    found: list[str] = []
    if not cowork.is_dir():
        return found
    for topic in sorted(cowork.iterdir()):
        if topic.is_dir() and topic.name[:1].isdigit() and "-" in topic.name:
            found.append(f"cowork/{topic.name}/ is an old topic folder; make it a bNN_<topic>/ Block")
            continue
        if not (topic.is_dir() and COWORK_BLOCK.fullmatch(topic.name)):
            continue
        board = topic / "board.md"
        text = board.read_text(encoding="utf-8", errors="ignore") if board.is_file() else ""
        if not text:
            found.append(f"cowork/{topic.name}/ has no board.md")
        elif not re.search(r"(?m)^board-kind:[ \t]*cowork-block[ \t]*$", text):
            found.append(f"cowork/{topic.name}/board.md does not declare board-kind: cowork-block")
        for name, hint in (("README.md", "a Block's README is its board.md"), ("PEOPLE.md", "people go in j00_people/")):
            if (topic / name).is_file():
                found.append(f"cowork/{topic.name}/{name}: {hint}")
        for sub in sorted(topic.iterdir()):
            if not sub.is_dir() or sub.name.startswith(".") or sub.name in COWORK_BLOCK_DIRS:
                continue
            if not COWORK_JOB.fullmatch(sub.name):
                found.append(f"cowork/{topic.name}/{sub.name}/ is not a Block folder; move it into a Job")
                continue
            page = sub / f"{sub.name}.md"
            ptext = page.read_text(encoding="utf-8", errors="ignore") if page.is_file() else ""
            if not ptext:
                found.append(f"cowork/{topic.name}/{sub.name}/ has no job page {sub.name}.md")
            elif not re.search(r"(?m)^job-kind:[ \t]*cowork-job[ \t]*$", ptext):
                found.append(f"cowork/{topic.name}/{sub.name}/{sub.name}.md does not declare job-kind: cowork-job")
            for inner in sorted(sub.iterdir()):
                if inner.is_dir() and not inner.name.startswith(".") and inner.name not in COWORK_JOB_DIRS:
                    found.append(f"cowork/{topic.name}/{sub.name}/{inner.name}/ is not a Job folder name")
        if not (topic / "j00_people").is_dir():
            found.append(f"cowork/{topic.name}/ has no j00_people/ (who to ask)")
    return found


def audit(project: Path) -> Result:
    errors: list[str] = []
    debts: list[str] = []
    manifest_path = project / "project.yaml"
    manifest = Manifest(values={}, migration={"legacy_paths": []})

    if not (project / "README.md").is_file():
        errors.append("missing README.md")
    if not manifest_path.is_file():
        errors.append("missing project.yaml")
    else:
        try:
            manifest = read_manifest(manifest_path)
        except (OSError, UnicodeError) as exc:
            errors.append(f"unreadable project.yaml: {exc}")

    values = manifest.values
    profile = values.get("profile", "?")
    declared_git_mode = values.get("git_mode", "?")
    state = values.get("state", "?")

    if values.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    if values.get("id") != project.name:
        errors.append("id must equal directory name")
    if profile not in PROFILES:
        errors.append("profile must be research, software, or hybrid")
    if declared_git_mode not in GIT_MODES:
        errors.append("git_mode must be workspace or submodule")
    observed_mode = observed_git_mode(project)
    if declared_git_mode in GIT_MODES and declared_git_mode != observed_mode:
        errors.append(
            f"git_mode says {declared_git_mode}; disk says {observed_mode}"
        )
    if state not in STATES:
        errors.append("state must be active, paused, or archived")
    if not values.get("mission", "").strip():
        errors.append("mission is required")

    allowed = set(WORLD_DIRS)
    if profile in {"software", "hybrid"}:
        allowed.update(CODE_DIRS)

    declared_legacy = {
        Path(str(item)).parts[0]
        for item in manifest.migration.get("legacy_paths", [])
        if str(item).strip()
    }
    root_dirs = {
        entry.name
        for entry in project.iterdir()
        if entry.is_dir() and not entry.name.startswith(".")
    }

    for name in sorted(root_dirs - allowed):
        if name in declared_legacy:
            debts.append(name)
        else:
            errors.append(f"undeclared noncanonical root: {name}/")

    for name in sorted(declared_legacy):
        if (project / name).exists() and name not in debts:
            debts.append(name)

    errors.extend(cowork_topic_findings(project / "cowork"))

    migration_status = str(manifest.migration.get("status", "")).strip()
    if debts and migration_status not in {"needed", "planned"}:
        errors.append("existing legacy paths require migration.status")
    if migration_status in {"needed", "planned"} and not declared_legacy:
        errors.append("migration.status requires legacy_paths")

    return Result(
        project=project,
        profile=profile,
        git_mode=declared_git_mode,
        state=state,
        errors=errors,
        debts=debts,
    )


def project_paths(args: argparse.Namespace) -> Iterable[Path]:
    if args.all:
        roots = [Path(r).resolve() for r in (args.root or ["examples", "examples-nlp"])]
        yield from sorted(
            path
            for root in roots
            for path in root.glob("Proj*")
            if path.is_dir() and path.name != "_backup"
        )
        return
    for raw in args.projects:
        yield Path(raw).resolve()


def cell(result: Result) -> str:
    details = [*result.errors, *[f"legacy: {item}/" for item in result.debts]]
    return "; ".join(details) if details else "—"


def print_markdown(results: list[Result]) -> None:
    print("| Project | Profile | Git mode | State | Status | Findings |")
    print("|---|---|---|---|---|---|")
    for result in results:
        detail = cell(result).replace("|", "\\|")
        print(
            f"| {result.project.name} | {result.profile} | {result.git_mode} | "
            f"{result.state} | {result.status} | {detail} |"
        )


def print_text(results: list[Result]) -> None:
    for result in results:
        print(
            f"{result.project.name}\t{result.profile}\t{result.git_mode}\t"
            f"{result.state}\t{result.status}\t{cell(result)}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("projects", nargs="*")
    parser.add_argument("--all", action="store_true")
    parser.add_argument(
        "--root", action="append", default=None,
        help="project world to walk with --all; repeatable; default: examples and examples-nlp",
    )
    parser.add_argument("--format", choices={"text", "markdown"}, default="text")
    parser.add_argument("--deep", action="store_true", help="also count every level below each Project (ladder.py)")
    args = parser.parse_args()

    if not args.all and not args.projects:
        parser.error("pass one or more Project paths, or use --all")

    paths = list(project_paths(args))
    below = [p for p in paths if not (p / "project.yaml").is_file()]
    if below:   # a Block, Job, Task or Run: the ladder audit (ladder.py)
        import subprocess
        ladder = Path(__file__).with_name("ladder.py")
        return subprocess.call([sys.executable, str(ladder), "audit", *map(str, below)])
    results = [audit(path) for path in paths]
    if args.format == "markdown":
        print_markdown(results)
    else:
        print_text(results)
    sys.stdout.flush()
    if args.deep:   # every Block, Job, Task and Run below each Project
        import subprocess
        ladder = Path(__file__).with_name("ladder.py")
        for result in results:
            print(f"\n{result.project.name}", flush=True)
            subprocess.call([sys.executable, str(ladder), "audit", str(result.project), "--summary"])
    return 1 if any(result.status == "failed" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
