"""CoWork Block workbench: one cowork/bNN_<topic>/ Block, or every Block of a Project.

Reads the Block's board.md (header lines, Questions, Related resources), its Jobs
(jNN_<job>/: the job page header, Timeline.md, CHECKLIST.md, emails/, meetings/, design/,
materials/) and its studio/ and reports/ on every open, and stores nothing. Questions and report Pages reuse the Task Workbench's reader
(live.task_questions); the page reuses its look and script (cowork_views.py).
"""
from __future__ import annotations

from datetime import date, datetime, timezone
import html
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlencode, urlparse, urlsplit

from host_registry import static_path_allowed
from live.home import _manifests, project_owner
from live.task_questions import QUESTION_ID, field, generated, inside, read, register, report_snapshot, words
from live.taskboard import _page_url, _source_url

ROUTE = "/_board/cowork-board"
KIND = "cowork-block"
_TITLE = re.compile(r"^#\s+(.+)$", re.M)
_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")
_STEP = re.compile(r"^\s*- \[( |x|X)\]\s*(?:(\d+)\.)?\s*(.*)$")
_TEXT = {".md", ".txt"}
_MAX_FILES = 300
_VIDEO = (".mp4", ".m4v", ".webm", ".mov")
_YOUTUBE = re.compile(r"https?://(?:www\.|m\.)?(?:youtube\.com/(?:watch\?(?:[^#]*?&)?v=|shorts/|embed/)|youtu\.be/)"
                      r"([\w-]{11})")


def is_cowork_board(board: Path) -> bool:
    return field(read(board / "board.md", board), "board-kind") == KIND


def cowork_boards(root: Path, within: Path | None = None) -> list[Path]:
    root = root.resolve()
    found = {m.parent for m in _manifests(within or root)
             if inside(m, root) and is_cowork_board(m.parent)}
    return sorted(found)


def resolve(root: Path, raw: str):
    """A request path -> ("block", Block) · ("project", its cowork/ folder) · ("all", root) · (None, None)."""
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
    if target.is_dir() and target.name == "cowork":
        return "project", target
    if target.name == "README.md" and target.parent.name == "cowork":
        return "project", target.parent
    for candidate in (target, *target.parents):
        if not candidate.is_relative_to(root):
            break
        if (candidate / "board.md").is_file():
            return ("block", candidate) if is_cowork_board(candidate) else (None, None)
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


def _iso(value) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()[:10]
    return words(value) if isinstance(value, str) else ("" if value is None else str(value))


def waited(since: str, today: date | None = None):
    try:
        return ((today or date.today()) - date.fromisoformat(since[:10])).days
    except (TypeError, ValueError):
        return None


_JOB = re.compile(r"j\d{2}_[a-z0-9]+(?:_[a-z0-9]+)*")
DONE, REFERENCE = "✅", "📇"            # a done Job and a reference Job (j00_people) are not open work


def notes(folder: Path, board: Path, root: Path, job: str = "") -> list[dict]:
    """Emails or meeting notes: one .md/.txt each, newest first; a draft is marked."""
    out = []
    if not folder.is_dir() or not inside(folder, board):
        return out
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.name.startswith(".") or path.suffix.lower() not in _TEXT:
            continue
        text = read(path, board)
        title = next((line.lstrip("# ").strip() for line in text.splitlines()
                      if line.strip() and not set(line.strip()) <= set("=-")), path.stem)
        found = _DATE.search(path.name)
        out.append({"name": path.name, "title": title[:140], "date": found.group(1) if found else "", "job": job,
                    "draft": "draft" in path.name.lower() or bool(re.search(r"(?mi)^status:\s*draft\b", text[:3000])),
                    "url": file_url(board, path, root)})
    out.sort(key=lambda n: (n["date"], n["name"]), reverse=True)
    return out


def steps(path: Path, board: Path, job: str = "") -> list[dict]:
    """A CHECKLIST.md's steps: `- [ ] 9. text` open, `- [x]` done, in file order; wrapped lines joined."""
    out, current = [], None
    for line in read(path, board).splitlines():
        found = _STEP.match(line)
        if found:
            current = {"done": found.group(1).lower() == "x", "number": found.group(2) or "", "job": job,
                       "text": found.group(3).replace("**", "").strip()}
            out.append(current)
        elif current is not None and line.startswith(" ") and line.strip() and not line.strip().startswith("- "):
            current["text"] += " " + line.strip().replace("**", "")      # the step's own wrapped line
        else:
            current = None                                                 # a sub-point or a blank ends it
    for step in out:
        step["text"] = step["text"][:240]
    return out


def files(folder: Path, board: Path, root: Path) -> list[dict]:
    out = []
    if not folder.is_dir() or not inside(folder, board):
        return out
    for path in sorted(folder.rglob("*")):
        if len(out) >= _MAX_FILES:
            break
        rel = path.relative_to(folder)
        if (not path.is_file() or any(p.startswith(".") or p == "_build" for p in rel.parts)
                or len(rel.parts) > 3 or not static_path_allowed(root, path)):
            continue
        out.append({"name": rel.as_posix(), "url": file_url(board, path, root)})
    return out


def jobs(board: Path, root: Path) -> tuple[list[dict], list[str]]:
    """Each jNN_<job>/ of the Block: its page header (state, waiting-on, since, next, ticket, url),
    its Timeline and Checklist, and its emails, meetings, design notes and materials."""
    out, issues = [], []
    for folder in sorted(board.iterdir()):
        if not (folder.is_dir() and _JOB.fullmatch(folder.name) and inside(folder, board)):
            continue
        page = folder / f"{folder.name}.md"
        text = read(page, board)
        if not text:
            issues.append(f"{folder.name}/ has no job page {folder.name}.md")
        elif field(text, "job-kind") != "cowork-job":
            issues.append(f"{folder.name}/{folder.name}.md does not declare job-kind: cowork-job")
        title = _TITLE.search(text)
        link = field(text, "url")
        since = field(text, "since")
        state = field(text, "state")
        out.append({"id": folder.name[:3], "name": folder.name, "title": title.group(1).strip() if title else folder.name,
                    "state": state, "open": not state.startswith((DONE, REFERENCE)), "waiting": field(text, "waiting-on") or "us",
                    "since": since, "days": waited(since), "next": field(text, "next"), "ticket": field(text, "ticket"),
                    "url": link if urlsplit(link).scheme in {"http", "https"} else "",
                    "page_url": file_url(board, page, root),
                    "timeline_url": file_url(board, folder / "Timeline.md", root),
                    "checklist_url": file_url(board, folder / "CHECKLIST.md", root),
                    "steps": steps(folder / "CHECKLIST.md", board, folder.name),
                    "emails": notes(folder / "emails", board, root, folder.name),
                    "meetings": notes(folder / "meetings", board, root, folder.name),
                    "design": files(folder / "design", board, root),
                    "materials": files(folder / "materials", board, root)})
    return out, issues



def _drawing_png(url: str, root: Path) -> str:
    """The .png beside a drawing opened as /_excalidraw/?board=<path>, when it exists."""
    rel = (parse_qs(urlparse(url).query).get("board") or [""])[0]
    png = root / (rel[:-len(".excalidraw")] + ".png") if rel.endswith(".excalidraw") else None
    return _source_url(png, root) if png is not None and png.is_file() else ""

def questions(text: str, board: Path, root: Path, only) -> tuple[list[dict], list[str]]:
    rows, issues = register(text, "Questions", "questions")
    out, seen = [], set()
    for row in rows:
        qid = words(row.get("id"))
        if not QUESTION_ID.fullmatch(qid) or qid in seen or not words(row.get("question")):
            issues.append(f"Invalid or duplicate Question: {qid or '(missing id)'}")
            continue
        seen.add(qid)
        question = {"id": qid, "title": words(row.get("title")) or row["question"], "question": row["question"],
                    "aim": words(row.get("aim")), "hypothesis": words(row.get("hypothesis")),
                    "acceptance": words(row.get("acceptance")), "group": words(row.get("group")),
                    "work": [], "issues": []}
        work = row.get("work", [])
        for entry in work if isinstance(work, list) else []:
            path = entry if isinstance(entry, str) else words(entry.get("path")) if isinstance(entry, dict) else ""
            target = board / path
            if not path or not inside(target, board) or not target.is_file():
                question["issues"].append(f"Work must name a file inside the Block: {path}")
                continue
            question["work"].append({"path": path, "role": words(entry.get("role")) if isinstance(entry, dict) else "",
                                     "url": file_url(board, target, root)})
        report = report_snapshot(row.get("report"), qid, board, root, only, _source_url, _page_url)
        report["url"] = report["url"].replace("/_board/work-board?", ROUTE + "?")
        # The report's one drawing (task_questions.report_snapshot keeps one) shows as its .png beside it;
        # a picture is never a second thumb: it goes inside the drawing (JL 261005).
        report["thumbs"] = [{"title": d["title"], "url": d["url"], "png": d["png"] if "png" in d else _drawing_png(d["url"], root)}
                            for d in report["drawings"]]
        # A video the report links to plays in the row itself (JL 261004: "in the workbench").
        report["videos"] = [{"title": link["title"], "url": link["url"]} for link in report["evidence"]
                            if link["mtime"] is not None and link["path"].lower().endswith(_VIDEO)]
        # ... and a YouTube link plays through YouTube's own embedded player.
        report["videos"] += [{"title": link["title"], "url": link["url"],
                              "embed": "https://www.youtube-nocookie.com/embed/" + _YOUTUBE.match(link["url"]).group(1)}
                             for link in report["evidence"] if _YOUTUBE.match(link["url"] or "")]
        question["report"] = report
        out.append(question)
    return out, issues


def onedrive(raw: str, root: Path) -> list[dict]:
    """The `onedrive:` header: SPACE-relative folders of the shared drive, comma separated. Their
    files sit outside the served root (a OneDrive shortcut), so they are named, never linked."""
    out = []
    for item in (part.strip() for part in raw.split(",") if part.strip()):
        folder = root / item
        if item.startswith("/") or ".." in Path(item).parts or not folder.is_dir():
            out.append({"path": item, "files": [], "missing": True})
            continue
        names = []
        for path in sorted(folder.rglob("*")):
            rel = path.relative_to(folder)
            if len(names) >= _MAX_FILES:
                break
            if path.is_file() and len(rel.parts) <= 2 and not any(p.startswith((".", "~$")) for p in rel.parts):
                names.append(rel.as_posix())
        out.append({"path": item, "files": names, "missing": False})
    return out


def drawings(board: Path, root: Path) -> list[dict]:
    out = []
    studio = board / "studio"
    if inside(studio, board) and studio.is_dir():
        for path in sorted(studio.glob("*.excalidraw")):
            if inside(path, studio) and path.is_file() and _source_url(path, root):
                out.append({"title": path.stem.replace("_", " ").replace("-", " ").capitalize(),
                             "path": path.relative_to(root).as_posix(), **generated(path, board)})
    return out


def header(text: str, board: Path) -> dict:
    title = _TITLE.search(text)
    return {"title": title.group(1).strip() if title else board.name, "block": board.name,
            **{key.replace("-", "_"): field(text, key)
               for key in ("state", "owner", "spine", "close", "status", "waits-for", "onedrive")}}


def people_page(board: Path) -> Path:
    page = board / "j00_people" / "j00_people.md"
    return page if page.is_file() else board / "PEOPLE.md"


def block_snapshot(board: Path, root: Path, only=()) -> dict:
    board, root = board.resolve(), root.resolve()
    if not inside(board, root) or not is_cowork_board(board):
        raise ValueError("Not a CoWork Block inside the served root")
    text = read(board / "board.md", board)
    job_rows, job_issues = jobs(board, root)
    question_rows, question_issues = questions(text, board, root, only)
    resources, resource_issues = register(text, "Related resources", "resources")
    clean = [{"title": words(r.get("title")), "url": words(r.get("url")),
              "questions": [q for q in r.get("questions", []) if isinstance(q, str)] if isinstance(r.get("questions"), list) else [],
              "contribution": words(r.get("contribution")), "notes": words(r.get("notes"))}
             for r in resources if words(r.get("title")) and urlsplit(words(r.get("url"))).scheme in {"http", "https"}]
    owner = project_owner(board, root)
    head = header(text, board)
    def every(key):
        return sorted((x for j in job_rows for x in j[key]), key=lambda n: (n["date"], n["name"]), reverse=True)
    return {**head, "onedrive_folders": onedrive(head["onedrive"], root), "project": owner.get("project") or "",
            "path": board_path(board, root), "source_url": _source_url(board / "board.md", root),
            # who to ask: the j00_people Job (JL 261004), else an older Block's PEOPLE.md
            "people_url": file_url(board, people_page(board), root), "people": read(people_page(board), board),
            "jobs": job_rows, "emails": every("emails"), "meetings": every("meetings"),
            "steps": [s for j in job_rows for s in j["steps"]],
            "questions": question_rows, "resources": clean, "drawings": drawings(board, root),
            "studio_path": (board.relative_to(root) / "studio").as_posix(), "studio_enabled": not only,
            "source_issues": job_issues + question_issues + resource_issues,
            "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}


def projects_snapshot(root: Path, folder: Path | None = None) -> list[dict]:
    """Every cowork Block (of one Project's cowork/ folder, or under root), grouped by Project."""
    root = root.resolve()
    groups: dict[str, dict] = {}
    for board in cowork_boards(root, folder):
        text = read(board / "board.md", board)
        rows, _ = jobs(board, root)
        open_rows = [j for j in rows if j["open"]]
        owner = project_owner(board, root)
        name = owner.get("project") or board.parent.parent.name
        group = groups.setdefault(name, {"project": name, "cowork": board.parent.relative_to(root).as_posix(), "blocks": []})
        group["blocks"].append({**header(text, board), "url": ROUTE + "?" + urlencode({"path": board_path(board, root)}),
                                "open": len(open_rows), "jobs": open_rows})
    return list(groups.values())


_MD_HEADING = re.compile(r"^#{1,4}\s+\S", re.M)


def render_file(board: Path, root: Path, raw: str, path_label: str) -> tuple[int, str]:
    """One text file of the Block for the pop-out: a .md written in Markdown (it has # headings) is rendered,
    as the Task Workbench renders Result files; anything else, including plain-text notes with underlined
    titles, is shown as written."""
    target = (board / raw).resolve() if isinstance(raw, str) and "\x00" not in raw else None
    if (target is None or not inside(target, board) or not target.is_file()
            or target.suffix.lower() not in _TEXT or not static_path_allowed(root, target)):
        return 404, '<!doctype html><meta charset="utf-8"><h1>File unavailable</h1>'
    body = read(target, board)
    rel = target.relative_to(board).as_posix()
    back = ROUTE + "?" + urlencode({"path": path_label})
    if target.suffix.lower() == ".md" and _MD_HEADING.search(body):
        from live.paper import _md_view
        plain = re.sub(r"(?m)^\s*(?:-{3,}|\*{3,})\s*$", "", body)     # divider lines read as gaps
        plain = re.sub(r"(?m)^\s*>\s?", "", plain)                     # quote markers are dropped
        content = f'<main class=md>{_md_view(plain)}</main>'
    else:
        content = f'<pre>{html.escape(body)}</pre>'
    return 200, (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
                 f'content="width=device-width,initial-scale=1"><title>{html.escape(rel)}</title><style>'
                 'body{font:15px/1.55 ui-sans-serif,system-ui,sans-serif;margin:0;background:#fff;color:#1f2328}'
                 'header{padding:10px 18px;border-bottom:1px solid #d0d7de;display:flex;gap:14px;align-items:baseline}'
                 'header a{color:#0969da;text-decoration:none}code{font:13px ui-monospace,monospace}'
                 'pre{margin:0;padding:16px 18px;white-space:pre-wrap;word-break:break-word;font:13.5px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace}'
                 'main.md{padding:8px 22px 24px;max-width:960px}main.md h3{font-size:1.45em;margin:18px 0 8px}'
                 'main.md h4{font-size:1.2em;margin:18px 0 6px}main.md h5,main.md h6{font-size:1.05em;margin:14px 0 4px}'
                 'main.md table{border-collapse:collapse;margin:8px 0}main.md th,main.md td{border:1px solid #d0d7de;padding:4px 8px;text-align:left;vertical-align:top}'
                 'main.md pre{background:#f6f8fa;border-radius:6px;padding:10px 12px}main.md li{margin:2px 0}'
                 f'</style></head><body><header><a href="{html.escape(back)}">← CoWork</a><code>{html.escape(rel)}</code></header>'
                 f'{content}</body></html>')


class CoworkBoardMixin:
    def cowork_board_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        raw = (query.get("path") or [""])[0]
        root = Path(self.root).resolve()
        only = getattr(self, "only", ())
        kind, target = resolve(root, raw)
        code, content_type = 200, "text/html; charset=utf-8"
        from live.cowork_views import render_block, render_projects, render_report
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
                body = json.dumps(snap, ensure_ascii=False)
            else:
                body = render_block(snap, (query.get("view") or query.get("space") or ["work"])[0])
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

    def plug_cowork_board(self, payload):
        root = Path(self.root).resolve()
        kind, board = resolve(root, payload.get("path") or "")
        if kind != "block":
            return None, "path must identify a CoWork Block with board-kind: cowork-block"
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
                spec = importlib.util.spec_from_file_location("cowork_question_author", script)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                module.update(Namespace(command="add-resource", block=board, question=ids, **values))
            except (OSError, ValueError) as error:
                return None, str(error)
        elif action:
            return None, "Unknown CoWork Workbench action"
        return {"url": ROUTE + "?" + urlencode({"path": board_path(board, root)})}, None
