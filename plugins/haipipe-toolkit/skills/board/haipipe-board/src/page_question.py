"""One question -> one <section class="slide q"> card (QB5: the card chunk of
the old render(), moved verbatim). page_stage.py owns embedded source content;
this file owns the page-template anatomy on stage."""
import re

from . import body as _bd
from .body import (body, flat_rows, inline, note_body, render_apparatus,
                   render_thread, sort_log)
from .common import aim_progress, aim_summary, esc, sec, stinfo

STAGE_LABELS = {
    "seed": "SEED PAGE",
    "work": "WORK PAGE",
    "venue": "VENUE PAGE",
    "display": "DISPLAY PAGE",
    "main": "MAIN SECTION",
    "appendix": "APPENDIX",
    "submission": "SUBMISSION PAGE",
}


def det(label, inner, open_=False):
    if not inner:
        return ""
    o = " open" if open_ else ""
    return (f'<details class="fold"{o}><summary>{esc(label)}</summary>'
            f'<div class="fb">{inner}</div></details>')


def chead(label, inner, tag="div"):
    """一个节标题：左边标签、底下一条线（CSS 画）、右边一个「expand all」。
    只有这一节真有可折叠的 item（body 里出现 class="it"）才挂那个按钮 ——
    没东西可开合就不放。纯增强：脚本剥掉后每个 item 仍能单独点开。
    tag="summary" 时它就是所在 <details> 的开合把手（见 sect()）。"""
    tog = ('<button class="secall" type="button" title="expand / collapse all">'
           '<span class="lbl">expand all</span></button>'
           if '<details class="it' in inner else '')
    return f'<{tag} class="ch"><span class="chl">{label}</span>{tog}</{tag}>'


def sect(label, inner, cls="", open_=False):
    """A whole page section that folds from its own heading (JL 260725), by the
    same native-details mechanism Diagram already uses. Shut, the section keeps
    its text in the DOM, so the zero-script invariant, Ctrl-F, and the section
    ⧉ copy button all keep working.

    Every section now starts SHUT (JL 260801). The 260725 default was open,
    for a reason that has since expired: back then the page had no sidebar, so
    a reader who never clicked had to be able to read straight down. QB2a's
    sidebar now carries the map, and a page like QB4 has grown past 6000 words of
    Content, where "open by default" means the reader meets a wall instead of a
    page. Shut, the page opens as what it actually is: a title, the paragraph
    on stage, and seven section names you can take in at a glance."""
    if not inner:
        return ""
    o = " open" if open_ else ""
    return (f'<details class="sect {cls}"{o}>'
            f'{chead(label, inner, tag="summary")}{inner}</details>')


# ── 🖼 Diagram = two subsections (QA4, JL 260726) ──────────────────────────
# The ASCII figure is the thing you almost always want, so it opens with the
# section. The Excalidraw canvas is one more click away: it is heavy, it is
# collaborative rather than referential, and inside a shut <details> its lazy
# iframe never loads, so a board with N canvases no longer boots N of them.
#
# The SOURCE keeps one plain `## Diagram`. The split is a render decision, so
# not one page had to be rewritten, and a page that later gains a canvas splits
# itself. This is the same bargain as `![[...]]` and the bare URL line: the
# markdown stays something a person types, the renderer does the arranging.
XCAL_HOSTED = re.compile(r"^\s*https?://(?:app\.)?excalidraw\.com/\S+\s*$")


def split_diagram(txt):
    """-> (figure_markdown, canvas_markdown).

    A bare Excalidraw URL alone on a line is the canvas; every other line is
    the figure. Fenced lines are never canvas lines, so a URL drawn inside an
    ASCII figure stays in the figure where its author put it."""
    fig, canvas, fence = [], [], False
    host = _bd.EXCAL_HOST
    ours = re.compile(r"^\s*" + re.escape(host) + r"/\S+\s*$") if host else None
    for ln in txt.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
            fig.append(ln)
            continue
        is_canvas = not fence and (XCAL_HOSTED.match(ln)
                                   or (ours is not None and ours.match(ln)))
        (canvas if is_canvas else fig).append(ln)
    return "\n".join(fig).strip("\n"), "\n".join(canvas).strip("\n")


def render_diagram(txt):
    """The 🖼 Diagram section: ▧ ASCII open, ✏️ Excalidraw shut."""
    fig, canvas = split_diagram(txt)
    parts = []
    if fig.strip():
        parts.append(
            '<details class="dsub dsub-a" open>'
            '<summary class="dsubh">▧ ASCII</summary>'
            f'<div class="dsubb">{body(fig, fold_code=False)}</div></details>')
    # The canvas row is emitted even when empty: it is where the 🖌 attach
    # button lives, and scriptless it still says truthfully that none is there.
    inner = (body(canvas, fold_code=False) if canvas.strip()
             else '<p class="dsub-empty">No canvas attached yet.</p>')
    parts.append(
        '<details class="dsub dsub-x">'
        '<summary class="dsubh">✏️ Excalidraw</summary>'
        f'<div class="dsubb">{inner}</div></details>')
    return ('<details class="diagram-section">'
            '<summary class="ch"><span class="chl">🖼 Diagram</span></summary>'
            f'<div class="dia">{"".join(parts)}</div>'
            '</details>')


def split_stage_record(kind, content_sections):
    """-> (legacy_record_markdown, remaining_sections).

    A stage declares its obligations under ONE name, `## Stage Contract`
    (JL 260801: "stage contract, no stage protocol"). Old stage pages still
    carry a hand-written `### Stage Record` under Content; it is pulled out
    here, because Content holds the stage's product and nothing else, and it
    is then printed as the contract's opening lines so no wording is lost.

    Both the page render and the sidebar outline call this, or they disagree:
    the outline counts Content's divisions and addresses them BY ORDER
    (`data-div`), so a section the page dropped and the sidebar kept shifted
    every division link on that page by one."""
    if kind != "stage":
        return "", content_sections
    for i, (heading, md) in enumerate(content_sections):
        if re.sub(r"\s+", " ", heading).strip().casefold() == "stage record":
            return md, content_sections[:i] + content_sections[i + 1:]
    return "", content_sections


def structure_rows(d, content_sections):
    """The DATA half of the page's Structure map: (key, label, value, subs)
    per section that exists, where key is the stable machine name the sidebar
    outline's JS resolves to a DOM selector, and subs is Content's division
    titles. Shared by the Opening drawer and the sidebar outline (QB2a,
    JL 260731), so the two views can never disagree."""
    rows = [("opening", "🧭 Opening", "the lead, and this drawer", [])]
    dia = sec(d, "Diagram").strip()
    if dia:
        fig, canvas = split_diagram(dia)
        nfig = fig.count("```") // 2
        v = f"{nfig} figure{'s' if nfig != 1 else ''}" if nfig else "no figure"
        v += " · canvas" if canvas.strip() else " · no canvas"
        rows.append(("diagram", "🖼 Diagram", v, []))
    divs = [(h, h) for h, _ in content_sections if h]
    if divs or sec(d, "Content").strip():
        v = (f"{len(divs)} division{'s' if len(divs) != 1 else ''}" if divs
             else "one flat body")
        rows.append(("content", "📚 Content", v, divs))
    aims = sec(d, "Done when")
    state = sec(d, "Now").strip()
    progress = aim_progress(aims, state)
    if aims.strip():
        isubs = []
        for h, b in parse_content_sections(aims):
            if not h:
                continue
            group = aim_progress(b, state)
            label = (f'{h} · {group["closed"]}/{group["total"]}'
                     if group["total"] else h)
            isubs.append((label, h))
        rows.append(("items", "🎯 Aims", aim_summary(aims, state), isubs))
    w = state
    if w:
        dated = len(re.findall(r"(?m)^- ?\d{6}", w))
        # Its ### subsections are jump targets too (JL 260731: "unfold the
        # Decision Now in the sidebar"); a Decision Now row carries how many
        # ticks it still owes.
        wsubs = []
        for h, b in parse_content_sections(w):
            if not h:
                continue
            owed = len(re.findall(r"(?m)^\s*[-*] \[ \]", b))
            wsubs.append((f"{h} · {owed} to tick" if owed else h, h))
        rows.append(("now", "📍 States",
                     f"{dated} dated entr{'ies' if dated != 1 else 'y'}"
                     if dated else "the present state", wsubs))
    ftxt = sec(d, "Files")
    nfiles = len(re.findall(r"(?m)^- ", ftxt))
    if nfiles:
        fsubs = [(h, h) for h, _ in parse_content_sections(ftxt) if h]
        rows.append(("files", "📎 Files",
                     f"{nfiles} file{'s' if nfiles != 1 else ''}", fsubs))
    return rows


AIM_ROW = re.compile(r"(?m)^(\s*[-*]\s*)((?:A\d+\.\d+|P\d+)\s*·)")


def stamp_aim_states(aims, state):
    """Put each Aim's CURRENT status emoji on its own row (JL 260802).

    An Aim row carried no marker at all, because status is States' job and an
    Aim must not claim progress. That rule is about the SOURCE: the markdown
    stays free of checkboxes, so there is still exactly one place a status is
    written. The render is free to show what States already says, the way the
    section count has always been derived rather than stored, and without it a
    reader had to hold two lists side by side to learn whether A1.1 was done.
    """
    if not state or re.search(r"(?m)^\s*[-*]\s*\[[ xX]\]", aims or ""):
        return aims                      # legacy checklists keep their boxes
    from .common import AIM_STATE_RE, AIM_STATUS_ALIAS
    seen = {}
    for emoji, aim_id in AIM_STATE_RE.findall(state):
        e = emoji.replace("\ufe0f", "")
        seen[aim_id] = AIM_STATUS_ALIAS.get(e, e)

    def mark(m):
        aim_id = m.group(2).split("·")[0].strip()
        return "%s%s %s" % (m.group(1), seen.get(aim_id, "⬜"), m.group(2))
    return AIM_ROW.sub(mark, aims or "")


def render_aims(aims, state=""):
    """Aims with optional Content-linked groups and progress derived from States.

    Canonical Aims are durable target records whose current emoji lives in
    States. Legacy checklists retain their checkbox count through aim_progress.
    """
    parts = []
    for title, b in parse_content_sections(aims):
        if not title:
            if b.strip():
                parts.append(body(b))
            continue
        if not b.strip():
            continue
        group = aim_progress(b, state)
        cnt = (f'<span class="shc">{group["closed"]}/{group["total"]}</span>'
               if group["total"] else "")
        # A group FOLDS, exactly like a Content division (JL 260802: "I want the
        # division in the Aims to be collapsed as what we have in the Content,
        # and of the same format"). It was a flat `.sh` row, which made Aims the
        # one section a reader could not collapse down to its group names, and
        # since 260801 every other section on the page starts shut.
        # The item opens with its group (JL 260802: "you can show the hidden
        # text out"). `Done when` IS the Aim's substance: an Aim you cannot
        # check is not one, so hiding the check behind a second click made the
        # row a title with nothing under it. The GROUP is still shut, so the
        # page still collapses to its group names.
        # A `### Q-consumer register` division renders in register mode: its
        # backticked binding tokens (bib keys, bank paths) become evidence
        # chips (JL 260806). The heading was split off above, so body() cannot
        # detect it on its own; the flag is how the division's identity travels.
        parts.append(f'<details class="csec"><summary>{inline(title)} {cnt}'
                     f'</summary><div class="cbody aims-open">'
                     f'{body(stamp_aim_states(b, state), register=bool(_bd.REGISTER_TITLE.match(title)))}'
                     f'</div></details>')
    return "".join(parts)


# Internal compatibility for extensions that imported the old helper name.
render_items = render_aims


def render_structure(d, content_sections):
    """The generated `Structure` row that OPENS the drawer (JL 260729: "the
    Structure subsection just above Boundary"): what this page is built of.
    Computed from the parsed page rather than authored, so the map can never
    go stale — the same bargain as split_diagram: the source gains nothing.
    Only sections that exist get a row."""
    def row(label, value):
        return (f'<div class="pmr"><span class="pml">{label}</span>'
                f'<span class="pmv">{value}</span></div>')
    rows = []
    for _, label, value, subs in structure_rows(d, content_sections):
        rows.append(row(label, value))
        shown = subs[:7]
        for disp, _t in shown:
            rows.append(f'<div class="pmd">{inline(disp)}</div>')
        if len(subs) > len(shown):
            rows.append(f'<div class="pmd">… +{len(subs) - len(shown)} more</div>')
    return ('<div class="fh">Structure</div>'
            f'<div class="pmap">{"".join(rows)}</div>')


def parse_content_sections(txt):
    """Split direct ### headings without treating headings inside fences as sections."""
    sections = []
    title, buf, fence = "", [], False
    for ln in txt.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
        if ln.startswith("### ") and not fence:
            if title or any(x.strip() for x in buf):
                sections.append((title, "\n".join(buf).strip()))
            title, buf = ln[4:].strip(), []
        else:
            buf.append(ln)
    if title or any(x.strip() for x in buf):
        sections.append((title, "\n".join(buf).strip()))
    return sections


def merge_prose_lines(md):
    """Join consecutive prose lines into one paragraph. Opening only (JL 260801).

    The board writes one sentence per source line so a single sentence can be
    quoted, commented on, and diffed on its own. Rendered literally that gives a
    column of one-sentence paragraphs, and JL read Opening's drawer as a list of
    fragments rather than as prose, and asked for those lines to be merged
    into one paragraph.
    So inside the Opening drawer the lines are rejoined and a BLANK LINE still
    starts a new paragraph, which is ordinary markdown behaviour. The source is
    untouched, so the sentence remains the unit a comment anchors to (QB5).
    Everywhere else the one-line-per-sentence render is unchanged, which is why
    this runs in the flat branch alone.
    """
    out, buf = [], []
    fence = False

    def flush():
        if buf:
            out.append(" ".join(buf))
            buf.clear()

    for ln in md.splitlines():
        s = ln.strip()
        if s.startswith("```"):
            flush()
            fence = not fence
            out.append(ln)
        elif fence:
            out.append(ln)
        elif not s:
            flush()
            out.append("")
        elif re.match(r"(#{1,6}\s|[-*+]\s|\d+[.)]\s|>|\||<!--)", s):
            # a heading, list item, apparatus lane, table row or marker is its
            # own line by construction; merging one into a paragraph would
            # destroy the very thing that makes it that kind of line.
            flush()
            out.append(ln)
        else:
            buf.append(s)
    flush()
    return "\n".join(out)


def render_subsections(sections, open_first=False, flat=False):
    """Render named markdown chunks as native disclosure rows.

    open_first was True until JL 260801 ("I always find the first subsection of
    the Content is opened, I don't like it"). One open division among nine shut
    ones reads as a state someone left behind rather than as a deliberate entry
    point, and it makes the first division look privileged when the numbering
    already says it is simply first.

    flat=True drops the disclosure entirely and emits a plain `.fh` heading plus
    its body. Opening uses it (JL 260725: "I don't want to have >"): behind the
    lead question everything is simply shown, the way Boundary already was, so no
    second layer of ▸ rows hides the stage style, venue section, or writing style.
    It also merges one-sentence source lines back into paragraphs (JL 260801),
    since flat is the Opening-only branch."""
    out = []
    for i, (heading, md) in enumerate(sections):
        # #### 不再压成 **…**（那会套上组标题的 🔹）；body() 现在自己渲染段落标题。
        # A register division carries its binding chips wherever it lives:
        # some topic pages keep `### Q-consumer register` in Content.
        rendered = body(merge_prose_lines(md) if flat else md,
                        register=bool(heading and _bd.REGISTER_TITLE.match(heading)))
        if heading and flat:
            out.append(f'<div class="fh">{inline(heading)}</div>'
                       f'<div class="cbody flat">{rendered}</div>')
        elif heading:
            out.append(
                f'<details class="csec"{" open" if (open_first and i == 0) else ""}>'
                f'<summary>{inline(heading)}</summary><div class="cbody">{rendered}</div>'
                '</details>')
        elif rendered:
            out.append(f'<div class="cbody prelude">{rendered}</div>')
    return "".join(out)


def face_name(q):
    """"S Main 7 · Results" -> "Main 7 Results": the page's own name, for labels."""
    return re.sub(r"\s+", " ", re.sub(r"^[QS]\s+", "", q.get("title", ""))
                  .replace("·", " ")).strip()


def render_content(sections, q=None, leading=""):
    """Render a page's remaining named Content subsections.

    On S pages the heading NAMES the stage ("Content · Main 7 Results") instead of
    counting subsections (JL 260725): an S page's Content is the stage's own
    substance, so the label should say which substance, not how many boxes.

    A Q page's heading is just "📚 Content" (JL 260801: "we will not add this,
    just call it Content should be ok"). The "· 9 sections" suffix it used to
    carry was a scanning aid, but the divisions are listed right underneath and
    the sidebar already counts them, so it only made the heading longer."""
    if not sections and not leading:
        return ""
    inner = leading + render_subsections(sections)
    name = face_name(q) if q else ""
    lab = f"📚 Content · {esc(name)}" if name else "📚 Content"
    return sect(lab, inner, cls="content")


def _display_live_artifact(unit):
    """Show the exact object that the current float references.

    preview.pdf is the reader's manuscript-level inspection surface.  This
    second row makes legacy or blocked units honest by showing the actual PDF,
    image, or table body behind that wrapper rather than describing it only.
    """
    path = unit.float_target
    if path is None:
        return ('<details class="csec display-artifact missing" open>'
                '<summary>📄 Live display artifact</summary><div class="cbody">'
                '<p><code>float.tex</code> has no resolvable asset target yet.</p>'
                '</div></details>')
    href = _bd._rel(path)
    if not href:
        return ""
    try:
        name = path.relative_to(unit.path).as_posix()
    except ValueError:
        name = path.name
    lower = path.name.lower()
    if lower.endswith(".pdf"):
        visual = (f'<object class="figpdf" data="{esc(href)}" type="application/pdf">'
                  f'<a class="fp" href="{esc(href)}">open {esc(name)}</a></object>')
        label = "📄 Live display PDF"
    elif lower.endswith((".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif")):
        visual = f'<img class="fig" src="{esc(href)}" alt="{esc(name)}" loading="lazy">'
        label = "🖼 Live display asset"
    else:
        visual = (f'<p>The Current Float above is assembled from '
                  f'<a class="fp" href="{esc(href)}"><code>{esc(name)}</code></a>.'
                  f'</p>')
        label = "📋 Live display artifact"
    return (f'<details class="csec display-artifact" open><summary>{label}</summary>'
            f'<div class="cbody">{visual}</div></details>')


def _display_versions(unit):
    """List the current artifact and every stored alternative without promoting one.

    ``float.tex`` is the one authority for *current*.  Files in ``versions/``,
    ``candidates/``, and a non-current ``assets/`` are useful to inspect, but
    their directory alone does not establish chronology, approval, or
    reproducibility.  This is especially important for legacy units whose
    history predates a version manifest.
    """
    def rel(path):
        try:
            return path.relative_to(unit.path).as_posix()
        except ValueError:
            return path.name

    def link(path):
        href = _bd._rel(path)
        name = rel(path)
        return (f'<a class="fp" href="{esc(href)}"><code>{esc(name)}</code></a>'
                if href else f'<code>{esc(name)}</code>')

    target = unit.float_target
    sections = []
    if target is None:
        sections.append('<p><b>Current printed artifact:</b> '
                        '<code>float.tex</code> has no resolvable target.</p>')
    else:
        sections.append(f'<p><b>Current printed artifact:</b> {link(target)} '
                        '(<code>float.tex</code> target).</p>')

    groups = (
        ("Saved versions", unit.path / "versions",
         "stored history; not necessarily approved or chronological"),
        ("Candidates", unit.path / "candidates",
         "not printed or promoted"),
        ("Other assets", unit.path / "assets",
         "not the artifact currently targeted by the float"),
    )
    listed = False
    for label, folder, note in groups:
        paths = [p for p in sorted(folder.iterdir())
                 if p.is_file() and p.name != ".gitkeep"] if folder.is_dir() else []
        if target is not None:
            paths = [p for p in paths if p.resolve() != target.resolve()]
        if not paths:
            continue
        listed = True
        items = "".join(f'<li>{link(path)}</li>' for path in paths)
        sections.append(f'<p><b>{esc(label)}:</b> {esc(note)}.</p>'
                        f'<ul class="display-version-list">{items}</ul>')
    if not listed:
        sections.append('<p>No saved alternatives or unpromoted candidates are present.</p>')
    sections.append('<p class="display-version-posture">Only the current row is selected by '
                    '<code>float.tex</code>. The remaining rows are an on-disk inventory; '
                    'their status and provenance require an explicit manifest or stage record.</p>')
    return ('<details class="csec display-versions" open><summary>🗂 Display Versions</summary>'
            f'<div class="cbody">{"".join(sections)}</div></details>')


def _display_folder(unit):
    """Render the actual unit layout, including its migration posture."""
    icon = {"intake": "📥", "recipe": "🧰", "assets": "🖼", "candidates": "🧪",
            "versions": "🗂", "source": "🕰"}
    note = {"intake": "approved snapshot", "recipe": "rebuild source", "assets": "promoted asset",
            "candidates": "unpromoted renders", "versions": "history", "source": "legacy mixed source"}
    target = "(none yet)"
    if unit.float_target is not None:
        try:
            target = unit.float_target.relative_to(unit.path).as_posix()
        except ValueError:
            target = unit.float_target.name
    lines = [f"📁 {unit.id}/", "├── 📄 README.md", f"├── 📄 float.tex  ──► {target}",
             "├── 🖼 preview.pdf  ← Current Float"]
    present = [name for name in ("intake", "recipe", "assets", "candidates", "versions", "source")
               if (unit.path / name).is_dir()]
    for i, name in enumerate(present):
        branch = "└──" if i == len(present) - 1 else "├──"
        files = [p.name for p in sorted((unit.path / name).iterdir())
                 if p.is_file() and p.name != ".gitkeep"]
        shown = ", ".join(files[:3]) or "(empty)"
        if len(files) > 3:
            shown += f", +{len(files) - 3} more"
        lines.append(f"{branch} {icon[name]} {name}/  ← {note[name]}: {shown}")
    legacy = (unit.path / "source").is_dir() and not (unit.path / "recipe").is_dir()
    posture = ("Legacy layout: do not rename or promote files until the unit has a deliberate "
               "provenance-safe migration into intake/ and recipe/." if legacy else
               "Target layout present. Verify the live asset, intake, and recipe before closing the gate.")
    tree = "\n".join(lines)
    tree_html = body("```text\n" + tree + "\n```", fold_code=False)
    return ('<details class="csec display-folder" open><summary>📁 Current display folder</summary>'
            f'<div class="cbody">{tree_html}'
            f'<p class="display-folder-posture">{esc(posture)}</p></div></details>')


def render_display_preview(q):
    """Render standard reader-facing Display content before authored explanation.

    Every resolved asset page begins with the printable Current Float, then the
    live artifact, an inventory of versions, and the actual folder tree.
    Authored Content follows with the display explanation.  This keeps the
    review surface uniform without pretending that a legacy folder has already
    reached the target layout or that a saved file has been promoted.
    """
    paper = _bd.PAPER
    if q.get("family") != "display" or paper is None:
        return ""
    unit = paper.unit_for_sdisplay(sec(q["sec"], "Content"))
    if unit is None:
        # S-Display-0 is a set-level design page, not an asset page. It has no
        # unit and therefore no single preview subsection.
        return ""

    path = unit.preview
    label = "CURRENT FLOAT · preview.pdf"
    stale = bool(unit.preview_stale)
    kind = "pdf"
    if path is None:
        pdfs = [name for name in unit.assets if name.lower().endswith(".pdf")]
        images = [name for name in unit.assets
                  if name.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif"))]
        if pdfs:
            path = unit.path / "assets" / pdfs[0]
            label = f"LIVE ASSET · {pdfs[0]} · wrapper preview missing"
        elif images:
            path = unit.path / "assets" / images[0]
            label = f"LIVE ASSET · {images[0]} · wrapper preview missing"
            kind = "img"

    if path is None:
        preview = (
            '<details class="csec display-preview missing" open>'
            '<summary>🖼 Current Float</summary><div class="cbody">'
            '<p>No printable preview exists yet. Build the unit\'s '
            '<code>preview.pdf</code> before treating the surrounding page text '
            'as a display review.</p></div></details>'
        )
        return (preview + _display_live_artifact(unit) + _display_versions(unit)
                + _display_folder(unit))

    href = _bd._rel(path)
    if not href:
        return ""
    warning = ' <span class="display-preview-stale">⚠️ older than the asset</span>' if stale else ""
    source_links = []
    for role, pptx in unit.pptx:
        pptx_href = _bd._rel(pptx)
        if pptx_href:
            source_links.append(
                f'<a class="fp" href="{esc(pptx_href)}" '
                f'title="{esc(pptx.name)}">PPTX {esc(role)}</a>')
    head = (f'<div class="display-preview-head"><a class="fp" href="{esc(href)}">open PDF</a>'
            + "".join(source_links) + warning + '</div>')
    if kind == "img":
        visual = (f'<img src="{esc(href)}" alt="{esc(label)}" loading="lazy">')
    else:
        visual = (f'<object data="{esc(href)}" type="application/pdf">'
                  f'<a class="fp" href="{esc(href)}">open {esc(label)}</a>'
                  '</object>')
    preview = (f'<details class="csec display-preview" open>'
               f'<summary>🖼 {esc(label)}</summary><div class="cbody">{head}{visual}</div>'
               '</details>')
    return (preview + _display_live_artifact(unit) + _display_versions(unit)
            + _display_folder(unit))


def render_contract(sections, lead=""):
    """Stage Contract renders INSIDE Opening (JL 260725), never its own section.

    It is shown outright behind the lead question, so Required Inputs, Writing
    Style and the venue section are read rather than hunted for. Its heading is a
    plain word like every other heading in that drawer (JL 260725: the drawer had
    two iconed headings and five bare ones, which is what read as inconsistent).

    `lead` carries a legacy `### Stage Record` block (JL 260801: "只统一叫一个吧,
    就叫 stage contract"). A stage page declares its obligations ONCE, under one
    name; the old block's text is kept word for word and simply reads as the
    contract's opening lines, because deleting someone else's writing on read
    would be a silent loss."""
    if not sections and not lead:
        return ""
    return ('<div class="fh">Stage Contract</div>'
            + (body(lead) if lead else "")
            + render_subsections(sections, flat=True))


def render_question(q, prv, nxt):
    nav = ('<div class="nav">'
           + (f'<a href="#{prv["id"]}">← {prv["id"]}</a>' if prv else '<span></span>')
           + f'<a class="all" href="#top">☰ Index</a>'
           + (f'<a href="#{nxt["id"]}">{nxt["id"]} →</a>' if nxt else '<span></span>')
           + '</div>')
    tok, cls, lab = stinfo(q["state"])
    who = "🧠 JL decides" if q["owner"] == "JL" else ("🔧 " + q["owner"] if q["owner"] else "")
    # Intent first, then the factual present (JL 260801): Aims are durable
    # target states; States owns progress, decisions, and verification.
    now, goal = sec(q["sec"], "Now"), sec(q["sec"], "Done when")
    progress = aim_progress(goal, now)
    cnt = (f'<span class="cnt">{progress["closed"]}/{progress["total"]}</span>'
           if progress["total"] else "")
    fs = ""
    if now or goal:
        nb, gb = render_aims(now), render_aims(goal, now)
        fs += ('<div class="cmp">'
               + sect(f"🎯 Aims{cnt}", gb, cls="col goal")
               + sect("📍 States", nb, cls="col now")
               + '</div>')
    # 「Why here」不再单独占台面：它该讲的（为什么难 / 不定会怎样）并进 ## Question
    # 的要点里，光读第一节就 orient。老板子里还写着这段的，收进底部折叠区，内容不丢。
    why = sec(q["sec"], "Why here")
    disc = sec(q["sec"], "Discussion").strip()
    # ## Question 是「一段话 + 几个要点」（JL 260723 改版）：走 body() 才吃得下要点。
    # 第一段是大字领句（CSS 挑 p:first-of-type），要点跟在下面 —— 光这一节就该让
    # 零背景的人明白：在问什么、为什么难、不定会怎样（原 Why here 的活并进来了）。
    # ## Question（JL 260724）：领句本身可点，点这一整行才铺开隐藏块。
    # 隐藏块带 Boundary 和 Why this matters（JL 260729：Q/S 一致，解释段跟着领句走；
    # 之前 Q 的解释段落在 Content 首节）。页面仍按 Opening -> Content -> Items -> Where 阅读。
    # 问句里的 **粗体** 要正常内联流动 —— 所以文字包进一个 .qt span，别让 flex 拆散它。
    # Boundary 收进【同一个】折叠块，不再单占一节；里头用扁平行，不套第二层折叠。
    q_md = sec(q["sec"], "Opening").strip()
    _parts = re.split(r"\n\s*\n", q_md, maxsplit=1)
    # A `<!-- haipipe:… -->` marker is addressed to a script, never to a reader.
    # body() already drops them at render, but the LEAD is composed here and
    # skipped that filter, so a generated page whose Opening opens with a
    # managed span printed the marker as its own lead sentence (found on the
    # first Meeting page, QC10).
    lead_lines = [x for x in _parts[0].splitlines()
                  if not (x.lstrip().startswith("<!--") and "haipipe:" in x)]
    qlead = inline(" ".join(x.strip() for x in lead_lines if not x.lstrip().startswith(">")))
    lead_app, lead_heads, lead_kind = render_apparatus(
        [x for x in lead_lines if x.lstrip().startswith(">")]
    )
    qrest = _parts[1].strip() if len(_parts) > 1 else ""
    content_sections = parse_content_sections(sec(q["sec"], "Content"))
    contract_md = re.sub(r"<!--.*?-->", "", sec(q["sec"], "Stage Contract"), flags=re.S)
    contract_sections = parse_content_sections(contract_md)
    is_stage = q.get("kind") == "stage"
    legacy_record, content_sections = split_stage_record(
        q.get("kind"), content_sections)
    opening_sections = []
    # Why this matters lives in Opening for BOTH kinds (JL 260729: it explains
    # the lead, so it belongs behind the lead). Until then Q carried it as
    # Content's first subsection; Content now holds only what the author wrote.
    # The row is labelled "More details" (JL 260801). "Why this matters" named the
    # rhetorical job the paragraph was supposed to do, and that framing is what
    # produced the mad-lib openings the 260801 rewrite banned; the drawer now just
    # says what it is, which is the rest of the Opening.
    if qrest:
        opening_sections.append(("More details", qrest))
    # Boundary 排在 Why this matters 之后（JL 260801）。这翻掉了 260729 的顺序，
    # 当时 Why this matters 被放在 Boundary「just below」。理由是读者的顺序：
    # pitch 给出承诺 → Why this matters 说明为什么值得在意 → 这时才轮到「哪些不归这页」。
    # 「不管什么」是个限定语，限定语要落在被限定的东西已经站住之后才有意义。
    btxt = sec(q["sec"], "Boundary").strip()
    if btxt:
        opening_sections.append(("Boundary", btxt))
    # Writing Style 是「页」的元素，不是 S 的（JL 260801：「here is not about S, or
    # Q ... it is just about the Page」）。它原来长在 S 的 Stage Contract 里，跟
    # Required Inputs、Venue 并列；但「这一页该怎么写」每一页都得有 —— 没有它，
    # 下一个人就没法照着改。所以它跟 Why this matters 一样收在领句后面：解释这一页
    # 该怎么被对待，而不是这一页的实质内容。
    wstyle = sec(q["sec"], "Writing Style").strip()
    if wstyle:
        opening_sections.append(("Writing Style", wstyle))
    # Stage Contract joins Opening's collapsed rows (JL 260725: "within the
    # Opening, not a separate section"), after Why this matters / Writing Style.
    # Boundary was retired on JL's ruling (260731, said twice): a page's scope is
    # the Opening's job. Old boards that still carry the section keep rendering
    # it, because deleting someone else's text on read would be a silent loss.
    # Structure 从抽屉里撤掉（JL 260801：「WE ALREADY HAVE THE LEFT PANEL INDEX.
    # SO WE CAN DROP THE STRUCTURE」）。它 260729 进来时是「这一页自己的地图」，
    # 那会儿还没有左侧栏；侧栏一上线，这一行就是同一张地图的第二份。
    # render_structure() 留着不删：它是纯函数，没有调用者时不产出任何东西，
    # 万一要回退，接回来就是这一行。
    inner = (f'<div class="sapp">{lead_app}</div>' if lead_app else "")
    # 抽屉里全是平的：Boundary 一直就是这样，Why this matters / Writing Style /
    # Stage Contract 现在跟它一致（JL 260725：「I don't want to have >」，以及
    # 「why other information are gone」—— 它们没丢，是被第二层 ▸ 关起来了）。
    inner += render_subsections(opening_sections, flat=True)
    if is_stage:
        inner += render_contract(contract_sections, lead=legacy_record)
    # Opening 本身不折（JL 260725：「no > in the Opening, it will always be there」）：
    # 🧭 Opening 这一行和领句永远在台面上。可点的是【领句】—— 点开它，Boundary、
    # Why this matters、Writing Style、Stage Contract 全在这一个抽屉里，用来解释这句问句。
    # 中间那版把折叠挂在 🧭 Opening 上，于是节名本身成了一个只写着「Opening」的 ▸ 行，
    # 读者看不出里头有 Boundary —— 正是 260724 那条 Law 要防的（fold 生效且不可见）。
    # 领句的排版跟原版一模一样：<summary> 里仍然是那个 <p class="qlead">，
    # 所以 `.q p` 的 serif 和 `.ask>p:first-of-type` 的字号都照旧命中（JL 260725：
    # 「I want the original font size and font type」—— 把 class 挪到 summary 上就丢了这两条）。
    lead_p = (f'<p class="qlead"><span class="qt">{qlead}</span>'
              + (f'<span class="sbadge">{lead_kind} {lead_heads}</span>' if lead_heads else "")
              + '<span class="cv"></span></p>')
    opening_head = '<div class="ch opening-head"><span class="chl">🧭 Opening</span></div>'
    qblock = (
        # The Opening drawer stays shut even when the lead carries a comment
        # (JL 260801: everything collapsed). The ⚑/💬 badge on the lead says it
        # is there, which is the same contract every other sentence now keeps.
        f'<details class="it row qd"><summary>{lead_p}</summary>'
        f'<div class="bd qbd">{inner}</div></details>'
        if inner else
        f'<p class="qlead"><span class="qt">{qlead}</span></p>'
    )
    ask = f'<div class="ask">{opening_head}{qblock}</div>'
    bnd = ""   # Boundary 现在收在 ask 的折叠块里，不再单独上台面
    # 📁 Files（JL 260723 新增，选填）：这题牵动哪些文件。读懂之后知道去哪儿动手；
    # 反过来改了哪个文件，也知道该回写哪一题。路径写反引号里，board.md 的
    # ## Links 声明过的会自动变成可点链接。
    # Files groups FOLD, like Content parts and the Aims/States groups
    # (JL 260802). Files was the last section rendering its `###` groups as
    # flat rows, so a long action map could not be collapsed to its group
    # names while every other section on the page could.
    flb = render_subsections(parse_content_sections(sec(q["sec"], "Files")))
    fls = sect("📁 Files", flb, cls="fls")
    dia_txt = sec(q["sec"], "Diagram")
    dia = render_diagram(dia_txt) if dia_txt else ""
    display_preview = render_display_preview(q)
    content = render_content(content_sections, q if is_stage else None,
                             leading=display_preview)

    ndisc = len(re.findall(r"^>+\s*[A-Z]{1,4}\d{0,4}\s*[「\"：:]", disc, re.M))
    # 讨论里加个「整段写想法」的框（要 serve.py 跑着）：写完 → 追加进 ## Discussion。
    # 不钉在某句话上，就是自由讨论；serve.py 没跑时按钮会提示改走手写（JL 260723）。
    dadd = (f'<div class="dadd" data-file="{esc(q.get("file",""))}">'
            f'<textarea placeholder="Write a thought into the discussion…"></textarea>'
            f'<div class="row"><select></select>'
            f'<button class="dsave" type="button">➕ Add to discussion</button></div></div>')
    # The form comes FIRST, above the thread (JL 260802): it is the one thing
    # in this fold a reader can act on, and the newest exchange is right under
    # it, so writing a reply never means scrolling past the whole history.
    folds = det(f"💬 Discussion ({ndisc})",
                dadd +
                (render_thread(disc) if disc else
                 f'<p class="mut">No discussion yet — add a line under '
                 f'<code>## Discussion</code> in {q["file"]}: '
                 f'<code>&gt; Comment JL …</code></p>'))
    # Why here 不再上台面（它的活并进 ## Question 的要点）；老板子里还写着的收进折叠区
    folds += det("💡 Why here", body(why, apparatus=False))
    # Every fold says how much is inside, the way Discussion and Log already
    # did (JL 260802). A shut row with no count makes a reader open it to find
    # out whether it is worth opening, which is the job the count removes.
    def _n(name):
        return len(re.findall(r"(?m)^\s*[-*]\s+\S", sec(q["sec"], name)))
    for icon, name in (("⚖️", "Law"), ("🧠", "Lesson"), ("📖", "Glossary")):
        n = _n(name)
        folds += det(f"{icon} {name}" + (f" ({n})" if n else ""),
                     body(sec(q["sec"], name), apparatus=False, show_lead=True))
    log = sort_log(sec(q["sec"], "Log").strip())
    nlog = len(re.findall(r"^(?:[-*]\s+)?\d{6}(?:\s+\d{3,4})?\s*[·|]", log, re.M))
    folds += det(f"📜 Log ({nlog})", note_body(log, apparatus=False))
    return (
        f'<section class="slide q {cls}" id="{q["id"]}"'
        f' data-title="{esc(q["title"])}" data-file="{esc(q.get("file",""))}"'
        f' data-session="{esc(q.get("session",""))}">'
        f'<div class="qh"><span class="qid">{q["id"]}</span>'
        f'<span class="pill {cls}">{tok} {esc(lab)}</span>'
        f'<span class="mut">{esc(who)}</span>'
        f'<span class="mut">· {inline(q["method"])}</span>'
        + (
            f'<span class="kind">'
            f'{esc(STAGE_LABELS.get(q.get("family"), "STAGE"))}</span>'
            if q.get("kind") == "stage" else
            # the skill kind wears its own badge (JL 260731): a skill page is a
            # synced mirror, and the head should say so before the prose does
            ('<span class="kind">SKILL</span>' if q.get("kind") == "skill" else
             ('<span class="kind">AGENT</span>' if q.get("kind") == "agent" else ""))
        )
        # 文件名做成链接：点它直接看这一题的原始 markdown（serve.py 把它当纯文本发）
        + f'<a class="src" href="{esc(q.get("file",""))}" target="_blank"'
        f' title="Open this question\'s raw markdown">📄 {esc(q.get("file",""))}</a>'
        f'<a class="top" href="#top">↑ Index</a></div>'
        # id 后面那个空格是真字符（不是 CSS margin）——复制这行标题时
        # 才不会粘成 QA4Single…，而是 QA4 Single…（JL 260723）
        f'<h2 class="h2"><span class="hid">{q["id"]} </span>{inline(q["title"])}</h2>'
        + f'<div class="opening">{ask}{bnd}</div>' + dia + content
        + f'{fs}{fls}<div class="folds">{folds}</div>{nav}</section>')
