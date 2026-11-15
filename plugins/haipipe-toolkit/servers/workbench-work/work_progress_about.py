"""The pop-out pages: a Job's overview and a Task's report, with the Studio drawings that name them."""
import re
from urllib.parse import urlencode

from live import frame
from live.work_progress_records import (
    clock, e, face_fields, goal, records, role_of, ROLE_ORDER, ROLES,
    section, snapshot, text_of,
)
from live.work_progress_html import (
    file_url, nav, run_mark, run_tally, TICKS,
)
from live.work_progress_deliverables import (
    deliverables, group_state, item_state, tally, task_of,
)
from live.work_progress_background import (
    background_md,
)


def topic_pictures(folder, root, job=None):
    """Every Studio topic that names this Job or Task, each its picture and a link to it in the Block's Studio (JL
    261022, sending b51's s01-food-api drawing: "we also need ... job level report and task level report"). A Job's own
    `sNN-jNN-…` topic comes first, then each topic whose face names it; a Task's topic must also name its Job, or be
    that Job's own topic, since Task names repeat across Jobs. s00 is the Block's index, never a Job's or a Task's."""
    block = frame.chain(folder, root).get("Block")
    topics = list(frame.studio_inventory(block, root)) if block else []
    jnn = (job or folder).name.split("_")[0]
    own = [t for t in topics if re.match(rf"^s\d\d-{jnn}-", t[1].name)]

    def names(t):
        said = text_of(frame._notes(t[1]))
        return folder.name in said and (job is None or job.name in said or t in own)
    picked = ([] if job else own) + [t for t in topics if not t[1].name.startswith("s00") and t not in
                                     ([] if job else own) and names(t)]
    out = []
    for owner, topic, _ in picked:
        png = topic / f"{topic.name}.png"
        png = png if png.is_file() else next(iter(sorted(topic.glob("*.png"))), None)
        if not png:
            continue
        url = frame.ROUTE + "?" + urlencode({"path": frame.rel(folder, root), "studio": "1", "studio_group": "all"})
        url += "#" + frame.studio_anchor(topic, owner, block)
        out.append(f'<figure><a href="{e(url)}"><img src="{file_url(png, root)}" alt="{e(topic.name)}" loading=lazy '
                   f'style="width:100%;max-width:900px;display:block"></a><figcaption class=md-file>'
                   f'{frame.link(url, topic.name)}</figcaption></figure>')
    return "".join(out)


def job_drawing(job, root):
    """The Job's Studio drawings: its own topic, then every topic that names it (topic_pictures)."""
    return topic_pictures(job, root)


def render_task_about(task, root):
    """A Task's report as one rendered Markdown page, for the pop-out: its goal, close line and state, its Runs by
    role (mark, when it finished, its one-line result; each opens its own page), its Opening, what it hands on, and
    the charts its figures Runs drew, all read from disk on each open."""
    from live import page_reader
    fields, face = face_fields(task), text_of(frame.face(task))
    title = next((l[2:].strip() for l in face.splitlines() if l.startswith("# ")), task.name)
    job = frame.chain(task, root).get("Job")
    items = [i for i in deliverables(job) if task_of(i) == task.name] if job else []
    data = snapshot("Task", task)
    states = {id(i): item_state(i, root, data)[0] for i in items}
    rows = records(task)
    md = [f"# 📂 {title}", "", f"**Goal.** {goal(task)}", ""]
    if fields.get("close"):
        md += [f"**Close when.** {fields['close']}", ""]
    if fields.get("state"):
        md += [f"**State.** {fields['state']}", ""]
    md += ["## Progress", "", f"Items {tally([states[id(i)] for i in items])}" if items else "no items listed for this Task"]
    md[-1] += f" · Runs {run_tally(rows)}" if rows else ""
    md.append("")
    if rows:
        names = {k: l for k, l, _ in ROLES}
        md += ["| Role | Run | Mark | Finished | Result |", "|---|---|---|---|---|"]
        for row in sorted(rows, key=lambda r: (ROLE_ORDER.get(role_of(r), len(ROLES)), r["run"])):
            rec = row["receipt"]
            url = frame.ROUTE + "?" + urlencode({"view": "work-run", "path": frame.rel(task, root), "run": row["run"]})
            said = str(row.get("headline") or "").split(";")[0].strip()
            said = "" if said.startswith(row["run"]) else said.replace("|", "/")
            when = clock(rec["finished_at"]) if rec.get("finished_at") else "-"
            md.append(f"| {names.get(role_of(row), 'no role')} | [{row['run']}]({url}) | {run_mark(row)} | {when} | "
                      f"{said[:160] or '-'} |")
        md.append("")
    opening = section(face, "Opening")
    if opening.strip():
        md += ["## Opening", "", opening.strip(), ""]
    html_ = page_reader.markdown_html("\n".join(md))
    if items:
        lines = ["## What it hands on", ""]
        for i in items:
            st = states[id(i)]
            means = i.get("means")
            first = (means[0] if isinstance(means, list) and means else str(means or "")).strip()
            lines.append(f"- {'☐' if st == 'todo' else TICKS[st]} **{i['what']}**" + (f": {first}" if first else ""))
        html_ += page_reader.markdown_html("\n".join(lines))
    figures = []
    for row in rows:                                   # the charts a figures Run drew, newest Run last
        if role_of(row) == "figures":
            res = task / "runs" / row["run"] / "result"
            res = res if res.is_dir() else task / "results" / row["run"]
            figures += sorted(res.glob("*.png"))[:6] if res.is_dir() else []
    if figures:
        html_ += page_reader.markdown_html("## Figures") + "".join(
            f'<figure><img src="{file_url(f, root)}" alt="{e(f.name)}" loading=lazy><figcaption class=md-file>'
            f'{e(f.parent.parent.name)} · {e(f.name)}</figcaption></figure>' for f in figures[:12])
    drawings = topic_pictures(task, root, job) if job else ""
    if drawings:                                       # the Studio topics that name this Task (JL 261022)
        html_ += page_reader.markdown_html("## Drawings") + drawings
    back = nav(task, root, "Audience Report", "Goal", "Open the Task page")
    return ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,'
            f'initial-scale=1"><title>Report · {e(task.name)}</title><style>{page_reader.MARKDOWN_CSS}'
            'figure{margin:.8em 0}td:nth-child(1),td:nth-child(3),td:nth-child(4){white-space:nowrap}'
            f'</style></head><body><p class=md-file>{e(task.name)} · report, read from disk · {back}</p>{html_}</body></html>')


def render_about(job, root):
    """A Job's overview as one rendered Markdown page, for the pop-out: its goal and close line, its progress Task by
    Task, its Topic, its Background, what it hands on, and its Studio drawing, all read from disk on each open."""
    from live import page_reader
    data = snapshot("Job", job)
    fields, face = face_fields(job), text_of(frame.face(job))
    title = next((l[2:].strip() for l in face.splitlines() if l.startswith("# ")), job.name)
    items = deliverables(job)
    states = {id(i): item_state(i, root, data)[0] for i in items}
    tasks = frame.children(job, "Job")
    rows = [r for t in tasks for r in records(t)]
    md = [f"# {fields.get('emoji') or '🗂'} {title}", "", f"**Goal.** {goal(job)}", ""]
    if fields.get("close"):
        md += [f"**Close when.** {fields['close']}", ""]
    md += ["## Progress", "", (f"Items {tally([states[id(i)] for i in items])}" if items else "no items listed")
           + (f" · Runs {run_tally(rows)}" if rows else ""), "", "| Task | What it delivers | Items | Runs |",
           "|---|---|---|---|"]
    for t in tasks:
        mine = [i for i in items if task_of(i) == t.name]
        st = group_state([states[id(i)] for i in mine]) if mine else "todo"
        tick = "☐" if st == "todo" else TICKS[st]
        url = frame.ROUTE + "?" + urlencode({"path": frame.rel(t, root), "space": "Audience Report", "sub": "Goal"})
        what = (face_fields(t).get("goal") or "").replace("|", "/")
        md.append(f"| {tick} [{t.name}]({url}) | {what} | {tally([states[id(i)] for i in mine]) if mine else '-'} | "
                  f"{run_tally(records(t)) or '-'} |")
    md.append("")
    topic = section(face, "Topic")
    if topic.strip():
        md += ["## Topic", "", topic.strip(), ""]
    html_ = page_reader.markdown_html("\n".join(md))
    pieces = background_md(job)
    if pieces:
        html_ += page_reader.markdown_html("## Background")
        html_ += "".join(page_reader.markdown_html(v) if k == "md" else v for k, v in pieces)
    if items:
        lines = ["## What it hands on", ""]
        for i in items:
            st = states[id(i)]
            means = i.get("means")
            first = (means[0] if isinstance(means, list) and means else str(means or "")).strip()
            lines.append(f"- {'☐' if st == 'todo' else TICKS[st]} **{i['what']}**" + (f": {first}" if first else ""))
        html_ += page_reader.markdown_html("\n".join(lines))
    drawing = job_drawing(job, root)
    if drawing:
        html_ += page_reader.markdown_html("## Drawings") + drawing
    back = nav(job, root, "Audience Report", "Goal", "Open the Job page")
    return ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,'
            f'initial-scale=1"><title>About · {e(job.name)}</title><style>{page_reader.MARKDOWN_CSS}'
            'figure{margin:.6em 0}svg{max-width:100%;height:auto}td:nth-child(1),td:nth-child(3),td:nth-child(4){white-space:nowrap}'
            f'</style></head><body><p class=md-file>{e(job.name)} · overview, read from disk · {back}</p>{html_}</body></html>')
