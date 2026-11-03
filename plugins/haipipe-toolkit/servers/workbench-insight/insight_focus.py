"""An insight Job's Work on the focus page (b11 j01 s55, JL 261101): the Report's letters, A Overall · B Grid ·
C vs previous (The pair's facts folded into A, s54 round 2), each view in two bands, ⚙️ Process then 📊 Results, drawn with the shared parts every
theme's page uses (ui_parts: numbered bars, bands, to-do rows with state pills, the one Prompt box), as the paper's
version Work (paper_version.version_work_views) and the labeling Task's steps (labeling_steps.view_html).

The round 1 reviews (s55 review/cell-s1-r01.md) set the shape: your signs first on every view (sign the plan, then
close the Job, the close greyed until the checks are done); Work B is the Report's question × cut grid, each cell its
next verb, with "all" verbs on its heading; every row ends in a state word; a Run's id sits behind the step's name.
focus_page.py asks job_work_views; the steps' facts and the person's actions stay insight_views' and insight_act's."""
from __future__ import annotations

import json
import re
from pathlib import Path

from live import insight_plan_c as P
from live import insight_views as V
from live.frame import esc, rel, table
from live import focus_draft as FD
from live.ui_parts import (GROUP_CSS, PB_CSS, PB_JS, PROCESS, PROMPT_CSS, PROMPT_JS, RESULTS, _band, _kv, _numbered, _pill,
                           _section, prompt_box)

VIEWS = (("overall", "Overall"), ("grid", "Grid"), ("vs-previous", "vs previous"))
CAPTIONS = {"overall": "the Overall Report, written last, and the pair this Job runs",
            "grid": "every question × cut: what each cell needs next",
            "vs-previous": "this Job against the one before: what changed, and the proposals it makes",
}

# a button that writes (data-post, as runs_panel's): the old frame carries it, the focus page needs its own copy
POST_JS = """<script>(function(){if(window.inPost)return;window.inPost=1;
 document.addEventListener('click',function(ev){var b=ev.target.closest('button[data-post]');if(!b)return;ev.preventDefault();
  var body={};try{body=JSON.parse(b.dataset.body||'{}');}catch(e){}
  var row=b.closest('.sign-row')||b.parentNode;(b.dataset.fields||'').split(' ').filter(Boolean).forEach(function(n){
   var i=row.querySelector('[name="'+n+'"]');if(i)body[n]=i.type==='checkbox'?i.checked:i.value;});
  b.disabled=true;
  fetch(b.dataset.post,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   .then(function(x){return x.json();}).then(function(j){if(j.ok){location.reload();return;}
    b.disabled=false;b.title=j.err||'';b.textContent='✗ '+(j.err||'refused');});});
})();</script>"""
CSS = """<style>.in-sign{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:6px 0 0;font-size:13px}
.in-big{font-size:19px;font-weight:600;margin:2px 0 4px}.in-cell .pb-pill{font-size:11.5px}
.in-grid{overflow-x:auto;max-width:100%}.in-grid td,.in-grid th{white-space:nowrap}
.pb-prompt.in-copy{display:inline;border:0;padding:0;margin:0;background:none}.in-grid tr.lv td{background:var(--wash);font-weight:600}</style>"""


def _old_css() -> str:
    """The six-Space page's own rules for the views carried over (q-row, rep-glance, wf-table, topic folds …), from
    frame.CSS; the Studio's and Related's rules left out."""
    from live import frame
    keep = r"\.(q-|rep-|wf-|st-ok|st-warn|chip|topic|dikw|lv-|report-doc|doc\b|files|links|where|check-it|sign-row)"
    rules = re.findall(r"[^{}]+\{[^{}]*\}", frame.CSS)
    return "<style>" + "".join(r.strip() for r in rules if re.search(keep, r.split("{")[0])
                               and not re.search(r"studio|related", r.split("{")[0])) + "</style>"


def is_job(folder: Path) -> bool:
    return bool(P.JOB_NAME.match(folder.name)) and (folder / f"{folder.name}.md").is_file()


def _session(jdir: Path) -> str:
    """The Claude session a prompt runs in: the Job face's `session:`, else its Board's."""
    for face in (jdir / f"{jdir.name}.md", jdir.parent / "board.md"):
        if face.is_file():
            m = re.search(r"(?m)^session:\s*`?([\w.-]+)`?", face.read_text(encoding="utf-8", errors="ignore")[:4000])
            if m:
                return m.group(1)
    return jdir.name


def _facts(jdir: Path, root: Path) -> dict:
    block = P.job_board(jdir)
    b, j = P.board(block), P.job(jdir)
    r = P.release(b["prototype"], j["release"])
    f = V._work_facts(j)
    return {"j": j, "b": b, "r": r, "f": f, "st": V._work_states(j, f), "folder": rel(jdir, root),
            "me": j["name"][:3], "prev": j["previous"][:3], "jdir": jdir, "root": root, "session": _session(jdir)}


def _copy(x: dict, label: str, still: str = "", verb: str = "Copy prompt") -> str:
    """A row's own Copy prompt (labeling_steps._rerun's shape): the run card's prompt with this Job filled in, shown on
    hover, copied with the session line; the full Prompt box is kept for a step's single next act."""
    text = V._card_prompt(label, x["folder"], x["me"], x["prev"])
    if not text:
        return ""
    tail = f'Run this in the Claude session "{x["session"]}"; start it if it is not running.'
    return (f'<span class="pb-prompt in-copy" title="{esc(text + still)}"><button type=button class="fd-btn pb-copy" '
            f'data-copy="{esc(text + still)}" data-tail="{esc(tail)}">{esc(verb)}</button></span>')


def _ask(x: dict, label: str, step: str, asks: str, still: str = "") -> str:
    """One step's Prompt box: its run card's prompt with this Job filled in, what is still to do after it."""
    text = V._card_prompt(label, x["folder"], x["me"], x["prev"])
    if not text:
        return ""
    return prompt_box(text + still, None, x["session"], step=step, asks=asks, key=f'notes:{x["folder"]}#{label}')


def _pop(href: str, label: str, html: str) -> str:
    """frame.pop with HTML inside (a pill, a mark and its word): the pop-out link, the content already escaped."""
    return f'<a data-pop="{esc(label)}" href="{esc(href)}" target=_blank rel=noopener>{html}</a>'


def _todo(rows: list) -> str:
    """Rows like ui_parts._todo, each with its own buttons: [(words, sub, state, verbs html)]."""
    return '<div class=pb-todos>' + "".join(
        f'<div class=pb-todo><span class=w>{esc(w)}' + (f"<small>{esc(s)}</small>" if s else "") + "</span>"
        + _pill(state) + verbs + "</div>" for w, s, state, verbs in rows) + "</div>"


# ── 🙋 what waits on you, first on every view ──────────────────────────────────────────────────────────────────
WAIT_WORD = {"1 · Launch": "the launch", "2 · Run": "the runs", "3 · Write": "the pages", "4 · Check": "the checks",
             "5 · Compare": "the comparison"}


def _done(signed) -> str:
    """A done sign's state word, with its date when the face has one: `done 261101`."""
    return ("done " + str(signed or "").lstrip("✅ ").strip()).strip()


def _plan_signed(x: dict) -> bool:
    return str(x["r"]["face"].get("signed") or "").startswith("✅")


def _sign_rows(x: dict) -> list:
    """Your two acts on a Job, in their order: sign the plan (in the Prototype; until then this Job is a preview),
    then close the Job (greyed until every step before it is done)."""
    j, r, st = x["j"], x["r"], x["st"]
    plan = r.get("label") or j["release"]
    if _plan_signed(x):
        sign = (f"Sign the plan {plan}", "signed in the Prototype", _done(r["face"]["signed"]), "")
    else:
        go = (f'<a class=fd-btn data-pop="{esc(plan)}" href="{esc(V.run_url(r["job"], x["root"]))}">Sign in the Prototype</a>'
              if r.get("job") else "")
        sign = (f"Sign the plan {plan}", "until then this Job is a preview", "waiting for you", go)
    waits = [WAIT_WORD[s] for s in V.WORK_STEPS[:-1] if st[s] not in ("done", "optional")]
    if j["state"] == "closed":
        close = ("Close the Job", "frozen: its pages, Runs and comparison", _done(j["face"].get("signed")), "")
    elif waits:
        close = ("Close the Job", "once every page is checked",
                 "waits on " + ", ".join(waits), '<button type=button class=fd-btn disabled>Close</button>')
    else:
        body = esc(json.dumps({"action": "close", "job": x["folder"]}))
        close = ("Close the Job", "every step is done: read what the close freezes, then sign", "waiting for you",
                 f'<span class="in-sign sign-row"><label><input type=checkbox name=attest> I read what it freezes</label>'
                 f'<button type=button class=fd-btn data-post="/_board/insight-act" data-body="{body}" '
                 f'data-fields="attest">Sign the close</button></span>')
    return [sign, close]


def _waits_on_you(x: dict, items=(), item_html=None) -> str:
    rows = _sign_rows(x)
    you = [rw for rw in rows if rw[2] == "waiting for you"]
    asks = "".join(item_html(i) for i in items) if item_html and items else ""
    title = "🙋 Waits on you" if you or asks else "🙋 Nothing waits on you"
    return _section(title, _todo(rows) + asks)


# ── the views ───────────────────────────────────────────────────────────────────────────────────────────────────
def _overall(x: dict) -> tuple:
    j, f = x["j"], x["f"]
    xs = [t for t in f["live"] if t["qid"][:1] == "X"]
    below = [t for t in f["live"] if t["qid"][:1] in "DIKW"]
    done = {t["name"] for t in f["written"]}
    waits = [t["qid"] for t in below if t["name"] not in done]
    if not xs:
        state = "no Executive question"
    elif all(t["name"] in done for t in xs):
        state = "done"
    else:
        state = "waits on " + ", ".join(waits[:4]) + (" …" if len(waits) > 4 else "") if waits else "ready"
    proc = _section("✍️ Write the Overall Report", _todo([(
        "Write the Overall Report", "each Executive question's page from the answers below it, then its one page",
        state, "")]) + (_ask(x, "Write the overall report", "Write the Overall Report", "use /haipipe-insight")
                        if state == "ready" else ""))
    res = (_section("📄 Overall Report", V._overall(j, x["b"], x["r"], x["root"])) if V._executive(j)
           else _section("📄 Overall Report", "<p class=mut>No Executive question in this plan: no Overall Report.</p>"))
    facts, freezes = _pair(x)
    return proc + freezes, res + facts


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


def _grid(x: dict, verbs: bool) -> str:
    """The question × cut grid, rows grouped by DIKW level (Report B); with `verbs`, each cell its next verb (Work B):
    launch on a cut not run, write on a page ready to write, check on a written page."""
    f, root = x["f"], x["root"]
    cuts = _cuts(x)
    ran = {t["name"] for t in f["ran"]}
    written, checked, returned = ({t["name"] for t in f[k]} for k in ("written", "checked", "returned"))
    rows = []
    for lv in V.WRITE_ORDER:
        ts = [t for t in f["live"] if t["qid"][:1] == lv]
        if not ts:
            continue
        rows.append((f'<b>{lv} · {V.LEVEL_WORD[lv]}</b>',) + ("",) * (len(cuts) + 2))
        for t in ts:
            by = {(h.get("partition") or h["run"].split("_", 1)[-1]): h for h in t["hard"]}
            cells = []
            for p in cuts:
                if lv not in V.RUN_LEVELS:
                    cells.append("<span class=mut>—</span>")
                elif p in by:                                # a cut its question asks: its Run, planned or run
                    s = str(by[p].get("status") or "planned")
                    word = _pill("launch") if verbs and s.lower() == "planned" else V.MARK.get(s, "·") + " " + esc(s)
                    cells.append(_pop(V.run_url(by[p]["path"], root), by[p]["run"], word))
                else:                                        # a cut the plan does not ask of this question
                    cells.append("<span class=mut>·</span>")
            if t["name"] in returned:
                page = _pill("↩ rewrite")
            elif t["name"] in written:
                page = V._page_link(t, root) + " ✅"
            elif lv not in V.RUN_LEVELS or t["name"] in ran:
                page = _pill("write") if verbs else "<span class=mut>⏳</span>"
            else:
                page = "<span class=mut>waits on runs</span>"
            if t["name"] in checked:
                check = "✅"
            elif t["name"] in written:
                check = V._check_form(t, root) if verbs else "<span class=mut>not yet</span>"
            else:
                check = "<span class=mut>—</span>"
            rows.append((f'<a href="{esc(V.run_url(Path(t["path"]), root))}" data-pop="{esc(t["name"])}">{esc(t["name"])}</a>',)
                        + tuple(cells) + (page, check))
    if not rows:
        return "<p class=mut>No question in this Job yet.</p>"
    html = table(("question",) + tuple(V._label(p) for p in cuts) + ("page", "check"), rows)
    return '<div class=in-grid>' + re.sub(r"<tr>(<td><b>[DIKWX] · )", r"<tr class=lv>\1", html) + "</div>"


def _grid_view(x: dict) -> tuple:
    f, st = x["f"], x["st"]
    ran = {t["name"] for t in f["ran"]}
    ready = [t for t in f["unwritten"] if t["qid"][:1] not in V.RUN_LEVELS or t["name"] in ran]
    lv = next((t["qid"][:1] for t in sorted(ready, key=lambda t: V.WRITE_ORDER.find(t["qid"][:1]))), "")
    state = lambda step, left, word: ("done" if st[step] == "done" else f"{left} {word}" if left else "ready")
    rows = [("Launch all", "one Run per question × cut, from the plan's thresholds",
             state("2 · Run", len(f["unrun"]), "to run"),
             _copy(x, "Run a partition", V._still(f["unrun"], "Still to run")) if f["unrun"] else ""),
            ("Write all", f"the next DIKW level first: {lv} · {V.LEVEL_WORD[lv]}" if lv else "pages are written up the levels",
             state("3 · Write", len(f["unwritten"]), "to write") if ready or st["3 · Write"] == "done" else "waits on runs",
             _copy(x, V.WRITE_CARD[lv], V._still([t for t in ready if t["qid"][:1] == lv], "Still to write")) if lv else ""),
            ("Check all", "alignment and CHECK, by another agent; or check a page yourself in its row",
             state("4 · Check", len(f["unchecked"]), "to check") if f["written"] else "waits on pages",
             _copy(x, "Check a report", V._still(f["unchecked"], "Still to check")) if f["unchecked"] else "")]
    now = "".join(f'<p class=mut>⏳ running now · {V._run_link(r, x["root"], r["run"])}</p>' for r in f["running"])
    # one grid (s55 round 2): the Report's question × cut grid, each cell its next verb, under Results
    return _section("🧮 Next in each cell", _todo(rows) + now), _section("🔲 Questions × cuts", _grid(x, True))


def _vs_view(x: dict) -> tuple:
    j, f, st = x["j"], x["f"], x["st"]
    prev = x["prev"]
    if not prev:
        return (_section("🔁 Compare", "<p class=mut>The first Job: nothing to compare with.</p>"),
                _section("🔁 Against the Job before", "<p class=mut>No Job before this one.</p>"))
    rows_vs = (j["vs"] or {}).get("rows", {})
    changed = [q for q, v in rows_vs.items() if str(v.get("status")).lower() in ("changed", "new question", "new finding", "dropped")]
    proposed = any(V._closed(r) for r in f["own"].get("propose", []))
    compared = bool(j["vs"]) or any(V._closed(r) for r in f["own"].get("compare", []))
    big = (f'<p class=in-big>{len(changed)} changed answers to turn into proposals</p>' if compared and changed else
           '<p class=in-big>No answer changed</p>' if compared else "")
    rows = [(f"Compare with {prev}", f"run-compare-{x['me']} · every answer against {prev}",
             "done" if compared else "ready" if st["4 · Check"] == "done" else "waits on checks", ""),
            ("Propose questions", f"run-propose-{x['me']} · each change or gap to the Prototype's proposals",
             "done" if proposed else "ready" if compared else "waits on Compare", "")]
    prompts = ("" if compared else _ask(x, "Compare with the Job before", "Compare", "use /haipipe-insight")) + \
        ("" if proposed or not compared else _ask(x, "Propose questions", "Propose", "use /haipipe-insight"))
    return (_section("🔁 Compare, then propose", big + _todo(rows) + prompts),
            _section("🔁 Against " + prev, V._vs_previous(j, x["root"])))


def _pair(x: dict) -> tuple:
    """This Job's facts (📊, under the Overall Report) and, once the close is yours to sign, what it freezes (⚙️)."""
    j, b, r, f = x["j"], x["b"], x["r"], x["f"]
    facts = [("plan", esc(V._rlabel(b, j["release"]))), ("freeze", esc(V._vlabel(b, j["data"]))),
             ("state", esc(("closed" if j["state"] == "closed" else "open")
                           + ("" if _plan_signed(x) else " · a preview: the plan is not signed"))),
             ("moved", esc(j["moved"] or "—")), ("Job before", esc(j["previous"] or "none: the first Job"))]
    freezes = [("pages", f'{len(f["checked"])} checked · {len(f["written"])} written · {len(f["live"])} asked'),
               ("Runs", f'{len(f["hard"])} hard · {len(f["soft"]) + len(j["runs"])} soft')]
    ready = x["st"]["6 · Close"] == "sign"
    close = _section("🔒 What the close freezes", _kv(freezes) + _ask(x, "Close the Job", "Close", "or sign it above yourself")) \
        if ready else ""
    return _section("🧷 This Job", _kv(facts)), close


PARTS = {"overall": _overall, "grid": _grid_view, "vs-previous": _vs_view}


def job_work_views(jdir: Path, root: Path, items=(), item_html=None) -> dict:
    """{key: (name, build)}: the Job's Work views in the Report's letters, each ⚙️ Process then 📊 Results; {} for a
    folder that is not an insight Job. The letters keep the Report's order; every view opens on your signs."""
    if not is_job(jdir):
        return {}
    root = root.resolve()
    views = {}
    for key, name in VIEWS:
        def build(key=key):
            x = _facts(jdir, root)
            proc, res = PARTS[key](x)
            body = (_band(PROCESS, _numbered(_waits_on_you(x, items, item_html) + proc)) + _band(RESULTS, _numbered(res)))
            return (PB_CSS + GROUP_CSS + FD.CSS + CSS + PROMPT_CSS + _old_css() + f'<p class="view-caption">{esc(CAPTIONS[key][:1].upper() + CAPTIONS[key][1:])}.</p>'
                    + body + PB_JS + FD.JS + PROMPT_JS + POST_JS)
        views["work-" + key] = (name, build)
    return views


# ── a Board's Report on the focus page (b11 j01 s51, JL 261101): five letters, A Answers · B Questions · C Jobs ·
# D Data · E Handoff, each its numbered sections only (no ⚙️ Process or 📊 Results band in a Report, s51-D02) ──────
BOARD_VIEWS = (("answers", "Answers"), ("questions", "Questions"), ("jobs", "Jobs"), ("data", "Data"), ("handoff", "Handoff"))
BOARD_CAPTIONS = {"answers": "the answers in one line each, then analysis plans × data freezes, the latest Overall Report, and what each question found",
                  "questions": "how the questions build on each other, then every question each analysis plan asks, by DIKW level",
                  "jobs": "each Job, what it pins, and the one clock it moved",
                  "data": "the data freezes and the cuts every question runs on",
                  "handoff": "the counsel Design reads, from one Job, signed by a person"}
MOVED = {"code": "the code", "data": "the data", "start": "the first Job"}


def is_board(folder: Path) -> bool:
    face = folder / "board.md"
    if not face.is_file():
        return False
    head = face.read_text(encoding="utf-8", errors="ignore")[:2000]
    return bool(re.search(r"(?m)^board-kind:\s*insight-board", head)) or (
        bool(re.search(r"(?m)^workbench:\s*insight", head)) and P.is_plan_c(folder))


def _focus(path: Path, root: Path, section: str = "report") -> str:
    from urllib.parse import quote
    return f"/_board/workbench?path={quote(rel(path, root))}&layout=focus&section={section}"


def _jlink(j: dict, root: Path, words: str = "") -> str:
    return f'<a href="{esc(_focus(j["path"], root))}" title="{esc(j["name"])}">{esc(words or j["name"][:3])}</a>'


def _big(words: str, sub: str = "") -> str:
    return f'<p class=in-big>{esc(words)}</p>' + (f'<p class=mut>{esc(sub)}</p>' if sub else "")


def _all_questions(b: dict) -> dict:
    """Every question any plan asks, by id, Executive first then D · I · K · W: {qid: (question, the plans asking it)}."""
    out = {}
    for r in b["prototype"]["releases"]:
        for qid, q in r["questions"].items():
            out.setdefault(qid, [q, []])[1].append(r.get("code") or r["name"])
    for j in b["jobs"]:                                      # a carried Job's questions, when no plan lists them
        for t in j["tasks"]:
            if t["qid"] and t["qid"] not in out:
                out[t["qid"]] = [{"id": t["qid"], "question": t["face"].get("question", ""), "file": t.get("page")}, []]
    order = lambda q: ("XDIKW".find(q[:1]) if q[:1] in "XDIKW" else 9, q)
    return {k: out[k] for k in sorted(out, key=order)}


def _qname(qid: str, t: dict | None) -> str:
    """A question as people read it: its id and its slug, `D01 extract-and-clock`."""
    if t:
        m = re.match(r"^t\d+_[DIKWX]\d+_(.+)$", t["name"])
        if m:
            return f"{qid} {m.group(1)}"
    return qid


def _in_job(j: dict, qid: str) -> tuple:
    """(state word, Task) for one question in one Job: not asked · ⏳ page to write · ✅ first | held | changed …"""
    t = next((t for t in j["tasks"] if t["qid"] == qid), None)
    if not t:
        return "not asked", None
    st = str(t["face"].get("answer-status") or "").lower()
    if st == "retired":
        return "retired", t
    if st not in ("answered", "written", "checked"):
        return "⏳ " + (st or "page to write"), t
    v = (j["vs"].get("rows") or {}).get(qid) if j["vs"] else None
    if v:
        s = str(v.get("status") or "")
        return "✅ " + (f"changed: {MOVED.get(j['moved'], j['moved'])}" if s.lower() == "changed" and j["moved"] in ("code", "data") else s), t
    return "✅ " + ("first" if not j["previous"] else "answered"), t


def _href(b: dict, root: Path):
    """The old six-Space views' link maker, pointed at the focus page: href(sub, space, path)."""
    return lambda sub="", space="", path=None: _focus(Path(path) if path else b["path"], root)


def _answers(b: dict, root: Path) -> str:
    """A Answers (JL 261102: "the first one here should also have some insights report so we can follow them"): the
    matrix of plans × data freezes, then the latest Job's Overall Report, then what each question found; the old
    Audience Report's content, carried over."""
    href = _href(b, root)
    if not b["jobs"]:
        return _section("🧷 Analysis plans × data freezes", V._map(b, root, href))
    newest = b["jobs"][-1]
    plan = P.release(b["prototype"], newest["release"])
    preview = "" if str(plan["face"].get("signed") or "").startswith("✅") else f'{newest["name"][:3]} is a preview: its plan is not signed'
    out = _big("What this dataset says, Job by Job", preview)
    out += _section("⚓ The answers, one line each", _headline(b, root))
    out += _section("🧷 Analysis plans × data freezes", '<div class=in-grid>' + V._map(b, root, href) + "</div>")
    if any(V._executive(j) for j in b["jobs"]):
        out += _section("📄 The Overall Report", V._board_overall(b, root, href))
    cut = next((V._part_key(x) for x in V._part_names(plan.get("partitions") or [])), "full") or "full"
    out += _section("🔎 What each question found", V._coverage(b, root, cut, href))
    return out


def _canvas(b: dict, root: Path, work: dict | None = None) -> str:
    """The question canvas of the newest analysis plan, on its newest Job (question_canvas.py): Report reads it, Work
    asks from it (JL 261102: "the questions should be in the Work, for the report, we just show the report")."""
    from live import question_canvas as QC
    if not b["prototype"]["releases"]:
        return ""
    r = b["prototype"]["releases"][-1]
    job = next((j for j in reversed(b["jobs"]) if j["release"] == r["name"]), None)
    if work is not None:
        work = dict(work, job=job["name"] if job else "", proposals=rel(b["prototype"]["path"], root) + "/proposals/")
    return QC.canvas(r, job, lambda t: _focus(t["path"], root), root, work,
                     b["prototype"]["proposals"] if work is not None else ())


def _plan_label(b: dict) -> str:
    r = b["prototype"]["releases"][-1] if b["prototype"]["releases"] else {}
    return r.get("label") or r.get("name") or ""


def _questions_view(b: dict, root: Path) -> str:
    """B Questions: the canvas to explore, each analysis plan's questions by DIKW level and the open proposals (the old
    Prototype view), then the Board's own questions over the Jobs' answers (the old Findings)."""
    href = _href(b, root)
    out = _section(f"🕸 How the questions build on each other · {_plan_label(b)}", _canvas(b, root))
    out += _section("💬 Each question and its answer", _question_answers(b, root))
    if b["reports"]:                                      # the Board's own questions, only when there are some
        out += _section("🧭 The Board's own questions", V._findings(b, root, "full", href))
    return out


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
</style>"""


def _question_answers(b: dict, root: Path) -> str:
    """B Questions, read: each DIKW level a row of dots (one a question, filled once answered) and its tally; open, each
    question with its one-line answer, its id opening it pinned on the canvas (JL 261102: "this is not cool": the old
    list told counts and "new", never what a question found)."""
    if not b["prototype"]["releases"]:
        return ""
    r = b["prototype"]["releases"][-1]
    job = next((j for j in reversed(b["jobs"]) if j["release"] == r["name"]), None)
    tasks = {t["qid"]: t for t in (job or {}).get("tasks", [])}
    url = _focus(b["path"], root) + "&group=questions"
    rows = []
    for lv, name, _ in V.LEVELS:
        qs = [q for q in r["questions"].values() if q["id"][:1] == lv]
        if not qs:
            continue
        dots, items, done = [], [], 0
        for q in qs:
            tf = (tasks.get(q["id"]) or {}).get("face", {})
            st = str(tf.get("answer-status") or "").lower()
            ans = str(tf.get("answer") or "").strip()
            written = st in V.WRITTEN
            done += written
            cls = "on" if written else "half" if st == "drafted" else "off"
            dots.append(f'<span class="dot {cls}" title="{esc(q["id"])} · {esc(q["question"])} · {esc(st or "not yet")}"></span>')
            items.append(f'<li><a class=id href="{esc(url)}#q={esc(q["id"])}" title="see what it rests on">{esc(q["id"])}</a>'
                         f'<span class=q>{esc(q["question"] or "")}</span>'
                         + (f'<span class=a>{esc(ans)}</span>' if ans and st != "retired" else
                            f'<span class="a none">{"retired" if st == "retired" else "not answered yet"}</span>') + '</li>')
        rows.append(f'<details{" open" if not rows else ""}><summary><span class=lv>{esc(name)}</span><span class=dots>{"".join(dots)}</span>'
                    f'<span class=tally>{done} of {len(qs)} answered</span></summary><ol>{"".join(items)}</ol></details>')
    return QA_CSS + f'<div class=qa>{"".join(rows)}</div>'


def _headline(b: dict, root: Path) -> str:
    """⚓ The newest Job's Executive answers, one line each; a line opens its question pinned on the canvas (Report ›
    Questions, #q=<id>), so its evidence is one click away."""
    j = b["jobs"][-1] if b["jobs"] else None
    xs = [t for t in (j["tasks"] if j else []) if t["qid"][:1] == "X" and str(t["face"].get("answer") or "").strip()]
    if not xs:
        return ""
    url = _focus(b["path"], root) + "&group=questions"
    rows = "".join(f'<li><a class=hl-id href="{esc(url)}#q={esc(t["qid"])}" title="see what it rests on">{esc(t["qid"])}</a>'
                   f'<span>{esc(str(t["face"].get("answer")))}</span></li>' for t in xs)
    return ('<style>.hl{list-style:none;padding:0;margin:4px 0}.hl li{display:flex;gap:10px;padding:7px 2px;border-bottom:1px solid #eaecef;'
            'line-height:1.45}.hl .hl-id{font-weight:700;min-width:34px;text-decoration:none;color:#1864ab}</style>'
            f'<p class=mut>{esc(j["name"][:3])}\'s answers a leader reads first; click an id to see what it rests on.</p><ul class=hl>{rows}</ul>')


def _jobs_view(b: dict, root: Path) -> str:
    """C Jobs: each Job, what it pins, the clock it moved, how far it has got (the old Work Details)."""
    href = _href(b, root)
    moved = [(j["name"][:3], esc(MOVED.get(j["moved"], j["moved"] or "—") + (f' · from {j["previous"][:3]}' if j["previous"] else "")))
             for j in b["jobs"]]
    return (_section("🧷 Each Job", V._jobs(b, root, href, "All"))
            + _section("⏱ What each Job moved", _kv(moved) if moved else "<p class=mut>No Job yet.</p>"))


def _data_view(b: dict, root: Path) -> str:
    """D Data: the data freezes with their sample rows, then the cuts (the old Dataset and Partitions views)."""
    href = _href(b, root)
    return (_section("🗄 Data freezes", V._dataset(b, root, href))
            + _section("✂️ Cuts", V._partitions(b, root, href)))


def _handoff_view(b: dict, root: Path) -> str:
    signed = [h for h in b["handoffs"] if str(h.get("signed") or "").startswith("✅")]
    out = _big("Handed off: " + ", ".join(str(h.get("counsel") or h["file"].stem) for h in signed) if signed else "No handoff yet")
    j = b["jobs"][-1] if b["jobs"] else None
    w = [t for t in (j["tasks"] if j else []) if t["qid"][:1] == "W"]
    answered = [t for t in w if str(t["face"].get("answer-status") or "").lower() in ("answered", "written", "checked")]
    draft = next((h for h in b["handoffs"] if not str(h.get("signed") or "").startswith("✅")), None)
    out += _section("🤝 The handoff draft", _kv([
        ("pair", esc(f'{V._rlabel(b, j["release"])} × {V._vlabel(b, j["data"])}') if j else "no Job yet"),
        ("counsel", esc(f"{len(answered)} of {len(w)} Wisdom answers written" if w else "no Wisdom question in this plan")),
        ("draft", _pop(_focus(draft["file"].parent, root), draft["file"].name, esc(draft["file"].name)) if draft else "not written")]))
    if b["handoffs"]:
        out += _section("📦 Handoffs", V._handoff(b, root))
    return out


BOARD_PARTS = {"answers": _answers, "questions": _questions_view, "jobs": _jobs_view, "data": _data_view, "handoff": _handoff_view}


def board_report_views(block: Path, root: Path) -> dict:
    """{key: (name, build)}: an insight Board's Report in its five letters, numbered sections only; {} for any other
    folder. The Board's facts are insight_plan_c's; nothing here writes."""
    if not is_board(block):
        return {}
    root = root.resolve()
    views = {}
    for key, name in BOARD_VIEWS:
        def build(key=key):
            return _page(BOARD_CAPTIONS[key], _numbered(BOARD_PARTS[key](P.board(block), root)))
        views[key] = (name, build)
    return views


# ── shared: a run card's prompt at any level, and a row's Copy prompt ──────────────────────────────────────────────
def _prompt(level: str, label: str, folder: str, fill: dict | None = None) -> str:
    card = next((c for c in V.run_cards() if c["level"] == level and c["label"] == label), None)
    if not card:
        return ""
    return V._card_kind(card, fill or {})["prompt"].replace("{folder}", folder)


def _copy_btn(text: str, session: str, verb: str = "Copy prompt") -> str:
    if not text:
        return ""
    tail = f'Run this in the Claude session "{session}"; start it if it is not running.'
    return (f'<span class="pb-prompt in-copy" title="{esc(text)}"><button type=button class="fd-btn pb-copy" '
            f'data-copy="{esc(text)}" data-tail="{esc(tail)}">{esc(verb)}</button></span>')


def _page(caption: str, html: str) -> str:
    return PB_CSS + GROUP_CSS + FD.CSS + CSS + PROMPT_CSS + _old_css() + f'<p class="view-caption">{esc(caption[:1].upper() + caption[1:])}.</p>' + html


def _work_page(caption: str, proc: str, res: str) -> str:
    return _page(caption, _band(PROCESS, _numbered(proc)) + _band(RESULTS, _numbered(res))) + PB_JS + FD.JS + PROMPT_JS + POST_JS


# ── a Board's Work (b11 j01 s52): the Report's letters, ⚙️ Process (your inbox first) then 📊 Results ────────────────
BOARD_WORK_CAPTIONS = {"answers": "what the answers wait on, then each question across the Jobs",
                       "questions": "ask about a question or propose a follow-up, then every question by DIKW level",
                       "jobs": "the newest Job's next step and a new Job, then each Job's steps",
                       "data": "a new freeze or cut, then the freezes and cuts",
                       "handoff": "the handoff's next step, then its draft"}


def _board_x(block: Path, root: Path) -> dict:
    b = P.board(block)
    folder = rel(block, root)
    return {"b": b, "root": root, "folder": folder, "session": _session_of(block),
            "newest": b["jobs"][-1] if b["jobs"] else None}


def _session_of(folder: Path) -> str:
    face = folder / "board.md"
    if face.is_file():
        m = re.search(r"(?m)^session:\s*`?([\w.-]+)`?", face.read_text(encoding="utf-8", errors="ignore")[:4000])
        if m:
            return m.group(1)
    return folder.name


def _board_inbox(x: dict, items=(), item_html=None) -> str:
    """🙋 what waits on you at the Board: the newest plan's sign and the open proposals, both in the Prototype."""
    b, root = x["b"], x["root"]
    proto = b["prototype"]
    rows = []
    if proto["releases"]:
        r = proto["releases"][-1]
        go = (f'<a class=fd-btn data-pop="{esc(r.get("label") or r["name"])}" href="{esc(V.run_url(r["job"], root))}">Open in the Prototype</a>'
              if r.get("job") else "")
        signed = str(r["face"].get("signed") or "")
        rows.append((f'Sign the plan {r.get("label") or r["name"]}', "in the Prototype",
                     _done(signed) if signed.startswith("✅") else "waiting for you", "" if signed.startswith("✅") else go))
    open_ = [p for p in proto["proposals"] if str(p.get("state") or "open").lower() in ("open", "proposed", "")]
    if open_:
        rows.append((f"Triage the open proposals ({len(open_)})", "into one batch for the next plan · in the Prototype",
                     "waiting for you", ""))
    asks = "".join(item_html(i) for i in items) if item_html and items else ""
    you = any(rw[2] == "waiting for you" for rw in rows) or asks
    return _section("🙋 Waits on you" if you else "🙋 Nothing waits on you", (_todo(rows) if rows else "") + asks)


def _bw_answers(x: dict) -> str:
    j = x["newest"]
    if not j:
        return ""
    f = V._work_facts(j)
    below = [t for t in f["live"] if t["qid"][:1] in "DIKW"]
    done = {t["name"] for t in f["written"]}
    waits = [t["qid"] for t in below if t["name"] not in done]
    state = ("done" if V._executive(j) and all(t["name"] in done for t in f["live"] if t["qid"][:1] == "X")
             else "no Executive question" if not V._executive(j)
             else "waits on " + ", ".join(waits[:4]) + (" …" if len(waits) > 4 else "") if waits else "ready")
    verb = _copy_btn(V._card_prompt("Write the overall report", rel(j["path"], x["root"]), j["name"][:3], j["previous"][:3]),
                     x["session"]) if state == "ready" else ""
    return _section("✍️ The Overall Report", _todo([(f'Write the Overall Report for {j["name"][:3]}', "in the Job, from the answers below it",
                                                     state, verb)]))


def _bw_questions(x: dict) -> str:
    j = x["newest"]
    rows = [("Propose questions", "the gaps and weak answers, as proposals for the next plan",
             "ready" if j else "waits on a Job", _copy_btn(_prompt("Block", "Propose questions", x["folder"]), x["session"]) if j else ""),
            ("Ask a Board question", "a question over the Jobs' answers (board.md ## Questions)", "ready",
             _copy_btn(_prompt("Block", "Ask a Block question", x["folder"]), x["session"]))]
    ask = _canvas(x["b"], x["root"], {"board": x["folder"], "tail": f'Run this in the Claude session "{x["session"]}"; start it if it is not running.'})
    return (_section("🙋 Ask about a question", '<p class=mut>Pin a question, then ask about it or propose a follow-up for the '
                     'next analysis plan; each copies a prompt with the question\'s context filled in.</p>' + ask)
            + _section("❓ New questions", _todo(rows)))


def _bw_jobs(x: dict) -> str:
    j, root = x["newest"], x["root"]
    out = ""
    if j and j["state"] != "closed":
        st = V._work_states(j, V._work_facts(j))
        step = next((s for s in V.WORK_STEPS if st[s] in ("next", "sign")), V.WORK_STEPS[-1])
        out += _section("✍️ The newest Job", _todo([(f'{j["name"][:3]} · next: {step.split(" · ")[-1].lower()}', "its Work, step by step",
                                                     st[step] if st[step] != "next" else "ready",
                                                     f'<a class=fd-btn href="{esc(_focus(j["path"], root, "work"))}">Open {esc(j["name"][:3])}</a>')]))
    out += _section("➕ A new Job", _todo([("Add a Job", "a signed analysis plan × a data freeze, one clock moved", "ready",
                                           _copy_btn(_prompt("Block", "Add a Job", x["folder"]), x["session"]))]))
    return out


def _bw_data(x: dict) -> str:
    return _section("🗄 Freezes and cuts", _todo([
        ("Add a data freeze", "a new extract, frozen, its rows counted per cut", "ready",
         _copy_btn(_prompt("Block", "Add a data version", x["folder"]), x["session"])),
        ("Propose a cut", "to the next analysis plan: a cut is plan, fixed before any outcome", "ready",
         _copy_btn(_prompt("Block", "Propose a cut", x["folder"]), x["session"]))]))


def _bw_handoff(x: dict) -> str:
    j = x["newest"]
    w = [t for t in (j["tasks"] if j else []) if t["qid"][:1] == "W"]
    done = [t for t in w if str(t["face"].get("answer-status") or "").lower() in ("answered", "written", "checked")]
    ready = bool(w) and len(done) == len(w)
    state = "ready" if ready else "waits on the Wisdom answers" if w else "no Wisdom question yet"
    return _section("🤝 The handoff", _todo([
        ("Write the counsel", "from the latest Job's Wisdom answers", state,
         _copy_btn(_prompt("Block", "Write the counsel", x["folder"]), x["session"]) if ready else ""),
        ("Draft the handoff", "for a person to sign; Design reads it by its pair", "waits on the counsel",
         "")]))


BOARD_PROC = {"answers": _bw_answers, "questions": _bw_questions, "jobs": _bw_jobs, "data": _bw_data, "handoff": _bw_handoff}


def _bw_answers_result(b: dict, root: Path) -> str:
    """Work · Answers' Results: the matrix only; the Overall Report and the findings are the Report's (JL 261102)."""
    return _section("🧷 Analysis plans × data freezes", '<div class=in-grid>' + V._map(b, root, _href(b, root)) + "</div>")


def _bw_questions_result(b: dict, root: Path) -> str:
    """Work · Questions' Results: the plan's lists and the Board's own questions; the canvas is in Process, to ask from."""
    href = _href(b, root)
    return (_section("❓ The questions, plan by plan", V._prototype(b, root, href))
            + _section("🧭 The Board's own questions", V._findings(b, root, "full", href)))


BOARD_WORK_RESULTS = {"answers": _bw_answers_result, "questions": _bw_questions_result}


def board_work_views(block: Path, root: Path, items=(), item_html=None) -> dict:
    """{key: (name, build)}: an insight Board's Work in the Report's letters, ⚙️ Process (your inbox first) then
    📊 Results (the Report view's own sections); {} for any other folder."""
    if not is_board(block):
        return {}
    root = root.resolve()
    views = {}
    for key, name in BOARD_VIEWS:
        def build(key=key):
            x = _board_x(block, root)
            return _work_page(BOARD_WORK_CAPTIONS[key], _board_inbox(x, items, item_html) + BOARD_PROC[key](x),
                              BOARD_WORK_RESULTS.get(key, BOARD_PARTS[key])(x["b"], root))
        views["work-" + key] = (name, build)
    return views


# ── a Job's Report (b11 j01 s54): Overall · Grid · vs previous, numbered sections only ─────────────────────────────
def job_report_views(jdir: Path, root: Path) -> dict:
    if not is_job(jdir):
        return {}
    root = root.resolve()

    def overall():
        x = _facts(jdir, root)
        j = x["j"]
        plan = "" if _plan_signed(x) else " · a preview: the plan is not signed"
        moved = f' · moved: {MOVED.get(j["moved"], j["moved"])}' + (f', from {j["previous"][:3]}' if j["previous"] else "") if j["moved"] else ""
        _, res = _overall(x)
        return _page(CAPTIONS["overall"], _big(f'Overall Report · {P.plan_code(j["release"])} × {P.freeze_code(j["data"])}',
                                               (plan + moved).strip(" ·")) + _numbered(res))

    def grid():
        x = _facts(jdir, root)
        f = x["f"]
        left = [t["qid"] for t in f["live"] if t["name"] not in {w["name"] for w in f["written"]}]
        big = _big("Every question answered at the cuts it asks" if not left else
                   f'{len(f["live"]) - len(left)} of {len(f["live"])} questions answered', "still to write: " + ", ".join(left[:6]) if left else "")
        return _page("every question × cut, read only", big + _numbered(_section("🔲 Questions × cuts", _grid(x, False))))

    def vs():
        x = _facts(jdir, root)
        j = x["j"]
        if not x["prev"]:
            return _page(CAPTIONS["vs-previous"], _big("The first Job: nothing to compare with"))
        what = MOVED.get(j["moved"], j["moved"] or "—")
        return _page(CAPTIONS["vs-previous"], _big(f'Against {x["prev"]}: only {what} moved', "so a changed answer has one cause")
                     + _numbered(_section("🔁 Per question", V._vs_previous(j, root))))

    return {"overall": ("Overall", overall), "grid": ("Grid", grid), "vs-previous": ("vs previous", vs)}


# ── a Task's Report and Work (b11 j01 s57, s58): Answer · By cut · Across Jobs · Plan ──────────────────────────────
TASK_VIEWS = (("answer", "Answer"), ("by-cut", "By cut"), ("across-jobs", "Across Jobs"), ("plan", "Plan"))
TASK_CAPTIONS = {"answer": "the answer, how sure it is, and what it rests on",
                 "by-cut": "each cut this question runs on: its Run, page and check",
                 "across-jobs": "this question in every Job of the Board",
                 "plan": "what the plan needs from this question, agreed before any Run"}
TASK_WORK_CAPTIONS = {"answer": "the whole chain, one verb live on the next step, then the answer",
                      "by-cut": "the next act on each cut, then each cut's Run, page and check",
                      "across-jobs": "track this question across the Jobs, then its answer in each",
                      "plan": "the plan's steps, then what it needs"}


def is_task(folder: Path) -> bool:
    return bool(P.TASK_NAME.match(folder.name)) and is_job(folder.parent)


def _task_x(tdir: Path, root: Path) -> dict:
    jdir = tdir.parent
    b, j = P.board(jdir.parent), P.job(jdir)
    t = next((t for t in j["tasks"] if t["name"] == tdir.name), P.task(tdir))
    q = P.question_of(b["prototype"], j["release"], t["qid"])
    return {"b": b, "j": j, "t": t, "q": q, "root": root, "folder": rel(tdir, root), "session": _session(jdir),
            "jfolder": rel(jdir, root)}


def _state(t: dict) -> str:
    return str(t["face"].get("answer-status") or "").lower()


def _t_answer(x: dict) -> str:
    t, root = x["t"], x["root"]
    fm = t["face"]
    marks = " · ".join(w for w in (_state(t) or "not written", "checked" if fm.get("check") else "") if w)
    big = _section("⚓ The answer", _big(str(fm.get("answer") or "Not written yet"), marks)
                   + (f'<p>{V._page_link(t, root)}</p>' if fm.get("answer") else ""))
    ok = [h for h in t["hard"] if str(h.get("status")) == "ok"]
    rests = ", ".join(V._run_link(h, root, h.get("partition") or h["run"]) for h in ok) or "<span class=mut>no Run yet</span>"
    return big + _section("🎯 How sure", _kv([("how sure", esc(fm.get("how-sure") or "—")), ("rests on", rests)]))


def _t_cuts(x: dict) -> str:
    t, root = x["t"], x["root"]
    fm = t["face"]
    page = "✅ written" if _state(t) in ("answered", "written", "checked") else "⏳ to write"
    check = "✅ checked" if fm.get("check") else "not yet"
    rows = []
    for h in t["hard"]:
        s = str(h.get("status") or "planned")
        n = h.get("n")
        rows.append((esc(h.get("partition") or h["run"]), _pop(V.run_url(h["path"], root), h["run"], esc(V.MARK.get(s, "·") + " " + s)),
                     esc(f"{n:,} rows" if isinstance(n, int) else (str(n) + " rows" if n else "—")),
                     esc(page if s == "ok" else "—"), esc(check if s == "ok" else "—")))
    out = _section("🔲 Cut × step", table(("cut", "Run", "rows", "page", "check"), rows) if rows
                   else "<p class=mut>No Run: this question cites the answers below it.</p>")
    full = next((h for h in t["hard"] if (h.get("partition") or "") in ("full", V.OVERALL) or h["run"].endswith("_full")), None)
    if full:
        out += _section("📈 The full result", V._q_report(t["qid"], full, root, "full"))
    return out


def _t_across(x: dict) -> str:
    b, t, root = x["b"], x["t"], x["root"]
    rows = []
    for j in b["jobs"]:
        word, tt = _in_job(j, t["qid"])
        if word == "not asked":
            continue
        rows.append((_jlink(j, root, f'{j["name"][:3]} · {P.plan_code(j["release"])} × {P.freeze_code(j["data"])}'),
                     esc(str((tt or {}).get("face", {}).get("answer") or "—")), V._st(word)))
    return _section("🔁 This question in each Job", table(("Job", "answer", "status"), rows) if rows else "<p class=mut>Only this Job.</p>")


def _t_plan(x: dict) -> str:
    q, t, root = x["q"], x["t"], x["root"]
    may = next((m for lv, _, m in V.LEVELS if lv == t["qid"][:1]), "")
    spec = V._spec(q)
    needs = V._needs(q)
    need = "<br>".join(esc(str(n.get("need") or n.get("ask") or n.get("what") or n.get("kind") or ""))
                       + (f' <span class=mut>{esc(V._goes(n))}</span>' if V._goes(n) else "") for n in needs) or "—"
    q = dict(q, question=q.get("question") or spec.get("ask") or spec.get("question") or "")
    return _section("📋 Needs", _kv([("question", esc(q.get("question") or "—")), ("need", need), ("may say", esc(may.replace("may say: ", ""))),
                                     ("agreed", esc(str(q.get("agreed") or "not yet")))])
                    + (f'<p>{_pop(V.run_url(Path(q["file"]).parent, root), t["qid"], "the question file ↗")}</p>' if q.get("file") else ""))


TASK_PARTS = {"answer": _t_answer, "by-cut": _t_cuts, "across-jobs": _t_across, "plan": _t_plan}


def _chain(x: dict) -> tuple:
    """The whole chain of one question, each link its state, and the next link (its label for the prompt)."""
    t, q = x["t"], x["q"]
    hard = t["hard"]
    ran = bool(hard) and all(str(h.get("status")) in ("ok", "refused") for h in hard)
    written = _state(t) in ("answered", "written", "checked")
    checked = bool(t["face"].get("check"))
    aligned = any(V._closed(r) for r in t["soft"] if "alignment" in r["run"])
    lv = t["qid"][:1]
    links = [("plan", bool(q.get("method")) or bool(q.get("question"))), ("agree", bool(q.get("agreed"))),
             ("Runs", ran if lv in V.RUN_LEVELS else True), ("page", written), ("check", checked), ("alignment", aligned)]
    nxt = next((k for k, done in links if not done), "")
    return links, nxt


def _tw_answer(x: dict) -> str:
    links, nxt = _chain(x)
    chain = " → ".join(f'{"✅" if done else "⏳" if k == nxt else "⬜"} {k}' for k, done in links)
    label = {"Runs": "Run a partition", "page": V.WRITE_CARD.get(x["t"]["qid"][:1], "Write a report"),
             "check": "Check a report", "alignment": "Check alignment"}.get(nxt, "")
    verb = _copy_btn(_prompt("Task", label, x["folder"]), x["session"]) if label else ""
    word = {"plan": "plan the evidence (in the Prototype)", "agree": "another agent agrees the plan", "Runs": "run every cut",
            "page": "write the page", "check": "check the page, in a fresh context", "alignment": "run the alignment check"}.get(nxt, "")
    return _section("🔗 Next: " + (word or "nothing: the chain is done"), f'<p class=in-sign>{esc(chain)}</p>'
                    + (_todo([(word[:1].upper() + word[1:], "a Task never asks you; you sign at the Job", "ready", verb)]) if word else ""))


def _tw_cuts(x: dict) -> str:
    rows = []
    for h in x["t"]["hard"]:
        s = str(h.get("status") or "planned")
        if s in ("planned", "failed"):
            rows.append((f'Run the {h.get("partition") or h["run"]} cut', h["run"], "ready",
                         _copy_btn(_prompt("Task", "Run a partition", x["folder"]), x["session"])))
    out = _section("🔲 Next on each cut", _todo(rows) if rows else "<p class=mut>Every cut has run.</p>")
    proto = rel(x["b"]["prototype"]["path"], x["root"]) if x["b"]["prototype"]["path"].exists() else x["folder"]
    return out + _section("✂️ A new cut", _todo([("Propose a cut to the next plan", "a cut is plan, fixed before any outcome", "ready",
                                                  _copy_btn(_prompt("Block", "Propose a cut", proto), x["session"]))]))


def _tw_across(x: dict) -> str:
    board = rel(x["b"]["path"], x["root"])
    many = sum(1 for j in x["b"]["jobs"] if any(t["qid"] == x["t"]["qid"] for t in j["tasks"])) > 1
    return _section("🔁 Track", _todo([(f'Track {x["t"]["qid"]} across the Jobs', "its answer Job by Job",
                                        "ready" if many else "waits on a second Job",
                                        _copy_btn(_prompt("Block", "Draw a track", board), x["session"]) if many else "")]))


def _tw_plan(x: dict) -> str:
    q = x["q"]
    return _section("📋 The plan", _todo([("Plan the evidence", "in the Prototype, before any Run", "done" if V._needs(q) or q.get("method") else "to do", ""),
                                          ("Agree the plan · another agent", "", _done(q.get("agreed")) if q.get("agreed") else "to do", "")]))


TASK_PROC = {"answer": _tw_answer, "by-cut": _tw_cuts, "across-jobs": _tw_across, "plan": _tw_plan}


def task_views(tdir: Path, root: Path, section: str) -> dict:
    """{key: (name, build)}: an insight Task's Report (numbered sections only) or Work (⚙️ Process then 📊 Results;
    no 🙋, a Task never asks you); {} for any other folder."""
    if not is_task(tdir):
        return {}
    root = root.resolve()
    views = {}
    for key, name in TASK_VIEWS:
        if section == "work":
            def build(key=key):
                x = _task_x(tdir, root)
                return _work_page(TASK_WORK_CAPTIONS[key], TASK_PROC[key](x), TASK_PARTS[key](x))
            views["work-" + key] = (name, build)
        else:
            def build(key=key):
                return _page(TASK_CAPTIONS[key], _numbered(TASK_PARTS[key](_task_x(tdir, root))))
            views[key] = (name, build)
    return views
