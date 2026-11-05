"""A paper version (a writing Job, j11_writing_<version>) on the focus page: its Delivery views (the paper, the Word
files, the supplement, the files) and its Work views (Draft-Main · Draft-Appendix · Display-Main · Display-Appendix),
one row per Section with its five step words (b16 s35, s36)."""
from __future__ import annotations

import re
from pathlib import Path

from live.frame import esc
from live.ui_parts import GROUP_CSS, PROCESS, RESULTS, _band, _file_link, _numbered, _section, _when
from live.focus_draft import CSS, JS, WORK, _facts, _interactions, preview, word
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
    views["files"] = ("Built files", lambda: CSS + ask + _section("The paper", paper_rows(vdir, root))
                      + _section("Its Sections", section_lanes(vdir, job, root)) + JS)
    return views


def paper_delivery(folder: Path, root: Path) -> str:
    """A version Job's Delivery (its paper, then its Sections), or a Board's (each version's paper); "" elsewhere."""
    from live.frame import level_of
    level = level_of(folder)
    if level == "Job":
        vdir = folder.parent / "delivery" / folder.name
        paper = paper_rows(vdir, root) if (vdir / "build-manifest.json").is_file() else ""
        return (CSS + _section("The paper", paper) + _section("Its Sections", section_lanes(vdir, folder, root)) + JS) if paper else ""
    if level == "Block":
        out = "".join(_section(v.name, paper_rows(v, root)) for v in sorted((folder / "delivery").glob("j[0-9]*_*"))
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


def version_work_views(version: Path, root: Path, items=(), item_html=None) -> dict:
    item_html = (lambda r: ix_item(r, root)) if item_html else None     # each item a folded row (JL 261031)
    if not is_version(version):                   # the display Job (j21_displays) and the citation Job are not versions
        return {}
    views = {}
    for key, name, kind, (lo, hi) in VERSION_BANDS:
        def build(kind=kind, lo=lo, hi=hi, name=name, key=key):
            if kind == "sections":
                tasks = [t for t in sorted(version.glob("t[0-9]*_*"), key=_num) if t.is_dir() and lo <= _num(t) <= hi]
                body = "".join(section_row(t, root) for t in tasks) or f'<p class=mut>No {esc(name)} Section yet.</p>'
            else:
                job = display_job(version)
                if job is not None:
                    tasks = [t for t in sorted(job.glob("t[0-9]*_*"), key=_num) if t.is_dir() and lo <= _num(t) <= hi]
                else:                              # displays as bands inside the version (b16 r02 Q3 A): t41-t49, t51-t59
                    band = (40, 49) if hi < 50 else (50, 59)
                    tasks = [t for t in sorted(version.glob("t[0-9]*_*"), key=_num) if t.is_dir() and band[0] <= _num(t) <= band[1]]
                    job = version if tasks else None
                body = ("".join(evidence_item(t, root) for t in tasks)
                        or (f'<p class=mut>No figure or table here yet in {esc(job.name)}.</p>' if job else
                            '<p class=mut>No display Job yet: the paper\'s figures and tables become one Job beside the versions, '
                            'one Task per figure or table (s01-D11).</p>'))
            # The same rows in the two parts every view has (JL 261101: "keep the content as much as possible but use the
            # new subsections layout"; "add the Interaction things as well, so we can track our changes along the way"):
            # ⚙️ Process is this page's interactions, then each Section and its step words; a display view's figures
            # and tables are its 📊 Results.
            asks = _interactions(version if kind == "sections" else (job or version), root)
            proc = _section("🙋 Interactions", asks) if asks else _section("🙋 Nothing waits on you", "<span hidden></span>")
            if kind == "sections":
                proc += _section("🪜 Sections", body)
                res = ""
            else:
                res = _section("🖼️ Displays", body)
            return CSS + VERSION_CSS + GROUP_CSS + _band(PROCESS, _numbered(proc)) + _band(RESULTS, _numbered(res)) + JS
        views["work-" + key] = (name, build)
    # Values and Citations: the paper's evidence Jobs beside the version (j02_evidence_value, j03_evidence_cite), else
    # bands inside a version (t61-t69, t71-t79); shown once they hold a Task (s36-D02: "even more of them. like the citations")
    for key, name, (lo, hi), pat in (("values", "Values", (60, 69), r"evidence_value"), ("citations", "Citations", (70, 79), r"evidence_cite|citation")):
        job = next((j for j in sorted(version.parent.glob("j[0-9]*_*")) if j.is_dir() and re.search(pat, j.name, re.I)), None)
        tasks = (sorted((x for x in job.glob("t[0-9]*_*") if x.is_dir()), key=_num) if job else []) or \
            [x for x in sorted(version.glob("t[0-9]*_*"), key=_num) if x.is_dir() and lo <= _num(x) <= hi]
        if tasks:
            asks = _interactions(job, root) if job else ""
            proc = _section("🙋 Interactions", asks) if asks else _section("🙋 Nothing waits on you", "<span hidden></span>")
            views["work-" + key] = (name, lambda tasks=tasks, name=name, proc=proc: CSS + VERSION_CSS + GROUP_CSS
                                    + _band(PROCESS, _numbered(proc))
                                    + _band(RESULTS, _numbered(_section(("🔢 " if name == "Values" else "📚 ") + name,
                                                                         "".join(evidence_item(x, root) for x in tasks)))) + JS)
    return linked_views(views, page_linker(version, root))   # every bNN.jNN.tNN.rNN a link (address_links, JL 261103)


VERSION_CSS = """<style>.fd-steps{display:flex;gap:6px;flex-wrap:wrap}.fd-step{font-size:12px;border:1px solid var(--line);
border-radius:6px;padding:1px 8px;text-decoration:none;color:var(--ink)}.fd-step b{font-weight:500;color:var(--muted)}
.fd-step.fd-you{border-color:#ffa94d}.fd-step.fd-you b{color:#b35c00}.fd-step.fd-ok b{color:#2b8a3e}
.fd-step:hover{border-color:var(--accent)}</style>"""
