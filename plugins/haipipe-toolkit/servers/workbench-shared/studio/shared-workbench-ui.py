"""Draw the Shared Workbench UI for Guide's RoadMap Draw (JL 261002: "for the map draw, you
missed the Workbench UI draw"). Three screens, left to right:

1. The Shared Workbench's own site (`/w/shared`): header, band, the Guide Space and its four Views.
2. Guide on every workbench: the Guide button mounted first on a family's Space row.
3. Studio inside a workbench: the drawing above, the chat below, and the files that serve them.

Studio style (skills/page/haipipe-workbench-studio/ref/draw.md): transparent boxes, colored
strokes, every label bound inside its box, every arrow bound at both ends, Comic Shanns.

    python3 plugins/haipipe-toolkit/servers/workbench-shared/studio/shared-workbench-ui.py
"""

import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "shared-workbench-ui.excalidraw"
INK, MUTED = "#1e1e1e", "#868e96"
BLUE, GREEN, ORANGE, PURPLE = "#1971c2", "#2f9e44", "#e8590c", "#9c36b5"
RNG = random.Random(261002)
E = []


def element(key, kind, x, y, w, h, stroke=INK, dashed=False, **extra):
    item = {"id": key, "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
            "strokeColor": stroke, "backgroundColor": "transparent", "fillStyle": "solid",
            "strokeWidth": 2, "strokeStyle": "dashed" if dashed else "solid", "roughness": 1,
            "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": {"type": 3} if kind == "rectangle" else None,
            "seed": RNG.randint(1, 2**31 - 1), "version": 1, "versionNonce": RNG.randint(1, 2**31 - 1),
            "isDeleted": False, "boundElements": [], "updated": 0, "link": None, "locked": False}
    item.update(extra)
    E.append(item)
    return item


def text(key, x, y, value, size=16, color=INK, container=None, align="left"):
    lines = value.split("\n")
    w = max(len(line) for line in lines) * size * 0.6
    h = len(lines) * size * 1.25
    return element(key, "text", x, y, w, h, color, text=value, originalText=value, fontSize=size,
                   fontFamily=8, textAlign=align, verticalAlign="middle" if container else "top",
                   containerId=container, autoResize=True, lineHeight=1.25)


def box(key, x, y, w, h, label, stroke=INK, size=16, dashed=False):
    """A rectangle with its label bound inside."""
    rect = element(key, "rectangle", x, y, w, h, stroke, dashed)
    lines = label.split("\n")
    label_h = len(lines) * size * 1.25
    inner = text(key + "-label", x + 10, y + (h - label_h) / 2, label, size, INK, rect["id"], "center")
    inner["width"] = w - 20
    rect["boundElements"].append({"type": "text", "id": inner["id"]})
    return rect


def arrow(key, start, end, label=""):
    """An arrow bound at both ends, from the bottom of `start` to the top of `end`."""
    x0, y0 = start["x"] + start["width"] / 2, start["y"] + start["height"]
    x1, y1 = end["x"] + end["width"] / 2, end["y"]
    item = element(key, "arrow", x0, y0 + 4, abs(x1 - x0), abs(y1 - y0) - 8, INK,
                   points=[[0, 0], [x1 - x0, y1 - y0 - 8]], lastCommittedPoint=None,
                   startBinding={"elementId": start["id"], "focus": 0, "gap": 4},
                   endBinding={"elementId": end["id"], "focus": 0, "gap": 4},
                   startArrowhead=None, endArrowhead="arrow", elbowed=False)
    start["boundElements"].append({"type": "arrow", "id": key})
    end["boundElements"].append({"type": "arrow", "id": key})
    if label:
        text(key + "-note", x0 + (x1 - x0) / 2 + 8, y0 + (y1 - y0) / 2 - 10, label, 13, MUTED)
    return item


def site(x, y):
    """Screen 1: the Shared Workbench's own site."""
    text("site-title", x, y, "1 · The Shared Workbench site · /w/shared", 22, BLUE)
    element("site-screen", "rectangle", x, y + 40, 560, 560, MUTED)
    text("site-h1", x + 20, y + 56, "🧩 Shared Workbench", 20)
    text("site-links", x + 20, y + 86, "all boards", 13, BLUE)
    box("site-band", x + 20, y + 112, 520, 40, "workbench-shared · reused by 6 families · Studio · Guide", BLUE, 13)
    guide = box("site-guide", x + 20, y + 168, 100, 36, "Guide", BLUE)
    views = [box(f"site-view-{i}", x + 20 + i * 130, y + 228, 122, 36, name, GREEN, 14)
             for i, name in enumerate(("Description", "Method", "RoadMap Draw", "Related Paper"))]
    arrow("site-guide-views", guide, views[0], "its Views")
    reads = ["What the\nWorkbench\ndoes", "Its steps,\nas text", "UI drawing\n+ table\ndrawing", "Papers it\nbuilds on"]
    for i, (view, read) in enumerate(zip(views, reads)):
        panel = box(f"site-panel-{i}", view["x"], y + 300, 122, 120, read, MUTED, 13, dashed=True)
        arrow(f"site-shows-{i}", view, panel)
    box("site-table", x + 20, y + 446, 520, 130,
        "RoadMap Draw · Workbench Table\nSpace · View · Run type · Agent · Skill · Person signs\n"
        "from haipipe-workbench-studio/ref/workbench-table.md", PURPLE, 14)


def mounted(x, y):
    """Screen 2: Guide mounted on another family's workbench."""
    text("mount-title", x, y, "2 · Guide on every workbench", 22, BLUE)
    element("mount-screen", "rectangle", x, y + 40, 460, 300, MUTED)
    text("mount-h1", x + 20, y + 56, "🔎 Insight Board (any family)", 18)
    guide = box("mount-guide", x + 20, y + 96, 80, 34, "Guide", BLUE, 15)
    for i, name in enumerate(("Scope", "Insight", "Check", "Delivery")):
        box(f"mount-space-{i}", x + 110 + i * 84, y + 96, 78, 34, name, INK, 13)
    views = box("mount-views", x + 20, y + 170, 420, 40, "Description · Method · RoadMap Draw · Related Paper", GREEN, 14)
    arrow("mount-guide-views", guide, views, "same four Views")
    box("mount-note", x + 20, y + 236, 420, 84,
        "mount_guide() adds the button first on the Space row;\nthe content is that family's entry in guide_families.py", MUTED, 13, dashed=True)


def studio(x, y):
    """Screen 3: Studio inside a workbench."""
    text("studio-title", x, y, "3 · Studio inside a workbench", 22, BLUE)
    element("studio-screen", "rectangle", x, y + 40, 460, 300, MUTED)
    text("studio-h1", x + 20, y + 56, "🎨 Studio tab of a Page or Board", 18)
    draw = box("studio-draw", x + 20, y + 92, 420, 100, "Draw · the live Excalidraw canvas\n✨ Draw it · Redraw on ask", ORANGE, 15)
    chat = box("studio-chat", x + 20, y + 216, 420, 100, "Chat · GUI (SDK chat) | TUI (terminal)\nKeep the session", PURPLE, 15)
    arrow("studio-chat-draw", draw, chat, "chat may redraw")
    box("studio-files", x, y + 360, 460, 110,
        "xcal.py + excalidraw_proxy.py + xcal-boot.js · open, create, save\n"
        "chat.py + turnring.py · term.py · the chat and terminal\nautodraw.py · ✨ Draw it", MUTED, 13, dashed=True)


def main():
    text("title", 0, 0, "Shared Workbench · UI", 28)
    text("subtitle", 0, 42, "What every workbench reuses: Guide explains, Studio draws and chats.", 16, MUTED)
    site(0, 100)
    mounted(620, 100)
    studio(620, 480)
    scene = {"type": "excalidraw", "version": 2, "source": "haipipe-workbench-shared-ui",
             "elements": E, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}
    OUT.write_text(json.dumps(scene, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.name}: {len(E)} elements")


if __name__ == "__main__":
    main()
