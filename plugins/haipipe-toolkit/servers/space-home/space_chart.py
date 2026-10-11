"""Read the SPACE ladder for the interactive Home chart, without writing data."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlsplit


def state_of(text: str) -> tuple[str, str]:
    """Use the face's declared state; an open red circle is not a failed run."""
    match = re.search(r"(?m)^state:\s*(.+)$", text)
    if not match:
        return "unknown", "No recorded status"
    raw = match.group(1).strip()
    word = raw.upper()
    if re.search(r"\b(BLOCKED|FAILED|ERROR)\b", word) or "⛔" in raw:
        return "blocked", raw
    if re.search(r"\b(PAUSED|HOLD|PARKED|ARCHIVED)\b", word) or "⏸" in raw:
        return "paused", raw
    if re.search(r"\b(OPEN|TODO|PLANNED|PENDING|NOT STARTED)\b", word):
        return ("active" if re.search(r"\b(ACTIVE|RUNNING|IN PROGRESS|RESULTS READY)\b", word)
                else "open"), raw
    if re.search(r"\b(DONE|COMPLETE|COMPLETED|SETTLED|CLOSED)\b", word) or "✅" in raw:
        return "done", raw
    if re.search(r"\b(ACTIVE|RUNNING|IN PROGRESS|RESULTS READY|PARTIAL)\b", word) \
            or any(mark in raw for mark in ("🟡", "🔄", "🏃")):
        return "active", raw
    return "unknown", raw


def _face(folder: Path) -> dict:
    from live.frame import face
    page = face(folder)
    text = page.read_text(encoding="utf-8", errors="replace") if page else ""
    # Only face fields drive this view. Run success does not mean the Task is done.
    title = re.search(r"(?m)^#\s+(.+)$", text)
    if not title:
        title = re.search(r"(?m)^([^\n]+)\n={3,}\s*$", text)
    state, raw = state_of(text)
    note = re.search(r"(?m)^(?:status|next|spine|goal):\s*(.+)$", text)
    return {"name": title.group(1).strip() if title else folder.name,
            "status": state, "state": raw, "note": note.group(1).strip() if note else ""}


def chart_data(root: Path, cards: list[dict], name: str = "SPACE", *, include_linked: bool = True) -> dict:
    """Examples → Projects → Scenes → Blocks → Jobs → Tasks, as in the frame."""
    from live.frame import children, studio_inventory, studio_anchor
    from src.themes import FOLDER
    tree = {"id": "space", "name": name, "level": "Space", "children": []}
    examples, projects, scenes = {}, {}, {}
    root = root.resolve()

    def folder_node(folder, level):
        relative = folder.relative_to(root).as_posix()
        details = _face(folder)
        details["title"] = details.pop("name")
        return {"id": relative, "path": relative, "folder": folder.name,
                "name": folder.name, "level": level,
                "href": "/_board/workbench?" + urlencode({"path": relative}),
                "children": [], **details}

    for card in cards:
        if card.get("linked_space") or not (card.get("ready") or card.get("workbench_ready")):
            continue
        project_path = str(card.get("project_path") or ".")
        example = (project_path.split("/")[0] if card.get("project_scope") == "project"
                   else str(card.get("project") or "Shared"))
        if example not in examples:
            examples[example] = {"id": "example:" + example, "name": example,
                                 "level": "Examples", "children": []}
            tree["children"].append(examples[example])
        project_key = str(card["project_key"])
        if project_key not in projects:
            projects[project_key] = {"id": project_key, "name": str(card["project"]),
                "path": project_path, "level": "Project" if card.get("project_scope") == "project" else "Folder", "children": [],
                "href": "/?" + urlencode({"project": project_path, "view": "radial"})}
            examples[example]["children"].append(projects[project_key])
        kind = str(card["kind_key"])
        scene_key = project_key + ":scene:" + kind
        if scene_key not in scenes:
            scenes[scene_key] = {"id": scene_key, "name": FOLDER.get(kind, kind),
                "kind": kind, "level": "Scene", "children": []}
            projects[project_key]["children"].append(scenes[scene_key])
        block = folder_node(root / str(card["path"]), "Block")
        block["title"] = str(card["title"])
        block["state"] = str(card.get("board_state") or "No recorded status")
        block["kind"] = kind
        block["archived"] = any(part in {"_legacy", "_old", "_archive"} for part in Path(block["path"]).parts)
        block["href"] = str(card["href"])
        # Count the shared Block list, including existing local topics until migration, once per folder.
        block["studios"] = []
        for source, topic, drawings in studio_inventory(root / str(card["path"]), root):
            if not topic.is_dir() or not re.match(r"^s\d+[-_]", topic.name):
                continue
            if root not in topic.resolve().parents:
                continue
            studio = folder_node(topic, "Studio")
            studio["drawings"] = len(drawings)
            studio["href"] = "/_board/workbench?" + urlencode({
                "path": block["path"], "space": "Idea Studio"}) + "#" + studio_anchor(topic, source, root / str(card["path"]))
            block["studios"].append(studio)
        scenes[scene_key]["children"].append(block)
        for job_folder in children(root / str(card["path"]), "Block"):
            job = folder_node(job_folder, "Job")
            block["children"].append(job)
            for task_folder in children(job_folder, "Job"):
                job["children"].append(folder_node(task_folder, "Task"))
        # Older layouts may put a tNN_ folder directly under a Block.
        for task_folder in children(root / str(card["path"]), "Job"):
            block["children"].append(folder_node(task_folder, "Task"))
    if include_linked:
        tree["children"].extend(_linked_groups(root))
    return {"tree": tree, "read_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def _linked_sources(root: Path) -> list[tuple]:
    """Read explicitly linked work folders through their own repository boundary."""
    from server_config import load_server_config
    from live.home import discover_boards, project_owner
    try:
        links = json.loads(load_server_config(root).get("INDEX_LINKED_SPACES", "{}"))
    except (TypeError, ValueError):
        return []
    if not isinstance(links, dict):
        return []
    sources, visited = [], {root.resolve()}
    for relative, setting in links.items():
        if not isinstance(relative, str) or not isinstance(setting, dict):
            continue
        link_path = Path(relative)
        if link_path.is_absolute() or ".." in link_path.parts or not link_path.parts:
            continue
        source = (root / link_path).resolve()
        if not source.is_dir() or source in visited or source.is_relative_to(root):
            continue
        origin = setting.get("url", "")
        if not isinstance(origin, str):
            continue
        try:
            parsed = urlsplit(origin)
        except ValueError:
            continue
        if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
            continue
        folders = setting.get("folders", [])
        if not isinstance(folders, list):
            continue
        cards, found = [], set()
        for folder in folders:
            if not isinstance(folder, str):
                continue
            part = Path(folder)
            if part.is_absolute() or ".." in part.parts or not part.parts:
                continue
            scan = (source / part).resolve()
            if not scan.is_dir() or not scan.is_relative_to(source):
                continue
            for card in discover_boards(scan, include_page_state=False):
                board = scan / str(card["path"])
                path = board.relative_to(source).as_posix()
                if path in found or "_build" in Path(path).parts:
                    continue
                found.add(path)
                owner = project_owner(board, source)
                if owner["project_scope"] != "project":
                    bucket = Path(path).parts[0]
                    owner.update(project=bucket, project_path=bucket,
                                 project_key="folder:" + bucket)
                cards.append({**card, **owner, "path": path,
                              "href": "/_board/workbench?" + urlencode({"path": path})})
        if not cards:
            continue
        visited.add(source)
        sources.append((link_path.as_posix(), source, origin.rstrip("/"), cards))
    return sources


def linked_home_cards(root: Path) -> list[dict]:
    """Give List Index the same linked work and its own reader links."""
    cards = []
    for prefix, source, origin, source_cards in _linked_sources(root.resolve()):
        for card in source_cards:
            project_key = str(card["project_key"])
            kind, value = project_key.split(":", 1)
            cards.append({**card, "path": prefix + "/" + str(card["path"]),
                "project_path": prefix + "/" + str(card["project_path"]),
                "project_key": kind + ":" + prefix + "/" + value,
                "href": origin + "/" + str(card["href"]).lstrip("/"),
                "linked_space": prefix})
    return cards


def _linked_groups(root: Path) -> list[dict]:
    groups = []
    for prefix, source, origin, cards in _linked_sources(root):
        source_tree = chart_data(source, cards, prefix, include_linked=False)["tree"]
        group = {"id": "example:" + prefix, "name": prefix, "level": "Examples",
                 "href": origin + "/?view=radial", "children": [], "linked": True}

        def qualify(node):
            previous = node["id"]
            if previous.startswith(("project:", "folder:")):
                kind, value = previous.split(":", 1)
                node["id"] = kind + ":" + prefix + "/" + value
            else:
                node["id"] = prefix + "/" + previous
            if node.get("path"):
                node["path"] = prefix + "/" + node["path"]
            if node.get("href"):
                if node["level"] == "Folder":
                    node["href"] = "/?" + urlencode({"view": "list", "q": node["name"]})
                node["href"] = origin + "/" + node["href"].lstrip("/")
            node["linked"] = True
            for child in node.get("children", []):
                qualify(child)
            for topic in node.get("studios", []):
                qualify(topic)

        for collection in source_tree["children"]:
            for project in collection["children"]:
                qualify(project)
                group["children"].append(project)
        groups.append(group)
    return groups


def chart_parts(root: Path, cards: list[dict], name: str) -> tuple[str, str, str]:
    data = json.dumps(chart_data(root, cards, name), ensure_ascii=False, separators=(",", ":"))
    # A face title is source text, never executable HTML or a closing script tag.
    data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    assets = Path(__file__).parent / "assets"
    markup = '''<div class="home-views" role="group" aria-label="Index view">
<button type="button" data-home-view="radial" aria-pressed="true">Chart · Progress</button>
<button type="button" data-home-view="list" aria-pressed="false">List · Index</button></div>
<section id="space-chart" hidden aria-label="Space progress visualization">
<div class="chart-controls chart-primary-controls">
<label>Project / Folder<select id="chart-project" aria-label="Project / Folder"><option value="">All Projects and Folders</option></select></label>
<label>Block<select id="chart-block" aria-label="Block"><option value="">All Blocks</option></select></label>
<label>Size by<select id="chart-measure" aria-label="Size by"><option value="tasks">Task count</option><option value="blocks" selected>Block count</option><option value="jobs">Job count</option><option value="studios">Studio topic count (sNN)</option></select></label>
<div class="chart-actions"><button type="button" id="chart-reset">Reset</button><button type="button" id="chart-refresh">Refresh</button></div></div>
<div class="chart-drawers">
<details id="chart-filters" class="chart-disclosure"><summary>Filters <span id="chart-filter-count"></span></summary>
<div class="chart-drawer-body"><div class="chart-controls chart-filter-controls">
<label>Group<select id="chart-example" aria-label="Group"><option value="">All groups</option></select></label>
<div id="chart-kind-slot"></div></div>
<div id="chart-status" class="chart-status" aria-label="Status filters"></div></div></details>
<details id="chart-options" class="chart-disclosure"><summary>Chart options <span id="chart-layer-summary"></span></summary>
<div class="chart-drawer-body chart-controls">
<label>Project / Folder names<select id="chart-names" aria-label="Project / Folder names"><option value="inside">Inside segments</option><option value="outside">Outside chart</option></select></label>
<label class="chart-job-toggle"><input type="checkbox" id="chart-jobs" checked>Show Job layer</label>
<label class="chart-job-toggle"><input type="checkbox" id="chart-tasks">Show Task layer</label>
<label class="chart-job-toggle"><input type="checkbox" id="chart-archived">Include legacy Blocks</label></div></details></div>
<div id="chart-active-filters" class="chart-active-filters" hidden aria-label="Active filters"></div>
<div id="chart-stats" class="chart-stats" aria-live="polite"></div>
<nav id="chart-breadcrumb" class="chart-breadcrumb" aria-label="Chart path"></nav>
<div class="chart-layout"><div class="chart-figure">
<div class="chart-zoom-controls" role="group" aria-label="Chart magnification">
<button type="button" id="chart-up">Back to parent</button><div class="chart-zoom-group">
<button type="button" id="chart-zoom-out" aria-label="Reduce chart">−</button>
<output id="chart-zoom-value" aria-live="polite">100%</output>
<button type="button" id="chart-zoom-in" aria-label="Magnify chart">+</button>
<button type="button" id="chart-fit">Fit</button></div>
<button type="button" id="chart-details">Scope details</button></div>
<div id="chart-canvas" class="chart-canvas" tabindex="0" aria-label="Chart. Use plus or minus to zoom, arrow keys to pan, zero to fit."></div>
<div id="chart-hover" class="chart-hover" aria-live="off">Hover for details. On mobile, tap a segment.</div>
</div>
<details id="chart-scope-list" class="chart-disclosure"><summary>Browse this scope <span id="chart-scope-count"></span></summary>
<div class="chart-detail"><div id="chart-children"></div><details class="chart-scope-info"><summary>Scope information and status</summary><div id="chart-selection"></div></details></div></details></div>
<details class="chart-disclosure chart-help"><summary>How to read this chart</summary>
<div class="chart-top"><p>Groups → Projects / Folders → Themes → Blocks → Jobs</p></div>
<p id="chart-area-note" class="chart-area-note"></p>
<div id="chart-legend" class="chart-legend" aria-label="Status colors"></div>
<p class="chart-footnote">Completion uses Task states, or Job and Block states when no Tasks exist. Each level has its own recorded status. Hidden Tasks still count toward completion. Legacy Blocks are excluded unless enabled. Studio topic counts use the shared Block list, including existing Job and Task topics; each folder counts once. Studio topics have no completion score.<span id="chart-read-at"></span></p>
<p class="chart-footnote">Select a segment to focus its branch. On mobile, tap for details, then choose Zoom in. Use + / − to magnify and drag to pan. Use Fit to reset the view.</p></details>
</section>'''
    markup += '<script id="space-chart-data" type="application/json">' + data + '</script>'
    return markup, assets.joinpath("space-chart.css").read_text(encoding="utf-8"), \
        assets.joinpath("space-chart.js").read_text(encoding="utf-8")
