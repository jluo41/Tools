"""Write the design-unit drawing (JL 261005): one design unit in five steps (④ ⑤ renamed Review item, Review whole, JL 261007).

  ① See input → ② Reason and propose design ideas (N, or N+5) → for each idea: ③ Conduct process
  (the input + that one idea → one design) → ④ Review item → ⑤ Review whole (rank all the
  designs together; keep N of N+5)

Above, every choice: each step a bucket, its parts as rows, the part's options as chips; ③ and ④
sit in one frame because they run once per idea. Below, one row per method, holding only the
choices that make it. The three-step version is _archive/design_unit_drawing-3step-261005.py.
An author script; rerun it after a change, and fold any canvas edit into it first.

It writes parts/design-unit-methods.excalidraw; build_s03_design_methods.py puts it in s03's one drawing (261007), in b12_theme_design's s03 (moved 261007); the
design board's Guide opens it there.

    python3 design_unit_drawing.py [out.excalidraw]
"""
import json, os, random, shutil, sys, tempfile
from pathlib import Path
random.seed(11)
HERE = Path(__file__).resolve().parent
OUT = sys.argv[1] if len(sys.argv) > 1 else str(HERE / "parts" / "design-unit-methods.excalidraw")
els = []


def base(kind, x, y, w, h, **kw):
    e = {"id": kw.pop("id", f"u{len(els):03d}"), "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": kw.pop("stroke", "#1e1e1e"), "backgroundColor": kw.pop("bg", "transparent"), "fillStyle": "solid",
         "strokeWidth": kw.pop("sw", 2), "strokeStyle": kw.pop("style", "solid"), "roughness": 0, "opacity": 100,
         "groupIds": [], "frameId": None, "roundness": kw.pop("round", {"type": 3}), "seed": random.randint(1, 2**30),
         "version": 1, "versionNonce": random.randint(1, 2**30), "isDeleted": False, "boundElements": [],
         "updated": 1791200000000, "link": None, "locked": False}
    e.update(kw); els.append(e); return e


FONT, CW = 6, 0.53                        # Nunito, about half an em per character


def text(x, y, s, size=16, color="#1e1e1e"):
    lines = s.split("\n")
    # the saved width is where Excalidraw clips the text: measure wide (w, m and capitals run past half
    # an em; "How many" lost its y at 0.53) and add a little room
    return base("text", x, y, max(len(l) for l in lines) * size * 0.62 + 6, len(lines) * size * 1.25, stroke=color,
                round=None, text=s, originalText=s, fontSize=size, fontFamily=FONT, textAlign="left",
                verticalAlign="top", containerId=None, autoResize=True, lineHeight=1.25)


def box(x, y, w, h, bg="#ffffff", stroke="#495057", **kw):
    return base("rectangle", x, y, w, h, bg=bg, stroke=stroke, **kw)


def polyline(pts, colour, sw=3, style="solid", head=False):
    x0, y0 = pts[0]
    rel = [[x - x0, y - y0] for x, y in pts]
    xs, ys = [p[0] for p in rel], [p[1] for p in rel]
    return base("arrow" if head else "line", x0, y0, max(xs) - min(xs), max(ys) - min(ys), stroke=colour, sw=sw,
                style=style, round=None, points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None,
                startArrowhead=None, endArrowhead="arrow" if head else None, **({"elbowed": False} if head else {}))


CH, CGAP = 30, 8
cw = lambda s, size=13: (len(s) + 1) * size * CW + 20          # a chip's width; an emoji is wide


def chips(x, y, right, items, bg, st, size=13):
    """Chips left to right from (x, y), wrapping at `right`; returns the y under the last line."""
    cx, cy = x, y
    for s in items:
        w = cw(s, size)
        if cx + w > right and cx > x:
            cx, cy = x, cy + CH + 6
        box(cx, cy, w, CH, bg=bg, stroke=st, sw=1.5)
        text(cx + 10, cy + 7, s, size, "#1e1e1e")
        cx += w + CGAP
    return cy + CH


def lines(items, width):
    n, cx = 1, 0
    for s in items:
        w = cw(s) + CGAP
        if cx + w > width and cx:
            n, cx = n + 1, 0
        cx += w
    return n


# the five steps: (title, sub, band, colours, parts); a part is a row of options ----------------------
IN, ID, PR, CK, OV = (("#e7f5ff", "#1864ab"), ("#f3f0ff", "#7048e8"), ("#f8f9fa", "#495057"),
                      ("#fff4e6", "#e67700"), ("#ebfbee", "#2b8a3e"))
STEPS = [
    ("① See input", "the content we put in front of it",
     "the goal first, then the rest: what we control;\nthe model's own knowledge is not given here", IN, [
         ("Goal · how much is set", ["the aim only", "aim + rules", "aim + rules + criteria"]),
         ("Goal · for whom", ["everyone", "one segment", "one person"]),
         ("Information · whose", ["ours", "other people's", "the people it is for"]),
         ("Information · form", ["raw data", "overall performance", "detailed evidence", "actionable insights",
                                 "a theory or rule", "the delivery setting", "the trial's outcome"]),
         ("Examples", ["a few good designs", "past designs + outcomes", "one design to revise"]),
         ("Tools", ["code to analyse data", "search", "a reader simulator"]),
         ("Reading", ["as given", "summarise first", "analyse with code"]),
         ("From the last unit", ["the last output"])]),
    ("② Reason ideas", "the content meets the brain: propose ideas",
     "each idea: its move and its source(s);\nall frozen before any design is made", ID, [
         ("How many", ["N ideas", "N + 5, then keep N"]),
         ("Who proposes", ["one planner agent", "several agents", "a person + an agent"]),
         ("Ideas come from", ["the model's own knowledge", "analysis of our data", "theory and literature",
                              "past designs", "the people it is for"]),
         # what the analysis is, and who made it when (JL 261005: an agent that calls the Insight agent
         # makes its own DIKW analysis): two axes, not one
         ("Analysis · form", ["performance numbers", "an analysis report", "DIKW insights"]),
         ("Analysis · made by", ["given: made before, checked", "itself, with code", "it calls the Insight agent"]),
         ("Spread", ["distinct in principle", "variations of one idea", "one element at a time"])]),
    ("③ Conduct process", "for each idea: the input + that idea",
     "one design per idea, made once:\nno iteration inside the unit", PR, [
         ("Reasoning style", ["direct (one shot)", "freestyle", "element-wise"]),
         ("Depth", ["little thinking", "a lot of thinking"]),
         ("Maker", ["one agent per idea", "one agent for all", "a person + an agent"]),
         ("Sees", ["its own idea only", "all the ideas"])]),
    ("④ Review item", "each design on its own",
     "checks only what this unit may see;\nnever another unit's input", CK, [
         ("Held against", ["the rules", "its idea", "its own claim", "readers' reactions"]),
         ("Who checks", ["a script", "the same agent", "a different agent", "an expert"]),
         ("How it judges", ["one verdict", "a reasoned critique", "element by element"]),
         ("Returns", ["pass · fail · unresolved", "notes for the next unit"])]),
    ("⑤ Review whole", "all the designs together",
     "ranks and predictions are frozen\nbefore the trial", OV, [
         ("Ranks by", ["predicted click-through", "a judge's comparison", "simulated readers", "real readers"]),
         ("Who ranks", ["a different agent", "an expert", "a panel of agents"]),
         ("Keeps", ["all N", "the top N of N + 5", "one per kind of idea"]),
         ("Gives back", ["a ranking", "predicted click-through + interval", "the kept set"])]),
]

EMOJI = {
    "the aim only": "🎯", "aim + rules": "📋", "aim + rules + criteria": "✅",
    "everyone": "🌍", "one segment": "🧩", "one person": "👤",
    "ours": "🏠", "other people's": "📚", "the people it is for": "🙋",
    "raw data": "🧾", "overall performance": "📊", "detailed evidence": "🔬", "actionable insights": "🔏",
    "a theory or rule": "📖", "the delivery setting": "🚚", "the trial's outcome": "🧪",
    "a few good designs": "⭐", "past designs + outcomes": "📁", "one design to revise": "✏",
    "code to analyse data": "💻", "search": "🔎", "a reader simulator": "🎭",
    "as given": "📄", "summarise first": "🗒", "analyse with code": "🧮", "the last output": "↩",
    "N ideas": "🔟", "N + 5, then keep N": "➕", "one planner agent": "🧭", "several agents": "👥",
    "a person + an agent": "🤝", "the model's own knowledge": "🧠", "analysis of our data": "📊",
    "theory and literature": "📖", "past designs": "📁",
    "performance numbers": "📈", "an analysis report": "🔬", "DIKW insights": "🔏",
    "given: made before, checked": "📥", "itself, with code": "🧮", "it calls the Insight agent": "🤖",
    "distinct in principle": "🌈", "variations of one idea": "🎨", "one element at a time": "🧱",
    "direct (one shot)": "⚡", "freestyle": "🌀", "element-wise": "🧱", "little thinking": "💭",
    "a lot of thinking": "💡", "one agent per idea": "🤖", "one agent for all": "🦾",
    "its own idea only": "🙈", "all the ideas": "👀",
    "the rules": "📜", "its idea": "🎯", "its own claim": "🔗", "readers' reactions": "😊",
    "a script": "⚙", "the same agent": "🪞", "a different agent": "🔀", "an expert": "🎓",
    "one verdict": "🔨", "a reasoned critique": "📝", "element by element": "🔬",
    "pass · fail · unresolved": "🚦", "notes for the next unit": "📨",
    "predicted click-through": "🔮", "a judge's comparison": "⚖", "simulated readers": "🎭", "real readers": "👥",
    "a panel of agents": "🗳", "all N": "📦", "the top N of N + 5": "🏆", "one per kind of idea": "🌈",
    "a ranking": "📶", "predicted click-through + interval": "🔮", "the kept set": "📦",
}
label = lambda o: f"{EMOJI.get(o, '•')} {o}"

# the methods: the Stage 2.5 arms, each only the choices that make it ---------------------------------
SHARED = [("How many", "N + 5, then keep N"), ("Who proposes", "one planner agent"),
          ("Spread", "distinct in principle"),
          ("Reasoning style", "freestyle"), ("Maker", "one agent per idea"), ("Sees", "its own idea only"),
          ("Held against", "its idea"), ("Who checks", "a different agent"),
          ("Ranks by", "predicted click-through"), ("Keeps", "the top N of N + 5")]
METHODS = [
    ("M01 · Goal only", "the more-shots baseline", "#1971c2",
     [("Goal · how much is set", "aim + rules + criteria"), ("Reading", "as given"),
      ("Ideas come from", "the model's own knowledge")] + SHARED,
     "Ideas from the goal and the model's own knowledge alone: what the LLM brings without our data."),
    ("M02 · Overall performance", "+ how each message did", "#0c8599",
     [("Information · whose", "ours"), ("Information · form", "overall performance"), ("Reading", "as given"),
      ("Ideas come from", "the model's own knowledge"), ("Ideas come from", "analysis of our data"),
      ("Analysis · form", "performance numbers"), ("Analysis · made by", "given: made before, checked")] + SHARED,
     "The same, with each Stage 1 message's rate, n and uncertainty to draw ideas from."),
    ("M03 · Detailed evidence", "+ the descriptive analysis", "#7048e8",
     [("Information · whose", "ours"), ("Information · form", "detailed evidence"), ("Reading", "as given"),
      ("Ideas come from", "the model's own knowledge"), ("Ideas come from", "analysis of our data"),
      ("Analysis · form", "an analysis report"), ("Analysis · made by", "given: made before, checked")] + SHARED,
     "The same, with the analysis report (element links, subgroups, limits): an idea may cite a row, never as a cause."),
    ("M04 · Actionable insights", "+ advice on that evidence", "#2b8a3e",
     [("Information · whose", "ours"), ("Information · form", "actionable insights"), ("Reading", "as given"),
      ("Ideas come from", "the model's own knowledge"), ("Ideas come from", "analysis of our data"),
      ("Analysis · form", "DIKW insights"), ("Analysis · made by", "given: made before, checked")] + SHARED,
     "The same, with the DIKW insights (claims, advice, limits); advice is used as the planner judges, never forced."),
    ("M05 · Raw-data agent", "benchmark: analyses, then designs", "#c2255c",
     [("Information · whose", "ours"), ("Information · form", "raw data"), ("Tools", "code to analyse data"),
      ("Reading", "analyse with code"), ("Ideas come from", "the model's own knowledge"),
      ("Ideas come from", "analysis of our data"), ("Analysis · form", "an analysis report"),
      ("Analysis · made by", "itself, with code")] + SHARED,
     "Reads the raw data with code, keeps its analysis, then proposes ideas from its own findings."),
]

# layout ---------------------------------------------------------------------------------------------
X0, BW, BGAP = 290, 370, 34               # first bucket, a bucket's width, the gap between buckets
bx = [X0 + i * (BW + BGAP) for i in range(len(STEPS))]
step_of = {p: si for si, st in enumerate(STEPS) for p, _ in st[4]}
opts_of = {p: o for st in STEPS for p, o in st[4]}
text(40, 24, "One design unit · See input → Reason ideas → for each idea: Conduct process → Review item → Review whole",
     30)
text(40, 66, "Above: every choice, each step's parts as rows. Below: one row per method, holding only the choices that "
             "make it; a part left out is not used.", 17, "#495057")

TOP = 150
part_y, part_end, cat_bottom = {}, {}, TOP
for si, (title, sub, band, (bg, st), parts) in enumerate(STEPS):
    x = bx[si]
    box(x, TOP, BW, 64, bg="#343a40", stroke="#343a40")
    text(x + 14, TOP + 7, title, 22, "#ffffff")
    text(x + 14, TOP + 40, sub, 13, "#dee2e6")
    box(x, TOP + 74, BW, 52, bg="#fff9db", stroke="#e67700", style="dashed")
    text(x + 12, TOP + 83, band, 13, "#343a40")
    y = TOP + 142
    for pname, opts in parts:
        part_y[pname] = y
        text(x, y, pname, 14, st if st != "#495057" else "#1e1e1e")
        y = chips(x, y + 22, x + BW, [label(o) for o in opts], bg, st)
        part_end[pname] = y
        y += 16
    cat_bottom = max(cat_bottom, y)
    if si < len(STEPS) - 1:
        polyline([(x + BW + 4, TOP + 32), (bx[si + 1] - 4, TOP + 32)], "#495057", sw=2.5, head=True)

# ③ and ④ run once per idea: one dashed frame around both
fx0, fx1 = bx[2] - 14, bx[3] + BW + 14
box(fx0, TOP - 44, fx1 - fx0, cat_bottom - TOP + 60, bg="transparent", stroke="#7048e8", style="dashed", sw=2)
text(fx0 + 12, TOP - 36, "for each idea · ×N (or N + 5)", 15, "#7048e8")

# the loop: what the unit gives back is the next unit's input
ly = cat_bottom + 40
rx = bx[4] + BW / 2
fy = part_y["From the last unit"] + 22 + CH / 2
polyline([(rx, part_end["Gives back"] + 8), (rx, ly), (X0 - 30, ly), (X0 - 30, fy), (X0 - 6, fy)],
         "#e67700", sw=3.5, head=True)
text(X0, ly + 10, "the loop: what the unit gave back (its designs, their checks, the ranking) is the next unit's input · "
                  "the trial's outcome comes in later as information, against the prediction", 15, "#e67700")

# the methods: one row each, only the choices that make it -------------------------------------------
RY = ly + 80
text(40, RY, "The methods · one row each, only the choices that make it (the Stage 2.5 arms)", 22)
SHORT = {"Goal · how much is set": "Goal", "Goal · for whom": "Goal", "Information · whose": "Information",
         "Information · form": "Information", "Examples": "Example", "Tools": "Tools", "Reading": "Reading",
         "From the last unit": "Last", "How many": "Ideas", "Who proposes": "Planner", "Ideas come from": "From",
         "Analysis · form": "Analysis", "Analysis · made by": "Made by",
         "Spread": "Spread", "Reasoning style": "Reasoning", "Depth": "Depth", "Maker": "Maker", "Sees": "Sees",
         "Held against": "Against", "Who checks": "Checker", "How it judges": "Judges", "Returns": "Returns",
         "Ranks by": "Ranks by", "Who ranks": "Ranker", "Keeps": "Keeps", "Gives back": "Gives back"}
y = RY + 46
for name, sub, colour, picks, explain in METHODS:
    for p, o in picks:
        assert o in opts_of[p], (name, p, o)
    rows = []
    for si, st in enumerate(STEPS):
        order = [q for q, _ in st[4]]
        mine = sorted((pk for pk in picks if step_of[pk[0]] == si), key=lambda pk: order.index(pk[0]))
        rows.append([f"{EMOJI.get(o, '•')} {SHORT[p]} · {o}" for p, o in mine])
    rh = max(lines(r, BW - 24) for r in rows) * (CH + 6) + 18
    box(40, y + rh / 2 - 26, 230, 52, bg="#ffffff", stroke=colour, sw=2.5)
    text(52, y + rh / 2 - 19, name, 15, colour)
    text(52, y + rh / 2 + 3, sub, 12, "#868e96")
    for si, items in enumerate(rows):
        bg, st = STEPS[si][3]
        box(bx[si], y, BW, rh, bg="transparent", stroke=colour, sw=1.5)
        if items:
            chips(bx[si] + 12, y + 12, bx[si] + BW - 12, items, bg, st)
        else:
            text(bx[si] + 14, y + 16, "nothing chosen", 13, "#adb5bd")
        x0 = 270 if si == 0 else bx[si - 1] + BW
        polyline([(x0 + 4, y + rh / 2), (bx[si] - 4, y + rh / 2)], colour, sw=2, head=True)
    text(bx[0] + 34, y + rh + 7, explain, 13, "#495057")
    y += rh + 44

# how to read it, once, at the bottom
y += 10
box(40, y, bx[-1] + BW - 40, 150, bg="#f8f9fa", stroke="#adb5bd")
text(58, y + 14, "How to read it", 17, "#343a40")
text(58, y + 44, "· ① is the content we give; the brain, the model's own knowledge, is always there and fixed by the model "
                 "snapshot; ② is where they meet, and each idea names its source(s)\n"
                 "· ③ and ④ run once per idea (the dashed frame): the input + one idea → one design → its own check\n"
                 "· ⑤ ranks every design together; with N + 5 ideas it keeps the best N · a chip names its part first\n"
                 "· an analysis has a form (numbers · a report · DIKW) and a maker: given, made before and checked, or "
                 "made inside the unit by the agent itself or by the Insight agent it calls (unsigned, frozen before ②)\n"
                 "· M01-M04 share the planner, the process and the checks and differ in ① and so in the analysis ② may "
                 "draw on; the brain is the same for all · M05 makes its own analysis", 14, "#495057")
y += 150

# never overwrite edits made on the canvas: an element saved from Excalidraw has a version above 1.
# Opening the canvas can re-save every element once (all at version 2, one timestamp); that is not an
# edit. Keep the previous file in the temp folder, and stop unless FORCE=1 is set.
if Path(OUT).is_file():
    old = json.load(open(OUT, encoding="utf-8"))
    live = [e for e in old.get("elements", []) if not e.get("isDeleted")]
    resaved = live and all(e.get("version") == 2 for e in live) and len({e.get("updated") for e in live}) == 1
    edited = [] if resaved else [e for e in live if e.get("version", 1) > 1]
    prev = Path(tempfile.gettempdir()) / (Path(OUT).name + ".prev")    # outside the repo
    shutil.copyfile(OUT, prev)
    if edited and os.environ.get("FORCE") != "1":
        sys.exit(f"{len(edited)} elements were edited on the canvas; kept {prev}. Fold the edits into "
                 "this script, or rerun with FORCE=1 to overwrite them.")
json.dump({"type": "excalidraw", "version": 2, "source": "haipipe-design-unit-studio", "elements": els,
           "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}},
          open(OUT, "w"), ensure_ascii=False, indent=2)
print(len(els), "elements; width", bx[-1] + BW + 40, "height", y)
