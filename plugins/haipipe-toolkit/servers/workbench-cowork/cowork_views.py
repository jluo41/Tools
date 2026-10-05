"""CoWork Block Views, drawn as the Task Workbench is (servers/workbench-task/task_views.py).

The title alone in the header, the Block band, the Spaces Guide → Scope → Work → Check →
Delivery, every View opened by a heading and one lead line, each Space beside the shared Runs
panel. The stylesheet and script are the Task Workbench's own files, so the two stay alike.
"""
import html
import json
from pathlib import Path
from urllib.parse import urlencode

HERE = Path(__file__).parent
TASK = HERE.parent / "workbench-task"
TABLE = HERE.parents[1] / "skills" / "cowork" / "haipipe-workbench-cowork" / "ref" / "workbench-table.md"
ROUTE = "/_board/cowork-board"
LEADS = {
    "block": ("Block", "The state, spine, close condition and status, from board.md."),
    "people": ("People", "Who to ask for help in this Block: its j00_people Job, as written."),
    "resources": ("Resources", "Outside links the Questions use, each Job's design notes and materials, then OneDrive."),
    "studio": ("RoadMap Draw", "The Block's drawings in studio/. Each opens on its own; a generated one is view only."),
    "jobs": ("Jobs", "Each line of work: who has the next move, since when, the next step, and its files."),
    "questions": ("Questions", "Each Question is one topic: the question, the Block files it uses, and its report."),
    "emails": ("Emails", "Every thread and draft in emails/, newest first. Only the person sends."),
    "meetings": ("Meetings", "Every meeting note in meetings/, newest first."),
    "waiting": ("Waiting on", "Open Jobs whose next move is someone else's, longest wait first."),
    "drafts": ("Drafts", "Email drafts not sent yet, and each Job's checklist steps still open."),
    "progress": ("Reports", "Each report's answer status, findings and next action."),
    "delivery": ("Reports", "The answered reports, word for word, with the files they cite."),
    "done": ("Done jobs", "Jobs whose state is done."),
}


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
    return (("scope", "Scope", (("block", "Block"), ("people", "People"), ("resources", "Resources"),
                                ("studio", "RoadMap Draw"))),
            ("work", "Work", (("jobs", "Jobs"), ("questions", "Questions"), ("emails", "Emails"),
                              ("meetings", "Meetings"))),
            ("check", "Check", (("waiting", "Waiting on"), ("drafts", "Drafts"), ("progress", "Reports"))),
            ("delivery", "Delivery", (("delivery", "Reports"), ("done", "Done jobs"))))


def wait_text(job):
    days = job["days"]
    return "" if days is None else ("today" if days == 0 else f'{days} day{"" if days == 1 else "s"}')


def block_html(snap):
    open_rows = [j for j in snap["jobs"] if j["open"]]
    job_list = ''.join(f'<li><span class="idtag">{e(j["name"])}</span> {e(j["state"])} '
                       f'<span class="mut">{e(j["title"])}</span></li>' for j in snap["jobs"])
    rows = [("state", e(snap["state"] or "Not recorded.")), ("spine", e(snap["spine"] or "Not recorded.")),
            ("close condition", e(snap["close"] or "Not recorded.")), ("status", e(snap["status"] or "Not recorded.")),
            ("waits for", e(snap["waits_for"] or "nothing")),
            ("jobs", f'<ul class="plain">{job_list or "<li class=mut>no jobs yet</li>"}</ul>'),
            ("work", f'{len(open_rows)} open jobs · {len(snap["questions"])} Questions · '
                     f'{len(snap["emails"])} emails · {len(snap["meetings"])} meeting notes'),
            ("described by", link(snap["source_url"], "board.md") + ' <span class="mut">· the header, the text and the '
                             'Questions register; each Job\'s state is in its own page</span>')]
    return '<table class="rows inputs">' + ''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k, v in rows) + '</table>'


def people_html(snap):
    if not snap["people"].strip():
        return note("No j00_people Job in this Block yet.")
    return f'<p>{pop(snap["people_url"], "j00_people.md")}</p><pre class="cw-text">{e(snap["people"])}</pre>'


def file_list(title, rows):
    items = ''.join(f'<li>{pop(r["url"], r["name"], cls="idtag") if r["url"] else e(r["name"])}</li>' for r in rows)
    return (f'<details class="draw ws" open><summary>{e(title)} <span class="mut">{len(rows)} files</span></summary>'
            f'<ul class="ws-files">{items or "<li class=mut>empty</li>"}</ul></details>')


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
    return (f'<h3>Related resources</h3>{links or note("No related resources yet.")}{FORM}'
            '<h3>Job files</h3>' + (''.join(file_list(f'{j["name"]}/{name}/', j[name]) for j in snap["jobs"]
                                            for name in ("design", "materials") if j[name])
                                    or note("No Job has design notes or materials yet."))
            + onedrive_html(snap["onedrive_folders"]))


def onedrive_html(folders):
    """The shared drive (the board.md `onedrive:` line): named, not linked; open them in OneDrive."""
    if not folders:
        return ''
    parts = []
    for f in folders:
        items = ''.join(f'<li><span class="idtag">{e(n)}</span></li>' for n in f["files"])
        state = "not found on this computer" if f["missing"] else f'{len(f["files"])} files'
        parts.append(f'<details class="draw ws"><summary><code>{e(f["path"])}</code> <span class="mut">{state}</span>'
                     f'</summary><ul class="ws-files">{items or "<li class=mut>empty</li>"}</ul></details>')
    return ('<h3>OneDrive · shared drive</h3><p class="note">Co-edited documents live in the study\'s OneDrive; '
            'they are listed here by name. Open them in OneDrive.</p>' + ''.join(parts))


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


def job_table(rows, done=False):
    if not rows:
        return note("No done jobs." if done else "No jobs here.")
    body = ''.join(
        f'<tr><td>{pop(j["page_url"], j["name"], cls="idtag")}<br><b>{e(j["title"])}</b></td>'
        f'<td>{e(j["state"])}</td>'
        f'<td><span class="pill {"acc" if j["waiting"].lower() == "us" else "warn"}">{e(j["waiting"])}</span></td>'
        f'<td class="mono">{e(j["since"])}</td><td class="num">{e(wait_text(j))}</td><td>{e(j["next"])}</td>'
        f'<td>{link(j["url"], j["ticket"]) if j["url"] else e(j["ticket"])}</td></tr>'
        for j in rows)
    return ('<div class="scroll"><table><tr><th>Job</th><th>State</th><th>Waiting on</th><th>Since</th><th>Waited</th>'
            f'<th>Next step</th><th>Ticket</th></tr>{body}</table></div>')


def steps_html(steps, only_open=False):
    rows = [s for s in steps if not (only_open and s["done"])]
    if not rows:
        return note("No open checklist steps." if only_open else "No checklist steps.")
    return '<ul class="cw-steps">' + ''.join(
        f'<li class="{"done" if s["done"] else "open"}">{"✅" if s["done"] else "⬜"} '
        f'<b>{e(s["number"] + "." if s["number"] else "")}</b> {e(s["text"])}'
        + (f' <span class="mono mut">{e(s["job"])}</span>' if only_open and s.get("job") else '') + '</li>' for s in rows) + '</ul>'


def job_detail(j):
    parts = [pop(j["page_url"], j["name"] + ".md", "job page"), pop(j["timeline_url"], "Timeline.md"),
             pop(j["checklist_url"], "CHECKLIST.md")]
    links = ' · '.join(x for x, u in zip(parts, (j["page_url"], j["timeline_url"], j["checklist_url"])) if u)
    counts = " · ".join(f'{len(j[k])} {k}' for k in ("emails", "meetings", "design", "materials") if j[k])
    lists = ''.join(f'<li><span class="mut">{e(k)}/</span> ' + ', '.join(pop(x["url"], x.get("title") or x["name"], x["name"])
                                                                       for x in j[k]) + '</li>'
                    for k in ("emails", "meetings", "design", "materials") if j[k])
    return (f'<details class="draw ws"><summary><span class="idtag">{e(j["name"])}</span> {e(j["title"])} '
            f'<span class="mut">{e(counts or "only its page")}</span></summary><div class="dr-body"><p>{links}</p>'
            + (f'<ul class="plain">{lists}</ul>' if lists else '')
            + ('<h4>Steps</h4>' + steps_html(j["steps"]) if j["steps"] else '') + '</div></details>')


def jobs_html(snap):
    open_rows = [j for j in snap["jobs"] if j["open"]]
    return (head("jobs") + job_table(open_rows) + '<h3>Each Job</h3>'
            + (''.join(job_detail(j) for j in snap["jobs"]) or note("No jobs yet.")))


def work_cell(question):
    if not question["work"]:
        return '<p class="wk-none">No Block file linked; reasoning or existing evidence can answer it.</p>'
    items = ''.join(f'<li>{pop(w["url"], w["path"], cls="idtag")}'
                    + (f' <span class="mut">{e(w["role"])}</span>' if w["role"] else '') + '</li>'
                    for w in question["work"])
    return f'<details class="wk" open><summary><span class="kind">Work</span></summary><ul class="plain">{items}</ul></details>'


def report_cell(question):
    report = question["report"]
    label = '<p class="rp-label"><span class="kind">Report</span></p>'
    if not report["present"]:
        return label + '<p class="wk-none">No report yet</p>'
    thumbs = ''.join(
        f'<a class="rp-thumb" data-run-result="Drawing · {e(t["title"])}" href="{e(t["url"])}" target="_blank" '
        f'rel="noopener" title="Open {e(t["title"])}">'
        + (f'<img src="{e(t["png"])}" alt="{e(t["title"])}" loading="lazy">' if t["png"] else e(t["title"]) + ' ↗')
        + '</a>' for t in report.get("thumbs", []))
    # Videos from the report's Evidence play here, one strip that scrolls sideways; #t=0.5 makes
    # every browser show a frame before play (Safari shows none with preload=metadata alone).
    videos = ''.join((f'<figure class="rp-video rp-yt"><iframe src="{e(v["embed"])}" title="{e(v["title"])}" loading="lazy" '
                      'allowfullscreen allow="encrypted-media; picture-in-picture; fullscreen" '
                      'referrerpolicy="strict-origin-when-cross-origin"></iframe>' if v.get("embed") else
                      f'<figure class="rp-video"><video controls preload="metadata" playsinline src="{e(v["url"])}#t=0.5" '
                      f'title="{e(v["title"])}"></video>') + f'<figcaption>{e(v["title"])}</figcaption></figure>'
                     for v in report.get("videos", []))
    videos = f'<div class="rp-videos">{videos}</div>' if videos else ''
    return (label + f'<p class="rp-title">{pop(report["url"] or report["source_url"], report["title"] or report["path"])}</p>'
            + (f'<p class="rp-text">{e(report["answer"])}</p>' if report["answer"] else '')
            + thumbs + videos + f'<p class="rp-tags">{e(report["status"])}</p>')


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
             + (f'<div class="q-aim"><b>Aim</b> {e(q["aim"])}</div>' if q["aim"] else '')
             + (f'<details class="q-more"><summary>More</summary><dl>{dl}</dl></details>' if dl else '') + '</div>')
    return (f'<div class="hl-row" id="question-{e(q["id"])}" data-key="{e(q["id"])}" data-label="{e(q["id"])} · '
            f'{e(q["title"])}">{logic}<div class="hl-r">{work_cell(q)}</div><div class="hl-p">{report_cell(q)}</div></div>')


def questions_html(snap):
    if not snap["questions"]:
        return head("questions") + note("No Questions registered yet. Ask one from this Space's Runs panel.")
    rows = ''.join(question_row(q) for q in snap["questions"])
    return (head("questions") + '<div class="hl-wrap"><div class="hl"><div class="hl-head"><span>Logic · the question</span>'
            f'<span>Work · the Block files it uses</span><span>Report · what it says</span></div>{rows}</div></div>')


def notes_html(view, rows):
    if not rows:
        return head(view) + note("Nothing here yet.")
    body = ''.join(f'<tr><td class="mono">{e(n["date"])}</td><td>{pop(n["url"], n["title"])}'
                   + (' <span class="pill warn">draft</span>' if n["draft"] else '') + f'</td>'
                   f'<td class="mono">{e(n["job"])}</td><td class="mono mut">{e(n["name"])}</td></tr>' for n in rows)
    return head(view) + f'<div class="scroll"><table><tr><th>Date</th><th>Title</th><th>Job</th><th>File</th></tr>{body}</table></div>'


def waiting_html(snap):
    rows = [j for j in snap["jobs"] if j["open"] and j["waiting"].lower() not in ("us", "nobody")]
    rows.sort(key=lambda j: -(j["days"] or 0))
    ours = [j for j in snap["jobs"] if j["open"] and j["waiting"].lower() == "us"]
    return ((head("waiting") + job_table(rows)) if rows else
            (head("waiting") + note("Nobody else has a move; every open Job waits on us."))) + \
        (f'<h3>Our move · {len(ours)}</h3>' + job_table(ours) if ours else '')


def drafts_html(snap):
    drafts = [n for n in snap["emails"] if n["draft"]]
    listing = ''.join(f'<li>{pop(n["url"], n["title"])} <span class="mono mut">{e(n["job"])}/emails/{e(n["name"])}</span></li>'
                      for n in drafts)
    return (head("drafts") + '<h3>Email drafts</h3>' + (f'<ul class="plain">{listing}</ul>' if listing else note("No email drafts."))
            + '<h3>Open checklist steps</h3>' + steps_html(snap["steps"], only_open=True))


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
        if not (r["present"] and r["status"] == "answered"):
            continue
        cards.append(f'<article class="card"><h3>{pop(r["url"], r["title"] or r["path"])} <span class="mut">{e(q["id"])}</span></h3>'
                     + ''.join(f'<p>{e(p)}</p>' for p in r.get("opening", []))
                     + (('<h4>Answer</h4>' + ''.join(f'<p>{e(p)}</p>' for p in r["answer_text"])) if r.get("answer_text") else '')
                     + '</article>')
    return head("delivery") + (''.join(cards) or note("No Question is answered yet. A report moves here when its "
                                                      "answer-status is answered."))


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
    """The shared Runs panel for one Space: its run types from the Workbench Table, each with
    its agent, skill and a prompt to copy. Nothing here starts a run or sends a message."""
    from live.runs_panel import panel_markup
    block = snap["path"].rsplit("/", 1)[0]
    kinds = []
    for r in rows:
        if r["Space"].lower() != space or r["Run type"] in ("", "none"):
            continue
        signs = f' The person signs {r["Person signs"]}.' if r["Person signs"] not in ("", "none") else ""
        planned = lambda value: value.replace(" (new)", " (planned)")
        about = " for {target}" if space == "work" else ""
        kinds.append({"label": r["Run type"], "pattern": "", "views": "",
                      "skills": [r["Skill"].replace(" (new)", "")] if r["Skill"] not in ("", "none") else [],
                      "prompt": f'Run with {planned(r["Agent"])}: {r["Run type"]}{about} in the CoWork Block {block} '
                                f'({r["Space"]} › {r["View"]}), following {planned(r["Skill"])}.{signs}'})
    if not kinds:
        return ""
    return panel_markup(space, kinds, [[] for _ in kinds], base=HERE, fill=lambda row: {},
                        whole=f"the Block {snap['block']}", folded=True)


def _assets():
    from live.runs_panel import PANEL_CSS, PANEL_JS, SPLIT_CSS
    css = ((TASK / 'assets/css/90-task-workbench.css').read_text(encoding="utf-8") + '\n' + PANEL_CSS + SPLIT_CSS
           + '.split{--card:var(--bg)}.cw-text{white-space:pre-wrap;font:13px/1.5 ui-monospace,monospace;'
             'background:var(--bg,#f6f8fa);padding:12px;border-radius:8px;max-height:640px;overflow:auto}'
             '.cw-steps{list-style:none;padding-left:0}.cw-steps li{margin:6px 0}.cw-steps li.done{color:#57606a}'
             '.rp-thumb{display:block;margin:8px 0}.rp-thumb img{display:block;width:100%;height:auto;max-height:260px;object-fit:contain;object-position:left top;'
             'border:1px solid var(--line,#d0d7de);border-radius:6px}.hl-r .idtag{overflow-wrap:anywhere}'
             '.rp-videos{display:flex;gap:10px;overflow-x:auto;margin:8px 0;padding-bottom:6px}'
             '.rp-video{flex:0 0 150px;margin:0}.rp-video video{display:block;width:150px;height:222px;object-fit:contain;'
             'background:#000;border-radius:6px}.rp-video figcaption{font-size:11.5px;line-height:1.3;margin-top:4px;'
             'color:var(--mut,#57606a)}.rp-yt{flex-basis:300px}.rp-yt iframe{display:block;width:300px;height:169px;'
             'border:0;border-radius:6px;background:#000}')
    return css, (TASK / 'assets/js/90-task-workbench.js').read_text(encoding="utf-8"), PANEL_JS


def render_block(snap, view="work"):
    space_list = spaces()
    space_of = {key: space for space, _, views in space_list for key, _ in views}
    aliases = {"scope": "block", "work": "jobs", "check": "waiting", "delivery": "delivery", "roadmap": "studio",
               "tickets": "jobs", "closed": "done"}
    view = view if view in space_of else aliases.get(view, "jobs")
    space = space_of[view]
    bodies = {"block": head("block") + block_html(snap), "people": head("people") + people_html(snap),
              "resources": head("resources") + resources_html(snap), "studio": head("studio") + studio_html(snap),
              "jobs": jobs_html(snap), "questions": questions_html(snap),
              "emails": notes_html("emails", snap["emails"]), "meetings": notes_html("meetings", snap["meetings"]),
              "waiting": waiting_html(snap), "drafts": drafts_html(snap), "progress": progress_html(snap),
              "delivery": delivery_html(snap),
              "done": head("done") + job_table([j for j in snap["jobs"] if not j["open"]], done=True)}
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
    open_rows = [j for j in snap["jobs"] if j["open"]]
    theirs = sum(j["waiting"].lower() not in ("us", "nobody") for j in open_rows)
    band = " · ".join(x for x in [snap["block"], snap["state"], f'{len(open_rows)} open jobs',
                                  f'{theirs} waiting on others', f'{len(snap["questions"])} Questions',
                                  f'{sum(n["draft"] for n in snap["emails"])} drafts'] if x)
    config = json.dumps({"path": snap["path"], "studio": snap["studio_path"], "studioEnabled": snap["studio_enabled"],
                         "home": "work", "route": ROUTE,
                         "spaces": {key: [k for k, _ in views] for key, _, views in space_list}, "aliases": aliases},
                        ensure_ascii=False).replace('<', '\\u003c')
    css, js, panel_js = _assets()
    content = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>📨 CoWork · {e(snap['title'])}</title><link rel="icon" href="data:,"><style>{css}</style></head>
<body class="tw"><main id="task-workbench"><header><h1>📨 CoWork · {e(snap['title'])}</h1></header>
<div class="dataset" title="{e(snap['spine'])}">{e(band)}</div>
<nav class="spaces" aria-label="Spaces">{space_row}</nav>
<div class="tw-source-issues">{issues(snap['source_issues'])}</div>
{''.join(panes)}
<dialog id="tw-run-dialog" aria-label="Pop-out"><div class="pop-bar"><span class="pop-title" id="tw-run-title">Pop-out</span><a class="pop-new" id="tw-run-new" target="_blank" rel="noopener">Open in its own tab ↗</a><button type="button" class="pop-x" id="tw-run-close" aria-label="Close">×</button></div><iframe class="pop-frame" id="tw-run-frame" title="Pop-out"></iframe></dialog><p id="tw-status" role="status"></p></main><script type="application/json" id="tw-config">{config}</script><script>{js}</script><script>{panel_js}</script></body></html>'''
    from live.workbench_guide import mount_guide
    return mount_guide(content, "cowork", {"path": snap["path"], "file": "board.md"},
                       "nav.spaces", "[data-space-pane],.tw-source-issues,#tw-status")


def render_report(report, board, root, board_path):
    """A Question's report Page, through the Task Workbench's report reader, with a CoWork back link."""
    from live.task_views import render_report as task_report
    page = task_report(report, board, root, board_path)
    return page.replace('/_board/task-board?', ROUTE + '?').replace('← Task</a>', '← CoWork</a>')


def render_projects(groups, where="", missing=""):
    """Every cowork Block of a Project (or under the root): state, status, open jobs, who we wait on."""
    css, _, _ = _assets()
    parts = []
    for group in groups:
        rows = []
        for b in group["blocks"]:
            waits = ", ".join(dict.fromkeys(j["waiting"] for j in b["jobs"])) or "nobody"
            nxt = next((f'{j["id"]}: {j["next"]}' for j in b["jobs"] if j["next"] and j["waiting"].lower() == "us"),
                       next((f'{j["id"]}: {j["next"]}' for j in b["jobs"] if j["next"]), ""))
            rows.append(f'<tr><td><a href="{e(b["url"])}"><span class="idtag">{e(b["block"])}</span></a><br>'
                        f'<b>{e(b["title"])}</b></td><td>{e(b["state"])}</td><td>{e(b["status"])}</td>'
                        f'<td class="num">{b["open"]}</td><td>{e(waits)}</td><td>{e(nxt)}</td></tr>')
        parts.append(f'<h2>{e(group["project"])} <span class="mut mono">{e(group["cowork"])}</span></h2>'
                     '<div class="scroll"><table><tr><th>Block</th><th>State</th><th>Status</th><th>Open jobs</th>'
                     f'<th>Waiting on</th><th>Next step</th></tr>{"".join(rows)}</table></div>')
    lead = (f'<p class="note">No CoWork Block at {e(missing)}.</p>' if missing else '')
    body = ''.join(parts) or '<p class="note">No CoWork Blocks (board-kind: cowork-block) under this root.</p>'
    title = "CoWork · " + (where or "every Project")
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width,initial-scale=1"><title>📨 {e(title)}</title><link rel="icon" href="data:,">'
            f'<style>{css}</style></head><body class="tw"><main id="cowork-projects"><header><h1>📨 {e(title)}</h1></header>'
            f'{lead}{body}</main></body></html>')
