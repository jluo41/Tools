"""Audience Report: one row per Question, Logic | Work | Report, and the report view with its group bar."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlencode

from live.frame_base import (ROUTE, Theme, _block_above, _e, _fields, _link, _reader, _rel, _title, _yaml_scalar,
                             children, face, pop, runs_of)
from live.frame_studio import _draw_url, _group_parts, _note_facts, _notes, _split_tags, _studio_topics
from live.frame_groups import group_list


# The Audience Report's views on a level no theme draws itself: the paper Board's four (JL 261009, over its
# Audience Report: "I want you to follow things like this"; b03 s01-D22), each a button, an empty one saying what
# belongs there. A Related Question is one someone else asks: its register group names who.
AUDIENCE_VIEWS = ("Ideation", "Narrative", "High-level logic + Low-level work", "Related Questions")
WHO_ASKS = ("reviewer", "coauthor", "editor", "reader")


# ── Audience Report: one row per Question, Logic │ Work │ Report (b10 s02-D25) ──────────────
def _register_set_groups(md: Path, qid: str, groups: list) -> None:
    """Write a Question's groups into its register row's `group:` line (b10 s05-D05): the line replaced, or
    added after the row's `title:` (else after its `id:`); no groups, no line. Only that line changes; the rest
    of the face stays as written."""
    text = md.read_text(encoding="utf-8")
    m = re.search(r"(?ms)^## Questions[ \t]*\n.*?```ya?ml\n(.*?)```", text)
    if not m:
        raise ValueError(f"{md.name} has no ## Questions register")
    lines = m.group(1).split("\n")
    start = next((i for i, ln in enumerate(lines)
                  if re.match(rf"""^\s*-\s+id:\s*['"]?{re.escape(qid)}['"]?\s*$""", ln)), None)
    if start is None:
        raise ValueError(f"{qid} is not in the register of {md.name}")
    dash = len(lines[start]) - len(lines[start].lstrip())
    indent = lambda ln: len(ln) - len(ln.lstrip())
    end = next((i for i in range(start + 1, len(lines)) if lines[i].strip() and indent(lines[i]) <= dash), len(lines))
    pad = " " * next((indent(lines[i]) for i in range(start + 1, end) if lines[i].strip()), dash + 2)
    value = ", ".join(groups)
    if re.search(r"""[:#\[\]{}&*!|>'"%@`]""", value) or value[:1] in "-?":
        value = json.dumps(value, ensure_ascii=False)
    at = next((i for i in range(start + 1, end) if lines[i].startswith(pad + "group:")), None)
    if at is not None:
        if groups:
            lines[at] = f"{pad}group: {value}"
        else:
            del lines[at]
    elif groups:
        after = next((i for i in range(start + 1, end) if lines[i].startswith(pad + "title:")), start)
        while after + 1 < end and lines[after + 1].strip() and indent(lines[after + 1]) > len(pad):
            after += 1                                    # past a title that wraps
        lines.insert(after + 1, f"{pad}group: {value}")
    md.write_text(text[:m.start(1)] + "\n".join(lines) + text[m.end(1):], encoding="utf-8")


def _register(md: Path | None) -> list:
    """The face's `## Questions` register (a fenced yaml `questions:` list), or []."""
    if not md:
        return []
    text = md.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"(?ms)^## Questions[ \t]*\n.*?```ya?ml\n(.*?)```", text)
    if not m:
        return []
    try:
        import yaml
        rows = (yaml.safe_load(m.group(1)) or {}).get("questions") or []
    except Exception:  # a broken register reads as none; the checker reports it
        return []
    return [r for r in rows if isinstance(r, dict) and r.get("id")]


def _opening(page: Path) -> str:
    """The report's answer line: the first paragraph of its Opening."""
    text = page.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"(?ms)^## Opening[ \t]*\n(.*?)(?=^## |\Z)", text)
    para = (m.group(1).strip().split("\n\n", 1)[0] if m else "")
    para = re.sub(r"<!--.*?-->", "", para, flags=re.S)
    para = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", para)
    return re.sub(r"\s+", " ", para.replace("**", "").replace("`", "")).strip()


def _answer_ids(md: Path | None) -> set:
    """The Question ids a face's `answers:` line names, lowercased; a need `<id>.E<n>` counts as its id."""
    m = re.search(r"(?m)^answers:\s*(.+)$", md.read_text(encoding="utf-8", errors="ignore")) if md else None
    return {re.sub(r"(?i)\.E\d+$", "", w.strip()).lower() for w in re.split(r"[,\s\[\]]+", m.group(1)) if w.strip()} \
        if m else set()


def _answering(folder: Path, level: str, qid: str, root: Path) -> list:
    """The Jobs and Tasks under this level whose face says `answers: <qid>`."""
    found = []
    for kid in children(folder, level) if level in ("Block", "Job") else []:
        for f in [kid] + (children(kid, "Job") if level == "Block" else []):
            md = face(f)
            m = re.search(r"(?m)^answers:\s*(.+)$", md.read_text(encoding="utf-8", errors="ignore")) if md else None
            # hai-report's link rule: `answers: <id>`, or a need of it, `<id>.E<n>`
            if m and qid.lower() in [re.sub(r"(?i)\.E\d+$", "", w.strip()).lower()
                                     for w in re.split(r"[,\s\[\]]+", m.group(1))]:
                found.append(f)
    return found


def _studio_links(page: Path) -> list:
    """(link text, drawing) for each link in a report Page to a drawing under a studio/ folder, in order."""
    out = []
    for name, href in re.findall(r"\[([^\]]+)\]\(([^)\s]+\.excalidraw)\)", page.read_text(encoding="utf-8", errors="ignore")):
        p = (page.parent / href).resolve()
        if "studio" in p.parts and p.is_file():
            out.append((name, p))
    return out


def _report_cell(qid: str, page: Path | None, root: Path, work: str = "") -> str:
    """The Report cell: the title (the Page in the pop-out), its answer line, then the work behind it (`work`, the
    Jobs, Tasks and Runs on this Question; b10 s32-D23, JL 261012: "the logic and report (which contains the work
    as well)"), its one drawing embedded live (view only, fitted to the box, loaded as it scrolls into view; JL
    261009), full size in the pop-out, and a tag."""
    line = f'<p class=q-work><span class=mut>Work:</span> {work}</p>' if work else ""
    if not page:
        return '<p class=mut>No report yet</p>' + line
    tag = page.stem.split("_", 1)[0]
    status = dict(_fields(page)).get("answer-status", "open")
    drawing = page.with_suffix(".excalidraw")
    if drawing.is_file():
        pic = (f'<div class=rp-live title="Click to pan and zoom"><iframe class=rp-draw inert loading=lazy '   # inert: it never
               f'title="{_e(page.stem)}" src="{_e(_draw_url(drawing, root))}" referrerpolicy=no-referrer></iframe></div>'  # takes focus
               f'<p class=rp-full>{pop(_draw_url(drawing, root), qid + " · Drawing · generated, view only", "full size ↗")}</p>')
    elif studio := _studio_links(page):                       # a report that draws nothing links the Studio frames
        pic = ('<p class=rp-full><span class=mut>Studio:</span> '   # that show it (b51, JL 261021: "No more draw in
               + " · ".join(pop(_draw_url(p, root), f"{qid} · Studio · {name}", f"{name} ↗") for name, p in studio)
               + '</p>')                                              # the reports")
    else:
        pic = '<p class=mut>no drawing yet</p>'
    answer = _opening(page)
    return (f'<p class=rp-title>{pop(_reader(page, root), qid + " · Report · the Page", _title(page) + " ↗")}</p>'
            + (f'<p class=rp-text>{_e(answer)}</p>' if answer else '<p class=mut>no answer yet</p>')
            + line + pic + f'<p class=rp-tags>report {_e(tag)} · {_e(status)}</p>')


# two columns (b10 s32-D23, JL 261012): the question │ its report, the work behind it inside the report
Q_HEAD = ('<div class="q-row q-two q-head-row"><div>Logic · the question</div>'
          '<div>Report · what it says, and the work behind it</div></div>')


def question_rows(level: str, folder: Path, root: Path, sub: str = "", keep=None) -> tuple:
    """(html, groups): one row per Question of this level: Logic (the question, its status, the
    studio topics that feed it) │ Work (the Jobs and Tasks that answer it) │ Report."""
    _, groups, recs = _question_records(level, folder, root, keep)
    out = [(q["group"], q["html"]) for q in recs if sub in ("", "All") or q["group"] == sub]
    if not out:
        return '<p class=mut>No Questions at this level yet.</p>', groups
    if groups and sub in ("", "All"):              # All: the table grouped the same way, a heading per group (b10 s02-D25)
        return Q_HEAD + "".join(f'<h3 class=q-group>{_e(g or "other")}</h3>' + "".join(h for k, h in out if k == g)
                                for g in groups + ([""] if any(not k for k, _ in out) else [])), groups
    return Q_HEAD + "".join(h for _, h in out), groups


def _theme_fixed(theme: "Theme | None", row: dict, owner: Path) -> list:
    """A theme's fixed Report groups for one register row: report_fixed(row, owner), the owner being the level
    whose register is read (a paper's come from its telling's **Feeds:**, b16 s05-D01), or report_fixed(row)
    for a rule that needs only the row (insight's level letter)."""
    fn = theme.report_fixed if theme is not None else None
    if not fn:
        return []
    import inspect
    try:
        takes_owner = len(inspect.signature(fn).parameters) >= 2
    except (TypeError, ValueError):
        takes_owner = False
    return [str(g) for g in ((fn(row, owner) if takes_owner else fn(row)) or []) if g]


# every theme's Report starts with this suggested group (b10 s05-D06, named by JL 261012, s05-D22): a question that
# came up outside the plan, from anyone, parked here until it finds its group; Untagged is a row with no group yet
REPORT_SUGGESTED = ("Random thoughts",)


def report_view(level: str, folder: Path, root: Path, theme: "Theme | None" = None, empty: str = "") -> str:
    """The Report as the Studio shows its topics (b10 s05-D05, JL 261011: "if the report card to show, it will
    be the same as the sNN, we can create and add the tags"): one folding card per Question under the group
    bar, Current · groups · Untagged · + Group; opened, its Logic │ Work │ Report row. A Question's groups are
    the theme's fixed ones for it (Theme.report_fixed, no ×) and then its register `group:` line, comma-separated;
    a drag writes that line (_register_set_groups); reports/_groups.txt keeps the order. Every level shows its
    bar, Block, Job and Task (b10 s05-D17, JL 261012: "the report group tags for both the block level, job level
    and task level"), even before its first Question: `empty` is then the list under it."""
    owner, _, recs = _question_records(level, folder, root)
    extra = list((theme.report_cards(level, folder, root) or []) if theme is not None and theme.report_cards else [])
    cards, tag_lists, fixed_all = [], [], []
    for c in extra:                     # the theme's own cards (a paper's ideas, its standing Questions): fixed
        groups = _split_tags(",".join(str(g) for g in (c.get("groups") or [])))
        name = f'{c["id"]} · {c.get("title") or ""}'.rstrip(" ·")
        attrs, _, current, chips = _group_parts(str(c["id"]), name, groups, noun="question", fixed=groups)
        fixed_all += groups
        status = str(c.get("status") or "")
        cards.append(f'<details class="topic q-card q-theme" data-studio-tags="{_e(json.dumps(groups))}"{attrs}>'
                     f'<summary><span class=related-head><b>{_e(name)}</b>{chips}'
                     + (f'<br><span class=topic-meta>{_e(status)}</span>' if status else "")
                     + f'</span><span class=topic-pop>{current}</span></summary>{c.get("html") or ""}</details>')
        tag_lists.append(groups)
    for q in recs:
        fixed = _theme_fixed(theme, q["row"], owner)
        fixed_all += fixed
        groups = _split_tags(",".join(fixed + [q["group"]]))
        name = f'{q["id"]} · {q["title"]}'
        attrs, handle, current, chips = _group_parts(q["id"], name, groups, noun="question", fixed=fixed)
        dot = "answered" if q["status"].startswith("answered") else "partial" if q["status"].startswith("partial") else "open"
        meta = f'{q["status"]} · {q["work"]} piece{"" if q["work"] == 1 else "s"} of work'
        cards.append(f'<details class="topic q-card" data-studio-tags="{_e(json.dumps(groups))}"{attrs}><summary>'
                     f'{handle}<span class="q-dot {dot}" title="{_e(q["status"])}"></span><span class=related-head>'
                     f'<b>{_e(name)}</b>{chips}<br><span class=topic-meta>{_e(meta)}</span></span>'
                     f'<span class=topic-pop>{current}</span></summary>{Q_HEAD}{q["html"]}</details>')
        tag_lists.append(groups)
    where = _rel(face(owner), root) if face(owner) else "the face"
    note = (f'<p class=mut>{_link(_reader(face(owner), root), where) if face(owner) else where}: one card per Question; its '
            'groups are its register group: line, made and added as on a Studio topic' +
            (', and the theme\'s own, fixed' if theme is not None and (theme.report_fixed or theme.report_cards)
             else '') + '.</p>')
    if not cards:
        note = ""
    listing = "".join(cards) or empty or '<p class=mut>No Questions at this level yet.</p>'
    return note + group_list(owner, root, "reports", tag_lists, listing,
                             starting=(tuple(theme.report_groups) if theme is not None else ()) + REPORT_SUGGESTED,
                             fixed=tuple(dict.fromkeys(fixed_all)))


def _question_records(level: str, folder: Path, root: Path, keep=None) -> tuple:
    """(owner, groups, records): one record per Question of this level (id, group, its register row, title,
    status, how much work answers it, and its Logic │ Work │ Report row). `owner` is the level whose register
    is read: the folder, or a Job's Block when the Job has none of its own but `answers:` the Block's."""
    md = face(folder)
    register = _register(md)
    owner = folder                              # the level whose register, reports and studio are read
    block = _block_above(folder) if level == "Job" and not register else None
    asked = _answer_ids(md) if block else set()
    if block and not asked:     # or the Block's Questions whose work: names a file of this Job (cowork, s05-D17)
        here = folder.name + "/"
        asked = {str(r["id"]).lower() for r in _register(face(block))
                 if any(str(w.get("task") or w.get("path") or "" if isinstance(w, dict) else w).startswith(here)
                        for w in (r.get("work") if isinstance(r.get("work"), list) else []))}
    if asked:   # a Job with no Questions of its own shows the Block's its face answers: (JL 261011, an empty j51)
        owner = block
        register = [r for r in _register(face(block)) if str(r["id"]).lower() in asked]
    reports = {q.name.split("_", 1)[0].lower(): q for q in sorted((owner / "reports").glob("q*/"))   # q01_x, q-food-1_x
               if re.match(r"(?i)q[a-z-]*\d+_", q.name)} \
        if (owner / "reports").is_dir() else {}
    rows = [dict(r) for r in register]
    known = {str(r["id"]).lower() for r in rows}
    if owner == folder:
        rows += [{"id": k.upper(), "title": ""} for k in reports if k not in known]  # a report not yet registered
    feeders = {}
    for topic, drawings in _studio_topics(owner):
        for q in _note_facts(_notes(topic))["feeds"]:
            feeders.setdefault(q.split("_", 1)[0].lower(), []).append((topic, drawings[0] if drawings else None))
    if keep is not None:                        # keep(group) -> bool: the rows one view shows
        rows = [r for r in rows if keep(str(r.get("group") or ""))]
    groups = list(dict.fromkeys(str(r["group"]) for r in rows if r.get("group")))
    # the level's own Runs on a Question, as the Work column's head says (b10 s05 Open 3, Q05 read "no work yet"
    # under two Runs): a run card whose target: is the Question's id, run-report-q05's and run-check-q05's
    on_q = {}
    for run in runs_of(folder):
        card = run["path"] / "run.yaml" if run["path"].is_dir() else None
        text = card.read_text(encoding="utf-8", errors="ignore") if card and card.is_file() else ""
        target = _yaml_scalar(text, "target")
        if re.fullmatch(r"(?i)q[a-z-]*\d+", target):           # q05, q-food-1
            ticket = run["path"] / (_yaml_scalar(text, "ticket") or "-")
            on_q.setdefault(target.lower(), []).append(
                f'{_link(_reader(ticket if ticket.is_file() else card, root), run["run"])} '
                f'<span class=mut>{_e(run["status"])}</span>')
    out = []
    for r in rows:
        qid = str(r["id"])
        rp = r.get("report")
        page = (owner / rp) if rp and (owner / rp).is_file() else None
        if not page and qid.lower() in reports:
            q = reports[qid.lower()]
            page = q / (q.name + ".md") if (q / (q.name + ".md")).is_file() else None
        title = r.get("title") or (_title(page) if page else qid)
        status = dict(_fields(page)).get("answer-status", "open") if page else "open"
        studio = "".join(f'<li>{pop(_draw_url(d, root), t.name + " · from the Idea Studio", t.name + " ↗") if d else _e(t.name)}</li>'
                         for t, d in feeders.get(qid.lower(), []))
        logic = question_cell(qid, r, title, status) + (
            f'<p class=from>from the Idea Studio</p><ul class=from-list>{studio}</ul>' if studio else "")
        work = [str(w.get("task") or w.get("path") or w) if isinstance(w, dict) else str(w) for w in (r.get("work") or [])]
        if owner != folder:                     # the Block's work under this Job, named from the Job
            here = folder.relative_to(owner).as_posix() + "/"
            work = [w[len(here):] for w in work if w.startswith(here)]
        kids = _answering(folder, level, qid, root)
        named = {_rel(k, folder) for k in kids}  # a Task its face and the register's work: both name, once (b51 261021)
        work = [w for w in dict.fromkeys(work) if w.rstrip("/") not in named]
        runs = on_q.get(qid.lower(), [])
        work_html = " · ".join([_link(ROUTE + "?" + urlencode({"path": _rel(k, root)}), _rel(k, folder)) for k in kids]
                               + [_link(_reader(folder / w, root), w) if (folder / w).is_file() else _e(w)
                                  for w in work if w] + runs) or '<span class=mut>no work yet</span>'   # a file opens in the reader
        out.append({"id": qid, "group": str(r.get("group") or ""), "row": r, "title": str(title),
                    "status": str(status), "work": len(kids) + len([w for w in work if w]) + len(runs),
                    "html": f'<div class="q-row q-two" id="question-{_e(qid)}"><div class=q-l>{logic}</div>'
                            f'<div class=q-r>{_report_cell(qid, page, root, work_html)}</div></div>'})
    return owner, groups, out

def _first_sentence(text: str, most: int = 160) -> str:
    """The question's first sentence, cut at `most` characters: the short explanation under its name."""
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    m = re.match(r"(.+?[.?!])(\s|$)", text)
    one = m.group(1) if m else text
    return one if len(one) <= most else one[:most].rsplit(" ", 1)[0] + " …"


def question_cell(qid: str, row: dict, title: str, status: str) -> str:
    """The Question cell, as the Insight row has it (JL 261007): a label (Question 1) and its state
    dot, the Question's short name, one short sentence of what is asked, then › More with the rest;
    no "builds on" line."""
    num = re.match(r"^[A-Za-z]*0*(\d+)$", qid)
    label = f"Question {num.group(1)}" if num else qid
    state = str(status or "open").lower()
    dot = "answered" if state.startswith("answered") else "partial" if state.startswith("partial") else "open"
    name = str(row.get("slug") or row.get("name") or title or qid)
    ask = str(row.get("question") or "")
    short = _first_sentence(ask) if ask and ask.strip() != name.strip() else ""
    more = [(k, row.get(k)) for k in ("question", "hypothesis", "acceptance") if row.get(k)]
    more_html = ("<details class=q-more><summary>› More</summary>" + "".join(
        f'<p><span class=mut>{_e(k)}</span> {_e(v)}</p>' for k, v in more) + "</details>") if more else ""
    return (f'<p class=q-top><span class=q-label>{_e(label)}</span>'
            f'<span class="q-dot {dot}" title="{_e(status or "open")}"></span></p>'
            f'<p class=q-slug>{_e(name)}</p>' + (f'<p class=q-text>{_e(short)}</p>' if short else "") + more_html)
