"""What each Space shows at an insight Task (one question), and the Task page and Run page drawn whole."""

from __future__ import annotations

from pathlib import Path

from live import insight_plan_c as P
from live.frame import Space, esc, rel, table
from live.insight_view_overall import _leads, _cap
from live.insight_view_parts import (
    _kind, _next_line, _carded, _rows, _st, _chip, _run_link, _open, LEVEL_WORD, _runs_table)


# ── a Task ──────────────────────────────────────────────────────────────────────────────────────
def task_spaces(tdir: Path, root: Path, sub: str, href) -> dict:
    jdir = P.task_job(tdir)
    b = P.board(P.job_board(jdir))
    j = P.job(jdir)
    t = P.task(tdir)
    q = P.question_of(b["prototype"], j["release"], t["qid"])
    level = LEVEL_WORD.get(t["qid"][:1], "")
    head = f'<p class=mut><code>{esc(t["qid"])}</code> on {esc(j["name"])} · {esc(level)} · {_st(t["face"].get("answer-status", "—"))}</p>'
    d_views = ("Question", "Records")
    d_open = sub if sub in d_views else "Question"
    a_views = ("Table", "Reading")
    a_open = sub if sub in a_views else "Table"
    r_views = ("All", "hard", "soft")
    r_open = sub if sub in r_views else "All"
    # page=True on each: the frame takes the subspaces and runs as set, so s13's views stand alone
    return _carded({
        "Description": Space(html=head + (_question(q, root) if d_open == "Question" else _records(t, root)),
                             subspaces=d_views, open=d_open, run_types=(), page=True,
                             note="Read only: a change to the question is made in the Question Book."),
        "Idea Studio": Space(run_types=(_kind("Add a topic", "Add or redraw a studio topic of {folder} (no Run: a pass in sNN-<topic>/passes/pNN-<MMDD>/): sNN-<topic>/, a pass per session."),)),
        "Audience Report": Space(html=head + (_task_table(t, q, root) if a_open == "Table" else _task_reading(t, q, root)),
                                 subspaces=a_views, open=a_open, page=True,
                                 run_types=(_kind(f"Write the {level} report", "Write the page of {folder}: a part per segment."),
                                            _kind("Check a report", "Check the page of {folder} (run-check-<tNN>).", run="run-check-<tNN>"))),
        "Work Details": Space(html=head + _task_parts(t, root), subspaces=("Partitions",), open="Partitions", page=True,
                              run_types=(_kind("Run a segment", "Run {folder} on one segment (rNN_<segment>).",
                                               rows=_rows(t["hard"], root, "hard")),
                                         _kind("Check alignment", "Check a run of {folder} against its plan (run-check).",
                                               rows=_rows(t["soft"], root, "check")))),
        "Runs": Space(html=_next_line(tdir) + head + _runs_table([x for x in t["hard"] + t["soft"] if r_open == "All" or x.get("kind") == r_open], root),
                      subspaces=r_views, open=r_open, page=True,
                      run_types=(_kind("Run a segment", "Run {folder} on one segment (rNN_<segment>)."),
                                 _kind("Check alignment", "Check a run of {folder} against its plan (run-check)."))),
        "Delivery": Space(html=head + "<p class=mut>None of its own: its answer goes up as a cite need.</p>",
                          page=True, note="Nothing to run here."),
    }, "Task", {"Audience Report": a_open, "Runs": r_open}, {"t<NN>": t["name"][:3]},
        keep=lambda c: not c["label"].startswith("Write the ") or c["label"] == f"Write the {level} report")


def _question(q: dict, root: Path) -> str:
    fm = q.get("fields") or (P.front(q["file"]) if q.get("file") else {})
    rows = [(esc(k), esc(v if not isinstance(v, dict) else " · ".join(f"{a}: {b}" for a, b in v.items())))
            for k, v in fm.items() if v]
    name = q["file"].name if q.get("fields") and q.get("file") else "question.md"
    return (f'<p><b>{esc(q["id"])}</b> {esc(q.get("question") or "")}</p>'
            f'<p>{_open(q.get("file"), root, q["id"], name)} · read only: a change is a proposal to the Question Book.</p>'
            + table(("field", "value"), rows))


def _records(t: dict, root: Path) -> str:
    rec = sorted((t["path"] / "draft" / "records").glob("*.md")) if (t["path"] / "draft" / "records").is_dir() else []
    rows = [(_open(r, root, r.stem), "") for r in rec] + [(esc(x["run"]), _st(x.get("status"))) for x in t["soft"]]
    return "<p class=mut>Its records: the page's draft records and its soft runs.</p>" + table(("record", "state"), rows)


def _task_table(t: dict, q: dict, root: Path) -> str:
    f = t["face"]
    rows = [(f'<b>{esc(r.get("partition"))}</b>', _st(r.get("status")), esc(r.get("answer") or f.get("answer") or "—"),
             esc(r.get("how-sure") or f.get("how-sure") or "—"),
             _run_link(r, root)) for r in t["hard"]]
    head = f'<p>{_open(t["page"], root, t["name"], "the page")} · CHECK {esc(f.get("check") or "—")}</p>'
    if not rows:                                  # Wisdom and Executive: no run, the answer cites the ones below
        return (head + f'<p><b>Answer</b>: {esc(f.get("answer") or "not written yet")}</p>'
                f'<p class=mut>How sure: {esc(f.get("how-sure") or "—")} · no runs: it cites the answers below it.</p>')
    return head + table(("partition", "run", "answer", "how sure", "its run"), rows)


def _task_reading(t: dict, q: dict, root: Path) -> str:
    m = (q.get("method") or {}).get("read")
    return (f'<p>Read by: {_chip((m or "—") + " ↗")}</p><p>{_open(t["page"], root, t["name"], "the page")}: '
            f'Answer: {esc(t["face"].get("answer") or "—")}</p>')


def _task_parts(t: dict, root: Path) -> str:
    rows = [(f'<b>{esc(r.get("partition"))}</b>', _run_link(r, root),
             _st(r.get("status")), esc(r.get("n", "—")), esc(r.get("power", "—"))) for r in t["hard"]]
    return table(("partition", "run", "status", "n", "power"), rows) if rows else \
        "<p class=mut>No segment runs: this question cites the answers below it.</p>"


def _run_report(rundir: Path) -> str:
    """The Run's report, an agent's reading of its result (runs/rNN_<segment>/report.md; hai-insight
    ref/run_report.py), first on its page: the headline, its sentences each with the file it cites, the caveat. A mark
    beside the heading: ✅ checked, ❗ returned or written before the result changed."""
    rep = P.run_report(rundir)
    if not rep:
        return ""
    check = rep["check"]
    mark = " ❗" if rep["stale"] or check.startswith("❗") else " ✅" if check.startswith("✅") else ""
    why = ('<p class=mut>The result changed after this was written: write it again.</p>' if rep["stale"] else
           f'<p class=mut>{esc(check.split(": ", 1)[-1])}</p>' if check.startswith("❗") else "")
    items = "".join(f'<li>{esc(str(s.get("text", "")))} <span class=mut>'
                    f'({esc(", ".join(s.get("files") or [s.get("file", "")]))})</span></li>'
                    for s in rep["sentences"] if isinstance(s, dict))
    return (f'<h2>Report{mark}</h2>{why}<p><b>{esc(rep["headline"])}</b></p>' + (f"<ul>{items}</ul>" if items else "")
            + (f'<p><b>Caveat</b>: {esc(rep["caveat"])}</p>' if rep["caveat"] else "")
            + (f'<p class=mut>Carried from <code>{esc(rep["carried"])}</code></p>' if rep["carried"] else ""))


# ── a hard Run's own page, for the pop-out (/_board/insight-run?run=<its folder>) ──────────────
def render_task_page(tdir: Path, root: Path) -> str:
    """One Task of a plan-C Job as a page: its answer (the face's fields and body), then each of its hard
    Runs with its lead lines, each opening its run page. Read-only."""
    from live.paper import _RESULT_PAGE, _md_view
    tdir, root = Path(tdir).resolve(), Path(root).resolve()
    t = P.task(tdir)
    f = t["face"]
    md = t["page"].read_text(encoding="utf-8")
    text = md.split("---", 2)[2] if md.startswith("---") else md
    fields = " · ".join(f"{k} {f[k]}" for k in ("question", "answer-status", "how-sure", "check") if f.get(k) not in (None, ""))
    body = [f'<p class="where mut"><code>{esc(rel(tdir, root))}</code></p><p>{esc(fields)}</p>',
            '<div class=doc>' + _md_view(text, base="/" + rel(tdir, root) + "/") + '</div>']   # its figures, by path
    if not f.get("answer"):
        body.append('<p class=mut>The answer is not written yet: run-write writes it here from the runs below.</p>')
    rows = []
    for run in t["hard"]:
        leads = [P.report_headline(run)] if P.report_headline(run) else _leads(run.get("report"))
        rows.append((_run_link(run, root, run["run"]), _st(run.get("status")), esc(run.get("n", "—")),
                     esc(_cap(leads[0])) if leads else ""))
    if rows:
        body.append(f'<h2>Runs · {len(rows)}</h2>' + table(("run", "status", "rows", "what it found"), rows))
    return _RESULT_PAGE.format(title=esc(tdir.name), body="\n".join(body))


def render_run_page(rundir: Path, root: Path) -> str:
    """One hard Run as a page: where it is, its card, its report (an agent's reading) first, then its generated tables
    (the point, its figures, its tables), every table it wrote, its receipt and its other files. Read-only."""
    from live.paper import _RESULT_PAGE, _csv_view, _md_view
    from urllib.parse import quote
    rundir, root = Path(rundir).resolve(), Path(root).resolve()
    from host_registry import static_path_allowed  # sealed labels, *.private.*, dot folders stay hidden (review 261031)
    if not static_path_allowed(root, rundir):
        return '<p class="mut">This Run is not shown here.</p>'
    res = rundir / "result"
    raw = lambda f: "/" + quote(f.resolve().relative_to(root).as_posix(), safe="/")
    card = P._yaml(rundir / "run.yaml")
    facts = " · ".join(f"{k} {card[k]}" for k in ("question", "partition", "release", "data", "n", "power", "status")
                       if card.get(k) not in (None, ""))
    links = [f'<a href="{esc(raw(f))}" target=_blank rel=noopener>{label} ↗</a>'
             for f, label in ((rundir / "run.sh", "Ticket"), (rundir / "run.yaml", "Run card"),
                              (res / "runtime.yaml", "Receipt")) if f.is_file()]
    body = [f'<h1>{esc(card.get("target", rundir.parent.parent.name))} · {esc(rundir.name)}</h1>'
            f'<p class="where mut"><code>{esc(rel(rundir, root))}</code></p><p>{esc(facts)}</p>',
            f'<div class=links>{" · ".join(links)}</div>']
    body.append(_run_report(rundir))
    report = next((f for f in (res / "tables.md", res / "report.md") if f.is_file()), res / "tables.md")
    if report.is_file():
        body.append('<h2>Tables</h2><div class=doc>'
                    + _md_view(report.read_text(encoding="utf-8", errors="replace"), base=raw(report).rsplit("/", 1)[0] + "/") + "</div>")
    else:
        body.append('<p class=mut>Not run yet.</p>')
    receipt = res / "runtime.yaml"
    if receipt.is_file():
        body.append(f'<details><summary><b>Receipt</b></summary><pre>{esc(receipt.read_text(encoding="utf-8", errors="replace")[:4000])}</pre></details>')
    files = sorted(f for f in res.rglob("*") if f.is_file() and static_path_allowed(root, f)) if res.is_dir() else []
    tabs = [f for f in files if f.suffix.lower() in (".csv", ".tsv")]
    if tabs:
        body.append(f'<details><summary><b>Tables · {len(tabs)}</b></summary>'
                    + "".join(f'<h3>{esc(f.name)}</h3>{_csv_view(f)}' for f in tabs) + "</details>")
    rest = [f for f in files if f not in tabs and f not in (receipt, report) and not f.name.startswith("fig_")]
    if rest:
        body.append(f'<details><summary><b>Other files · {len(rest)}</b></summary><ul class=files>' + "".join(
            f'<li><a href="{esc(raw(f))}" target=_blank rel=noopener>{esc(f.relative_to(res).as_posix())}</a></li>'
            for f in rest) + "</ul></details>")
    return _RESULT_PAGE.format(title=esc(rundir.name), body="\n".join(body))
