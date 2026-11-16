"""Every Run as a table or a tree: by Job, Task and role, with what runs now and what failed."""
from collections import Counter

from live import frame
from live.work_progress_records import (
    clock, e, elapsed, face_fields, goal, last_finish, location, role_of,
    ROLE_ORDER, ROLES, show, STATE, state_of,
)
from live.work_progress_html import (
    card, file_url, nav, node, RUN_LEGEND, run_link, run_mark, run_tally,
    TREE_CSS, TREE_TOOLS,
)


def child_rows(level, folder, root, data, mode, view):
    """One row per Job (a Block) or Task (a Job): its goal, its Tasks or Runs, its Runs by state, its last finish. The
    number columns never wrap; the goal gives way (JL 261020: "this is not readable")."""
    nw = ' style="white-space:nowrap"'
    heads = ["Job" if level == "Block" else "Task", "Goal"] + (["Tasks"] if level == "Block" else []) + [
        "Runs", "✅", "🏃", "❌", "⛔", "◌", "last finished"]
    rows = []
    for child in frame.children(folder, level):
        tasks = [t for t in data if t == child or child in t.parents]
        runs = [r for t in tasks for r in data[t]]
        c = Counter(state_of(r) for r in runs)
        when, _ = last_finish(runs)
        g = goal(child)
        cells = [(nav(child, root, mode, view, child.name), ""), (e(g if len(g) <= 120 else g[:117] + "…"), "")]
        cells += [(e(str(len(tasks))), nw)] if level == "Block" else []
        cells += [(e(str(len(runs))), nw)] + [(e(str(c[k]) if c[k] else ""), nw)
                                             for k in ("finished", "running", "failed", "blocked", "waiting")]
        cells += [(e(when[:16].replace("T", " ")) if when else "", nw)]
        rows.append("<tr>" + "".join(f"<td{st}>{v}</td>" for v, st in cells) + "</tr>")
    if not rows:
        return "<p class=mut>Nothing here yet.</p>"
    head = "".join(f"<th{nw if i > 1 else ''}>{e(h)}</th>" for i, h in enumerate(heads))
    return f"<table class=wf-table><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table>" + LEGEND


LEGEND = ("<p class=mut>✅ finished · 🏃 running · ❌ failed · ⛔ blocked · ◌ waiting for a person to start it. Read from each "
          "Run's receipt (runtime.yaml), else its card; a finished Run is not the goal accepted.</p>")


def run_rows(rows, root, full=True):
    """A Task's Runs (full): grouped by role in the order a Task lives (trial, make, fix, check, describe, figures,
    evidence, publish), the role named once at the top of its group. Not full: Runs across Tasks, as a list."""
    label = dict((k, l) for k, l, _ in STATE)
    nb = lambda v: e(v).replace(" ", "&nbsp;")                               # a state or a time never breaks in two
    if not full:
        return frame.table(("Run", "Task", "Started at", "What it says"), [
            (run_link(r, root), e(r["task"].name), nb(clock(r["receipt"].get("started_at"))),
             e(str(r["receipt"].get("failure") or r["card"].get("failure") or r["headline"] or ""))[:200]) for r in rows])
    if not rows:
        return '<p class=mut>Nothing here yet.</p>'
    names = {k: (l, why) for k, l, why in ROLES}
    rows = sorted(rows, key=lambda r: (ROLE_ORDER.get(role_of(r), len(ROLES)), r["run"]))
    body, last = [], None
    for r in rows:
        role = role_of(r)
        first = role != last
        last = role
        n = sum(1 for x in rows if role_of(x) == role)
        name, why = names.get(role, ("◻ no role", "its card names no role"))
        cell = (f'<b>{nb(name)}</b> <span class=mut>{n}</span><div class=mut style="font-size:12px">{e(why)}</div>'
                if first else "")
        cells = (cell, run_link(r, root), nb(label.get(state_of(r), "no record")), e(show(location(r["receipt"]))),
                 nb(clock(r["receipt"].get("started_at"))), nb(elapsed(r["receipt"])),
                 e("" if str(r["headline"]).startswith(r["run"]) else r["headline"]))
        style = ' style="border-top:2px solid #d0d7de"' if first and body else ""
        body.append(f"<tr{style}>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    head = "".join(f"<th>{h}</th>" for h in ("Role", "Run", "Status", "Where", "Started at", "Elapsed", "Key result"))
    return f"<table class=wf-table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def run_node(row, root, task=False):
    """One Run on one line: its mark, its name, and only what its receipt holds: when it finished, how long it took,
    the first words of its result (JL 261021: "result 跟 go 一样的 structure"); where it ran shows on hover."""
    mark_, word = run_mark(row).split(" ", 1)
    rec = row["receipt"]
    said = str(row.get("headline") or "").split(";")[0].strip()
    said = "" if said.startswith(row["run"]) else said
    took = elapsed(rec)
    meta = ([e(row["task"].name)] if task else []) + [e(word)] + ([e(clock(rec["finished_at"]))] if rec.get("finished_at") else []) \
        + ([e(took)] if took not in ("Not recorded", "Conflicting timestamps") else []) + ([e(said[:110])] if said else [])
    tip = f"Ran on {show(location(rec))}; started {clock(rec.get('started_at'))}"
    return f'<li><span title="{e(tip)}">{mark_} {run_link(row, root)}</span>' + "".join(f"<span class=m>{m}</span>" for m in meta) + "</li>"


def role_nodes(task, rows, root):
    """A Task's Runs by the job each does (trial, make, fix, check, describe, figures, evidence, publish), each group
    folded at first."""
    groups, names, out = {}, {k: l for k, l, _ in ROLES}, ""
    for row in rows:
        groups.setdefault(role_of(row), []).append(row)
    for role in sorted(groups, key=lambda k: ROLE_ORDER.get(k, len(ROLES))):
        rs = sorted(groups[role], key=lambda r: r["run"])
        head = f'<span class=lvl>{e(names.get(role, "◻ no role"))}</span><span class=chip>{e(run_tally(rs))}</span>'
        out += node(head, "".join(run_node(r, root) for r in rs), key=f"runs-{task.name}-{role}")
    return out


def task_pictures(task, rows):
    """The picture each finished Run of a Task drew, latest Run number first (r01 before a carried r00_previous_draft),
    then by finish time: [(run, its preview.png, else its first .png)]; a Run that drew none is left out."""
    out = []
    for row in sorted(rows, key=lambda r: (r["run"][:3], str(r["receipt"].get("finished_at") or "")), reverse=True):
        if state_of(row) != "finished":
            continue
        res = task / "runs" / row["run"] / "result"
        res = res if res.is_dir() else task / "results" / row["run"]
        found = sorted(res.glob("*.png")) if res.is_dir() else []
        pick = next((f for f in found if f.name == "preview.png"), found[0] if found else None)
        if pick:
            out.append((row["run"], pick))
    return out


def task_run_node(task, rows, root, mode):
    head = (f'<span class=lvl>📂 {nav(task, root, mode, "Execution", e(task.name))}</span>'
            f'<span class=chip>{e(run_tally(rows))}</span>')
    # every Run's picture shows on the Task's folded line, side by side (JL 261023: "why I cannot see the images shown by
    # default?"; "why this is not available in the results", of a carried previous-draft Run)
    pics = task_pictures(task, rows)[:4]
    width = 760 if len(pics) == 1 else 460
    below = ('<div style="display:flex;flex-wrap:wrap;gap:12px;align-items:flex-start;margin:4px 0 8px">' + "".join(
        f'<figure style="margin:0"><a href="{file_url(pic, root)}" target=_blank rel=noopener><img src="{file_url(pic, root)}" '
        f'alt="{e(pic.name)}" loading=lazy style="display:block;max-width:min(100%,{width}px);max-height:260px;'
        'border:1px solid var(--line,#e3e3e6)"></a>'
        + (f'<figcaption class=m style="margin:2px 0 0">{e(run)}</figcaption>' if len(pics) > 1 else "") + '</figure>'
        for run, pic in pics) + '</div>') if pics else ""
    return node(head, role_nodes(task, rows, root) or "<li class=m>No Runs yet.</li>", key="runs-" + frame.rel(task, root),
                below=below)


def status_tree(level, folder, root, data, mode):
    """Every Run as one tree like the Goal's: Job, Task, the job a Run does, the Run (JL 261021: "result 跟 go 一样的
    structure 可以吗？")."""
    every = [r for rs in data.values() for r in rs]
    if level == "Block":
        html_ = ""
        for job in frame.children(folder, "Block"):
            tasks = [t for t in data if job in t.parents]
            runs = [r for t in tasks for r in data[t]]
            head = (f'<span class="lvl job">{face_fields(job).get("emoji") or "🗂"} {nav(job, root, mode, "Execution", e(job.name))}</span>'
                    f'<span class=chip>{e(run_tally(runs))}</span>')
            html_ += node(head, "".join(task_run_node(t, data[t], root, mode) for t in tasks), key="runs-" + frame.rel(job, root))
    elif level == "Job":
        html_ = "".join(task_run_node(t, rows, root, mode) for t, rows in data.items())
    else:
        html_ = role_nodes(folder, data.get(folder, []), root)
    head = f'<p class=stat-line style="margin-bottom:2px"><b>📊 Runs</b><span class=mut style="margin-left:12px">{e(run_tally(every))}</span></p>'
    return TREE_CSS + '<div class=dtree-wrap>' + head + TREE_TOOLS + f'<ul class=dtree>{html_}</ul>' + RUN_LEGEND + '</div>'


def hot_runs(every, root):
    """What runs now and what failed, each a short list of one-line Runs with their Task."""
    out = ""
    for k, title in (("running", "🏃 Running now"), ("failed", "❌ Failed")):
        rows = [r for r in every if state_of(r) == k]
        body = f'<ul class=dtree>{"".join(run_node(r, root, task=True) for r in rows)}</ul>' if rows else "<p class=mut>None.</p>"
        out += card(f"{title} · {len(rows)}", body, "" if rows else "none", key=k)
    return out


def status_cards(level, folder, root, data, mode):
    """The Result part every view opens with: every Run as a tree, then what runs now and what failed."""
    every = [r for rs in data.values() for r in rs]
    return status_tree(level, folder, root, data, mode) + hot_runs(every, root)
