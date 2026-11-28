"""A trace in the Files pane: one piece of work's files on the real tree, each with its state.

A trace is `<Block>/trace/<YYMMDD>/<HHMM>_<slug>.md` (hai-trace): front matter with `title`, `date`, `aim`,
`closed`, `plan` (do: add, edit, move or delete; path from the SPACE root; what) and `changed` (paths written so far).
Each file gets one mark (file_icons.STATE_MARKS):

    plan   in the plan, not touched yet           dashed ring
    edit   touched, the trace still open          half-filled ring
    done   the trace closed, not committed yet    filled ring with a tick
    off    touched, but the plan left it out      amber diamond

The marks sit on the one Files tree: a file to add that is not on disk yet gets a row where it will sit (+, grey
italic, slowly fading), a file being changed has a light sweeping across it, a folder with marked files inside shows a
dot. The Trace button lights up one trace's files and folders, opens the tree down to them and dims the rest.
"""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

import yaml

from live import frame
from live.file_icons import STATE_MARKS, STATE_ORDER, file_icon
from live.frame_base import chain


_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)   # libyaml: ten times faster on the first visit (t03 p01)
_READ: dict = {}      # {face: (mtime, meta)}: a trace is parsed again only when it changes
_DIRTY: dict = {}     # {root: (when, paths asked, paths open)}: one git call serves one page (JL 261125: slow Files)


def read(face: Path) -> dict | None:
    """One trace's front matter, or None when the file has none."""
    try:
        stamp = face.stat().st_mtime_ns
        if face in _READ and _READ[face][0] == stamp:
            return _READ[face][1]
        text = face.read_text(encoding="utf-8")
    except OSError:
        return None
    meta = _parse(text)
    _READ[face] = (stamp, meta)
    return meta


def _parse(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    try:
        meta = yaml.load(text.split("---", 2)[1], Loader=_LOADER) or {}
    except (yaml.YAMLError, IndexError):
        return None
    return meta if isinstance(meta, dict) else None


def traces(block: Path) -> list[tuple[Path, dict]]:
    """The Block's traces, newest first."""
    found = []
    for face in sorted((block / "trace").glob("[0-9]*/[0-9]*_*.md"), reverse=True):
        meta = read(face)
        if meta is not None:
            found.append((face, meta))
    return found


def visiting(block: Path, root: Path) -> list[tuple[Path, dict]]:
    """Traces kept in other Blocks that planned or changed a file of this one, newest first (JL 261126: b11's pane
    showed no trace bar, though b17's traces had moved its files)."""
    block, root = block.resolve(), root.resolve()
    rel = block.relative_to(root).as_posix() + "/"
    found = []
    for face in sorted(root.glob("examples/*/*/*/trace/[0-9]*/[0-9]*_*.md"),
                       key=lambda f: f.parent.name + f.name, reverse=True):
        if block in face.parents:
            continue
        meta = read(face)
        if not meta:
            continue
        paths = [str(i.get("path") or "") for i in meta.get("plan") or [] if isinstance(i, dict)]
        paths += [str(p) for p in meta.get("changed") or []]
        if any(p.strip().startswith(rel) for p in paths):
            found.append((face, meta))
    return found


def blueprint_blocks(block: Path, root: Path) -> list[Path]:
    """The other Blocks of a blueprint Block's own folder that its traces planned or changed a file in, in folder
    order: Blocks it keeps as it keeps its own, so their files are marked in place and never listed under Touch.
    A Block of another theme has none: what its traces touch outside it stays Touch."""
    block, root = block.resolve(), root.resolve()
    home = block.parent
    if home.name != "blueprint" or not home.is_relative_to(root):
        return []
    base, names = home.relative_to(root).as_posix() + "/", set()
    for _, meta in traces(block):
        paths = [str(i.get("path") or "") for i in meta.get("plan") or [] if isinstance(i, dict)]
        paths += [str(p) for p in meta.get("changed") or [] if p]
        names |= {p.strip()[len(base):].split("/", 1)[0] for p in paths if p.strip().startswith(base)}
    return [home / n for n in sorted(names) if home / n != block and (home / n / "board.md").is_file()]


def dirty(root: Path, paths) -> set[str]:
    """The SPACE-relative paths among these that git says are not committed."""
    paths = sorted(set(paths))
    if not paths:
        return set()
    hit = _DIRTY.get(str(root))
    if hit and time.monotonic() - hit[0] < 10 and hit[1].issuperset(paths):   # one page build, even on a busy machine (t03 p02)
        return hit[2] & set(paths)
    try:
        out = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "-uall", "--ignore-submodules=all", "--", *paths],
                             capture_output=True, text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return set(paths)                         # no git: treat every file as still open
    found = {line[3:].split(" -> ")[-1].strip('"') for line in out.splitlines() if len(line) > 3}
    _DIRTY[str(root)] = (time.monotonic(), frozenset(paths), found)
    return found


def warm(root: Path, metas) -> None:
    """Ask git once about every closed trace's files, so states() below reads the answer instead of one call each."""
    paths = set()
    for meta in metas:
        if meta.get("closed"):
            paths |= {str(i["path"]).strip() for i in meta.get("plan") or [] if isinstance(i, dict) and i.get("path")}
            paths |= {str(p).strip() for p in meta.get("changed") or [] if p}
    dirty(root, paths)


def states(meta: dict, root: Path, keep: bool = False) -> dict[str, dict]:
    """{path: {state, do, what}} for every file of one trace; a closed trace's committed files are left out,
    or marked kept when `keep` (the timeline shows history)."""
    closed = bool(meta.get("closed"))
    changed = {str(p).strip() for p in meta.get("changed") or [] if p}
    rows: dict[str, dict] = {}
    for item in meta.get("plan") or []:
        if not isinstance(item, dict) or not item.get("path"):
            continue
        path = str(item["path"]).strip()
        do = str(item.get("do") or "edit")
        touched = path in changed or (do == "add" and (root / path).exists()) or (do == "delete" and not (root / path).exists())
        rows[path] = {"state": "edit" if touched else "plan", "do": do, "what": str(item.get("what") or "")}
    for path in changed - set(rows):
        rows[path] = {"state": "off", "do": "edit", "what": ""}
    if closed:
        open_files = dirty(root, rows)
        rows = {p: dict(r, state="kept" if p not in open_files else "off" if r["state"] == "off" else "done")
                for p, r in rows.items() if keep or p in open_files}
    return rows


def overall(meta: dict, rows: dict) -> str:
    """One trace's own mark: done once closed, editing once any file is touched, else planned."""
    if meta.get("closed"):
        return "done"
    return "edit" if any(r["state"] in ("edit", "off") for r in rows.values()) else "plan"


def sections(face: Path) -> dict[str, str]:
    """The trace body's `## Part` texts by name (Prompts, Check, Summary)."""
    import re
    try:
        body = face.read_text(encoding="utf-8").split("---", 2)[2]
    except (OSError, IndexError):
        return {}
    return {name: text.strip() for name, text in re.findall(r"^## (\w+)\n(.*?)(?=^## |\Z)", body, re.M | re.S)}


def _bullets(text: str) -> list[str]:
    """A part's bullet lines, their **bold** marks and wraps flattened ('- **14:18** said' -> '14:18 said')."""
    items, cur = [], None
    for line in text.splitlines():
        if line.startswith("- "):
            cur = line[2:].replace("**", "").strip()
            items.append(cur)
        elif cur is not None and line.startswith("  "):
            items[-1] += " " + line.strip()
    return items or ([" ".join(text.split())] if text else [])


def _when(face: Path, meta: dict) -> tuple[str, str, str]:
    """(sort key, MM-DD, HH:MM) of a trace, from its folder and file name."""
    day, hhmm = face.parent.name, face.stem[:4]
    short = f"{day[2:4]}-{day[4:6]}" if len(day) == 6 and day.isdigit() else day
    return day + hhmm, short, f"{hhmm[:2]}:{hhmm[2:]}" if hhmm.isdigit() else hhmm


def in_play(found) -> dict[str, dict]:
    """{path: {s, t, w, miss}} for every file of the traces still in play (open, or closed and not committed), the
    strongest state when two traces hold one file."""
    out: dict[str, dict] = {}
    for face, meta, rows in found:
        title = str(meta.get("title") or face.stem)
        for rel, row in rows.items():
            if row["state"] == "kept":
                continue
            old = out.get(rel)
            if old and STATE_ORDER.index(old["s"]) <= STATE_ORDER.index(row["state"]):
                continue
            out[rel] = {"s": row["state"], "t": title, "w": row["do"] + (" · " + row["what"] if row["what"] else "")}
    return out


def _group(rel: str) -> str:
    """The folder a Touch part is named for: plugins/<package>/<servers|skills>/, else its top folder, else
    the SPACE root ('')."""
    parts = rel.split("/")
    if len(parts) > 3 and parts[0] == "plugins":
        return "/".join(parts[:3]) + "/"
    return parts[0] + "/" if len(parts) > 1 else ""


def also_touched(marks: dict, root: Path, covered) -> str:
    """Touch: one part, a numbered path line per folder (Touch 2), for the planned or touched files that sit under none of the tree's parts (a skill
    that does not own this page, another server), each file inside its real folders below that folder."""
    from live.work_files import allowed_source, nested_rows
    bases = [Path(c).resolve() for c in covered]
    groups: dict[str, list[str]] = {}
    for rel in sorted(marks):
        path = (root / rel).resolve()
        if any(path == b or b in path.parents for b in bases) or path.is_dir():
            continue
        groups.setdefault(_group(rel), []).append(rel)
    if not groups:
        return ""
    html = []
    for n, folder in enumerate(sorted(groups, key=lambda g: (g != "", g)), 1):    # the SPACE root first, then by folder
        found = [(root / rel).resolve() for rel in groups[folder]]
        shown = [p for p in found if allowed_source(p, root)]          # on disk: in its real folders, opened down to it
        rows = [nested_rows((root / folder).resolve(), shown, root)] if shown else []
        for rel, path in zip(groups[folder], found):
            if path not in shown:                                       # still to create: one row, by its path
                short = rel[len(folder):]
                rows.append(f'<li class="file-leaf" data-path="{frame.esc(rel)}"><span class="tm-name">'
                            f'<span aria-hidden="true">{file_icon(path)}</span>{frame.esc(short)}</span></li>')
        html.append(f'<p class="files-where" data-n="{n}" title="{frame.esc(folder or "./")}">{frame.esc(folder or "./")}</p>'
                    f'<ul class="file-sources">{"".join(rows)}</ul>')
    return '<section class="files-part files-touch tm-also files-first"><h3>Touch</h3>' + "".join(html) + '</section>'


def render(folder: Path, root: Path, files_tree: str, covered=()) -> str:
    """The one Files tree, its files marked by the traces in play (plan ◌, touched ◐, done ●✓, off the plan ◆, still to
    create +), and a Trace button: trace mode lights up one trace's files and folders (the newest open one first; a
    click on another trace file under trace/ picks that one), opens the tree down to them, dims the rest, and shows the
    trace's card (aim, prompts, check, summary) under the top row."""
    block = (chain(folder, root).get("Block") or folder).resolve()
    own, other = traces(block), visiting(block, root)            # its own, and other Blocks' that touched it
    warm(root, [m for _, m in own + other])
    mine = block.relative_to(root.resolve()).as_posix() + "/"
    found = [(face, meta, states(meta, root, keep=True)) for face, meta in own]
    found += [(face, meta, {p: r for p, r in states(meta, root, keep=True).items() if p.startswith(mine)})
              for face, meta in other]                         # another Block's trace marks only this Block's files
    found = [t for t in found if t[2]]
    if not found:                                               # the bar stays, so every Block's pane looks the same
        return (TRACE_STYLE + '<div class="tm-bar"><button type="button" class="tm-mode" disabled title="No trace touches '
                f'this Block" aria-label="Trace">{HIGHLIGHTER}</button><button type="button" class="tm-only" disabled '
                f'aria-label="Tracked only">{FUNNEL}</button></div>' + files_tree)
    marks = in_play(found)
    for rel, m in marks.items():
        path = root / rel
        if not path.exists():
            m["miss"] = 1
            m["icon"] = file_icon(path)
    playing = [t for t in found if not t[1].get("closed")]      # a chip per open trace; a closed one keeps its marks
    for face, meta, rows in playing:                            # an open trace opens the tree down to its files
        for rel, row in rows.items():
            if rel in marks and row["state"] != "kept":
                marks[rel]["o"] = 1
    extra = also_touched(marks, root, covered) if covered else ""
    if extra and files_tree.endswith("</div>"):
        files_tree = files_tree[:-len("</div>")] + extra + "</div>"
    key = frame.esc(frame.rel(block, root))
    order = sorted(found, key=lambda t: _when(t[0], t[1])[0], reverse=True)
    picks = [{"k": face.stem, "t": f"{_when(face, meta)[2]}  {meta.get('title') or face.stem}", "p": frame.rel(face, root),
              "aim": str(meta.get("aim") or ""), "f": sorted(rows), "day": _when(face, meta)[1], "hm": _when(face, meta)[2],
              "title": str(meta.get("title") or face.stem), "u": frame.ROUTE + "?view=focus-file&path=" + frame.rel(face, root),
              "pr": _bullets(sections(face).get("Prompts", "")), "chk": _bullets(sections(face).get("Check", "")),
              "sum": " ".join(sections(face).get("Summary", "").split()),
              "s": {rel: ("delete" if row["do"] == "delete" and row["state"] in ("plan", "edit") else row["state"])
                    for rel, row in rows.items()},
              "c": "#b9b9b3" if all(r["state"] == "kept" for r in rows.values()) else METRO[i % len(METRO)]}
             for i, (face, meta, rows) in enumerate(order)]
    current = next((t[0].stem for t in order if not t[1].get("closed")), order[0][0].stem)
    bar = (f'<div class="tm-bar" data-trace-block="{key}"><button type="button" class="tm-mode" aria-pressed="false" '
           f'title="Trace" aria-label="Trace">{HIGHLIGHTER}</button><button type="button" class="tm-name" aria-expanded="false" hidden></button>'
           f'<button type="button" class="tm-only" aria-pressed="false" title="Tracked only" aria-label="Tracked only">{FUNNEL}</button>'
           '<button type="button" class="tm-zoom" data-z="-1" title="Zoom out" aria-label="Zoom out">−</button>'
           '<button type="button" class="tm-zoom" data-z="1" title="Zoom in" aria-label="Zoom in">+</button>'
           '<button type="button" class="tm-step" data-step="-1" title="Earlier" aria-label="Earlier">‹</button>'
           '<button type="button" class="tm-step" data-step="1" title="Later" aria-label="Later">›</button>'
           f'<button type="button" class="tm-metro-btn" aria-pressed="true" title="Metro map" aria-label="Metro map">{BRANCH}</button></div>')
    data = json.dumps({"m": marks, "svg": STATE_MARKS, "traces": picks, "current": current}).replace("</", "<\\/")
    return (TRACE_STYLE + bar + '<div class="tm-card" hidden></div><div class="tm-wrap">' + files_tree + '<div class="tm-split" title="Drag; double-click to reset"></div><div class="tm-metro"><svg class="tm-map"></svg></div></div>'
            + f'<script type="application/json" class="tm-data">{data}</script>' + TRACE_SCRIPT + METRO_SCRIPT)


METRO = ("#8e6cc4", "#2a9d8f", "#e76f51", "#2f6fd6", "#d4a017", "#43aa8b", "#c0392b", "#5c7cfa", "#e64980", "#0ca678")
HIGHLIGHTER = ('<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M9.5 2.5l4 4-6 6H3.5v-4z" fill="none" '
               'stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M2 14h12" stroke="#f2c94c" stroke-width="2.5" '
               'stroke-linecap="round"/></svg>')
FUNNEL = ('<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 3h11l-4.2 5v4.5l-2.6 1.3V8z" fill="none" '
          'stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>')
BRANCH = ('<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 12h4c2 0 2-8 5-8h3M6 12h8" fill="none" '
          'stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><circle cx="11" cy="4" r="1.6" fill="currentColor"/>'
          '<circle cx="11" cy="12" r="1.6" fill="currentColor"/></svg>')


TRACE_STYLE = """<style>
.tm-bar{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:0 0 8px;padding:6px 0;position:sticky;top:0;z-index:15;background:var(--bg,#fff)}
.tm-bar>.tm-card{position:absolute;top:calc(100% + 2px);left:0;right:0;margin:0}
.tm-mode,.tm-metro-btn{border:0;background:none;border-radius:6px;padding:4px;line-height:0;color:var(--text);cursor:pointer}
.tm-mode[aria-pressed=true],.tm-metro-btn[aria-pressed=true]{background:var(--line)}.tm-metro-btn[aria-pressed=false]{color:var(--muted)}
.tm-card{position:absolute;z-index:20;max-height:60vh;overflow:auto;box-shadow:0 14px 36px rgba(0,0,0,.16)!important;background:var(--bg,#fff);border:1px solid var(--line);border-radius:10px;
 box-shadow:0 6px 18px rgba(0,0,0,.08);padding:8px 12px;margin:0 0 10px;font-size:12.5px}
.tm-card p{margin:6px 0}.tm-card b.k{display:block;margin-top:8px;font-size:10.5px;color:var(--muted);letter-spacing:.05em}
.tm-card ul{margin:2px 0;padding-left:16px}.tm-card li{margin:2px 0}
.tm-card .more{border:0;background:none;color:var(--accent,#1f5fbf);cursor:pointer;padding:0;font:inherit;font-size:11.5px}
.tm-wrap{display:grid;grid-template-columns:var(--tm-left,fit-content(min(34%,260px))) 7px minmax(120px,1fr);align-items:start}.tm-wrap.nometro{grid-template-columns:minmax(0,1fr)}
.tm-wrap.nometro :is(.tm-metro,.tm-split){display:none}
.tm-split{align-self:stretch;cursor:col-resize;touch-action:none;background:linear-gradient(var(--line,#e5e7eb),var(--line,#e5e7eb)) center/1px 100% no-repeat}
.tm-split:hover,.tm-split.drag{background:linear-gradient(#4c6ef5,#4c6ef5) center/3px 100% no-repeat}
.tm-zoom,.tm-step{border:0;background:none;color:var(--text);cursor:pointer;font-size:16px;line-height:1;padding:2px 6px;border-radius:6px}
.tm-zoom:hover,.tm-step:hover{background:var(--line)}.tm-zoom:disabled,.tm-step:disabled{opacity:.3;cursor:default;background:none}
.tm-bar:has(.tm-metro-btn[aria-pressed=false]) :is(.tm-step,.tm-zoom){display:none}
.tm-bar:has(.tm-metro-btn[aria-pressed=false]) .tm-only{margin-left:auto}
.tm-metro{min-width:0;overflow-x:auto;overflow-y:hidden;scrollbar-width:none;cursor:grab}
.tm-metro::-webkit-scrollbar{display:none}.tm-metro.drag{cursor:grabbing;user-select:none}.tm-map{display:block;overflow:visible;max-width:none}
.tm-map text{font-size:10px;fill:var(--muted);font-variant-numeric:tabular-nums}.tm-map .tm-t{cursor:pointer}
.tm-map .tm-t.on text{fill:var(--text);font-weight:700}.tm-map .tm-day{font-size:10px;fill:var(--text);font-weight:600}
.tm-map .tm-st{cursor:pointer}.tm-map .tm-live{animation:tm-grow 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes tm-grow{50%{transform:scale(1.3)}}
.tm-wrap:not(.nometro) .file-tree li.tm>.state-mark,.tm-wrap:not(.nometro) .file-tree .tm-dot{display:none}
.file-tree.tm-on li.file-leaf a{cursor:pointer}
.tm-name{flex:1;min-width:0;border:0;background:none;padding:3px 6px;border-radius:6px;font:inherit;font-size:12.5px;font-weight:600;
 color:var(--text);text-align:left;cursor:pointer;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.tm-name:hover,.tm-name[aria-expanded=true]{background:var(--line)}
.tm-bar .tm-only{margin-left:auto}
.tm-only{border:0;background:none;border-radius:6px;padding:4px;line-height:0;color:var(--muted);cursor:pointer}.tm-only[aria-pressed=true]{background:var(--line);color:var(--text)}
.file-tree .tm-fold{display:none!important}.file-tree li.tm-more>button{display:block;width:100%;border:0;border-radius:4px;background:none;color:var(--muted);cursor:pointer;font:inherit;font-size:17px;font-weight:700;line-height:18px;padding:0 0 0 17px;text-align:left;letter-spacing:.15em}.file-tree li.tm-more>button:hover{background:var(--line);color:var(--text)}
.tm-wrap>.file-tree{min-width:0;overflow-x:auto;overflow-y:hidden;scrollbar-width:none}.tm-wrap>.file-tree::-webkit-scrollbar{display:none}.tm-wrap .file-tree li>a,.tm-wrap .file-tree summary>span{white-space:nowrap;overflow-wrap:normal}.tm-wrap .file-tree li,.tm-wrap .file-tree summary{min-width:max-content}
.file-tree.tm-on li.file-leaf:not(.tm-hit),.file-tree.tm-on details.file-branch:not(.tm-hit)>summary{opacity:.3}
.file-tree.tm-on .tm-hit>a,.file-tree.tm-on details.tm-hit>summary>span{font-weight:600}
.state-mark{flex:none}
.file-tree li.tm{display:flex;align-items:center;gap:6px}.file-tree li.tm>a,.file-tree li.tm>.tm-name{flex:1;min-width:0}
.file-tree li.tm>.state-mark{flex:none;margin-right:4px}
.file-tree .tm-name{display:block;padding:5px 0 5px 17px;font-size:13px;font-style:italic;color:var(--muted)}
.file-tree .tm-name>span{opacity:.5;margin-right:5px}
.file-tree .tm-ghost>.tm-name{animation:tm-fade 2.6s ease-in-out infinite}
.file-tree .tm-ghost>.tm-name::before{content:"+";display:inline-block;width:12px;margin-left:-14px;font-style:normal}
@keyframes tm-fade{50%{opacity:.45}}
.file-tree .tm-edit>a{background:linear-gradient(90deg,transparent,rgba(47,111,214,.12),transparent);background-size:200% 100%;
 animation:tm-shine 2.4s ease-in-out infinite;border-radius:5px}
@keyframes tm-shine{0%{background-position:150% 0}100%{background-position:-50% 0}}
.file-tree .tm-edit>.state-mark{animation:tm-breathe 1.8s ease-in-out infinite}
@keyframes tm-breathe{50%{filter:drop-shadow(0 0 4px rgba(47,111,214,.8));transform:scale(1.15)}}
.file-tree .tm-done>.state-mark{animation:tm-pop .7s cubic-bezier(.3,1.6,.5,1) 1}
@keyframes tm-pop{0%{transform:scale(.3)}100%{transform:scale(1)}}
.file-tree .tm-also a,.file-tree .tm-also .tm-name{overflow-wrap:anywhere}
.file-tree .tm-delete>a{text-decoration:line-through;opacity:.55}
.file-tree .tm-dot{flex:none;width:6px;height:6px;border-radius:50%;margin:0 6px 0 auto}
.file-tree .tm-dot.tm-edit{animation:tm-ping 1.8s ease-out infinite}
@keyframes tm-ping{0%{box-shadow:0 0 0 0 rgba(47,111,214,.55)}100%{box-shadow:0 0 0 6px rgba(47,111,214,0)}}
@media (prefers-reduced-motion:reduce){.file-tree .tm *,.file-tree .tm,.file-tree .tm-dot,.tm-map .tm-live{animation:none!important}}
</style>"""
TRACE_SCRIPT = """<script>(function(){
var here=document.currentScript.parentNode,bar=here.querySelector('.tm-bar');if(!bar)return;here.tmReady=1;
var tree=here.querySelector('.file-tree');
var D=JSON.parse(here.querySelector('.tm-data').textContent),M=D.m,SVG=D.svg,RANK=['off','edit','plan','done'];
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function apply(){
 tree.querySelectorAll('li>a:not([title]),summary>span:not([title])').forEach(function(e){e.title=e.textContent.trim();});  // the whole name on hover
 tree.querySelectorAll('li.file-leaf[data-path]:not([data-tm])').forEach(function(li){var m=M[li.dataset.path];li.dataset.tm='1';if(!m)return;
  li.classList.add('tm','tm-'+m.s);if(m.miss)li.classList.add('tm-ghost');if(/^delete/.test(m.w))li.classList.add('tm-delete');li.title=m.t+' · '+m.w;li.insertAdjacentHTML('beforeend',SVG[m.s]);});
 tree.querySelectorAll('details.file-branch[data-folder-path]').forEach(function(d){var f=d.dataset.folderPath+'/',best=-1;
  for(var k in M)if(k.indexOf(f)===0){var r=RANK.indexOf(M[k].s);if(best<0||r<best)best=r;}
  var s=d.querySelector(':scope>summary');if(best>=0&&s&&!s.querySelector('.tm-dot'))
   s.insertAdjacentHTML('beforeend','<i class="tm-dot tm-'+RANK[best]+'" style="background:'+({off:'#d98a12',edit:'#2f6fd6',plan:'#9a9a94',done:'#2f9e5b'})[RANK[best]]+'" aria-hidden="true"></i>');
  var ul=d.querySelector(':scope>.folder-children>ul');if(!ul)return;
  for(var p in M){var m=M[p];if(!m.miss||p.slice(0,p.lastIndexOf('/'))!==d.dataset.folderPath)continue;
   if(ul.querySelector('[data-ghost="'+CSS.escape(p)+'"]'))continue;
   ul.insertAdjacentHTML('beforeend','<li class="file-leaf tm tm-ghost" data-tm="1" data-ghost="'+esc(p)+'" title="'+esc(m.t+' · '+m.w)+'">'
    +'<span class="tm-name"><span aria-hidden="true">'+m.icon+'</span>'+esc(p.split('/').pop())+'</span>'+SVG.plan+'</li>');}
 });}
function openUp(d){d.open=true;if(d.dataset.folderSrc&&!d.dataset.loaded)setTimeout(function(){   // ask the loader again: a
  if(d.open&&!d.dataset.loaded&&!d.dataset.loading)d.dispatchEvent(new Event('toggle'));},120);}             // toggle can come too early
function reach(){if(only||!on)return;var n=0;   // closed until a trace is picked; the funnel decides what is open (JL 261126)
 tree.querySelectorAll('details.file-branch[data-folder-path]:not([open]):not([data-auto])').forEach(function(d){
  var f=d.dataset.folderPath+'/';for(var k in M)if(M[k].o&&k.indexOf(f)===0){d.dataset.auto='1';openUp(d);n++;return;}});
 if(n)setTimeout(function(){apply();reach();},60);}            // a folder whose rows are already here changes nothing: go on
apply();reach();var t;new MutationObserver(function(){clearTimeout(t);t=setTimeout(function(){apply();reach();},30);}).observe(tree,{childList:true,subtree:true});
var T=D.traces,on=false,cur=D.current,btn=bar.querySelector('.tm-mode');
var store='wb:trace:'+bar.dataset.traceBlock;
function files(){var t=T.find(function(x){return x.k===cur;});return t?t.f:[];}
function light(){var F=files(),opened=0;
 tree.querySelectorAll('li.file-leaf').forEach(function(li){var p=li.dataset.path||li.dataset.ghost;li.classList.toggle('tm-hit',on&&F.indexOf(p)>=0);});
 tree.querySelectorAll('details.file-branch[data-folder-path]').forEach(function(d){var f=d.dataset.folderPath+'/',hit=on&&F.some(function(p){return p.indexOf(f)===0;});
  d.classList.toggle('tm-hit',hit);if(hit&&!d.dataset.lit&&(!d.open||!d.dataset.loaded&&d.dataset.folderSrc)){d.dataset.lit='1';openUp(d);opened++;}});
 if(opened)setTimeout(function(){apply();light();},60);}       // rows already here change nothing: go on down
var cardEl=here.querySelector('.tm-card'),nameEl=bar.querySelector('.tm-name'),opened=false,all=false;
function card(){var t=T.find(function(x){return x.k===cur;});nameEl.hidden=!on||!t;
 if(t){nameEl.textContent=t.title;nameEl.title=t.day+' '+t.hm;}nameEl.setAttribute('aria-expanded',on&&opened?'true':'false');
 cardEl.hidden=!(on&&opened&&t);if(cardEl.hidden)return;
 var ps=all?t.pr:t.pr.slice(0,3),li=function(x){var m=/^([0-9][0-9]:[0-9][0-9]) +(.*)$/.exec(x);return '<li>'+(m?'<b>'+esc(m[1])+'</b> '+esc(m[2]):esc(x))+'</li>';};
 cardEl.innerHTML=(t.aim?'<p>'+esc(t.aim)+'</p>':'')
  +(t.pr.length?'<b class="k">PROMPTS</b><ul>'+ps.map(li).join('')+'</ul>'+(t.pr.length>3&&!all?'<button type="button" class="more">'+(t.pr.length-3)+' more</button>':''):'')
  +(t.chk.length?'<b class="k">CHECK</b><ul>'+t.chk.map(function(x){return '<li>'+esc(x)+'</li>';}).join('')+'</ul>':'')
  +(t.sum?'<b class="k">SUMMARY</b><p>'+esc(t.sum)+'</p>':'');
 var m=cardEl.querySelector('.more');if(m)m.addEventListener('click',function(){all=true;card();});}
bar.appendChild(cardEl);                                        // the content hangs from the top row, which stays at the top
nameEl.addEventListener('click',function(){opened=!opened;card();});
document.addEventListener('click',function(e){if(opened&&!cardEl.contains(e.target)&&!nameEl.contains(e.target)){opened=false;card();}});
document.addEventListener('keydown',function(e){if(e.key!=='Escape'||e.defaultPrevented||!opened)return;e.preventDefault();opened=false;card();});
function mode(v,key){if(key&&key!==cur)all=false;on=v;if(key)cur=key;btn.setAttribute('aria-pressed',on?'true':'false');
 card();tree.classList.toggle('tm-on',on);
 tree.querySelectorAll('[data-lit]').forEach(function(d){delete d.dataset.lit;});light();
 try{sessionStorage.setItem(store,on?cur:'');}catch(e){}if(here.tmFold)here.tmFold();if(here.tmDraw)here.tmDraw();}
btn.addEventListener('click',function(){mode(!on);if(!on&&only)onlyBtn.click();});   // the funnel means one trace
var onlyBtn=bar.querySelector('.tm-only'),only=false,TRACKED=[];   // the funnel folds what the trace left alone; nothing is hidden
T.forEach(function(t){t.f.forEach(function(p){if(TRACKED.indexOf(p)<0)TRACKED.push(p);});});
function keep(){return on&&cur?files():[];}                     // a picked trace: its files; else every trace's files
function fkey(){return only?(on&&cur?cur:'*'):'';}
function fold(){var K=keep(),key=fkey(),opened=0;
 tree.querySelectorAll('li.tm-more').forEach(function(m){if(!key||m.dataset.fk!==key)m.remove();});
 tree.querySelectorAll('li.file-leaf').forEach(function(li){var p=li.dataset.path||li.dataset.ghost,ul=li.parentNode;
  li.classList.toggle('tm-fold',!!key&&!!p&&K.indexOf(p)<0&&ul.dataset.all!==key);});
 if(!key){if(here.tmDraw)here.tmDraw();return;}
 tree.querySelectorAll('details.file-branch[data-folder-path]').forEach(function(d){
  var f=d.dataset.folderPath+'/',hit=K.some(function(x){return x.indexOf(f)===0;});
  if(hit){if(d.dataset.fk!==key){d.dataset.fk=key;openUp(d);opened++;}}
  else if(d.open&&d.dataset.user!==key)d.open=false;});           // fold all, open only its path; what the person opened stays

 tree.querySelectorAll('ul').forEach(function(ul){var n=ul.querySelectorAll(':scope>li.tm-fold').length,m=ul.querySelector(':scope>li.tm-more');
  if(!n){if(m)m.remove();return;}if(m)return;
  ul.insertAdjacentHTML('beforeend','<li class="tm-more" data-fk="'+esc(key)+'"><button type="button" title="Other files">⋯</button></li>');});
 if(opened)setTimeout(function(){apply();fold();},60);if(here.tmDraw)here.tmDraw();}
tree.addEventListener('click',function(e){var sm=e.target.closest('details.file-branch>summary');if(sm&&e.isTrusted)sm.parentNode.dataset.user=fkey();
 var b=e.target.closest('li.tm-more>button');if(!b)return;var ul=b.closest('ul');
 ul.dataset.all=fkey();b.parentNode.remove();fold();});               // ⋯ unfolds the files beside them
var picked='';function reveal(){if(!only||!on||!cur||picked===cur)return;picked=cur;
 setTimeout(function(){var h=tree.querySelector('li.file-leaf.tm-hit');if(h){var x=tree.scrollLeft;h.scrollIntoView({block:'center'});tree.scrollLeft=x;}},400);}
onlyBtn.addEventListener('click',function(){only=!only;onlyBtn.setAttribute('aria-pressed',only?'true':'false');picked='';
 try{localStorage.setItem('wb:tracked-only',only?'1':'0');}catch(e){}
 if(only&&!on&&T.length){mode(true,cur||T[0].k);return;}       // no trace picked: the newest
 fold();reveal();try{localStorage.setItem('wb:tracked-only',only?'1':'0');}catch(e){}});
here.tmFold=function(){picked=picked===cur?picked:'';fold();reveal();};
var onlyT;new MutationObserver(function(){if(only){clearTimeout(onlyT);onlyT=setTimeout(function(){apply();fold();},50);}}).observe(tree,{childList:true,subtree:true});
try{if(localStorage.getItem('wb:tracked-only')==='1')onlyBtn.click();}catch(e){}
here.tmPick=function(k){mode(true,k);};here.tmState=function(){return {on:on,cur:cur};};
window.addEventListener('click',function(e){if(!on||!tree.contains(e.target))return;var li=e.target.closest('li.file-leaf[data-path]');if(!li)return;
 var t=T.find(function(x){return x.p===li.dataset.path;});if(!t)return;                      // in trace mode a trace file picks its trace,
 e.preventDefault();e.stopImmediatePropagation();mode(true,t.k);},true);                        // before the viewer opens it
new MutationObserver(function(){if(on){clearTimeout(t);t=setTimeout(function(){apply();reach();light();},40);}}).observe(tree,{childList:true,subtree:true});
try{var saved=sessionStorage.getItem(store);if(saved&&T.some(function(x){return x.k===saved;}))mode(true,saved);}catch(e){}
})();</script>"""
METRO_SCRIPT = """<script>(function(){
var here=document.currentScript.parentNode,wrap=here.querySelector('.tm-wrap');if(!wrap)return;
var tree=wrap.querySelector('.file-tree'),box=wrap.querySelector('.tm-metro'),svg=box.querySelector('svg'),btn=here.querySelector('.tm-metro-btn');
var ALL=JSON.parse(here.querySelector('.tm-data').textContent).traces.slice().reverse();   // oldest first: time runs left to right
var LEVELS=['day','hour','half','trace','close'],Z=3;                 // by day, hour, half hour, trace; close up
try{var z=localStorage.getItem('wb:metro-level');if(LEVELS.indexOf(z)>=0)Z=LEVELS.indexOf(z);}catch(e){}
function bucket(t,z){var h=t.hm.slice(0,2),mm=+t.hm.slice(3,5);
 return z===0?t.day:z===1?t.day+' '+h+':00':t.day+' '+h+(mm<30?':00':':30');}
function columns(z){if(z===undefined)z=Z;if(z>=3)return ALL;var by={},out=[];ALL.forEach(function(t){var key=bucket(t,z),d=by[key];
  if(!d){d=by[key]={k:'b:'+key,day:t.day,hm:z===0?t.day:key.slice(-5),t:key,c:'#6b6b66',s:{},first:t.k};out.push(d);}
  for(var p in t.s){var a=d.s[p],b=t.s[p];if(!a||RANK.indexOf(b)<RANK.indexOf(a))d.s[p]=b;}});return out;}
var T=ALL;
var COL=22,PAD=12,WIDE=[22,22,22,22,44],RANK=['off','edit','delete','plan','done','kept'],first=true;
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function rows(){var out=[];tree.querySelectorAll('li.file-leaf, details.file-branch[data-folder-path]>summary').forEach(function(el){
  if(!el.offsetParent||el.closest('details:not([open])>.folder-children'))return;
  var li=el.matches('summary')?null:el,p=li?(li.dataset.path||li.dataset.ghost):el.parentNode.dataset.folderPath;if(!p)return;
  var head=li?(li.querySelector(':scope>a,:scope>.tm-name,:scope>span')||li):el,r=head.getBoundingClientRect();
  out.push({p:p,folder:!li,open:!li&&el.parentNode.open,y:r.top+Math.min(r.height,30)/2});});return out;}
function stateOf(t,row){if(!row.folder)return t.s[row.p]||null;var f=row.p+'/',best=null;
 for(var k in t.s)if(k.indexOf(f)===0){var s=t.s[k];if(best===null||RANK.indexOf(s)<RANK.indexOf(best))best=s;}return best;}
function station(x,y,s,c,small){var r=small?3.5:5;
 if(s==='off')return '<path d="M'+x+' '+(y-r-1)+'l'+(r+1)+' '+(r+1)+'-'+(r+1)+' '+(r+1)+'-'+(r+1)+'-'+(r+1)+'z" fill="#d98a12" stroke="#fff" stroke-width="1.5"/>';
 if(s==='edit')return '<circle class="tm-live" cx="'+x+'" cy="'+y+'" r="'+r+'" fill="#fff" stroke="'+c+'" stroke-width="2.6"/>';
 if(s==='plan')return '<circle cx="'+x+'" cy="'+y+'" r="'+r+'" fill="#fff" stroke="'+c+'" stroke-width="1.8" stroke-dasharray="2 2"/>';
 if(s==='delete')return '<circle cx="'+x+'" cy="'+y+'" r="'+r+'" fill="#fff" stroke="'+c+'" stroke-width="1.8"/><path d="M'+(x-2.5)+' '+(y-2.5)+'l5 5M'+(x+2.5)+' '+(y-2.5)+'l-5 5" stroke="'+c+'" stroke-width="1.5"/>';
 return '<circle cx="'+x+'" cy="'+y+'" r="'+r+'" fill="'+c+'" stroke="#fff" stroke-width="1.5"/>';}
function colw(z,n){var b=WIDE[z],fit=(box.clientWidth-PAD*2-14)/Math.max(1,n-1);return Math.min(b*3,Math.max(b,fit));}  // spread to fill, at most 3x
function draw(){if(wrap.classList.contains('nometro'))return;T=columns();COL=colw(Z,T.length);
 var top=box.getBoundingClientRect().top,R=rows(),st=here.tmState?here.tmState():{on:false,cur:''},W=PAD*2+(T.length-1)*COL+14;
 var H=Math.max(tree.scrollHeight,R.length?R[R.length-1].y-top+20:0),g='',lastDay='';
 T.forEach(function(t,c){var x=PAD+c*COL;
  if(Z!==0&&t.day!==lastDay){g+='<text class="tm-day" x="'+(x-4)+'" y="10">'+esc(t.day)+'</text>';lastDay=t.day;}
  g+='<g class="tm-t'+(st.on&&st.cur===t.k?' on':'')+'" data-k="'+esc(t.k)+'"><title>'+esc(t.t)+'</title><text x="'+x+'" y="40" transform="rotate(-60 '+x+' 40)">'+esc(Z===4?t.hm+' '+String(t.title||'').slice(0,16):t.hm)+'</text></g>';});
 R.forEach(function(row){var y=row.y-top,cs=[];T.forEach(function(t,c){if(stateOf(t,row))cs.push(c);});if(!cs.length)return;
  var live=cs.some(function(c){var s=stateOf(T[c],row);return s==='edit'||s==='plan';}),x1=PAD+cs[0]*COL,x2=live?W-4:PAD+cs[cs.length-1]*COL;
  if(x2>x1)g+='<line x1="'+x1+'" x2="'+x2+'" y1="'+y+'" y2="'+y+'" stroke="'+(row.folder?'#d6d6d1':'#3b3b38')+'" stroke-width="'+(row.folder?2.5:3)+'" stroke-linecap="round"/>';
  if(live&&!row.folder)g+='<path d="M'+x2+' '+(y-4)+'l6 4-6 4z" fill="#3b3b38"/>';});
 T.forEach(function(t,c){var x=PAD+c*COL,ys=R.filter(function(r){return !(r.folder&&r.open)&&stateOf(t,r);}).map(function(r){return r.y-top;}),pick=st.on&&st.cur===t.k;
  if(ys.length>1)g+='<line x1="'+x+'" x2="'+x+'" y1="'+Math.min.apply(0,ys)+'" y2="'+Math.max.apply(0,ys)+'" stroke="'+t.c+'" stroke-width="'+(pick?3:1.4)+'"'+(pick?'':' stroke-dasharray="3 3" opacity=".7"')+'/>';});
 T.forEach(function(t,c){var x=PAD+c*COL;R.forEach(function(r){if(r.folder&&r.open)return;var s=stateOf(t,r);if(!s)return;   // an open folder's files carry its stations
  g+='<g class="tm-st" data-k="'+esc(t.k)+'"><title>'+esc(t.t)+'</title>'+station(x,r.y-top,s,t.c,r.folder&&r.open)+'</g>';});});
 svg.setAttribute('width',W);svg.setAttribute('height',H);svg.innerHTML=g;
 if(first){box.scrollLeft=box.scrollWidth;first=false;}if(typeof ends==='function')ends();}
var raf=0;function soon(){cancelAnimationFrame(raf);raf=requestAnimationFrame(draw);}
here.tmDraw=soon;
svg.addEventListener('click',function(e){var g=e.target.closest('[data-k]');if(!g)return;var k=g.dataset.k;
 if(k.indexOf('b:')===0){var b=T.find(function(c){return c.k===k;});zoom(Z+1,b&&b.first);return;}if(here.tmPick)here.tmPick(k);});
var zin=here.querySelector('.tm-zoom[data-z="1"]'),zout=here.querySelector('.tm-zoom[data-z="-1"]');
function zoom(z,trace){var from=COL,mid=(box.scrollLeft+box.clientWidth/2)/from*colw(z,columns(z).length);Z=z;
 try{localStorage.setItem('wb:metro-level',LEVELS[Z]);}catch(e){}zin.disabled=Z===4;zout.disabled=Z===0;draw();
 if(trace){var C=columns(),i=C.findIndex(function(c){return c.k===trace||c.first===trace||(c.k.indexOf('b:')===0&&bucket(ALL.find(function(t){return t.k===trace;}),Z)===c.t);});
  if(i>=0)mid=PAD+i*COL;}                                   // a bucket click zooms in centred on it
 else if(from<3||Z<3)mid=box.scrollWidth;                       // across bucket levels: the newest end
 box.scrollLeft=Math.max(0,mid-box.clientWidth/2);ends();}
zin.addEventListener('click',function(){if(Z<4)zoom(Z+1);});zout.addEventListener('click',function(){if(Z>0)zoom(Z-1);});
zin.disabled=Z===4;zout.disabled=Z===0;
box.addEventListener('wheel',function(e){if(!(e.ctrlKey||e.metaKey))return;e.preventDefault();          // Ctrl/Cmd + wheel, or a pinch
 if(e.deltaY<0&&Z<4)zoom(Z+1);else if(e.deltaY>0&&Z>0)zoom(Z-1);},{passive:false});
tree.addEventListener('toggle',soon,true);new MutationObserver(soon).observe(tree,{childList:true,subtree:true});
if(window.ResizeObserver){var ro=new ResizeObserver(soon);ro.observe(tree);ro.observe(box);}
function show(on){wrap.classList.toggle('nometro',!on);btn.setAttribute('aria-pressed',on?'true':'false');try{localStorage.setItem('wb:metro',on?'1':'0');}catch(e){}if(on){first=true;soon();}}
btn.addEventListener('click',function(){show(btn.getAttribute('aria-pressed')!=='true');});
var steps=here.querySelectorAll('.tm-step');                    // the strip is as tall as the tree: its own scrollbar is out of sight
function ends(){steps[0].disabled=box.scrollLeft<=0;steps[1].disabled=box.scrollLeft+box.clientWidth>=box.scrollWidth-1;}
steps.forEach(function(b){b.addEventListener('click',function(){box.scrollBy({left:+b.dataset.step*COL*4,behavior:'smooth'});});});
box.addEventListener('scroll',ends);
var down=null,moved=false;                                    // press and drag sideways
box.addEventListener('pointerdown',function(e){if(e.button!==0)return;down={x:e.clientX,l:box.scrollLeft};moved=false;});
window.addEventListener('pointermove',function(e){if(!down)return;var dx=e.clientX-down.x;if(Math.abs(dx)>4){moved=true;box.classList.add('drag');}
 if(moved)box.scrollLeft=down.l-dx;});
window.addEventListener('pointerup',function(){down=null;box.classList.remove('drag');});
box.addEventListener('click',function(e){if(moved){e.stopPropagation();e.preventDefault();moved=false;}},true);   // a drag is not a pick
var split=wrap.querySelector('.tm-split');                   // the line between the tree and the map: drag it, double-click resets
function setw(w){if(w){w=Math.round(Math.max(80,Math.min(w,wrap.clientWidth-127)));wrap.style.setProperty('--tm-left',w+'px');}else wrap.style.removeProperty('--tm-left');soon();}
try{var sw=+localStorage.getItem('wb:tree-width');if(sw)setw(sw);}catch(e){}
split.addEventListener('pointerdown',function(e){if(e.button!==0)return;e.preventDefault();split.setPointerCapture(e.pointerId);split.classList.add('drag');
 var x0=wrap.getBoundingClientRect().left;function mv(ev){setw(ev.clientX-x0);}
 function up(){split.classList.remove('drag');split.removeEventListener('pointermove',mv);split.removeEventListener('pointerup',up);
  try{localStorage.setItem('wb:tree-width',parseInt(wrap.style.getPropertyValue('--tm-left'))||'');}catch(e){}}
 split.addEventListener('pointermove',mv);split.addEventListener('pointerup',up);});
split.addEventListener('dblclick',function(){setw(0);try{localStorage.removeItem('wb:tree-width');}catch(e){}});
try{if(localStorage.getItem('wb:metro')==='0')show(false);}catch(e){}
soon();
})();</script>"""
