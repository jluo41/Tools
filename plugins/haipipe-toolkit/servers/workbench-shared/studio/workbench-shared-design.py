"""Generate the shared Workbench UI proposal as an Excalidraw scene.

Matches the geometry and colors of the Paper / Insight design studios.
Only --previews needs Pillow; the scene uses the standard library. Previews
are local and git-ignored.
The examples are illustrative. This script does not register a server route.
"""

import argparse
import json
import random
from pathlib import Path


INK, MUTED, RULE, PANEL = "#1e1e1e", "#495057", "#ced4da", "#f8f9fa"
BLUE, BLUE_BG = "#1864ab", "#e7f5ff"
GREEN, GREEN_BG = "#2b8a3e", "#ebfbee"
PURPLE, PURPLE_BG = "#6741d9", "#f3f0ff"
ORANGE = "#d9480f"
E, FRAMES = [], []
RNG = random.Random(261002)
FW, FH, GAP = 1480, 1000, 64
CURRENT_FRAME = None


def base(key, kind, x, y, w, h, stroke=INK, bg="transparent", dashed=False):
    return {
        "id": key, "type": kind, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": "solid", "strokeWidth": 2,
        "strokeStyle": "dashed" if dashed else "solid", "roughness": 0,
        "opacity": 100, "groupIds": [], "frameId": CURRENT_FRAME,
        "roundness": {"type": 3} if kind == "rectangle" else None,
        "seed": RNG.randint(1, 2**31 - 1), "version": 1,
        "versionNonce": RNG.randint(1, 2**31 - 1), "isDeleted": False,
        "boundElements": [], "updated": 0, "link": None, "locked": False,
    }


def rect(key, x, y, w, h, stroke=RULE, bg="transparent", dashed=False):
    item = base(key, "rectangle", x, y, w, h, stroke, bg, dashed)
    E.append(item)
    return item


def text(key, x, y, value, size=16, color=INK, mono=False, width=None):
    lines = value.split("\n")
    item = base(key, "text", x, y,
                width or max(len(line) for line in lines) * size * 0.62,
                len(lines) * size * 1.25, color)
    item.update(text=value, originalText=value, fontSize=size,
                fontFamily=3 if mono else 8, textAlign="left",
                verticalAlign="top", containerId=None, autoResize=True,
                lineHeight=1.25)
    E.append(item)
    return item


def button(key, x, y, w, h, label, selected=False, size=16, dashed=False):
    color, bg = (BLUE, BLUE_BG) if selected else (MUTED, "#ffffff")
    box = rect(key, x, y, w, h, color if selected else RULE, bg, dashed)
    label_item = text(key + "-label", x + 8, y + (h - size * 1.25) / 2,
                      label, size, color, width=w - 16)
    label_item.update(containerId=key, textAlign="center", verticalAlign="middle")
    box["boundElements"] = [{"id": label_item["id"], "type": "text"}]


def line(key, x, y, w, color=RULE):
    item = base(key, "line", x, y, w, 0, color)
    item.update(points=[[0, 0], [w, 0]], lastCommittedPoint=None,
                startBinding=None, endBinding=None,
                startArrowhead=None, endArrowhead=None)
    E.append(item)


def arrow(key, x, y, points, color=BLUE):
    item = base(key, "arrow", x, y,
                max(p[0] for p in points) - min(p[0] for p in points),
                max(p[1] for p in points) - min(p[1] for p in points), color)
    item.update(points=points, lastCommittedPoint=None, startBinding=None,
                endBinding=None, startArrowhead=None, endArrowhead="arrow",
                elbowed=False)
    E.append(item)


def tabs(key, x, y, labels, selected, size=16, height=42, minimum=90):
    for index, label in enumerate(labels):
        width = max(minimum, len(label) * size * 0.62 + 28)
        button(f"{key}-{index}", x, y, width, height, label,
               selected=label == selected, size=size)
        x += width + 8


def card(key, x, y, w, h, title, body, color=INK, bg="#ffffff", size=16):
    rect(key, x, y, w, h, RULE, bg)
    text(key + "-title", x + 16, y + 12, title, 19, color)
    text(key + "-body", x + 16, y + 42, body, size, MUTED)


def frame(key, name, x, y, w=FW, h=FH):
    global CURRENT_FRAME
    CURRENT_FRAME = None
    item = base(key, "frame", x, y, w, h)
    item.update(name=name)
    E.append(item)
    FRAMES.append(item)
    CURRENT_FRAME = key
    return x, y


def heading(key, x, y, title, subtitle):
    text(key + "-heading", x + 24, y + 18, title, 28)
    text(key + "-subtitle", x + 24, y + 60, subtitle, 17, MUTED)


INTRO_VIEWS = ["Skill set", "Workbench", "Folder map"]
BLOCK_VIEWS = ["Goal", "Design", "Studio", "Progress", "Checklist"]
GUIDE_VIEWS = INTRO_VIEWS + BLOCK_VIEWS
FAMILY_SPACES = {"Labeling": ["Data", "Labeling", "Quality", "Delivery"],
                 "Task": ["Runs", "Scope"]}


def shell(key, x, y, family, selected="Guide"):
    rect(key + "-screen", x + 24, y + 108, FW - 48, 630, INK, "#ffffff")
    text(key + "-family", x + 44, y + 128, family + " Workbench", 23)
    text(key + "-block", x + 44, y + 159, "Block b01_example", 15, MUTED)
    button(key + "-switch", x + 1088, y + 130, 208, 38, "Switch Block  v", size=16)
    button(key + "-folder", x + 1308, y + 130, 128, 38, "Folder >", size=16)
    text(key + "-space-label", x + 44, y + 212, "Space", 16, MUTED)
    tabs(key + "-spaces", x + 104, y + 202,
         ["Guide"] + FAMILY_SPACES[family],
         selected, size=15, height=42, minimum=82)
    line(key + "-rule", x + 44, y + 260, FW - 88)
    return x + 44, y + 330, x + 956


def guide_views(key, x, y, selected):
    text(key + "-view-label", x, y + 9, "View", 16, MUTED)
    tabs(key + "-views", x + 60, y, GUIDE_VIEWS, selected,
         size=15, height=42, minimum=82)


def annotation(key, x, y, w, title, body, color, bg):
    rect(key, x, y, w, 172, color, bg)
    text(key + "-title", x + 16, y + 14, title, 20, color)
    text(key + "-body", x + 16, y + 52, body, 16, MUTED)


def composition(x, y):
    key = "composition"
    heading(key, x, y, "Shared Workbench UI · composition",
            "Choose a Space first, then its View. Guide is the one shared Space; this family's other Spaces stay its own.")
    lx, cy, rx = shell(key, x, y, "Labeling")
    guide_views(key, lx, y + 276, "Workbench")
    rect(key + "-content", lx, cy, 890, 350, RULE, PANEL)
    text(key + "-content-title", lx + 18, cy + 18, "Guide Space · how this Workbench is organized", 22)
    text(key + "-content-caption", lx + 18, cy + 54,
         "Guide contains both the family explanation and the shared Block Views.", 16, MUTED)
    card(key + "-intro", lx + 18, cy + 100, 418, 168,
         "1 · About this Workbench",
         "Skill set · Workbench · Folder map\n\nShared explanation for this family.\nKept when the Block changes.", BLUE, BLUE_BG, size=16)
    card(key + "-block-content", lx + 454, cy + 100, 418, 168,
         "2 · This Block",
         "Goal · Design · Studio\nProgress · Checklist\n\nShared View structure; instance content.", GREEN, GREEN_BG, size=16)
    text(key + "-native", lx + 18, cy + 292,
         "Choose Guide first. All eight shared Views are inside it.", 16, MUTED)
    rect(key + "-family-spaces", rx, cy, 480, 350, RULE, PANEL)
    text(key + "-family-title", rx + 18, cy + 18, "3 · Labeling's own Spaces", 22, PURPLE)
    card(key + "-family-map", rx + 18, cy + 62, 444, 190,
         "Each Space opens its own Views",
         "Data        Preparation · Contract · Embedding\nLabeling    Definition · Rounds · Guideline\nQuality     Test · Evaluation · Audit\nDelivery    Handoff · Scan · Final", PURPLE, size=15)
    text(key + "-family-note", rx + 18, cy + 278,
         "Paper supplies its own Space / View roster.\nGuide joins that roster as one shared Space.", 16, MUTED)
    text(key + "-scope", lx, y + 704,
         "Labeling Workbench  /  b01_example  /  Guide  /  Workbench", 15, MUTED)
    notes = [
        ("1 · Inside Guide: explanation", "Skill set · Workbench · Folder map\nDocuments describe this family.\nSwitch Block: keep the explanation.\nSwitch family: load its explanation.", BLUE, BLUE_BG),
        ("2 · Inside Guide: Block Views", "Goal · Design · Studio\nProgress · Checklist\nSame Views across Block instances.\nContent comes from the current owner.", GREEN, GREEN_BG),
        ("3 · Family-owned Spaces", "Here: Data · Labeling · Quality\nDelivery, with their own Views.\nPaper supplies its own Space roster.\nEach family's structure stays its own.", PURPLE, PURPLE_BG),
    ]
    for i, (title, body, color, bg) in enumerate(notes):
        annotation(f"{key}-note-{i}", x + 24 + i * 484, y + 770,
                   464, title, body, color, bg)


def guide(x, y):
    key = "guide"
    heading(key, x, y, "1 · Guide Space",
            "The family explanation is shared across instances; Folder map can show the active instance path.")
    lx, cy, rx = shell(key, x, y, "Task")
    guide_views(key, lx, y + 276, "Skill set")
    rect(key + "-content", lx, cy, 890, 350, RULE, PANEL)
    text(key + "-family-title", lx + 18, cy + 16, "HAI Pipe Task · skill set", 22)
    rows = [
        ("Workflow · haipipe-workflow", "Coordinates the workflow, Spec and owner boundaries."),
        ("Work · haipipe-task", "Owns Block / Job / Task / Run identity and lifecycle."),
        ("UI · Workbench skills", "haipipe-workbench-task: Block     haipipe-workbench-page: Task Page"),
    ]
    for i, (title, body) in enumerate(rows):
        card(f"{key}-skill-{i}", lx + 18, cy + 60 + i * 88,
             854, 76, title, body, BLUE, size=15)
    rect(key + "-map", rx, cy, 480, 350, RULE, PANEL)
    text(key + "-map-title", rx + 18, cy + 16, "Views inside Guide Space", 20)
    map_rows = [
        ("Skill set", "Family skills and their roles"),
        ("Workbench", "UI structure and design rationale"),
        ("Folder map", "Folders and owner mapping"),
        ("Goal", "Overview · Rules"),
        ("Design", "Roadmap · Decisions"),
        ("Studio", "Draw above Chat"),
        ("Progress", "Jobs · Tasks · Runs"),
        ("Checklist", "Checks · Readings"),
    ]
    for i, (view, content) in enumerate(map_rows):
        sy = cy + 63 + i * 33
        text(f"{key}-map-view-{i}", rx + 18, sy, view, 16, BLUE if i < 3 else GREEN)
        text(f"{key}-map-content-{i}", rx + 138, sy, content, 14, MUTED)
    text(key + "-footer", lx, y + 704,
         "Family · Task     Active Block · b01_example     Guide content · family skill / reference documents", 15, MUTED)
    rect(key + "-folder-map-panel", x + 24, y + 770, 890, 172, BLUE, BLUE_BG)
    text(key + "-folder-title", x + 40, y + 783, "Folder map · active path example", 20, BLUE)
    text(key + "-tree", x + 40, y + 820,
         "tasks/b01_example/\n  board.md\n  j01_inputs/t01_inventory/\n    t01_inventory.md   scripts/config/r01_example.yaml\n    runs/r01_example.sh   results/r01_example/   studio/", 15, mono=True)
    rect(key + "-behavior", x + 938, y + 770, 518, 172, BLUE, "#ffffff")
    text(key + "-behavior-title", x + 954, y + 783, "When the instance changes", 20, BLUE)
    text(key + "-behavior-body", x + 954, y + 821,
         "Block A -> Block B in Task Workbench:\nkeep this explanation; update the active path.\n\nTask -> Labeling Workbench:\nkeep the Guide Views; load Labeling's documents.", 16, MUTED)


def progress(x, y):
    key = "progress"
    heading(key, x, y, "2 · Guide Space / Progress View",
            "Guide > Progress shows this Block's native Jobs, Tasks and Runs using the common View structure.")
    lx, cy, rx = shell(key, x, y, "Task")
    guide_views(key, lx, y + 276, "Progress")
    rect(key + "-content", lx, cy, 890, 350, RULE, PANEL)
    text(key + "-title", lx + 18, cy + 16, "Progress · j01_inputs", 22)
    tabs(key + "-scope-filter", lx + 18, cy + 55,
         ["Jobs", "Tasks", "Runs"], "Tasks", size=14, height=30, minimum=78)
    text(key + "-summary", lx + 340, cy + 62,
         "4 Tasks · 2 executions complete · 1 current reading", 14, MUTED)
    for i, (label, dx) in enumerate([
        ("Task", 18), ("Execution", 350), ("Report / Page", 526), ("Reading", 712),
    ]):
        text(f"{key}-column-{i}", lx + dx, cy + 100, label, 16, MUTED)
    line(key + "-table-head", lx + 18, cy + 130, 854)
    rows = [
        ("t01 Input inventory", "Complete", "Current", "Pending"),
        ("t02 Contract draft", "Running", "Previous", "Reopened"),
        ("t03 Review sample", "Waiting", "Missing", "Not started"),
        ("t04 Export review", "Complete", "Current", "Passed"),
    ]
    for i, values in enumerate(rows):
        sy = cy + 143 + i * 43
        if i == 1:
            rect(key + "-selected-task", lx + 10, sy - 5, 870, 37, BLUE, BLUE_BG)
        for j, (value, dx) in enumerate(zip(values, [18, 350, 526, 712])):
            color = BLUE if i == 1 else (GREEN if value == "Passed" else INK)
            text(f"{key}-row-{i}-{j}", lx + dx, sy, value, 16, color)
    text(key + "-legend", lx + 18, cy + 316,
         "Execution, Report / Page currency and reading are separate facts.", 15, MUTED)
    rect(key + "-runs", rx, cy, 480, 350, RULE, PANEL)
    text(key + "-runs-title", rx + 18, cy + 16, "Runs · t02 Contract draft", 22)
    button(key + "-selected-run", rx + 18, cy + 60, 444, 38,
           "r02_example", selected=True)
    text(key + "-receipt", rx + 18, cy + 119,
         "Recorded execution state · running", 17, BLUE)
    text(key + "-receipt-detail", rx + 18, cy + 154,
         "Latest native receipt, when available\nA receipt alone does not show live liveness.", 15, MUTED)
    line(key + "-run-rule", rx + 18, cy + 212, 444)
    text(key + "-run-sections", rx + 18, cy + 235,
         "> Prompt                        Copy\n> Process                       Open\n> Results                       Open", 17)
    text(key + "-footer", lx, y + 704,
         "Task Workbench  /  b01_example  /  Guide  /  Progress     Selected Task · t02 Contract draft", 15, MUTED)
    annotation(key + "-structure", x + 24, y + 770, 706,
               "Shared structure · instance content",
               "Block A and Block B keep Guide and its Progress View.\nJobs, Tasks, prompts, receipts and Results come from each Block.\nSelection opens the native owner; the shared UI projects its records.",
               GREEN, GREEN_BG)
    annotation(key + "-checks", x + 750, y + 770, 706,
               "Guide / Checklist keeps the gates visible",
               "Checks / Readings show the owner's current evidence and gates.\nCompleted execution can still have a pending or reopened reading.\nTask closure follows its owner contract and current Results.",
               GREEN, "#ffffff")


def studio(x, y):
    key = "studio"
    heading(key, x, y, "2 · Guide Space / Studio View",
            "Follow the existing Studio: drawing above chat, both visible in one room.")
    lx, cy, rx = shell(key, x, y, "Task")
    guide_views(key, lx, y + 276, "Studio")
    button(key + "-full-screen", rx + 216, y + 276, 264, 42, "Open full screen >", size=16)
    rect(key + "-draw", lx, cy, 890, 204, RULE, "#ffffff")
    text(key + "-draw-title", lx + 16, cy + 12, "Draw · roadmap.excalidraw", 18)
    button(key + "-draw-it", lx + 750, cy + 10, 122, 32, "Draw it", size=15)
    for i, label in enumerate(["Goal", "Plan", "Work", "Check"]):
        nx = lx + 36 + i * 211
        button(f"{key}-node-{i}", nx, cy + 72, 174, 50, label,
               selected=i == 1, size=18)
        if i < 3:
            arrow(f"{key}-flow-{i}", nx + 176, cy + 97, [[0, 0], [31, 0]])
    arrow(key + "-feedback", lx + 334, cy + 124,
          [[422, 0], [422, 42], [0, 42], [0, 0]], MUTED)
    text(key + "-feedback-label", lx + 410, cy + 168, "revise from the check", 14, MUTED)
    rect(key + "-chat", lx, cy + 216, 890, 134, RULE, PANEL)
    text(key + "-chat-title", lx + 16, cy + 228, "Chat · current discussion", 18)
    text(key + "-person", lx + 16, cy + 265,
         "Person   Link the draft to its checks.", 16)
    text(key + "-agent", lx + 16, cy + 293,
         "Agent     Show the reading gate after Work.", 16, MUTED)
    rect(key + "-context", rx, cy, 480, 350, RULE, PANEL)
    text(key + "-context-title", rx + 18, cy + 16, "Studio · t01_inventory", 22)
    card(key + "-drawing-source", rx + 18, cy + 60, 444, 104,
         "Kept drawing", "t01_inventory/studio/draw/\nroadmap.excalidraw", BLUE, size=16)
    card(key + "-chat-source", rx + 18, cy + 180, 444, 104,
         "Kept conversation", "t01_inventory/studio/chat/\nThe same native owner as the drawing", size=16)
    text(key + "-context-footer", rx + 18, cy + 306,
         "Owner selection changes both panes together.", 15, MUTED)
    text(key + "-footer", lx, y + 704,
         "Task Workbench  /  b01_example  /  Guide  /  Studio     Selected owner · j01_inputs / t01_inventory", 15, MUTED)
    annotation(key + "-layout", x + 24, y + 770, 706,
               "Shared Studio layout",
               "Guide's Studio View contains Draw above Chat, both visible.\nThe person's discussion can refer to what is on the canvas.\nKeep the established Studio composition and lane ownership.",
               GREEN, GREEN_BG)
    annotation(key + "-binding", x + 750, y + 770, 706,
               "Block scope selects a native owner",
               "This example opens a Task's existing studio/draw and studio/chat.\nSwitching owners loads that owner's drawing and conversation.\nA future Block-owned Studio needs an explicit storage contract.",
               GREEN, "#ffffff")


def block_map(x, y):
    key = "block-map"
    width = FW * 2 + GAP
    heading(key, x, y, "Guide Space / Block Views · shared structure, instance content",
            "All five working Views live inside Guide, alongside its Skill set, Workbench and Folder map Views.")
    rows = [
        ("Goal", "Overview · Rules", "What are we trying to do?", "Current goal and scope\nAcceptance rules\nInputs and constraints", "Read the goal's native owner."),
        ("Design", "Roadmap · Decisions", "How will the work fit together?", "The working design\nDependencies and alternatives\nDecisions and their reasons", "Read the design's native owner."),
        ("Studio", "Draw above Chat", "Where do we think together?", "Kept drawing\nKept conversation\nSelected owner context", "Open the selected owner's Studio."),
        ("Progress", "Jobs · Tasks · Runs", "What has happened so far?", "Native membership and order\nExecution receipts and Results\nDeclared Reports / Pages", "Read the Block's native hierarchy."),
        ("Checklist", "Checks · Readings", "What still needs to be checked?", "Required checks\nCurrent reading gates\nEvidence and open questions", "Read the checks' native owners."),
    ]
    for i, (view, sections, question, content, binding) in enumerate(rows):
        cx = x + 24 + i * 600
        rect(f"{key}-space-{i}", cx, y + 112, 576, 308, GREEN, GREEN_BG)
        text(f"{key}-title-{i}", cx + 18, y + 128, view + " View", 25, GREEN)
        text(f"{key}-sections-{i}", cx + 18, y + 169, sections, 17)
        line(f"{key}-rule-{i}", cx + 18, y + 206, 540)
        text(f"{key}-question-{i}", cx + 18, y + 223, question, 18, GREEN)
        text(f"{key}-content-{i}", cx + 18, y + 264, content, 17, MUTED)
        text(f"{key}-binding-{i}", cx + 18, y + 375, binding, 16, GREEN)
    text(key + "-instance", x + 24, y + 459,
         "Switch instance: keep Guide and its Views; resolve new content.    Switch family: load its explanation and its own other Spaces.", 19)
    text(key + "-proposal", x + 24, y + 501,
         "One shared Space: Guide. View names are a proposal; content and storage follow the native owner contracts.", 17, MUTED)


def write_previews(directory, font_path, mono_path, names=None):
    from PIL import Image, ImageDraw, ImageFont

    scale = 1.5
    font_cache = {}

    def font(size, mono):
        key = size, mono
        if key not in font_cache:
            path = mono_path if mono else font_path
            font_cache[key] = ImageFont.truetype(path, round(size * scale)) if path else ImageFont.load_default(size=round(size * scale))
        return font_cache[key]

    names = names or ["01-composition", "02-guide", "03-progress", "04-studio", "05-guide-views"]
    for bounds, name in zip(FRAMES, names):
        image = Image.new("RGB", (round(bounds["width"] * scale), round(bounds["height"] * scale)), "white")
        draw = ImageDraw.Draw(image)

        def point(px, py):
            return (round((px - bounds["x"]) * scale), round((py - bounds["y"]) * scale))

        for item in E:
            if item["frameId"] != bounds["id"]:
                continue
            x, y, w, h = (item[k] for k in ("x", "y", "width", "height"))
            color = item["strokeColor"]
            if item["type"] == "rectangle":
                fill = None if item["backgroundColor"] == "transparent" else item["backgroundColor"]
                draw.rounded_rectangle([point(x, y), point(x + w, y + h)],
                                       radius=round(10 * scale), fill=fill, outline=color, width=3)
            elif item["type"] == "text":
                size = item["fontSize"]
                face = font(size, item["fontFamily"] == 3)
                for i, value in enumerate(item["text"].split("\n")):
                    px, py = point(x, y + i * size * 1.25)
                    if item["textAlign"] == "center":
                        px += (w * scale - draw.textlength(value, font=face)) / 2
                    draw.text((px, py), value, fill=color, font=face, anchor="lt")
            elif item["type"] in ("line", "arrow"):
                points = [point(x + px, y + py) for px, py in item["points"]]
                draw.line(points, fill=color, width=3)
                if item.get("endArrowhead"):
                    import math
                    a, b = points[-2:]
                    angle = math.atan2(b[1] - a[1], b[0] - a[0])
                    head = [b, (b[0] - 10 * scale * math.cos(angle - .45), b[1] - 10 * scale * math.sin(angle - .45)),
                            (b[0] - 10 * scale * math.cos(angle + .45), b[1] - 10 * scale * math.sin(angle + .45))]
                    draw.line([head[1], head[0], head[2]], fill=color, width=3)
        image.save(directory / (name + ".png"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previews", action="store_true")
    parser.add_argument("--font")
    parser.add_argument("--mono-font")
    args = parser.parse_args()
    output = Path(__file__).resolve().parent
    text("title", 48, 20, "Workbench Shared · UI design studio", 34)
    text("subtitle", 48, 76,
         "One shared Guide Space: 1 Family explanation + 2 Instance Views.    Other Spaces: 3 Family-owned UI.", 21, MUTED)
    text("draft", 48, 116, "Design proposal · illustrative content and states", 16, MUTED)
    x0, x1 = 48, 48 + FW + GAP
    y0, y1 = 176, 176 + FH + GAP
    composition(*frame("frame-composition", "01 · Composition", x0, y0))
    guide(*frame("frame-guide", "02 · Guide Space", x1, y0))
    progress(*frame("frame-progress", "03 · Guide / Progress", x0, y1))
    studio(*frame("frame-studio", "04 · Guide / Studio", x1, y1))
    block_map(*frame("frame-block-map", "05 · Guide's Block Views", x0, y1 + FH + GAP, FW * 2 + GAP, 560))
    scene = {"type": "excalidraw", "version": 2, "source": "haipipe-workbench-shared-design",
             "elements": E, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}
    scene_path = output / "workbench-shared-design.excalidraw"
    scene_path.write_text(json.dumps(scene, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.previews:
        write_previews(output, args.font, args.mono_font)
    print(f"Wrote {scene_path.name}: {len(E)} elements, {len(FRAMES)} frames")


if __name__ == "__main__":
    main()
