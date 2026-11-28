"""A folder as a left tab of a Studio topic: its right side is one fold per file, the file's content inside the fold
(JL 261127: "if it is a folder, in the right content, could we make the right content to have the fold, and content
as well?"). A skill's `ref/` and `scripts/` read this way, so the left lists the skill's top level only.

studio-views.json: {"name": "ref", "folder": "plugins/<plugin>/skills/<layer>/<family>/<skill>/ref"}.
Optional "skip": ["SKILL.md"] leaves those files out.
Nothing is copied: a fold's frame opens the file itself, and only when the fold is opened (LOAD below; the page's own
loader, studio_tabs.SCRIPT, would fetch every file of the folder as soon as the tab shows: a closed fold still has a
box, so its frame counts as seen).
"""
from pathlib import Path

from live import frame

SKIP_SUFFIX = {".pyc", ".pyo", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".pptx", ".docx", ".zip"}


class Folder(str):
    """A folder item's address: the first file's url (so a caller that only wants a link still has one), with the
    folder's files beside it as `.files`, [(name, url)]."""
    files: list = []


def files_of(folder: Path, root: Path, skip=()) -> list:
    """[(name, url)] for the files directly in `folder`, by name; no hidden file, no cache, no picture or archive,
    none named in `skip` (a skill's loose files leave out the SKILL.md and CONSTITUTION.md that have their own tab)."""
    root = Path(root).resolve()
    folder = Path(folder).resolve()
    if not folder.is_dir() or not folder.is_relative_to(root):
        return []
    out = []
    for path in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file() or path.name.startswith((".", "_")) or path.suffix.lower() in SKIP_SUFFIX or path.name in skip:
            continue
        if not path.resolve().is_relative_to(root):          # a link that leaves the SPACE
            continue
        out.append((path.name, frame._file_url(path, root)))
    return out


def folder_item(folder: Path, root: Path, skip=()):
    """The Folder address of `folder`, or None when it has no file to show."""
    files = files_of(folder, root, skip)
    if not files:
        return None
    item = Folder(files[0][1])
    item.files = files
    return item


def folds(title: str, item: Folder) -> str:
    """One fold per file, closed; an opened fold shows the file, fetched on that first open."""
    esc = frame.esc
    return STYLE + LOAD + '<div class="st-folds">' + "".join(
        f'<details class="st-fold"><summary>{esc(name)}</summary>'
        f'<iframe title="{esc(title)} · {esc(name)}" data-fold-src="{esc(url)}"></iframe></details>'
        for name, url in item.files) + "</div>"


STYLE = """<style>
.st-folds{display:flex;flex-direction:column;gap:6px;min-width:0}
.st-fold{border:1px solid var(--line);border-radius:8px;background:var(--paper)}
.st-fold>summary{cursor:pointer;padding:6px 10px;font-size:13.5px;font-weight:500}
.st-fold[open]>summary{border-bottom:1px solid var(--line);color:var(--accent)}
.studio-topic-content .st-fold iframe{border:0;border-radius:0 0 8px 8px;height:480px}
</style>"""

LOAD = """<script>(function(){if(window.stFolds)return;window.stFolds=1;
document.addEventListener('toggle',function(e){var d=e.target;if(!d.classList||!d.classList.contains('st-fold')||!d.open)return;
 var f=d.querySelector('iframe[data-fold-src]');if(f&&!f.hasAttribute('src'))f.src=f.dataset.foldSrc;},true);
})();</script>"""
