#!/usr/bin/env python3
"""Collapse the v0.6.1 one-Job-per-Block shape into real Board Blocks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from migrate_bjtr import (
    CANONICAL_BLOCK_RE,
    nested_scalar,
    replace_project_references,
    scalar,
    slugify,
    top_level_sections,
)


CANONICAL_JOB_RE = re.compile(r"^j[0-9]{2}_.+_.+$")
CANONICAL_TASK_RE = re.compile(r"^t[0-9]{2}_.+_.+$")


@dataclass(frozen=True)
class GroupMove:
    bank: Path
    old_block: str
    old_job: str
    new_block: str
    new_job: str
    block_title: str
    job_title: str

    @property
    def old_path(self) -> Path:
        return self.bank / self.old_block / self.old_job

    @property
    def new_path(self) -> Path:
        return self.bank / self.new_block / self.new_job

    @property
    def old_address(self) -> str:
        return f"{self.old_block[:3]}.{self.old_job[:3]}"

    @property
    def new_address(self) -> str:
        return f"{self.new_block[:3]}.{self.new_job[:3]}"


def plan_bank(bank: Path, board_slug: str, board_title: str) -> list[GroupMove]:
    bank = bank.resolve()
    if bank.name != "discoveries" or not bank.is_dir():
        raise ValueError(f"not a Discovery bank: {bank}")
    blocks = sorted(
        path
        for path in bank.iterdir()
        if path.is_dir() and CANONICAL_BLOCK_RE.fullmatch(path.name)
    )
    if len(blocks) < 2:
        raise ValueError(f"regroup needs at least two one-Job Blocks: {bank}")
    new_block = f"b01_{slugify(board_slug)}"
    if (bank / new_block).exists() and new_block not in {path.name for path in blocks}:
        raise FileExistsError(bank / new_block)

    moves: list[GroupMove] = []
    for job_number, block in enumerate(blocks, start=1):
        jobs = sorted(
            path
            for path in block.iterdir()
            if path.is_dir() and CANONICAL_JOB_RE.fullmatch(path.name)
        )
        if len(jobs) != 1:
            raise ValueError(
                f"expected the v0.6.1 one-Job Block shape at {block}; found {len(jobs)} Jobs"
            )
        old_job = jobs[0]
        manifests = sorted(old_job.glob("t[0-9][0-9]_*/discovery.yaml"))
        if not manifests:
            raise ValueError(f"Job has no Discovery Tasks: {old_job}")
        manifest_text = manifests[0].read_text(encoding="utf-8")
        job_title = nested_scalar(
            manifest_text,
            "job",
            "title",
            old_job.name[4:].replace("_", " ").capitalize(),
        )
        moves.append(
            GroupMove(
                bank=bank,
                old_block=block.name,
                old_job=old_job.name,
                new_block=new_block,
                new_job=f"j{job_number:02d}_{old_job.name[4:]}",
                block_title=board_title,
                job_title=job_title,
            )
        )
    return moves


def rewrite_manifest(manifest: Path, move: GroupMove) -> None:
    text = manifest.read_text(encoding="utf-8")
    task = manifest.parent.name
    if not CANONICAL_TASK_RE.fullmatch(task):
        raise ValueError(f"invalid Task folder: {manifest.parent}")
    address = f"{move.new_address}.{task[:3]}"
    replacements = {
        "address": f"address: {address}\n",
        "address_compact": f"address_compact: {address.replace('.', '')}\n",
        "block": (
            "block:\n"
            f"  id: {move.new_block[:3]}\n"
            f"  slug: {move.new_block[4:]}\n"
            f"  title: {json.dumps(move.block_title, ensure_ascii=False)}\n"
        ),
        "job": (
            "job:\n"
            f"  id: {move.new_job[:3]}\n"
            f"  slug: {move.new_job[4:]}\n"
            f"  title: {json.dumps(move.job_title, ensure_ascii=False)}\n"
        ),
    }
    sections = []
    seen = set()
    for key, section in top_level_sections(text):
        if key in replacements:
            sections.append(replacements[key].rstrip())
            seen.add(key)
        else:
            sections.append(section.rstrip())
    missing = set(replacements) - seen
    if missing:
        raise ValueError(f"manifest missing identity fields {sorted(missing)}: {manifest}")
    manifest.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")


def reference_pairs(moves: list[GroupMove]) -> list[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for move in moves:
        old_group = f"{move.old_block}/{move.old_job}"
        new_group = f"{move.new_block}/{move.new_job}"
        pairs.add((f"discoveries/{old_group}", f"discoveries/{new_group}"))
        pairs.add((f"discoveries/{move.old_block}", f"discoveries/{new_group}"))
        pairs.add((old_group, new_group))
        pairs.add((move.old_block, new_group))
        pairs.add((f"{move.old_address}.", f"{move.new_address}."))
        pairs.add((move.old_address.replace(".", ""), move.new_address.replace(".", "")))
    return sorted((pair for pair in pairs if pair[0] != pair[1]), key=lambda pair: len(pair[0]), reverse=True)


def apply_bank(moves: list[GroupMove]) -> tuple[int, int, int, int]:
    if not moves:
        return 0, 0, 0, 0
    bank = moves[0].bank
    final_block = bank / moves[0].new_block
    stage = bank / ".bjtr_regroup_stage"
    if stage.exists():
        raise FileExistsError(stage)
    if final_block.exists() and final_block.name not in {move.old_block for move in moves}:
        raise FileExistsError(final_block)
    stage_block = stage / moves[0].new_block
    stage_block.mkdir(parents=True)

    task_count = 0
    for move in moves:
        old_block = bank / move.old_block
        old_job = old_block / move.old_job
        staged_job = stage_block / move.new_job
        old_job.rename(staged_job)
        for item in sorted(old_block.iterdir()):
            destination = staged_job / item.name
            if destination.exists():
                raise FileExistsError(destination)
            item.rename(destination)
        old_block.rmdir()
        task_count += len(
            [path for path in staged_job.iterdir() if path.is_dir() and CANONICAL_TASK_RE.fullmatch(path.name)]
        )

    stage_block.rename(final_block)
    stage.rmdir()

    for move in moves:
        for manifest in sorted(move.new_path.glob("t[0-9][0-9]_*/discovery.yaml")):
            rewrite_manifest(manifest, move)
    changed_refs = replace_project_references(bank.parent, reference_pairs(moves))
    return 1, len(moves), task_count, changed_refs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="regroup v0.6.1 one-Job Discovery Blocks into one Board Block"
    )
    parser.add_argument("bank", type=Path)
    parser.add_argument("--board-slug", required=True)
    parser.add_argument("--board-title", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    moves = plan_bank(args.bank, args.board_slug, args.board_title)
    print(f"BANK {args.bank.resolve()}")
    for move in moves:
        print(f"  {move.old_path.relative_to(move.bank.parent)}")
        print(f"    -> {move.new_path.relative_to(move.bank.parent)} [{move.new_address}]")
    if args.write:
        blocks, jobs, tasks, refs = apply_bank(moves)
        print(f"WROTE blocks={blocks} jobs={jobs} tasks={tasks} reference_files={refs}")
    else:
        print(f"DRY-RUN blocks=1 jobs={len(moves)} tasks=- reference_files=-")
    return 0


if __name__ == "__main__":
    sys.exit(main())
