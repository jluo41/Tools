"""scaffold_block.py <Block> [--question <id>] · write the run tickets of an Insight Block.

An Insight Block (ref/block-contract.md) is a task Block: one Job per DIKW level, one Task
per question (`tNN_<name>/` with `question.md`, `scripts/`, the page). Every question with a
compute need gets one ticket per dataset (board.md `datasets:`) x partition it is asked on:
`runs/<dataset>_<partition>.sh`, the same lines in every ticket, so a run has no config of its
own. The code is never copied: each Task's `scripts/` is the one copy.

Never overwrites a file. Prints what it made, and any ticket for a run the Block no longer asks.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_question import (META, asked_partitions, block_meta, front, live_needs,  # noqa: E402
                          question_folders, question_id)

TICKET = """#!/bin/bash
# <dataset>_<partition>.sh · runs this question on one dataset x partition, writing results/<run>/
# and reports/<run>/ (haipipe-insight ref/block-contract.md § The run). The same lines in every
# run ticket; the file name is the run.
R="$(cd "$(dirname "$0")" && while [ ! -f env.sh ] && [ "$PWD" != / ]; do cd ..; done; pwd)"
source "$R/env.sh" >/dev/null 2>&1
exec "$R/.venv/bin/python" "$R/Tools/plugins/haipipe-toolkit/skills/2_theme/insight/haipipe-insight/ref/run_question.py" \\
  "$(cd "$(dirname "$0")/.." && pwd)" "$(basename "$0" .sh)"
"""


def wanted_runs(block, q, partitions):
    """The run stems a question owes: every dataset x asked partition, when it has a compute need."""
    if not any(n.get("kind") == "compute" for n in live_needs(q).values()):
        return []                                           # no compute need: the page alone, no run
    return [f"{d}_{p}" for d in block_meta(block)["datasets"] for p in asked_partitions(q, partitions)]


def scaffold(block, only=None):
    block = Path(block).resolve()
    partitions = front(block / META / "partitions.md")[0]["partitions"]
    made, extra = [], []
    for task in question_folders(block):
        qid = question_id(task)
        if only and only not in (task.name, qid):
            continue
        q = front(task / "question.md")[0]
        want = wanted_runs(block, q, partitions)
        for stem in want:
            ticket = task / "runs" / f"{stem}.sh"
            if not ticket.exists():
                ticket.parent.mkdir(parents=True, exist_ok=True)
                ticket.write_text(TICKET)
                ticket.chmod(0o755)
                made.append(ticket)
        if (task / "runs").is_dir():
            extra += [t for t in sorted((task / "runs").glob("*.sh")) if t.stem not in want]
    for p in made:
        print(f"made   {p.relative_to(block)}")
    for p in extra:
        print(f"extra  {p.relative_to(block)}  (the Block no longer asks this run)")
    return made, extra


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("block")
    a.add_argument("--question", help="one question, by id (D01) or task folder name")
    args = a.parse_args()
    scaffold(args.block, args.question)
