"""The 🔎 Findings band of a work page: a Block's 🗄️ Data stores, its 🔢 Values, 🖼️ Displays and 🧩 generated Fn
code, as rows under the Project's and the Block's Review Content, and each part alone for its pop-out."""
from __future__ import annotations

import re
import traceback
from pathlib import Path
from urllib.parse import urlencode

import yaml

from live import frame
from live.work_files import python_preview
from live.ui_parts import PB_JS, _side_tabs
from live.focus_page import (
    FIT_FRAME_JS,
    OPEN_HASH_JS,
    display_rows,
    display_sections,
    document,
    inside,
    map_sections,
    numbered,
    page_level,
    page_url,
    side_css,
    task_values,
    value_sections,
)
from live.project_face import _dotted, _load


def find_part_document(folder: Path, root: Path, key: str) -> str:
    """One Findings part alone, for a row opened in place (the Project's and a Block's 🔎 Findings): a Block's 🗄️ Data
    stores, its or a Job's 🔢 Values tabs, or one display Task's preview, each the same panel its Findings view draws."""
    if key == "find-data":
        body = data_section(folder, root)[0]
    elif key == "find-values":
        body = "".join(h for _, h, _ in value_sections(folder, root)) or '<p class=mut>No values here.</p>'
    elif key == "find-fn":
        body = "".join(h for _, h, _ in fn_sections(folder, root)) or '<p class=mut>No generated Fn here.</p>'
    else:
        try:
            from live.board_results import evidence_body
            body = evidence_body(folder, root)[2]
        except Exception:
            traceback.print_exc()                              # in the server log, not hidden
            body = '<p class=mut>No preview.</p>'
    fixed = '.find-alone iframe,.find-alone embed,.find-alone object{height:620px!important;max-height:none!important}' \
        if key == "find-display" else ''                    # a preview's own height, not the frame's (it sets the frame's)
    return document(f"{folder.name} · {key}", '<base target="_top"><style>body{margin:0;background:transparent}.find-alone{padding:2px 0}'
                    + fixed + '</style>'
                    '<main class="focus-page find-alone"><div class="focus-content">' + side_css() + body + PB_JS + '</div></main>')


def data_stores(block: Path) -> list:
    """The stores a Block reads or writes, from the ```yaml block in its board.md whose top key is `data:`, so a reader
    sees where the data is. A person writes the rows; a count is never typed but points at a Result (`file:` under the
    Block, a JSON or YAML file, and a dotted `key:`), so it stays live as haipipe-evidence VALUEs do. None when the
    block is there but does not parse, [] when there is none."""
    face = block / "board.md"
    text = face.read_text(encoding="utf-8", errors="replace") if face.is_file() else ""
    for body in re.findall(r"(?ms)^```ya?ml[ \t]*\n(.*?)^```", text):
        if re.match(r"\s*data:", body):
            try:
                rows = (yaml.safe_load(body) or {}).get("data") or []
            except yaml.YAMLError:
                traceback.print_exc()                          # in the server log, not hidden
                return None
            return [r for r in rows if isinstance(r, dict) and r.get("name")]
    return []


def store_count(block: Path, ref) -> str:
    """'67 tables' from {file, key, label}: the value read from the Result now; '' when it cannot be read."""
    if not isinstance(ref, dict) or not ref.get("file") or not ref.get("key"):
        return ""
    path = (block / str(ref["file"])).resolve()
    if block.resolve() not in path.parents:
        return ""
    doc = _dotted(_load(path), ref["key"])
    if doc is None:
        return ""
    value = f"{doc:,}" if isinstance(doc, int) else str(doc)
    return (value + " " + str(ref.get("label") or "")).strip()


DATA_CSS = """<style>
.ds-table{width:100%;border-collapse:collapse;font-size:13.5px;line-height:1.45;table-layout:fixed}
.ds-table th{text-align:left;font-weight:500;color:var(--muted);font-size:12px;padding:6px 10px;border-bottom:1px solid var(--line)}
.ds-table td{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top;overflow-wrap:anywhere}
.ds-table td:first-child b{display:block}
.ds-table td:first-child code{display:block;margin-top:3px;font-weight:400;color:var(--muted);font-size:12px;overflow-wrap:anywhere}
.ds-table code{font-size:12.5px}.ds-table .n span{display:block}
@media(max-width:700px){.ds-table thead{display:none}.ds-table tr{display:block;padding:8px 0;border-bottom:1px solid var(--line)}
  .ds-table td{display:block;border:0;padding:1px 0}}
</style>"""


def data_section(block: Path, root: Path) -> tuple:
    """(html, state word) of 🗄️ Data: one row per store, its name, where it is, what it holds, how many (read from its
    Result), who can read it."""
    rows = data_stores(block)
    if rows is None:
        return '<p class=mut>The <code>data:</code> block in board.md does not parse.</p>', ""
    if not rows:
        return "", ""                                  # no stores: the section is not drawn (JL 261114)
    out = []
    for r in rows:
        name = frame.esc(str(r["name"]))
        link = str(r.get("link") or "")
        if link.startswith(("http://", "https://", "/")):
            name = f'<a href="{frame.esc(link)}" target=_blank rel=noopener>{name} ↗</a>'
        counts = r.get("count") or []
        counts = [counts] if isinstance(counts, dict) else counts
        many = "".join(f"<span>{frame.esc(p)}</span>" for c in (store_count(block, c) for c in counts) if c
                       for p in c.split(" · "))                  # one count per line, so the column stays narrow
        where = str(r.get("where") or "")
        out.append(f'<tr><td><b>{name}</b>' + (f'<code>{frame.esc(where)}</code>' if where else '') + '</td>'
                   f'<td>{frame.esc(str(r.get("holds") or ""))}</td><td class=n>{many}</td>'
                   f'<td>{frame.esc(str(r.get("access") or ""))}</td></tr>')
    return (DATA_CSS + '<table class=ds-table><colgroup><col style="width:30%"><col style="width:36%">'
            '<col style="width:17%"><col style="width:17%"></colgroup><thead><tr><th>Store</th><th>What it holds</th>'
            '<th>How many</th><th>Who can read it</th></tr></thead><tbody>' + "".join(out) + '</tbody></table>'), ""


VERSION_DIR = re.compile(r"^v[A-Za-z0-9]*?(\d{6})$")       # a generated Fn's version folder, vDemoSet261111


def fn_file(task: Path, root: Path):
    """The generated Fn a Task makes: the code/haifn/…/<FnName>.py its face's `output:` (else `develops:`) names. When a
    newer version folder (v<name><yymmdd>/) under code/haifn/ holds a file of the same name, that one; None when none."""
    face = task / f"{task.name}.md"
    text = face.read_text(encoding="utf-8", errors="replace") if face.is_file() else ""
    named = None
    for key in ("output", "develops"):
        m = re.search(rf"(?m)^{key}:.*?\b(code/haifn/[\w./-]+?\.py)\b", text)
        if m:
            named = m.group(1)
            break
    if not named:
        return None
    base = root / "code" / "haifn"
    stem = Path(named).name
    versioned = []
    for p in base.rglob(stem) if base.is_dir() else []:
        dates = [VERSION_DIR.match(d).group(1) for d in p.relative_to(base).parts[:-1] if VERSION_DIR.match(d)]
        if dates:
            versioned.append((dates[-1], p.stat().st_mtime, p))
    if versioned:
        return max(versioned)[2]
    path = root / named
    return path if path.is_file() and inside(path, root) else None


FN_CSS = """<style>
.fn-doc{white-space:pre-wrap;font-size:13.5px;line-height:1.5;margin:0 0 10px;overflow-wrap:anywhere}
.fn-code{margin:6px 0 10px;border:1px solid var(--line);border-radius:8px}
.fn-code>summary{cursor:pointer;padding:7px 10px;font-weight:600;font-size:13px}
.fn-code pre{margin:0;padding:10px 12px;border-top:1px solid var(--line);overflow:auto;font-size:12.5px;
  line-height:1.45;max-height:70vh}
.fn-code .py-keyword{color:#8250df}.fn-code .py-function{color:#0550ae;font-weight:600}.fn-code .py-builtin{color:#6639ba}
.fn-code .py-string{color:#0a7a3a}.fn-code .py-number{color:#b35900}.fn-code .py-comment{color:var(--muted);font-style:italic}
@media(prefers-color-scheme:dark){.fn-code .py-keyword{color:#d2a8ff}.fn-code .py-function{color:#79c0ff}
  .fn-code .py-builtin{color:#d2a8ff}.fn-code .py-string{color:#7ee787}.fn-code .py-number{color:#ffa657}}
</style>"""


def fn_panel(task: Path, path: Path, root: Path) -> str:
    """One generated Fn, read-only: its docstring (what it is, generated from what), then its module-level settings,
    then each function, each part folded; then that Fn's own map, when a Run in its Block drew one
    (result/maps/<FnName>.mindmap.md)."""
    import ast
    code = path.read_text(encoding="utf-8", errors="replace")
    lines = code.splitlines(keepends=True)
    docs, settings, funcs = [], [], []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        tree = None
    for node in tree.body if tree else []:
        chunk = "".join(lines[node.lineno - 1: node.end_lineno])
        if isinstance(node, ast.Expr) and isinstance(getattr(node, "value", None), ast.Constant) and isinstance(node.value.value, str):
            docs.append(node.value.value.strip())
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            funcs.append((node.name, chunk))
        elif not isinstance(node, (ast.Import, ast.ImportFrom)):
            settings.append(chunk)
    fold = lambda title, body: (f'<details class=fn-code><summary>{frame.esc(title)}</summary>'
                                + python_preview(body) + '</details>')
    html = (f'<div class=find-verbs><code>{frame.esc(frame.rel(path, root))}</code></div>'
            + "".join(f'<p class=fn-doc>{frame.esc(d)}</p>' for d in docs))
    if settings:
        html += fold("Settings", "".join(settings))
    html += "".join(fold(name, body) for name, body in funcs)
    if tree is None:
        html += fold("Code", code)
    name = path.stem
    block = task.parent.parent
    maps = sorted(block.glob(f"j*/t*/runs/*/result/maps/{name}.mindmap.md"))
    if maps:
        href = frame.ROUTE + "?" + urlencode({"path": frame.rel(maps[-1], root), "view": "focus-map"})
        html += (f'<div class=find-verbs>{frame.pop(href, name + " · mind map", "Enlarge map ↗")}</div>'
                 f'<iframe class=find-map loading=lazy title="{frame.esc(name)} mind map" src="{frame.esc(href)}&amp;fit=1" '
                 'onload="window.fitMap&&fitMap(this)"></iframe>')
    return html


def fn_found(folder: Path, root: Path) -> list:
    """[(job, [(task, fn file)])] of the Tasks at this page or below whose face's `output:` (else `develops:`) names a
    generated Fn under code/haifn/; Jobs with none left out."""
    level = page_level(folder)
    jobs = ([j for j in frame.children(folder, "Block") if inside(j, root)] if level == "Block"
            else [folder] if level == "Job" else [])
    if level == "Task":
        p = fn_file(folder, root)
        return [(folder.parent, [(folder, p)])] if p else []
    out = []
    for j in jobs:
        found = [(t, p) for t in frame.children(j, "Job") if inside(t, root) and (p := fn_file(t, root))]
        if found:
            out.append((j, found))
    return out


def fn_sections(folder: Path, root: Path) -> list:
    """[(title, html, word)] of 🧩 Fn: the generated Fn code a Task makes (its face's `output:` names a file under
    code/haifn/), one side tab per Fn; a Block one side tab per Job that makes Fns, its Fns as tabs inside."""
    groups = fn_found(folder, root)
    if not groups:
        return []
    tabset = lambda eid, found: _side_tabs(eid, [(p.stem, "") for _, p in found], [fn_panel(t, p, root) for t, p in found])
    if page_level(folder) == "Block":
        body = _side_tabs("fFbx", [(j.name, "") for j, _ in groups],
                          [tabset(f"fF{k}x", f) for k, (_, f) in enumerate(groups)])
    else:
        body = tabset("fF" + folder.name[:3] + "x", groups[0][1] if len(groups) == 1 else [x for _, f in groups for x in f])
    return [("🧩 Fn", FN_CSS + body + FIT_FRAME_JS, "")]   # no count: the tabs show how many


def work_findings(folder: Path, root: Path) -> str:
    """A work Block's, Job's or Task's Findings. A Block leads with 🗄️ Data, where its data is (`data:` in board.md);
    then, at every level, 🔢 Values and 🖼️ Displays, drawn
    as the paper Board's Evidence › Values and Displays. Values is one section for the page, from its value
    Jobs' newest tables.json with the numbers its values.json lets the text quote (haipipe-evidence); Displays its
    display Tasks' preview.pdf (haipipe-display). A section with nothing in it is not drawn (JL 261114: "if this is
    empty, why you still list them here"), and the rest renumber. Last, 🧠 Maps, only when the page or its
    Tasks' newest Runs drew maps (result/maps/); Studio topics are Around the Work's Studio, not Findings."""
    level = page_level(folder)
    vals = task_values(folder, root) if level == "Task" else value_sections(folder, root)
    disp = display_sections(folder, root)
    v_body = "".join(h for _, h, _ in vals)
    secs = ([("🔢 Values", vals[0][2], v_body, "", None, "find-values")] if v_body else []) \
        + ([("🖼️ Displays", disp[0][2], disp[0][1], "", None, "find-displays")] if disp else [])
    if level == "Block":                         # where the data is first, before its numbers
        html, word = data_section(folder, root)
        if html:
            secs.insert(0, ("🗄️ Data", word, html, "", None, "find-data"))
    # then its maps, only when it has some: Data, then displays, then Maps
    secs += [(t, w, h, "") for t, h, w in map_sections(folder, root)]
    # last, the generated Fn code its Tasks make, so a reader can open the code a Result came from
    secs += [(t, w, h, "", None, "find-fn") for t, h, w in fn_sections(folder, root)]
    if not secs:
        return '<p class=mut>No findings here.</p>'
    return side_css() + numbered(secs) + PB_JS + OPEN_HASH_JS


def findings_parts(block: Path, root: Path) -> str:
    """A work Block's Findings parts as child rows under its Project Findings row, the way Review Content lists its
    Jobs: 🗄️ Data (its `data:` stores), 🔢 Values (its value tabs), 🖼️ Displays, 🧩 Fn, each opening that part of the
    Block's Findings view. Only the parts it has; a row carries no count (AGENTS.md § Page words): opening it shows how many."""
    parts = []
    level = page_level(block)                        # a Block, or one Job (its own page: its Values, its Displays)
    stores = (data_stores(block) or []) if level == "Block" else []
    if stores:
        parts.append(("🗄️", "Data", "", "find-data"))
    try:
        from live import board_evidence as be
        jobs = [j for j in (frame.children(block, "Block") if level == "Block" else [block]) if inside(j, root)
                and next(j.glob("t[0-9]*_*/runs/r[0-9]*/result/tables.json"), None)]
    except Exception:
        traceback.print_exc()                                  # in the server log, not hidden
        jobs, be = [], None
    tabs = 0
    for j in jobs:
        try:
            tabs += len(be.value_tabs(j, root))
        except (KeyError, TypeError):                          # a tables.json that is no value table (a Source
            pass                                               # Run's list of table names): not a Values part
        except Exception:
            traceback.print_exc()                              # in the server log, not hidden
    if tabs:
        parts.append(("🔢", "Values", "", "find-values"))
    disp = display_sections(block, root)
    if disp:
        parts.append(("🖼️", "Displays", "", "find-displays"))
    fns = sum(len(f) for _, f in fn_found(block, root))   # the generated Fn code its Tasks make
    if fns:
        parts.append(("🧩", "Fn", "", "find-fn"))
    href = page_url(block, root, "report", "findings")
    part_url = lambda key, at: frame.ROUTE + "?" + urlencode({"view": "focus-part", "part": key, "path": frame.rel(at, root)})
    frame_of = lambda url, name: f'<iframe class=find-frame data-src="{frame.esc(url)}" title="{frame.esc(name)}"></iframe>'

    def row(mark, name, word, link, inner, cls=""):        # a closed row, as a Job's in Review Content: its name goes to
        return (f'<details class="job-row find-row{cls}"><summary><span class=jn>{mark}</span>'   # the page, ▸ opens it
                f'<a href="{frame.esc(link)}"><b>{frame.esc(name)}</b></a><small>{frame.esc(word)}</small>'
                f'<span class=bar style="visibility:hidden"></span></summary><div class=find-body>{inner}</div></details>')
    out = ""
    for mark, name, word, sid in parts:
        if sid == "find-displays":                       # its displays, each opening to its preview in place
            inner = "".join(row("", head, line, page_url(t, root), frame_of(part_url("find-display", t), head), " find-sub")
                            for t, head, line in display_rows(block, root))
        else:
            inner = frame_of(part_url(sid, block), name)
        out += row(mark, name, word, f"{href}#{sid}", inner)
    return out + FIND_ROW_JS if out else ""


# a Findings row's frame loads only when the row is first opened, and takes its page's height
FIND_ROW_JS = """<script>(function(){
if(window.__findRows)return;window.__findRows=1;
function body(f){return f.contentDocument.querySelector('main')||f.contentDocument.body}
function fit(f){try{f.style.height=Math.ceil(body(f).getBoundingClientRect().bottom+6)+'px'}catch(e){}}
document.addEventListener('toggle',function(e){
  var r=e.target;if(!r.open||!r.classList||!r.classList.contains('find-row'))return;
  var f=r.querySelector(':scope>.find-body>iframe.find-frame');if(!f||f.src)return;
  f.addEventListener('load',function(){fit(f);try{new ResizeObserver(function(){fit(f)}).observe(body(f))}catch(e){}});
  f.src=f.dataset.src},true)})()</script>"""


FIND_ROW_CSS = """<style>
.topic-row{display:flex;align-items:center;gap:8px;padding:7px 15px 7px 22px;font-size:14px}
.topic-row a{color:inherit;text-decoration:none}
.find-body{padding:4px 15px 8px 22px}.find-body>.find-sub{margin:0 -15px 0 -22px}
.find-frame{width:100%;height:240px;border:0;display:block}
.find-sub>summary{padding-left:46px}.find-sub>summary>a{flex:0 0 auto;white-space:nowrap}
.find-sub>summary>small{flex:1 1 0;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.find-none{padding:7px 15px 7px 22px;margin:0}
</style>"""


def findings_band(folder: Path, root: Path) -> str:
    """🔎 Findings under a work Block's or Job's Plan + Results Review Content, the same rows the Project's Findings
    shows for it; nothing at all when it has none."""
    rows = findings_parts(folder, root)
    return (FIND_ROW_CSS + '<h3 class=wk-band>🔎 Findings</h3><div class=find-band>' + rows + '</div>') if rows else ""


__all__ = ['find_part_document', 'data_stores', 'store_count', 'DATA_CSS', 'data_section', 'VERSION_DIR', 'fn_file', 'FN_CSS', 'fn_panel', 'fn_found', 'fn_sections', 'work_findings', 'findings_parts', 'FIND_ROW_JS', 'FIND_ROW_CSS', 'findings_band']
