"""A paper version (a writing Job, j11_writing_<version>) on the focus page: its Delivery views (the paper, the Word
files, the supplement, the files) and its Work views (Draft-Main · Draft-Appendix · Display-Main · Display-Appendix),
one row per Section with its five step words (b16 s35, s36)."""
from __future__ import annotations

import re
from pathlib import Path

from live.frame import esc
from live.ui_parts import GROUP_CSS, PROCESS, RESULTS, _band, _file_link, _numbered, _section, _when
from live.focus_draft import CSS, JS, WORK, _facts, preview, word
from live.board_read import PAPER_CAPTIONS, _num, _task_url, display_job, is_version
from live.board_interactions import ix_item
from live.board_evidence import evidence_item
from live.address_links import linked_views, page_linker


def built_outputs(vdir: Path) -> dict | None:
    """The build's named outputs, or None when there is none to show. The Word step alone writes `outputs` as a list when
    no build came before it (it keeps a build's dict, `carried_over`); reading the list dropped the connection
    (Paper-PhyAbsence 261103: "'list' object has no attribute 'get'")."""
    import json
    try:
        out = json.loads((vdir / "build-manifest.json").read_text(encoding="utf-8")).get("outputs", {})
    except Exception:
        return None
    return out if isinstance(out, dict) else None


def build_running(vdir: Path) -> bool:
    """A build of this delivery folder is running now: build_delivery.py's lock file (same name as its `lock_path`) names
    a live process. The file keeps its words after a crash, so the process is what counts. The panel only reads it."""
    import hashlib, os, tempfile
    digest = hashlib.sha1(str(vdir.resolve()).encode("utf-8")).hexdigest()[:12]
    try:
        held = re.match(r"build pid (\d+) ", (Path(tempfile.gettempdir()) / f"haipipe-paper-build-{digest}.lock").read_text(encoding="utf-8"))
        if held:
            os.kill(int(held.group(1)), 0)
        return bool(held)
    except PermissionError:      # alive, under another user
        return True
    except (OSError, ValueError):
        return False


def paper_rows(vdir: Path, root: Path) -> str:
    """The assembled paper of one version: PDF, Word, Word supplement (each opens in the pop-out), built when, its state;
    then the earlier rounds the word lane keeps."""
    out = built_outputs(vdir)
    if out is None:
        return ""
    sup = out.get("supplement_docx_pdf")
    pieces = [("The whole paper · PDF", out.get("pdf")), ("Word", out.get("docx")),
              ("Word supplement", sup[:-4] + ".docx" if sup else None)]
    rows, shown = [], set()
    for label, rel in pieces:
        f = vdir / rel if rel else None
        if not f or not f.is_file():
            continue
        shown.add(f.name)
        state = "draft" if "-draft" in f.stem else "built"
        rows.append(f'<div class=fd-row><span class=n>{esc(label)}</span><span class=d>{_file_link(f, root)}</span>'
                    f'<span class=w>{esc(state)} · {_when(f)}</span></div>')
    older = sorted((f for f in (vdir / "word").glob("*.docx") if f.name not in shown and "supplement" not in f.name),
                   key=lambda f: f.stat().st_mtime, reverse=True) if (vdir / "word").is_dir() else []
    earlier = "".join(f'<div class=fd-row><span class=n>Earlier round</span><span class=d>{_file_link(f, root)}</span>'
                      f'<span class=w>{_when(f)}</span></div>' for f in older)
    if earlier:                                  # behind one closed fold (JL 261103: "first to hide them")
        rows.append('<details><summary style="cursor:pointer;color:var(--muted);padding:6px 0">Earlier rounds</summary>'
                    + earlier + '</details>')
    return "".join(rows)


def section_lanes(vdir: Path, job: Path, root: Path) -> str:
    """Each Section's built lanes (web, latex, word), one row per Section, its files opening in the pop-out."""
    tasks = [t.name for t in sorted(job.glob("t[0-9]*_*"))] if job.is_dir() else []
    names = tasks + sorted(d.name for d in vdir.glob("t[0-9]*_*") if d.is_dir() and d.name not in tasks)
    rows = []
    for name in names:
        d = vdir / name
        if not d.is_dir():
            continue
        main = (("web", d / "web" / "index.html"), ("LaTeX", d / "latex" / f"{name}.pdf"), ("Word", d / "word" / f"{name}.docx"))
        files = [(lane, f) for lane, f in main if f.is_file()]       # each lane's main file, as the Section's Delivery
        if files:
            rows.append(f'<div class=fd-row><span class=n>{esc(name)}</span><span class=d>'
                        + " · ".join(f'{lane}: {_file_link(f, root)}' for lane, f in files) + '</span></div>')
    return "".join(rows)


def version_delivery_views(job: Path, root: Path) -> dict:
    """A paper version's Delivery view-button-list: Paper · Word · Supplement · Files, each previewed in the page; the
    send waits here, since the paper is what is sent. {} when the Board holds no built paper for this version."""
    vdir = job.parent / "delivery" / job.name
    out = built_outputs(vdir)
    if out is None:
        return {}
    at = lambda key: vdir / out[key] if out.get(key) else None
    table = job.parent / "delivery" / "delivery.md"
    sent = table.is_file() and any(job.name in ln and "sent" in ln.lower() for ln in table.read_text(encoding="utf-8").splitlines())
    ask = "" if sent else (CSS + '<div class=fd-ask role=status><span>Waiting for you: check the paper, then mark the send '
                           'in <code>delivery.md</code>.</span></div>')            # on every view: the paper is what is sent
    views = {"paper": ("Paper", lambda: ask + preview(at("pdf"), root)),
             "word": ("Word", lambda: ask + preview(at("docx_pdf"), root, at("docx")))}
    if out.get("supplement_docx_pdf"):
        sup = at("supplement_docx_pdf")
        views["supplement"] = ("Supplement", lambda: ask + preview(sup, root, sup.with_suffix(".docx")))
    views["files"] = ("Built files", lambda: CSS + ask + _section("The paper", paper_rows(vdir, root), "sent" if sent else "built")
                      + _section("Its Sections", section_lanes(vdir, job, root), "built") + JS)
    return views


def paper_delivery(folder: Path, root: Path) -> str:
    """A version Job's Delivery (its paper, then its Sections), or a Board's (each version's paper); "" elsewhere."""
    from live.frame import level_of
    level = level_of(folder)
    if level == "Job":
        vdir = folder.parent / "delivery" / folder.name
        if not is_version(folder) and vdir.is_dir():   # an evidence or submission Job: what the Board's delivery/<Job>/
            files = sorted(f for f in vdir.rglob("*") if f.is_file() and not f.name.startswith("."))   # holds for it (r02:
            rows = "".join(f'<div class=fd-row><span class=n>{_file_link(f, root)}</span><span class=w>built {_when(f)}</span>'   # the
                           '</div>' for f in files)                                               # fill page was not listed)
            return CSS + _section("Handed over", rows, f"{len(files)} file{'s' * (len(files) != 1)}") + JS if rows else ""
        paper = paper_rows(vdir, root) if (vdir / "build-manifest.json").is_file() else ""
        return (CSS + _section("The paper", paper, "built") + _section("Its Sections", section_lanes(vdir, folder, root), "built")
                + JS) if paper else ""
    if level == "Block":
        out = "".join(_section(v.name, paper_rows(v, root), "built") for v in sorted((folder / "delivery").glob("j[0-9]*_*"))
                      if (v / "build-manifest.json").is_file()) if (folder / "delivery").is_dir() else ""
        return CSS + out + JS if out else ""
    return ""


# ── a paper version's Work: Draft-Main · Draft-Appendix · Display-Main · Display-Appendix (JL 261031, b16 t02 r02 Q2: A,
# s36-D02); one row per Section with its five step words, each opening that step (Q1: A, s36-D01). Displays are one
# Job of their own beside the versions, one Task per figure or table (s01-D11): the Display views list its Tasks ──────
VERSION_BANDS = (("draft-main", "Draft-Main", "sections", (0, 19)), ("draft-appendix", "Draft-Appendix", "sections", (20, 39)),
                 ("display-main", "Display-Main", "displays", (0, 49)), ("display-appendix", "Display-Appendix", "displays", (50, 99)))


VERSION_CAPTIONS = {"draft-main": "The main paper's Sections, each with its five steps; a word opens that step.",
                    "draft-appendix": "The appendix's Sections, each with its five steps; a word opens that step.",
                    "display-main": "The main paper's figures and tables, from the paper's display Job.",
                    "display-appendix": "The appendix's figures and tables, from the paper's display Job."}


PAPER_CAPTIONS.update({"work-" + k: v for k, v in VERSION_CAPTIONS.items()})


# a version's Report shows the same views, results only (261106); the Values and Citations keys stay the Board's
PAPER_CAPTIONS.update({"draft-main": "The main paper's Sections, each one's text to read.",
                       "draft-appendix": "The appendix's Sections, each one's text to read.",
                       "display-main": VERSION_CAPTIONS["display-main"], "display-appendix": VERSION_CAPTIONS["display-appendix"],
                       "values": "The printed numbers, one Task per group, each read from a returned Result.",
                       "citations": "The citations, one Task per claim group, each paper checked."})


def section_row(task: Path, root: Path) -> str:
    """A Section: its name, then its five step words, each opening that step (s36-D01)."""
    try:
        f, st, k = _facts(task, root)
        chips = "".join(f'<a class="fd-step {cls}" href="{esc(_task_url(task, root, key))}">{esc(step.split(" · ")[1])} '
                        f'<b>{esc(w)}</b></a>' for key, step in WORK for w, cls in [word(st[step], k)])
    except Exception:
        chips = '<span class=mut>its steps do not read yet</span>'
    return (f'<div class=fd-row><a class=n href="{esc(_task_url(task, root))}">{esc(task.name)}</a>'
            f'<span class="d fd-steps">{chips}</span></div>')


def version_work_views(version: Path, root: Path, items=(), item_html=None, work: bool = True) -> dict:
    """A version's views, Draft-Main · Draft-Appendix · Display-Main · Display-Appendix · Values · Citations (JL 261106:
    "a paper version's Report gets the same six views as its Work, showing results only"). `work`: Work's views, keys
    `work-<key>`, each ⚙️ Process then 📊 Results; else Report's, keys `<key>`, the Results alone, as board_views.banded.
    A Draft view's Results are its Sections' text, one side tab per Section (board_results.section_tabs)."""
    from live.board_results import _evidence_kinds, display_groups, section_tabs, sections_word, text_word
    from live.board_views import SIDE_CSS
    from live.ui_parts import PB_CSS, PB_JS
    item_html = (lambda r: ix_item(r, root)) if item_html else None     # each item a folded row (JL 261031)
    if not is_version(version):                   # the display Job (j21_displays) and the citation Job are not versions
        return {}
    pre = "work-" if work else ""
    from live.focus_draft import text_count
    changes, since = send_changes(version), evidence_since(version)   # a revision: what this send did to each tab

    def page(proc: str, res: str) -> str:
        body = (_band(PROCESS, _numbered(proc)) + _band(RESULTS, _numbered(res))) if work else _numbered(res)
        return CSS + VERSION_CSS + GROUP_CSS + PB_CSS + SIDE_CSS + body + PB_JS + JS

    views = {}
    for key, name, kind, (lo, hi) in VERSION_BANDS:
        def build(kind=kind, lo=lo, hi=hi, name=name, key=key):
            if kind == "sections":
                tasks = [t for t in sorted(version.glob("t[0-9]*_*"), key=_num) if t.is_dir() and lo <= _num(t) <= hi]
                rows = "".join(section_row(t, root) for t in tasks) or f'<p class=mut>No {esc(name)} Section yet.</p>'
                # ⚙️ Process: each Section and its five step words; 📊 Results: each Section's text to read (261106)
                proc = _section("🪜 Sections", rows, *sections_word(tasks, root))
                words = {t: changes.get(t) for t in tasks} if changes else None if work else {t: text_count(t) for t in tasks}
                res = _section("📝 Text", section_tabs(tasks, root, f"vt{key[-4:]}", words) if tasks else
                               f'<p class=mut>No {esc(name)} Section yet.</p>', text_word(tasks))
                return page(proc, res)
            # the paper's displays, drawn as the Board's Displays (side tabs, grouped Main then the appendix; r02: "move
            # Display-Main, Values and Citations rows into side tabs, as on the Board's Evidence"): Main here, the rest in
            # Display-Appendix, by where the display plan puts each one
            job = display_job(version)
            if job is None:
                return page("", _section("🖼️ Displays", '<p class=mut>No display Job yet: the paper\'s figures and tables '
                                                       'become one Job beside the versions, one Task per figure or table.</p>',
                                         "nothing yet"))
            tasks = [t for t in sorted(job.glob("t[0-9]*_*"), key=_num) if t.is_dir() and not t.name.startswith("t99_")]
            only = ("main",) if key == "display-main" else ("supplement", "unplanned")
            placed = display_groups(version.parent, tasks)
            tasks = [t for t in tasks if placed.get(t) in only]
            res, _ = _evidence_kinds(version.parent, root, ("Displays",), only=only, since=since)
            res = res or _section("🖼️ Displays", f'<p class=mut>No {esc(name)} display yet in {esc(job.name)}.</p>', "nothing yet")
            return page("", res)                # each display's state is its tab's (JL 261109), no second list
        views[pre + key] = (name, build)
    # Values and Citations: the paper's evidence Jobs beside the version (j02_evidence_value, j03_evidence_cite), drawn
    # as the Board's Evidence (side tabs; the whole-paper check once, a verdict line; each key counted once)
    for key, name, pat in (("values", "Values", r"evidence_value|value"), ("citations", "Citations", r"evidence_cite|citation|cite")):
        job = next((j for j in sorted(version.parent.glob("j[0-9]*_*")) if j.is_dir() and not is_version(j)
                    and re.search(pat, j.name, re.I) and not re.search("display|submission", j.name, re.I)), None)
        tasks = [x for x in sorted(job.glob("t[0-9]*_*"), key=_num) if x.is_dir() and not x.name.startswith("t99_")] if job else []
        if tasks:
            def build(tasks=tasks, name=name):
                res, _ = _evidence_kinds(version.parent, root, (name,), since=since)
                return page("", res)            # each item's state is its tab's (JL 261109), no second list
            views[pre + key] = (name, build)
    return linked_views(views, page_linker(version, root))   # every bNN.jNN.tNN.rNN a link (address_links, JL 261103)


def _came_from(version: Path) -> Path | None:
    """The version a revision was made from (its face's `from:`), None for a first send."""
    from live.board_read import _field
    came = _field(_face_of(version), "from")
    prev = version.parent / came if came else None
    return prev if prev is not None and prev.is_dir() and prev != version else None


def send_changes(version: Path) -> dict:
    """{Section: what this send did to it} of a revision (r02: "what changed since version 1: could not"): "new in this
    send" when the version it came from has no such Section, "changed" (for whoever's point lands on it) when its text
    differs, else "same as <that version>" (and whose point still lands on it). {} for a first send."""
    from live.focus_draft import paragraphs
    prev = _came_from(version)
    if prev is None:
        return {}
    points = reviewer_points(version)
    out = {}
    for t in (x for x in version.glob("t[0-9]*_*") if x.is_dir()):
        old = prev / t.name
        who = list(dict.fromkeys(w for _, w, lands, _, _ in points if w and lands.split()[:1] == [t.name]))
        if not old.is_dir():
            out[t] = "new in this send"
        elif [x[2] for x in paragraphs(t)] != [x[2] for x in paragraphs(old)]:
            out[t] = "changed" + (f" for {' and '.join(who)}" if who else "")
        else:
            out[t] = f"same as {prev.name}" + (f"; {' and '.join(who)}'s point lands here" if who else "")
    return out


def evidence_since(version: Path):
    """A revision's word for an evidence tab (a display, a value table, a claim group; they are the Board's, shared by
    every send): "asked by <who>" when a reviewer's point names it, "new in this send" when this send's text names it
    and the version it came from never did, else "same as <that version>". None for a first send."""
    from live.focus_draft import paragraphs
    from live.board_read import _field
    prev = _came_from(version)
    if prev is None:
        return None
    points = reviewer_points(version)
    text = lambda v: " ".join(t for s in v.glob("t[0-9]*_*") if s.is_dir() for _, _, t in paragraphs(s))
    now, before = text(version), text(prev)
    said = lambda name, words: re.search(rf"(?<![\w-]){re.escape(name)}(?![\w])", words, re.I) is not None

    def since(task, head):
        face = _face_of(task) if task is not None else ""
        names = [x for x in (_field(face, "number"), _field(face, "label"), re.sub(r"\s*\(.*\)$", "", head or "")) if x]
        who = list(dict.fromkeys(w for p, w, *_ in points if w and any(said(n, p) for n in names)))
        if who:
            return f"asked by {' and '.join(who)}"
        if any(said(n, now) and not said(n, before) for n in names):
            return "new in this send"
        return f"same as {prev.name}"
    return since


def version_report_views(version: Path, root: Path) -> dict:
    """A version's Report: its MindMap (the send's facts, a revision's reviewer points, each Section's question), then
    its Work's six views, the Results alone (JL 261106, decision 1). The focus page keeps the MindMap first."""
    views = version_work_views(version, root, work=False)
    if views:
        views = {"mindmap": ("MindMap", lambda: version_mindmap(version, root)), **views}
    return views


VERSION_CSS = """<style>.fd-steps{display:flex;gap:6px;flex-wrap:wrap}.fd-step{font-size:12px;border:1px solid var(--line);
border-radius:6px;padding:1px 8px;text-decoration:none;color:var(--ink)}.fd-step b{font-weight:500;color:var(--muted)}
.fd-step.fd-you{border-color:#ffa94d}.fd-step.fd-you b{color:#b35c00}.fd-step.fd-ok b{color:#2b8a3e}
.fd-step:hover{border-color:var(--accent)}</style>"""


# ── a version's MindMap (stage-2 review round 2, 261106): the send's own facts as leaves of its root (state, venue,
# close, where it tells from, the version it revises and the comments it answers, as links); for a revision, the
# reviewers' points, each with the Section it lands on, its reply in the response letter and its state; then each
# Section with what it must find out (its reader question) and its next step. The Run tree stays in Status. ─────────
def _face_of(folder: Path) -> str:
    f = folder / f"{folder.name}.md"
    return f.read_text(encoding="utf-8", errors="ignore") if f.is_file() else ""


def _report_of(version: Path) -> Path | None:
    """The comments report a revision answers (its face's `responds-to:`), else None."""
    from live.focus_draft import responds_to
    return responds_to(version)


def reviewer_points(version: Path) -> list:
    """[(the point, who raised it, the Section it lands on, its reply, its state)] from the comments report, each reply
    read from the response letter itself (focus_draft.review_points; r02: two points said "routed" while the letter
    held a reply to each), so the map, the letter's Answers line and its Text agree."""
    from live.focus_draft import paragraphs, review_points
    report = _report_of(version)
    if report is None:
        return []
    letter = next((t for t in sorted(version.glob("t3[0-9]_*response*")) if t.is_dir()), None)
    paras = {pid.split(".")[-1]: name for pid, name, _ in paragraphs(letter)} if letter is not None else {}
    return [(point, who, lands, (f"{letter.name} {reply}: {paras[reply]}" if letter is not None and reply in paras else
                                 f"{letter.name} {reply}" if reply and letter is not None else "not written yet"), state)
            for point, who, lands, reply, state in review_points(report, letter)]


# A read-only map drawn inside its own box (r03: the leaves ran 94 px past the box, and at 390 px the opened map was
# 5,000 px tall with every leaf cut off): the leaves wrap in the space left, a phone stacks each branch over its
# leaves; no `.focus-map` class, so the frame's map script adds no second fold bar (⊟ ⊞) and no folds of its own, and
# the map's own Open all opens every level.
MAP_CSS = """<style>.vmap{border:1px solid var(--line);border-radius:10px;padding:12px 14px 14px;background:var(--paper);
overflow:hidden}.vmap .pm{width:auto;min-width:0;grid-template-columns:170px minmax(0,1fr);gap:0 32px}
.vmap .pm-para{grid-template-columns:210px minmax(0,1fr);gap:0 30px;margin:3px 0}
.vmap .pm-leaves,.vmap .pm-leaves li,.vmap .pm-sub li{white-space:normal!important;min-width:0;max-width:none!important;
overflow-wrap:break-word}.vmap .pm-root b{font-size:15px;overflow-wrap:break-word}.vmap .pm-pnode{font-size:13.5px}
.vmap .pm-leaves li{font-size:13px}.vmap .pm-s{display:none}.vmap .pm-more[data-empty]{display:none}
.vmap .pm-role:empty{display:none}.vmap .pm-leaves li>.pm-role,.vmap .pm-sub li>.pm-role{min-width:0;padding:0 8px;
border-color:transparent;background:var(--tab-wash,#e7f5ff);color:var(--tab-on,#1864ab);font-weight:600;font-size:12px}
.vmap .pm-sub{padding-left:18px}.vmap .pm-foldbar{margin:0 0 8px}
@media(max-width:600px){.vmap{padding:10px}.vmap .pm{grid-template-columns:minmax(0,1fr);gap:10px 0}
.vmap .pm-para{grid-template-columns:minmax(0,1fr);gap:4px 0;margin:8px 0}.vmap .pm-wires{display:none}
.vmap .pm-leaves{margin-left:10px;padding-left:10px;border-left:2px solid var(--line)}.vmap .pm-sub{padding-left:12px}}
</style>"""


def breakable(name: str) -> str:
    """A folder name that breaks only after "_" (r03: "j11_writing_v1130_des / k"): a zero-width space after each."""
    return name.replace("_", "_\u200b")


def paper_map(title: str, kids: list, note=(), key: str = "map") -> str:
    """One read-only map of a paper page (a version, an evidence Job, an evidence Task, the Board's Paper flow): its
    root, then a branch per kid, each leaf a "[role] words" line; ids relative to the page (no folder path in the
    HTML)."""
    from live import frame
    mm_ = frame.mindmap_module()                 # puts haipipe-mindmap's scripts on the path first
    import mmbuild
    import mmtree
    node = mmbuild.built(".", breakable(title), kids, list(note))
    node.id = "root"
    tree = mmtree.MindMap({"mindmap": "1", "title": title, "built": "focus-page"}, node)
    return MAP_CSS + f'<div class="vmap" data-map="{esc(key)}">' + mm_.draw(tree, "", editable=False) + '</div>'


def version_mindmap(version: Path, root: Path) -> str:
    """The version's map: its root's leaves, the reviewers' points (a revision), its Sections with their questions."""
    try:
        return _version_mindmap(version, root)
    except Exception:                            # a map that does not draw never takes the page down
        import traceback
        traceback.print_exc()
        return '<p class=mut>The map does not draw yet.</p>'


def _version_mindmap(version: Path, root: Path) -> str:
    from live import frame
    from live.board_read import _field, _section_state, _state_words
    from live.address_links import href
    frame.mindmap_module()                       # puts haipipe-mindmap's scripts on the path first
    import mmbuild
    text = _face_of(version)
    v = version.name
    link = lambda words, folder, extra="": f"[{words}]({href(folder, root, extra)})"
    facts = []                                   # the send's own facts; a link opens the version it revises or the
    for role, key in (("state", "state"), ("venue", "venue"), ("close", "close"), ("tells", "tells")):   # comments
        val = _field(text, key)                                                                          # it answers
        if val:
            facts.append(mmbuild.built(f"{v}/{key}", f"[{role}] {val}"))
    came = _field(text, "from")
    if came and (version.parent / came).is_dir():
        facts.append(mmbuild.built(f"{v}/from", f"[from] {link(came, version.parent / came)}"))
    report = _report_of(version)
    if report is not None:
        facts.append(mmbuild.built(f"{v}/responds", f"[responds to] [{report.parent.name}]({frame.reader(report, root)})"))
    kids = [mmbuild.built(f"{v}/send", f"This send · {_field(text, 'state') or 'open'}", facts)] if facts else []
    points = reviewer_points(version)
    if points:
        nodes = [mmbuild.built(f"{v}/point/{i}", f"[{state or 'open'}] {point}",
                               [mmbuild.built(f"{v}/point/{i}/who", f"[raised by] {who}")] * bool(who)
                               + [mmbuild.built(f"{v}/point/{i}/lands", f"[lands on] {lands}")] * bool(lands)
                               + [mmbuild.built(f"{v}/point/{i}/reply", f"[reply] {reply}")])
                 for i, (point, who, lands, reply, state) in enumerate(points)]
        done = sum(st in ("answered", "applied") for *_, st in points)
        # the closed branch carries its tally (r02: "Reviewer points" showed none)
        kids.append(mmbuild.built(f"{v}/points", f"Reviewer points · {done} of {len(points)} answered", nodes))
    sections, waits = [], 0
    for t in sorted(x for x in version.glob("t[0-9]*_*") if x.is_dir()):
        face = _face_of(t)
        first = face.split("\n", 1)[0]
        title = first.split(" · ", 1)[1].strip() if " · " in first else t.name.split("_", 1)[-1]
        asks = _field(face, "reader-question") or _field(face, "goal")
        step = _state_words(_section_state(t, root))
        waits += "your" in step
        sections.append(mmbuild.built(f"{v}/{t.name}", f"[{t.name}] {title}",
                                      [mmbuild.built(f"{v}/{t.name}/asks", f"[finds out] {asks}")] * bool(asks)
                                      + [mmbuild.built(f"{v}/{t.name}/step", f"[now] {step}")] * bool(step)))
    if sections:                                 # its state word on the closed branch, not a bare count (r03: "▾ 2")
        said = f"{waits} wait{'s' * (waits == 1)} for you" if waits else f"{len(sections)} Sections"
        kids.append(mmbuild.built(f"{v}/sections", f"Sections · {said}", sections))
    return paper_map(v, kids, key=v)
