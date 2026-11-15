"""A Task's six Spaces (s13): t00 reason ideas, t99 review whole and one design's Task
(split from design_views.py, which re-exports every name here)."""
from __future__ import annotations

from pathlib import Path

from live import design_reader as R
from live.frame import Space, esc, table
from live.design_views_parts import _kind, _rows, _st, _fold, _pairs, _id, _test, _qhead, _mins, _pred
from live.design_views_channel import draft_files, as_read, as_it_reads
from live.design_views_disk import _disk
from live.design_views_job import _reason_ideas, _card, _review_whole


# ── Task (s13) ───────────────────────────────────────────────────────────────────────────────
def task_spaces(tdir: Path, root: Path, sub: str, href) -> dict:
    j = R.job(tdir.parent)
    kind = R.kind_of(tdir)
    rs = R.runs(tdir)
    rows = lambda *t: _rows(rs, root, *t)
    draw = _kind("run-draw-s01", "Draw a studio topic about this Task: {folder}/sNN-<topic>/ (run-draw-<sNN>).",
                 "haipipe-studio")
    if kind == "t00":
        r = _kind("run-reason-t00", "Reason ideas for the Job (② run-reason-t00): inputs/ only, topic by topic, to N + 5 "
                  "ideas, each naming its source.", "haipipe-design-unit", rows=rows("reason"), level="Task")
        opend = _kind(f"run-open-designs-{j['id']}", "Open one design Task per idea (run-open-designs-jNN).", "haipipe-design",
                      rows=_rows(j["runs"], root, "open-designs"))
        ar = ("Topics", "Ideas")
        a_open = sub if sub in ar else "Topics"
        return {"Description": Space(html=_t00_task(j, root), subspaces=("Task",), open="Task", run_types=(r,), page=True,
                                     disk=_disk("t00", "Task", tdir)),
                "Audience Report": Space(html=(_reason_ideas(j, {}, root, href) if a_open == "Topics" else _t00_ideas(j, href)),
                                         subspaces=ar, open=a_open, run_types=(r,) if a_open == "Topics" else (opend,), page=True,
                                         disk=_disk("t00", a_open, tdir)),
                # the Task's Work is its type's steps, Operation over Result (b12 s41 · s42 · s43, 261023)
                "Work Details": _work(tdir, root, sub, href),
                "Idea Studio": Space(run_types=(draw,), page=True),
                "Runs": Space(html=_task_runs_table(rs, sub), subspaces=("All", "hard", "soft"),
                              open=sub if sub in ("hard", "soft") else "All", run_types=(r,), page=True,
                              disk=_disk("t00", "Runs", tdir)),
                "Delivery": Space(disk=_disk("t00", "Delivery", tdir), html='<p class=mut>Hands on ideas.yaml: run-open-designs opens one design Task per idea.</p>',
                                  page=True, note="Nothing to run here: t00 hands its ideas to the Job.")}
    if kind == "t99":
        r = _kind("run-rank-t99", "Review the whole (⑤ run-rank-t99): rank the N + 5, keep the top N, each with its predicted "
                  "outcome; another agent.", "haipipe-design-unit", rows=rows("rank"), level="Task")
        ar = ("Ranking", "Coverage")
        a_open = sub if sub in ar else "Ranking"
        return {"Description": Space(html=_t99_task(j), subspaces=("Task",), open="Task", run_types=(r,), page=True,
                                     disk=_disk("t99", "Task", tdir)),
                "Audience Report": Space(html=(_review_whole(j, {}, root, href) if a_open == "Ranking" else _coverage(j)),
                                         subspaces=ar, open=a_open, run_types=(r,), page=True, disk=_disk("t99", a_open, tdir)),
                # the Task's Work is its type's steps, Operation over Result (b12 s41 · s42 · s43, 261023)
                "Work Details": _work(tdir, root, sub, href),
                "Idea Studio": Space(run_types=(draw,), page=True),
                "Runs": Space(html=_task_runs_table(rs, sub), subspaces=("All", "hard", "soft"),
                              open=sub if sub in ("hard", "soft") else "All", run_types=(r,), page=True,
                              disk=_disk("t99", "Runs", tdir)),
                "Delivery": Space(disk=_disk("t99", "Delivery", tdir), html='<p class=mut>Hands on the kept N and their predictions: the Job\'s run-release '
                                       'writes its delivery/.</p>', page=True, note="Nothing to run here: the Job releases.")}
    d = R.design(tdir)
    did = d["id"]
    gen = _kind(f"run-generate-{did}", f"Generate {did} from its idea (③ run-generate-{did}): inputs/ only.",
                "haipipe-design-unit", rows=rows("generate"), level="Task")
    ver = _kind(f"run-verify-{did}", f"Verify {did} (④ run-verify-{did}-v<k>) in a fresh context, by another agent.",
                "haipipe-design-unit", rows=rows("verify"), level="Task")
    rev = _kind(f"run-revise-{did}", f"Revise {did} after a failed review (run-revise-{did}), then verify again.",
                "haipipe-design-unit", rows=rows("revise"), level="Task")
    frz = _kind(f"run-freeze-prediction-{did}", f"Freeze {did}'s prediction at release (the Job's run-freeze-predictions).",
                "haipipe-design", rows=_rows(j["runs"], root, "freeze-predictions"))
    desc = ("Design", "Evaluation")
    d_open = sub if sub in desc else "Design"
    ar = ("Tests", "Drafts", "Performance")
    a_open = sub if sub in ar else "Tests"
    b = R.board(R.block_of(tdir.parent.parent) or tdir.parent.parent, with_jobs=False)
    return {"Description": Space(html=_design(d, j, href, root) if d_open == "Design" else _evaluation(d), subspaces=desc, open=d_open,
                                 page=True, disk=_disk("design", d_open, tdir), note="Nothing to run here: the design is made in Runs."),
            "Audience Report": Space(html={"Tests": _tests, "Drafts": _drafts, "Performance": _task_perf}[a_open](d, j, b, root),
                                     subspaces=ar, open=a_open,
                                     run_types={"Tests": (ver,), "Drafts": (gen, rev), "Performance": (frz,)}[a_open], page=True,
                                     disk=_disk("design", a_open, tdir)),
            # the Task's Work is its type's steps, Operation over Result (b12 s41 · s42 · s43, 261023)
            "Work Details": _work(tdir, root, sub, href),
            "Idea Studio": Space(run_types=(draw,), page=True),
            "Runs": Space(html=_task_runs_table(rs, sub), subspaces=("All", "hard", "soft"),
                          open=sub if sub in ("hard", "soft") else "All", run_types=(gen, ver, rev), page=True,
                          disk=_disk("design", "Runs", tdir)),
            "Delivery": Space(html=_task_delivery(d, j), page=True, disk=_disk("design", "Delivery", tdir), note="Released with the Job's run-release (a person).")}


def _work(tdir: Path, root: Path, sub: str, href) -> Space:
    from live.task_design import work_space
    return work_space(tdir, root, sub, href)


def _t00_task(j: dict, root: Path) -> str:
    r = j["reason"]
    return _pairs([("step", "② Reason ideas: from inputs/ to N + 5 ideas, frozen before any design is made"),
                   ("reads", f'<code>{esc(j["name"])}/inputs/</code> only (the fence)'),
                   ("by", esc(f'the designer agent · {r["run"]} (hard)') if r else "—"),
                   ("returns", esc(f'{len(j["topics"])} topics → {len(j["ideas"])} ideas')),
                   ("state", _st(r["status"] if r else "waiting"))])


def _t00_ideas(j: dict, href) -> str:
    designs = {d["id"]: d for d in j["designs"]}
    rows = []
    for i in j["ideas"]:
        d = designs.get(i.get("design", ""))
        rows.append((f'<code>{esc(i.get("id", ""))}</code>', esc(i.get("idea", "")), esc(i.get("topic", "")),
                     (f'<a href="{esc(href("", "", d["path"]))}">{esc(d["id"])}</a> {_st(d["state"])}') if d else "—"))
    return table(("idea", "what", "topic", "its design"), rows)


def _t00_chains(j: dict) -> str:
    rows = [(esc(t.get("id", "")), esc(k + 1), esc(s.get("says", "")), esc(s.get("so", "")), esc(t.get("from", "")))
            for t in j["topics"] for k, s in enumerate(t.get("steps") or [])]
    return table(("topic", "step", "says", "so", "from (in the manifest)"), rows)


def _t99_task(j: dict) -> str:
    r = j["rank"]
    kept = sum(x.get("kept") == "yes" for x in j["ranking"])
    return _pairs([("step", "⑤ Review whole: rank the N + 5, keep the top N, each with its predicted outcome"),
                   ("by", esc(f'another agent · {r["run"]} (hard)') if r else "—"),
                   ("returns", esc(f'ranked {len(j["ranking"])} · kept {kept}')), ("state", _st(r["status"] if r else "waiting"))])


def _coverage(j: dict) -> str:
    kept = [d for d in j["designs"] if d["state"] != "dropped"]
    topics = {i.get("design"): i.get("topic") for i in j["ideas"]}
    covered = sorted({topics.get(d["id"], "") for d in kept} - {""})
    return _pairs([("topics covered by the kept", esc(" · ".join(covered) or "—")),
                   ("kept", esc(f"{len(kept)} designs")), ("each one distinct", "read from the ranking's why")])


def _kept(j: dict, href) -> str:
    kept_, dropped_ = [], []
    for d in j["designs"]:
        dropped = d["state"] == "dropped"
        (dropped_ if dropped else kept_).append(_fold(f'{d["name"][:3]} · {d["id"]}',
                                                     ("dropped, folded" if dropped else "kept") + f' · {_st(d["state"])}', mono=True))
    return "".join(kept_) + (_fold("Dropped by t99, kept for the record", "", "".join(dropped_))
                             if dropped_ else "")


def _task_runs_table(rs: list, sub: str) -> str:
    view = sub if sub in ("hard", "soft") else "All"
    return table(("Run", "kind", "by", "state"), [(f'<code>runs/{esc(r["run"])}/</code>', esc(r["kind"]), esc(r["by"] or "—"),
                                                   _st(r["status"])) for r in rs if view in ("All", r["kind"])])


def _design(d: dict, j: dict, href, root: Path) -> str:
    """The Job's design card, opened (s12's Design display), then its state, its name and its Job."""
    r = {x.get("design"): x for x in j["ranking"]}.get(d["id"], {})
    kept = ("kept" if r.get("kept") == "yes" else "dropped") + f' (rank #{r.get("rank")} of {len(j["ranking"])})' if r else "not ranked yet"
    released = any(x.get("design") == d["id"] for x in j["delivered"])
    return (_qhead("Design", "Process (③): its idea, each element's source", "Review (④ ⑤) · expected outcome") + _card(d, j, href, root)
            + _pairs([("state", _st(d["state"]) + esc(f' · draft {len(d["drafts"])} · {kept} · '
                                                          + ("released" if released else "not released yet"))),
                      ("name", esc(f'{d["short"]} · born with its idea {d["idea"]} in t00')),
                      ("Job", esc(f'{j["name"]} · {j["goal"]} × design method {j["method"]}, version {j["version"]} × inputs {j["inputs"]}'))]))


def _evaluation(d: dict) -> str:
    tests = d["verifies"][-1]["card"].get("tests", {}) if d["verifies"] else {}
    return _pairs([("review (④)", " · ".join(f"{_test(t)} {_st(v)}" for t, v in tests.items()) or "—"),
                   ("by", esc(d["verifies"][-1]["by"]) if d["verifies"] else "—"),
                   ("as written", esc(d["evaluation"] or "—")), ("state", _st(d["state"]))])


def _tests(d: dict, j: dict, b: dict, root: Path) -> str:
    rows = [(f'<code>{esc(v["run"])}</code>', _test(t), _st(res), esc(v["by"])) for v in d["verifies"]
            for t, res in (v["card"].get("tests") or {}).items()]
    return table(("Run", "test", "result", "by"), rows) if rows else '<p class=mut>Not verified yet.</p>'


def _drafts(d: dict, j: dict, b: dict, root: Path) -> str:
    out = []
    files = draft_files(d)
    for k, (r, f) in enumerate(files, 1):
        text = f.read_text(encoding="utf-8", errors="ignore").strip() if f.is_file() else ""
        where = r["run"] + (f" · {f.parent.name}" if r["type"] == "revise" else "")
        out.append((f"draft {k}", _id(where), as_it_reads(text, d["path"] if k == len(files) else None, root,
                                                          venue=R.venue_of(d["path"]))))
    return table(("draft", "Run", "as it reads"), out) if out else '<p class=mut>No draft yet.</p>'


def _task_perf(d: dict, j: dict, b: dict, root: Path) -> str:
    a = R.arm_of(b, j["id"], d["id"])
    s = b["scores"].get((j["id"], d["id"]), {})
    mins = [r["minutes"] for r in d["runs"] if r["minutes"] is not None]
    return _pairs([("tokens", "— <span class=mut>(usage: not in the Run receipt yet)</span>"),
                   ("time", esc(_mins(sum(mins)) if mins else "—")), ("rounds", esc(len(d["drafts"]))),
                   ("predicted", _pred(d["prediction"])), ("frozen", _st(d["prediction"].get("frozen", "—"))),
                   ("observed (Exp)", esc(f'{a.get("observed")} · arm {a.get("arm")} of {a.get("exp")}') if a else "<span class=mut>not tested</span>"),
                   ("matched", (f'direction {_st(s.get("direction"))} · in range {_st(s.get("in_range"))}') if s else "—")])


def _elements(d: dict) -> str:
    rows = [(esc(e.get("element", "")), esc(e.get("words", "")), esc(e.get("from", "")), esc(e.get("because", "")),
             esc(e.get("step", "")), esc(e.get("changed", "") or "—")) for e in d["elements"]]
    return table(("element", "words", "from", "because", "step", "changed"), rows) if rows else \
        '<p class=mut>No elements.yaml yet.</p>'


def _task_delivery(d: dict, j: dict) -> str:
    rel_ = next((x for x in j["delivered"] if x.get("design") == d["id"]), None)
    if rel_:
        return as_read(rel_.get("words", ""), R.venue_of(d["path"])) + f'<p class=mut>released {_st("✅ " + str(rel_.get("released", "")))} · predicted</p>' + _pred(rel_)
    return '<p class=mut>Not released: released with the Job\'s run-release (a person); the prediction freezes then.</p>'
