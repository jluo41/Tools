"""A Task's Work on the focus page (the chain of steps behind each Report view), and the Task's views
assembled."""

from __future__ import annotations

from pathlib import Path

from live import insight_views as V
from live.frame import rel
from live.ui_parts import _numbered
from live.insight_view_parts import _section
from live.insight_focus_parts import (
    _todo, _step, _written, _page, _work_page, _map_view, _done, _prompt, _copy_btn, _writing)
from live.insight_focus_task_report import (
    _task_mindmap, TASK_VIEWS, is_task, _task_x, _state, _cite_only, _plan_cites, _qlabel, _aligned, _cite_word,
    _gather_word, TASK_PARTS)


def _chain(x: dict) -> tuple:
    """The whole chain of one question, each link its state, and the next link (its label for the prompt). A question
    with no Run of its own gathers what it cites in place of its Runs: done once every page it cites is written."""
    t, q = x["t"], x["q"]
    hard = t["hard"]
    ran = bool(hard) and all(str(h.get("status")) in ("ok", "refused") for h in hard)
    written = _state(t) in ("answered", "written", "checked") and not str(t["face"].get("check") or "").startswith("↩")
    checked = str(t["face"].get("check") or "").startswith("✅")
    aligned = any(V._closed(r) for r in t["soft"] if "alignment" in r["run"])
    gathered = all(_written(c) for c, via in _plan_cites(x) if not via) if _cite_only(x) else ran
    links = [("plan", bool(q.get("method")) or bool(q.get("question"))), ("agree", bool(q.get("agreed"))),
             ("Runs", gathered), ("page", written), ("check", checked), ("alignment", aligned)]
    nxt = next((k for k, done in links if not done), "")
    return links, nxt


# each link of the chain: what it is, who does it (the role), and its run card's label for the prompt
CHAIN = {"plan": ("Plan the evidence", "writer · in the Question Book, before any Run", ""),
         "agree": ("Agree the plan", "checker · another agent agrees the needs", ""),
         "Runs": ("Run every segment", "the scripts · one Run per segment, from the plan", "Run a segment"),
         "gather": ("Gather what it cites", "writer · the answers its plan cites, each page written first", ""),
         "page": ("Write the page", "writer · from the Runs' results", "page"),
         "check": ("Check the page", "checker · in a fresh context", "Check a report"),
         "alignment": ("Check the alignment", "checker · each cell against its question", "Check alignment")}


def _tw_answer(x: dict) -> str:
    """The chain of roles (the theme drawing's Task Work: writer, checker, the scripts), a row per link with its state,
    the verb live on the next link only; a Task never asks the person, who signs at the Job. The alignment row carries
    its verdict and its one line, its pass one click away (round 1, D01); a page being written says running."""
    links, nxt = _chain(x)
    rows = []
    for k, done in links:
        key = "gather" if k == "Runs" and _cite_only(x) else k
        words, who, label = CHAIN[key]
        label = V.WRITE_CARD.get(x["t"]["qid"][:1], "Write a report") if label == "page" else label
        state = "done" if done else "ready" if k == nxt else "to do"
        verb = _copy_btn(_prompt("Task", label, x["folder"]), x["session"]) if k == nxt and label else ""
        if key == "gather":                          # one word for gathering, from one source (round 2, X01)
            state, verb = _gather_word(x), ""
        if k == "page" and not done and _writing(x["t"]):
            state, verb = "running", ""
        if k == "alignment":
            verdict, line, passed = _aligned(x["t"])
            if verdict:
                state, who = verdict, line or who
                verb = V._open(passed, x["root"], "the alignment check", "Open its pass") if passed else verb
        rows.append((words, who, state, verb))
    nxt_words = CHAIN["gather" if nxt == "Runs" and _cite_only(x) else nxt][0] if nxt else ""
    word = "done" if not nxt else ("running: write the page" if nxt == "page" and _writing(x["t"])
                                   else _gather_word(x) if nxt == "Runs" and _cite_only(x)
                                   else f"next: {nxt_words[:1].lower() + nxt_words[1:]}")
    return _section("🔗 The chain", _todo(rows), word) + _tw_cuts(x)


def _tw_cuts(x: dict) -> str:
    """By segment's Process: the next act on each segment, a new segment for the next plan; a question with no Run of its own
    gathers what it cites instead (round 1, W01: no "Next on each segment" or "A new segment" there)."""
    if _cite_only(x):
        rows = [(f'Cite {_qlabel(x, c)}', "its page written first", _cite_word(c), "")
                for c, via in _plan_cites(x) if not via]
        return _step("🔗 Gather what it cites", rows) if rows else ""
    rows = []
    for h in x["t"]["hard"]:
        s = str(h.get("status") or "planned")
        if s in ("planned", "failed"):
            rows.append((f'Run the {h.get("partition") or h["run"]} segment', h["run"], "ready",
                         _copy_btn(_prompt("Task", "Run a segment", x["folder"]), x["session"])))
    out = (_step("🔲 Next on each segment", rows) if rows else
           _section("🔲 Next on each segment", "<p>Every segment has run.</p>", "done"))
    proto = rel(x["b"]["prototype"]["path"], x["root"]) if x["b"]["prototype"]["path"].exists() else x["folder"]
    return out + _step("✂️ A new segment", [("Propose a segment to the next question version", "a segment is set before any result is seen", "ready",
                                        _copy_btn(_prompt("Block", "Propose a segment", proto), x["session"]))])


def _tw_across(x: dict) -> str:
    board = rel(x["b"]["path"], x["root"])
    many = sum(1 for j in x["b"]["jobs"] if any(t["qid"] == x["t"]["qid"] for t in j["tasks"])) > 1
    return _step("🔁 Track", [(f'Track {x["t"]["qid"]} across the Jobs', "its answer Job by Job",
                              "ready" if many else "waits on a second Job",
                              _copy_btn(_prompt("Block", "Draw a track", board), x["session"]) if many else "")])


def _tw_plan(x: dict) -> str:
    q = x["q"]
    return _step("📋 Method", [("Plan the evidence", "in the Question Book, before any Run", "done" if V._needs(q) or q.get("method") else "to do", ""),
                                ("Agree the method · another agent", "", _done(q.get("agreed")) if q.get("agreed") else "to do", "")])


TASK_PROC = {"answer": _tw_answer, "across-jobs": _tw_across, "plan": _tw_plan}


def task_views(tdir: Path, root: Path, section: str) -> dict:
    """{key: (name, build)}: an insight Task's Report (numbered sections only; the page adds its MindMap) or Work
    (⚙️ Process then 📊 Results, the Report's view by the same function, the MindMap last); {} for any other folder."""
    if not is_task(tdir):
        return {}
    root = root.resolve()
    views = {}
    for key, name in TASK_VIEWS:
        if section == "work":
            def build(key=key):
                x = _task_x(tdir, root)
                return _work_page(TASK_PROC[key](x), TASK_PARTS[key](x))
            views["work-" + key] = (name, build)
        else:
            def build(key=key):
                x = _task_x(tdir, root)
                return _page(_numbered(TASK_PARTS[key](x)))
            views[key] = (name, build)
    if section == "work":
        views["work-mindmap"] = _map_view(_task_mindmap(tdir, root))
    else:
        views["mindmap"] = ("MindMap", _task_mindmap(tdir, root))
    return views
