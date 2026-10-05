"""Discovery Block Views, drawn as the Task and CoWork Workbenches are (one style, JL 261004).

The title alone in the header, the Block band, the Spaces Guide → Scope → Work → Check →
Delivery, every View opened by a heading and one lead line, each Space beside the shared Runs
panel. The stylesheet and script are the Task Workbench's own files.
"""
import html
import json
from pathlib import Path
from urllib.parse import urlencode

HERE = Path(__file__).parent
TASK = HERE.parent / "workbench-task"
TABLE = HERE.parents[1] / "skills" / "discovery" / "haipipe-workbench-discovery" / "ref" / "workbench-table.md"
ROUTE = "/_board/discovery-board"
LEADS = {
    "block": ("Block", "The state, spine, close condition, Jobs and Tasks, from board.md and the tree."),
    "register": ("Questions", "Each Question is one topic; its report answers it from the Block's Results."),
    "resources": ("Resources", "Outside links the Questions use."),
    "studio": ("RoadMap Draw", "The Block's drawings in studio/. Each opens on its own; a generated one is view only."),
    "papers": ("Papers", "Every Paper Run: the paper, what kind of source it is, how deeply it was read, and its status."),
    "tasks": ("Tasks", "Each Task Page: its Runs, its papers still to verify, and its synthesis."),
    "questions": ("Questions", "Each Question: the question, the Tasks and papers it uses, and its report."),
    "runs": ("Runs", "Every Run and its receipt status, blocked and failed first."),
    "citations": ("Citations", "Papers a person must still verify, or whose claim the reading did not support."),
    "progress": ("Reports", "Each report's answer status, findings and next action."),
    "delivery": ("Reports", "The answered reports, word for word."),
    "bib": ("BibTeX", "Every one-entry .bib the Block's Runs wrote, together."),
}
TONE = {"complete": "ok", "running": "acc", "waiting": "warn", "planned": "warn",
        "blocked": "bad", "failed": "bad", "missing": "bad"}


def e(value):
    return html.escape(str(value), quote=True)


def link(url, label):
    return f'<a href="{e(url)}" target="_blank" rel="noopener">{e(label)} ↗</a>' if url else ""


def pop(url, label, text=None, cls=""):
    """A link that opens in the shared pop-out, with an own-tab link in its header."""
    return (f'<a class="{e(cls)}" data-run-result="{e(label)}" href="{e(url)}" target="_blank" rel="noopener">'
            f'{e(label if text is None else text)}</a>') if url else e(label if text is None else text)


def issues(rows):
    return '<ul class="findings">' + ''.join(f'<li>{e(v)}</li>' for v in rows) + '</ul>' if rows else ""


def head(view, lead=None):
    title, text = LEADS[view]
    return f'<h2>{e(title)}</h2><p class=lead>{e(lead or text)}</p>'


def note(text):
    return f'<p class="note">{e(text)}</p>'


def spaces():
    return (("scope", "Scope", (("block", "Block"), ("register", "Questions"), ("resources", "Resources"),
                                ("studio", "RoadMap Draw"))),
            ("work", "Work", (("papers", "Papers"), ("tasks", "Tasks"), ("questions", "Questions"))),
            ("check", "Check", (("runs", "Runs"), ("citations", "Citations"), ("progress", "Reports"))),
            ("delivery", "Delivery", (("delivery", "Reports"), ("bib", "BibTeX"))))


def pill(status):
    return f'<span class="pill {TONE.get(status, "")}">{e(status)}</span>'


def block_html(snap):
    t = snap["totals"]
    jobs = ''.join(f'<li><span class="idtag">{e(j["name"])}</span> {e(j["title"])} '
                   f'<span class="mut">· {len(j["tasks"])} Tasks · {sum(len(x["papers"]) for x in j["tasks"])} papers</span></li>'
                   for j in snap["jobs"])
    rows = [("state", e(snap["state"] or "Not recorded.")), ("spine", e(snap["spine"] or "Not recorded.")),
            ("close condition", e(snap["close"] or "Not recorded.")),
            ("jobs", f'<ul class="plain">{jobs or "<li class=mut>no Jobs yet</li>"}</ul>'),
            ("reading", f'{t["papers"]} papers · {t["complete"]} Runs complete · {t["blocked"]} blocked · '
                        f'{t["needs_person"]} to verify · {t["bib"]} BibTeX entries'),
            ("described by", link(snap["source_url"], "board.md"))]
    return '<table class="rows inputs">' + ''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k, v in rows) + '</table>'


def register_html(snap):
    rows = ''.join(f'<tr><td><a href="#question-{e(q["id"])}" data-question="{e(q["id"])}">{e(q["id"])}</a></td>'
                   f'<td>{e(q.get("group") or "")}</td><td>{e(q["title"])}</td><td>{e(q["question"])}</td>'
                   f'<td class="num">{len(q["work"])}</td></tr>' for q in snap["questions"])
    return ('<div class="scroll"><table><tr><th>Id</th><th>Group</th><th>Topic</th><th>Question</th><th>Tasks</th></tr>'
            f'{rows}</table></div>' if rows else note("No Questions registered yet. Ask one from this Space's Runs panel."))


FORM = """<details class="draw" id="add-resource"><summary>+ Add resource</summary>
<form id="tw-add-resource"><label>Title<input name="title" required maxlength="300"></label>
<label>Source URL<input name="url" type="url" required placeholder="https://" maxlength="2000"></label>
<label>Related Questions<input name="questions" placeholder="Q01, Q02"></label>
<label>How it helps<textarea name="contribution" rows="2"></textarea></label>
<label>Notes<textarea name="notes" rows="3"></textarea></label><button type="submit">Save resource</button><p role="status"></p></form></details>"""


def resources_html(snap):
    links = ''.join(f'<details class="draw"><summary>{e(r["title"])} <span class="mut">'
                    f'{e(", ".join(r["questions"]) or "Block reference")}</span></summary><div class="dr-body">'
                    f'<p>{e(r["contribution"])}</p><p class="mut">{e(r["notes"] or "No notes yet.")}</p>'
                    f'<p>{link(r["url"], "Open source")}</p></div></details>' for r in snap["resources"])
    return (links or note("No related resources yet.")) + FORM


def drawing_html(drawing):
    url = '/_excalidraw/?' + urlencode({"board": drawing["path"]})
    if drawing.get("source"):
        stale = '❗ board.md changed after it was drawn: rerun ' if drawing.get("stale") else 'generated by '
        bar = (f'<span class="mut">{stale}<span class="mono">{e(drawing["source"])}</span>, never edited</span>'
               f'{link(url, "Open full screen")}')
    else:
        bar = (f'<span><button type="button" class="draw-edit">Edit drawing</button> '
               f'<span class="mono mut">{e(drawing["path"])}</span></span>{link(url + "&edit=1", "Open full screen")}')
    return (f'<details class="draw" data-board="{e(drawing["path"])}"><summary>{e(drawing["title"])}</summary>'
            f'<div class="st-bar">{bar}</div><iframe class="st-frame" title="{e(drawing["title"])}" '
            f'data-src="{e(url)}" referrerpolicy="no-referrer"></iframe></details>')


def studio_html(snap):
    drawings = ''.join(drawing_html(d) for d in snap["drawings"])
    empty = '<p class="note" id="tw-no-drawings">No drawings in studio/ yet.</p>'
    return (f'<div id="tw-drawings">{drawings or empty}</div><form id="tw-add-drawing"><label>Drawing name<input name="name" '
            'required placeholder="Drawing 1" maxlength="80" pattern="[A-Za-z0-9_ -]+"></label><button type="submit">'
            '+ Add drawing</button><p role="status"></p></form>'
            + ('' if snap["studio_enabled"] else note("This host has drawing routes disabled.")))


def paper_rows(papers, show_task=True):
    if not papers:
        return note("No papers here.")
    rows = []
    for p in papers:
        where = f'<td class="mono">{e(p["job"][:3])} {e(p["task_id"][-3:])}</td>' if show_task else ''
        subject = link(p["subject_url"], p["subject_kind"] or "source") if p["subject_url"] else e(p["subject_kind"])
        verify = f'<span class="pill {"warn" if p["needs_person"] else "ok"}">{e(p["verification"])}</span>'
        rows.append(f'<tr>{where}<td>{pop(p["card_url"], p["run"], p["id"], "idtag")}</td>'
                    f'<td>{pop(p["card_url"], p["run"], p["title"])}'
                    + (f'<div class="mut">{e(p["readout"][:220])}</div>' if p["readout"] else '') + '</td>'
                    f'<td>{subject}</td><td>{e(p["reading_depth"])}</td><td>{verify}</td><td>{pill(p["status"])}</td></tr>')
    heads = ('<th>Task</th>' if show_task else '') + '<th>Run</th><th>Paper</th><th>Source</th><th>Read</th><th>Verified</th><th>Status</th>'
    return f'<div class="scroll"><table><tr>{heads}</tr>{"".join(rows)}</table></div>'


def papers_html(snap):
    parts = []
    for job in snap["jobs"]:
        for task in job["tasks"]:
            if task["papers"]:
                parts.append(f'<h3><span class="idtag">{e(job["id"])} {e(task["name"])}</span> {e(task["title"])} '
                             f'<span class="mut">{len(task["papers"])} papers</span></h3>' + paper_rows(task["papers"], False))
    t = snap["totals"]
    lead = f'{t["papers"]} papers in {t["tasks"]} Tasks. Click a paper for its Result card.'
    return head("papers", lead) + (''.join(parts) or note("No Paper Runs yet. Find papers from this Space's Runs panel."))


def tasks_html(snap):
    rows = ''.join(
        f'<tr><td class="mono">{e(t["job"][:3])}</td><td>{pop(t["page_url"] or t["source_url"], t["name"], cls="idtag")}'
        f'<br><b>{e(t["title"])}</b></td><td>{e(t["discovery_type"])}</td>'
        f'<td class="num">{t["complete"]}/{t["total"]}</td><td class="num">{sum(p["needs_person"] for p in t["papers"])}</td>'
        f'<td>{" ".join(pop(s["url"], s["name"]) for s in t["synthesis"]) or "<span class=mut>none yet</span>"}</td>'
        f'<td>{e("; ".join(t["issues"][:2]) or "none")}</td></tr>' for t in snap["tasks"])
    return head("tasks") + ('<div class="scroll"><table><tr><th>Job</th><th>Task</th><th>Type</th><th>Runs complete</th>'
                            f'<th>To verify</th><th>Synthesis</th><th>Findings</th></tr>{rows}</table></div>'
                            if rows else note("No Task Pages yet."))


def qnumber(qid):
    return "Question " + str(int(qid[1:])) if qid[1:].isdigit() else qid


def question_row(q):
    more = [("What we expect", q["hypothesis"]), ("What would answer it", q["acceptance"])]
    dl = ''.join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k, v in more if v)
    if q["issues"]:
        dl += f'<dt>Register findings</dt><dd>{issues(q["issues"])}</dd>'
    logic = (f'<div class="hl-l"><div class="q-top"><span class="kind">{e(qnumber(q["id"]))}</span></div>'
             f'<div class="q-title"><b class="q-name">{e(q["title"])}</b></div>'
             + (f'<div class="q-text">{e(q["question"])}</div>' if q["question"] != q["title"] else '')
             + (f'<div class="q-aim"><b>Aim</b> {e(q["aim"])}</div>' if q.get("aim") else '')
             + (f'<details class="q-more"><summary>More</summary><dl>{dl}</dl></details>' if dl else '') + '</div>')
    work = ''.join(f'<li>{pop(w["task"]["page_url"] or w["task"]["source_url"], w["task"]["name"], cls="idtag")} '
                   f'<span class="mut">{len(w["task"]["papers"])} papers · {w["task"]["complete"]}/{w["task"]["total"]} Runs</span></li>'
                   for w in q["work"])
    work_cell = (f'<details class="wk" open><summary><span class="kind">Work</span></summary><ul class="plain">{work}</ul></details>'
                 if work else '<p class="wk-none">No Task linked yet.</p>')
    r = q["report"]
    report = '<p class="rp-label"><span class="kind">Report</span></p>' + (
        f'<p class="rp-title">{pop(r["url"] or r["source_url"], r["title"] or r["path"])}</p>'
        + (f'<p class="rp-text">{e(r["answer"])}</p>' if r["answer"] else '') + f'<p class="rp-tags">{e(r["status"])}</p>'
        if r["present"] else '<p class="wk-none">No report yet</p>')
    return (f'<div class="hl-row" id="question-{e(q["id"])}" data-key="{e(q["id"])}" data-label="{e(q["id"])} · '
            f'{e(q["title"])}">{logic}<div class="hl-r">{work_cell}</div><div class="hl-p">{report}</div></div>')


def questions_html(snap):
    if not snap["questions"]:
        return head("questions") + note("No Questions registered yet. Ask one from Scope.")
    rows = ''.join(question_row(q) for q in snap["questions"])
    return (head("questions") + '<div class="hl-wrap"><div class="hl"><div class="hl-head"><span>Logic · the question</span>'
            f'<span>Work · the Tasks and their papers</span><span>Report · what it says</span></div>{rows}</div></div>')


def runs_html(snap):
    order = {"failed": 0, "blocked": 1, "missing": 2, "running": 3, "waiting": 4, "planned": 5, "complete": 6}
    runs = sorted(snap["runs"], key=lambda r: order.get(r["status"], 9))
    rows = ''.join(f'<tr><td class="mono">{e(r["job"][:3])} {e(r["task_id"][-3:])}</td>'
                   f'<td>{pop(r["result_url"], r["name"], cls="idtag")}</td><td>{pill(r["status"])}</td>'
                   f'<td>{e(r["failure"] or "; ".join(r["issues"][:1]))}</td></tr>' for r in runs)
    t = snap["totals"]
    return head("runs", f'{t["complete"]}/{len(snap["runs"])} Runs complete; {t["blocked"]} blocked or failed.') + (
        '<div class="scroll"><table><tr><th>Task</th><th>Run</th><th>Status</th><th>Why</th></tr>'
        f'{rows}</table></div>' if rows else note("No Runs yet."))


def citations_html(snap):
    todo = [p for p in snap["papers"] if p["needs_person"]]
    return head("citations", f'{len(todo)} of {len(snap["papers"])} papers need a person.') + paper_rows(todo)


def progress_html(snap):
    cards = []
    for q in snap["questions"]:
        r = q["report"]
        cards.append(f'<article class="card"><h3><a href="#question-{e(q["id"])}" data-question="{e(q["id"])}">'
                     f'{e(q["id"])} · {e(q["title"])}</a><span class="pill acc">{e(r["status"].capitalize())}</span></h3>'
                     f'<p>{e(r["answer"] or "No answer yet.")}</p>'
                     f'<p><strong>Next:</strong> {e(r["next"] or "Record the next action in the Report.")}</p>'
                     + issues(q["issues"] + r["issues"]) + f'<p class="links">{link(r["url"], "Report")}</p></article>')
    return head("progress") + (''.join(cards) or note("No Questions registered yet."))


def delivery_html(snap):
    cards = []
    for q in snap["questions"]:
        r = q["report"]
        if r["present"] and r["status"] == "answered":
            cards.append(f'<article class="card"><h3>{pop(r["url"], r["title"] or r["path"])} <span class="mut">{e(q["id"])}</span></h3>'
                         + ''.join(f'<p>{e(p)}</p>' for p in r.get("opening", []))
                         + (('<h4>Answer</h4>' + ''.join(f'<p>{e(p)}</p>' for p in r["answer_text"])) if r.get("answer_text") else '')
                         + '</article>')
    return head("delivery") + (''.join(cards) or note("No Question is answered yet."))


def bib_html(snap):
    entries = [p for p in snap["papers"] if p["bib"]]
    if not entries:
        return head("bib") + note("No Run has written a .bib yet.")
    files = ''.join(f'<li>{pop(p["bib_url"], p["run"] + ".bib")}</li>' for p in entries)
    text = "\n\n".join(p["bib"].strip() for p in entries)
    return (head("bib", f'{len(entries)} entries from {len(snap["papers"])} papers.') + f'<ul class="plain">{files}</ul>'
            f'<pre class="cw-text">{e(text)}</pre>')


def table_rows():
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
    """The shared Runs panel for one Space: its run types from the Workbench Table, each with its
    agent, skill and a prompt to copy. Work's "Read a paper" lists every Paper Run with its status."""
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
        about = " for {target}" if space == "work" else ""
        kinds.append({"label": r["Run type"], "pattern": "", "views": "",
                      "skills": [r["Skill"]] if r["Skill"] not in ("", "none") else [],
                      "prompt": f'Run with {r["Agent"]}: {r["Run type"]}{about} in the Discovery Block {block} '
                                f'({r["Space"]} › {r["View"]}), following {r["Skill"]}.{signs}'})
        if r["Run type"] == "Read a paper":
            buckets.append([{"run_id": f'{run["job"][:3]}·{run["task_id"][-3:]}·{run["name"]}', "status": run["status"],
                             "target": run["task_title"], "_keys": " ".join(serves.get(run["task_id"], [])),
                             "ticket": run["ticket_url"].lstrip("/"), "result": run["receipt_url"].lstrip("/"),
                             "_display": f'{run["job"][:3]} {run["task_id"][-3:]} {run["name"]}'} for run in snap["runs"]])
        else:
            buckets.append([])
    if not kinds:
        return ""
    fill = lambda row: {"ticket": row.get("ticket") or "<job>/<task>/runs/<run>.sh"}
    return panel_markup(space, kinds, buckets, base=HERE, fill=fill, whole=f"the Block {snap['block']}", folded=True)


def _assets():
    from live.runs_panel import PANEL_CSS, PANEL_JS, SPLIT_CSS
    css = ((TASK / 'assets/css/90-task-workbench.css').read_text(encoding="utf-8") + '\n' + PANEL_CSS + SPLIT_CSS
           + '.split{--card:var(--bg)}.cw-text{white-space:pre-wrap;font:13px/1.5 ui-monospace,monospace;'
             'background:var(--bg,#f6f8fa);padding:12px;border-radius:8px;max-height:640px;overflow:auto}')
    return css, (TASK / 'assets/js/90-task-workbench.js').read_text(encoding="utf-8"), PANEL_JS


def render_block(snap, view="papers"):
    space_list = spaces()
    space_of = {key: space for space, _, views in space_list for key, _ in views}
    aliases = {"scope": "block", "work": "papers", "check": "runs", "delivery": "delivery", "roadmap": "studio"}
    view = view if view in space_of else aliases.get(view, "papers")
    space = space_of[view]
    bodies = {"block": head("block") + block_html(snap), "register": head("register") + register_html(snap),
              "resources": head("resources") + resources_html(snap), "studio": head("studio") + studio_html(snap),
              "papers": papers_html(snap), "tasks": tasks_html(snap), "questions": questions_html(snap),
              "runs": runs_html(snap), "citations": citations_html(snap), "progress": progress_html(snap),
              "delivery": delivery_html(snap), "bib": bib_html(snap)}
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
    t = snap["totals"]
    band = " · ".join(x for x in [snap["block"], snap["state"], f'{t["jobs"]} Jobs', f'{t["tasks"]} Tasks',
                                  f'{t["papers"]} papers', f'{t["blocked"]} blocked', f'{t["needs_person"]} to verify',
                                  f'{len(snap["questions"])} Questions'] if x)
    config = json.dumps({"path": snap["path"], "studio": snap["studio_path"], "studioEnabled": snap["studio_enabled"],
                         "home": "work", "route": ROUTE,
                         "spaces": {key: [k for k, _ in views] for key, _, views in space_list}, "aliases": aliases},
                        ensure_ascii=False).replace('<', '\\u003c')
    css, js, panel_js = _assets()
    content = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>🔭 Discovery · {e(snap['title'])}</title><link rel="icon" href="data:,"><style>{css}</style></head>
<body class="tw"><main id="task-workbench"><header><h1>🔭 Discovery · {e(snap['title'])}</h1></header>
<div class="dataset" title="{e(snap['spine'])}">{e(band)}</div>
<nav class="spaces" aria-label="Spaces">{space_row}</nav>
<div class="tw-source-issues">{issues(snap['source_issues'])}</div>
{''.join(panes)}
<dialog id="tw-run-dialog" aria-label="Pop-out"><div class="pop-bar"><span class="pop-title" id="tw-run-title">Pop-out</span><a class="pop-new" id="tw-run-new" target="_blank" rel="noopener">Open in its own tab ↗</a><button type="button" class="pop-x" id="tw-run-close" aria-label="Close">×</button></div><iframe class="pop-frame" id="tw-run-frame" title="Pop-out"></iframe></dialog><p id="tw-status" role="status"></p></main><script type="application/json" id="tw-config">{config}</script><script>{js}</script><script>{panel_js}</script></body></html>'''
    from live.workbench_guide import mount_guide
    return mount_guide(content, "discovery", {"path": snap["path"], "file": "board.md"},
                       "nav.spaces", "[data-space-pane],.tw-source-issues,#tw-status")


def render_report(report, board, root, board_path):
    """A Question's report Page, through the Task Workbench's report reader, with a Discovery back link."""
    from live.task_views import render_report as task_report
    page = task_report(report, board, root, board_path)
    return page.replace('/_board/task-board?', ROUTE + '?').replace('← Task</a>', '← Discovery</a>')


def render_projects(groups, where="", missing=""):
    """Every Discovery Block of a Project (or under the root): state, Jobs, Tasks, papers."""
    css, _, _ = _assets()
    parts = []
    for group in groups:
        rows = ''.join(f'<tr><td><a href="{e(b["url"])}"><span class="idtag">{e(b["block"])}</span></a><br>'
                       f'<b>{e(b["title"])}</b></td><td>{e(b["state"])}</td><td>{e(b["spine"])}</td>'
                       f'<td class="num">{b["jobs"]}</td><td class="num">{b["tasks"]}</td><td class="num">{b["papers"]}</td></tr>'
                       for b in group["blocks"])
        parts.append(f'<h2>{e(group["project"])} <span class="mut mono">{e(group["folder"])}</span></h2>'
                     '<div class="scroll"><table><tr><th>Block</th><th>State</th><th>Spine</th><th>Jobs</th><th>Tasks</th>'
                     f'<th>Papers</th></tr>{rows}</table></div>')
    lead = f'<p class="note">No Discovery Block at {e(missing)}.</p>' if missing else ''
    body = ''.join(parts) or '<p class="note">No Discovery Blocks (board-kind: discovery-block) under this root.</p>'
    title = "Discovery · " + (where or "every Project")
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width,initial-scale=1"><title>🔭 {e(title)}</title><link rel="icon" href="data:,">'
            f'<style>{css}</style></head><body class="tw"><main id="discovery-projects"><header><h1>🔭 {e(title)}</h1></header>'
            f'{lead}{body}</main></body></html>')
