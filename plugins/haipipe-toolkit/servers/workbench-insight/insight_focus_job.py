"""A Job on the focus page: what a person signs, the Overall answer, the question × segment grid, this Job against
the previous one, and the Job's Work and Report views assembled."""

from __future__ import annotations

import json
from pathlib import Path

from live import insight_plan_c as P
from live import insight_views as V
from live.frame import esc, rel
from live.ui_parts import _kv, _numbered
from live.insight_view_parts import _pill, _section
from live.insight_focus_parts import (
    VIEWS, _ctable, is_job, _facts, _copy, _ask, _pop, _step, _big, _proto_work, _written, _dot, DOT, KEY,
    _cap1, _page, _work_page, _map_view, _done, draw_map, MOVED, _qname)


# ── a Job: its signs, its views ────────────────────────────────────────────────────────────────────────────────
WAIT_WORD = {"1 · Launch": "the launch", "2 · Run": "the runs", "3 · Write": "the pages", "4 · Check": "the checks",
             "5 · Compare": "the comparison"}


def _plan_signed(x: dict) -> bool:
    return str(x["r"]["face"].get("signed") or "").startswith("✅")


def _sign_rows(x: dict) -> list:
    """Your two acts on a Job, in their order: sign the plan (in the Question Book; the row names the act only, no state sentence),
    then close the Job (greyed until every step before it is done). Steps of the Overall's ⚙️ Process (R2)."""
    j, r, st = x["j"], x["r"], x["st"]
    plan = r.get("label") or j["release"]
    if _plan_signed(x):
        sign = (f"Sign {plan}", "signed in the Question Book", _done(r["face"]["signed"]), "")
    else:
        go = (f'<a class=fd-btn data-pop="{esc(plan)}" href="{esc(_proto_work(r["job"], x["root"]))}">Sign in the Question Book</a>'
              if r.get("job") else "")
        sign = (f"Sign {plan}", "", "waiting for you", go)
    waits = [WAIT_WORD[s] for s in V.WORK_STEPS[:-1] if st[s] not in ("done", "optional")]
    if j["state"] == "closed":
        close = ("Close the Job", "locked: its pages, Runs and comparison", _done(j["face"].get("signed")), "")
    elif waits:
        close = ("Close the Job", "first: " + ", ".join(waits),
                 "waits on " + waits[0], '<button type=button class=fd-btn disabled>Close</button>')
    else:
        body = esc(json.dumps({"action": "close", "job": x["folder"]}))
        close = ("Close the Job", "every step is done: read what the close locks, then sign", "waiting for you",
                 f'<span class="in-sign sign-row"><label><input type=checkbox name=attest> I read what it locks</label>'
                 f'<button type=button class=fd-btn data-post="/_board/insight-act" data-body="{body}" '
                 f'data-fields="attest">Sign the close</button></span>')
    return [sign, close]


def _overall_state(f: dict) -> str:
    xs = [t for t in f["live"] if t["qid"][:1] == "X"]
    done = {t["name"] for t in f["written"]}
    waits = [t["qid"] for t in f["live"] if t["qid"][:1] in "DIKW" and t["name"] not in done]
    if not xs:
        return "no Executive question"
    if all(t["name"] in done for t in xs):
        return "done"
    return "waits on " + ", ".join(waits[:4]) + (" …" if len(waits) > 4 else "") if waits else "ready"


def _overall_proc(x: dict) -> str:
    state = _overall_state(x["f"])
    out = _step("🔏 Sign and close", _sign_rows(x))
    if x["st"]["6 · Close"] == "sign":                      # what it freezes, once the close is yours to sign
        out += _section("🔒 What the close locks", _kv([
            ("pages", "every page as it reads now"), ("Runs", "every Run and its receipt")])
            + _ask(x, "Close the Job", "Close", "or sign it in the step above"), "ready to sign")
    return out + _step("✍️ Write the Overall Report", [(
        "Write the Overall Report", "each Executive question's page from the answers below it, then its one page",
        state, _copy(x, "Write the overall report") if state == "ready" else "")])


def _overall_res(x: dict, eid: str = "ov") -> str:
    """The Job's Overall (Report, and Work's Results): the pair in one large line, the Overall Report as side tabs (one
    Executive question open, its figure beside), then this Job's facts."""
    j, b, r = x["j"], x["b"], x["r"]
    xs = V._executive(j)
    first = next((t for t in xs if _written(t)), None)    # the headline is X01's one line once written (round 1, yes)
    big = _big(str(first["face"]["answer"]) if first else
               f'Overall Report · {P.plan_code(j["release"])} × {P.freeze_code(j["data"])}')
    written, asked = V.written_of(xs)
    ov = (_section("📄 Overall Report", V._overall_tabs(j, b, r, x["root"], eid), V.far(written, asked, "written"))
          if xs else _section("📄 Overall Report", "<p class=mut>This question version asks no Executive question, so it has no "
                                                  "Overall Report.</p>", "none in this version"))
    closed = str((j.get("face") or {}).get("signed") or "") if j["state"] == "closed" else ""
    changed = ("nothing (the first Job)" if not j["previous"] or j["moved"] == "start"
               else f'{MOVED.get(j["moved"], j["moved"] or "—")}, from {j["previous"][:3]}')
    facts = [("questions", esc(V._rlabel(b, j["release"]))), ("data", esc(V._vlabel(b, j["data"]))),
             ("changed from the Job before", esc(changed))]
    word = ("closed " + closed).strip() if j["state"] == "closed" else "open"   # the sign waits in 🔏 Sign and close, not here
    return big + ov + _section("🧷 This Job", _kv(facts), word)


def _cuts(x: dict) -> list:
    cuts = []
    for t in x["f"]["asked"]:
        for h in t["hard"]:
            p = h.get("partition") or h["run"].split("_", 1)[-1]
            if p not in cuts:
                cuts.append(p)
    for label in V._part_names(x["r"].get("partitions") or []):
        key = V._part_key(label)
        if key and key not in cuts and key != V.OVERALL:
            cuts.append(key)
    return cuts


QA_CSS = """<style>
.qa{margin:4px 0}.qa details{border-bottom:1px solid #e6e8eb}
.qa summary{display:flex;align-items:center;gap:14px;padding:10px 4px;cursor:pointer;list-style:none}
.qa summary::-webkit-details-marker{display:none}.qa summary::before{content:"▸";color:#8a8f98;width:10px}
.qa details[open] summary::before{content:"▾"}
.qa .lv{font-weight:700;min-width:110px}.qa .dots{display:flex;flex-wrap:wrap;gap:3px;flex:1}
.qa .dot{width:11px;height:11px;border-radius:50%;border:1.5px solid #1a7f37;box-sizing:border-box}
.qa .dot.on{background:#1a7f37}.qa .dot.half{background:#f2c94c;border-color:#b58105}.qa .dot.off{border-color:#c4c8ce}
.qa .tally{color:#57606a;font-size:13px;white-space:nowrap}
.qa ol{list-style:none;margin:0 0 8px;padding:0}
.qa li{display:grid;grid-template-columns:42px 1fr;gap:4px 10px;padding:8px 4px 8px 26px;border-top:1px solid #f0f1f3}
.qa li a.id{font-weight:700;text-decoration:none;color:#1864ab}.qa li .q{font-weight:600}
.qa li .a{grid-column:2;color:#24292f;line-height:1.45}.qa li .a.none{color:#8a8f98;font-style:italic}
.qa .in-grid{padding:0 4px 10px 26px}
</style>"""


def _grid(x: dict, verbs: bool) -> str:
    """The question × segment grid, folded by DIKW level, one dot a cell: a
    level's closed row is its questions' dots and how many are answered; open, a row per question, a dot per segment, its
    page and its check. With `verbs` (Work), each cell its next verb: launch a segment not run, write a page ready to
    write, check a written page."""
    f, root = x["f"], x["root"]
    cuts = _cuts(x)
    ran = {t["name"] for t in f["ran"]}
    written, checked, returned = ({t["name"] for t in f[k]} for k in ("written", "checked", "returned"))
    folds, opened = [], False
    for lv in V.WRITE_ORDER:
        ts = [t for t in f["live"] if t["qid"][:1] == lv]
        if not ts:
            continue
        rows, dots = [], []
        for t in ts:
            by = {(h.get("partition") or h["run"].split("_", 1)[-1]): h for h in t["hard"]}
            cells = []
            for p in cuts:
                if lv not in V.RUN_LEVELS:
                    cells.append("<span class=mut>—</span>")
                elif p in by:                                # a segment its question asks: its Run, planned or run
                    s = str(by[p].get("status") or "planned").lower()
                    mark = _pill("launch") if verbs and s == "planned" else _dot(DOT.get(s, "off"), f"{p} · {s}")
                    cells.append(_pop(V.run_url(by[p]["path"], root), by[p]["run"], mark))
                else:                                        # a segment the plan does not ask of this question
                    cells.append("<span class=mut>—</span>")
            writing = any(V._rtype(r) == "write" and str(r.get("status") or "").lower() in ("running", "started")
                          for r in t["soft"])
            if t["name"] in returned:                       # its reason on its own row (round 1)
                why = str(t["face"].get("check") or "").lstrip("↩ ").split(" · ", 2)
                page = _pill("↩ rewrite") + (f'<span class=in-why>{esc(why[-1])}</span>' if len(why) == 3 else "")
            elif writing:
                page = _pill("running")
            elif t["name"] in written:
                page = V._page_link(t, root)
            elif lv not in V.RUN_LEVELS or t["name"] in ran:
                page = _pill("write") if verbs else "<span class=mut>⬜</span>"
            else:
                page = "<span class=mut>waits on runs</span>"
            if t["name"] in checked:
                check = "✅"
            elif t["name"] in written:
                check = V._check_form(t, root) if verbs else "<span class=mut>⬜</span>"
            else:
                check = "<span class=mut>—</span>"
            dots.append(f'<span class="dot {"on" if t["name"] in written else "off"}" title="{esc(t["qid"])} · '
                        f'{"written" if t["name"] in written else "to write"}"></span>')
            ask = str((x["r"]["questions"].get(t["qid"]) or {}).get("question") or "")
            rows.append((f'<a href="/_board/insight-run?answer={esc(rel(Path(t["path"]), root))}" data-pop="{esc(t["name"])} · '
                         f'the page" title="{esc(ask)}">{esc(_qname(t["qid"], t))}</a>',) + tuple(cells) + (page, check))
        done = sum(t["name"] in written for t in ts)
        opens = done < len(ts) and not opened          # the first level with work left opens (round 2, j02)
        opened = opened or opens
        folds.append(f'<details{" open" if opens else ""}><summary><span class=lv>{esc(V.LEVEL_WORD[lv])}</span>'
                     f'<span class=dots>{"".join(dots)}</span><span class=tally>{V.far(done, len(ts), "answered")}</span></summary>'
                     f'<div class=in-grid>{_ctable(("question",) + tuple(V._label(p) for p in cuts) + ("page", "check"), rows)}'
                     f'</div></details>')
    if not folds:
        return "<p class=mut>This Job asks no question yet.</p>"
    if not opened:                                     # every level written: the first opens
        folds[0] = folds[0].replace("<details>", "<details open>", 1)
    return QA_CSS + KEY + f'<div class=qa>{"".join(folds)}</div>'


def _grid_word(x: dict) -> str:
    f = x["f"]
    return V.far(len(f["written"]), len(f["live"]), "answered")


def _grid_res(x: dict, verbs: bool) -> str:
    f = x["f"]
    left = [t for t in f["live"] if t["name"] not in {w["name"] for w in f["written"]}]
    name = lambda t: t["name"].split("_", 2)[-1].replace("-", " ")      # the question's name, never its id (round 2)
    big = _big("Every question answered at the segments it asks" if not left else
               "Still to write: " + ", ".join(name(t) for t in left[:6]))
    return big + _section("🔲 Progress", _grid(x, verbs), _grid_word(x))


def _grid_proc(x: dict) -> str:
    f, st = x["f"], x["st"]
    ran = {t["name"] for t in f["ran"]}
    ready = [t for t in f["unwritten"] if t["qid"][:1] not in V.RUN_LEVELS or t["name"] in ran]
    lv = next((t["qid"][:1] for t in sorted(ready, key=lambda t: V.WRITE_ORDER.find(t["qid"][:1]))), "")
    state = lambda step, left, word: ("done" if st[step] == "done" else word if left else "ready")
    rows = [("Launch all", "one Run per question × segment, from the question version's thresholds",
             state("2 · Run", len(f["unrun"]), "to run"),
             _copy(x, "Run a segment", V._still(f["unrun"], "Still to run")) if f["unrun"] else ""),
            ("Write all", f"the next DIKW level first: {lv} · {V.LEVEL_WORD[lv]}" if lv else "pages are written up the levels",
             state("3 · Write", len(f["unwritten"]), "to write") if ready or st["3 · Write"] == "done" else "waits on runs",
             _copy(x, V.WRITE_CARD[lv], V._still([t for t in ready if t["qid"][:1] == lv], "Still to write")) if lv else ""),
            ("Check all", "alignment and CHECK, by another agent; or check a page yourself in its row",
             ("done" if st["4 · Check"] == "done" else "to check" if f["unchecked"] else "ready") if f["written"]
             else "waits on pages",                                                  # a check carries no count
             _copy(x, "Check a report", V._still(f["unchecked"], "Still to check")) if f["unchecked"] else "")]
    now = "".join(f'<p class=mut>🏃 {V._run_link(r, x["root"], r["run"])}</p>' for r in f["running"])
    return _step("🧮 Next in each cell", rows, now)


def _vs_res(x: dict) -> str:
    j = x["j"]
    what = MOVED.get(j["moved"], j["moved"] or "—")
    rows = (j["vs"] or {}).get("rows", {})
    changed = [q for q, v in rows.items() if str(v.get("status")).lower() == "changed"]
    word = ("changed" if changed else "none changed") if j["vs"] else "to compare"
    return (_big(f'Against {x["prev"]}: only {what} moved, so a changed answer has one cause')
            + _section("🔁 Changes", V._vs_previous(j, x["root"], tabs="vs"), word))


def _vs_proc(x: dict) -> str:
    j, f, st = x["j"], x["f"], x["st"]
    prev = x["prev"]
    rows_vs = (j["vs"] or {}).get("rows", {})
    changed = [q for q, v in rows_vs.items() if str(v.get("status")).lower() in ("changed", "new question", "new finding", "dropped")]
    proposed = any(V._closed(r) for r in f["own"].get("propose", []))
    compared = bool(j["vs"]) or any(V._closed(r) for r in f["own"].get("compare", []))
    rows = [(f"Compare with {prev}", f"run-compare-{x['me']} · every answer against {prev}",
             "done" if compared else "ready" if st["4 · Check"] == "done" else "waits on checks", ""),
            ("Propose questions", f"run-propose-{x['me']} · each change or gap to the Question Book's Ideas"
             + (" · changed answers to turn into ideas" if compared and changed else ""),
             "done" if proposed else "ready" if compared else "waits on Compare", "")]
    prompts = ("" if compared else _ask(x, "Compare with the Job before", "Compare", "use /haipipe-insight")) + \
        ("" if proposed or not compared else _ask(x, "Propose questions", "Propose", "use /haipipe-insight"))
    return _step("🔁 Compare, then propose", rows, prompts)


def _job_mindmap(jdir: Path, root: Path):
    """A Job's MindMap: a card per DIKW level, each Task a leaf with the question it
    asks, from the plan; how far each has got stays in Status and the Grid."""
    def build():
        x = _facts(jdir, root)
        branches = []
        for lv, name, _ in V.LEVELS:
            leaves = []
            for t in (t for t in x["j"]["tasks"] if t["qid"][:1] == lv):
                q = x["r"]["questions"].get(t["qid"], {})
                asks = str(q.get("question") or V._spec(q).get("question") or "").strip() or t["name"].split("_", 2)[-1].replace("-", " ")
                leaves.append(f'[{t["qid"]}] {_cap1(asks)}')
            branches.append((name, leaves))
        return draw_map(jdir, root, branches, "This Job asks no question yet.")
    return build


def job_work_views(jdir: Path, root: Path, items=(), item_html=None) -> dict:
    """{key: (name, build)}: the Job's Work views in the Report's letters, each ⚙️ Process then 📊 Results (the
    Report's view by the same function); vs previous from the second Job; the MindMap last. {} for any other folder.
    `items` and `item_html` are no longer drawn here: the page's own 🙋 Interaction shows each view's forms (R2)."""
    if not is_job(jdir):
        return {}
    root = root.resolve()
    parts = {"overall": (_overall_proc, lambda x: _overall_res(x)), "grid": (_grid_proc, lambda x: _grid_res(x, True)),
             "vs-previous": (_vs_proc, _vs_res)}
    views = {}
    for key, name in VIEWS:
        if key == "vs-previous" and not P.job(jdir)["previous"]:
            continue                                         # hidden until a second Job

        def build(key=key):
            x = _facts(jdir, root)
            proc, res = parts[key]
            return _work_page(proc(x), res(x))
        views["work-" + key] = (name, build)
    views["work-mindmap"] = _map_view(_job_mindmap(jdir, root))
    return views


def job_report_views(jdir: Path, root: Path) -> dict:
    """{key: (name, build)}: the Job's Report, its sections only: Findings · Changes (from the second Job) · Progress ·
    MindMap (Tasks by DIKW level); {} for any other folder."""
    if not is_job(jdir):
        return {}
    root = root.resolve()
    N = dict(VIEWS)                                    # the button words, said once (VIEWS)
    views = {"overall": (N["overall"], lambda: _page(_numbered(_overall_res(_facts(jdir, root)))))}
    if P.job(jdir)["previous"]:
        views["vs-previous"] = (N["vs-previous"], lambda: _page(_numbered(_vs_res(_facts(jdir, root)))))
    views["grid"] = (N["grid"], lambda: _page(_numbered(_grid_res(_facts(jdir, root), False))))
    views["mindmap"] = ("MindMap", _job_mindmap(jdir, root))
    return views
