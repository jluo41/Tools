"""A paper Board's evidence and display sections: the evidence kinds' numbered sections, the Display side tabs in
groups (Main, Supplement), each tab's place and type line (_grouped_tabs, DISPLAY_CSS)."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import esc
from live.ui_parts import _bar, _cap, _open_btn, _side_tabs, _when
from live.board_read import display_plan, _field, _num, _task_url, _version_url, is_version
from live.board_evidence import EVIDENCE_KINDS, VALUES_CSS, VALUES_DIALOG, VALUES_JS, empty_job, evidence_body, evidence_word, value_tabs, values_word


def _check_href(job: Path, root: Path, kind: str) -> str:
    """The evidence Job's Check view, where the whole-paper check is read in full."""
    return _version_url(job, root, "report") + "&group=" + ("value-check" if kind == "Values" else "cite-check")


def _evidence_kinds(board: Path, root: Path, kinds: tuple, n: int = 0, only: tuple | None = None,
                    check: bool = True, since=None) -> tuple[str, int]:
    """The numbered sections of these evidence kinds (Values, Citations, Displays), in that order, each a side tab per
    Task; the displays also as one PDF (`delivery/<job>/<job>-all-displays.pdf`). The Board's Evidence, a version's
    Values, Citations and Display views and the evidence Jobs draw these same sections, so their words agree (261106,
    review round 2). A Job's whole-paper check (t99) is never a tab: it shows once, a verdict line above the tabs
    (`check`; off in the Check view itself). Its state word comes from that check, each citation key counted once;
    what differs or is missing waits under the closed bar. `only`: only these display groups (main, supplement,
    unplanned), as a version's Display-Main and Display-Appendix. `since(task or None, tab name)`: a revision's word for
    a tab, what this send did to it ("same as j11_…", "new in this send", "asked by Reviewer 2"), or None."""
    from live import evidence_read as er
    since = since or (lambda task, head: None)
    jobs = [d for d in sorted(board.glob("j[0-9]*_*")) if d.is_dir() and not is_version(d)]
    out = ""
    for kind, pat in sorted((k for k in EVIDENCE_KINDS if k[0] in kinds), key=lambda k: ("Values", "Citations", "Displays").index(k[0])):
        job = next((j for j in jobs if re.search(pat, j.name, re.I)), None)
        if job is None:
            continue
        top = er.verdict(job, root, kind, _check_href(job, root, kind)) if check and kind != "Displays" else ""
        vtabs = value_tabs(job, root) if kind == "Values" else None
        if vtabs:                                # side tabs, each a readable topic with its raw table (JL 261104)
            n += 1
            # no check tally on the bar (AGENTS § Page words): each printed number and raw table shows its own state
            word, waits = er.value_state(er.job_values(job))
            out += _bar(n, kind, f'<div class=pb-verbs>{_open_btn(f"Open {job.name}", _task_url(job, root))}</div>' + top + VALUES_CSS
                        + _side_tabs("evV", [(h, since(None, h) or w) for h, w, _ in vtabs], [p for _, _, p in vtabs]) + VALUES_DIALOG + VALUES_JS,
                        word, waits)
            continue
        tasks = sorted((x for x in job.glob("t[0-9]*_*") if x.is_dir() and not er.is_check(x)
                        and not (kind == "Displays" and retired(x))), key=_num)
        tiles, panels = [], []
        dp = display_plan() if kind == "Displays" else None
        paper_as = {r.get("display", ""): dp.title(r) for r in (dp.rows(board) if dp else [])}
        plan_of = {r.get("display", ""): r for r in (dp.rows(board) if dp else [])}
        groups = []                              # (group, plan order) per tile, for the Displays' Main / Appendix lists
        statuses = []                            # each Task's status, for the section's state word
        for t in tasks:                          # each item to read: its list on the left, the thing itself on the right
            label, status, body = evidence_body(t, root)
            if kind == "Citations" and er.cite_rows(t):   # its claim, then one line per key; the cards are the Check
                body = er.cite_lines(t, root)               # view's (r02: the same three cards in both views)
                status = er.cite_state(er.cite_rows(t))[0]
            if kind == "Values" and er.value_data(t).get("rows"):   # each printed number drawn, no framed page
                data = er.value_data(t)
                body = er.value_check_html(data, t, root) + f'<p><a class=fd-btn href="{esc(_task_url(t, root))}">Open {esc(t.name)} ↗</a></p>'
                status = er.value_state(data)[0]
            statuses.append(status)
            words = re.sub(r"^t\d+_", "", t.name).replace("-", " ")
            words = re.sub(r"^(?:e?figure|e?table|values|cite)\d*\s*", "", words, flags=re.I)
            head = label if label and label.lower() not in ("values", "citations") else _cap(words)
            line = words if head == label else re.sub(r"^\d+\s+", "", status or "")
            line = "waiting" if line.startswith("waits") else line
            if kind in ("Citations", "Values") and (er.cite_rows(t) or er.value_data(t).get("rows")):
                line = status                    # no tally: each key or number shows its own state in the panel
            if kind == "Displays":               # JL 261101: "for each display, we might also want to have the name and type"
                group, order, head, line = _display_head(t, label, head, words, dp, paper_as, plan_of)
                groups.append((group, order))
            emo = _face_emoji(t)                 # the Task face's `emoji:` marks its tab (JL 261110)
            head = f"{emo} {head}" if emo and not head.startswith(emo) else head
            tiles.append((head, since(t, head) or line or status, ""))
            panels.append(body)
        if kind == "Displays" and only is not None:   # a version's Display-Main or Display-Appendix: those groups only
            keep = [k for k, (g, _) in enumerate(groups) if g in only]
            tiles, panels, groups, statuses = ([x[k] for k in keep] for x in (tiles, panels, groups, statuses))
            if not tiles:
                continue
        book = board / "delivery" / job.name / f"{job.name}-all-displays.pdf"   # build_displays_pdf.py writes it
        whole = (_open_btn("Open all displays as one PDF", "/" + quote(ds._rel(book, root)), book.name)
                 + f'<span class=pb-state>built {_when(book)}</span>') if kind == "Displays" and book.is_file() else ""
        n += 1
        if kind == "Displays" and tiles:         # grouped, Main then Appendix (JL 261101: "groups them in different groups,
            tabs = _display_groups("evD", groups, tiles, panels, list(paper_as.values()))   # like the main"), each card thinner
        else:
            tabs = _side_tabs("ev" + kind[0], [(h, w) for h, w, _ in tiles], panels) if tiles else empty_job(job)
        keys = er.job_cites(job) if kind == "Citations" else []
        checked = er.job_values(job) if kind == "Values" else {}
        if keys:                                 # each key once, from the whole-paper check (a key in two groups, or in
            word, waits = er.cite_state(keys)    # a group and the check, was counted twice: "0 of 6")
        elif checked.get("rows"):                # the Values word is the check's: what differs waits under the bar
            word, waits = er.value_state(checked)
        else:
            word, waits = evidence_word(kind, statuses), ""
        out += _bar(n, kind, f'<div class=pb-verbs>{whole}{_open_btn(f"Open {job.name}", _task_url(job, root))}</div>' + top + tabs,
                    word, waits)
    return out, n


def _display_head(t: Path, label: str, head: str, words: str, dp=None, paper_as=None, plan_of=None) -> tuple:
    """(group, order, tab name, tab line) of one display Task: where it goes, and its tab's two lines (name; type · name)."""
    group, order, head = _display_place(t, label, head, dp, paper_as or {}, plan_of or {})
    face = t / f"{t.name}.md"
    ks = dp.keys(face.read_text(encoding="utf-8", errors="ignore")) if dp and face.is_file() else []
    row = next(((plan_of or {})[k] for k in ks if k in (plan_of or {})), None)
    return group, order, head, _display_line(t, words, (row or {}).get("name", ""))


def retired(task: Path) -> bool:
    """A display Task the paper no longer prints: its face says `number: not printed` (or `retired`). Its folder and
    passes stay on disk; the Displays lists leave it out (Pp-AgreeableRx 261121: an old Table D4 under Others, JL "what
    is this??? is this the new one?? I am confused")."""
    face = task / f"{task.name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore")[:3000] if face.is_file() else ""
    return bool(re.search(r"(?mi)^(?:number|status):\s*(?:not printed|retired)\b", text))


GROUP_ORDER = ("main", "supplement", "si", "method", "unplanned")


def _display_groups(eid: str, groups: list, tiles: list, panels: list, planned=(), names=None) -> str:
    """The display tabs in their groups, Main, Appendix, Method, Others (JL 261102: candidates not in the plan, "a new
    section here as Others"), each by its plan order; `names` renames a group (a work Block has no Main text)."""
    sup = _supplement_word(list(planned) + [h for h, _w, _x in tiles])
    name = {"main": "Main", "supplement": sup, "si": "Supplementary Information", "method": "Method", "unplanned": "Others",
            **(names or {})}   # si: a Nature journal's SI tables apart from its Extended Data (JL 261122)
    keyed = sorted(zip(groups, tiles, panels), key=lambda x: (GROUP_ORDER.index(x[0][0]), x[0][1]))
    return _grouped_tabs(eid, [(name[g], (h, w), b) for (g, _), (h, w, _), b in keyed])


def display_tabs(tasks: list, root: Path, eid: str = "evD", names: dict | None = None) -> tuple[str, str]:
    """(html, state word) of these display Task folders drawn exactly as a paper's Displays view draws them, for any
    page that lists displays (the work Block's Findings, JL 261109: "consistent with the paper theme's displays"). One
    side tab per Task: its `label:` (else its folder words) over its type and `name:`; its panel the shown version
    (display_pick: the face's `printed:` Run, else the newest preview.pdf; else the newest picture), its facts and its
    Open button. Grouped by the face's `group:` (method, others) or its label (Figure, Extended Data, eTable) or its
    number (t50 on: Appendix); `names` renames a group, e.g. {"main": "Results", "method": "Methods"}. No display
    plan is read: a paper Board's plan places its displays in _evidence_kinds. workbench focus_page.display_sections
    calls it: keep this signature and the ("", "") empty return, or tell the work side."""
    groups, tiles, panels, statuses = [], [], [], []
    for t in (t for t in tasks if not retired(t)):
        label, status, body = evidence_body(t, root)
        words = re.sub(r"^t\d+_", "", t.name).replace("-", " ").replace("_", " ")
        words = re.sub(r"^(?:e?figure|e?table|values|cite)\d*\s*", "", words, flags=re.I)
        group, order, head, line = _display_head(t, label, label or _cap(words), words)
        groups.append((group, order))
        tiles.append((head, line or status, ""))
        panels.append(body)
        statuses.append(status)
    if not tiles:
        return "", ""
    return _display_groups(eid, groups, tiles, panels, names=names), evidence_word("Displays", statuses)


def _display_place(t: Path, label: str, head: str, dp, paper_as: dict, plan_of: dict) -> tuple:
    """(group, order, head) of one display Task: where it goes (main, supplement, method, unplanned), its place in the plan, and
    what the paper calls it (Figure 1 (Display A)), from the display plan, by any key its face answers to."""
    face = t / f"{t.name}.md"
    ks = dp.keys(face.read_text(encoding="utf-8", errors="ignore")) if dp and face.is_file() else []
    head = next((paper_as[k] for k in ks if k in paper_as), head)
    r = next((plan_of[k] for k in ks if k in plan_of), None)
    order = list(plan_of).index(r.get("display", "")) if r is not None else 999
    fgroup = _field(face.read_text(encoding="utf-8", errors="ignore"), "group").lower() if face.is_file() else ""
    if fgroup in ("method", "methods"):
        group = "method"             # a display that explains how the study is done, for a reader such as an
                                     # advisor (JL 261106: "we might have a section named Method")
    elif fgroup == "others":
        group = "unplanned"          # a draft shown apart until it is placed (JL 261104: "先放到 other 里面去")
    elif r is not None:              # the plan says where it goes
        group = r["where"]
    elif plan_of:                    # a plan that does not name it
        group = "unplanned"
    else:                            # no plan: the face's label says where it goes and its number (JL 261103:
        lab = re.match(r"(Extended Data |Supplementary )?(Figure|Table) (\d+)", label or "")   # "I didn't see
        if lab:                      # the fairness figure": label "Extended Data Figure 1" on t53 sat under Main's
            group = "supplement" if lab.group(1) else "main"   # t07 and Figure 4 (t06) after Figure 5 (t04))
            order = (lab.group(2) == "Table") * 100 + int(lab.group(3))
        else:                        # t51 and on, or an eTable / Appendix label, is outside the main text
            group = "supplement" if _num(t) >= 50 or re.match(r"(?i)(e(?=fig|tab)|appendix|supp)", label or "") else "main"
    return group, order, head


def display_groups(board: Path, tasks: list) -> dict:
    """{display Task: its group}, as the Displays tabs place it (a version's Display-Main and its Process list the same
    displays)."""
    dp = display_plan()
    rows = dp.rows(board) if dp else []
    paper_as = {r.get("display", ""): dp.title(r) for r in rows}
    plan_of = {r.get("display", ""): r for r in rows}
    out = {}
    for t in (t for t in tasks if not retired(t)):
        face = t / f"{t.name}.md"
        label = _field(face.read_text(encoding="utf-8", errors="ignore"), "label") if face.is_file() else ""
        out[t] = _display_place(t, label, label, dp, paper_as, plan_of)[0]
    return out


def _supplement_word(labels: list) -> str:
    """What the venue calls the displays outside the main text: Extended Data (Nature journals), Supplement (eFigure,
    Supplementary Table), else Appendix."""
    if any(x.startswith("Extended Data") for x in labels):
        return "Extended Data"
    return "Supplement" if any(re.match(r"(?:e(?:Figure|Table)|Supplementary)", x) for x in labels) else "Appendix"


def _grouped_tabs(eid: str, items: list) -> str:
    """Side tabs in groups (Main, Appendix): the shared side-tab markup (ui_parts._side_tabs, so its clicks work), a
    small group name above each group's cards, each card thinner (this theme's own style, DISPLAY_CSS)."""
    rows, panels, last = "", "", None
    for k, (group, (h, w), body) in enumerate(items):
        if group != last:
            rows += f'<div class=pb-lgroup>{esc(group)}</div>'
            last = group
        rows += (f'<button type=button class="pb-item{" on" if k == 0 else ""}" data-pbtab="{eid}{k}"><b>{esc(h)}</b>'
                 f'<span title="{esc(w)}">{esc(w)}</span></button>')
        panels += f'<div class=pb-panel data-pbpanel="{eid}{k}"{"" if k == 0 else " hidden"}>{body}</div>'
    return (DISPLAY_CSS + f'<div class="pb-tabset pb-side pb-thin"><div class=pb-list>{rows}</div>'
            f'<div class=pb-read>{panels}</div></div>')


# the Displays' side lists: thinner cards, a group name above each group (this theme's own look; ui_parts stays shared)
DISPLAY_CSS = ("<style>.pb-thin .pb-item{padding:3px 9px;margin:0 0 1px}.pb-thin .pb-item b{font-size:13px;line-height:1.3}"
               ".pb-thin .pb-item span{font-size:11.5px;line-height:1.3}"
               ".pb-lgroup{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);"
               "margin:10px 0 3px 2px}.pb-lgroup:first-child{margin-top:0}"
               "@media(max-width:600px){.pb-lgroup{flex-basis:100%;margin:6px 0 2px}}</style>")


DISPLAY_TYPES = (("figure", "📈 Figure"), ("table", "📊 Table"))


def _display_line(task: Path, slug: str, plan_name: str = "") -> str:
    """A Display tab's second line: its type, then its name. The name is the face's `name:` line, else the display
    plan's name for it, else the title after "<label>," in its first line, else the folder's words without the number
    they began with (after a renumber the folder keeps its old number: t57_tablec3-icd-codes is Table C4); the type is
    the face's `type:` (or `kind:`) line, else what its newest float.tex begins (a figure or a table environment)."""
    face = task / f"{task.name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    field = lambda k: (re.search(rf"^{k}:\s*(.+?)\s*$", text, re.M) or [None, ""])[1]
    name = field("name") or plan_name
    if not name:
        slug = re.sub(r"^[a-z]?\d+[a-z]?\s+", "", slug, flags=re.I)   # "c3 icd codes": the old number goes
        m = re.match(r"#\s*[^,\n]*?\b(?:Display|e?Figure|e?Table)\s+\w+\s*[,:·]\s*(.+)", text.strip())
        name = m.group(1).strip() if m else _cap(slug)
    kind = (field("type") or field("kind")).lower()
    if not kind:
        floats = sorted([*task.glob("runs/*/result/float.tex"), *task.glob("display/*/float.tex")],
                        key=lambda f: f.stat().st_mtime)
        body = floats[-1].read_text(encoding="utf-8", errors="ignore") if floats else ""
        kind = next((k for k in ("table", "figure") if f"\\begin{{{k}" in body), "")
    word = next((w for k, w in DISPLAY_TYPES if k in kind), kind.capitalize())
    return f"{word} · {name}" if word else name


def _face_emoji(task: Path) -> str:
    """A Task face's `emoji:` line, the mark on its tab; empty when the face has none."""
    face = task / f"{task.name}.md"
    if not face.is_file():
        return ""
    m = re.search(r"(?m)^emoji:\s*(\S+)\s*$", face.read_text(encoding="utf-8", errors="ignore")[:2000])
    return m[1] if m else ""
