"""A mind map drawn as the draft's §1 Structure map is (servers/workbench/workbench-task-draft/draft_steps.py
`_plan_map`): HTML, not a canvas. The root on the left, each node's children in a column to its right, a curved
wire from a node to each child; a node's note shows on hover. Edited where it is read: click a node and type,
Enter adds the next node below it, ＋ adds a child, an emptied node is taken out, a node dragged onto another goes
before it. Each change is one POST to `/_board/mindmap`, which `act` writes into the `.mindmap.md` file, the source.

    fragment(md, rel, editable)   the map for the workbench card (or, read only, for the static page)
    act(root, payload)            one change, written into the file; refused when the file changed under the page
"""
from __future__ import annotations

import html
import re
from pathlib import Path

import mmhtml as MH
import mmtree as MT

esc = lambda s: html.escape(str(s), quote=True)
norm = lambda s: " ".join(str(s or "").split())


LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
IMAGE = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")


def _opens(raw: str, base: Path | None, url_of) -> str:
    """A node whose words link a file (`[s01.png](s01.png)`) gets a button beside its words that opens it: a picture
    shows as itself, a drawing in its editor, a page in its reader (url_of, the host's), else the file as it is. A
    link to a file that is not there opens nothing."""
    out = []
    for label, target in LINK.findall(raw):
        if re.match(r"^[a-z]+:", target):
            url = target
        else:
            path = (base / target) if base else None
            if url_of and path is not None:
                url = url_of(path) if path.exists() else None
            else:
                url = target                              # the static page sits beside the files it links
        if url:
            icon = "🖼" if target.lower().endswith(IMAGE) else "↗"
            out.append(f'<a class=mm-open data-pop="{esc(label)}" href="{esc(url)}" target=_blank rel=noopener '
                       f'title="open {esc(label)}">{icon}</a>')
    return "".join(out)


FULL_LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)")


def _resolve(md: str, base: Path | None, url_of) -> str:
    """A detail's links and pictures pointed where the host opens them; one to a file not on disk keeps its words."""
    def one(m):
        bang, label, target = m.groups()
        if re.match(r"^[a-z]+:", target) or not (base and url_of):
            return m.group(0)
        path = base / target
        return f"{bang}[{label}]({url_of(path)})" if path.exists() else label
    return FULL_LINK.sub(one, md)


def _node(n: MT.Node, depth: int, editable: bool, base: Path | None = None, url_of=None, k: int = 0) -> str:
    """A card: a few words, the bubble that opens the file it names (🖼 or ↗), and ▸ that opens its detail (the lines
    under its bullet, Markdown, with its links and pictures) below the words (JL 261026: "它既有可以点开的泡泡链接，
    点开之后也可以看到 detail information")."""
    raw = MT.ID_MARK.sub("", n.text)
    shown = MH.inline(LINK.sub(lambda m: m.group(1), raw))     # the card shows a link's words; its bubble opens it
    words = (f'<span class=mm-t data-edit=text data-raw="{esc(raw)}" contenteditable=plaintext-only '
             f'spellcheck=false>{shown}</span>') if editable else f'<span class=mm-t>{shown}</span>'
    note = "\n".join(n.note)
    more = (f'<button type=button class=mm-more aria-expanded=false title="{"its detail" if note else "add a detail"}"'
            f'{"" if note else " data-empty=1"}>▸</button>') if note or editable else ""
    body = MH.blocks(_resolve(note, base, url_of)) if note else ""
    pen = (f'<button type=button class=mm-pen data-raw="{esc(note)}" title="edit the detail">✎</button>'
           if editable else "")
    detail = f'<div class=mm-detail hidden>{body}{pen}</div>' if more else ""
    kids = "".join(_node(c, depth + 1, editable, base, url_of, j) for j, c in enumerate(n.children))
    plus = (f'<div class=mm-add><button type=button class=mm-plus data-add=child>＋</button></div>'
            if editable else "")
    cls = "mm-node mm-root" if depth == 0 else f"mm-node mm-d{min(depth, 3)}"   # any depth; the deepest, a leaf
    drag = " draggable=true" if editable and depth else ""
    branch = f" mm-b{k + 1 if k < 8 else 0}" if depth == 1 else ""   # eight hues in fixed order; a ninth on is grey
    return (f'<div class="mm-row{branch}" data-id="{esc(n.id)}"><div class="{cls}"{drag}>{words}{_opens(raw, base, url_of)}'
            f'{more}{detail}</div><div class=mm-kids>{kids}{plus}</div></div>')


def fragment(md: Path, rel: str = "", editable: bool = True, url_of=None) -> str:
    """The map of one `.mindmap.md`: CSS, the map, and (editable) the script that posts each change. `url_of(path)`:
    where the host opens a linked file (a picture, a drawing, a page)."""
    mm = MT.load(md)
    if editable and MT.ensure_ids(mm):
        MT.save(mm, md)                               # a bullet typed by hand gets its id before it can be edited
    return draw(mm, rel, editable, Path(md).parent, url_of)


def draw(mm: MT.MindMap, rel: str = "", editable: bool = False, base: Path | None = None, url_of=None) -> str:
    """The map of a tree already read; `rel`, the file's path from the host's root, is where its edits post;
    `base`, the folder its links are read from."""
    attrs = f' data-file="{esc(rel)}"' if editable else ""
    styles = "".join(f'<button type=button data-mm-style={k} aria-pressed="{str(k == "branches").lower()}">{v}</button>'
                     for k, v in STYLES)
    return (CSS + f'<div class=mm-edit{attrs} data-style=branches><span class=mm-msg role=status></span>'
            f'<div class=mm-style role=group aria-label="Mind map style">{styles}</div>'
            f'<div class=mm><svg class=mm-wires aria-hidden=true></svg>{_node(mm.root, 0, editable, base, url_of)}</div></div>'
            + WIRES + (EDIT if editable else ""))


# ── one change into the file ───────────────────────────────────────────────────────────────────────────────
def act(root: Path, p: dict, read_only: bool = False) -> tuple:
    """(status, reply) for one change a person makes on the map: `text` (a node's words), `add` (a new node under
    `parent`, after `after`), `drop` (taken out; what hung under it moves up), `move` (before `before`, or last
    under `parent`). `was` is the node's words as the page showed them: a change to words that changed on disk since
    is refused, so nothing typed elsewhere is lost."""
    if read_only:
        return 403, {"ok": False, "err": "this host is read-only"}
    root = Path(root).resolve()
    md = (root / str(p.get("file") or "").strip("/")).resolve()
    if not (md.is_file() and md.name.endswith(MT.SUFFIX) and root in md.parents):
        return 400, {"ok": False, "err": "no such mind map"}
    what, value, was = str(p.get("what") or ""), norm(p.get("value")), norm(p.get("was"))
    if any(c in value for c in "<>") or len(value) > 4000:
        return 400, {"ok": False, "err": "plain words only"}
    mm = MT.load(md)
    MT.ensure_ids(mm)
    node, parent = MT.find(mm, str(p.get("id") or ""))
    gone = (409, {"ok": False, "err": "it changed on disk; the map reloads", "reload": True})
    if what in ("text", "drop", "move") and node is None:
        return gone
    if what in ("text", "drop") and norm(MT.ID_MARK.sub("", node.text)) != was:
        return gone
    if what != "note" and "\n" in str(p.get("value") or ""):
        return 400, {"ok": False, "err": "one line: a node's words; a detail takes lines"}
    out = {"ok": True}
    if what == "text":
        if not value:
            return 400, {"ok": False, "err": "empty: take the node out instead"}
        node.text = value
        out["html"] = MH.inline(value)
    elif what == "note":                              # the detail: lines, Markdown; a line never starts a bullet
        if norm(" ".join(node.note)) != was:
            return gone
        lines = [ln.rstrip() for ln in str(p.get("value") or "").replace("\r", "").split("\n") if ln.strip()]
        node.note = [MT.BULLET.sub(lambda m: m.group(1) + "· " + m.group(2), ln) for ln in lines]
    elif what == "drop":
        if parent is None:
            return 400, {"ok": False, "err": "the root stays; change its words instead"}
        k = parent.children.index(node)
        parent.children[k:k + 1] = node.children
    elif what == "add":
        if not value:
            return 400, {"ok": False, "err": "empty"}
        under, _ = MT.find(mm, str(p.get("parent") or "root"))
        if under is None:
            return gone
        taken = {n.id for n, *_ in MT.walk(mm.root)}
        new = MT.Node(next(MT.next_ids(taken)), value)
        ids = [c.id for c in under.children]
        under.children.insert(ids.index(p["after"]) + 1 if p.get("after") in ids else len(ids), new)
        out["id"] = new.id
    elif what == "move":
        if parent is None:
            return 400, {"ok": False, "err": "the root stays where it is"}
        before, bp = MT.find(mm, str(p.get("before") or ""))
        under = bp if before is not None else MT.find(mm, str(p.get("parent") or ""))[0]
        if under is None:
            return gone
        if _inside(node, under):
            return 400, {"ok": False, "err": "a node cannot go under itself"}
        parent.children.remove(node)
        k = under.children.index(before) if before is not None and before in under.children else len(under.children)
        under.children.insert(k, node)
    else:
        return 400, {"ok": False, "err": f"unknown change {what!r}"}
    MT.save(mm, md)
    v = MT.views(md)
    with open(v["html"], "w", encoding="utf-8", newline="\n") as f:     # the static page follows the file
        f.write(MH.page(mm))
    return 200, out


def _inside(node: MT.Node, other: MT.Node) -> bool:
    """`other` is `node` or hangs somewhere under it."""
    return any(x is other for x, *_ in MT.walk(node))


STYLES = (("branches", "Branches"), ("filled", "Filled"), ("ink", "Ink"))   # the map's looks; Branches first

CSS = """<style>
/* the branch colours: the dataviz reference categorical palette in its fixed order (validated light and dark; every
   branch also carries its name, so no colour is read alone); a ninth branch on is grey, never a made-up hue */
.mm-edit{--mm-c1:#2a78d6;--mm-c2:#eb6834;--mm-c3:#1baf7a;--mm-c4:#eda100;--mm-c5:#e87ba4;--mm-c6:#008300;--mm-c7:#6250d6;
 --mm-c8:#e34948;--mm-c0:#868e96;--mm-ink:var(--fg,#1e1e1e);--mm-card:var(--card,#fff)}
@media (prefers-color-scheme: dark){:root:where(:not([data-theme="light"])) .mm-edit{--mm-c1:#3987e5;--mm-c2:#d95926;
 --mm-c3:#199e70;--mm-c4:#c98500;--mm-c5:#d55181;--mm-c6:#008300;--mm-c7:#9085e9;--mm-c8:#e66767}}
:root[data-theme="dark"] .mm-edit{--mm-c1:#3987e5;--mm-c2:#d95926;--mm-c3:#199e70;--mm-c4:#c98500;--mm-c5:#d55181;
 --mm-c6:#008300;--mm-c7:#9085e9;--mm-c8:#e66767}
.mm-b0{--br:var(--mm-c0)}.mm-b1{--br:var(--mm-c1)}.mm-b2{--br:var(--mm-c2)}.mm-b3{--br:var(--mm-c3)}.mm-b4{--br:var(--mm-c4)}
.mm-b5{--br:var(--mm-c5)}.mm-b6{--br:var(--mm-c6)}.mm-b7{--br:var(--mm-c7)}.mm-b8{--br:var(--mm-c8)}
.mm-style{display:inline-flex;margin:0 0 6px 4px;border:1px solid var(--line,#ced4da);border-radius:6px;overflow:hidden}
.mm-style button{font:500 11.5px system-ui,sans-serif;border:0;padding:2px 9px;cursor:pointer;background:var(--mm-card);color:var(--mut,#868e96)}
.mm-style button+button{border-left:1px solid var(--line,#ced4da)}.mm-style button[aria-pressed=true]{color:var(--mm-ink);background:var(--wash,#f1f3f5)}
/* Branches: a branch's card edged in its colour, its leaves in a thin line of it (no side bar: JL 261026, "左边这个东西
   … 太 AI 了") */
.mm-edit[data-style=branches] .mm-d1{border-color:var(--br);border-width:2px}
.mm-edit[data-style=branches] .mm-d2,.mm-edit[data-style=branches] .mm-d3{border-color:color-mix(in srgb,var(--br) 55%,var(--mm-card))}
/* Filled: a branch's card filled with its colour (white words; dark on yellow), its leaves tinted */
.mm-edit[data-style=filled] .mm-d1{background:var(--br);border-color:var(--br);color:#fff}
.mm-edit[data-style=filled] .mm-b4 .mm-d1{color:#0b0b0b}
.mm-edit[data-style=filled] .mm-d2,.mm-edit[data-style=filled] .mm-d3{background:color-mix(in srgb,var(--br) 13%,var(--mm-card));
 border-color:color-mix(in srgb,var(--br) 45%,var(--mm-card))}
.mm-edit[data-style=filled] .mm-d1 .mm-more,.mm-edit[data-style=filled] .mm-d1 .mm-open{color:inherit}
/* Ink: black and grey only, as the draft's §1 map */
.mm-edit[data-style=ink],.mm-edit[data-style=ink] .mm-row{--br:var(--mut,#868e96)}
/* a detail is its own panel: a soft box washed in its branch's colour, so it reads apart from the card's words */
.mm-edit .mm-detail{background:color-mix(in srgb,var(--br,#868e96) 8%,var(--mm-card));
 border:1px solid color-mix(in srgb,var(--br,#868e96) 22%,var(--mm-card));border-radius:7px;padding:6px 10px;margin:7px -4px 2px}
.mm-edit[data-style=ink] .mm-detail{background:var(--wash,#f1f3f5);border-color:var(--line,#ced4da)}
.mm-edit[data-style=filled] .mm-d1 .mm-detail{color:var(--mm-ink)}
/* the §1 Structure map's look (draft_steps.py PLAN_CSS): a node is a card, its children a column to its right */
.mm{position:relative;width:max-content;min-width:100%;box-sizing:border-box;padding:8px 4px}
.mm-wires{position:absolute;left:0;top:0;pointer-events:none;overflow:visible}
.mm-wires path{fill:none;stroke-width:1.5;stroke-opacity:.75}
/* siblings share one column (a row's box is `display:contents` in its parent's grid), so every child of a node starts
   at one x, as §1's paragraphs do; a node sits level with the middle of what hangs from it */
.mm>.mm-row,.mm-kids{display:grid;grid-template-columns:max-content max-content;gap:6px 56px;align-items:center}
.mm-kids>.mm-row{display:contents}.mm-add{grid-column:1}
.mm-node{position:relative;justify-self:start;max-width:420px;background:var(--card,#fff);border:1.5px solid var(--fg,#1e1e1e);
 border-radius:10px;padding:7px 12px;font-size:14px;line-height:1.4}
.mm-root{padding:12px 16px;font-size:17px;font-weight:600;background:#fff3bf;color:#1e1e1e}
.mm-d1{font-size:15px;font-weight:600}.mm-d2,.mm-d3{border-width:1px;border-color:var(--line,#ced4da);font-size:13.5px;white-space:nowrap;max-width:none}
.mm-node code{font-size:.92em}
.mm-open{margin-left:7px;text-decoration:none;font-size:13px;opacity:.75}.mm-open:hover{opacity:1}
.mm-more{border:0;background:none;padding:0 2px 0 6px;font:12px/1 system-ui,sans-serif;color:var(--mut,#868e96);cursor:pointer}
.mm-more[aria-expanded=true]{transform:rotate(90deg)}.mm-more[data-empty]{opacity:0}.mm-node:hover .mm-more[data-empty]{opacity:.5}
.mm-detail{margin:6px 0 2px;padding-top:6px;border-top:1px dashed var(--line,#ced4da);white-space:normal;
 width:max-content;max-width:520px;font-size:12.5px;font-weight:400;line-height:1.5;color:var(--fg,#1e1e1e)}
.mm-detail p{margin:0 0 4px}.mm-detail ul{margin:0 0 4px;padding-left:18px}.mm-detail img{display:block;max-width:420px;
 max-height:300px;border:1px solid var(--line,#ced4da);border-radius:6px;margin:4px 0;background:#fff}
.mm-pen{border:0;background:none;padding:0;font-size:12px;color:var(--mut,#868e96);cursor:pointer;opacity:.6}.mm-pen:hover{opacity:1}
.mm-detail textarea{display:block;width:460px;min-height:90px;font:12.5px/1.5 ui-monospace,Menlo,monospace}
.mm-edit{position:relative}.mm-msg{position:absolute;right:4px;top:0;font-size:12px;color:var(--mut,#868e96)}
.mm [data-edit]{outline:none;border-radius:3px;cursor:text}.mm [data-edit]:hover{background:var(--wash,#f1f3f5)}
.mm [data-edit]:focus{background:#fff3bf;color:#1e1e1e}.mm [data-edit].mm-bad{outline:1.5px dashed #e03131;outline-offset:2px}
.mm-err{color:#e03131;font-size:12px;font-weight:600}
.mm-node[draggable=true]{cursor:grab}.mm-node.mm-drop{box-shadow:0 -3px 0 var(--acc,#1971c2)}.mm-add.mm-drop .mm-plus{color:var(--acc,#1971c2);opacity:1}
.mm-plus{border:0;background:none;padding:0 4px;font:13px/1.4 system-ui,sans-serif;color:var(--mut,#868e96);opacity:.6;cursor:pointer}
.mm-plus:hover{opacity:1;color:var(--acc,#1971c2)}.mm-add{padding:1px 0}
/* the ＋ stays hidden until the mouse is over its node's row (as §1's); a touch screen always shows it */
@media(hover:hover){.mm-add{opacity:0;transition:opacity .12s}.mm-row:hover>.mm-kids>.mm-add,.mm-add:focus-within,.mm-add.mm-drop{opacity:1}}
@media(max-width:800px){.mm>.mm-row,.mm-kids{grid-template-columns:minmax(0,1fr);gap:4px}.mm-kids{padding-left:16px;border-left:2px solid var(--line,#ced4da)}
 .mm-wires{display:none}.mm{width:auto}.mm-d2,.mm-d3{white-space:normal}}
</style>"""

# the wires drawn after layout, curved as the draft's §1 map draws them (draft_steps.py PLAN_JS; JL 261026: "还是那种曲线
# 型的"): from a node's right side to each child's left side, each end at the card's first line, so a card opened to
# its detail is still met at its words, not halfway down (JL 261026, of the opened card: "它那个比较奇怪"); each wire in
# its branch's colour
WIRES = """<script>
(function(){if(window.__mmWires)return;window.__mmWires=1;
 function ink(el){var c=getComputedStyle(el).getPropertyValue('--br').trim();return c||getComputedStyle(el).getPropertyValue('--mut').trim()||'#868e96';}
 function at(r,o){return r.top+Math.min(r.height/2,18)-o.top;}            /* the card's first line, opened or not */
 function wire(a,b,o){var p=a.getBoundingClientRect(),q=b.getBoundingClientRect();
  var x1=p.right-o.left,y1=at(p,o),x2=q.left-o.left-4,y2=at(q,o),m=(x1+x2)/2;
  return '<path stroke="'+ink(b)+'" d="M'+x1+','+y1+' C'+m+','+y1+' '+m+','+y2+' '+x2+','+y2+'"/>';}
 function draw(){document.querySelectorAll('.mm').forEach(function(m){var svg=m.querySelector('.mm-wires');
  if(!m.offsetParent||getComputedStyle(svg).display==='none')return;var o=m.getBoundingClientRect(),d='';
  svg.setAttribute('width',o.width);svg.setAttribute('height',o.height);
  m.querySelectorAll('.mm-row').forEach(function(r){var n=r.querySelector(':scope>.mm-node');
   r.querySelectorAll(':scope>.mm-kids>.mm-row>.mm-node').forEach(function(c){d+=wire(n,c,o);});});
  svg.innerHTML=d;});}
 /* the style switch: Branches · Filled · Ink, remembered in this browser */
 var KEY='workbench.mindmap.style.v1';
 function look(h,st){h.dataset.style=st;h.querySelectorAll('.mm-style [data-mm-style]').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.mmStyle===st));});}
 function looks(){var st=null;try{st=localStorage.getItem(KEY);}catch(e){}if(!st)return;
  document.querySelectorAll('.mm-edit').forEach(function(h){if(h.querySelector('[data-mm-style="'+st+'"]'))look(h,st);});}
 window.mmLooks=looks;looks();document.addEventListener('DOMContentLoaded',function(){looks();draw();});   /* maps below this script too */
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.mm-style [data-mm-style]');if(!b)return;
  e.preventDefault();try{localStorage.setItem(KEY,b.dataset.mmStyle);}catch(x){}
  document.querySelectorAll('.mm-edit').forEach(function(h){look(h,b.dataset.mmStyle);});draw();});
 /* ▸: a card's detail opens below its words; an empty one (on an editable map) opens straight into its editor */
 window.mmOpen=window.mmOpen||new Set();
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.mm .mm-more');if(!b)return;e.preventDefault();e.stopPropagation();
  var d=b.parentNode.querySelector(':scope>.mm-detail'),on=d.hidden,id=b.closest('.mm-row').dataset.id;d.hidden=!on;b.setAttribute('aria-expanded',String(on));
  if(on)window.mmOpen.add(id);else window.mmOpen.delete(id);
  if(on&&b.dataset.empty){var pen=d.querySelector('.mm-pen');if(pen)pen.click();}draw();});
 window.mmDraw=draw;window.addEventListener('resize',draw);window.addEventListener('load',draw);setTimeout(draw,60);
 document.addEventListener('toggle',function(){setTimeout(draw,0);},true);
 document.addEventListener('input',function(e){if(e.target.closest&&e.target.closest('.mm'))draw();});
})();
</script>"""

EDIT = """<script>
(function(){if(window.__mmEdit)return;window.__mmEdit=1;
 function host(el){return el.closest('.mm-edit');}
 function say(el,t,bad){var m=host(el).querySelector('.mm-msg');m.textContent=t||'';m.style.color=bad?'#c92a2a':'';
  if(t&&!bad)setTimeout(function(){if(m.textContent===t)m.textContent='';},1800);}
 function bad(el,msg){var x=el.parentNode.querySelector(':scope > .mm-err');if(!x){x=document.createElement('span');x.className='mm-err';el.after(x);}
  x.textContent=' not saved: '+msg;el.classList.add('mm-bad');say(el,'not saved: '+msg,true);}
 function words(el){return el.innerText.replace(/\\s+/g,' ').trim();}
 /* the map again from the server, after a node was added, taken out or moved */
 function refresh(h){fetch(location.href,{credentials:'same-origin'}).then(function(r){return r.text();}).then(function(t){
  var n=new DOMParser().parseFromString(t,'text/html').querySelector('.mm-edit[data-file="'+h.dataset.file+'"]');
  if(n)h.innerHTML=n.innerHTML;if(window.mmLooks)window.mmLooks();(window.mmOpen||new Set()).forEach(function(id){var r=h.querySelector('.mm-row[data-id="'+id+'"]>.mm-node');
   if(r&&r.querySelector(':scope>.mm-detail')){r.querySelector(':scope>.mm-detail').hidden=false;r.querySelector(':scope>.mm-more').setAttribute('aria-expanded','true');}});
  if(window.mmDraw)window.mmDraw();});}
 /* ✎: the detail as its Markdown, in a box; leaving the box saves it */
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.mm-edit .mm-pen');if(!b)return;e.preventDefault();
  var d=b.closest('.mm-detail'),t=document.createElement('textarea');t.value=b.dataset.raw;t.dataset.raw=b.dataset.raw;t.className='mm-notebox';
  d.innerHTML='';d.appendChild(t);t.focus();if(window.mmDraw)window.mmDraw();});
 document.addEventListener('focusout',function(e){var t=e.target.closest&&e.target.closest('.mm-edit .mm-notebox');if(!t)return;
  var h=host(t),row=t.closest('.mm-row'),v=t.value.replace(/\s+$/,'');
  if(v===t.dataset.raw){refresh(h);return;}
  post(t,{what:'note',id:row.dataset.id,was:t.dataset.raw,value:v}).then(function(){refresh(h);})
   .catch(function(err){if(err.reload)refresh(h);else bad(t,err.message);});});
 function post(el,body){var h=host(el);body.file=h.dataset.file;say(el,'…');
  return fetch('/_board/mindmap',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   .then(function(r){return r.json();}).then(function(j){if(!j.ok){var e=new Error(j.err||'not saved');e.reload=!!j.reload;throw e;}
    say(el,'saved');return j;});}
 function newnode(kids,before,parent,after){var r=document.createElement('div');r.className='mm-row mm-new';r.dataset.parent=parent;r.dataset.after=after||'';
  r.innerHTML='<div class="mm-node mm-d3"><span class=mm-t data-edit=new contenteditable=plaintext-only spellcheck=false></span></div><div class=mm-kids></div>';
  kids.insertBefore(r,before);r.querySelector('[data-edit]').focus();if(window.mmDraw)window.mmDraw();}
 /* ＋: a new node last under this one */
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.mm-edit [data-add]');if(!b)return;e.preventDefault();
  var row=b.closest('.mm-row'),kids=row.querySelector(':scope>.mm-kids'),last=kids.querySelectorAll(':scope>.mm-row[data-id]');
  newnode(kids,b.closest('.mm-add'),row.dataset.id,last.length?last[last.length-1].dataset.id:'');});
 document.addEventListener('focusin',function(e){var el=e.target.closest&&e.target.closest('.mm-edit [data-edit=text]');if(!el||el._html!=null)return;
  el._html=el.innerHTML;if(!el.classList.contains('mm-bad'))el.textContent=el.dataset.raw;});
 document.addEventListener('keydown',function(e){var el=e.target.closest&&e.target.closest('.mm-edit [data-edit]');if(!el)return;
  if(e.key==='Escape'){e.preventDefault();if(el.dataset.edit==='text')el.textContent=el.dataset.raw;else el.textContent='';el.blur();return;}
  if(e.key!=='Enter')return;e.preventDefault();var row=el.closest('.mm-row');
  /* Enter: a new node below this one, under the same parent */
  if(words(el)&&row.parentNode.closest('.mm-row')){var par=row.parentNode.closest('.mm-row');el.blur();
   newnode(row.parentNode,row.nextSibling,par.dataset.id,row.dataset.id||'');}else el.blur();});
 document.addEventListener('focusout',function(e){var el=e.target.closest&&e.target.closest('.mm-edit [data-edit]');if(!el)return;
  var h=host(el),row=el.closest('.mm-row'),v=words(el);
  if(el.dataset.edit==='new'){if(!v){row.remove();if(window.mmDraw)window.mmDraw();return;}
   post(el,{what:'add',parent:row.dataset.parent,after:row.dataset.after,value:v}).then(function(){refresh(h);})
    .catch(function(err){if(err.reload)refresh(h);else bad(el,err.message);});return;}
  var was=el.dataset.raw,html=el._html;el._html=null;
  if(v===was){el.innerHTML=html!=null?html:el.innerHTML;return;}
  var body={what:v?'text':'drop',id:row.dataset.id,was:was,value:v};
  post(el,body).then(function(j){if(body.what==='drop'){refresh(h);return;}el.dataset.raw=v;el.innerHTML=j.html!=null?j.html:v;
   if(window.mmDraw)window.mmDraw();}).catch(function(err){if(err.reload)refresh(h);else bad(el,err.message);});});
 /* a node dragged onto another goes before it; onto a ＋, last under that node */
 var drag=null;
 document.addEventListener('dragstart',function(e){var n=e.target.closest&&e.target.closest('.mm-edit .mm-node[draggable=true]');if(!n)return;
  drag=n.closest('.mm-row');e.dataTransfer.effectAllowed='move';e.dataTransfer.setData('text/plain',drag.dataset.id);});
 function spot(e){return drag&&e.target.closest&&(e.target.closest('.mm-edit .mm-node')||e.target.closest('.mm-edit .mm-add'));}
 document.addEventListener('dragover',function(e){var t=spot(e);document.querySelectorAll('.mm-drop').forEach(function(x){x.classList.remove('mm-drop');});
  if(!t||drag.contains(t)||host(t)!==host(drag)||t.classList.contains('mm-root'))return;e.preventDefault();t.classList.add('mm-drop');});
 document.addEventListener('drop',function(e){var t=spot(e);document.querySelectorAll('.mm-drop').forEach(function(x){x.classList.remove('mm-drop');});
  if(!t||drag.contains(t))return;e.preventDefault();var h=host(drag),body={what:'move',id:drag.dataset.id};
  if(t.classList.contains('mm-add'))body.parent=t.closest('.mm-row').dataset.id;else body.before=t.closest('.mm-row').dataset.id;drag=null;
  post(t,body).then(function(){refresh(h);}).catch(function(err){say(t,'not saved: '+err.message,true);if(err.reload)refresh(h);});});
 document.addEventListener('dragend',function(){drag=null;});
})();
</script>"""
