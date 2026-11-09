"""delivery_index.py <Board>

The Board's delivery/ as one table a person reads (b11 round 2: "the Delivery rail's rows carry a state"): each thing
the Board hands over, linked, with its state:

    a handoff draft      delivery/handoff-<W>.md        signed ✅ <date> | not signed
    an Overall Report    delivery/<job>/overall-report  its Job's state: closed ✅ <date> | a preview (the Job is open)

It writes <Board>/delivery/delivery.md, which the workbench's Delivery shows in place of the folder's file list.
Generated: never edit it; run this again once a handoff is drafted or signed, or a Job closes (overall_report.py
runs it after every Overall Report).
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_question as RQ  # noqa: E402
from open_job import JOB, code_id, data_id  # noqa: E402

def _signed(value) -> str:
    v = str(value or "").strip()
    return v if v.startswith("✅") else ""


def _plain(job: str) -> str:
    """A Job in plain words, `j02 · code-v1 × data-v2`, from its folder name (an older name reads the same)."""
    m = JOB.match(job)
    return f"j{m.group(1)} · {code_id(m.group(2))} × {data_id(m.group(4))}" if m else job


def rows(board: Path) -> list:
    """[(its link(s) in Markdown, what it is, state)]: each handoff draft, then each Job's Overall Report, newest
    first."""
    deliv = board / "delivery"
    out = []
    for h in sorted(deliv.glob("handoff-*.md")) if deliv.is_dir() else []:
        face, _ = RQ.front(h)
        counsel = str(face.get("counsel") or h.stem.replace("handoff-", ""))
        job = str(face.get("job") or "")
        what = f"{counsel}'s handoff to Design" + (f", from {_plain(job)}" if job else "")
        signed = _signed(face.get("signed"))
        out.append((f"[{h.name}]({h.name})", what, f"signed {signed}" if signed else "not signed"))
    jobs = sorted((p for p in board.iterdir() if p.is_dir() and JOB.match(p.name)), key=lambda p: p.name, reverse=True)
    for job in jobs:
        part = deliv / job.name
        files = [f"[{n}]({job.name}/{n})" for n in ("overall-report.html", "overall-report.pdf") if (part / n).is_file()]
        if not files:
            continue
        face, _ = RQ.front(job / f"{job.name}.md")
        closed = str(face.get("state") or "") == "closed"
        signed = _signed(face.get("signed"))
        state = ("closed " + signed).strip() if closed else "preview"
        out.append((" · ".join(files), f"The Overall Report of {_plain(job.name)}", state))
    return out


def write(board: Path) -> Path | None:
    """Write <Board>/delivery/delivery.md; None when the Board hands over nothing yet."""
    board = Path(board).resolve()
    got = rows(board)
    if not got:
        return None
    lines = ["| Handed over | What it is | State |", "|---|---|---|"]     # no marker line: the Delivery shows
                                                                       # the file whole (this docstring says it is made)
    lines += [f"| {link} | {w} | {s} |" for link, w, s in got]
    out = board / "delivery" / "delivery.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("board")
    a = ap.parse_args()
    board = Path(a.board).resolve()
    if not (board / "board.md").is_file():
        raise SystemExit(f"{board.name} is not a Board (no board.md)")
    out = write(board)
    if out is None:
        print("nothing handed over yet: no handoff draft and no Overall Report")
        return
    print(f"wrote {out.relative_to(RQ.space_root(board)).as_posix()}")


if __name__ == "__main__":
    main()
