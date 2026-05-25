#!/usr/bin/env python3
"""
regen_task_log.py — Regenerate <task>/task-log.md from results/<RUN>/runtime.yaml.

Called by run-sh-template.sh at finalize. Idempotent: scans the whole
results/ tree every time, so the output reflects current state regardless
of which run just finished.

Usage:
  python3 regen_task_log.py <task-folder>
  python3 regen_task_log.py                # defaults to cwd

Output:
  <task-folder>/task-log.md (overwritten, never appended)

This script avoids external deps — parses the simple key:value
runtime.yaml schema by hand.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path


LETTER_TO_TYPE = {
    "A": "training",
    "B": "eval",
    "C": "display",
    "D": "data-pipeline",
    "E": "individual",
    "F": "agent",
    "X": "algo-dev",
}


def parse_runtime_yaml(path: Path) -> dict:
    """Minimal YAML key:value parser. runtime.yaml has a flat schema."""
    out = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip()
    return out


def fmt_short_dt(s: str) -> str:
    """ISO 8601 → 'YYYY-MM-DD HH:MM' for compactness."""
    if not s or s == "-":
        return "-"
    try:
        return datetime.fromisoformat(s).strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return s


def is_abandoned(rt: dict, now: datetime, hours: int = 24) -> bool:
    """status=running with started > N hours ago → likely crashed."""
    if rt.get("status") != "running":
        return False
    started = rt.get("started", "")
    if not started:
        return False
    try:
        s = datetime.fromisoformat(started)
        return (now - s).total_seconds() > hours * 3600
    except ValueError:
        return False


def render(task_dir: Path) -> str:
    results_dir = task_dir / "results"
    rows = []
    abandoned = []
    now = datetime.now(timezone.utc).astimezone()

    if results_dir.exists():
        for rt_path in sorted(results_dir.glob("*/runtime.yaml")):
            rt = parse_runtime_yaml(rt_path)
            rt["__run__"] = rt_path.parent.name
            rows.append(rt)
            if is_abandoned(rt, now):
                abandoned.append(rt_path.parent.name)

    rows.sort(key=lambda r: r.get("started", ""), reverse=True)

    parent = task_dir.parent.name
    type_hint = LETTER_TO_TYPE.get(parent[:1], "-") if parent else "-"

    code_review = task_dir / "CODE_REVIEW.md"
    review_status = "exists" if code_review.exists() else "missing"

    lines = []
    lines.append("# task-log.md (auto-generated — do not edit)")
    lines.append("")
    lines.append(f"- task:      `{task_dir.name}`")
    lines.append(f"- group:     `{parent}`")
    lines.append(f"- type:      {type_hint}")
    lines.append(f"- updated:   {now.isoformat(timespec='seconds')}")
    lines.append(f"- runs:      {len(rows)}")
    lines.append(f"- CODE_REVIEW.md: {review_status}")
    lines.append("")

    if rows:
        lines.append("## Runs (newest first)")
        lines.append("")
        lines.append("| Run | Status | Started | Duration | Exit | Headline | Notebook |")
        lines.append("|-----|--------|---------|----------|------|----------|----------|")
        for r in rows:
            nb = r.get("notebook", "-")
            nb_short = nb.rsplit("/", 1)[-1] if nb != "-" else "-"
            lines.append(
                "| `{}` | {} | {} | {} | {} | {} | `{}` |".format(
                    r["__run__"],
                    r.get("status", "-"),
                    fmt_short_dt(r.get("started", "-")),
                    r.get("duration", "-"),
                    r.get("exit_code", "-"),
                    r.get("headline", "-"),
                    nb_short,
                )
            )
        lines.append("")

    if abandoned:
        lines.append("## Abandoned runs (status=running > 24h — likely crashed)")
        lines.append("")
        for run in abandoned:
            lines.append(f"- `{run}`")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("Source of truth: each `results/<RUN>/runtime.yaml` (written atomically")
    lines.append("by `runs/<RUN>.sh`). This file is a derived view; regenerated at each")
    lines.append("run's finalize step. To re-render manually:")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 Tools/plugins/haipipe-toolkit/skills/C_task/haipipe-task-logging/ref/regen_task_log.py \\")
    lines.append(f"        {task_dir}")
    lines.append("```")

    return "\n".join(lines) + "\n"


def main():
    task_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not task_dir.exists():
        print(f"task-folder not found: {task_dir}", file=sys.stderr)
        sys.exit(1)
    (task_dir / "task-log.md").write_text(render(task_dir))


if __name__ == "__main__":
    main()
