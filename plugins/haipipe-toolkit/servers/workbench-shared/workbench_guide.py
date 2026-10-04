"""Shared Guide Space over family definitions; no instance ledger or writer.

The existing Excalidraw proxy opens virtual, source-backed Guide scenes in
its isolated viewing mode. Working Studio files and their save API retain
their native ownership. All URLs are origin-relative.
"""

import hashlib
import html
import json
import re
import textwrap
from pathlib import Path
from urllib.parse import parse_qs, quote, urlencode, urlparse

from live.guide_families import FAMILIES

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[3]
VIEWS = (("description", "Description", "What does this Workbench do?"),
         ("method", "Method", "How does this family reach a supported answer or product?"),
         ("roadmap-draw", "RoadMap Draw", "Space · View · Run type · Agent & Skill, in one drawing"),
         ("related-paper", "Related Paper", "Which papers does this Workbench build on?"))
DRAW_NAMES = {"roadmap-draw": "RoadMap"}
# Earlier View keys (a saved link, a family's `explain` entry) and the View that now holds them.
OLD_VIEWS = {"skill-set": "roadmap-draw", "methods": "method", "workbench": "roadmap-draw", "folder-map": "roadmap-draw"}


def esc(value):
    return html.escape(str(value), quote=True)


def url(**values):
    return "/_board/guide?" + urlencode(values)


# A family's declared drawings, view only, through Guide's own route (JL 261003: a `--only
# labeling` host refuses /_excalidraw/, so the methods canvas and the Workbench design came up
# 404). `method` is the entry's method_drawing; `explain-<view>` is the board an `explain`
# drawing names. Only these declared files are served, never an arbitrary path.
def family_drawing(profile, key):
    if key == "method":
        return profile.get("method_drawing") or None
    if key.startswith("explain-"):
        explain = (profile.get("explain") or {}).get(key[len("explain-"):])
        if explain and explain[0] == "/_excalidraw/":
            board = str(explain[1].get("board", ""))
            return board[len("Tools/"):] if board.startswith("Tools/") else None
    return None


def drawing_url(family, key, file=""):
    # `file` names the declared drawing, so the address says which file it shows; Guide checks it
    return url(mode="drawing", guide="1", board=url(mode="drawing-scene", family=family, drawing=key).lstrip("/"),
               family=family, drawing=key, file=file)


def script_json(value):
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c")


def family_profile(family, context):
    profile = FAMILIES[family]
    if family == "design" and context.get("file") not in (None, "", "board.md"):
        return dict(profile, presenter="plugins/haipipe-toolkit/servers/workbench-design/design.py",
                    spaces=[("Board › Design Tasks", "One row per Design page: its task, method, N designs and how many are ready"),
                            ("Design Goal", "The task once: Aim · Venue · Rules · Resources (the starting text and its named elements) · Leave out"),
                                     ("Design", "The element matrix, then one card per design: Design · Rationale · Evaluation, its runs folded inside"),
                                     ("Delivery", "Every design whose independent Verify passed, word for word, and the csv")],
                    folders=[("Design Goal", "Design Page owner", "<same-stem Page>.md", "*.md"),
                             ("Design items", "Design Folder owner", "draft/<stem>-design-items.md", "draft/*-design-items.md"),
                             ("Runs", "Design Run owner", "runs/", "runs"),
                             ("Results and element records", "Design Run owner", "results/<run>/ (content, checks, elements.yaml)", "results"),
                             ("Delivery", "Design delivery owner", "delivery/", "delivery")])
    return profile


def instance(context):
    """Whether a Guide request names an instance whose paths it can resolve."""
    return bool(context.get("path") or context.get("file"))


def mount_guide(document, family, context, nav, native):
    """Attach one Guide button to a native Space row; retain its own layout."""
    if family not in FAMILIES or not (instance(context) or FAMILIES[family].get("standalone")):
        return document
    config = dict(family=family, context=context, nav=nav, native=native)
    styles = (HERE / "assets/guide-mount.css").read_text(encoding="utf-8")
    javascript = (HERE / "assets/guide-mount.js").read_text(encoding="utf-8")
    insertion = (f'<style>{styles}</style><script type="application/json" id="wb-guide-mount">'
                 f'{script_json(config)}</script><script>{javascript}</script>')
    return document.replace("</body>", insertion + "</body>", 1)


def contract_path(family, index, context=None):
    profile = family_profile(family, context or {})
    paths = ([item["path"] for item in profile["skills"]] + [profile["presenter"],
             "plugins/haipipe-toolkit/servers/workbench-shared/guide_families.py",
             "plugins/haipipe-toolkit/servers/workbench-shared/workbench_guide.py"])
    if index < 0 or index >= len(paths):
        raise ValueError("Unknown Guide source")
    candidate = (REPOSITORY / paths[index]).resolve()
    candidate.relative_to(REPOSITORY.resolve())
    if not candidate.is_file():
        raise FileNotFoundError(paths[index])
    return candidate


def folder_matches(root, source, family, row, context, allowed=None):
    """Resolve declared patterns inside the instance, with the static boundary."""
    from host_registry import static_path_allowed
    allowed = allowed or (lambda candidate: static_path_allowed(root, candidate))
    folders = family_profile(family, context)["folders"]
    if row < 0 or row >= len(folders):
        raise ValueError("Unknown folder mapping")
    pattern = folders[row][3]
    base = source.parent
    matches = []
    for candidate in base.glob(pattern):
        if allowed(candidate):
            matches.append(candidate)
            if len(matches) >= 80:
                break
    return sorted(matches)


class Scene:
    """Deterministic Excalidraw elements, plus an accessible SVG projection."""
    def __init__(self, family, view):
        self.prefix = family + "-" + view
        self.elements, self.svg = [], []
        self.height = 120

    def add(self, kind, x, y, width, height, **extra):
        identity = self.prefix + "-" + str(len(self.elements))
        element = dict(id=identity, type=kind, x=x, y=y, width=width, height=height,
                       angle=0, strokeColor="#495057", backgroundColor="transparent",
                       fillStyle="solid", strokeWidth=1.5, strokeStyle="solid",
                       roughness=1, opacity=100, groupIds=[], frameId=None,
                       roundness=None, seed=int(hashlib.sha256(identity.encode()).hexdigest()[:7], 16),
                       version=1, versionNonce=1, isDeleted=False, boundElements=None,
                       updated=1, link=None, locked=False)
        element.update(extra)
        self.elements.append(element)
        self.height = max(self.height, y + height + 24)
        return element

    def text(self, x, y, value, size=18, color="#495057", mono=False):
        lines = str(value).splitlines()
        self.add("text", x, y, max(map(len, lines), default=0) * size * .62,
                 len(lines) * size * 1.25, text=value, originalText=value, fontSize=size,
                 fontFamily=3 if mono else 8, textAlign="left", verticalAlign="top",
                 containerId=None, autoResize=True, lineHeight=1.25, strokeColor=color)
        for index, line in enumerate(lines):
            self.svg.append(f'<text x="{x}" y="{y + size + index * size * 1.25}" fill="{color}" '
                            f'font-size="{size}" font-family="{("monospace" if mono else "sans-serif")}">{esc(line)}</text>')

    def box(self, x, y, width, title, body="", link=None, color="#1864ab"):
        title = "\n".join(textwrap.wrap(title, width=max(1, int((width - 28) / 11.2))))
        title_height = max(52, len(title.splitlines()) * 22.5 + 24)
        height = title_height + (len(body.splitlines()) * 22 if body else 0)
        start = len(self.elements)
        box = self.add("rectangle", x, y, width, height, backgroundColor="#f8f9fa", link=link,
                       roundness={"type": 3})
        self.svg.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="6" fill="#f8f9fa" stroke="#ced4da"/>')
        self.text(x + 14, y + 12, title, 18, color)
        if body:
            self.text(x + 14, y + title_height - 12, body, 16)
        for element in self.elements[start:]:
            element["groupIds"] = [box["id"] + "-group"]
        return height

    def arrow(self, x, y, dx, dy, label):
        self.add("arrow", x, y, abs(dx), abs(dy), points=[[0, 0], [dx, dy]],
                 lastCommittedPoint=None, startBinding=None, endBinding=None,
                 startArrowhead=None, endArrowhead="arrow", elbowed=False)
        self.svg.append(f'<path d="M{x} {y} l{dx} {dy}" stroke="#495057" fill="none" marker-end="url(#arrow)"/>')
        if label:
            self.text(x + (dx / 2 - 24 if dx else 12), y + (dy / 2 - 10 if dy else -25), label, 14)

    def data(self):
        return dict(type="excalidraw", version=2, source="haipipe-workbench-guide",
                    elements=self.elements, appState={"viewBackgroundColor": "#ffffff", "gridSize": None}, files={})

    def vector(self, title):
        return ('<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 1480 %s">'
                '<title>%s</title><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
                'refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="#495057"/></marker></defs>%s</svg>'
                % (self.height, esc(title), "".join(self.svg)))


def wrap(value, width):
    return "\n".join(textwrap.fill(line, width=width) for line in str(value).splitlines())


def table_scene(family, view, profile, rows):
    """The Workbench Table drawn as a table: Space · View · Run type · Agent & Skill, and
    Folder when the table has it; then the family's workflow when it declares `flow`.

    Studio style: transparent boxes, one colored stroke per column, every label bound
    inside its box, Comic Shanns. A repeated Space or View cell spans its rows."""
    scene = Scene(family, view)
    scene.text(0, 0, profile["label"] + " · RoadMap", 26, "#1e1e1e")
    columns = (("Space", 200, "#1971c2"), ("View", 200, "#2f9e44"), ("Run type", 280, "#e8590c"),
               ("Agent & Skill", 420, "#9c36b5")) + ((("Folder", 420, "#0c8599"),) if "Folder" in rows[0] else ())
    xs, x = [], 0
    for _, width, _ in columns:
        xs.append(x)
        x += width + 12
    top, row_h, gap = 96, 66, 8

    def cell(key, x, y, width, height, label, color, size=16):
        box = scene.add("rectangle", x, y, width, height, strokeColor=color, backgroundColor="transparent",
                        roundness={"type": 3}, boundElements=[{"type": "text", "id": key + "-label"}])
        scene.add("text", x + 8, y + 8, width - 16, height - 16, id=key + "-label", text=label, originalText=label,
                  fontSize=size, fontFamily=8, textAlign="center", verticalAlign="middle", containerId=box["id"],
                  autoResize=True, lineHeight=1.25, strokeColor="#1e1e1e")
        scene.svg.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="8" fill="none" stroke="{color}"/>')
        for i, line in enumerate(label.splitlines()):
            scene.svg.append(f'<text x="{x + width / 2}" y="{y + height / 2 + (i - (len(label.splitlines()) - 1) / 2) * 20 + 5}" '
                             f'text-anchor="middle" font-size="{size}" font-family="sans-serif">{esc(line)}</text>')

    for i, (name, width, color) in enumerate(columns):
        cell(f"{scene.prefix}-head-{i}", xs[i], 44, width, 40, name, color, 18)
    plain = lambda value: "—" if value in ("", "none") else value
    y = top
    for i, row in enumerate(rows):
        for c, key in enumerate(("Space", "View")):
            if i == 0 or any(rows[i - 1][k] != row[k] for k in ("Space", "View")[:c + 1]):
                n = 1
                while i + n < len(rows) and all(rows[i + n][k] == row[k] for k in ("Space", "View")[:c + 1]):
                    n += 1
                cell(f"{scene.prefix}-{key.lower()}-{i}", xs[c], y, columns[c][1], n * row_h + (n - 1) * gap,
                     wrap(row[key], 18), columns[c][2], 17 if c == 0 else 16)
        cell(f"{scene.prefix}-run-{i}", xs[2], y, columns[2][1], row_h, wrap(plain(row["Run type"]), 28), columns[2][2])
        who = plain(row["Agent"]) + ("\n" + plain(row["Skill"]) if plain(row["Skill"]) != "—" else "")
        cell(f"{scene.prefix}-who-{i}", xs[3], y, columns[3][1], row_h, who, columns[3][2], 14)
        if len(columns) > 4:
            cell(f"{scene.prefix}-folder-{i}", xs[4], y, columns[4][1], row_h, wrap(plain(row["Folder"]), 46),
                 columns[4][2], 13)
        y += row_h + gap
    scene.text(0, y + 10, "(new) marks a planned agent or skill. Drawn from " + Path(profile["table"]).name
               + " in " + Path(profile["table"]).parent.parent.name + ".", 14)
    if profile.get("flow"):
        flow_scene(scene, profile["flow"], y + 80, cell)
    return scene


def flow_scene(scene, flow, top, cell):
    """The workflow under the table (a family's `flow`): the logic row Question → Work → Report
    over the data row Input → Processing → Output, a link between each pair, and the loop that
    repeats it."""
    scene.text(0, top, "Workflow · how one question is answered, and how it repeats", 22, "#1e1e1e")
    width, height, gap, drop = 380, 104, 90, 80
    xs = [i * (width + gap) for i in range(3)]
    rows = ((top + 56, flow["logic"], "#1971c2", ("→", "→")),
            (top + 56 + height + drop, flow["data"], "#2f9e44", ("→", "→")))
    for r, (y, boxes, color, _) in enumerate(rows):
        for c, (title, body) in enumerate(boxes):
            cell(f"{scene.prefix}-flow-{r}-{c}", xs[c], y, width, height, title + "\n" + wrap(body, 40), color, 15)
            if c < 2:
                scene.arrow(xs[c] + width + 6, y + height / 2, gap - 12, 0, "")
    logic_y, data_y = rows[0][0], rows[1][0]
    for c, label in enumerate(flow["links"]):
        up = c == len(flow["links"]) - 1          # the last link runs up: the output fills the report
        x = xs[c] + width / 2
        if up:
            scene.arrow(x, data_y - 4, 0, -(drop - 8), label)
        else:
            scene.arrow(x, logic_y + height + 4, 0, drop - 8, label)
    # the loop: from Report, round the two rows, back into Question
    sx, sy, bottom = xs[2] + width, logic_y + height / 2, data_y + height + 50
    points = [[0, 0], [50, 0], [50, bottom - sy], [-sx - 50, bottom - sy], [-sx - 50, 0], [-sx - 6, 0]]
    scene.add("arrow", sx, sy, sx + 100, bottom - sy, points=points, lastCommittedPoint=None, startBinding=None,
              endBinding=None, startArrowhead=None, endArrowhead="arrow", elbowed=False, strokeColor="#e8590c")
    scene.svg.append('<polyline fill="none" stroke="#e8590c" marker-end="url(#arrow)" points="'
                     + " ".join(f"{sx + px},{sy + py}" for px, py in points) + '"/>')
    scene.text(0, bottom + 14, "↻ " + wrap(flow["repeat"], 120), 16, "#e8590c")


def guide_scene(family, view, context):
    """The family's one RoadMap: its Workbench Table when it has one, else four columns,
    skills to folders."""
    profile = family_profile(family, context)
    rows = table_rows(profile)
    if rows:
        return table_scene(family, view, profile, rows)
    scene = Scene(family, view)
    scene.text(24, 14, profile["label"] + " · RoadMap", 26, "#1e1e1e")
    width, gap, top = 320, 56, 116
    xs = [24 + i * (width + gap) for i in range(4)]
    for x, name, color in zip(xs, ("Skills", "Method", "Workbench", "Folders"), ("#2b8a3e", "#1864ab", "#1864ab", "#2b8a3e")):
        scene.text(x, 70, name, 20, color)
    for x, label in zip(xs[:3], ("define", "shown in", "reads from")):
        scene.arrow(x + width + 6, 84, gap - 12, 0, label)
    y = top
    for i, item in enumerate(profile["skills"]):
        y += scene.box(xs[0], y, width, Path(item["path"]).parent.name, wrap(item["role"], 34),
                       url(mode="source", family=family, source=i), "#2b8a3e") + 14
    y = top
    for i, (name, description) in enumerate(profile["method"]):
        height = scene.box(xs[1], y, width, f"{i + 1}. {name}", wrap(description, 34))
        if i < len(profile["method"]) - 1:
            scene.arrow(xs[1] + width / 2, y + height + 3, 0, 30, "then")
        y += height + 36
    y = top
    for name, content in [("Guide Space", "This explanation: Description / Method / RoadMap Draw / Related Paper")] + [
            (name + " Space", content) for name, content in profile["spaces"]]:
        y += scene.box(xs[2], y, width, name, wrap(content, 34), color="#1864ab" if name == "Guide Space" else "#2b8a3e") + 14
    rows = [("Guide", "plugins/haipipe-toolkit/servers/workbench-shared/guide_families.py",
             url(mode="source", family=family, source=len(profile["skills"]) + 1, **context)),
            ("Working UI", profile["presenter"], url(mode="source", family=family, source=len(profile["skills"]), **context))]
    rows += [(surface + " · " + owner, pattern, url(mode="folder", family=family, row=i, **context) if instance(context) else None)
             for i, (surface, owner, pattern, _) in enumerate(profile["folders"])]
    y = top
    for title, pattern, link in rows:
        # Break long paths at folder boundaries so names stay whole.
        lines, line = [], ""
        for part in re.findall(r'[^/\s]+[/\s]*|[/\s]+', pattern):
            if line and len(line + part) > 34:
                lines.append(line.rstrip())
                line = ""
            line += part
        if line:
            lines.append(line.rstrip())
        y += scene.box(xs[3], y, width, title, "\n".join(lines), link, "#2b8a3e") + 14
    scene.text(24, scene.height + 4, "Paths are conventions. " + ("Open a folder box to resolve it in this instance." if instance(context)
               else "Open Guide from a Board to resolve them in that instance."), 16)
    return scene


def drawing_row(family, view, context, opened=False):
    params = dict(family=family, view=view, **context)
    canvas = url(mode="canvas", guide="1", board=url(mode="scene", **params).lstrip("/"), **params)
    vector = url(mode="svg", **params)
    return (f'<details class="wg-drawing" data-drawing="{view}"{" open" if opened else ""}>'
            # the card is its name only (JL 261003: "Make the card clean")
            f'<summary><span><strong>{DRAW_NAMES[view]}</strong></span></summary><div class="wg-drawing-body">'
            f'<div class="wg-canvas-actions"><span>{esc(family)} / {view}.excalidraw</span>'
            f'<span><a href="{esc(url(mode="scene", **params))}" download="{esc(family)}-{view}.excalidraw">Download Excalidraw</a> · '
            f'<a href="{esc(canvas)}" target="_blank" rel="noopener">Open full screen ↗</a></span></div>'
            f'<iframe title="{esc(DRAW_NAMES[view])}" referrerpolicy="no-referrer" data-src="{esc(canvas)}"></iframe>'
            f'<noscript><img src="{esc(vector)}" alt="{esc(DRAW_NAMES[view])}"></noscript>'
            '</div></details>')


def explain_html(profile, view, context, family=None):
    """A family's own explanation page for one Guide View (its optional `explain` entry:
    view -> (route, params)), opened inside Guide. The family's presenter renders and owns
    it; Guide only frames it, for the instance the context names."""
    explain = (profile.get("explain") or {}).get(view)
    if not explain:
        return ""
    route, params, title = (tuple(explain) + ("", ""))[:3]
    drawing = route == "/_excalidraw/"
    # a design drawing opens read-only in Guide's viewing mode (guide=1), at a fixed canvas height
    source = (drawing_url(family, "explain-" + view, family_drawing(profile, "explain-" + view) or "") if drawing and family else
              route + "?" + urlencode(dict(params, guide="1") if drawing else dict(params, path=context.get("path") or "")))
    size = "height:550px" if drawing else "min-height:70vh"
    # a titled explanation folds like the RoadMap card, closed at first so the View opens as a list
    # of cards (JL 261003: "why this draw cannot be hidden?", "make it into this style"), and its
    # frame loads when the card opens (guide.js); an untitled one is the View's body and stays open
    head, tail = ((f'<details class="wg-drawing wg-explain" data-drawing="{esc(view)}-explain"><summary><span><strong>' + esc(title)
                   + '</strong></span></summary><div class="wg-drawing-body">', '</div></details>') if title else
                  ('<section class="wg-explain">', '</section>'))
    return (head +
            f'<iframe class="wg-explain-frame" title="{esc(profile["label"])} · {esc(view)}" {"data-src" if title else "src"}="{esc(source)}" '
            # no referrer: the Excalidraw viewer refuses a same-site embed that sends one
            'referrerpolicy="no-referrer" '
            f'style="display:block;width:100%;{size};border:0"></iframe>'
            '<script>addEventListener("message",function(e){if(e.origin!==location.origin||'
            'e.data?.kind!=="haipipe-explain-height")return;document.querySelectorAll(".wg-explain-frame").forEach('
            'function(f){if(f.contentWindow===e.source)f.style.height=Math.ceil(e.data.height)+"px"})})</script>' + tail)


TABLE_COLUMNS = ("Space", "View", "Run type", "Agent", "Skill")
TABLE_HEAD = ("Space", "View", "Run type", "Agent · Skill")


def table_rows(profile):
    """The family's Workbench Table rows, or [] when it declares none or the file has none."""
    if not profile.get("table"):
        return []
    import importlib.util
    reader = REPOSITORY / "plugins/haipipe-toolkit/skills/0_utils/table-workbench/ref/render_workbench_table.py"
    try:
        spec = importlib.util.spec_from_file_location("render_workbench_table", reader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.read_table(REPOSITORY / profile["table"])
    except (OSError, SystemExit):
        return []


def workbench_table(profile):
    """The family's Workbench Table (skills/0_utils/table-workbench) as one HTML table: Space ·
    View · Run type · Agent · Skill (one column: the agent, the skill under it), and Folder when the
    table has it (where the run writes); a repeated Space or View cell is merged into the first.
    Empty when the family declares no `table` or the file has no Workbench Table."""
    rows = table_rows(profile)
    if not rows:
        return ""

    def cell(value):
        planned = value.endswith(" (new)")
        name = value.removesuffix(" (new)")
        if name in ("", "none"):
            return '<span class="wg-none">—</span>'
        return f'<code>{esc(name)}</code>' + (' <span class="wg-planned">planned</span>' if planned else '')

    def span(i, key):
        n = 1
        while i + n < len(rows) and all(rows[i + n][k] == rows[i][k] for k in TABLE_COLUMNS[:TABLE_COLUMNS.index(key) + 1]):
            n += 1
        return n

    folder = bool(rows) and "Folder" in rows[0]
    body = []
    for i, row in enumerate(rows):
        tds = []
        for key in ("Space", "View"):
            first = i == 0 or any(rows[i - 1][k] != row[k] for k in TABLE_COLUMNS[:TABLE_COLUMNS.index(key) + 1])
            if first:
                tds.append(f'<th scope="rowgroup" rowspan="{span(i, key)}">{esc(row[key])}</th>')
        run = row["Run type"]
        tds.append(f'<td>{esc(run) if run != "none" else "<span class=wg-none>—</span>"}</td>')
        pair = (f'<span class="wg-agent">{cell(row["Agent"])}</span><span class="wg-skill">{cell(row["Skill"])}</span>'
                if row["Agent"] != "none" or row["Skill"] != "none" else cell("none"))
        tds.append(f'<td>{pair}</td>')
        if folder:
            tds.append(f'<td>{cell(row["Folder"])}</td>')
        body.append("<tr>" + "".join(tds) + "</tr>")
    head = "".join(f"<th>{c}</th>" for c in TABLE_HEAD + (("Folder",) if folder else ()))
    # a closed card like the drawings beside it, its name only (JL 261003: "make it into this
    # style", "remove this, we don't need this")
    return ('<details class="wg-drawing" data-drawing="workbench-table"><summary><span><strong>Workbench Table</strong>'
            '</span></summary><div class="wg-drawing-body">'
            f'<div class="wg-table"><table><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div></div></details>')


def guide_runs(profile, view):
    """Guide's Runs panel: the family's Workbench Table rows on the Guide Space, those of the
    open View first (JL 261003: "always put the run in the right panel"). Each run type gives
    its agent, skill and a prompt to copy; Guide keeps no run records, so none are listed."""
    rows = [r for r in table_rows(profile) if r["Space"] == "Guide" and r["Run type"] not in ("", "none")]
    if not rows:
        return ""
    from live.runs_panel import PANEL_CSS, PANEL_JS, SPLIT_CSS, panel_markup
    label = dict((key, name) for key, name, _ in VIEWS)[view]
    rows = [r for r in rows if r["View"] == label] or rows
    plain = lambda value: value.replace(" (new)", " (planned)")
    kinds = [{"label": r["Run type"], "pattern": "", "views": "",
              "skills": [r["Skill"].replace(" (new)", "")] if r["Skill"] not in ("", "none") else [],
              "prompt": (f'Run with {plain(r["Agent"])}. {r["Run type"]} for the {profile["label"]} workbench, '
                         f'Guide › {r["View"]}, following {plain(r["Skill"])}.'
                         + (f' The person signs {r["Person signs"]}.' if r.get("Person signs") not in ("", "none", None) else ""))}
             for r in rows]
    panel = panel_markup("guide", kinds, [[] for _ in kinds], base=REPOSITORY, fill=lambda row: {},
                         whole=f'the {profile["label"]} Guide')
    css = (".wg-split{--line:var(--wg-rule);--card:var(--wg-bg);--acc:var(--wg-blue);--fg:var(--wg-ink);--mut:var(--wg-muted)}"
           + PANEL_CSS + SPLIT_CSS)
    return f'<style>{css}</style>{panel}<script>{PANEL_JS}</script>'


def guide_html(family, view, context, embedded=False, tab_url=None, prelude="", title=None):
    """One Guide View. A host page may supply its own View links and a prelude above them."""
    view = OLD_VIEWS.get(view, view)
    profile = family_profile(family, context)
    tab_url = tab_url or (lambda key: url(family=family, view=key, embed=int(embedded), **context))
    css = (HERE / "assets/guide.css").read_text(encoding="utf-8")
    js = (HERE / "assets/guide.js").read_text(encoding="utf-8")
    tabs = "".join(f'<a href="{esc(tab_url(key))}" '
                   f'aria-current="{("page" if key == view else "false")}">{label}</a>' for key, label, _ in VIEWS)
    source_links = "".join(f'<li><a href="{esc(url(mode="source", family=family, source=i))}" '
                          f'target="_blank" rel="noopener">{esc(Path(item["path"]).parent.name)}</a>'
                          f'<span>{esc(item["role"])}</span></li>' for i, item in enumerate(profile["skills"]))
    explain = profile.get("explain") or {}

    def lead(keys):
        """A family's own explanation pages for these View keys: before the View's body or after it."""
        first = "".join(explain_html(profile, key, context, family) for key in keys
                        if len(explain.get(key) or ()) > 3 and explain[key][3] in ("first", "only"))
        after = "".join(explain_html(profile, key, context, family) for key in keys
                        if explain.get(key) and not (len(explain[key]) > 3 and explain[key][3] in ("first", "only")))
        return first, after

    section = lambda title, text: f'<section class="wg-explanation"><h2>{esc(title)}</h2><p>{esc(text)}</p></section>'
    if view == "description":
        first, after = lead(["description"])
        content = first + f'<section class="wg-explanation"><p>{esc(profile.get("description") or profile["boundary"])}</p></section>'
        content += "".join(section(name + " Space", body) for name, body in profile["spaces"])
        content += after
    elif view == "method":
        first, after = lead(["method", "methods"])
        # "only": the family's page carries its own steps, so Guide's list would repeat them (JL 261003,
        # Design: "why we still have this? I am thinking to merge this together")
        only = (explain.get("method") or ())[3:4] == ("only",)
        steps = "" if only else "".join(section(f"{i}. {name}", body) for i, (name, body) in enumerate(profile["method"], 1))
        content = first + steps + after
    elif view == "roadmap-draw":
        first, after = lead(["roadmap-draw", "skill-set", "workbench", "folder-map"])
        folders = "".join((f'<li><a href="{esc(url(mode="folder", family=family, row=i, **context))}" target="_blank" '
                           f'rel="noopener">{esc(surface)} · <code>{esc(pattern)}</code> ↗</a></li>') if instance(context) else
                          f'<li>{esc(surface)} · <code>{esc(pattern)}</code></li>'
                          for i, (surface, _, pattern, _) in enumerate(profile["folders"]))
        # a family with a Workbench Table shows it in place of the Skills and Workbench lists (JL 261002)
        table = workbench_table(profile)
        lists = table or ('<section class="wg-explanation"><h2>Skills</h2><ul class="wg-sources">' + source_links + '</ul></section>'
                          '<section class="wg-explanation"><h2>Workbench</h2><ul class="wg-sources">' +
                          "".join(f'<li>{esc(name)} Space<span>{esc(body)}</span></li>' for name, body in profile["spaces"]) +
                          '</ul></section>')
        # a family with a Workbench Table shows no Folders list beside it (JL 261002: "remove this part")
        folders = ('' if table else
                   f'<section class="wg-explanation"><h2>Folders</h2><ul class="wg-sources">{folders}</ul></section>')
        content = first + drawing_row(family, view, context, not first) + lists + folders + after
    else:
        first, after = lead(["related-paper"])
        # a family's papers table (skills/0_utils/table-papers) renders here through the shared
        # Related Paper cards; a family whose own papers page leads the View needs neither
        papers = ""
        if profile.get("papers_table") and not (profile.get("explain") or {}).get("related-paper"):
            from live.related_papers import PAPERS_CSS, PAPERS_JS, papers_page
            papers = ('<style>.wg-papers{--line:var(--wg-rule);--mut:var(--wg-muted);--acc:var(--wg-blue);'
                      '--fg:var(--wg-ink);--soft:var(--wg-wash);--ok:#2f9e44}' + PAPERS_CSS
                      # Guide's frame takes its page's height: a PDF sized by the viewport would grow it without end
                      + '.wg-papers .rp-frame{height:720px}</style>'
                      '<section class="wg-papers">' + papers_page(None, REPOSITORY.parent, REPOSITORY / profile["papers_table"])
                      + f'</section><script>{PAPERS_JS}</script>')
        none = ('' if papers or (profile.get("explain") or {}).get("related-paper") else
                '<section class="wg-explanation"><p>No related papers are declared for this family yet. '
                'A workbench keeps them in <code>ref/&lt;name&gt;-papers.md</code> beside its skill '
                '(skills/0_utils/table-papers) and names it as <code>papers_table</code> in its '
                '<code>guide_families.py</code> entry.</p></section>')
        content = first + papers + none + after
    heading = prelude or ('' if embedded else f'<header><h1>{esc(profile["label"])} Workbench</h1><p>Guide</p></header>')
    boot = dict(family=family, view=view, context=context)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(title or profile["label"] + " · Guide")}</title><style>{css}</style></head><body>'
            # the Views and their content sit in one box, as a workbench Space's content does (JL 261003)
            # the Guide Space's runs sit in the shared Runs panel on the right, as every Space's do
            f'{heading}<div class="split wg-split"><div class="wg-shell space-main"><nav class="wg-views" aria-label="Guide Views">{tabs}</nav><main>'
            f'<h1>{dict((key, label) for key, label, _ in VIEWS)[view]}</h1>{content}</main></div>{guide_runs(profile, view)}</div>'
            f'<script type="application/json" id="wg-boot">{script_json(boot)}</script><script>{js}</script></body></html>')


# Guide › Method's family page (JL 261003: "create a method canvas as they do"): the family's
# method file with its method cards, then its methods canvas, as Insight's and Design's pages show
# them. A family names `method_doc` and `method_drawing` in its guide_families.py entry and points
# its `explain["method"]` here (mode=method); the cards and the papers are drawn by the Design
# workbench's renderer, so every family's cards look the same. The canvas opens editable: it is
# the source, and edits save back to the skill's ref/.
def method_page_html(family, profile, editable=True):
    from live.designboard import _CSS, _plain_md, method_cards
    doc = REPOSITORY / profile["method_doc"]
    papers = REPOSITORY / profile.get("papers_table", "")
    if doc.is_file():
        cards = method_cards(REPOSITORY, REPOSITORY.parent, doc, papers) if papers.is_file() else None
        page = re.sub(r"<h1>.*?</h1>", "", _plain_md(doc.read_text(encoding="utf-8"), cards), count=1)
        # every part folds, in the card style of Design's Method page (JL 261003: "make each
        # section collapsable", "this is not updated following others"), and every card starts
        # closed, so the page opens as a list of its parts (JL 261003: "make it into this style")
        lead, *parts = re.split(r"(?=<h2>)", page)

        def fold(part):
            title = re.match(r"<h2>(.*?)</h2>", part)
            name = re.sub(r"<[^>]+>", "", title.group(1))
            return (f'<details class=sec-fold><summary><strong>{name}</strong>'
                    f'</summary><div class=sec-body>{part[title.end():]}</div></details>')
        page = lead + "".join(fold(part) for part in parts)
        body = f'<article class=theory>{page}</article>'
    else:
        body = f'<div class=empty>No method file yet: this family keeps it as <code>{esc(profile["method_doc"])}</code>.</div>'
    drawing = profile.get("method_drawing", "")
    if drawing and (REPOSITORY / drawing).is_file():
        # view only inside Guide; it is edited full screen, in its own tab (JL 261003: an editable
        # methods canvas open in Guide beside a Page's editable RoadMap shared the browser's
        # drawing storage, and the RoadMap saved the methods drawing into its own file)
        src = drawing_url(family, "method", drawing)
        edit = "/_excalidraw/?board=" + quote("Tools/" + drawing, safe="/") + "&edit=1"
        # no file notes on screen (JL 261003): the bar holds only the way to open it full screen;
        # a host that cannot edit (`--only`) shows no edit link
        canvas = ('<div class=st-bar><span></span>'
                  + (f'<a href="{esc(edit)}" target="_blank" rel="noopener">Edit full screen ↗</a>' if editable else '')
                  + '</div>'
                  # no referrer: Excalidraw refuses a same-site embed that sends one
                  f'<iframe class=st-frame title="{esc(profile["label"])} methods" referrerpolicy="no-referrer" '
                  f'data-src="{esc(src)}"></iframe>'
                  # the canvas loads only near view: it takes focus as it loads, and a canvas loaded at
                  # once scrolls Guide down to it and leaves the page blank above (as Insight's does)
                  "<script>(function(){var fs=document.querySelectorAll('iframe.st-frame[data-src]'),"
                  "go=function(f){if(!f.getAttribute('src'))f.setAttribute('src',f.dataset.src)};"
                  "if(!window.IntersectionObserver){fs.forEach(go);return}"
                  "var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)"
                  "{go(e.target);io.unobserve(e.target)}})},{rootMargin:'400px'});fs.forEach(function(f){io.observe(f)});"
                  # a reader may have left the drawing card closed: opening it loads the canvas (as Design's does)
                  "document.addEventListener('toggle',function(ev){var d=ev.target;if(d.matches&&d.matches('details.draw-fold')&&d.open)"
                  "d.querySelectorAll('iframe.st-frame[data-src]').forEach(go)},true)})()</script>")
    else:
        canvas = (f'<div class=empty>No methods drawing yet: draw it from the method file with '
                  f'<code>servers/workbench-shared/studio/method-canvas.py</code>.</div>')
    height = ("<script>(function(){function post(){parent.postMessage({kind:'haipipe-explain-height',"
              "height:document.documentElement.scrollHeight},location.origin)}"
              "if(window.ResizeObserver)new ResizeObserver(post).observe(document.body);"
              "addEventListener('load',post);document.addEventListener('toggle',post,true)})()</script>")
    # a reader's folds are kept per family and part, so the page opens as it was left
    remember = ("<script>(function(){document.querySelectorAll('details.sec-fold,details.draw-fold').forEach(function(d,i){"
                f"var k='method-fold:{esc(family)}:'+i;try{{var v=localStorage.getItem(k);if(v!==null)d.open=v==='1'}}catch(e){{}}"
                "d.addEventListener('toggle',function(){try{localStorage.setItem(k,d.open?'1':'0')}catch(e){}})})})()</script>")
    # the page sits inside Guide: a pinch over it must not zoom the tab (guide-mount.js says why)
    no_pinch = ("<script>addEventListener('wheel',function(e){if(e.ctrlKey)e.preventDefault()},{passive:false})</script>")
    return ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
            # inside Guide the frame takes this page's height, so nothing here is sized by the viewport
            f'<title>{esc(profile["label"])} · Method</title><style>{_CSS}body{{max-width:none;padding:2px 2px 12px}}'
            '.st-frame{height:640px;min-height:0}'
            # the folding cards (draw-fold, sec-fold) are Design's, from its _CSS above
            'article.theory h3{font-size:14.5px;margin:18px 0 6px}</style></head><body><main>'
            # the picture first, in the card Guide › RoadMap Draw gives "Workbench design", then the
            # document's parts (JL 261003, as Design's Method page)
            '<details class=draw-fold><summary><strong>Method design</strong></summary>'
            f'<div class=draw-body>{canvas}</div></details>{body}</main>{remember}{height}{no_pinch}</body></html>')


class WorkbenchGuideMixin:
    def guide_path_allowed(self, path):
        from host_registry import static_path_allowed
        return static_path_allowed(Path(self.root), path)

    def guide_send(self, body, code=200, content_type="text/html; charset=utf-8", head_only=False):
        raw = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(raw)

    def guide_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        get = lambda key, default="": (query.get(key) or [default])[0]
        family, mode = get("family"), get("mode")
        only = getattr(self, "only", None)
        if family not in FAMILIES or (only and family not in only):
            return self.guide_send("Guide family is not served by this host.", 404, head_only=head_only)
        try:
            contract_path(family, 0)  # optional plugins must actually be present
            if mode == "method":
                return self.guide_send(method_page_html(family, family_profile(family, {}), editable=not only),
                                       head_only=head_only)
            if mode in ("drawing", "drawing-scene"):
                key = get("drawing")
                rel = family_drawing(family_profile(family, {}), key)
                if not rel or not (REPOSITORY / rel).is_file():
                    return self.guide_send("This family's Guide declares no such drawing.", 404, head_only=head_only)
                if mode == "drawing-scene":
                    return self.guide_send((REPOSITORY / rel).read_text(encoding="utf-8"),
                                           content_type="application/json; charset=utf-8", head_only=head_only)
                canonical = drawing_url(family, key, rel)
                if query != parse_qs(urlparse(canonical).query):
                    self.send_response(303)
                    self.send_header("Location", canonical)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                # the same viewer and storage isolation as mode=canvas, read only (guide=1)
                original = self.path
                self.path = "/_excalidraw/?" + urlparse(original).query
                try:
                    return self.proxy_excalidraw(head_only=head_only)
                finally:
                    self.path = original
            if mode == "source":
                path = contract_path(family, int(get("source", "0")), {"file": get("file")})
                body = f'<!doctype html><meta charset="utf-8"><title>{esc(path.name)}</title><h1>{esc(path.relative_to(REPOSITORY))}</h1><pre style="white-space:pre-wrap;overflow-wrap:anywhere">{esc(path.read_text(encoding="utf-8"))}</pre>'
                return self.guide_send(body, head_only=head_only)
            context = {"path": get("path"), "file": get("file")}
            if family == "labeling" and not context["path"] and only == {"labeling"}:
                source, error = self._labeling_page_target(context["file"])
                result = (source, error)
            elif not instance(context):
                result = (None, None)  # family-only Guide (the Shared Workbench): no instance to resolve
            else:
                result = self.target(context)
            if result[0] is None and result[1] is not None:
                return self.guide_send(esc(result[1]), 404, head_only=head_only)
            source = Path(result[0]) if result[0] else None
            if mode == "folder" and source is None:
                return self.guide_send("Folder paths resolve only inside a Board. Open Guide from that Board.",
                                       404, head_only=head_only)
            if mode == "folder":
                matches = folder_matches(Path(self.root), source, family, int(get("row", "0")), context,
                                         self.guide_path_allowed)
                entries = []
                for match in matches:
                    entries.append(f'<h2>{esc(match.relative_to(self.root))}</h2>')
                    children = sorted(match.iterdir())[:100] if match.is_dir() else [match]
                    for child in children:
                        if not self.guide_path_allowed(child):
                            continue
                        relative = child.relative_to(self.root).as_posix()
                        entries.append(f'<p><code>{esc(child.name)}</code></p>' if child.is_dir() else
                                       f'<p><a href="/{esc(quote(relative, safe="/"))}">{esc(child.name)}</a></p>')
                message = "".join(entries) or '<p>No accessible source at this declared path in the current instance. Open the owning Workbench for private sources or external stores.</p>'
                return self.guide_send('<!doctype html><meta charset="utf-8"><title>Guide · source paths</title>' + message, head_only=head_only)
            view = OLD_VIEWS.get(get("view"), get("view") or VIEWS[0][0])
            if view not in dict((key, label) for key, label, _ in VIEWS):
                return self.guide_send("Unknown Guide View.", 404, head_only=head_only)
            if mode in ("scene", "svg", "canvas") and view not in DRAW_NAMES:
                return self.guide_send("This View has no standalone drawing.", 404, head_only=head_only)
            if mode == "scene":
                return self.guide_send(json.dumps(guide_scene(family, view, context).data()),
                                       content_type="application/json; charset=utf-8", head_only=head_only)
            if mode == "svg":
                scene = guide_scene(family, view, context)
                return self.guide_send(scene.vector(DRAW_NAMES[view]), content_type="image/svg+xml; charset=utf-8", head_only=head_only)
            if mode == "canvas":
                canonical = url(mode="canvas", guide="1",
                                board=url(mode="scene", family=family, view=view, **context).lstrip("/"),
                                family=family, view=view, **context)
                if query != parse_qs(urlparse(canonical).query):
                    # Guide uses only its own generated scene and viewing mode.
                    self.send_response(303)
                    self.send_header("Location", canonical)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                # The proxy's boot script reads board= from the browser URL.
                # Keep its existing per-iframe storage isolation and viewing mode.
                original = self.path
                self.path = "/_excalidraw/?" + urlparse(original).query
                try:
                    return self.proxy_excalidraw(head_only=head_only)
                finally:
                    self.path = original
            # Guide alone has no Spaces: a family that names its board page (`board_route`) opens there,
            # Guide open on this View, so its Spaces are beside it (JL 261003: "where are other spaces?")
            profile = family_profile(family, context)
            route = profile.get("board_route")
            if get("embed") != "1" and route and context.get("path"):
                board = Path(context["path"]).parent.as_posix()
                self.send_response(303)
                self.send_header("Location", route.format(board=quote(board, safe="/")) + "&guide=" + quote(view))
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            prelude = ""
            if get("embed") != "1" and route and profile.get("boards"):
                found = sorted(b.parent.relative_to(Path(self.root)).as_posix() for b in Path(self.root).glob(profile["boards"])
                               if self.guide_path_allowed(b))
                links = " · ".join(f'<a href="{esc(route.format(board=quote(b, safe="/")) + "&guide=" + quote(view))}">{esc(Path(b).name)}</a>'
                                   for b in found)
                prelude = (f'<header><h1>{esc(profile["label"])} Workbench</h1><p>Guide · open it on a board to see its Spaces: '
                           + (links or "no board found") + '</p></header>')
            return self.guide_send(guide_html(family, view, context, get("embed") == "1", prelude=prelude), head_only=head_only)
        except (ValueError, OSError, RuntimeError) as error:
            return self.guide_send(esc(error), 404, head_only=head_only)
