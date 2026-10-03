"""Question-led Task Views using native report Pages and Excalidraw files."""
import html
import json
import re
from pathlib import Path
from urllib.parse import urlencode, quote, urljoin, urlsplit

HERE = Path(__file__).parent
# Spaces and their Views, in work order (ref/workbench-table.md). A View key is the `view=` value;
# the earlier keys `related-paper` and `progress` keep their meaning (Block resources, Reports).
SPACES = (("scope", "Scope", (("block", "Block"), ("register", "Questions"), ("related-paper", "Resources"))),
          ("task", "Task", (("task", "Questions"), ("studio", "Studio"))),
          ("check", "Check", (("runs", "Runs"), ("tasks", "Tasks"), ("progress", "Reports"))))
VIEWS = tuple((key, title) for _, _, views in SPACES for key, title in views)
SPACE_OF = {key: space for space, _, views in SPACES for key, _ in views}
TABLE = HERE.parents[1] / "skills" / "task" / "haipipe-workbench-task" / "ref" / "workbench-table.md"


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
    return '<ul class="tw-findings">' + ''.join(f'<li>{e(v)}</li>' for v in rows) + '</ul>' if rows else ""


def pop(url, label, text=None, cls=""):
    """A link that opens in the shared pop-out, with an own-tab link in its header."""
    return (f'<a class="{e(cls)}" data-run-result="{e(label)}" href="{e(url)}" target="_blank" rel="noopener">'
            f'{e(label if text is None else text)}</a>') if url else e(label if text is None else text)


def report_html(report):
    """Insight's Report cell: the report's title, which pops out, then its Opening."""
    if not report["present"]:
        return '<p class="tw-none">No report yet</p>'
    return (f'<p class="tw-rp-title">{pop(report["url"], report["title"] or report["path"])}</p>'
            + (f'<p class="tw-rp-text">{e(report["answer"])}</p>' if report["answer"] else '')
            + ''.join(f'<p class="tw-rp-draw">{pop(d["url"], d["title"], "Drawing · " + d["title"])}</p>'
                      for d in report.get("drawings", [])))


def idname(name):
    """`j51_some_job` -> idtag `j51` + `some_job`."""
    head, _, tail = name.partition('_')
    return f'<span class="idtag">{e(head)}</span>' + (f' {e(tail)}' if tail else '')


def work_tree(items):
    """Insight's Task Work: Block → Job → Task → Run, each level written once.

    Items are (task, role) in register order; a Task folds its Runs and Task Page.
    """
    out, last_block, last_job = [], None, None
    for task, role in items:
        if task['block'] != last_block:
            out.append(f'<div class="tw-b">{idname(task["block"])}</div>')
            last_block, last_job = task['block'], None
        if task['job'] != last_job:
            out.append(f'<div class="tw-j">{idname(task["job"])}</div>')
            last_job = task['job']
        count = len(task['runs'])
        runs = ''.join(f'<div class="tw-r">{pop(run["result_url"], run["name"], cls="idtag")}</div>'
                       for run in task['runs'])
        runs += f'<div class="tw-r">{pop(task["page_url"], task["name"], "Task Page", cls="tw-pg")}</div>'
        out.append(f'<details class="tw-t"><summary title="{e(role or task["purpose"])}">{idname(task["name"])} '
                   f'<span class="mut">▸ {count} run{"" if count == 1 else "s"}</span></summary>{runs}</details>')
    return '<div class="tw-tree">' + ''.join(out) + '</div>'


def work_html(question):
    if not question['work']:
        return '<p class="tw-none">No Task linked; reasoning or existing evidence can answer it.</p>'
    # The register's order is the authored workflow; Jobs are grouped as first met.
    jobs = list(dict.fromkeys(item['task']['job'] for item in question['work']))
    items = [(item['task'], item['role']) for job in jobs for item in question['work'] if item['task']['job'] == job]
    return work_tree(items)


def context(question):
    report = question["report"]
    return '\n'.join(['Block: ' + question["block_path"],
                      f'{question["id"]}: {question["question"]}',
                      'Hypothesis: ' + question["hypothesis"], 'Acceptance: ' + question["acceptance"],
                      'Work: ' + ', '.join(w["path"] for w in question["work"]),
                      'Report: ' + report["path"], 'Answer status: ' + report["status"],
                      'Answer: ' + report["answer"],
                      'Evidence: ' + '; '.join(r['title'] + ': ' + (r['path'] or r['url']) for r in report['evidence']),
                      'Limits: ' + report["limits"], 'Next: ' + report["next"],
                      'Review: ' + '; '.join(question["issues"] + report["issues"])])


def question_html(question):
    q, r = question, question["report"]
    search = ' '.join([q["id"], q["title"], q["question"], r["answer"], r["limits"], r["next"]])
    return (f'<details class="tw-question" id="question-{e(q["id"])}" data-search="{e(search.lower())}" open>'
            f'<summary><strong>{e(q["id"])} · {e(q["title"])}</strong><span>{e(q["question"])}</span>'
            f'<small>{e(r["answer"] or "No answer yet")}</small></summary>'
            '<div class="tw-columns">'
            f'<section><h3>Logic</h3><h4>Hypothesis</h4><p>{e(q["hypothesis"] or "Not recorded.")}</p>'
            f'<h4>Acceptance</h4><p>{e(q["acceptance"] or "Not recorded.")}</p>' + issues(q["issues"]) + '</section>'
            f'<section class="tw-work-column"><h3>Task Work</h3>{work_html(q)}</section>'
            f'<section><h3>Report</h3>{report_html(r)}</section></div></details>')


def progress_html(question):
    q, report = question, question["report"]
    completed = sum(w["task"]["complete"] for w in q["work"])
    total = sum(w["task"]["total"] for w in q["work"])
    return (f'<article class="tw-progress-card" data-search="{e(context(q).lower())}">'
            f'<h2><a href="#question-{e(q["id"])}" data-question="{e(q["id"])}">{e(q["id"])} · {e(q["title"])}</a>'
            f'<span class="tw-answer-state">{e(report["status"].capitalize())}</span></h2>'
            f'<p>{e(report["answer"] or "No answer yet.")}</p>'
            f'<p class="tw-muted">Work: {completed}/{total} Task Runs complete · {len(q["work"])} linked Tasks</p>'
            f'<p><strong>Next:</strong> {e(report["next"] or "Record the next action in the Report.")}</p>'
            + issues(q["issues"] + report["issues"])
            + f'<div class="tw-links">{link(report["url"], "Report")}</div></article>')


def drawing_html(drawing, index):
    url = '/_excalidraw/?' + urlencode({"board": drawing["path"]})
    return (f'<details class="tw-drawing" id="drawing-{index}" data-board="{e(drawing["path"])}">'
            f'<summary>{e(drawing["title"])}</summary><div class="tw-drawing-body">'
            f'<div class="tw-links"><button type="button" data-edit-drawing>Edit drawing</button>'
            f'{link(url + "&edit=1", "Open full screen")}<code>{e(drawing["path"])}</code></div>'
            f'<iframe title="{e(drawing["title"])}" data-src="{e(url)}" referrerpolicy="no-referrer"></iframe>'
            '</div></details>')


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
    "Run a Task"; nothing here starts a run."""
    from live.runs_panel import panel_markup
    block = snap["path"].rsplit("/", 1)[0]
    kinds, buckets = [], []
    for r in rows:
        if r["Space"].lower() != space or r["Run type"] in ("", "none"):
            continue
        signs = f' The person signs {r["Person signs"]}.' if r["Person signs"] not in ("", "none") else ""
        planned = lambda value: value.replace(" (new)", " (planned)")
        target = " {ticket}" if r["Run type"] == "Run a Task" else ""
        kinds.append({"label": r["Run type"], "pattern": "", "views": "",
                      "skills": [r["Skill"].replace(" (new)", "")] if r["Skill"] not in ("", "none") else [],
                      "prompt": f'Run with {planned(r["Agent"])}: {r["Run type"]}{target} in the Task Block {block} '
                                f'({r["Space"]} › {r["View"]}), following {planned(r["Skill"])}.{signs}'})
        if r["Run type"] == "Run a Task":
            buckets.append([{"run_id": f'{run["job"][:3]}·{run["task_id"][-3:]}·{run["name"]}',
                             "status": run["status"], "target": run["task_title"],
                             "ticket": run["ticket_url"].lstrip("/"), "result": run["receipt_url"].lstrip("/"),
                             "_display": f'{run["job"][:3]} {run["task_id"][-3:]} {run["name"]}'}
                            for run in snap["runs"]])
        else:
            buckets.append([])
    if not kinds:
        return ""
    fill = lambda row: {"ticket": row.get("ticket") or "<job>/<task>/runs/<run>.sh"}
    return panel_markup(space, kinds, buckets, base=HERE, fill=fill, whole=f"the Block {snap['block']}")


def block_html(snap):
    jobs = ''.join(f'<li><span class="idtag">{e(j["id"])}</span> {e(j["name"][4:])} · {len(j["tasks"])} Tasks</li>'
                   for j in snap["jobs"])
    return (f'<section class="tw-scope-block"><h3>Spine</h3><p>{e(snap["spine"] or "Not recorded.")}</p>'
            f'<h3>Close condition</h3><p>{e(snap["close"] or "Not recorded.")}</p>'
            f'<h3>Jobs</h3><ul class="tw-jobs">{jobs}</ul>'
            f'<div class="tw-links">{link(snap["source_url"], "board.md")}</div></section>')


def register_html(snap):
    rows = ''.join(f'<tr data-search="{e((q["id"] + " " + q["title"] + " " + q["question"]).lower())}">'
                   f'<td><a href="#question-{e(q["id"])}" data-question="{e(q["id"])}">{e(q["id"])}</a></td>'
                   f'<td>{e(q["title"])}</td><td>{e(q["question"])}</td><td>{len(q["work"])}</td></tr>'
                   for q in snap["questions"])
    return ('<div class="tw-table-scroll"><table><thead><tr><th>Id</th><th>Topic</th><th>Question</th>'
            f'<th>Tasks</th></tr></thead><tbody>{rows}</tbody></table></div>' if rows else
            '<p class="tw-empty">No Questions registered yet. Ask one from this Space\'s Runs panel.</p>')


def runs_html(snap):
    rows = ''.join(f'<tr data-search="{e((run["job"] + " " + run["task_title"] + " " + run["name"] + " " + run["status"]).lower())}">'
                   f'<td>{e(run["job"][:3])} {e(run["task_id"][-3:])}</td><td>{pop(run["result_url"], run["name"], cls="idtag")}</td>'
                   f'<td><span class="tw-badge tw-{e(run["status"])}">{e(run["status"])}</span></td>'
                   f'<td>{e(run["finished"] or run["started"])}</td></tr>'
                   for run in snap["runs"])
    return ('<div class="tw-table-scroll"><table><thead><tr><th>Task</th><th>Run</th><th>Status</th><th>Finished</th>'
            f'</tr></thead><tbody>{rows}</tbody></table></div>' if rows else '<p class="tw-empty">No Runs yet.</p>')


def tasks_html(snap):
    rows = ''.join(f'<tr data-search="{e((t["job"] + " " + t["name"] + " " + " ".join(t["issues"])).lower())}">'
                   f'<td>{e(t["job"][:3])}</td><td>{pop(t["page_url"], t["name"], cls="idtag")}</td>'
                   f'<td>{t["complete"]}/{t["total"]}</td><td>{e("; ".join(t["issues"]) or "none")}</td></tr>'
                   for t in snap["tasks"])
    return ('<div class="tw-table-scroll"><table><thead><tr><th>Job</th><th>Task</th><th>Runs complete</th>'
            f'<th>Findings</th></tr></thead><tbody>{rows}</tbody></table></div>')


def workspace_html(stores):
    """Scope › Resources, first part: the _WorkSpace folders the Block's Jobs declare.
    Data files are named and sized only; documents, figures, drawings and scripts pop out."""
    if not stores:
        return ('<h3 class="tw-res-head">Workspace data</h3><p class="tw-empty">No Job declares a _WorkSpace folder '
                '(raw_store + cohort, or a _WorkSpace/ path, in jNN_<job>/src/config-defaults.yaml).</p>')
    order = {"data": 0, "doc": 1, "drawing": 2, "figure": 3, "script": 4}
    cards = []
    for store in stores:
        files = sorted(store["files"], key=lambda f: (order.get(f["kind"], 9), f["name"]))
        rows = ''.join(f'<li><span class="tw-kind">{e(f["kind"])}</span> '
                       + (pop(f["url"], f["name"], cls="idtag") if f["url"] else f'<span class="idtag">{e(f["name"])}</span>')
                       + f' <span class="mut">{e(f["size"])}</span></li>' for f in files)
        used = (" · read by " + ", ".join(j[:3] for j in store["jobs"])) if store["jobs"] else ""
        cards.append(f'<details class="tw-store" data-search="{e(store["path"].lower())}"><summary><code>{e(store["path"])}</code>'
                     f' <span class="mut">{e(store["role"])}{e(used)} · {len(files)} files</span></summary>'
                     f'<ul class="tw-store-files">{rows or "<li class=mut>empty</li>"}</ul></details>')
    return ('<h3 class="tw-res-head">Workspace data</h3><p class="tw-explain">The _WorkSpace folders this Block reads, '
            'from each Job\'s config-defaults.yaml, and where its heavy Run output goes. A data file is named and sized, '
            'never opened here.</p>' + ''.join(cards))


def render(snap, view="task"):
    view = view if view in SPACE_OF else {"scope": "block", "check": "runs"}.get(view, "task")
    space = SPACE_OF[view]
    questions = ''.join(question_html(q) for q in snap["questions"])
    progress = ''.join(progress_html(q) for q in snap["questions"])
    if snap["unassigned"]:
        questions += ('<details class="tw-unassigned" id="unassigned"><summary>Not under a Question · '
                      + str(len(snap["unassigned"])) + ' Tasks</summary><div class="tw-work-column">'
                      + work_tree([(t, "") for t in snap["unassigned"]]) + '</div></details>')
    resources = ''.join(f'<details class="tw-resource" id="resource-{i}" data-search="{e(str(r).lower())}">'
                        f'<summary><strong>{e(r["title"])}</strong><span>{e(r["contribution"])}</span>'
                        f'<small>{e(", ".join(r["questions"]) or "Block reference")}</small></summary>'
                        f'<p>{e(r["notes"] or "No notes yet.")}</p>{link(r["url"], "Open source")}</details>'
                        for i, r in enumerate(snap["resources"]))
    drawings = ''.join(drawing_html(d, i) for i, d in enumerate(snap["drawings"]))
    empty = '<p class="tw-empty">No Questions registered yet. Ask one from Scope; existing work is listed below.</p>'
    no_draw = '<p class="tw-empty" id="tw-no-drawings">No drawings yet. Add a drawing to explore an idea, workflow or folder map.</p>'
    form = """<details class="tw-resource-form" id="add-resource"><summary>+ Add resource</summary>
<form id="tw-add-resource"><label>Title<input name="title" required maxlength="300"></label>
<label>Source URL<input name="url" type="url" required placeholder="https://" maxlength="2000"></label>
<label>Related Questions<input name="questions" placeholder="Q01, Q02"></label>
<label>How it helps<textarea name="contribution" rows="2"></textarea></label>
<label>Notes<textarea name="notes" rows="3"></textarea></label><button type="submit">Save resource</button><p role="status"></p></form></details>"""
    studio = (f'<div id="tw-drawings">{drawings or no_draw}</div><form id="tw-add-drawing"><label>Drawing name<input name="name" required placeholder="Drawing 1" maxlength="80" pattern="[A-Za-z0-9_ -]+"></label><button type="submit">+ Add drawing</button><p role="status"></p></form>'
              + ('' if snap['studio_enabled'] else '<p class="tw-findings">This host has drawing routes disabled. Open this Block on the full Studio-enabled host to edit drawings.</p>'))
    bodies = {
        "block": block_html(snap),
        "register": register_html(snap),
        "related-paper": workspace_html(snap.get("workspace", []))
                         + f'<h3 class="tw-res-head">Related resources</h3><p class="tw-explain">Papers, repositories and other '
                           f'links this Block’s Questions use.</p>{resources or "<p class=tw-empty>No related resources yet.</p>"}{form}',
        "task": f'<p class="tw-explain">One Question per card · Logic │ Task Work │ Report</p>{"" if snap["questions"] else empty}{questions}',
        "studio": f'<p class="tw-explain">Draw freely. Each drawing opens independently; use Edit drawing to take the pen.</p>{studio}',
        "runs": f'<p class="tw-explain">{snap["totals"]["complete"]}/{snap["totals"]["runs"]} Task Runs complete. A running receipt is not a heartbeat.</p>{runs_html(snap)}',
        "tasks": f'<p class="tw-explain">Each Task Folder and what its audit found.</p>{tasks_html(snap)}',
        "progress": f'<p class="tw-explain">{len(snap["questions"])} Questions. Answers come from the Reports.</p>{progress or empty}'
                    f'<details class="tw-scope" id="block-scope"><summary>Block scope and close condition</summary><p>{e(snap["close"])}</p>{link(snap["source_url"], "Block source")}</details>',
    }
    rows = table_rows()
    panes = []
    for key, title, views in SPACES:
        tabs = ''.join(f'<button type="button" class="wtab{" on" if k == view else ""}" data-view="{k}">{t}</button>'
                       for k, t in views)
        sections = ''.join(f'<section class="view{" on" if k == view else ""}" data-panel="{k}">{bodies[k]}</section>'
                           for k, _ in views)
        panes.append(f'<section class="pane{" on" if key == space else ""}" data-space-pane="{key}"><div class="split">'
                     f'<div class="space-main"><div class="wtabs" role="tablist" aria-label="{title} Views">{tabs}</div>'
                     f'{sections}</div>{runs_panel(key, snap, rows)}</div></section>')
    space_row = ''.join(f'<button type="button" class="space{" on" if key == space else ""}" data-space="{key}" '
                        f'aria-selected="{str(key == space).lower()}">{title}</button>' for key, title, _ in SPACES)
    band = " · ".join([snap["block"], f'{snap["totals"]["jobs"]} Jobs', f'{snap["totals"]["tasks"]} Tasks',
                       f'{snap["totals"]["runs"]} Runs', f'{len(snap["questions"])} Questions'])
    config = json.dumps({"path": snap["path"], "studio": snap["studio_path"], "studioEnabled": snap["studio_enabled"],
                         "spaces": {key: [k for k, _ in views] for key, _, views in SPACES}},
                        ensure_ascii=False).replace('<', '\\u003c')
    from live.runs_panel import PANEL_CSS, PANEL_JS, SPLIT_CSS
    from live.work_items import WORK_ITEM_CSS
    css = ((HERE / 'assets/css/90-task-workbench.css').read_text() + '\n' + WORK_ITEM_CSS + PANEL_CSS + SPLIT_CSS
           + '.tw .split{--line:var(--line);--card:var(--card);--acc:var(--accent);--fg:var(--ink);--mut:var(--muted)}')
    js = (HERE / 'assets/js/90-task-workbench.js').read_text()
    content = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>📋 {e(snap['title'])}</title><link rel="icon" href="data:,"><style>{css}</style></head>
<body class="tw"><main id="task-workbench"><header><h1>📋 {e(snap['title'])}</h1><div class="mut"><a href="{e(snap['source_url'])}">board.md</a></div></header>
<div class="dataset" title="{e(snap['spine'])}">{e(band)}</div>
<nav class="spaces" aria-label="Spaces">{space_row}</nav>
<div class="tw-source-issues">{issues(snap['source_issues'])}</div>
{''.join(panes)}
<dialog id="tw-run-dialog" aria-label="Pop-out"><header><strong id="tw-run-title">Pop-out</strong><a id="tw-run-new" target="_blank" rel="noopener">Open in its own tab ↗</a><button type="button" id="tw-run-close" aria-label="Close pop-out">✕</button></header><iframe id="tw-run-frame" title="Pop-out"></iframe></dialog><p id="tw-status" role="status"></p></main><script type="application/json" id="tw-config">{config}</script><script>{js}</script><script>{PANEL_JS}</script></body></html>'''
    from live.workbench_guide import mount_guide
    return mount_guide(content, "task", {"path": snap["path"], "file": "board.md"},
                       "nav.spaces", "[data-space-pane],.tw-source-issues,#tw-status")
