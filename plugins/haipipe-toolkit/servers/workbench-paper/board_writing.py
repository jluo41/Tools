"""A paper Board's Writing view: each version's Sections as side tabs to read, the assembled paper's files
(LaTeX, Word, Submission), the portal packet, and the state words of each."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import esc
from live.ui_parts import _cap, _open_btn, _section, _side_tabs, _when, plural_word
from live.focus_draft import paragraphs
from live.board_read import _section_state, _state_words, _task_url, _version_url, is_version
from live.paper_version import build_running


def _section_read(task: Path, root: Path | None = None) -> str:
    """A Section's text to read: its paragraphs in order, each under its name, each sentence on its own numbered line
    (JL 261101: "the content here is not readable? could you still make each sentence to be a line"); a citation
    command reads as its keys. One owner, focus_draft.content_read, so the Section's own Text reads the same (r02)."""
    from live.focus_draft import content_read
    return content_read(task, root) or '<p class=mut>No text yet: 2 · Write writes it.</p>'


def _pdf_facts(pdf: Path | None) -> tuple[str, str]:
    """A PDF's page count and the program that drew it, read from the file on every open."""
    import subprocess
    if pdf is None or pdf.suffix != ".pdf":
        return "", ""
    try:
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return "", ""
    field = lambda k: (re.search(rf"^{k}:\s*(.+)$", info, re.M) or [None, ""])[1].strip()
    return field("Pages"), field("Producer")


def _tab_flag(kind: str, man: dict, pdf: Path | None, running: bool, stand_in: bool = False) -> str:
    """Each tab's state, one short line on the tab (JL 261104: "could you flag each tab' status?"): can it be read now,
    and what is not final yet. Everything comes from the manifest and the file itself; nobody types it."""
    pages, producer = _pdf_facts(pdf)
    count = f" · {pages} pages" if pages else ""
    draft = " · draft" if man.get("status") != "READY" else ""
    if kind == "latex":
        if running and not man.get("pdf_only"):
            return "⏳ Rebuilding: last build shown"
        return f"✅ Read now{draft}{count}"
    if kind == "word":
        if running:
            return "⏳ Rebuilding: do not open"
        if stand_in or "LibreOffice" in producer:
            return "❗ Word stuck: layout not final"
        return f"✅ Read now{draft}{count}"
    if kind == "letter":
        cover = man.get("cover_letter") or {}
        off = [c for c in cover.get("checks", []) if not c.get("ok")]
        return "❗ Checks open" if off else f"✅ Read now{draft}"
    if kind == "portal":
        return "⬜"                               # each slot shows its own state in the portal table
    return ""


def _tracked_word(vdir: Path) -> tuple:
    """The co-authors' own Word file with their tracked changes and comments kept and ours added as tracked changes (JL
    261110: "the Word-Change-Track, which is based on the previous change tracks from professors and you add the changes
    as well"): the newest *-tracked.pdf and .docx in delivery/<writing Job>/word-tracked/; its line, the newest
    headline.txt of a review Job's tracked-Word Run (e.g. "v4 + 37 changes by <author>"). (name, line, pdf, docx)."""
    folder = vdir / "word-tracked"
    newest = lambda pat: max(folder.glob(pat), key=lambda x: x.stat().st_mtime, default=None) if folder.is_dir() else None
    pdf, doc = newest("*-tracked.pdf"), newest("*-tracked.docx")
    heads = [h for h in vdir.parent.parent.glob("j[0-9]*_*review*/t[0-9]*_*tracked*/runs/*/result/headline.txt") if h.is_file()]
    head = max(heads, key=lambda x: x.stat().st_mtime, default=None)
    line = head.read_text(encoding="utf-8", errors="ignore").strip().splitlines()[0] if head else ""
    short = re.search(r"-(v\d+)\.docx \+ (\d+) tracked changes? by (.+?)\s*->", line)   # "<file>-v4.docx + 2 tracked
    line = f"{short[1]} + {short[2]} changes by {short[3]}" if short else line             # changes by X -> …" → "v4 + 2 changes by X"
    web = head.parent / "onedrive.txt" if head else None             # the shared copy in Word online (JL 261111)
    web = web.read_text(encoding="utf-8").strip() if web and web.is_file() else ""
    return ("Paper-Word-Tracked", line or "the co-authors' Word file, our changes tracked", pdf, doc, web)


def _latex_diff(vdir: Path) -> tuple:
    """The paper's change since the round the co-authors saw, as one LaTeX diff PDF (JL 261113: "make the paper - latex
    diff for me"; haipipe-paper-assemble scripts/latex_diff.py): the newest *-latexdiff.pdf in delivery/<writing
    Job>/latex-diff/; its line, the newest headline.txt of a review Job's latex-diff Run. (name, line, pdf, None)."""
    folder = vdir / "latex-diff"
    pdf = max(folder.glob("*-latexdiff.pdf"), key=lambda x: x.stat().st_mtime, default=None) if folder.is_dir() else None
    heads = [h for h in vdir.parent.parent.glob("j[0-9]*_*review*/t[0-9]*_*latex_diff*/runs/*/result/headline.txt") if h.is_file()]
    head = max(heads, key=lambda x: x.stat().st_mtime, default=None)
    line = head.read_text(encoding="utf-8", errors="ignore").strip().splitlines()[0] if head else ""
    return ("Paper-Latex-Diff", line or "what changed since the last round, in the venue's LaTeX", pdf, None)


def _paper_files(vdir: Path, root: Path, eid: str = "pp") -> str:
    """The assembled paper to read (JL 261101: "should we show it as well? like different versions of the output with the
    left panel?"): side tabs, each output on the left (the paper as LaTeX builds it, as Word prints it, the Word
    supplement, then earlier rounds), the open one shown on the right as its PDF, with its Open buttons."""
    import json
    try:
        man = json.loads((vdir / "build-manifest.json").read_text(encoding="utf-8"))
    except Exception:
        return ""
    out = man.get("outputs") or {}
    if not isinstance(out, dict):      # the Word step ran alone, with no build before it (see paper_version.built_outputs)
        return ""
    f = lambda r: vdir / r if r and (vdir / r).is_file() else None
    sup_pdf = f(out.get("supplement_docx_pdf"))
    sup_docx = f(out.get("supplement_docx_pdf", "")[:-4] + ".docx") if out.get("supplement_docx_pdf") else None
    letter = (man.get("cover_letter") or {}).get("outputs") or {}
    if not letter.get("pdf"):                    # JL 261103: "where is the cover letter?": a letter Task exported on its
        for own in sorted(vdir.glob("t3[0-9]_*letter*")):   # own, before the build has [coverletter], still shows
            letter = {"pdf": f"{own.name}/word/{own.name}.pdf", "docx": f"{own.name}/word/{own.name}.docx"}
            break
    by = man.get("word_pdf_printed_by") or {}      # b16.j02-s22 261104: Word stuck, and these tabs showed LibreOffice's print
    running_now = build_running(vdir)
    word_how = lambda key, pdf: _tab_flag("word", man, pdf, running_now, by.get(key) == "stand-in")
    # JL 261102: "we should say the results here as well": every document the build makes, the letter too
    pieces = [("Paper-Latex", _tab_flag("latex", man, f(out.get("pdf")), running_now), f(out.get("pdf")), None),
              ("Paper-Word", word_how("main_docx", f(out.get("docx_pdf"))), f(out.get("docx_pdf")), f(out.get("docx"))),
              _latex_diff(vdir),
              _tracked_word(vdir),
              ("Supplement-Latex", _tab_flag("latex", man, f(out.get("supplement")), running_now), f(out.get("supplement")), None),
              ("Supplement-Word", word_how("supplement_docx", sup_pdf), sup_pdf, sup_docx),
              ("Combined-Latex", "paper and supplement in one PDF", f(out.get("combined")), None),
              ("Cover-Letter", _tab_flag("letter", man, f(letter.get("pdf")), running_now), f(letter.get("pdf")), f(letter.get("docx")))]
    # JL 261102: "add the new tab for the submission portal": the send's submission Job (jNN_submission_…, its face
    # `for: <this version>`) writes delivery/<that Job>/portal-fill.html, every portal field with its value to paste
    for sj in sorted(vdir.parent.parent.glob("j[0-9]*_submission_*")):
        face = sj / f"{sj.name}.md"
        if face.is_file() and re.search(rf"(?m)^for:\s*{re.escape(vdir.name)}\s*$", face.read_text(encoding="utf-8", errors="ignore")):
            fill = vdir.parent / sj.name / "portal-fill.html"
            pieces.append(("Portal", _tab_flag("portal", man, None, running_now), fill if fill.is_file() else None, None))
    pieces = [_or_adopted(vdir, p) if p[0].endswith("· Word") else p for p in pieces]
    shown = {p.name for row in pieces for p in row[2:4] if p}
    word = vdir / "word"
    older = sorted((x for x in word.glob("*.docx") if x.name not in shown and "supplement" not in x.name),
                   key=lambda x: x.stat().st_mtime, reverse=True) if word.is_dir() else []
    pieces += [(f"Earlier round · {_when(x)}", x.stem, x.with_suffix(".pdf") if x.with_suffix(".pdf").is_file() else None, x) for x in older]
    pieces = [p for p in pieces if p[2] or p[3]]
    if not pieces:
        return ""
    # the named tabs by heading, then the rest (earlier rounds) in their own order; a tab missing from TAB_GROUPS
    # ("Combined-Latex" was, 261120) no longer breaks the page
    pieces = sorted((p for p in pieces if p[0] in TAB_GROUPS), key=lambda p: TAB_GROUP_ORDER.index(TAB_GROUPS[p[0]][0])) + \
        [p for p in pieces if p[0] not in TAB_GROUPS]
    earlier = sum(1 for p in pieces if p[0] in TAB_GROUPS)   # the named tabs come first; the rest fold under Earlier
    href = lambda x: "/" + quote(ds._rel(x, root))
    items, panels = [], []
    for name, how, pdf, doc, *web in pieces:
        newest = max((x for x in (pdf, doc) if x), key=lambda x: x.stat().st_mtime)
        items.append((TAB_GROUPS.get(name, (None, name))[1], how))
        made = f'<span class=pb-state>{"draft" if "-draft" in newest.stem else "built"} {_when(newest)}</span>'
        view = (f'<div class=pb-ptop>{made}{_open_btn("⤢ Pop out", href(pdf), f"{name} · {pdf.name}")}</div>'   # a large view pops out
                f'<iframe class=pb-pdf src="{esc(href(pdf))}{"" if pdf.suffix == ".html" else "#view=FitH"}" title="{esc(name)}"></iframe>') if pdf \
            else f'<p class=mut>{esc(how)}: no PDF beside it to show here.</p>'
        verbs = ((_open_btn("Open the page" if pdf.suffix == ".html" else "Open the PDF", href(pdf), pdf.name) if pdf else "")
                 + (_open_btn("Open the Word file", href(doc), doc.name) if doc else "")
                 + "".join(f'<a class=fd-btn href="{esc(w)}" target=_blank rel=noopener>Open in OneDrive</a>' for w in web if w))
        panels.append(view + f'<div class=pb-verbs>{verbs}</div>')
    running = '<p class=pb-state>⏳ A build is running: these are the last built files.</p>' if build_running(vdir) else ""
    draft = ('<p class=pb-state>📝 Word draft: displays float to page tops, not placed by measuring. Run a full build before sending.</p>'
             if man.get("word_draft") else "")
    tabs = _side_tabs(eid, items, panels)
    groups = [TAB_GROUPS[p[0]][0] for p in pieces[:earlier]]
    for k in reversed(range(len(groups))):                 # a heading over each group's first tab
        if k == 0 or groups[k] != groups[k - 1]:
            at = tabs.rindex("<button", 0, tabs.index(f'data-pbtab="{eid}{k}"'))
            head = (f'<p class=pb-tabgroup style="flex-basis:100%;margin:{0 if k == 0 else 14}px 0 4px;padding:0 9px;'
                    f'font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.04em">{esc(groups[k])}</p>')
            tabs = tabs[:at] + head + tabs[at:]
    return running + draft + _fold_earlier(tabs, eid, earlier, len(items))


# JL 261113: "we can add more subsections like the Latex, Word, portal here": each current file under its kind's heading,
# its tab named without the kind (the heading says it). Full name -> (heading, tab name); the pop-out keeps the full name.
TAB_GROUP_ORDER = ["LaTeX", "Word", "Submission"]


TAB_GROUPS = {   # JL 261121: "call it Paper-Latex, and Paper-Latex-Diff"; every item names its artifact (CONSTITUTION A01)
    "Paper-Latex": ("LaTeX", "Paper-Latex"),
    "Paper-Latex-Diff": ("LaTeX", "Paper-Latex-Diff"),
    "Supplement-Latex": ("LaTeX", "Supplement-Latex"),
    "Combined-Latex": ("LaTeX", "Combined-Latex"),
    "Paper-Word": ("Word", "Paper-Word"),
    "Paper-Word-Tracked": ("Word", "Paper-Word-Tracked"),
    "Supplement-Word": ("Word", "Supplement-Word"),
    "Cover-Letter": ("Submission", "Cover-Letter"),
    "Portal": ("Submission", "Portal"),
}


def _or_adopted(vdir: Path, row: tuple) -> tuple:
    """A Word row with no file: `word_round.py adopt` renames the build's -draft files to -v<n> (Paper-PhyAbsence 261104:
    "the panel's Word rows have no file until the next full build"), so the newest adopted copy shows until then."""
    name, how, pdf, doc = row
    if pdf or doc:
        return row
    supplement = "supplement" in name.lower()
    kept = sorted((x for x in (vdir / "word").glob("*-v[0-9]*.docx") if ("supplement" in x.name) == supplement),
                  key=lambda x: x.stat().st_mtime, reverse=True)
    if not kept:
        return row
    twin = kept[0].with_suffix(".pdf")
    return name, "the copy adopted for the round", twin if twin.is_file() else None, kept[0]


def _fold_earlier(tabs: str, eid: str, start: int, total: int) -> str:
    """The older rounds' side tabs behind one closed fold at the list's end (JL 261103: "for the early round, could you
    just first to hide them?"), no count; they open as before once it is unfolded. A build with nothing current yet
    leaves the fold open, so the panel on show has its tab in sight."""
    if start >= total:
        return tabs
    first = tabs.index(f'data-pbtab="{eid}{start}"')
    at, end = tabs.rindex("<button", 0, first), tabs.index("</div><div class=pb-read>", first)
    return (tabs[:at] + f'<details class=pb-earlier style="flex-basis:100%"{" open" if start == 0 else ""}>'
            '<summary style="cursor:pointer;font-size:13px;color:var(--muted);padding:6px 9px">Earlier rounds</summary>'
            + tabs[at:end] + "</details>" + tabs[end:])


PORTAL_WORDS = {"ready": "✅ ready", "draft": "🔶 built, not approved", "stale": "❗ stale", "missing": "⬜ missing"}


def _portal(vdir: Path, root: Path) -> str:
    """What goes into the venue's portal as it is (JL 261102: "the final delivery content that are ready to submit
    directly in the portal"): the build's portal packet, delivery/<job>/portal/, one row per upload slot with its
    file and its state, each file opening in the pop-out (haipipe-paper-assemble § The portal packet)."""
    import json
    try:
        portal = json.loads((vdir / "build-manifest.json").read_text(encoding="utf-8")).get("portal") or {}
    except Exception:
        return ""
    ups = portal.get("uploads") or []
    if not ups:
        return ""
    folder = vdir / str(portal.get("folder", "portal"))
    href = lambda x: "/" + quote(ds._rel(x, root))
    rows = []
    for i, u in enumerate(ups, 1):
        files = [folder / n for n in u.get("files") or [] if (folder / n).is_file()]
        links = " ".join(_open_btn(x.name, href(x), x.name) for x in files) or '<span class=mut>no file yet</span>'
        note = "; ".join(x for x in (u.get("detail", ""), u.get("note", "")) if x)
        rows.append(f'<tr><td>{i}</td><td>{esc(u.get("slot", ""))}</td><td>{links}</td>'
                    f'<td>{esc(PORTAL_WORDS.get(u.get("state"), u.get("state", "")))}</td><td class=mut>{esc(note)}</td></tr>')
    table = folder / "portal.md"
    head = (f'<p class=pb-state>Upload these files as they are, each into its slot · '
            f'{_open_btn("Open portal.md", href(table), table.name) if table.is_file() else ""}</p>')
    return (head + '<table class=pb-portal><tr><th>#</th><th>slot</th><th>file</th><th>state</th><th>note</th></tr>'
            + "".join(rows) + '</table>'
            + '<style>.pb-portal{border-collapse:collapse;width:100%;font-size:13px}.pb-portal td,.pb-portal th'
              '{border-top:1px solid var(--line);padding:5px 6px;text-align:left;vertical-align:top}</style>')


def writing_view(board: Path, root: Path, md, items=()) -> str:
    """F · Writing: a numbered section per version; its Sections as card tabs (each panel its step words), then the
    assembled paper."""
    out, n = "", 0
    plan = board / "revision-plan.md"               # the Board's plan for the round under way, first (JL 261110)
    if plan.is_file():
        text = re.sub(r"^#\s+.*\n", "", plan.read_text(encoding="utf-8"), count=1)
        n += 1                                    # each line keeps its own ✅ / ⬜ / ⏳; no tally on the bar
        out += _section(f"{n} · 🗺️ Revision plan", md(text, board) if md else f"<pre>{esc(text)}</pre>")
    for job in sorted(d for d in board.glob("j[0-9]*_*") if d.is_dir() and is_version(d)):
        tasks = sorted(d for d in job.glob("t[0-9]*_*") if d.is_dir())
        paper = _paper_files(board / "delivery" / job.name, root, f"pp{n}")
        n += 1
        word, waits = sections_word(tasks, root)
        out += _section(f"{n} · ✍️ {job.name}", f'<div class=pb-verbs>{_open_btn("Open the version", _version_url(job, root, "report"))}'
                        + STRUCT_BTN + '</div>'
                        + (section_tabs(tasks, root, f"wr{n}") if tasks else '<p class=mut>No Sections yet.</p>'), word, waits)
        if paper:
            n += 1
            out += _section(f"{n} · 📄 The assembled paper", paper, paper_word(board / "delivery" / job.name))
        portal = _portal(board / "delivery" / job.name, root)
        if portal:
            n += 1
            out += _section(f"{n} · 📮 Ready for the portal", portal, portal_word(board / "delivery" / job.name))
    rules = board / "writing-patterns.md"          # the Board's own list of patterns a co-author flagged (JL 261110)
    if rules.is_file():
        text = re.sub(r"^#\s+.*\n", "", rules.read_text(encoding="utf-8"), count=1)
        k = len(re.findall(r"^###\s+\d", text, re.M))
        n += 1
        out += _section(f"{n} · 🚫 Writing patterns to avoid", md(text, board) if md else f"<pre>{esc(text)}</pre>",
                        plural_word(k, "pattern", "patterns") if k else "the list")
    # every section starts closed (JL 261104: "this should be closed at the begining"); focus_draft's fold reads the mark
    return '<i data-fd-closed hidden></i>' + out if out else '<p class=mut>No version yet.</p>'


def section_tabs(tasks: list, root: Path, eid: str, words: dict | None = None) -> str:
    """Each Section's text to read, one side tab per Section (its name, its next step), its sentences on the right with
    its Open button in the corner: the Board's Writing and a version's Draft views draw the same tabs (JL 261106).
    `words` {Section: its word} names each tab's word instead (a revision: what this send did to it; a Report: how
    much text it has); a tab is never left without one (r03: the Cover letter tab had none)."""
    from live.focus_draft import text_count
    secs = [(_cap(re.sub(r"^t\d+_", "", t.name).replace("-", " ")), _state_words(_section_state(t, root))) for t in tasks]
    if words is not None:
        secs = [(h, words.get(t) or w) for (h, w), t in zip(secs, tasks)]
    elif len({w for _, w in secs}) == 1:        # the same step on every tab says nothing: how much text each has
        secs = [(h, text_count(t)) for (h, _), t in zip(secs, tasks)]
    panels = [f'<div class=pb-corner>{_open_btn("Open the Section", _task_url(t, root), t.name)}</div>' + _section_plan(t)
              + _section_read(t, root) for t in tasks]
    return _side_tabs(eid, secs, panels)


# JL 261113: "how about we just open it in the same page?": the button opens every Section's Structure fold of this
# version in place (and closes them on the next click), never a new page
STRUCT_BTN = ('<button type=button class=fd-btn onclick="var s=this.closest(\'.pb-verbs\').nextElementSibling,'
              'd=s.querySelectorAll(\'details.pb-struct\'),o=![].some.call(d,function(x){return x.open});'
              '[].forEach.call(d,function(x){x.open=o});this.classList.toggle(\'on\',o)">Structure</button>')


def _section_plan(task: Path) -> str:
    """The Section's Structure, its Plan mind map, folded above its text (JL 261113: "could we put a things named
    'Structure' so we can preview each section's structure here"); closed until clicked (AGENTS rule 15)."""
    from live.paper_structure import _plan_mind_map
    mm = _plan_mind_map(task, _cap(re.sub(r"^t\d+_", "", task.name).replace("-", " ")))
    return f'<details class=pb-struct><summary>Structure</summary>{mm}</details>' if mm else ""


def text_word(tasks: list) -> str:
    """The text bar's word: none. Each Section shows its own text or its absence; a count of the Sections with text
    is a progress tally, which a page never carries (AGENTS § Page words)."""
    return ""


def sections_word(tasks: list, root: Path) -> tuple:
    """(state word, waiting line) of a version's Sections: how many wait for you and the first of them, else how many
    are done (each Section's own next step, board_read._section_state)."""
    if not tasks:
        return "", ""
    states = [(t, _state_words(_section_state(t, root))) for t in tasks]
    you = [(t, w) for t, w in states if "your" in w]
    signs = _waiting_steps(tasks, root)          # every step that waits on you, as many as the sign chips (r02: "1
    if you or signs:                              # waits for you" stood beside two "sign" chips)
        n = max(len(signs), len(you))
        return f'{n} wait{"s" if n == 1 else ""} for you', ""   # no line under the bar: the word says it, the
                                                                  # rows say which (JL 261109: "we don't want this")
    return "", ""                                 # no "N of M done": each Section row shows its own mark


def _waiting_steps(tasks: list, root: Path) -> list:
    """[(Section, "<step>: waits for …")] of every step of these Sections that waits on the person (sign, asked, send,
    pass), in Section order."""
    from live.focus_draft import STATUS_WHAT, WAITS, WORK, _facts
    out = []
    for t in tasks:
        try:
            f, st, k = _facts(t, root)
        except Exception:
            continue
        out += [(t, f'{step.split(" · ")[1]}: {STATUS_WHAT[st[step]].format(k=k)}') for _, step in WORK if st.get(step) in WAITS]
    return out


def paper_word(vdir: Path) -> str:
    """The assembled paper's word: rebuilding while a build runs, else built (the manifest READY) or a draft."""
    import json
    if build_running(vdir):
        return "rebuilding"
    try:
        man = json.loads((vdir / "build-manifest.json").read_text(encoding="utf-8"))
    except Exception:
        return ""
    return "built" if man.get("status") == "READY" else "draft"


def portal_word(vdir: Path) -> str:
    """The portal packet's bar word: none. Each upload slot shows its own state in the portal table; a count of the
    ready ones is a progress tally, which a page never carries (AGENTS § Page words)."""
    return ""
