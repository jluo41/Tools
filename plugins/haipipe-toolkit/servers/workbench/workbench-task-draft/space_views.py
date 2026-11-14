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
import os
from src.common import delivery_dir, delivery_relative
import html
import re
from pathlib import Path
from urllib.parse import quote, unquote, urljoin

from src.outline_version import latest_outline, plan_dir
from src.item_table import short_name
from src.plan_layout import is_sectioned

# The parts of this module live in their own files; every name still answers here.
from live.space_views_assets import (  # noqa: F401
    SPACE_CSS, SPACE_JS, SPACE_SHELL_CSS, SPACE_VIEW_CSS,
)

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
        for name in re.findall(r"\brun-(?:citation|value|display)-[a-z0-9]+(?:-[a-z0-9]+)*", line):
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
        return urljoin(asset_base.rstrip("/") + "/", quote(rel))
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
        return urljoin("%s/%s/%s/" % (base, folder.group(1), folder.group(2)), quote(rel))
    return urljoin(base.rstrip("/") + "/", quote(rel))


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
    formats = [(key, label, delivery_relative(base) + "/" + folder.split("/", 1)[1], names)
               for key, label, folder, names in FORMATS]
    built = [key for key, _l, folder, _p in formats if (base / folder).is_dir()]
    first = "latex" if "latex" in built else (built[0] if built else "latex")
    tabs, previews, artifacts = [], [], []
    for key, label, folder, wanted in formats:
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
