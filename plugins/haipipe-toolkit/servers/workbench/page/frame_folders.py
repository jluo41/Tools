"""Studio > Folder: what a Block's folders and files hold, as rows."""

from __future__ import annotations

import datetime
import re
from pathlib import Path

from live.frame_base import _e, _file_url, _rel, _title, chain, face, pop
from live.frame_studio import _draw_url
from live.frame_delivery import _size
from live.frame_sessions import touched_set


FOLDER_SKIP = {"__pycache__", "node_modules", ".ipynb_checkpoints"}
# what a folder of a Block holds, for the names every Block shares (haipipe-block); any other folder says its face's title
FOLDER_WORDS = {"studio": "the Studio: a folder per topic", "reports": "the Questions: a folder each, with its report",
                "runs": "the Runs: a folder each", "related": "what came in from outside, kept as it came",
                "delivery": "what was built to send", "passes": "the sessions, one folder each",
                "result": "what the Run produced", "history": "older copies, kept"}
FILE_ICONS = {".md": "📝", ".excalidraw": "✏️", ".png": "🖼️", ".jpg": "🖼️", ".jpeg": "🖼️", ".gif": "🖼️", ".svg": "🖼️",
              ".webp": "🖼️", ".pdf": "📕", ".py": "🐍", ".ipynb": "📓", ".yaml": "⚙️", ".yml": "⚙️", ".json": "🧾",
              ".csv": "📊", ".tsv": "📊", ".parquet": "📊", ".sh": "▶️", ".docx": "📘", ".pptx": "📙", ".eml": "✉️",
              ".tex": "📜", ".bib": "📚", ".html": "🌐", ".txt": "📄", ".log": "📄"}


def _when(t: float) -> str:
    d = datetime.datetime.fromtimestamp(t)
    return d.strftime("%d %b" if d.year == datetime.date.today().year else "%d %b %Y")


def _shown(p: Path) -> bool:
    return not p.name.startswith(".") and p.name not in FOLDER_SKIP


def _run_word(folder: Path) -> str:
    """A Run folder's one line from its card: `soft · draw · done · 10 passes`; '' without run.yaml."""
    try:
        card = (folder / "run.yaml").read_text(encoding="utf-8", errors="ignore")[:4000]
    except OSError:
        return ""
    get = lambda k: (re.search(rf"(?m)^{k}:[ \t]*(.+)$", card) or [None, ""])[1].strip()
    n = len(re.findall(r"(?m)^- p\d+-", card))
    return " · ".join(x for x in (get("kind"), get("type").strip("[]").replace(",", " +"), get("status"),
                                  f"{n} pass{'es' if n != 1 else ''}" if n else "") if x and x != "null")


def folder_word(p: Path) -> str:
    """What a folder is for, in one line: a shared name's fixed line, a Run's card, else its face's title; '' when
    that would only repeat the folder's name (b10 s09-D13)."""
    word = FOLDER_WORDS.get(p.name) or _run_word(p)
    if not word and (md := face(p)):
        word = _title(md)
    return "" if word == p.name else word


def folder_rows(folder: Path, root: Path, most: int | None = 300) -> str:
    """One folder's rows for Studio › Folder (b10 s09): its folders first, then its files, by name. A folder
    folds, says how many things it holds and what it is for, and its rows load when it is opened
    (`?view=dir&path=`), so a Block of thousands of files stays light (b00_rawdata: 5,317). A file opens in the
    pop-out and says its size and the day it last changed. Past `most` rows, a button loads the rest (None:
    all). Dotfiles and caches are left out, and a link that leaves the root is named but not followed."""
    try:
        kids = sorted((p for p in folder.iterdir() if _shown(p)), key=lambda p: (not p.is_dir(), p.name.casefold()))
    except OSError:
        return '<li class=mut>This folder could not be read.</li>'
    rows, top = [], root.resolve()
    block = chain(folder, root).get("Block")
    marked = touched_set(block) if block else set()      # 🧵: an episode touched it (Studio › Sessions)

    def thread(p: Path) -> str:
        return (f'<button type=button class=fd-th data-th="{_e(_rel(p, root))}" title="Sessions">🧵</button>'
                if p.resolve() in marked else "")

    for p in kids[:most]:
        if not p.resolve().is_relative_to(top):
            rows.append(f'<li class=fd-file><span class=fd-row><span class=fd-i>🔗</span>{_e(p.name)}'
                        f'<span class=fd-n>a link outside this root</span></span></li>')
            continue
        rel = _rel(p, root)
        if p.is_dir():
            try:
                n = sum(1 for c in p.iterdir() if _shown(c))
            except OSError:
                n = 0
            word = folder_word(p)
            rows.append(f'<li class=fd-dir><details data-dir="{_e(rel)}"><summary class=fd-row title="{_e(rel)}/">'
                        f'<span class=fd-name>{_e(p.name)}/</span><span class=fd-n>{n}</span>'
                        + (f'<span class=fd-word>{_e(word)}</span>' if word else "") + thread(p)
                        + '</summary><ul></ul></details></li>')
            continue
        try:
            st = p.stat()
        except OSError:
            continue
        href = _draw_url(p, root) if p.suffix == ".excalidraw" else _file_url(p, root)
        rows.append(f'<li class=fd-file><span class=fd-row title="{_e(rel)}"><span class=fd-i>'
                    f'{FILE_ICONS.get(p.suffix.lower(), "📄")}</span>{pop(href, p.name)}'
                    f'<span class=fd-n>{_size(st.st_size)}</span><span class=fd-when>{_when(st.st_mtime)}</span>{thread(p)}</span></li>')
    if most is not None and len(kids) > most:
        rows.append(f'<li class=fd-more><button type=button data-dir="{_e(_rel(folder, root))}">'
                    f'Show the other {len(kids) - most}</button></li>')
    return "".join(rows) or '<li class=mut>Empty.</li>'


def studio_folder(block: Path, root: Path) -> str:
    """The Studio's sixth folding part, Folder, under Timeline (b10 s09-block-folder; JL 261012: "在 related 和 timeline 下面
    再搞一个 folder，这样我就可以看到这些 folder 里面（也就是这个 block 的 folder）都长什么内容"): the Block's own
    folder as a tree. Its first level is drawn here; each folder's rows load when it is opened."""
    rel = _rel(block, root)
    return (f'<details class="studio-related studio-folder" id=studio-folder><summary><b>Folder</b></summary>'
            f'<div class=related-in><p class=fd-root>{_e(rel)}/</p>'
            f'<ul class=fd-tree>{folder_rows(block, root)}</ul></div></details>')
