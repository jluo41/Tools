#!/usr/bin/env python3
"""Deterministically plan subjective-label Level-4 Run instances."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Iterable


OPERATION_KINDS = (
    "corpus-contract",
    "discovery-search",
    "guideline-seed",
    "test-reserve",
    "embedding-build",
    "round-prepare",
    "weak-prelabel",
    "human-calibration",
    "guideline-learn",
    "round-measure",
    "round-close",
    "handoff-freeze",
    "test-gold-lock",
    "executor-predict",
    "executor-score",
    "executor-select",
    "scan-preflight",
    "scan-shard",
    "risk-route",
    "human-review",
    "reconcile",
    "audit-sample",
    "audit-human-gold",
    "audit-analyze",
    "dstar-materialize",
)


@dataclass(frozen=True)
class PlannedRun:
    run: str
    phase: str
    operation: str
    episode: str
    target: str


def _slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "target"


def _append(
    rows: list[tuple[str, str, str, str]],
    phase: str,
    operation: str,
    episode: str,
    target: str,
) -> None:
    rows.append((phase, operation, episode, target))


def plan_runs(
    discovery: int,
    round_weak: Iterable[int],
    executors: int,
    shards: int,
) -> list[PlannedRun]:
    weak_counts = tuple(round_weak)
    for name, value in (
        ("discovery", discovery),
        ("executors", executors),
        ("shards", shards),
        *((f"round_weak[{index}]", value) for index, value in enumerate(weak_counts)),
    ):
        if value < 0:
            raise ValueError(f"{name} must be non-negative")

    rows: list[tuple[str, str, str, str]] = []
    _append(rows, "P0", "corpus-contract", "contract", "job-v1")
    for index in range(1, discovery + 1):
        _append(rows, "P0", "discovery-search", "contract", f"query-{index:02d}")
    _append(rows, "P0", "guideline-seed", "contract", "G-00")
    _append(rows, "P0", "test-reserve", "contract", "test-v1")
    _append(rows, "P0", "embedding-build", "contract", "corpus-v1")

    for round_index, weak_count in enumerate(weak_counts, start=1):
        episode = f"round_{round_index:02d}"
        _append(rows, "P1", "round-prepare", episode, episode)
        for weak_index in range(1, weak_count + 1):
            _append(
                rows,
                "P1",
                "weak-prelabel",
                episode,
                f"{episode}-weak-{weak_index:02d}",
            )
        _append(rows, "P1", "human-calibration", episode, episode)
        _append(rows, "P1", "guideline-learn", episode, episode)
        _append(rows, "P1", "round-measure", episode, episode)
        _append(rows, "P1", "round-close", episode, episode)

    _append(rows, "P2", "handoff-freeze", "freeze", "label-v1")
    _append(rows, "P3", "test-gold-lock", "test_01", "test-v1")
    for executor_index in range(1, executors + 1):
        target = f"test-v1-executor-{executor_index:02d}"
        _append(rows, "P3", "executor-predict", "test_01", target)
    for executor_index in range(1, executors + 1):
        target = f"test-v1-executor-{executor_index:02d}"
        _append(rows, "P3", "executor-score", "test_01", target)
    _append(rows, "P3", "executor-select", "test_01", "route-v1")

    _append(rows, "P4", "scan-preflight", "production_01", "corpus-v1")
    for shard_index in range(1, shards + 1):
        _append(
            rows,
            "P4",
            "scan-shard",
            "production_01",
            f"corpus-v1-shard-{shard_index:02d}",
        )
    _append(rows, "P4", "risk-route", "production_01", "corpus-v1")
    _append(rows, "P4", "human-review", "production_01", "risk-queue-v1")
    _append(rows, "P4", "reconcile", "production_01", "corpus-v1")

    _append(rows, "P5", "audit-sample", "audit_01", "audit-v1")
    _append(rows, "P5", "audit-human-gold", "audit_01", "audit-v1")
    _append(rows, "P5", "audit-analyze", "audit_01", "audit-v1")
    _append(rows, "P5", "dstar-materialize", "audit_01", "D-star-v1")

    width = max(2, len(str(len(rows))))
    return [
        PlannedRun(
            run=f"r{index:0{width}d}_labeling-{operation}_{_slug(target)}",
            phase=phase,
            operation=operation,
            episode=episode,
            target=target,
        )
        for index, (phase, operation, episode, target) in enumerate(rows, start=1)
    ]


def _parse_round_weak(value: str) -> tuple[int, ...]:
    if not value.strip():
        return ()
    try:
        return tuple(int(item.strip()) for item in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("use comma-separated integers, e.g. 0,2,2") from exc


def _render_text(runs: list[PlannedRun]) -> str:
    phase_counts = Counter(run.phase for run in runs)
    lines = ["Phase  Runs", "-----  ----"]
    for phase in ("P0", "P1", "P2", "P3", "P4", "P5"):
        lines.append(f"{phase:<5}  {phase_counts[phase]:>4}")
    lines.extend((f"TOTAL  {len(runs):>4}", "", "Run  Phase  Operation              Episode        Target"))
    lines.append("---  -----  ---------------------  -------------  ------------------------")
    for run in runs:
        lines.append(
            f"{run.run:<48}  {run.phase:<5}  {run.operation:<21}  "
            f"{run.episode:<13}  {run.target}"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    plan = subparsers.add_parser("plan", help="plan happy-path Run instances")
    plan.add_argument("--discovery", type=int, required=True, help="bounded discovery queries D")
    plan.add_argument(
        "--round-weak",
        type=_parse_round_weak,
        required=True,
        help="weak executors per calibration round, e.g. 0,2,2",
    )
    plan.add_argument("--executors", type=int, required=True, help="qualification candidates K, baseline included")
    plan.add_argument("--shards", type=int, required=True, help="production shards S")
    plan.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    try:
        runs = plan_runs(args.discovery, args.round_weak, args.executors, args.shards)
    except ValueError as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps({"planned_count": len(runs), "runs": [asdict(run) for run in runs]}, indent=2))
    else:
        print(_render_text(runs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
