"""Draw the revised sharing boundary and question-led domain work.

Guide holds family explanations only. Working Views stay in their owning
Workbench's Spaces. Paper's Question -> Work -> Task -> Runs folds provide
the reference; Insight keeps its own Logic / Work / Report composition.
"""

import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "shared_guide_primitives", HERE / "workbench-shared-design.py")
ui = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ui)
rect, text, button, line, card = ui.rect, ui.text, ui.button, ui.line, ui.card
INK, MUTED, RULE, PANEL = ui.INK, ui.MUTED, ui.RULE, ui.PANEL
BLUE, BLUE_BG, GREEN, GREEN_BG = ui.BLUE, ui.BLUE_BG, ui.GREEN, ui.GREEN_BG
ORANGE, PURPLE, PURPLE_BG = ui.ORANGE, ui.PURPLE, ui.PURPLE_BG
FW, FH, GAP, CW = 1480, 1060, 64, 1388
GUIDE_VIEWS = ["Skill set", "Methods", "Workbench", "Folder map", "RoadMap Draw"]
FAMILY_SPACES = {"Paper": ["Ideation", "Story", "Sections", "Delivery"],
                 "Insight": ["Scope", "Insight", "Check", "Delivery"]}
PREVIEWS = ["v4-01-guide", "v4-02-paper-questions",
            "v4-03-paper-question-work", "v4-04-insight-questions"]


def chevron(key, x, y, opened=False, color=MUTED):
    points = [[0, 0], [6, 8], [12, 0]] if opened else [[0, 0], [8, 6], [0, 12]]
    item = ui.base(key, "line", x, y, 12 if opened else 8, 8 if opened else 12, color)
    item.update(points=points, lastCommittedPoint=None, startBinding=None,
                endBinding=None, startArrowhead=None, endArrowhead=None)
    ui.E.append(item)


def shell(key, x, y, family, space, views, view, title, description):
    rect(key + "-screen", x + 24, y + 110, FW - 48, 800, INK, "#ffffff")
    text(key + "-family", x + 44, y + 132, family + " Workbench", 24)
    text(key + "-instance", x + 44, y + 165, "Instance · example-01", 16, MUTED)
    button(key + "-switch", x + 1098, y + 134, 202, 38, "Switch instance  v", size=15)
    button(key + "-folder", x + 1312, y + 134, 122, 38, "Folder >", size=15)
    text(key + "-space-label", x + 44, y + 214, "Space", 16, MUTED)
    ui.tabs(key + "-spaces", x + 108, y + 204,
            ["Guide"] + FAMILY_SPACES[family], space,
            size=16, height=42, minimum=96)
    text(key + "-view-label", x + 44, y + 280, "View", 16, MUTED)
    ui.tabs(key + "-views", x + 108, y + 270, views, view,
            size=15, height=42, minimum=96)
    line(key + "-nav-rule", x + 44, y + 326, FW - 88)
    text(key + "-view-title", x + 44, y + 344, title, 28)
    text(key + "-description", x + 44, y + 388, description, 16, MUTED)
    text(key + "-footer", x + 44, y + 884,
         family + " Workbench  /  example-01  /  " + space + "  /  " + view, 14, MUTED)
    return x + 44, y + 424


def heading(key, x, y, title, subtitle):
    text(key + "-heading", x + 24, y + 18, title, 28)
    text(key + "-subtitle", x + 24, y + 64, subtitle, 17, MUTED)


def note(key, x, y, title, body, color=BLUE, bg=BLUE_BG):
    rect(key + "-note", x + 24, y + 934, FW - 48, 94, color, bg)
    text(key + "-note-title", x + 40, y + 947, title, 20, color)
    text(key + "-note-body", x + 40, y + 982, body, 16, MUTED)


def guide(x, y):
    key = "v4-guide"
    heading(key, x, y, "Guide · shared explanations only",
            "The common Guide describes the family. Instance goals, design, Studio, progress and checks stay in the family's working Spaces.")
    cx, cy = shell(key, x, y, "Paper", "Guide", GUIDE_VIEWS, "Workbench",
                   "Workbench", "The Paper family's UI structure, methods, skill roles and folder mapping")
    rect(key + "-article", cx, cy, CW, 434, RULE, PANEL)
    text(key + "-article-title", cx + 18, cy + 16, "How Paper Workbench is organized", 23)
    text(key + "-article-body", cx + 18, cy + 58,
         "Ideation frames the paper. Story connects its questions to evidence and work.\n"
         "Sections develop the argument; Delivery assembles and checks the manuscript.", 17, MUTED)
    rows = [
        ("Skill set", "haipipe-paper-workflow\nhaipipe-paper-story\nhaipipe-workbench-paper", "Responsibilities and how the skills work together"),
        ("Methods", "Question -> hypotheses -> claims\nWork and evidence\nReview and acceptance", "How the family reasons about its product"),
        ("Folder map", "Story sources and Section Pages\nSupporting Task owners\nNative Tickets and Results", "How Views map to their owning files"),
    ]
    for i, (title, body, caption) in enumerate(rows):
        dx = cx + 18 + i * 454
        card(f"{key}-doc-{i}", dx, cy + 128, 438, 212,
             title, body, BLUE, size=17)
        text(f"{key}-doc-caption-{i}", dx + 16, cy + 287, caption, 14, MUTED)
    text(key + "-family-scope", cx + 18, cy + 374,
         "These explanations are shared across Paper instances. Each instance's working records appear in its own Spaces.", 17, MUTED)
    note(key, x, y, "Guide now keeps kind 1 only",
         "Skill set / Methods / Workbench / Folder map / RoadMap Draw explain the family. Instance work belongs in its working Spaces.")


def paper_shell(key, x, y, description):
    return shell(key, x, y, "Paper", "Story",
                 ["Spine", "RoadMap Draw", "High-level logic + low-level work", "Related Papers"],
                 "High-level logic + low-level work", "Questions", description)


def closed_question(key, cx, cy, label, question, answer, answer_color, detail):
    rect(key, cx, cy, CW, 100, RULE, "#ffffff")
    chevron(key + "-chevron", cx + 18, cy + 21)
    text(key + "-label", cx + 46, cy + 14, label, 16, BLUE)
    text(key + "-question", cx + 46, cy + 44, question, 20)
    text(key + "-detail", cx + 46, cy + 75, detail, 14, MUTED)
    text(key + "-answer", cx + 1110, cy + 16, answer, 16, answer_color)


def paper_questions(x, y):
    key = "v4-paper-questions"
    heading(key, x, y, "Paper / Story · questions lead the view",
            "The collapsed outline shows each question's answer and open issue. Work stays inside the question's fold.")
    cx, cy = paper_shell(key, x, y, "Current Story · expand a question to read its reasoning, answer and related work")
    closed_question(key + "-q1", cx, cy, "Question 1 · Claim support",
                    "Does the proposed method improve on the baseline?",
                    "Partial answer", ORANGE, "Draft report exists; robustness review remains open.")
    closed_question(key + "-q2", cx, cy + 114, "Question 2 · Boundaries",
                    "Which boundary cases change the conclusion?",
                    "Open", MUTED, "No current answer; the evidence need is recorded.")
    closed_question(key + "-q3", cx, cy + 228, "Question 3 · Contribution",
                    "What does the approach add beyond existing methods?",
                    "Reviewed answer", GREEN, "The current report and reading record the reviewed answer.")
    rect(key + "-unassigned", cx, cy + 352, CW, 80, RULE, PANEL)
    chevron(key + "-unassigned-chevron", cx + 18, cy + 374)
    text(key + "-unassigned-title", cx + 46, cy + 366, "Not under a question", 19, MUTED)
    text(key + "-unassigned-body", cx + 46, cy + 398,
         "Shared preparation and other native work remain visible here when no question names them.", 15, MUTED)
    note(key, x, y, "Question progress belongs to the domain View",
         "The question's answer and remaining issue lead the outline. Job / Task / Run records expand together inside related Work.",
         GREEN, GREEN_BG)


def paper_expanded(x, y):
    key = "v4-paper-expanded"
    heading(key, x, y, "Paper / Story · one question, its answer and its Work",
            "Follow Paper's nested folds: open Question, open Work, then open a Task's Runs in the same tree.")
    cx, cy = paper_shell(key, x, y, "Question 1 selected · current answer, evidence, remaining review and related work")
    rect(key + "-question", cx, cy, CW, 434, RULE, "#ffffff")
    rect(key + "-question-head", cx, cy, CW, 88, BLUE, BLUE_BG)
    chevron(key + "-question-chevron", cx + 18, cy + 24, opened=True, color=BLUE)
    text(key + "-question-label", cx + 46, cy + 14, "Question 1 · Claim support", 16, BLUE)
    text(key + "-question-text", cx + 46, cy + 45,
         "Does the proposed method improve on the baseline?", 21)
    text(key + "-question-answer", cx + 1150, cy + 16, "Partial answer", 17, ORANGE)

    lx, rx = cx + 18, cx + 708
    text(key + "-logic-title", lx, cy + 106, "Answer & reasoning", 21)
    text(key + "-answer-label", lx, cy + 149, "Current answer", 16, BLUE)
    text(key + "-answer-text", lx, cy + 178,
         "The main comparison supports improvement;\nrobustness has not been reviewed.", 18)
    text(key + "-evidence-label", lx, cy + 238, "What supports it", 16, BLUE)
    text(key + "-evidence-text", lx, cy + 267,
         "Hypothesis 1a · improvement on the primary metric\nClaim 1a · provisional, pending the robustness check", 16, MUTED)
    text(key + "-next-label", lx, cy + 326, "What remains open", 16, ORANGE)
    text(key + "-next-text", lx, cy + 356,
         "Review the boundary comparison and the current Report.", 16, MUTED)
    button(key + "-report", lx, cy + 392, 212, 28, "Report · draft >", size=14)

    text(key + "-work-title", rx, cy + 106, "Work", 21)
    chevron(key + "-foundation-chevron", rx, cy + 148)
    text(key + "-foundation", rx + 24, cy + 140,
         "Prepare shared input", 17)
    text(key + "-foundation-meta", rx + 24, cy + 167,
         "Foundation work · also for Question 2", 14, MUTED)

    rect(key + "-work-fold", rx - 8, cy + 202, 670, 198, RULE, PANEL)
    chevron(key + "-work-chevron", rx + 4, cy + 218, opened=True, color=BLUE)
    text(key + "-work-name", rx + 26, cy + 210,
         "Compare method and baseline", 17, BLUE)
    text(key + "-block", rx + 26, cy + 242, "b03_cases", 15, MUTED)
    text(key + "-job", rx + 46, cy + 267, "j01_compare", 15, MUTED)
    chevron(key + "-task-chevron", rx + 60, cy + 300, opened=True)
    text(key + "-task", rx + 84, cy + 292, "t01_metrics", 15)
    text(key + "-run", rx + 104, cy + 320,
         "run-compare-1002-baseline", 14, BLUE)
    text(key + "-run-status", rx + 424, cy + 320, "Complete", 14, GREEN)
    button(key + "-run-result", rx + 526, cy + 313, 110, 28, "Result >", size=14)
    chevron(key + "-task2-chevron", rx + 60, cy + 381)
    text(key + "-task2", rx + 84, cy + 373,
         "t02_robustness · 2 Runs", 15)
    text(key + "-review", rx + 24, cy + 404,
         "Next: review the interpretation", 15, MUTED)
    note(key, x, y, "Question state and work receipts remain distinct",
         "This example has a completed Run and a partial answer awaiting review. The owning question / Report records its answer state.",
         GREEN, GREEN_BG)


def insight(x, y):
    key = "v4-insight"
    heading(key, x, y, "Insight / Questions · preserve the family's composition",
            "Insight keeps its partition-specific Logic / Work / Report layout. Working progress stays in Insight, alongside the question.")
    cx, cy = shell(key, x, y, "Insight", "Insight", ["Questions"], "Questions",
                   "Questions · Full", "Each question keeps its own answer state, work and report on the selected partition")
    col = [cx + 18, cx + 486, cx + 954]
    for i, label in enumerate(["Logic · the question", "Work", "Report · the answer"]):
        text(f"{key}-column-{i}", col[i], cy, label, 18, MUTED)
    rect(key + "-data", cx, cy + 40, CW, 40, RULE, PANEL)
    chevron(key + "-data-chevron", cx + 16, cy + 54)
    text(key + "-data-label", cx + 42, cy + 48, "Data questions", 17)

    rect(key + "-information", cx, cy + 92, CW, 234, RULE, "#ffffff")
    chevron(key + "-information-chevron", cx + 16, cy + 106, opened=True, color=BLUE)
    text(key + "-information-label", cx + 42, cy + 100, "Information questions", 18, BLUE)
    line(key + "-information-rule", cx + 16, cy + 133, CW - 32)
    text(key + "-q1-label", col[0], cy + 150, "Question 1 · Variant comparison", 16, BLUE)
    text(key + "-q1-question", col[0], cy + 178,
         "Which variant performs best?", 18)
    text(key + "-q1-state", col[0], cy + 210, "Partial answer", 16, ORANGE)
    chevron(key + "-work-chevron", col[1], cy + 156, opened=True)
    text(key + "-work-label", col[1] + 22, cy + 148, "Compare variants", 17)
    text(key + "-work-task", col[1] + 22, cy + 180, "t01_compare · 1 Run", 15, MUTED)
    text(key + "-work-run", col[1] + 40, cy + 209,
         "run-insight-1002-variant", 14, BLUE)
    text(key + "-work-state", col[1] + 40, cy + 233, "Complete · Result >", 14, GREEN)
    text(key + "-report", col[2], cy + 150,
         "Difference detected; subgroup\ncomparison remains open.", 17)
    button(key + "-report-open", col[2], cy + 204, 138, 28, "Report >", size=14)
    line(key + "-q-divider", cx + 16, cy + 267, CW - 32)
    text(key + "-q2", col[0], cy + 283, "Question 2 · Why does it differ?", 16)
    text(key + "-q2-work", col[1], cy + 283, "No work commissioned", 15, MUTED)
    text(key + "-q2-answer", col[2], cy + 283, "No current report", 15, MUTED)
    for i, title in enumerate(["Knowledge questions", "Wisdom questions"]):
        ry = cy + 340 + i * 52
        rect(f"{key}-fold-{i}", cx, ry, CW, 40, RULE, PANEL)
        chevron(f"{key}-fold-chevron-{i}", cx + 16, ry + 14)
        text(f"{key}-fold-label-{i}", cx + 42, ry + 8, title, 17)
    note(key, x, y, "Former kinds 2 and 3 now belong together",
         "The family's native question marks, reports and work references supply its working UI. Guide supplies explanatory knowledge only.",
         PURPLE, PURPLE_BG)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previews", action="store_true")
    parser.add_argument("--font")
    parser.add_argument("--mono-font")
    args = parser.parse_args()
    text("v4-title", 48, 20, "Workbench Shared · Guide v4", 34)
    text("v4-subtitle", 48, 75,
         "Guide = family explanations. Working Spaces = questions, answers, evidence and related work for this instance.", 20, MUTED)
    text("v4-status", 48, 116, "Design proposal · illustrative answer states and work records", 16, MUTED)
    x0, x1 = 48, 48 + FW + GAP
    y0, y1 = 176, 176 + FH + GAP
    for key, name, x, y, render in [
        ("v4-frame-guide", "01 · Guide / Workbench", x0, y0, guide),
        ("v4-frame-questions", "02 · Paper / Story / Questions", x1, y0, paper_questions),
        ("v4-frame-work", "03 · Paper / Question / Work", x0, y1, paper_expanded),
        ("v4-frame-insight", "04 · Insight / Questions", x1, y1, insight),
    ]:
        render(*ui.frame(key, name, x, y, FW, FH))
    scene = {"type": "excalidraw", "version": 2, "source": "haipipe-workbench-shared-guide-v4",
             "elements": ui.E, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}
    path = HERE / "workbench-shared-guide-v4.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ui.write_svg(HERE / "workbench-shared-guide-v4.svg")
    if args.previews:
        ui.write_previews(HERE, args.font, args.mono_font, PREVIEWS)
    print(f"Wrote {path.name}: {len(ui.E)} elements, {len(ui.FRAMES)} frames")


if __name__ == "__main__":
    main()
