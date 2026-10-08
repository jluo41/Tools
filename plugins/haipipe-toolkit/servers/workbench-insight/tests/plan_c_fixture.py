"""A placeholder plan-C Project for the insight theme's tests and screenshots (b11 s00 · s11 · s12 · s13).

Plan C (Tools/designs/b11_theme_insight): the Prototype (questions + scripts) is its own work Block whose
Jobs are versions (j0N_pN/); the insight Board holds one dataset with dated versions, and its Jobs pin one
Prototype version and one data version (j0N_pN_<d>vM/). No real names and no data values: every value is a
placeholder. `make(root)` writes the Project under root and returns its folder.

    python plan_c_fixture.py <out-dir>
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

PROJECT = "Project-InsightDemo"
BOARD = "insights/b01_topic"
PROTO = "work/b01_topic_prototype"
PARTS = ("full", "part-a", "part-b")            # Cross is a test across them, not a cut of rows
QUESTIONS = {   # id -> (folder slug, level, ask, answer, read)
    "D01": ("question-a", "data", "By level", "By exploring", ""),
    "I01": ("question-b", "information", "By analysis plan", "By exploring", "By heterogeneity"),
    "K01": ("question-c", "knowledge", "By estimand", "By hypothesis test", "By multiverse"),
    "K02": ("question-d", "knowledge", "By partition and power", "By model comparison", "By heterogeneity"),
    "W01": ("question-e", "wisdom", "By goal-question-metric", "", "By sensemaking"),
    "I04": ("question-f", "information", "By question type", "By pattern mining", "By heterogeneity"),
}
RELEASES = {   # release -> {qid: (release that holds its Task, change in this release)}
    "p1": {q: ("p1", "new") for q in ("D01", "I01", "K01", "K02", "W01")},
    "p2": {"D01": ("p1", "kept"), "I01": ("p1", "kept"), "K01": ("p2", "changed: its script fixed"),
           "K02": ("p1", "kept"), "W01": ("p1", "kept"), "I04": ("p2", "new")},
}
JOBS = [   # (job, release, data version, state, moved, previous Job)
    ("j01_p1_demov1", "p1", "v1", "closed", "start", ""),
    ("j02_p1_demov2", "p1", "v2", "closed", "data", "j01_p1_demov1"),
    ("j03_p2_demov2", "p2", "v2", "closed", "code", "j02_p1_demov2"),
    ("j04_p2_demov3", "p2", "v3", "open", "data", "j03_p2_demov2"),
]
VS = {   # the run-compare reports: job -> {qid: (status, why)}
    "j02_p1_demov2": {"D01": ("held", "data moved: v1 → v2"), "I01": ("held", "data moved: v1 → v2"),
                      "K01": ("held", "data moved: v1 → v2"), "K02": ("changed", "data moved: v1 → v2"),
                      "W01": ("held", "data moved: v1 → v2")},
    "j03_p2_demov2": {"D01": ("held", "code moved: p1 → p2"), "I01": ("new finding", "code moved: p1 → p2"),
                      "K01": ("changed", "code moved: K01's script fixed in p2"),
                      "K02": ("not comparable", "part-b was refused in j02"), "W01": ("held", "code moved: p1 → p2"),
                      "I04": ("new question", "asked first in p2")},
}


def _front(fields: dict, body: str = "") -> str:
    return "---\n" + yaml.safe_dump(fields, sort_keys=False, allow_unicode=True) + "---\n\n" + body


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _task(qid: str, n: int) -> str:
    return f"t{n:02d}_{qid}_{QUESTIONS[qid][0]}"


def _prototype(base: Path) -> None:
    proto = base / PROTO
    _write(proto / "board.md", _front({"board-kind": "prototype", "serves": BOARD},
                                      "# b01 · <topic> Prototype\n\nThe questions and their scripts, by version.\n"))
    _write(proto / "proposals" / "p001-a-cut.md", _front({"kind": "cut", "from": "j03_p2_demov2", "state": "open"},
                                                         "# Propose a cut\n\n<why this cut>\n"))
    _write(proto / "proposals" / "p002-a-question.md", _front({"kind": "new question", "from": "q02_moved",
                                                               "state": "open"}, "# A new question\n\n<the ask>\n"))
    order = list(QUESTIONS)
    for rel, qs in RELEASES.items():
        job = proto / f"j0{int(rel[1:])}_{rel}"
        _write(job / f"{job.name}.md", _front({"release": rel, "state": "closed", "signed": "✅ <initials> <date>",
                                               "from": "" if rel == "p1" else "p1"},
                                              f"# {rel} · the release\n\n<what changed>\n"))
        rows = {q: {"task": (f"../j0{int(home[1:])}_{home}/" if home != rel else "") + _task(q, order.index(q) + 1),
                    "change": change} for q, (home, change) in qs.items()}
        _write(job / "release.yaml", yaml.safe_dump({"release": rel, "questions": rows}, sort_keys=False))
        _write(job / "partitions.md", _front({"partitions": [
            {"name": "full", "where": "every row", "why": "the whole extract"},
            {"name": "part-a", "where": "<filter A>", "why": "<why A>"},
            {"name": "part-b", "where": "<filter B>", "why": "<why B>"},
            {"name": "cross", "of": ["part-a", "part-b"], "why": "one test of the difference"}]},
            "# The cuts\n\nPart of the plan, fixed before any outcome.\n"))
        _write(job / "thresholds.yaml", yaml.safe_dump({"power": {"smallest_effect_pp": "<pp>", "alpha": "<alpha>"}},
                                                       sort_keys=False))
        for q, (home, change) in qs.items():
            if home != rel:
                continue
            slug, level, ask, answer, read = QUESTIONS[q]
            method = {k: v for k, v in (("ask", ask), ("answer", answer), ("read", read)) if v}
            _write(job / _task(q, order.index(q) + 1) / "question.md", _front(
                {"id": q, "level": level, "question": "<question>", "method": method,
                 "agreed": "✅ <date>", "signed": "✅ <date>"},
                f"# {q} · <question>\n\n**Ask:** <the full ask>\n\n**Why now:** <why>\n\n"
                "**What would answer it:** <the evidence, in words>\n\n**Needs:** E1 compute · E2 cite\n"))


def _board(base: Path) -> None:
    board = base / BOARD
    register = ("## Questions\n\n```yaml\nquestions:\n"
                "- {id: Q01, title: What did each Job answer?, level: data, report: reports/q01_record/q01_record.md}\n"
                "- {id: Q02, title: What moved and why?, level: information, report: reports/q02_moved/q02_moved.md}\n"
                "- {id: Q03, title: What replicates across data versions?, level: knowledge, "
                "report: reports/q03_replicates/q03_replicates.md}\n"
                "- {id: Q04, title: What do we counsel?, level: wisdom, report: reports/q04_counsel/q04_counsel.md}\n"
                "```\n")
    _write(board / "board.md", _front({
        "workbench": "insight", "dataset": "demo", "prototype": PROTO, "accumulates": "?",
        "versions": [{"version": "v1", "extract": "$EXTRACTS/demo-v1", "frozen": "<date>", "rows": "<n>", "new": "the first extract"},
                     {"version": "v2", "extract": "$EXTRACTS/demo-v2", "frozen": "<date>", "rows": "<n>", "new": "<what is new>"},
                     {"version": "v3", "extract": "$EXTRACTS/demo-v3", "frozen": "<date>", "rows": "<n>", "new": "<what is new>"}]},
        "# b01 · <topic>\n\nOne dataset, its versions, a Job per pair (Prototype version × data version).\n\n" + register))
    _write(board / "meta" / "status.md", "# Status\n\n(written only by the checker)\n")
    for slug, level, title in (("q01_record", "data", "What did each Job answer?"), ("q02_moved", "information", "What moved and why?"),
                               ("q03_replicates", "knowledge", "What replicates across data versions?"),
                               ("q04_counsel", "wisdom", "What do we counsel?")):
        _write(board / "reports" / slug / f"{slug}.md", _front(
            {"answer-status": "answered" if slug != "q04_counsel" else "draft", "level": level, "reads": "the Jobs' answers"},
            f"# {title}\n\n**Answer:** <one line>\n\n**Evidence:** <the Jobs it cites>\n"))
    _write(board / "studio" / "s01-question-map" / "s01-question-map.md", "**Topic:** the question map, generated.\n")
    for run, rtype, target in (("run-coverage", "coverage", "every Job"), ("run-track-k01", "track", "K01"),
                               ("run-consistency-j02-j03", "consistency", "j02 · j03"), ("run-report-q03", "report", "Q03"),
                               ("run-add-j04", "add", "j04_p2_demov3")):
        _write(board / "runs" / run / "run.yaml", yaml.safe_dump(
            {"run": run, "kind": "soft", "type": rtype, "target": target, "status": "closed", "passes": 1}, sort_keys=False))
    _write(board / "delivery" / "handoff-w01.md", _front({"counsel": "W01", "job": "j03_p2_demov2",
                                                          "signed": "✅ <initials> <date>"},
                                                         "# W01 · the counsel\n\n<the counsel, one paragraph>\n"))
    order = list(QUESTIONS)
    for job, rel, data, state, moved, prev in JOBS:
        jdir = board / job
        _write(jdir / f"{job}.md", _front({"release": rel, "prototype": f"{PROTO}/j0{int(rel[1:])}_{rel}", "hash": "<sha>",
                                           "data": data, "state": state, "moved": moved, "previous": prev},
                                          f"# {job}\n\nPrototype {rel} on data {data}.\n"))
        for q in RELEASES[rel]:
            slug, level, *_ = QUESTIONS[q]
            tdir = jdir / _task(q, order.index(q) + 1)
            done = state == "closed"
            _write(tdir / f"{tdir.name}.md", _front(
                {"question": q, "answer-status": "answered" if done else "open", "answer": "<one line>" if done else "",
                 "how-sure": "<interval>" if level == "knowledge" and done else "", "check": "✅" if done else ""},
                f"# {q} · the page\n\n**Answer:** <one line>\n"))
            if level == "wisdom":
                continue
            names = list(PARTS) + (["cross"] if level in ("information", "knowledge") else [])
            for k, part in enumerate(names, 1):
                refused = q == "K02" and part == "part-b" and job == "j02_p1_demov2"
                rdir = tdir / "runs" / f"r{k:02d}_{part}"
                _write(rdir / "run.yaml", yaml.safe_dump({
                    "run": rdir.name, "kind": "hard", "type": "cross" if part == "cross" else "partition", "partition": part,
                    "target": tdir.name, "question": q, "script": "<hash>", "release": rel, "data": data,
                    "n": "<n>", "power": "low" if refused else "ok",
                    "status": ("refused" if refused else "ok") if done else "planned", "passes": 1 if done else 0},
                    sort_keys=False))
                if done and not refused:
                    _write(rdir / "result" / "report.md", f"# {rdir.name} · report (generated)\n\n<metrics · the first figure>\n")
            for soft in ("write", "check"):
                _write(tdir / "runs" / f"run-{soft}-{tdir.name[:3]}" / "run.yaml", yaml.safe_dump(
                    {"run": f"run-{soft}-{tdir.name[:3]}", "kind": "soft", "type": soft, "target": tdir.name,
                     "status": "closed" if done else "planned"}, sort_keys=False))
        own = [("launch", job), ("power", job)] + ([("compare", prev[:3])] if prev else []) + ([("close", job)] if state == "closed" else [])
        for rtype, target in own:
            run = f"run-{rtype}-{target[:3] if rtype != 'compare' else target}"
            _write(jdir / "runs" / run / "run.yaml", yaml.safe_dump(
                {"run": run, "kind": "soft", "type": rtype, "target": target, "status": "closed" if state == "closed" else "open"},
                sort_keys=False))
        if job in VS:
            rows = "\n".join(f"| {q} | <answer> | <answer> | {st} | {why} |" for q, (st, why) in VS[job].items())
            _write(jdir / "reports" / f"vs-{prev[:3]}.md", _front(
                {"compares": prev, "with": job, "rule": "the release's compare rule (open)"},
                f"# {job} against {prev}\n\n| question | previous | this | status | why |\n|---|---|---|---|---|\n{rows}\n"))


def make(root: Path) -> Path:
    base = Path(root) / PROJECT
    _write(base / "project.yaml", "name: InsightDemo\n")
    _prototype(base)
    _board(base)
    return base


if __name__ == "__main__":
    print(make(Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()))
