"""Today's register board read as plan C (b11 s11 · s12 · s13, 261007): nothing is moved or copied.

A register board (insights/<board>/: 0-MT-meta/ with MT00 and the MT01-MT04 registers, one folder per
partition holding its answering pages) gets one carried Job, `j01_p1_<dataset><vM>/`, and one Task per
registered question, `tNN_<L><NN>_<slug>/`, written by carry_today.py. Their faces hold pointers only
(`carried: today`, `question: QD1`); everything shown is read live from today's folders by the old page's
reader (insightboard.board_snapshot):

    the Prototype, release p1   the MT01-MT04 registers (the questions) and the work Block whose Tasks
                                hold the scripts; the cuts from MT00
    the dataset, version vM     the extract MT00 names (`20250616_<dataset><vM>_…`)
    a Task's hard Run per cut   the question's cell on that partition: its tickets, its answering page
    a Task's soft Runs          the page runs beside each cell (runs/run-<type>-….md)
    the Board's handoff         the signed Wisdom answers

The dicts have plan C's shapes (insight_plan_c.board · job · task), so insight_views draws them unchanged.
Read-only.
"""
from __future__ import annotations

import re
import time
from pathlib import Path

from live import insight_plan_c as P
from live import insightboard as IB

MARK = {"✅": "✅ answered", "🟡": "🟡 partial", "🚫": "refused"}
_CACHE: dict = {}
TTL = 120.0   # a cold read of a large board takes seconds; answers change slowly


def is_carried(block: Path) -> bool:
    return any(P.front(j / f"{j.name}.md").get("carried") for j in _jobs(block))


def _jobs(block: Path) -> list:
    return sorted(p for p in block.iterdir() if p.is_dir() and P.JOB_NAME.match(p.name)) if block.is_dir() else []


def _root(block: Path) -> Path:
    """The SPACE root: the nearest folder above holding env.sh (else .git)."""
    for mark in ("env.sh", ".git"):
        for p in block.parents:
            if (p / mark).exists():
                return p
    return Path(block.anchor)


def snapshot(block: Path) -> dict:
    """The old page's snapshot of this board, kept a few seconds (one page view reads it several times)."""
    block = block.resolve()
    hit = _CACHE.get(block)
    if hit and time.time() - hit[0] < TTL:
        return hit[1]
    snap = IB.board_snapshot(block, _root(block), block.name)
    _CACHE[block] = (time.time(), snap)
    return snap


def qid(cid: str) -> str:
    """QD1 -> D01."""
    m = re.match(r"^Q([DIKW])(\d+)$", cid)
    return f"{m.group(1)}{int(m.group(2)):02d}" if m else cid


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "question"


def part_name(snap: dict, pid: str) -> str:
    return pid if pid in (IB.FULL, IB.CROSS) else IB._part_label(snap, pid)


def dataset_version(snap: dict) -> tuple:
    """(dataset, version, extract, frozen, rows) from the extract MT00 names."""
    short, full = IB._dataset_line(snap)
    name = short.split(" · ")[0]
    m = re.match(r"^(.+?)(v\d+)$", name)
    text = (snap["by_id"].get("MT00") or {}).get("text", "")
    window = IB._WINDOW.search(text)
    rows = next((p["rows"] for p in snap["partitions"] if p["id"] == IB.FULL), "")
    return ((m.group(1), m.group(2)) if m else (name, "v1")) + (full, window.group(2) if window else "", rows)


def prototype(block: Path) -> dict:
    """Release p1: today's questions (the registers), the cuts (MT00), the scripts' work Block."""
    snap = snapshot(block)
    notes = IB.question_notes(snap)
    tasks = [Path(r["task_path"]) for r in IB.work_runs(snap) if r.get("task_path")]
    work = next((p for t in tasks for p in t.parents if re.match(r"^b\d+_", p.name)), None)
    path = work if work and work.is_dir() else block / "0-MT-meta"
    qs = {}
    for q in snap["questions"]:
        n = notes.get(q["id"], {})
        qs[qid(q["id"])] = {"id": qid(q["id"]), "level": P.LEVEL_OF.get(q["id"][1], ""),
                            "question": (f'{n["name"]}: ' if n.get("name") else "") + q["question"],
                            "method": {}, "signed": "", "agreed": n.get("agreed", ""), "change": "",
                            "task": None, "file": Path(q["register"]["path"]), "cells": q["cells"], "cid": q["id"],
                            "fields": {"register": q["register"]["id"], "the ask": n.get("ask", ""), "why now": n.get("why", ""),
                                       "what would answer it": n.get("answer", ""),
                                       "evidence needs": " · ".join(f"{e[0]} {e[2]}" for e in n.get("needs") or []),
                                       "needs agreed": n.get("agreed", "")}}
    names = [part_name(snap, p["id"]) for p in snap["partitions"] if p["id"] != IB.CROSS]
    parts = [{"name": part_name(snap, p["id"]), "where": p["where"] or "",
              "why": " · ".join(x for x in (f'{p["rows"]} rows' if p["rows"] else "", p["share"] or "") if x)}
             if p["id"] != IB.CROSS else {"name": "cross", "of": names, "why": "compares the cuts"}
             for p in snap["partitions"]]
    rel = {"name": "p1", "job": path, "face": {"state": "today's questions, not yet versioned", "signed": ""},
           "questions": qs, "partitions": parts, "thresholds": {}}
    return {"path": path, "releases": [rel], "proposals": []}


def _hard(snap: dict, block: Path, q: dict) -> list:
    """One hard Run per cut the question is asked on: its tickets, its answering page."""
    from live.insight_theme import _cell_runs
    answered = IB._answered_by(snap)
    rows = {p["id"]: p for p in snap["partitions"]}
    out = []
    for p in snap["partitions"]:
        cell = q["cells"].get(p["id"])
        if not cell or cell["mark"] == "·":
            continue
        runs = _cell_runs(snap, q, p["id"], answered) or []
        page = snap["by_id"].get(cell.get("page", ""))
        rep = IB.report(snap, q["id"], p["id"]) if page else None
        receipt = Path(runs[0]["receipt"]) if runs and runs[0].get("receipt") else None
        name = (runs[0]["call"] + (f" +{len(runs) - 1}" if len(runs) > 1 else "")) if runs else (cell.get("page") or "—")
        out.append({"run": name, "kind": "hard", "type": "hard", "partition": part_name(snap, p["id"]),
                    "target": p["id"], "status": MARK.get(cell["mark"], "—") + (f' · {cell["note"]}' if cell["note"] else ""),
                    "path": receipt.parent if receipt else block, "report": Path(page["path"]) if page else None,
                    "n": rows[p["id"]]["rows"] or "—", "power": "—",
                    "answer": rep["headline"] if rep else "", "how-sure": rep["strength"] if rep else ""})
    return out


def _soft(hard: list) -> list:
    """The page runs beside each answering page (runs/run-<type>-….md)."""
    out = []
    for h in hard:
        if not h["report"]:
            continue
        for f in sorted((h["report"].parent / "runs").glob("run-*.md")):
            out.append({"run": f.stem, "kind": "soft", "type": f.stem.split("-")[1], "partition": h["partition"],
                        "target": h["target"], "status": "—", "path": f, "report": f})
    return out


def task(tdir: Path) -> dict:
    block = tdir.parent.parent
    snap = snapshot(block)
    fm = P.front(tdir / f"{tdir.name}.md")
    q = next((x for x in snap["questions"] if x["id"] == fm.get("question")), None)
    hard = _hard(snap, block, q) if q else []
    marks = [h["status"][:1] for h in hard]
    state = ("answered" if marks and all(m == "✅" for m in marks) else "partial" if "🟡" in marks
             else "refused" if marks and all(m == "r" for m in marks) else "answered" if "✅" in marks else "—")
    first = next((h for h in hard if h["report"]), None)
    face = {"answer-status": state, "answer": first["answer"] if first else "", "how-sure": first["how-sure"] if first else "",
            "check": "", "question": fm.get("question", "")}
    return {"name": tdir.name, "path": tdir, "qid": qid(fm.get("question", "")), "page": first["report"] if first else None,
            "face": face, "hard": hard, "soft": _soft(hard)}


def job(jdir: Path) -> dict:
    fm = P.front(jdir / f"{jdir.name}.md")
    m = P.JOB_NAME.match(jdir.name)
    tasks = [task(t) for t in sorted(jdir.iterdir()) if t.is_dir() and P.TASK_NAME.match(t.name)]
    return {"name": jdir.name, "path": jdir, "face": fm, "release": fm.get("release") or (m.group(1) if m else "p1"),
            "data": fm.get("data") or (m.group(3) if m else "v1"), "state": fm.get("state", "open"),
            "moved": fm.get("moved", "start"), "previous": fm.get("previous", ""), "tasks": tasks, "runs": [], "vs": {}}


def board(block: Path) -> dict:
    snap = snapshot(block)
    dataset, version, extract, frozen, rows = dataset_version(snap)
    jobs = [job(j) for j in _jobs(block)]
    latest = jobs[-1]["name"] if jobs else ""
    handoffs = [{"file": Path(h["record"]["path"]), "counsel": h["title"], "job": latest,
                 "signed": "signed" if h["bindable"] else h["eligibility"]} for h in snap["handoffs"]]
    return {"path": block, "face": {}, "dataset": dataset,
            "versions": [{"version": version, "extract": extract, "frozen": frozen, "rows": rows, "new": "the first version"}],
            "accumulates": "", "jobs": jobs, "runs": [], "reports": [], "handoffs": handoffs,
            "prototype": prototype(block)}


def release(proto: dict, name: str) -> dict:
    return P.release(proto, name)
