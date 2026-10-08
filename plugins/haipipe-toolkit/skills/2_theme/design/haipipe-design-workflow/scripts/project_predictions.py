"""Project t99's ranking into each design Task, once run-rank-t99 has closed (haipipe-design/ref/design-ladder.md, rule 8).

    python project_predictions.py <job folder> [--against "the control"] [--dry]

Reads `t99_review-whole/runs/run-rank-t99/result/ranking.csv` (rank · design · predicted · why · kept) and, for each
row, writes the design Task's `prediction.yaml` (predicted · against · by · frozen: draft) and moves its face's
`state:` from `passed` to `kept` or `dropped`. A prediction already frozen (`frozen:` other than `draft`) is never
touched, and a design not `passed` keeps its state. Prints what it changed. The rank Run itself writes only its
result/; this projection is the workflow's.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

import yaml

RANK = Path("t99_review-whole") / "runs" / "run-rank-t99"
OLD_RANK = re.compile(r"^r\d\d_rank_")                  # drawn before 261007, still read


def rank_run(job: Path) -> Path | None:
    if (job / RANK).is_dir():
        return job / RANK
    runs = job / "t99_review-whole" / "runs"
    old = sorted(p for p in runs.iterdir() if OLD_RANK.match(p.name)) if runs.is_dir() else []
    return old[-1] if old else None


def _card(run: Path) -> dict:
    try:
        return yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}


def _state(face: Path) -> str:
    m = re.search(r"(?m)^state:\s*(\S+)", face.read_text(encoding="utf-8"))
    return m.group(1) if m else ""


def _set_state(face: Path, state: str) -> None:
    text = face.read_text(encoding="utf-8")
    face.write_text(re.sub(r"(?m)^state:\s*\S+", f"state: {state}", text, count=1), encoding="utf-8")


def project(job: Path, against: str = "the control", dry: bool = False) -> list:
    run = rank_run(job)
    if run is None:
        sys.exit(f"no run-rank-t99 in {job.name}/t99_review-whole/runs/")
    card = _card(run)
    if card.get("status") not in ("closed", "passed"):
        sys.exit(f"{run.name} is {card.get('status', 'not closed')!r}: project once it has closed")
    ranking = run / "result" / "ranking.csv"
    if not ranking.is_file():
        sys.exit(f"{run.name} has no result/ranking.csv")
    tasks = {m.group(1): p for p in job.iterdir() if p.is_dir() and (m := re.match(r"^t\d+_(d\d+)_", p.name))}
    by = card.get("by") or "the ④ ⑤ reviewer"
    changed = []
    with ranking.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            task = tasks.get(row.get("design", ""))
            if task is None:
                print(f"skip {row.get('design')}: no design Task")
                continue
            pred = task / "prediction.yaml"
            old = yaml.safe_load(pred.read_text(encoding="utf-8")) if pred.is_file() else {}
            if isinstance(old, dict) and str(old.get("frozen", "draft")) != "draft":
                print(f"keep {task.name}: its prediction is frozen ({old['frozen']})")
                continue
            face = task / f"{task.name}.md"
            kept = str(row.get("kept", "")).strip().lower() in ("yes", "true", "1", "kept")
            new_state = ("kept" if kept else "dropped") if face.is_file() and _state(face) == "passed" else None
            if not dry:
                pred.write_text(yaml.safe_dump({"predicted": row.get("predicted", ""), "against": against, "by": by,
                                                "frozen": "draft"}, sort_keys=False, allow_unicode=True),
                                encoding="utf-8")
                if new_state:
                    _set_state(face, new_state)
            changed.append((task.name, row.get("predicted", ""), new_state or "state unchanged"))
            print(f"{'would write' if dry else 'wrote'} {task.name}: predicted {row.get('predicted')}, "
                  f"{new_state or 'state unchanged'}")
    return changed


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("job", type=Path)
    ap.add_argument("--against", default="the control")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args(argv)
    return project(a.job, a.against, a.dry)


if __name__ == "__main__":
    main()
