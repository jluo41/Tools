"""The pieces every insight focus view shares: the view names and their skills, the page's stylesheet and post
script, the small words and links (a step, a dot, a pair, written or not), the page around a view, the question
map's drawing, and a run card's prompt with its Copy button."""

from __future__ import annotations

import re
from pathlib import Path

from live import insight_plan_c as P
from live import insight_views as V
from live.frame import esc, rel
from live import focus_draft as FD
from live.ui_parts import GROUP_CSS, PB_CSS, PB_JS, PROMPT_CSS, PROMPT_JS, _numbered, prompt_box
from live.insight_view_parts import _pill, _section


VIEWS = (("overall", "Findings"), ("vs-previous", "Changes"), ("grid", "Progress"))   # plain words; keys stay for links
# the skills each view's work calls on (the rail's Skills: focus_page.page_skills reads it, 261106)
VIEW_SKILLS = {
    "answers": (("haipipe-insight", "writes the Overall Report from the answers below it"),),
    "questions": (("haipipe-insight-question", "proposes questions and segments for the next question version"),
                  ("haipipe-insight-evidence-plan", "plans each question's evidence before any Run")),
    "jobs": (("haipipe-insight", "adds a Job: a signed question version × a data version, one clock moved"),),
    "data": (("haipipe-insight-meta", "adds a data version and counts its rows per segment"),),
    "handoff": (("haipipe-insight-wisdom", "writes the advice and drafts it for your sign"),),
    "overall": (("haipipe-insight", "writes the Overall Report and closes the Job"),),
    "grid": (("haipipe-insight-data", "writes a Data page from its Runs"),
             ("haipipe-insight-information", "writes an Information page"),
             ("haipipe-insight-knowledge", "writes a Knowledge page"),
             ("haipipe-insight-check", "checks each page against its question")),
    "vs-previous": (("haipipe-insight-knowledge", "compares each answer with the Job before"),),
    "answer": (("haipipe-insight-check", "runs the alignment check"), ("haipipe-insight", "runs the question on a segment")),
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
        return "", ""
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
    """Where a plan is signed and its proposals triaged: the Question Book's (or the release's) Work · Findings, whose ⚙️
    Process carries both (round 2: "the Board's Open the proposals landed on MindMap")."""
    return _focus(Path(path), root, "work") + "&group=findings"


def _jlink(j: dict, root: Path, words: str = "") -> str:
    return f'<a href="{esc(_focus(j["path"], root))}" title="{esc(j["name"])}">{esc(words or j["name"][:3])}</a>'


def _pair(j: dict) -> str:
    """A Job in plain words: `j02 · question-v1 × data-v2` (the same id on screen and on disk)."""
    return f'{j["name"][:3]} · {P.plan_code(j["release"])} × {P.freeze_code(j["data"])}'


def _written(t: dict) -> bool:
    """A page is written: the one count every "N of M" reads (insight_views.is_written; round 1, 261106)."""
    return V.is_written(t)


def _page_word(t: dict) -> str:
    """A page's state in a word: returned (a CHECK sent it back), else its own answer-status, else to write."""
    return V.page_word(t)


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


def _page(html: str) -> str:
    """A Report view: its numbered sections, the side tabs' script and the fold script (R1: every bar starts closed on
    Report too). No caption: a line that only names the sections under it says nothing."""
    return _head() + html + PB_JS + FD.JS


def _work_page(proc: str, res: str) -> str:
    """A view's steps then its results, numbered as one list (the Report shows the Work, so the view
    carries no heading of its own): no ⚙️ Process or 📊 Results heading, no grey caption."""
    return _head() + _numbered(proc + res) + PB_JS + FD.JS + PROMPT_JS + POST_JS


def _map_view(build) -> tuple:
    """The MindMap as a Work view: its Results only, the Report's map (R6: the mind map is always shown)."""
    return ("MindMap", lambda: _head() + build())                    # no caption, no 📊 Results heading


def _parts_map(folder: Path, root: Path):
    def build():
        from live import focus_page as FP
        return FP.parts_mindmap(folder, root)
    return build


def _done(signed) -> str:
    """A done sign's state word, with its date when the face has one: `done 261101`."""
    return ("done " + str(signed or "").lstrip("✅ ").strip()).strip()


def draw_map(folder: Path, root: Path, branches: list, empty: str) -> str:
    """A map drawn by the shared mind-map module from [(label, [leaf words])]: the folder at its root, a card per
    branch, each leaf whole (a Job's DIKW levels, a Task's answer and segments, a release's questions)."""
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


MOVED = {"code": "the code", "data": "the data", "start": "the first Job"}


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
        return ("🏃" if _writing(t) else "⬜"), t
    v = (j["vs"].get("rows") or {}).get(qid) if j["vs"] else None
    if v:
        s = str(v.get("status") or "")
        return "✅ " + (f"changed: {MOVED.get(j['moved'], j['moved'])}" if s.lower() == "changed" and j["moved"] in ("code", "data") else s), t
    return "✅" + (" first" if not j["previous"] else ""), t


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


def _writing(t: dict) -> bool:
    return any(V._rtype(r) == "write" and str(r.get("status") or "").lower() in ("running", "started") for r in t["soft"])
