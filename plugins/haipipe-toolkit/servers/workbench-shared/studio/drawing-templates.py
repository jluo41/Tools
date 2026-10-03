"""Prepare the catalog's seven editable starter diagrams and its UI proposal.

Templates contain explicit slots, not invented instance facts. Their filenames,
purposes and required content come from drawing-catalog.json. Optional PNG
previews use the same font and color system as the other Workbench studios.
"""

import argparse
import importlib.util
import json
import textwrap
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SPEC = importlib.util.spec_from_file_location("guide_drawings", HERE / "guide-view-drawings.py")
drawing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(drawing)
ui = drawing.ui
rect, text, button, arrow, line = ui.rect, ui.text, ui.button, ui.arrow, ui.line
node = drawing.node
INK, MUTED, RULE, PANEL = ui.INK, ui.MUTED, ui.RULE, ui.PANEL
BLUE, BLUE_BG, GREEN, GREEN_BG = ui.BLUE, ui.BLUE_BG, ui.GREEN, ui.GREEN_BG
PURPLE, PURPLE_BG = ui.PURPLE, ui.PURPLE_BG
CATALOG = drawing.CATALOG
FW, FH = 1480, 720


def labeled_arrow(key, x, y, points, label, tx, ty, color=BLUE):
    arrow(key, x, y, points, color)
    text(key + "-label", tx, ty, label, 14, MUTED)


def skill_map(key, x, y):
    roles = [
        ("workflow", "Workflow / method owner", "<skill name and responsibilities>\n<routing and review rules>", BLUE, BLUE_BG),
        ("content", "Content / meaning owner", "<skill name and responsibilities>\n<question and product semantics>", GREEN, GREEN_BG),
        ("surface", "Workbench presentation", "<Workbench skill and scope>\n<what the surface reads and shows>", PURPLE, PURPLE_BG),
    ]
    for i, (slug, title, body, color, bg) in enumerate(roles):
        node(key + "-" + slug, x + i * 470, y, 400, 112, title, body, color, bg)
    labeled_arrow(key + "-route", x + 404, y + 56, [[0, 0], [62, 0]], "routes", x + 406, y + 26)
    labeled_arrow(key + "-read", x + 874, y + 56, [[0, 0], [62, 0]], "reads", x + 880, y + 26)
    owners = [
        ("semantic", "Semantic owners", "<named skills and artifacts>\n<what each owner may change>", BLUE),
        ("work", "Native work owners", "<named skills and native records>\n<input, configuration, Ticket, Result>", GREEN),
        ("product", "Product owners", "<named skills and product records>\n<report, Page, delivery or other product>", PURPLE),
    ]
    for i, (slug, title, body, color) in enumerate(owners):
        node(key + "-" + slug, x + i * 470, y + 190, 400, 112, title, body, color)
    labeled_arrow(key + "-semantic-route", x + 200, y + 116, [[0, 0], [0, 70]],
                  "routes", x + 216, y + 143)
    labeled_arrow(key + "-work-reference", x + 670, y + 116, [[0, 0], [0, 70]],
                  "references", x + 686, y + 143)
    labeled_arrow(key + "-product-read", x + 1140, y + 186, [[0, 0], [0, -70]],
                  "reads", x + 1156, y + 143, MUTED)


def method_flow(key, x, y):
    drawing.methods(key, x, y)
    replacements = {
        "question-body": "<question type>\n<accepted answer form>",
        "reason-body": "<reasoning / candidate answers>\n<existing evidence and limits>",
        "need-body": "<missing evidence>\n<information to obtain>",
        "work-body": "<native owner, when needed>\n<input -> required evidence>",
        "result-body": "<Result / evidence source>\n<source and provenance>",
        "review-body": "<interpretation rules>\n<review and acceptance criteria>",
        "answer-body": "<how the family states answers>\n<how uncertainty is recorded>",
        "open-body": "<how issues are recorded>\n<revision / review trigger>",
    }
    for element in ui.E:
        if element["type"] != "text":
            continue
        suffix = element["id"].removeprefix(key + "-")
        if suffix in replacements:
            value = replacements[suffix]
            element.update(text=value, originalText=value,
                           width=max(map(len, value.split("\n"))) * element["fontSize"] * .62)


def branches(key, x, y, label="contains"):
    for i, center in enumerate([200, 670, 1140]):
        arrow(f"{key}-branch-{i}", x + 670, y + 84,
              [[0, 0], [0, 20], [center - 670, 20], [center - 670, 46]])
    text(key + "-branch-label", x + 690, y + 84, label, 14, MUTED)


def ui_map(key, x, y):
    node(key + "-family", x + 470, y, 400, 80, "Family Workbench",
         "<family name and scope>", BLUE, BLUE_BG)
    branches(key, x, y)
    node(key + "-guide", x, y + 134, 400, 182, "Guide · explanations",
         "Skill set / Methods / Workbench\nFolder map / RoadMap Draw\nSources: <family definitions>\nShared across this family's instances", BLUE, BLUE_BG)
    for i in range(2):
        node(f"{key}-space-{i}", x + 470 + i * 470, y + 134, 400, 182,
             "Working Space · <name>",
             "Views: <declared View list>\nShows: <content and purpose>\nOwner: <native record owner>\nSources: <owning records>", GREEN, GREEN_BG)


def folder_map(key, x, y):
    drawing.folder_links(key, x, y, [
        ("Guide", "<family contract owner>",
         "<repo: skill / method / Workbench source paths>", "defined in"),
        ("<working View>", "<native content owner>",
         "<instance-relative source folder / file>", "stored at"),
        ("<another View>", "<native content owner>",
         "<instance-relative source folder / file>", "stored at"),
        ("<working Draw>", "<drawing owner>",
         "<native .excalidraw path>", "stored at"),
        ("<related Work>", "<native work owner>",
         "<work home: configuration / Ticket / Result>", "stored at"),
        ("<product View>", "<native product owner>",
         "<product folder / file>", "stored at"),
        ("<external reference>", "<external owner>",
         "<external: declared source path>", "stored at"),
    ])


def question_map(key, x, y):
    node(key + "-goal", x + 470, y, 400, 80, "Goal · <name>",
         "<goal and native owner reference>", BLUE, BLUE_BG)
    branches(key, x, y, "asks")
    for i in range(3):
        node(f"{key}-question-{i}", x + i * 470, y + 134, 400, 182,
             "Question · <id / short name>",
             "<question and answer form>\nAnswer: <answer / not yet answered>\nEvidence: <reasoning / source>\nOpen: <remaining issue>\nWork: <native references, if any>", GREEN, GREEN_BG, body_size=14)


def design_map(key, x, y):
    rect(key + "-boundary", x + 334, y, 744, 160, RULE, PANEL)
    text(key + "-boundary-name", x + 350, y + 8, "Design boundary · <scope>", 15, MUTED)
    entries = [
        ("input", 0, 264, "Inputs", "<input contract>\n<source owner>"),
        ("component-1", 374, 278, "Component · <name>", "<responsibility>\n<contract / interface>"),
        ("component-2", 750, 278, "Component · <name>", "<responsibility>\n<contract / interface>"),
        ("output", 1134, 206, "Outputs", "<product>\n<acceptance>"),
    ]
    for slug, dx, width, title, body in entries:
        node(key + "-" + slug, x + dx, y + 38, width, 106, title, body, BLUE, BLUE_BG, title_size=17)
    for i, (start, end) in enumerate([(268, 370), (656, 746), (1032, 1130)]):
        labeled_arrow(f"{key}-flow-{i}", x + start, y + 91, [[0, 0], [end - start, 0]],
                      "<flow>", x + start + 18, y + 57)
    node(key + "-decisions", x, y + 212, 646, 104, "Decisions and questions",
         "Decision: <choice + rationale + source>\nOpen question: <issue and native reference>", GREEN, GREEN_BG)
    node(key + "-criteria", x + 694, y + 212, 646, 104, "Constraints and acceptance",
         "Constraint: <boundary or limit>\nReady when: <criterion and native review owner>", PURPLE, PURPLE_BG)


def roadmap(key, x, y):
    text(key + "-goal", x, y, "Goal: <goal reference> · Plan: <owning plan and current records>", 18, BLUE)
    for i in range(3):
        node(f"{key}-milestone-{i}", x + i * 470, y + 44, 400, 170,
             "Milestone · <name>",
             "Question: <question reference>\nDeliverable: <artifact / outcome>\nReady when: <acceptance criterion>\nOwner / Work: <native reference>\nState: <owner state / unknown>", GREEN, GREEN_BG, body_size=14)
        if i < 2:
            labeled_arrow(f"{key}-dependency-{i}", x + i * 470 + 404, y + 128,
                          [[0, 0], [62, 0]], "enables", x + i * 470 + 398, y + 22)
    node(key + "-changes", x, y + 240, 646, 76, "Plan changes",
         "<decision / open issue> -> <affected milestone>", BLUE, title_size=17)
    node(key + "-review", x + 694, y + 240, 646, 76, "Review and readiness",
         "<criterion source> · <review owner and current record>", PURPLE, title_size=17)


RENDERERS = {
    "guide.skill_map": skill_map,
    "guide.method_flow": method_flow,
    "guide.ui_map": ui_map,
    "guide.folder_map": folder_map,
    "work.question_map": question_map,
    "work.design_map": design_map,
    "work.roadmap": roadmap,
}


def save(path, title, description, args):
    path.parent.mkdir(parents=True, exist_ok=True)
    scene = {"type": "excalidraw", "version": 2, "source": "haipipe-workbench-drawing-templates",
             "elements": ui.E, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}
    path.write_text(json.dumps(scene, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ui.write_svg(path.with_suffix(".svg"), title=title, description=description)
    if args.previews:
        ui.write_previews(path.parent, args.font, args.mono_font, [path.stem])
    print(f"Wrote {path.relative_to(ROOT)}: {len(ui.E)} elements")


def template(entry, args):
    drawing.reset()
    key = entry["id"].replace(".", "-")
    ui.frame(key + "-frame", entry["label"] + " · starter template", 0, 0, FW, FH)
    text(key + "-title", 24, 18, entry["label"] + " · starter template", 30)
    text(key + "-question", 24, 67, entry["question"], 18, MUTED)
    text(key + "-unfilled", 1132, 27, "Template · not filled", 16, ui.ORANGE)
    RENDERERS[entry["id"]](key + "-diagram", 44, 124)
    rect(key + "-contract", 24, 506, FW - 48, 178, RULE, PANEL)
    text(key + "-contract-title", 40, 519, "What this drawing must contain", 20, BLUE)
    required = textwrap.fill(" · ".join(entry["required_elements"]), width=142)
    text(key + "-required", 40, 554, required, 15, MUTED)
    text(key + "-sources", 40, 620, "Fill from: " + " · ".join(entry["sources"]), 14, MUTED)
    text(key + "-slot-rule", 40, 654,
         "Replace the slots from the owning records. Add or remove nodes as needed; keep the drawing's defined purpose and required content.", 14, MUTED)
    save(ROOT / entry["template"], entry["label"] + " · starter template", entry["question"], args)


def catalog_preview(args):
    drawing.reset()
    ui.frame("drawing-catalog-frame", "Draw · predefined diagram types", 0, 0, 1480, 1800)
    text("catalog-title", 24, 18, "Draw · predefined diagram types", 30)
    text("catalog-subtitle", 24, 66,
         "The type fixes the question, required content and starting structure. The family or instance supplies the actual content.", 17, MUTED)
    rect("catalog-screen", 24, 126, 1432, 1540, INK, "#ffffff")
    text("catalog-screen-title", 44, 144, "Diagram types", 24)
    button("catalog-close", 1306, 142, 128, 34, "Close", size=15)
    text("catalog-instruction", 44, 193,
         "One column. Open a row to see what to draw and its embedded template; click the row again to collapse it.", 17, MUTED)
    text("catalog-guide-heading", 44, 234, "Guide · family explanations", 21, BLUE)
    guide_types = [entry for entry in CATALOG["types"] if entry["scope"] == "guide"]
    work_types = [entry for entry in CATALOG["types"] if entry["scope"] == "work"]
    row_y = 270
    for entry in guide_types:
        row_y += drawing.drawing_row("catalog-" + entry["id"].replace(".", "-"),
                                     entry, 44, row_y, 1388,
                                     opened=entry["id"] == "guide.method_flow",
                                     renderer=RENDERERS[entry["id"]],
                                     filename=Path(entry["template"]).name,
                                     template=True) + 12
    text("catalog-work-heading", 44, row_y + 12,
         "Working Draw · optional starter templates", 21, GREEN)
    row_y += 48
    for entry in work_types:
        row_y += drawing.drawing_row("catalog-" + entry["id"].replace(".", "-"),
                                     entry, 44, row_y, 1388, template=True) + 12
    rect("catalog-availability", 44, 1540, 1388, 100, RULE, PANEL)
    text("catalog-availability-title", 60, 1552, "Visible expectations", 20, GREEN)
    text("catalog-availability-body", 60, 1588,
         "Guide definitions show missing preparation. A ready template is a starting structure, not a filled drawing.\nWorking Studios may use freely named drawings; template choice and metadata remain optional.", 16, MUTED)
    rect("catalog-note", 24, 1690, 1432, 84, BLUE, BLUE_BG)
    text("catalog-note-title", 40, 1702, "Single-column catalog · embedded drawings in independent folds", 20, BLUE)
    text("catalog-note-body", 40, 1738,
         "Guide and working types appear in successive sections. Each drawing opens under its own row and keeps its source owner.", 16, MUTED)
    save(HERE / "drawing-type-catalog.excalidraw", "Draw · predefined diagram types",
         "Seven predefined diagram types in a single-column list with independently collapsible embedded templates.", args)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previews", action="store_true")
    parser.add_argument("--font")
    parser.add_argument("--mono-font")
    args = parser.parse_args()
    for entry in CATALOG["types"]:
        template(entry, args)
    catalog_preview(args)


if __name__ == "__main__":
    main()
