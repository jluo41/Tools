"""insight_ladder's `review` command: where a Board's answers stand against their Runs, and what its Question Book
leaves unsaid. Read-only; `audit` says whether the folders are current, this says whether the answers are.

  reread    a written answer older than a table of one of its Runs (no `results-read:`, or one before the
            receipt's `content_since`): run-write-t<NN> reads the results again
  check     a written answer with no ✅ on its `check:` line: run-check-t<NN>, by an agent that did not write it
  refused   a hard Run that refused, with its reason: an answer, never a missing Run
  book      per question, what ref/deliverables.py notes (a judge with no pass:, a table with no figure); a
            Knowledge or Wisdom question that reads nothing below it; a segment with no `why`
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from insight_ladder_base import TASK, front, read_yaml, project_of, face


def _utc(v) -> dt.datetime | None:
    try:
        t = v if isinstance(v, dt.datetime) else dt.datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)


def answers(board: Path) -> list[tuple]:
    """(Task, kind, words) for each Board Task that owes a reread or a check, and each refused Run."""
    out = []
    for task in sorted(p for p in board.glob("j*/t*") if p.is_dir() and TASK.match(p.name)):
        f = face(task)
        receipts = [(rt.parents[1].name, read_yaml(rt)) for rt in sorted(task.glob("runs/r*/result/runtime.yaml"))]
        for run, r in receipts:
            if r.get("status") == "refused":
                out.append((task, "refused", f"{run}: {str(r.get('reason') or '').strip()}"))
        if not str(f.get("answer") or "").strip():
            continue
        read = _utc(f.get("results-read")) if f.get("results-read") else None
        newer = [run for run, r in receipts if r.get("status") == "ok"
                 and (read is None or (_utc(r.get("content_since") or r.get("ended")) or read) > read)]
        if newer:
            out.append((task, "reread", "no results-read: line" if read is None else "tables newer in " + ", ".join(newer)))
        if not str(f.get("check") or "").startswith("✅"):
            out.append((task, "check", str(f.get("check") or "").strip() or "not checked"))
    return out


def book(ver: Path) -> list[str]:
    """One line per thing a question version leaves unsaid; nothing is judged, only named."""
    import deliverables as DL                                 # ref/, on the path through insight_ladder_base
    notes = []
    for q in sorted(ver.glob("t*/question.md")):
        fm = front(q)[0]
        if fm.get("retired"):
            continue
        notes += DL.gaps(fm)
        live = [n for n in (fm.get("needs") or {}).values() if isinstance(n, dict) and not n.get("retired")]
        if str(fm.get("id", ""))[:1] in "KW" and live and not any(n.get("kind") == "cite" for n in live):
            notes.append(f"{fm.get('id')}: links · a {fm.get('level')} question cites no need below it")
    for p in front(ver / "partitions.md")[0].get("partitions") or []:
        if p.get("name") not in ("full", "cross") and not str(p.get("why") or "").strip():
            notes.append(f"segment {p.get('name')}: no why")
    return notes


def review(folder: Path) -> tuple[list, list]:
    """Print and return (answers rows, book notes) for a Board; for a Question Book version, its notes alone."""
    folder = folder.resolve()
    rows, notes, vers = [], [], []
    if (folder / "board.md").is_file() and front(folder / "board.md")[0].get("prototype"):
        rows = answers(folder)
        proto = project_of(folder) / str(front(folder / "board.md")[0]["prototype"])
        pinned = {str(face(j).get("release") or "") for j in folder.glob("j*") if j.is_dir()}
        vers = [v for v in sorted(proto.glob("j*_*")) if v.is_dir() and any(r and f"_{r}" in v.name for r in pinned)]
    elif (folder / "partitions.md").is_file():
        vers = [folder]
    else:
        vers = [v for v in sorted(folder.glob("j*_*")) if (v / "partitions.md").is_file()]
    for v in vers:
        notes += [f"{v.name} · {n}" for n in book(v)]
    for kind, head in (("reread", "run-write-t<NN>"), ("check", "run-check-t<NN>, another agent"), ("refused", "an answer")):
        got = [(t, w) for t, k, w in rows if k == kind]
        print(f"{'✅' if not got or kind == 'refused' else '❗'} {kind:<8} {len(got):>4}" + (f"   ▶ {head}" if got else ""))
        for t, w in got:
            print(f"     {t.parent.name.split('_')[0]}/{t.name}  {w}")
    print(f"{'✅' if not notes else '❗'} {'book':<8} {len(notes):>4}")
    for n in notes:
        print(f"     {n}")
    return rows, notes
