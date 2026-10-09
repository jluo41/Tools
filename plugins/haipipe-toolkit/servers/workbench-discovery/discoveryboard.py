"""Discovery Block workbench: one discoveries/bNN_<block>/ Block, or every Block of a Project.

A Discovery Block has the Task shape (Block → Job → Task Page → Paper Run), so Task Pages
and their Runs are read with the Task Workbench's reader (live.taskboard.task_snapshot);
this adds what a Paper Run left: its Result card, receipt fields and one-entry BibTeX.
Reads on every open and stores nothing. Drawn by discovery_views.py in the Task style.
"""
from __future__ import annotations

from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlencode, urlparse, urlsplit

import yaml

from host_registry import static_path_allowed
from live.home import _manifests, project_owner
from live.task_questions import extend_snapshot, field, inside, read, section
from live.taskboard import _page_url, _source_url, task_snapshot
from src.themes import kind_of as theme_kind_of

ROUTE = "/_board/discovery-board"
KIND = "discovery-block"
_TITLE = re.compile(r"^#\s+(.+)$", re.M)
_JOB = re.compile(r"^j\d{2}_[a-z0-9_]+$", re.I)
_TASK = re.compile(r"^t\d{2}_[a-z0-9_]+$", re.I)
_RUN = re.compile(r"^rp?\d{2}_[\w.-]+$")
_BULLET = re.compile(r"(?m)^- (cite|subject|venue|verification|run):[ \t]*(.+)$")
_TEXT = {".md", ".txt", ".bib", ".yaml", ".yml", ".sh"}
SYNTHESIS = ("summary.md", "verdict.md", "landscape.md")
TASK_ONLY = ("READING",)          # Task-Page findings that do not apply to a Discovery Task Page


def is_discovery_board(board: Path) -> bool:
    return field(read(board / "board.md", board), "board-kind") == KIND


def discovery_boards(root: Path, within: Path | None = None) -> list[Path]:
    root = root.resolve()
    return sorted({m.parent for m in _manifests(within or root)
                   if inside(m, root) and is_discovery_board(m.parent)})


def resolve(root: Path, raw: str):
    """A request path -> ("block", Block) · ("project", its discoveries/ folder) · ("all", root) · (None, None)."""
    root = root.resolve()
    if not isinstance(raw, str) or "\x00" in raw:
        return None, None
    if not raw:
        return "all", root
    try:
        target = (root / raw.split("?", 1)[0].split("#", 1)[0].lstrip("/")).resolve()
    except (OSError, ValueError, RuntimeError):
        return None, None
    if not target.is_relative_to(root):
        return None, None
    if target.is_dir() and theme_kind_of(target.name) == "discovery":   # discovery/ or discoveries/
        return "project", target
    for candidate in (target, *target.parents):
        if not candidate.is_relative_to(root):
            break
        if (candidate / "board.md").is_file():
            return ("block", candidate) if is_discovery_board(candidate) else (None, None)
    return None, None


def board_path(board: Path, root: Path) -> str:
    return (board.relative_to(root) / "board.md").as_posix()


def file_url(board: Path, path: Path, root: Path) -> str:
    """A Block file in the pop-out: text through this workbench's reader, anything else as itself."""
    if not inside(path, board) or not path.is_file():
        return ""
    if path.suffix.lower() in _TEXT:
        return ROUTE + "?" + urlencode({"path": board_path(board, root), "show": path.relative_to(board).as_posix()})
    return _source_url(path, root)


def _receipt(path: Path, board: Path) -> dict:
    try:
        data = yaml.safe_load(read(path, board)) or {}
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def run_results(task: Path) -> list[tuple[str, Path]]:
    """(run, Result folder) for each Paper Run of a Task: runs/<run>/result/, or the older results/<run>/."""
    found = {}
    if (task / "results").is_dir():
        found.update((r.name, r) for r in (task / "results").iterdir() if r.is_dir() and _RUN.match(r.name))
    if (task / "runs").is_dir():
        found.update((r.name, r / "result") for r in (task / "runs").iterdir()
                     if r.is_dir() and _RUN.match(r.name) and (r / "result").is_dir())
    return sorted(found.items())


def paper(result: Path, board: Path, root: Path, task: dict, name: str = "") -> dict:
    """One Paper Run's Result: its card's title and lines, its receipt's status and analysis."""
    name = name or result.name
    card = result / f"{name}.md"
    text = read(card, board)
    lines = dict((k, v.strip()) for k, v in _BULLET.findall(text))
    title = _TITLE.search(text)
    receipt = _receipt(result / "runtime.yaml", board)
    subject = receipt.get("subject") if isinstance(receipt.get("subject"), dict) else {}
    analysis = receipt.get("analysis") if isinstance(receipt.get("analysis"), dict) else {}
    readout = section(text, "Readout").split("\n\n", 1)[0].strip()
    bib = result / f"{name}.bib"
    url = lines.get("subject", "") or str(subject.get("canonical_url") or "")
    verification = lines.get("verification", "") or "not stated"
    return {"run": name, "id": name.split("_", 1)[0], "task_id": task["id"], "task": task["name"], "job": task["job"],
            "title": (title.group(1).strip() if title else str(subject.get("title") or name))[:200],
            "cite": lines.get("cite", ""), "venue": lines.get("venue", ""), "verification": verification,
            "subject_url": url if urlsplit(url).scheme in {"http", "https"} else "",
            "subject_kind": str(subject.get("kind") or ""), "status": str(receipt.get("status") or "no receipt"),
            "reading_depth": str(analysis.get("reading_depth") or ""),
            "claim_support": str(analysis.get("claim_support") or ""),
            "readout": re.sub(r"\s+", " ", readout)[:400],
            "card_url": file_url(board, card, root), "bib_url": file_url(board, bib, root),
            "bib": read(bib, board) if bib.is_file() else "",
            "needs_person": verification.upper().startswith("NEEDS") or (
                bool(analysis.get("claim_support")) and str(analysis.get("claim_support")) != "supported")}


def task_row(task: Path, board: Path, root: Path, only) -> dict:
    snap = task_snapshot(task, board, root, only)
    snap["issues"] = [i for i in snap["issues"] if not any(word in i for word in TASK_ONLY)]
    spec = _receipt(task / "discovery.yaml", board)
    snap["discovery_type"] = str(spec.get("discovery_type") or "")
    snap["synthesis"] = [{"name": n, "url": file_url(board, task / n, root)} for n in SYNTHESIS if (task / n).is_file()]
    snap["papers"] = [paper(r, board, root, snap, name) for name, r in run_results(task) if inside(r, task)]
    for run in snap["runs"]:                        # a Run opens this workbench's view of its card
        found = next((p for p in snap["papers"] if p["run"] == run["name"]), None)
        run["result_url"] = found["card_url"] if found and found["card_url"] else run.get("receipt_url", "")
    return snap


def header(text: str, board: Path) -> dict:
    title = _TITLE.search(text)
    return {"title": title.group(1).strip() if title else board.name, "block": board.name,
            **{key: field(text, key) for key in ("state", "owner", "spine", "close")}}


def block_snapshot(board: Path, root: Path, only=()) -> dict:
    board, root = board.resolve(), root.resolve()
    if not inside(board, root) or not is_discovery_board(board):
        raise ValueError("Not a Discovery Block inside the served root")
    text = read(board / "board.md", board)
    jobs, tasks = [], []
    for job in sorted(board.iterdir()):
        if not (job.is_dir() and _JOB.match(job.name) and inside(job, board)):
            continue
        spec = {}
        children = [task_row(t, board, root, only) for t in sorted(job.iterdir())
                    if t.is_dir() and _TASK.fullmatch(t.name) and inside(t, job)]
        if children:
            spec = _receipt(job / children[0]["name"] / "discovery.yaml", board).get("job") or {}
        jobs.append({"name": job.name, "id": job.name[:3], "tasks": children,
                     "title": (spec.get("title") if isinstance(spec, dict) else "") or job.name[4:].replace("_", " ")})
        tasks.extend(children)
    papers = [p for t in tasks for p in t["papers"]]
    runs = [dict(r, task_id=t["id"], task_title=t["title"], job=t["job"], runs_url=t["runs_url"])
            for t in tasks for r in t["runs"]]
    owner = project_owner(board, root)
    snap = {**header(text, board), "project": owner.get("project") or "", "path": board_path(board, root),
            "source_url": _source_url(board / "board.md", root), "jobs": jobs, "tasks": tasks, "runs": runs,
            "papers": papers, "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "totals": {"jobs": len(jobs), "tasks": len(tasks), "papers": len(papers),
                       "complete": sum(r["status"] == "complete" for r in runs),
                       "blocked": sum(r["status"] in ("blocked", "failed", "missing") for r in runs),
                       "needs_person": sum(p["needs_person"] for p in papers),
                       "bib": sum(bool(p["bib"]) for p in papers)}}
    snap = extend_snapshot(board, root, snap, only, _source_url, _page_url)
    for question in snap["questions"]:
        question["report"]["url"] = question["report"]["url"].replace("/_board/work-board?", ROUTE + "?")
    return snap


def projects_snapshot(root: Path, folder: Path | None = None) -> list[dict]:
    """Every Discovery Block (of one Project's discoveries/ folder, or under root), grouped by Project.
    Counts come from the tree, not from reading every Result, so the page stays quick."""
    root = root.resolve()
    groups: dict[str, dict] = {}
    for board in discovery_boards(root, folder):
        text = read(board / "board.md", board)
        tasks = [t for j in board.iterdir() if j.is_dir() and _JOB.match(j.name)
                 for t in j.iterdir() if t.is_dir() and _TASK.fullmatch(t.name)]
        results = [r for t in tasks for r in run_results(t)]
        owner = project_owner(board, root)
        name = owner.get("project") or board.parent.parent.name
        group = groups.setdefault(name, {"project": name, "folder": board.parent.relative_to(root).as_posix(), "blocks": []})
        group["blocks"].append({**header(text, board), "url": ROUTE + "?" + urlencode({"path": board_path(board, root)}),
                                "jobs": sum(1 for j in board.iterdir() if j.is_dir() and _JOB.match(j.name)),
                                "tasks": len(tasks), "papers": len(results)})
    return list(groups.values())


def render_file(board: Path, root: Path, raw: str, path_label: str) -> tuple[int, str]:
    """One text file of the Block (a card, a receipt, a ticket, a .bib), as written, for the pop-out."""
    target = (board / raw).resolve() if isinstance(raw, str) and "\x00" not in raw else None
    if (target is None or not inside(target, board) or not target.is_file()
            or target.suffix.lower() not in _TEXT or not static_path_allowed(root, target)):
        return 404, '<!doctype html><meta charset="utf-8"><h1>File unavailable</h1>'
    rel = target.relative_to(board).as_posix()
    back = ROUTE + "?" + urlencode({"path": path_label})
    return 200, (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
                 f'content="width=device-width,initial-scale=1"><title>{html.escape(rel)}</title><style>'
                 'body{font:15px/1.55 ui-sans-serif,system-ui,sans-serif;margin:0;background:#fff;color:#1f2328}'
                 'header{padding:10px 18px;border-bottom:1px solid #d0d7de;display:flex;gap:14px;align-items:baseline}'
                 'header a{color:#0969da;text-decoration:none}code{font:13px ui-monospace,monospace}'
                 'pre{margin:0;padding:16px 18px;white-space:pre-wrap;word-break:break-word;font:13.5px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace}'
                 f'</style></head><body><header><a href="{html.escape(back)}">← Discovery</a><code>{html.escape(rel)}</code></header>'
                 f'<pre>{html.escape(read(target, board))}</pre></body></html>')


class DiscoveryBoardMixin:
    def discovery_board_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        raw = (query.get("path") or [""])[0]
        root = Path(self.root).resolve()
        only = getattr(self, "only", ())
        kind, target = resolve(root, raw)
        code, content_type = 200, "text/html; charset=utf-8"
        from live.discovery_views import render_block, render_projects, render_report
        if kind == "block":
            snap = block_snapshot(target, root, only)
            # `show=` names a Block file for the pop-out; `file=board.md`, which /w/ adds, is the Block itself
            wanted, report_id = (query.get("show") or [""])[0], (query.get("report") or [""])[0]
            if wanted:
                code, body = render_file(target, root, wanted, snap["path"])
            elif report_id:
                report = next((q["report"] for q in snap["questions"] if q["id"] == report_id), None)
                if not report or not report["present"]:
                    code, body = 404, '<h1>Report unavailable</h1><p>This Question has no report Page yet.</p>'
                else:
                    try:
                        body = render_report(report, target, root, snap["path"])
                    except (OSError, ValueError) as error:
                        code, body = 400, '<h1>Report unavailable</h1><p>' + html.escape(str(error)) + '</p>'
            elif (query.get("format") or [""])[0] == "json":
                content_type = "application/json; charset=utf-8"
                body = json.dumps(snap, ensure_ascii=False, default=str)
            else:
                body = render_block(snap, (query.get("view") or query.get("space") or ["papers"])[0])
        elif kind in ("project", "all"):
            body = render_projects(projects_snapshot(root, target if kind == "project" else None),
                                   target.relative_to(root).as_posix() if kind == "project" else "")
        else:
            code = 404
            body = render_projects(projects_snapshot(root), "", missing=raw)
        encoded = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(encoded)

    def plug_discovery_board(self, payload):
        root = Path(self.root).resolve()
        kind, board = resolve(root, payload.get("path") or "")
        if kind != "block":
            return None, "path must identify a Discovery Block with board-kind: discovery-block"
        action = payload.get("action")
        if action == "add-resource":
            from argparse import Namespace
            import importlib.util
            from host_paths import skill_dir
            script = skill_dir("haipipe-question") / "ref/block_questions.py"
            values = {name: payload.get(name, "") for name in ("title", "url", "contribution", "notes")}
            ids = payload.get("questions", [])
            if (any(not isinstance(value, str) or len(value) > 10000 for value in values.values())
                    or not isinstance(ids, list) or any(not isinstance(value, str) for value in ids)):
                return None, "Invalid resource fields"
            try:
                spec = importlib.util.spec_from_file_location("discovery_question_author", script)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                module.update(Namespace(command="add-resource", block=board, question=ids, **values))
            except (OSError, ValueError) as error:
                return None, str(error)
        elif action:
            return None, "Unknown Discovery Workbench action"
        return {"url": ROUTE + "?" + urlencode({"path": board_path(board, root)})}, None
