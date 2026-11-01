"""The shared pieces of a workbench view (haipipe-ui: numbered bars, bands, card tabs, side tabs, to-do rows with
state pills, plan rows with Open and Copy prompt) and their stylesheet. Any theme's page draws with these; no theme's
data is read here. The phone rules come last in PB_CSS: a rule placed before the base rule it changes loses to it."""
from __future__ import annotations

import re
from pathlib import Path

from live.frame import esc


def _section(title: str, body: str) -> str:
    return f'<section class=fd-sec><h3 class=fd-h>{esc(title)}</h3>{body}</section>' if body else ""


# ── a paper version's whole paper (JL 261031, on t00_summary › Delivery: "the delviery should be here, right?") ────
# A version Job keeps no delivery/ of its own: the paper build (haipipe-paper-assemble) writes the Board's
# delivery/<version>/, its build-manifest.json naming the assembled files. A version's Delivery shows that paper first,
# then each Section's lanes; the Board's Delivery shows each version's paper.
def _file_link(p: Path, root: Path) -> str:
    from live.frame import _file_url
    return f'<a data-pop="{esc(p.name)}" href="{esc(_file_url(p, root))}">{esc(p.name)}</a>'


def _when(p: Path) -> str:
    import datetime
    return datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")


BOARD_CSS = """<style>.pb-topic{font-size:15px;margin:0 0 8px}.pb-verbs{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 14px}
.pb-part{font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin:26px 0 10px}
.pb-draw{display:block;max-height:520px;overflow:auto}
.pb-map{max-height:85vh;overflow:auto;border:1px solid var(--line);border-radius:6px;padding:8px}.pb-draw img{display:block;max-width:100%}</style>"""


# ── the Board Report's views in the shape settled in b16 s32 (JL 261031): every section a numbered heading bar with
# one emoji, in reading order; the main point large under section 1; content shown as what it is (tiles, tabs, a
# chain); the helpers (🙋 Interactions, 🖼️ The drawing, 🧠 The mind map) unnumbered at the bottom ───────────────────
EMOJI = {"direction": "🧭", "directions considered": "🔀", "hand-off": "🤝", "pitch": "💡", "questions": "❓",
         "stakes and evidence basis": "⚖️", "venues": "🏛️", "roadmaps": "🗺️", "section narrative": "🧠",
         "interactions": "🙋", "the drawing": "🖼️", "the mind map": "🧠", "flow": "🔗", "questions to runs": "🧩",
         "waits on": "🚧", "interactions": "🙋", "open": "🚧", "skills": "🧰", "where each stands": "📋", "steps": "🪜", "send": "📮", "sections": "📑", "displays": "🖼️", "timeline": "🗓️", "work blocks": "🧪",
         "discovery blocks": "🔎", "values": "🔢", "citations": "📚", "work": "🧪", "discovery": "🔎"}


PB_CSS = """<style>
:root{--pb-soft:light-dark(#e7f5ff,#253749);--pb-ok:light-dark(#2b8a3e,#8bd49a);--pb-ok-bg:light-dark(#ebfbee,#1d3324);
 --pb-you:light-dark(#b35c00,#ffb36b);--pb-you-line:light-dark(#e8590c,#ff922b);--pb-you-bg:light-dark(#fff4e6,#3b2a17);
 --pb-run:light-dark(#1864ab,#91caff)}   /* every state colour reads in dark mode too (b16 review 261101) */
.pb-big{font-size:20px;line-height:1.5;margin:4px 0 4px;color:var(--ink)}.pb-state{font-size:12px;color:var(--pb-ok);margin:0 0 6px}
.pb-tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px;margin:4px 0 8px}
.pb-tile{border:1px solid var(--line);border-radius:8px;padding:10px 12px;background:var(--paper);text-align:left;font:inherit;color:var(--ink)}
.pb-tile b{display:block;color:var(--accent);font-size:13.5px;margin:0 0 4px}.pb-tile span{font-size:13px;line-height:1.45}
.pb-tile small{display:block;color:var(--muted);font-size:12px;margin-top:4px}
.pb-tile span{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.pb-panel .fd-row .d,.pb-kv dd{overflow-wrap:anywhere;min-width:0}
button.pb-tile{cursor:pointer;display:flex;flex-direction:column;justify-content:flex-start}button.pb-tile:hover{border-color:var(--accent)}button.pb-tile.on{border-color:var(--accent);background:var(--pb-soft)}
.pb-panel{border:1px solid var(--accent);border-radius:8px;padding:10px 14px;margin:0 0 8px}.pb-panel[hidden]{display:none}
.pb-kv{display:grid;grid-template-columns:150px 1fr;gap:6px 14px;font-size:13.5px;line-height:1.5}.pb-kv dt{color:var(--accent);font-weight:500}
.pb-kv dd{margin:0}
.pb-tiles>.pb-tile{height:100%}.pb-tile.pb-chosen{grid-column:1/-1;border-left:4px solid var(--pb-ok)}
.pb-tile.pb-chosen b,.pb-tile.pb-chosen1 b{color:var(--pb-ok)}.pb-tile.pb-gone b{color:var(--muted)}
.pb-tile.pb-chosen1{border-left:4px solid var(--pb-ok)}
.pb-chain{display:flex;flex-wrap:wrap;align-items:stretch;gap:10px 4px;margin:4px 0 10px}
.pb-chain .pb-step{display:flex;flex-direction:column;gap:3px;width:190px}.pb-chain .pb-role{font-size:11px;color:var(--muted)}
.pb-chain .pb-tile{width:100%;flex:1}.pb-chain .pb-arrow{color:var(--muted);padding:0 4px;align-self:center;margin-top:14px;font-size:18px}
.pb-chain .pb-step:first-child .pb-role{color:var(--accent)}
.pb-pic{display:flex;align-items:flex-end;gap:12px;flex-wrap:wrap}.pb-pic img{max-width:360px;max-height:220px;border:1px solid var(--line);border-radius:6px}
.pb-lead{font-size:14px;margin:0 0 8px}
.pb-tree{font-size:13.5px;line-height:1.5;margin:4px 0 10px}.pb-root{display:inline-block;border:1px solid var(--accent);
 background:var(--pb-soft);border-radius:6px;padding:3px 10px;font-weight:600}.pb-tree ul{list-style:none;margin:6px 0 0 18px;padding-left:14px;
 border-left:1px solid var(--line)}.pb-tree li{margin:6px 0}.pb-tree li b{color:var(--accent)}.pb-c{font-size:11.5px;color:var(--muted);margin-right:4px}
.pb-rule{border:0;border-top:1px dashed var(--line);margin:22px 0 16px}
.pb-flow{position:relative;display:grid;grid-template-columns:repeat(4,1fr);gap:18px 34px;margin:10px 0 6px}
.pb-col{display:flex;flex-direction:column;gap:10px;position:relative;z-index:1}.pb-colh{margin:0 0 2px;font-size:12px;font-weight:600;
 color:var(--accent);text-transform:uppercase;letter-spacing:.04em}.pb-colh small{display:block;text-transform:none;letter-spacing:0;
 color:var(--muted);font-weight:400}.pb-node{border:1px solid var(--line);border-radius:8px;background:var(--paper);padding:7px 10px;
 font-size:12.5px;line-height:1.35}.pb-node b{display:block;font-size:13px}.pb-node span{display:block;color:var(--ink)}
.pb-node small{display:block;color:var(--muted);font-size:11px;margin-top:2px}.pb-col:last-child .pb-node{border-color:var(--accent)}
.pb-wires{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible;z-index:0}
.pb-ftree,.pb-ftree ul{list-style:none;margin:0;padding:0}.pb-ftree ul{margin-left:9px;padding-left:16px;border-left:1px solid var(--line)}
.pb-ftree li{position:relative;padding:3px 0;font-size:13.5px}.pb-ftree ul>li::before{content:"";position:absolute;left:-16px;top:13px;
 width:12px;border-top:1px solid var(--line)}.pb-ftree a,.pb-ftree span{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
 font-size:13px;color:var(--accent);text-decoration:none}.pb-ftree span{color:var(--muted)}.pb-ftree a:hover{text-decoration:underline}
.pb-frow{display:flex;gap:12px;align-items:baseline;min-width:0}.pb-frow a{flex:none}
.pb-ftree small{flex:1;min-width:0;color:var(--muted);font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pb-ftree li{padding:2px 0}.pb-ftree a.pb-main{font-weight:700}.pb-mainw{flex:none;font-style:normal;font-size:11.5px;color:var(--pb-ok);border:1px solid var(--pb-ok);border-radius:10px;padding:0 7px}.pb-ftree+.pb-ftree{margin-top:14px}
.pb-side{display:grid;grid-template-columns:170px minmax(0,1fr);gap:14px;align-items:start;margin:4px 0 8px}
.pb-list{display:flex;flex-direction:column;gap:4px;position:sticky;top:12px}.pb-item{display:block;text-align:left;border:1px solid transparent;
 border-radius:7px;padding:6px 10px;background:none;font:inherit;color:var(--ink);cursor:pointer}.pb-item b{display:block;font-size:13.5px;
 font-weight:600}.pb-item span{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;font-size:12px;color:var(--muted);overflow:hidden}
.pb-checks{list-style:none;margin:4px 0 8px;padding:0;font-size:13.5px;line-height:1.6}.pb-sketch{margin:8px 0 0;padding:8px 10px;border-radius:6px;
 background:var(--wash);font:12.5px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:pre;overflow-x:auto}
.pb-item:hover{border-color:var(--line)}.pb-item.on{border-color:var(--accent);background:var(--pb-soft)}.pb-item.on b{color:var(--accent)}
.pb-read .pb-panel{margin:0;min-height:120px}.pb-text h4{font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;
 letter-spacing:.04em;margin:14px 0 4px}.pb-text h4:first-child{margin-top:2px}.pb-text p{font-size:15px;line-height:1.65;margin:0 0 6px}
.pb-ptop{display:flex;justify-content:space-between;align-items:center;gap:10px;margin:0 0 6px}.pb-ptop .pb-state{margin:0}
.pb-pdf{display:block;width:100%;height:60vh;border:1px solid var(--line);border-radius:6px;background:#fff}
.pb-wide img{display:block;max-width:100%;border:1px solid var(--line);border-radius:6px;margin:6px 0}
.pb-steps{border-left:2px solid var(--line);margin:4px 0 8px 6px}.pb-srow{display:flex;gap:12px;align-items:baseline;padding:6px 0 6px 14px;font-size:13.5px}
.pb-when{flex:none;width:52px;color:var(--muted)}.pb-what{flex:1}.pb-what small{display:block;color:var(--muted);font-size:12px}
.pb-st{flex:none;font-size:12.5px;white-space:nowrap}
.pb-panel .fd-steps{display:flex;flex-wrap:wrap;gap:6px}.pb-panel .fd-step{border:1px solid var(--line);border-radius:5px;padding:2px 8px;
 font-size:12px;text-decoration:none;color:var(--ink)}.pb-panel .fd-step b{font-weight:600;margin-left:3px}
.pb-hop{display:flex;align-items:stretch;flex:1 1 0;min-width:130px}.pb-hop .pb-step{flex:1;width:auto}
.pb-chain{flex-wrap:nowrap;overflow-x:auto}.pb-nar{margin:8px 0 0 16px;padding-left:16px;border-left:2px solid var(--line)}
.pb-nrow{display:flex;gap:12px;align-items:flex-start;margin:8px 0}.pb-sbox{flex:none;width:120px;border:1px solid var(--accent);
 border-radius:6px;padding:4px 10px;font-weight:600;color:var(--accent);background:var(--paper)}
.pb-chips{display:flex;flex-wrap:wrap;gap:6px}.pb-chip{border:1px solid var(--line);border-radius:14px;padding:3px 10px;font-size:12.5px;
 background:var(--wash)}.pb-chip b{color:var(--muted);font-weight:600;margin-right:2px}
.pb-todos{display:flex;flex-direction:column;gap:8px;margin:2px 0 6px}.pb-todo{display:flex;align-items:center;gap:12px;
 border:1px solid var(--line);border-radius:8px;padding:9px 14px;background:var(--paper)}.pb-todo .w{flex:1;min-width:0;font-size:15px;
 line-height:1.4}.pb-todo .w small{display:block;font-size:12px;color:var(--muted)}
.pb-pill{flex:none;font-size:12px;border:1px solid var(--line);border-radius:6px;padding:2px 9px;background:var(--wash);white-space:nowrap}
.pb-pill.you{border-color:var(--pb-you-line);background:var(--pb-you-bg);color:var(--pb-you)}.pb-pill.run{border-color:var(--pb-run);background:var(--pb-soft);color:var(--pb-run)}
.pb-pill.ok{border-color:var(--pb-ok);background:var(--pb-ok-bg);color:var(--pb-ok)}
.pb-agents{border:1px solid var(--line);border-radius:8px;padding:6px 14px}.pb-agents div{padding:4px 0;font-size:13.5px}
.pb-agents b{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px}
.pb-group{display:flex;align-items:center;gap:12px;margin:26px 0 12px;font-size:17px;font-weight:600;color:var(--ink)}
.pb-group::after{content:"";flex:1;border-top:1px solid var(--line)}.pb-group:first-child{margin-top:6px}
.pb-skill{display:flex;gap:12px;align-items:baseline;padding:6px 0;border-bottom:1px solid var(--line);font-size:13.5px}
.pb-skill b{flex:none;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px}.pb-skill span{color:var(--muted)}
.pb-askbox{border:1px solid var(--pb-you-line);border-radius:8px;background:var(--pb-you-bg);padding:2px 12px}.pb-askbox .fd-row{border-bottom:0}
.fd-body table{display:block;overflow-x:auto;max-width:100%}
@media(max-width:600px){.fd-row{flex-wrap:wrap}.fd-row .n{min-width:0;flex-basis:100%}.pb-kv{grid-template-columns:1fr}
 .pb-chain{flex-direction:column}.pb-chain .pb-step{width:100%}.pb-chain .pb-arrow{transform:rotate(90deg);margin:0;align-self:flex-start;padding:2px 20px}.pb-pic img{max-width:100%}}
/* phone rules last: an @media rule placed before its base rule loses to it (b16 s32 review r02) */
@media(max-width:700px){.pb-flow{grid-template-columns:1fr}.pb-wires{display:none}.pb-side{grid-template-columns:1fr}
 .pb-list{position:static;flex-direction:row;flex-wrap:wrap}.pb-item span{display:none}}
@media(max-width:600px){.pb-panel table,.pb-panel tbody,.pb-panel tr,.pb-panel td{display:block;width:100%;min-width:0}
 .pb-panel thead{display:none}.pb-panel tr{border-bottom:1px solid var(--line);padding:6px 0}.pb-panel td{border:0;padding:2px 0}
 .pb-srow{flex-wrap:wrap}.pb-what{flex:1 1 calc(100% - 64px)}.pb-st{margin-left:64px;white-space:normal}
 .fd-body td,.fd-body th{min-width:120px}.pb-nrow{flex-direction:column;gap:6px}
 .pb-hop{flex-direction:column}.fd-body pre{white-space:pre-wrap;overflow-wrap:anywhere}.fd-row{flex-wrap:wrap}.fd-row .n{min-width:0}}
@media(max-width:600px){.pb-srow{flex-wrap:wrap}.pb-what{flex:1 1 calc(100% - 64px);min-width:0}.pb-st{margin-left:64px}
 .pb-ftree ul{margin-left:4px;padding-left:10px}.pb-ftree ul>li::before{left:-10px;width:8px}.pb-frow{flex-direction:column;gap:0}
 .pb-skill{flex-direction:column;gap:0}.pb-todo{flex-wrap:wrap}.pb-todo .w{flex:1 1 100%}.pb-ftree a{overflow-wrap:anywhere}.pb-ftree small{white-space:normal;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}.pb-item span{display:none}}
</style>"""


PB_JS = """<script>(function(){if(window.pbTabs)return;window.pbTabs=1;
 document.addEventListener('click',function(ev){var t=ev.target.closest('[data-pbtab]');if(!t)return;
  var set=t.closest('.pb-tabset');if(!set)return;var own=function(e){return e.closest('.pb-tabset')===set;};  /* a tabset inside a panel keeps its own */
  set.querySelectorAll('[data-pbtab]').forEach(function(b){if(own(b))b.classList.toggle('on',b===t);});
  set.querySelectorAll('.pb-panel').forEach(function(p){if(own(p))p.hidden=p.dataset.pbpanel!==t.dataset.pbtab;});});
 function wire(){document.querySelectorAll('.pb-flow').forEach(function(f){var svg=f.querySelector('.pb-wires');if(!svg)return;
  var r=f.getBoundingClientRect(),out='';JSON.parse(f.dataset.links||'[]').forEach(function(l){
   var a=f.querySelector('[data-key="'+CSS.escape(l[0])+'"]'),b=f.querySelector('[data-key="'+CSS.escape(l[1])+'"]');if(!a||!b)return;
   var p=a.getBoundingClientRect(),q=b.getBoundingClientRect();if(!p.width||!q.width)return;
   var x1=p.right-r.left,y1=p.top+p.height/2-r.top,x2=q.left-r.left,y2=q.top+q.height/2-r.top,m=(x1+x2)/2;
   out+='<path d="M'+x1+' '+y1+' C'+m+' '+y1+' '+m+' '+y2+' '+x2+' '+y2+'" fill="none" stroke="#adb5bd" stroke-width="1.5"/>';});
  svg.innerHTML=out;});}
 window.addEventListener('load',wire);window.addEventListener('resize',wire);document.addEventListener('click',function(){setTimeout(wire,30);});
 setTimeout(wire,50);})();</script>"""


def _bar(n, name: str, body: str) -> str:
    """One section: `N · <emoji> name` (or unnumbered, a helper), its content under it."""
    title = (f"{n} · " if n else "") + f"{EMOJI.get(name.lower(), '')} {name}".strip()
    return _section(title, body)


def _plain(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\*\*|`|\[([^\]]+)\]\([^)]*\)", lambda m: m.group(1) or "", text)).strip()


def _clean(text: str) -> str:
    """A sentence for the large line: no ⟦…⟧ process notes."""
    return re.sub(r"\s*⟦[^⟧]*⟧", "", text).strip()


def _cap(text: str) -> str:
    return text[:1].upper() + text[1:]


def _card_tabs(eid: str, tiles: list, panels: list, chain: bool = False) -> str:
    """Card tabs (JL 261031: "we will use the cards-tab"): cards that act as a view-button-list, the first open, one
    open at a time, its panel below; `chain` draws them as a card-tab chain, an arrow before each card after the first."""
    btns = []
    for k, (head, line, role, *cls) in enumerate(tiles):
        b = (f'<button type=button class="pb-tile{" on" if k == 0 else ""}{cls[0] if cls else ""}" data-pbtab="{eid}{k}"><b>{esc(head)}</b>'
             f'<span>{esc(line)}</span></button>')
        step = f'<div class=pb-step><span class=pb-role>{esc(role)}</span>{b}</div>'
        btns.append((f'<div class=pb-hop>{"<span class=pb-arrow>→</span>" if k else ""}{step}</div>') if chain else b)
    row = (f'<div class=pb-chain>{"".join(btns)}</div>' if chain else f'<div class=pb-tiles>{"".join(btns)}</div>')
    return (f'<div class=pb-tabset>{row}' + "".join(f'<div class=pb-panel data-pbpanel="{eid}{k}"{"" if k == 0 else " hidden"}>{p}</div>'
                                                   for k, p in enumerate(panels)) + '</div>')


def _side_tabs(eid: str, items: list, panels: list) -> str:
    """Side tabs (JL 261101: "in the left there is a panel, and we can read the content quickly"): the items as a list
    on the left, one line each (its name, its state), the open one's content on the right to read; the first open.
    For content that is read (a Section's text, a display, a value list), where card tabs would push it down."""
    rows = "".join(f'<button type=button class="pb-item{" on" if k == 0 else ""}" data-pbtab="{eid}{k}"><b>{esc(h)}</b>'
                   f'<span title="{esc(w)}">{esc(w)}</span></button>' for k, (h, w) in enumerate(items))
    return (f'<div class="pb-tabset pb-side"><div class=pb-list>{rows}</div><div class=pb-read>'
            + "".join(f'<div class=pb-panel data-pbpanel="{eid}{k}"{"" if k == 0 else " hidden"}>{p}</div>' for k, p in enumerate(panels))
            + '</div></div>')


def _kv(pairs) -> str:
    return '<dl class=pb-kv>' + "".join(f'<dt>{esc(k)}</dt><dd>{v}</dd>' for k, v in pairs if v) + '</dl>'


def _open_btn(label: str, url: str, pop: str = "") -> str:
    return f'<a class=fd-btn{f" data-pop={chr(34)}{esc(pop)}{chr(34)}" if pop else ""} href="{esc(url)}">{esc(label)}</a>'


# A view's two parts, one look in every theme (b15 s58's decision report draws the same, workbench-labeling
# decision_report_view.py): a heading with its emoji and a thin rule after it, no subtitle (JL 261101).
PROCESS, RESULTS = "⚙️ Process", "📊 Results"


GROUP_CSS = """<style>.pb-group{display:flex;align-items:center;gap:12px;margin:26px 0 12px;font-size:17px;font-weight:600;
color:var(--ink)}.pb-group::after{content:"";flex:1;border-top:1px solid var(--line)}.pb-group:first-child{margin-top:6px}</style>"""


def _numbered(html: str) -> str:
    """Each top-level section of `html` numbered in order, "N · <its title>" (a nested one keeps its title)."""
    import re as _re
    out, depth, n, pos = [], 0, 0, 0
    for m in _re.finditer(r"<section\b[^>]*>|</section>", html):
        if m.group(0).startswith("</"):
            depth -= 1
            continue
        if depth == 0 and m.group(0) == "<section class=fd-sec>":
            h = _re.match(r"<h3 class=fd-h>(?!\d+ · )", html[m.end():])
            if h:
                n += 1
                out.append(html[pos:m.end() + h.end()] + f"{n} · ")
                pos = m.end() + h.end()
        depth += 1
    return "".join(out) + html[pos:]


def _band(name: str, body: str) -> str:
    """One part of a view, PROCESS or RESULTS, its sections under it; nothing when it has none."""
    return f'<h3 class=pb-group>{esc(name)}</h3>' + body if body else ""


TODO_CLASS = (("waiting for you", "you"), ("needs your", "you"), ("running", "run"), ("in progress", "run"), ("done", "ok"),
              ("checked", "ok"), ("answered", "ok"), ("drawn", "ok"))


def _pill(state: str) -> str:
    """A state as a coloured word (s58: orange waits on you, blue running, green done, grey open or not started)."""
    low = state.lower()
    cls = next((c for w, c in TODO_CLASS if w in low), "")
    return f'<span class="pb-pill {cls}">{esc(state)}</span>' if state else ""


def _todo(rows) -> str:
    """One full-width row per thing to do, step by step: its words large, its state a pill, its verb on the row (b15 s58
    C2, JL 261101: "in each step, we should have something to do step by step")."""
    return '<div class=pb-todos>' + "".join(
        f'<div class=pb-todo><span class=w>{esc(words)}{f"<small>{esc(sub)}</small>" if sub else ""}</span>{_pill(state)}'
        + (f'<a class=fd-btn href="{esc(href)}"{" data-pop=" + chr(34) + esc(words) + chr(34) if pop else ""}>{esc(verb)}</a>' if href else "")
        + '</div>' for words, sub, state, verb, href, pop in rows) + '</div>'


def _plan_html(steps: list, session: str = "", key: str = "") -> str:
    """Each plan step in the one Prompt box (prompt_box below; JL 261101): its name and the skill to use on the head,
    Open beside Copy prompt, the prompt, a "your notes" row, the session line."""
    return "".join(prompt_box(prompt, None, session, step=t, asks=f"use /{skill}", key=f"{key}#{t}" if key else "",
                              verbs=f'<a class=fd-btn data-pop="{esc(t)}" href="{esc(href)}">Open</a>')
                   for t, what, skill, href, prompt in steps)



# ── one Prompt box for every theme (JL 261101, relayed by Theme_Labeling; drawn in b15 s58 view C1): its head
# "✍️ Prompt · <step> · <what it asks for>" with Copy prompt (and any verbs) at the right, the prompt filled from the
# step's real inputs in a grey block, one labeled row per field only the person fills, then the session line. Copy
# prompt copies the prompt, the filled fields ("<label>: <value>") and the session line, in that order. Each step
# keeps its own words (template, fields); only the box is shared. ──────────────────────────────────────────────────
PROMPT_CSS = """<style>.pb-prompt{border:1px solid var(--line);border-radius:8px;padding:8px 12px 10px;margin:0 0 10px;background:var(--paper)}
.pb-ph{display:flex;align-items:center;gap:8px;font-size:14px;margin:0 0 6px}.pb-ph span{flex:1;min-width:0}
.pb-pt{margin:0 0 6px;padding:8px 10px;border-radius:6px;background:var(--wash);white-space:pre-wrap;overflow-wrap:anywhere;
 font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}
.pb-fr{display:grid;grid-template-columns:120px minmax(0,1fr);gap:10px;align-items:start;margin:0 0 6px;font-size:12.5px;color:var(--muted)}
.pb-fr textarea{width:100%;box-sizing:border-box;min-height:32px;resize:vertical;border:1px solid var(--line);border-radius:6px;
 padding:5px 8px;font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--paper);color:var(--ink)}
.pb-sess{margin:2px 0 0;font-size:12px;color:var(--muted)}
@media(max-width:600px){.pb-fr{grid-template-columns:1fr;gap:2px}.pb-ph{flex-wrap:wrap}}</style>"""
PROMPT_JS = """<script>(function(){if(window.pbPrompt)return;window.pbPrompt=1;
 function get(k){try{return localStorage.getItem(k)||'';}catch(e){return '';}}
 function put(k,v){try{localStorage.setItem(k,v);}catch(e){}}
 function ready(fn){if(document.readyState!=='loading')fn();else document.addEventListener('DOMContentLoaded',fn);}
 ready(function(){document.querySelectorAll('.pb-prompt [data-field][data-key]').forEach(function(t){
  if(!t.value&&!t.readOnly)t.value=get(t.dataset.key);t.addEventListener('input',function(){put(t.dataset.key,t.value);});});});
 document.addEventListener('click',function(ev){var b=ev.target.closest('.pb-copy');if(!b)return;ev.preventDefault();
  var box=b.closest('.pb-prompt'),text=b.dataset.copy||'';
  box.querySelectorAll('[data-field]').forEach(function(t){if(t.value.trim())text+='\\n'+t.dataset.field+': '+t.value.trim();});
  if(b.dataset.tail)text+='\\n'+b.dataset.tail;
  var was=b.textContent,done=function(){b.textContent='Copied';setTimeout(function(){b.textContent=was;},1400);};
  cp(text,done);});
 /* a row that takes an image (upload): the host keeps a pasted image and the row names where (b15 s41-D14) */
 document.addEventListener('paste',function(ev){var t=ev.target.closest&&ev.target.closest('.pb-prompt textarea[data-upload]');if(!t)return;
  var items=(ev.clipboardData&&ev.clipboardData.items)||[];
  for(var i=0;i<items.length;i++){if(items[i].type.indexOf('image/')!==0)continue;ev.preventDefault();var r=new FileReader();
   r.onload=function(){fetch(t.dataset.upload,{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({folder:t.dataset.folder,data:r.result})}).then(function(x){return x.json();}).then(function(j){
    t.value=(t.value?t.value.replace(/\\s*$/,'\\n'):'')+(j.ok?('🖼 an image, kept at '+j.path):('✗ the image was not kept: '+j.err))+'\\n';
    if(t.dataset.key)put(t.dataset.key,t.value);});};r.readAsDataURL(items[i].getAsFile());return;}});
 /* the pages are served over http, where navigator.clipboard is missing: copy through a hidden textarea then */
 function cp(text,done){if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(text).then(done,function(){old(text);done();});}else{old(text);done();}}function old(text){var t=document.createElement('textarea');t.value=text;t.setAttribute('readonly','');t.style.position='fixed';t.style.top='-1000px';document.body.appendChild(t);t.select();try{document.execCommand('copy');}catch(e){}document.body.removeChild(t);}
})();</script>"""
NOTES = (("your notes", "notes, a row, a sentence to change"),)


def prompt_box(template: str, fields=None, session: str = "", step: str = "", asks: str = "", key: str = "",
               verbs: str = "", sent: dict | None = None, upload: tuple | None = None) -> str:
    """The shared Prompt box. `fields`: [(label, placeholder)], the rows only the person fills (default: one "your
    notes" row; () for none); `session`: the Claude session it runs in; `step`, `asks`: its head; `key`: where the
    fields are kept in this browser; `verbs`: more buttons on the head (Open); `sent`: {label: value} once the step
    has run, shown read only in place of the empty fields; `upload`: (folder, url) lets the first row take a pasted
    image, which the host keeps in that folder and names in the row (labeling's notes, b15 s41-D14)."""
    fields = NOTES if fields is None else fields
    tail = f'Run this in the Claude session "{session}"; start it if it is not running.' if session else ""
    head = " · ".join(x for x in ("✍️ Prompt", step, asks) if x)
    rows = "".join(
        f'<label class=pb-fr><span>{esc(lab)}</span><textarea rows=1 data-field="{esc(lab)}" '
        + (f'data-key="{esc(key)}#{esc(lab)}" ' if key and not sent else "")
        + (f'data-folder="{esc(upload[0])}" data-upload="{esc(upload[1])}" ' if upload and not sent and n == 0 else "")
        + ('readonly ' if sent else "") + f'placeholder="{esc(ph)}">{esc((sent or {}).get(lab, ""))}</textarea></label>'
        for n, (lab, ph) in enumerate(fields))
    return ("<!--pb-prompt-->" + PROMPT_CSS + f'<div class=pb-prompt><div class=pb-ph><span>{esc(head)}</span>{verbs}'
            f'<button type=button class="fd-btn pb-copy" data-copy="{esc(template)}"' + (f' data-tail="{esc(tail)}"' if tail else "")
            + f'>Copy prompt</button></div><pre class=pb-pt>{esc(template)}</pre>{rows}'
            + (f'<p class=pb-sess>{esc(tail)}</p>' if tail else "") + "</div>" + PROMPT_JS + "<!--/pb-prompt-->")
