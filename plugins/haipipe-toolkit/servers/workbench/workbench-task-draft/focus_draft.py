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
from live.ui_parts import GROUP_CSS, PROCESS, RESULTS, WORD_CSS, _band, _numbered, _file_link, _section, _when


WORK = (("plan", "1 · Plan"), ("write", "2 · Write"), ("evidence", "3 · Evidence"), ("display", "4 · Display"),
        ("revise", "5 · Revise"))


STATE_WORD = {"done": "done", "next": "next", "sign": "sign", "asked": "asked", "send": "send", "optional": "optional",
              "pass": "pass {k}", "todo": "later"}


WAITS = ("sign", "asked", "send", "pass")              # a word the person acts on, shown in the warn colour


# what a step waits for, as the Interactions rows read (JL 261102: "make it the same style as the interactions"):
# its name, then what it waits for, then the button
# what the person does is the row's button (Sign the plan); how, its hover (r02: "✅ on approved: in the draft" read as an
# instruction line)
ASKS = {"1 · Plan": {"sign": ("Plan", "waits for your sign")},
        "3 · Evidence": {"asked": ("Evidence asks", "waits for you: tick each ask, and settle each open point")},
        "4 · Display": {"sign": ("Displays", "waits for you: write <code>accepted:</code> in each display's README")},
        "5 · Revise": {"pass": ("Revise cards", "waits for you: accept or reject each card")},
        "Delivery": {"send": ("Built files", "waits for you: check them, then mark the send in <code>delivery.md</code>")}}


# the verb on a step's waiting row, and how it is done (its hover)
SIGN = {"1 · Plan": ("Sign the plan", "Read the plan, then type ✅ on approved: in the draft; no skill signs."),
        "5 · Revise": ("Open the cards", "Accept or reject each card."), "3 · Evidence": ("Open the draft", "Tick each ask.")}


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
            "status": "Where each step stands, and what waits for you.",
            # the Interactions views say what they hold, no instruction (r03: "…; each opens the same form its Work row opens")
            "all": "Everything asked at this page or below.", "waiting": "What waits for your answer.",
            "answered": "What you have answered."}


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
.fd-sec iframe.fd-draw{display:block;width:100%;height:760px;border:1px solid var(--line,#e5e7eb);border-radius:8px}
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
 border-radius:6px;margin:0 0 12px;font-size:14px}.fd-ask .n{min-width:170px;font-weight:500;overflow-wrap:anywhere}
.fd-ask .d{flex:1;color:var(--muted);font-size:13px}
/* a phone: each evidence card's rows stack under their sentence, the card's words on a line of their own (r02: the
   cards ran 35 px past the screen, "no ev") */
@media(max-width:600px){.rv-card .rv-rows,.rv-card .rv-rows tbody{display:block;width:100%}
 .rv-card .rv-rows tr{display:flex;flex-wrap:wrap;gap:0 6px;padding:4px 0}
 .rv-card .rv-rows td{display:block;width:auto!important;padding:0!important}.rv-card .rv-rows td:last-child{flex:1 1 100%}}
/* a phone: a bar keeps its arrow, title and word on one row, the title wrapping in place (r02: the arrow sat alone on
   the first line and the word fell to a third) */
@media(max-width:600px){.fd-h{flex-wrap:nowrap!important}.fd-h>.word{white-space:normal!important;text-align:right;max-width:42%}}
@media(max-width:600px){.fd-ask{flex-wrap:wrap;gap:4px 10px}.fd-ask .n{min-width:0;flex:1 1 100%}.fd-ask .d{flex:1 1 100%}
 .fd-row{flex-wrap:wrap;gap:2px 10px}.fd-row .n{min-width:0;flex:1 1 100%}}
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
</style>""" + WORD_CSS                    # each bar's state word and the waiting line under a closed bar (261106)


JS = """<script>(function(){
 if(window.fdCopy)return;window.fdCopy=1;
 function get(k){try{return localStorage.getItem(k)||'';}catch(e){return '';}}   /* the old page's key: the same notes */
 function put(k,v){try{localStorage.setItem(k,v);}catch(e){}}
 function ready(fn){if(document.readyState!=='loading')fn();else document.addEventListener('DOMContentLoaded',fn);}
 ready(function(){
  document.querySelectorAll('.fd-run textarea[data-key]').forEach(function(t){
   if(!t.value)t.value=get(t.dataset.key);t.addEventListener('input',function(){put(t.dataset.key,t.value);});});
  /* each section folds by its heading (JL 261031: "for the view page's subsection, could they be like collapse as well")
     and starts closed on every page (JL 261104: "默认的话，大家都是合着的"); what you open stays open in this browser */
  var page=new URLSearchParams(location.search),at='fd-fold:'+(page.get('path')||'')+':'+(page.get('section')||'')+':'+(page.get('group')||'');
  var shut={};try{shut=JSON.parse(localStorage.getItem(at)||'{}');}catch(e){}
  document.querySelectorAll('section.fd-sec').forEach(function(sec){
   var h=sec.querySelector(':scope>h3.fd-h');if(!h||h.dataset.fold)return;
   var body=document.createElement('div');body.className='fd-body';
   /* the waiting line stays under the bar, outside the fold, so it shows while the section is closed (261106) */
   for(var n=h.nextSibling,x;n;n=x){x=n.nextSibling;if(!(n.classList&&n.classList.contains('fd-wait')))body.appendChild(n);}
   sec.appendChild(body);
   /* the remembered state keys on the title alone: the state word on the right changes with the work (261106) */
   var c=h.cloneNode(true);c.querySelectorAll('.word').forEach(function(w){w.remove();});
   var key=c.textContent.trim().slice(0,80);h.dataset.fold='1';h.tabIndex=0;h.setAttribute('role','button');
   function set(open){body.hidden=!open;h.setAttribute('aria-expanded',String(open));}
   set(key in shut?!shut[key]:sec.hasAttribute('data-open'));   /* a Section's Text starts open (261106) */
   function flip(){var open=body.hidden;set(open);shut[key]=open?0:1;
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
  cp(text,done);
 });
 /* http has no navigator.clipboard: copy through a hidden textarea then (b16 review 261101: "Copied" copied nothing) */
 function cp(text,done){if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(text).then(done,function(){old(text);done();});}else{old(text);done();}}function old(text){var t=document.createElement('textarea');t.value=text;t.setAttribute('readonly','');t.style.position='fixed';t.style.top='-1000px';document.body.appendChild(t);t.select();try{document.execCommand('copy');}catch(e){}document.body.removeChild(t);}
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
    # text adopted into the face (## Content) is written, though no draft holds it (r03: Status said "not started" and
    # Write "later" over "2 paragraphs, adopted"); the steps after it come next
    if st.get("2 · Write") in ("todo", "next") and any(t for _, _, t in paragraphs(folder)):
        st["2 · Write"] = "done"
        st.update({s_: "next" for s_ in ("3 · Evidence", "5 · Revise", "Delivery") if st.get(s_) == "todo"})
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
    ask = ASKS.get(step, {}).get(state)
    if not ask:
        return ""
    name, what = ask
    from live.frame import reader
    verb, how = SIGN.get(step, ("Open the draft", ""))
    open_ = (f'<a class=fd-btn data-pop="{esc(draft.name)}" title="{esc(how)}" href="{esc(reader(draft, root))}">{esc(verb)}</a>'
             if draft and root and draft.is_file() else "")
    return f'<div class=fd-ask role=status><span class=n>{name}</span><span class=d>{what}</span>{open_}</div>'


def _runs(folder: Path, root: Path, step: str) -> str:
    """The Task's own Runs this step makes, one row each: name, type, status."""
    rows = [r for r in runs_of(folder) if r["run"].startswith(RUN_PREFIX.get(step, ("\0",)))]
    if not rows:
        return ""
    states = [str(r["status"] or "").lower() for r in rows]
    done = sum(x in ("done", "complete", "completed", "ok", "succeeded") for x in states)
    word = "running" if any(x in ("running", "queued") for x in states) else f"{done} of {len(rows)} done"
    return _section("🏃 Runs of this step", "".join(
        f'<div class=fd-row><span class=n><code>{esc(r["run"])}</code></span><span class=d>{esc(r["type"])}</span>'
        f'<span class=w>{esc(r["status"])}</span></div>' for r in rows), word)


def flatten(html: str) -> str:
    """Every fold left in a step's HTML becomes a section, its summary the heading (haipipe-ui rule 4: no fold arrows);
    a drawing that loaded only when its fold opened is embedded where it stands, its heading's Open still pops it out
    (JL 261104: "why the draw is not emebeded"). `loading=lazy`, so a page of them stays quick."""
    html = LAZY.sub(lambda m: f'<iframe class="st-frame fd-draw" title="{m.group(1)}" src="{m.group(2)}" loading=lazy '
                              'referrerpolicy=no-referrer></iframe>', html)
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
        scratch = (ds._editor(folder, root, "📝 Scratch · your notes, a paragraph each", view="scratch", open_=True)
                   if step == "1 · Plan" and f["draft"] and f["draft"]["structure"] else "")
        running = ds._running(f, step)
    finally:
        ds.FLAT.reset(token)
    table = INPUT.search(op)
    report = responds_to(folder) if step == "1 · Plan" else None
    if table and report is not None:             # a response letter's plan reads the comments it answers (r02)
        from live.frame import reader
        row = ds._kv([("Comments it answers", f'<a data-pop="{esc(report.parent.name)}" href="{esc(reader(report, root))}">'
                       f'{esc(report.parent.name)}</a>')])
        row = re.search(r"<tr>.*</tr>", row, re.S).group(0)
        table = re.search(r"(?s)(.*)", table.group(1).replace("</tbody></table>", row + "</tbody></table>", 1))
    sign = re.search(r"<p class=sign-row>(.*?)</p>|<p><span class=\"st st-ok\">✓ signed</span>(.*?)</p>", op, re.S)
    signed = (f'<p class=mut>✓ signed {sign.group(2)}</p>' if sign and sign.group(2) else "")
    # The same sections as before, in the two parts every view has (JL 261101: "keep the previous draft workbench,
    # keep the content as much as possible but use the new subsections layout"): ⚙️ Process, the step's input, prompt
    # and sign (b15 s58), then 📊 Results, the step's own cards; each part numbered from 1.
    # the open forms are the view's last section, 🙋 Interaction, so this step no longer repeats them (JL 261105: "keep
    # only the bottom"); what is left is the step's own state: a Run running, its ask, its sign
    waits = running + _ask(step, st[step], (f["draft"] or {}).get("file"), root) + signed
    # each bar's state word is the step's own (JL 261106: "every closed bar shows a state word on its right"); what the
    # step waits for shows under its closed bar
    said = "running" if running else STATUS_WHAT[st[step]].format(k=k)
    ask = ASKS.get(step, {}).get(st[step])
    line = f"🙋 {ask[0]} {re.sub(r'<[^>]+>', '', ask[1])}" if ask and not running else ""
    process = _section("📌 Where this step stands", waits, said, line) if waits else ""
    boxes = quiet(boxes_of(op))                  # the shared Prompt boxes, whole; the session line rides the copy only
    n_boxes = boxes.count("<!--pb-prompt-->")      # its own word: the wait is said once, on Where this step stands (r01)
    process += _section("🤖 Ask the agent", boxes, f"{n_boxes} prompt{'s' * (n_boxes != 1)}") if step in ASK_STEPS and boxes else ""
    process += _section("📥 Input", table.group(1) if table else "", input_word(table.group(1) if table else "")) + _runs(folder, root, step)
    results = _drop_repeats(step, _after_first_section(flatten(result), flatten(scratch)))
    if NO_TEXT in results and paragraphs(folder):   # no draft yet, but adopted Content: Write and Revise read the text
        results = results.replace(NO_TEXT, _section("📝 The adopted text", content_read(folder, root), text_count(folder)), 1)
    if step == "3 · Evidence":                  # the Section's own bib, one row per key, where a [key] in the text opens
        results += bib_section(folder, root)    # (r03: no .bib on Evidence or Files)
    return CSS + GROUP_CSS + _band(PROCESS, _numbered(process)) + _band(RESULTS, _numbered(results)) + JS


def bib_section(folder: Path, root: Path) -> str:
    """📚 Its bib: each entry of the Section's bib (its key, paper, year, DOI), where its text cites it, and each key the
    text cites that the bib lacks; the file one Pop out away."""
    bib = bib_entries(folder)
    text = " ".join(t for _, _, t in paragraphs(folder))
    for d in sorted((folder / "draft").glob("*-draft-v*.md")) if (folder / "draft").is_dir() else []:
        text += " " + d.read_text(encoding="utf-8", errors="ignore")
    cited = list(dict.fromkeys(k.strip() for m in re.finditer(r"\\cite[pt]?\{([^}]*)\}", text) for k in m.group(1).split(",")))
    if not bib and not cited:
        return ""
    from live.frame import reader
    rows = "".join(
        f'<div class=fd-row id="bib-{esc(k)}"><span class=n><code>{esc(k)}</code></span><span class=d>'
        f'{esc(" · ".join(x for x in (e["title"], e["year"], ("DOI " + e["doi"]) if e["doi"] else "no DOI") if x))}</span>'
        f'<span class="w {"fd-ok" if k in cited else ""}">{"cited" if k in cited else "not cited"}</span></div>'
        for k, e in bib.items())
    rows += "".join(f'<div class=fd-row id="bib-{esc(k)}"><span class=n><code>{esc(k)}</code></span><span class=d>no entry in '
                    f'this Section\'s bib</span><span class="w fd-you">not in the bib</span></div>' for k in cited if k not in bib)
    files = sorted({e["file"] for e in bib.values()})
    pop = "".join(f'<p style="margin-top:8px"><a class=fd-btn data-pop="{esc(f.name)}" href="{esc(reader(f, root))}">'
                  f'Open {esc(f.name)}</a></p>' for f in files)
    missing = [k for k in cited if k not in bib]
    return _section("📚 Its bib", rows + pop, f"{len(missing)} not in the bib" if missing else f"{len(bib)} entries",
                    f"🙋 cited, not in the bib: {', '.join(missing)}" if missing else "")


NO_TEXT = "<p class=space-empty>No text yet.</p>"


def _top_sections(html: str) -> list:
    """[(start, end, title)] of the top-level `fd-sec` sections of a step's HTML."""
    out, depth, start = [], 0, 0
    for m in re.finditer(r"<section\b[^>]*>|</section>", html):
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                title = re.sub(r"<[^>]+>", "", (re.search(r"<h3 class=fd-h>(.*?)</h3>", html[start:m.end()], re.S) or [None, ""])[1])
                out.append((start, m.end(), title.strip()))
        else:
            if depth == 0:
                start = m.start()
            depth += 1
    return out


def _drop_repeats(step: str, html: str) -> str:
    """A section that repeats the text-and-cards section above it goes (r01): Evidence's Open points (each is already a
    row beside its sentence), Display's one card per display (each is already beside the sentence that calls it)."""
    secs = _top_sections(html)
    if not secs or "The text and its" not in secs[0][2]:
        return html
    if step == "3 · Evidence":
        drop = [x for x in secs[1:] if x[2].startswith("❓ Open points")]
    elif step == "4 · Display":
        drop = [x for x in secs[1:] if re.match(r"(?:e?Figure|e?Table|Display)\b", x[2])]
    else:
        return html
    for start, end, _ in reversed(drop):
        html = html[:start] + html[end:]
    return html


def boxes_of(html: str) -> str:
    return "".join(re.findall(r"<!--pb-prompt-->.*?<!--/pb-prompt-->", html, re.S))


def quiet(boxes: str) -> str:
    """A Prompt box without its session line on the page (r02: "Run this in the Claude session …" in every box); the
    Copy prompt button still copies it (its data-tail)."""
    return re.sub(r"<p class=pb-sess>.*?</p>", "", boxes, flags=re.S)


def input_word(table: str) -> str:
    """The Input table's word: how many of its rows have nothing yet (a muted or warned value), else all in place."""
    rows = re.findall(r"<tr>(.*?)</tr>", table, re.S)
    missing = sum(bool(re.search(r'class=(?:mut|"st st-warn")', r)) for r in rows)
    return f"{missing} of {len(rows)} missing" if missing else "all in place"


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


CONTENT_CSS = ("<style>.fd-sents{margin:2px 0 12px;padding-left:2.1em;line-height:1.55;font-size:15px}"
               ".fd-sents li{margin:0 0 4px;padding-left:2px}.fd-sents li::marker{color:var(--muted);font-size:11.5px}"
               ".fd-cite{color:var(--muted);font-size:.88em}.fd-content h4{margin:12px 0 4px;font-size:14px}</style>")


def bib_entries(folder: Path) -> dict:
    """{key: {title, year, doi, author, file}} of a Section's own bib (draft/evidence/bibex/*.bib, the one its build
    prints from), in file order."""
    out = {}
    for f in sorted((folder / "draft" / "evidence").glob("**/*.bib")) if (folder / "draft" / "evidence").is_dir() else []:
        text = f.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)(?=^@|\Z)", text, re.S | re.M):
            field = lambda k: re.sub(r"[{}]", "", (re.search(rf"(?im)^\s*{k}\s*=\s*[{{\"](.*?)[}}\"]\s*,?\s*$", m.group(2)) or [None, ""])[1])
            out.setdefault(m.group(1), {"title": field("title"), "year": field("year"), "doi": field("doi"),
                                        "author": field("author"), "file": f})
    return out


def bib_href(folder: Path, root: Path | None, key: str) -> str:
    """Where a [key] in the text opens: its row under Work › 3 · Evidence (r03: the keys linked nowhere)."""
    if root is None:
        return ""
    from live.board_read import _task_url
    return _task_url(folder, root, "evidence") + f"#bib-{quote(key)}"


def content_read(folder: Path, root: Path | None = None) -> str:
    """A Section's adopted Content to read (its `## Content` paragraphs), each under its name, a sentence a numbered
    line, a citation command as its keys: the one way a Section's text is drawn on its own page and on its version's
    Draft views (r02: Text showed raw \\citep keys while Draft-Main showed [keys]). With `root`, each key links to its
    bib entry under Work › Evidence; a key not in the Section's bib says so on hover."""
    paras = [(name or pid, t) for pid, name, t in paragraphs(folder) if t]
    if not paras:
        return ""
    try:
        from live.outline_revise import split_sentences
    except ImportError:
        split_sentences = lambda t: [t]
    bib = bib_entries(folder) if root is not None else {}

    def key(k: str) -> str:
        k = k.strip()
        if root is None:
            return esc(k)
        if k in bib:
            return f'<a href="{esc(bib_href(folder, root, k))}" title="{esc(bib[k]["title"])}">{esc(k)}</a>'
        return f'<span title="not in this Section\'s bib">{esc(k)} ⚠</span>'
    cite = lambda h: re.sub(r"\\cite[pt]?\{([^}]*)\}", lambda m: '<span class=fd-cite>[' + ", ".join(key(k) for k in m.group(1).split(",")) + ']</span>', h)
    return CONTENT_CSS + '<div class=fd-content>' + "".join(
        f'<h4>{esc(h)}</h4><ol class=fd-sents>' + "".join(f'<li>{cite(esc(x))}</li>' for x in split_sentences(t)) + '</ol>'
        for h, t in paras) + '</div>'


def text_count(folder: Path) -> str:
    n = sum(1 for _, _, t in paragraphs(folder) if t)
    return f"{n} paragraph{'s' * (n != 1)}, adopted" if n else "nothing yet"


READ_ONLY = ("<style>.fd-read .rv-acts,.fd-read .nt-acts,.fd-read .nt-box,.fd-read .nt-plus,.fd-read .nt-gut,"
             ".fd-read .rv-accept-all{display:none!important}</style>")


def text_html(folder: Path, root: Path) -> str:
    """The Section at sentence level (JL 261031: "why there are no things like sentence level, and the tracking, and
    the evidence etc. left and right panel"): the newest draft, one sentence a row with its S number, and on the right
    each sentence's cards, in reading order: its evidence, its changes (old to new, the tracking), the review's logic
    and the comments, each kind switched on or off above. Report checks, so the cards are read here, never decided:
    Accept, Reject and comments are Work › 5 · Revise's. A draft not yet written shows the adopted Content."""
    board = reply_board(folder, root)            # a response letter: each reply beside its point (r02: six identical
    if board:                                    # "no evidence" cards beside the replies)
        return answers_line(folder, root) + CSS + board
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
        if board:                                # the text is what the view is for: it starts open (261106)
            return (answers_line(folder, root) + CSS + READ_ONLY
                    + f'<div class=fd-read>{flatten(board).replace("<section class=fd-sec>", "<section class=fd-sec data-open>", 1)}</div>')
    if paragraphs(folder):
        return answers_line(folder, root) + CSS + _section_open("📝 The text", content_read(folder, root), text_count(folder))
    return '<p class=mut>No text yet: 2 · Write writes it.</p>'


def _section_open(title: str, body: str, word: str = "") -> str:
    return _section(title, body, word).replace("<section class=fd-sec>", "<section class=fd-sec data-open>", 1)


# ── a letter that answers comments (a response letter's `responds-to:`): the comments report linked, and each of its
# Review Items beside the reply that answers it (r01: "open the reviewers' comments it answers: could not") ─────────
def md_tables(text: str) -> list:
    """Every Markdown table of a text, each a list of dicts by its header."""
    out, rows, head = [], None, None
    for line in text.splitlines() + [""]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not line.lstrip().startswith("|"):
            if rows is not None:
                out.append(rows)
            rows, head = None, None
        elif head is None:
            head, rows = cells, []
        elif not set("".join(cells)) <= set("-: "):
            rows.append(dict(zip(head, cells + [""] * (len(head) - len(cells)))))
    return out


def responds_to(folder: Path) -> Path | None:
    """The comments report a page answers (its face's `responds-to:`), else None."""
    md = face(folder)
    m = re.search(r"(?m)^responds-to:\s*(\S+)", md.read_text(encoding="utf-8", errors="ignore")) if md else None
    hit = (folder / m.group(1)).resolve() if m else None
    return hit if hit is not None and hit.is_file() else None


def review_items(report: Path) -> list:
    """[(the point, who raised it, the Section it lands on, its reply paragraph, its state)] from a comments report's
    Feedback Concern Table and Review Items."""
    tables = md_tables(report.read_text(encoding="utf-8", errors="ignore"))
    concerns = {r.get("item", ""): r for t in tables for r in t if r.get("concern")}
    items = next((t for t in tables if t and "lands on" in t[0]), [])
    out = []
    for r in items:
        c = concerns.get(r.get("cites", ""), {})
        out.append((c.get("concern") or r.get("item", ""), c.get("source", ""), r.get("lands on", ""), r.get("reply", ""),
                    r.get("state", "") or c.get("state", "")))
    return out


def review_points(report: Path, letter: Path | None) -> list:
    """review_items, each reply read from the letter when the report names none: the one paragraph whose name names who
    raised the point ("Reply to Reviewer 1 on …"), its state answered (r02: the report said "routed" for two points
    while the letter held a reply to each, so the Answers line said "1 of 3" beside three replies)."""
    items = review_items(report)
    if letter is None:
        return items
    paras = [(pid.split(".")[-1], name) for pid, name, t in paragraphs(letter) if t]
    taken = {reply for _, _, _, reply, _ in items if reply}
    out = []
    for point, who, lands, reply, state in items:
        if not reply and who:
            hits = [p for p, name in paras if p not in taken and re.search(rf"\b{re.escape(who)}\b", name, re.I)]
            if len(hits) == 1:
                reply, state = hits[0], "answered"
                taken.add(reply)
        out.append((point, who, lands, reply, state))
    return out


REPLY_CSS = ("<style>.fd-reply{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:8px 18px;padding:10px 0;"
             "border-bottom:1px solid var(--line)}.fd-reply h4{margin:0 0 4px;font-size:14px}"
             ".fd-point{border:1px solid var(--line);border-left:3px solid light-dark(#2b8a3e,#8bd49a);border-radius:8px;"
             "padding:7px 11px;font-size:13.5px}.fd-point.open{border-left-color:light-dark(#b35c00,#ffc078)}"
             ".fd-point b{display:block;margin:0 0 4px}.fd-point small{display:block;color:var(--muted)}"
             "@media(max-width:700px){.fd-reply{grid-template-columns:minmax(0,1fr)}}</style>")


def reply_board(folder: Path, root: Path) -> str:
    """A response letter's text, each reply paragraph beside the reviewer's point it answers (who raised it, where it
    lands, its state); a point with no reply yet listed after them. "" for any other Section."""
    report = responds_to(folder)
    paras = [p for p in paragraphs(folder) if p[2]]
    if report is None or not paras:
        return ""
    try:
        from live.outline_revise import split_sentences
    except ImportError:
        split_sentences = lambda t: [t]
    points = review_points(report, folder)
    by_reply = {reply: (point, who, lands, state) for point, who, lands, reply, state in points if reply}

    def card(point, who, lands, state):
        done = state in ("answered", "applied")
        return (f'<div class="fd-point{"" if done else " open"}"><b>{esc(point)}</b>'
                + "".join(f'<small>{esc(k)}: {esc(v)}</small>' for k, v in (("raised by", who), ("lands on", lands),
                                                                           ("state", state or "open")) if v) + '</div>')
    rows = ""
    for pid, name, text in paras:
        hit = by_reply.get(pid.split(".")[-1])
        rows += (f'<div class=fd-reply><div><h4>{esc(pid)} · {esc(name)}</h4><ol class=fd-sents>'
                 + "".join(f"<li>{esc(x)}</li>" for x in split_sentences(text)) + '</ol></div><div>'
                 + (card(*hit) if hit else '<p class=mut>No Review Item names this reply.</p>') + '</div></div>')
    left = [(point, who, lands, state) for point, who, lands, reply, state in points if not reply]
    rows += "".join(f'<div class=fd-reply><div><p class=mut>No reply yet.</p></div><div>{card(*x)}</div></div>' for x in left)
    done = sum(st in ("answered", "applied") for *_, st in points)
    return CONTENT_CSS + REPLY_CSS + _section_open("✉️ Each reply beside the point it answers", rows,
                                                   f"{done} of {len(points)} points answered")


def answers_line(folder: Path, root: Path) -> str:
    """One line above a response letter's text: the comments it answers, opening the report, and how many are answered."""
    report = responds_to(folder)
    if report is None:
        return ""
    from live.frame import reader
    items = review_points(report, folder)
    done = sum(st in ("answered", "applied") for *_, st in items)
    said = f" · {done} of {len(items)} points answered" if items else ""
    return (CSS + f'<div class=fd-ask role=status><span class=n>Answers</span><span class=d>{esc(report.parent.name)}{esc(said)}'
            f'</span><a class=fd-btn data-pop="{esc(report.parent.name)}" href="{esc(reader(report, root))}">Open the comments</a></div>')


STATUS_WHAT = {"done": "done", "next": "comes next", "sign": "waits for your sign", "asked": "waits for your ticks",
               "send": "built, waits for your send", "optional": "optional", "pass": "pass {k}: cards wait for you",
               "todo": "later"}


def status_html(folder: Path, root: Path, url) -> str:
    """The Section's aims and opening (what it must do, when it is done, where it is now), then each step, one row: its
    name, what it waits for in its state's colour, Go (into Work, or the rail's section)."""
    f, st, k = _facts(folder, root)
    now = now_line(st, k)                        # "Now" from the steps, never the face's typed word (r03: "not started"
    rows = [f'<div class=fd-row><span class=n>{esc(n)}</span><span class=d>{esc(now if n == "Now" else v)}</span></div>'
            for n, v in aims(folder)]            # stood over "2 paragraphs, adopted")
    if not any(n == "Now" for n, _ in aims(folder)):
        rows.insert(0, f'<div class=fd-row><span class=n>Now</span><span class=d>{esc(now)}</span></div>')
    for step in ds.STEPS:
        key = dict((s, kk) for kk, s in WORK).get(step)
        if key == "display" and not f["displays"]:   # Work shows no Display then, so its row would open Plan (261105)
            continue
        href = url("work", key) if key else url(step.lower(), "")
        w, cls = word(st[step], k)
        rows.append(f'<div class=fd-row><span class=n>{esc(step)}</span><span class="d {cls}">{esc(STATUS_WHAT[st[step]].format(k=k))}'
                    f'</span><a class=fd-btn href="{esc(href)}">Go</a></div>')
    return CSS + "".join(rows)


def now_line(st: dict, k: int = 1) -> str:
    """Where the Section stands, from its steps: the steps done, then the one that waits for the person or comes next."""
    steps = [step for _, step in WORK if step in st]
    done = [step.split(" · ")[1] for step in steps if st[step] == "done"]
    wait = next((step for step in steps if st[step] in WAITS), None)
    nxt = next((step for step in steps if st[step] == "next"), None)
    bits = ([f"{', '.join(done)} done"] if done else []) + \
           ([f"{wait.split(' · ')[1]} {STATUS_WHAT[st[wait]].format(k=k)}"] if wait else
            [f"{nxt.split(' · ')[1]} comes next"] if nxt else [])
    return "; ".join(bits) or "not started"


def aims(folder: Path) -> list:
    """[(name, words)] of the face's `## Aims` (Target · Done when · Now) and the first line of its `## Opening`
    (r02: they showed nowhere on the Section's page)."""
    md = face(folder)
    text = md.read_text(encoding="utf-8", errors="ignore") if md else ""
    sec = lambda name: (re.search(rf"(?ms)^## {name}\s*\n(.*?)(?=^## |\Z)", text) or [None, ""])[1].strip()
    out = []
    for line in sec("Aims").splitlines():
        for part in line.lstrip("- ").split(" · "):
            k, _, v = part.partition(":")
            if v.strip() and k.strip() in ("Target", "Done when", "Now"):
                out.append((k.strip(), v.strip()))   # "Target", as the face says (r03: two "Aim"s on one page)
    opening = " ".join(sec("Opening").split())
    if opening:
        out.append(("Opening", opening[:280] + ("…" if len(opening) > 280 else "")))
    return out


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
    # only the step's Copy prompt box, as the Section Studio drawing settled (s40 r03, pick B: "Copy prompt only, no
    # new-topic button"); it was worked out and then dropped, so the Studio showed no prompt (found 261105)
    prompt = quiet(boxes_of(op))                 # r02: Studio said it was empty twice; the base Studio says it once
    return CSS + prompt + JS


READER = (".pdf", ".docx", ".html")             # what a reader opens; .tex, .json and -view.html stay in Files only


PREVIEW_CSS = ("<style>.fd-prev{display:block;width:100%;height:calc(100vh - 300px);min-height:620px;border:1px solid "
               "var(--line);border-radius:6px;background:#fff}.fd-prev-h{font-size:13px;color:var(--muted);margin:0 0 8px}"
               "</style>")


def build_prompts(folder: Path, root: Path) -> list:
    """The Section's Delivery prompts (build, render the pages, check, read back), each a Prompt box with Copy prompt,
    the session line copied but not shown."""
    f, st, k = _facts(folder, root)
    token = ds.FLAT.set(True)
    try:
        op, _, _ = ds._delivery_step(f, folder, root, st["Delivery"])
    finally:
        ds.FLAT.reset(token)
    return [quiet(b) for b in re.findall(r"<!--pb-prompt-->.*?<!--/pb-prompt-->", op, re.S)]


def preview(f: Path | None, root: Path, also: Path | None = None, ask: str = "") -> str:
    """One built file, previewed in the page (JL 261007: "the card and the preview of the results, the embedded
    content"; JL 261031: "I thnk we want to make it to be previewed here"): its name, state and built time, Open ↗ to a
    new tab, then the file itself; Word through the PDF twin the build writes beside the .docx (`also`)."""
    if not f or not f.is_file():                 # r01: "Ask the agent builds it" named no control; its Copy prompt is here
        return ('<p class=mut>Not built yet.</p>' + ask
                if ask else '<p class=mut>Not built yet.</p>')
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
    states = [lane.get("state", "") for lane in lanes]
    built = ("nothing built yet" if not states or all(x == "not-built" for x in states) else
             "current" if all(x == "pass" for x in states) else f'{sum(x == "stale" for x in states)} stale' if "stale" in states
             else f'{sum(x == "pass" for x in states)} of {len(states)} current')
    try:
        asks = "".join(build_prompts(folder, root))
    except Exception:
        asks = ""
    return (CSS + _section("Built files", "".join(rows) or '<p class=mut>Nothing built yet.</p>', built)
            + _section("The pages, as Word lays them out", pics, f'{len(f["pages"])} pages' if f["pages"] else "")
            + _section("Sends", sends, "sent" if any("sent" in str(c).lower() for _, _, c in f["rows"]) else "not sent yet")
            + _runs(folder, root, "Delivery")
            + _section("🤖 Ask the agent", asks, "nothing built yet" if built == "nothing built yet" else built) + JS)


def section_delivery_views(folder: Path, root: Path) -> dict:
    """A Section's Delivery view-button-list: PDF · Word · Web · Files, each lane previewed in the page."""
    name = face(folder).stem if face(folder) else folder.name
    lane = lambda key: ds.delivery_read_lane_dir(folder, key)

    def gap() -> str:
        """JL 261102: the PDF printed draft v0.1 while the plan beside it was v0.3, and the page did not say so."""
        try:
            from src.page_adopt import content_gap
            g = content_gap(folder)
        except Exception:
            return ""
        return (f'<div class=fd-ask role=status><span>⚠️ This prints {esc(g["printed"])}; the current draft is '
                f'{esc(g["current"])}. It is behind: {esc(g["why"])}, then export, before reading it as final.'
                '</span></div>') if g else ""
    def ask() -> str:                            # the build's own Copy prompt, where a lane is not built yet
        try:
            return build_prompts(folder, root)[0]
        except Exception:
            return ""
    return {"pdf": ("PDF", lambda: CSS + gap() + preview(lane("latex") / f"{name}.pdf", root, ask=ask()) + JS),
            "word": ("Word", lambda: CSS + gap() + preview(lane("word") / f"{name}.pdf", root, lane("word") / f"{name}.docx", ask()) + JS),
            "web": ("Web", lambda: CSS + gap() + preview(lane("web") / "index.html", root, ask=ask()) + JS),
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
    if not d or not (d.get("text") or d.get("structure")):
        return content_branches(folder) + answers_branch(folder, root)   # r02: Text showed the adopted Content while
    said, order = {}, []                                 # the map said "Nothing to map yet"; §3: S<n> -> its sentence
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
    return (out or content_branches(folder)) + answers_branch(folder, root)


def content_branches(folder: Path) -> list:
    """The adopted Content as the map, when no draft holds a plan or a text: each paragraph, each sentence under it, the
    same text Report › Text shows."""
    import mmbuild
    try:
        from live.outline_revise import split_sentences
    except ImportError:
        split_sentences = lambda t: [t]
    out = []
    for k, (pid, name, text) in enumerate(p for p in paragraphs(folder) if p[2]):
        sents = [re.sub(r"\\cite[pt]?\{([^}]*)\}", lambda m: "[" + m.group(1).replace(",", ", ") + "]", x)
                 for x in split_sentences(text)]               # a citation command reads as its keys, as on Text
        kids = [mmbuild.built(f"{folder}/c/{k}/S{j}", f"[S{j}] {' '.join(x.split()[:8])}", [], [x])
                for j, x in enumerate(sents, 1)]
        out.append(mmbuild.built(f"{folder}/c/{k}", f"[{pid}] {name or pid}", kids))
    return out


def answers_branch(folder: Path, root: Path) -> list:
    """A response letter's map: the comments it answers, each point with who raised it, where it lands, its reply
    paragraph and its state (r01: "put each Review Item beside its reply in MindMap")."""
    import mmbuild
    report = responds_to(folder)
    if report is None:
        return []
    from live.frame import reader
    names = {pid.split(".")[-1]: name for pid, name, _ in paragraphs(folder)}
    kids = [mmbuild.built(f"{folder}/answers/report", f"[report] [{report.parent.name}]({reader(report, root)})")]
    for i, (point, who, lands, reply, state) in enumerate(review_points(report, folder)):
        kids.append(mmbuild.built(f"{folder}/answers/{i}", f"[{state or 'open'}] {point}",
                                  [mmbuild.built(f"{folder}/answers/{i}/who", f"[raised by] {who}")] * bool(who)
                                  + [mmbuild.built(f"{folder}/answers/{i}/lands", f"[lands on] {lands}")] * bool(lands)
                                  + [mmbuild.built(f"{folder}/answers/{i}/reply",
                                                   f"[reply] {reply}: {names[reply]}" if reply in names else
                                                   f"[reply] {reply}" if reply else "[reply] not written yet")]))
    return [mmbuild.built(f"{folder}/answers", "Comments it answers", kids)]


def parts(folder: Path, root: Path, url) -> dict:
    """What the base focus page asks of a draft Task (its one hook): Work's views, their words and the open one,
    Report's views, Studio's topics, Delivery, the Aim and the captions."""
    from live.address_links import linked_views, page_linker
    link = page_linker(folder, root)                    # every bNN.jNN.tNN.rNN a link (address_links, JL 261103)
    work, words, waiting = work_views(folder, root)
    work = linked_views(work, link)
    work["runs"] = ("Runs", None)                       # the base fills it with the Task's Runs
    return {"work": work, "words": words, "open": waiting, "report": linked_views(report_views(folder, root, url), link),
            "delivery_views": section_delivery_views(folder, root),
            "studio": studio_inventory(folder, root), "studio_top": lambda: studio_top(folder, root), "delivery": lambda: delivery_html(folder, root),
            "aim": aim(folder), "captions": CAPTIONS, "verbs": SECTION_VERBS, "css": WIDE + borrowed_css() + JS}
