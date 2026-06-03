"""
End-to-End Roadmap Generator.

Create and update roadmap markdown files from command-line arguments.

Usage:
  python roadmap_generator.py create "project-name" \
    --start "have raw data" \
    --stages "clean,analyze,report" \
    --end "published report"

  python roadmap_generator.py update _WorkSpace/project-name/roadmap.md \
    --stage 2 --status "done" --metric "98.5% accuracy"
"""
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Optional


TEMPLATE = """\
---
name: {name}
description: {name}
metadata:
  version: "1.0.0"
  start_date: "{date}"
  last_updated: "{date}"
  expected_completion: "TBD"
---

# Roadmap: {name}

## START: {start}

| 脚本 | 输入 | 输出 | 成功率 | 状态 |
|------|------|------|--------|------|
{stage_rows}

## END: {end}
"""

STAGE_ROW_TEMPLATE = "| stage_{i}.py | TBD | TBD | TBD | ⬜ pending |"


def create_roadmap(
    name: str,
    start: str,
    stages: List[str],
    end: str,
    output_dir: Optional[Path] = None
) -> Path:
    """Create a new roadmap markdown file.

    Args:
        name: Project name
        start: START state description
        stages: List of stage names
        end: END goal description
        output_dir: Directory to write roadmap (default: _WorkSpace/{name})

    Returns:
        Path to created roadmap file
    """
    if output_dir is None:
        output_dir = Path("_WorkSpace") / name

    output_dir.mkdir(parents=True, exist_ok=True)
    roadmap_path = output_dir / "roadmap.md"

    # Generate stage rows
    stage_rows = []
    for i, stage_name in enumerate(stages, 1):
        stage_rows.append(f"| {stage_name}.py | TBD | TBD | TBD | ⬜ pending |")

    date = datetime.now().strftime("%Y-%m-%d")

    content = TEMPLATE.format(
        name=name,
        start=start,
        end=end,
        stage_rows="\n".join(stage_rows),
        date=date
    )

    roadmap_path.write_text(content)
    print(f"✅ Created roadmap: {roadmap_path}")
    return roadmap_path


def update_roadmap(
    roadmap_path: Path,
    stage: int,
    status: Optional[str] = None,
    metric: Optional[str] = None
) -> None:
    """Update a stage's status in an existing roadmap.

    Args:
        roadmap_path: Path to roadmap.md
        stage: Stage number (1-indexed)
        status: One of "pending", "running", "done", "failed"
        metric: Success metric string
    """
    if not roadmap_path.exists():
        print(f"❌ Roadmap not found: {roadmap_path}")
        return

    content = roadmap_path.read_text()

    # Simple approach: find and replace the stage row
    # Assumes format: | stage_N.py | ... |

    status_emoji_map = {
        "pending": "⬜ pending",
        "running": "⏳ running",
        "done": "✅ done",
        "failed": "❌ failed"
    }

    if status not in status_emoji_map and status:
        print(f"❌ Invalid status: {status}. Use: pending, running, done, failed")
        return

    # Find the stage row
    lines = content.split("\n")
    updated = False
    for i, line in enumerate(lines):
        if f"| stage_{stage}.py |" in line:
            # Parse current row
            parts = [p.strip() for p in line.split("|")]
            # Format: ["", "stage_N.py", "input", "output", "metric", "status", ""]
            if len(parts) >= 7:
                if metric:
                    parts[4] = metric
                if status:
                    parts[5] = status_emoji_map[status]
                lines[i] = " | ".join(parts)
                updated = True
                break

    if updated:
        # Update last_updated timestamp
        new_date = datetime.now().strftime("%Y-%m-%d")
        content = "\n".join(lines)
        content = content.replace(
            'last_updated: "',
            f'last_updated: "{new_date}'
        )
        roadmap_path.write_text(content)
        print(f"✅ Updated stage {stage}: {status} {metric or ''}")
    else:
        print(f"❌ Stage {stage} not found in roadmap")


def main():
    parser = argparse.ArgumentParser(
        description="End-to-End Roadmap Generator"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # create command
    create_parser = subparsers.add_parser("create", help="Create new roadmap")
    create_parser.add_argument("name", help="Project name")
    create_parser.add_argument("--start", required=True, help="START state")
    create_parser.add_argument(
        "--stages",
        required=True,
        help="Comma-separated stage names, e.g., 'clean,analyze,report'"
    )
    create_parser.add_argument("--end", required=True, help="END goal")

    # update command
    update_parser = subparsers.add_parser("update", help="Update stage status")
    update_parser.add_argument("roadmap", type=Path, help="Path to roadmap.md")
    update_parser.add_argument("--stage", type=int, required=True, help="Stage number")
    update_parser.add_argument("--status", help="Status: pending/running/done/failed")
    update_parser.add_argument("--metric", help="Success metric")

    args = parser.parse_args()

    if args.command == "create":
        stages = [s.strip() for s in args.stages.split(",")]
        create_roadmap(args.name, args.start, stages, args.end)
    elif args.command == "update":
        update_roadmap(args.roadmap, args.stage, args.status, args.metric)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
