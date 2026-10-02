"""Write the methods studio drawing by input (JL 261002): design requirements, internal
insights and external insights → Design → Exp, then thirteen cards in six families. A one-off
author script; the drawing is then edited in Excalidraw. Study counts are read from the
papers table, as the Design methods view counts them."""
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
text(40, 24, "Design methods · one task, thirteen ways to design it", 36)
text(40, 78, "Three inputs go into Design, and the Exp tests it. Methods differ in which inputs they read before "
             "designing and in what they must return with the design.", 18, "#495057")

# 1 · three inputs → Design → Exp --------------------------------------------
Y0, IW, IH, IG = 140, 360, 92, 14
inputs = [("Design requirements", "the Design Goal: what it must do and keep", "approved by a person · given, not inferred", REQ),
          ("Internal insights", "our own data: past Exps, readers' records", "signed on an InsightBoard · our induction", INT),
          ("External insights", "the literature and theory: other people's data", "cited · other people's induction", EXT)]
DX, DW = 470, 1010
DY, DH = Y0, 3 * IH + 2 * IG + 40
for i, (a, b, c, (bg, st)) in enumerate(inputs):
    y = Y0 + i * (IH + IG)
    box(40, y, IW, IH, bg=bg, stroke=st)
    text(56, y + 10, a, 20, st)
    text(56, y + 40, b, 14, "#343a40")
    text(56, y + 62, c, 13, "#868e96")
    arrow(40 + IW + 6, y + IH / 2, [[0, 0], [DX - 40 - IW - 14, DY + 112 - (y + IH / 2)]], st)
box(DX, DY, DW, DH, bg="#f8f9fa", stroke="#343a40")
text(DX + 18, DY + 12, "Design", 24)
text(DX + 118, DY + 19, "abduction: from the requirements (the result wanted) and an insight (the how), the design (the what)", 14, "#495057")
steps = [("Method", "choose one; read the inputs it reads"), ("Generate", "the design, and what it returns"),
         ("Evaluate", "before sending: the rules, a critique, a pretest"), ("Ready", "a person approves")]
sx, sw, sh, sg = DX + 20, 222, 104, 24
for i, (a, b) in enumerate(steps):
    hi = a in ("Method", "Generate")
    box(sx, DY + 60, sw, sh, bg="#e7f5ff" if hi else "#ffffff", stroke="#1864ab" if hi else "#495057")
    text(sx + 12, DY + 70, a, 18)
    text(sx + 12, DY + 96, wrap(b, 30), 12, "#495057")
    if i < len(steps) - 1:
        arrow(sx + sw + 3, DY + 60 + sh / 2, [[0, 0], [sg - 6, 0]])
    sx += sw + sg
# the Revise loop (JL 261002: "go back to the Method if it think it is not good"): a broken rule
# goes back to Generate, a weak reason to Method
RV = "#e8590c"
mc, gc, ec = DX + 20 + sw / 2, DX + 20 + (sw + sg) + sw / 2, DX + 20 + 2 * (sw + sg) + sw / 2
arrow(ec + 12, DY + 168, [[0, 0], [0, 22], [gc - ec - 12, 22], [gc - ec - 12, 0]], RV)
text(gc + 14, DY + 194, "a broken rule: back to Generate", 12, RV)
arrow(ec - 12, DY + 168, [[0, 0], [0, 50], [mc - ec + 12, 50], [mc - ec + 12, 0]], RV)
text(mc + 14, DY + 222, "a weak reason: back to Method", 12, RV)
text(DX + 20, DY + 248, "Revise loop (inner): Method, Generate, Evaluate, until it passes · minutes, many rounds · "
                        "gives back a revised design", 15, RV)
text(DX + 20, DY + 276, "only Method and Generate change from one method to another; every method keeps the same requirements,\n"
                        "the same tests and the same approval. With no insight, Design is abduction-2: it must invent the how too.",
     13, "#1864ab")
EX, EY, EW, EH = DX + DW + 60, DY + 60, 1820 - (DX + DW + 60), 150
arrow(DX + DW + 6, EY + EH / 2, [[0, 0], [EX - DX - DW - 14, 0]], "#343a40")
box(EX, EY, EW, EH, bg="#fff9db", stroke="#e67700")
text(EX + 16, EY + 12, "Exp", 24, "#e67700")
text(EX + 16, EY + 48, wrap("tested in use: a randomized trial against the control", 30), 14, "#343a40")
text(EX + 16, EY + 100, wrap("observes the result; what it records is new internal data", 30), 13, "#868e96")
# the Exp's data goes back as internal data
by = DY + DH + 34
iy = Y0 + IH + IG + IH / 2
arrow(EX + EW / 2, EY + EH + 4, [[0, 0], [0, by - EY - EH - 4], [20 - EX - EW / 2, by - EY - EH - 4],
                                 [20 - EX - EW / 2, iy - EY - EH - 4], [36 - EX - EW / 2, iy - EY - EH - 4]], INT[1])
text(560, by + 8, "Learning loop (outer): the Exp's data becomes the next internal insights · weeks, once a round · "
                 "gives back an insight", 15, INT[1])

# 2 · five families ----------------------------------------------------------
FY = by + 92
COLW, GAP = 284, 15
CX = [40 + i * (COLW + GAP) for i in range(6)]
line = lambda x0, x1, y, c: base("line", x0, y, x1 - x0, 0, stroke=c, round=None, points=[[0, 0], [x1 - x0, 0]],
                                 lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None, endArrowhead=None)
text(CX[0], FY - 50, "Abduction · reads none of our own data", 17, "#495057")
line(CX[0], CX[1] + COLW, FY - 22, "#adb5bd")
text(CX[2], FY - 50, "Induction · learns from our own data: before, during and after Design", 17, "#495057")
line(CX[2], CX[5] + COLW, FY - 22, "#adb5bd")

R = ("req", "design requirements")
fams = [
 ("Requirements only", "abduction-2: the how is invented", "+ nothing else", REQ, [
   (1, "By goal", "Write the design straight from the requirements; keep the first that passes the rules.", [R],
    "The baseline every other method must beat.", "Newell & Simon 1972 · Simon 1969", "none: no approach develops from the goal alone", False),
   (2, "By principle", "Frame what the requirements really ask, then design to that frame.", [R],
    "Freeze the frame before the first draft.", "Schön 1983 · Dorst 2015", "the first activity of human-centred design", False)]),
 ("With external insights", "abduction-1, on other people's induction", "+ the literature and theory", EXT, [
   (3, "By theory", "Use the technique a named theory prescribes; predict the one variable it moves.",
    [R, ("ext", "external insights: named theories")],
    "A second agent codes the technique blind (T1).", "Bartholomew 1998 · Michie 2011", "evidence and theory-based", False),
   (4, "By implementation", "Design for real-world use: who it reaches, who delivers it, whether it lasts.",
    [("req", "design requirements: the delivery setting"), ("ext", "external insights: RE-AIM")],
    "Reach and adoption are measured in the Exp, not reasoned.", "Glasgow 1999 (RE-AIM)", "implementation-based", False)]),
 ("With internal insights", "our induction, then abduction-1", "+ our signed insights", INT, [
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
 ("With both insights", "abduction-1 on two hows that agree", "+ our signed insights and theory", ("#fff0f6", "#c2255c"), [
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
bottom = 0
for col, (fam, reason, reads, (fbg, fst), cards) in enumerate(fams):
    x = CX[col]
    box(x, FY, COLW, 96, bg=fbg, stroke=fst)
    text(x + 14, FY + 10, fam, 19, fst)
    text(x + 14, FY + 40, reason, 14, "#343a40")
    text(x + 14, FY + 64, reads, 13, "#868e96")
    y = FY + 112
    for n, name, move, ins, ai, frm, tax, future in cards:
        mv = wrap(move, 31)
        aiw = wrap("AI: " + ai, 35)
        frw, taxw = wrap("comes from " + frm, 38), wrap("O'Cathain 2019: " + tax, 38)
        rds = [(kind, "\n".join(textwrap.wrap("reads  " + label, 37, subsequent_indent="   ", break_on_hyphens=False)))
               for kind, label in ins]
        h = 58 + 20 * nlines(mv) + sum(17 * nlines(r) + 3 for _, r in rds) + 18 * nlines(aiw) + 17 * (nlines(frw) + nlines(taxw)) + 34
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
        text(x + 14, yy, taxw, 12, "#868e96")
        y += h + 14
    bottom = max(bottom, y)

# every design, element by element (JL 261002: "how to choose each element … the reasoning of
# the designer … sometimes … the intuitive or a sudden of light … we can document both") -------
y = bottom + 30
text(40, y, "Every design, element by element", 22)
text(420, y + 6, "each Generate records where each element came from and how it was chosen, in elements.yaml "
                 "· an illustration, not a pilot design", 14, "#868e96")
y += 40
cols = [("element", 150), ("words", 560), ("from · source", 560), ("how chosen", 470)]
ex = [("sender", "Hi, it's Dr. {NAME}'s office.", ("req", "requirements · Design Goal: personalization"), "reasoned · System 2"),
      ("news", "New prescription details are ready.", ("int", "internal insight · a signed row on what worked"), "reasoned · System 2"),
      ("reason", "Check them before your next visit", ("ext", "external insight · Reason (because)"), "reasoned · System 2"),
      ("ask", "Take a look:", ("", "intuition · none"), "intuitive · System 1: a hunch, never warrant"),
      ("link, opt-out", "{LINK} Reply STOP to opt-out", ("req", "requirements · Design Goal: links, opt-out"), "reasoned · System 2")]
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
text(40, y + 40, "In the Revise loop: Evaluate, before anything is sent", 16, RV)
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
text(60, y + 14, "The bet", 20, "#e67700")
text(60, y + 44, "No approach has been compared with another (O'Cathain 2019). Design one task by several methods and compare them "
                 "in the Revise loop (T0 to T2) and in the Exp (T4):\ndoes reading more inputs give better designs, and do internal insights beat external ones?", 16)

json.dump({"type": "excalidraw", "version": 2, "source": "haipipe-design-methods-studio", "elements": els,
           "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}},
          open(OUT, "w"), ensure_ascii=False, indent=2)
print(len(els), "elements; height", y + 120, "; studies", {k: v for k, v in studies.items() if k.startswith("by")})
