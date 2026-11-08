"""A paper Board's evidence and submission Tasks on their own pages (stage-2 review round 2, 261106): a display, a value
group, a claim group, the portal walk and fill, the submission's letter. Each fell back to the frame's old shape, a
Findings that said "No takeaways" and a Work that was the old Progress list, while what the Task made sat two clicks
deep in a Run pop-out. Now:

    Report   MindMap · Findings · Status       its own map and Status (r03); Findings' section 1 is what it made, as
                                               side tabs (the display, its
                                               table and how it was made; each value; each key; each portal step)
    Work     Findings · Status                 the same views, ⚙️ Process (how it is made, its Runs) then 📊 Results

focus_page.render asks `views` through one hook line per section; any other Task keeps the base views. Read-only."""
from __future__ import annotations

import re
import traceback
from pathlib import Path
from urllib.parse import quote, urlencode

from live import draft_steps as ds
from live.frame import esc
from live.ui_parts import (GROUP_CSS, PB_CSS, PB_JS, PROCESS, RESULTS, _band, _numbered, _section, _side_tabs, prompt_box,
                           todo_section)
from live.focus_draft import CSS, JS


def kind_of(task: Path) -> str:
    """What this evidence or submission Task makes: display, values, tables, citations, portal-walk, portal-fill,
    letter; '' for a Section (a draft Task) or any other Task."""
    from live.paper_jobs import job_kind
    from live import evidence_read as er
    job = job_kind(task.parent)
    if not job:
        return ""
    if job == "display":
        return "display"
    if job == "value":
        return "values" if er.newest(task, "values.yaml") else "tables" if er.newest(task, "tables.json") else "values"
    if job == "citation":
        return "citations"
    if er.newest(task, "portal-fields.yaml") is not None or "walk" in task.name:
        return "portal-walk"
    if "fill" in task.name:
        return "portal-fill"
    if "letter" in task.name:
        return "letter"
    return ""


def _face(task: Path) -> str:
    f = task / f"{task.name}.md"
    return f.read_text(encoding="utf-8", errors="ignore") if f.is_file() else ""


def _field(text: str, key: str) -> str:
    m = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    return m.group(1) if m else ""


def _url(f: Path, root: Path) -> str:
    return "/" + quote(ds._rel(f, root))


def _run_url(run: Path, root: Path) -> str:
    from live import frame
    return frame.ROUTE + "?" + urlencode({"view": "focus-part", "part": "run", "path": frame.rel(run, root)})


def _runs(task: Path) -> list:
    return sorted(d for d in (task / "runs").glob("r[0-9]*") if d.is_dir()) if (task / "runs").is_dir() else []


def _run_state(run: Path) -> tuple:
    """(pill, what it says) of one Run: its receipt's status, else its card's; a starter with no receipt is 'not run'."""
    text = "".join(f.read_text(encoding="utf-8", errors="ignore") for f in (run / "result" / "runtime.yaml", run / "run.yaml")
                   if f.is_file())
    st = (re.search(r"(?m)^status:\s*(\S+)", text) or [None, ""])[1].lower()
    says = (re.search(r"(?m)^says:\s*['\"]?(.+?)['\"]?\s*$", text) or [None, ""])[1]
    pill = ("done" if st in ("done", "complete", "completed", "ok", "succeeded") else "running" if st in ("running", "queued")
            else "waiting for you" if st == "waiting" else st if st.startswith("starter") else "not run")
    if pill == "not run" and re.search(r"not opened|starter", str((portal_starter(run) or ""))):
        pill = "starter, not walked"             # one word for the walk's starter fields, page and Status alike (r02)
    return pill, says


def portal_starter(run: Path) -> str:
    """A portal walk Run's `draft_saved:` ("not opened yet: a starter, not a walk"), '' for any other Run."""
    f = run / "result" / "portal-fields.yaml"
    m = re.search(r"(?m)^draft_saved:\s*['\"]?(.+?)['\"]?\s*$", f.read_text(encoding="utf-8", errors="ignore")) if f.is_file() else None
    return m.group(1) if m else ""


# ── what each kind made: (title, body, word, waiting line) ────────────────────────────────────────────────────
def _display(task: Path, root: Path) -> tuple:
    """A display: the display as the paper prints it (preview.pdf), its table as a table, and how it was made, one side
    tab each; its open proposals wait under the bar."""
    from live.board_evidence import display_pick, latex_table_html
    from live import evidence_read as er
    text = _face(task)
    preview, _ = display_pick(task, text)
    items, panels = [], []
    if preview is not None:
        items.append(("The display", f"{preview.parent.parent.name} · as the paper prints it"))
        panels.append(f'<div class=pb-verbs><a class=fd-btn data-pop="{esc(task.name)} · preview" href="{esc(_url(preview, root))}">'
                      f'⤢ Pop out</a></div><iframe class=pb-pdf src="{esc(_url(preview, root))}#view=FitH" loading=lazy '
                      f'title="{esc(task.name)}" style="width:100%;height:max(620px,80vh);border:1px solid var(--line);border-radius:6px"></iframe>')
    body = er.newest(task, "table-body.tex")
    if body is not None:
        items.append(("The table", "its rows, from table-body.tex"))
        panels.append(latex_table_html(body.read_text(encoding="utf-8", errors="ignore")))
    method = er.newest(task, "method.md")
    if method is not None:
        items.append(("How it was made", "method.md"))
        panels.append(f'<pre class=pb-pt style="white-space:pre-wrap">{esc(method.read_text(encoding="utf-8", errors="ignore"))}</pre>')
    if not items:
        return "🖼️ The display", '<p class=mut>Not drawn yet: its draw Run writes preview.pdf.</p>', "not drawn yet", ""
    # the caption is the page's Aim line (its face's goal:), so no line here repeats it (r02); the bindings the value
    # search proposed are a tab of their own, each value, its cell and its Run, waiting for a person's tick
    props = proposals(task)
    if props:
        f = task / "evidence" / "proposals.md"
        items.insert(1, ("Waiting for your tick", f"{len(props)} proposed values"))
        panels.insert(1, "".join(f'<div class=fd-row><span class=n>{esc(what or vid)}</span><span class=d>{esc(value)} in '
                                 f'{esc(cell)} · from {esc(src)}</span><span class="w fd-you">waits for your tick</span></div>'
                                 for vid, value, cell, what, src in props)
                      + f'<p style="margin-top:10px"><a class=fd-btn data-pop="proposals.md" href="{esc(_url(f, root))}">'
                        'Open evidence/proposals.md</a></p>')
    waits = (f"🙋 {len(props)} proposed value{'s' * (len(props) != 1)} wait{'s' * (len(props) == 1)} for your tick, in the tab "
             "Waiting for your tick" if props else "")
    status = _field(text, "status")
    word = "drawn" if preview is not None and "not" not in status.lower() else (status or "drawn")
    return "🖼️ The display", _side_tabs(f"pt{task.name[:3]}", items, panels), word, waits


def proposals(task: Path) -> list:
    """[(value id, value, cell, what it is, its Run)] of the open `bind VALUE` lines in a Task's evidence/proposals.md."""
    f = task / "evidence" / "proposals.md"
    if not f.is_file():
        return []
    out = []
    for m in re.finditer(r'(?m)^- \[ \] bind VALUE (\S+) \(([^)]*)\) to \S+ (.+?) "[^"]*"(.*)$', f.read_text(encoding="utf-8", errors="ignore")):
        rest = m.group(4)
        what = (re.search(r"for: (.+?)(?: · |\s*<!--|$)", rest) or [None, ""])[1]
        src = (re.search(r"from (\S+)", rest) or [None, ""])[1]
        out.append((m.group(1), m.group(2), m.group(3), what, src))
    return out


def _values(task: Path, root: Path) -> tuple:
    from live import evidence_read as er
    data = er.value_data(task)
    if not data.get("rows"):
        return "🔢 Its values", '<p class=mut>No values yet: its value Run writes values.yaml.</p>', "nothing yet", ""
    word, waits = er.value_state(data)
    page = er.newest(task, "values.html")
    pop = (f'<div class=pb-verbs><a class=fd-btn data-pop="{esc(task.name)} · values" href="{esc(_url(page, root))}">'
           f'⤢ Open {esc(page.parent.parent.name)}{chr(39)}s table</a></div>') if page else ""
    return ("🔢 Its values", f'<p class=ev-line>{esc(er.value_line(data))}</p>' + pop
            + er.value_tabs_per_value(data, f"pv{task.name[:3]}"), word, waits)


def _tables(task: Path, root: Path) -> tuple:
    from live.board_evidence import VALUES_CSS, VALUES_DIALOG, VALUES_JS, value_tabs, values_word
    tabs = value_tabs(task.parent, root)
    if not tabs:
        return "🔢 The raw tables", '<p class=mut>No tables yet: its build Run writes tables.json.</p>', "nothing yet", ""
    return ("🔢 The raw tables", VALUES_CSS + _side_tabs("ptT", [(h, w) for h, w, _ in tabs], [p for _, _, p in tabs])
            + VALUES_DIALOG + VALUES_JS, values_word(task.parent, root), "")


def _citations(task: Path, root: Path) -> tuple:
    from live import evidence_read as er
    rows = er.cite_rows(task)
    if not rows:
        return "📚 Its citations", '<p class=mut>Not checked yet: its check Run writes citations.csv.</p>', "nothing yet", ""
    word, waits = er.cite_state(rows)
    page = er.newest(task, "citations.html")
    pop = (f'<div class=pb-verbs><a class=fd-btn data-pop="{esc(task.name)} · citations" href="{esc(_url(page, root))}">'
           f'⤢ Open {esc(page.parent.parent.name)}{chr(39)}s table</a></div>') if page else ""
    return "📚 Its citations", f'<p class=ev-line>{esc(er.cite_line(rows))}</p>' + pop + er.cite_key_tabs(rows, f"pc{task.name[:3]}"), word, waits


def _portal_walk(task: Path, root: Path) -> tuple:
    from live import evidence_read as er
    data = er.portal_fields(task)
    if not data.get("steps"):
        return "📮 The portal's fields", '<p class=mut>Not walked yet: the walk writes portal-fields.yaml.</p>', "not walked", ""
    starter = re.search(r"not opened|starter", str(data.get("draft_saved", "")), re.I)
    word = "starter, not walked" if starter else "walked"
    waits = "🙋 A person starts this walk: log in to the portal and open this send's draft" if starter else ""
    lead = f'<p class=pb-state>{esc(str(data.get("portal", "")))}' + (f' · {esc(str(data.get("draft_saved", "")))}' if data.get("draft_saved") else "") + '</p>'
    return "📮 The portal's fields", lead + er.portal_tabs(data, f"pp{task.name[:3]}"), word, waits


def _portal_fill(task: Path, root: Path) -> tuple:
    fill = task.parent.parent / "delivery" / task.parent.name / "portal-fill.html"
    if not fill.is_file():
        return "📮 The fill page", '<p class=mut>Not built yet: its fill Run writes the fill page.</p>', "not built yet", ""
    u = _url(fill, root)
    return ("📮 The fill page", f'<div class=pb-verbs><a class=fd-btn data-pop="{esc(fill.name)}" href="{esc(u)}">⤢ Pop out</a></div>'
            f'<iframe src="{esc(u)}" loading=lazy title="The portal fill page" style="width:100%;height:max(620px,80vh);'
            'border:1px solid var(--line);border-radius:6px;background:#fff"></iframe>', "built",
            "🙋 Check every field on the fill page, then press Submit in the portal yourself")


def _letter(task: Path, root: Path) -> tuple:
    from live.focus_draft import content_read
    from live.board_read import _task_url
    ref = _field(_face(task), "words-in")
    words = (task / ref).resolve() if ref else None
    if words is None or not words.is_dir():
        return "✉️ The letter", '<p class=mut>No letter Section named yet (`words-in:`).</p>', "nothing yet", ""
    return ("✉️ The letter", f'<div class=pb-verbs><a class=fd-btn href="{esc(_task_url(words, root))}">Open the Section '
            f'{esc(words.parent.name)} · {esc(words.name)}</a></div>' + (content_read(words, root) or '<p class=mut>No text yet.</p>'),
            "written" if content_read(words) else "nothing yet", "")


MADE = {"display": _display, "values": _values, "tables": _tables, "citations": _citations, "portal-walk": _portal_walk,
        "portal-fill": _portal_fill, "letter": _letter}


FACTS = (("label", "Label"), ("number", "Number"), ("type", "Type"), ("caption", "Caption"), ("answers", "Answers"),
         ("cited-in", "Cited in"), ("close", "Done when"), ("reads", "Reads"), ("state", "State"))


def _facts(task: Path) -> str:
    """Its face's facts, none the Aim line already shows (r02: the Goal row repeated the Aim)."""
    text = _face(task)
    aim = _field(text, "goal")
    rows = [(name, _field(text, key)) for key, name in FACTS if _field(text, key) and _field(text, key) not in aim]
    return "".join(f'<div class=fd-row><span class=n>{esc(k)}</span><span class=d>{esc(v)}</span></div>' for k, v in rows)


def findings(task: Path, root: Path, kind: str) -> str:
    """Findings: 1 · what it made (side tabs), 2 · its facts from its face."""
    from live.evidence_read import VALUE_CSS
    title, body, word, waits = MADE[kind](task, root)
    facts = _facts(task)
    return VALUE_CSS + _section(title, body, word, waits) + (_section("📋 Its facts", facts, f"{facts.count('fd-row')} fact{'s' * (facts.count('fd-row') != 1)}") if facts else "")


def _process(task: Path, root: Path, kind: str, view: str) -> str:
    """Work's ⚙️ Process: its Runs as to-do rows (Status), or how it is made, a Copy prompt to make it again (Findings)."""
    runs = _runs(task)
    if view == "standing":
        rows = [(r.name, says, pill, "Open", _run_url(r, root), True) for r in runs for pill, says in [_run_state(r)]]
        return todo_section("🏃 Its Runs", rows) if rows else ""
    last = runs[-1] if runs else None
    ticket = next((f for f in (last / f"{last.name}.sh", last / f"{last.name}.md") if f.is_file()), None) if last else None
    if last is None:
        return ""
    rel = ds._rel(task, root)
    how = (f"Use /haipipe-run. Rerun the ticket {rel}/runs/{last.name}/{ticket.name} and read its result/ back into "
           f"{task.name}; change nothing by hand." if ticket is not None and ticket.suffix == ".sh" else
           f"Use /haipipe-run. Read {rel}/runs/{last.name}/{ticket.name if ticket else 'run.yaml'} and tell me what a person "
           "must do to start it; start nothing yourself.")
    pill, says = _run_state(last)
    box = prompt_box(how, (), step=last.name, asks=says or "make it again", key=f"{rel}#make")
    return _section("🧭 How it is made", box, pill)


def headline(task: Path, root: Path, kind: str) -> str:
    """What its newest Run returned, in the words its Findings use (r02: Status's bar 1 was the Run's coded headline,
    "0 card-only, 2 bib-only, 1 missing-bib, 0 TOADD")."""
    from live import evidence_read as er
    if kind == "citations" and er.cite_rows(task):
        rows = er.cite_rows(task)
        return f"{er.cite_state(rows)[0]} · {er.cite_line(rows)}"
    if kind == "values" and er.value_data(task).get("rows"):
        return er.value_line(er.value_data(task))
    if kind == "portal-walk":
        data = er.portal_fields(task)
        n = sum(len(s_.get("fields") or []) for s_ in data.get("steps") or [])
        return (f"{n} fields the portal asks, a starter: a person logs in and opens this send's draft to walk it"
                if re.search(r"not opened|starter", str(data.get("draft_saved", ""))) else f"{n} fields the portal asks, walked")
    runs = _runs(task)
    head = next((h.read_text(encoding="utf-8", errors="ignore").strip().split("\n")[0]
                 for h in [r / "result" / "headline.txt" for r in reversed(runs)] if h.is_file()), "")
    if not head and kind == "display" and runs:  # a draw Run writes no headline: what it drew, and when
        text = _face(task)
        rt = runs[-1] / "result" / "runtime.yaml"
        when = (re.search(r"(?m)^finished_at:\s*['\"]?(\d{4}-\d{2}-\d{2})", rt.read_text(encoding="utf-8", errors="ignore"))
                or [None, ""])[1] if rt.is_file() else ""
        what = _field(text, "number") or _field(text, "label") or "the display"
        return f"{what} drawn" + (f" {when}" if when else "") + f" by {runs[-1].name}" if (runs[-1] / "result").is_dir() else ""
    return re.sub(r"^t\d+_[\w-]+:\s*", "", head)


def status(task: Path, root: Path, kind: str, work: bool) -> str:
    """Its Status (r02): 📌 Headline, what its newest Run returned in Findings' words and its files; then (Report only)
    🧪 Runs, each Run's state and what it does. Work's Process lists the Runs as to-do rows, so its Results do not."""
    from live.ui_parts import _file_link
    from live.evidence_read import VALUE_CSS
    runs = _runs(task)
    _, _, word, _ = MADE[kind](task, root)
    last = next((r for r in reversed(runs) if (r / "result").is_dir()), runs[-1] if runs else None)
    files = ""
    if last is not None:
        shown = sorted(f for f in (last / "result").glob("*") if f.is_file() and not f.name.startswith(".")
                       and f.suffix in (".txt", ".csv", ".html", ".yaml", ".md", ".pdf", ".json")) if (last / "result").is_dir() else []
        files = (f'<p class=pb-state><a class=fd-btn data-pop="{esc(task.name)} · {esc(last.name)}" href="{esc(_run_url(last, root))}">'
                 f'Open {esc(last.name)} ↗</a> ' + " · ".join(_file_link(f, root) for f in shown) + '</p>')
    said = headline(task, root, kind)
    out = VALUE_CSS + _section("📌 Headline", (f'<p class=ev-line>{esc(said)}</p>' if said else '<p class=mut>No Run has returned anything yet.</p>')
                   + files, word)
    if not work and runs:
        states = [_run_state(r) for r in runs]
        done = sum(pill == "done" for pill, _ in states)
        rows = "".join(f'<div class=fd-row><span class=n>{esc(r.name)}</span><span class=d>{esc(says)}</span>'
                       f'<span class="w {"fd-ok" if pill == "done" else "fd-you" if "you" in pill or "starter" in pill else ""}">'
                       f'{esc(pill)}</span></div>' for r, (pill, says) in zip(runs, states))
        out += _section("🧪 Runs", rows, f"{done} of {len(runs)} done" if done or len(runs) > 1 else states[0][0])
    return out


def task_mindmap(task: Path, root: Path, kind: str) -> str:
    """Its map (r02: a root and one closed box; an unlabeled dot on "Runs"): what it made, by its state, with what it
    must find out; then its Runs, each with what it does and its state."""
    try:
        from live import frame
        from live.paper_version import paper_map
        frame.mindmap_module()
        import mmbuild
        text = _face(task)
        title, _, word, _ = MADE[kind](task, root)
        made = [mmbuild.built(f"{task.name}/made/{k}", f"[{k}] {v}") for k, v in
                (("finds out", _field(text, "goal") or _field(text, "answers")), ("returned", headline(task, root, kind)))
                if v]
        kids = [mmbuild.built(f"{task.name}/made", f"{re.sub(r'^[^A-Za-z]+', '', title)} · {word}", made)]
        runs = [(r, *_run_state(r)) for r in _runs(task)]
        if runs:
            done = sum(pill == "done" for _, pill, _ in runs)
            kids.append(mmbuild.built(f"{task.name}/runs", f"Runs · {done} of {len(runs)} done",
                                      [mmbuild.built(f"{task.name}/runs/{r.name}", f"[{pill}] {r.name}: {says or 'no says: line'}")
                                       for r, pill, says in runs]))
        return paper_map(task.name, kids, key=task.name)
    except Exception:                            # a map that does not draw never takes the page down
        traceback.print_exc()
        return '<p class=mut>The map does not draw yet.</p>'


def views(task: Path, root: Path, section: str, base: dict) -> dict:
    """The Task's Report (`section` "report") or Work ("work") views, {} -> `base` for any Task this does not draw. Base
    keys kept: MindMap and Status come from the frame; Findings is this module's."""
    try:
        kind = kind_of(task)
        if not kind or not base:
            return base
        page = lambda body: CSS + GROUP_CSS + PB_CSS + body + PB_JS + JS
        if section == "report":                  # its map, what it made, then what its Runs returned (r02: its own)
            return {"mindmap": ("MindMap", lambda: page(task_mindmap(task, root, kind))),
                    "findings": ("Findings", lambda: page(_numbered(findings(task, root, kind)))),
                    "standing": ("Status", lambda: page(_numbered(status(task, root, kind, False))))}

        def work(view):
            def build():
                if view == "findings":
                    res = findings(task, root, kind)
                else:                            # its Runs are Process's to-do rows; Results says what they returned
                    res = status(task, root, kind, True)
                return page(_band(PROCESS, _numbered(_process(task, root, kind, view))) + _band(RESULTS, _numbered(res)))
            return build
        return {"work-findings": ("Findings", work("findings")), "work-standing": ("Status", work("standing"))}
    except Exception:                            # a Task page that does not draw keeps the base page
        traceback.print_exc()
        return base
