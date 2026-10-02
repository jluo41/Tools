"""Build insight-workbench-design.excalidraw, the Insight workbench design drawing.

The drawing is generated: change this file, then run it (AGENTS.md rule 8):

    .venv/bin/python Tools/plugins/haipipe-toolkit/servers/workbench-insight/studio/insight-workbench-design.py

It follows the Paper workbench drawing (servers/workbench-paper/studio/), same sizes,
colours and grammar. One workbench reads one dataset (JL 261001). Part 1: the Spaces,
their sub-spaces, the runs of each in order and the skill of each run. Part 2: each
Space as the workbench shows it, content left, Runs panel right. Part 3: Insight ›
Questions, one High/Low table per partition: logic left (the questions asked at
D, I, K and W), work right (the runs that answer them). Part 4: one dataset, one
workbench; what changes; what each Space reads.
"""
import json
import random
import sys
import time
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_suffix(".excalidraw")
random.seed(261001)
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


def vline(id_, x, y, h, color=RULE):
    e = base(id_, "line", x, y, 0, h, stroke=color, rounded=False)
    e.update(points=[[0, 0], [0, h]], lastCommittedPoint=None, startBinding=None,
             endBinding=None, startArrowhead=None, endArrowhead=None)
    E.append(e)


def arrow(id_, x, y, points, color, both=False):
    e = base(id_, "arrow", x, y, max(p[0] for p in points), max(abs(p[1]) for p in points), stroke=color,
             rounded=False)
    e.update(points=points, lastCommittedPoint=None, startBinding=None, endBinding=None,
             startArrowhead="arrow" if both else None, endArrowhead="arrow", elbowed=False)
    E.append(e)


def chips(key, x, y, labels, sel, size=16, h=40):
    """A row of buttons, each as wide as its label (tabs, views, partitions)."""
    for n, label in enumerate(labels):
        w = max(96, int(len(label) * size * 0.56) + 32)
        button(f"{key}-{n}", x, y, w, h, label, sel=n == sel, size=size)
        x += w + 10
    return x


FW, FH, GAP = 1176, 820, 32
X = [48 + i * (FW + GAP) for i in range(4)]
PARTS = ["Full", "Young male", "Young female", "Older", "Midlife male", "Midlife female", "Cross"]

# ---- title and the one dataset -------------------------------------------------
text("title", 48, 24, "Insight Workbench · design", 34)
text("subtitle", 48, 74, "One workbench, one dataset. Logic on the left: the questions asked at Data, "
     "Information, Knowledge and Wisdom. Work on the right: the runs that answer them. "
     "One table per partition.", 18, MUTED)
rect("ds-box", 48, 118, 4 * FW + 3 * GAP, 64, BLUE, "#e7f5ff")
text("ds-text", 72, 128,
     "Dataset  SMSR2v1 · 20250616_SMSR2v1_min_2025-07-03 · one row = one sent invitation · 444,691 rows · "
     "122 columns · 13 messages · 2025-06-16 → 2025-07-03", 19, BLUE)
text("ds-rule", 72, 154,
     "Every Space reads this one extract. Partitions are cuts of it. A new extract is a new workbench "
     "(SMSR3Full → A03_SMSR3Full-InsightBoard).", 15, MUTED)

# ---- part 1 · Space → sub-space → runs in order → skill ----------------------
P1 = 222
text("p1-title", 48, P1, "1 · Spaces, sub-spaces, runs in order, and the skill of each run", 28)

# Part 1 is drawn from the Workbench Table, never kept by hand beside it
# (skills/insight/haipipe-workbench-insight/ref/workbench-table.md, read with
# table-workbench's own reader, so `render_workbench_table.py --check` and this
# drawing see the same rows).
_HERE = Path(__file__).resolve()
_PLUGIN = _HERE.parents[3]
sys.path.insert(0, str(_PLUGIN / "skills" / "0_utils" / "table-workbench" / "ref"))
from render_workbench_table import read_table  # noqa: E402

TABLE = _PLUGIN / "skills" / "insight" / "haipipe-workbench-insight" / "ref" / "workbench-table.md"
SPACE_TEXT = {   # what each Space asks, and what it hands on: prose the table does not hold
    "Scope": ("Which data, which cuts, which questions?", "hands on: the questions → Insight › Questions"),
    "Insight": ("What does each question need, and what answers it?",
                "tabs Full · Young male · … · Cross pick the partition · hands on: Wisdom answers → Delivery"),
    "Check": ("Can each answer be trusted?", "hands on: a failed check routes back to the run that owns it"),
    "Delivery": ("What goes to Design?", "hands on: the signed handoff → the DesignBoard"),
}


def _map_from_table(rows):
    spaces = []
    for r in rows:
        if r["Level"] != "board":
            continue
        if not spaces or spaces[-1][0] != r["Space"]:
            spaces.append((r["Space"], []))
        views = spaces[-1][1]
        if not views or views[-1][0] != r["View"]:
            views.append((r["View"], []))
        views[-1][1].append(r)
    out = []
    for space, views in spaces:
        n, subs = 0, []
        for view, runs in views:
            items = []
            for r in runs:
                control = r["Run type"] == "none" or r["Agent"] == "none"
                if not control:
                    n += 1
                signs = "" if r["Person signs"] == "none" else f" · signs {r['Person signs']}"
                note = "a view, no run" if control else f"agent {r['Agent'].replace(' (new)', '*')}{signs}"
                items.append(("·" if control else str(n), r["Run type"] if not control else "(read only)",
                              r["Skill"].replace(" (new)", "*") if not control else "", note))
            subs.append((view, items))
        asks, hands = SPACE_TEXT.get(space, ("", ""))
        out.append((f"{space} Space", asks, subs, hands))
    return out


MAP = _map_from_table(read_table(TABLE))


def _height(subs):
    y = 120
    for _sub, runs in subs:
        ry = y + sum(62 if note else 44 for *_x, note in runs)
        y = max(y + 56, ry + 12)
    return y


BH = max(_height(subs) for _t, _a, subs, _h in MAP) + 76
for i, (title, asks, subs, hands) in enumerate(MAP):
    x0, y0 = X[i], P1 + 56
    rect(f"m{i}-box", x0, y0, FW, BH)
    text(f"m{i}-title", x0 + 24, y0 + 22, title, 28)
    text(f"m{i}-asks", x0 + 24, y0 + 64, asks, 19, BLUE)
    line(f"m{i}-rule", x0 + 24, y0 + 100, FW - 48)
    y = y0 + 120
    for n, (sub, runs) in enumerate(subs):
        button(f"m{i}-sub{n}", x0 + 24, y, 200, 40, sub, size=17)
        ry = y
        for k, (num, run, skill, note) in enumerate(runs):
            ctl = num == "·"                              # a control action: no run identity
            text(f"m{i}-sub{n}-run{k}", x0 + 248, ry + 4, "%s  %-16s" % (num, run), 19, MUTED if ctl else INK, mono=True)
            text(f"m{i}-sub{n}-skill{k}", x0 + 540, ry + 4, skill, 17, MUTED if ctl else GREEN, mono=True)
            if note:
                text(f"m{i}-sub{n}-note{k}", x0 + 540, ry + 30, note, 14, MUTED)
            ry += 62 if note else 44
        y = max(y + 56, ry + 12)
    text(f"m{i}-hands", x0 + 24, y0 + BH - 52, hands, 16, MUTED)

mid = P1 + 56 + 60
for i in range(3):
    arrow(f"m-link{i}", X[i] + FW + 2, mid, [[0, 0], [GAP - 4, 0]], BLUE)
text("m-rules", 48, P1 + 56 + BH + 28,
     "Drawn from haipipe-workbench-insight/ref/workbench-table.md. The number is the order inside a Space; · marks a view with no run; * marks a planned skill or agent. "
     "A question is written first; a run answers it, and the run's config names that question (answers: [QI2, …]).\n"
     "Each run names its skill. Creating a config never starts a run: the person presses Run.", 17)

# ---- part 2 · each Space as the workbench shows it ----------------------------
P2 = P1 + 56 + BH + 130
text("p2-title", 48, P2, "2 · Each Space: content on the left, its Runs panel on the right", 28)
Y0 = P2 + 56


def space(key, i, title, tabs, sel_tab, views, sel_view, draw_content, types, sel_type, run, notes):
    x0 = X[i]
    rect(f"{key}-space", x0, Y0, FW, FH)
    text(f"{key}-title", x0 + 24, Y0 + 26, title, 30)
    line(f"{key}-rule", x0 + 24, Y0 + 62, FW - 48)
    chips(f"{key}-tab", x0 + 24, Y0 + 76, tabs, sel_tab, size=19, h=50)
    text(f"{key}-ds", x0 + 24, Y0 + 148, "SMSR2v1 · 444,691 rows", 16, MUTED)
    if views:
        chips(f"{key}-view", x0 + 24, Y0 + 186, views, sel_view, size=14, h=38)
    cx, cy = x0 + 24, Y0 + 272
    rect(f"{key}-content", cx, cy, 552, 410)
    draw_content(key, cx, cy)
    rx, ry = x0 + 600, Y0 + 272
    rect(f"{key}-runs", rx, ry, 552, 410, bg=PANEL)
    text(f"{key}-runs-title", rx + 18, ry + 22, "Runs", 22)
    for n, label in enumerate(types):
        button(f"{key}-type-{n}", rx + 18, ry + 70 + n * 50, 180, 40, label, sel=n == sel_type,
               size=14, dashed=label.startswith("+"))
    dx, dy = rx + 210, ry + 70
    rect(f"{key}-detail", dx, dy, 324, 316, bg="#ffffff")
    text(f"{key}-run-name", dx + 14, dy + 12, run["name"], 15)
    text(f"{key}-skill", dx + 14, dy + 38, "Skill " + run["skill"], 12, GREEN, mono=True)
    button(f"{key}-rerun", dx + 232, dy + 8, 80, 28, "Rerun", size=13)
    button(f"{key}-copy", dx + 232, dy + 58, 80, 28, "Copy", size=13)
    text(f"{key}-prompt-label", dx + 14, dy + 62, "Prompt", 15)
    text(f"{key}-prompt", dx + 14, dy + 84, run["prompt"], 12, MUTED)
    text(f"{key}-process-label", dx + 14, dy + 156, "Running process", 15)
    text(f"{key}-process", dx + 14, dy + 178, run["process"], 12)
    text(f"{key}-results-label", dx + 14, dy + 228, "Results", 15)
    text(f"{key}-results", dx + 14, dy + 250, run["results"], 12, BLUE)
    text(f"{key}-notes", x0 + 24, Y0 + 706, notes, 16)


def kv(key, x, y, rows, lw=150, w=516, size=13):
    """Label/value rows as a two-column table with cell edges and a shaded label cell."""
    h = 30
    for n, (k, v) in enumerate(rows):
        rect(f"{key}-k{n}", x, y + n * h, lw, h, RULE, PANEL)
        rect(f"{key}-v{n}", x + lw, y + n * h, w - lw, h, RULE)
        text(f"{key}-kt{n}", x + 8, y + n * h + 7, k, size, MUTED)
        text(f"{key}-vt{n}", x + lw + 8, y + n * h + 7, v, size)


def scope_content(key, cx, cy):
    kv(f"{key}-kv", cx + 18, cy + 24, [
        ("Extract", "20250616_SMSR2v1_min_2025-07-03"),
        ("One row", "one sent invitation"),
        ("Rows · columns", "444,691 · 122"),
        ("Dates", "2025-06-16 → 2025-07-03 · 18 days"),
        ("Experiment", "13 message wordings, about 34,000 each"),
        ("Outcomes", "messaged → clicked → authenticated"),
        ("Cut of", "SMSR2Full (751,110 rows, to 2025-07-17)"),
        ("Partitions", "Full + 5 cuts · Cross compares them"),
        ("Results", "in each page folder: results/<ticket>/"),
        ("Files", "manifest.json · data_dictionary.csv"),
    ])


space("scope", 0, "Scope Space", ["Dataset", "Partitions", "Methods", "Questions"], 0, [], None, scope_content,
      ["1 Prepare extract", "2 Ask", "3 Method · paper", "+ New Run"], 1,
      {"name": "run-ask-1001-message-order", "skill": "haipipe-insight-question",
       "prompt": "Register this question: does the\norder of messages matter? Pick the\nlevel and partitions; do not answer.",
       "process": "Done · Knowledge question 17,\nFull only",
       "results": "MT03 · one new row"},
      "Dataset → 1 Prepare extract · Questions → 2 Ask\n"
      "Methods → Discovery methods · Design methods · Methods studio · Papers → 3 Add a method or a paper\n"
      "Partitions: Full, Young male, Young female, Older, Midlife male, Midlife female, Cross.\n"
      "No dataset switcher: this workbench has one extract.")


def insight_content(key, cx, cy):
    x = cx + 14
    text(f"{key}-head", x, cy + 14, "LOGIC          │ WORK           │ REPORT", 12, MUTED, mono=True)
    rect(f"{key}-sel", x - 6, cy + 76, 530, 80, BLUE, "#e7f5ff")
    text(f"{key}-tree", x, cy + 36,
         "▸ Data          │                │\n"
         "▾ Information   │                │\n"
         "  Question 2  ✅│ Task  Funnel   │ How the 13\n"
         "  How does each │   rates        │ messages did\n"
         "  message do?   │ smsr2v1 ok  ↗  │ salience leads\n"
         "                │                │ at 66.06%\n"
         "  Question 4  ✅│ Task  Funnel   │ Weekday barely\n"
         "                │   rates        │ moves clicks\n"
         "▾ Knowledge     │                │\n"
         "  Question 2  ✅│ Runs behind it │ Segmenting does\n"
         "                │                │ not beat one\n"
         "  Question 10 🚫│ —              │ No answer\n"
         "▸ Wisdom        │                │", 12, INK, mono=True)


space("insight", 1, "Insight Space", ["Questions"], 0, PARTS, 0, insight_content,
      ["3 Data runs · 4", "4 Information runs · 1", "5 Report", "6 Pool or split", "+ New Run"], 1,
      {"name": "03_funnel_rates · smsr2v1", "skill": "haipipe-task",
       "prompt": "/haipipe-task run D02_extract_profile/\n03_funnel_rates with configs/smsr2v1;\nJL presses Run.",
       "process": "Done · status ok · answers\nInformation questions 1-6, 15-18",
       "results": "<page>/results/\nrun_b51j21t01r01_full_funnel_rates/"},
      "Questions → 3 Data runs · 4 Information runs · 5 Report · 6 Pool or split (Cross)\n"
      "Picking a question narrows the Runs panel to it, in this partition.\n"
      "A run opens its results, a report opens as a document, in a pop-out (part 3).")


def check_content(key, cx, cy):
    x = cx + 18
    text(f"{key}-gates", x, cy + 26,
         "GI0  the extract is recorded        🟡 MT00 partial\n"
         "GI1  each question has a row        ✅\n"
         "GI2  each answer cites its runs     ✅\n"
         "GI3  numbers match their run files  ⬜ check\n"
         "GI4  the Cross verdict is current   ✅ POOL\n"
         "GI5  the Wisdom answer is signed    ⬜ re-sign\n"
         "GI6  the register cell is settled   ✅", 13, INK, mono=True)
    text(f"{key}-note", x, cy + 200,
         "A gate is shown on its own row; the person or\n"
         "the owner closes it, never the screen.", 13, MUTED)


space("check", 2, "Check Space", ["Gates", "Checks"], 0, [], None, check_content,
      ["1 Mechanical check", "2 Answer review", "+ New Run"], 0,
      {"name": "run-check-1001-numbers", "skill": "haipipe-insight-check",
       "prompt": "Check every number on the board\nagainst the run file it cites.",
       "process": "Done · 1 finding: one fact,\nfour numbers (prior messages)",
       "results": "_runs/insight/run-check-1001/\nfindings.md"},
      "Gates → shown, closed by their owners · Checks → 1 Mechanical · 2 Answer review\n"
      "A finding routes back to the run that owns the number.")


def delivery_content(key, cx, cy):
    kv(f"{key}-kv", cx + 18, cy + 24, [
        ("Serves", "Wisdom question 1 · Full"),
        ("Finding", "Keep sending salience"),
        ("Strength", "STRONG, from Knowledge question 1"),
        ("Boundary", "round 2 only; no untested message"),
        ("Overreach", "no segment-specific copy"),
        ("Cross", "POOL: the five cuts defer to Full"),
        ("Signed", "⬜ not current · re-sign"),
        ("Goes to", "B00 DesignBoard"),
    ])


space("delivery", 3, "Delivery Space", ["Handoff"], 0, [], None, delivery_content,
      ["1 Handoff draft", "· Sign", "+ New Run"], 0,
      {"name": "run-handoff-1001-wisdom-1", "skill": "haipipe-insight-wisdom",
       "prompt": "Draft the Design Handoff from the\nWisdom report; leave signed: for\nthe person.",
       "process": "Held · waiting for your signature",
       "results": "1-full/W01-full-<slug>/\n· Design Handoff"},
      "Handoff → 1 Handoff draft · Sign is a control: the person writes signed:.\n"
      "Design reads only a signed, current handoff.")

for i in range(3):
    arrow(f"link{i}", X[i] + FW + 2, Y0 + 346, [[0, 0], [GAP - 4, 0]], BLUE if i == 0 else MUTED)

# ---- part 3 · Insight › Questions: one High/Low table per partition ------------
P3 = Y0 + FH + 90
text("p3-title", 48, P3, "3 · Insight › Questions: one table per partition · Logic · Work · Report", 28)
text("p3-sub", 48, P3 + 44, "The question asks, the runs compute, the report says what the answer is. The same "
     "questions in the same order in every table; a refused question says why in Report.", 18, MUTED)
TY, TH = P3 + 96, 900
CW = (330, 330)                                     # Logic and Work widths; Report takes the rest


def table(key, i, sel, title, logic, work, report, foot, marks=()):
    """Three columns: Logic (the question) · Work (the runs) · Report (what it says)."""
    x0 = X[i]
    xl, xw, xr = x0 + 24, x0 + 24 + CW[0] + 20, x0 + 24 + CW[0] + CW[1] + 40
    rect(f"{key}-box", x0, TY, FW, TH)
    text(f"{key}-title", x0 + 24, TY + 22, title, 26)
    chips(f"{key}-part", x0 + 24, TY + 70, PARTS, sel, size=15, h=38)
    for col, (x, label) in enumerate(((xl, "LOGIC · the question"), (xw, "WORK · the runs"), (xr, "REPORT · what it says"))):
        text(f"{key}-h{col}", x, TY + 134, label, 16, MUTED)
    line(f"{key}-rule", x0 + 24, TY + 164, FW - 48)
    vline(f"{key}-split1", xw - 10, TY + 172, TH - 260)
    vline(f"{key}-split2", xr - 10, TY + 172, TH - 260)
    for n, (y, h) in enumerate(marks):                # a picked question: light fill across all three
        rect(f"{key}-pick{n}", x0 + 16, TY + y, FW - 32, h, BLUE, "#e7f5ff")
    text(f"{key}-logic", xl, TY + 182, logic, 13, INK, mono=True)
    text(f"{key}-work", xw, TY + 182, work, 13, INK, mono=True)
    text(f"{key}-report", xr, TY + 182, report, 13, INK, mono=True)
    text(f"{key}-foot", x0 + 24, TY + TH - 72, foot, 15, MUTED)


R = 16.25                                            # one mono line at 13px
table("full", 0, 0, "Full · 444,691 rows",
      "▸ Data questions         4  ✅\n"
      "▾ Information questions 18\n"
      "\n"
      "▾ Question 2                ✅\n"
      "  How does each message\n"
      "  perform?\n"
      "  builds on Data questions 2, 3\n"
      "\n"
      "  Question 4                ✅\n"
      "  Engagement over time?\n"
      "  builds on Data question 3\n"
      "\n"
      "▾ Knowledge questions   16\n"
      "\n"
      "  Question 2                ✅\n"
      "  Should messages be\n"
      "  segmented?\n"
      "  builds on Information\n"
      "  questions 7, 8, 9, 11, 18\n"
      "\n"
      "  Question 10               🚫\n"
      "  Differ across cultural\n"
      "  groups?\n"
      "\n"
      "▸ Wisdom questions       2  ✅",
      "\n\n\n"
      "⌄ Task  Funnel rates\n"
      "  1 run · answers 9 more\n"
      "    D02 extract_profile\n"
      "      03 funnel_rates ▸ 1 run\n"
      "        smsr2v1  ok   ↗\n"
      "› Task  Funnel rates\n"
      "  1 run · smsr2v1 · ok\n"
      "\n\n\n\n"
      "› Runs behind it\n"
      "  5 runs, from the\n"
      "  questions it builds on\n"
      "\n\n\n"
      "—",
      "\n\n\n"
      "How the 13 messages performed\n"
      "salience leads at 66.06% clicked;\n"
      "default trails at 62.47%.\n"
      "per invitation · round 2 only\n"
      "\n"
      "Weekday barely moves clicks\n"
      "a 3.7-point weekday spread, far\n"
      "below the gap between messages.\n"
      "\n\n\n"
      "Segmenting does not beat one message\n"
      "no age, day, region or drug class\n"
      "has a different best message.\n"
      "STRONG · round 2 only\n"
      "\n\n"
      "No answer · the extract has no\n"
      "cultural measure",
      "Full is the template: every question is asked here first. Its runs are the smsr2v1 calls.",
      marks=[(182 + 3 * R - 4, 5 * R + 6)])

table("young", 1, 1, "Young male · 53,342 rows",
      "▾ Data questions         4\n"
      "  Question 1                🚫\n"
      "  What does the extract hold?\n"
      "\n"
      "  Question 3                ✅\n"
      "  How many reach each step?\n"
      "\n"
      "▾ Information questions 18\n"
      "\n"
      "▾ Question 2                ✅\n"
      "  How does each message\n"
      "  perform?\n"
      "\n\n\n"
      "  Question 8                🚫\n"
      "  Message × medical context?\n"
      "\n"
      "▾ Knowledge questions   16\n"
      "  Question 2                🚫\n"
      "  Should messages be\n"
      "  segmented?\n"
      "\n"
      "▾ Wisdom questions       2\n"
      "  Question 1                ✅\n"
      "  Which messages to exploit?",
      "\n—\n\n\n"
      "› Task  Funnel rates\n"
      "  1 run · youngmale · ok\n"
      "\n\n\n"
      "⌄ Task  Funnel rates\n"
      "    D02 extract_profile\n"
      "      03 funnel_rates ▸ 1 run\n"
      "        youngmale  ok   ↗\n"
      "\n\n"
      "—\n\n\n\n"
      "—\n\n\n\n\n"
      "—",
      "\n"
      "Answered on Full · a property\n"
      "of the whole extract\n"
      "\n"
      "The funnel in this cut\n"
      "counts at each step, young men only\n"
      "\n\n\n"
      "How the 13 messages performed here\n"
      "the same leader as Full; the middle\n"
      "nine still cannot be told apart.\n"
      "\n\n\n"
      "Too few rows · 2 of 34 drug classes\n"
      "reach the 300-row floor\n"
      "\n\n"
      "Defers to Full · asking “segment?”\n"
      "from inside a segment is circular\n"
      "\n\n\n"
      "Defers to Full · the Cross verdict\n"
      "says POOL",
      "Same questions, same order as Full. Work shows only this cut's runs (youngmale).",
      marks=[(182 + 9 * R - 4, 4 * R + 6)])

table("cross", 2, 6, "Cross · compares the cuts",
      "▾ Data questions         1\n"
      "  Question 4                ✅\n"
      "  What does chance do to\n"
      "  balance?\n"
      "\n"
      "▾ Information questions  1\n"
      "  Question 14               ✅\n"
      "  How large is the gap\n"
      "  between the partitions?\n"
      "\n"
      "▾ Knowledge questions    2\n"
      "  Question 15               ✅\n"
      "  Do the partitions really\n"
      "  differ?\n"
      "\n"
      "  Question 16               ✅\n"
      "  Pool them or serve them\n"
      "  apart?\n"
      "  builds on Knowledge\n"
      "  question 15",
      "\n"
      "› Task  Expected balance\n"
      "  06 balance_expected\n"
      "  ▸ 6 runs\n"
      "\n\n"
      "No run names it under\n"
      "answers: yet\n"
      "\n\n\n"
      "—\n"
      "\n\n\n"
      "—",
      "\n"
      "Chance balance, cut by cut\n"
      "the deviation each cut's size allows\n"
      "\n\n\n"
      "The gap between the cuts\n"
      "same best and worst message in all\n"
      "six cuts\n"
      "\n\n"
      "The cuts differ in size, not in\n"
      "which message wins\n"
      "\n\n"
      "One story: pool the cuts\n"
      "POOL · every Wisdom answer waits for it",
      "Cross owns no rows. It lists only the questions that compare the cuts, and the verdict.",
      marks=[(182 + 15 * R - 4, 5 * R + 6)])


def popout(key, i):
    """A run line opens its results over the table (the Paper run-result pop-out)."""
    x0 = X[i]
    rect(f"{key}-box", x0, TY, FW, TH)
    text(f"{key}-title", x0 + 24, TY + 22, "A run opens its results · pop-out", 26)
    rect(f"{key}-sheet", x0 + 48, TY + 80, FW - 96, TH - 190, INK, "#ffffff")
    sx, sy = x0 + 80, TY + 104
    text(f"{key}-h1", sx, sy, "smsr2v1", 26)
    text(f"{key}-where", sx, sy + 44,
         "1-full/<page>/results/run_bNNjNNtNNrNN_full_<task>/", 13, MUTED, mono=True)
    for n, lab in enumerate(["Run script ↗", "Config ↗", "answers.yaml ↗"]):
        text(f"{key}-link{n}", sx + n * 160, sy + 76, lab, 15, BLUE)
    text(f"{key}-receipt", sx, sy + 118, "Receipt", 20)
    text(f"{key}-rt", sx, sy + 150,
         "status: ok\nconfig: configs/smsr2v1.yaml\nanswers: [QI1, QI2, QI3, QI4, QI5, QI6, QI15 … QI18]", 13, INK, mono=True)
    text(f"{key}-tables", sx, sy + 228, "Tables · 24", 20)
    text(f"{key}-csv", sx, sy + 260, "rates_by_arm.csv", 15, BLUE)
    text(f"{key}-rows", sx, sy + 288,
         "arm                sent     clicked %\n"
         "salience           34,…     66.06\n"
         "progressFeedback   34,…     64.45\n"
         "default            34,…     62.47\n"
         "…                  13 rows", 14, INK, mono=True)
    text(f"{key}-more", sx, sy + 404,
         "overall_rates.csv · rates_by_age_band.csv · rates_by_gender.csv · …\n"
         "Other files · metrics.json · grouping_audit.csv", 14, MUTED)
    text(f"{key}-close", x0 + FW - 340, TY + 96, "Esc closes · Open in its own tab ↗", 14, MUTED)
    text(f"{key}-foot", x0 + 24, TY + TH - 90,
         "No page in between: the run's results are the evidence, and the Report column says what they\n"
         "mean. A report opens the same way, with links to the runs it read.", 15, MUTED)


popout("pop", 3)
for i in range(3):
    arrow(f"t-link{i}", X[i] + FW + 2, TY + 90, [[0, 0], [GAP - 4, 0]], MUTED)

# ---- part 4 · one dataset; what changes; what each Space reads ----------------
P4 = TY + TH + 90
text("p4-title", 48, P4, "4 · One dataset, one workbench", 28)
rect("one-box", 48, P4 + 56, FW, 520)
text("one-text", 72, P4 + 82,
     "1. The workbench is born from one extract: MT00 names it, the banner\n"
     "   shows it on every Space, and there is no dataset switcher.\n\n"
     "2. A partition is a cut of that extract, never a second dataset:\n"
     "   one config per task, its population block names the cut.\n\n"
     "3. Task folders are shared functions. A config's store: line names\n"
     "   its board, so this workbench lists only its own calls\n"
     "   (smsr2v1, youngmale, … and not smsr3full).\n\n"
     "4. A config's answers: line names the questions its run answers.\n"
     "   That line joins the Logic side to the Work side.\n\n"
     "5. A new extract is a new workbench: SMSR3Full → A03. Round 3\n"
     "   checking round 2 is a comparison between two workbenches,\n"
     "   not a partition of either.", 17, INK)

CX = X[1]
text("change-title", CX, P4, "What changes", 28)
rect("change-box", CX, P4 + 56, FW + GAP + FW, 520)
text("change-table", CX + 24, P4 + 82,
     "Before                                          Now\n"
     "\n"
     "6 Spaces: Scope, Insight, Evidence, Check,      4 Spaces, a Runs panel beside each: Scope, Insight,\n"
     "  Run, Delivery                                   Check, Delivery (Evidence → the Work side; Run → the panels)\n"
     "Question × partition grid                       one High/Low table per partition; logic left, work right\n"
     "D/I/K/W answer pages (D03-full, I02-full …)     Work: each need's bound results · Report: the page itself,\n"
     "                                                  one small file per question per cut, written by a Report run\n"
     "Page-level Insight view (This page, Cites,      retired: a run line opens its results in a pop-out\n"
     "  Cited by, Gates, Log)\n"
     "QK2, FD02, B, C … on screen                     Knowledge questions › Question 2 · Young male; codes stay in files\n"
     "“Runs here” line under each tab                 the Runs panel, narrowed to the picked question\n"
     "Dataset shown only on MT00                      one dataset banner on every Space", 16, INK, mono=True)

RX = X[3]
text("files-title", RX, P4, "What each Space reads", 28)
rect("files-box", RX, P4 + 56, FW, 520)
text("files-map", RX + 24, P4 + 82,
     "UI tab               reads                     runs live in\n"
     "\n"
     "Scope › Dataset      MT00 · manifest.json       7-AgentStore/A0-DIKW-\n"
     "                                                Prepare/<extract>/\n"
     "Scope › Partitions   MT00 § Partition Register  configs/<call>.yaml\n"
     "Scope › Questions    MT01 – MT04 Queues         (rows, no runs)\n"
     "Insight › Questions  MT01 – MT04 + each         <page>/answers.yaml + results/\n"
     "                     config's answers: line     <board>/<job>/<task>/\n"
     "                                                results/<call>/\n"
     "Check › Gates        the GI records             _runs/insight/\n"
     "Check › Checks       haipipe-insight-check      page CHECK runs\n"
     "Insight › Report     <page>.md (haipipe-page)   the page flow + CHECK\n"
     "Delivery › Handoff   the Wisdom report          its Design Handoff",
     15, BLUE, mono=True)

# ---- part 5 · how one run attaches to its dataset and its result -------------
P5 = P4 + 680
text("p5-title", 48, P5, "5 · One run: which dataset it reads, which cut, which questions, where its result lands", 28)
text("p5-sub", 48, P5 + 44, "The run's stem names everything it is: r02_smsr2v1_youngmale is its config, its ticket and its "
     "result folder. The config names the dataset and the cut; the board names where the result goes.", 18, MUTED)
BY, BH5 = P5 + 100, 330


def box(key, x, y, w, h, title, body, color=INK, bg="transparent", sub=""):
    rect(f"{key}-box", x, y, w, h, color, bg)
    text(f"{key}-title", x + 20, y + 16, title, 22, color)
    if sub:
        text(f"{key}-sub", x + 20, y + 48, sub, 14, MUTED)
    text(f"{key}-body", x + 20, y + (78 if sub else 56), body, 14, INK, mono=True)


box("ds", X[0], BY, FW, BH5, "1 · The dataset · read, never written",
    "_WorkSpace/7-AgentStore/A0-DIKW-Prepare/20250616_SMSR2v1/\n"
    "├── 20250616_SMSR2v1_min_2025-07-03_dikw_input.parquet\n"
    "├── manifest.json            source set · end date · version\n"
    "└── data_dictionary.csv\n\n"
    "one prepared extract = one InsightBoard (MT00 names it)\n"
    "444,691 rows · one row = one sent invitation",
    sub="prepared before the board exists; every run of this board reads it")
box("task", X[1], BY, FW, BH5, "2 · The run · authored, in the Task folder",
    "tasks/b51_sms_dikw/j21_information_funnel/t01_funnel_rates/\n"
    "├── scripts/funnel_rates.py               the code, dataset-neutral\n"
    "├── scripts/config/r02_smsr2v1_youngmale.yaml\n"
    "│     input.parquet_path: …/20250616_SMSR2v1/…parquet   ← 1\n"
    "│     population.where: gender = M · age ≤ 35           ← the cut\n"
    "│     answers: [QI4.E1, QI9.E1, …]  from the pages' answers.yaml\n"
    "└── runs/r02_smsr2v1_youngmale.sh          the ticket you press\n\n"
    "the config names the needs it serves; the page ticket calls it",
    BLUE, "#f3f8fd", sub="one config + one ticket per dataset × cut; same stem rNN_<dataset>_<cut>")
box("res", X[2], BY, FW, BH5, "3 · The result · generated, in the page folder",
    "2-youngmale/I04-youngmale-<slug>/            ← 4\n"
    "├── runs/run_b51j21t01r02_youngmale_funnel_rates.sh\n"
    "├── answers.yaml   QI4.E1 → rates_by_weekday.csv …\n"
    "└── results/run_b51j21t01r02_youngmale_funnel_rates/\n"
    "    ├── runtime.yaml   status · ticket · config · git sha\n"
    "    ├── rates_by_weekday.csv · rates_by_hour.csv · …\n"
    "    └── metrics.json · fig_*.png\n\n"
    "RESULT_DIR = the page's results/<ticket>/",
    GREEN, "#f4fbf5", sub="never edited by hand; rerun the ticket to change it")
box("wb", X[3], BY, FW, BH5, "5 · The workbench · reads, never writes",
    "Insight › Questions › Young male\n\n"
    "LOGIC                 WORK                     REPORT\n"
    "Information           Task  Funnel rates       Report  …\n"
    "question 2            t01_funnel_rates\n"
    "                        r02_smsr2v1_youngmale ok ↗\n\n"
    "answers.yaml puts each need beside its files;\n"
    "↗ opens 3 (runtime.yaml, tables, figures) in the pop-out",
    sub="the row is joined by the evidence need, bound on the page")
box("board", X[0], BY + BH5 + 80, FW, 250, "4 · The board · holds the questions and the pages",
    "insights/SMSR2v1-InsightBoard/\n"
    "├── board.md      one extract, no store\n"
    "├── 0-MT-meta/    MT00 extract · partitions · MT01–MT04 needs\n"
    "└── 2-youngmale/I04-youngmale-<slug>/   page · runs/ · results/\n\n"
    "the page ticket calls the task ticket with RESULT_DIR = its results/",
    sub="the Task never names a board; the page hands it a path")
box("two", X[2], BY + BH5 + 80, FW, 250, "Same Task, another dataset → another board",
    "scripts/config/r11_smsr3full_full.yaml\n"
    "  input.parquet_path: …/20250829_SMSR3Full/…parquet\n"
    "→ insights/SMSR3Full-InsightBoard/1-full/<page>/\n"
    "    results/run_b51j21t01r11_full_funnel_rates/\n\n"
    "one dataset · one board · its pages hold its results",
    MUTED, sub="the code is shared; the result is not")
box("heavy", X[3], BY + BH5 + 80, FW, 250, "Heavy output stays out of results/",
    "a model, an array, a row-level table, any file > 10 MB\n"
    "→ _WorkSpace/ProjectResult/<Project>/<page path>/results/<ticket>/\n"
    "  results/<run>/heavy.yaml points to it   (AGENTS.md rule 10)\n\n"
    "receipts write paths relative to the SPACE root (rule 7)",
    MUTED, sub="the result stays light")
mid5 = BY + BH5 // 2
arrow("a-ds-task", X[0] + FW + 2, mid5, [[0, 0], [GAP - 4, 0]], BLUE)
arrow("a-task-res", X[1] + FW + 2, mid5, [[0, 0], [GAP - 4, 0]], GREEN)
arrow("a-res-wb", X[2] + FW + 2, mid5, [[0, 0], [GAP - 4, 0]], MUTED)
arrow("a-board-task", X[0] + FW // 2, BY + BH5 + 78, [[0, 0], [0, -40], [X[1] - X[0], -40], [X[1] - X[0], -76]], INK)
text("a-board-label", X[0] + FW // 2 + 20, BY + BH5 + 14, "RESULT_STORE (the board hands the run its store)", 15, INK)
arrow("a-task-two", X[1] + FW - 120, BY + BH5 + 2, [[0, 0], [0, 140], [X[2] - X[1] - FW + 118, 140]], MUTED)
text("p5-rules", 48, BY + BH5 + 360,
     "1. The stem is the identity: config, ticket and result folder share rNN_<dataset>_<cut>.   "
     "2. The dataset and the cut live in the config, never in the code.\n"
     "3. The board decides the place: RESULT_STORE = the board's store; the result is RESULT_STORE/<block>/<job>/<task>/results/<run>/.   "
     "4. runtime.yaml writes the attachment down: config, input, store, git sha.", 17)


text("footer", 48, BY + BH5 + 450, "Design drawing: illustrative states from A00 (SMSR2v1), not live data. "
     "Generated by studio/insight-workbench-design.py; edit that file, then run it.", 16, MUTED)

# ---- frame · how a question is asked (JL 261002: "who are in charge of asking questions") ----------
# Its own Excalidraw frame, to the right of parts 1-5, which it leaves as they are.
QA0 = len(E)
QX = [X[3] + FW + 300 + i * (FW + GAP) for i in range(4)]
QY = 222
text("qa-title", QX[0], QY, "How a question is asked · who asks it, how it is made small, who checks it, who signs it", 28)
text("qa-sub", QX[0], QY + 44, "A question asks one thing, and its evidence needs form a logic: each need is a premise, and the "
     "logic line says how they lead to the answer. Today no one checks a question's size: D01 asked four things with eight "
     "unrelated needs.", 18, MUTED)
QB, QH = QY + 100, 430
box("qa-src", QX[0], QB, FW, QH, "1 · Where a question comes from",
    "a decision a DesignBoard must make        what the designer needs to know\n"
    "                                          (the question's consumer)\n"
    "a finding on this data                    a contradiction or a refuted answer:\n"
    "                                          the area fields that describe the\n"
    "                                          prescriber's ZIP, the 'percentages'\n"
    "                                          that are codes\n"
    "a cause moved up a rung                   a Data or Information ask that\n"
    "                                          claims a cause becomes a Knowledge\n"
    "                                          question\n"
    "a prior study's topic                     Gen 1's chapters: a candidate only,\n"
    "                                          never a question as written\n\n"
    "a raw ask names where it came from and what will use its answer",
    sub="the asker raises a raw ask; the asker never answers it")
box("qa-shape", QX[1], QB, FW, QH, "2 · Make it small · the shaper",
    "split the raw ask at every 'and', comma and second verb\n\n"
    "each small question gets:\n"
    "  ask        one thing, in plain words\n"
    "  rung       D · I · K · W; a D or I ask states no cause\n"
    "  logic      one line: how its needs lead to the answer\n"
    "  needs      at most three, each one used in the logic\n"
    "  partitions asked where it means the same, and why not elsewhere\n"
    "  parent     the raw ask or finding it came from\n"
    "  consumer   the decision or higher question that reads it\n\n"
    "the shaper plans from the ask and the column list only;\n"
    "it never reads results to fit a question to them",
    BLUE, "#f3f8fd", sub="haipipe-insight-agent · skill haipipe-insight-question")
box("qa-review", QX[2], QB, FW, QH, "3 · Check it · the reviewer, another agent",
    "one thing?        the ask has no 'and', no list, one verb\n"
    "logic follows?    the answer follows from these needs, and\n"
    "                  every need is used\n"
    "small?            three needs or fewer\n"
    "rung legal?       no cause at D or I; cites one rung below\n"
    "new?              not a duplicate of a question already asked\n"
    "placed?           parent and consumer named\n\n"
    "AGREE, or FIX with the exact split or wording;\n"
    "a reviewer never reviews a question it shaped",
    GREEN, "#f4fbf5", sub="haipipe-insight-reviewer-agent")
box("qa-sign", QX[3], QB, FW, QH, "4 · Sign it, then it lands",
    "the person signs the question list         ✅ <YYMMDD>\n"
    "  may refuse a question, merge two, or ask for a split\n\n"
    "→ Prototype question file  <rung>/<L><NN>-<name>/\n"
    "    ask · rung · logic · partitions · needs · agreed\n"
    "→ the needs' specs and the script follow (the evidence plan)\n"
    "→ each Instance scaffolds it and runs it, partition by partition\n\n"
    "a question is never answered on the screen that asked it",
    sub="the person · Scope › Questions › Ask in the workbench")
arrow("qa-a1", QX[0] + FW + 2, QB + QH // 2, [[0, 0], [GAP - 4, 0]], BLUE)
arrow("qa-a2", QX[1] + FW + 2, QB + QH // 2, [[0, 0], [GAP - 4, 0]], GREEN)
arrow("qa-a3", QX[2] + FW + 2, QB + QH // 2, [[0, 0], [GAP - 4, 0]], MUTED)
QB2, QH2 = QB + QH + 80, 470
box("qa-roles", QX[0], QB2, FW, QH2, "5 · Who is in charge",
    "role       who                        does                        never\n\n"
    "asker      a person, or the insight   raises a raw ask from a     answers it\n"
    "           agent from a source        source above\n"
    "shaper     haipipe-insight-agent      splits it into small        reads results to\n"
    "           (haipipe-insight-question) questions with their logic  fit the question\n"
    "reviewer   haipipe-insight-reviewer-  checks size, logic, rung,   reviews what it\n"
    "           agent                      newness and placement       shaped\n"
    "signer     the person                 signs the question list     writes the spec\n\n"
    "the person owns the list; the agents propose and check",
    sub="today: the asks came from Gen 1's chapters; no role checked their size")
box("qa-example", QX[1], QB2, 2 * FW + GAP, QH2, "6 · Example · D01 re-asked as small questions whose needs form a logic",
    "raw ask   what is in this extract, at what shape, with what missingness and what column types?   (four asks, eight needs)\n\n"
    "small question                         needs                                             logic\n"
    "What is one row?                       rows per invitation key · rows per patient key    invitation key unique, patient key repeats\n"
    "                                                                                         ⇒ one row is one invitation\n"
    "Which extract is this?                 manifest identity · file hash · counts from file  counts agree and hash recorded\n"
    "                                                                                         ⇒ identity bound to this file\n"
    "Is a gap missing data, or by design?   null share · columns empty on the same rows      shared gaps that follow a funnel step\n"
    "                                                                                         ⇒ by design; a lone gap ⇒ missing\n"
    "Patient's area or prescriber's?        distinct per patient ZIP3 · per prescriber ZIP5  constant within one key only, against\n"
    "                                       · the dictionary's label                          the label ⇒ which area, where it is wrong\n"
    "Does a column hold what its name says? stored type · range and distinct count · note    'percentage' as whole numbers 0-19\n"
    "                                                                                         ⇒ a code, not a share",
    BLUE, "#f3f8fd", sub="each question: one ask, two or three needs, every need used in its logic")
box("qa-open", QX[3], QB2, FW, QH2, "7 · To decide together",
    "1. does the person sign each question, or the list per rung?\n\n"
    "2. must every question name a consumer before it is asked?\n\n"
    "3. when does a finding become a new question, and when\n"
    "   only a note on the page that found it?\n\n"
    "4. how many questions does one rung hold before the list\n"
    "   is reviewed as a whole?\n\n"
    "5. a Knowledge question's needs are its premises, rivals and\n"
    "   test, and its judge is the conclusion: is three needs\n"
    "   enough there?",
    "#e8590c", sub="open; nothing here is built yet")
text("qa-rules", QX[0], QB2 + QH2 + 36,
     "1. One question asks one thing.   2. Its needs form a logic: at most three, each used in the logic line.   "
     "3. An ask joined by 'and' or a list is split.\n"
     "4. A Data or Information ask states no cause.   5. A question names its parent and its consumer.   "
     "6. The shaper never reads results; the reviewer never reviews its own; the person signs.", 17)


def _qa_bounds(e):
    if e.get("points"):
        xs, ys = [e["x"] + p[0] for p in e["points"]], [e["y"] + p[1] for p in e["points"]]
        return min(xs), min(ys), max(xs), max(ys)
    return e["x"], e["y"], e["x"] + e["width"], e["y"] + e["height"]


_qa = [_qa_bounds(e) for e in E[QA0:]]
_qf = base("frame-ask", "frame", min(b[0] for b in _qa) - 32, min(b[1] for b in _qa) - 32,
           max(b[2] for b in _qa) - min(b[0] for b in _qa) + 64, max(b[3] for b in _qa) - min(b[1] for b in _qa) + 64,
           rounded=False)
_qf["name"] = "How a question is asked"
for e in E[QA0:]:
    e["frameId"] = "frame-ask"
E.append(_qf)

OUT.write_text(json.dumps({"type": "excalidraw", "version": 2, "source": "haipipe-insight-workbench-design",
                           "elements": E, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
                           "files": {}}, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(E), "elements →", OUT)
