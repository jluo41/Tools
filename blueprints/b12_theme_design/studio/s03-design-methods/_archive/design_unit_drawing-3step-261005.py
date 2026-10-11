"""Write the design-unit drawing (JL 261004): one design unit is See input → Conduct process →
Check output. Above, three buckets, one per step, with every choice: each step's parts as rows, the
part's options as chips ("for each step, what are the elements could be here"). Below, one row per
method, the same three buckets holding only the choices that make that method; a part left out is
not used ("we don't need to fill every slot"), so no option is "none". The rows are examples of how
a method reads, not the method cards. An author script; rerun it after a change, and fold any canvas
edit into it first.

    python3 design_unit_drawing.py design-unit-methods.excalidraw
"""
import json, os, random, shutil, sys, tempfile
from pathlib import Path
random.seed(11)
OUT = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).with_name("design-unit-methods.excalidraw"))
els = []


def base(kind, x, y, w, h, **kw):
    e = {"id": kw.pop("id", f"u{len(els):03d}"), "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": kw.pop("stroke", "#1e1e1e"), "backgroundColor": kw.pop("bg", "transparent"), "fillStyle": "solid",
         "strokeWidth": kw.pop("sw", 2), "strokeStyle": kw.pop("style", "solid"), "roughness": 0, "opacity": kw.pop("op", 100),
         "groupIds": [], "frameId": None, "roundness": kw.pop("round", {"type": 3}), "seed": random.randint(1, 2**30),
         "version": 1, "versionNonce": random.randint(1, 2**30), "isDeleted": False, "boundElements": [],
         "updated": 1791100000000, "link": None, "locked": False}
    e.update(kw); els.append(e); return e


FONT, CW = 6, 0.53                        # Nunito, about half an em per character


def text(x, y, s, size=16, color="#1e1e1e"):
    lines = s.split("\n")
    return base("text", x, y, max(len(l) for l in lines) * size * CW, len(lines) * size * 1.25, stroke=color,
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


# the steps, each split into its parts. A unit is one step (JL 261004: "from input to design to
# evaluation"): it sees once, makes one design once, checks it once. Seeing something new is the next
# unit, so iteration is a chain of units, and the last check is one more input ("the iteration means
# you can see something new"; "the input could be the last check, that is how we get the loop started").
STEPS = [
    ("① See input", "what the designer may use",
     "the goal comes first: what we will do and for whom;\nits rules: what to add, what to leave out",
     ("#e7f5ff", "#1864ab"), [
         ("Goal · how much is set", ["the aim only", "aim + rules (add, leave out)", "aim + rules + criteria"]),
         ("Goal · for whom", ["everyone", "one segment", "one person"]),
         ("Information · whose", ["ours", "other people's", "the people it is for"]),
         ("Information · form", ["raw data", "analysed results", "signed insights", "a theory or rule",
                                 "the delivery setting", "the trial's outcome"]),
         ("Examples", ["a few good designs", "past designs + outcomes", "one design to revise"]),
         ("Tools", ["code to analyse data", "search", "a reader simulator"]),
         # the output links back as the input (JL 261004: "if it is looped, output can be link back to
         # be the input"): one chip, the last unit's design and what its check returned
         ("From the last unit", ["the last output"])]),
    ("② Conduct process", "how the design is made",
     "one design, made once:\nno iteration inside the unit",
     ("#f8f9fa", "#495057"), [
         ("Reasoning style", ["direct (one shot)", "freestyle reasoning", "reframe first", "element-wise"]),
         ("Depth", ["little thinking", "a lot of thinking"]),
         ("Who makes it", ["one agent", "agents with roles", "a person + an agent"])]),
    ("③ Check output", "check this one design",
     "it also predicts its outcome,\nfrozen before the trial",
     ("#fff4e6", "#e67700"), [
         ("Held against", ["the rules", "its own claim", "a reviewer's judgment", "readers' reactions"]),
         ("Who checks", ["a script", "the same agent", "a different agent", "an expert", "simulated readers",
                         "real readers"]),
         ("How it judges", ["one verdict", "a reasoned critique", "element by element"]),
         ("What it returns", ["pass · fail · unresolved", "a score", "notes for the next unit"])]),
]

# one emoji per option (JL 261004: "for each item, add the emoji"; no "none" options: a part a method
# does not name is not used, and a unit with nothing From the last unit is a first unit)
EMOJI = {
    "the aim only": "🎯", "aim + rules (add, leave out)": "📋", "aim + rules + criteria": "✅",
    "everyone": "🌍", "one segment": "🧩", "one person": "👤",
    "ours": "🏠", "other people's": "📚", "the people it is for": "🙋",
    "raw data": "🧾", "analysed results": "📊", "signed insights": "🔏", "a theory or rule": "📖", "the delivery setting": "🚚",
    "a few good designs": "⭐", "past designs + outcomes": "📁", "one design to revise": "✏",
    "code to analyse data": "💻", "search": "🔎", "a reader simulator": "🎭",
    "the last output": "↩", "the trial's outcome": "🧪",
    "direct (one shot)": "⚡", "freestyle reasoning": "🌀", "reframe first": "🖼", "element-wise": "🧱",
    "little thinking": "💭", "a lot of thinking": "🧠",
    "one agent": "🤖", "agents with roles": "👥", "a person + an agent": "🤝",
    "the rules": "📜", "its own claim": "🔗", "a reviewer's judgment": "🧐", "readers' reactions": "😊",
    "a script": "⚙", "the same agent": "🪞", "a different agent": "🔀", "an expert": "🎓",
    "simulated readers": "🎭", "real readers": "👀",
    "one verdict": "🔨", "a reasoned critique": "📝", "element by element": "🔬",
    "pass · fail · unresolved": "🚦", "a score": "💯", "notes for the next unit": "📨",
}
label = lambda o: f"{EMOJI[o]} {o}"
# a row's chip names its part first (JL 261004: "Goal - xxx, information, Example, Tools, Last")
SHORT = {"Goal · how much is set": "Goal", "Goal · for whom": "Goal", "Information · whose": "Information",
         "Information · form": "Information", "Examples": "Example", "Tools": "Tools", "From the last unit": "Last",
         "Reasoning style": "Reasoning", "Depth": "Depth", "Who makes it": "Maker", "Held against": "Against",
         "Who checks": "Checker", "How it judges": "Judges", "What it returns": "Returns"}
row_label = lambda p, o: f"{EMOJI[o]} {SHORT[p]} · {o}"

# the methods (JL 261004: "we might have more about the design methods"): the old cards that fit one
# unit, then new ones; only the choices that make each, a part not named is not used. The colour is
# the family, by what the unit sees. By exploring (card 12) is several units side by side, not one.
GOAL_C, EXT_C, INT_C, NEW_C = "#1971c2", "#7048e8", "#2b8a3e", "#c2255c"
METHODS = [
    ("By goal · one shot", "card 01 · Goal Only", GOAL_C, [
        ("Goal · how much is set", "aim + rules (add, leave out)"), ("Reasoning style", "direct (one shot)"),
        ("Held against", "the rules"), ("Who checks", "a script")]),
    ("By principle", "card 02 · Goal Only", GOAL_C, [
        ("Goal · how much is set", "the aim only"), ("Reasoning style", "reframe first"),
        ("Depth", "a lot of thinking"), ("Held against", "a reviewer's judgment"),
        ("How it judges", "a reasoned critique")]),
    ("By slots", "card 13 · Goal Only", GOAL_C, [
        ("Examples", "one design to revise"), ("Reasoning style", "element-wise"), ("Depth", "little thinking"),
        ("Held against", "the rules"), ("How it judges", "element by element")]),
    ("By theory", "card 03 · External", EXT_C, [
        ("Information · whose", "other people's"), ("Information · form", "a theory or rule"),
        ("Reasoning style", "element-wise"), ("Held against", "its own claim"), ("Who checks", "a different agent")]),
    ("By implementation", "card 04 · External", EXT_C, [
        ("Information · whose", "other people's"), ("Information · form", "the delivery setting"),
        ("Reasoning style", "reframe first"), ("Held against", "the rules"), ("Who checks", "an expert")]),
    ("By insight", "card 05 · Internal", INT_C, [
        ("Information · whose", "ours"), ("Information · form", "signed insights"),
        ("Reasoning style", "element-wise"), ("Held against", "its own claim"),
        ("How it judges", "element by element")]),
    ("By theory and insight", "card 09 · Internal + External", INT_C, [
        ("Information · form", "signed insights"), ("Information · form", "a theory or rule"),
        ("Reasoning style", "element-wise"), ("Held against", "its own claim"), ("Who checks", "an expert")]),
    ("By precedent", "card 06 · Internal", INT_C, [
        ("Examples", "past designs + outcomes"), ("Reasoning style", "freestyle reasoning"),
        ("Held against", "its own claim")]),
    ("By revising", "card 07 · Internal", INT_C, [
        ("Examples", "one design to revise"), ("From the last unit", "the last output"),
        ("Reasoning style", "element-wise"), ("Held against", "its own claim"),
        ("What it returns", "notes for the next unit")]),
    ("By tailoring", "card 08 · Internal", INT_C, [
        ("Goal · for whom", "one segment"), ("Information · form", "analysed results"),
        ("Held against", "its own claim")]),
    ("By user test", "card 10 · a next unit", INT_C, [
        ("Examples", "one design to revise"), ("From the last unit", "the last output"),
        ("Held against", "readers' reactions"), ("Who checks", "simulated readers")]),
    ("By co-design", "card 11 · Internal", INT_C, [
        ("Information · whose", "the people it is for"), ("Who makes it", "a person + an agent"),
        ("Held against", "readers' reactions"), ("Who checks", "real readers")]),
    ("Agent analyses raw data", "new", NEW_C, [
        ("Goal · for whom", "one segment"), ("Information · form", "raw data"), ("Tools", "code to analyse data"),
        ("Reasoning style", "freestyle reasoning"), ("Depth", "a lot of thinking"),
        ("Held against", "its own claim"), ("Who checks", "a different agent")]),
    ("Agents with roles", "new", NEW_C, [
        ("Who makes it", "agents with roles"), ("Reasoning style", "element-wise"),
        ("Held against", "a reviewer's judgment"), ("Who checks", "a different agent")]),
    ("Learn from the trial", "new · a next unit", NEW_C, [
        ("Information · form", "the trial's outcome"), ("Information · form", "signed insights"),
        ("Depth", "a lot of thinking"), ("Held against", "its own claim"), ("What it returns", "a score")]),
]

# what each method does, in one plain sentence (JL 261004: "each method, to have an explanation"),
# written under its row
EXPLAIN = {
    "By goal · one shot": "Write the design straight from the goal and its rules, in one go; a script checks the rules.",
    "By principle": "First restate what the goal really asks, then design to that frame; a reviewer critiques it.",
    "By slots": "Take one design and change one element only, so the check can tell which element mattered.",
    "By theory": "Pick a named theory and build each part from the technique it prescribes; check the technique is there.",
    "By implementation": "Design for the real delivery setting from the start: who it reaches, who sends it; an expert checks the fit.",
    "By insight": "Build each part of the design from one of our signed insights; check each part cites a real insight.",
    "By theory and insight": "Use an insight from our data that a named theory also explains; an expert checks both are used.",
    "By precedent": "Start from our closest past design that worked, and adapt it to this goal.",
    "By revising": "Take the last design and its check, and change only what the check said to change; then loop.",
    "By tailoring": "Make the design for one segment, from what our analysis says about that segment.",
    "By user test": "Show the last design to readers, simulated here, and redraft on what they did; then loop.",
    "By co-design": "Design together with the people it is for; real readers judge the result.",
    "Agent analyses raw data": "Give the agent the raw data and code: it finds its own pattern, then designs; another agent re-checks it.",
    "Agents with roles": "Several agents, each with a role (writer, critic …), make the design; another agent reviews it.",
    "Learn from the trial": "Read the last trial's outcome beside our insights, think hard, design the next one, and score it.",
}

# layout: three buckets side by side (JL 261004: "make each column thinner"); inside one, a part is its
# name with its options as chips under it, wrapping
X0, BW, BGAP = 290, 470, 50                # first bucket, a bucket's width, the gap between buckets
CH, CGAP = 30, 8                           # a chip's height, the gap between chips
cw = lambda s, size=13: (len(s) + 1) * size * CW + 20          # a chip's width for its text; an emoji is wide
step_of = {p: si for si, st in enumerate(STEPS) for p, _ in st[4]}
opts_of = {p: o for st in STEPS for p, o in st[4]}
bx = [X0 + si * (BW + BGAP) for si in range(len(STEPS))]

text(40, 24, "One design unit · See input → Conduct process → Check output", 34)
text(40, 72, "Above: every choice, each step's parts as rows. Below: one row per method, holding only the choices "
             "that make it; a part left out is not used.", 17, "#495057")


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


TOP = 120
part_y = {}                                # part → the y of its row in the catalog
part_end = {}                              # part → the y under its last chip
cat_bottom = TOP
for si, (title, sub, always, (bg, st), parts) in enumerate(STEPS):
    x = bx[si]
    box(x, TOP, BW, 64, bg="#343a40", stroke="#343a40")
    text(x + 16, TOP + 7, title, 24, "#ffffff")
    text(x + 16, TOP + 40, sub, 14, "#dee2e6")
    box(x, TOP + 74, BW, 52, bg="#fff9db", stroke="#e67700", style="dashed")
    text(x + 12, TOP + 83, always, 13, "#343a40")
    y = TOP + 142
    for pname, opts in parts:
        part_y[pname] = y
        text(x, y, pname, 14, st if st != "#495057" else "#1e1e1e")
        y = chips(x, y + 22, x + BW, [label(o) for o in opts], bg, st)
        part_end[pname] = y
        y += 16
    cat_bottom = max(cat_bottom, y)

# the loop: the output links back as the input. The arrow leaves Check output's What it returns and
# lands on the one chip of From the last unit; the trial's outcome comes in later as information
ly = cat_bottom + 40
rx = bx[2] + BW / 2
fy = part_y["From the last unit"] + 22 + CH / 2
polyline([(rx, part_end["What it returns"] + 8), (rx, ly), (X0 - 30, ly), (X0 - 30, fy), (X0 - 6, fy)],
         "#e67700", sw=3.5, head=True)
text(X0, ly + 10, "the loop: a unit's output (its design and what its check returned) is the next unit's input ·\n"
                  "the trial's outcome, outside the unit, comes in later as information, against the prediction",
     15, "#e67700")

# the methods: one row each; its name on the left, then the three buckets with its choices only ------
RY = ly + 90
text(40, RY, "The methods · one row each, only the choices that make it", 22)
# rows stand apart, grouped by family under a heading (JL 261004: "these are nested together,
# separate them a bit"); the explanation is one box at the bottom, not a label on every loop
FAMILY = {GOAL_C: "Goal Only · the unit sees only the goal", EXT_C: "External Insights · it also sees other people's work",
          INT_C: "Internal Insights · it also sees our own work", NEW_C: "New · not a method card yet"}
y = RY + 30
last_colour = None
for name, sub, colour, picks in METHODS:
    if colour != last_colour:
        y += 26
        text(40, y, FAMILY[colour], 17, colour)
        y += 34
        last_colour = colour
    for p, o in picks:
        assert o in opts_of[p], (name, p, o)
    assert name in EXPLAIN, name
    rows = []
    for si, (_, _, _, (bg, st), _) in enumerate(STEPS):
        order = [q for q, _ in STEPS[si][4]]                 # in the catalog's part order
        mine = sorted((pk for pk in picks if step_of[pk[0]] == si), key=lambda pk: order.index(pk[0]))
        rows.append([row_label(p, o) for p, o in mine])
    # a row's height: the tallest bucket once its chips wrap (a dry run that draws nothing)
    def lines_needed(items):
        n, cx = 1, 0
        for s in items:
            w = cw(s) + CGAP
            if cx + w > BW - 24 and cx:
                n, cx = n + 1, 0
            cx += w
        return n
    rh = max(lines_needed(r) for r in rows) * (CH + 6) + 18
    box(40, y + rh / 2 - 26, 220, 52, bg="#ffffff", stroke=colour, sw=2.5)
    text(52, y + rh / 2 - 19, name, 15, colour)
    text(52, y + rh / 2 + 3, sub, 12, "#868e96")
    for si, items in enumerate(rows):
        bg, st = STEPS[si][3]
        box(bx[si], y, BW, rh, bg="transparent", stroke=colour, sw=1.5)
        if items:
            chips(bx[si] + 12, y + 12, bx[si] + BW - 12, items, bg, st)
        else:
            text(bx[si] + 14, y + 16, "nothing chosen", 13, "#adb5bd")
        x0 = 260 if si == 0 else bx[si - 1] + BW
        polyline([(x0 + 4, y + rh / 2), (bx[si] - 4, y + rh / 2)], colour, sw=2, head=True)
    text(bx[0] + 34, y + rh + 7, EXPLAIN[name], 13, "#495057")   # what it does, under the row
    # a method that reads the last output loops: its check's output back to its own input, at the
    # buckets' outer edges so the line passes beside the explanation, not through it
    if any(p == "From the last unit" for p, _ in picks):
        lo = y + rh + 36
        polyline([(bx[2] + BW - 24, y + rh + 2), (bx[2] + BW - 24, lo), (bx[0] + 16, lo), (bx[0] + 16, y + rh + 4)],
                 colour, sw=2, style="dashed", head=True)
        y += 18
    y += 26
    y += rh + 26

# the explanation, once, at the bottom
y += 14
box(40, y, bx[2] + BW - 40, 132, bg="#f8f9fa", stroke="#adb5bd")
text(58, y + 14, "How to read the rows", 17, "#343a40")
text(58, y + 44, "· the colour is the family, by what the unit sees: blue Goal Only · purple External Insights · "
                 "green Internal Insights · pink new\n"
                 "· a chip names its part first (Goal, Information, Example, Tools, Last · Reasoning, Depth, Maker · "
                 "Against, Checker, Judges, Returns)\n"
                 "· a dashed arrow under a row is a loop: the row's output is its next unit's input (Last · the last "
                 "output) · nothing chosen: the method does not set that step\n"
                 "· card 12 By exploring is several units side by side, each a different design, so it is not one row",
     14, "#495057")
y += 132

# never overwrite edits made on the canvas: an element saved from Excalidraw has a version above 1.
# Keep the previous file in the temp folder, and stop unless FORCE=1 is set.
if Path(OUT).is_file():
    old = json.load(open(OUT, encoding="utf-8"))
    edited = [e for e in old.get("elements", []) if not e.get("isDeleted") and e.get("version", 1) > 1]
    prev = Path(tempfile.gettempdir()) / (Path(OUT).name + ".prev")    # outside the repo
    shutil.copyfile(OUT, prev)
    if edited and os.environ.get("FORCE") != "1":
        sys.exit(f"{len(edited)} elements were edited on the canvas; kept {prev}. Fold the edits into "
                 "this script, or rerun with FORCE=1 to overwrite them.")
json.dump({"type": "excalidraw", "version": 2, "source": "haipipe-design-unit-studio", "elements": els,
           "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}},
          open(OUT, "w"), ensure_ascii=False, indent=2)
print(len(els), "elements; width", bx[-1] + BW + 40, "height", y)
