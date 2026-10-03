"""Task Workbench design, in the existing Paper / Page / Insight Studio style.

The base, text, rect, button, line and arrow primitives below are copied from
workbench-paper/studio/paper-workbench-design.py. Preserve their palette,
fonts, line treatment and dimensions when changing Task contents.

Generate: python task-workbench-design.py
Named frames: Structure, Task, Studio, RelatedPaper, Progress, Guide.
All data is illustrative. Task has four Views: Task, Roadmap Studio, Related
Paper, Progress. The Task View follows Paper's vertically stacked Question
cards: one full-width question header and three side-by-side columns,
Logic left, Work in the middle and Report right, following Insight's layout.
Report includes the answer, evidence, limits and next action.
Roadmap Studio is a freeform list: each drawing independently expands into
its own embedded Excalidraw canvas.
"""
import json
import random
import sys
import textwrap
import time
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_suffix(".excalidraw")
random.seed(261002)
NOW = int(time.time() * 1000)
E = []

BLUE, GREEN, INK, MUTED, RULE, PANEL = "#1864ab", "#2b8a3e", "#1e1e1e", "#495057", "#ced4da", "#f8f9fa"


def base(id_, type_, x, y, w, h, stroke=INK, bg="transparent", dashed=False, rounded=True):
    return {"id": id_, "type": type_, "x": x, "y": y, "width": w, "height": h, "angle": 0,
            "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": 2,
            "strokeStyle": "dashed" if dashed else "solid", "roughness": 0, "opacity": 100,
            "groupIds": [], "frameId": None, "roundness": {"type": 3} if rounded else None,
            "seed": random.randint(1, 2**31 - 1), "version": 1,
            "versionNonce": random.randint(1, 2**31 - 1), "isDeleted": False,
            "boundElements": [], "updated": NOW, "link": None, "locked": False}


def text(id_, x, y, s, size=16, color=INK, mono=False):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * size * (0.6 if mono else 0.56)
    e = base(id_, "text", x, y, w, len(lines) * size * 1.25, stroke=color, rounded=False)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=3 if mono else 8,
             textAlign="left", verticalAlign="top", containerId=None, autoResize=True,
             lineHeight=1.25)
    E.append(e)


def rect(id_, x, y, w, h, stroke=INK, bg="transparent", dashed=False):
    E.append(base(id_, "rectangle", x, y, w, h, stroke, bg, dashed))
    return E[-1]


def button(id_, x, y, w, h, label, sel=False, size=17, dashed=False, green=False):
    stroke = GREEN if green else (BLUE if sel else INK)
    bg = "#ebfbee" if green else ("#e7f5ff" if sel else "transparent")
    r = rect(id_, x, y, w, h, stroke, bg, dashed)
    tw, th = len(label) * size * 0.56, size * 1.25
    t = base(id_ + "-text", "text", x + (w - tw) / 2, y + (h - th) / 2, tw, th,
             stroke=stroke, rounded=False)
    t.update(text=label, originalText=label, fontSize=size, fontFamily=8, textAlign="center",
             verticalAlign="middle", containerId=id_, autoResize=True, lineHeight=1.25)
    r["boundElements"] = [{"id": id_ + "-text", "type": "text"}]
    E.append(t)


def line(id_, x, y, w, color=RULE):
    e = base(id_, "line", x, y, w, 0, stroke=color, rounded=False)
    e.update(points=[[0, 0], [w, 0]], lastCommittedPoint=None, startBinding=None,
             endBinding=None, startArrowhead=None, endArrowhead=None)
    E.append(e)


def arrow(id_, x, y, points, color, both=False):
    e = base(id_, "arrow", x, y, max(p[0] for p in points), max(abs(p[1]) for p in points), stroke=color,
             rounded=False)
    e.update(points=points, lastCommittedPoint=None, startBinding=None, endBinding=None,
             startArrowhead="arrow" if both else None, endArrowhead="arrow", elbowed=False)
    E.append(e)



FW, FH, GAP = 1176, 820, 32
X = [48 + i * (FW + GAP) for i in range(3)]
TASK_VIEWS = ["Task", "Roadmap Studio", "Related Paper", "Progress"]
GUIDE_VIEWS = ["Skill set", "Methods", "Workbench", "Folder map", "RoadMap Draw"]
QUESTION_HEIGHT = 480
TASK_HEIGHT = 1800
PROGRESS_HEIGHT = 900


def framed(name, x, y, w, h, draw):
    # Frames are export/navigation boundaries; the visible geometry uses the
    # unmodified Paper Studio primitives above.
    f = base("frame-" + name.lower(), "frame", x, y, w, h, rounded=False)
    f.update(name=name)
    E.append(f)
    start = len(E)
    draw(x, y)
    for e in E[start:]:
        e["frameId"] = f["id"]


def view_row(key, x, y, labels, selected):
    for i, label in enumerate(labels):
        w = max(112, len(label) * 9 + 28)
        button(f"{key}-{i}", x, y, w, 40, label, sel=i == selected, size=17)
        x += w + 12


def shell(key, x, y, title, space, views, selected, reads, height=FH):
    rect(key + "-box", x, y, FW, height)
    text(key + "-title", x + 24, y + 26, title, 30)
    line(key + "-rule", x + 24, y + 62, FW - 48)
    text(key + "-space-label", x + 24, y + 88, "Space", 17, MUTED)
    button(key + "-guide", x + 94, y + 76, 176, 50, "Guide", sel=space == "Guide", size=19)
    button(key + "-task", x + 282, y + 76, 176, 50, "Task", sel=space == "Task", size=19)
    text(key + "-view-label", x + 24, y + 152, "View", 17, MUTED)
    view_row(key + "-view", x + 94, y + 140, views, selected)
    text(key + "-reads", x + 24, y + 202, reads, 16, MUTED)


text("title", 48, 24, "Task Workbench · design", 34)
text("subtitle", 48, 74,
     "One Block. Each Question holds Logic → Work → Report: what we ask, what we do, and what we learn. "
     "Cards stack vertically in the Paper Workbench layout.", 18, MUTED)
text("p1-title", 48, 128, "1 · Spaces, Views, work, and the Skills behind it", 28)


def structure(x, y):
    columns = [
        ("Guide Space", "How do this Workbench and its Skills work?", [
            ("Skill set", "Task family and roles", "haipipe-task · haipipe-page", "Same explanation across Task Blocks"),
            ("Methods", "How questions become answers", "", "Reasoning, evidence, optional work and interpretation"),
            ("Workbench", "Spaces and Views", "haipipe-workbench-task", "Each Question: Logic → Work → Report"),
            ("Folder map", "Block / Job / Task / Run", "haipipe-task", "Canonical folders, readers and writers"),
            ("RoadMap Draw", "Explanatory diagrams", "", "Skill map, Method flow, UI map and Folder map"),
        ], "Shared Guide structure; explanations belong to the Task family."),
        ("Task Space", "What questions does this Block need to answer?", [
            ("Task", "Logic → Work → Report", "haipipe-task · haipipe-page", "One Question per card; Logic left, Work middle, Report right"),
            ("Roadmap Studio", "Freeform drawings", "", "One collapsible row per drawing; expand to edit in Excalidraw"),
            ("Related Paper", "External knowledge and resources", "", "Papers, repositories and references linked to a Question"),
            ("Progress", "Report status, work, next actions", "haipipe-task", "Question → Job → Task → Run; evidence and blockers"),
        ], "Task-owned Views; the current Block's questions, work and drawings."),
        ("Shared foundation", "Which parts do Workbench families share?", [
            ("Navigation", "Space → View", "", "View navigation sits directly below the selected Space"),
            ("Drawing row", "Expand / collapse independently", "", "One column; each expanded row embeds its own Excalidraw"),
            ("Guide drawings", "Four explanatory types", "", "A common introduction, filled from each family's own contracts"),
            ("Working Studio", "Freeform contents", "", "Templates are optional; no required type, status or metadata form"),
            ("Ownership", "Read the native records", "", "Families own their Views, content, actions and saved drawings"),
        ], "Shared presentation; family-owned workflow and content."),
    ]
    for i, (title, asks, rows, footer) in enumerate(columns):
        xx = x + i * (FW + GAP)
        rect(f"map-{i}", xx, y, FW, 578)
        text(f"map-title-{i}", xx + 24, y + 22, title, 28)
        text(f"map-asks-{i}", xx + 24, y + 64, asks, 19, BLUE)
        line(f"map-rule-{i}", xx + 24, y + 100, FW - 48)
        for j, (view, work, skill, note) in enumerate(rows):
            yy = y + 120 + j * 76
            button(f"map-view-{i}-{j}", xx + 24, yy, 200, 40, view)
            text(f"map-work-{i}-{j}", xx + 248, yy + 3, work, 17)
            if skill:
                text(f"map-skill-{i}-{j}", xx + 650, yy + 3, skill, 16, GREEN, mono=True)
            text(f"map-note-{i}-{j}", xx + 248, yy + 33, note, 15, MUTED)
        text(f"map-foot-{i}", xx + 24, y + 528, footer, 17, MUTED)


framed("Structure", 48, 184, 3 * FW + 2 * GAP, 578, structure)
text("structure-rule", 48, 794,
     "Guide explains the Task family. Task holds this Block's work. A View reads the owning records; "
     "it does not allocate a Run. P-B-E-R are lifecycle commands; concrete work keeps its native Run identity.", 17, MUTED)
text("p2-title", 48, 862, "2 · The working Views, using the Paper / Page / Insight Studio drawing grammar", 28)
Y = 918


def question_card(key, x, y, number, name, question, hypothesis, criterion,
                  work, report_state, answer, evidence, boundary, next_action):
    # Paper's stacked Question cards use Insight's three-column reading order.
    # Keep each Report in the right column of its own Question.
    w, h = FW - 48, QUESTION_HEIGHT
    lx, wx, rx = x + 20, x + 370, x + 720

    def paragraph(id_, xx, yy, value, width, size=16, color=INK):
        wrapped = "\n".join(textwrap.fill(part, width=int(width / (size * 0.6)))
                            for part in value.split("\n"))
        text(id_, xx, yy, wrapped, size, color)
        return yy + len(wrapped.split("\n")) * size * 1.25

    def divider(id_, xx):
        e = base(id_, "line", xx, y + 120, 0, h - 140, stroke=RULE, rounded=False)
        e.update(points=[[0, 0], [0, h - 140]], lastCommittedPoint=None,
                 startBinding=None, endBinding=None, startArrowhead=None, endArrowhead=None)
        E.append(e)

    rect(key + "-card", x, y, w, h)
    text(key + "-chevron", x + 16, y + 17, "▾", 21, MUTED)
    text(key + "-question", x + 44, y + 17, f"Question {number} · {name}", 21)
    text(key + "-sentence", x + 44, y + 48, question, 17)
    line(key + "-header-rule", x + 16, y + 78, w - 32)
    text(key + "-logic-label", lx, y + 91, "Logic", 19)
    text(key + "-work-label", wx, y + 91, "Work", 19)
    text(key + "-report-label", rx, y + 91, "Report", 19)
    divider(key + "-logic-work-rule", wx - 16)
    divider(key + "-work-report-rule", rx - 16)
    text(key + "-hypothesis-label", lx, y + 128, f"Hypothesis {number}a", 15, BLUE)
    logic_y = paragraph(key + "-hypothesis", lx, y + 155, hypothesis, 310)
    text(key + "-acceptance-label", lx, logic_y + 24, "Acceptance", 15, BLUE)
    paragraph(key + "-acceptance", lx, logic_y + 51, criterion, 310)
    work_y = y + 138
    for i, (label, name, explanation, counts) in enumerate(work):
        text(f"{key}-work-chevron-{i}", wx, work_y, "›", 17, MUTED)
        pill_width = len(label) * 8 + 16
        button(f"{key}-work-type-{i}", wx + 20, work_y, pill_width, 22, label, sel=True, size=13)
        name_y = paragraph(f"{key}-work-name-{i}", wx + 28 + pill_width, work_y,
                           name, 282 - pill_width, 16)
        work_y = paragraph(f"{key}-work-explanation-{i}", wx + 20, max(work_y + 29, name_y + 5),
                           explanation, 292, 15)
        work_y = paragraph(f"{key}-work-counts-{i}", wx + 20, work_y + 7, counts, 292, 13, MUTED) + 24
    paragraph(key + "-work-expand", wx, y + 400,
              "Expand: Block → Job → Task → Run\nOpen a Run to read its Result.", 310, 13, MUTED)
    text(key + "-report-state", rx, y + 124, report_state, 15, BLUE)
    report_y = y + 157
    for suffix, value, color in [
        ("answer", "Answer · " + answer, INK),
        ("evidence", "Evidence · " + evidence, BLUE),
        ("boundary", boundary, MUTED),
        ("next", "Next · " + next_action, BLUE),
    ]:
        report_y = paragraph(key + "-" + suffix, rx, report_y, value, 388, 15, color) + 12
    button(key + "-report-open", rx, y + h - 48, 198, 30, "Open full report ↗", size=15)


def task_view(x, y):
    shell("task", x, y, "Task Space · Task", "Task", TASK_VIEWS, 0,
          "b11_method_comparison · Questions, work and their reports · illustrative contents",
          height=TASK_HEIGHT)
    text("task-intro", x + 24, y + 239,
         "Each Question · Logic | Work | Report · three columns side by side", 17, MUTED)
    cards = [
        (1, "Comparable conditions",
         "Can we compare both methods using the same data and evaluation rules?",
         "Fair comparison: use identical inputs and rules.",
         "Data version, split and metric are recorded.",
         [("Data", "Source audit", "Which records can both methods use?", "1 task · 1 run"),
          ("Data", "Comparison protocol", "Can both methods follow the same rules?", "also for Q02 · 1 task · 1 run")],
         "Answered",
         "Both methods use the same recorded data split and evaluation protocol.",
         "j01 / t01 / r01 input checks ↗ · j01 / t02 protocol page ↗",
         "Boundary · This answer applies to the recorded data version, split and metric.",
         "Use this protocol in Question 2."),
        (2, "Method improvement",
         "Does the new method improve the metric, and is the improvement stable?",
         "Improvement: the gain survives repeated trials.",
         "Complete evaluation and uncertainty analysis.",
         [("Evaluation", "Metric comparison", "Does the metric improve?", "1 task · 4 runs"),
          ("Analysis", "Repeated trials", "Is the improvement stable?", "1 task · 0 runs")],
         "Partial · evidence missing",
         "Completed evaluations suggest a gain; stable improvement is still unconfirmed.",
         "j02 / t01 / r01–r03 metrics ↗ · evaluation page reading ↗",
         "Gap · r04 failed; the repeated-trial analysis has not run.",
         "Inspect r04 → recover evaluation → run analysis → update this Report."),
        (3, "Cost and usefulness",
         "Is the improvement worth the added time and compute cost?",
         "Useful gain: the improvement justifies its cost.",
         "Compare runtime and resources with the baseline.",
         [("Benchmark", "Cost comparison", "What does the method cost?", "1 task · 0 runs"),
          ("Synthesis", "Trade-off review", "Is the trade-off acceptable?", "1 task · 0 runs")],
         "Open · awaiting evidence",
         "No conclusion yet; benefit and cost evidence are both needed.",
         "Cost benchmark pending · Question 2 Report is still partial",
         "Gap · No cost measurements yet; the acceptable trade-off must be defined.",
         "Define the cost comparison plan and the acceptance threshold."),
    ]
    for i, args in enumerate(cards):
        question_card(f"task-question-{i + 1}", x + 24, y + 278 + i * (QUESTION_HEIGHT + 18), *args)
    text("task-footer", x + 24, y + TASK_HEIGHT - 32,
         "Report gaps lead back to Work or Logic. Open a Report for its full answer and evidence; copy context to the session.",
         15, MUTED)


framed("Task", X[0], Y, FW, TASK_HEIGHT, task_view)


def studio(x, y):
    shell("studio", x, y, "Task Space · Roadmap Studio", "Task", TASK_VIEWS, 1,
          "b11_method_comparison · Draw freely; open or close each drawing independently")
    cx, cy, cw = x + 24, y + 240, FW - 48
    # Each header controls only its own canvas. Several drawings may be open.
    # Drawing names and contents are freeform; this is an illustrative sketch.
    rect("studio-drawing-1", cx, cy, cw, 360)
    text("studio-drawing-1-title", cx + 18, cy + 18, "▾ Drawing 1", 22)
    button("studio-fullscreen", cx + 914, cy + 12, 196, 32, "Open full screen ↗", size=15)
    line("studio-drawing-1-rule", cx + 12, cy + 52, cw - 24)
    rect("studio-canvas", cx + 12, cy + 64, cw - 24, 282, RULE)
    text("studio-excalidraw", cx + 28, cy + 78, "Excalidraw", 17, MUTED)
    text("studio-tools", cx + 326, cy + 80,
         "Select    Rectangle    Arrow    Draw    Text", 15, MUTED)
    line("studio-toolbar-rule", cx + 12, cy + 110, cw - 24)
    rect("studio-idea", cx + 382, cy + 142, 364, 48)
    text("studio-idea-label", cx + 412, cy + 155, "What could we try?", 22)
    rect("studio-option-a", cx + 174, cy + 248, 274, 48)
    text("studio-option-a-label", cx + 213, cy + 263, "Try a smaller example?", 17)
    rect("studio-option-b", cx + 684, cy + 248, 274, 48)
    text("studio-option-b-label", cx + 723, cy + 263, "Try another approach?", 17)
    arrow("studio-branch-a", cx + 500, cy + 196, [[0, 0], [-180, 46]], MUTED)
    arrow("studio-branch-b", cx + 628, cy + 196, [[0, 0], [180, 46]], MUTED)
    text("studio-sketch-note", cx + 822, cy + 171, "What else?", 20, BLUE)
    for i, yy in [(2, y + 618), (3, y + 688)]:
        rect(f"studio-drawing-{i}", cx, yy, cw, 52)
        text(f"studio-drawing-{i}-title", cx + 18, yy + 14, f"▸ Drawing {i}", 22)
    button("studio-add", cx, y + 762, 200, 36, "+ Add drawing", size=16)


framed("Studio", X[1], Y, FW, FH, studio)


def related_paper(x, y):
    shell("related", x, y, "Task Space · Related Paper", "Task", TASK_VIEWS, 2,
          "b11_method_comparison · External papers, methods, repositories and reference material")
    text("related-intro", x + 24, y + 244,
         "One resource per card: what it contributes and which Question it helps answer.", 18)
    entries = [
        ("Paper · Evaluation protocol", "Source · Paper title / authors / year / original link",
         "For Question 1 · Learn how prior work controls the comparison.",
         "Use here · Data split, metric definitions and baseline settings."),
        ("Paper · Stability analysis", "Source · Paper title / authors / year / original link",
         "For Question 2 · Learn how prior work checks repeated trials.",
         "Use here · Uncertainty estimates and evidence required for the answer."),
        ("Repository / documentation · Cost benchmark", "Source · Repository / version / original link",
         "For Question 3 · Reuse a reference method for measuring cost.",
         "Use here · Runtime, resource usage and reproducible configurations."),
    ]
    for i, (title, source, question, use) in enumerate(entries):
        yy = y + 290 + i * 146
        rect(f"related-card-{i}", x + 24, yy, FW - 48, 128)
        text(f"related-title-{i}", x + 42, yy + 14, "▸ " + title, 20)
        text(f"related-source-{i}", x + 62, yy + 45, source, 15, MUTED)
        text(f"related-question-{i}", x + 62, yy + 72, question, 16, BLUE)
        text(f"related-use-{i}", x + 62, yy + 99, use, 15)
        button(f"related-open-{i}", x + 930, yy + 12, 204, 32, "Read / Open source ↗", size=14)
    button("related-add", x + 24, y + 744, 226, 38, "+ Add resource", size=16)
    text("related-footer", x + 278, y + 752,
         "Illustrative placeholders · expand a paper card to read its PDF and notes.", 15, MUTED)


framed("RelatedPaper", X[2], Y, FW, FH, related_paper)


def progress(x, y):
    shell("progress", x, y, "Task Space · Progress", "Task", TASK_VIEWS, 3,
          "b11_method_comparison · Report status, work progress and next actions · illustrative contents",
          height=PROGRESS_HEIGHT)
    text("progress-summary", x + 24, y + 244,
         "Report · 1 answered / 1 partial / 1 open     Work · 1 failed Run", 20)
    rows = [
        ("Question 1 · Comparable conditions", "Report · Answered ↗",
         "The comparison uses the same recorded inputs and evaluation rules.",
         "Work · j01 / t01 + t02 · Input checks and protocol are recorded.",
         "Next · Use the protocol in Question 2."),
        ("Question 2 · Method improvement", "Report · Partial ↗",
         "Early gain; stable improvement is still unconfirmed.",
         "Work · j02 / t01 · 3 of 4 Runs complete · r04 failed · Log / Results ↗",
         "Next · Recover evaluation → run analysis → update Report."),
        ("Question 3 · Cost and usefulness", "Report · Open ↗",
         "No conclusion yet; benefit and cost evidence are needed.",
         "Work · j03 / t01 + t02 · Planned; no Run allocated yet.",
         "Next · Define the cost benchmark and acceptance threshold."),
    ]
    for i, (title, report_state, answer, work, next_action) in enumerate(rows):
        yy = y + 290 + i * 164
        rect(f"progress-card-{i}", x + 24, yy, FW - 48, 146)
        text(f"progress-question-{i}", x + 42, yy + 16, title, 20)
        text(f"progress-report-{i}", x + 824, yy + 19, report_state, 17, BLUE)
        text(f"progress-answer-{i}", x + 42, yy + 50, answer, 17)
        text(f"progress-work-{i}", x + 42, yy + 81, work, 16, MUTED)
        text(f"progress-next-{i}", x + 42, yy + 114, next_action, 16, BLUE)
    button("progress-copy", x + 24, y + 806, 248, 38, "Copy next-step context", size=16)
    text("progress-footer", x + 300, y + 814,
         "New Results flag dependent Reports for review.", 16, MUTED)
    text("progress-reading-note", x + 24, y + 861,
         "Report status comes from the current reading and its evidence. Run completion is tracked alongside it.", 15, MUTED)


framed("Progress", X[1], Y + FH + 40, FW, PROGRESS_HEIGHT, progress)


def guide(x, y):
    shell("guide", x, y, "Guide Space · Skill set", "Guide",
          GUIDE_VIEWS, 0,
          "Task family · How its skills cooperate · the same explanation across Task Blocks")
    lx, cy, cw = x + 24, y + 244, FW - 48
    rect("guide-drawing-row", lx, cy, cw, 56)
    text("guide-drawing-title", lx + 18, cy + 17, "▸ Skill map", 20)
    text("guide-drawing-purpose", lx + 248, cy + 19,
         "Skills, responsibilities and native owners · expand drawing", 17, MUTED)
    text("guide-skills-title", lx, cy + 80, "Skills and responsibilities", 22)
    skill_rows = [
        ("haipipe-task", "Plan → Build → Execute → Report\nTask identity, Tickets, Results and readiness."),
        ("haipipe-page", "Readable interpretation and evidence binding;\naccepted text, CHECK and release."),
        ("haipipe-workbench-task", "Open this Block's working surface;\ninspect Questions, work, results and progress."),
    ]
    for i, (name, meaning) in enumerate(skill_rows):
        yy = cy + 122 + i * 118
        rect(f"guide-skill-card-{i}", lx, yy, cw, 104, RULE, PANEL)
        text(f"guide-skill-{i}", lx + 18, yy + 13, name, 17, GREEN, mono=True)
        text(f"guide-skill-role-{i}", lx + 18, yy + 42, meaning, 16)
    text("guide-footer", x + 24, y + 754,
         "Guide explains the family. This Block's questions, plans, sketches and progress live in Task Space.", 16, MUTED)


framed("Guide", X[2], Y + FH + 40, FW, FH, guide)
text("p3-title", 48, Y + FH + 40 + PROGRESS_HEIGHT + 80, "3 · What the views read, and how a session continues the work", 28)
PY = Y + FH + 40 + PROGRESS_HEIGHT + 136
for i, (heading, lines) in enumerate([
    ("Logic → Work → Report", [
        "The Block declares its Questions and their logic items.",
        "Question cards stack vertically; Logic | Work | Report sit side by side.",
        "Work keeps its Task / Run / Result references when execution is involved.",
        "A Question can use several Tasks; shared work can serve several Questions.",
        "Report: answer, exact evidence, limits and next action in the same card.",
        "board.md binds Questions to native Tasks and Block-owned Report Pages."]),
    ("The session and Workbench", [
        "Read one Question's Logic, Work and current Report.",
        "Copy its goal, evidence, blockers and next action into the session.",
        "The session uses the owning Task / Page workflow to change records.",
        "A Question may have reasoning and a Report before any Job / Task / Run.",
        "Roadmap Studio: expand any drawing row to use its freeform canvas."]),
    ("Existing source records", [
        "board.md                       Scope, Questions and related resources",
        "workflow/plan.yaml             Planned Run Specs",
        "runs/ + runtime.yaml           Allocated executions and receipts",
        "workflow/report.yaml           Declared execution report",
        "reports/qNN_topic/             Ordinary Page: answer and evidence",
        "studio/*.excalidraw             Freeform drawings beside reports/"]),
]):
    xx = X[i]
    rect(f"source-box-{i}", xx, PY, FW, 368)
    text(f"source-title-{i}", xx + 24, PY + 22, heading, 25)
    text(f"source-body-{i}", xx + 24, PY + 78, "\n\n".join(lines), 16,
         BLUE if i == 2 else INK, mono=i == 2)
text("footer", 48, PY + 410,
     "Design proposal · illustrative records · styles and drawing primitives follow Paper Studio. "
     "Generated by studio/task-workbench-design.py; edit the generator, then regenerate.", 16, MUTED)

OUT.write_text(json.dumps({"type": "excalidraw", "version": 2,
                           "source": "haipipe-task-workbench-design",
                           "elements": E, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
                           "files": {}}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(E), "elements →", OUT)
