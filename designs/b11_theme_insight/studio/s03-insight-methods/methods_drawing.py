"""Write the Insight methods drawing, the first fold of Guide › Method (JL 261003: "too thin, you can
check the content here", Design's "the method in one picture"): the ladder for any data, the
inputs → the six steps → Design, then the sixteen method cards under their three families, then
the nine tests at their steps. The cards are read from their files and the study counts from
the papers table, as Guide › Method counts them. An author script, as Design's: the drawing is
then edited in Excalidraw, so check it for canvas edits before running this again.

    .venv/bin/python Tools/designs/b11_theme_insight/studio/s03-insight-methods/methods_drawing.py
"""
import json
import random
import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/servers/_host"))   # moved to b11 (261007)
from host_paths import skill_dir  # noqa: E402

SERVER = Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/servers/workbench-insight"
REF = SERVER / "guide"   # the Insight Guide: method.md, methods/{answer,read}/, methods.excalidraw (261007)
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else REF / "methods.excalidraw"
random.seed(261003)
els = []


def base(kind, x, y, w, h, **kw):
    e = {"id": kw.pop("id", f"m{len(els):03d}"), "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": kw.pop("stroke", "#1e1e1e"), "backgroundColor": kw.pop("bg", "transparent"), "fillStyle": "solid",
         "strokeWidth": kw.pop("sw", 2), "strokeStyle": kw.pop("style", "solid"), "roughness": 0, "opacity": 100,
         "groupIds": [], "frameId": None, "roundness": kw.pop("round", {"type": 3}), "seed": random.randint(1, 2**30),
         "version": 1, "versionNonce": random.randint(1, 2**30), "isDeleted": False, "boundElements": [],
         "updated": 1791000000000, "link": None, "locked": False}
    e.update(kw)
    els.append(e)
    return e


FONT, CW = 6, 0.6                         # Nunito; a little wide, so a title is never clipped


def text(x, y, s, size=16, color="#1e1e1e"):
    lines = s.split("\n")
    return base("text", x, y, max(len(l) for l in lines) * size * CW, len(lines) * size * 1.25, stroke=color, round=None,
                text=s, originalText=s, fontSize=size, fontFamily=FONT, textAlign="left", verticalAlign="top",
                containerId=None, autoResize=True, lineHeight=1.25)


def box(x, y, w, h, bg="#ffffff", stroke="#495057", **kw):
    return base("rectangle", x, y, w, h, bg=bg, stroke=stroke, **kw)


def arrow(x, y, pts, color="#1864ab", style="solid"):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return base("arrow", x, y, max(xs) - min(xs), max(ys) - min(ys), stroke=color, round=None, points=pts, style=style,
                lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None,
                endArrowhead="arrow", elbowed=False)


wrap = lambda s, n: "\n".join(textwrap.wrap(s, n, break_on_hyphens=False))
nlines = lambda s: s.count("\n") + 1
INK, MUT, SOFT = "#343a40", "#495057", "#868e96"
ASK, ANS, READ = ("#ebfbee", "#2b8a3e"), ("#fff4e6", "#e8590c"), ("#f3f0ff", "#7048e8")
BLUE, GOLD = ("#e7f5ff", "#1864ab"), ("#fff9db", "#e67700")


def card(path: Path) -> dict:
    """A method card's head: its name, then each `key: value` line, continuation lines folded in."""
    lines = path.read_text(encoding="utf-8").split("What the literature says")[0].splitlines()
    head, key = {"name": lines[0].strip()}, None
    for line in lines[2:]:
        m = re.match(r"^([a-z ]+): (.*)$", line)
        if m:
            key = m.group(1)
            head[key] = m.group(2).strip()
        elif key and line.startswith("  "):
            head[key] += " " + line.strip()
        elif not line.strip():
            key = None
    return head


studies = {}                              # evidence rows per method group, as Guide › Method counts them
for line in (SERVER / "related" / "papers.md").read_text(encoding="utf-8").splitlines():
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) >= 2 and cells[1].lower() == "evidence":
        for g in cells[0].lower().split(";"):
            studies[g.strip()] = studies.get(g.strip(), 0) + 1

# title ------------------------------------------------------------------------------------------
text(40, 24, "How we ask · the method in one picture", 36)
text(40, 78, "A question is asked and planned before any data is read, run on each partition, and read into an answer "
             "on a page. Steps 1, 3 and 5 have methods to choose from.", 18, MUT)

# 0 · the ladder, for any data (JL 261003: "it can be all kinds of data"): the question form with X and Y,
# examples from three kinds of data, and what the answer may say
RY = 136
text(40, RY, "The ladder · four kinds of question, for any data (X a factor, Y an outcome)", 20, INK)
LAD = [("Data", "what is there: how many, which fields, what is missing?",
        "visits per clinic · readings per sensor · orders per day", "counts, what was seen", ("#f8f9fa", MUT)),
       ("Information", "what pattern: a rate, a trend, a difference between groups?",
        "no-show rate by weekday · failure rate by model", "rates and contrasts, never \"because\"", BLUE),
       ("Knowledge", "does X change Y, with other things held equal, and how sure are we?",
        "do reminders cut no-shows? · does heat shorten a sensor's life?", "one claim, how sure, its rivals, its limits", ASK),
       ("Wisdom", "what should we do about X?",
        "which clinics get reminders · when to replace sensors", "advice, signed by a person, for Design", GOLD)]
RW, RH = 437, 150
for i, (name, ask, eg, say, (bg, st)) in enumerate(LAD):
    x = 40 + i * (RW + 12)
    box(x, RY + 38, RW, RH, bg=bg, stroke=st)
    text(x + 14, RY + 48, name, 20, st)
    text(x + 14, RY + 80, wrap(ask, 50), 15, INK)
    text(x + 14, RY + 124, wrap("e.g. " + eg, 58), 13, SOFT)
    text(x + 14, RY + 160, "may say: " + say, 13, st)
    if i < 3:
        arrow(x + RW + 1, RY + 38 + RH / 2, [[0, 0], [10, 0]], SOFT)

# 1 · inputs → the six steps → Design -------------------------------------------------------------
Y0, IW, IH, IG = RY + RH + 90, 360, 92, 14
inputs = [("The question", "asked by a person, or a need a Design board raised", "signed by a person · one ask at its DIKW level", ASK),
          ("The extract", "one dataset, cut into partitions", "its meta and partitions, fixed before any outcome", BLUE),
          ("The Prototype", "the question files and their scripts", "no data · every extract reads the same one", ("#f8f9fa", MUT))]
DX, DW = 470, 1060
DY, DH = Y0, 3 * IH + 2 * IG + 40
for i, (a, b, c, (bg, st)) in enumerate(inputs):
    y = Y0 + i * (IH + IG)
    box(40, y, IW, IH, bg=bg, stroke=st)
    text(56, y + 10, a, 20, st)
    text(56, y + 40, b, 14, INK)
    text(56, y + 62, c, 13, SOFT)
    arrow(40 + IW + 6, y + IH / 2, [[0, 0], [DX - 40 - IW - 14, DY + 112 - (y + IH / 2)]], st)
box(DX, DY, DW, DH, bg="#f8f9fa", stroke=INK)
text(DX + 18, DY + 12, "Insight", 24)
text(DX + 122, DY + 19, "induction: from what was sent and what happened, the rule behind it", 14, MUT)
STEPS = [("1 Ask", "one ask at its DIKW level; question-asking methods", ASK, "Logic"), ("2 Plan", "steps before any data; another agent agrees", None, "Logic"),
         ("3 Run", "once per partition; question-answering methods", ANS, "Work"), ("4 Check", "the run against its plan", None, "Work"),
         ("5 Page", "the answer at its DIKW level; question-results reading", READ, "Report"), ("6 Hand off", "a signed Wisdom answer", None, "Report")]
sx, sw, sh, sg = DX + 20, 152, 108, 17
xs = []
for i, (a, b, fam, col) in enumerate(STEPS):
    bg, st = fam if fam else ("#ffffff", MUT)
    box(sx, DY + 78, sw, sh, bg=bg, stroke=st)
    text(sx + 10, DY + 88, a, 18, st if fam else INK)
    text(sx + 10, DY + 116, wrap(b, 20), 12, MUT)
    xs.append(sx)
    if i < len(STEPS) - 1:
        arrow(sx + sw + 2, DY + 78 + sh / 2, [[0, 0], [sg - 4, 0]])
    sx += sw + sg
for k, col in enumerate(("Logic · in the Prototype, once per topic", "Work · in the Instance, per dataset", "Report · in the Instance")):     # the three columns over their two steps
    x0, x1 = xs[2 * k], xs[2 * k + 1] + sw
    base("line", x0, DY + 66, x1 - x0, 0, stroke=SOFT, round=None, points=[[0, 0], [x1 - x0, 0]], lastCommittedPoint=None,
         startBinding=None, endBinding=None, startArrowhead=None, endArrowhead=None)
    text(x0, DY + 44, col, 15, SOFT)
RV = "#c92a2a"                                            # back to step 1: a question changes
c1, c2, c5 = xs[0] + sw / 2, xs[1] + sw / 2, xs[4] + sw / 2
arrow(c2, DY + 78 + sh + 4, [[0, 0], [0, 22], [c1 - c2, 22], [c1 - c2, 0]], RV)
text(c1 + 12, DY + 78 + sh + 30, "a refused word or a weak partition: ask again", 12, RV)
arrow(c5, DY + 78 + sh + 4, [[0, 0], [0, 52], [c1 - c5 - 18, 52], [c1 - c5 - 18, 0]], RV)
text(xs[2], DY + 78 + sh + 60, "a fragile answer, or a pattern seen while looking: a new question", 12, RV)
text(DX + 20, DY + 288, "only the method at steps 1, 3 and 5 changes; every method keeps the same question file, plan fields, "
                        "second agent and tests", 13, BLUE[1])
EX, EY, EW, EH = DX + DW + 60, DY + 70, 1820 - (DX + DW + 60), 150
arrow(DX + DW + 6, EY + EH / 2, [[0, 0], [EX - DX - DW - 14, 0]], INK)
box(EX, EY, EW, EH, bg=GOLD[0], stroke=GOLD[1])
text(EX + 16, EY + 12, "Design", 24, GOLD[1])
text(EX + 16, EY + 48, wrap("reads only a signed Wisdom answer, as an internal insight", 26), 14, INK)
text(EX + 16, EY + 100, wrap("its Exp's data is the next extract", 26), 13, SOFT)
by = DY + DH + 34                                        # the Exp's data comes back as the next extract
iy = Y0 + IH + IG + IH / 2
arrow(EX + EW / 2, EY + EH + 4, [[0, 0], [0, by - EY - EH - 4], [20 - EX - EW / 2, by - EY - EH - 4],
                                 [20 - EX - EW / 2, iy - EY - EH - 4], [36 - EX - EW / 2, iy - EY - EH - 4]], BLUE[1])
text(560, by + 8, "Learning loop: the Exp's data becomes the next extract, read through the same Prototype", 15, BLUE[1])

# 2 · three families, one per step, and their cards --------------------------------------------------
FY = by + 92
COLW, GAP = 284, 15
CX = [40 + i * (COLW + GAP) for i in range(6)]
FAMS = [("Question-asking methods · step 1", "what exactly are we asking, and what would answer it?", "before any data is read · Logic", ASK, "ask", 3),
        ("Question-answering methods · step 3", "how does the run find the answer?", "look first, or ask first · Work", ANS, "answer", 2),
        ("Question-results reading · step 5", "does the answer survive the ways it could be wrong?", "before a page claims it · Report", READ, "read", 1)]
col, bottom = 0, 0
for fam, question, sub, (fbg, fst), folder, ncols in FAMS:
    x0, x1 = CX[col], CX[col + ncols - 1] + COLW
    q, ft = wrap(question, int((x1 - x0 - 28) / (14 * CW))), wrap(fam, int((x1 - x0 - 28) / (21 * CW)))
    box(x0, FY, x1 - x0, 140, bg=fbg, stroke=fst)                  # room for a title and a question on two lines
    text(x0 + 14, FY + 10, ft, 21, fst)
    qy = FY + 14 + 27 * nlines(ft)
    text(x0 + 14, qy, q, 14, INK)
    text(x0 + 14, qy + 4 + 18 * nlines(q), sub, 13, SOFT)
    cards = [card(p) for p in sorted((REF / "methods" / folder if folder != "ask" else
                                      skill_dir("haipipe-question-asking") / "methods").glob("*.md"))]
    per = -(-len(cards) // ncols)
    for c in range(ncols):
        x, y = CX[col + c], FY + 156
        for n, h in enumerate(cards[c * per:(c + 1) * per], c * per + 1):
            future = h.get("status", "").startswith("future")
            mv, rd = wrap(h.get("move", ""), 31), wrap("reads  " + h.get("reads", ""), 37)
            tn = wrap("tested now  " + h.get("test now", ""), 38)
            fr = wrap("comes from " + re.sub(r",[^;]*", "", h.get("comes from", "")).replace(";", " ·"), 38)
            hh = 58 + 20 * nlines(mv) + 17 * nlines(rd) + 17 * nlines(tn) + 17 * nlines(fr) + 30
            box(x, y, COLW, hh, bg="#ffffff", stroke=fst if future else MUT, style="dashed" if future else "solid")
            text(x + 14, y + 12, f"{n}  {h['name']}", 19)
            k = studies.get(h["name"].lower(), 0)
            status = "future · not run yet" if future else f"tested in {k} stud{'y' if k == 1 else 'ies'}" if k else "no study tests it yet"
            tone = (fst, fbg) if future else ("#2b8a3e", "#ebfbee") if k else ("#c92a2a", "#fff5f5")
            tw = len(status) * 12 * CW + 16
            box(x + COLW - tw - 12, y + 42, tw, 22, bg=tone[1], stroke=tone[0], sw=1)
            text(x + COLW - tw - 4, y + 45, status, 12, tone[0])
            yy = y + 70
            text(x + 14, yy, mv, 15)
            yy += 20 * nlines(mv) + 6
            text(x + 14, yy, rd, 13, fst)
            yy += 17 * nlines(rd) + 3
            text(x + 14, yy, tn, 13, BLUE[1])
            yy += 17 * nlines(tn) + 3
            text(x + 14, yy, fr, 12, SOFT)
            y += hh + 14
        bottom = max(bottom, y)
    col += ncols

# 3 · nine tests, each at its step ----------------------------------------------------------------------
y = bottom + 30
text(40, y, "How an answer is checked · nine tests, each at its step", 22)
GROUPS = [("step 2 · Plan and agree, before any data", [("T0 Covered", "every word of the ask maps to a step"),
                                                       ("T1 Specified", "each step names its partition, unit, measure"),
                                                       ("T2 Agreed", "another agent agrees the plan"),
                                                       ("T3 Powered", "each partition can detect the effect")], ASK),
          ("step 4 · Check the run", [("T4 Spec", "the files and columns the plan names"),
                                      ("T7 Robustness", "rival analyses agree in sign and size")], ANS),
          ("step 5 · Write the page", [("T5 Fidelity", "each sentence says what its result says"),
                                       ("T6 Independent", "an agent that did not write it checks it")], READ),
          ("in use", [("T8 Replication", "another extract gives it again")], GOLD)]
x, TW = 40, 186
for label, tests, (bg, st) in GROUPS:
    w = len(tests) * (TW + 8) - 8
    text(x, y + 40, label, 15, st)
    base("line", x, y + 64, w, 0, stroke=st, round=None, points=[[0, 0], [w, 0]], lastCommittedPoint=None,
         startBinding=None, endBinding=None, startArrowhead=None, endArrowhead=None)
    for a, b in tests:
        box(x, y + 76, TW, 84, bg=bg, stroke=st)
        text(x + 12, y + 86, a, 16, st)
        text(x + 12, y + 112, wrap(b, 26), 12, MUT)
        x += TW + 8
    x += 22
y += 196
box(40, y, 1780, 96, bg=GOLD[0], stroke=GOLD[1])
text(60, y + 14, "The bet", 20, GOLD[1])
text(60, y + 44, "No study compares these methods head to head on one question. Does a question planned before the data, agreed "
                 "by a second agent and powered per partition\ngive answers that hold on the next extract (T8) more often than "
                 "one fitted to the runs already in hand?", 16)

OUT.write_text(json.dumps({"type": "excalidraw", "version": 2, "source": "haipipe-insight-methods-studio", "elements": els,
                           "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}},
                          ensure_ascii=False, indent=2), encoding="utf-8")
print(len(els), "elements; height", y + 120, "→", OUT.name)
