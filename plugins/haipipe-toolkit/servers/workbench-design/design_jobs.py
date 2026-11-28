"""Design content for the shared Jobs selector; reads existing records, never writes them."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from live import design_reader as R, design_views as V
from live.frame import esc, reader, table
from live.focus_base import page_url
from live.ui_parts import _kv, _side_tabs, open_dot
from live.design_focus_parts import _page, _section

TASK_TOPICS = {"ideas": "Ideas", "designs": "Designs", "review": "Review"}


def content(build) -> str:
    """Nested views share the outer page's assets, without repeating their CSS per step."""
    from live.design_focus_parts import _head_css, PB_JS, FD, PROMPT_JS, POST_JS
    html = build()
    for asset in (_head_css(), PB_JS, FD.JS, PROMPT_JS, POST_JS):
        html = html.replace(asset, "")
    return html


def applies(folder: Path) -> bool:
    return R.is_method_book(folder) or R.is_ladder(folder)


def topic(job: Path) -> tuple[str, str]:
    face = R.front(R.face(job))
    if R.is_release(job):              # a Book Job: its authored family, else its method's registry family
        family = str(face.get("family") or R.registry().get(R.method_pin(face.get("method"))[0] or "", {}).get("family") or "")
        return ("family-" + hashlib.sha256(family.encode()).hexdigest()[:12], family) if family else ("methods", "Methods")
    mid, _ = R.method_pin(face.get("method"))
    family = str(R.registry().get(mid or "", {}).get("family") or "")
    if family:                       # a Board Job groups by its method's family; the goal is in its label
        return "family-" + hashlib.sha256(family.encode()).hexdigest()[:12], family
    goal = str(face.get("goal") or "")
    gid = R.goal_pin(goal)
    from live.design_focus_design import _goal_name
    board = R.board(job.parent, with_jobs=False)
    return (gid, _goal_name(board, gid)) if gid else ("goals", "Goals")


def label(job: Path) -> str:
    f = R.front(R.face(job))
    if R.is_release(job):
        return f'{job.name[:3]} · {f.get("method", "")} {f.get("title", "")}'.strip()
    j = R.job(job)
    gid = R.goal_pin(str(f.get("goal") or ""))
    return " · ".join(p for p in (j["id"], gid, f'{j["method"]} {j["version"]}', j["inputs"]) if p)


def task_topic(task: Path) -> str:
    return {"t00": "ideas", "t99": "review"}.get(R.kind_of(task), "designs")


def tabs(folder: Path, key: str, items: list[tuple[str, str]]) -> str:
    """Names and HTML, using the same left tabs as the rest of the workbench."""
    if not items:
        return ""
    if len(items) == 1:
        return items[0][1]
    uid = hashlib.sha256(str(folder).encode()).hexdigest()[:12] + "-" + key + "-"
    return _side_tabs(uid, [(name, "") for name, _ in items], [body for _, body in items])


def runs(folder: Path, root: Path) -> str:
    from live.focus_plan_results import runs_section
    section = runs_section(folder, root)
    return _section(section[0], section[2], section[1]) if section else ""


def task_body(task: Path, root: Path) -> str:
    from live.design_focus import views
    from live.focus_jobs import label as task_label
    items = [(name, content(build)) for key, (name, build) in views(task, root, "report").items() if key != "mindmap"]
    return tabs(task, "steps", items) + runs(task, root) if items else esc(task_label(task))


def task_list(job: Path, root: Path) -> str:
    from live.focus_jobs import label as task_label, task_mark
    rows = []
    for task in sorted(job.iterdir()):
        if task.is_dir() and re.match(r"^t\d\d[_-]", task.name):
            rows.append(f'<li><a href="{esc(page_url(task, root))}" data-jsub-to="{esc(task.name[:3])}" '
                        f'data-topic="{task_topic(task)}">{esc(task_label(task))}</a> {esc(task_mark(task, root))}</li>')
    return '<ul class="wk-rows">' + ''.join(rows) + '</ul>' if rows else ""


def execution_main(job: Path, root: Path) -> str:
    from live.design_focus import views
    from live.design_focus_design import _goal_name, _pvo
    from live.design_ladder_act import ready
    j = R.job(job)
    b = R.board(job.parent, with_jobs=False)
    brief = _kv([("Goal", esc(_goal_name(b, j["goal"]))),
                 ("Method", esc(f'{j["method"]} {j["version"]}'.strip())), ("Inputs", esc(j["inputs"]))])
    body = _section("📌 Brief", brief)
    tasks = task_list(job, root)
    if tasks:
        body += _section("🧩 Tasks", tasks)
    kept = [d for d in j["designs"] if any(r.get("design") == d["id"] and r.get("kept") == "yes" for r in j["ranking"])]
    if kept:
        cards = [(f'{d["id"]} · {d["short"]}', V.as_it_reads(d["message"], d["path"], root)
                  + V._pred(d["prediction"])) for d in kept]
        body += _section("✏️ Kept designs", tabs(job, "kept", cards))
    if j["ranking"]:
        body += _section("🏆 Ranking", V._review_whole(j, b, root, lambda **kw: page_url(Path(kw["path"]), root)))
    observed, _ = _pvo(b, [j], root)
    if observed:
        body += _section("🎯 Predicted vs observed", observed)
    designs, _ = ready(job)
    if designs:
        panel = V._approve_panel(j, job, root, head=False)
        body += _section("✍️ Review and approve", panel, "waiting for you", "🙋 Review and approve")
    elif j["delivered"]:
        body += _section("📦 Delivery", V._job_delivery(j, root, "designs.md"), "done")
    # All established setup, workflow and close actions stay reachable from Main.
    items = [(name, content(build)) for key, (name, build) in views(job, root, "report").items() if key != "mindmap"]
    body += _section("📋 Workflow", tabs(job, "workflow", items)) + runs(job, root)
    return _page("", "", body)


def method_main(job: Path, root: Path) -> str:
    from live.design_book import _steps_table
    book = R.method_book(job.parent, root)
    method = next((m for m in book["types"] if m["path"] == job), None)
    if not method:
        return ""
    versions = method["releases"]
    face = R.face(job)
    fields = R.front(face)
    brief = _kv([("Method", esc(f'{method["method"]} · {method["title"]}')),
                 ("Goal", esc(str(fields.get("goal") or "")))])
    body = _section("📌 Method", open_dot(brief, reader(face, root), job.name, pop=job.name) if face else brief)
    if versions:
        body += _section("🪜 Steps", _steps_table(versions[-1]))
        cards = [(v["version"], open_dot(_kv([("Signed", esc(v["signed"]))]) + _steps_table(v),
                   reader(v["card_path"], root), v["id"], pop=v["id"])) for v in reversed(versions)]
        body += _section("🔖 Versions", tabs(job, "versions", cards))
        used = [j for v in versions for j in v["jobs"]]
        if used:
            body += _section("🔗 Used by", '<ul class="wk-rows">' + ''.join(
                f'<li><a href="{esc(page_url(j["board"], root, "jobs", j["id"]))}">{esc(j["name"])}</a></li>'
                for j in used) + '</ul>')
    # Only explicitly attributed proposals belong to this method; never assign by a guessed title.
    proposals = []
    for prop in book["proposals"]:
        f = R.front(prop["path"])
        if str(f.get("method", "")).split(" ")[0] != method["method"]:
            continue
        from live.focus_base import markdown
        proposals.append((prop["title"], markdown(prop["body"], prop["path"].parent, root)))
    if proposals:
        body += _section("💡 Proposals", tabs(job, "proposals", proposals))
    return _page("", "", body + runs(job, root))


def main(job: Path, root: Path) -> str:
    return method_main(job, root) if R.is_release(job) else execution_main(job, root)
