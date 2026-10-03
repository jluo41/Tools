"""Block-authored Questions and Page-owned answers; no execution allocation."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import tomllib
from urllib.parse import unquote, urlsplit, urlencode

import yaml

QUESTION_ID = re.compile(r"Q[0-9]{2,}")
PAGE_STEM = re.compile(r"q[0-9]{2,}_[a-z0-9][a-z0-9_]*")
MAX_TEXT = 1024 * 1024


def inside(path, root):
    try:
        return Path(path).resolve().is_relative_to(Path(root).resolve())
    except (OSError, RuntimeError, ValueError):
        return False


def read(path, root):
    try:
        if not inside(path, root) or path.stat().st_size > MAX_TEXT:
            return ""
        return path.read_text(encoding="utf-8")
    except (OSError, ValueError, UnicodeError):
        return ""


def field(text, name):
    # Metadata belongs to the Page header, never a quoted passage in Content.
    header = re.split(r"^##\s", text, maxsplit=1, flags=re.M)[0]
    match = re.search(rf"^{re.escape(name)}:[ \t]*(.*)$", header, re.M)
    return match.group(1).strip() if match else ""


def section(text, heading):
    match = re.search(rf"(?m)^## {re.escape(heading)}[ \t]*$", text)
    if not match:
        return ""
    return re.split(r"^## ", text[match.end():], maxsplit=1, flags=re.M)[0].strip()


def register(text, heading, key):
    """Read one optional fenced YAML register without reformatting board.md."""
    if len(re.findall(rf"(?m)^## {re.escape(heading)}[ \t]*$", text)) > 1:
        return [], [f"{heading}: duplicate sections"]
    body = section(text, heading)
    if not body:
        return [], []
    blocks = re.findall(r"(?ms)^```ya?ml[ \t]*\n(.*?)^```[ \t]*$", body)
    if len(blocks) != 1:
        return [], [f"{heading}: expected one YAML block"]
    try:
        data = yaml.safe_load(blocks[0])
    except yaml.YAMLError:
        return [], [f"{heading}: invalid YAML"]
    if not isinstance(data, dict) or not isinstance(data.get(key), list):
        return [], [f"{heading}: {key} must be a list"]
    if any(not isinstance(row, dict) for row in data[key]):
        return [], [f"{heading}: each entry must be a mapping"]
    return data[key], []


def replace_register(text, heading, key, rows):
    """Replace only the designated YAML fence; preserve surrounding narrative."""
    fence = "```yaml\n" + yaml.safe_dump({key: rows}, sort_keys=False, allow_unicode=True) + "```"
    match = re.search(rf"(?m)^## {re.escape(heading)}[ \t]*$", text)
    if not match:
        return text.rstrip() + f"\n\n## {heading}\n\n{fence}\n"
    _, errors = register(text, heading, key)
    if errors:
        raise ValueError("; ".join(errors))
    end = re.search(r"(?m)^## ", text[match.end():])
    stop = match.end() + end.start() if end else len(text)
    body = text[match.end():stop]
    body = (re.sub(r"(?ms)^```ya?ml[ \t]*\n.*?^```[ \t]*$", lambda _: fence, body, count=1)
            if body.strip() else '\n\n' + fence + '\n\n')
    return text[:match.end()] + body + text[stop:]


def words(value):
    return value.strip() if isinstance(value, str) else ""


def plain(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"(?m)^\s*(?:#{1,6} |>|\*\*(?:Division map|Where this Page sits|Why it matters):).*?$", "", text)
    return re.sub(r"\s+", " ", text.replace("**", "").replace("`", "")).strip()


def report_section(text, names):
    body = section(text, "Content")
    headings = list(re.finditer(r"(?m)^### (?:\d+\s*[·.]\s*)?(.+?)\s*$", body))
    for index, match in enumerate(headings):
        if match.group(1).lower() in names:
            end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
            return body[match.end():end].strip()
    return ""


def source_links(text, page, root, source_url):
    links = []
    for label, target in re.findall(r"\[([^\]\n]+)\]\(([^\s)]+)\)", text):
        try:
            split = urlsplit(target)
        except ValueError:
            continue
        if split.scheme in {"https", "http"} and split.netloc:
            links.append({"title": label, "url": target, "path": "", "mtime": None})
        elif not split.scheme and not split.netloc and split.path:
            path = page.parent / unquote(split.path)
            try:
                modified = path.stat().st_mtime if inside(path, root) and path.is_file() else None
            except (OSError, ValueError):
                modified = None
            if modified is not None:
                links.append({"title": label, "url": source_url(path, root),
                              "path": path.resolve().relative_to(root).as_posix(),
                              "mtime": modified})
            else:
                links.append({"title": label, "url": "", "path": target, "mtime": None})
    return links


def report_snapshot(raw, qid, board, root, only, source_url, page_url):
    result = dict(path=words(raw), present=False, title="", answer="", status="open",
                  page_state="", evidence=[], evidence_text="", limits="", next="",
                  url="", workbench_url="", source_url="", issues=[], changed_evidence=False, drawings=[])
    if not result["path"]:
        return result
    rel = Path(result["path"])
    if (rel.is_absolute() or len(rel.parts) != 3 or rel.parts[0] != "reports"
            or not PAGE_STEM.fullmatch(rel.parts[1]) or rel.name != rel.parts[1] + ".md"):
        result["issues"].append("Report must be reports/qNN_topic/qNN_topic.md")
        return result
    page = board / rel
    body = read(page, board / "reports") if inside(page, board) else ""
    if not body:
        result["issues"].append("Report Page is missing, unreadable or outside its Block")
        return result
    result["present"] = True
    result["title"] = next((line[2:] for line in body.splitlines() if line.startswith("# ")), rel.stem)
    result["page_state"] = field(body, "state") or "Not declared"
    declared = field(body, "answer-status").lower()
    result["status"] = declared if declared in {"open", "partial", "answered"} else "unknown"
    if declared not in {"open", "partial", "answered"}:
        result["issues"].append("Report answer-status is missing or invalid")
    answers = [p.strip() for p in field(body, "answers").split(",")]
    if qid not in answers:
        result["issues"].append(f"Report answers does not name {qid}")
    opening = section(body, "Opening").split("\n\n", 1)[0]
    result["answer"] = plain(opening)
    evidence = report_section(body, {"evidence"})
    result["evidence_text"] = plain(evidence)
    result["evidence"] = source_links(evidence, page, root, source_url)
    for evidence_link in result["evidence"]:
        if evidence_link["mtime"] is not None and not evidence_link["url"]:
            # Results may be private static lanes. Keep the reference visible
            # and navigate through its native Task Run reader when available.
            target = root / evidence_link["path"]
            for folder in target.parents:
                if not inside(folder, board):
                    break
                if re.fullmatch(r"t\d{2}_[\w]+", folder.name):
                    evidence_link["url"] = page_url(folder / (folder.name + ".md"), board, root, "runs", only)
                    break
    # A drawing the report links to opens read-only in the shared Excalidraw viewer.
    result["drawings"] = [{"title": link["title"],
                           "url": "/_excalidraw/?" + urlencode({"board": link["path"]})}
                          for link in result["evidence"] if link["path"].endswith(".excalidraw") and link["mtime"] is not None]
    result["limits"] = plain(report_section(body, {"limits", "boundaries", "gaps"}))
    result["next"] = plain(report_section(body, {"next", "next actions"}))
    result["url"] = page_url(page, board, root, "draft", only)
    try:
        manifest = tomllib.loads(read(page.parent / "page.toml", page.parent))
    except ValueError:
        manifest = {}
    if (type(manifest.get("version")) is not int or manifest["version"] != 1
            or manifest.get("source") != page.name or not isinstance(manifest.get("title"), str)):
        result["url"] = ""
        result["issues"].append("Register this report with an ordinary Page page.toml to open its Workbench")
    if result["url"]:
        result["workbench_url"] = result["url"]
        result["url"] = "/_board/task-board?" + urlencode({
            "path": (board.relative_to(root) / "board.md").as_posix(), "report": qid})
    result["source_url"] = source_url(page, root)
    stamp = field(body, "results-read")
    try:
        instant = datetime.fromisoformat(stamp.replace("Z", "+00:00")) if stamp else None
        checked = instant.timestamp() if instant and instant.tzinfo else None
    except ValueError:
        checked = None
    if result["evidence"] and checked is None:
        result["issues"].append("Evidence review time is not recorded (results-read)")
    for link in result["evidence"]:
        if link["path"] and link["mtime"] is None:
            result["issues"].append(f"Evidence is unavailable: {link['path']}")
        if checked is not None and link["mtime"] is not None and link["mtime"] > checked:
            result["changed_evidence"] = True
    if result["changed_evidence"]:
        result["issues"].append("Linked evidence changed after the recorded reading; review this Report")
    return result


def extend_snapshot(board, root, snap, only, source_url, page_url):
    body = read(board / "board.md", board)
    rows, issues = register(body, "Questions", "questions")
    resources, errors = register(body, "Related resources", "resources")
    issues.extend(errors)
    questions, seen, assigned = [], set(), set()
    task_by_path = {f"{t['job']}/{t['name']}": t for t in snap["tasks"]}
    for row in rows:
        qid = words(row.get("id"))
        if not QUESTION_ID.fullmatch(qid) or qid in seen or not words(row.get("question")):
            issues.append(f"Invalid or duplicate Question: {qid or '(missing id)'}")
            continue
        seen.add(qid)
        question = {"id": qid, "title": words(row.get("title")) or row["question"],
                    "block_path": snap["path"],
                    "question": row["question"], "hypothesis": words(row.get("hypothesis")),
                    "acceptance": words(row.get("acceptance")), "work": [], "issues": []}
        work = row.get("work", [])
        if not isinstance(work, list):
            question["issues"].append("work must be a list of Task paths")
            work = []
        for entry in work:
            path = entry if isinstance(entry, str) else words(entry.get("path")) if isinstance(entry, dict) else ""
            role = words(entry.get("role")) if isinstance(entry, dict) else ""
            task = task_by_path.get(path)
            if not task:
                question["issues"].append(f"Work reference does not identify a Task in this Block: {path}")
                continue
            if any(w["path"] == path for w in question["work"]):
                question["issues"].append(f"Repeated Work reference: {path}")
                continue
            stage = words(entry.get("stage")) if isinstance(entry, dict) else ""
            question["work"].append({"role": role, "stage": stage, "path": path, "task": task})
            assigned.add(task["id"])
        question["report"] = report_snapshot(row.get("report"), qid, board, root, only, source_url, page_url)
        questions.append(question)
    for question in questions:
        for item in question["work"]:
            item["also"] = [q["id"] for q in questions if q["id"] != question["id"]
                            and any(w["path"] == item["path"] for w in q["work"])]
    clean_resources = []
    for row in resources:
        title, url = words(row.get("title")), words(row.get("url"))
        try:
            split = urlsplit(url)
        except ValueError:
            issues.append(f"Invalid resource URL: {title}")
            continue
        if not title or split.scheme not in {"http", "https"} or not split.netloc:
            issues.append("A Related resource needs a title and an http(s) source URL")
            continue
        ids = row.get("questions", [])
        if not isinstance(ids, list) or any(not isinstance(v, str) or v not in seen for v in ids):
            issues.append(f"{title}: questions must name registered Question ids")
            ids = []
        clean_resources.append({"title": title, "url": url, "questions": ids,
                                "contribution": words(row.get("contribution")), "notes": words(row.get("notes"))})
    drawings = []
    studio = board / "studio"
    if inside(studio, board) and studio.is_dir():
        for path in sorted(studio.glob("*.excalidraw")):
            if inside(path, studio) and path.is_file() and source_url(path, root):
                drawings.append({"title": path.stem.replace("_", " "),
                                 "path": path.relative_to(root).as_posix()})
    snap.update(questions=questions, resources=clean_resources, drawings=drawings,
                source_issues=issues, unassigned=[t for t in snap["tasks"] if t["id"] not in assigned],
                studio_path=(board.relative_to(root) / "studio").as_posix(),
                studio_enabled=not only, native_only=list(only))
    return snap
