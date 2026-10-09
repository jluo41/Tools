"""Write the methods drawing, the top of Guide › Method (JL 261002; 261003: "put it at the top"), redrawn on the design
unit (JL 261007: "frame 1 is outdated, compared to frame 2 … we need to update it"; the 3 Oct version is in _archive/):
the four kinds of reasoning, each tagged to its step; one design unit in five steps (see input → reason ideas → for
each idea: conduct process → review item → review whole) inside the Revise and Learning loops; then the thirteen cards
as method types in three families (a family is step ①'s choice: whose information the unit sees), each card naming the
registered methods of its type (M01 – M05, read from design_unit_drawing.py). Study counts are read from the papers
table, as the Design methods view counts them. An author script: fold any canvas edit into it first.

    python methods_drawing.py parts/design-methods.excalidraw <server>/related/papers.md"""
import json, random, re, sys, textwrap
from pathlib import Path
random.seed(7)
OUT, PAPERS = sys.argv[1], Path(sys.argv[2])
els = []


def base(kind, x, y, w, h, **kw):
    e = {"id": kw.pop("id", f"m{len(els):03d}"), "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": kw.pop("stroke", "#1e1e1e"), "backgroundColor": kw.pop("bg", "transparent"), "fillStyle": "solid",
         "strokeWidth": kw.pop("sw", 2), "strokeStyle": kw.pop("style", "solid"), "roughness": 0, "opacity": 100,
         "groupIds": [], "frameId": None, "roundness": kw.pop("round", {"type": 3}), "seed": random.randint(1, 2**30),
         "version": 1, "versionNonce": random.randint(1, 2**30), "isDeleted": False, "boundElements": [],
         "updated": 1791000000000, "link": None, "locked": False}
    e.update(kw); els.append(e); return e


FONT, CW = 6, 0.53                        # Nunito, about half an em per character


def text(x, y, s, size=16, color="#1e1e1e", width=None):
    lines = s.split("\n")
    w = width or max(len(l) for l in lines) * size * CW
    return base("text", x, y, w, len(lines) * size * 1.25, stroke=color, round=None, text=s, originalText=s,
                fontSize=size, fontFamily=FONT, textAlign="left", verticalAlign="top", containerId=None,
                autoResize=True, lineHeight=1.25)


def box(x, y, w, h, bg="#ffffff", stroke="#495057", **kw):
    return base("rectangle", x, y, w, h, bg=bg, stroke=stroke, **kw)


def arrow(x, y, pts, color="#1864ab", style="solid"):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return base("arrow", x, y, max(xs) - min(xs), max(ys) - min(ys), stroke=color, round=None, points=pts, style=style,
                lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None,
                endArrowhead="arrow", elbowed=False)


GREEN = "#2f9e44"                         # a change note (JL 261007): "✎ <date>  what changed", at the spot
note = lambda x, y, s: text(x, y, "✎ 261007  " + s, 13, GREEN)
wrap = lambda s, n: "\n".join(textwrap.wrap(s, n, break_on_hyphens=False))
nlines = lambda s: s.count("\n") + 1

# the inputs' colours, as the Design methods view colours a card's reads
REQ, INT, EXT = ("#e7f5ff", "#1864ab"), ("#ebfbee", "#2b8a3e"), ("#f3f0ff", "#7048e8")
KIND = {"req": REQ[1], "int": INT[1], "ext": EXT[1], "": "#495057"}

# studies per method, from the papers table: rows whose group names the method and whose role is evidence
studies = {}
for line in PAPERS.read_text(encoding="utf-8").splitlines():
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) >= 2 and cells[1].lower() == "evidence":
        for g in cells[0].lower().split(";"):
            studies[g.strip()] = studies.get(g.strip(), 0) + 1

# title -----------------------------------------------------------------
text(40, 24, "How we design · the method in one picture", 36)   # JL 261003: no "Design methods" title
text(40, 78, "One design unit in five steps turns what we give into N designs, and the Exp tests them. A method is the "
             "choices it makes at each step; its type is one of the thirteen cards.", 18, "#495057")

# 1 · three inputs → Design → Exp --------------------------------------------
# 0 · the four kinds of reasoning (JL 261003: "add the Reasoning method to the Draw"): what each
# knows and finds, a soup example, and where it sits in this method
RY = 136
text(40, RY, "Four kinds of reasoning · the thing + the rule → the result; ✓ known, ? found", 20, "#343a40")
RSN = [("Deduction · predict", "演绎", "[thing ✓] + [rule ✓] → [result ?]", "salt added + salt makes it salty → it will be salty",
        "here: ④ review item checks it · ⑤ review whole predicts", ("#f8f9fa", "#495057")),
       ("Induction · learn a rule", "归纳", "[thing ✓] + [rule ?] → [result ✓]", "5 salted bowls were all salty → salt makes soup salty",
        "here: after the Exp, an Insight Block learns the rule", INT),
       ("Abduction-1 · solve", "溯因 1", "[thing ?] + [rule ✓] → [result ✓]", "want salty soup + know salt works → add salt",
        "here: ② reason ideas, when ① gives a rule", EXT),
       ("Abduction-2 · create", "溯因 2", "[thing ?] + [rule ?] → [result ✓]", "want happy guests → invent a rule (warm soup) → make it",
        "here: ② reason ideas, goal only: invent the rule", REQ)]
RW, RH = 437, 138
for i, (name, zh, form, ex, here, (bg, st)) in enumerate(RSN):
    x = 40 + i * (RW + 12)
    box(x, RY + 38, RW, RH, bg=bg, stroke=st)
    text(x + 14, RY + 48, f"{name} · {zh}", 18, st)        # the Chinese term beside the name, never clipped
    text(x + 14, RY + 78, form, 15, "#343a40")
    text(x + 14, RY + 102, wrap(ex, 54), 13, "#495057")
    text(x + 14, RY + 140, here, 13, st)
note(1000, RY, "each kind of reasoning tagged to its step of the unit")
text(40, RY + 38 + RH + 14, "In one loop:  learn (induction)  →  ① see  →  ② reason ideas (abduction)  →  ③ conduct  →  ④ ⑤ review (deduction)  →  the Exp  →  learn again", 17, "#1864ab")
Y0, IW = RY + RH + 110, 360
# the content we give (JL 261005: "see the content and also the 'Brain'"), then the brain
content = [("goal", "the aim, for whom, the rules, what to leave out"),
           ("information", "whose: none · ours · other people's; its form"),
           ("examples", "a few good designs, past designs + outcomes"),
           ("tools", "code to analyse data, search, a reader simulator"),
           ("from the last unit", "its designs, checks and ranking")]
CH = 50 + len(content) * 42
box(40, Y0, IW, CH, bg=REQ[0], stroke=REQ[1])
text(56, Y0 + 10, "① the content we give", 20, REQ[1])
note(40, Y0 - 24, "the three inputs became the content we give + the brain")
for i, (a, b) in enumerate(content):
    text(56, Y0 + 48 + i * 42, a, 14, "#343a40")
    text(56, Y0 + 66 + i * 42, b, 12, "#868e96")
BY = Y0 + CH + 16
box(40, BY, IW, 92, bg="#f8f9fa", stroke="#495057", style="dashed")
text(56, BY + 10, "the brain", 20, "#495057")
text(56, BY + 40, "the model's own knowledge: always there,", 14, "#343a40")
text(56, BY + 62, "never handed over; fixed by the model snapshot", 12, "#868e96")
DX, DW = 470, 1010
DY, DH = Y0, max(CH + 16 + 92, 400)
arrow(40 + IW + 6, Y0 + CH / 2, [[0, 0], [DX - 40 - IW - 14, 0]], REQ[1])
arrow(40 + IW + 6, BY + 46, [[0, 0], [DX - 40 - IW - 14, DY + 112 - BY - 46]], "#868e96", "dashed")
box(DX, DY, DW, DH, bg="#f8f9fa", stroke="#343a40")
text(DX + 18, DY + 12, "One design unit", 24)
note(DX + 18, DY - 24, "Method → Generate → Evaluate → Ready became the five-step design unit (frame 2)")
text(DX + 228, DY + 19, "the same five steps for every method; a method is the choices it makes in each", 14, "#495057")
steps = [("① See input", "the content, read: as given, summarised, or analysed with code", "what we control"),
         ("② Reason ideas", "the content meets the brain: N (or N + 5) ideas, each with its source", "abduction"),
         ("③ Conduct process", "one design per idea, made once from the input + that idea", "make"),
         ("④ Review item", "each design on its own: held against the rules and its idea", "check · deduction"),
         ("⑤ Review whole", "all together: rank, predict, keep N", "predict · deduction")]
sx, sw, sh, sg = DX + 20, 180, 128, 15
for i, (a, b, tag) in enumerate(steps):
    hi = i in (1, 2)
    box(sx, DY + 70, sw, sh, bg="#e7f5ff" if hi else "#ffffff", stroke="#1864ab" if hi else "#495057")
    text(sx + 10, DY + 80, a, 16)
    text(sx + 10, DY + 106, wrap(b, 25), 11, "#495057")
    text(sx + 10, DY + 70 + sh - 20, tag, 12, "#1864ab")
    if i < len(steps) - 1:
        arrow(sx + sw + 2, DY + 70 + sh / 2, [[0, 0], [sg - 4, 0]])
    sx += sw + sg
# ③ and ④ run once per idea (JL 261005)
fx = DX + 20 + 2 * (sw + sg) - 6
base("rectangle", fx, DY + 56, 2 * sw + sg + 12, sh + 26, stroke="#7048e8", style="dashed", sw=1, round=None)
text(fx + 4, DY + 58, "for each idea · ×N (or N + 5)", 11, "#7048e8")
# the Revise loop: the next unit reads what this one gave back
RV = "#e8590c"
c1, c5 = DX + 20 + sw / 2, DX + 20 + 4 * (sw + sg) + sw / 2
arrow(c5, DY + 70 + sh + 4, [[0, 0], [0, 40], [c1 - c5, 40], [c1 - c5, 0]], RV)
text(c1 + 14, DY + 70 + sh + 50, "Revise loop (inner): what the unit gives back (its designs, checks, ranking) is the next "
                                 "unit's input · minutes", 13, RV)
text(DX + 20, DY + 70 + sh + 82, wrap("no iteration inside a unit: one design per idea, made once; a revision is a new unit "
                                      "that sees the last one's output (①: from the last unit)", 120), 13, "#1864ab")
text(DX + 20, DY + 70 + sh + 122, "after ⑤: a person releases the kept N, word for word", 13, "#495057")
EX, EY, EW, EH = DX + DW + 60, DY + 70, 1820 - (DX + DW + 60), 150
arrow(DX + DW + 6, EY + EH / 2, [[0, 0], [EX - DX - DW - 14, 0]], "#343a40")
box(EX, EY, EW, EH, bg="#fff9db", stroke="#e67700")
text(EX + 16, EY + 12, "Exp", 24, "#e67700")
text(EX + 16, EY + 48, wrap("tested in use: a randomized trial against the control", 30), 14, "#343a40")
text(EX + 16, EY + 100, wrap("observes the real result, against ⑤'s frozen prediction", 30), 13, "#868e96")
# the Learning loop: the Exp's result becomes our next information (①)
by = DY + DH + 34
iy = Y0 + 48 + 42 + 8
arrow(EX + EW / 2, EY + EH + 4, [[0, 0], [0, by - EY - EH - 4], [20 - EX - EW / 2, by - EY - EH - 4],
                                 [20 - EX - EW / 2, iy - EY - EH - 4], [36 - EX - EW / 2, iy - EY - EH - 4]], INT[1])
text(560, by + 8, "Learning loop (outer): the Exp's result, learned by an Insight Block, becomes ①'s information "
                 "(ours) · weeks, once a round", 15, INT[1])

# 2 · three families by where the rule comes from (JL 261003) ----------------------------------------------------------
FY = by + 92
COLW, GAP = 284, 15
CX = [40 + i * (COLW + GAP) for i in range(6)]
line = lambda x0, x1, y, c: base("line", x0, y, x1 - x0, 0, stroke=c, round=None, points=[[0, 0], [x1 - x0, 0]],
                                 lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None, endArrowhead=None)

R = ("req", "design requirements")
fams = [
 ("Goal Only", "abduction-2: the how is invented", "+ nothing else", REQ, [
   (1, "By goal", "Write the design straight from the requirements; keep the first that passes the rules.", [R],
    "The baseline every other method must beat.", "Newell & Simon 1972 · Simon 1969", "none: no approach develops from the goal alone", False),
   (2, "By principle", "Frame what the requirements really ask, then design to that frame.", [R],
    "Freeze the frame before the first draft.", "Schön 1983 · Dorst 2015", "the first activity of human-centred design", False)]),
 ("External Insights", "abduction-1, on other people's induction", "+ the literature and theory", EXT, [
   (3, "By theory", "Use the technique a named theory prescribes; predict the one variable it moves.",
    [R, ("ext", "external insights: named theories")],
    "A second agent codes the technique blind (T1).", "Bartholomew 1998 · Michie 2011", "evidence and theory-based", False),
   (4, "By implementation", "Design for real-world use: who it reaches, who delivers it, whether it lasts.",
    [("req", "design requirements: the delivery setting"), ("ext", "external insights: RE-AIM")],
    "Reach and adoption are measured in the Exp, not reasoned.", "Glasgow 1999 (RE-AIM)", "implementation-based", False)]),
 ("Internal Insights", "our induction, then abduction-1", "+ our signed insights", INT, [
   (5, "By insight", "Make each part of the design follow from a signed insight.",
    [R, ("int", "internal insights: signed rows")],
    "The Evidence chain checks each cited row (T1).", "Sackett 1996 · MacLean 1991", "evidence and theory-based", False),
   (6, "By precedent", "Find the closest past design and adapt it to these requirements.",
    [R, ("int", "internal insights: past designs and results")],
    "Check it is not a copy of its case (T1).", "Kolodner 1993 · Aamodt & Plaza 1994", "adaptation, outside the eight", False),
   (7, "By revising", "Take one design already tested, and change what its result says to change.",
    [R, ("int", "internal insights: one design and its result")],
    "Only the named change may differ (T1).", "Nielsen 1993 · Kohavi 2009", "refinement, which every approach does", False),
   (8, "By tailoring", "Fit the design to who the reader is: per segment now, per reader later.",
    [R, ("int", "internal insights: who the reader is")],
    "Readers' records are protected health information.", "Hawkins 2008 · Noar 2007 · Nahum-Shani 2018",
    "tailoring to sub-groups, found by experiment", False)]),
 ("Both Insights", "abduction-1 on two hows that agree", "+ our signed insights and theory", ("#fff0f6", "#c2255c"), [
   (9, "By theory and insight", "Follow a signed insight that a named theory explains; predict the variable it moves.",
    [R, ("int", "internal insights: signed rows"), ("ext", "external insights: named theories")],
    "Name the theory's prediction before writing.", "Michie 2011 · Bartholomew 1998 · Sackett 1996",
    "evidence and theory-based, both halves", False)]),
 ("Making internal insights now", "induction in small loops", "+ data gathered while designing", ("#e6fcf5", "#0c8599"), [
   (10, "By user test", "Show drafts to readers, real or simulated, and revise on what they do.",
    [R, ("", "reader profiles")],
    "Simulated readers first, real readers in the pretest (T3).", "Gould & Lewis 1985 · Yardley 2015", "target population-centred", False),
   (11, "By co-design", "Design with the people it is for: they help decide what it should do, and choose.",
    [R, ("", "the people it is for")],
    "A simulated patient panel helps decide; real patients later.", "O'Cathain 2019 · Voorberg 2015", "partnership", True)]),
 ("Making internal insights next", "the Exp does the induction", "+ nothing; it sends several options", ("#fff4e6", "#e8590c"), [
   (12, "By exploring", "Make several designs that differ in principle; the Exp chooses.",
    [R, ("", "any insights, internal or external")],
    "Force the designs apart; AI ideas converge.", "Sobek 1999 · Dow 2010", "combination: may run any of the others", False),
   (13, "By slots", "Split the artifact into slots and change one slot at a time.",
    [R, ("", "the artifact's slots")],
    "A word diff checks only one slot changed.", "Zwicky 1969 · Suh 1990 · Collins 2018", "efficiency-based", False)]),
]
# the thirteen cards by name, then three families over six columns: Goal Only (2), External (1), Internal (3)
card = {c[1]: c for _, _, _, _, cards in fams for c in cards}
FAMS = [("Goal Only", "① information: none · the rule is invented (abduction-2)", "the goal and the brain only; or several designs, the Exp picks", REQ,
         [["By goal", "By principle"], ["By exploring", "By slots"]]),
        ("External Insights", "① information: other people's · abduction-1", "+ the literature and theory", EXT,
         [["By theory", "By implementation"]]),
        ("Internal Insights", "① information: ours · abduction-1", "+ our analysis, past designs, or readers", INT,
         [["By insight", "By precedent", "By revising"], ["By tailoring", "By theory and insight"], ["By user test", "By co-design"]])]
columns, col = [], 0
note(40, FY - 24, "a family is ①'s choice (whose information); each card names its registered methods")
for fam, reason, reads, (fbg, fst), cols in FAMS:
    x0, x1 = CX[col], CX[col + len(cols) - 1] + COLW
    box(x0, FY, x1 - x0, 96, bg=fbg, stroke=fst)
    text(x0 + 14, FY + 10, fam, 21, fst)
    text(x0 + 14, FY + 42, reason, 14, "#343a40")
    text(x0 + 14, FY + 66, reads, 13, "#868e96")
    for names in cols:
        columns.append((col, [card[n] for n in names])); col += 1
# the registered methods, from the design unit catalog (design_unit_drawing.py), by their type; a "?" type is
# proposed (JL 261007: a card is a method's type; the registered methods are the rows of the catalog)
_u = (Path(__file__).resolve().parent / "design_unit_drawing.py").read_text(encoding="utf-8")
_ns = {}
exec(_u[_u.index("IN, ID, PR, CK, OV"):_u.index("# layout")], _ns)
TYPE = {"M01": ("By goal", ""), "M02": ("By precedent", ""), "M03": ("By insight", ""), "M04": ("By insight", ""),
        "M05": ("By insight", "")}
REG = {}
for m in _ns["METHODS"]:
    mid = m[0].split(" · ")[0]
    card_name, q = TYPE.get(mid, ("", "?"))
    REG.setdefault(card_name, []).append(f"{q}{m[0]}")
bottom = 0
for col, cards in columns:
    x = CX[col]
    y = FY + 112
    for n, name, move, ins, ai, frm, tax, future in cards:
        mv = wrap(move, 31)
        aiw = wrap("AI: " + ai, 35)
        frw, taxw = wrap("comes from " + frm, 38), wrap("O'Cathain 2019: " + tax, 38)
        rds = [(kind, "\n".join(textwrap.wrap("reads  " + label, 37, subsequent_indent="   ", break_on_hyphens=False)))
               for kind, label in ins]
        regs = REG.get(name, [])
        regw = wrap("registered: " + (" · ".join(regs) if regs else "none yet"), 38)
        h = 58 + 20 * nlines(mv) + sum(17 * nlines(r) + 3 for _, r in rds) + 18 * nlines(aiw) + 17 * (nlines(frw) + nlines(taxw)) + 18 * nlines(regw) + 40
        box(x, y, COLW, h, bg="#ffffff", stroke=REQ[1] if future else "#495057", style="dashed" if future else "solid")
        text(x + 14, y + 12, f"{n}  {name}", 19)
        k = studies.get(name.lower(), 0)
        status = "future · not run yet" if future else f"tested in {k} stud{'y' if k == 1 else 'ies'}" if k else "no study tests it yet"
        tone = (REQ[1], REQ[0]) if future else ("#2b8a3e", "#ebfbee") if k else ("#c92a2a", "#fff5f5")
        tw = len(status) * 12 * CW + 16
        box(x + COLW - tw - 12, y + 42, tw, 22, bg=tone[1], stroke=tone[0], sw=1)
        text(x + COLW - tw - 4, y + 45, status, 12, tone[0])
        yy = y + 70
        text(x + 14, yy, mv, 15); yy += 20 * nlines(mv) + 6
        for kind, r in rds:
            text(x + 14, yy, r, 13, KIND[kind]); yy += 17 * nlines(r) + 3
        text(x + 14, yy + 2, aiw, 13, REQ[1]); yy += 18 * nlines(aiw) + 6
        text(x + 14, yy, frw, 12, "#868e96"); yy += 17 * nlines(frw)
        text(x + 14, yy, taxw, 12, "#868e96"); yy += 17 * nlines(taxw) + 6
        text(x + 14, yy, regw, 13, "#c92a2a" if "?" in regw else ("#343a40" if regs else "#adb5bd"))
        y += h + 14
    bottom = max(bottom, y)

text(40, bottom + 4, "a card is a method's type; a registered method (M01 – M05, the rows of the design unit catalog) is a "
                    "row of choices at the five steps, and names its type · red ? = a proposed type", 14, "#495057")
note(40, bottom + 30, "types settled: M02 By precedent (how past messages did), M03 and M05 By insight (our evidence)")
bottom += 60
# every design, element by element (JL 261002: "how to choose each element … the reasoning of
# the designer … sometimes … the intuitive or a sudden of light … we can document both") -------
y = bottom + 30
text(40, y, "Every design, element by element", 22)
text(420, y + 6, "each Generate records where each element came from and how it was chosen, in elements.yaml "
                 "· an illustration, not a pilot design", 14, "#868e96")
y += 40
cols = [("element", 150), ("words", 560), ("from · source", 560), ("how chosen", 470)]
ex = [("sender", "<sender line>", ("req", "the goal · its rules: personalization"), "reasoned · System 2"),
      ("news", "<what is new>", ("int", "information (ours) · a signed row on what worked"), "reasoned · System 2"),
      ("reason", "<why act now>", ("ext", "information (other people's) · a named theory"), "reasoned · System 2"),
      ("ask", "<the ask>", ("", "the brain · no source"), "intuitive · System 1: a hunch, never warrant"),
      ("link, opt-out", "<link> <opt-out>", ("req", "the goal · its rules: links, opt-out"), "reasoned · System 2")]
x = 40
for name, w in cols:
    text(x + 10, y, name, 13, "#868e96")
    x += w
y += 24
for i, (el, words, (kind, src), how) in enumerate(ex):
    box(40, y, 1740, 34, bg="#f8f9fa" if i % 2 else "#ffffff", stroke="#dee2e6", sw=1, round=None)
    text(50, y + 8, el, 15)
    text(40 + 150 + 10, y + 8, words, 15)
    text(40 + 710 + 10, y + 8, src, 14, KIND[kind] if kind else "#c92a2a")
    text(40 + 1270 + 10, y + 8, how, 14, "#c92a2a" if how.startswith("intuitive") else "#495057")
    y += 38
text(40, y + 6, "a reasoned element writes its because; an intuitive one is recorded as a labeled hunch. If a hunch works, "
                "the Exp's data, not the hunch, becomes the internal insight (Evans & Stanovich 2013: Type 1 and Type 2)",
     14, "#495057")
bottom = y + 30

# every card, open ------------------------------------------------------------
y = bottom + 30
text(40, y, "Every card, open", 22)
y += 40
box(40, y, 870, 150, bg="#ffffff", stroke="#495057")
text(56, y + 12, "What the literature says", 18)
text(56, y + 44, "rationale · context · the steps its authors specify · strengths · limitations\n"
                 "each claim names its source in brackets, [Prestwich 2013], and opens that paper,\n"
                 "PDF and all; (ours) marks the workbench's own judgment\n"
                 "set out as O'Cathain et al. 2019 describe approaches (their Table 2)", 15, "#495057")
box(950, y, 870, 150, bg="#e7f5ff", stroke="#1864ab")
text(966, y + 12, "Applied to AI", 18, "#1864ab")
text(966, y + 44, "the agent: which inputs it reads · steps: its procedure · returns: what comes with the design\n"
                  "verify: how a second agent tests it · AI risk: what goes wrong when an AI does it\n"
                  "evidence on AI: the language-model studies · skill: the skill that would run it\n"
                  "the head: family · reasoning · move · reads, coloured by input · returns · tests", 15, "#1864ab")

# where O'Cathain's eight categories are ----------------------------------------
y += 184
text(40, y, "O'Cathain et al. 2019: eight approaches, and where each is here", 22)
cats = [("Partnership", "By co-design (future)"), ("Target population-centred", "By user test"),
        ("Evidence and theory-based", "By theory · By insight · By theory and insight"), ("Implementation-based", "By implementation"),
        ("Efficiency-based", "By slots · its tailoring to sub-groups: By tailoring"), ("Stepped or phased", "the shared format: inputs → Design → Exp"),
        ("Intervention-specific", "a board's design requirements"), ("Combination", "By exploring")]
for i, (c, here) in enumerate(cats):
    cx, cy = 40 + (i % 4) * 448, y + 40 + (i // 4) * 70
    box(cx, cy, 428, 58, bg="#f8f9fa", stroke="#adb5bd", sw=1)
    text(cx + 14, cy + 8, c, 16)
    text(cx + 14, cy + 32, "→ " + here, 14, "#1864ab")
y += 40 + 2 * 70 + 30

# the tests, and the bet -----------------------------------------------------------
text(40, y, "How a design is tested", 22)
# the five tests sit where the format puts them: four inside Design before sending, one in the Exp
text(40, y + 40, "In the Revise loop: ④ review item and ⑤ review whole, before anything is sent", 16, RV)
line(40, 40 + 4 * 362 - 30, y + 66, RV)
text(40 + 4 * 362, y + 40, "In the Learning loop: the Exp", 16, INT[1])
line(40 + 4 * 362, 40 + 5 * 362 - 30, y + 66, INT[1])
tests = [("T0 Rules", "keeps every rule", "deduction, from the design"), ("T1 Fidelity", "does what its method claims", "deduction, from the design"),
         ("T2 Critique", "an independent expert reads it", "deduction, from the design"), ("T3 Pretest", "readers understand, trust, would act", "a few readers: a small Exp"),
         ("T4 Exp", "randomized, against the control", "observes the result")]
x = 40
for i, (a, b, c) in enumerate(tests):
    box(x, y + 80, 332, 84, bg="#f8f9fa" if i < 4 else "#fff9db", stroke="#495057" if i < 4 else "#e67700")
    text(x + 14, y + 90, a, 18)
    text(x + 14, y + 116, b, 14, "#495057")
    text(x + 14, y + 138, c, 13, "#868e96")
    x += 362
y += 200
box(40, y, 1780, 96, bg="#fff9db", stroke="#e67700")
text(60, y + 14, "The open question · which method gives better designs?", 20, "#e67700")
text(60, y + 44, "No approach has been compared with another (O'Cathain 2019). Design one goal by several registered methods "
                 "(M01 – M05), review them (④ ⑤, T0 to T2), and let the Exp (T4) answer:\ndoes reading more give better designs, "
                 "and do our own insights beat the literature?", 16)

# never overwrite edits made on the canvas (JL 261003): an element saved from Excalidraw has a
# version above 1. Keep the previous file in the temp folder, and stop unless FORCE=1 is set.
import os, shutil, tempfile
if Path(OUT).is_file():
    old = json.load(open(OUT, encoding="utf-8"))
    edited = [e for e in old.get("elements", []) if not e.get("isDeleted") and e.get("version", 1) > 1]
    prev = Path(tempfile.gettempdir()) / (Path(OUT).name + ".prev")    # outside the repo
    shutil.copyfile(OUT, prev)
    if edited and os.environ.get("FORCE") != "1":
        sys.exit(f"{len(edited)} elements were edited on the canvas; kept {prev}. Fold the edits into "
                 "this script, or rerun with FORCE=1 to overwrite them.")
json.dump({"type": "excalidraw", "version": 2, "source": "haipipe-design-methods-studio", "elements": els,
           "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}},
          open(OUT, "w"), ensure_ascii=False, indent=2)
print(len(els), "elements; height", y + 120, "; studies", {k: v for k, v in studies.items() if k.startswith("by")})
