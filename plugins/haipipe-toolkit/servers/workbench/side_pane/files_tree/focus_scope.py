"""The page's own folder in the 📁 file tree (JL 261125: "how could I highligth the related files and folder for this
specific folder ... what is out of this job's scope, we can make them to be transparent"): the open page's folder is
marked, what lies inside it reads as usual, and every row outside it (sibling Jobs, the Block's records/, runs/, ...)
fades. The folders on the way down to it stay plain, so the path still reads. Rows are matched by their folder path
(`data-folder-path` on a branch, the branch's path plus the name on a file), so the tree's writer does not change.

What a Job, Task, Studio or chat folder is about (its face's short title) is no longer grey text on its row: the hover
card says it (side_pane/files_tree/file_info.py; JL 261125: "we don't wnat this as well, this will be hover over")."""
from __future__ import annotations

import json
import re
from pathlib import Path

STYLE = """<style>
.file-tree .fixed-folder .sc-out{opacity:.32;transition:opacity .15s}.file-tree .fixed-folder .sc-out:hover{opacity:.85}
.file-tree .sc-here{background:color-mix(in srgb,var(--accent) 12%,transparent);border-radius:6px;font-weight:600}
</style>"""

SCRIPT = """<script>
(function(){if(window.__scopeOn)return;window.__scopeOn=1;var F=window.__scopePage||'',W=null,until=0;
function inside(p,f){return p===f||p.indexOf(f+'/')===0;}
function mark(row,p){if(!row||!p)return;row.classList.remove('sc-out','sc-here');
 var want=W||(F?[F]:[]);if(!want.length)return;
 if(want.indexOf(p)>=0)row.classList.add('sc-here');
 else if(!want.some(function(w){return inside(p,w)||w.indexOf(p+'/')===0;}))row.classList.add('sc-out');}   // inside it, or on the way down
function fold(){if(!W||Date.now()>until)return;   // a right-click on the page: every folder closes but the way to its folders
 document.querySelectorAll('.file-tree details.file-branch[data-folder-path]').forEach(function(d){var f=d.dataset.folderPath;
  var way=W.some(function(w){return inside(w,f);});
  if(way&&!d.open){d.open=true;setTimeout(function(){if(d.open&&d.dataset.folderSrc&&!d.dataset.loaded&&!d.dataset.loading)d.dispatchEvent(new Event('toggle'));},120);}
  else if(!way&&d.open)d.open=false;});}
function run(){fold();document.querySelectorAll('.file-tree details.file-branch[data-folder-path]').forEach(function(d){
  mark(d.querySelector(':scope>summary'),d.dataset.folderPath);});
 document.querySelectorAll('.file-tree li.file-leaf>a').forEach(function(a){
  var d=a.closest('details.file-branch[data-folder-path]');
  mark(a,d?d.dataset.folderPath+'/'+a.textContent.trim():'');});}
window.__scopeFocus=function(p){if(!p)return;W=[p].concat((window.__scopeOwns||{})[p]||[]);until=Date.now()+4000;run();
 setTimeout(function(){var h=document.querySelector('.file-tree .sc-here');if(h)h.scrollIntoView({block:'center'});},400);};
run();var t;new MutationObserver(function(){clearTimeout(t);t=setTimeout(run,30);})   // folders load as they open
 .observe(document.body,{childList:true,subtree:true});
})();
</script>"""


def block_of(folder: Path, root: Path) -> Path:
    """The Block the page sits in (the nearest bNN_ folder up), else the page's own folder."""
    for p in (folder, *folder.parents):
        if p == root or root not in p.parents and p != root:
            break
        if re.match(r"^b\d\d_", p.name):
            return p
    return folder


def owns(block: Path, root: Path) -> dict:
    """{Task folder: [folders its face's ## Files names]}: the code a Task owns, opened with it on a right-click
    (t01_files_tree names side_pane/files_tree/)."""
    out = {}
    for face in block.glob("j[0-9]*_*/t[0-9]*_*/t[0-9]*_*.md"):
        if face.stem != face.parent.name:
            continue
        part = re.search(r"(?ms)^## Files\s*\n(.*?)(?=^## |\Z)", face.read_text(encoding="utf-8", errors="ignore"))
        paths = [p.rstrip("/") for p in re.findall(r"`([\w./-]+/)`", part[1])] if part else []
        found = [p for p in paths if (root / p).is_dir()]
        if found:
            out[face.parent.relative_to(root).as_posix()] = found
    return out


def assets(folder: Path, root: Path) -> str:
    """The scope marks for one page: its folder, relative to the SPACE root, and what each Task of its Block owns."""
    rel = folder.relative_to(root).as_posix() if folder != root else ""
    block = block_of(folder, root)
    return (STYLE + f"<script>window.__scopePage={json.dumps(rel)};"
            f"window.__scopeOwns={json.dumps(owns(block, root) if block != root else {})};</script>" + SCRIPT)
