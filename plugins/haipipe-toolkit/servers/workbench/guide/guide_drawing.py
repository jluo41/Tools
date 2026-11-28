"""Guide's RoadMap drawing: deterministic Excalidraw scenes and their SVG projection."""

import hashlib
import re
import textwrap
from pathlib import Path

from live.guide_core import esc, family_profile, instance, url
from live.guide_tables import table_rows


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
                 fontFamily=3 if mono else 6, textAlign="left", verticalAlign="top",
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
        return dict(type="excalidraw", version=2, source="hai-workbench-guide",
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
    inside its box, Nunito (no hand-drawn font, JL 261009). A repeated Space or View cell spans its rows."""
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
                  fontSize=size, fontFamily=6, textAlign="center", verticalAlign="middle", containerId=box["id"],
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
    rows = [("Guide", "plugins/haipipe-toolkit/servers/workbench/guide/guide_families.py",
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
