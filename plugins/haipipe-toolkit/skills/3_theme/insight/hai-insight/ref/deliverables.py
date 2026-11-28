"""deliverables.py <question folder | question.md | Board Task> · what one question delivers and how each part is reviewed.

Read from the question file alone (ref/block-contract.md § What a question delivers), so the list exists
before any Run: nothing here opens a result.

  per live need   compute: its tables (`output:`) and the figure each one gets (the need's own `figures:`,
                  else the shape figures.py knows from the columns, else none; `kind: none` on one table
                  or `figures: []` on the need says none is wanted); cite: the need it borrows;
                  judge: a reading made on the page. Each with its `pass:`, the test a reviewer applies.
  the answer      the Task page: the answer in one line, how sure, one takeaway per segment asked
  the review      one line per need (its `pass:`), then the level's rule

The same list serves three readers: the maker (what to produce), the checker (`run-check-t<NN>`: what to
test, one verdict per line) and the workbench (the Task page's Needs section). Printed as Markdown.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figures  # noqa: E402
import run_question as RQ  # noqa: E402

MAY_SAY = {"D": "counts and what was seen; no rate compared, no cause",
           "I": "rates and contrasts inside a segment; never a cause",
           "K": "one claim, how sure, its rivals and where it stops",
           "W": "advice a person signs, resting on Knowledge",
           "X": "the plain answer, each point resting on a question below"}
ANSWER = ["the answer in one line", "how sure", "one takeaway per segment asked"]


def planned_shape(columns) -> str:
    """The figure shape figures.py will know a table by, from its declared columns (taken as numbers)."""
    return figures.shape(pd.DataFrame({str(c): pd.Series(dtype=float) for c in columns or []}))


def need_row(nid: str, n: dict) -> dict:
    """One live need → {id, kind, what, tables, figures, no_figure, source, test}."""
    kind = str(n.get("kind") or "")
    row = {"id": nid, "kind": kind, "what": str(n.get("what") or ""), "tables": [], "figures": [], "no_figure": [],
           "source": "", "test": str(n.get("pass") or "")}
    if kind == "compute":
        out = n.get("output") if isinstance(n.get("output"), dict) else {}
        row["tables"] = list(out)
        declared = n.get("figures")
        if declared == []:                                   # `figures: []`: the need asks for no figure
            return row
        named = {f.get("table"): str(f.get("kind") or "line") for f in declared or [] if isinstance(f, dict)}
        for f, cols in out.items():
            if not f.endswith(".csv"):
                continue
            k = named.get(f) or planned_shape(cols)
            if k == "none":                                  # {table: <file>.csv, kind: none}: no figure wanted for it
                continue
            if k:
                row["figures"].append({"table": f, "kind": k, "declared": f in named})
            else:
                row["no_figure"].append(f)
    elif kind == "cite":
        row["source"] = str(n.get("from") or "")
    elif kind == "judge":
        reads = n.get("from") or []
        row["source"] = ", ".join(str(x) for x in (reads if isinstance(reads, list) else [reads]))
    return row


def deliverables(q: dict) -> dict:
    """{needs: [need_row], answer: [str], may_say: str} for one question file's front matter."""
    letter = str(q.get("id") or "?")[:1]
    return {"needs": [need_row(nid, n) for nid, n in RQ.live_needs(q).items() if isinstance(n, dict)],
            "answer": list(ANSWER), "may_say": MAY_SAY.get(letter, "")}


def gaps(q: dict) -> list:
    """What the question leaves unsaid about its own delivery: a judge with no test, a table with no figure."""
    out = []
    for r in deliverables(q)["needs"]:
        if r["kind"] == "judge" and not r["test"]:
            out.append(f"{q.get('id')}.{r['id']}: review · a judge need has no pass: line, so its reading has no test")
        for f in r["no_figure"]:
            out.append(f"{q.get('id')}.{r['id']}: figure · {f} has no known shape and the need declares no figure")
    return out


def brief(q: dict) -> str:
    """The question's delivery and review list, as Markdown: the maker's target and the checker's test."""
    d, qid = deliverables(q), q.get("id")
    lines = [f"# {qid} · what it delivers, how it is reviewed", "", f"**The ask**: {q.get('ask') or ''}", "",
             "## Delivers", ""]
    for r in d["needs"]:
        if r["kind"] == "compute":
            figs = ", ".join(f"{f['kind']} of {f['table']}" for f in r["figures"]) or "none"
            lines.append(f"- {qid}.{r['id']} · tables {', '.join(r['tables']) or 'none'} · figures {figs}")
        elif r["kind"] == "cite":
            lines.append(f"- {qid}.{r['id']} · borrowed from {r['source']}")
        else:
            lines.append(f"- {qid}.{r['id']} · a reading on the page, from {r['source']}")
    lines += [f"- the Task page · {'; '.join(d['answer'])}", "", "## Review, one verdict per line", ""]
    for r in d["needs"]:
        test = r["test"] or ("the cited need is answered" if r["kind"] == "cite" else "NO TEST WRITTEN")
        lines.append(f"- {qid}.{r['id']} · {r['what']} · counts when: {test}")
    lines += [f"- level · the page says only: {d['may_say']}", "- trace · every number on the page is in a Run's result/", ""]
    return "\n".join(lines)


def question_file(path: Path) -> Path:
    """The question file of a question folder, a question.md, or a Board Task (found through its Job's release)."""
    path = Path(path).resolve()
    if path.is_file():
        return path
    if (path / RQ.QFILE).is_file():
        return path / RQ.QFILE
    import run_job as RJ                                     # a Board Task: board.md prototype: + the Job's release:
    job, board = path.parent, path.parent.parent
    jm, tm = RJ.JOB.match(job.name), RJ.TASK.match(path.name)
    rel = RQ.front(job / f"{job.name}.md")[0].get("release") or (jm.group(2) if jm else "")
    qid = RQ.front(path / f"{path.name}.md")[0].get("question") or (tm.group(1) if tm else "")
    proto = board.parent.parent / str(RQ.front(board / "board.md")[0].get("prototype", ""))
    for rdir in sorted(proto.glob(f"j*_{rel}*")):
        row = (RJ._yaml(rdir / "release.yaml").get("questions") or {}).get(qid)
        if row:
            return rdir / row["task"] / RQ.QFILE
    raise SystemExit(f"no question file for {path}")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        raise SystemExit(__doc__)
    q, _ = RQ.front(question_file(Path(argv[0])))
    print(brief(q))
    for g in gaps(q):
        print(f"note: {g}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
