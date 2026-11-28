"""A theme Block's 🧩 Elements section, the first section of its Block UI · Job UI · Task UI · Run UI view (JL 261118:
"change the Block UI to Block UI + element, so we have a Element Section at the first ... and we can understand what
we will need"). It lists the parts a page at that level is made of, one left tab each: what it shows, the folder it
reads, the code that draws it, its rules, then the theme's example page live with that part outlined. Each tab carries
marks and cards (tab_cards), so a part's design can be commented on and checked where it is shown.

Source: the theme Block's `delivery/page-spec/<level>-elements.md`: `# <type>` with `example: <path>` starts one type of page at the
level (JL 261118: "Elements - Block UI Type 1, Elements - Block UI Type 2"), each its own 🧩 Elements section; `## ` names a view (Page frame, Overview,
Plan + Results, ..., Around the Work), `### ` one part in it; each view is its own short list of left tabs.

    ## Plan + Results
    ### Section bar
    show: details.band-sec          a CSS selector on the example page; only the part is shown
    text: How it ran                 only a match holding these words (optional)
    list: yes                        every match, not only the first (optional)
    page: examples/.../runs/r02_x  another example page for this part, a path as on a `ui-run:` line (optional)
    view: standing                   the example page's view (`group=`), or a query (`section=timeline`)
    folder: a band of Jobs (face `bands:`)
    code: workbench/page/block_index_page/focus_styles_bands.py band_sec
    A plain line and `- ` rules: kept in the file as design notes, not shown on the page.
"""
from __future__ import annotations

import re
from pathlib import Path

from live import frame
from live.focus_base import inside
from live.ui_parts import PB_CSS, PB_JS, _side_tabs
from live.page_spec import spec_dir

FIELDS = ("show", "text", "list", "page", "view", "folder", "code")



def parse_types(text: str) -> list:
    """[(type, example, groups)]: each `# <type>` with an `example:` line starts a type; a file with none is one
    type with no name, shown on the level's first example page."""
    chunks = re.split(r"(?m)^#\s+(.+?)\s*$", text)
    typed = [(chunks[i], chunks[i + 1]) for i in range(1, len(chunks), 2)
             if re.search(r"(?m)^example:\s*\S", chunks[i + 1])]
    if not typed:
        return [("", "", parse(text))]
    out = []
    for name, body in typed:
        example = re.search(r"(?m)^example:\s*(.+?)\s*$", body)[1]
        out.append((name, example, parse(body)))
    return out


def parse(text: str) -> list:
    """[(view, [{name, show, view, ...}])]: `## ` a view and `### ` its parts; a file with no `### ` reads each `## `
    as a part of one unnamed view."""
    nested = re.search(r"(?m)^###\s", text) is not None
    groups = [] if nested else [("", [])]
    for line in text.splitlines():
        head = re.match(r"^(#{2,3})\s+(.+?)\s*$", line)
        if head and nested and head[1] == "##":
            groups.append((head[2], []))
            continue
        if head:
            if not groups:
                groups.append(("", []))
            groups[-1][1].append({"name": head[2], "words": [], "rules": []})
            continue
        els = groups[-1][1] if groups else []
        if not els or not line.strip():
            continue
        topic = re.match(r"^topic:\s*(.+?)\s*$", line)
        if topic:
            els[-1].setdefault("topics", []).append(topic[1])
            continue
        field = re.match(r"^(%s):\s*(.+?)\s*$" % "|".join(FIELDS), line)
        if field:
            els[-1][field[1]] = field[2]
        elif re.match(r"^\s*[-*]\s+", line):
            els[-1]["rules"].append(re.sub(r"^\s*[-*]\s+", "", line))
        else:
            els[-1]["words"].append(line.strip())
    return [(g, els) for g, els in groups if els]


def _example(el: dict, example: str, folder: Path, root: Path) -> str:
    """The page this part is shown on: its own `page:` when it names one here, else the level's first example."""
    if not el.get("page"):
        return example
    from urllib.parse import urlencode
    from live.focus_ui import ui_base
    page = ui_base(el["page"], folder, root)
    return (frame.ROUTE + "?" + urlencode({"path": page.relative_to(root.resolve()).as_posix(), "layout": "focus"})
            if page is not None else example)


def _panel(el: dict, example: str) -> str:
    """Only the part itself, live (JL 261118: the words about it are the design file's, not the page's)."""
    if not example:
        return ""
    topics = ""
    if el.get("topics"):                          # a Section: the topics it holds here, fixed by the view or the page's own
        rows = []
        for line in el["topics"]:
            bits = [b.strip() for b in line.split(" · ")]
            kind = bits.pop() if len(bits) > 2 and bits[-1] in ("fixed", "free") else ""
            num = bits.pop(0) if len(bits) > 1 and bits[0].isdigit() else ""
            rows.append(f'<li><span class=el-tn>Topic {frame.esc(num)}</span> {frame.esc(" · ".join(bits))}'
                        + (f' <small class="el-tk el-{kind}">{kind}</small>' if kind else "") + "</li>")
        topics = "<ul class=el-topics>" + "".join(rows) + "</ul>"
    view = el.get("view") or ""
    href = example + (f"&{view}" if "=" in view else f"&section=report&group={view}" if view else "")
    return topics + (f'<iframe class="ui-page el-live" title="{frame.esc(el["name"])}" data-src="{frame.esc(href)}" '
            f'data-show="{frame.esc(el.get("show") or "")}" data-text="{frame.esc(el.get("text") or "")}"'
            f'{" data-list=1" if el.get("list") else ""}></iframe>')


def elements_section(folder: Path, root: Path, key: str, example: str) -> list:
    """[("🧩 Elements · <type>", "", body)], one per type of page at this level; [] when the theme Block has no
    `ui/<key>-elements.md`."""
    path = spec_dir(folder) / f"{key}-elements.md" if folder and key else None
    if path is None or not inside(path, root) or not path.is_file():
        return []
    from live.tab_cards import slug
    out = []
    for t, (kind, ref, groups) in enumerate(parse_types(path.read_text(encoding="utf-8"))):
        page = _example({"page": ref}, example, folder, root) if ref else example
        body = ""
        for n, (view, els) in enumerate(groups):
            prefix = f"elements.{key}" + (f".{slug(kind)}" if kind else "") + (f".{slug(view)}" if view else "")
            body += (f"<h3 class=pb-group>{frame.esc(view)}</h3>" if view else "") + _side_tabs(
                f"fE{key[:1]}{t}x{n}x", [(el["name"], "") for el in els],
                [_panel(el, _example(el, page, folder, root)) for el in els], cards=(folder, root, prefix))
        if body:
            out.append(("🧩 Elements" + (f" · {kind}" if kind else ""), "", PB_CSS + body + PB_JS + ASSETS))
    return out


# the example page shows only the part: each match kept inside bare copies of its parents (so the page's CSS still
# applies), the rest of the page removed, its styles and listeners kept, the frame as tall as the part
ASSETS = """<style>.el-topics{list-style:none;padding:0;margin:2px 0 10px;font-size:14px}.el-topics li{padding:3px 0}
.el-tn{color:var(--muted,#6b7280);display:inline-block;min-width:62px}.el-tk{font-size:11.5px;padding:0 6px;border-radius:8px;margin-left:6px}
.el-fixed{background:#e7f0fb;color:#1864ab}.el-free{background:#fff4e6;color:#c2410c}.el-found{font-size:13.5px;margin:4px 0 8px}
iframe.el-live{width:100%;height:120px;border:1px solid var(--border,#e5e7eb);border-radius:8px}</style><script>
(function(){if(window.__elLive)return;window.__elLive=1;
function block(el,d){var sm=el.closest&&el.closest('summary');if(sm&&sm.parentNode.tagName==='DETAILS')return sm.parentNode;if(!/^H[234]$/.test(el.tagName))return el;var pa=el.parentNode;if(pa&&pa.tagName==='SECTION'&&pa.firstElementChild===el)return pa;var w=d.createElement('div'),n=el;el.parentNode.insertBefore(w,el);while(n&&!(n!==el&&n.tagName===el.tagName)){var nx=n.nextElementSibling;w.appendChild(n);n=nx;}return w;}
function shell(el,d){var cur=el;el.hidden=false;for(var p=el.parentElement;p&&p.tagName!=='BODY';p=p.parentElement){
 var c=p.tagName==='DETAILS'?d.createElement('div'):p.cloneNode(false);if(p.tagName==='DETAILS')c.className=p.className;c.removeAttribute('hidden');c.removeAttribute('id');c.appendChild(cur);cur=c;}[].slice.call(el.querySelectorAll('iframe[data-src]:not([src])')).forEach(function(x){x.src=x.dataset.src;});return cur;}
function show(f){try{var d=f.contentDocument,s=f.dataset.show;if(!d||!d.body||!s)return;f.style.display='';
 var all=[].slice.call(d.querySelectorAll(s)),w=f.dataset.text;
 if(w)all=all.filter(function(x){return x.textContent.indexOf(w)>=0;});
 if(!f.dataset.list)all=all.slice(0,1);
 var old=f.parentNode.querySelector('.el-found');if(old)old.remove();
 if(!all.length){var n=document.createElement('p');n.className='el-found mut';n.textContent='Not on the example page.';
  f.parentNode.insertBefore(n,f);f.style.display='none';return;}
 var keep=[].slice.call(d.body.querySelectorAll('style,link[rel=stylesheet]')),parts=all.map(function(x){var el=block(x,d),pa=el.parentElement,c;for(var q=pa;q;q=q.parentElement){if(q.tagName==='DETAILS')q.open=true;}el.style.outline='2px solid #e03131';el.style.outlineOffset='3px';el.style.borderRadius='6px';if(pa&&pa.tagName!=='BODY'&&pa.tagName!=='MAIN'&&!/focus-page|focus-card|focus-content|work-section-group/.test(pa.className)&&pa.getBoundingClientRect().height<420)c=pa;else{c=d.createElement('div');var pv=el.previousElementSibling,nx=el.nextElementSibling;while(pv&&/^(SCRIPT|STYLE|DIALOG|TEMPLATE)$/.test(pv.tagName))pv=pv.previousElementSibling;while(nx&&/^(SCRIPT|STYLE|DIALOG|TEMPLATE)$/.test(nx.tagName))nx=nx.nextElementSibling;pa.insertBefore(c,el);if(pv)c.appendChild(pv);c.appendChild(el);if(nx)c.appendChild(nx);}return shell(c,d);});
 [].slice.call(d.body.children).forEach(function(c){if(c.tagName!=='SCRIPT'&&c.tagName!=='DIALOG'&&c.tagName!=='TEMPLATE')c.remove();});
 var box=d.createElement('div');box.style.cssText='padding:14px 18px';keep.forEach(function(x){box.appendChild(x);});
 parts.forEach(function(x){box.appendChild(x);});d.body.appendChild(box);
 var fit=function(){f.style.height=Math.min(Math.max(d.documentElement.scrollHeight,60),900)+'px';};fit();
 new ResizeObserver(fit).observe(box);}catch(e){}}
setInterval(function(){document.querySelectorAll('iframe.el-live[src]').forEach(function(f){try{var d=f.contentDocument;
 if(!d||d.readyState!=='complete'||d.__elDone||d.location.href==='about:blank')return;d.__elDone=1;setTimeout(function(){show(f);},150);}catch(e){}});},500);
})();</script>"""
