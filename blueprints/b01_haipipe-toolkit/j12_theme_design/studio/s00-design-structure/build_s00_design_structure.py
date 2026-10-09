"""b12 s00 · Design structure: s00-design-structure.excalidraw: the thinking behind the design ladder.

A design scratch (JL 261007: "for the design, the key thing is what is the design method, right?"), the
design side of b11's s00: what a design method is (five parts, from a generic card to a signed version);
the methods as their own work Block whose Jobs are method versions; the design Board whose Jobs pin a
goal, one method version and one inputs version; the clocks; where a new method version comes from and
what triggers it; and a Questions frame (the Block's register, read from board.md, with our ideas in
blue and the choices in pink).

Placeholders only (<project>, bNN_<app>, <goal>, m1, i1); ink and gray, red for what is open. The canvas
writer (haipipe-studio scripts/canvas.py) keeps every mark a person adds through a rebuild.

    python build_s00_design_structure.py [out.excalidraw]
"""
import random
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]                                   # b12_theme_design/
sys.path.insert(0, str(HERE.parents[3] / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio" / "_build"))
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402

random.seed(1)
HAND, MONO = 6, 3
INK, GRAY, RED = "#1e1e1e", "#868e96", "#e03131"
STICKY = {"ask": "#ffec99", "idea": "#d0ebff", "open": "#ffc9c9"}
els = []
FRAME = [None]


def base(kind, x, y, w, h, stroke=INK, bg="transparent", sw=2, dashed=False):
    e = {"id": f"t{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": sw,
         "strokeStyle": "dashed" if dashed else "solid", "roughness": 1, "opacity": 100, "groupIds": [],
         "frameId": FRAME[0], "roundness": {"type": 3} if kind == "rectangle" else None,
         "seed": random.randint(1, 2**31 - 1), "version": 1, "versionNonce": random.randint(1, 2**31 - 1),
         "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False}
    els.append(e)
    return e


def text(x, y, s, size=22, color=INK, font=HAND, container=None):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * size * (0.6 if font == MONO else 0.58)
    e = base("text", x, y, w, len(lines) * size * 1.25, color)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",
             containerId=container, autoResize=True, lineHeight=1.25)
    return e


def box(x, y, w, h, stroke=INK, bg="transparent", dashed=False, sw=2):
    return base("rectangle", x, y, w, h, stroke, bg, sw, dashed)


def sticky(x, y, w, body, kind, size=18):
    """A note the person can rewrite: its text is bound to it; sized to its text."""
    lines = []
    for para in body.split("\n"):
        line = ""
        for word in para.split():
            if line and len(line) + 1 + len(word) > (w - 32) / (size * 0.58):
                lines.append(line)
                line = word
            else:
                line = f"{line} {word}" if line else word
        lines.append(line)
    h = 30 + len(lines) * size * 1.3
    r = box(x, y, w, h, RED if kind == "open" else INK, STICKY[kind], sw=1)   # red = still open (no fills, 261007)
    t = text(x + 16, y + 14, "\n".join(lines), size, INK, container=r["id"])
    r["boundElements"] = [{"type": "text", "id": t["id"]}]
    return y + h


LINE = 16 * 1.55                                          # one tree line


def tree(x, y, rows, size=16, gap=430, title=None):
    """A folder tree: each row (path, its meaning); a meaning in red is open. Returns the bottom."""
    if title:
        text(x, y, title, 24)
        y += 44
    for i, (path, meaning) in enumerate(rows):
        text(x, y + i * size * 1.55, path, size, INK, MONO)
        if meaning:
            text(x + gap, y + i * size * 1.55 + 1, meaning, size - 1, RED if meaning.endswith("?") else GRAY)
    return y + len(rows) * size * 1.55


def arrow(pts, color=INK, dashed=False, label=None, label_at=None):
    x, y = pts[0]
    rel = [[px - x, py - y] for px, py in pts]
    e = base("arrow", x, y, max(abs(p[0]) for p in rel) or 1, max(abs(p[1]) for p in rel) or 1, color,
             dashed=dashed)
    e.update(points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None,
             startArrowhead=None, endArrowhead="arrow")
    if label:
        lx, ly = label_at or ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2 - 30)
        text(lx, ly, label, 17, color)


# ── 1 · a Design Project ─────────────────────────────────────────────────────────────────────────
PROJECT = [("<project>/", ""),
           ("├── README.md · project.yaml", "the Project's face; themes: work · designs · insights"),
           ("├── work/", "the work theme"),
           ("│   └── bNN_<app>_methods/", "the methods: each a recipe, versioned"),
           ("├── designs/", "the design theme"),
           ("│   └── bNN_<app>/", "the design Board: goals, inputs, Jobs, designs"),
           ("├── insights/   (optional)", "its signed Wisdom handoff is an input"),
           ("└── discoveries/   (optional)", "papers: theory, or a better procedure"),
           ("<outside>: the Exp", "released designs tested; results go to insights/"),
           ("", "one methods Block per design Board, or per Project ?")]

# ── 2 · what a design method is ─────────────────────────────────────────────────────────────────
PARTS = [("1 · See input", "which inputs it reads: goal · rules · theory · handoff · precedent"),
         ("2 · Reason ideas", "its kind of reasoning: deduce from theory · learn from data · analogy · explore"),
         ("3 · Conduct", "the procedure: the generate prompt, N, how far apart the N must be"),
         ("4 · Check each", "T0 rules · T1 fidelity (each element names its source) · T2 critique · T3 pretest"),
         ("5 · Check overall", "the N together: they cover the goal and are not alike")]
LAYERS = [("a card (the Guide)", "generic: 13 cards in\n3 families, no app"),
          ("a method version mN", "this app: inputs named,\nprompt written, checks\ncoded, a bench"),
          ("a Job pins mN", "path + hash; never\na copy, never edited")]

# ── 3 · the two Blocks: a box, its definition, its tree ─────────────────────────────────────────
METHODS = ("bNN_<app>_methods/", "work theme: each method made per version, benched, signed", [
    ("├── board.md", "kind: methods · serves: designs/bNN_<app>"),
    ("├── proposals/", "backlog: new · fix · retire"),
    ("├── bench/", "fixed goals + inputs: versions compare"),
    ("├── j01_by-insight_m1/", "Job = one method's version, frozen"),
    ("│   ├── method.md", "the five parts, from card 05"),
    ("│   ├── prompts/", "part 3: the generate steps"),
    ("│   ├── checks/", "parts 4-5: T0 · T1 as code or rubric"),
    ("│   └── runs/", "soft: write · bench · review · sign"),
    ("├── j02_by-theory_m1/", "another method, its first version"),
    ("└── j03_by-insight_m2/", "only what changed, + release.yaml")])
BOARD = ("bNN_<app>/", "design theme: one app, one channel, its goals and the designs", [
    ("├── board.md", "app · channel · the goal list"),
    ("├── inputs/", "rules · theory · handoff: version iM"),
    ("├── reports/qNN_<topic>/", "answers across Jobs: which method wins"),
    ("├── j01_<goal>_<design-method>/", "Job = goal x m1 x i1, frozen"),
    ("│   ├── j01_<goal>_<design-method>.md", "pins: method j01 (hash) · inputs i1"),
    ("│   ├── runs/", "commission · generate N (hard)"),
    ("│   └── t01_d01_<slug>/", "one design: elements.yaml"),
    ("│       └── runs/", "verify (hard) · revise (soft)"),
    ("├── j02_<goal>_<design-method>/", "inputs moved: i2 (a new handoff)"),
    ("├── j03_<goal>_<design-method>/", "method moved: m2"),
    ("├── j04_<goal>_<design-method>/", "a sibling: another method, same pair"),
    ("└── delivery/", "the released designs -> the Exp")])

# ── 5 · where a new method version comes from ──────────────────────────────────────────────────
TRIGGERS = [("checks fail often", "T0 · T1 in verify -> fix the conduct or the checks"),
            ("the N are alike", "check overall -> widen the conduct"),
            ("critique or pretest", "T2 · T3 find a pattern -> change the reasoning"),
            ("the Exp says it loses", "T4, read by insights/ -> rework or retire"),
            ("a paper suggests it", "Discovery: a better procedure, or a new method"),
            ("a new kind of input", "insight now answers K or W -> the method can read it")]
FLOW = ["proposals/\nthe backlog", "open jNN_<method>_mN+1\n(a version Job)", "write the five parts\nprompts · checks",
        "bench: mN+1 vs mN\nreviewed (another agent)", "sign (a person)\nclose = frozen",
        "design Board\nAdd a Job: mN+1 x latest"]
WHEN = ["when to cut a version ?", "  the bench shows a gain on the same goals and inputs",
        "  a batch of proposals agreed", "  on demand, by a person"]

# ── 6 · the Questions frame: the register, our ideas, the choices ───────────────────────────────
IDEAS = {"Q01": ("Board = goals + inputs + Jobs + designs; the methods are their own work Block; "
                 "Job = goal x method version x inputs version; Task = one design; Runs = generate, verify, revise.",
                 "Methods in their own work Block, or frozen inside each Job (method.md, as today)?"),
         "Q02": ("Description shows the pins (mN, iM); the Board's Audience Report compares Jobs on one goal: "
                 "methods side by side, versions over time.",
                 "Board Audience Report = goals down, methods across?"),
         "Q03": ("The handoff is an input: a new handoff moves the inputs clock, not the method; part 1 of a "
                 "method names which inputs it reads.",
                 "Does a newer handoff make a closed Job's designs stale?")}
PROPOSED = ("(proposed) Q04", "What is a design method, and how does it evolve?",
            "Five parts (see · reason · conduct · check each · check overall) + prompts + checks + a bench; "
            "triggers -> proposals/ -> the next version Job -> bench -> sign -> the Board adds a Job.",
            "Does the Guide's card grow to five parts? Is a version cut on a bench gain?")


def register():
    """The Block's questions, from board.md's `## Questions` yaml."""
    m = re.search(r"(?ms)^## Questions\s*\n```yaml\n(.*?)```", (BLOCK / "board.md").read_text(encoding="utf-8"))
    return yaml.safe_load(m.group(1))["questions"] if m else []


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s00-design-structure.excalidraw"
    text(0, 0, "Design structure: a method that evolves, a Board that runs it on goals and inputs", 40)
    text(0, 62, "Design scratch: placeholders only. Red = open. Draw anywhere; your marks stay through a rebuild.",
         20, GRAY)

    # 1 · the Project
    text(0, 160, "A Design Project", 30)
    tree(0, 220, PROJECT, gap=470)

    # 2 · what a design method is: its five parts, then card -> version -> pin
    mx = 1300
    text(mx, 160, "What a design method is: the key", 30)
    text(mx, 210, "a recipe, frozen per version: a goal + its inputs -> N designs", 20, GRAY)
    for i, (part, what) in enumerate(PARTS):
        y = 260 + i * 78
        box(mx, y, 280, 60)
        text(mx + 18, y + 16, part, 21)
        text(mx + 310, y + 18, what, 18, GRAY)
    text(mx, 660, "T4, the Exp, is not in the method: it is the Learning loop, read by insights/", 18, GRAY)
    text(mx, 694, "today the card has 3 parts (see · conduct · check) and the unit 5: one shape ?", 18, RED)
    lx = mx
    for k, (name, what) in enumerate(LAYERS):
        box(lx, 750, 330, 150, RED if k == 1 else INK)
        text(lx + 18, 764, name, 21, RED if k == 1 else INK)
        text(lx + 18, 806, what, 17, GRAY)
        if k < len(LAYERS) - 1:
            arrow([(lx + 340, 825), (lx + 420, 825)])
        lx += 430
    text(mx, 920, "the middle layer is new: where a method is made concrete and evolves", 18, RED)

    # 3 · the two Blocks
    by = 1060
    for k, (name, define, rows) in enumerate((METHODS, BOARD)):
        x = k * 1300
        box(x, by, 520, 70)
        text(x + 20, by + 18, name, 22, INK, MONO)
        text(x, by + 88, define, 18, GRAY)
        tree(x, by + 140, [(name, "")] + rows, gap=430)
    row = lambda i: by + 140 + i * LINE + 10                 # the middle of tree line i
    arrow([(1290, row(5)), (960, row(4))], INK, label="uses m1 (path + hash), never copies",
          label_at=(980, row(5) + 12))
    arrow([(1290, row(3)), (960, row(2))], INK, label="proposals: new · fix · retire",
          label_at=(980, row(1) - 40))

    # 4 · the clocks
    cy = by + 560
    text(0, cy, "One goal, two clocks; a Job pins one of each and is frozen once closed", 30)
    text(0, cy + 60, "method", 22)
    text(240, cy + 62, "m1  ->  m2 (a check fixed, the N wider)  ->  m3 …", 18, INK, MONO)
    text(0, cy + 110, "inputs", 22)
    text(240, cy + 112, "i1  ->  i2 (a new handoff)  ->  i3 (new rules) …", 18, INK, MONO)
    chain = [("j01 by-insight m1 i1", "start"), ("j02 by-insight m1 i2", "inputs moved"),
             ("j03 by-insight m2 i2", "method moved"), ("j04 by-theory m1 i2", "sibling: another method")]
    x = 0
    for k, (job, moved) in enumerate(chain):
        box(x, cy + 180, 470, 100, GRAY if k == 3 else INK, dashed=k == 3)
        text(x + 20, cy + 196, job, 20, INK, MONO)
        text(x + 20, cy + 236, moved, 18, GRAY)
        if k < 2:
            arrow([(x + 480, cy + 230), (x + 590, cy + 230)])
        x += 600
    text(0, cy + 310, "one clock per Job ?  then a change in the designs has one cause: new inputs, or a new method",
         20, RED)
    text(0, cy + 350, "comparing methods is a sibling Job on the same goal and inputs, never a version", 18, GRAY)

    # 5 · where a new method version comes from
    ty = cy + 470
    text(0, ty, "Where a new method version comes from: what triggers the evolving", 30)
    for i, (what, why) in enumerate(TRIGGERS):
        box(0, ty + 60 + i * 74, 300, 56, GRAY, sw=1)
        text(16, ty + 74 + i * 74, what, 19)
        text(320, ty + 76 + i * 74, why, 17, GRAY)
        arrow([(900, ty + 88 + i * 74), (1040, ty + 260)], GRAY)
    fx = 1060
    for k, step in enumerate(FLOW):
        red = "sign" in step or "bench" in step
        box(fx, ty + 220, 300, 90, RED if red else INK)
        text(fx + 18, ty + 236, step, 18, RED if red else INK)
        if k < len(FLOW) - 1:
            arrow([(fx + 305, ty + 265), (fx + 375, ty + 265)])
        fx += 380
    text(1060, ty + 340, "new inputs need no new version: a new handoff lands -> the Board adds a Job mN x iM+1",
         18, GRAY)
    for i, line in enumerate(WHEN):
        text(1060, ty + 400 + i * 30, line, 19 if i == 0 else 17, RED)

    # 6 · Questions frame: one row per question; the ask, our idea, the choice (open: red)
    qy = ty + 640
    fr = base("frame", -40, qy - 40, 10, 10, GRAY)
    fr["name"], fr["roundness"] = "Questions", None
    FRAME[0] = fr["id"]
    text(0, qy, "Questions: the Block's register (left), our idea (middle), your choice (right, in red)", 30)
    rows = [(q["id"], q["title"]) + IDEAS.get(q["id"], ("", "")) for q in register()]
    rows.append(PROPOSED)
    y = qy + 70
    for qid, title, idea, choice in rows:
        bottom = sticky(0, y, 520, f"{qid} · {title}", "ask")
        if idea:
            bottom = max(bottom, sticky(560, y, 640, idea, "idea"))
        if choice:
            bottom = max(bottom, sticky(1240, y, 560, choice, "open"))
        y = bottom + 30
    FRAME[0] = None
    kids = [e for e in els if e.get("frameId") == fr["id"]]
    fr.update(x=-40, y=qy - 40, width=max(e["x"] + e["width"] for e in kids) + 80 + 40,
              height=max(e["y"] + e["height"] for e in kids) - qy + 80)
    canvas.write(out, list(els), "build_s00_design_structure.py")


if __name__ == "__main__":
    main()
