#!/usr/bin/env python3
"""Audit the haipipe-project/v1 contract at Project-root depth only."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SCHEMA = "haipipe-project/v1"
PROFILES = {"research", "software", "hybrid"}
GIT_MODES = {"workspace", "submodule"}
STATES = {"active", "paused", "archived"}
WORLD_DIRS = {
    "tasks",
    "discoveries",
    "diagram",
    "papers",
    "applications",
    "external",
}
CODE_DIRS = {"src", "tests", "scripts", "configs", "docs"}


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
        root = Path(args.root).resolve()
        yield from sorted(
            path
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
    parser.add_argument("--root", default="examples")
    parser.add_argument("--format", choices={"text", "markdown"}, default="text")
    args = parser.parse_args()

    if not args.all and not args.projects:
        parser.error("pass one or more Project paths, or use --all")

    results = [audit(path) for path in project_paths(args)]
    if args.format == "markdown":
        print_markdown(results)
    else:
        print_text(results)
    return 1 if any(result.status == "failed" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
