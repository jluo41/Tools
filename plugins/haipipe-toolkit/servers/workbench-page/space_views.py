"""The three Spaces as the Page design draws them (Page 0.118).

    Draft     Structure line · Reads line · Table / Reading / Scratch / Revise · whole page
    Evidence  Citations / Displays / Values / Supporting Runs · Reads line · All items / Card / Source
    Delivery  Web / LaTeX / Word / Slides · Reads line · Preview / Artifacts / Checks

Each tab shows one part of a file: the Draft views read the three `##` sections
of the Draft Markdown, the Evidence tabs read the three `##` sections of the
Evidence Markdown, and the Delivery tabs read `delivery/<format>/`. The fourth
Evidence tab, Supporting Runs, reads every item's `Supporting Runs` line and
draws those Runs as their Block > Job > Task > Run tree. Nothing
here writes. The Runs panel under each Space (runs_panel.py) follows the tab
and the selected paragraph or item.
"""
from __future__ import annotations

import datetime
import html
import re
from pathlib import Path
from urllib.parse import quote, unquote

from src.outline_version import latest_outline, plan_dir
from src.item_table import short_name
from src.plan_layout import is_sectioned

EVIDENCE_TABS = (("citations", "Citations"), ("displays", "Displays"), ("values", "Values"))
SUPPORT_TAB = ("supporting", "Supporting Runs")
_KIND_TAB = {"CITE": "citations", "DISPLAY": "displays", "VALUE": "values"}
_LEVEL = re.compile(r"^([bjt])\d+_")
# (tab, label, folder, preview files in order of preference)
FORMATS = (
    ("web", "Web", "delivery/web", ("index.html",)),
    ("latex", "LaTeX", "delivery/latex", ("{stem}.pdf", "{stem}-view.html")),
    ("word", "Word", "delivery/word", ("{stem}-view.html", "{stem}.pdf")),
    ("slides", "Slides", "delivery/slide", ("{stem}-deck.html",)),
)
_CHECK_LANE = {"web": "web", "latex": "latex", "word": "word", "slides": "slide"}
_ITEM = re.compile(r"^### (E\d+)-([A-Z]+)-([\w-]+)(?:\s*·\s*(.*))?$")
_FIELD = re.compile(r"^- \*\*(?P<key>[^*]+)\*\*:\s*(?P<value>.*)$")
_VIEWABLE = {".html", ".htm", ".pdf", ".png", ".jpg", ".jpeg", ".svg"}


def _e(value) -> str:
    return html.escape(str(value or ""), quote=True)


def _current_plan(page_src: Path):
    return latest_outline(plan_dir(page_src.parent), page_src.stem)


# ---- Draft Space -----------------------------------------------------------

def draft_reads_html(page_src: Path) -> str:
    """Which file and which `##` section each Draft view shows."""
    plan = _current_plan(page_src)
    if plan is None:
        return ""
    name = "%s/%s" % (plan.parent.name, plan.name)
    sectioned = is_sectioned(plan.read_text(encoding="utf-8", errors="replace"))
    parts = (" · Table <code>## 1 Structure</code> · Scratch <code>## 2 Scratch</code>"
             " · Reading, Revise <code>## 3 Draft</code>") if sectioned else ""
    return '<div class=space-reads>Reads <code>%s</code>%s</div>' % (_e(name), parts)


# ---- Evidence Space --------------------------------------------------------

def evidence_file(page_src: Path) -> Path:
    return plan_dir(page_src.parent) / ("%s-evidence-items.md" % page_src.stem)


def evidence_items(page_src: Path) -> list[dict]:
    """The current (`###`) items of the Evidence Markdown, with their tab and state.

    Retired items are `####` headings and stay out, as the Draft ignores them.
    """
    try:
        text = evidence_file(page_src).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    items, tab, current, sectioned = [], None, None, False
    tabs = {key for key, _ in EVIDENCE_TABS}
    by_kind = {"CITE": "citations", "DISPLAY": "displays", "VALUE": "values"}
    for line in text.splitlines():
        if line.startswith("## "):
            name = line[3:].strip().lower()
            tab, current, sectioned = (name if name in tabs else None), None, True
            continue
        if line.startswith("#"):
            current = None
            match = _ITEM.match(line)
            if match and not sectioned:  # a flat file: each item goes to its kind's tab
                tab = by_kind.get(match.group(2))
            if match and tab:
                parts = [p.strip() for p in (match.group(4) or "").split("·")]
                current = {"id": match.group(1), "kind": match.group(2), "tab": tab,
                           "full": "%s-%s-%s" % match.group(1, 2, 3),
                           "name": match.group(3).replace("-", " "),
                           "target": parts[0] if parts else "",
                           "title": " · ".join(p for p in parts[1:] if p), "fields": {}}
                items.append(current)
            continue
        field = _FIELD.match(line) if current else None
        if field:
            current["fields"][field["key"].strip().lower()] = field["value"].strip()
    for item in items:
        fields = item["fields"]
        item["target"] = fields.get("target") or item["target"]
        item["verified"] = fields.get("verified", "").startswith("✅")
        item["state"] = ("verified" if item["verified"] else
                         "bound" if fields.get("local run") else "open")
    return items


def run_tabs(page_src: Path) -> dict[str, dict]:
    """{`pj02t01r01`: {tab, item, target}}: the Evidence Item an older Paper-local run serves.

    Read from each item's `Local Run` line (retired `####` items included), from
    any line that names an item id beside the run, such as a "moved out" note, and
    from an Evidence Run ticket's `legacy_run:` line: a migration-binding
    `re-display-01` ticket names the older `pj05t01r01` that drew the display, which
    otherwise has no item and falls into "Other".
    """
    try:
        text = evidence_file(page_src).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    tab_of = {"CITE": "citations", "DISPLAY": "displays", "VALUE": "values"}
    out, item = {}, None
    for line in text.splitlines():
        head = re.match(r"^#{3,4} (E\d+)-([A-Z]+)-[\w-]+(?:\s*·\s*(C\d+\.P\d+\.B\d+))?", line)
        if head:
            item = {"tab": tab_of.get(head.group(2)), "item": head.group(1), "target": head.group(3) or ""}
            continue
        if line.startswith("#"):
            item = None
        named = re.search(r"\b(E\d+)-([A-Z]+)-", line)
        owner = ({"tab": tab_of.get(named.group(2)), "item": named.group(1), "target": ""}
                 if named and not (item and line.startswith("- **Local Run**")) else item)
        if not owner or not (line.startswith("- **Local Run**") or named):
            continue
        for key in re.findall(r"\bp[._]?j(\d+)[._]?t(\d+)[._]?r(\d+)", line):
            if owner["tab"]:
                out.setdefault("pj%st%sr%s" % key, owner)
        # A renamed run (`run-value-0906-score-validation`, page.py run-names) keeps its item here.
        for name in re.findall(r"\brun-(?:citation|value|display)-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*", line):
            if owner["tab"]:
                out.setdefault(name, owner)
    runs = page_src.parent / "runs"
    for ticket in sorted(runs.rglob("re-*.md")) if runs.is_dir() else []:
        try:
            head = ticket.read_text(encoding="utf-8", errors="replace")[:1500]
        except OSError:
            continue
        item = re.search(r"(?m)^item:\s*(E\d+)-([A-Z]+)-", head)
        legacy = re.search(r"(?m)^legacy_run:\s*p[._]?j(\d+)[._]?t(\d+)[._]?r(\d+)", head)
        target = re.search(r"(?m)^target:\s*(C\d+\.P\d+\.B\d+)", head)
        if item and legacy and tab_of.get(item.group(2)):
            out.setdefault("pj%st%sr%s" % legacy.groups(),
                           {"tab": tab_of[item.group(2)], "item": item.group(1),
                            "target": target.group(1) if target else ""})
    return out


def _section_text(text: str, heading: str) -> str:
    match = re.search(r"(?ms)^## %s\s*$(.*?)(?=^## |\Z)" % re.escape(heading), text)
    return match.group(1).strip("\n") if match else ""


def _tree_path(ticket: Path) -> tuple[str, list[str]]:
    """A ticket path → (its world, e.g. `task/`, and [block, job, task] folders).

    The world is the folder above the Block, named from its Project when the Run
    lives in another Project than the Page."""
    parts = Path(ticket).parts
    start = next((i for i, part in enumerate(parts) if _LEVEL.match(part) and part[0] == "b"), None)
    if start is None:
        return "", []
    chain = []
    for part in parts[start:-1]:
        if not _LEVEL.match(part):
            break
        chain.append(part)
    world = parts[start - 1] if start else ""
    project = parts[start - 2] if start > 1 else ""
    return "%s/%s/" % (project, world) if project else world + "/", chain


_KIND_ORDER = ("CITE", "DISPLAY", "TABLE", "VALUE")      # the tab order: Citations, Displays, Values


def _item_groups(refs: list, titles: dict) -> str:
    """The items a Run feeds by their short names, grouped by type in tab order:
    `Ecite25 · Edisplay13 Edisplay14 · Evalue01 Evalue02`. Each opens that item on its tab."""
    kinds: dict = {}
    for full in refs:
        match = re.match(r"^(E\d+)-([A-Z]+)-", full)
        if match:
            kinds.setdefault(match.group(2), {})[match.group(1)] = full
    out = []
    for kind in sorted(kinds, key=lambda k: _KIND_ORDER.index(k) if k in _KIND_ORDER else 9):
        ids = sorted(kinds[kind], key=lambda e: int(e[1:]))
        out.append('<span class=sup-group>%s</span>' % "".join(
            '<button type=button class=sup-item data-item="%s" data-tab="%s" title="%s">%s</button>'
            % (_e(e), _KIND_TAB.get(kind, ""), _e(titles.get(e) or kinds[kind][e]), _e(short_name(e, kind)))
            for e in ids))
    return "".join(out)


def _name_html(name: str) -> str:
    """`b03_CD_visit_pain` with its level prefix `b03` marked; the name stays as written."""
    match = re.match(r"^([bjtr]\d+[a-z]?)(_.*)?$", name)
    if not match:
        return _e(name)
    return '<span class=sup-lvl>%s</span>%s' % (_e(match.group(1)), _e(match.group(2) or ""))


def supporting_tree_html(page_src: Path, runs: list[dict], items: list[dict]) -> str:
    """The Supporting Runs of this Page's Evidence Items as a Block > Job > Task > Run tree.

    Each Run names the Evidence Items it feeds; a Run the registry does not know
    shows under "Not found" by its address."""
    if not runs:
        return '<div class=space-empty>No Supporting Runs declared on this page yet.</div>'
    above = {p.name for p in Path(page_src).resolve().parents}   # the Page's own Project is not named
    titles = {i["id"]: "%s · %s" % (i["full"], i["title"] or i["name"]) for i in items}
    tree: dict = {}
    for run in runs:
        ticket = Path(str(run.get("ticket") or ""))
        world, chain = _tree_path(ticket) if run.get("ticket") else ("", [])
        project = world.split("/")[0] if world.count("/") > 1 else ""
        if project in above:
            world = world[len(project) + 1:]
        kind = str(run.get("kind") or "Task")
        top = (kind, world) if chain else ("Not found", "")
        node = tree.setdefault(top, {})
        for level in chain:
            node = node.setdefault(level, {})
        node.setdefault("", []).append(run)

    def leaf(run: dict) -> str:
        ticket = str(run.get("ticket") or "")
        name = Path(ticket).stem if ticket else str(run.get("run_id") or "")
        state = str(run.get("status") or "unknown")
        return ('<div class=sup-run tabindex=0 data-run="%s"><span class="sup-dot st-%s" title="%s"></span>'
                '<code class=sup-name title="%s">%s</code><span class=sup-state>%s</span>'
                '<span class=sup-items>%s</span></div>'
                % (_e(run.get("compact_id") or ""), _e(state.lower()), _e(state),
                   _e(run.get("run_id") or ""), _name_html(name), _e(state),
                   _item_groups(run.get("refs") or [], titles)))

    def branch(node: dict, depth: int) -> str:
        runs = sorted(node.get("", []), key=lambda r: Path(str(r.get("ticket") or r.get("run_id") or "")).stem)
        out = "".join(leaf(run) for run in runs)
        for name in sorted(k for k in node if k):
            out += ('<details open class="sup-node sup-d%d"><summary><code>%s</code></summary>%s</details>'
                    % (depth, _name_html(name), branch(node[name], depth + 1)))
        return out

    return '<div class=sup-tree>%s</div>' % "".join(
        '<details open class="sup-node sup-world"><summary><b>%s</b>%s</summary>%s</details>'
        % (_e(kind), (" <code class=sup-path>%s</code>" % _e(world)) if world else "", branch(tree[(kind, world)], 1))
        for kind, world in sorted(tree, key=lambda k: (k[0] == "Not found", k)))


def evidence_space_html(page_src: Path, *, card_url: str, supporting: list[dict] | None = None) -> str:
    items = evidence_items(page_src)
    path = evidence_file(page_src)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        text = ""
    counts = {key: sum(1 for i in items if i["tab"] == key) for key, _ in EVIDENCE_TABS}
    first = next((key for key, _ in EVIDENCE_TABS if counts[key]), "citations")
    tabs = "".join(
        '<button type=button class="space-tab%s" data-tab="%s" data-label="%s">%s '
        '<span class=space-count>%d</span></button>'
        % (" on" if key == first else "", key, label, label, counts[key])
        for key, label in EVIDENCE_TABS)
    supporting = supporting or []
    tabs += ('<button type=button class=space-tab data-tab="%s" data-label="%s" data-views="items source">'
             '%s <span class=space-count>%d</span></button>'
             % (SUPPORT_TAB[0], SUPPORT_TAB[1], SUPPORT_TAB[1], len(supporting)))
    lists, sources = [], []
    for key, label in EVIDENCE_TABS:
        mine = [i for i in items if i["tab"] == key]
        rows = "".join(
            '<tr class=ev-row tabindex=0 data-item="%s" data-full="%s" data-focus="%s">'
            '<td><code>%s</code></td><td>%s<span class=ev-label>%s</span></td>'
            '<td><code>%s</code></td><td class="ev-state st-%s">%s %s</td>'
            '<td><button type=button class=ev-open>Card</button></td></tr>'
            % (_e(i["id"]), _e(i["full"]), _e("run-" + re.sub(r"[^A-Za-z0-9_-]", "-", i["full"])),
               _e(short_name(i["full"])), _e(i["title"] or i["name"]),
               _e(" · " + i["fields"]["label"])
               if i["fields"].get("label") and i["fields"]["label"] != (i["title"] or i["name"]) else "",
               _e(i["target"]), i["state"], "✓" if i["verified"] else "○", i["state"])
            for i in mine)
        body = ('<table class=ev-table><thead><tr><th>ID</th><th>Item</th><th>Used by</th>'
                '<th>State</th><th></th></tr></thead><tbody>%s</tbody></table>' % rows
                if mine else '<div class=space-empty>No %s on this page yet.</div>' % label.lower())
        lists.append('<section class=space-pane data-view=items data-tab="%s"%s>'
                     '<div class=space-head><b>All %s for this page · %d</b></div>%s</section>'
                     % (key, "" if key == first else " hidden", label.lower(), len(mine), body))
        source = _section_text(text, label)
        sources.append('<section class=space-pane data-view=source data-tab="%s" hidden>'
                       '<pre class=space-source>%s</pre></section>'
                       % (key, _e("## %s\n\n%s" % (label, source)) if source else "(empty)"))
    lists.append('<section class=space-pane data-view=items data-tab="%s" hidden>%s</section>'
                 % (SUPPORT_TAB[0], supporting_tree_html(page_src, supporting, items)))
    lines = "\n\n".join("%s\n- **Supporting Runs**: %s" % (i["full"], i["fields"]["supporting runs"])
                         for i in items if i["fields"].get("supporting runs"))
    sources.append('<section class=space-pane data-view=source data-tab="%s" hidden>'
                   '<pre class=space-source>%s</pre></section>' % (SUPPORT_TAB[0], _e(lines or "(empty)")))
    return (
        '<div class="space-tabs" data-space=evidence role=tablist>%s</div>'
        '<div class=space-reads>Reads <code>%s</code></div>'
        '<div class=space-views data-space=evidence><span class=space-views-label>View</span>'
        '<button type=button class="space-view on" data-view=items>All items</button>'
        '<button type=button class=space-view data-view=card>Card</button>'
        '<button type=button class=space-view data-view=source>Source</button></div>'
        '<div class=space-body data-space=evidence>%s'
        '<section class=space-pane data-view=card hidden><iframe class="workspace-frame space-frame" '
        'title="Evidence cards" data-src="%s"></iframe></section>%s</div>'
        % (tabs, _e("%s/%s" % (path.parent.name, path.name)), "".join(lists),
           _e(card_url), "".join(sources)))


# ---- Delivery Space --------------------------------------------------------

def file_url(rel: str, *, path_q: str, file_q: str, asset_base) -> str:
    """A Page file's URL on this host (the Python twin of delivery.py's savedUrl)."""
    if asset_base is not None:
        return "%s/%s" % (asset_base.rstrip("/"), quote(rel))
    board = unquote(path_q or "")
    cut = board.rfind("/board/")
    base = board[:cut] if cut >= 0 else (board.rsplit("/", 1)[0] if board.endswith(".md") else "")
    if not base:
        return ""
    # A route like /_board/draft?path=examples%2F... carries no leading slash;
    # without one the frame URL resolves under /_board/ and 404s.
    base = "/" + base.lstrip("/")
    folder = re.match(r"^(.*)/([^/]+)/\2\.md$", file_q or "")
    if folder:
        return "%s/%s/%s/%s" % (base, folder.group(1), folder.group(2), quote(rel))
    return "%s/%s" % (base, quote(rel))


def _stamp(path: Path) -> str:
    return datetime.datetime.fromtimestamp(path.stat().st_mtime).strftime("%y%m%d %H:%M")


def _size(path: Path) -> str:
    size = path.stat().st_size
    return "%.1f MB" % (size / 1e6) if size >= 1e6 else "%d KB" % max(1, round(size / 1e3))


def delivery_states(page_src: Path) -> dict[str, str]:
    try:
        from live.delivery import check_delivery
        receipt = check_delivery(page_src)
    except Exception:  # the tabs still render without the check
        return {}
    return {lane["lane"]: lane["state"] for lane in receipt["lanes"]}


def delivery_space_html(page_src: Path, *, checks_url: str, path_q: str, file_q: str,
                        asset_base) -> str:
    base = page_src.parent
    stem = page_src.stem
    states = delivery_states(page_src)
    built = [key for key, _l, folder, _p in FORMATS if (base / folder).is_dir()]
    first = "latex" if "latex" in built else (built[0] if built else "latex")
    tabs, previews, artifacts = [], [], []
    for key, label, folder, wanted in FORMATS:
        state = states.get(_CHECK_LANE[key], "not-built")
        tabs.append('<button type=button class="space-tab%s" data-tab="%s" data-label="%s">%s '
                    '<span class="space-count st-%s">%s</span></button>'
                    % (" on" if key == first else "", key, label, label, _e(state),
                       _e(state.replace("-", " "))))
        hidden = "" if key == first else " hidden"
        preview = next((base / folder / name.format(stem=stem) for name in wanted
                        if (base / folder / name.format(stem=stem)).is_file()), None)
        if preview is not None:
            url = file_url("%s/%s" % (folder, preview.name), path_q=path_q, file_q=file_q,
                           asset_base=asset_base)
            # An .html frame must say ?embed: over plain http the browser sends no
            # Sec-Fetch-Dest, so the board answers a bare .html with its split shell.
            if url and preview.suffix == ".html":
                url += "?embed"
            body = ('<iframe class="space-frame preview-frame" title="%s preview" data-src="%s">'
                    '</iframe>' % (label, _e(url)))
            note = "built %s · %s" % (_stamp(preview), state.replace("-", " "))
        else:
            body = '<div class=space-empty>No %s build yet.</div>' % label
            note = "not built"
        shown = "%s/%s" % (folder, preview.name) if preview is not None else folder + "/"
        previews.append('<section class=space-pane data-view=preview data-tab="%s"%s>'
                        '<div class=space-head><code>%s</code><span class=space-hint>%s</span></div>'
                        '%s</section>' % (key, hidden, _e(shown), _e(note), body))
        files = sorted((p for p in (base / folder).iterdir() if p.is_file() and not p.name.startswith(".")),
                       key=lambda p: p.name) if (base / folder).is_dir() else []
        rows = "".join(
            '<tr><td>%s</td><td>%s</td><td>%s</td></tr>'
            % (('<a href="%s" target=_blank rel=noopener>%s</a>'
                % (_e(file_url("%s/%s" % (folder, p.name), path_q=path_q, file_q=file_q,
                               asset_base=asset_base)), _e(p.name)))
               if p.suffix.lower() in _VIEWABLE else '<code>%s</code>' % _e(p.name),
               _e(_size(p)), _e(_stamp(p)))
            for p in files)
        artifacts.append('<section class=space-pane data-view=artifacts data-tab="%s" hidden>'
                         '<div class=space-head><code>%s/</code><span class=space-hint>%d files</span></div>%s</section>'
                         % (key, _e(folder), len(files),
                            '<table class=ev-table><thead><tr><th>File</th><th>Size</th>'
                            '<th>Built</th></tr></thead><tbody>%s</tbody></table>' % rows
                            if files else '<div class=space-empty>Nothing built yet.</div>'))
    return (
        '<div class="space-tabs" data-space=delivery role=tablist>%s</div>'
        '<div class=space-views data-space=delivery><span class=space-views-label>View</span>'
        '<button type=button class="space-view on" data-view=preview>Preview</button>'
        '<button type=button class=space-view data-view=artifacts>Artifacts</button>'
        '<button type=button class=space-view data-view=checks>Checks</button></div>'
        '<div class=space-body data-space=delivery>%s%s'
        '<section class=space-pane data-view=checks hidden><iframe class="workspace-frame space-frame" '
        'title="Delivery checks" data-src="%s"></iframe></section></div>'
        % ("".join(tabs), "".join(previews), "".join(artifacts), _e(checks_url)))


SPACE_CSS = """
.space-tabs{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 8px}
.space-tab,.space-view,.ev-open{font:600 11.5px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
 border:1px solid var(--line);border-radius:7px;padding:3px 10px;cursor:pointer;background:var(--card);color:var(--mut)}
.space-tab{color:var(--fg);font-size:12.5px;padding:4px 12px}
.space-tab.on,.space-view.on,.space-view.shown{border-color:var(--acc);color:var(--acc)}
.space-count{margin-left:4px;color:var(--mut);font-weight:500}
.space-count.st-stale{color:#a43d35}.space-count.st-pass{color:#24733d}
.space-reads{margin:2px 0 8px;color:var(--mut);font:12px/1.6 system-ui,sans-serif}
.space-reads code{font-size:11.5px;color:var(--fg)}
.space-views{display:flex;align-items:center;gap:5px;margin:2px 0 12px}
.space-views-label{font:600 10px/1.5 system-ui,sans-serif;color:var(--mut);text-transform:uppercase;
 letter-spacing:.05em;margin-right:2px}
.space-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;margin:6px 0 10px;
 font:13.5px/1.45 system-ui,sans-serif}
.space-hint{color:var(--mut);font-size:12px}
.space-empty{color:var(--mut);font:13px/1.5 system-ui,sans-serif;padding:14px;border:1px dashed var(--line);
 border-radius:9px}
.space-source{white-space:pre-wrap;overflow-wrap:anywhere;margin:0;padding:10px 12px;border:1px solid var(--line);
 border-radius:9px;background:var(--card);font:12px/1.55 ui-monospace,Menlo,monospace}
.space-frame{display:block;width:100%;height:calc(100vh - 230px);min-height:360px;
 border:1px solid var(--line);border-radius:10px;background:var(--card)}
.ev-table{width:100%;border-collapse:collapse;font:13px/1.45 system-ui,sans-serif}
.ev-table th{text-align:left;font-weight:500;color:var(--mut);font-size:12px;padding:6px 8px;
 border-bottom:1px solid var(--line)}
.ev-table td{padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top}
.ev-table td:last-child{text-align:right;width:1%;white-space:nowrap}
.ev-row{cursor:pointer}
.ev-row:hover{background:color-mix(in srgb,var(--acc) 6%,var(--card))}
.ev-row.runs-selected{outline:2px solid var(--acc);outline-offset:-2px}
.ev-label{color:var(--mut)}
.ev-state{white-space:nowrap;color:var(--mut)}.ev-state.st-verified{color:#24733d}
details.paragraph-group>summary.prow::before{display:inline;content:"▸";position:static;transform:none;
 width:10px;height:auto;background:none;border-radius:0;color:var(--acc)}
details.paragraph-group[open]>summary.prow::before{content:"▾"}
.structure-card:not([open]) .structure-hint{display:none}
/* Evidence · Supporting Runs: Block > Job > Task > Run, each Run with the items it feeds.
   A file-tree look: guide lines, the level prefix (b03 j02 t01 r04) in the accent colour,
   the items by their short names (Edisplay13), grouped by type, a status dot, no box per row. */
.space-view[hidden]{display:none}
.sup-tree{font:13px/1.55 system-ui,sans-serif;margin:4px 0 12px}
.sup-node>summary{cursor:pointer;list-style:none;padding:2px 4px;border-radius:6px;text-transform:none;
 letter-spacing:normal;font:13px/1.55 system-ui,sans-serif;color:var(--fg);display:flex;align-items:center;gap:4px}
.sup-node>summary::-webkit-details-marker{display:none}
.sup-node>summary::before{content:"▸";width:12px;color:var(--mut);font-size:11px;flex:none}
.sup-node[open]>summary::before{content:"▾"}
.sup-node>summary:hover{background:color-mix(in srgb,var(--acc) 6%,transparent)}
.sup-world{margin:6px 0 10px}
.sup-world>summary{font-weight:600;font-size:13.5px}
.sup-path{color:var(--mut);font:12px ui-monospace,Menlo,monospace;font-weight:400}
.sup-node .sup-node,.sup-node>.sup-run{margin-left:10px;padding-left:12px;border-left:1px solid var(--line)}
.sup-node code{font:12.5px ui-monospace,Menlo,monospace;color:var(--fg)}
.sup-lvl{color:var(--acc);font-weight:700}
.sup-run{display:flex;align-items:center;gap:8px;padding:4px 8px;border-radius:0 7px 7px 0;cursor:pointer;min-height:28px}
.sup-run:hover{background:color-mix(in srgb,var(--acc) 6%,transparent)}
.sup-run.runs-selected{background:color-mix(in srgb,var(--acc) 12%,transparent);box-shadow:inset 2px 0 0 var(--acc)}
.sup-dot{width:8px;height:8px;border-radius:50%;background:var(--mut);flex:none}
.sup-dot.st-ready,.sup-dot.st-done{background:var(--ok)}
.sup-dot.st-held,.sup-dot.st-failed,.sup-dot.st-running{background:var(--warn)}
.sup-name{font:12.5px ui-monospace,Menlo,monospace}
.sup-state{font-size:12px;color:var(--mut)}
.sup-items{margin-left:auto;display:flex;flex-wrap:wrap;justify-content:flex-end;gap:4px 16px}
.sup-group{display:inline-flex;flex-wrap:wrap;align-items:center;gap:2px}
.sup-item{font:600 12px ui-monospace,Menlo,monospace;color:var(--fg);background:none;border:0;
 border-radius:5px;padding:1px 4px;cursor:pointer}
.sup-item:hover{background:color-mix(in srgb,var(--acc) 14%,transparent);color:var(--acc)}
/* Each Space: the content on the left, its Runs panel on the right at every width
   (JL 260927). The panel stays in view while the page scrolls; folded, it is a thin strip. */
.lens.show.space-split{display:flex;align-items:flex-start;gap:16px}
.space-split>.space-main{flex:1 1 auto;min-width:0}
.space-split>.runs-panel{flex:0 0 clamp(260px,30vw,600px);margin:0;position:sticky;top:8px;
 max-height:calc(100vh - 16px);display:flex;flex-direction:column;overflow:hidden}
.space-split>.runs-panel .runs-bar{flex-wrap:wrap}
.space-split>.runs-panel .runs-body{overflow:auto;min-height:0;grid-template-columns:1fr}
.space-split>.runs-panel .runs-types{flex-direction:row;flex-wrap:wrap}
.space-split>.runs-panel .run-type{gap:8px}
.space-split>.runs-panel.folded{flex-basis:42px}
.space-split>.runs-panel.folded .runs-bar{writing-mode:vertical-rl;flex-wrap:nowrap;padding:10px 9px;gap:10px}
"""

SPACE_JS = r"""
(function(){
 function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e){return null;}}
 function scope(space,view,label,mode){document.dispatchEvent(new CustomEvent('space-scope',{detail:{space:space,view:view,label:label,mode:mode}}));}
 function target(space,t){document.dispatchEvent(new CustomEvent('space-target',{detail:{space:space,target:t}}));}
 function lazy(root){root.querySelectorAll('iframe[data-src]').forEach(function(f){
  if(f.closest('[hidden]'))return;if(!f.getAttribute('src')&&f.dataset.src)f.setAttribute('src',f.dataset.src);});}
 document.querySelectorAll('.space-body').forEach(function(body){
  var space=body.dataset.space,lens=body.closest('.lens');
  var tabs=lens.querySelectorAll('.space-tabs[data-space="'+space+'"] .space-tab');
  var views=lens.querySelectorAll('.space-views[data-space="'+space+'"] .space-view');
  function current(list){var on=[].filter.call(list,function(b){return b.classList.contains('on');})[0];return on||list[0];}
  function show(){
   var tab=current(tabs),view=current(views);
   /* a tab may offer only some views (Supporting Runs: All items, Source); the
      chosen view stays chosen for the other tabs */
   var allow=(tab.dataset.views||'').split(' ').filter(Boolean),forced=false;
   views.forEach(function(b){b.hidden=allow.length>0&&allow.indexOf(b.dataset.view)<0;});
   if(view.hidden){view=[].filter.call(views,function(b){return !b.hidden;})[0]||view;forced=true;}
   views.forEach(function(b){b.classList.toggle('shown',b===view);});
   body.querySelectorAll('.space-pane').forEach(function(p){
    p.hidden=!((p.dataset.view===view.dataset.view)&&(!p.dataset.tab||p.dataset.tab===tab.dataset.tab));});
   if(lens.classList.contains('show'))lazy(body);
   store('space-tab:'+space,tab.dataset.tab);if(!forced)store('space-view:'+space,view.dataset.view);
   scope(space,tab.dataset.tab,tab.dataset.label,view.dataset.view);
   syncCards();
  }
  /* Evidence Card view: the cards come from the older Evidence page in a frame
     (same origin). Opening a card selects its item, like clicking its row; a
     selected item opens its card; the frame shows only the current tab's kind. */
  var frame=body.querySelector('.space-pane[data-view=card] iframe');
  var KIND={citations:'CITE',displays:'DISPLAY',values:'VALUE'};
  function frameDoc(){try{return frame&&frame.contentDocument&&frame.contentDocument.body?frame.contentDocument:null;}catch(e){return null;}}
  function selectItem(item){
   body.querySelectorAll('.ev-row.runs-selected').forEach(function(x){x.classList.remove('runs-selected');});
   var r=item&&body.querySelector('.ev-row[data-item="'+item+'"]');if(r)r.classList.add('runs-selected');
   target(space,item||'');
  }
  function syncCards(){
   var d=frameDoc();if(!d)return;
   if(!d.getElementById('space-card-style')){
    var st=d.createElement('style');st.id='space-card-style';
    st.textContent='body.embedded>header,.evidence-overview,.source-details{display:none!important}';
    d.head.appendChild(st);
    d.addEventListener('toggle',function(ev){var c=ev.target;
     if(!c.matches||!c.matches('details.evidence-card')||!c.open)return;
     var id=(c.dataset.evidenceId||'').match(/^E\d+/);if(id)selectItem(id[0]);},true);
   }
   var tab=current(tabs).dataset.tab;
   d.querySelectorAll('section.evidence-type-section').forEach(function(sec){
    sec.hidden=!!KIND[tab]&&sec.dataset.evidenceType!==KIND[tab];});
   var row=body.querySelector('.ev-row.runs-selected');
   if(row&&current(views).dataset.view==='card'){
    var card=d.querySelector('details.evidence-card[data-evidence-id^="'+row.dataset.item+'-"]');
    if(card){if(!card.open)card.open=true;card.scrollIntoView({block:'center'});}
   }
  }
  if(frame)frame.addEventListener('load',syncCards);
  function pick(list,key,value){list.forEach(function(b){b.classList.toggle('on',b.dataset[key]===value);});}
  tabs.forEach(function(b){b.addEventListener('click',function(){
   pick(tabs,'tab',b.dataset.tab);
   var chosen=body.querySelectorAll('.ev-row.runs-selected,.sup-run.runs-selected');
   chosen.forEach(function(x){x.classList.remove('runs-selected');});
   show();if(chosen.length)target(space,'');});});
  views.forEach(function(b){b.addEventListener('click',function(){pick(views,'view',b.dataset.view);show();});});
  var t=store('space-tab:'+space),v=store('space-view:'+space);
  if(t&&[].some.call(tabs,function(b){return b.dataset.tab===t;}))pick(tabs,'tab',t);
  if(v&&[].some.call(views,function(b){return b.dataset.view===v;}))pick(views,'view',v);
  var q=new URLSearchParams(location.search);
  if(space==='evidence'&&q.get('lens')==='evidence'&&q.get('focus'))pick(views,'view','card');
  show();
  /* A Draft evidence chip opens the Evidence Space on that item's card. */
  document.addEventListener('lens-shown',function(ev){
   if(ev.detail.name!==space)return;
   if(space==='evidence'&&ev.detail.focus){pick(views,'view','card');show();}
   else lazy(body);});
  new MutationObserver(function(){if(lens.classList.contains('show'))lazy(body);}).observe(lens,{attributes:true,attributeFilter:['class']});
  body.addEventListener('click',function(ev){
   /* Supporting Runs: an item chip opens that item on its own tab; a Run narrows the Runs panel */
   var chip=ev.target.closest('.sup-item');
   if(chip){pick(tabs,'tab',chip.dataset.tab);pick(views,'view','items');show();selectItem(chip.dataset.item);
    var hit=body.querySelector('.ev-row.runs-selected');if(hit)hit.scrollIntoView({block:'center'});return;}
   var run=ev.target.closest('.sup-run');
   if(run){var again=run.classList.contains('runs-selected');
    body.querySelectorAll('.sup-run.runs-selected').forEach(function(x){x.classList.remove('runs-selected');});
    if(!again)run.classList.add('runs-selected');target(space,again?'':run.dataset.run);return;}
   var row=ev.target.closest('.ev-row');if(!row)return;
   if(ev.target.closest('.ev-open')){
    selectItem(row.dataset.item);
    if(!frame.getAttribute('src'))frame.setAttribute('src',frame.dataset.src);
    pick(views,'view','card');show();return;}
   selectItem(row.classList.contains('runs-selected')?'':row.dataset.item);
  });
  body.addEventListener('keydown',function(ev){var row=ev.target.closest('.ev-row,.sup-run');if(row&&ev.key==='Enter')row.click();});
 });
 /* Draft Space: the Structure card remembers whether it is open. */
 var card=document.querySelector('.structure-card');
 if(card){
  if(store('structure-open')==='1')card.open=true;
  card.addEventListener('toggle',function(){store('structure-open',card.open?'1':'0');});
 }
})();
"""
