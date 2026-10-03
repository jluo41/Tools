"""Draw the Design family in one drawing, Guide's RoadMap Draw (JL 261002: "one draw contains all
the skills, Methods, Workbench, and Folder"; "I want things like this",
design-workbench-design.excalidraw; "don't follow the template in the shared"). One canvas:
the skills, the method, then the workbench (the board level, then the page level with its
Spaces side by side, each with its Runs panel), what moved, the folders and files, and one
design followed run by run. The content is board B00's, as of 2026-10-02; states are
illustrative, not live.

    python3 plugins/haipipe-toolkit/servers/workbench-design/studio/design-workbench-ui.py
"""

import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "design-workbench-ui.excalidraw"
INK, MUTED, RULE, PANEL = "#1e1e1e", "#495057", "#ced4da", "#f8f9fa"
BLUE, BLUE_BG, GREEN, GREEN_BG = "#1864ab", "#e7f5ff", "#2b8a3e", "#ebfbee"
PURPLE, ORANGE, RED, RED_BG = "#6741d9", "#e8590c", "#c92a2a", "#fff5f5"
RNG = random.Random(261002)
E = []


def base(key, kind, x, y, w, h, stroke=INK, bg="transparent", dashed=False):
    item = {"id": key, "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
            "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": 2,
            "strokeStyle": "dashed" if dashed else "solid", "roughness": 0, "opacity": 100,
            "groupIds": [], "frameId": None, "roundness": {"type": 3} if kind == "rectangle" else None,
            "seed": RNG.randint(1, 2**31 - 1), "version": 1, "versionNonce": RNG.randint(1, 2**31 - 1),
            "isDeleted": False, "boundElements": [], "updated": 0, "link": None, "locked": False}
    E.append(item)
    return item


def T(key, x, y, value, size=16, color=INK, mono=False):
    lines = value.split("\n")
    item = base(key, "text", x, y, max(len(l) for l in lines) * size * (0.6 if mono else 0.56),
                len(lines) * size * 1.25, color)
    item.update(text=value, originalText=value, fontSize=size, fontFamily=3 if mono else 8,
                textAlign="left", verticalAlign="top", containerId=None, autoResize=True, lineHeight=1.25)
    return item


def R(key, x, y, w, h, stroke=INK, bg="transparent", dashed=False):
    return base(key, "rectangle", x, y, w, h, stroke, bg, dashed)


def B(key, x, y, w, h, label, selected=False, size=16, dashed=False, color=None):
    color = color or (BLUE if selected else INK)
    box = R(key, x, y, w, h, color, BLUE_BG if selected else "transparent", dashed)
    label_item = T(key + "-text", x + 6, y + (h - size * 1.25) / 2, label, size, color)
    label_item.update(containerId=key, textAlign="center", verticalAlign="middle", width=w - 12)
    box["boundElements"] = [{"id": label_item["id"], "type": "text"}]


def L(key, x, y, w, color=RULE, dx=None, dy=0, arrowhead=False):
    item = base(key, "arrow" if arrowhead else "line", x, y, abs(dx if dx is not None else w), abs(dy), color)
    item.update(points=[[0, 0], [dx if dx is not None else w, dy]], lastCommittedPoint=None,
                startBinding=None, endBinding=None, startArrowhead=None,
                endArrowhead="arrow" if arrowhead else None)


def tabs(key, x, y, labels, selected, size=16, h=36, gap=12, pad=34):
    for i, label in enumerate(labels):
        w = len(label) * size * 0.56 + pad
        B(f"{key}-{i}", x, y, w, h, label, label == selected, size)
        x += w + gap


def chips(key, x, y, items, size=13):
    for i, (label, color) in enumerate(items):
        w = len(label) * size * 0.56 + 20
        R(f"{key}-{i}", x, y, w, 24, color, "#ffffff")
        T(f"{key}-{i}-t", x + 10, y + 4, label, size, color)
        x += w + 8
    return x


def space(key, x, y, w, h, title, note=None):
    R(key, x, y, w, h)
    T(key + "-title", x + 24, y + 20, title, 28)
    if note:
        T(key + "-note", x + 24 + len(title) * 28 * 0.56 + 16, y + 32, note, 15, MUTED)
    L(key + "-rule", x + 24, y + 62, w - 48)


def runs(key, x, y, w, title, scope, types, selected, detail, saved, h=300):
    """A Space's Runs panel, as in the reference: run types on the left, the picked run on the right."""
    R(key, x, y, w, h, INK, PANEL)
    T(key + "-h", x + 18, y + 14, title, 21)
    T(key + "-s", x + 18, y + 46, "Scope  " + scope, 15, MUTED)
    by = y + 80
    for i, name in enumerate(types):
        B(f"{key}-t{i}", x + 18, by, 180, 40, name, name == selected, 14, name.startswith("+"))
        by += 50
    dx, dw = x + 212, w - 230
    R(key + "-d", dx, y + 80, dw, h - 130, INK, "#ffffff")
    yy = y + 92
    for i, (line, size, color) in enumerate(detail):
        T(f"{key}-d{i}", dx + 14, yy, line, size, color)
        yy += size * 1.25 * (line.count("\n") + 1) + 6
    T(key + "-saved", x + 18, y + h - 34, "Saved in  " + saved, 15, MUTED)


def lines_block(key, x, y, rows, size=17, color=INK):
    if rows:
        T(key, x, y, "\n".join(rows), size, color)


# ---------------------------------------------------------------- title --
T("title", 48, 24, "Design Workbench · skills, method, workbench and folders", 34)
T("subtitle", 48, 74, "The skills, the method, the workbench and the folders of the Design family in one drawing: "
  "Guide's RoadMap Draw.", 18, MUTED)
FIRST = len(E)          # everything after the title moves down to make room for skills and method

# ------------------------------------------------------------- board bar --
R("boardbar", 48, 118, 1864, 72, INK, PANEL)
T("boardbar-1", 68, 128, "Board  B00 · DesignBoard R2Messages · SMS prescription-review messages", 18)
T("boardbar-2", 68, 158, "6 design tasks   ·   70 designs   ·   60 ready   ·   10 waiting for release   ·   records check 136",
  16, MUTED)
B("boardbar-check", 1290, 130, 180, 48, "Records check · 136", size=16)
B("boardbar-csv", 1484, 130, 180, 48, "↓ Board csv", size=16)
B("boardbar-all", 1678, 130, 214, 48, "All runs (Board)", True, 16)

# Guide ------------------------------------------------------------------
space("guide", 48, 214, 920, 820, "Guide", "how the Design family works · the same on every board")
tabs("guide-views", 72, 292, ["Description", "Method", "RoadMap Draw", "Related Paper"], "Method")
T("guide-reads", 72, 346, "Reads  ref/design-theory.md  ·  ref/design-methods.md  ·  ref/methods/  ·  ref/design-papers.md", 16, MUTED)
tabs("guide-sub", 72, 380, ["Design theory", "Design methods", "Methods studio"], "Design methods", size=15, h=32, pad=28)
R("guide-box", 72, 428, 872, 452)
T("guide-box-h", 90, 442, "Design methods · 13 cards in 6 families", 19)
T("guide-box-s", 90, 472, "▸ / ▾ opens a card; a cited paper opens its card in Papers, PDF and all.", 14, MUTED)
fams = [("Requirements only · abduction-2", "By goal · By principle"),
        ("With external insights · abduction-1", "By theory · By implementation"),
        ("With internal insights · induction, then abduction-1", "By insight · By precedent · By revising · By tailoring"),
        ("With both insights · two hows that must agree", "By theory and insight"),
        ("Making internal insights now · small loops", "By user test · By co-design (future)"),
        ("Making internal insights next · the Exp does it", "By exploring · By slots")]
for i, (fam, methods) in enumerate(fams):
    T(f"guide-fam{i}", 90, 500 + i * 26, "▸ " + fam, 15, BLUE)
    T(f"guide-met{i}", 520, 500 + i * 26, methods, 15, INK)
R("guide-card", 84, 664, 848, 196, BLUE, BLUE_BG)
T("guide-card-h", 100, 676, "▾ 5  By insight", 17, BLUE)
T("guide-card-st", 760, 678, "no study tests it yet", 14, RED)
T("guide-card-m", 100, 704, "Make each part of the design follow from a signed insight.", 15)
T("guide-card-rl", 100, 734, "reads", 13, MUTED)
chips("guide-card-in", 150, 731, [("design requirements", BLUE), ("internal insights: signed rows", GREEN)])
T("guide-card-ret", 560, 734, "→  returns one cited decision per part", 13, MUTED)
T("guide-card-r", 100, 764, "reasoning   abduction-1 on our own induction: requirements + signed insights → a design", 13, MUTED)
T("guide-card-t", 100, 788, "tested      in Evaluate  T1 each cited row says it   ·   in the Exp  T4 against the control", 13, MUTED)
T("guide-card-p", 100, 812, "papers      Sackett 1996 PDF · MacLean 1991        What the literature says  |  Applied to AI", 13, MUTED)
T("guide-card-f", 100, 836, "family      With internal insights", 13, MUTED)
T("guide-noruns", 72, 892, "Guide reads; it never runs, so it has no Runs panel.", 15, MUTED)
lines_block("guide-map", 72, 922, ["Description    →  what the Design workbench does, its Spaces",
                                   "Method          →  Design theory · Design methods · Methods studio",
                                   "RoadMap Draw  →  this drawing: skills, method, workbench, folders",
                                   "Related Paper  →  the papers behind the methods, PDF and all"], 16)

# Design Tasks ----------------------------------------------------------
space("tasks", 992, 214, 920, 820, "Design Tasks Space")
tabs("tasks-views", 1016, 292, ["Tasks", "Compare"], "Tasks")
T("tasks-reads", 1016, 346, "Reads  0-BR-brief/BR00-brief.md  ·  each 2-Design/*/ register  ·  its Verify results", 16, MUTED)
R("tasks-box", 1016, 380, 872, 330)
T("tasks-box-h", 1034, 394, "Design tasks · 6 · one row per Design page", 19)
heads = [("design task", 0), ("method", 290), ("designs", 470), ("elements", 560), ("state", 670)]
for h, dx in heads:
    T(f"tasks-h{dx}", 1034 + dx, 432, h, 13, MUTED)
L("tasks-hr", 1034, 454, 836)
rows = [("All patients", "mixed · 4", "20", "3 of 6", "6 ready · 14 to release"),
        ("Young male, 35 or under", "mixed · 3", "10", "·", "10 ready"),
        ("Young female, 35 or under", "mixed · 3", "10", "·", "10 ready"),
        ("Older patients, 55 and over", "mixed · 3", "10", "·", "10 ready"),
        ("Midlife male, 40 to 50", "mixed · 3", "10", "·", "10 ready"),
        ("Midlife female, 40 to 50", "mixed · 3", "10", "·", "10 ready")]
for i, row in enumerate(rows):
    for (h, dx), v in zip(heads, row):
        T(f"tasks-r{i}-{dx}", 1034 + dx, 464 + i * 28, v, 15,
          BLUE if h == "design task" else (ORANGE if v.startswith("mixed") else (GREEN if "ready" in v else INK)))
R("tasks-pilot", 1028, 640, 848, 56, MUTED, "transparent", dashed=True)
T("tasks-pilot-t", 1042, 648, "Design-07 to 10 · the methods pilot · one method each: By goal · By theory ·\n"
  "By insight · By theory and insight · N = 3 each   (proposed)", 14, MUTED)
runs("tasks-runs", 1016, 724, 872, "Runs  >  Design Tasks", "Board > Space",
     ["Add design tasks · 0", "Set shared rules · 0", "+ New Run"], "Add design tasks · 0",
     [("Add design tasks", 17, INK), ("no runs yet", 14, MUTED),
      ("Skill  haipipe-design-brief", 14, MUTED),
      ("Writes the Brief's task lines and opens\none Design Folder per new line.", 14, MUTED)],
     "0-BR-brief/  ·  2-Design/Design-NN-…/", h=300)
L("board-link", 968, 600, 24)

# ------------------------------------------------------------- page bar --
PY = 1100
T("page-h", 48, PY - 44, "Page level · one Design page = one design task + one method → N designs", 24)
R("pagebar", 48, PY, 1864, 72, INK, PANEL)
T("pagebar-1", 68, PY + 10, "Folder  Design-01  ·  Prescription review SMS for all patients  ·  ↑ Board B00", 18)
T("pagebar-2", 68, PY + 40, "Goal  20 registered  ·  6 ready  ·  14 not commissioned  ·  elements 3 of 6 explored  ·  "
  "methods mixed (4): one per page from now", 16, MUTED)
B("pagebar-guide", 1290, PY + 12, 180, 48, "Guide", size=16)
B("pagebar-check", 1484, PY + 12, 180, 48, "Records check ✓", size=16)
B("pagebar-all", 1678, PY + 12, 214, 48, "All runs (Folder)", True, 16)

SY = PY + 96
# Design Goal Space -------------------------------------------------------
space("goal", 48, SY, 600, 1010, "Design Goal Space")
tabs("goal-views", 72, SY + 78, ["Aim", "Venue", "Rules", "Resources", "Leave out"], "Resources", size=15, gap=8, pad=24)
T("goal-reads", 72, SY + 132, "Reads  design-goal.md beside board.md\n·  a Task · Design-01 section overrides a line", 15, MUTED)
R("goal-box", 72, SY + 186, 552, 392)
T("goal-box-h", 90, SY + 200, "Resources · what the designer may draw on", 19)
T("goal-st-k", 90, SY + 238, "Starting text", 15)
R("goal-sms", 90, SY + 262, 516, 74, RULE, BLUE_BG)
T("goal-sms-t", 102, SY + 270, "Hi, it's Dr. {NAME}'s office. New prescription\ndetails require your review: {LINK}\nReply STOP to opt-out", 14)
T("goal-el-k", 90, SY + 350, "Elements", 15)
chips("goal-el", 90, SY + 374, [(s, ORANGE) for s in ("greeting", "sender", "news", "ask", "link", "opt-out")])
T("goal-me-k", 90, SY + 414, "Method", 15)
T("goal-me-v", 190, SY + 414, "one per page (proposed) · today 4 mixed", 15, ORANGE)
T("goal-pr-k", 90, SY + 444, "Prior designs", 15)
T("goal-pr-v", 230, SY + 444, "13 round-1 variants; salience is the start", 15, MUTED)
T("goal-th-k", 90, SY + 474, "Message theories", 15)
T("goal-th-v", 258, SY + 474, "design-theory.md · external insights", 15, MUTED)
T("goal-note", 90, SY + 512, "Elements names the starting text's parts; every new\ndesign returns its element record under these names.", 14, MUTED)
runs("goal-runs", 72, SY + 596, 552, "Runs  >  Design Goal", "Folder > Space > View",
     ["Frame the aim", "Set the rules", "Gather resources", "+ New Run"], "Gather resources",
     [("Gather resources", 16, INK), ("no runs yet", 13, MUTED), ("Skill  haipipe-design-goal", 13, MUTED),
      ("Fills the lines the Space marks\n\"Not specified\"; a person signs\nthe aim and the rules.", 13, MUTED)],
     "design-goal.md", h=300)
lines_block("goal-map", 72, SY + 920, ["Resources view  →  starting text, elements, method",
                                       "Rules view        →  what every design keeps"], 16)

# Design Space --------------------------------------------------------------
space("design", 680, SY, 600, 1010, "Design Space")
tabs("design-views", 704, SY + 78, ["Designs"], "Designs", size=15, pad=30)
T("design-reads", 704, SY + 132, "Reads  draft/…-design-items.md  ·  results/<run>/\n·  elements.yaml, when a run wrote one", 15, MUTED)
R("design-box", 704, SY + 186, 552, 392)
T("design-mx-h", 722, SY + 198, "▾ Design elements · 6 designs × 6 slots · 3 explored", 15)
mx = ("design    sender      news        added\n"
      "Design 1  ·           ·           ★ from your visit\n"
      "Design 2  ·           ★           ★ One more step\n"
      "Design 3  removed     ·           ·\n"
      "Design 4  ★ doctor    ★           ·\n"
      "changed   2 of 6      3 of 6      4 of 6")
T("design-mx", 722, SY + 224, mx, 12, MUTED, mono=True)
T("design-l1", 722, SY + 318, "▸ Design 2 ✅ · Salience framed as a finishing step", 14)
T("design-l2", 722, SY + 340, "▸ Design 3 ✅ · No sender named at all", 14)
R("design-open", 712, SY + 366, 536, 200, BLUE, BLUE_BG)
T("design-open-h", 726, SY + 376, "▾ Design 1 ✅ · Salience that names the visit", 15, BLUE)
R("design-sms", 726, SY + 404, 200, 112, RULE, "#ffffff")
T("design-sms-t", 734, SY + 410, "Hi, it's Dr. {NAME}'s\noffice. New prescription\ndetails from your visit\nrequire your review:\n{LINK} Reply STOP to\nopt-out", 12)
T("design-rec", 938, SY + 404, "Rationale · element by element\nsender      requirements · reasoned\nnews        internal W1 · reasoned\n"
  "added       internal W3 · reasoned\n\nEvaluation · what remains open\nEvaluate  T0 ✓ 6 of 6 · T2 2 notes\nExp         not tested yet", 12, MUTED)
T("design-open-f", 726, SY + 528, "ready for Delivery · run-design-generate-0918-design-1 · verified", 12, BLUE)
runs("design-runs", 704, SY + 596, 552, "Runs  >  Design  >  Design 1", "Folder > Space > Design",
     ["Commission · 1", "Generate · 1", "Verify · 1", "+ New Run"], "Generate · 1",
     [("run-design-generate-0918-design-1", 14, INK), ("pass · self-check 6 of 6", 13, MUTED),
      ("Prompt                                        Copy", 13, INK),
      ("Generate Design 1 from its frozen\nconfig; write the text and, when\nasked, its element record.", 12, MUTED),
      ("✓ 113 characters  ✓ 6 of 6 rules", 12, GREEN)],
     "runs/run-design-*.yaml  ·  results/run-design-*/", h=300)
lines_block("design-map", 704, SY + 920, ["Element matrix  →  what each design changed",
                                          "A card             →  Commission · Generate · Verify"], 16)

# Delivery Space -------------------------------------------------------------
space("deliv", 1312, SY, 600, 1010, "Delivery Space")
tabs("deliv-views", 1336, SY + 78, ["Ready designs", "csv"], "Ready designs", size=15, pad=30)
T("deliv-reads", 1336, SY + 132, "Reads  each design whose independent Verify\npassed (read only)", 15, MUTED)
R("deliv-box", 1336, SY + 186, 552, 392)
T("deliv-box-h", 1354, SY + 200, "Ready designs · 6 · word for word", 19)
for i, (n, t) in enumerate([("Design 1", "Hi, it's Dr. {NAME}'s office. New prescription\ndetails from your visit require your review: …"),
                            ("Design 2", "Hi, it's Dr. {NAME}'s office. One more step for\nyour new prescription. The details require …"),
                            ("Design 3", "Hi, new prescription details require your review:\n{LINK} Reply STOP to opt-out"),
                            ("Design 4", "Hi, Dr. {NAME} wrote you a new prescription.\nThe details require your review: …")]):
    T(f"deliv-n{i}", 1354, SY + 238 + i * 70, n, 15, BLUE)
    T(f"deliv-t{i}", 1446, SY + 238 + i * 70, t, 13, INK)
T("deliv-csv", 1354, SY + 530, "↓ Download all designs · 6 · csv          Nothing is edited here.", 14, BLUE)
runs("deliv-runs", 1336, SY + 596, 552, "Runs  >  Delivery", "Folder > Space",
     ["Export csv · 0", "+ New Run"], "Export csv · 0",
     [("Export csv", 16, INK), ("no runs yet", 13, MUTED),
      ("Writes every ready design of this\nfolder as one csv, word for word.", 13, MUTED)],
     "delivery/", h=300)
lines_block("deliv-map", 1336, SY + 920, ["Ready designs  →  the patient's words",
                                          "csv                 →  the same designs, one file"], 16)
L("page-link-1", 648, SY + 380, 32)
L("page-link-2", 1280, SY + 380, 32)

# ------------------------------------------------------- takeaways, what moved --
KY = SY + 1040
lines_block("takeaways", 48, KY, [
    "1. Guide explains the family: skills, methods, the UI, the folders. It reads and never runs.",
    "2. Guide has four views: Description · Method · RoadMap Draw · Related Paper.",
    "3. Each working Space keeps its Runs panel: pick a run to see its prompt, process and results.",
    "4. A Design page is one design task and one method; it returns N designs.",
    "5. The element matrix shows what each design changed, and where each element came from."], 18)
R("moved", 1000, KY - 8, 912, 176)
T("moved-h", 1020, KY + 4, "What moved", 21)
T("moved-b", 1020, KY + 40, "Theory of Design Space   →  Guide › Method (theory, methods, studio)\n"
  "its Papers view           →  Guide › Related Paper\n"
  "old space=theory links     →  forward to Guide (papers to Related Paper)\n"
  "Design Tasks, Design Goal, Design, Delivery  →  stay working Spaces", 15, MUTED)

# ------------------------------------------------------------ the files --
FY = KY + 230
T("files-h", 48, FY, "What the files look like", 30)
T("files-s", 48, FY + 46, "Guide reads the family's files in Tools; each working Space reads one part of the board.", 18, MUTED)
R("files-goal", 48, FY + 90, 930, 360)
T("files-goal-h", 68, FY + 108, "The Design Goal  ·  design-goal.md beside board.md", 21, BLUE)
T("files-goal-b", 68, FY + 148, "Resources\n---------\n\n"
  "Starting text: Hi, it's Dr. {NAME}'s office. New prescription details\n  require your review: Reply STOP to opt-out <- the round-1 winner\n"
  "Elements: greeting = \"Hi,\" · sender = \"it's Dr. {NAME}'s office.\" ·\n  news = \"New prescription details\" · ask = \"require your review:\" ·\n"
  "  link = \"{LINK}\" · opt-out = \"Reply STOP to opt-out\"\n"
  "Design theory: the board's message theories <- design-theory.md\n\n"
  "Task · Design-01-all-patients-prescription-review-sms\n"
  "Method: By insight   (proposed: one method per page)", 13, INK, mono=True)
R("files-folder", 1000, FY + 90, 912, 360)
T("files-folder-h", 1020, FY + 108, "The Design Folder", 21, GREEN)
T("files-folder-b", 1020, FY + 148, "Design-01-all-patients-prescription-review-sms/\n"
  "├── Design-01-….md                   Page Face\n"
  "├── draft/…-design-items.md          the register: goal, rules, evidence\n"
  "├── runs/run-design-<step>-<MMDD>-<design>.yaml   one record per run\n"
  "├── scripts/config/                  frozen goal and rules\n"
  "└── results/run-design-generate-0918-design-1/\n"
  "    ├── content/sms.txt              the design\n"
  "    ├── checks.yaml                  each rule, pass or fail\n"
  "    └── elements.yaml                each element: source, reasoned or intuitive\n\n"
  "Guide's files: Tools/…/haipipe-workbench-design/ref/\n"
  "  design-theory.md · design-methods.md · methods/ · design-papers.md · papers/", 13, INK, mono=True)

# ------------------------------------------------------ one design, run by run --
CY = FY + 500
T("chain-h", 48, CY, "One design, run by run", 30)
T("chain-s", 48, CY + 46, "Design 1 on Design-01: a person releases, an agent generates, a different agent verifies.", 18, MUTED)
cards = [("Commission", "run-design-commission-0918-design-1", "you · release",
          "froze the goal, the rules\nand the evidence files", "✓ release", INK, GREEN, "transparent"),
         ("Generate", "run-design-generate-0918-design-1", "agent · designer",
          "113 characters; element record\nwhen the item asks for it", "✓ pass (self) · 6 of 6", INK, MUTED, "transparent"),
         ("Verify", "run-design-verify-0918-design-1", "fresh agent · reviewer",
          "every rule on the exact draft;\nreview notes beside it", "✓ pass · 6 of 6", INK, GREEN, "transparent"),
         ("Delivery", "Design 1", "read only", "in the list, as the patient\nreads it", "ready ✓", BLUE, BLUE, BLUE_BG)]
cx = 48
for i, (name, run, who, what, verdict, color, vcolor, bg) in enumerate(cards):
    R(f"chain-{i}", cx, CY + 96, 420, 206, color, bg)
    T(f"chain-{i}-n", cx + 18, CY + 112, name, 22, color)
    T(f"chain-{i}-r", cx + 18, CY + 146, run, 14, MUTED)
    T(f"chain-{i}-w", cx + 18, CY + 172, who, 15, INK)
    T(f"chain-{i}-x", cx + 18, CY + 204, what, 13, MUTED)
    T(f"chain-{i}-v", cx + 18, CY + 262, verdict, 16, vcolor)
    if i < len(cards) - 1:
        L(f"chain-a{i}", cx + 420, CY + 199, 0, MUTED, dx=28, arrowhead=True)
    cx += 448
T("chain-note", 48, CY + 330, "A failed Verify becomes feedback on a new Generate; the old draft stays. "
  "A broken rule goes back to Generate, a weak reason back to Method: the Revise loop.", 15, MUTED)
T("footer", 48, CY + 380, "Design mockup: illustrative states from board B00 as of 2026-10-02, not live status.", 14, MUTED)

# ------------------------------------------------- skills and method, on top --
DY = 920
for item in E[FIRST:]:
    item["y"] += DY
SK = 124
T("skills-h", 48, SK, "The skills · who does what", 30)
T("skills-s", 48, SK + 46, "Five skills; each owns its files. A person signs the aim and the rules, and releases each "
  "Commission; agents do the rest.", 18, MUTED)
skills = [("haipipe-design", "the family door", "boards, design tasks and\nDesign pages", "routes a request to its owner"),
          ("haipipe-design-goal", "the design requirements", "design-goal.md: aim, venue,\nrules, resources, leave out",
           "a person signs the aim\nand the rules"),
          ("haipipe-design-workflow", "Commission · Generate · Verify", "runs/ and results/, the queue",
           "a person releases each\nCommission"),
          ("haipipe-design-unit", "one Generate or Verify", "content, checks.yaml,\nelements.yaml",
           "a designer agent; a different\nagent verifies"),
          ("haipipe-workbench-design", "the surfaces and the theory", "board and page Spaces; the\nmethods page, cards, papers",
           "reads; writes only through\nits own buttons")]
for i, (name, role, owns, who) in enumerate(skills):
    x = 48 + i * 377
    R(f"skill-{i}", x, SK + 92, 356, 196, BLUE if i == 0 else INK, BLUE_BG if i == 0 else "transparent")
    T(f"skill-{i}-n", x + 16, SK + 106, name, 17, BLUE)
    T(f"skill-{i}-r", x + 16, SK + 136, role, 16, INK)
    T(f"skill-{i}-o", x + 16, SK + 166, "owns  " + owns, 14, MUTED)
    T(f"skill-{i}-w", x + 16, SK + 226, who, 14, MUTED)
    if 1 <= i < 3:
        L(f"skill-a{i}", x + 356, SK + 190, 0, MUTED, dx=21, arrowhead=True)
T("skills-a-note", 48 + 377 + 30, SK + 298, "the goal freezes into each Commission  →  one run is one Generate or one Verify", 14, MUTED)

MY = SK + 340
T("method-h", 48, MY, "The method · three inputs, Design, Exp", 30)
T("method-s", 48, MY + 46, "Every design reads the requirements; its method decides which insights it may read. "
  "Thirteen methods in six families; Guide › Method has the full page.", 18, MUTED)
for i, (name, body, color, bg) in enumerate([
        ("Design requirements", "the Design Goal: aim, rules,\nstarting text and its elements", BLUE, BLUE_BG),
        ("Internal insights", "our own data, signed on an\nInsightBoard", GREEN, GREEN_BG),
        ("External insights", "the literature and theory, cited", PURPLE, "#f3f0ff")]):
    y = MY + 92 + i * 78
    R(f"in-{i}", 48, y, 330, 66, color, bg)
    T(f"in-{i}-n", 62, y + 8, name, 16, color)
    T(f"in-{i}-b", 62, y + 32, body, 13, MUTED)
    L(f"in-a{i}", 378, y + 33, 0, color, dx=60, dy=(MY + 92 + 78 + 33) - (y + 33), arrowhead=True)
R("m-design", 446, MY + 92, 1000, 222, INK, PANEL)
T("m-design-h", 466, MY + 104, "Design · abduction", 20)
for i, (name, note) in enumerate([("Method", "choose one per page"), ("Generate", "N designs + element records"),
                                  ("Evaluate", "T0 to T3: rules, fidelity,\ncritique, pretest"), ("Ready", "a person releases")]):
    x = 466 + i * 240
    B(f"m-step{i}", x, MY + 144, 210, 44, name, name in ("Method", "Generate"), 16)
    T(f"m-step{i}-n", x + 4, MY + 196, note, 13, MUTED)
    if i < 3:
        L(f"m-stepa{i}", x + 210, MY + 166, 0, MUTED, dx=30, arrowhead=True)
T("m-revise", 466, MY + 262, "Revise loop: a broken rule → back to Generate · a weak reason → back to Method", 14, ORANGE)
L("m-to-exp", 1446, MY + 203, 0, INK, dx=50, arrowhead=True)
R("m-exp", 1496, MY + 92, 416, 222, ORANGE, "#fff4e6")
T("m-exp-h", 1514, MY + 104, "Exp · the test in use", 20, ORANGE)
T("m-exp-b", 1514, MY + 140, "T4: a randomized trial against\nthe control; it observes the result", 14, MUTED)
T("m-learn", 1514, MY + 230, "Learning loop: its data becomes\nthe next internal insights", 14, GREEN)
fam = [("Requirements only", "By goal · By principle"), ("External insights", "By theory · By implementation"),
       ("Internal insights", "By insight · precedent · revising · tailoring"), ("Both insights", "By theory and insight"),
       ("Making them now", "By user test · By co-design"), ("Making them next", "By exploring · By slots")]
for i, (f, m) in enumerate(fam):
    x = 48 + i * 312
    R(f"fam-{i}", x, MY + 344, 298, 70, RULE, "#ffffff")
    T(f"fam-{i}-f", x + 12, MY + 352, f, 15, BLUE)
    T(f"fam-{i}-m", x + 12, MY + 380, m, 13, MUTED)
T("method-el", 48, MY + 428, "Design elements: each element of a design records where it came from (requirements, internal, "
  "external or intuition) and whether it was reasoned or intuitive.", 15, MUTED)
T("workbench-h", 48, MY + 490, "The workbench · Guide and the working Spaces", 30)

json.dump({"type": "excalidraw", "version": 2, "source": "haipipe-design-workbench-ui", "elements": E,
           "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}},
          OUT.open("w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(E), "elements →", OUT.name, "· height", CY + 420 + DY)
