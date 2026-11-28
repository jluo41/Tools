"""Idea Studio: a topic's facts, notes, sessions, drawings, its row, and where it sits (address, label, inventory)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote, urlencode

from live.frame_base import _dir_signature, _e, _file_url, _reader, _rel, _title, chain, children, level_of, pop


# ── Idea Studio: one closed row per studio topic, opened in place (b10 s02-D25, D27) ───────
# a topic's stage, its **Stage:** line (b10 s09-D03): a person moves it; the badge only shows it
STAGES = ("explore", "shaping", "agreed", "closed")   # in order; the badge fills one step per stage


# An sNN's main delivery type, the one thing besides its deck that it hands over (hai-studio, one delivery,
# JL 261030: "for each delivery, we should also say what is the type, give the main delivery type"): its face's
# **Delivery type:** line. A deck is never the type: every sNN ends in one.
DELIVERY_TYPES = ("skill", "ui", "code", "draft", "display", "data")


_FACTS: dict = {}                                    # (path, mtime, size) -> facts: a Block page asked 4,608 times (261103)


def _note_facts(md: Path | None) -> dict:
    """What a topic's notes file says: its **Topic:** line, stage, decisions, open points, feeds. Read once per
    version of the file (keyed by its mtime and size), a copy handed out each time."""
    if not md:
        return {"topic": "", "decided": 0, "open": 0, "feeds": [], "tags": [], "stage": "", "at": "", "dtype": ""}
    try:
        st = md.stat()
        key = (str(md), st.st_mtime_ns, st.st_size)
    except OSError:
        key = None
    if key in _FACTS:
        return {k: (list(v) if isinstance(v, list) else v) for k, v in _FACTS[key].items()}
    facts = _read_note_facts(md)
    if key:
        _FACTS[key] = facts
    return {k: (list(v) if isinstance(v, list) else v) for k, v in facts.items()}


def _read_note_facts(md: Path) -> dict:
    text = md.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"\*\*Topic:\*\*\s*(.+?)(?:\n\s*\n|\Z)", text, re.S)
    topic = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    opened = re.search(r"(?ims)^(?:#+\s*)?Open\b[^\n]*\n(?:[-=]{3,}\n)?(.*?)(?=^\S[^\n]*\n[-=]{3,}\n|^#+ |\Z)", text)
    feeds = re.search(r"\*\*Feeds:\*\*(.+?)(?:\n\s*\n|\Z)", text, re.S)
    tags = _split_tags(",".join(re.findall(r"(?mi)^\*\*(?:Tags|Type):\*\*[^\S\n]*([^\n]*)", text)))
    stage = re.search(r"(?mi)^\*\*Stage:\*\*[^\S\n]*`?([A-Za-z]+)", text)
    stage = stage.group(1).lower() if stage and stage.group(1).lower() in STAGES else ""
    at = re.search(r"(?mi)^\*\*At:\*\*[^\S\n]*`?([bjt]\d+(?:\.[jt]\d+)*)", text)   # the rung it hangs from (b35 s01-D05)
    at = at.group(1).lower() if at else ""
    dtype = re.search(r"(?mi)^\*\*Delivery type:\*\*[^\S\n]*`?([A-Za-z]+)", text)   # the one main thing it hands over
    dtype = dtype.group(1).lower() if dtype and dtype.group(1).lower() in DELIVERY_TYPES else ""
    return {"topic": topic, "tags": tags, "stage": stage, "at": "" if re.fullmatch(r"b\d+", at) else at, "dtype": dtype,
            "decided": len(re.findall(r"(?m)^s\d+-D\d+\b", text)),
            "open": len(re.findall(r"(?m)^\d+\.\s", opened.group(1))) if opened else 0,
            # a report's folder name, q08_workbench_base, or its bare id, Q08 (b10 s05 Open 8: s32 wrote `Q08 (...)`)
            "feeds": list(dict.fromkeys(m.group(1) or m.group(2).lower() for m in
                                        re.finditer(r"\b(q\d\d_[A-Za-z0-9_]+)|\b([Qq]\d\d)\b", feeds.group(1))))
                     if feeds else []}


def _split_tags(line: str) -> list:
    """The groups on a **Tags:** line or in a related row's group cell: split at , · or |, backticks off,
    each name once whatever its case."""
    tags = []
    for value in re.split(r"[,·|]", line):
        value = value.strip().strip(chr(96)).strip()
        if value and value.casefold() not in {tag.casefold() for tag in tags}:
            tags.append(value)
    return tags


def _notes(topic: Path) -> Path | None:
    if not topic.is_dir():
        return None
    md = topic / (topic.name + ".md")
    return md if md.is_file() else next(iter(sorted(topic.glob("*.md"))), None)


def _draw_url(d: Path, root: Path, edit: bool = False) -> str:
    return "/_excalidraw/?" + urlencode({"board": _rel(d, root), **({"edit": "1"} if edit else {})})


def _report_page(name: str, folder: Path, root: Path) -> Path | None:
    """reports/<name>/<name>.md at this level or one above; a bare id (q08) finds its folder, q08_<topic>/."""
    for f in [folder] + list(chain(folder, root).values()):
        for d in [f / "reports" / name] if "_" in name else sorted((f / "reports").glob(f"{name.lower()}_*/")):
            page = d / (d.name + ".md")
            if page.is_file():
                return page
    return None


def _feed_chip(name: str, folder: Path, root: Path) -> str:
    """A Question the topic feeds: its report in the pop-out."""
    label = name.split("_", 1)[0].upper()
    page = _report_page(name, folder, root)
    if page:
        return f'<a class=chip data-pop="{_e(label)} · Report" href="{_e(_reader(page, root))}" title="{_e(name)}">{_e(label)}</a>'
    return f'<span class=chip title="{_e(name)}">{_e(label)}</span>'


def _sessions(topic: Path, folder: Path) -> list:
    """A topic's rounds, newest first: its own `passes/pNN-<MMDD>/` (JL 261029: a Studio is the discussion and its
    rounds live with it), then an older `runs/run-draw-<sNN>/passes/` beside it, then older `chat/` summaries."""
    out = []
    m = re.match(r"(s\d+)", topic.name)
    for passes in ([topic / "passes"] if topic.is_dir() else []) + \
            ([folder / "runs" / f"run-draw-{m.group(1)}" / "passes"] if m else []):
        if passes.is_dir():
            for p in sorted((p for p in passes.iterdir() if p.is_dir()), reverse=True):
                md = next(iter(sorted(p.glob("*.md"))), None)
                out.append({"name": p.name, "title": _title(md) if md else p.name, "path": md or p})
    if topic.is_dir() and (topic / "chat").is_dir():
        for md in sorted((topic / "chat").glob("*.md"), reverse=True):
            out.append({"name": md.stem, "title": _title(md), "path": md})
    return out


def _group_parts(key: str, name: str, tags: list, source: str = "", noun: str = "topic", fixed=()) -> tuple:
    """What a row needs under a group bar (b10 s02-D16), a Studio topic or a Related item alike: its data-
    attributes, the ⋮⋮ handle, the Add to Current button, and its group chips, each with × to take it out;
    a group in `fixed` (a related item's subfolder, a theme's own Report group) has no ×, since only moving the
    file, or the theme, changes it; `data-studio-fixed` keeps it so when the page redraws the chips."""
    fixed = {t.casefold() for t in fixed if t}
    attrs = (f' data-studio-key="{_e(key)}" data-studio-name="{_e(name)}" data-studio-source="{_e(source)}"'
             + (f' data-studio-fixed="{_e(json.dumps(sorted(fixed)))}"' if fixed else ""))
    handle = (f'<span class=studio-drag draggable=false title="Drag this {noun} onto a group"'
              f' aria-label="Drag this {noun} onto a group">⋮⋮</span>')
    current = '<button type=button class=studio-current aria-pressed=false>Add to Current</button>'
    chips = "".join(f'<span class=chip data-tag="{_e(tag)}">{_e(tag)}</span>' if tag.casefold() in fixed else
                    f'<span class=chip data-tag="{_e(tag)}">{_e(tag)}<button type=button class=tag-x title="Take '
                    f'out of {_e(tag)}" aria-label="Take {_e(name)} out of {_e(tag)}">×</button></span>' for tag in tags)
    return attrs, handle, current, f'<span class=topic-tags>{chips}</span>' if chips else ""


def _studio_transcripts(topic: Path, root: Path, topic_id: str) -> str:
    """A topic's transcript originals, read in place. The index names a local PDF (optionally a book
    chapter's page range), its source and raw text; source records and credentials are never served here.
    The PDF may sit anywhere in the topic's Block: the Studio's book, or a video Run's own copy in
    runs/<rid>_…/result/ (JL 261012: each video's transcript PDF lives in its Run)."""
    index = topic / "transcripts" / "index.json" if topic.is_dir() else None
    if index is None or not index.is_file():
        return ""
    try:
        data = json.loads(index.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    if not isinstance(data, dict) or data.get("schema") != "studio-transcripts/v1":
        return ""
    cards = []
    for item in data.get("documents", []):
        if not isinstance(item, dict):
            continue
        try:
            path = (index.parent / str(item.get("file") or "")).resolve()
            path.relative_to(root.resolve())
            path.relative_to(topic_owner(topic).resolve())                 # inside this topic's Block
            page = max(1, int(item.get("page") or 1))
            end = max(page, int(item.get("end_page") or page))
        except (OSError, RuntimeError, ValueError, TypeError):
            continue
        # Only kept PDFs inside this Block; no hidden file, symlink escape or other file kind.
        if path.suffix.lower() != ".pdf" or not path.is_file() or any(p.startswith(".") for p in path.relative_to(root.resolve()).parts):
            continue
        destination = str(item.get("destination") or "")
        fragment = ("#nameddest=" + quote(destination, safe="") if destination else f"#page={page}")
        url = _file_url(path, root) + fragment + "&zoom=page-width"
        rid = str(item.get("rid") or "source")
        name = str(item.get("title") or item.get("bv") or path.stem)
        article = item.get("presentation") == "article"
        presentation = "Article PDF" if article else "Transcript PDF"
        note = ("Article arranged from an automatic transcript; not manually verified." if article else
                "Automatic speech-recognition transcript; not manually verified.")
        if item.get("transcription") != "automatic_unchecked":
            note = "Source transcript; its verification state is recorded with the source."
        warnings = item.get("warnings") or []
        note += " " + " ".join(str(w) for w in warnings)
        links = [f'<a href="{_e(url)}" target="_blank" rel="noopener">Open PDF ↗</a>']
        if article and item.get("original_pdf"):
            try:
                original = (index.parent / str(item["original_pdf"])).resolve()
                original.relative_to(root.resolve())
                original.relative_to(topic_owner(topic).resolve())
                original_page = max(1, int(item.get("original_page") or 1))
                if original.suffix.lower() == ".pdf" and original.is_file():
                    original_url = _file_url(original, root) + f"#page={original_page}&zoom=page-width"
                    links.append(f'<a href="{_e(original_url)}" target="_blank" rel="noopener">逐字原文 PDF ↗</a>')
            except (OSError, RuntimeError, ValueError, TypeError):
                pass
        source = str(item.get("source_url") or "")
        if source.startswith(("https://", "http://")):
            links.append(f'<a href="{_e(source)}" target="_blank" rel="noopener">Video ↗</a>')
        raw = (index.parent / str(item.get("raw_file") or "")).resolve()
        if raw.parent == index.parent.resolve() and raw.suffix == ".md" and raw.is_file():
            links.append(pop(_file_url(raw, root), name + " · Original text", "Original text ↗"))
        cards.append(f'<details class="topic studio-transcript" id="{_e(topic_id + "--transcript-" + rid)}">'
                     f'<summary><b>{_e(rid)} · {_e(name)}</b><span class="topic-meta">{_e("文章版" if article else "逐字原文")} · pp. {page}-{end}</span></summary>'
                     f'<p class="studio-transcript-note">{_e(note)}</p>'
                     f'<p class="studio-transcript-links">{" · ".join(links)}</p>'
                     f'<iframe class="st-frame" title="{_e(name + " · " + presentation)}" data-src="{_e(url)}" '
                     'referrerpolicy="no-referrer"></iframe></details>')
    for item in data.get("missing", []):
        if isinstance(item, dict):
            cards.append(f'<p class="studio-transcript-note">{_e(item.get("rid", ""))} · {_e(item.get("title", ""))}: '
                         'No transcript available; a summary is not a full transcript.</p>')
    return ('<section class="studio-transcripts"><h3>Video articles and transcripts · 视频文章与原文</h3>'
            + "".join(cards) + "</section>") if cards else ""


def studio_parts(topic: Path, drawings: list) -> list:
    """(part, label, drawing) for each of a topic's part drawings, `<topic>.<part>.excalidraw` (JL 261022: "They
    will share the same sNN"); a part named `3a-<kind>` reads as "sNN · ③a <kind>"."""
    if not topic.is_dir():
        return []
    nn = re.match(r"s\d+", topic.name)
    out = []
    for dr in drawings:
        if not dr.name.startswith(topic.name + ".") or dr.name == topic.name + ".excalidraw":
            continue
        part = dr.name[len(topic.name) + 1:-len(".excalidraw")]
        m = re.match(r"(\d)([a-z])-(.+)", part)
        label = f"{'①②③④⑤⑥⑦⑧⑨'[int(m.group(1)) - 1]}{m.group(2)} {m.group(3)}" if m else part
        out.append((part, ((nn.group(0) + " · ") if nn else "") + label, dr))
    return out


def _studio_parts(topic: Path, drawings: list, root: Path, topic_id: str) -> str:
    """A topic's part drawings, `<topic>.<part>.excalidraw` beside its own (JL 261022: "one section to be one
    excalidraw ... They will share the same sNN"): each a row inside the topic's row, opened in place like it.
    A part named `3a-<kind>` reads as ③a <kind>."""
    rows = [f'<details class="topic studio-part" id="{_e(topic_id + "--" + part)}"><summary><b>{_e(label)}</b></summary>'
            f'<iframe class=st-frame title="{_e(dr.stem)}" data-src="{_e(_draw_url(dr, root))}" '
            'referrerpolicy=no-referrer></iframe></details>' for part, label, dr in studio_parts(topic, drawings)]
    return f'<section class="studio-parts">{"".join(rows)}</section>' if rows else ""


def _topic_row(topic: Path, drawings: list, root: Path, folder: Path, shared: Path | None = None) -> str:
    """One closed row with its name, tags and controls; opened in place, its live drawing."""
    md = _notes(topic)
    facts = _note_facts(md)
    name = topic.name if topic.is_dir() else topic.stem
    # A face may give a readable Label (for example, its associated Job names); its folder still owns
    # anchors, grouping keys and paths. Faces without a Label keep the existing folder-name display.
    label = re.search(r"(?m)^\*\*Label:\*\*[^\S\n]*(\S[^\n]*)", md.read_text(encoding="utf-8", errors="ignore")) if md else None
    display_name = label.group(1).strip() if label else name
    drawings = [d for d in drawings if not is_structured(d)]
    first = drawings[0] if drawings else None
    mnn = structured_of(topic)
    full = pop(_draw_url(first, root), f"{display_name} · the topic, full size", "↗") if first else ""
    scripts = sorted(topic.glob("build_*.py")) if topic.is_dir() else []
    # an opened row is only its drawing (JL 261007); a hand-drawn one edits in place from the row. A topic's
    # other drawings get no link on its row (JL 261012, on s02's "studio-and-report ↗ studio-workbench-reference ↗":
    # "for the studio, remove the content in the block box here"): its face lists them
    tools = []
    frame_of = lambda d: (f'<iframe class=st-frame title="{_e(d.stem)}" data-src="{_e(_draw_url(d, root))}" '
                          f'data-edit="{_e(_draw_url(d, root, True))}" referrerpolicy=no-referrer></iframe>')
    if first and not scripts:
        tools.append('<button type=button class=draw-edit>Edit</button>')
    if first:
        body = frame_of(first)
    else:
        files = sorted(p.name for p in topic.iterdir() if p.is_file() and not p.name.startswith(".")) if topic.is_dir() else []
        body = f'<p class="mut none">No drawing; it holds {_e(" · ".join(files)) or "nothing yet"}.</p>'
    sides = ""
    if mnn:                       # Free | Structured: one pane a side. Structured is the topic's mind map drawn as the
        side = "free" if first else "structured"      # draft's §1 Structure map, drawn by the one renderer §1 uses (hai-mindmap);
        editable = ["free"] if first and not scripts else []   # Edit opens the free canvas, and only a hand-drawn one
        tools = [t for t in tools if "draw-edit" not in t]
        tools.append('<span class=st-side role=group aria-label="Free or Structured">'
                     f'<button type=button data-side=free aria-pressed="{str(side == "free").lower()}"'
                     f'{"" if first else " disabled"} title="the topic\'s own drawing">Free</button>'
                     f'<button type=button data-side=structured aria-pressed="{str(side == "structured").lower()}"'
                     f' title="{_e(mnn.name)}: its mind map; click a node to type, ＋ adds one">Structured</button></span>')
        if editable:
            tools.append(f'<button type=button class=draw-edit data-sides="free"{"" if side == "free" else " hidden"}>Edit</button>')
        page = mnn.with_name(mnn.name[: -len(".mindmap.md")] + ".mindmap.html")
        links = {"free": (_draw_url(first, root), f"{display_name} · the topic, full size") if first else None,
                 "structured": (_file_url(page, root), f"{display_name} · its mind map") if page.is_file() else None}
        if links[side]:
            href, label = links[side]
            full = (f'<a class=side-link data-pop="{_e(label)}" href="{_e(href)}" target=_blank rel=noopener'
                    + "".join(f' data-href-{k}="{_e(v[0])}" data-pop-{k}="{_e(v[1])}"' for k, v in links.items() if v)
                    + '>↗</a>')
        try:
            opens = lambda f: _draw_url(f, root) if f.suffix == ".excalidraw" else _file_url(f, root)   # a card's file:
            mind = mindmap_module().fragment(mnn, _rel(mnn, root), editable=not READ_ONLY_MAPS, url_of=opens)  # pop-out
        except Exception as e:            # a file that does not parse says why, in the pane, instead of a blank card
            mind = f'<p class="mut none">{_e(mnn.name)} could not be read: {_e(e)}</p>'
        body = (f'<div class=st-pane data-side=free{"" if side == "free" else " hidden"}>{body}</div>'
                f'<div class="st-pane st-map" data-side=structured{"" if side == "structured" else " hidden"}>{mind}</div>')
        sides = f' data-sides="free structured" data-side="{side}"'
    tags = "".join(f'<span class=chip data-tag="{_e(tag)}">{_e(tag)}</span>' for tag in facts["tags"])
    badges = f'<span class=topic-tags>{tags}</span>' if tags else ""
    stage = facts["stage"]
    # a coloured pill with four steps, filled up to the stage (JL 261010: no emoji, more vivid)
    steps = "".join(f'<b class="{"on" if stage and k <= STAGES.index(stage) else ""}"></b>' for k in range(len(STAGES)))
    stage_badge = (f'<span class="stage stage-{stage}" title="Stage {STAGES.index(stage) + 1} of 4: {stage} '
                   f'(its **Stage:** line)"><i class=stage-steps>{steps}</i>{stage}</span>' if stage else
                   '<span class="stage stage-none" title="No **Stage:** line yet">no stage</span>')
    topic_id, attrs, focus = "topic-" + name, "", ""
    if shared is not None:                  # in the shared Studio: the group bar's handle, Current and chips with ×
        topic_id = studio_anchor(topic, folder, shared)
        source = folder.relative_to(shared).as_posix() if folder != shared else ""
        attrs, focus, current, badges = _group_parts(topic.relative_to(shared).as_posix(), name, facts["tags"], source)
        tools.insert(0, current)
    body += _studio_parts(topic, drawings, root, topic_id)
    body += _studio_transcripts(topic, root, topic_id)
    return (f'<details class=topic id="{_e(topic_id)}" data-studio-tags="{_e(json.dumps(facts["tags"]))}"'
            f' data-stage="{_e(stage)}"{sides}{attrs}>'
            f'<summary>{focus}<b>{_e(display_name)}</b>{badges}'
            f'<span class=topic-pop>{" ".join(tools + ([full] if full else []))}</span>'
            f'{stage_badge}</summary>{body}</details>')       # the stage sits at the far right (JL 261010)


STRUCTURED = re.compile(r"^m\d{2}[-_]")          # a topic's structured side, sNN-<topic>.mindmap.md (hai-studio)
READ_ONLY_MAPS = False                            # a read-only host draws the map without its editing script


def is_structured(drawing: Path) -> bool:
    """A file of an older structured side (`mNN-<topic>.…`): never the topic's main drawing."""
    return bool(STRUCTURED.match(drawing.name)) and bool(re.match(r"s\d{2}[-_]", drawing.parent.name))


def structured_of(topic: Path) -> Path | None:
    """A topic's structured side, its mind map `<topic>.mindmap.md` (the topic's own name); an older one named
    `sNN-<topic>.mindmap.md` still reads."""
    if not topic.is_dir():
        return None
    if (topic / f"{topic.name}.mindmap.md").is_file():
        return topic / f"{topic.name}.mindmap.md"
    found = sorted(d for d in topic.glob("m[0-9][0-9]*.mindmap.md") if is_structured(d))
    own = [d for d in found if d.name[1:3] == topic.name[1:3]]
    return (own or found or [None])[0]


def mindmap_module():
    """hai-mindmap's mmmap.py: draws a .mindmap.md with the structure map a draft's §1 is drawn by (mapview.py)
    and writes its edits."""
    import importlib
    import sys
    from host_paths import skill_dir
    scripts = str(skill_dir("hai-mindmap") / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    return importlib.import_module("mmmap")


def render_module():
    """hai-studio's render_delivery.py: where each piece of an sNN's delivery/ goes, and whether it is there."""
    import importlib
    import sys
    from host_paths import skill_dir
    scripts = str(skill_dir("hai-studio") / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    return importlib.import_module("render_delivery")


def topic_drawings(topic: Path) -> list:
    """A topic folder's drawings, its own first, never an older structured side (mNN)."""
    return sorted((f for f in topic.glob("*.excalidraw") if not is_structured(f)),
                  key=lambda f, own=topic.name + ".excalidraw": (f.name != own, f.name))


STUDIO_ITEM = re.compile(r"^s\d+-")


def topic_owner(topic: Path) -> Path:
    """The Block, Job or Task an sNN belongs to: the folder it sits in, or the one above an older studio/."""
    return topic.parent.parent if topic.parent.name == "studio" else topic.parent


def _studio_topics(folder: Path) -> list:
    """(topic, drawings) for each sNN of this level: `sNN-<topic>/` beside its Jobs or Tasks (JL 261030: "we just
    have sNN, along side with jNN, to make it visible directly"), then any in an older `studio/` (a loose drawing
    there is its own topic). A topic's mind map is not among its drawings: its row shows it on the Structured side."""
    studio, out = folder / "studio", []
    if folder.is_dir():
        out += [(p, topic_drawings(p)) for p in sorted(folder.iterdir()) if p.is_dir() and STUDIO_ITEM.match(p.name)]
    if studio.is_dir():
        for p in sorted(studio.iterdir()):
            if p.is_dir() and not p.name.startswith(("_", ".")):
                out.append((p, topic_drawings(p)))       # the topic's own drawing first
            elif p.suffix == ".excalidraw":
                out.append((p, [p]))
    return out


def _topic_rows(folder: Path, root: Path, words: tuple) -> str:
    """The studio topics whose name holds one of `words`, as Idea Studio draws them; '' when none."""
    return "".join(_topic_row(t, d, root, folder) for t, d in _studio_topics(folder) if any(w in t.name for w in words))


def _rungs(folder: Path) -> list:
    """The ladder names from the Block down to this folder, ['b17', 'j01', 't03']; [] above a Block."""
    out = []
    while re.fullmatch(r"[bjt]\d+", folder.name.split("_")[0]):
        out.insert(0, folder.name.split("_")[0])
        if out[0].startswith("b"):
            return out
        folder = folder.parent
    return []


def topic_address(topic: Path, at: str = "") -> str:
    """A Studio topic's address, b17.j01-s07: its Block, the rung it hangs from (the face's **At:**, else the
    folder whose studio/ holds it), then its number (b35 s01-D06). Always shown after the folder name (s01-D03)."""
    num = re.match(r"s\d+", topic.name)
    ladder = _rungs(topic_owner(topic))
    if not num or not ladder:
        return ""
    rungs = [ladder[0]] + at.split(".") if at else ladder
    return ".".join(rungs) + "-" + num.group(0)


def _short(name: str, words: int = 3) -> str:
    """A folder's name without its number, cut to its first words: 'b02_B_case_visits_for_cohort' -> 'B_case_visits'."""
    rest = re.sub(r"^[bjtsr]\d+[_-]?", "", name)
    rest = "_".join(re.split(r"[_.-]+", rest)[:words]) if words else re.sub(r"[.-]+", "_", rest)
    return rest or name                          # '-' and '.' become '_': they separate rungs in a label


def topic_label(topic: Path, at: str = "") -> tuple[str, str]:
    """How people read a topic (JL 261029: "let's do b17-s04:theme_work @ workbench_page_structure"): the address, a
    colon, each rung's short name joined by dots, then ' @ ' and the topic: b17.j01.t03-s09:theme_work.tables.cut @
    which_cut_first; returns ('b17.j01.t03-s09:theme_work.tables.cut @ ', 'which_cut_first'), ('', name) outside a Block."""
    address, ladder = topic_address(topic, at), _rungs(topic_owner(topic))
    if not address:
        return "", topic.name
    here = topic_owner(topic)
    for _ in ladder[1:]:
        here = here.parent
    names = [_short(here.name)]
    for rung in (at.split(".") if at else ladder[1:]):
        found = sorted(p for p in here.glob(f"{rung}[_-]*") if p.is_dir())
        if not found:
            break
        here = found[0]
        names.append(_short(here.name))
    return f"{address}:" + ".".join(names) + " @ ", _short(topic.name, 0)


def _hung_here(folder: Path, root: Path, seen: set) -> list:
    """The Block's topics whose face says **At:** this Job or Task, or a Task below it (b35 s01-D05: one studio/
    per Block, each topic names its rung)."""
    rungs = _rungs(folder)
    block = folder
    for _ in rungs[1:]:
        block = block.parent
    if len(rungs) < 2:
        return []
    here, out = ".".join(rungs[1:]), []
    for topic, drawings in _studio_topics(block):
        at = _note_facts(_notes(topic)).get("at", "") if topic.is_dir() else ""
        actual = topic.resolve()
        if not (at == here or at.startswith(here + ".")) or actual in seen or root not in actual.parents:
            continue
        seen.add(actual)
        out.append((block, topic, [d for d in drawings if root in d.resolve().parents]))
    return out


def studio_inventory(folder: Path, root: Path) -> list:
    """The level's own topics, then its children's: a Block adds its Jobs' and Tasks', a Job its Tasks'
    (JL 261028; older Job and Task studio/ folders stay readable), then the Block's topics hung at this rung by
    their face's **At:** (b35 s01-D05: one studio/ per Block).

    Keep each topic's source for its feeds and sessions. Never enter an archive or a link
    outside this Block/root, and count a linked topic only once.
    """
    key, sig = (str(folder), str(root)), _inventory_signature(folder)
    hit = _INVENTORY.get(key)
    if hit and sig is not None and hit[0] == sig:      # every render of an open Draft page asked again (a hung host)
        return list(hit[1])
    out = _studio_inventory(folder, root)
    _INVENTORY[key] = (sig, out)
    return list(out)


_INVENTORY: dict = {}                     # (folder, root) -> (signature, inventory)


def _inventory_signature(folder: Path):
    """The mtimes the inventory depends on: this folder, its Jobs and Tasks, their studio/ folders and every topic
    folder in them, so a topic or drawing added anywhere reads again at once. None when a folder cannot be read."""
    try:
        sources = [folder]
        if level_of(folder) == "Block":
            jobs = children(folder, "Block")
            sources += jobs + children(folder, "Job") + [t for j in jobs for t in children(j, "Job")]
        elif level_of(folder) == "Job":
            sources += children(folder, "Job")
        sig = []
        for src in sources:
            for d in (src, src / "studio"):
                if d.is_dir():
                    sig.append((str(d),) + _dir_signature(d))
        return tuple(sig)
    except OSError:
        return None


def _studio_inventory(folder: Path, root: Path) -> list:
    root, folder = root.resolve(), folder.resolve()
    if folder != root and root not in folder.parents:
        return []
    sources = [folder]
    if level_of(folder) == "Block":
        jobs = children(folder, "Block")
        sources += jobs + children(folder, "Job")
        for job in jobs:
            sources += children(job, "Job")
    elif level_of(folder) == "Job":
        sources += children(folder, "Job")
    out, seen = [], set()
    for source in sources:
        resolved = source.resolve()
        if resolved != folder and folder not in resolved.parents:
            continue
        for topic, drawings in _studio_topics(source):
            actual = topic.resolve()
            if root not in actual.parents or folder not in actual.parents or actual in seen:
                continue
            seen.add(actual)
            drawings = [d for d in drawings if root in d.resolve().parents and folder in d.resolve().parents]
            out.append((source, topic, drawings))
        if source == folder:
            out += _hung_here(folder, root, seen)              # the Block's topics at this rung, after its own
    return out


def studio_anchor(topic: Path, source: Path, block: Path) -> str:
    """Keep Block topic links; qualify older local topics so repeated sNN names stay distinct."""
    prefix = source.relative_to(block).as_posix().replace("/", "--") + "--" if source != block else ""
    return "topic-" + prefix + (topic.name if topic.is_dir() else topic.stem)
