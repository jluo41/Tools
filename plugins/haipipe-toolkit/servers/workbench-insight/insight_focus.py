"""The insight pages on the focus page (b11 j01): a Board, a Job and a Task, each with its Report and its Work, on the
shared page rules every theme's page follows (haipipe-ui "The person's page rules", 261106):

  every section a numbered bar, closed until opened, its state word on its right; what waits on the person under the
  closed bar (ui_parts._section's `word` and `waits`); the fold script on Report too.
  Report shows results only; Work has the same views, each ⚙️ Process then 📊 Results, the Results drawn by the same
  function as the Report's view. Whatever does something (sign the plan, triage the proposals, close the Job, sign the
  handoff, launch, write, check, ask) is a Process step with its state word, never a 🙋 section of its own: 🙋
  Interaction is the last section of every view, added by the page itself with that view's own forms (view_of_item).
  Lists of items are side tabs, their labels with no count; the MindMap is always a view.

Board: Answers · Questions · Jobs · Data · Handoff · MindMap. Job: Overall · Grid · vs previous (from the second Job) ·
MindMap. Task: Answer · By cut · Across Jobs · Plan · MindMap. The facts are insight_plan_c's; the older views' parts
insight_views'; the person's actions insight_act's. Nothing here writes."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from live import insight_plan_c as P
from live import insight_views as V
from live.frame import esc, rel, table
from live import focus_draft as FD
from live.ui_parts import (GROUP_CSS, PB_CSS, PB_JS, PROCESS, PROMPT_CSS, PROMPT_JS, RESULTS, _band, _kv, _numbered, _pill,
                           _section, _side_tabs, prompt_box)

VIEWS = (("overall", "Overall"), ("grid", "Grid"), ("vs-previous", "vs previous"))
CAPTIONS = {"overall": "the Overall Report, written last, and the analysis plan and data freeze it runs",
            "grid": "every question × cut, by DIKW level: one dot a cell",
            "vs-previous": "this Job against the one before: what changed",
            }
WORK_CAPTIONS = {"overall": "your sign and the close, the Overall Report to write, then the Report's Overall",
                 "grid": "the next act in each cell, then the grid, each cell its next verb",
                 "vs-previous": "compare and propose, then each question against the Job before"}
MAP_CAPTION = "How it is built, as a map: its parts, and what each must find out."

# the skills each view's work calls on (the rail's Skills: focus_page.page_skills reads it, 261106)
VIEW_SKILLS = {
    "answers": (("haipipe-insight", "writes the Overall Report from the answers below it"),),
    "questions": (("haipipe-insight-question", "proposes questions and cuts for the next plan"),
                  ("haipipe-insight-evidence-plan", "plans each question's evidence before any Run")),
    "jobs": (("haipipe-insight", "adds a Job: a signed plan × a data freeze, one clock moved"),),
    "data": (("haipipe-insight-meta", "adds a data freeze and counts its rows per cut"),),
    "handoff": (("haipipe-insight-wisdom", "writes the counsel and drafts the handoff"),),
    "overall": (("haipipe-insight", "writes the Overall Report and closes the Job"),),
    "grid": (("haipipe-insight-data", "writes a Data page from its Runs"),
             ("haipipe-insight-information", "writes an Information page"),
             ("haipipe-insight-knowledge", "writes a Knowledge page"),
             ("haipipe-insight-check", "checks each page against its question")),
    "vs-previous": (("haipipe-insight-knowledge", "compares each answer with the Job before"),),
    "answer": (("haipipe-insight-check", "runs the alignment check"),),
    "by-cut": (("haipipe-insight", "runs the question on a cut"),),
    "across-jobs": (("haipipe-insight-check", "draws the question's track across the Jobs"),),
    "plan": (("haipipe-insight-evidence-plan", "plans and agrees the evidence"),),
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
.pb-prompt.in-copy{display:inline;border:0;padding:0;margin:0;background:none}.in-grid tr.lv td{background:var(--wash);font-weight:600}
.in-dot{display:inline-block;width:11px;height:11px;border-radius:50%;border:1.5px solid #1a7f37;box-sizing:border-box;vertical-align:middle}
.in-dot.on{background:#1a7f37}.in-dot.half{background:#f2c94c;border-color:#b58105}.in-dot.off{border-color:#c4c8ce}
.in-dot.bad{background:#ffe3e3;border-color:#c92a2a}.in-key{font-size:12.5px;color:var(--muted);margin:2px 0 8px}
.in-key .in-dot{margin:0 3px 0 8px}.in-key .in-dot:first-child{margin-left:0}
.jb{list-style:none;margin:2px 0;padding:0}.jb li{display:flex;flex-wrap:wrap;align-items:center;gap:4px 12px;padding:8px 2px;
 border-bottom:1px solid var(--line);font-size:14px}.jb li:last-child{border-bottom:0}.jb .pins{color:var(--muted);font-size:13px}
.jb .strip,.in-plans .strip{display:inline-flex;flex-wrap:wrap;align-items:center;gap:3px 4px;font-size:12px;color:var(--muted);margin:3px 0}
.jb .strip b,.in-plans .strip b{margin-left:6px;font-weight:600}.jb .strip b:first-child,.in-plans .strip b:first-child{margin-left:0}
.in-plans td{vertical-align:top}.in-plans .pb-pill{font-size:11.5px}.jb small{margin-left:auto;font-size:12.5px;color:var(--muted)}
.in-card{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;margin:2px 0 10px}
.in-card div{border:1px solid var(--line);border-radius:8px;padding:8px 10px;background:var(--paper)}
.in-card b{display:block;font-size:17px;font-weight:600;overflow-wrap:anywhere}.in-card span{font-size:12px;color:var(--muted)}
.in-files{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13.5px;margin:0 0 10px}
.in-wl{list-style:none;margin:2px 0;padding:0}.in-wl li{padding:7px 2px;border-bottom:1px solid var(--line);font-size:14px;line-height:1.45}
.in-wl li:last-child{border-bottom:0}.in-wl b{margin-right:8px}.in-wl .q{color:var(--muted);font-size:13px;display:block}
.pb-lv{margin:10px 0 4px;font-size:13.5px}.pb-lv:first-child{margin-top:0}
.in-fig{margin:8px 0 6px;max-width:520px}.in-fig img{display:block;width:100%;border:1px solid var(--line);border-radius:8px;background:#fff}
.in-fig figcaption{font-size:12.5px;color:var(--muted);margin:4px 0 0}
.in-why{display:block;max-width:300px;white-space:normal;font-size:12.5px;line-height:1.35;color:var(--ink);margin:3px 0 0}
.in-facts{margin:6px 0 4px;padding-left:18px;font-size:14px;line-height:1.5}.in-facts li{margin:2px 0}
.in-sub{font-size:14.5px;line-height:1.5;margin:0 0 8px}.in-cites td{vertical-align:top}
.in-tab-fig{margin:8px 0 4px;max-width:560px}.in-tab-fig img{display:block;width:100%;border:1px solid var(--line);border-radius:8px;background:#fff}
@media(max-width:600px){.jb small{margin-left:0;flex-basis:100%}.in-grid td,.in-grid th{white-space:normal}
 .in-ct,.in-ct tbody,.in-ct tr,.in-ct td{display:block;width:100%;min-width:0}.in-ct thead{display:none}
 .in-ct tr{display:flex;flex-wrap:wrap;gap:2px 14px;border-bottom:1px solid var(--line);padding:6px 0}
 .in-ct td{border:0!important;padding:2px 0;overflow-wrap:anywhere;width:auto;max-width:100%}.in-ct td:first-child{flex:1 1 100%}
 .in-ct td[data-th]:not([data-th=""])::before{content:attr(data-th) " · ";color:var(--muted);font-size:12px}
 .in-grid{overflow-x:auto}.in-why{max-width:none}.qa summary{flex-wrap:wrap;gap:6px 10px}.qa .lv{min-width:0}
 .qa li{grid-template-columns:34px minmax(0,1fr);padding-left:8px}.qa .in-grid{padding-left:8px}
 .in-card{grid-template-columns:repeat(2,minmax(0,1fr))}.in-files{gap:6px 10px}}</style>"""


def _ctable(heads, rows) -> str:
    """A table that stacks into short cards under 600 px, each cell its column's name before it (round 1, F: at 390
    nothing slides the page sideways)."""
    head = "".join(f"<th>{esc(h)}</th>" for h in heads)
    body = "".join("<tr>" + "".join(f'<td data-th="{esc(h)}">{c}</td>' for h, c in zip(heads, r)) + "</tr>" for r in rows)
    return f'<table class="wf-table in-ct"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


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


def _rows_word(rows: list) -> tuple:
    """(state word, waiting line) of a Process section's to-do rows, read from the rows themselves (R1, 261106): how
    many wait for the person and the first of them; else done, ready, running, or the first row's own word."""
    states = [str(r[2] or "").lower() for r in rows]
    if not rows:
        return "nothing yet", ""
    you = [r for r, s in zip(rows, states) if "waiting for you" in s]
    if you:
        return (f'{len(you)} wait{"s" if len(you) == 1 else ""} for you',
                f"🙋 {you[0][0]}" + (f": {you[0][1]}" if you[0][1] else ""))
    if all(s.startswith(("done", "closed", "signed")) for s in states):
        return "done", ""
    ready = sum(s == "ready" for s in states)
    if ready:
        return ("ready" if ready == 1 else f"{ready} ready"), ""
    if any("running" in s for s in states):
        return "running", ""
    return next(str(r[2]) for r, st in zip(rows, states) if not st.startswith(("done", "closed", "signed"))), ""


def _step(title: str, rows: list, extra: str = "") -> str:
    """A ⚙️ Process section: its to-do rows, its state word and waiting line read from them."""
    word, waits = _rows_word(rows)
    return _section(title, _todo(rows) + extra, word, waits)


def _big(words: str, sub: str = "") -> str:
    return f'<p class=in-big>{esc(words)}</p>' + (f'<p class=mut>{esc(sub)}</p>' if sub else "")


def _focus(path: Path, root: Path, section: str = "report") -> str:
    from urllib.parse import quote
    return f"/_board/workbench?path={quote(rel(path, root))}&layout=focus&section={section}"


def _proto_work(path: Path, root: Path) -> str:
    """Where a plan is signed and its proposals triaged: the Prototype's (or the release's) Work · Findings, whose ⚙️
    Process carries both (round 2: "the Board's Open the proposals landed on MindMap")."""
    return _focus(Path(path), root, "work") + "&group=findings"


def _jlink(j: dict, root: Path, words: str = "") -> str:
    return f'<a href="{esc(_focus(j["path"], root))}" title="{esc(j["name"])}">{esc(words or j["name"][:3])}</a>'


def _pair(j: dict) -> str:
    """A Job in plain words: `j02 · analysis plan 1 × data freeze 2` (round 2: never "(pN × vM)")."""
    return f'{j["name"][:3]} · {P.plan_code(j["release"])} × {P.freeze_code(j["data"])}'


def _written(t: dict) -> bool:
    """A page is written: the one count every "N of M" reads (insight_views.is_written; round 1, 261106)."""
    return V.is_written(t)


def _page_word(t: dict) -> str:
    """A page's state in a word: returned (a CHECK sent it back), else its own answer-status, else to write."""
    return "returned" if str(t["face"].get("check") or "").startswith("↩") else str(t["face"].get("answer-status") or "to write")


def _dot(cls: str, title: str) -> str:
    """One mark, its meaning in its hover title and in the key beside it (haipipe-ui rule 5)."""
    return f'<span class="in-dot {cls}" title="{esc(title)}"></span>'


DOT = {"ok": "on", "refused": "bad", "failed": "bad", "running": "half", "planned": "off"}
JOB_KEY = ('<p class=in-key>' + _dot("on", "written") + 'page written' + _dot("half", "drafted") + 'drafted'
           + _dot("off", "to write") + 'to write</p>')
KEY = ('<p class=in-key>' + _dot("on", "ran") + 'ran' + _dot("off", "planned") + 'planned' + _dot("half", "running")
       + 'running' + _dot("bad", "refused or failed") + 'refused or failed · <span class=mut>— not asked</span></p>')


# ── the page around a view ─────────────────────────────────────────────────────────────────────────────────────
def _head() -> str:
    return PB_CSS + GROUP_CSS + FD.CSS + CSS + PROMPT_CSS + _old_css()


def _cap1(text: str) -> str:
    return text[:1].upper() + text[1:]


def _page(caption: str, html: str) -> str:
    """A Report view: its caption, its numbered sections, the side tabs' script and the fold script (R1: every bar
    starts closed on Report too)."""
    return _head() + f'<p class="view-caption">{esc(_cap1(caption))}.</p>' + html + PB_JS + FD.JS


def _work_page(caption: str, proc: str, res: str) -> str:
    """A Work view: ⚙️ Process (its numbered steps), then 📊 Results (the Report's view, by the same function)."""
    return (_head() + f'<p class="view-caption">{esc(_cap1(caption))}.</p>' + _band(PROCESS, _numbered(proc))
            + _band(RESULTS, _numbered(res)) + PB_JS + FD.JS + PROMPT_JS + POST_JS)


def _map_view(build) -> tuple:
    """The MindMap as a Work view: its Results only, the Report's map (R6: the mind map is always shown)."""
    return ("MindMap", lambda: _head() + f'<p class="view-caption">{esc(MAP_CAPTION)}</p>' + _band(RESULTS, build()))


def _parts_map(folder: Path, root: Path):
    def build():
        from live import focus_page as FP
        return FP.parts_mindmap(folder, root)
    return build


# ── a Job: its signs, its views ────────────────────────────────────────────────────────────────────────────────
WAIT_WORD = {"1 · Launch": "the launch", "2 · Run": "the runs", "3 · Write": "the pages", "4 · Check": "the checks",
             "5 · Compare": "the comparison"}


def _done(signed) -> str:
    """A done sign's state word, with its date when the face has one: `done 261101`."""
    return ("done " + str(signed or "").lstrip("✅ ").strip()).strip()


def _plan_signed(x: dict) -> bool:
    return str(x["r"]["face"].get("signed") or "").startswith("✅")


def _sign_rows(x: dict) -> list:
    """Your two acts on a Job, in their order: sign the plan (in the Prototype; until then this Job is a preview),
    then close the Job (greyed until every step before it is done). Steps of the Overall's ⚙️ Process (R2)."""
    j, r, st = x["j"], x["r"], x["st"]
    plan = r.get("label") or j["release"]
    if _plan_signed(x):
        sign = (f"Sign the plan {plan}", "signed in the Prototype", _done(r["face"]["signed"]), "")
    else:
        go = (f'<a class=fd-btn data-pop="{esc(plan)}" href="{esc(_proto_work(r["job"], x["root"]))}">Sign in the Prototype</a>'
              if r.get("job") else "")
        sign = (f"Sign the plan {plan}", "until then this Job is a preview", "waiting for you", go)
    waits = [WAIT_WORD[s] for s in V.WORK_STEPS[:-1] if st[s] not in ("done", "optional")]
    if j["state"] == "closed":
        close = ("Close the Job", "frozen: its pages, Runs and comparison", _done(j["face"].get("signed")), "")
    elif waits:
        close = ("Close the Job", "once every step before it is done: " + ", ".join(waits) + " still open",
                 "waits on " + waits[0], '<button type=button class=fd-btn disabled>Close</button>')
    else:
        body = esc(json.dumps({"action": "close", "job": x["folder"]}))
        close = ("Close the Job", "every step is done: read what the close freezes, then sign", "waiting for you",
                 f'<span class="in-sign sign-row"><label><input type=checkbox name=attest> I read what it freezes</label>'
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
    out = _step("🔏 The plan and the close", _sign_rows(x))
    if x["st"]["6 · Close"] == "sign":                      # what it freezes, once the close is yours to sign
        f, j = x["f"], x["j"]
        out += _section("🔒 What the close freezes", _kv([
            ("pages", f'{len(f["checked"])} checked · {len(f["written"])} written · {len(f["live"])} asked'),
            ("Runs", f'{len(f["hard"])} hard · {len(f["soft"]) + len(j["runs"])} soft')])
            + _ask(x, "Close the Job", "Close", "or sign it in the step above"), "ready to sign")
    return out + _step("✍️ Write the Overall Report", [(
        "Write the Overall Report", "each Executive question's page from the answers below it, then its one page",
        state, _copy(x, "Write the overall report") if state == "ready" else "")])


def _overall_res(x: dict, eid: str = "ov") -> str:
    """The Job's Overall (Report, and Work's Results): the pair in one large line, the Overall Report as side tabs (one
    Executive question open, its figure beside; JL 261106), then this Job's facts."""
    j, b, r = x["j"], x["b"], x["r"]
    xs = V._executive(j)
    first = next((t for t in xs if _written(t)), None)    # the headline is X01's one line once written (round 1, yes)
    big = _big(str(first["face"]["answer"]) if first else
               f'Overall Report · {P.plan_code(j["release"])} × {P.freeze_code(j["data"])}')
    if not _plan_signed(x):
        big += '<p class=in-sub>A preview: the plan is not signed.</p>'
    written, asked = V.written_of(xs)
    ov = (_section("📄 Overall Report", V._overall_tabs(j, b, r, x["root"], eid), f"{written} of {asked} written")
          if xs else _section("📄 Overall Report", "<p class=mut>This plan asks no Executive question, so it has no "
                                                  "Overall Report.</p>", "none in this plan"))
    closed = str((j.get("face") or {}).get("signed") or "") if j["state"] == "closed" else ""
    changed = ("nothing (the first Job)" if not j["previous"] or j["moved"] == "start"
               else f'{MOVED.get(j["moved"], j["moved"] or "—")}, from {j["previous"][:3]}')
    facts = [("plan", esc(V._rlabel(b, j["release"]))), ("freeze", esc(V._vlabel(b, j["data"]))),
             ("state", esc((("closed " + closed).strip() if j["state"] == "closed" else "preview: still open")
                           + ("" if _plan_signed(x) else " · its plan is not signed"))),
             ("changed from the Job before", esc(changed))]
    word = (("closed " + closed).strip() if j["state"] == "closed" else "preview") + ("" if _plan_signed(x) else " · plan not signed")
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
    """The question × cut grid, folded by DIKW level, one dot a cell (JL 261106: "one dot, folded by DIKW level"): a
    level's closed row is its questions' dots and how many are answered; open, a row per question, a dot per cut, its
    page and its check. With `verbs` (Work), each cell its next verb: launch a cut not run, write a page ready to
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
                elif p in by:                                # a cut its question asks: its Run, planned or run
                    s = str(by[p].get("status") or "planned").lower()
                    mark = _pill("launch") if verbs and s == "planned" else _dot(DOT.get(s, "off"), f"{p} · {s}")
                    cells.append(_pop(V.run_url(by[p]["path"], root), by[p]["run"], mark))
                else:                                        # a cut the plan does not ask of this question
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
                page = _pill("write") if verbs else "<span class=mut>to write</span>"
            else:
                page = "<span class=mut>waits on runs</span>"
            if t["name"] in checked:
                check = "checked"
            elif t["name"] in written:
                check = V._check_form(t, root) if verbs else "<span class=mut>to check</span>"
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
                     f'<span class=dots>{"".join(dots)}</span><span class=tally>{done} of {len(ts)} answered</span></summary>'
                     f'<div class=in-grid>{_ctable(("question",) + tuple(V._label(p) for p in cuts) + ("page", "check"), rows)}'
                     f'</div></details>')
    if not folds:
        return "<p class=mut>This Job asks no question yet.</p>"
    if not opened:                                     # every level written: the first opens
        folds[0] = folds[0].replace("<details>", "<details open>", 1)
    return QA_CSS + KEY + f'<div class=qa>{"".join(folds)}</div>'


def _grid_word(x: dict) -> str:
    f = x["f"]
    return f'{len(f["written"])} of {len(f["live"])} answered'


def _grid_res(x: dict, verbs: bool) -> str:
    f = x["f"]
    left = [t for t in f["live"] if t["name"] not in {w["name"] for w in f["written"]}]
    name = lambda t: t["name"].split("_", 2)[-1].replace("-", " ")      # the question's name, never its id (round 2)
    big = _big("Every question answered at the cuts it asks" if not left else
               f'{len(f["live"]) - len(left)} of {len(f["live"])} questions answered',
               "still to write: " + ", ".join(name(t) for t in left[:6]) if left else "")
    return big + _section("🔲 Questions × cuts", _grid(x, verbs), _grid_word(x))


def _grid_proc(x: dict) -> str:
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
    return _step("🧮 Next in each cell", rows, now)


def _vs_res(x: dict) -> str:
    j = x["j"]
    what = MOVED.get(j["moved"], j["moved"] or "—")
    rows = (j["vs"] or {}).get("rows", {})
    changed = [q for q, v in rows.items() if str(v.get("status")).lower() == "changed"]
    word = (f"{len(changed)} changed" if changed else "none changed") if j["vs"] else "to compare"
    return (_big(f'Against {x["prev"]}: only {what} moved, so a changed answer has one cause')
            + _section("🔁 Per question", V._vs_previous(j, x["root"], tabs="vs"), word))


def _vs_proc(x: dict) -> str:
    j, f, st = x["j"], x["f"], x["st"]
    prev = x["prev"]
    rows_vs = (j["vs"] or {}).get("rows", {})
    changed = [q for q, v in rows_vs.items() if str(v.get("status")).lower() in ("changed", "new question", "new finding", "dropped")]
    proposed = any(V._closed(r) for r in f["own"].get("propose", []))
    compared = bool(j["vs"]) or any(V._closed(r) for r in f["own"].get("compare", []))
    rows = [(f"Compare with {prev}", f"run-compare-{x['me']} · every answer against {prev}",
             "done" if compared else "ready" if st["4 · Check"] == "done" else "waits on checks", ""),
            ("Propose questions", f"run-propose-{x['me']} · each change or gap to the Prototype's proposals"
             + (f" · {len(changed)} changed answers to turn into proposals" if compared and changed else ""),
             "done" if proposed else "ready" if compared else "waits on Compare", "")]
    prompts = ("" if compared else _ask(x, "Compare with the Job before", "Compare", "use /haipipe-insight")) + \
        ("" if proposed or not compared else _ask(x, "Propose questions", "Propose", "use /haipipe-insight"))
    return _step("🔁 Compare, then propose", rows, prompts)


def draw_map(folder: Path, root: Path, branches: list, empty: str) -> str:
    """A map drawn by the shared mind-map module from [(label, [leaf words])]: the folder at its root, a card per
    branch, each leaf whole (a Job's DIKW levels, a Task's answer and cuts, a release's questions)."""
    from live import frame
    from live import focus_page as FP
    mm_ = frame.mindmap_module()
    import mmbuild, mmtree
    nodes = [mmbuild.built(f"{folder}/b{k}", str(label), [mmbuild.built(f"{folder}/b{k}/{i}", str(leaf)) for i, leaf in enumerate(leaves)])
             for k, (label, leaves) in enumerate(branches) if leaves]
    if not nodes:
        return f'<p class="mut">{esc(empty)}</p>'
    top = mmbuild.built(".", folder.name, nodes)
    top.id = "root"
    tree = mmtree.MindMap({"mindmap": "1", "title": folder.name, "built": "focus-page"}, top)
    html = FP.map_html(mm_.draw(tree, "", editable=False), folder, root)
    return ('<style>' + FP.FIT_MAP + '.focus-map .pm-detail{max-width:380px}.focus-map .pm-detail,'
            '.focus-map .pm-detail *{white-space:normal}</style><div class="focus-map fit-map">' + html + '</div>')


def _job_mindmap(jdir: Path, root: Path):
    """A Job's MindMap (JL 261106: "Tasks by DIKW level"): a card per DIKW level, each Task a leaf with the question it
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


def _task_mindmap(tdir: Path, root: Path):
    """A Task's MindMap (round 2: "each Run leaf says what it found, not its name"): the answer; each cut and what its
    Run found (a cite-only question: each answer it cites); then what each check said."""
    def build():
        x = _task_x(tdir, root)
        t = x["t"]
        fm = t["face"]
        said = str(fm.get("answer") or "").strip()
        last = None if said else _last_answer(x)
        answer = said or (f'[last Job] {last[1]["face"]["answer"]}' if last else
                          f'Its page is {"being written" if _writing(t) else "still to write"}')
        branches = [("The answer", [answer])]
        if _cite_only(x):
            branches.append(("What it cites", [f'[{c["qid"]}] {_qlabel(x, c).split(" · ", 1)[-1]}: '
                                               f'{c["face"].get("answer") or "its page is still to write"}'
                                               for c, via in _plan_cites(x)]))
        else:
            from live import focus_page as FP
            takes = fm.get("takeaways") if isinstance(fm.get("takeaways"), dict) else {}
            leaves = []
            for h in sorted(t["hard"], key=lambda h: h["run"]):
                cut = str(h.get("partition") or h["run"].split("_", 1)[-1])
                st = str(h.get("status") or "planned").lower()
                found = (str(takes.get(cut) or "").strip() if st == "ok" else "") or (
                    FP.run_headline(Path(h["path"])) if st == "ok" else
                    str(h.get("reason") or "refused: too thin to answer") if st == "refused" else f"{CUT_WORD.get(st, st)}: not run yet")
                leaves.append(f"[{cut}] {found or 'ran; its page says what it found'}")
            branches.append(("By cut", leaves))
        checks = []
        if str(fm.get("check") or "").startswith(("✅", "↩")):
            checks.append(f'[page check] {"passed " + str(fm["check"]).lstrip("✅ ") if str(fm["check"]).startswith("✅") else "returned: " + str(fm["check"]).lstrip("↩ ")}')
        verdict, line, _ = _aligned(t)
        if verdict:
            checks.append(f"[alignment] {verdict}" + (f": {line}" if line else ""))
        branches.append(("Its checks", checks))
        return draw_map(tdir, root, branches, "Nothing to map yet.")
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
            continue                                         # hidden until a second Job (JL 261106)

        def build(key=key):
            x = _facts(jdir, root)
            proc, res = parts[key]
            return _work_page(WORK_CAPTIONS[key], proc(x), res(x))
        views["work-" + key] = (name, build)
    views["work-mindmap"] = _map_view(_job_mindmap(jdir, root))
    return views


def job_report_views(jdir: Path, root: Path) -> dict:
    """{key: (name, build)}: the Job's Report, its sections only: Overall · Grid · vs previous (from the second Job) ·
    MindMap (Tasks by DIKW level); {} for any other folder."""
    if not is_job(jdir):
        return {}
    root = root.resolve()
    views = {"overall": ("Overall", lambda: _page(CAPTIONS["overall"], _numbered(_overall_res(_facts(jdir, root))))),
             "grid": ("Grid", lambda: _page(CAPTIONS["grid"], _numbered(_grid_res(_facts(jdir, root), False))))}
    if P.job(jdir)["previous"]:
        views["vs-previous"] = ("vs previous", lambda: _page(CAPTIONS["vs-previous"], _numbered(_vs_res(_facts(jdir, root)))))
    views["mindmap"] = ("MindMap", _job_mindmap(jdir, root))
    return views


# ── a Board: Answers · Questions · Jobs · Data · Handoff ────────────────────────────────────────────────────────
BOARD_VIEWS = (("answers", "Answers"), ("questions", "Questions"), ("jobs", "Jobs"), ("data", "Data"), ("handoff", "Handoff"))
BOARD_CAPTIONS = {"answers": "the newest answer first, the newest Overall Report, and what each question found",
                  "questions": "how the questions build on each other, then every plan's questions",
                  "jobs": "the analysis plans × data freezes, a Job in each cell, the newest Job's Tasks, and the one clock each Job moved",
                  "data": "each data freeze's key numbers and files, then the cuts every question runs on",
                  "handoff": "what the handoff will say, its draft, and what was handed to Design"}
BOARD_WORK_CAPTIONS = {"answers": "the Overall Report to write, then the Report's Answers with each question's trail through the Jobs",
                       "questions": "your sign on the next plan, the proposals, new questions, then the questions to ask about",
                       "jobs": "each Job's steps and a new Job, then the Report's Jobs",
                       "data": "a new freeze or cut, then the freezes and cuts",
                       "handoff": "the counsel, the draft and your sign, then the Report's Handoff"}
MOVED = {"code": "the code", "data": "the data", "start": "the first Job"}


def is_board(folder: Path) -> bool:
    face = folder / "board.md"
    if not face.is_file():
        return False
    head = face.read_text(encoding="utf-8", errors="ignore")[:2000]
    return bool(re.search(r"(?m)^board-kind:\s*insight-board", head)) or (
        bool(re.search(r"(?m)^workbench:\s*insight", head)) and P.is_plan_c(folder))


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


def _preview(b: dict, j: dict) -> str:
    plan = P.release(b["prototype"], j["release"])
    return "" if str(plan["face"].get("signed") or "").startswith("✅") else f'{j["name"][:3]} is a preview: its plan is not signed'


def _job_state(j: dict) -> str:
    """A Job's state in a word: closed, else a preview (round 2, settled: the newest Job, still open, is a preview of
    what its plan will say once it closes)."""
    return "closed" if j["state"] == "closed" else "preview"


def _map_word(b: dict) -> str:
    n = sum(j["state"] != "closed" for j in b["jobs"])
    return f"{n} preview" if n else "all closed"


def _plans_grid(b: dict, root: Path) -> str:
    """The analysis plans × data freezes (the Board's two clocks crossed; shown once, in Jobs, round 2): a row per plan
    (its questions, cuts and sign), a column per data freeze, a Job in each cell: its state word, its pages as a dot
    row per DIKW level and how many are written. Stacks into cards under 600 px (round 2: "the grid scrolls sideways")."""
    versions = b["versions"]
    rels = b["prototype"]["releases"] or [{"name": n, "label": n, "questions": {}, "partitions": [], "face": {}}
                                          for n in sorted({j["release"] for j in b["jobs"]})]
    cell = {(j["release"], j["data"]): j for j in b["jobs"]}
    heads = ["analysis plan"] + [V._vlabel(b, str(v.get("version", ""))) + (f' · frozen {v["frozen"]}' if v.get("frozen") else "")
                                 for v in versions]
    rows = []
    for r in rels:
        signed = str(r["face"].get("signed") or "")
        row = [f'<b>{esc(r.get("label") or r["name"])}</b><br><span class=mut>{len(r["questions"])} questions · '
               f'{len(r.get("partitions") or [])} cuts · {esc("signed " + signed if signed.startswith("✅") else "not signed yet")}</span>']
        for v in versions:
            j = cell.get((r["name"], v.get("version")))
            if not j:
                row.append('<span class=mut>no Job yet</span>')   # a new Job is Work's (Jobs › ➕ A new Job)
                continue
            wrote, asked = V.written_of(j["tasks"])
            row.append(f'{_jlink(j, root)} {_pill(_job_state(j) + (" · plan not signed" if _preview(b, j) else ""))}'
                       f'<br>{_strip(j)}<br><span class=mut>{wrote} of {asked} written</span>')
        rows.append(row)
    return JOB_KEY + '<div class=in-plans>' + _ctable(heads, rows) + '</div>'


def _answers(b: dict, root: Path, work: bool = False) -> str:
    """Answers (JL 261102, 261106; rounds 1, 2): the newest Job's X01 in one line as the view's headline, the newest
    Job's Overall Report as side tabs (each Executive answer once), then what each question found, a side tab per DIKW
    level. The plans × data freezes are Jobs' (shown once, round 2); each question's trail through the Jobs is Work's
    (`work`). Every "N of M" by the one count (insight_views.is_written)."""
    href = _href(b, root)
    if not b["jobs"]:
        return _section("🔎 What each question found", "<p class=mut>No Job yet: add one in Work › Jobs.</p>", "no Job yet")
    newest = b["jobs"][-1]
    shown = next((j for j in reversed(b["jobs"]) if V._executive(j)), None)    # the newest Job with an Overall Report
    first = next((t for t in (V._executive(shown) if shown else []) if _written(t)), None)
    out = _big(str(first["face"]["answer"]) if first else "What this dataset says, Job by Job")
    if first and shown is not None:
        out += (f'<p class=in-sub>{_pill(_job_state(shown))} {_jlink(shown, root, _pair(shown))}'
                + (f'; {esc(_preview(b, shown))}' if _preview(b, shown) else "") + '</p>')
    if shown:
        xs = V._executive(shown)
        earlier = [j for j in b["jobs"] if V._executive(j) and j is not shown]
        lead = (f'<p class=in-sub>{_jlink(shown, root, shown["name"][:3])}\'s report'
                + (" · earlier: " + ", ".join(_jlink(j, root) for j in earlier) if earlier else "") + "</p>")
        written, asked = V.written_of(xs)
        out += _section("📄 The Overall Report", lead + V._overall_tabs(shown, b, P.release(b["prototype"], shown["release"]),
                                                                      root, "bov"), f"{written} of {asked} written")
    plan = P.release(b["prototype"], newest["release"])
    cut = next((V._part_key(x) for x in V._part_names(plan.get("partitions") or [])), "full") or "full"
    asked = V._questions(b)                              # each question by its newest Job's page (the one count)
    said = sum(bool(V.newest_task(b, q)) and _written(V.newest_task(b, q)) for q in asked)
    out += _section("🔎 What each question found", V._coverage(b, root, cut, href, tabs="cov", work=work),
                    f'{said} of {len(asked)} written')
    return out


def _answering(b: dict, r: dict) -> dict | None:
    """The Job a plan's answers are read from: its newest Job; for a plan no Job runs yet (a draft), the newest Job,
    each Task of it replaced by the newest written answer of that question in any Job, so a kept question keeps its
    answer while the next plan is drafted."""
    job = next((j for j in reversed(b["jobs"]) if j["release"] == r["name"]), None)
    if job or not b["jobs"]:
        return job
    tasks = {}
    for j in b["jobs"]:                                  # each question's newest Job's page: the counts' one rule
        for t in j["tasks"]:
            tasks[t["qid"]] = t
    return dict(b["jobs"][-1], tasks=list(tasks.values()))


def _canvas(b: dict, root: Path, work: dict | None = None) -> str:
    """The question canvas of the newest analysis plan, on its newest Job (question_canvas.py): Report reads it, Work
    asks from it (JL 261102: "the questions should be in the Work, for the report, we just show the report")."""
    from live import question_canvas as QC
    if not b["prototype"]["releases"]:
        return ""
    r = b["prototype"]["releases"][-1]
    job = _answering(b, r)
    if work is not None:
        work = dict(work, job=job["name"] if job else "", proposals=rel(b["prototype"]["path"], root) + "/proposals/")
    return QC.canvas(r, job, lambda t: _focus(t["path"], root), root, work,
                     b["prototype"]["proposals"] if work is not None else ())


def _plan_label(b: dict) -> str:
    r = b["prototype"]["releases"][-1] if b["prototype"]["releases"] else {}
    return r.get("label") or r.get("name") or ""


def _open_proposals(b: dict) -> list:
    return [p for p in b["prototype"]["proposals"] if str(p.get("state") or "open").lower() in ("open", "proposed", "")]


def _questions_view(b: dict, root: Path, work: dict | None = None) -> str:
    """Questions: the canvas (Report explores it; Work, by the same call, asks from a pinned question), every plan's
    questions as side tabs, then the Board's own questions; each question's answer is Answers' (round 1)."""
    href = _href(b, root)
    r = b["prototype"]["releases"][-1] if b["prototype"]["releases"] else {}
    signed = str((r.get("face") or {}).get("signed") or "")
    out = _section(f"🕸 How the questions build on each other · {_plan_label(b)}", _canvas(b, root, work),
                   "plan signed" if signed.startswith("✅") else "plan not signed yet")
    open_ = _open_proposals(b)                            # each question's answer is Answers' (shown once, round 1)
    out += _section("❓ The questions, plan by plan", V._prototype_tabs(b, root, "plans"),
                    (f'{len(open_)} proposal{"" if len(open_) == 1 else "s"} open') if open_ else "every proposal triaged")
    if b["reports"]:                                      # the Board's own questions, only when there are some
        out += _section("🧭 The Board's own questions", V._findings(b, root, "full", href, tabs="own"),
                        f'{sum(str(x.get("answer-status") or "").lower() in V.WRITTEN for x in b["reports"])} of '
                        f'{len(b["reports"])} answered')
    return out


def _strip(j: dict) -> str:
    """A Job's pages as a dot row per DIKW level (JL 261106: "a dot row per DIKW level, as Questions"): the level's
    letter, a dot a question, filled once its page is written."""
    out = []
    for lv, name, _ in V.LEVELS:
        ts = [t for t in j["tasks"] if t["qid"][:1] == lv]
        if ts:
            out.append(f'<b title="{esc(name)}">{lv}</b>' + "".join(
                _dot("on" if _written(t) else "half" if str(t["face"].get("answer-status") or "").lower() == "drafted" else "off",
                     f'{t["qid"]} · {_page_word(t)}') for t in ts))
    return f'<span class=strip>{"".join(out)}</span>'


def _job_tasks(j: dict, root: Path) -> tuple:
    """A Job's Tasks as dot rows by DIKW level, as Questions: closed, a level's dots and how many pages are written;
    open, a row per Task: its id, its question's words, its Runs, its page's state. (html, written, asked)."""
    rows, wrote, n = [], 0, 0
    for lv, name, _ in V.LEVELS:
        ts = [t for t in j["tasks"] if t["qid"][:1] == lv]
        if not ts:
            continue
        dots, items = [], []
        for t in ts:
            st = str(t["face"].get("answer-status") or "").lower()
            dots.append(f'<span class="dot {"on" if _written(t) else "half" if st == "drafted" else "off"}" '
                        f'title="{esc(t["qid"])} · {esc(_page_word(t))}"></span>')
            tally = {}
            for r in t["hard"]:
                tally[str(r.get("status") or "—")] = tally.get(str(r.get("status") or "—"), 0) + 1
            runs = (" · ".join(f"{k} {s}" for s, k in tally.items()) if t["hard"] else
                    "not run yet" if lv in V.RUN_LEVELS else "cites the answers below it")
            words = t["name"].split("_", 2)[-1].replace("-", " ")
            items.append(f'<li><a class=id href="{esc(_focus(t["path"], root))}">{esc(t["qid"])}</a>'
                         f'<span class=q>{esc(words)}</span><span class=a>{esc(runs)} · page {esc(_page_word(t))}</span></li>')
        done = sum(_written(t) for t in ts)
        rows.append(f'<details{" open" if not rows else ""}><summary><span class=lv>{esc(name)}</span><span class=dots>{"".join(dots)}</span>'
                    f'<span class=tally>{done} of {len(ts)} written</span></summary><ol>{"".join(items)}</ol></details>')
        wrote, n = wrote + done, n + len(ts)
    return QA_CSS + f'<div class=qa>{"".join(rows)}</div>', wrote, n


def _jobs_view(b: dict, root: Path) -> str:
    """Jobs: each Job a row, its pins and its pages as a dot row per DIKW level; the newest Job's Tasks by level, as
    Questions; the one clock each Job moved."""
    if not b["jobs"]:
        return _section("🧷 Analysis plans × data freezes", _plans_grid(b, root), "no Job yet")
    out = _section("🧷 Analysis plans × data freezes", _plans_grid(b, root), _map_word(b))
    newest = b["jobs"][-1]
    html, wrote, n = _job_tasks(newest, root)
    out += _section(f"📂 The newest Job, {newest['name'][:3]} · its Tasks", html,
                    f"{wrote} of {n} written · {_job_state(newest)}")
    moved = [(j["name"][:3], esc(MOVED.get(j["moved"], j["moved"] or "—") + (f' · from {j["previous"][:3]}' if j["previous"] else "")))
             for j in b["jobs"]]
    last = b["jobs"][-1]
    return out + _section("⏱ What each Job moved", _kv(moved),
                          f'{last["name"][:3]} moved {MOVED.get(last["moved"], last["moved"] or "—")}')


def _version_panel(b: dict, v: dict, root: Path) -> str:
    """One data freeze (JL 261106: "a card of key numbers, files one click away"): its numbers as a card, what is new,
    its files each one click away, a few rows."""
    import zlib
    name = str(v.get("version", ""))
    folder = P.version_folder(v, root, b["path"])
    on = [j for j in b["jobs"] if j["data"] == v.get("version")]
    new = f'<p class=in-sub>{esc(_cap1(str(v.get("new"))))}</p>' if v.get("new") and not str(v["new"]).startswith("<") else ""
    if not folder or not folder.is_dir():                 # the card from board.md alone: never a dead end (round 1)
        nums = [(str(v.get("rows") or "—"), "rows"), (str(v.get("frozen") or "—"), "frozen"),
                (", ".join(j["name"][:3] for j in on) or "—", "Jobs on it")]
        return new + '<div class=in-card>' + "".join(f'<div><b>{esc(a)}</b><span>{esc(k)}</span></div>' for a, k in nums) + '</div>'
    d = P.data_folder(folder, str(v.get("extract", "")))
    m = d["manifest"]
    span = " to ".join(str(x) for x in (m.get("start_date"), m.get("end_date")) if x)
    nums = [(f'{m["n_rows"]:,}' if m.get("n_rows") else str(v.get("rows") or "—"), "rows"),
            (str(m.get("n_cols") or "—"), "columns"), (span or "—", "dates"), (str(v.get("frozen") or "—"), "frozen"),
            (", ".join(j["name"][:3] for j in on) or "—", "Jobs on it")]
    card = new + '<div class=in-card>' + "".join(f'<div><b>{esc(a)}</b><span>{esc(k)}</span></div>' for a, k in nums) + '</div>'
    files = [V._open(folder / f, root, f) for f in ("cohort_summary.txt", "data_dictionary.csv", "manifest.json")
             if (folder / f).is_file()]
    files += [V._open(f, root, f.name) for f in d["figures"] + d["docs"] + d["tables"]]
    if d["data"]:
        files.append(f'<span class=mut>{esc(d["data"].name)}</span>')
    s = P.sample_rows(d["data"], V.SAMPLE_N, zlib.crc32(name.encode()), tuple((m.get("groups") or {}).get("identity") or ())) \
        if d["data"] else {}
    sample = ""
    if s and s["rows"]:
        vals = dict(zip(s["columns"], zip(*s["rows"])))
        cols = [c for c in (v.get("preview") or []) if c in vals] or s["columns"][:V.SAMPLE_COLS]
        sample = (f'<p class=pb-lv><b>A few rows</b> <span title="drawn at random; identifying columns left out">'
                  f'{len(s["rows"])} of {s["total"]:,}</span></p><div class=wk-scroll>'
                  + table(tuple(cols), [tuple(esc(r[s["columns"].index(c)]) for c in cols) for r in s["rows"]]) + '</div>')
    return card + f'<div class=in-files>{" ".join(files)}</div>' + sample


def _data_view(b: dict, root: Path) -> str:
    """Data: a side tab per data freeze, its new line and key numbers and files; then the cuts, a side tab each."""
    vs = list(reversed(b["versions"]))
    freezes = _side_tabs("frz", [(V._vlabel(b, str(v.get("version", ""))), f'frozen {v.get("frozen")}' if v.get("frozen") else "")
                                 for v in vs], [_version_panel(b, v, root) for v in vs]) if vs else ""
    r = b["prototype"]["releases"][-1] if b["prototype"]["releases"] else {}
    floor = ((r.get("thresholds") or {}).get("power") or {}).get("smallest_effect_pp")
    return (_section("🗄 Data freezes", freezes or "<p>Add a data freeze in Work.</p>", f"{len(vs)} frozen" if vs else "none yet")
            + _section("✂️ Cuts", _cuts_tabs(b, r, root), f"power floor {floor} points" if floor else "fixed in the plan"))


def _cuts_tabs(b: dict, r: dict, root: Path) -> str:
    """The plan's cuts, a side tab each (round 1: no grey paragraph): where, why, the questions that ask it, its rows
    in each data freeze; the plan's files one click away."""
    parts = r.get("partitions") or []
    if not parts:
        return "<p>The cuts are set in the Prototype's analysis plan.</p>"
    items, panels = [], []
    for p in parts:
        name = str(p.get("name") or "")
        n = {}
        for v in b["versions"]:
            for j in (j for j in b["jobs"] if j["data"] == v.get("version")):
                for t in j["tasks"]:
                    for h in t["hard"]:
                        if (h.get("partition") or "") == name and isinstance(h.get("n"), int) and h["n"] > 0:
                            n.setdefault(str(v.get("version")), h["n"])
        asks = [q for q, row in r["questions"].items() if row.get("asked") == "all" or name in (row.get("asked") or [])
                or row.get("asked") == name]
        rows = ", ".join(f'{V._vlabel(b, k).split(" · ")[0]}: {c:,}' if isinstance(c, int) else f"{k}: {c}" for k, c in n.items())
        items.append((name, V._where(p)))
        panels.append(_kv([("where", f'<code>{esc(V._where(p))}</code>'), ("why", esc(str(p.get("why") or "—"))),
                           ("asked by", esc(", ".join(asks) or "—")), ("rows", esc(rows or "—"))]))
    files = [V._open(r["job"] / f, root, f) for f in ("partitions.md", "thresholds.yaml") if r.get("job") and (r["job"] / f).is_file()]
    head = (f'<p class=in-sub>Fixed in {esc(r.get("label") or r.get("name") or "the plan")} before any outcome.</p>'
            + (f'<div class=in-files>{" ".join(files)}</div>' if files else ""))
    return head + _side_tabs("cut", items, panels)


def _draft_handoff(b: dict) -> dict | None:
    """The handoff drafted and not yet signed: it waits for a person's sign before Design may read it."""
    return next((h for h in b["handoffs"] if not str(h.get("signed") or "").startswith("✅")), None)


def _sign_handoff_row(b: dict, root: Path) -> tuple | None:
    h = _draft_handoff(b)
    return (f'Sign the handoff {h.get("counsel") or h["file"].stem}', "Design reads only a signed handoff",
            "waiting for you", V._open(h["file"], root, h["file"].name, "Read the draft")) if h else None


def _handoff_view(b: dict, root: Path) -> str:
    """Handoff (JL 261106: "the Wisdom drafts, one line each"): what it will say, its draft, what was handed over."""
    signed = [h for h in b["handoffs"] if str(h.get("signed") or "").startswith("✅")]
    draft = _draft_handoff(b)
    wait = f'{draft.get("counsel") or draft["file"].stem} waits for a person\'s sign' if draft else ""
    out = _big("Handed off: " + ", ".join(str(h.get("counsel") or h["file"].stem) for h in signed) if signed else
               "A handoff waits for a person's sign" if draft else "Still to hand off", wait if signed else "")
    j = b["jobs"][-1] if b["jobs"] else None
    w = [t for t in (j["tasks"] if j else []) if t["qid"][:1] == "W"]
    answered = [t for t in w if _written(t)]
    if w:
        r = P.release(b["prototype"], j["release"])
        lines = "".join(f'<li><b>{_jlink(dict(t), root, t["qid"])}</b>{esc(str(t["face"].get("answer") or "its page is still to write"))}'
                        f'<span class=q>{esc(str((r["questions"].get(t["qid"]) or {}).get("question") or ""))} · '
                        f'{esc(str(t["face"].get("answer-status") or "to write"))}</span></li>' for t in w)
        out += _section("🧠 What the handoff will say", f'<ul class=in-wl>{lines}</ul>', f"{len(answered)} of {len(w)} written")
    out += _section("🤝 The handoff draft", _kv([
        ("pair", esc(f'{V._rlabel(b, j["release"])} × {V._vlabel(b, j["data"])}') if j else "no Job yet"),
        ("counsel", esc(f"{len(answered)} of {len(w)} Wisdom answers written" if w else "no Wisdom question in this plan")),
        ("draft", V._open(draft["file"], root, draft["file"].name) if draft else "not written")]),
        "a draft, not signed" if draft else "signed" if signed else "not written")
    if b["handoffs"]:
        out += _section("📦 Handoffs", V._handoff(b, root), f"{len(signed)} signed" if signed else "none signed yet")
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


# ── a Board's Work (b11 j01 s52): the Report's letters, ⚙️ Process then 📊 Results ──────────────────────────────────
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


def _bw_answers(x: dict) -> str:
    j = x["newest"]
    if not j:
        return ""
    state = _overall_state(V._work_facts(j))
    verb = _copy_btn(V._card_prompt("Write the overall report", rel(j["path"], x["root"]), j["name"][:3], j["previous"][:3]),
                     x["session"]) if state == "ready" else ""
    return _step("✍️ The Overall Report", [(f'Write the Overall Report for {j["name"][:3]}', "in the Job, from the answers below it",
                                           state, verb)])


def _bw_questions(x: dict) -> str:
    """Your acts on the next plan (sign it, triage the proposals; both in the Prototype), then new questions."""
    b, root, j = x["b"], x["root"], x["newest"]
    proto = b["prototype"]
    rows = []
    if proto["releases"]:
        r = proto["releases"][-1]
        go = (f'<a class=fd-btn data-pop="{esc(r.get("label") or r["name"])}" href="{esc(_proto_work(r["job"], root))}">Sign in the Prototype</a>'
              if r.get("job") else "")
        signed = str(r["face"].get("signed") or "")
        rows.append((f'Sign the plan {r.get("label") or r["name"]}', "in the Prototype",
                     _done(signed) if signed.startswith("✅") else "waiting for you", "" if signed.startswith("✅") else go))
    open_ = _open_proposals(b)
    if proto["proposals"]:
        pgo = (f'<a class=fd-btn data-pop="proposals" href="{esc(_proto_work(proto["path"], root))}">Open the proposals</a>'
               if open_ and proto["path"].exists() else "")
        rows.append(("Triage the open proposals", "into one batch for the next plan · in the Prototype",
                     "waiting for you" if open_ else "done", pgo))
    out = _step("📋 The next analysis plan", rows) if rows else ""
    new = [("Propose questions", "the gaps and weak answers, as proposals for the next plan",
            "ready" if j else "waits on a Job", _copy_btn(_prompt("Block", "Propose questions", x["folder"]), x["session"]) if j else ""),
           ("Ask a Board question", "a question over the Jobs' answers (board.md ## Questions)", "ready",
            _copy_btn(_prompt("Block", "Ask a Block question", x["folder"]), x["session"]))]
    return out + _step("❓ New questions", new)


def _job_steps(x: dict) -> str:
    """Each Job, its steps (the theme drawing's Board Work › Jobs): a row per Job, each step's state, Open on a Job
    still open."""
    root = x["root"]
    word = lambda s: {"done": "done", "optional": "—", "next": "next", "sign": "your sign", "todo": "to do"}.get(s, s)
    rows = []
    for j in reversed(x["b"]["jobs"]):
        st = V._work_states(j, V._work_facts(j))
        rows.append((_jlink(j, root, f'{j["name"][:3]} · {P.plan_code(j["release"])} × {P.freeze_code(j["data"])}'),)
                    + tuple(esc(word(st[s])) for s in ("2 · Run", "3 · Write", "4 · Check", "6 · Close"))
                    + ("" if j["state"] == "closed" else
                       f'<a class=fd-btn href="{esc(_focus(j["path"], root, "work"))}">Open {esc(j["name"][:3])}</a>',))
    return table(("Job", "Runs", "pages", "checks", "close", ""), rows) if rows else ""


def _bw_jobs(x: dict) -> str:
    j = x["newest"]
    out = ""
    if j:
        st = V._work_states(j, V._work_facts(j))
        step = next((s for s in V.WORK_STEPS if st[s] in ("next", "sign")), "")
        word = (f'{j["name"][:3]} next: {step.split(" · ")[-1].lower()}' if step else "every Job closed"
                if all(o["state"] == "closed" for o in x["b"]["jobs"]) else "done")
        out += _section("🪜 Each Job, its steps", _job_steps(x), word)
    return out + _step("➕ A new Job", [("Add a Job", "a signed analysis plan × a data freeze, one clock moved", "ready",
                                        _copy_btn(_prompt("Block", "Add a Job", x["folder"]), x["session"]))])


def _bw_data(x: dict) -> str:
    return _step("🗄 Freezes and cuts", [
        ("Add a data freeze", "a new extract, frozen, its rows counted per cut", "ready",
         _copy_btn(_prompt("Block", "Add a data version", x["folder"]), x["session"])),
        ("Propose a cut", "to the next analysis plan: a cut is plan, fixed before any outcome", "ready",
         _copy_btn(_prompt("Block", "Propose a cut", x["folder"]), x["session"]))])


def _bw_handoff(x: dict) -> str:
    j = x["newest"]
    w = [t for t in (j["tasks"] if j else []) if t["qid"][:1] == "W"]
    done = [t for t in w if _written(t)]
    ready = bool(w) and len(done) == len(w)
    state = "ready" if ready else "waits on the Wisdom answers" if w else "no Wisdom question yet"
    sign = _sign_handoff_row(x["b"], x["root"])
    signed = any(str(h.get("signed") or "").startswith("✅") for h in x["b"]["handoffs"])
    return _step("🤝 The handoff", [
        ("Write the counsel", "from the latest Job's Wisdom answers", "done" if sign or signed else state,
         _copy_btn(_prompt("Block", "Write the counsel", x["folder"]), x["session"]) if ready and not (sign or signed) else ""),
        sign or ("Draft the handoff", "for a person to sign; Design reads it by its pair",
                 "done" if signed else "waits on the counsel", "")])


BOARD_PROC = {"answers": _bw_answers, "questions": _bw_questions, "jobs": _bw_jobs, "data": _bw_data, "handoff": _bw_handoff}


def board_work_views(block: Path, root: Path, items=(), item_html=None) -> dict:
    """{key: (name, build)}: an insight Board's Work in the Report's letters, ⚙️ Process then 📊 Results (the Report's
    view by the same function; Questions' canvas there in its asking mode), the MindMap last; {} for any other folder.
    `items` and `item_html` are no longer drawn here: the page's own 🙋 Interaction shows each view's forms (R2)."""
    if not is_board(block):
        return {}
    root = root.resolve()
    views = {}
    for key, name in BOARD_VIEWS:
        def build(key=key):
            x = _board_x(block, root)
            if key == "questions":
                res = _questions_view(x["b"], root, {"board": x["folder"],
                                                      "tail": f'Run this in the Claude session "{x["session"]}"; start it if it is not running.'})
            elif key == "answers":                      # the trail through the Jobs is Work's (round 2)
                res = _answers(x["b"], root, work=True)
            else:
                res = BOARD_PARTS[key](x["b"], root)
            return _work_page(BOARD_WORK_CAPTIONS[key], BOARD_PROC[key](x), res)
        views["work-" + key] = (name, build)
    views["work-mindmap"] = _map_view(_parts_map(block, root))
    return views


# ── a Task's Report and Work (b11 j01 s57, s58): Answer · By cut · Across Jobs · Plan ──────────────────────────────
TASK_VIEWS = (("answer", "Answer"), ("by-cut", "By cut"), ("across-jobs", "Across Jobs"), ("plan", "Plan"))
TASK_CAPTIONS = {"answer": "the answer, its evidence, how sure it is and what it rests on",
                 "by-cut": "each cut this question runs on: its takeaway, its figure, its Run and its power",
                 "cites": "the answers it cites, each with its page",
                 "across-jobs": "this question in every Job of the Board",
                 "plan": "what the plan needs from this question, agreed before any Run"}
TASK_WORK_CAPTIONS = {"answer": "the chain of roles, one verb live on the next link, then the answer",
                      "by-cut": "the next act on each cut, then each cut's takeaway, figure, Run and power",
                      "cites": "what it gathers from the answers it cites, then each with its page",
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


def _cited(x: dict) -> list:
    """The Tasks of its Job a page cites, `(K01 · t05)`, in order: what a question with no Run of its own rests on."""
    page = x["t"].get("page")
    text = Path(page).read_text(encoding="utf-8") if page and Path(page).is_file() else ""
    by = {t["name"].split("_", 1)[0]: t for t in x["j"]["tasks"]}
    return [by[n] for n in dict.fromkeys(m.group(2) for m in V.CITE.finditer(text)) if n in by]


def _blank(png: Path) -> bool:
    """A Run's figure whose table holds only zeros (every column complete, 0% missing): it says nothing a number
    does not, so the page says the number instead (round 1, D01: "a key-number tile, not the all-zero chart")."""
    m = re.match(r"^fig_(?:E\d+_)?(.+?)(?:_\d+)?$", png.stem)
    table = png.parent / f"{m.group(1)}.csv" if m else None
    if not table or not table.is_file():
        return False
    try:
        with table.open(encoding="utf-8", newline="") as fh:
            vals = [float(v) for row in csv.DictReader(fh) for v in row.values() if re.fullmatch(r"-?\d+(\.\d+)?", str(v or ""))]
    except (OSError, ValueError):
        return False
    return bool(vals) and all(v == 0 for v in vals)


def _figures(x: dict, run: dict | None = None, keep_blank: bool = False) -> list:
    """The page's figures, first one first: an Executive page's `figures:` (drawn into the Board's delivery), else the
    figures its ok Runs drew, the full cut's first (one Run's only, with `run`); an all-zero chart left out unless
    `keep_blank` (a Data page shows it under its tiles, round 2: "move the missing by column figure into The answer").
    [(png, caption)]."""
    t, j, b = x["t"], x["j"], x["b"]
    figs = [s for s in t["face"].get("figures") or [] if isinstance(s, dict)]
    if figs and run is None:
        part = b["path"] / "delivery" / j["name"]
        return [(V._fig_png(part, j, t["qid"], s.get("name")), str(s.get("title") or s.get("name") or ""))
                for s in figs if V._fig_png(part, j, t["qid"], s.get("name")).is_file()]
    ok = [run] if run is not None else sorted(
        (h for h in t["hard"] if str(h.get("status")) == "ok"),
        key=lambda h: (str(h.get("partition") or "") not in ("full", V.OVERALL), h["run"]))
    name = lambda p: FIG_NAME.sub("", p.stem).replace("_", " ")
    return [(p, f'{name(p)} · {h.get("partition") or h["run"]}')
            for h in ok if str(h.get("status")) == "ok" for p in sorted((Path(h["path"]) / "result").glob("fig_*.png"))
            if keep_blank or not _blank(p)]


FIG_NAME = re.compile(r"^fig_(?:E\d+_)?")
TILE_WORDS = {"n_rows": "rows", "n_cols": "columns", "n_days": "days", "first_day": "first day", "last_day": "last day"}


def _tiles(x: dict) -> str:
    """A Data page's key numbers as tiles (round 1, D01): its whole-extract Run's counts (a flat JSON it wrote) and the
    most any column is missing; '' when its Runs wrote none."""
    full = next((h for h in x["t"]["hard"] if str(h.get("status")) == "ok"
                 and (h.get("partition") or "") in ("full", V.OVERALL)), None)
    if x["t"]["qid"][:1] != "D" or full is None:
        return ""
    res = Path(full["path"]) / "result"
    nums = []
    for f in sorted(res.glob("*.json")):
        try:
            got = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(got, dict):
            nums += [(f"{v:,}" if isinstance(v, int) else str(v), TILE_WORDS.get(k, k.replace("n_", "").replace("_", " ")))
                     for k, v in got.items() if isinstance(v, (int, float, str)) and len(str(v)) <= 12]
    for f in sorted(res.glob("*.csv")):
        try:
            with f.open(encoding="utf-8", newline="") as fh:
                pct = [float(r["null_pct"]) for r in csv.DictReader(fh) if r.get("null_pct") not in (None, "")]
        except (OSError, ValueError, KeyError):
            continue
        if pct:
            nums.append((f"{max(pct):g}%", "missing, the most in any column"))
    return ('<div class=in-card>' + "".join(f'<div><b>{esc(a)}</b><span>{esc(k)}</span></div>' for a, k in nums) + '</div>') if nums else ""


def _sourced(x: dict) -> str:
    """The page's sourced facts: the bullets of its first section, each with its source (a `(K01 · t05)` opens that
    Task's page), as the face holds them (round 1: "the three sourced facts under the answer")."""
    from live.page_reader import markdown_html
    secs = V._sections(x["t"].get("page"))
    for _, md in secs:
        items = [ln for ln in md.splitlines() if ln.startswith("- ")]
        if items:
            html_ = V._cites(markdown_html("\n".join(items)), x["j"], x["root"])
            return html_.replace("<ul>", "<ul class=in-facts>", 1)
    return ""


def _cite_only(x: dict) -> bool:
    """A question with no Run of its own (Wisdom, Executive): it answers from the pages it cites."""
    return x["t"]["qid"][:1] not in V.RUN_LEVELS and not x["t"]["hard"]


def _plan_cites(x: dict) -> list:
    """[(Task, through)]: the questions this one's plan cites, in its Job, then what those rest on (through which);
    then any its written page cites beyond the plan (round 1, W01: "fill What it cites from the plan's needs")."""
    by = {t["qid"]: t for t in x["j"]["tasks"]}

    def cites_of(q):
        return [str(n["from"]).split(".")[0] for n in V._needs(q) if n.get("kind") in ("cite", "reuse")
                and isinstance(n.get("from"), str) and re.match(r"^[DIKWX]\d+", str(n["from"]))]
    out, seen = [], {x["t"]["qid"]}
    for c in cites_of(x["q"]):
        if c in by and c not in seen:
            out.append((by[c], ""))
            seen.add(c)
    for t, _ in list(out):
        for c in cites_of(P.question_of(x["b"]["prototype"], x["j"]["release"], t["qid"])):
            if c in by and c not in seen:
                out.append((by[c], t["qid"]))
                seen.add(c)
    for t in _cited(x):
        if t["qid"] not in seen:
            out.append((t, ""))
            seen.add(t["qid"])
    return out


def _qlabel(x: dict, t: dict) -> str:
    """A question by its id and its words, `I01 · outcome by arm`, never its id alone (round 1)."""
    q = V._spec(P.question_of(x["b"]["prototype"], x["j"]["release"], t["qid"]))
    return f'{t["qid"]} · {q.get("name") or t["name"].split("_", 2)[-1].replace("-", " ")}'


def _answer_pop(t: dict, root: Path, words: str) -> str:
    return _pop("/_board/insight-run?answer=" + rel(Path(t["path"]), root), f'{t["name"]} · the page', esc(words) + " ↗")


def _aligned(t: dict) -> tuple:
    """(verdict, its one line, its pass) of the Task's alignment check, from its newest pass; ('', '', None) without."""
    run = next((r for r in t["soft"] if "alignment" in r["run"]), None)
    passes = sorted((Path(run["path"]) / "passes").glob("*/pass.md")) if run else []
    if not passes:
        return "", "", None
    text = passes[-1].read_text(encoding="utf-8", errors="ignore")
    verdict = text.lstrip().split("\n", 1)[0].lstrip("# ").strip()
    m = re.search(r"(?ms)^## Summary\s*\n(.*?)(?=^## |\Z)", text)
    line = re.split(r"(?<=[.!?])\s+", " ".join((m.group(1) if m else "").split()), maxsplit=1)[0]
    return verdict, line, passes[-1]


def _answer_word(t: dict) -> str:
    """The Answer bar's state, each check named (round 1: "page checked · aligned", never a bare "checked")."""
    words = ["being written" if _writing(t) and not _written(t) else _page_word(t)]
    if str(t["face"].get("check") or "").startswith("✅"):
        words.append("page checked")
    verdict = _aligned(t)[0]
    if verdict:
        words.append(verdict)
    return " · ".join(words)


def _writing(t: dict) -> bool:
    return any(V._rtype(r) == "write" and str(r.get("status") or "").lower() in ("running", "started") for r in t["soft"])


def _last_answer(x: dict) -> tuple | None:
    """(Job, Task) of the newest Job before this one whose page answers the same question: what stands while this
    Job's page is written (round 2, W01: "the last Job's counsel in the headline slot, marked last Job")."""
    jobs = x["b"]["jobs"]
    me = next((i for i, j in enumerate(jobs) if j["name"] == x["j"]["name"]), len(jobs))
    for j in reversed(jobs[:me]):
        t = next((t for t in j["tasks"] if t["qid"] == x["t"]["qid"]), None)
        if t and _written(t):
            return j, t
    return None


def _t_answer(x: dict) -> str:
    """Answer: the answer as the view's headline (the bar stays closed, round 1: settled), then the answer's bar: what
    its one cut adds, its lead picture (a Data page its key numbers, then its figure under them), its sourced facts,
    its page; then how sure it is and what it rests on, each question by its words. A page still to write heads the
    view with the last Job's answer, marked "last Job" (round 2, W01), never with a status line."""
    t, root = x["t"], x["root"]
    fm = t["face"]
    said = str(fm.get("answer") or "").strip()
    last = None if said else _last_answer(x)
    now = "being written" if _writing(t) else "still to write"
    if said:
        head = _big(said)
    elif last:
        head = (_big(str(last[1]["face"]["answer"]))
                + f'<p class=in-sub>{_pill("last Job")} {_jlink(last[0], root)}\'s answer; this Job\'s page is {now}.</p>')
    else:
        head = _big(f"Its page is {now}")
    takes = fm.get("takeaways") if isinstance(fm.get("takeaways"), dict) else {}
    under = (f'<p class=in-sub>{esc(next(iter(takes.values())))}</p>'     # the cross takeaway under the verdict (K01)
             if len(takes) == 1 and str(next(iter(takes.values()))).strip() != said else "")
    tiles = _tiles(x)
    figs = _figures(x, keep_blank=bool(tiles))          # a Data page: its figure under its tiles (round 2, D01)
    lead = figs[0] if figs else None
    first = "" if not lead else (
        f'<figure class=in-fig><a href="/{esc(rel(lead[0], root))}" target=_blank rel=noopener data-pop="{esc(lead[1])}">'
        f'<img src="/{esc(rel(lead[0], root))}" alt="{esc(lead[1])}" loading=lazy></a>'
        f'<figcaption>{esc(lead[1])}</figcaption></figure>')
    thumbs = "".join(f'<a class=ov-thumb data-pop="{esc(c)}" href="/{esc(rel(p, root))}" target=_blank rel=noopener>'
                     f'<img src="/{esc(rel(p, root))}" alt="" loading=lazy><span>{esc(c)}</span></a>' for p, c in figs[1:])
    cites = _plan_cites(x) if _cite_only(x) else []
    if said:
        body = (under + tiles + first + (V.OV_CSS + f'<div class=ov-thumbs>{thumbs}</div>' if thumbs else "")
                + _sourced(x) + f'<p>{V._page_link(t, root)}</p>')
    elif last:                                      # what it rests on is How sure's and By cut's (round 2, W01)
        body = (f'<p class=in-sub>This Job\'s page is {now}; until then {_jlink(last[0], root)}\'s answer stands: '
                f'{_answer_pop(last[1], root, "its page")}</p>')
    else:
        body = (f'<p class=in-sub>Its page is {now}, from the answers it cites.</p>' if cites
                else '<p class=in-sub>Its Runs come first; then its page.</p>')
    big = _section("⚓ The answer", body, _answer_word(t))
    ok = [h for h in t["hard"] if str(h.get("status")) == "ok"]
    plan = [c for c, via in (_plan_cites(x) if not cites else cites) if not via]
    rests = ", ".join([V._run_link(h, root, f'the {h.get("partition") or h["run"]} cut') for h in ok]
                      + [_answer_pop(c, root, _qlabel(x, c)) for c in plan]) or "its Runs, once they run"
    sure = str(fm.get("how-sure") or "").strip() or ("once its page is written" if not said else "not said on its page")
    return head + big + _section("🎯 How sure", _kv([("how sure", esc(sure)), ("rests on", rests)]),
                                 "checked" if str(fm.get("check") or "").startswith("✅") else "not checked yet")


def _power(h: dict) -> str:
    """A cut's power, in words: its card's `power:` and, when its Run wrote partition_power.csv, the smallest gap it
    can see (the minimum detectable effect, in points)."""
    said = str(h.get("power") or "")
    f = Path(h.get("path") or "") / "result" / "partition_power.csv"
    mde = ""
    if f.is_file():
        try:
            with f.open(encoding="utf-8", newline="") as fh:
                row = next(csv.DictReader(fh), {})
            mde = f'can see a gap of {float(row["mde"]):.0f} points or more' if row.get("mde") else ""
        except (OSError, ValueError, KeyError):
            mde = ""
    return " · ".join(w for w in ("enough" if said == "ok" else said, mde) if w) or "—"


CUT_WORD = {"ok": "answered", "refused": "refused", "failed": "failed", "planned": "planned", "running": "running"}


def _t_cuts(x: dict) -> str:
    """By cut: a side tab per cut (round 1, I01: "side tabs, one per cut, a planned cut says planned"), each its
    takeaway, its figure, its Run and its power; a question with no Run of its own (Wisdom, Executive) keeps the view's
    name and shows what it cites instead, each answer with its page."""
    t, root = x["t"], x["root"]
    fm = t["face"]
    if _cite_only(x):
        cites = _plan_cites(x)
        return _section("🔗 What it cites", _cite_chain(x, cites) if cites else
                        "<p class=in-sub>Its plan names the answers it will cite.</p>", _gather_word(x) if cites else "cites none yet")
    takes = fm.get("takeaways") if isinstance(fm.get("takeaways"), dict) else {}
    hard = sorted(t["hard"], key=lambda h: h["run"])
    items, panels = [], []
    for h in hard:
        cut = str(h.get("partition") or h["run"].split("_", 1)[-1])
        st = str(h.get("status") or "planned").lower()
        take = str(takes.get(cut) or "").strip()
        figs = _figures(x, h) if st == "ok" else []
        pics = "".join(f'<figure class=in-tab-fig><a href="/{esc(rel(p, root))}" data-pop="{esc(c)}" target=_blank rel=noopener>'
                       f'<img src="/{esc(rel(p, root))}" alt="{esc(c)}" loading=lazy></a></figure>' for p, c in figs[:2])
        n = h.get("n")
        facts = [("Run", _pop(V.run_url(h["path"], root), h["run"], esc(f'{h["run"]} · {V.MARK.get(st, "·")} {st}'))),
                 ("power", esc(_power(h)) if st == "ok" else "—"), ("rows", esc(f"{n:,}" if isinstance(n, int) and n else "—"))]
        if st == "planned":
            take = take or "Its Run is planned: launch it in Work › By cut."
        elif st == "refused":
            take = take or str(h.get("reason") or "Refused: too thin to answer.")
        items.append((cut, CUT_WORD.get(st, st)))
        panels.append((f'<p class=in-sub>{esc(take)}</p>' if take else "") + pics + _kv(facts))
    ran = sum(str(h.get("status")) in V.FINAL for h in hard)
    if not hard:
        return _section("🔲 By cut", "<p class=in-sub>Its Runs are opened with its Job.</p>", "to launch")
    return _section("🔲 By cut", _side_tabs("cut", items, panels), f"{ran} of {len(hard)} ran")


def _cite_word(c: dict) -> str:
    """One cited question's state, one word from one source (round 2, X01: "four state words for one step"): cited once
    its page in this Job is written, else what it waits on."""
    return "cited" if _written(c) else f"waits on {c['qid']}'s page"


def _gather_word(x: dict) -> str:
    """Gathering what a page cites, in that same word: cited when every question it cites directly is, else the first
    it waits on (the chain row, Work · By cut and What it cites all read this)."""
    direct = [c for c, via in _plan_cites(x) if not via]
    return next((_cite_word(c) for c in direct if not _written(c)), "cited") if direct else "cites none yet"


CHAIN_CSS = """<style>.in-chain{display:flex;flex-direction:column;gap:10px;margin:2px 0 6px}
.in-chain .row{display:flex;flex-wrap:wrap;align-items:stretch;gap:6px 8px}
.in-chain .node{flex:1 1 220px;max-width:380px;border:1px solid var(--line);border-radius:8px;padding:8px 10px;background:var(--paper);
 font-size:13.5px;line-height:1.45}.in-chain .node b{display:block;font-size:14px;margin:0 0 2px}
.in-chain .node .pb-pill{margin-top:4px}.in-chain .to{align-self:center;color:var(--muted);font-size:18px}
.in-chain .to .dn{display:none}
@media(max-width:600px){.in-chain .row{flex-direction:column}.in-chain .node{max-width:none;flex:none}
 .in-chain .to .rt{display:none}.in-chain .to .dn{display:inline}.in-chain .to{align-self:flex-start;padding-left:14px}}</style>"""


def _cite_chain(x: dict, cites: list) -> str:
    """What a page cites drawn as a chain (round 2, W01: "K01 → I01"): a row per question it cites, then the questions
    that one rests on, each a card with its answer and its state word."""
    root = x["root"]

    def node(c, word):
        return (f'<div class=node><b>{_answer_pop(c, root, _qlabel(x, c))}</b>'
                f'{esc(str(c["face"].get("answer") or "its page is still to write"))}<br>{_pill(word)}</div>')
    arrow = '<span class=to title="rests on"><span class=rt>→</span><span class=dn>↓</span></span>'
    rows = []
    for c, via in cites:
        if via:
            continue
        under = [d for d, v in cites if v == c["qid"]]
        rows.append('<div class=row>' + node(c, _cite_word(c))
                    + "".join(arrow + node(d, f"under {c['qid']}") for d in under) + '</div>')
    return CHAIN_CSS + f'<div class=in-chain>{"".join(rows)}</div>'


ACROSS_CSS = """<style>.in-across .st-m{display:none}
@media(max-width:600px){.in-across .st-m{display:block;margin:3px 0 0}.in-across td.st{display:none!important}}</style>"""


def _t_across(x: dict) -> str:
    """This question in each Job: the Job, its answer, its status; under 600 px the status sits under the Job's name
    (round 2: "Across Jobs status cut off at 390 px")."""
    b, t, root = x["b"], x["t"], x["root"]
    rows = []
    for j in b["jobs"]:
        word, tt = _in_job(j, t["qid"])
        if word == "not asked":
            continue
        st = V._st(word)
        rows.append(f'<tr><td>{_jlink(j, root, _pair(j))}<span class=st-m>{st}</span></td>'
                    f'<td>{esc(str((tt or {}).get("face", {}).get("answer") or "—"))}</td><td class=st>{st}</td></tr>')
    grid = (ACROSS_CSS + '<table class="wf-table in-ct in-across"><thead><tr><th>Job</th><th>answer</th><th>status</th></tr>'
            f'</thead><tbody>{"".join(rows)}</tbody></table>')
    return _section("🔁 This question in each Job", grid if rows else "<p class=mut>Only this Job asks it so far.</p>",
                    f"in {len(rows)} Jobs" if len(rows) > 1 else "this Job only")


def _t_plan(x: dict) -> str:
    q, t, root = x["q"], x["t"], x["root"]
    may = next((m for lv, _, m in V.LEVELS if lv == t["qid"][:1]), "")
    spec = V._spec(q)
    needs = V._needs(q)
    need = "<br>".join(esc(str(n.get("need") or n.get("ask") or n.get("what") or n.get("kind") or ""))
                       + (f' <span class=mut>{esc(V._goes(n))}</span>' if V._goes(n) else "") for n in needs) or "—"
    steps = " · ".join(dict.fromkeys(V.STEP.get(str(n.get("kind")), _cap1(str(n.get("kind") or "step"))) for n in needs))
    q = dict(q, question=q.get("question") or spec.get("ask") or spec.get("question") or "")
    return _section("📋 Needs", _kv([("question", esc(q.get("question") or "—")), ("need", need),
                                     ("steps", esc(steps or "—")), ("may say", esc(may.replace("may say: ", ""))),
                                     ("agreed", esc(str(q.get("agreed") or "not yet")))])
                    + (f'<p>{_pop(V.open_url(Path(q["file"]), root), t["qid"], "the question file ↗")}</p>' if q.get("file") else ""),
                    "agreed" if q.get("agreed") else "to agree")


TASK_PARTS = {"answer": _t_answer, "by-cut": _t_cuts, "across-jobs": _t_across, "plan": _t_plan}


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
CHAIN = {"plan": ("Plan the evidence", "writer · in the Prototype, before any Run", ""),
         "agree": ("Agree the plan", "checker · another agent agrees the needs", ""),
         "Runs": ("Run every cut", "the scripts · one Run per cut, from the plan", "Run a partition"),
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
    return _section("🔗 The chain", _todo(rows), word)


def _tw_cuts(x: dict) -> str:
    """By cut's Process: the next act on each cut, a new cut for the next plan; a question with no Run of its own
    gathers what it cites instead (round 1, W01: no "Next on each cut" or "A new cut" there)."""
    if _cite_only(x):
        rows = [(f'Cite {_qlabel(x, c)}', "its page written first", _cite_word(c), "")
                for c, via in _plan_cites(x) if not via]
        return _step("🔗 Gather what it cites", rows) if rows else ""
    rows = []
    for h in x["t"]["hard"]:
        s = str(h.get("status") or "planned")
        if s in ("planned", "failed"):
            rows.append((f'Run the {h.get("partition") or h["run"]} cut', h["run"], "ready",
                         _copy_btn(_prompt("Task", "Run a partition", x["folder"]), x["session"])))
    out = (_step("🔲 Next on each cut", rows) if rows else
           _section("🔲 Next on each cut", "<p>Every cut has run.</p>", "done"))
    proto = rel(x["b"]["prototype"]["path"], x["root"]) if x["b"]["prototype"]["path"].exists() else x["folder"]
    return out + _step("✂️ A new cut", [("Propose a cut to the next plan", "a cut is plan, fixed before any outcome", "ready",
                                        _copy_btn(_prompt("Block", "Propose a cut", proto), x["session"]))])


def _tw_across(x: dict) -> str:
    board = rel(x["b"]["path"], x["root"])
    many = sum(1 for j in x["b"]["jobs"] if any(t["qid"] == x["t"]["qid"] for t in j["tasks"])) > 1
    return _step("🔁 Track", [(f'Track {x["t"]["qid"]} across the Jobs', "its answer Job by Job",
                              "ready" if many else "waits on a second Job",
                              _copy_btn(_prompt("Block", "Draw a track", board), x["session"]) if many else "")])


def _tw_plan(x: dict) -> str:
    q = x["q"]
    return _step("📋 The plan", [("Plan the evidence", "in the Prototype, before any Run", "done" if V._needs(q) or q.get("method") else "to do", ""),
                                ("Agree the plan · another agent", "", _done(q.get("agreed")) if q.get("agreed") else "to do", "")])


TASK_PROC = {"answer": _tw_answer, "by-cut": _tw_cuts, "across-jobs": _tw_across, "plan": _tw_plan}


def task_views(tdir: Path, root: Path, section: str) -> dict:
    """{key: (name, build)}: an insight Task's Report (numbered sections only; the page adds its MindMap) or Work
    (⚙️ Process then 📊 Results, the Report's view by the same function, the MindMap last); {} for any other folder."""
    if not is_task(tdir):
        return {}
    root = root.resolve()
    views = {}
    def cap(key, x, words):                      # a cite-only Task's By cut keeps its name, its caption its own
        return words["cites" if key == "by-cut" and _cite_only(x) else key]
    for key, name in TASK_VIEWS:
        if section == "work":
            def build(key=key):
                x = _task_x(tdir, root)
                return _work_page(cap(key, x, TASK_WORK_CAPTIONS), TASK_PROC[key](x), TASK_PARTS[key](x))
            views["work-" + key] = (name, build)
        else:
            def build(key=key):
                x = _task_x(tdir, root)
                return _page(cap(key, x, TASK_CAPTIONS), _numbered(TASK_PARTS[key](x)))
            views[key] = (name, build)
    if section == "work":
        views["work-mindmap"] = _map_view(_task_mindmap(tdir, root))
    else:
        views["mindmap"] = ("MindMap", _task_mindmap(tdir, root))
    return views


# ── a Prototype's own parts (the shared page asks; round 1, 261106: "a Prototype is insight's") ────────────────────
def prototype_parts(folder: Path, root: Path, level: str) -> list:
    """A Prototype's Findings parts before 📦 Delivery: the questions by release (Block) or by DIKW level (a release),
    each in words with its script; the proposals; the cuts (insight_prototype.py)."""
    from live import insight_prototype as PR
    return PR.parts(folder, root, level)


def prototype_delivery_tabs(folder: Path, root: Path, level: str) -> list:
    """A Prototype's 📦 Delivery tabs, in place of the shared lanes: each release and the files a Board Job pins."""
    from live import insight_prototype as PR
    return PR.delivery_tabs(folder, root, level)


def prototype_status(folder: Path, root: Path, level: str) -> list:
    """A Prototype's Status bars in place of the shared ones: each release by its state and sign, each question by
    question.md and its Runs; a question its Runs (insight_prototype.py)."""
    from live import insight_prototype as PR
    return PR.status(folder, root, level)


def prototype_process(folder: Path, root: Path, level: str, view: str) -> list | None:
    """A Prototype's ⚙️ Process steps on a Work view, in place of the shared ones: on Findings triage its proposals
    and sign the analysis plan, each a Copy prompt; on Status each question's next step, or "nothing to do"; None
    leaves the shared steps (insight_prototype.process)."""
    from live import insight_prototype as PR
    return PR.process(folder, root, level, view)


def prototype_lead(folder: Path, root: Path, level: str, view: str) -> str:
    """The main line a Prototype's Status or Findings opens with (insight_prototype.lead)."""
    from live import insight_prototype as PR
    return PR.lead(folder, root, level, view)


def prototype_map_branches(folder: Path, root: Path, level: str) -> list:
    """A release's MindMap: its questions by DIKW level, each leaf the question (insight_prototype.map_branches)."""
    from live import insight_prototype as PR
    return PR.map_branches(folder, root, level)


# ── which view a form belongs to (focus_page.view_items asks; R2, 261106) ──────────────────────────────────────────
def view_of_item(row: dict, folder: Path, root: Path, level: str, keys) -> str | None:
    """The view whose 🙋 Interaction shows a form, by what it is about: at a Board, a Wisdom Task's form under Handoff,
    an Executive one's under Answers, a form about the questions or the data under that view, the rest of its Jobs'
    under Jobs; at a Job, an Executive Task's form under Overall, the rest under Grid; at a Task, under Answer. None
    leaves it to the page's default (the page's own forms under MindMap)."""
    page = Path(row.get("page") or folder)
    topic = row.get("topic")
    about = (getattr(topic, "name", "") or "") + " " + str(row.get("about") or "")
    m = next((P.TASK_NAME.match(p.name) for p in [page, *page.parents] if P.TASK_NAME.match(p.name)), None)
    qid = m.group(1) if m else ""
    if level == "Block":
        if qid[:1] == "W" or re.search(r"handoff|counsel", about, re.I):
            return "handoff"
        if qid[:1] == "X":
            return "answers"
        if page == folder and re.search(r"question|proposal|plan", about, re.I):
            return "questions"
        if page == folder and re.search(r"data|freeze|cut", about, re.I):
            return "data"
        return "jobs" if page != folder else None
    if level == "Job":
        return "overall" if qid[:1] == "X" or page == folder else "grid"
    if level == "Task":
        return "answer"
    return None
