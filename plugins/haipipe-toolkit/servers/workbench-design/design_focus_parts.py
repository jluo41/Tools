"""The shared pieces of a design focus view: the page's script and style, a row's Copy prompt, a Process step with
its state word, the big line, side tabs, chains and tiles, links, and `_page` that draws one view as one numbered
list (split out of design_focus.py)."""
from __future__ import annotations

import re
from pathlib import Path

from live import design_views as V
from live import focus_draft as FD
from live.frame import esc, rel
from live.ui_parts import GROUP_CSS, PB_CSS, PB_JS, PROMPT_CSS, PROMPT_JS, _numbered, _pill, _side_tabs, waits_on_you
from live.ui_parts import _section as _bar_section

_TALLY = re.compile(r"^(\d+) (?:kept )?of (?:N = )?(\d+)\b")
_NOT_YET = re.compile(r"^(no|not|none|nothing)\b", re.I)
_COUNTED = re.compile(r"^\d+ [a-z]+(, \d+ [a-z]+)*$")
_DONE = {"done", "released", "closed", "signed", "answered", "kept", "passed", "frozen"}
_UNDER_WAY = {"open", "running", "started", "in review"}


def state_mark(word: str) -> str:
    """A bar's state as a mark, never a tally or a sentence about state: ✅ all there, 🏃 under way, ⬜ not yet.
    A word that asks the person to act, names a thing (a goal, a version) or gives a reason stays as it is."""
    word = (word or "").strip()
    if not word or waits_on_you(word):
        return word
    tally = _TALLY.match(word)
    if tally:
        have, want = int(tally.group(1)), int(tally.group(2))
        return "⬜" if not have else "✅" if have >= want else "🏃"
    if _NOT_YET.match(word):
        return "⬜"
    if _COUNTED.match(word) or word.startswith("all ") or word.lower() in _DONE:
        return "✅"
    if word.lower() in _UNDER_WAY or word.endswith(" at work"):
        return "🏃"
    return word


def _section(title: str, body: str, word: str = "", waits: str = "") -> str:
    """The shared section bar. A tally or state word becomes a mark first, so the bar's own rule (ui_parts.word_span)
    draws ✓ on a finished section, 🙋 with how many on one that waits, and nothing on any other."""
    return _bar_section(title, body, state_mark(word), waits)

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
CSS = """<style>.pb-prompt.in-copy{display:inline;border:0;padding:0;margin:0;background:none}
.dz-flow{display:grid;grid-template-columns:1fr auto 1fr auto 1fr;gap:8px;align-items:stretch;margin:2px 0 8px}
.dz-flow>div{border:1px solid var(--line);border-radius:8px;padding:8px 12px;background:var(--paper);font-size:13px}
.dz-flow small{display:block;color:var(--muted);font-size:11.5px}.dz-flow b{display:block}.dz-arrow{align-self:center;color:var(--muted)}
.dz-part{margin:4px 0 8px;font-size:13px;color:var(--muted)}.sign-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.work-act{font:inherit;font-size:13px;border:1px solid var(--line);border-radius:6px;padding:3px 10px;background:var(--paper);cursor:pointer}
.work-act[disabled]{opacity:.55;cursor:default}
.dz-close{font-size:13px;margin:2px 0 4px}.pb-state.you{color:light-dark(#b35c00,#ffc078)}
.pb-prompt.in-copy.dz-pick{display:inline-flex;flex-wrap:wrap;gap:6px;align-items:center}
.dz-pick select{font:inherit;font-size:13px;border:1px solid var(--line);
 border-radius:6px;padding:2px 6px;background:var(--paper);color:var(--ink)}
.dz-strip{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:0 0 14px;font-size:13px}
.dz-strip b{font-weight:600;margin-right:4px}.dz-chip{border:1px solid var(--line);border-radius:12px;padding:2px 10px;background:var(--paper)}
.dz-chip.on{border-color:var(--accent);color:var(--accent)}.dz-chip.bad{color:light-dark(#b02a37,#ff8787)}
.dz-next{margin:18px 0 6px;font-size:14px}.dz-next b{font-weight:600}
.dz-verdict{font-size:18px;margin:2px 0 8px}
.dz-pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:0 0 4px}.dz-pair small{display:block;
 color:var(--muted);font-size:12px;margin:0 0 2px}
.dz-card{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:18px;align-items:start}
.dz-text{white-space:pre-wrap;font-size:13.5px;line-height:1.5;margin:0}
@media(max-width:600px){.dz-flow{grid-template-columns:1fr}.dz-card,.dz-pair{grid-template-columns:1fr}
.dz-arrow{transform:rotate(90deg);justify-self:start}
 .pb-chain .pb-step{width:100%}.pb-chain .pb-arrow{transform:rotate(90deg);margin:0}}</style>"""


def _href(root: Path):
    """design_views' links (space, sub, path) on the focus page: a folder opens its own focus page."""
    from live import focus_page as F
    return lambda space="", sub="", path=None: F.page_url(Path(path), root) if path else "#"


def _session(folder: Path) -> str:
    for face in (folder / f"{folder.name}.md", folder.parent / f"{folder.parent.name}.md", folder / "board.md",
                 folder.parent / "board.md", folder.parent.parent / "board.md"):
        if face.is_file():
            m = re.search(r"(?m)^session:\s*`?([\w.-]+)`?", face.read_text(encoding="utf-8", errors="ignore")[:4000])
            if m:
                return m.group(1)
    return folder.name


# ── the shared pieces of a view ─────────────────────────────────────────────────────────────────────────────────
def _copy(label: str, level: str, folder: Path, root: Path, fallback: str = "", verb: str = "Copy prompt") -> str:
    """A row's own Copy prompt: the run card's prompt (its agent, its sign) with this folder filled in, shown on hover."""
    text = V._kind(label, fallback, level=level)["prompt"].replace("{folder}", rel(folder, root))
    if not text:
        return ""
    tail = f'Run this in the Claude session "{_session(folder)}"; start it if it is not running.'
    return (f'<span class="pb-prompt in-copy" title="{esc(text)}"><button type=button class="fd-btn pb-copy" '
            f'data-copy="{esc(text)}" data-tail="{esc(tail)}">{esc(verb)}</button></span>')


def _todo(rows: list) -> str:
    """Rows like ui_parts._todo, each with its own buttons: [(words html, sub, state, verbs html)]."""
    return '<div class=pb-todos>' + "".join(
        f'<div class=pb-todo><span class=w>{w}' + (f"<small>{esc(s)}</small>" if s else "") + "</span>"
        + _pill(state) + verbs + "</div>" for w, s, state, verbs in rows) + "</div>"


def _plain(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(html or ""))).strip()


DONE_WORDS = ("done", "closed", "signed", "released", "passed", "kept", "not needed", "approved", "pinned", "dropped")


def _rows_word(rows: list) -> tuple:
    """(state word, waiting line) of a Process section's rows, read from the rows themselves (R1, 261106): how many wait
    for the person and the first of them; else done, running, how many are done, or the first open row's own word."""
    states = [str(r[2] or "").lower() for r in rows]
    if not rows:
        return "nothing yet", ""
    you = [r for r, s in zip(rows, states) if "waiting for you" in s]
    if you:
        sub = str(you[0][1] or "")
        return (f'{len(you)} wait{"s" if len(you) == 1 else ""} for you',
                f"🙋 {_plain(you[0][0])}" + (f": {sub}" if sub and len(sub) <= 70 else ""))
    done = sum(s.startswith(DONE_WORDS) for s in states)
    if done == len(states):
        return "done", ""
    if any("running" in s for s in states):
        return "running", ""
    if done:
        return f"{done} of {len(states)} done", ""
    return next(str(r[2]) for r, s in zip(rows, states) if not s.startswith(DONE_WORDS)), ""


def _step(title: str, rows: list, extra: str = "") -> str:
    """A ⚙️ Process section: its rows, its state word and waiting line read from them."""
    word, waits = _rows_word(rows)
    return _section(title, _todo(rows) + extra, word, waits)


def _big(line: str, state: str = "") -> str:
    """A view's main point, large, first (haipipe-ui rule 1: seen at a glance), and its state as a mark or an ask.
    A view whose point is only a count of its rows has no line: each row carries its own mark."""
    you = " you" if "for you" in state or "your" in state else ""
    state = state_mark(state)
    return (f'<p class=pb-big>{esc(line)}</p>' if line else "") + (f'<p class="pb-state{you}">{esc(state)}</p>' if state else "")


def _tabs(eid: str, items: list) -> str:
    """Side tabs (the one kind of tabs, R4): [(name, state word, panel html)], no count in a name."""
    items = [i for i in items if i[2]]
    return _side_tabs(eid, [(h, w) for h, w, _ in items], [p for _, _, p in items]) if items else ""


def _chain(steps: list) -> str:
    """A row of steps, each a tile with its role above, joined by arrows: [(role, head, line)]."""
    out = []
    for k, (role, head, line) in enumerate(steps):
        if k:
            out.append('<span class=pb-arrow aria-hidden=true>→</span>')
        out.append(f'<div class=pb-step><span class=pb-role>{esc(role)}</span><div class=pb-tile><b>{esc(head)}</b>'
                   f'<span>{esc(line)}</span></div></div>')
    return '<div class=pb-chain>' + "".join(out) + '</div>'


def _tiles(items: list) -> str:
    return ('<div class=pb-tiles>' + "".join(f'<div class=pb-tile><b>{esc(a)}</b><span>{esc(b)}</span></div>'
                                            for a, b in items) + '</div>')


def _link(path: Path, root: Path, words: str) -> str:
    from live import focus_page as F
    return f'<a href="{esc(F.page_url(path, root))}">{esc(words)}</a>'


def _link_btn(path: Path, root: Path, section: str, group: str, verb: str) -> str:
    from live import focus_page as F
    return f'<a class=fd-btn href="{esc(F.page_url(path, root, section, group))}">{esc(verb)}</a>'


def _closed(r: dict | None) -> bool:
    return bool(r) and str(r.get("status", "")).lower() in ("closed", "done", "ok", "passed")


def _has(rs: list, rtype: str) -> bool:
    return any(_closed(r) for r in rs if r["type"] == rtype)


def _head_css() -> str:
    return PB_CSS + GROUP_CSS + FD.CSS + PROMPT_CSS + CSS


def _page(lead: str, process: str, results: str, after: str = "") -> str:
    """A view: its lead (a design's drafts strip), its steps then its results numbered as one list, where the next step
    is, the side tabs' script and the fold script (R1: every bar starts closed). Work is retired: Report and an old Work link draw this same view, with no ⚙️ Process or 📊 Results heading and
    no grey caption (AGENTS: no secondary labels)."""
    body = lead + _numbered(process + results) + after
    return _head_css() + body + PB_JS + FD.JS + PROMPT_JS + POST_JS


def _work_map(folder: Path, root: Path):
    """The MindMap as a Work view: its Results only, the Report's map (R6: the mind map is always shown)."""
    def build():
        from live import focus_page as FP
        return _head_css() + FP.parts_mindmap(folder, root)          # no caption, no 📊 Results heading
    return ("MindMap", build)


def _views(keys, build, report: bool, folder: Path, root: Path) -> dict:
    """{key: (name, build)}: the same view under the plain key (Report) and under `work-<key>` (an old Work link; R3: the
    rail's same-views check and rail_view read them so), the MindMap last in Work (the page adds Report's)."""
    out = {}
    for key, name in keys:
        def make(key=key):
            _caption, lead, process, results, after = build(key)   # the caption is no longer drawn
            return _page(lead, process, results, after)
        out[key if report else "work-" + key] = (name, make)
    if not report:
        out["work-mindmap"] = _work_map(folder, root)
    return out
