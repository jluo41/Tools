"""A draft Task on the focus page (`layout=focus`), b32 s42-draft-task-focus-page.

The base page (focus_page.py) asks this module, through one hook (`parts`), for what a Task whose face says
`task-type: draft` shows in each section. Each section has its own aim (haipipe-ui): Report checks, Work does,
Studio thinks, Delivery hands over (JL 261031: "for each page, we have the report, work, and studio, they serve
differnet aims"). Under each view the content is sections, a heading each, never folds or a card in a card (JL
261031: "under each view, we will have the sections"):

    Report     MindMap · Text · Status
    Work       1 · Plan · 2 · Write · 3 · Evidence · 4 · Display · 5 · Revise · Runs
    Studio     the base Studio, fed the Block topics that name this Task
    Delivery   the four operations, the built files, the pages, the sends

Each Work step reads draft_steps' own builders (what the old page showed, JL 261031: "put the old ones back to here
so we can operate on it ourself"), drawn with FLAT set so their Result cards come out as sections. Nothing here
writes: the copy buttons copy a prompt; the cards, comments and Scratch post through the existing actions.
"""
from __future__ import annotations

import html as _html
import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import esc, face, runs_of
from live.ui_parts import GROUP_CSS, PROCESS, RESULTS, _band, _numbered, _file_link, _section, _when


WORK = (("plan", "1 · Plan"), ("write", "2 · Write"), ("evidence", "3 · Evidence"), ("display", "4 · Display"),
        ("revise", "5 · Revise"))


STATE_WORD = {"done": "done", "next": "next", "sign": "sign", "asked": "asked", "send": "send", "optional": "optional",
              "pass": "pass {k}", "todo": "later"}


WAITS = ("sign", "asked", "send", "pass")              # a word the person acts on, shown in the warn colour


# what a step waits for, said once in its first row; the verb the person uses is on the row
ASKS = {"1 · Plan": {"sign": "Waits for your sign: ✅ on <code>approved:</code> in the draft."},
        "3 · Evidence": {"asked": "Waiting for you: tick each ask, and settle each open point."},
        "4 · Display": {"sign": "Waiting for you: write <code>accepted:</code> in each display's README."},
        "5 · Revise": {"pass": "Waiting for you: accept or reject each card."},
        "Delivery": {"send": "Waiting for you: check the built files, then mark the send in <code>delivery.md</code>."}}


# the button on each prompt: the step's own verb, so the row says what the copy is for
VERBS = {"plan": "Copy prompt: plan", "write": "Copy prompt: write", "evidence": "Copy prompt: find evidence",
         "display": "Copy prompt: make the displays", "revise": "Copy prompt: revise", "studio": "Copy prompt: talk and sketch",
         "delivery-build": "Copy prompt: build", "delivery-render": "Copy prompt: render the pages",
         "delivery-send": "Copy prompt: check", "delivery-back": "Copy prompt: read back"}


# the Task's Runs each step makes, by the start of their names (haipipe-draft's Run families)
RUN_PREFIX = {"1 · Plan": ("run-structure", "run-context", "run-scratch"),
              "2 · Write": ("run-section", "run-write", "run-paragraph"),
              "3 · Evidence": ("run-value", "run-citation", "run-evidence"),
              "4 · Display": ("run-display",),
              "5 · Revise": ("run-revise", "run-paragraph", "run-section"),
              "Delivery": ("run-delivery", "run-check")}


CAPTIONS = {"plan": "The plan: its paragraphs and their points, before the sentences.",
            "write": "The text, and your own sentences typed beside it.",
            "evidence": "The text beside the evidence for each sentence, and what is still open.",
            "display": "The Tables and Figures the text calls, each beside its sentence.",
            "revise": "The text beside its review cards: accept or reject each change.",
            "runs": "Every Run of this Task.",
            "pdf": "The Section as the LaTeX build prints it.", "web": "The Section as a web page.",
            "word": "The Word file, through the PDF the build writes beside it.",
            "files": "Every built file, the sends, the Runs, and the prompts that build them.",
            "paper": "The whole paper, as the LaTeX build prints it.", "supplement": "The supplement, through its PDF twin.",
            "mindmap": "The content as a map: each part, then what it holds.",
            "text": "Each sentence beside its evidence, its changes and the review's notes.",
            "status": "Where each step stands, and what waits for you."}


PROMPT = re.compile(r'<details class=run-prompt-box open><summary>(.*?) <button type=button class="run-copy work-act" '
                    r'data-copy="([^"]*)"(?: data-tail="([^"]*)")?>Copy prompt</button></summary>.*?'
                    r'data-key="([^"]*)"', re.S)


INPUT = re.compile(r"<h4>Input</h4>(<table.*?</table>)", re.S)


# the folds draft_steps writes by hand (an example, an Evidence card, the open points, a display, the canvas, the
# Scratch editor), each with no fold inside: on this page each is a section under its heading
FOLD = re.compile(r'<details class="topic work-task(?: items-step)?"(?: open)?><summary>(.*?)</summary>(.*?)</details>', re.S)


LAZY = re.compile(r'<iframe class=st-frame title="([^"]*)" data-src="([^"]*)"[^>]*></iframe>')


# the common workbench width, the title at the same x as every page (JL 261031, b10-s33-D06: paper pages use the
# common width, no verb after the section word); only the draft's own rules stay here
WIDE = """<style>.section-views{flex-wrap:wrap}.section-views a{white-space:nowrap}
.pm-role:empty::before{content:"no role";color:var(--muted);font-size:11px}
.rv-split.wr-split{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
.wr-split .rv-right iframe,.fd-sec iframe.space-frame{display:block;width:100%}
</style>"""


CSS = """<style>
/* the box is the heading bar only; the content follows below it, unboxed (JL 261031: "could we put the box just in the
   section? and the content below it we should be outside of the box") */
.fd-sec{margin:0 0 12px}
.fd-h{font-size:15px;font-weight:600;margin:0;display:flex;align-items:center;gap:8px;border:1px solid var(--line);
 border-radius:8px;background:var(--paper);padding:8px 14px}.fd-h::before{flex:none}
.fd-h>.topic-pop,.fd-h>.fd-verb{margin-left:auto;font-size:12.5px;font-weight:400}
.fd-h .topic-pop a{border:1px solid var(--line);border-radius:6px;padding:2px 10px;text-decoration:none}
.fd-body{margin:10px 0 18px;padding:0 2px;overflow-x:auto}.fd-body[hidden]{display:none}
.fd-body .pm-edit{max-height:85vh;overflow:auto;border:1px solid var(--line);border-radius:6px;padding:8px}   /* the map's own frame */
/* one frame level: what sits inside a section's box draws no second box (haipipe-ui review 261031) */
.fd-sec .fd-sec>.fd-h{border:0;padding:4px 0;background:none}.fd-body .space-empty{border:0;padding:0;background:none}
.fd-body pre,.fd-body .raw-source{border:0;background:var(--wash)}
@media(max-width:700px){.rv-split.wr-split{grid-template-columns:minmax(0,1fr)}}
.focus-content:has(>.fd-sec,>section>.fd-sec){border:0;padding-left:0;padding-right:0;background:none}
.fd-h[data-fold]{cursor:pointer;user-select:none}.fd-h[data-fold]::before{content:"▾";display:inline-block;width:16px;
 color:var(--muted);font-size:12px}.fd-h[aria-expanded="false"]::before{content:"▸"}.fd-h[data-fold]:hover{color:var(--accent)}
.fd-ask{display:flex;align-items:center;gap:12px;padding:9px 14px;border:1px solid var(--line);border-left:3px solid #b35c00;
 border-radius:6px;margin:0 0 12px;font-size:14px}.fd-ask span{flex:1}
.fd-run{margin:0 0 6px}.fd-run textarea{width:100%;min-height:36px;resize:vertical;border:1px solid var(--line);border-radius:5px;
 background:var(--wash);padding:6px 10px;font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink)}
.fd-run .fd-bar{display:flex;gap:8px;align-items:center;margin-top:4px}.fd-run .fd-bar small{color:var(--muted);font-size:12px}
.fd-btn{font-size:12px;border:1px solid var(--line);border-radius:5px;padding:3px 10px;background:var(--paper);color:var(--ink);
 cursor:pointer;white-space:nowrap;text-decoration:none}.fd-btn:hover{border-color:var(--accent);text-decoration:none}
.fd-row{display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid var(--line);font-size:14px}
.fd-row .n{min-width:170px;font-weight:500;overflow-wrap:anywhere}.fd-row .d{flex:1;color:var(--muted);font-size:13px}
.fd-row .w{font-size:12px;white-space:nowrap}
.fd-you{color:#b35c00;font-weight:600}.fd-ok{color:#2b8a3e}
.section-views a .vw{font-size:11px;margin-left:5px;color:var(--muted)}.section-views a .vw.fd-you{color:#b35c00}
.section-views a .vw.fd-ok{color:#2b8a3e}
.fd-text h3{font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin:18px 0 4px}
.fd-text p{font-size:16px;line-height:1.7;margin:0 0 10px}
@media(max-width:600px){.fd-body td,.fd-body th{min-width:120px}.fd-body pre{white-space:pre-wrap;overflow-wrap:anywhere}
 .fd-row{flex-wrap:wrap}.fd-row .n{min-width:0}}
</style>"""


JS = """<script>(function(){
 if(window.fdCopy)return;window.fdCopy=1;
 function get(k){try{return localStorage.getItem(k)||'';}catch(e){return '';}}   /* the old page's key: the same notes */
 function put(k,v){try{localStorage.setItem(k,v);}catch(e){}}
 function ready(fn){if(document.readyState!=='loading')fn();else document.addEventListener('DOMContentLoaded',fn);}
 ready(function(){
  document.querySelectorAll('.fd-run textarea[data-key]').forEach(function(t){
   if(!t.value)t.value=get(t.dataset.key);t.addEventListener('input',function(){put(t.dataset.key,t.value);});});
  /* each section folds by its heading, open by default; what you fold stays folded in this browser (JL 261031:
     "for the view page's subsection, could they be like collapse as well") */
  var page=new URLSearchParams(location.search),at='fd-fold:'+(page.get('path')||'')+':'+(page.get('section')||'')+':'+(page.get('group')||'');
  var shut={};try{shut=JSON.parse(localStorage.getItem(at)||'{}');}catch(e){}
  document.querySelectorAll('section.fd-sec').forEach(function(sec){
   var h=sec.querySelector(':scope>h3.fd-h');if(!h||h.dataset.fold)return;
   var body=document.createElement('div');body.className='fd-body';
   while(h.nextSibling)body.appendChild(h.nextSibling);sec.appendChild(body);
   var key=h.textContent.trim().slice(0,80);h.dataset.fold='1';h.tabIndex=0;h.setAttribute('role','button');
   function set(open){body.hidden=!open;h.setAttribute('aria-expanded',String(open));}
   set(!shut[key]);
   function flip(){var open=body.hidden;set(open);if(open)delete shut[key];else shut[key]=1;
    try{localStorage.setItem(at,JSON.stringify(shut));}catch(e){}window.dispatchEvent(new Event('resize'));}
   h.addEventListener('click',function(ev){if(ev.target.closest('a,button'))return;flip();});
   h.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();flip();}});
  });
 });
 document.addEventListener('click',function(ev){
  var b=ev.target.closest('.fd-copy,.run-copy');if(!b)return;ev.preventDefault();
  var box=b.closest('.fd-run,.run-prompt-box'),notes=box&&box.querySelector('textarea');
  var text=b.dataset.copy||'';if(notes&&notes.value.trim())text+='\\nuser feedback: '+notes.value.trim();
  if(b.dataset.tail)text+='\\n'+b.dataset.tail;
  var was=b.textContent,done=function(){b.textContent='Copied';setTimeout(function(){b.textContent=was;},1400);};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(text).then(done,done);else done();
 });
})();</script>"""


# the classes draft_steps' HTML is drawn with that only the old page's stylesheet defines (frame.CSS, frame.WORK_CSS,
# runs_panel.PANEL_CSS, space_views.SPACE_VIEW_CSS): borrowed rule by rule, so their look keeps one owner
BORROW = ("wf-table", ".st{", ".st ", ".st-ok", ".st-warn", ".st-bar", "chip", "stage", "topic-meta", "topic-pop",
          "space-reads", "space-empty", "space-source", "run-prompt", "work-act", "dl-note", "dl-src")


TOKENS = (":root{--ok:light-dark(#24733d,#8bd49a);--warn:light-dark(#996b00,#e4bd62);--miss:light-dark(#c92a2a,#ff8787);"
          "--tab-line:light-dark(#ced4da,#414852);--tab-on:light-dark(#1864ab,#91caff);--tab-wash:light-dark(#e7f5ff,#253749)}"
          ".focus-content table{display:table}")          # focus.css blocks every table, which shrinks a width:100% one


def _rules(css: str) -> list:
    """The top-level rules of a stylesheet (an @media block is left out: the focus page has its own)."""
    out, depth, start = [], 0, 0
    for i, ch in enumerate(css):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                out.append(css[start:i + 1].strip())
                start = i + 1
    return [r for r in out if not r.startswith("@")]


def borrowed_css() -> str:
    from live import frame
    sheets = [frame.CSS, frame.WORK_CSS]
    for mod, name in (("runs_panel", "PANEL_CSS"), ("space_views", "SPACE_VIEW_CSS")):
        try:
            sheets.append(getattr(__import__(f"live.{mod}", fromlist=[name]), name))
        except Exception:
            pass
    keep = [r for css in sheets for r in _rules(css) if "::before" not in r and any(b in r.split("{", 1)[0] + "{" for b in BORROW)]
    return "<style>" + TOKENS + "".join(keep) + "</style>"


SECTION_VERBS = {"report": "check", "work": "do", "studio": "think", "delivery": "hand over", "timeline": "look back",
                 "files": "browse", "related": "take in"}


def is_draft(folder: Path) -> bool:
    from live.frame import task_type
    return task_type(folder) == "draft"


def word(state: str, k: int = 1) -> tuple:
    """(the state's word, its class): a step's state as a word (haipipe-ui rule 5), warn when it waits on you."""
    w = STATE_WORD.get(state, state).format(k=k)
    return w, "fd-you" if state in WAITS else "fd-ok" if state == "done" else ""


def _facts(folder: Path, root: Path) -> tuple:
    f = ds.facts(folder, root)
    st = ds.states(f)
    k = len((f["draft"] or {}).get("previous", [])) + 1
    return f, st, k


def _prompts(op: str) -> list:
    """[(its title, prompt, tail, notes key)] of the old Operation's prompt boxes, the prompt text as draft_steps
    wrote it (one owner of every prompt)."""
    return [(re.sub(r"<[^>]+>", "", _html.unescape(t)).strip(), _html.unescape(c), _html.unescape(tail or ""),
             _html.unescape(key)) for t, c, tail, key in PROMPT.findall(op)]


def _run_rows(prompts: list) -> str:
    """The prompts as verbs: one box for your notes, then a button per prompt that copies it with them (and the line
    that sends it to the Task's session); the prompt itself shows when you rest on its button."""
    if not prompts:
        return ""
    buttons = "".join(f'<button type=button class="fd-btn fd-copy" title="{esc(prompt)}" data-copy="{esc(prompt)}"'
                      + (f' data-tail="{esc(tail)}"' if tail else "")
                      + f'>{esc(VERBS.get(key.rsplit("#", 1)[-1], "Copy prompt"))}</button>'
                      for title, prompt, tail, key in prompts)
    return (f'<div class=fd-run><textarea rows=1 data-key="{esc(prompts[0][3])}" placeholder="your notes, copied with '
            f'the prompt"></textarea><div class=fd-bar>{buttons}</div></div>')


def _ask(step: str, state: str, draft: Path | None = None, root: Path | None = None) -> str:
    """What the step waits for, one row, with Open: the draft, where the person signs."""
    text = ASKS.get(step, {}).get(state)
    if not text:
        return ""
    from live.frame import reader
    open_ = (f'<a class=fd-btn data-pop="{esc(draft.name)}" href="{esc(reader(draft, root))}">Open the draft</a>'
             if draft and root and draft.is_file() else "")
    return f'<div class=fd-ask role=status><span>{text}</span>{open_}</div>'


def _runs(folder: Path, root: Path, step: str) -> str:
    """The Task's own Runs this step makes, one row each: name, type, status."""
    rows = [r for r in runs_of(folder) if r["run"].startswith(RUN_PREFIX.get(step, ("\0",)))]
    if not rows:
        return ""
    return _section("🏃 Runs of this step", "".join(
        f'<div class=fd-row><span class=n><code>{esc(r["run"])}</code></span><span class=d>{esc(r["type"])}</span>'
        f'<span class=w>{esc(r["status"])}</span></div>' for r in rows))


def _interactions(folder: Path, root: Path) -> str:
    """This Task's own interactions (JL 261101: "add the Interaction things as well, so we can track our changes along
    the way"): each form that waits, with Answer, then each decided record, newest first, with See answers."""
    rows = []
    for run in sorted((folder / "runs").glob("r*_collect_*"), reverse=True):
        card = (run / "run.yaml").read_text(encoding="utf-8", errors="ignore") if (run / "run.yaml").is_file() else ""
        status = (re.search(r"(?m)^status:\s*(\S+)", card) or [None, ""])[1]
        q = run / "question_collection.md"
        title = (re.search(r"(?m)^#\s+(.+)$", q.read_text(encoding="utf-8", errors="ignore")) or [None, run.name])[1] \
            if q.is_file() else run.name
        page = run / f"{run.name}.html"
        href = "/" + quote(ds._rel(page, root)) if page.is_file() else ""
        waiting = status == "waiting"
        verb = f'<a class=fd-btn data-pop="{esc(title)}" href="{esc(href)}">{"Answer" if waiting else "See answers"}</a>' if href else ""
        rows.append((0 if waiting else 1, f'<div class={"fd-ask" if waiting else "fd-row"}><span class=n>{esc(title)}</span>'
                                          f'<span class=d>{"waits for you" if waiting else "decided"}</span>{verb}</div>'))
    return "".join(r for _, r in sorted(rows, key=lambda x: x[0]))


def flatten(html: str) -> str:
    """Every fold left in a step's HTML becomes a section, its summary the heading; a drawing that loaded only when its
    fold opened becomes Open, in the popup (haipipe-ui rule 4: no fold arrows; a large view opens in the popup)."""
    html = LAZY.sub(lambda m: f'<p><a class=fd-btn data-pop="{m.group(1)}" href="{m.group(2)}">Open the drawing</a></p>', html)
    return FOLD.sub(lambda m: f'<section class=fd-sec><h3 class=fd-h>{m.group(1).replace(">↗</a>", ">Open ↗</a>")}</h3>'
                    f'{re.sub(r"^<div class=work-body[^>]*>(.*)</div>$", lambda b: b.group(1), m.group(2), flags=re.S)}</section>',
                    html)


def _after_first_section(html: str, extra: str) -> str:
    """`extra` placed after the first section (Scratch, a note per paragraph, right under the plan it annotates)."""
    first = html.find("<section class=fd-sec>")
    second = html.find("<section class=fd-sec>", first + 1) if first >= 0 else -1
    return html[:second] + extra + html[second:] if second > 0 else html + extra


# "Ask the agent" only where JL asked for prompts, structure and drafting (JL 261020); elsewhere it was clutter (JL
# 260927, and 261031 on 4 · Display: "I don't think we need this")
ASK_STEPS = ("1 · Plan", "2 · Write", "5 · Revise")


def step_html(folder: Path, root: Path, step: str) -> str:
    """One step, its sections in order: what waits for you, Ask the agent (the prompts as verbs), the step's Result
    cards (each a section), its Input, its Runs. Scratch (1 · Plan) is the Page's own editor, as on the old page."""
    f, st, k = _facts(folder, root)
    token = ds.FLAT.set(True)
    try:
        op, result, _ = ds.STEP_VIEWS[step](f, folder, root, st[step])
        scratch = (ds._editor(folder, root, "Scratch · your notes, a paragraph each", view="scratch", open_=True)
                   if step == "1 · Plan" and f["draft"] and f["draft"]["structure"] else "")
        running = ds._running(f, step)
    finally:
        ds.FLAT.reset(token)
    table = INPUT.search(op)
    sign = re.search(r"<p class=sign-row>(.*?)</p>|<p><span class=\"st st-ok\">✓ signed</span>(.*?)</p>", op, re.S)
    signed = (f'<p class=mut>✓ signed {sign.group(2)}</p>' if sign and sign.group(2) else "")
    # The same sections as before, in the two parts every view has (JL 261101: "keep the previous draft workbench,
    # keep the content as much as possible but use the new subsections layout"): ⚙️ Process, the step's input, prompt
    # and sign (b15 s58), then 📊 Results, the step's own cards; each part numbered from 1.
    waits = running + _ask(step, st[step], (f["draft"] or {}).get("file"), root) + signed + _interactions(folder, root)
    process = (_section("🙋 Interactions", waits) if waits else _section("🙋 Nothing waits on you", "<span hidden></span>"))
    boxes = "".join(re.findall(r"<!--pb-prompt-->.*?<!--/pb-prompt-->", op, re.S))   # the shared Prompt boxes, whole
    process += _section("🤖 Ask the agent", boxes) if step in ASK_STEPS and boxes else ""
    process += _section("📥 Input", table.group(1) if table else "") + _runs(folder, root, step)
    results = _after_first_section(flatten(result), flatten(scratch))
    return CSS + GROUP_CSS + _band(PROCESS, _numbered(process)) + _band(RESULTS, _numbered(results)) + JS


def work_views(folder: Path, root: Path) -> tuple:
    """({key: (name, html builder)}, {key: (word, class)}, the step a bare link opens): Work's view-button-list."""
    f, st, k = _facts(folder, root)
    # a view with nothing in it does not show (haipipe-ui; JL 261031): no Display when no display is called or made
    steps = [(key, step) for key, step in WORK if key != "display" or f["displays"]]
    views = {key: (step, (lambda s=step: step_html(folder, root, s))) for key, step in steps}
    words = {key: word(st[step], k) for key, step in steps}
    waiting = next((key for key, step in steps if st[step] in ("sign", "asked", "pass", "next")), "plan")
    return views, words, waiting


# ── Report: check ───────────────────────────────────────────────────────────────────────────────────
def paragraphs(folder: Path) -> list:
    """[(paragraph id, its name, its text)] of the face's adopted `## Content` (`#### C1.P1 · Background · S1 to S2`)."""
    md = face(folder)
    text = md.read_text(encoding="utf-8", errors="ignore") if md else ""
    text = text.split("\n## Content", 1)[1] if "\n## Content" in text else ""
    text = re.split(r"(?m)^## ", text, maxsplit=1)[0]
    out = []
    for head, body in re.findall(r"(?ms)^#### (.+?)\n(.*?)(?=^#{2,4} |\Z)", text):
        pid, _, rest = head.partition(" · ")
        body = "\n".join(line for line in re.sub(r"<!--.*?-->", "", body, flags=re.S).splitlines()
                          if not line.lstrip().startswith(">"))   # a working note (> Value:, > Note:) is not the text
        words = " ".join(body.split())
        out.append((pid.strip(), rest.split(" · ")[0].strip(), words))
    return out


READ_ONLY = ("<style>.fd-read .rv-acts,.fd-read .nt-acts,.fd-read .nt-box,.fd-read .nt-plus,.fd-read .nt-gut,"
             ".fd-read .rv-accept-all{display:none!important}</style>")


def text_html(folder: Path, root: Path) -> str:
    """The Section at sentence level (JL 261031: "why there are no things like sentence level, and the tracking, and
    the evidence etc. left and right panel"): the newest draft, one sentence a row with its S number, and on the right
    each sentence's cards, in reading order: its evidence, its changes (old to new, the tracking), the review's logic
    and the comments, each kind switched on or off above. Report checks, so the cards are read here, never decided:
    Accept, Reject and comments are Work › 5 · Revise's. A draft not yet written shows the adopted Content."""
    f = ds.facts(folder, root)
    d = f["draft"]
    if d and d["text"]:
        token = ds.FLAT.set(True)
        try:
            board = ds._text_and_cards(d, f["ev"], root, f["revise"], folder)
            if "No Revise cards yet" in board:          # no pass yet: each sentence beside its evidence and open points
                board = ds._text_and_evidence(d, f["ev"], root, ds._open_points(d), f["displays"])
        finally:
            ds.FLAT.reset(token)
        if board:
            return CSS + READ_ONLY + f'<div class=fd-read>{flatten(board)}</div>'
    paras = paragraphs(folder)
    if paras:
        body = "".join(f'<h3>{esc(name or pid)}</h3><p>{esc(t)}</p>' for pid, name, t in paras if t)
        return CSS + f'<div class=fd-text>{body}</div>'
    return '<p class=mut>No text yet: 2 · Write writes it.</p>'


STATUS_WHAT = {"done": "done", "next": "comes next", "sign": "waits for your sign", "asked": "waits for your ticks",
               "send": "built, waits for your send", "optional": "optional", "pass": "pass {k}: cards wait for you",
               "todo": "later"}


def status_html(folder: Path, root: Path, url) -> str:
    """Each step, one row: its name, what it waits for, its state word, Go (into Work, or the rail's section)."""
    f, st, k = _facts(folder, root)
    rows = []
    for step in ds.STEPS:
        key = dict((s, kk) for kk, s in WORK).get(step)
        href = url("work", key) if key else url(step.lower(), "")
        w, cls = word(st[step], k)
        rows.append(f'<div class=fd-row><span class=n>{esc(step)}</span><span class=d>{esc(STATUS_WHAT[st[step]].format(k=k))}'
                    f'</span><span class="w {cls}">{esc(w)}</span><a class=fd-btn href="{esc(href)}">Go</a></div>')
    return CSS + "".join(rows)


def report_views(folder: Path, root: Path, url) -> dict:
    """Report's views after MindMap: Text, Status (the base adds MindMap first and Questions last). The review report
    is Work › 5 · Revise's, beside the cards it judges (JL 261031: "the revise should be in the Work Section")."""
    return {"text": ("Text", lambda: text_html(folder, root)),
            "status": ("Status", lambda: status_html(folder, root, url))}


# ── Studio and Delivery ─────────────────────────────────────────────────────────────────────────────
def studio_inventory(folder: Path, root: Path) -> list:
    """(source, topic, drawings) of the Block topics whose face names this Task: what the base Studio lists."""
    try:
        return ds._studio_topics(folder, root)
    except Exception:
        return []


def studio_top(folder: Path, root: Path) -> str:
    """Above the base Studio's rows: the Studio step's prompt as a verb (talk and sketch); "none yet" when no topic
    names this Task."""
    f, st, k = _facts(folder, root)
    op, _, _ = ds._studio(f, folder, root, st["Studio"])
    none = "" if f["topics"] else f'<p class=mut>No Studio topic names {esc(folder.name)} yet.</p>'
    return CSS + none + JS


READER = (".pdf", ".docx", ".html")             # what a reader opens; .tex, .json and -view.html stay in Files only


PREVIEW_CSS = ("<style>.fd-prev{display:block;width:100%;height:calc(100vh - 300px);min-height:620px;border:1px solid "
               "var(--line);border-radius:6px;background:#fff}.fd-prev-h{font-size:13px;color:var(--muted);margin:0 0 8px}"
               "</style>")


def preview(f: Path | None, root: Path, also: Path | None = None) -> str:
    """One built file, previewed in the page (JL 261007: "the card and the preview of the results, the embedded
    content"; JL 261031: "I thnk we want to make it to be previewed here"): its name, state and built time, Open ↗ to a
    new tab, then the file itself; Word through the PDF twin the build writes beside the .docx (`also`)."""
    if not f or not f.is_file():
        return '<p class=mut>Not built yet: Files › Ask the agent builds it.</p>'
    url = "/" + quote(ds._rel(f, root))
    state = "draft" if "-draft" in f.stem else "built"
    extra = f' · {_file_link(also, root)}' if also and also.is_file() else ""
    return (PREVIEW_CSS + f'<p class=fd-prev-h>{esc(f.name)}{extra} · {state} · {_when(f)} · '
            f'<a href="{esc(url)}" target=_blank rel=noopener>Open ↗</a></p>'
            f'<iframe class=fd-prev src="{esc(url)}" loading=lazy title="{esc(f.name)}"></iframe>')


def delivery_html(folder: Path, root: Path) -> str:
    """A Section's Delivery › Files: each lane's reader files (current or not built), the rendered pages, the sends,
    the Runs, and last the prompts (build, render, check, read back). The send itself waits on the version page."""
    f, st, k = _facts(folder, root)
    token = ds.FLAT.set(True)
    try:
        op, _, _ = ds._delivery_step(f, folder, root, st["Delivery"])
    finally:
        ds.FLAT.reset(token)
    try:
        from live.delivery import check_delivery
        lanes = check_delivery(f["md"]).get("lanes", []) if f["md"] else []
    except Exception:
        lanes = []
    url = lambda p: "/" + quote(ds._rel(p, root))
    rows = []
    for lane in lanes:
        key = lane.get("lane", "")
        ldir = ds.delivery_read_lane_dir(folder, key)
        files = sorted(p for p in ldir.rglob("*") if p.is_file() and p.suffix in READER and not p.name.startswith(".")
                       and not p.stem.endswith("-view")) if ldir.is_dir() else []
        state = {"pass": "current", "stale": "stale", "not-built": "not built"}.get(lane.get("state", ""), lane.get("state", ""))
        cls = "fd-ok" if state == "current" else "fd-you" if state == "stale" else ""
        links = " · ".join(_file_link(p, root) for p in files) or "nothing built"
        rows.append(f'<div class=fd-row><span class=n>{esc(ds.LANE_ICON.get(key, ""))} {esc(lane.get("label", key))}</span>'
                    f'<span class=d>{links}</span><span class="w {cls}">{esc(state)}</span></div>')
    pics = "".join(f'<a data-pop="{esc(p.stem)}" href="{esc(url(p))}"><img src="{esc(url(p))}" alt="{esc(p.stem)}" '
                   f'style="width:200px;margin:4px;border:1px solid var(--line)"></a>' for p in f["pages"])
    sends = "".join(f'<div class=fd-row><span class=n>{esc(a)}</span><span class=d>{esc(b)}</span><span class=w>{esc(c)}</span></div>'
                    for a, b, c in f["rows"])
    return (CSS + _section("Built files", "".join(rows) or '<p class=mut>Nothing built yet.</p>')
            + _section("The pages, as Word lays them out", pics) + _section("Sends", sends)
            + _runs(folder, root, "Delivery") + JS)


def section_delivery_views(folder: Path, root: Path) -> dict:
    """A Section's Delivery view-button-list: PDF · Word · Web · Files, each lane previewed in the page."""
    name = face(folder).stem if face(folder) else folder.name
    lane = lambda key: ds.delivery_read_lane_dir(folder, key)
    return {"pdf": ("PDF", lambda: preview(lane("latex") / f"{name}.pdf", root)),
            "word": ("Word", lambda: preview(lane("word") / f"{name}.pdf", root, lane("word") / f"{name}.docx")),
            "web": ("Web", lambda: preview(lane("web") / "index.html", root)),
            "files": ("Built files", lambda: delivery_html(folder, root))}


def aim(folder: Path) -> str:
    """The Task's Aim: a Section's `reader-question:` (its face has no goal)."""
    md = face(folder)
    m = re.search(r"(?m)^reader-question:\s*(.+)$", md.read_text(encoding="utf-8", errors="ignore")) if md else None
    return m.group(1).strip() if m else ""


SENT = re.compile(r"^- B\d+ · (S\d+[a-z]*) · (?:\[[^\]]+\]\s*)?(.*\S)")


def branches(folder: Path, root: Path) -> list:
    """A draft Task's MindMap is its paper content (JL 261031: "I think the mindmap here should be the paper content"):
    each paragraph of §1 Structure, under it each point (its Bullet's head), and the point's sentence from §3 Draft
    unfolded beneath it. Steps, files and Runs are not on it: they are Report › Status, Delivery and Work › Runs."""
    import mmbuild
    d = ds.read_draft(folder)
    if not d:
        return []
    said, order = {}, []                                 # §3: S<n> -> its sentence, paragraph by paragraph
    for _, body in d["text"]:
        para = None
        for line in body.splitlines():
            h = re.match(r"^###\s+(.*\S)", line)
            if h:
                para = h.group(1)
                order.append((para, []))
                continue
            m = SENT.match(line)
            if m and para:
                said[m.group(1)] = m.group(2)
                order[-1][1].append(m.group(1))
    plan = ds._paragraphs(d["structure"][1]) if d.get("structure") else []
    points = {head: bullets for head, bullets in plan}
    out = []
    for k, (head, ids) in enumerate(order or [(h, [b[0] for b in bs]) for h, bs in plan]):
        pid, _, rest = head.partition(" · ")
        name = rest.split(" · ")[0].strip() or pid
        planned = {sid: words for sid, _, words in points.get(head, [])}
        sids = ids or list(planned)
        kids = [mmbuild.built(f"{folder}/c/{k}/{sid}", f"[{sid}] {planned.get(sid) or ' '.join(said.get(sid, '').split()[:8])}",
                              [], [said[sid]] if sid in said else [])
                for sid in sids]
        out.append(mmbuild.built(f"{folder}/c/{k}", f"[{pid}] {name}", kids))
    return out


def parts(folder: Path, root: Path, url) -> dict:
    """What the base focus page asks of a draft Task (its one hook): Work's views, their words and the open one,
    Report's views, Studio's topics, Delivery, the Aim and the captions."""
    work, words, waiting = work_views(folder, root)
    work["runs"] = ("Runs", None)                       # the base fills it with the Task's Runs
    return {"work": work, "words": words, "open": waiting, "report": report_views(folder, root, url),
            "delivery_views": section_delivery_views(folder, root),
            "studio": studio_inventory(folder, root), "studio_top": lambda: studio_top(folder, root), "delivery": lambda: delivery_html(folder, root),
            "aim": aim(folder), "captions": CAPTIONS, "verbs": SECTION_VERBS, "css": WIDE + borrowed_css() + JS}
