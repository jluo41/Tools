"""Question-led Task Views using native report Pages and Excalidraw files.

The page follows the Insight Workbench (servers/workbench-insight/insightboard.py): the title
alone in the header, the band, the Spaces Guide → Scope → Task → Check → Delivery, every View
opened by a heading and one lead line, and the Task Space as one Logic / Work / Report table per
register group, a row per Question.
"""
import html
import json
import re
from pathlib import Path
from urllib.parse import urlencode, quote, urljoin, urlsplit

HERE = Path(__file__).parent
TABLE = HERE.parents[1] / "skills" / "task" / "haipipe-workbench-task" / "ref" / "workbench-table.md"
# Each View's heading and lead line (the Insight shape: <h2>, then <p class=lead>).
LEADS = {
    "block": ("Block", "The spine, the close condition and the Jobs, from board.md."),
    "register": ("Questions", "Each Question is one main topic; its Logic is a person's to sign. Ask one from the "
                              "Runs panel."),
    "related-paper": ("Resources", "The _WorkSpace folders the Jobs read, then the papers and links the "
                                   "Questions use."),
    "studio": ("RoadMap Draw", "The question map, drawn from the register by its script, then any drawing in "
                               "studio/. Each drawing opens on its own, and several can stay open."),
    "runs": ("Runs", "Every Run and its receipt status; a running receipt is not a heartbeat."),
    "tasks": ("Tasks", "Each Task Folder's Runs and what its audit found."),
    "progress": ("Reports", "Each report's answer status, evidence warnings and next action."),
    "delivery": ("Reports", "The answered reports, word for word, with the Results they cite."),
}


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "questions"


def groups(questions):
    """The register's groups in the order it first names them, each with its Questions; a
    register without groups is one group, Questions."""
    out = {}
    for q in questions:
        out.setdefault(q.get("group") or "Questions", []).append(q)
    return out or {"Questions": []}


def spaces(snap):
    """Spaces and their Views, in the shared order Guide → setup → work → Delivery
    (workbench-shared/README.md § Space order). A View key is the `view=` value; the earlier keys
    `related-paper`, `studio` and `progress` keep their meaning."""
    task = tuple(("q-" + slug(name), name) for name in groups(snap["questions"]))
    return (("scope", "Scope", (("block", "Block"), ("register", "Questions"), ("related-paper", "Resources"),
                                ("studio", "RoadMap Draw"))),
            ("task", "Task", task),
            ("check", "Check", (("runs", "Runs"), ("tasks", "Tasks"), ("progress", "Reports"))),
            ("delivery", "Delivery", (("delivery", "Reports"),)))


def render_report(report, board, root, board_path):
    """Show the current Page Face with the existing Page reader and appearance.

    Draft Reading displays plan-bound prose. A new report may have no Draft;
    reading its Page Face must still work without allocating a writing Run.
    """
    from src.page_workspace import load_page, render_page
    page = board / report["path"]
    document = render_page(load_page(page))
    base = '/' + quote(page.parent.relative_to(root).as_posix(), safe='/') + '/'
    # Preserve in-page fragment controls; resolve only relative source links.
    markup, separator, scripts = document.partition('<script')
    def source_attribute(match):
        value = html.unescape(match.group(2))
        if not value or value.startswith(('#', '/')) or urlsplit(value).scheme:
            return match.group(0)
        return match.group(1) + '="' + e(urljoin(base, value)) + '"'
    markup = re.sub(r'\b(href|src|poster)="([^"]*)"', source_attribute, markup)
    document = markup + separator + scripts
    document = document.replace('<details class="sect content">', '<details class="sect content" open>')
    # A Content section that holds a video starts open, so its players show without a click
    # (JL 261004: the setup videos in a CoWork Question report).
    head_part, *sections = document.split('<details class="csec">')
    document = head_part + ''.join(('<details class="csec" open>' if '<video' in part.split('</details>', 1)[0]
                                    else '<details class="csec">') + part for part in sections)
    back = '/_board/task-board?' + urlencode({"path": board_path, "view": "task"})
    controls = (f'<a href="{e(back)}">← Task</a> '
                + link(report["workbench_url"], 'Page Workbench')
                + ' ' + link(report["source_url"], 'Source'))
    return document.replace('<nav><a href="#reading">Page</a>', '<nav>' + controls, 1)


def e(value):
    return html.escape(str(value), quote=True)


def link(url, label):
    return f'<a href="{e(url)}" target="_blank" rel="noopener">{e(label)} ↗</a>' if url else ""


def issues(rows):
    return '<ul class="findings">' + ''.join(f'<li>{e(v)}</li>' for v in rows) + '</ul>' if rows else ""


def pop(url, label, text=None, cls=""):
    """A link that opens in the shared pop-out, with an own-tab link in its header."""
    return (f'<a class="{e(cls)}" data-run-result="{e(label)}" href="{e(url)}" target="_blank" rel="noopener">'
            f'{e(label if text is None else text)}</a>') if url else e(label if text is None else text)


def head(view, lead=None):
    title, text = LEADS[view]
    return f'<h2>{e(title)}</h2><p class=lead>{e(lead or text)}</p>'


def idname(name):
    """`j51_some_job` -> idtag `j51` + `some_job`."""
    first, _, rest = name.partition('_')
    return f'<span class="idtag">{e(first)}</span>' + (f' {e(rest)}' if rest else '')


def qnumber(qid):
    """Q01 -> "Question 1": the id stays in the row's tag and links (as Insight's); Q-food-1 shows as itself."""
    return "Question " + str(int(qid[1:])) if qid[1:].isdigit() else qid


def work_tree(items):
    """Insight's Task Work tree: Block → Job → Task → Run, each level written once.

    Items are (task, role) in register order; a Task folds its Runs and Task Page.
    """
    out, last_block, last_job = [], None, None
    for task, role in items:
        if task['block'] != last_block:
            out.append(f'<div class="bj-b">{idname(task["block"])}</div>')
            last_block, last_job = task['block'], None
        if task['job'] != last_job:
            out.append(f'<div class="bj-j">{idname(task["job"])}</div>')
            last_job = task['job']
        count = len(task['runs'])
        runs = ''.join(pop(run["result_url"], run["name"], cls="bj-run idtag") for run in task['runs'])
        runs += pop(task["page_url"], task["name"], "Task Page", cls="bj-run bj-page")
        out.append(f'<details class="bj-tr"><summary class="bj-t" title="{e(role or task["purpose"])}">{idname(task["name"])} '
                   f'<span class="mut">▸ {count} run{"" if count == 1 else "s"}</span></summary>'
                   f'<div class="bj-runs">{runs}</div></details>')
    return '<div class="bj">' + ''.join(out) + '</div>'


def work_html(question):
    if not question['work']:
        return '<p class="wk-none">No Task linked; reasoning or existing evidence can answer it.</p>'
    # The register's order is the authored workflow; Jobs are grouped as first met.
    jobs = list(dict.fromkeys(item['task']['job'] for item in question['work']))
    items = [(item['task'], item['role']) for job in jobs for item in question['work'] if item['task']['job'] == job]
    runs = sum(len(item['task']['runs']) for item in question['work'])
    count = (f'{len(items)} Task{"" if len(items) == 1 else "s"} · {runs} run{"" if runs == 1 else "s"}')
    return (f'<details class="wk" open><summary><span class="kind">Task Work</span> <span class="mut">{count}</span>'
            f'</summary>{work_tree(items)}</details>')


def report_html(question):
    """Insight's Report cell: the report's title, which pops out, then its Opening, then a tag."""
    report = question["report"]
    label = '<p class="rp-label"><span class="kind">Report</span></p>'
    if not report["present"]:
        return label + '<p class="wk-none">No report yet</p>'
    tag = Path(report["path"]).stem.split("_", 1)[0]
    return (label + f'<p class="rp-title">{pop(report["url"], report["title"] or report["path"])}</p>'
            + (f'<p class="rp-text">{e(report["answer"])}</p>' if report["answer"] else '')
            + ''.join(f'<a class="rp-thumb" data-run-result="Drawing · {e(d["title"])}" href="{e(d["url"])}" '
                      f'target="_blank" rel="noopener" title="Open {e(d["title"])}">'
                      f'<img src="{e(d["png"])}" alt="{e(d["title"])}" loading="lazy"></a>' if d.get("png") else
                      f'<p class="rp-draw">{pop(d["url"], d["title"], "Drawing · " + d["title"])}</p>'
                      for d in report.get("drawings", []))
            + f'<p class="rp-tags">report {e(tag)}</p>')


def question_row(question):
    """One row of the Task table: Logic │ Work │ Report (Insight's .hl-row), no status."""
    q = question
    more = [("What we expect", q["hypothesis"]), ("What would answer it", q["acceptance"])]
    dl = ''.join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k, v in more if v)
    if q["issues"]:
        dl += f'<dt>Register findings</dt><dd>{issues(q["issues"])}</dd>'
    logic = (f'<div class="hl-l"><div class="q-top"><span class="kind">{e(qnumber(q["id"]))}</span></div>'
             f'<div class="q-title"><b class="q-name">{e(q["title"])}</b></div>'
             + (f'<div class="q-text">{e(q["question"])}</div>' if q["question"] != q["title"] else '')
             + (f'<div class="q-aim"><b>Aim</b> {e(q["aim"])}</div>' if q.get("aim") else '')
             + (f'<details class="q-more"><summary>More</summary><dl>{dl}</dl></details>' if dl else '') + '</div>')
    return (f'<div class="hl-row" id="question-{e(q["id"])}" data-key="{e(q["id"])}" data-label="{e(q["id"])} · {e(q["title"])}">'
            f'{logic}<div class="hl-r">{work_html(q)}</div><div class="hl-p">{report_html(q)}</div></div>')


def task_view(name, questions, unassigned):
    rows = ''.join(question_row(q) for q in questions)
    other = ''
    if unassigned:
        other = (f'<details class="lvl" id="unassigned"><summary>Not under a Question <span class="mut">'
                 f'{len(unassigned)} Tasks</span></summary><div class="hl-free">'
                 + work_tree([(t, "") for t in unassigned]) + '</div></details>')
    if not rows and not other:
        rows = '<p class="note">No Questions registered yet. Ask one from Scope; existing work is listed here.</p>'
    count = f'{len(questions)} Question{"" if len(questions) == 1 else "s"}'
    # a heading and no lead line, as Insight's partition Views: the head row says what each column holds
    return (f'<h2>{e(name)} · {count}</h2><div class="hl-wrap"><div class="hl">'
            '<div class="hl-head"><span>Logic · the question</span><span>Work · the Tasks and Runs</span>'
            f'<span>Report · what it says</span></div>{rows}{other}</div></div>')


def progress_html(question):
    q, report = question, question["report"]
    completed = sum(w["task"]["complete"] for w in q["work"])
    total = sum(w["task"]["total"] for w in q["work"])
    return (f'<article class="card">'
            f'<h3><a href="#question-{e(q["id"])}" data-question="{e(q["id"])}">{e(q["id"])} · {e(q["title"])}</a>'
            f'<span class="pill acc">{e(report["status"].capitalize())}</span></h3>'
            f'<p>{e(report["answer"] or "No answer yet.")}</p>'
            f'<p class="mut">Work: {completed}/{total} Task Runs complete · {len(q["work"])} linked Tasks</p>'
            f'<p><strong>Next:</strong> {e(report["next"] or "Record the next action in the Report.")}</p>'
            + issues(q["issues"] + report["issues"])
            + f'<p class="links">{link(report["url"], "Report")}</p></article>')


def delivery_html(snap):
    """Delivery › Reports: each answered report, its Opening and Answer word for word, then the
    Results and drawings it cites."""
    cards = []
    for q in snap["questions"]:
        r = q["report"]
        if not (r["present"] and r["status"] == "answered"):
            continue
        evidence = ''.join(f'<li>{pop(x.get("url"), x["title"])}</li>' for x in r["evidence"])
        drawings = ''.join(f'<li>{pop(d["url"], d["title"], "Drawing · " + d["title"])}</li>' for d in r.get("drawings", []))
        cards.append(f'<article class="card"><h3>{pop(r["url"], r["title"] or r["path"])} <span class="mut">'
                     f'{e(q["id"])}</span></h3>'
                     + ''.join(f'<p>{e(p)}</p>' for p in r.get("opening", []))
                     + (('<h4>Answer</h4>' + ''.join(f'<p>{e(p)}</p>' for p in r["answer_text"])) if r.get("answer_text") else '')
                     + (f'<h4>Evidence</h4><ul>{evidence}{drawings}</ul>' if evidence or drawings else '')
                     + '</article>')
    return ''.join(cards) or ('<p class="note">No Question is answered yet. A report moves here when its '
                              'answer-status is answered.</p>')


def drawing_html(drawing):
    """A RoadMap Draw row (Insight's details.draw): a generated drawing is view only and names its
    script; any other drawing takes the pen with Edit drawing."""
    url = '/_excalidraw/?' + urlencode({"board": drawing["path"]})
    if drawing.get("source"):
        note = ('❗ the register changed after it was drawn: rerun ' if drawing.get("stale") else 'generated by ')
        bar = (f'<span class="mut">{note}<span class="mono">{e(drawing["source"])}</span>, never edited</span>'
               f'{link(url, "Open full screen")}')
    else:
        bar = (f'<span><button type="button" class="draw-edit">Edit drawing</button> '
               f'<span class="mono mut">{e(drawing["path"])}</span></span>{link(url + "&edit=1", "Open full screen")}')
    return (f'<details class="draw" data-board="{e(drawing["path"])}"><summary>{e(drawing["title"])}</summary>'
            f'<div class="st-bar">{bar}</div>'
            f'<iframe class="st-frame" title="{e(drawing["title"])}" data-src="{e(url)}" referrerpolicy="no-referrer"></iframe>'
            '</details>')


def table_rows():
    """The Task Workbench Table (skills/0_utils/table-workbench), or [] when it cannot be read."""
    import importlib.util
    reader = HERE.parents[1] / "skills" / "0_utils" / "table-workbench" / "ref" / "render_workbench_table.py"
    try:
        spec = importlib.util.spec_from_file_location("render_workbench_table", reader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.read_table(TABLE)
    except (OSError, SystemExit):
        return []


def runs_panel(space, snap, rows):
    """The shared Runs panel (live.runs_panel) for one Space: its run types from the Workbench
    Table, each with its agent, skill and a prompt to copy. Native Runs and their status sit under
    "Run a Task"; a selected Question row narrows them to its Tasks and names it in each prompt.
    Nothing here starts a run; the panel starts folded, as Insight's."""
    from live.runs_panel import panel_markup
    block = snap["path"].rsplit("/", 1)[0]
    serves = {}
    for q in snap["questions"]:
        for w in q["work"]:
            serves.setdefault(w["task"]["id"], []).append(q["id"])
    kinds, buckets = [], []
    for r in rows:
        if r["Space"].lower() != space or r["Run type"] in ("", "none"):
            continue
        signs = f' The person signs {r["Person signs"]}.' if r["Person signs"] not in ("", "none") else ""
        planned = lambda value: value.replace(" (new)", " (planned)")
        target = " {ticket}" if r["Run type"] == "Run a Task" else ""
        about = " for {target}" if space == "task" else ""
        kinds.append({"label": r["Run type"], "pattern": "", "views": "",
                      "skills": [r["Skill"].replace(" (new)", "")] if r["Skill"] not in ("", "none") else [],
                      "prompt": f'Run with {planned(r["Agent"])}: {r["Run type"]}{target}{about} in the Task Block {block} '
                                f'({r["Space"]} › {r["View"]}), following {planned(r["Skill"])}.{signs}'})
        if r["Run type"] == "Run a Task":
            buckets.append([{"run_id": f'{run["job"][:3]}·{run["task_id"][-3:]}·{run["name"]}',
                             "status": run["status"], "target": run["task_title"],
                             "_keys": " ".join(serves.get(run["task_id"], [])),
                             "ticket": run["ticket_url"].lstrip("/"), "result": run["receipt_url"].lstrip("/"),
                             "_display": f'{run["job"][:3]} {run["task_id"][-3:]} {run["name"]}'}
                            for run in snap["runs"]])
        else:
            buckets.append([])
    if not kinds:
        return ""
    fill = lambda row: {"ticket": row.get("ticket") or "<job>/<task>/runs/<run>.sh"}
    return panel_markup(space, kinds, buckets, base=HERE, fill=fill, whole=f"the Block {snap['block']}", folded=True)


def block_html(snap):
    """Scope › Block, in the shape of Insight's Scope › Dataset: one label column, one value column."""
    jobs = ''.join(f'<li>{idname(j["name"])} <span class="mut">· {len(j["tasks"])} Tasks</span></li>' for j in snap["jobs"])
    rows = [("spine", e(snap["spine"] or "Not recorded.")), ("close condition", e(snap["close"] or "Not recorded.")),
            ("jobs", f'<ul class="plain">{jobs}</ul>'),
            ("described by", link(snap["source_url"], "board.md") + ' <span class="mut">· the spine, Questions and '
                             'related resources</span>')]
    return '<table class="rows inputs">' + ''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k, v in rows) + '</table>'


def register_html(snap):
    rows = ''.join(f'<tr><td><a href="#question-{e(q["id"])}" data-question="{e(q["id"])}">{e(q["id"])}</a></td>'
                   f'<td>{e(q.get("group") or "")}</td><td>{e(q["title"])}</td><td>{e(q["question"])}</td>'
                   f'<td class="num">{len(q["work"])}</td></tr>'
                   for q in snap["questions"])
    return ('<div class="scroll"><table><tr><th>Id</th><th>Group</th><th>Topic</th><th>Question</th><th>Tasks</th></tr>'
            f'{rows}</table></div>' if rows else
            '<p class="note">No Questions registered yet. Ask one from this Space\'s Runs panel.</p>')


def runs_html(snap):
    tone = {"complete": "ok", "running": "acc", "failed": "bad", "missing": "bad", "attention": "warn", "planned": "warn"}
    rows = ''.join(f'<tr><td class="mono">{e(run["job"][:3])} {e(run["task_id"][-3:])}</td>'
                   f'<td>{pop(run["result_url"], run["name"], cls="idtag")}</td>'
                   f'<td><span class="pill {tone.get(run["status"], "")}">{e(run["status"])}</span></td>'
                   f'<td class="mono">{e(run["finished"] or run["started"])}</td></tr>'
                   for run in snap["runs"])
    lead = (f'{snap["totals"]["complete"]}/{snap["totals"]["runs"]} Task Runs complete. '
            'A running receipt is not a heartbeat.')
    return (head("runs", lead) + ('<div class="scroll"><table><tr><th>Task</th><th>Run</th><th>Status</th><th>Finished</th>'
            f'</tr>{rows}</table></div>' if rows else '<p class="note">No Runs yet.</p>'))


def tasks_html(snap):
    rows = ''.join(f'<tr><td class="mono">{e(t["job"][:3])}</td><td>{pop(t["page_url"], t["name"], cls="idtag")}</td>'
                   f'<td class="num">{t["complete"]}/{t["total"]}</td><td>{e("; ".join(t["issues"]) or "none")}</td></tr>'
                   for t in snap["tasks"])
    return ('<div class="scroll"><table><tr><th>Job</th><th>Task</th><th>Runs complete</th>'
            f'<th>Findings</th></tr>{rows}</table></div>')


def workspace_html(stores):
    """Scope › Resources, first part: the _WorkSpace folders the Block's Jobs declare.
    Data files are named and sized only; documents, figures, drawings and scripts pop out."""
    if not stores:
        return ('<h3>Workspace data</h3><p class="note">No Job declares a _WorkSpace folder '
                '(raw_store + cohort, or a _WorkSpace/ path, in jNN_<job>/src/config-defaults.yaml).</p>')
    order = {"data": 0, "doc": 1, "drawing": 2, "figure": 3, "script": 4}
    cards = []
    for store in stores:
        files = sorted(store["files"], key=lambda f: (order.get(f["kind"], 9), f["name"]))
        rows = ''.join(f'<li><span class="ws-kind">{e(f["kind"])}</span> '
                       + (pop(f["url"], f["name"], cls="idtag") if f["url"] else f'<span class="idtag">{e(f["name"])}</span>')
                       + f' <span class="mut">{e(f["size"])}</span></li>' for f in files)
        used = (" · read by " + ", ".join(j[:3] for j in store["jobs"])) if store["jobs"] else ""
        cards.append(f'<details class="draw ws"><summary><code>{e(store["path"])}</code>'
                     f' <span class="mut">{e(store["role"])}{e(used)} · {len(files)} files</span></summary>'
                     f'<ul class="ws-files">{rows or "<li class=mut>empty</li>"}</ul></details>')
    return '<h3>Workspace data</h3>' + ''.join(cards)


FORM = """<details class="draw" id="add-resource"><summary>+ Add resource</summary>
<form id="tw-add-resource"><label>Title<input name="title" required maxlength="300"></label>
<label>Source URL<input name="url" type="url" required placeholder="https://" maxlength="2000"></label>
<label>Related Questions<input name="questions" placeholder="Q01, Q02"></label>
<label>How it helps<textarea name="contribution" rows="2"></textarea></label>
<label>Notes<textarea name="notes" rows="3"></textarea></label><button type="submit">Save resource</button><p role="status"></p></form></details>"""


def render(snap, view="task"):
    space_list = spaces(snap)
    space_of = {key: space for space, _, views in space_list for key, _ in views}
    first_task = space_list[1][2][0][0]
    aliases = {"scope": "block", "task": first_task, "check": "runs", "roadmap": "studio"}
    view = view if view in space_of else aliases.get(view, first_task)
    space = space_of[view]
    resources = ''.join(f'<details class="draw"><summary>{e(r["title"])} <span class="mut">'
                        f'{e(", ".join(r["questions"]) or "Block reference")}</span></summary><div class="dr-body">'
                        f'<p>{e(r["contribution"])}</p><p class="mut">{e(r["notes"] or "No notes yet.")}</p>'
                        f'<p>{link(r["url"], "Open source")}</p></div></details>'
                        for r in snap["resources"])
    drawings = ''.join(drawing_html(d) for d in snap["drawings"])
    no_draw = ('<p class="note" id="tw-no-drawings">No drawings yet: run "Draw the question map" in the Runs panel, '
               'or add a drawing to explore an idea, workflow or folder map.</p>')
    studio = (f'<div id="tw-drawings">{drawings or no_draw}</div><form id="tw-add-drawing"><label>Drawing name<input name="name" required placeholder="Drawing 1" maxlength="80" pattern="[A-Za-z0-9_ -]+"></label><button type="submit">+ Add drawing</button><p role="status"></p></form>'
              + ('' if snap['studio_enabled'] else '<p class="note">This host has drawing routes disabled. Open this Block on the full Studio-enabled host to edit drawings.</p>'))
    bodies = {
        "block": head("block") + block_html(snap),
        "register": head("register") + register_html(snap),
        "related-paper": head("related-paper") + workspace_html(snap.get("workspace", []))
                         + f'<h3>Related resources</h3>{resources or "<p class=note>No related resources yet.</p>"}{FORM}',
        "studio": head("studio") + studio,
        "runs": runs_html(snap),
        "tasks": head("tasks") + tasks_html(snap),
        "progress": head("progress", f'{len(snap["questions"])} Questions. Each report\'s answer status, evidence '
                                     'warnings and next action.')
                    + (''.join(progress_html(q) for q in snap["questions"]) or '<p class="note">No Questions registered yet.</p>'),
        "delivery": head("delivery") + delivery_html(snap),
    }
    grouped = groups(snap["questions"])
    task_keys = [key for key, _ in space_list[1][2]]
    for index, (name, questions) in enumerate(grouped.items()):
        last = index == len(grouped) - 1
        bodies[task_keys[index]] = task_view(name, questions, snap["unassigned"] if last else [])
    rows = table_rows()
    panes = []
    for key, title, views in space_list:
        tabs = ''.join(f'<button type="button" class="wtab{" on" if k == view else ""}" data-view="{k}">{e(t)}</button>'
                       for k, t in views)
        sections = ''.join(f'<section class="view{" on" if k == view else ""}" data-panel="{k}">{bodies[k]}</section>'
                           for k, _ in views)
        panes.append(f'<section class="pane{" on" if key == space else ""}" data-space-pane="{key}"><div class="split">'
                     f'<div class="space-main"><div class="wtabs" role="tablist" aria-label="{title} Views">{tabs}</div>'
                     f'{sections}</div>{runs_panel(key, snap, rows)}</div></section>')
    space_row = ''.join(f'<button type="button" class="space{" on" if key == space else ""}" data-space="{key}" '
                        f'aria-selected="{str(key == space).lower()}">{title}</button>' for key, title, _ in space_list)
    band = " · ".join([snap["block"], f'{snap["totals"]["jobs"]} Jobs', f'{snap["totals"]["tasks"]} Tasks',
                       f'{snap["totals"]["runs"]} Runs', f'{len(snap["questions"])} Questions'])
    config = json.dumps({"path": snap["path"], "studio": snap["studio_path"], "studioEnabled": snap["studio_enabled"],
                         "spaces": {key: [k for k, _ in views] for key, _, views in space_list}, "aliases": aliases},
                        ensure_ascii=False).replace('<', '\\u003c')
    from live.runs_panel import PANEL_CSS, PANEL_JS, SPLIT_CSS
    css = ((HERE / 'assets/css/90-task-workbench.css').read_text() + '\n' + PANEL_CSS + SPLIT_CSS
           + '.split{--card:var(--bg)}')
    js = (HERE / 'assets/js/90-task-workbench.js').read_text()
    content = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>📋 Task · {e(snap['title'])}</title><link rel="icon" href="data:,"><style>{css}</style></head>
<body class="tw"><main id="task-workbench"><header><h1>📋 Task · {e(snap['title'])}</h1></header>
<div class="dataset" title="{e(snap['spine'])}">{e(band)}</div>
<nav class="spaces" aria-label="Spaces">{space_row}</nav>
<div class="tw-source-issues">{issues(snap['source_issues'])}</div>
{''.join(panes)}
<dialog id="tw-run-dialog" aria-label="Pop-out"><div class="pop-bar"><span class="pop-title" id="tw-run-title">Pop-out</span><a class="pop-new" id="tw-run-new" target="_blank" rel="noopener">Open in its own tab ↗</a><button type="button" class="pop-x" id="tw-run-close" aria-label="Close">×</button></div><iframe class="pop-frame" id="tw-run-frame" title="Pop-out"></iframe></dialog><p id="tw-status" role="status"></p></main><script type="application/json" id="tw-config">{config}</script><script>{js}</script><script>{PANEL_JS}</script></body></html>'''
    from live.workbench_guide import mount_guide
    return mount_guide(content, "task", {"path": snap["path"], "file": "board.md"},
                       "nav.spaces", "[data-space-pane],.tw-source-issues,#tw-status")
