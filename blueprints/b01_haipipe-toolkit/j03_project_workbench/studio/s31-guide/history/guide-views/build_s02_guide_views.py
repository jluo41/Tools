"""Create explanatory drawings, their Guide Views and a RoadMap Draw View.

Paper supplies the concrete family example, matching Guide v4. These drawings
explain roles and methods; they contain no live instance state. Scene
generation uses the standard library. Optional PNG previews require Pillow and
are local and git-ignored.
"""

import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "shared_guide_v4", HERE.parent / "guide-design" / "build_s04_guide_design.py")
guide = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guide)
ui = guide.ui
rect, text, button, line, arrow = ui.rect, ui.text, ui.button, ui.line, ui.arrow
INK, MUTED, RULE, PANEL = ui.INK, ui.MUTED, ui.RULE, ui.PANEL
BLUE, BLUE_BG, GREEN, GREEN_BG = ui.BLUE, ui.BLUE_BG, ui.GREEN, ui.GREEN_BG
PURPLE, PURPLE_BG = ui.PURPLE, ui.PURPLE_BG
FW, FH, GAP = 1480, 1540, 64
DW, DH = 1340, 330
CATALOG = json.loads((HERE / "drawing-catalog.json").read_text(encoding="utf-8"))
GUIDE_TYPES = [item for item in CATALOG["types"] if item["scope"] == "guide"]
TYPE_BY_VIEW = {item["view"]: item for item in GUIDE_TYPES}


def reset():
    ui.E.clear()
    ui.FRAMES.clear()
    ui.CURRENT_FRAME = None
    ui.RNG.seed(261002)


def node(key, x, y, w, h, title, body, color=BLUE, bg="#ffffff",
         title_size=18, body_size=15):
    start = len(ui.E)
    rect(key, x, y, w, h, color, bg)
    text(key + "-title", x + 14, y + 12, title, title_size, color)
    text(key + "-body", x + 14, y + 43, body, body_size, MUTED)
    for element in ui.E[start:]:
        element["groupIds"] = [key + "-group"]


def skill_set(key, x, y):
    node(key + "-workflow", x, y, 370, 116, "Workflow · rules and routing",
         "haipipe-paper-workflow\nRun Specs, dependencies and G0-G5 gates", BLUE, BLUE_BG)
    node(key + "-story", x + 470, y, 400, 116, "Story · questions and argument",
         "haipipe-paper-story\nQuestions, evidence needs and intended claims", GREEN, GREEN_BG)
    node(key + "-workbench", x + 970, y, 370, 116, "Workbench · presentation",
         "workbench-paper\nSpaces and Views over the owning records", PURPLE, PURPLE_BG)
    arrow(key + "-rules-route", x + 374, y + 58, [[0, 0], [92, 0]])
    text(key + "-rules-route-label", x + 392, y + 26, "routes", 14, MUTED)
    arrow(key + "-story-read", x + 874, y + 58, [[0, 0], [92, 0]])
    text(key + "-story-read-label", x + 892, y + 26, "reads", 14, MUTED)
    arrow(key + "-workflow-owners", x + 185, y + 120, [[0, 0], [0, 54]])
    text(key + "-workflow-owners-label", x + 200, y + 135, "routes work", 14, MUTED)
    arrow(key + "-story-owners", x + 670, y + 120, [[0, 0], [0, 54]])
    text(key + "-story-owners-label", x + 686, y + 135, "references", 14, MUTED)
    arrow(key + "-owners-read", x + 1155, y + 174, [[0, 0], [0, -54]], MUTED)
    text(key + "-owners-read-label", x + 1172, y + 135, "reads", 14, MUTED)
    node(key + "-ideation", x, y + 180, 370, 120, "Idea owners",
         "haipipe-ideation\nhaipipe-paper-ideation\nCandidate work and its admission", BLUE, title_size=18, body_size=15)
    node(key + "-evidence", x + 470, y + 180, 400, 120, "Supporting work owners",
         "haipipe-task / haipipe-discovery\nNative inputs, Runs, Tickets and Results\nReferenced by the Story", GREEN, title_size=18, body_size=15)
    node(key + "-page", x + 970, y + 180, 370, 120, "Page and delivery owners",
         "haipipe-page-workflow + PageType\nhaipipe-paper-assemble\nhaipipe-paper-round", PURPLE, title_size=18, body_size=15)
    text(key + "-caption", x, y + 310,
         "The family explains how these skills cooperate. Native owners retain their own content and execution records.", 15, MUTED)


def methods(key, x, y):
    w, step, top, lower = 270, 350, 22, 211
    top_nodes = [
        ("question", "Question", "What needs an answer?\nWhat would answer it?"),
        ("reason", "Reason about it", "Hypotheses and claim candidates\nExisting evidence and boundaries"),
        ("need", "Missing evidence", "What is still unknown?\nWhat evidence must be obtained?"),
        ("work", "Related Work · when needed", "Task or Discovery owner\nProduce or find supporting evidence"),
    ]
    for i, (slug, title, body) in enumerate(top_nodes):
        node(key + "-" + slug, x + i * step, y + top, w, 106,
             title, body, BLUE, BLUE_BG, title_size=17, body_size=14)
        if i < 3:
            arrow(f"{key}-top-arrow-{i}", x + i * step + w + 4, y + top + 53,
                  [[0, 0], [step - w - 8, 0]])
    lower_nodes = [
        ("open", "Remaining questions", "Record the unresolved issue\nRevise the question or plan"),
        ("answer", "Current answer", "State what is supported\nKeep limits and uncertainty visible"),
        ("review", "Interpret and review", "Read evidence against the question\nReview claims and their limits"),
        ("result", "Native supporting Results", "Read the owner's evidence\nKeep its source and provenance"),
    ]
    for i, (slug, title, body) in enumerate(lower_nodes):
        node(key + "-" + slug, x + i * step, y + lower, w, 106,
             title, body, GREEN, GREEN_BG, title_size=17, body_size=14)
        if i:
            arrow(f"{key}-lower-arrow-{i}", x + i * step - 4, y + lower + 53,
                  [[0, 0], [-(step - w - 8), 0]])
    arrow(key + "-work-result", x + step * 3 + w / 2, y + top + 110,
          [[0, 0], [0, lower - top - 114]])
    text(key + "-work-result-label", x + step * 3 + w / 2 + 14, y + 155, "evidence", 14, MUTED)
    arrow(key + "-reason-answer", x + step + w / 2, y + top + 110,
          [[0, 0], [0, lower - top - 114]], MUTED)
    text(key + "-reason-answer-label", x + step + w / 2 + 14, y + 143,
         "reasoning /\nexisting evidence", 14, MUTED)
    arrow(key + "-revise", x + w / 2, y + lower - 4,
          [[0, 0], [0, -(lower - top - 114)]], MUTED)
    text(key + "-revise-label", x + w / 2 + 14, y + 155, "revise", 14, MUTED)


def workbench(key, x, y):
    text(key + "-family", x, y, "One Workbench · family explanations plus this instance's working Spaces", 20)
    rect(key + "-guide", x, y + 42, 344, 270, BLUE, BLUE_BG)
    text(key + "-guide-title", x + 18, y + 58, "Guide · explanation", 21, BLUE)
    text(key + "-guide-scope", x + 18, y + 91, "Shared across this family's instances", 14, MUTED)
    for i, label in enumerate(guide.GUIDE_VIEWS):
        button(f"{key}-guide-view-{i}", x + 18, y + 122 + i * 36,
               308, 30, label, size=15)

    rx = x + 374
    rect(key + "-working", rx, y + 42, 966, 270, GREEN, GREEN_BG)
    text(key + "-working-title", rx + 18, y + 58, "Working Spaces · instance content", 21, GREEN)
    text(key + "-space-label", rx + 18, y + 113, "Space", 15, MUTED)
    ui.tabs(key + "-spaces", rx + 86, y + 103,
            ["Ideation", "Story", "Sections", "Delivery"], "Story", size=15, height=34, minimum=120)
    text(key + "-view-label", rx + 18, y + 163, "View", 15, MUTED)
    ui.tabs(key + "-views", rx + 86, y + 153,
            ["Spine", "RoadMap Draw", "Logic + Work", "Related Papers"], "Logic + Work",
            size=15, height=34, minimum=106)
    node(key + "-content", rx + 18, y + 207, 930, 76,
         "Selected View · reasoning, related Work and its product",
         "Goals, design, Studio, progress and checks follow the family's own workflow.", GREEN,
         title_size=17, body_size=15)
    text(key + "-caption", x, y + 318,
         "Space first, then View directly underneath. A family's own Spaces and Views determine how its working content is presented.", 14, MUTED)


def folder_links(key, x, y, rows):
    """Linked nodes trace each surface to its native owner and source path."""
    columns = [(0, 218, "Space / View"), (284, 300, "Native owner"),
               (676, 664, "Folder / file · source convention")]
    for col, (dx, _, label) in enumerate(columns):
        text(f"{key}-heading-{col}", x + dx, y, label, 17, MUTED)
    for row, (surface, owner, path, relation) in enumerate(rows):
        ry = y + 36 + row * 42
        color, bg = (BLUE, BLUE_BG) if row == 0 else (GREEN, GREEN_BG)
        for col, (value, (dx, width, _)) in enumerate(zip((surface, owner, path), columns)):
            cell = f"{key}-node-{row}-{col}"
            start = len(ui.E)
            rect(cell, x + dx, ry, width, 36, RULE, bg if col == 0 else "#ffffff")
            text(cell + "-label", x + dx + 10, ry + 9, value,
                 14 if col < 2 else 13, color if col == 0 else MUTED, mono=col == 2)
            for element in ui.E[start:]:
                element["groupIds"] = [cell + "-group"]
        arrow(f"{key}-reads-{row}", x + 222, ry + 24, [[0, 0], [58, 0]], MUTED)
        text(f"{key}-reads-label-{row}", x + 229, ry + 3, "reads", 12, MUTED)
        arrow(f"{key}-source-{row}", x + 588, ry + 24, [[0, 0], [84, 0]], MUTED)
        text(f"{key}-source-label-{row}", x + 592, ry + 3, relation, 12, MUTED)


def folder_map(key, x, y):
    folder_links(key, x, y, [
        ("Guide", "Family skill + UI contracts",
         "repo: skills/2_theme/paper/<skill>/ + servers/workbench-paper/", "defined in"),
        ("Ideation", "haipipe-paper-ideation",
         "A1-Story/Story00-ideation/", "stored at"),
        ("Story", "haipipe-paper-story",
         "A1-Story/Story<Letter>-<desk>-<idea>/", "stored at"),
        ("Sections", "Section Page owners",
         "Ba-<desk>-Main/ + Bb-<desk>-Appendix/", "stored at"),
        ("Delivery", "Assemble + Round owners",
         "delivery/ + Bc-<desk>-Round/", "stored at"),
        ("Story / RoadMap Draw", "Story drawing owner",
         "studio/<Story stem>.excalidraw", "stored at"),
        ("Related Work", "Task / Discovery owners",
         "external: task-home / discovery-home -> native records", "stored at"),
    ])


VIEWS = [
    {"slug": "skill-set", "label": "Skill set", "title": "Skill set · who owns what",
     "subtitle": "The Paper family's workflow, semantic contracts, native work owners and Workbench presentation.",
     "draw": skill_set,
     "explanations": [
         ("Workflow", "Defines bounded Run Specs, dependencies and gates.\nRoutes work to the artifact's owner."),
         ("Semantic and work owners", "Story explains the research meaning. Native owners\nproduce evidence and keep their records."),
         ("Workbench", "Presents the family's records and routes the reader\nto the owner responsible for an action."),
     ]},
    {"slug": "methods", "label": "Methods", "title": "Methods · how a question reaches an answer",
     "subtitle": "Questions, reasoning, evidence, optional supporting work, interpretation and the issues that remain.",
     "draw": methods,
     "explanations": [
         ("Start with the question", "Name what needs an answer and what would count\nas evidence. Keep the anticipated answer explicit."),
         ("Use related Work when needed", "Existing evidence or reasoning can move an answer\nforward. A Question need not have BJTR work."),
         ("Read the answer and its limits", "Completed work supplies evidence. The owner records\nwhat it supports and what remains unresolved."),
     ]},
    {"slug": "workbench", "label": "Workbench", "title": "Workbench · how the UI is organized",
     "subtitle": "One explanatory Guide joins each family's working Spaces. A selected Space determines its View row.",
     "draw": workbench,
     "explanations": [
         ("Guide", "The four explanation Views describe the family.\nRoadMap Draw brings their drawings together."),
         ("Working Spaces", "Goals, questions, design, Studio and checks belong\nto their family's own working Views."),
         ("Navigation", "Choose Space, then View on the row underneath.\nThe working content keeps the available width."),
     ]},
    {"slug": "folder-map", "label": "Folder map", "title": "Folder map · View -> owner -> folder / file",
     "subtitle": "Follow the arrows to the source. Paper paths are relative to Paper-<Slug>/; repo and external paths are marked.",
     "draw": folder_map,
     "explanations": [
         ("Read the graph", "Start at a Space or View, follow reads to its native owner, then follow stored at to its source folder or file."),
         ("Resolve the actual path", "This Guide explains conventions. board.md binds the active Story, Pages and external work homes for each Paper instance."),
         ("Open the source", "The folder or file node opens its native source in the proposed UI. Task and Discovery keep their own records."),
     ]},
]


def write_scene(stem, title, description, args, preview_names, folder=HERE / "parts"):
    scene = {"type": "excalidraw", "version": 2, "source": "haipipe-workbench-guide-drawings",
             "elements": ui.E, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}
    (folder / (stem + ".excalidraw")).write_text(
        json.dumps(scene, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.previews:
        ui.write_previews(HERE, args.font, args.mono_font, preview_names)
    print(f"Wrote {stem}.excalidraw: {len(ui.E)} elements, {len(ui.FRAMES)} frames")


def drawing_row(key, entry, x, y, w, opened=False, renderer=None,
                filename=None):
    """One full-width fold; an open drawing remains directly under its header."""
    height = 596 if opened else 88
    rect(key + "-row", x, y, w, height, RULE, "#ffffff")
    guide.chevron(key + "-toggle", x + 18, y + 28, opened)
    text(key + "-label", x + 50, y + 14, entry["label"], 22, BLUE)
    text(key + "-purpose", x + 50, y + 53, entry["question"], 16, MUTED)
    text(key + "-state", x + w - 240, y + 19,
         "Family example", 15, GREEN)
    if opened:
        line(key + "-header-rule", x + 16, y + 88, w - 32)
        text(key + "-required", x + 18, y + 105,
             "Required: " + entry["caption"], 16, MUTED)
        rect(key + "-canvas", x + 16, y + 144, w - 32, 394, RULE, "#ffffff")
        text(key + "-filename", x + 30, y + 158, filename, 15, BLUE)
        button(key + "-fullscreen", x + w - 220, y + 152, 190, 30,
               "Open full screen >", size=14)
        renderer(key + "-diagram", x + 24, y + 192)
        text(key + "-sources", x + 18, y + 558,
             "Sources: " + " · ".join(entry["sources"]), 14, MUTED)
    return height


def view_preview(view, x, y):
    key = "guide-view-" + view["slug"]
    guide.heading(key, x, y, "Guide / " + view["label"],
                  "A corresponding drawing in each explanatory View · Paper family example")
    cx, cy = guide.shell(key, x, y, "Paper", "Guide", guide.GUIDE_VIEWS, view["label"],
                         view["label"], view["subtitle"])
    for element in ui.E:
        if element["id"] == key + "-screen":
            element["height"] = 1280
        elif element["id"] == key + "-footer":
            element["y"] = y + 1362
    drawing_row(key + "-draw", TYPE_BY_VIEW[view["label"]], cx, cy,
                guide.CW, opened=True, renderer=view["draw"],
                filename="guide-" + view["slug"] + ".excalidraw")
    rect(key + "-explanation", cx, cy + 612, guide.CW, 314, RULE, PANEL)
    for i, (title, body) in enumerate(view["explanations"]):
        dy = cy + 628 + i * 94
        text(f"{key}-explanation-title-{i}", cx + 18, dy, title, 20, BLUE)
        text(f"{key}-explanation-body-{i}", cx + 18, dy + 32,
             body.replace("\n", " "), 16, MUTED)
    rect(key + "-note", x + 24, y + 1420, FW - 48, 84, BLUE, BLUE_BG)
    text(key + "-note-title", x + 40, y + 1432,
         "One column · drawing and explanation stacked", 20, BLUE)
    text(key + "-note-body", x + 40, y + 1468,
         "Click the drawing row to expand or collapse its canvas. RoadMap Draw opens the same file; the content keeps its native owner.", 16, MUTED)


def roadmap_preview(x, y):
    key = "guide-view-roadmap-draw"
    guide.heading(key, x, y, "Guide / RoadMap Draw",
                  "A single-column drawing View · each row expands its own embedded canvas")
    cx, cy = guide.shell(key, x, y, "Paper", "Guide", guide.GUIDE_VIEWS, "RoadMap Draw",
                         "RoadMap Draw", "Four defined Guide diagram types · each has a question and required content")
    for element in ui.E:
        if element["id"] == key + "-screen":
            element["height"] = 1280
        elif element["id"] == key + "-footer":
            element["y"] = y + 1362
    button(key + "-types", cx + guide.CW - 188, y + 342, 188, 36,
           "Diagram types >", size=15)
    row_y = cy
    for entry in GUIDE_TYPES:
        view = next(view for view in VIEWS if view["label"] == entry["view"])
        row_y += drawing_row(key + "-" + view["slug"], entry, cx, row_y,
                             guide.CW, opened=entry["id"] == "guide.method_flow",
                             renderer=view["draw"], filename=Path(entry["example"]).name) + 12
    rect(key + "-note", x + 24, y + 1420, FW - 48, 84, BLUE, BLUE_BG)
    text(key + "-note-title", x + 40, y + 1432,
         "One row per drawing · independent folds", 20, BLUE)
    text(key + "-note-body", x + 40, y + 1468,
         "Open any row to read its requirements and embedded drawing. Several rows can stay open; collapsing keeps the same drawing file.", 16, MUTED)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previews", action="store_true")
    parser.add_argument("--font")
    parser.add_argument("--mono-font")
    args = parser.parse_args()
    for view in VIEWS:
        reset()
        stem = "guide-" + view["slug"]
        ui.frame(stem + "-frame", "Guide / " + view["label"] + " · drawing", 0, 0, 1388, 466)
        text(stem + "-title", 24, 18, view["title"], 29)
        text(stem + "-subtitle", 24, 64, view["subtitle"], 16, MUTED)
        view["draw"](stem + "-diagram", 24, 108)
        write_scene(stem, view["title"], view["subtitle"], args, [stem])

    reset()
    ui.frame("guide-view-roadmap-draw-frame", "Guide / RoadMap Draw", 0, 0, FW, FH)
    roadmap_preview(0, 0)
    write_scene("guide-roadmap-draw", "Guide / RoadMap Draw",
                "A single-column Guide drawing View with independently collapsible embedded diagrams.",
                args, ["guide-view-roadmap-draw"])

    reset()
    text("guide-drawings-title", 48, 20, "Guide · explanations and RoadMap Draw", 34)
    text("guide-drawings-subtitle", 48, 76,
         "Skill set / Methods / Workbench / Folder map / RoadMap Draw · Space above View · family explanations and drawings", 20, MUTED)
    for i, view in enumerate(VIEWS):
        x = 48
        y = 136 + i * (FH + GAP)
        ui.frame("guide-view-" + view["slug"] + "-frame",
                 "Guide / " + view["label"], x, y, FW, FH)
        view_preview(view, x, y)
    i = len(VIEWS)
    x = 48
    y = 136 + i * (FH + GAP)
    ui.frame("guide-view-roadmap-draw-frame", "Guide / RoadMap Draw", x, y, FW, FH)
    roadmap_preview(x, y)
    write_scene("s02-guide-views", "Guide · explanatory Views and RoadMap Draw",
                "Five Guide UI design previews with explanations and a dedicated drawing View for the Paper family.",
                args, ["guide-view-" + view["slug"] for view in VIEWS] + ["guide-view-roadmap-draw"], HERE)


if __name__ == "__main__":
    main()
