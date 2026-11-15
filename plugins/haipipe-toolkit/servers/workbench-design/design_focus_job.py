"""A design Job on the focus page (s54 Report, s55 Work): Setup, Ideas, Designs, Ranking and Release, and
`job_view` (split out of design_focus.py)."""
from __future__ import annotations

from pathlib import Path

from live import design_canvas as C
from live import design_reader as R
from live import design_views as V
from live.frame import esc, table
from live.ui_parts import _cap
from live.design_focus_parts import _section
from live.design_focus_layout import CAPTIONS
from live.design_focus_parts import _big, _closed, _copy, _has, _href, _link, _step, _tabs
from live.design_focus_design import (_chain_words, _coverage, _coverage_md, _design_card, _design_state,
                                      _fence_verdict, _goal_name, _job_closed, _pvo, d_state)

# ── the Job (s54 Report, s55 Work) ──────────────────────────────────────────────────────────────────────────────


def _release_line(j: dict, jdir: Path, root: Path) -> str:
    """The Design Method Book's method type a Job runs, linked to its page; "" for a Board with no Book."""
    book = R.book_of(jdir.parent)
    if not (book and j["method"]):
        return ""
    kind = next((p for p in sorted(book.glob("j*_*")) if str(R.front(R.face(p)).get("method", "")) == j["method"]), None)
    return (f'<p>Runs {_link(kind, root, j["release"]) if kind else esc(j["release"])} of '
            f'{_link(book, root, book.name)}.</p>')


def _j_setup(j: dict, b: dict, jdir: Path, root: Path) -> tuple:
    href, jid = _href(root), j["id"]
    pins = (("Goal", bool(j["goal"]), "setup-goal"), ("Method", bool(j["method"]), "setup-method"),
            ("Inputs", bool(j["manifest"]), "setup-inputs"))
    n = sum(ok for _w, ok, _t in pins)
    big = _big(f'{_goal_name(b, j["goal"])} × {C.method_words(j["method"])}, {C.version_words(j["version"])} × '
               f'{C.inputs_words(j["inputs"])}', "all three pinned" if n == 3 else f"{n} of 3 pinned")
    man = j["manifest"]
    res = (big + _section("🎯 Goal", V._setup_strip(j) + V._job_goal(j, b, root), f'{j["goal"]} pinned' if j["goal"] else "not pinned")
           + _section("🧩 Method", _release_line(j, jdir, root) + V._job_method(j, b, root, href=href),
                      j["release"] if j["method"] else "not pinned")
           + _section("📥 Inputs", V._job_inputs(j, b, root, fold=False),
                      f'{j["inputs"]} · frozen {man.get("frozen", "—")}' if man else "no fence yet"))
    proc = _step("📌 The three pins", [
        (f"Set up the {w.lower()}", {"Goal": f'pinned: {j["goal"] or "—"}', "Method": f'{j["method"]} {j["version"]}'.strip()
                                     or "—", "Inputs": f'{j["inputs"] or "—"} · its manifest frozen'}[w],
         "done" if ok else "next", "" if ok else _copy(f"run-{t}-{jid}", "Job", jdir, root)) for w, ok, t in pins])
    return proc, res


def _chain_panel(t: dict, words: dict) -> str:
    steps = t.get("steps") or []
    rows = [(esc(k + 1), esc(s.get("says", "")), esc(s.get("so", "")), esc(s.get("from", "") or t.get("from", "")))
            for k, s in enumerate(steps)]
    return (f'<p class=mut style="margin:0 0 6px">from {esc(t.get("from", ""))}</p>'
            + (table(("step", "says", "so", "from"), rows) if rows else "")
            + '<p style="margin:8px 0 0"><b>Ideas</b> ' + " · ".join(V._id(i, words.get(str(i), "")) for i in t.get("ideas", []))
            + '</p>')


def _j_ideas(j: dict, b: dict, jdir: Path, root: Path) -> tuple:
    href, jid = _href(root), j["id"]
    opened = bool(j["designs"]) or _has(j["runs"], "open-designs")
    fence = _fence_verdict(jdir)
    big = _big("" if j["ideas"] else "No idea reasoned yet",
               ("fence check: " + fence[0]) if fence else "the fence check comes next" if j["ideas"] else "next: reason ideas (t00)")
    words = V._ideas_text(j)
    res = big + _section("🔗 Where each design came from", C.lineage(j, href) or '<p class=mut>Nothing reasoned yet.</p>',
                         f'{len(j["designs"])} designs traced' if j["designs"] else "nothing traced yet")
    tabs = _tabs("chain", [(str(t.get("title") or t.get("id", "")), str(t.get("from", "")).split(" · ")[0], _chain_panel(t, words))
                           for t in j["topics"]])
    res += _section("🔗 Chains", tabs or '<p class=mut>Nothing reasoned yet.</p>',
                    f'{len(j["topics"])} chains' if j["topics"] else "nothing yet")
    n_open = sum(1 for i in j["ideas"] if any(d["id"] == i.get("design") for d in j["designs"]))
    res += _section("💡 The ideas", V._t00_ideas(j, href) if j["ideas"] else '<p class=mut>No idea yet.</p>',
                    f'{n_open} of {len(j["ideas"])} opened as designs' if j["ideas"] else "no idea yet")
    proc = _step("💡 Reason, then open", [
        ("Reason ideas (t00)", f'{len(j["topics"])} topics → {len(j["ideas"])} ideas, from inputs/ only',
         "done" if _closed(j["reason"]) and j["ideas"] else "running" if j["reason"] and j["reason"]["status"] == "running" else "next",
         "" if j["ideas"] else _copy("run-reason-t00", "Task", j["t00"] or jdir, root)),
        ("Check the fence, open the design Tasks", "another agent; one Task per idea, only after a pass",
         "done" if opened else "next" if j["ideas"] else "waits on the ideas",
         "" if opened else _copy(f"run-open-designs-{jid}", "Job", jdir, root))])
    return proc, res


def _j_designs(j: dict, b: dict, jdir: Path, root: Path) -> tuple:
    ds = j["designs"]
    kept = [d for d in ds if d_state(d) in ("kept", "released")]
    dropped = [d for d in ds if d_state(d) == "dropped"]
    big = _big("" if ds else "No design yet",
               ("released" if any(d_state(d) == "released" for d in ds) else "waits for your review" if kept
                else "at work") if ds else "the fence check opens them")
    order = kept + [d for d in ds if d not in kept and d not in dropped] + dropped
    tabs = _tabs("design", [(f'{d["id"]} · {d["short"]}', _design_state(d), _design_card(d, j, root)) for d in order])
    res = big + _section("✏️ The designs, as they read", tabs or '<p class=mut>No design Task yet: the fence check opens them.</p>',
                         f"{len(kept)} kept of {len(ds)}" if ds else "no design yet")
    rows = [(_link(d["path"], root, f'{d["id"]} · {d["short"]}'), _chain_words(d), _design_state(d), "") for d in ds]
    proc = (_step("✏️ Each design's next Run", rows) if rows else
            _section("✏️ Each design's next Run", "<p class=mut>No design Task yet: the fence check opens them.</p>", "waits on the fence check"))
    return proc, res


def _j_ranking(j: dict, b: dict, jdir: Path, root: Path) -> tuple:
    href = _href(root)
    kept = sum(r.get("kept") == "yes" for r in j["ranking"])
    big = _big("" if j["ranking"] else "Not ranked yet",
               "ranked by another agent" if j["ranking"] else "waits on the designs" if not j["designs"] else "next: t99")
    res = big + _section("🏆 Ranking", V._review_whole(j, b, root, href), f"{kept} kept" if j["ranking"] else "not ranked yet")
    res += _section("🧭 Coverage", _coverage(j, root), "checked" if _coverage_md(j) else "from the kept" if j["ranking"] else "not yet")
    proc = _step("🏆 Review the whole", [(
        "Rank, keep the top N, a predicted effect each (t99)", "another agent, in a fresh context",
        "done" if _closed(j["rank"]) and j["ranking"] else "next" if j["designs"] else "waits on the designs",
        "" if j["ranking"] else _copy("run-rank-t99", "Task", j["t99"] or jdir, root))])
    return proc, res


def _frozen(j: dict) -> tuple:
    rows, frozen = [], set()
    for d in j["designs"]:
        p = d["prediction"] if isinstance(d["prediction"], dict) else {}
        if not p.get("predicted") or d_state(d) not in ("kept", "released"):
            continue
        frozen.add(str(p.get("frozen") or "draft"))
        rows.append((f'{esc(d["id"])} · {esc(d["short"])}', esc(p.get("predicted", "")), esc(p.get("against") or "the control"),
                     esc(p.get("why", "")), V._st(str(p.get("frozen") or "draft"))))
    return rows, frozen


def _j_release(j: dict, b: dict, jdir: Path, root: Path) -> tuple:
    from live.design_ladder_act import ready
    designs, why = ready(jdir)
    approved = V._approved(j)[0]
    closed = _job_closed(j)
    tested = [d for d in j["designs"] if R.arm_of(b, j["id"], d["id"])]
    if approved:
        big = _big(f'{_cap(approved.replace("approved", "released"))}' + (f'; tested in {R.arm_of(b, j["id"], tested[0]["id"])["exp"]}'
                                                                          if tested else ""),
                   "closed" if closed else "waiting for you: the close")
    elif designs:
        big = _big(f'{len(designs)} kept design{" waits" if len(designs) == 1 else "s wait"} for your review and approval',
                   "waiting for you")
    else:
        big = _big("Nothing to release yet", "waits on " + (why.split(":")[0][:60] if why else "the ranking"))
    res = big + _section("📄 Released designs", V._job_delivery(j, root, "designs.md"),
                         "released" if j["delivered"] else "not yet")
    rows, frozen = _frozen(j)
    fword = ("frozen " + next(iter(frozen)) if len(frozen) == 1 and "draft" not in frozen else
             "draft: freezes at your sign" if designs else "draft" if rows else "nothing kept yet")
    res += _section("🔒 Frozen predictions", table(("design", "predicted", "against", "why", "frozen"), rows) if rows else
                    '<p class=mut>No kept design yet: t99 keeps the top N, each with its prediction.</p>', fword)
    pvo, _n = _pvo(b, [j], root)
    res += _section("🎯 Predicted vs observed", pvo or '<p class=mut>None of this Job\'s designs is in an Exp yet.</p>',
                    "tested in " + R.arm_of(b, j["id"], tested[0]["id"])["exp"] if tested else "not tested yet")
    rel_state = "done" if approved else "waiting for you" if designs else "waits on " + (why.split(":")[0][:60] if why else "the ranking")
    rows = [("Review and approve", "read each kept design, its prediction and why; one sign freezes and releases", rel_state, ""),
            ("Close the Job", "once every design is released or dropped; you sign",
             "done" if closed else "waits on the release" if not approved else "waiting for you",
             _copy(f'run-close-{j["id"]}', "Job", jdir, root, "Close {folder} once its designs are released; frozen.")
             if approved and not closed else "")]
    panel = V._approve_panel(j, jdir, root, head=False) if designs or approved else ""
    return _step("✍️ Review and approve, then close", rows, panel), res


JOB_PARTS = {"setup": _j_setup, "ideas": _j_ideas, "designs": _j_designs, "ranking": _j_ranking, "release": _j_release}


def job_view(jdir: Path, root: Path, key: str) -> tuple:
    """(caption, lead, process, results, after) of a Job view."""
    j = R.job(jdir)
    b = R.board(R.block_of(jdir.parent) or jdir.parent, with_jobs=False)
    proc, res = JOB_PARTS[key](j, b, jdir, root)
    return CAPTIONS[key], "", proc, res, ""
