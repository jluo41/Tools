"""Task Block workbench over Questions, report Pages and native Work records.

The existing Page Run reader owns Ticket/Result pairing, including redirected
Job stores and attempt history. This adapter aggregates its records and keeps
execution, the workflow's declared report, and the Page's READING separate.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, quote, urlencode, urlparse

import yaml

from host_registry import route_allowed, static_path_allowed
from live.home import _manifests, project_owner
from live.runs import local_runs
from src.dialect_task_block import page_info
from src.item_table import compact_global_run

ASSETS = Path(__file__).parent / "assets"
_JOB = re.compile(r"^j\d{2}_", re.I)
_TASK = re.compile(r"^t\d{2}_[a-z0-9_]+$", re.I)
_TITLE = re.compile(r"^#\s+(.+)$", re.M)
_READING = re.compile(r"^####\s+READING\s*·\s*current\s*$", re.M)
_MAX_TEXT = 1024 * 1024


def _inside(path: Path, root: Path) -> bool:
    try:
        return path.resolve().is_relative_to(root.resolve())
    except (OSError, RuntimeError):
        return False


def _read(path: Path, boundary: Path | None = None) -> str:
    if boundary is not None and not _inside(path, boundary):
        return ""
    try:
        if path.stat().st_size > _MAX_TEXT:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        return ""


def _field(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:[ \t]*(.*)$", text, re.M)
    return match.group(1).strip().strip("\"'") if match else ""


def _yaml(path: Path, issues: list[str], label: str, boundary=None) -> dict:
    text = _read(path, boundary)
    if not text.strip():
        if path.exists():
            issues.append(f"{label} is empty, unreadable or outside its source folder")
        return {}
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        issues.append(f"{label} contains invalid YAML")
        return {}
    if not isinstance(data, dict):
        issues.append(f"{label} must be a mapping")
        return {}
    return data


def is_task_board(board: Path) -> bool:
    return _field(_read(board / "board.md", board), "board-kind") == "task-block"


def task_boards(root: Path) -> list[Path]:
    root = root.resolve()
    return sorted({p.parent for p in _manifests(root)
                   if _inside(p, root) and is_task_board(p.parent)})


def resolve_task_board(root: Path, raw: str) -> Path | None:
    """Resolve a source/generated-page URL to its owning Task Block in root."""
    root = root.resolve()
    if not isinstance(raw, str) or "\x00" in raw:
        return None
    if not raw:
        boards = task_boards(root)
        return boards[0] if len(boards) == 1 else None
    try:
        target = (root / raw.split("?", 1)[0].split("#", 1)[0].lstrip("/")).resolve()
        if not target.is_relative_to(root):
            return None
        for candidate in (target, *target.parents):
            if not candidate.is_relative_to(root):
                break
            if (candidate / "board.md").is_file():
                return candidate if is_task_board(candidate) else None
    except (OSError, ValueError, RuntimeError):
        return None
    return None


def _source_url(path: Path | None, root: Path) -> str:
    if path is None or not path.is_file() or not static_path_allowed(root, path):
        return ""
    return "/" + quote(path.resolve().relative_to(root.resolve()).as_posix(), safe="/")


def _page_url(page: Path, board: Path, root: Path, route: str, only) -> str:
    if not _inside(page, board) or not page.is_file() or not route_allowed("/_board/" + route, only):
        return ""
    return "/_board/" + route + "?" + urlencode({
        "path": page.relative_to(root).as_posix(),
        "file": page.relative_to(board).as_posix(),
    })


def _reading(text: str, runs: list[dict]) -> dict:
    """Read signed rows, without claiming a CHECK/release freshness audit."""
    matches = list(_READING.finditer(text))
    if not matches:
        return {"rows": [], "signed": 0, "total": 0, "issues": ["No current READING table"]}
    section = re.split(r"^#{1,4}\s", text[matches[0].end():], maxsplit=1, flags=re.M)[0]
    rows, issues, seen = [], [], set()
    if len(matches) > 1:
        issues.append("More than one current READING table")
    by_id = {r["compact_id"]: r for r in runs if r["compact_id"]}
    for line in section.splitlines():
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not re.fullmatch(r"R\d+", cells[0]):
            continue
        rid, topic, verdict, ruling, meaning = cells[:5]
        signed = bool(re.search(r"✅\s+read\s*·\s*[^·]+\s*·\s*\S+", ruling))
        compact = compact_global_run(verdict)
        bound = by_id.get(compact)
        if rid in seen:
            issues.append(f"Duplicate READING id {rid}")
        seen.add(rid)
        if not signed:
            issues.append(f"{rid}: awaiting a signed reading")
        if not bound:
            issues.append(f"{rid}: Verdict Run does not resolve in this Task")
        elif bound["status"] != "complete":
            issues.append(f"{rid}: Verdict Run is {bound['status']}")
        elif signed:
            try:
                signed_at = datetime.fromisoformat(ruling.rsplit("·", 1)[-1].strip().replace("Z", "+00:00"))
                finished_at = datetime.fromisoformat(bound["finished"].replace("Z", "+00:00"))
                if signed_at.tzinfo and finished_at.tzinfo and signed_at < finished_at:
                    issues.append(f"{rid}: signature predates the current Verdict Result")
            except ValueError:
                pass  # Historical signatures without comparable timestamps stay declared facts.
        rows.append({"id": rid, "topic": topic, "verdict": verdict,
                     "ruling": ruling, "meaning": meaning, "signed": signed})
    if not rows:
        issues.append("Current READING table has no reading rows")
    return {"rows": rows, "signed": sum(r["signed"] for r in rows),
            "total": len(rows), "issues": issues}


def _run_row(row: dict, root: Path) -> dict:
    issues = list(row.get("audit", []))
    receipt = _yaml(row["runtime"], issues, "Run receipt") if row.get("runtime") else {}
    raw = str(receipt.get("status") or "").lower()
    status = {"Ready": "planned", "Running": "running", "Waiting": "waiting",
              "Done": "complete", "Failed": "failed", "Held": "blocked"}.get(row["status"], "unknown")
    if raw == "superseded":
        status = "superseded"
    ticket_open = not row.get("runtime") and row["status"] == "Running" and not issues
    if not row.get("runtime"):
        if any("no runtime receipt" in issue or "nor a runtime receipt" in issue for issue in issues):
            status = "missing"
    elif not receipt:
        status = "blocked"
    if status == "failed" and not issues:
        issues.append(str(receipt.get("failure") or "Run failed"))
    if status == "blocked" and not issues:
        issues.append("Complete receipt has no available Result" if raw in {"complete", "completed", "done", "ok"}
                      else "Run is blocked or its receipt needs review")
    # The shared reader can include absolute paths in an audit of duplicate
    # stores. Keep the finding, and use its existing Page detail for inspection.
    issues = [i.split(": ", 1)[0] if "Result locations" in i else i for i in issues]
    return {"id": row["run_id"], "detail_key": row.get("global_id") or row["run_id"],
            "compact_id": row.get("compact_id", ""),
            "name": row["ticket"].stem if row.get("ticket") else row["result_path"].name,
            "lane": row.get("lane", "task"), "allocated": bool(row.get("ticket")),
            "status": status, "recorded_status": raw or ("open (Ticket)" if ticket_open else
                "missing" if status == "missing" else "source projection"),
            "target": row.get("target", ""), "outcome": row.get("outcome", ""),
            "started": str(receipt.get("started_at") or ""),
            "finished": str(receipt.get("finished_at") or ""),
            "failure": str(receipt.get("failure") or ""), "issues": issues,
            "ticket_url": _source_url(row.get("ticket"), root),
            "receipt_url": _source_url(row.get("runtime"), root)}


def task_snapshot(task: Path, board: Path, root: Path, only=()) -> dict:
    page = task / (task.name + ".md")
    info = page_info(board, page)
    text = _read(page, board)
    issues = []
    if not text:
        issues.append("Task Page missing or unreadable")
    plan = _yaml(task / "workflow/plan.yaml", issues, "Workflow plan", task)
    report = _yaml(task / "workflow/report.yaml", issues, "Workflow report", task)
    specs = plan.get("run_specs", [])
    if not isinstance(specs, list):
        issues.append("Workflow run_specs must be a list")
        specs = []
    summary = report.get("summary") or {}
    if not isinstance(summary, dict):
        issues.append("Workflow report summary must be a mapping")
        summary = {}
    # Confine authored lanes. A declared external Job Result store is still
    # read by local_runs, but receives no static link outside the served root.
    lanes = [task / n for n in ("runs", "results", "scripts", "workflow", "draft", "outline")]
    lanes.append(task.parent / "src/config-defaults.yaml")
    unsafe = not _inside(page, board) or any(p.exists() and not _inside(p, root) for p in lanes)
    runs = []
    if unsafe:
        issues.append("A Task source lane points outside the served root")
    else:
        try:
            runs = [_run_row(row, root) for row in local_runs(page)]
        except (OSError, ValueError, RuntimeError) as exc:
            issues.append(f"Could not read Run records ({type(exc).__name__})")
    owned = [r for r in runs if r["lane"] == "task" and r["allocated"] and r["status"] != "superseded"]
    counts = Counter(r["status"] for r in owned)
    execution = ("attention" if any(counts[s] for s in ("failed", "blocked", "missing", "unknown"))
                 else "running" if counts["running"] else "waiting" if counts["waiting"]
                 else "planned" if counts["planned"] else "complete" if owned else "empty")
    reading = _reading(text, runs)
    issues.extend(reading["issues"])
    for run in runs:
        if run["issues"] or run["status"] in {"failed", "blocked", "missing"}:
            issues.append(f"{run['name']}: {run['failure'] or '; '.join(run['issues']) or run['status']}")
    if execution == "complete" and not report:
        issues.append("Runs complete; workflow report not recorded")
    if str(summary.get("status", "")).lower() == "closed" and execution != "complete":
        issues.append("Report declares closed while execution is not complete")
    configs = task / "scripts/config"
    config_count = sum(1 for p in configs.glob("r[0-9][0-9]_*.y*ml")
                       if p.is_file() and _inside(p, task)) if _inside(configs, task) else 0
    title = _TITLE.search(text)
    from live.task_questions import section, plain
    purpose = plain(section(text, "Opening").split("\n\n", 1)[0])
    for run in runs:
        run["result_url"] = "/_board/task-board?" + urlencode({
            "path": (board.relative_to(root) / "board.md").as_posix(),
            "task": info["id"], "run": run["detail_key"]})
    return {"id": info["id"], "name": task.name, "job": info["job"],
            "block": board.name, "kind": _field(text, "task-type") or "Task", "purpose": purpose,
            "title": title.group(1) if title else task.name,
            "page_state": _field(text, "state") or "Not declared",
            "plan_specs": len(specs), "plan_present": bool(plan),
            "plan_url": _source_url(task / "workflow/plan.yaml", root),
            "config_count": config_count, "ticket_count": sum(r["allocated"] and r["lane"] == "task" for r in runs),
            "report_present": bool(report), "report_status": str(summary.get("status") or "Not declared"),
            "report_route": str(summary.get("terminal_route") or ""),
            "report_url": _source_url(task / "workflow/report.yaml", root),
            "execution": execution, "complete": counts["complete"], "total": len(owned),
            "reading": reading, "issues": list(dict.fromkeys(issues)), "runs": runs,
            "page_url": _page_url(page, board, root, "draft", only),
            "runs_url": _page_url(page, board, root, "runs", only),
            "folder_url": _page_url(page, board, root, "folderstat", only),
            "source_url": _source_url(page, root)}


# What a workspace file is, by suffix: data is named and sized, never linked (a raw extract is
# read through its Task, not opened in a browser); the rest opens in the shared pop-out.
_WS_KIND = {".parquet": "data", ".csv": "data", ".tsv": "data", ".feather": "data", ".pkl": "data",
            ".txt": "doc", ".md": "doc", ".json": "doc", ".yaml": "doc", ".yml": "doc",
            ".excalidraw": "drawing", ".png": "figure", ".svg": "figure", ".jpg": "figure", ".pdf": "figure",
            ".py": "script"}


def _size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def _ws_files(folder: Path, root: Path) -> list[dict]:
    """The files of one workspace folder and of its studio/ (one level each), by kind."""
    out = []
    for base in (folder, folder / "studio"):
        if not base.is_dir():
            continue
        for f in sorted(base.iterdir()):
            kind = _WS_KIND.get(f.suffix.lower())
            if not kind or not f.is_file() or f.name.startswith(".") or not _inside(f, root):
                continue
            rel = f.relative_to(root).as_posix()
            url = ("" if kind == "data" else
                   "/_excalidraw/?" + urlencode({"board": rel}) if kind == "drawing" else
                   "/" + quote(rel) if static_path_allowed(root, f) else "")
            out.append({"name": f.relative_to(folder).as_posix(), "kind": kind, "size": _size(f.stat().st_size),
                        "url": url})
    return out


def workspace_resources(board: Path, root: Path, jobs: list[dict], project: str) -> list[dict]:
    """The _WorkSpace folders this Block reads or writes, from its own declarations.

    A Job's `src/config-defaults.yaml` names its input: `raw_store` + `cohort` is one raw-store
    folder, and any other value starting with `_WorkSpace/` that is a folder counts too. Heavy Run
    output is `_WorkSpace/ProjectResult/<Project>/<Block path below tasks/>`. Read-only."""
    stores: dict[str, dict] = {}

    def add(folder: Path, role: str, job: str = ""):
        if not folder.is_dir() or not _inside(folder, root):
            return
        rel = folder.relative_to(root).as_posix()
        entry = stores.setdefault(rel, {"path": rel, "role": role, "jobs": [], "files": _ws_files(folder, root)})
        if job and job not in entry["jobs"]:
            entry["jobs"].append(job)

    for job in jobs:
        defaults = _yaml(board / job["name"] / "src" / "config-defaults.yaml", [], "Job defaults", board)
        if not isinstance(defaults, dict):
            continue
        if isinstance(defaults.get("raw_store"), str) and isinstance(defaults.get("cohort"), str):
            add(root / defaults["raw_store"] / defaults["cohort"], "input", job["name"])
        for key, value in defaults.items():
            if key != "raw_store" and isinstance(value, str) and value.startswith("_WorkSpace/"):
                add(root / value, "input", job["name"])
    tasks_dir = next((p for p in board.parents if p.name == "tasks"), None)
    if tasks_dir is not None and project:
        add(root / "_WorkSpace" / "ProjectResult" / project / board.relative_to(tasks_dir), "heavy output")
    return list(stores.values())


def task_board_snapshot(board: Path, root: Path, only=()) -> dict:
    board, root = board.resolve(), root.resolve()
    if not _inside(board, root) or not is_task_board(board):
        raise ValueError("Not a Task Block inside the served root")
    text = _read(board / "board.md", root)
    title = _TITLE.search(text)
    jobs, tasks = [], []
    for job in sorted(board.iterdir()):
        if not _JOB.match(job.name) or not job.is_dir() or not _inside(job, board):
            continue
        children = [task_snapshot(t, board, root, only) for t in sorted(job.iterdir())
                    if _TASK.fullmatch(t.name) and t.is_dir() and _inside(t, job)]
        jobs.append({"name": job.name, "id": job.name[:3],
                     "title": job.name[4:].replace("_", " "), "tasks": children})
        tasks.extend(children)
    runs = [dict(r, task_id=t["id"], task_title=t["title"], job=t["job"], runs_url=t["runs_url"])
            for t in tasks for r in t["runs"]]
    owner = project_owner(board, root)
    workspace = workspace_resources(board, root, jobs, owner.get("project") or "")
    snap = {"title": title.group(1) if title else board.name, "block": board.name,
            "project": owner["project"], "path": (board.relative_to(root) / "board.md").as_posix(),
            "spine": _field(text, "spine"), "close": _field(text, "close"),
            "source_url": _source_url(board / "board.md", root),
            "board_url": _source_url(board / "board/index.html", root),
            "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "jobs": jobs, "tasks": tasks, "runs": runs, "workspace": workspace,
            "totals": {"jobs": len(jobs), "tasks": len(tasks),
                       "complete": sum(t["complete"] for t in tasks), "runs": sum(t["total"] for t in tasks),
                       "attention": sum(bool(t["issues"]) for t in tasks)}}
    from live.task_questions import extend_snapshot
    return extend_snapshot(board, root, snap, only, _source_url, _page_url)


def _e(value) -> str:
    return html.escape(str(value), quote=True)


def _link(url: str, label: str) -> str:
    return f'<a href="{_e(url)}" target="_blank" rel="noopener">{_e(label)} ↗</a>' if url else ""


def _badge(state: str, label: str = "") -> str:
    labels = {"complete": "Runs complete", "attention": "Needs attention", "empty": "No runs"}
    return f'<span class="tw-badge tw-{_e(state)}">{_e(label or labels.get(state, state.capitalize()))}</span>'


def _task_html(task: dict) -> str:
    t = task
    warnings = "".join(f"<li>{_e(s)}</li>" for s in t["issues"])
    readings = "".join(f'<tr><td>{_e(r["id"])}</td><td>{_e(r["topic"])}</td>'
                       f'<td><code>{_e(r["verdict"])}</code></td><td>{_e(r["ruling"])}</td></tr>'
                       for r in t["reading"]["rows"])
    reading = f'{t["reading"]["signed"]}/{t["reading"]["total"]} signed' if t["reading"]["total"] else "Not recorded"
    search = " ".join((t["id"], t["title"], t["name"], *t["issues"]))
    return f'''<article class="tw-task" data-search="{_e(search.lower())}" data-job="{_e(t['job'])}" data-state="{t['execution']}" data-attention="{str(bool(t['issues'])).lower()}">
<details id="{_e(t['id'])}"><summary><div class="tw-task-name"><code>{_e(t['id'])}</code><strong>{_e(t['title'])}</strong></div>
<span class="tw-task-state">{_badge(t['execution'])}<span class="tw-muted">{len(t['issues'])} to review</span></span></summary>
<div class="tw-task-detail"><div class="tw-links">{_link(t['page_url'], 'Page')}{_link(t['runs_url'], 'Runs')}{_link(t['folder_url'], 'Folder')}{_link(t['source_url'], 'Source')}</div>
<p>Page state (declared): <strong>{_e(t['page_state'])}</strong></p>
{'<ul class="tw-findings">' + warnings + '</ul>' if warnings else '<p>No findings in this projection. Folder closure still requires the owning workflow and current Page CHECK.</p>'}
{'<div class="tw-table-scroll"><table><caption>READING · current</caption><thead><tr><th>ID</th><th>Topic</th><th>Verdict Run</th><th>Ruling</th></tr></thead><tbody>' + readings + '</tbody></table></div>' if readings else ''}
</div></details>
<div class="tw-stages"><div><small>Plan</small><span>{str(t['plan_specs']) + ' Run Specs' if t['plan_present'] else 'Not recorded'}</span>{_link(t['plan_url'], 'Plan')}</div>
<div><small>Build · files</small><span>{t['ticket_count']} Tickets · {t['config_count']} configs</span></div>
<div><small>Execute · Task Runs</small><span>{t['complete']}/{t['total']} complete</span><progress max="{max(t['total'], 1)}" value="{t['complete']}" aria-label="{_e(t['title'])}: Task Runs complete"></progress></div>
<div><small>Report · declared</small><span>{_e(t['report_status']) if t['report_present'] else 'Not recorded'}</span>{_link(t['report_url'], 'Report')}</div>
<div><small>Reading</small><span>{reading}</span></div></div></article>'''


def render_task_board(snap: dict, space="task") -> str:
    from live.task_views import render
    return render(snap, space)


class TaskBoardMixin:
    def task_board_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        raw = (query.get("path") or [""])[0]
        root = Path(self.root).resolve()
        board = resolve_task_board(root, raw)
        code, content_type = 200, "text/html; charset=utf-8"
        if board is None:
            links = "".join(f'<li><a href="/_board/task-board?{_e(urlencode({"path": (b.relative_to(root) / "board.md").as_posix()}))}">{_e(b.name)}</a></li>' for b in task_boards(root))
            code = 404 if raw else 200
            body = f'<!doctype html><meta charset="utf-8"><title>📋 Task · Blocks</title><h1>📋 Task · Blocks</h1><ul>{links or "<li>No Task Blocks under this root.</li>"}</ul>'
        else:
            snap = task_board_snapshot(board, Path(self.root), getattr(self, "only", ()))
            report_id = (query.get("report") or [""])[0]
            task_id, run_id = (query.get("task") or [""])[0], (query.get("run") or [""])[0]
            if task_id or run_id:
                task = next((t for t in snap["tasks"] if t["id"] == task_id), None)
                if not task or not any(r["detail_key"] == run_id for r in task["runs"]):
                    code, body = 404, '<h1>Run unavailable</h1><p>This Run is not present in the selected Task.</p>'
                else:
                    from live.task_run import render_task_run
                    page = board / task["job"] / task["name"] / (task["name"] + ".md")
                    try:
                        body = render_task_run(page, root, run_id)
                    except (OSError, ValueError) as error:
                        code, body = 400, '<h1>Run unavailable</h1><p>' + _e(error) + '</p>'
            elif report_id:
                report = next((q["report"] for q in snap["questions"] if q["id"] == report_id), None)
                if not report or not report["url"]:
                    code, body = 404, '<h1>Report unavailable</h1><p>Open its Task card to see the source findings.</p>'
                else:
                    from live.task_views import render_report
                    try:
                        body = render_report(report, board, root, snap["path"])
                    except (OSError, ValueError) as error:
                        code, body = 400, '<h1>Report unavailable</h1><p>' + _e(error) + '</p>'
            elif (query.get("format") or [""])[0] == "json":
                content_type = "application/json; charset=utf-8"
                body = json.dumps(snap, ensure_ascii=False)
            else:
                body = render_task_board(snap, (query.get("view") or query.get("space") or ["task"])[0])
        encoded = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(encoded)

    def plug_task_board(self, payload):
        root = Path(self.root).resolve()
        board = resolve_task_board(root, payload.get("path"))
        if board is None:
            return None, "path must identify a Task Block with board-kind: task-block"
        action = payload.get("action")
        if action == "add-resource":
            from argparse import Namespace
            import importlib.util
            script = Path(__file__).resolve().parents[2] / "skills/question/haipipe-question/ref/block_questions.py"
            values = {name: payload.get(name, "") for name in ("title", "url", "contribution", "notes")}
            ids = payload.get("questions", [])
            if (any(not isinstance(value, str) or len(value) > 10000 for value in values.values())
                    or not isinstance(ids, list) or any(not isinstance(value, str) for value in ids)):
                return None, "Invalid resource fields"
            try:
                spec = importlib.util.spec_from_file_location("task_question_author", script)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                module.update(Namespace(command="add-resource", block=board, question=ids, **values))
            except (OSError, ValueError) as error:
                return None, str(error)
        elif action:
            return None, "Unknown Task Workbench action"
        return {"url": "/_board/task-board?" + urlencode({"path": (board.relative_to(root) / "board.md").as_posix()})}, None
