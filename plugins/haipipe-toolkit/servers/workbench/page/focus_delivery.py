"""The focus page's Delivery: delivery tabs and lanes, live pages, a topic's rendered pieces."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlencode

from live import frame
from live.ui_parts import PB_JS, _side_tabs
from live.focus_base import (document, inside, is_topic, markdown, origin, page_level, page_module, page_url,
    rollup)
from live.focus_styles_bands import side_css


def own_delivery_tabs(theme: str, folder: Path, root: Path, level: str) -> list:
    """A page's own 📦 Delivery tabs in place of the shared lanes, from its page_module's `delivery_tabs` (a Question Book:
    each release and the files a Board Job pins); else the shared lanes (delivery_tabs)."""
    mod, prefix = page_module(theme, folder, root)
    fn = getattr(mod, prefix + "delivery_tabs", None) if mod is not None else None
    try:
        own = [tuple(x) for x in fn(folder, root, level) or []] if fn else []
    except Exception:
        own = []
    return own or delivery_tabs(folder, root)


def live_page_blocks(folder: Path) -> list:
    """The Blocks whose live pages can be at this page or below: those it rolls up, and the one above it."""
    blocks = [p for p in rollup(folder) if frame.level_of(p) == "Block"]
    above = frame._block_above(folder)
    return blocks + ([above] if above and above not in blocks else [])


def live_pages_html(folder: Path, root: Path) -> str:
    """A closed card per deliverable with a `url:` at this page or below (frame._live_pages reads the Job's face); opened,
    the page itself in a frame, loaded only then; a page on another host gets only its link."""
    below = rollup(folder)
    cards = []
    for block in live_page_blocks(folder):
        for i in frame._live_pages(block):
            if i["folder"] not in below:
                continue
            href = frame.live_url(i, root)
            url, title = frame.esc(href), frame.esc(i["title"])
            where = origin(i["folder"], folder)
            frame_ = (f'<iframe title="{title}" data-src="{url}" referrerpolicy=no-referrer '
                      f'style="width:100%;height:85vh;border:1px solid var(--line,#ddd)"></iframe>'
                      if href.startswith("/") else "")
            cards.append(f'<details class=live-page ontoggle="var f=this.querySelector(\'iframe\');'
                         f'if(this.open&&f&&!f.src)f.src=f.dataset.src"><summary><b>{title}</b>'
                         f'{" <span class=mut>" + frame.esc(where) + "</span>" if where else ""} '
                         f'<span class=mut>live page</span> '
                         f'<a href="{url}" target=_blank rel=noopener>own tab ↗</a></summary>{frame_}</details>')
    return f'<section class="delivery-part">{"".join(cards)}</section>' if cards else ""


def block_delivery_part(folder: Path) -> Path | None:
    """A Job's or Task's own part of its Block's delivery: haipipe-delivery files what a Job or Task hands over under
    `<Block>/delivery/<job>/[<task>/]` (261106: a Job's or Task's Delivery was empty while its Block's held its files)."""
    level = page_level(folder)
    if level not in ("Job", "Task"):
        return None
    job = folder if level == "Job" else folder.parent
    part = job.parent / "delivery" / job.name / ("" if level == "Job" else folder.name)
    return part if part.is_dir() else None


def delivery_sources(folder: Path, root: Path) -> list:
    """[(delivery folder, where)]: the page's own delivery/ and its children's, then its part of its Block's."""
    out = [(source / "delivery", origin(source, folder) or "this page") for source in rollup(folder)]
    part = block_delivery_part(folder)
    if part is not None:
        out.append((part, "this page"))
    return [(d, w) for d, w in out if d.is_dir() and inside(d, root)]


def delivery_html(folder: Path, root: Path) -> str:
    """The page's live pages (JL 261104: a page a host serves, e.g. the food API's try page, seen and used right here),
    then each level's delivery/, the page's own first, then its children's: its table (delivery.md) or its files; a Job
    or a Task also its part of its Block's delivery/ (block_delivery_part)."""
    out = [live_pages_html(folder, root)]
    level = page_level(folder)
    mod, prefix = page_module(frame.theme_of(folder, root), folder, root) if level in ("Block", "Job", "Task") else (None, "")
    if mod is not None and hasattr(mod, prefix + "delivery_tabs"):   # a page's own handover (a Question Book's releases;
        tabs = own_delivery_tabs(frame.theme_of(folder, root), folder, root, level)   # round 2, 261108: its rail said
        out.append(side_css() + _side_tabs("rDx", [(t[0], t[1]) for t in tabs], [t[2] for t in tabs]) + PB_JS)   # "Nothing
    for deliv, where in delivery_sources(folder, root):   # handed over yet" beside its signed release)
        table = deliv / "delivery.md"
        files = sorted(p for p in deliv.iterdir() if not p.name.startswith("."))
        if not table.is_file() and not files:        # an empty delivery/ a scaffold made says nothing (261108: "Empty.")
            continue
        if table.is_file():
            body = markdown(table.read_text(encoding="utf-8", errors="replace"), deliv, root)
        else:
            body = "<ul>" + "".join(f'<li><a href="{frame.esc(frame._file_url(p, root))}" target=_blank rel=noopener>'
                                    f'{frame.esc(p.name)}</a></li>' for p in files) + "</ul>" if files else '<p class="mut">Empty.</p>'
        out.append(f'<section class="delivery-part"><h3 class="focus-sub">{frame.esc(where)}</h3>{body}</section>')
    return "".join(out)


PICTURES = {".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp"}


def delivered_picture(q: Path, root: Path) -> str:
    """A delivered picture shows as itself, opening in the pop-out (round 1, 261106: "preview the delivered figure in
    Delivery: its picture, opening in the pop-out"); the list item is closed by its caller."""
    url = frame.esc(frame._file_url(q, root))
    return (f'<li class=dl-pic><a data-pop="{frame.esc(q.name)}" href="{url}" target=_blank rel=noopener>'
            f'<img src="{url}" alt="{frame.esc(q.stem.replace("_", " ").replace("-", " "))}" loading=lazy '
            f'style="display:block;max-width:min(100%,360px);max-height:220px;border:1px solid var(--line);border-radius:6px">'
            f'{frame.esc(q.name)}</a>')


DELIVERY_LANES = (("Models", ("model", "models", "checkpoint", "checkpoints"), "a model it hands over"),
                  ("Data", ("data", "dataset", "datasets"), "a dataset it hands over"),
                  ("Website", ("web", "website", "site"), "a site or page it hands over"))


def delivery_tabs(folder: Path, root: Path) -> list:
    """[(tab, line, panel)]: what a Block hands over, by kind (JL 261104: "in case we will delivery some models or data or
    website"), each tab always there and saying where its files go; then every file, when there are any. A lane is
    delivery/<lane>/, or the same under a Job's or a Task's address (haipipe-delivery)."""
    delivs = [d for d, _ in delivery_sources(folder, root)]
    only = {}                                    # a Job: the Block's sends its delivery.md says came from this Job
    above = folder.parent / "delivery" / "delivery.md"
    if page_level(folder) == "Job" and above.is_file():
        names = set(re.findall(r"`([^`\n]+)`[^|\n]*\bfrom " + re.escape(folder.name) + r"\b",   # a name never spans lines
                               above.read_text(encoding="utf-8", errors="ignore")))   # (261106: a backtick in the intro hid a row)
        if names:
            delivs.append(above.parent)
            only[above.parent] = names
    tabs = []
    for name, words, what in DELIVERY_LANES:
        rows, shown = [], set()
        for deliv in delivs:
            for lane in [p for pat in ("*", "j[0-9]*/*", "j[0-9]*/t[0-9]*/*", "t[0-9]*/*") for p in sorted(deliv.glob(pat))]:
                if lane.is_dir() and lane.name.lower() in words:
                    where = lane.parent.relative_to(deliv).as_posix()
                    files = [q for q in sorted(lane.iterdir()) if not q.name.startswith(".")
                             and (deliv not in only or q.relative_to(deliv).as_posix() in only[deliv])]
                    shown |= {frame._file_url(q, root) for q in files}
                    rows += [(delivered_picture(q, root) if q.suffix.lower() in PICTURES else
                              f'<li><a href="{frame.esc(frame._file_url(q, root))}" target=_blank rel=noopener>{frame.esc(q.name)}</a>')
                             + (f' <small>{frame.esc(where)}</small>' if where != "." else "") + '</li>' for q in files]
        if name == "Website":                    # a live page is embedded once, in 🌐 Service; here only its link
            below = rollup(folder)
            rows += [f'<li><a href="{frame.esc(frame.live_url(i, root))}" target=_blank rel=noopener>{frame.esc(i["title"])}</a>'
                     f' <small>live page</small></li>' for block in live_page_blocks(folder) for i in frame._live_pages(block)
                     if i["folder"] in below and frame.live_url(i, root) not in shown]
        panel = f'<ul class=find-r>{"".join(rows)}</ul>' if rows else ""
        # an empty lane draws nothing (AGENTS.md § Page words); where a delivery goes is haipipe-delivery's to say
        tabs.append((name, "ready" if panel else "nothing yet", panel))
    # no "All files" tab: it drew the whole Delivery section again inside Findings (round 3); the rail's Delivery has it
    return tabs


def service_section(folder: Path, root: Path) -> str:
    """Findings' 🌐 Service (JL 261104: "a new section named service, and each tab is a website, embedded there"): a side
    tab per live page at this page or below, the site itself on the right, working; a frame loads when its tab first
    shows, so a closed section costs nothing."""
    below = rollup(folder)
    pages = [i for block in live_page_blocks(folder) for i in frame._live_pages(block) if i["folder"] in below]
    if not pages:
        return ""
    panels = []
    for i in pages:
        href = frame.live_url(i, root)
        url, name = frame.esc(href), frame.esc(i["service"])
        site = (f'<iframe title="{name}" data-src="{url}" referrerpolicy=no-referrer '
                f'style="width:100%;height:80vh;border:1px solid var(--line,#ddd);border-radius:6px"></iframe>'
                if href.startswith("/") else "")
        panels.append(f'<div class=find-verbs><a href="{url}" target=_blank rel=noopener>Own tab ↗</a></div>{site}')
    script = ("<script>(function(){var w=document.getElementById('find-service'),s=w.closest('details');"
              "function load(){if(s.open)w.querySelectorAll('.pb-panel:not([hidden]) iframe[data-src]:not([src])')"
              ".forEach(function(f){f.src=f.dataset.src})}"
              "s.addEventListener('toggle',load);w.addEventListener('click',function(){setTimeout(load)});load()})()</script>")
    return ('<div id=find-service>' + _side_tabs("fSx", [(i["service"], i["title"]) for i in pages], panels)
            + '</div>' + script)


# a piece's state from render_delivery.py, in words a reader acts on, and its mark
PIECE_STATE = {"same": ("✅", "in place"), "rendered": ("✅", "in place"), "differs": ("⬜", "changed, not rendered yet"),
               "not placed": ("❗", "not placed"), "no source": ("❗", "its source is missing"),
               "code": ("", "built by a Run"), "theme": ("", "built by its Theme's skill")}


READ_AS_TEXT = {".json", ".yaml", ".yml", ".txt", ".py", ".tex", ".csv", ".tsv", ".bib", ".js", ".css", ".sh", ".ps1", ".do"}


def readable(path: Path | None, root: Path) -> str:
    """A file opened in place, under its row (JL 261030: "怎么能直接把每个 file 展开来读一下呢"): Markdown drawn, other
    text as it is, a picture shown; a web page, a Word file or a PDF opens in a new tab."""
    if not path or not path.is_file() or not inside(path, root):
        return '<p class="mut">Nothing to read here yet.</p>'
    url = ("/" + frame.rel(path, root)) if path.suffix == ".html" else frame._file_url(path, root)
    opener = f'<p><a class="row-verb" href="{frame.esc(url)}" target=_blank rel=noopener>Open {frame.esc(path.name)}</a></p>'
    if path.suffix == ".md":
        return markdown(path.read_text(encoding="utf-8", errors="replace")[:60000], path.parent, root)
    if path.suffix.lower() in READ_AS_TEXT:
        return f'<pre>{frame.esc(path.read_text(encoding="utf-8", errors="replace")[:60000])}</pre>'
    if path.suffix.lower() in (".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp"):
        return f'<img src="{frame.esc(frame._file_url(path, root))}" alt="{frame.esc(path.name)}" loading="lazy">'
    return opener


def topic_delivery(folder: Path, root: Path) -> str:
    """An sNN's delivery in its two parts (JL 261030: "we have two things in the delivery, one is the delivery, and the
    other one is the render"): 1 the delivery, what `delivery/` holds, the agreed version, each file opened in place;
    2 the render, where each piece goes (`delivery/render.yaml`, checked by haipipe-studio's render_delivery.py) and
    whether it landed, each opened to what now sits there."""
    deliv, owner = folder / "delivery", frame.topic_owner(folder)
    card = deliv / "render.yaml"
    try:
        rd = frame.render_module()
        rows = [(piece, *rd.state(folder, piece)) for piece in rd.pieces(folder)]
    except Exception:                                    # a broken render.yaml shows the files, never a crash
        rd, rows = None, []

    #   1 · the delivery: the thing itself
    out = ['<h3 class="focus-sub">1 · Delivery: what it hands over</h3>'
           '<p class="mut">delivery/, the agreed version; open a file to read it</p>']
    # its deck and preview are Delivery's views, the buttons under the title (delivery_views)
    files = sorted(p for p in deliv.rglob("*") if p.is_file() and not p.name.startswith(".") and p != card
                   and inside(p, root))[:80]
    out.append("".join(f'<details class="deliv-file"><summary>{frame.esc(p.relative_to(deliv).as_posix())}</summary>'
                       f'<div class="deliv-body">{readable(p, root)}</div></details>' for p in files)
               if files else '<p class="mut">Empty: nothing agreed yet.</p>')

    #   2 · the render: where each piece goes, and whether it is there
    out.append('<h3 class="focus-sub">2 · Render: where it goes</h3>'
               '<p class="mut">delivery/render.yaml; open a piece to see what now sits at its target</p>')
    items = []
    for piece, st, words in rows:
        mark, said = PIECE_STATE.get(st, ("", st))
        name = piece.get("block") or piece.get("code") or piece.get("from") or "a piece"
        if "code" in piece:                              # the Run, or the Task's Runs, that build it, and what their cards say
            run = owner / str(piece.get("by", ""))
            cards = [run / "run.yaml"] if (run / "run.yaml").is_file() else sorted(run.glob("runs/*/run.yaml"))
            states = [(re.search(r"(?m)^status:\s*(\S+)", c.read_text(encoding="utf-8", errors="ignore")) or [None, ""])[1]
                      for c in cards]
            done = sum(x == "done" for x in states)
            mark = "✅" if states and done == len(states) else "⬜"
            said = f"built by {run.name}, " + (states[0] or "no status" if len(states) == 1 else
                                               ("Runs done" if done == len(states) else "Runs in progress") if states else "no Run yet")   # no tally (JL 261113)
            task = run.parent.parent if (run / "run.yaml").is_file() else run
            where = (f'<a href="{frame.esc(page_url(task, root))}" target=_blank rel=noopener>{frame.esc(frame.rel(run, root))}</a>'
                     if run.is_dir() and inside(run, root) else frame.esc(str(piece.get("by", ""))))
            body = readable(run / f"{run.name}.md", root)  # what the Run says it built, or the Task's face
        elif "to" in piece:
            base = rd.root_for(folder, piece["to"])
            target = base / piece["to"] if base else None
            link = (f'<a href="{frame.esc(frame.reader(target, root))}" target=_blank rel=noopener>{frame.esc(piece["to"])}</a>'
                    if target and target.is_file() and inside(target, root) else frame.esc(piece["to"]))
            where = f'delivery/{frame.esc(piece.get("from", ""))} → {link}'
            body = rendered_region(rd, folder, piece, target, root)
        else:
            where, body = frame.esc(words), '<p class="mut">Its Theme\'s skill builds it.</p>'
        items.append(f'<details class="status-row deliv-piece"><summary><span class="row-name">{mark} {frame.esc(name)}</span>'
                     f'<p class="row-line">{where}</p><p class="row-meta">{frame.esc(said)}</p></summary>'
                     f'<div class="deliv-body">{body}</div></details>')
    out.append("".join(items) if items else '<p class="mut">No render.yaml yet: nothing says where it goes.</p>')
    if card.is_file() and inside(card, root):
        out.append(f'<details class="deliv-file"><summary>render.yaml</summary><div class="deliv-body">{readable(card, root)}</div></details>')
    return "".join(out)


def rendered_region(rd, folder: Path, piece: dict, target: Path | None, root: Path) -> str:
    """What sits between the piece's render markers in its target now: the render's result, not its source."""
    if not target or not target.is_file() or not inside(target, root):
        return '<p class="mut">Its target is not there yet.</p>'
    start, end = rd.markers(rd.address(folder), piece["block"])
    m = re.search(re.escape(start) + r"[^\n]*-->\n(.*?)\n" + re.escape(end), target.read_text(encoding="utf-8", errors="replace"), re.S)
    if not m:
        return f'<p class="mut">No render markers for {frame.esc(piece["block"])} in {frame.esc(target.name)} yet.</p>'
    return markdown(m.group(1)[:60000], target.parent, root)


def delivery_document(folder: Path, root: Path) -> str:
    """An sNN's Delivery alone, for the pop-out from its card (JL 261030: "这些都是 pop out ... 不要让它直接出现")."""
    if not (is_topic(folder) and (folder / "delivery").is_dir() and inside(folder, root)):
        return ""
    return document(folder.name + " · delivery", '<main class="focus-page"><h1>' + frame.esc(folder.name)
                    + '<span class="h1-section">Delivery</span></h1><section class="focus-card"><div class="focus-content">'
                    + topic_delivery(folder, root) + '</div></section></main>')


def delivery_views(folder: Path, root: Path) -> list:
    """Delivery's views, as buttons under the title (key, name, href): the overview the workbench draws, then the pages
    the sNN's builder writes into delivery/, when they exist."""
    views = [("overview", "Overview", frame.ROUTE + "?" + urlencode({"view": "focus-delivery", "path": frame.rel(folder, root)}))]
    for key, name, page in (("preview", "Preview", "web/index.html"), ("contract", "Contract", "web/contract.html"),
                            ("slides", "Slides", "deck/index.html")):
        q = folder / "delivery" / page
        if q.is_file() and inside(q, root):
            views.append((key, name, "/" + frame.rel(q, root)))
    return views


def views_bar(views: list, current: str) -> str:
    return ('<nav class="section-views" aria-label="Views">' + "".join(
        f'<a href="{frame.esc(href)}"' + (' aria-current="page"' if key == current else '') + f'>{frame.esc(name)}</a>'
        for key, name, href in views) + '</nav>') if len(views) > 1 else ""
