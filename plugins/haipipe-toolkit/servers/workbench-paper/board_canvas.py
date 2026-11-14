"""A paper Board's canvases: a topic's mind map to work on, a drawing shown live (live_canvas, JUMP_JS), a Board
topic's drawing (_topic_canvas) and the venue's display examples."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import esc
from live.ui_parts import _open_btn


def _canvas(topic: Path, root: Path) -> str:
    """The topic's mind map as the canvas to work on, edited in place where it is read (JL 261102: "I think we should
    have the mindmap canvas to work on"): the same map and endpoint as the topic card's Structured side."""
    from live import frame
    mind = topic / f"{topic.name}.mindmap.md"
    if not mind.is_file():
        return (f'<p class=pb-state>No mind map yet: <code>mindmap.py from-topic {esc(topic.name)}</code> '
                f'(haipipe-mindmap) makes {esc(mind.name)}.</p>')
    try:
        html = frame.mindmap_module().fragment(mind, ds._rel(mind, root), editable=not frame.READ_ONLY_MAPS,
                                               url_of=lambda q: "/" + quote(ds._rel(q, root)))
        # a map not written yet says so by its state word, never by a grey instruction on its root (r03: "Not written
        # yet: ask in the Studio chat…" on Idea's and Story's roots); its root line stays there to type into
        html = re.sub(r'(<p data-edit=arc data-raw=")Not written yet[^"]*("[^>]*>)Not written yet[^<]*(</p>)', r"\1\2\3", html)
        return '<div class=pb-map>' + html + '</div>'
    except Exception as e:                          # a map that fails to read says so, never a blank view
        return f'<p class=pb-state>The mind map did not read: {esc(str(e))}</p>'


LIVE_CSS = ("<style>.pb-live{position:relative;margin:0 0 8px}.pb-live iframe{display:block;width:100%;height:70vh;min-height:420px;"
            "border:1px solid var(--line);border-radius:6px;background:#fff}.pb-live .pb-livepng{display:none}"
            ".pb-jumps{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 8px}.pb-jump{font-size:12.5px;border:1px solid var(--line);"
            "border-radius:14px;padding:2px 10px;background:var(--paper);color:var(--ink);cursor:pointer}.pb-jump.on{border-color:var(--accent);"
            "color:var(--accent);background:var(--soft)}"
            "@media(max-width:700px){.pb-jumps{display:none}.pb-live iframe{display:none}.pb-live .pb-livepng{display:block;max-width:100%;"
            "border:1px solid var(--line);border-radius:6px}}</style>")


def live_canvas(drawing: Path, root: Path, title: str = "", png: Path | None = None) -> str:
    """A drawing shown live and read-only, the Studio's embed (`/_excalidraw/?board=…`, xcal-boot.js: the hand tool,
    pan and zoom), opened at its width, top first, its drawing tools off (`fit=width&bare=1`), with Draw to edit it
    (JL 261111: "how could we make this to the canvas, and the item is also clickable"); a card's Excalidraw `link`
    opens its page. A drawing in named frames (one area per paper) gets a jump button per frame and opens on the first
    (JL 261111: "I want each abstract to be a area"); on a phone, its picture instead."""
    import json
    from live import frame
    if drawing is None or not drawing.is_file():
        return ""
    png = png if png is not None else drawing.with_suffix(".png")
    try:
        frames = [e.get("name") for e in json.loads(drawing.read_text(encoding="utf-8")).get("elements", [])
                  if e.get("type") == "frame" and not e.get("isDeleted") and e.get("name")]
    except Exception:
        frames = []
    base = frame._draw_url(drawing, root) + "&fit=width&bare=1"
    src = base + (f"&focus={quote(frames[0])}" if frames else "")
    jumps = ""
    if len(frames) > 1:
        jumps = ('<div class=pb-jumps>' + "".join(
            f'<button type=button class="pb-jump{" on" if k == 0 else ""}" data-src="{esc(base + "&focus=" + quote(n))}">{esc(n)}</button>'
            for k, n in enumerate(frames))
            + f'<button type=button class=pb-jump data-src="{esc(base)}">Whole drawing</button></div>')
    pic = (f'<img class=pb-livepng src="/{esc(quote(ds._rel(png, root)))}" alt="{esc(title or drawing.stem)}" loading=lazy>'
           if png.is_file() else "")
    return (LIVE_CSS + f'<div class=pb-verbs>{_open_btn("Draw", frame._draw_url(drawing, root, True), title or drawing.stem)}</div>'
            + jumps + f'<div class=pb-live><iframe title="{esc(title or drawing.stem)}" src="{esc(src)}" '
            f'loading=lazy referrerpolicy=no-referrer></iframe>{pic}</div>' + (JUMP_JS if jumps else ""))


JUMP_JS = ("<script>if(!window.__pbJump){window.__pbJump=1;document.addEventListener('click',function(e){"
           "var b=e.target.closest('.pb-jump');if(!b)return;var box=b.parentNode;var f=box.nextElementSibling&&"
           "box.nextElementSibling.querySelector('iframe');if(!f)return;f.src=b.dataset.src;"
           "box.querySelectorAll('.pb-jump').forEach(function(x){x.classList.toggle('on',x===b);});});}</script>")


def _topic_canvas(board: Path, root: Path, slug: str) -> str:
    """A Board topic `sNN-<slug>` shown as its drawing only, live (live_canvas); its picture when it has no
    .excalidraw. Empty when the topic or its drawing is missing."""
    topic = next((t for t in sorted(board.glob(f"s[0-9]*-{slug}")) if t.is_dir()), None)
    if topic is None:
        return ""
    png, drw = topic / f"{topic.name}.png", topic / f"{topic.name}.excalidraw"
    if drw.is_file():
        return live_canvas(drw, root, topic.name, png)
    if not png.is_file():
        return ""
    return (f'<a data-pop="{esc(topic.name)}" href="/{esc(quote(ds._rel(png, root)))}"><img src="/{esc(quote(ds._rel(png, root)))}" '
            f'alt="{esc(topic.name)}" loading=lazy style="display:block;max-width:100%;border:1px solid var(--line);'
            'border-radius:6px"></a>')


def _display_examples(board: Path, root: Path) -> str:
    """3 · Examples: the displays of the target venue's papers on one canvas, to compare with ours (JL 261102: "what I
    want is just one excalidraw and put all other papers's displays only ... no more text here"): the Board's
    `sNN-paper-display-examples` drawing only."""
    return _topic_canvas(board, root, "paper-display-examples")
