"""A design Task on the focus page (s57 Report, s58 Work), by its type: one view per step (t00 reason ideas, one
design, t99 review whole), its drafts strip and its "next: ..." pointer (split out of design_focus.py)."""
from __future__ import annotations

import re
from pathlib import Path

from live import design_canvas as C
from live import design_reader as R
from live import design_views as V
from live.frame import esc, pop, reader, table
from live.ui_parts import _kv
from live.design_focus_parts import _section
from live.design_focus_layout import NEXT, TASK_STEPS
from live.design_focus_parts import _chain, _closed, _copy, _has, _href, _link, _link_btn, _step, _tiles
from live.design_focus_design import (_chain_words, _coverage, _coverage_md, _design_card, _design_state,
                                      _fence_verdict, _md_lines, _section_of, d_state)

# ── the Task (s57 Report, s58 Work), by type ────────────────────────────────────────────────────────────────────
def _flow(inn: tuple, who: tuple, out: tuple) -> str:
    box = lambda word, head, line: f'<div><small>{esc(word)}</small><b>{esc(head)}</b>{esc(line)}</div>'
    arrow = '<span class=dz-arrow aria-hidden=true>→</span>'
    return f'<div class=dz-flow>{box("In", *inn)}{arrow}{box("Who works", *who)}{arrow}{box("Out", *out)}</div>'


NONE = '<p class=dz-part>Your part: none here; an agent works, another agent checks. You sign at the Job.</p>'


def task_steps(tdir: Path) -> tuple:
    icon, typ, steps = TASK_STEPS[R.kind_of(tdir)]
    return icon, typ, steps


def _key(step: str) -> str:
    return re.sub(r"\W+", "-", step.lower())


def _stays_out(j: dict, b: dict, root: Path) -> tuple:
    """What stays out of the fence: the Block's inputs version files the method's step ① does not see, and what no
    design may use (the goal's leave-out, the shared rules' leave-out list)."""
    version = next((v for v in b["inputs"] if v["id"] == j["inputs"]), None)
    have = {f["name"].rstrip("/") for f in j["files"]}
    files = sorted(p.name for p in version["path"].iterdir() if p.is_file() and p.name != "manifest.yaml"
                   and p.name not in have) if version and version["path"].is_dir() else []
    seen = V._keyed(j["fence"] / "goal.md")
    leave = [x for x in ([seen.get("leave out", "")] + V._bullets(j["fence"] / "rules.md", "Leave out")) if x]
    sees = (j["method_card"].get("steps") or {}).get("① See input", "")
    body = _kv([("not in the fence", esc(" · ".join(files)) + (f' <span class=mut>(in {esc(C.inputs_words(j["inputs"]))}; '
                                                              f'{esc(C.method_words(j["method"]))}\'s step ① does not see it)</span>'
                                                              if files else "") if files else "every file of the inputs version is in"),
                ("step ① sees", esc(sees or "—")), ("no design may use", V._ul(leave) if leave else "—")])
    return body, (f'{len(files)} file{"" if len(files) == 1 else "s"} left out' if files else "nothing left out")


def _topics(j: dict) -> str:
    return _tiles([(str(t.get("title") or t.get("id", "")),
                    f'{len(t.get("ideas", []))} idea{"" if len(t.get("ideas", [])) == 1 else "s"} · from '
                    f'{str(t.get("from", "")).split(" · ")[0]}') for t in j["topics"]])


def _opened_chain(j: dict) -> str:
    ds = j["designs"]
    names = (ds[0]["name"] + (f" … {ds[-1]['name']}" if len(ds) > 1 else "")) if ds else "none yet"
    return _chain([("② ideas", "t00", (j["t00"].name if j["t00"] else "not opened")),
                   ("③ ④ designs", f'{len(ds)} design Task{"" if len(ds) == 1 else "s"}', names),
                   ("⑤ rank", "t99", j["t99"].name if j["t99"] else "not opened")])


def _feedback(d: dict, root: Path) -> tuple:
    """The frozen feedback each failed verify gave, and what the revise read: (html, word)."""
    out = []
    for i, v in enumerate(d["verifies"]):
        if v["status"] != "failed":
            continue
        review = v["result"] / "review.md"
        change = _section_of(review, "What to change")
        tests = " · ".join(f"{V.TESTS.get(t, t)} {r}" for t, r in (v["card"].get("tests") or {}).items())
        out.append(f'<p style="margin:0 0 4px"><b>{esc(v["run"])}</b> <span class=mut>· {esc(tests)} · {esc(v["by"])}</span></p>'
                   + (_md_lines(change) if change else '<p class=mut>Its review names no change.</p>')
                   + (f'<p class=mut style="margin:4px 0 10px">{pop(reader(review, root), "review.md", "review.md ↗")}</p>'
                      if review.is_file() else ""))
    if not out:
        return "", ""
    return "".join(out), "❗"


def _changes(d: dict, root: Path) -> tuple:
    """What each revise changed: the draft before beside the draft after, and the pass's own summary."""
    files = V.draft_files(d)
    if len(files) < 2:
        return "", ""
    venue = R.venue_of(d["path"])
    where = lambda r, f: r["run"] + (f" · {f.parent.name}" if r["type"] == "revise" else "")
    out = []
    for k in range(1, len(files)):
        (r0, f0), (r1, f1) = files[k - 1], files[k]
        before = f0.read_text(encoding="utf-8", errors="ignore") if f0.is_file() else ""
        after = f1.read_text(encoding="utf-8", errors="ignore") if f1.is_file() else ""
        summary = _section_of(f1.parent / "pass.md", "Summary")
        out.append(f'<div class=dz-pair><div><small>draft {k} · {esc(where(r0, f0))}</small>{V.as_read(before, venue)}</div>'
                   f'<div><small>draft {k + 1} · {esc(where(r1, f1))}</small>{V.as_read(after, venue)}</div></div>'
                   + (f'<p style="margin:2px 0 12px">{esc(summary)}</p>' if summary else ""))
    return "".join(out), f"{len(out)} revise pass" + ("" if len(out) == 1 else "es")


def _walk(d: dict, j: dict) -> tuple:
    """A design's state walk (hai-design-workflow): draft → verify → revise → passed → kept | dropped → released,
    each step with its word."""
    n = len(V.draft_files(d)) or len(d["drafts"])
    steps = [("③ draft", "v1", "done" if n else "not yet")]
    for i, v in enumerate(d["verifies"]):
        steps.append((f"④ verify v{i + 1}", v["status"], v["by"].split(" (")[0] or "another agent"))
        if v["status"] == "failed" and i + 1 < n:
            steps.append(("revise", f"v{i + 2}", "done"))
    state = d_state(d)
    steps.append(("⑤ rank", state if state in ("kept", "dropped", "released") else "not ranked yet", "by t99"))
    if state != "dropped":
        steps.append(("release", "released" if state == "released" else "not yet", "a person signs at the Job"))
    return _chain(steps), state if state in ("kept", "dropped", "released") else _design_state(d)


def _strip(d: dict) -> str:
    """The drafts strip, above every view of a design Task (b12 j01 B1 to B4): v1 · v2 · kept."""
    chips, n = [], len(V.draft_files(d)) or len(d["drafts"])
    for i in range(n):
        v = d["verifies"][i] if i < len(d["verifies"]) else None
        word = ("verify " + v["status"]) if v else "to verify"
        bad = " bad" if v and v["status"] == "failed" else ""
        on = " on" if i == n - 1 else ""
        chips.append(f'<span class="dz-chip{bad}{on}">v{i + 1} · {esc(word)}</span>')
    state = d_state(d)
    if state in ("kept", "dropped", "released"):
        chips.append(f'<span class=dz-chip>{esc(state)} · {"by t99" if state != "released" else "at the Job"}</span>')
    if not chips:
        chips.append('<span class=dz-chip>not drafted yet</span>')
    return f'<p class=dz-strip><b>✏️ Drafts of {esc(d["id"])}</b>' + ' <span class=mut>→</span> '.join(chips) + '</p>'


def _kept_table(j: dict, root: Path) -> str:
    """Each design and where t99 left it: kept first, the dropped kept for the record (no fold, no count in a label)."""
    rank = {r.get("design"): r for r in j["ranking"]}
    order = sorted(j["designs"], key=lambda d: (d_state(d) == "dropped", int(rank.get(d["id"], {}).get("rank") or 99)
                                                if str(rank.get(d["id"], {}).get("rank") or "").isdigit() else 99))
    rows = [(_link(d["path"], root, f'{d["id"]} · {d["short"]}'), esc(str(rank.get(d["id"], {}).get("rank") or "—")),
             V._st(d_state(d))) for d in order]
    return table(("design", "rank", "state"), rows) if rows else ""


def _next_link(tdir: Path, root: Path, key: str) -> str:
    """The "next: …" pointer under a Task's Work: the next step's view, in this Task or the next one."""
    if key not in NEXT:
        return ""
    words, to = NEXT[key]
    j = tdir.parent
    if to == "design":
        target = next((p for p in sorted(j.iterdir()) if R.DESIGN_TASK.match(p.name)), None)
        group = "work-draft"
    elif to == "t99":
        target, group = next(iter(sorted(j.glob("t99_*"))), None), "work-rank"
    elif to == "release":
        target, group = j, "work-release"
    else:
        target, group = tdir, "work-" + to
    link = _link_btn(target, root, "work", group, words) if target is not None else esc(words)
    return f'<p class=dz-next><b>next:</b> {link}</p>'


def task_view(tdir: Path, root: Path, step: str) -> tuple:
    """(caption, process, results) of one step of a Task: its flow and row, then what the step wrote."""
    j, href = R.job(tdir.parent), _href(root)
    b = R.board(R.block_of(tdir.parent.parent) or tdir.parent.parent)
    kind, jid = R.kind_of(tdir), j["id"]
    icon, typ, _steps = TASK_STEPS[kind]
    opened = bool(j["designs"]) or _has(j["runs"], "open-designs")
    if kind == "t00":
        fence = _fence_verdict(tdir.parent)

        def inputs_res():
            out, word = _stays_out(j, b, root)
            return (_section("📂 What the fence holds", V._job_inputs(j, b, root, fold=False),
                             f'{len(j["files"])} files · frozen {j["manifest"].get("frozen", "—")}' if j["manifest"] else "no fence yet")
                    + _section("🚫 What stays out", out, word))

        def fence_res():
            ds = j["designs"]
            verdict = (f'<p class=dz-verdict>{esc(fence[0])}</p>'
                       if fence else '<p class=mut>Not checked yet: another agent checks the fence before any design Task opens.</p>')
            rows = [(_link(d["path"], root, f'{d["id"]} · {d["short"]}'), esc(d["idea"]), V._st(d["state"])) for d in ds]
            return (_section("✅ The verdict", verdict, fence[0] if fence else "not checked yet")
                    + _section("📂 Tasks opened", _opened_chain(j) + (table(("design", "idea", "state"), rows) if rows else ""),
                               f'{len(ds)} design Tasks' if ds else "none yet"))
        spec = {"Inputs": (("Inputs version", j["inputs"] or "—"), ("🤖 Designer agent", "keep what step ① names"),
                           ("inputs/ + manifest.yaml", "every file the work may read"),
                           "done" if j["manifest"] else "next", f"run-setup-inputs-{jid}", "Job", tdir.parent, inputs_res),
                "Chains": (("inputs/", "goal · method · rules"), ("🤖 Designer agent", "② reason, step by step"),
                           ("chains.yaml", "each step and its source"),
                           "done" if j["topics"] else "next", "run-reason-t00", "Task", tdir,
                           lambda: (_section("🔗 Reasoning chains", V._t00_chains(j), f'{len(j["topics"])} chains')
                                    + _section("🧭 Topics", _topics(j), f'{len(j["topics"])} topics'))
                           if j["topics"] else ""),
                "Ideas": (("chains.yaml", "the reasoning"), ("🤖 Designer agent", "one idea per chain's end"),
                          ("ideas.yaml", f'{len(j["ideas"])} ideas'),
                          "done" if j["ideas"] else "next", "run-reason-t00", "Task", tdir,
                          lambda: _section("💡 The ideas", V._t00_ideas(j, href), f'{len(j["ideas"])} ideas') if j["ideas"] else ""),
                "Fence check": (("chains.yaml", "every step's from: line"), ("🤖 Reviewer agent", "a fresh context"),
                                ("fence-check.md", "pass, then the design Tasks open"),
                                "done" if opened else "next" if j["ideas"] else "waits on the ideas",
                                f"run-open-designs-{jid}", "Job", tdir.parent, fence_res)}
    elif kind == "design":
        d = R.design(tdir)
        did = d["id"]
        state = dstate = _design_state(d)               # dstate: the design's own word (the closures below read it)
        k = len(V.draft_files(d))                       # drafts so far: the generate's, then one per revise pass
        revised = max(k - 1, 0)

        def verify_res():
            fb, word = _feedback(d, root)
            return (_section("🧪 Tests", V._tests(d, j, b, root), d["verifies"][-1]["status"] if d["verifies"] else "not yet")
                    + _section("📝 Feedback", fb or '<p class=mut>No feedback to act on: every verify passed.</p>',
                               word or ("none needed" if d["verifies"] else "not verified yet")))

        def revise_res():
            ch, word = _changes(d, root)
            return (_section("↔️ What changed", ch or '<p class=mut>Not revised: it needed no revise.</p>', word or "not needed")
                    + _section("🔁 The loop", f'<p style="margin:0 0 6px">{esc(_chain_words(d))}</p><p class=mut>fail → revise '
                               'what the verify named → verify again, until it passes or t99 drops it</p>', dstate))

        def state_res():
            walk, word = _walk(d, j)
            return (_section("🪜 Its walk", walk, word)
                    + _section("📊 Its prediction", V._task_perf(d, j, b, root),
                               str((d["prediction"] or {}).get("frozen") or ("draft" if d["prediction"] else "none yet"))))
        spec = {"Draft": ((f'Idea {d["idea"] or "—"}', "from t00's ideas.yaml, and inputs/ only"),
                          ("🤖 Designer agent", "③ conduct the method's process"), ("Draft + elements.yaml", f'{k} draft{"" if k == 1 else "s"}'),
                          "done" if d["drafts"] else "next", f"run-generate-{did}", "Task", tdir,
                          lambda: (_section("📄 The design, as it reads", _design_card(d, j, root), dstate)
                                   + _section("🧩 Elements and sources", V._elements(d),
                                              f'{len(d["elements"])} elements' if d["elements"] else "none yet"))),
                "Verify": (("The last draft", "the design + elements.yaml"), ("🤖 Reviewer agent", "④ T0 rules · T1 sources, fresh"),
                           ("verdict", d["verifies"][-1]["status"] if d["verifies"] else "not yet"),
                           "done" if d["verifies"] and d["verifies"][-1]["status"] == "passed" else
                           "next" if d["drafts"] else "waits on the draft", f"run-verify-{did}-v{max(k, 1)}", "Task", tdir, verify_res),
                "Revise": (("A failed verify", "its notes"), ("🤖 Designer agent", "one more draft, then verify again"),
                           ("Draft v" + str(k + 1 if state == "revise next" else k),
                            f"{revised} revision{'' if revised == 1 else 's'}"),
                           "next" if state == "revise next" else "done" if revised else "not needed",
                           f"run-revise-{did}", "Task", tdir, revise_res),
                "State": (("t99's ranking", "rank and kept"), ("🤖 Reviewer agent", "⑤ at t99; you sign at the Job"),
                          ("prediction.yaml", str((d["prediction"] or {}).get("frozen") or "draft")),
                          {"kept": "kept", "released": "done", "dropped": "dropped"}.get(d_state(d), state),
                          "", "Task", tdir, state_res)}
    else:
        kept = [d for d in j["designs"] if d_state(d) in ("kept", "released")]
        dropped = [d for d in j["designs"] if d_state(d) == "dropped"]
        failed = [d for d in j["designs"] if d["verifies"] and d["verifies"][-1]["status"] == "failed"]

        def kept_res():
            approved = V._approved(j)[0]
            to = ('<p style="margin:0 0 6px">The kept go to the Job\'s Review and approve, where a person signs once: the '
                  'predictions freeze and the designs are released.</p>'
                  + _link_btn(j["path"], root, "work", "work-release", "Open the Job's Release"))
            return (_section("✅ Kept and dropped", _tiles([(str(len(kept)), f'kept: the goal\'s N = {j["n"]}'),
                                                           (str(len(dropped)), "dropped, kept for the record"),
                                                           (str(len(failed)), "failed their last verify")])
                             + _kept_table(j, root), f"{len(kept)} kept" if j["ranking"] else "not ranked yet")
                    + _section("➡️ To the release", to, approved.replace("approved", "released") if approved
                               else "at the Job" if kept else "waits on the ranking"))
        spec = {"Rank": (("The designs", f'{len(j["designs"])} drafted'), ("🤖 Reviewer agent", "⑤ rank, a predicted effect each"),
                         ("ranking.csv", "rank · predicted · why · kept"),
                         "done" if _closed(j["rank"]) and j["ranking"] else "next" if j["designs"] else "waits on the designs",
                         "run-rank-t99", "Task", tdir,
                         lambda: _section("🏆 Ranking", V._review_whole(j, b, root, href),
                                          f'{len(kept)} kept' if j["ranking"] else "not ranked yet")),
                "Coverage": (("ranking.csv", "the kept designs"), ("🤖 Reviewer agent", "which parts of the goal they cover"),
                             ("coverage", "by goal part"), "done" if j["ranking"] else "waits on the ranking", "", "Task", tdir,
                             lambda: _section("🧩 Goal parts", _coverage(j, root),
                                              "checked" if _coverage_md(j) else "from the kept" if j["ranking"] else "not yet")),
                "Kept": (("ranking.csv", "the top N"), ("🤖 Reviewer agent", "projected onto each design's face"),
                         ("kept", f'{len(kept)} of N = {j["n"]}'), "done" if kept else "waits on the ranking", "", "Task", tdir,
                         kept_res)}
    inn, who, out, state, label, level, folder, result = spec[step]
    row = [(f'{icon} {esc(step)}', f"{typ} · {who[0].split(' ', 1)[-1]}", state,
            _copy(label, level, folder, root) if label and state in ("next", "revise next") else "")]
    part = NONE
    if kind == "t99" and step == "Kept":
        part = (f'<p class=dz-part>Your part is at the Job: {_link_btn(j["path"], root, "work", "work-release", "Review and approve")}'
                f' freezes the kept designs\' predictions and releases them.</p>')
    proc = _step(f"{icon} {step}", row, _flow(inn, who, out) + part)
    res = result() or _section(f"📊 {step}", "<p class=mut>Nothing here yet.</p>", "nothing yet")
    return f"{typ} · {step}: what the step reads, who works, what it writes", proc, res


def _task_build(tdir: Path, root: Path, key: str, steps: tuple) -> tuple:
    step = next(s for s in steps if _key(s) == key)
    caption, proc, res = task_view(tdir, root, step)
    lead = _strip(R.design(tdir)) if R.kind_of(tdir) == "design" else ""
    return caption, lead, proc, res, _next_link(tdir, root, key)
