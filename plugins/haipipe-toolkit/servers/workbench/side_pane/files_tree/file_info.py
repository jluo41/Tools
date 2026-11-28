"""The Files pane's right-click card: what a file or folder is, where it sits, its last commit, the traces that touched
it, and Open and Copy path.

A file says what it is by its own first words: a Python module's docstring, a Markdown file's `# title` or its
front matter `title:`. A folder says it by its face (`<name>/<name>.md`, `# s03 · How does work climb the ladder?`)
or its README. The card is fetched on a right-click (`?view=focus-file-info&path=`), never on hover; Shift and a
right-click keeps the browser's own menu. The tree itself carries no grey titles on its rows.
"""
from __future__ import annotations

import ast
import re
import subprocess
from pathlib import Path

from live import frame
from live.file_icons import STATE_MARKS, file_icon
from live.ui_parts import FOLDER_ICON


def _head(path: Path, n: int = 4000) -> str:
    try:
        with path.open(encoding="utf-8", errors="replace") as f:
            return f.read(n)
    except OSError:
        return ""


def _first_sentence(text: str) -> str:
    text = " ".join(text.split())
    m = re.match(r"(.+?[.?!])(?:\s|$)", text)
    return (m.group(1) if m else text)[:220]


def what(path: Path) -> str:
    """One line on what this file or folder is, from its own words; '' when it says nothing."""
    if path.is_dir():
        from live.focus_base import face_title
        title = face_title(path / f"{path.name}.md")
        if title:
            return title
        for name in ("README.md", "SKILL.md", f"{path.name}.md"):
            if (path / name).is_file():
                return what(path / name)
        return ""
    text, suffix = _head(path), path.suffix.lower()
    if suffix == ".py":
        try:
            doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8", errors="replace")))
        except (SyntaxError, ValueError, OSError):
            m = re.match(r'\s*(?:"""|\'\'\')(.+?)(?:"""|\'\'\'|\n\n)', text, re.S)
            doc = m.group(1) if m else ""
        return _first_sentence(doc or "")
    if suffix == ".md":
        m = re.search(r"^title:\s*(.+)$", text.split("---", 2)[1], re.M) if text.startswith("---") and text.count("---") >= 2 else None
        if m:
            return m.group(1).strip().strip("\"'")
        m = re.search(r"^#\s+(.+)$", text, re.M)
        if m:
            return m.group(1).split(" · ", 1)[-1].strip()
    return ""


def _git(root: Path, *args) -> str:
    try:
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def commit(path: Path, root: Path) -> tuple[str, bool]:
    """(last commit 'YYYY-MM-DD subject', whether the path has changes not committed)."""
    rel = frame.rel(path, root)
    last = _git(root, "log", "-1", "--format=%cs %s", "--", rel)
    return last, bool(_git(root, "status", "--porcelain", "--", rel))


def traces(path: Path, root: Path, most: int = 3) -> list[tuple[str, str, str]]:
    """(state, 'HH:MM title', MM-DD) of the newest traces whose plan or changed list holds this path (or a path under
    this folder), from the Block the path sits in and every Block in its Project's work/."""
    from live import trace_view
    rel = frame.rel(path, root)
    found = []
    for face in sorted(root.glob("examples/*/*/*/trace/[0-9]*/[0-9]*_*.md"), reverse=True):
        meta = trace_view.read(face)
        if not meta:
            continue
        paths = {str(i.get("path", "")).strip() for i in meta.get("plan") or [] if isinstance(i, dict)}
        paths |= {str(p).strip() for p in meta.get("changed") or []}
        if any(p == rel or p.startswith(rel + "/") for p in paths):
            rows = trace_view.states(meta, root, keep=True)
            day, hhmm = face.parent.name, face.stem[:4]
            found.append((trace_view.overall(meta, rows),
                          f"{hhmm[:2]}:{hhmm[2:]} {meta.get('title') or face.stem}", f"{day[2:4]}-{day[4:6]}"))
        if len(found) >= most:
            break
    return found


def card(path: Path, root: Path) -> str:
    """The card's HTML for one path; '' outside the SPACE."""
    path = path.resolve()
    if not (path == root or root in path.parents) or not path.exists():
        return ""
    from live.work_files import file_node, folder_url
    icon = FOLDER_ICON if path.is_dir() else file_icon(path)
    line = what(path)
    last, dirty = commit(path, root)
    rel = frame.rel(path, root)
    rows = "".join(f'<li>{STATE_MARKS[s]}<span>{frame.esc(t)}</span><small>{frame.esc(d)}</small></li>'
                   for s, t, d in traces(path, root))
    dot = '<b title="not committed">●</b> ' if dirty else ""
    when = f'<p class="fi-git">{dot}{frame.esc(last)}</p>' if last or dirty else ""
    href = folder_url(path, root) if path.is_dir() else file_node(path, root).split('href="', 1)[1].split('"', 1)[0]
    return (f'<div class="fi-head"><span aria-hidden="true">{icon}</span><b>{frame.esc(path.name)}</b>'
            f'<button type="button" class="fi-x" data-fi="close" aria-label="Close">✕</button></div>'
            + (f'<p class="fi-what">{frame.esc(line)}</p>' if line else "")
            + f'<code class="fi-path">{frame.esc(rel)}</code>' + when
            + (f'<ul class="fi-traces">{rows}</ul>' if rows else "")
            + f'<p class="fi-do"><a href="{href}" target="_blank" rel="noopener">Open ↗</a>'
            f'<button type="button" data-fi="copy" data-path="{frame.esc(rel)}">📋 Copy path</button></p>')


CARD = '''<style>
.fi-card{position:fixed;z-index:950;width:290px;max-width:calc(100vw - 24px);background:var(--bg,#fff);color:var(--text,#1d1d1b);
 border:1px solid var(--line);border-radius:10px;box-shadow:0 12px 32px rgba(0,0,0,.16);padding:10px 12px;font-size:12px;line-height:1.45}
.fi-card[hidden]{display:none}
.fi-head{display:flex;align-items:center;gap:6px;font-size:13px}.fi-head svg{flex:none}.fi-head b{flex:1}
.fi-x{border:0;background:none;color:var(--muted);cursor:pointer;padding:2px 4px;border-radius:5px}.fi-x:hover{color:var(--text)}
.fi-do{display:flex;gap:10px;align-items:center;margin:8px 0 0;padding-top:6px;border-top:1px solid var(--line)}
.fi-do a{color:var(--accent,#1f5fbf)}.fi-do button{border:1px solid var(--line);background:none;border-radius:6px;padding:2px 8px;font:inherit;font-size:12px;cursor:pointer;color:var(--text)}
.fi-what{margin:6px 0 4px}.fi-path{display:block;font:11px/1.4 ui-monospace,Menlo,monospace;color:var(--muted);overflow-wrap:anywhere;user-select:all}
.fi-git{margin:6px 0 0;color:var(--muted)}.fi-git b{color:#d98a12}
.fi-traces{list-style:none;margin:6px 0 0;padding:6px 0 0;border-top:1px solid var(--line)}
.fi-traces li{display:flex;align-items:center;gap:6px;margin:3px 0}.fi-traces span{flex:1}.fi-traces small{color:var(--muted)}
</style><script>(function(){
if(window.__fileCard)return;window.__fileCard=1;
var box=document.createElement('div');box.className='fi-card';box.hidden=true;box.setAttribute('role','dialog');box.setAttribute('aria-label','File');document.body.appendChild(box);
var cache={},on=null;
var ROW='.file-tree li.file-leaf[data-path], .file-tree details.file-branch[data-folder-path]>summary';
function pathOf(row){return row.matches('li')?row.dataset.path:row.parentNode.dataset.folderPath;}
function place(x,y){var w=box.offsetWidth,h=box.offsetHeight;
 box.style.left=Math.min(Math.max(8,x),innerWidth-w-8)+'px';box.style.top=(y+h>innerHeight-8?Math.max(8,y-h):y)+'px';}
function show(row,x,y){var p=pathOf(row);if(!p)return;on=row;
 var put=function(html){if(on!==row)return;if(!html){hide();return;}box.innerHTML=html;box.hidden=false;place(x,y);};
 if(p in cache)return put(cache[p]);
 fetch('/_board/workbench?view=focus-file-info&path='+encodeURIComponent(p)).then(function(r){return r.ok?r.text():'';})
  .then(function(t){cache[p]=t;put(t);}).catch(function(){});}
function hide(){on=null;box.hidden=true;}
document.addEventListener('contextmenu',function(e){if(e.shiftKey)return;             // shift: the browser's own menu
 var row=e.target.closest&&e.target.closest(ROW);if(!row)return;
 e.preventDefault();e.stopImmediatePropagation();show(row,e.clientX+4,e.clientY+4);},true);
box.addEventListener('click',function(e){var b=e.target.closest('[data-fi]');if(!b)return;
 if(b.dataset.fi==='close')return hide();
 if(b.dataset.fi==='copy'){copy(b.dataset.path);b.textContent='✓ Copied';}});
function copy(text){if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(text).catch(function(){old(text);});return;}
 old(text);}                                                    // plain http has no clipboard: a hidden text box, as ui_parts does
function old(text){var t=document.createElement('textarea');t.value=text;t.setAttribute('readonly','');t.style.position='fixed';
 t.style.top='-1000px';document.body.appendChild(t);t.select();try{document.execCommand('copy');}catch(e){}document.body.removeChild(t);}
document.addEventListener('click',function(e){if(!box.hidden&&!box.contains(e.target))hide();});
document.addEventListener('scroll',function(e){if(!box.contains(e.target))hide();},true);
window.addEventListener('blur',hide);
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!box.hidden&&!e.defaultPrevented){e.preventDefault();hide();}});
})();</script>'''
