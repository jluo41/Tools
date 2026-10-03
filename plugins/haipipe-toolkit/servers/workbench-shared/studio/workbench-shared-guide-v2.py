"""Draw a second Guide layout: Space tabs above a grouped View sidebar.

Kinds 1 and 2 share Guide. The family's remaining Spaces show the selected
instance's specialized work. This is a separate design variant for comparison.
Uses the original studio's drawing and preview primitives.
"""

import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "shared_guide_drawing", HERE / "workbench-shared-design.py")
ui = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ui)

rect, text, button = ui.rect, ui.text, ui.button
line, card, arrow = ui.line, ui.card, ui.arrow
INK, MUTED, RULE, PANEL = ui.INK, ui.MUTED, ui.RULE, ui.PANEL
BLUE, BLUE_BG = ui.BLUE, ui.BLUE_BG
GREEN, GREEN_BG = ui.GREEN, ui.GREEN_BG
PURPLE, PURPLE_BG = ui.PURPLE, ui.PURPLE_BG
FW, FH, GAP = 1480, 1060, 64
CONTENT_W, MAIN_W, SIDE_W, COLUMN_GAP = 1124, 752, 348, 24
PREVIEWS = ["v2-01-guide-skills", "v2-02-guide-progress",
            "v2-03-labeling-definition", "v2-04-guide-studio"]


def sidebar_item(key, x, y, label, selected):
    if selected:
        rect(key + "-selected", x, y, 198, 36, BLUE, BLUE_BG)
    text(key + "-label", x + 14, y + 7, label, 17,
         BLUE if selected else MUTED)


def shell(key, x, y, space, view, title, description):
    rect(key + "-screen", x + 24, y + 110, FW - 48, 800, INK, "#ffffff")
    text(key + "-family", x + 44, y + 132, "Labeling Workbench", 24)
    text(key + "-instance", x + 44, y + 165, "Instance · b01_pilot", 16, MUTED)
    button(key + "-switch", x + 1098, y + 134, 202, 38, "Switch instance  v", size=15)
    button(key + "-folder", x + 1312, y + 134, 122, 38, "Folder >", size=15)
    text(key + "-space-label", x + 44, y + 214, "Space", 16, MUTED)
    ui.tabs(key + "-spaces", x + 108, y + 204,
            ["Guide", "Data", "Labeling", "Quality", "Delivery"], space,
            size=16, height=42, minimum=96)
    line(key + "-divider", x + 44, y + 266, FW - 88)

    sx, sy = x + 44, y + 286
    rect(key + "-sidebar", sx, sy, 238, 580, RULE, PANEL)
    text(key + "-sidebar-title", sx + 18, sy + 14, space, 22)
    if space == "Guide":
        text(key + "-about-title", sx + 18, sy + 60, "About the Workbench", 15, MUTED)
        for i, label in enumerate(ui.INTRO_VIEWS):
            sidebar_item(f"{key}-intro-{i}", sx + 20, sy + 88 + i * 42,
                         label, label == view)
        line(key + "-sidebar-rule", sx + 18, sy + 228, 202)
        text(key + "-block-title", sx + 18, sy + 252, "This Block", 15, MUTED)
        for i, label in enumerate(ui.BLOCK_VIEWS):
            sidebar_item(f"{key}-block-{i}", sx + 20, sy + 280 + i * 42,
                         label, label == view)
    else:
        text(key + "-views-title", sx + 18, sy + 60, "Views", 15, MUTED)
        for i, label in enumerate(["Definition", "Rounds", "Guideline"]):
            sidebar_item(f"{key}-domain-{i}", sx + 20, sy + 88 + i * 42,
                         label, label == view)
    text(key + "-sidebar-instance", sx + 18, sy + 526,
         "Current instance\nb01_pilot", 14, MUTED)

    cx = x + 306
    text(key + "-breadcrumb", cx, y + 291, space + " / " + view, 15, MUTED)
    text(key + "-view-title", cx, y + 326, title, 28)
    text(key + "-description", cx, y + 369, description, 16, MUTED)
    text(key + "-footer", cx, y + 875,
         "Labeling Workbench  /  b01_pilot  /  " + space + "  /  " + view, 14, MUTED)
    return cx, y + 408


def heading(key, x, y, title, subtitle):
    text(key + "-heading", x + 24, y + 18, title, 28)
    text(key + "-subtitle", x + 24, y + 64, subtitle, 17, MUTED)


def note(key, x, y, title, body, color=BLUE, bg=BLUE_BG):
    rect(key + "-note", x + 24, y + 934, FW - 48, 94, color, bg)
    text(key + "-note-title", x + 40, y + 947, title, 20, color)
    text(key + "-note-body", x + 40, y + 982, body, 16, MUTED)


def skills(x, y):
    key = "v2-skills"
    heading(key, x, y, "Guide · family explanation",
            "Guide contains the family's explanation and the common working Views for the current instance.")
    cx, cy = shell(key, x, y, "Guide", "Skill set", "Skill set",
                   "How this Workbench's skills fit together")
    rows = [
        ("Semantic rules", "label-building",
         "Defines meaning, authority\nand human decisions.\n\nContract · Round · Freeze"),
        ("Workflow", "label-building-workflow",
         "Organizes Building Run order\nand its internal steps.\n\nConnects work to its owner."),
        ("Workbench UI", "haipipe-workbench-labeling",
         "Presents the family's Spaces\nand their working Views.\n\nKeeps native records visible."),
    ]
    card_w = (CONTENT_W - 32) / 3
    for i, (title, skill, body) in enumerate(rows):
        dx = cx + i * (card_w + 16)
        rect(f"{key}-card-{i}", dx, cy, card_w, 256, RULE, PANEL)
        text(f"{key}-title-{i}", dx + 16, cy + 16, title, 22)
        text(f"{key}-skill-{i}", dx + 16, cy + 56, skill, 14, BLUE)
        text(f"{key}-body-{i}", dx + 16, cy + 94, body, 16, MUTED)
        button(f"{key}-open-{i}", dx + 16, cy + 210, 144, 32, "Open skill >", size=15)
    rect(key + "-connections", cx, cy + 278, CONTENT_W, 156, RULE, "#ffffff")
    text(key + "-connections-title", cx + 18, cy + 294,
         "Where to go next", 21)
    half_w = (CONTENT_W - 58) / 2
    card(key + "-ui-doc", cx + 18, cy + 336, half_w, 80,
         "Workbench", "UI structure, design logic and each Space's role", BLUE, size=15)
    card(key + "-folder-doc", cx + 40 + half_w, cy + 336, half_w, 80,
         "Folder map", "How the UI maps to folders and owning records", BLUE, size=15)
    note(key, x, y, "1 · About the Workbench",
         "Skill set / Workbench / Folder map explain this family. Switching instances keeps this explanation; the active path can update.")


def progress(x, y):
    key = "v2-progress"
    heading(key, x, y, "Guide · common View, current instance",
            "Guide > Progress opens the common working View. Its records come from the selected Block.")
    cx, cy = shell(key, x, y, "Guide", "Progress", "Progress",
                   "b01_pilot · current Jobs, Tasks and native Run records")
    for i, (title, value) in enumerate([
        ("Tasks", "4 in this Job"),
        ("Executions", "2 complete"),
        ("Readings", "1 current"),
    ]):
        metric_w = (MAIN_W - 32) / 3
        dx = cx + i * (metric_w + 16)
        rect(f"{key}-metric-{i}", dx, cy, metric_w, 78, RULE, PANEL)
        text(f"{key}-metric-title-{i}", dx + 16, cy + 12, title, 15, MUTED)
        text(f"{key}-metric-value-{i}", dx + 16, cy + 38, value, 22)
    ty = cy + 96
    rect(key + "-tasks", cx, ty, MAIN_W, 338, RULE, "#ffffff")
    ui.tabs(key + "-filter", cx + 16, ty + 14,
            ["Jobs", "Tasks", "Runs"], "Tasks", size=14, height=30, minimum=76)
    text(key + "-job", cx + MAIN_W - 336, ty + 20, "j01_inputs", 16, MUTED)
    column_offsets = [16, MAIN_W * .372, MAIN_W * .598, MAIN_W * .782]
    for i, (title, offset) in enumerate(zip(
            ["Task", "Execution", "Page", "Reading"], column_offsets)):
        text(f"{key}-column-{i}", cx + offset, ty + 67, title, 15, MUTED)
    line(key + "-table-rule", cx + 16, ty + 96, MAIN_W - 32)
    rows = [
        ("t01 Prepare input", "Complete", "Current", "Pending"),
        ("t02 Label definition", "Running", "Previous", "Reopened"),
        ("t03 Pilot labels", "Waiting", "Missing", "Not started"),
        ("t04 Review export", "Complete", "Current", "Passed"),
    ]
    for i, values in enumerate(rows):
        ry = ty + 112 + i * 46
        if i == 1:
            rect(key + "-selected-row", cx + 8, ry - 5, MAIN_W - 16, 37, BLUE, BLUE_BG)
        for j, (value, offset) in enumerate(zip(values, column_offsets)):
            color = BLUE if i == 1 else (GREEN if value == "Passed" else INK)
            text(f"{key}-row-{i}-{j}", cx + offset, ry, value, 15, color)
    text(key + "-reading-note", cx + 16, ty + 305,
         "Checklist shows the current checks and reading gates.", 15, MUTED)
    rx = cx + MAIN_W + COLUMN_GAP
    rect(key + "-runs", rx, cy, SIDE_W, 434, RULE, PANEL)
    text(key + "-runs-title", rx + 18, cy + 16, "Runs", 23)
    text(key + "-runs-task", rx + 18, cy + 58, "t02 Label definition", 17, MUTED)
    button(key + "-run", rx + 18, cy + 104, 312, 38,
           "r02_definition", selected=True, size=16)
    text(key + "-state", rx + 18, cy + 174, "Recorded state · running", 17, BLUE)
    text(key + "-scope", rx + 18, cy + 210,
         "Latest native receipt\nSelected Task and Run", 16, MUTED)
    line(key + "-run-divider", rx + 18, cy + 276, 312)
    text(key + "-run-sections", rx + 18, cy + 299,
         "> Prompt                 Copy\n> Process                Open\n> Results                Open", 17)
    note(key, x, y, "2 · This Block",
         "Goal / Design / Studio / Progress / Checklist share their View structure. Each instance supplies its own goals, work and records.",
         GREEN, GREEN_BG)


def domain(x, y):
    key = "v2-domain"
    heading(key, x, y, "A specialized Space · this instance's work",
            "Selecting Labeling opens its own Views. Guide remains one entry in the Space navigation.")
    cx, cy = shell(key, x, y, "Labeling", "Definition", "Definition",
                   "b01_pilot · the label definitions used by this instance")
    rect(key + "-definition", cx, cy, MAIN_W, 434, RULE, PANEL)
    text(key + "-definitions-title", cx + 18, cy + 18, "Label definitions", 22)
    text(key + "-definitions-desc", cx + 18, cy + 58,
         "Meaning, boundary examples and review rules", 16, MUTED)
    for i, (title, body) in enumerate([
        ("Keep", "Meets the definition.\n\nRecord the supporting\nexample and rationale."),
        ("Revise", "Needs a correction.\n\nRecord the boundary\nand the proposed change."),
        ("Uncertain", "Needs human review.\n\nKeep the case and its\nopen question visible."),
    ]):
        label_w = (MAIN_W - 56) / 3
        card(f"{key}-label-{i}", cx + 18 + i * (label_w + 10), cy + 110,
             label_w, 234, title, body, size=15)
    text(key + "-definition-footer", cx + 18, cy + 379,
         "Definitions and their history belong to this labeling instance.", 15, MUTED)
    rx = cx + MAIN_W + COLUMN_GAP
    rect(key + "-runs", rx, cy, SIDE_W, 434, RULE, PANEL)
    text(key + "-runs-title", rx + 18, cy + 18, "Definition Runs", 22)
    button(key + "-run-type", rx + 18, cy + 66, 312, 38,
           "Definition discussion", selected=True, size=15)
    card(key + "-run-details", rx + 18, cy + 126, 312, 174,
         "Current discussion",
         "Pending human feedback\n\n> Prompt            Copy\n> Result            Open", size=16)
    text(key + "-owner", rx + 18, cy + 330,
         "This family's workflow\nand native owner records", 16, MUTED)
    note(key, x, y, "3 · Specialized instance work",
         "Data / Labeling / Quality / Delivery carry this instance's domain work. Each family defines its own Spaces and Views.",
         PURPLE, PURPLE_BG)


def studio(x, y):
    key = "v2-studio"
    heading(key, x, y, "Guide · Studio View",
            "Studio is a common working View inside Guide. The existing Draw-above-Chat arrangement stays together.")
    cx, cy = shell(key, x, y, "Guide", "Studio", "Studio",
                   "Selected owner · j01_inputs / t02_label_definition")
    rect(key + "-draw", cx, cy, MAIN_W, 236, RULE, "#ffffff")
    text(key + "-drawing-title", cx + 16, cy + 14, "Draw · roadmap.excalidraw", 18)
    button(key + "-draw-action", cx + MAIN_W - 154, cy + 10, 138, 32, "Draw it", size=15)
    node_w = (MAIN_W - 120) / 4
    node_step = node_w + 26
    for i, label in enumerate(["Goal", "Definition", "Pilot", "Review"]):
        nx = cx + 18 + i * node_step
        button(f"{key}-node-{i}", nx, cy + 82, node_w, 52, label,
               selected=i == 1, size=17)
        if i < 3:
            arrow(f"{key}-arrow-{i}", nx + node_w + 2, cy + 108, [[0, 0], [21, 0]])
    feedback_x = cx + 18 + node_step + node_w / 2
    arrow(key + "-feedback", feedback_x, cy + 138,
          [[node_step * 2, 0], [node_step * 2, 44], [0, 44], [0, 0]], MUTED)
    text(key + "-feedback-text", feedback_x + 49, cy + 188,
         "revise the definition", 15, MUTED)
    rect(key + "-chat", cx, cy + 252, MAIN_W, 182, RULE, PANEL)
    text(key + "-chat-title", cx + 16, cy + 266, "Chat · current discussion", 20)
    text(key + "-person", cx + 16, cy + 310,
         "Person   Keep the uncertain cases visible.", 16)
    text(key + "-agent", cx + 16, cy + 344,
         "Agent     Add a review step after the pilot.", 16, MUTED)
    button(key + "-chat-open", cx + 16, cy + 385, 158, 32, "Open chat >", size=15)
    rx = cx + MAIN_W + COLUMN_GAP
    rect(key + "-context", rx, cy, SIDE_W, 434, RULE, PANEL)
    text(key + "-context-title", rx + 18, cy + 18, "Owner context", 22)
    text(key + "-owner", rx + 18, cy + 66, "t02_label_definition", 17, BLUE)
    card(key + "-drawing-context", rx + 18, cy + 110, 312, 100,
         "Kept drawing", "studio/draw/\nroadmap.excalidraw", size=16)
    card(key + "-conversation", rx + 18, cy + 226, 312, 100,
         "Kept conversation", "studio/chat/\nThe same selected owner", size=16)
    button(key + "-full-screen", rx + 18, cy + 362, 312, 38,
           "Open full screen >", size=16)
    note(key, x, y, "A common room, with the current owner's content",
         "Switch the instance or selected owner to load its kept drawing and chat. Guide's navigation and Studio's layout remain shared.",
         GREEN, GREEN_BG)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previews", action="store_true")
    parser.add_argument("--font")
    parser.add_argument("--mono-font")
    args = parser.parse_args()
    text("v2-title", 48, 20, "Workbench Shared · Guide v2", 34)
    text("v2-subtitle", 48, 75,
         "Space -> View. Guide holds 1 Explanation + 2 Common instance Views. The other Spaces hold 3 Specialized instance work.", 20, MUTED)
    text("v2-status", 48, 116, "Alternative layout · illustrative content and states", 16, MUTED)
    x0, x1 = 48, 48 + FW + GAP
    y0, y1 = 176, 176 + FH + GAP
    for key, name, x, y, render in [
        ("v2-frame-skills", "01 · Guide / Skill set", x0, y0, skills),
        ("v2-frame-progress", "02 · Guide / Progress", x1, y0, progress),
        ("v2-frame-domain", "03 · Labeling / Definition", x0, y1, domain),
        ("v2-frame-studio", "04 · Guide / Studio", x1, y1, studio),
    ]:
        render(*ui.frame(key, name, x, y, FW, FH))
    scene = {"type": "excalidraw", "version": 2, "source": "haipipe-workbench-shared-guide-v2",
             "elements": ui.E, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}
    path = HERE / "workbench-shared-guide-v2.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ui.write_svg(HERE / "workbench-shared-guide-v2.svg")
    if args.previews:
        ui.write_previews(HERE, args.font, args.mono_font, PREVIEWS)
    print(f"Wrote {path.name}: {len(ui.E)} elements, {len(ui.FRAMES)} frames")


if __name__ == "__main__":
    main()
