"""The four views (Goal, Plan, Execution, Results) and the Spaces a work page shows."""
from datetime import datetime, timezone
import re
from urllib.parse import urlencode

from live import frame
from live.work_progress_records import (
    e, face_fields, goal, MODES, plan_data, read_yaml, role_of, ROLE_ORDER,
    ROLES, show, snapshot, text_of, VIEWS,
)
from live.work_progress_html import (
    card, CSVP_CSS, file_url, mark, nav, node, part,
    REFRESH, run_link, run_tally, source_link, TREE_CSS, TREE_TOOLS, ZOOM,
)
from live.work_progress_deliverables import (
    deliverables, group_state, items_nodes, level_head, tally, task_nodes, task_of,
)
from live.work_progress_background import (
    background_html,
)
from live.work_progress_runs import (
    child_rows, hot_runs, status_cards, status_tree,
)


def goal_cards(level, folder, root, data, mode):
    """The Goal first, as one tree like the folders (JL 261020: "like the TODO list ... Large TODO items, and small TODO
    items, and the final check list"; "你这两个合成一块儿吧 ... 像 folder 那种 structure 的 mind map"): the goal at
    the root, then each Job, its Tasks, and each deliverable, ticked from disk and never typed."""
    if level == "Block":
        states, html_ = [], ""
        for job in frame.children(folder, "Block"):
            got, kids = task_nodes(job, deliverables(job), root, data, mode, about=True)
            states += got
            icon = face_fields(job).get("emoji") or "🗂"
            html_ += node(level_head(icon, nav(job, root, mode, "Goal", e(job.name)), got, job=True), kids,
                          key="tree-" + frame.rel(job, root))
        got, kids = items_nodes(deliverables(folder), root, data)
        if got:
            states += got
            html_ += node(level_head("🧩", "Across all Jobs", got, job=True), kids, key="tree-across")
    elif level == "Job":
        states, html_ = task_nodes(folder, deliverables(folder), root, data, mode)
    else:
        job = frame.chain(folder, root).get("Job")
        states, html_ = items_nodes([i for i in deliverables(job) if task_of(i) == folder.name] if job else [], root, data)
    accepted = face_fields(folder).get("goal-status") or "not recorded"
    state = group_state(states) if states else "todo"
    head = (f'<p class=stat-line style="margin-bottom:2px">{mark(state)} <b>{e(goal(folder))}</b>'
            f'<span class=mut style="margin-left:12px">{tally(states)}</span></p>')
    if not states:
        head = f'<p class=stat-line><b>🎯 {e(goal(folder))}</b></p><p class=mut>No deliverables listed yet: add a ## Deliverables list to the face.</p>'
    head += background_html(folder)
    return (part("Goal") + TREE_CSS + CSVP_CSS + '<div class=dtree-wrap>' + head + (TREE_TOOLS + f'<ul class=dtree>{html_}</ul>' if html_ else "")
            + f'<p class=mut style="font-size:12px">Goal accepted by a person: {e(accepted)}</p></div>')


def studio(folder, root):
    """The Studio topics of this folder as the Studio lists them (JL 261022: "update this, to the same format"): one
    folded row each, its name, its tags, ↗ and its stage, opened in place to its drawing, its part drawings as rows
    inside it (frame._topic_row). A Job or Task shows the topics that name it, and the Block's s00 first."""
    block = frame.chain(folder, root).get("Block")
    if not block:
        return ""
    rows = []
    for owner, topic, drawings in frame.studio_inventory(block, root):
        background = topic.name.startswith("s00-")
        if folder != block and not background and folder.name not in text_of(frame._notes(topic)) \
                and not owner.is_relative_to(folder):
            continue
        rows.append(frame._topic_row(topic, drawings, root, owner))
    url = frame.ROUTE + "?" + urlencode({"path": frame.rel(folder, root), "studio": "1", "studio_group": "all"})
    if not rows:
        return '<p class=mut>No Studio topic for this folder yet.</p><p>' + frame.link(url, "Open the Block's Studio") + '</p>'
    return '<div class=studio-topics-lite>' + "".join(rows) + '</div><p>' + frame.link(url, "Open the Block's Studio") + '</p>'


def goal_view(level, folder, root, data, mode):
    report = read_yaml(folder / "workflow/report.yaml")
    summary = report.get("summary")
    body = goal_cards(level, folder, root, data, mode)
    body += part("Result") + status_cards(level, folder, root, data, mode)
    body += card("📌 Current conclusion and next step",
                 '<pre>' + e(show(summary)) + '</pre>' if summary else
                 '<p>No summary saved yet (workflow/report.yaml). ' + nav(folder, root, mode, "Results", "Read the results") + '</p>',
                 "saved" if summary else "not saved", key="conclusion")
    return body + part("Studio") + studio(folder, root)        # its own part, open (JL 261022: "the Studio section")


def plan_view(level, folder, root, data, mode):
    plan, specs = plan_data(folder)
    body = part("Operation")
    if specs:
        rows = [(e(s.get("id", "")), e(show(s.get("purpose") or s.get("goal"))), e(show(s.get("input"))),
                 e(show(s.get("result") or s.get("target"))), e(show(s.get("depends_on"))), e(show(s.get("exit_gate")))) for s in specs]
        saved = ('<p>' + source_link(folder / "workflow/plan.yaml", root, "Open the saved plan") + '</p>'
                 + frame.table(("Work item", "Purpose", "Input", "Output", "Dependencies", "Completion criteria"), rows))
    else:
        saved = '<p class=mut>No workflow/plan.yaml saved. The Result below indexes what exists; it is not an execution order.</p>'
    body += card("📋 Saved plan", saved, f"{len(specs)} work items" if specs else "none saved", open_=bool(specs), key="plan")
    if level == "Task":
        files = [p for pattern in ("scripts/**/*", "workflow/**/*", "tests/**/*", "CODE_REVIEW.md", "notebooks/*.ipynb")
                 for p in sorted(folder.glob(pattern)) if p.is_file() and not any(
                     part_.startswith(".") or part_ == "__pycache__" for part_ in p.relative_to(folder).parts)]
        body += card("🔧 Build · code, configuration and checks", '<ul>' + ''.join(
            '<li>' + source_link(p, root, p.relative_to(folder).as_posix()) + '</li>' for p in files) + '</ul>',
            f"{len(files)} files", key="build")
    body += part("Result")
    if level == "Task":
        roles = {k: l for k, l, _ in ROLES}
        rows = [(e(roles.get(role_of(r), "◻ no role")), run_link(r, root),
                 e(r["purpose"] or "Not specified. Open the Run to read its inputs and results."),
                 e(show(r["card"].get("close") or r["receipt"].get("close"))))
                for r in sorted(data[folder], key=lambda r: (ROLE_ORDER.get(role_of(r), len(ROLES)), r["run"]))]
        body += card(f"🏃 Runs and their purposes · {len(rows)}", frame.table(("Role", "Run", "Purpose", "Completion criteria"), rows),
                     run_tally(data[folder]) or "no Runs yet", open_=True, key="purposes")
    else:
        kids = frame.children(folder, level)
        body += card(f"🗂 {'Jobs' if level == 'Block' else 'Tasks'} · {len(kids)}", child_rows(level, folder, root, data, mode, "Plan"),
                     "how the work is divided", open_=True, key="children")
    return body


def execution_view(level, folder, root, data):
    every = [r for rs in data.values() for r in rs]
    return (part("Result") + hot_runs(every, root) + status_tree(level, folder, root, data, "Audience Report")
            + '<p class=mut>Status comes from Run records, not a process health check.</p>')


def results_view(level, folder, root, data, mode, theme):
    body = part("Operation")
    report = folder / "workflow/report.yaml"
    body += card("📝 Result interpretation", '<p>' + source_link(frame.face(folder), root, "Open the description and its interpretation")
                 + '</p><p class=mut>Interpretations stay on their pages; the numbers below come from Runs and change no conclusion.</p>',
                 key="interpretation")
    body += card("🧾 Execution report", '<p>' + (source_link(report, root) or "No workflow/report.yaml saved") + '</p>',
                 "saved" if report.is_file() else "not saved", key="report")
    body += part("Result")
    for task, rows in data.items():
        chain = frame.chain(task, root)
        name = " / ".join(chain[k].name for k in ("Job", "Task") if k in chain) or task.name
        content = frame.table(("Run", "Key result", "Source"), [
            (run_link(r, root), e(r["headline"] or "No result summary recorded"),
             source_link(r["receipt_path"], root, "Run record") or "Not recorded") for r in sorted(rows, key=lambda r: r["run"])])
        # the pictures the Runs drew, shown and not only linked (JL 261023: "how do I see all the tables?");
        # a display Run writes preview.png and figure.png of the same picture, so the preview stands for both
        pics = []
        for r in sorted(rows, key=lambda r: r["run"]):
            res = task / "runs" / r["run"] / "result"
            res = res if res.is_dir() else task / "results" / r["run"]
            found = sorted(res.glob("*.png")) if res.is_dir() else []
            preview = [f for f in found if f.name == "preview.png"]
            pics += (preview or found)[:4]
        if pics:
            content += "".join(
                f'<figure style="margin:10px 0"><a href="{file_url(f, root)}" target=_blank rel=noopener><img src="{file_url(f, root)}" '
                f'alt="{e(f.name)}" loading=lazy style="max-width:100%;max-height:640px;border:1px solid var(--line)"></a>'
                f'<figcaption class=mut style="font-size:12.5px">{e(f.parent.parent.name)} · {e(f.name)}</figcaption></figure>'
                for f in pics[:8])
        content += '<p>' + source_link(frame.face(task), root, "Read the Task's interpretation") + '</p>'
        # a Task's pictures show open at every level: a Job of displays reads at a glance (JL 261023, j21_paper_displays:
        # "these displays don't show the big result at a glance")
        body += card(f"📊 {name}", content, "",
                     open_=level == "Task" or bool(pics),
                     key="res-" + frame.rel(task, root))
    return body + card("❓ Questions and reports", frame.report_view(level, folder, root, theme), key="questions")


def status_board(level, folder, root, data=None):
    """The Description's status (JL 261020: "show the status of each jobs and runs here ... what runs are running, and
    what runs are finished"): the Result cards every view opens with."""
    return part("Status") + status_cards(level, folder, root, data if data is not None else snapshot(level, folder), "Audience Report")


def spaces(level, folder, root, sub, theme):
    selected = sub if sub in VIEWS else "Goal"
    data = snapshot(level, folder)
    out = {}
    for mode in MODES:
        if selected == "Goal":
            body = goal_view(level, folder, root, data, mode)
        elif selected == "Plan":
            body = plan_view(level, folder, root, data, mode)
        elif selected == "Execution":
            body = execution_view(level, folder, root, data)
        else:
            body = results_view(level, folder, root, data, mode, theme)
        live = selected in ("Goal", "Execution")
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        stamp = f'<p class=mut data-work-refresh>Last read at {timestamp} · Refreshes every 20 seconds</p>' if live else ''
        body = re.sub(r"<table(?=[\s>])", "<div class=work-table-scroll><table", body).replace('</table>', '</table></div>')   # every table, classed or not, so each wrap closes
        body = f'<section class=workflow-view data-work-progress="{e(selected)}">{stamp}{body}</section>' + (REFRESH if live else '') + ZOOM
        label, verb = {"Goal": ("Define the goal and completion criteria", "plan"), "Plan": ("Create a run plan", "plan"),
                       "Execution": ("Execute the plan", "execute"), "Results": ("Write the result interpretation", "report")}[selected]
        prompt = (f"/haipipe-task {verb} {{folder}}" if level == "Task" else
                  f"Read {{folder}} and its Tasks. {label}. Preserve each Task's own plan, Runs and results.")
        run_name = "rNN_<slug>" if verb == "execute" else f"run-{verb}-{folder.name.split('_')[0]}"
        kinds = (frame.run_type(run_name, label, prompt, "haipipe-task"),)
        if selected == "Plan" and mode == "Work Details":
            kinds += (frame.run_type(f"run-build-{folder.name.split('_')[0]}", "Prepare code and configuration for the plan",
                                     "/haipipe-task build {folder}" if level == "Task" else
                                     "Build the planned Tasks under {folder} through each Task's own workflow.", "haipipe-task"),)
        if mode == "Audience Report":
            kinds = (frame.run_type(f"run-report-{folder.name.split('_')[0]}", "Update the result interpretation",
                                   "Read {folder} and its source records. Explain what the results establish and what remains open.", "haipipe-task"),)
        out[mode] = frame.Space(html=body, subspaces=VIEWS, open=selected, run_types=kinds, page=True,
                               disk=(("workflow/", "saved plan and report, when present"),
                                     ("runs/", "existing Run cards and receipts")))
    md = frame.face(folder)                                                  # Description: the face, then its status
    if md:
        rows = [(e(k), e(v)) for k, v in frame._fields(md)]
        desc = (f'<h2>{e(frame._title(md))}</h2><p class=mut>{frame.link(frame._reader(md, root), frame._rel(md, root))}</p>'
                + (frame._table(("field", "value"), rows) if rows else ""))
        head, fields = desc.split("<table", 1) if "<table" in desc else (desc, "")
        out["Description"] = frame.Space(html=head + goal_cards(level, folder, root, data, "Audience Report")
                                         + status_board(level, folder, root, data)
                                         + (part("Face fields") + "<table" + fields if fields else "") + REFRESH + ZOOM)
    return out
