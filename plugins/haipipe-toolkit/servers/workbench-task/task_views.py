"""Question-led Task Views using native report Pages and Excalidraw files."""
import html
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlencode, quote, urljoin, urlsplit

HERE = Path(__file__).parent
VIEWS = (("task", "Task"), ("studio", "Roadmap Studio"),
         ("related-paper", "Related Paper"), ("progress", "Progress"))


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


def report_html(report):
    if not report["present"]:
        return '<p class="tw-muted">No Report yet.</p>' + issues(report["issues"])
    evidence = ''.join(f'<li>{link(r["url"], r["title"]) or e(r["title"] + (" · see related Work" if r["mtime"] is not None else " · unavailable"))}</li>' for r in report["evidence"])
    return (f'<p class="tw-answer-state">{e(report["status"].capitalize())}</p>'
            f'<p>{e(report["answer"] or "No answer recorded.")}</p>'
            f'<h4>Evidence</h4><ul>{evidence}</ul>'
            + ('' if evidence else f'<p>{e(report["evidence_text"] or "No evidence linked yet.")}</p>')
            + f'<h4>Limits</h4><p>{e(report["limits"] or "Not recorded.")}</p>'
            f'<h4>Next</h4><p>{e(report["next"] or "Not recorded.")}</p>'
            + issues(report["issues"])
            + f'<div class="tw-links">{link(report["url"], "Open full report")}{link(report["source_url"], "Source")}</div>'
            f'<p class="tw-muted">Page: {e(report["page_state"])} · answer status is declared</p>'
            f'<code>{e(report["path"])}</code>')


def task_work(task, key, role="", stage="", also=()):
    """Paper's Work line, with this family's native Task and Run records."""
    from live.work_items import work_item
    runs = ''.join(
        f'<a class="bj-run" data-run-result="{e(run["name"])}" href="{e(run["result_url"])}" '
        f'target="_blank" rel="noopener"><span class="idtag">{e(run["name"])}</span> '
        f'<span class="mut">{e(run["status"])}'
        + (' · Page Run' if run['lane'] == 'page' else ' · no Ticket' if not run['allocated'] else '')
        + '</span></a>' for run in task['runs'])
    run_count = len(task['runs'])
    run_states = ' · '.join(f'{count} {state}' for state, count in Counter(r['status'] for r in task['runs']).items())
    size = f'1 task · {run_count} run' + ('' if run_count == 1 else 's')
    tags = (f'<span class="lw-also">also for {e(", ".join(also))}</span>' if also else '')
    tags += f'<span class="lw-size">{e(size)}</span>'
    folder_name = lambda name: e(name[4:].replace('_', ' '))
    folders = (f'<div class="bj-home mut">tasks/</div>'
               f'<div class="bj-b"><span class="idtag">{e(task["block"][:3])}</span> <b>{folder_name(task["block"])}</b></div>'
               f'<div class="bj-j"><span class="idtag">{e(task["job"][:3])}</span> {folder_name(task["job"])}</div>')
    task_line = f'<span class="idtag">{e(task["name"][:3])}</span> {folder_name(task["name"])}'
    if runs:
        folders += (f'<details class="bj-tr" id="{e(key + "-runs")}"><summary class="bj-t">{task_line}'
                    f'<span class="bj-rs">{run_count} run{("" if run_count == 1 else "s")} · {e(run_states)}</span></summary>'
                    f'<div class="bj-runs">{runs}</div></details>')
    else:
        folders += f'<div class="bj-t">{task_line} <span class="bj-rn mut">no runs yet</span></div>'
    # Technical navigation stays behind its own disclosure, as on Paper's Work.
    folders += (f'<details class="tw-work-details" id="{e(key + "-details")}"><summary>Task details</summary>'
                f'<code>{e(task["job"] + "/" + task["name"])}</code>'
                f'<div class="tw-links">{link(task["page_url"], "Task Page")}{link(task["folder_url"], "Folder")}'
                f'{link(task["plan_url"], "Plan")}{link(task["report_url"], "Execution report")}</div>'
                f'<p>Page: {e(task["page_state"])} · {task["reading"]["signed"]}/{task["reading"]["total"]} readings signed</p>'
                + issues(task["issues"]) + '</details>')
    return work_item(stage or task['kind'].capitalize(), task['title'], role or task['purpose'],
                     tags, folders, key=key, element_id=key)


def work_html(question):
    if not question['work']:
        return '<p class="tw-muted">No execution linked. Reasoning and existing evidence can still answer this Question.</p>'
    # The register's order is the authored workflow, independent of folder sorting.
    return ''.join(task_work(item['task'], question['id'] + '-' + item['task']['id'],
                             item['role'], item['stage'], item['also']) for item in question['work'])


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
            f'<small>{e(r["status"].capitalize())} · {e(r["answer"] or "No answer yet")}</small></summary>'
            '<div class="tw-columns">'
            f'<section><h3>Logic</h3><h4>Hypothesis</h4><p>{e(q["hypothesis"] or "Not recorded.")}</p>'
            f'<h4>Acceptance</h4><p>{e(q["acceptance"] or "Not recorded.")}</p>' + issues(q["issues"]) + '</section>'
            f'<section class="tw-work-column"><h3>Work</h3>{work_html(q)}</section>'
            f'<section><h3>Report</h3>{report_html(r)}</section></div>'
            f'<div class="tw-card-actions"><button type="button" data-copy="{e(context(q))}">Copy context to session</button></div></details>')


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
            + f'<div class="tw-links">{link(report["url"], "Report")}<button type="button" data-copy="{e(context(q))}">Copy context to session</button></div></article>')


def drawing_html(drawing, index):
    url = '/_excalidraw/?' + urlencode({"board": drawing["path"]})
    return (f'<details class="tw-drawing" id="drawing-{index}" data-board="{e(drawing["path"])}">'
            f'<summary>{e(drawing["title"])}</summary><div class="tw-drawing-body">'
            f'<div class="tw-links"><button type="button" data-edit-drawing>Edit drawing</button>'
            f'{link(url + "&edit=1", "Open full screen")}<code>{e(drawing["path"])}</code></div>'
            f'<iframe title="{e(drawing["title"])}" data-src="{e(url)}" referrerpolicy="no-referrer"></iframe>'
            '</div></details>')


def render(snap, view="task"):
    view = view if view in dict(VIEWS) else "task"
    questions = ''.join(question_html(q) for q in snap["questions"])
    progress = ''.join(progress_html(q) for q in snap["questions"])
    unassigned = ''.join(task_work(t, "unassigned-" + t["id"]) for t in snap["unassigned"])
    if unassigned:
        questions += '<details class="tw-unassigned" id="unassigned"><summary>Not under a Question · ' + str(len(snap["unassigned"])) + ' Tasks</summary>' + unassigned + '</details>'
    resources = ''.join(f'<details class="tw-resource" id="resource-{i}" data-search="{e(str(r).lower())}">'
                        f'<summary><strong>{e(r["title"])}</strong><span>{e(r["contribution"])}</span>'
                        f'<small>{e(", ".join(r["questions"]) or "Block reference")}</small></summary>'
                        f'<p>{e(r["notes"] or "No notes yet.")}</p>{link(r["url"], "Open source")}</details>'
                        for i, r in enumerate(snap["resources"]))
    drawings = ''.join(drawing_html(d, i) for i, d in enumerate(snap["drawings"]))
    empty = '<p class="tw-empty">No Questions registered yet. Add a Question through the Task skill; existing work is available below.</p>'
    no_draw = '<p class="tw-empty" id="tw-no-drawings">No drawings yet. Add a drawing to explore an idea, workflow or folder map.</p>'
    tabs = ''.join(f'<a data-view="{key}" aria-current="{str(key == view).lower()}" href="?{e(urlencode({"path": snap["path"], "view": key}))}">{title}</a>' for key, title in VIEWS)
    form = '''<details class="tw-resource-form" id="add-resource"><summary>+ Add resource</summary>
<form id="tw-add-resource"><label>Title<input name="title" required maxlength="300"></label>
<label>Source URL<input name="url" type="url" required placeholder="https://" maxlength="2000"></label>
<label>Related Questions<input name="questions" placeholder="Q01, Q02"></label>
<label>How it helps<textarea name="contribution" rows="2"></textarea></label>
<label>Notes<textarea name="notes" rows="3"></textarea></label><button type="submit">Save resource</button><p role="status"></p></form></details>'''
    config = json.dumps({"path": snap["path"], "studio": snap["studio_path"], "studioEnabled": snap["studio_enabled"]}, ensure_ascii=False).replace('<', '\\u003c')
    from live.work_items import WORK_ITEM_CSS
    css = (HERE / 'assets/css/90-task-workbench.css').read_text() + '\n' + WORK_ITEM_CSS
    js = (HERE / 'assets/js/90-task-workbench.js').read_text()
    content = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Task · {e(snap['title'])}</title><style>{css}</style></head>
<body class="tw"><main id="task-workbench"><header><div class="tw-topline"><a href="/">SPACE Home</a><span>{e(snap['project'])} / tasks / {e(snap['block'])}</span><span class="tw-live">Read {e(snap['updated_at'])}</span></div>
<div class="tw-heading"><div><h1>{e(snap['title'])}</h1><p class="tw-spine">{e(snap['spine'])}</p></div><div class="tw-refresh"><button type="button" id="tw-refresh">Refresh</button><label><input type="checkbox" id="tw-auto"> Every 30s</label></div></div></header>
<nav class="tw-nav" aria-label="Spaces"><span>Space</span><button type="button" aria-selected="true" id="tw-task-space">Task</button></nav>
<nav class="tw-views" aria-label="Task Views"><span>View</span>{tabs}</nav>
<div class="tw-toolbar"><label class="tw-search">Search<input id="tw-search" type="search" placeholder="Question, answer or resource…"></label></div>
<div class="tw-source-issues">{issues(snap['source_issues'])}</div>
<section data-panel="task" {'hidden' if view != 'task' else ''}><p class="tw-explain">One Question per card · Logic | Work | Report</p>{'' if snap['questions'] else empty}{questions}</section>
<section data-panel="studio" {'hidden' if view != 'studio' else ''}><p class="tw-explain">Draw freely. Each drawing opens independently; use Edit drawing to take the pen.</p>
<div id="tw-drawings">{drawings or no_draw}</div><form id="tw-add-drawing"><label>Drawing name<input name="name" required placeholder="Drawing 1" maxlength="80" pattern="[A-Za-z0-9_ -]+"></label><button type="submit">+ Add drawing</button><p role="status"></p></form>
{'' if snap['studio_enabled'] else '<p class="tw-findings">This host has drawing routes disabled. Open this Block on the full Studio-enabled host to edit drawings.</p>'}</section>
<section data-panel="related-paper" {'hidden' if view != 'related-paper' else ''}><p class="tw-explain">Papers, repositories and other resources that help answer this Block’s Questions.</p>{resources or '<p class="tw-empty">No related resources yet.</p>'}{form}</section>
<section data-panel="progress" {'hidden' if view != 'progress' else ''}><p class="tw-explain">{len(snap['questions'])} Questions · {snap['totals']['complete']}/{snap['totals']['runs']} Task Runs complete. Answers come from the Reports.</p>{progress or empty}
<details class="tw-scope" id="block-scope"><summary>Block scope and close condition</summary><p>{e(snap['close'])}</p>{link(snap['source_url'], 'Block source')}</details></section>
<dialog id="tw-run-dialog" aria-label="Run results"><header><strong id="tw-run-title">Run results</strong><a id="tw-run-new" target="_blank" rel="noopener">Open in its own tab ↗</a><button type="button" id="tw-run-close" aria-label="Close Run results">✕</button></header><iframe id="tw-run-frame" title="Run results"></iframe></dialog><p class="tw-empty" id="tw-no-match" hidden>No matches.</p><p id="tw-status" role="status"></p></main><script type="application/json" id="tw-config">{config}</script><script>{js}</script></body></html>'''
    from live.workbench_guide import mount_guide
    return mount_guide(content, "task", {"path": snap["path"], "file": "board.md"},
                       ".tw-nav", ".tw-views,.tw-toolbar,[data-panel],#tw-no-match,.tw-source-issues,#tw-status")
