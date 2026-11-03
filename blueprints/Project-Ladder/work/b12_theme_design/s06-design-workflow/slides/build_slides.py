"""b12 s06 · the design workflow as slides, each one editable Excalidraw drawing, drawn vivid (JL 261102: "we have the
workflow for the insight, could you make one for the design as well? try to make it to be vivid").

The same shape as b11 s05's deck: one `idea-NN-<slug>.excalidraw` per slide, 1920 x 1080, each a headline and one
picture (a fan, a fence, a loop, a walk, a cycle), drawn through excalidraw-studio's draw.py, so a person's marks
survive a rebuild. A design is drawn as a small phone with placeholder lines: a design prototype, never real content.
Then each is rendered to its PNG, `s06-design-workflow.slides.json` records them, and haipipe-studio's topic_slides.py
gathers them into the deck (.slides.html, .slides.pptx). The words follow the topic's map
(s06-design-workflow-workflow.yaml) and haipipe-design-workflow's routes and gates.

    python slides/build_slides.py
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPIC = HERE.parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
STUDIO = TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts"))
sys.path.insert(0, str(STUDIO))
from draw import Drawing, canvas  # noqa: E402

INK, MUTED, BLUE, PURPLE, TEAL, ORANGE, RED, GOLD = ("#1e1e1e", "#75849a", "#1971c2", "#8563c6", "#2b8a3e",
                                                    "#d9480f", "#e03131", "#e8b500")
FILL = {BLUE: "#e7f5ff", PURPLE: "#f3f0ff", TEAL: "#ebfbee", ORANGE: "#fff4e6", INK: "#ffffff", RED: "#fff5f5",
        MUTED: "#f8f9fa", GOLD: "#fff9db"}
MAKER, CHECKER, YOU = BLUE, PURPLE, ORANGE           # who does a step: the designer, the reviewer, a person
W, H = 1920, 1080


class Slide(Drawing):
    def head(self, n, title, headline):
        self.box(0, 0, W, H, "#dee2e6", 1, "#ffffff")
        self.text(80, 56, f"{n:02d}", 28, MUTED)
        self.text(150, 48, title, 54, INK)
        self.para(152, 128, headline, 1600, 30, MUTED)

    def card(self, x, y, w, h, title, lines=(), color=INK, size=26, dashed=False, sw=2.4):
        self.box(x, y, w, h, color, sw, FILL.get(color, "#ffffff"), dashed=dashed)
        yy = self.para(x + 24, y + 20, title, w - 48, size + 6, color)
        for ln in lines:
            yy = self.para(x + 24, yy + 8, ln, w - 48, size - 2, INK)
        return (x, y, w, h)

    def dot(self, cx, cy, r, color, words="", size=30):
        self.el("ellipse", cx - r, cy - r, 2 * r, 2 * r, strokeColor=color, strokeWidth=3,
                backgroundColor=FILL.get(color, "#ffffff"), fillStyle="solid")
        if words:
            lines = words.split("\n")
            ww = max(self.measure(ln, size) for ln in lines)
            self.text(cx - ww / 2, cy - len(lines) * size * 0.62, words, size, color)

    def phone(self, x, y, label, color=INK, mark="", w=150, h=250):
        """One design, drawn as a phone with placeholder lines; a mark (✅ ⭐ ❌ ✏️) on its corner."""
        self.box(x, y, w, h, color, 3, "#ffffff")
        self.box(x + 14, y + 30, w - 28, h - 70, MUTED, 1, FILL.get(color, "#f8f9fa"))
        for k, f in enumerate((0.8, 0.6, 0.7, 0.4)):
            self.line([(x + 28, y + 56 + k * 30), (x + 28 + (w - 56) * f, y + 56 + k * 30)], color, False, sw=4)
        self.el("ellipse", x + w / 2 - 9, y + h - 30, 18, 18, strokeColor=color, strokeWidth=2)
        self.text(x + 8, y + h + 10, label, 24, color)
        if mark:
            self.text(x + w - 30, y - 26, mark, 44, color)

    def arrow(self, pts, color=INK, label="", lx=0, ly=0, dashed=False, size=24, sw=2.6):
        self.line(pts, color, True, dashed, sw)
        if label:
            self.text(lx, ly, label, size, color)

    def pill(self, x, y, words, color, w=None, size=26):
        w = w or self.measure(words, size) + 44
        self.box(x, y, w, 58, color, 2.4, FILL.get(color))
        self.text(x + 22, y + 12, words, size, color)
        return x + w

    def who(self, x=1180, y=H - 100):
        for k, (c, words) in enumerate(((MAKER, "■ the designer agent"), (CHECKER, "■ the reviewer agent"), (YOU, "■ 🙋 you"))):
            self.text(x + k * 250, y, words, 24, c)

    def foot(self, words):
        self.para(152, H - 96, words, 1000, 26, INK)


def chain(d, x, y, items, w=360, gap=70, h=300):
    for k, (t, lines, c) in enumerate(items):
        bx = x + k * (w + gap)
        d.card(bx, y, w, h, t, lines, c)
        if k:
            d.arrow([(bx - gap + 4, y + h / 2), (bx - 6, y + h / 2)], INK)


def s01(d):
    d.head(1, "What does a design Job make?", "One goal × one method version × one inputs version → a set of designs; the Job pins all three.")
    for k, (t, w_, c) in enumerate((("🎯 the goal", "<the aim> · for <whom> · <channel> · how many", ORANGE),
                                    ("🧪 the method version", "a recipe in five steps · frozen", PURPLE),
                                    ("📦 the inputs version", "the Block's files, each fingerprinted · frozen", TEAL))):
        d.card(100, 300 + k * 190, 520, 150, t, [w_], c)
        d.arrow([(620, 375 + k * 190), (760, 560)], c, sw=3)
    d.dot(880, 560, 120, BLUE, "⚙️ a Job", 40)
    marks = ["⭐", "⭐", "", "⭐", "❌"]
    for k in range(5):
        x = 1100 + k * 160
        d.phone(x, 420, f"design {k + 1}", TEAL if marks[k] == "⭐" else MUTED, marks[k], w=130, h=220)
        d.arrow([(1000, 560), (x + 10, 530)], BLUE, sw=1.6)
    d.para(1100, 720, "five more ideas than the goal asks for become designs; the best are kept ⭐, each with a predicted "
                      "effect · the rest dropped ❌", 760, 26, INK)
    d.foot("A changed answer has one cause, because the Job froze all three before it started.")


def s02(d):
    d.head(2, "The goal comes first", "Written once at the Block, signed by you, then pinned by every Job that works on it.")
    d.card(100, 290, 600, 560, "🎯 the goal", ["aim: <the change for the person>", "for whom: <the audience>",
                                              "channel: <text message, email …>", "how many designs: <a number>",
                                              "its own rules: <beyond the shared>", "leave out: <what no design uses>",
                                              "signed: ✅ <date>, by you"], ORANGE, 28)
    steps = [("📋 the goal list", "board.md, Goals", ORANGE), ("🔒 a Job pins it", "a changed goal is a new goal", BLUE),
             ("🚧 in the fence", "inputs/goal.md: all the design work sees", TEAL),
             ("✅ checked on every design", "the rules check reads its rules", PURPLE),
             ("🏆 the ranking covers it", "the kept designs answer the aim", PURPLE)]
    for k, (t, w_, c) in enumerate(steps):
        y = 290 + k * 120
        d.card(860, y, 640, 100, t, [w_], c, 24, sw=2)
        d.arrow([(700, 560), (860, y + 50)], ORANGE, sw=1.6)
    d.card(1560, 290, 300, 280, "🙋 you sign it", ["once, at the Block", "only an unsigned goal", "may be edited"], YOU, 26)
    d.foot("On the screen: the Block's Goals view, and each Job's Setup view.")


def s03(d):
    d.head(3, "One change at a time", "A new goal, a new inputs version or a new method version is a new Job, never an edit.")
    d.text(620, 290, "inputs version 1", 32, MUTED)
    d.text(1140, 290, "inputs version 2 · a newer handoff", 32, MUTED)
    d.text(110, 410, "method version 2", 32, MUTED)
    d.text(110, 670, "method version 3", 32, MUTED)
    d.card(620, 370, 420, 140, "Job 1", ["the start"], INK)
    d.card(1140, 370, 420, 140, "Job 2", ["the inputs moved"], TEAL)
    d.card(1140, 630, 420, 140, "Job 3", ["the method moved"], PURPLE)
    d.arrow([(1040, 440), (1140, 440)], TEAL, "inputs", 1050, 390, sw=3)
    d.arrow([(1350, 510), (1350, 630)], PURPLE, "method", 1370, 555, sw=3)
    d.card(620, 630, 420, 140, "not run", ["both changed at once"], MUTED, dashed=True)
    d.arrow([(830, 510), (1140, 690)], RED, dashed=True)
    d.text(380, 560, "✗ two changes at once", 28, RED)
    d.card(1620, 370, 240, 400, "🔒", ["a released Job is never edited"], RED, 28)
    d.foot("Two Jobs on the same goal and inputs, with different method versions, are the comparison.")


def s04(d):
    d.head(4, "A · Set up the Block, once", "You sign the goal and the shared rules; an inputs version is frozen before any Job.")
    chain(d, 110, 360, [("🎯 write the goal", ["aim, for whom, channel,", "how many; 🙋 you sign it"], YOU),
                        ("📏 the shared rules", ["what every design keeps,", "checkable on the text; 🙋 you sign"], YOU),
                        ("📦 an inputs version", ["handoffs, theory, past designs,", "each file fingerprinted"], MAKER),
                        ("🧪 a method version", ["registered in the design skill,", "not written in the Block"], MAKER)], w=380, gap=60)
    d.who()
    d.foot("Every Block step writes a page; a person signs what matters.")


def s05(d):
    d.head(5, "B · Launch a Job behind a fence", "The Job copies the method, fences its inputs, and reasons its ideas only from what is inside.")
    d.card(110, 330, 330, 200, "🚀 launch a Job", ["goal × method version", "× inputs version"], MAKER)
    d.card(110, 600, 330, 200, "📌 pin all three", ["goal · method · inputs"], MAKER)
    d.arrow([(275, 530), (275, 600)], INK)
    d.box(560, 300, 760, 560, TEAL, 5, "#f4fcf5", dashed=True)
    d.text(590, 316, "🚧 the fence: inputs/", 32, TEAL)
    for k, f in enumerate(("the goal", "the method", "the handoff", "the file list, fingerprinted")):
        d.card(600, 380 + k * 100, 300, 80, f"📄 {f}", [], TEAL, 22, sw=1.6)
    d.card(960, 420, 320, 260, "💡 reason the ideas", ["each step of reasoning", "names its source:", "a fence file or", "own knowledge"], MAKER)
    d.arrow([(900, 520), (960, 540)], TEAL)
    d.arrow([(440, 700), (600, 600)], INK)
    d.card(1430, 420, 400, 260, "🔍 check the fence", ["another agent:", "is every source inside?", "pass → open the Tasks"], CHECKER)
    d.arrow([(1280, 550), (1430, 550)], INK)
    d.text(1440, 720, "✗ a source from outside the fence", 24, RED)
    d.who()
    d.foot("The fence never changes once the ideas are reasoned.")


def s06(d):
    d.head(6, "Every idea gets its Task", "Five more ideas than the goal asks for; opening never chooses: each becomes a design Task.")
    d.card(110, 380, 380, 360, "💡 Reason ideas", ["idea 1 · its short name", "idea 2 · its short name", "idea 3 · …",
                                                 "each with its chain", "and its source"], MAKER)
    for k in range(5):
        y = 290 + k * 128
        d.card(700, y, 500, 100, f"✏️ design {k + 1} · <its name>", [], BLUE, 24)
        d.arrow([(490, 560), (700, y + 50)], BLUE, sw=1.8)
        d.arrow([(1200, y + 50), (1410, 560)], MUTED, sw=1.6)
    d.dot(1560, 560, 150, CHECKER, "⚖️ Review\nthe whole", 34)
    d.foot("Choosing among the ideas is the ranking's job at the end, never the opening's.")


def s07(d):
    d.head(7, "C · Write one design: draft, check, redraft", "The designer drafts; another agent checks it; a failed check is a new draft, never an edit.")
    d.phone(140, 380, "first draft", BLUE, "✏️", w=200, h=330)
    d.card(520, 360, 420, 360, "🔍 check it", ["rules: every rule, on the text", "sources: each part names its own",
                                               "critique: read cold (if the method asks)", "never by the one who wrote it"], CHECKER)
    d.arrow([(340, 540), (520, 540)], INK, "write", 380, 490)
    d.card(1160, 300, 300, 160, "✅ passed", ["waits for the ranking"], TEAL)
    d.arrow([(940, 450), (1160, 380)], TEAL, "pass", 1020, 370, sw=3)
    d.card(1160, 620, 300, 160, "❌ failed", ["with its reasons"], RED)
    d.arrow([(940, 640), (1160, 700)], RED, "fail", 1030, 690, sw=3)
    d.phone(1600, 560, "second draft", BLUE, "✏️", w=170, h=270)
    d.arrow([(1460, 700), (1600, 700)], INK, "redraft", 1480, 650)
    d.arrow([(1685, 560), (1685, 270), (730, 270), (730, 360)], PURPLE, "↩ check the newest draft", 1000, 220, True, sw=3)
    d.who(152, H - 150)
    d.foot("Every design runs this loop at once.")


def s08(d):
    d.head(8, "A design's state walk", "Each design Task carries one state; only the steps after a Run move it.")
    walk = [("draft", MUTED), ("checking", CHECKER), ("redraft", RED), ("passed", TEAL), ("kept ⭐", GOLD), ("released 🚀", ORANGE)]
    x = 110
    for k, (st, c) in enumerate(walk):
        nx = d.pill(x, 480, st, c, size=32)
        if k < len(walk) - 1:
            d.arrow([(nx + 6, 509), (nx + 54, 509)], INK)
        if st == "redraft":
            rx = x
        if st == "checking":
            vx = x
        x = nx + 60
    d.arrow([(rx + 60, 538), (rx + 60, 620), (vx + 60, 620), (vx + 60, 538)], RED, "a new draft", vx + 80, 630, True)
    d.pill(1250, 690, "dropped ❌", MUTED, size=32)
    d.arrow([(1190, 540), (1300, 690)], MUTED, "the ranking, or you", 1260, 600)
    d.foot("A dropped design keeps its Task, folded, with its reason on its page.")


def s09(d):
    d.head(9, "Out of the fence is not a redraft", "When a fix needs something the fence does not hold, the design stops here.")
    d.phone(140, 390, "design 4", RED, "❓", w=200, h=330)
    d.card(470, 380, 520, 200, "the check says:", ["it needs a sender, a fact,", "or a newer handoff"], RED)
    d.arrow([(340, 540), (470, 480)], RED)
    d.card(1160, 300, 640, 180, "🙋 drop it", ["dropped, its reason on its page"], YOU)
    d.card(1160, 560, 640, 280, "📦 a new inputs version", ["holding what was missing", "→ a new Job runs it again",
                                                          "the inputs moved"], TEAL)
    d.arrow([(990, 460), (1160, 390)], INK, "or", 1060, 380)
    d.arrow([(990, 500), (1160, 680)], INK)
    d.foot("A redraft may use only the Job's fence; the fence never moves inside a Job.")


def s10(d):
    d.head(10, "D · Rank the passed, keep the best, predict", "Another agent ranks the passed designs, keeps as many as the goal asks, and predicts each one's effect.")
    cols = ("rank", "design", "predicted effect", "why", "kept")
    widths = (130, 200, 400, 440, 140)
    rows = [("1", "design 2", "+<x> points [<low>; <high>]", "<why it ranks here>", "⭐"),
            ("2", "design 1", "+<x> points [<low>; <high>]", "<why>", "⭐"),
            ("3", "design 4", "+<x> points [<low>; <high>]", "<why>", "⭐"),
            ("4", "design 3", "+<x> points [<low>; <high>]", "<why it is dropped>", "·")]
    x0, y0 = 240, 300
    d.box(x0 - 20, y0 - 20, sum(widths) + 40, 90 + 100 * len(rows), CHECKER, 2.4, FILL[CHECKER])
    xx = x0
    for c, w in zip(cols, widths):
        d.text(xx, y0, c, 30, CHECKER)
        xx += w
    for i, row in enumerate(rows):
        y = y0 + 80 + i * 100
        xx = x0
        for c, w in zip(row, widths):
            d.text(xx, y, c, 28 if c != "⭐" else 40, TEAL if row[-1] == "⭐" else MUTED)
            xx += w
    d.card(240, 840, 620, 120, "🧪 a pretest with readers", ["on the kept only, when the method asks"], CHECKER, 24)
    d.para(940, 850, "Always percentage points against the control, with a range, so every Job of the Block is scored side "
                     "by side; the why sits beside every number.", 900, 26, INK)


def s11(d):
    d.head(11, "🙋 Review and approve, then close", "One review, one sign: it freezes each kept design's prediction and releases them together.")
    for k in range(3):
        d.phone(110 + k * 190, 400, f"design {k + 1}", TEAL, "⭐", w=150, h=250)
    d.card(700, 330, 560, 380, "🙋 Review and approve", ["read each kept design as it reads,", "its prediction and its why;",
                                                        "tick, approve once", "(a button on the Job's Release view)"], YOU)
    d.arrow([(660, 520), (700, 520)], INK)
    d.card(1360, 300, 470, 170, "🧊 predictions frozen", ["the experiment is scored against them"], TEAL, 24)
    d.card(1360, 520, 470, 200, "🚀 the delivery", ["the designs, word for word", "and their screens"], TEAL, 24)
    d.arrow([(1260, 450), (1360, 385)], INK)
    d.arrow([(1260, 580), (1360, 615)], INK)
    d.dot(1590, 880, 100, YOU, "🔒 close", 30)
    d.para(940, 860, "then the close, once every design is released or dropped; you sign", 540, 26, YOU)
    d.foot("After the release the Job is read, never edited.")


def s12(d):
    d.head(12, "The Map: where Jobs are compared", "Goals down × methods across; each cell holds its chain of Jobs, one change each time.")
    cols = ("Goal only", "Actionable insights", "Raw-data agent")
    x0, y0, cw, rh = 400, 290, 480, 250
    for k, c in enumerate(cols):
        d.text(x0 + k * cw + 20, y0, "🧪 " + c, 28, PURPLE)
    for i, g in enumerate(("🎯 <the first goal>", "🎯 <the second goal>")):
        y = y0 + 60 + i * rh
        d.para(90, y + 70, g, 290, 28, ORANGE)
        for k in range(3):
            d.box(x0 + k * cw, y, cw - 30, rh - 30, MUTED, 1.4, "#ffffff")
    d.text(x0, y0 + 60 + 2 * rh - 10, "✅ released · ⭐ waits for your approval · ⏸ held · ✏️ designing", 24, INK)
    d.card(x0 + 20, y0 + 85, 410, 66, "Job 1 · version 2  ✅", [], TEAL, 21, sw=1.8)
    d.card(x0 + cw + 20, y0 + 85, 410, 66, "Job 2 · version 2  ✅", [], TEAL, 21, sw=1.8)
    d.card(x0 + cw + 20, y0 + 185, 410, 66, "Job 3 · version 3  ⭐", [], ORANGE, 21, sw=1.8)
    d.arrow([(x0 + cw + 225, y0 + 151), (x0 + cw + 225, y0 + 185)], PURPLE)
    d.card(x0 + 2 * cw + 20, y0 + 85, 410, 66, "Job 5 · version 2  ⏸", [], RED, 21, sw=1.8)
    d.card(x0 + 2 * cw + 20, y0 + 185, 410, 66, "Job 6 · version 3  ✏️", [], BLUE, 21, sw=1.8)
    for k in range(3):
        d.text(x0 + k * cw + 30, y0 + 60 + rh + 90, "· launch a Job", 24, MUTED)
    d.card(110, 900, 820, 120, "↔ two Jobs in one cell", ["what changed · passed · first try · time per passed"], PURPLE, 24)
    d.card(980, 900, 820, 120, "⏸ held: a Job that cannot run", ["its Hold says why; it stays, and a new version follows"], RED, 24)


def s13(d):
    d.head(13, "E · Learn: the experiment starts the next round", "What it returns lands once, at the Block, as totals per arm, and feeds the inputs and the method.")
    nodes = [("📤 released\n→ experiment", MUTED, 900, 300), ("📥 add totals\nper arm", MAKER, 1300, 480),
             ("⚖️ score\n(another agent)", CHECKER, 1150, 820), ("📦 next round:\nnew inputs", TEAL, 650, 820),
             ("🚀 new Jobs:\ninputs moved", MAKER, 500, 480)]
    for t, c, x, y in nodes:
        d.dot(x, y, 112, c, t, 26)
    for a_, b_ in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0)):
        (_, _, x1, y1), (_, _, x2, y2) = nodes[a_], nodes[b_]
        dx, dy = x2 - x1, y2 - y1
        n = (dx * dx + dy * dy) ** 0.5
        d.arrow([(x1 + dx / n * 122, y1 + dy / n * 122), (x2 - dx / n * 122, y2 - dy / n * 122)], INK, sw=3)
    d.text(750, 560, "predicted vs observed:\ndirection · in range", 28, CHECKER)
    d.card(1480, 600, 380, 170, "🏅 method scorecard", ["summed per method version;", "a loser is a reason to change"], CHECKER, 24)
    d.card(1480, 830, 380, 170, "🙋 sign a method change", ["the skill writes the next version", "→ a Job, the method moved"], YOU, 24)
    d.arrow([(1262, 790), (1480, 700)], CHECKER)
    d.arrow([(1670, 770), (1670, 830)], CHECKER)
    d.card(80, 860, 420, 150, "📝 questions and reports", ["and the one-page summary"], MAKER, 24)


def s14(d):
    d.head(14, "Who does what", "Eighteen steps: the designer agent makes nine, the reviewer agent checks four, you sign five.")
    names = ["goal", "rules", "inputs", "method", "launch", "pin", "ideas", "fence", "write",
             "check", "redraft", "rank", "approve", "close", "results back", "score", "report", "method change"]
    role = {1: YOU, 2: YOU, 13: YOU, 14: YOU, 18: YOU, 8: CHECKER, 10: CHECKER, 12: CHECKER, 16: CHECKER}
    for k, nm in enumerate(names):
        x, y = 110 + (k % 9) * 190, 290 + (k // 9) * 220
        c = role.get(k + 1, MAKER)
        d.card(x, y, 172, 170, str(k + 1), [nm, "you" if c == YOU else "checks" if c == CHECKER else "makes"], c, 26)
    d.para(140, 760, "🙋 you: the goal · the shared rules · review and approve · the close · a method change", 1640, 32, YOU)
    d.para(140, 830, "🔍 the reviewer agent: the fence · each design · the ranking · the score; never what it made", 1640, 30, CHECKER)
    d.para(140, 890, "✏️ the designer agent: the rest, each Run on its card", 1640, 30, MAKER)


def s15(d):
    d.head(15, "Still open", "Laying the steps beside the skills and the screens shows three gaps.")
    for k, (t, w_) in enumerate((("❓ Where is a method version written?", "in the Tools registry, outside any Job or Run; only the proposal is a Block step (s05 proposes a Task per version)"),
                                 ("❓ Who benches a new method version before its sign?", "the method skill says it is benched against the last version and checked by another agent; no Run does it yet"),
                                 ("❓ What is next?", "only the focus page works out each Job's next move; no script prints the next Run"))):
        d.card(140, 300 + k * 220, 1640, 180, t, [w_], RED)


SLIDES = [("01", "what-a-job-makes", "What does a design Job make?", s01), ("02", "the-goal", "The goal comes first", s02),
          ("03", "one-change", "One change at a time", s03), ("04", "set-up-block", "A · Set up the Block, once", s04),
          ("05", "fence", "B · Launch a Job behind a fence", s05), ("06", "idea-per-task", "Every idea gets its Task", s06),
          ("07", "draft-check-redraft", "C · Draft, check, redraft", s07), ("08", "state-walk", "A design's state walk", s08),
          ("09", "out-of-fence", "Out of the fence is not a redraft", s09), ("10", "rank-keep", "D · Rank, keep the best, predict", s10),
          ("11", "release", "Review and approve, then close", s11), ("12", "map", "The Map: where Jobs are compared", s12),
          ("13", "learn", "E · Learn: the experiment starts the next round", s13), ("14", "who-does-what", "Who does what", s14),
          ("15", "still-open", "Still open", s15)]


def main():
    record = []
    for n, slug, idea, fn in SLIDES:
        d = Slide()
        fn(d)
        for i, e in enumerate(d.els):
            e["id"], e["roughness"] = f"s-06-slide{n}-{i}", 0      # "s-": a builder's own, so a rebuild redraws it
        canvas.assign_ids = lambda els: els
        out = HERE / f"idea-{n}-{slug}.excalidraw"
        d.write(out, "slides/build_slides.py")
        png = out.with_suffix(".png")
        subprocess.run([sys.executable, str(STUDIO / "render_png.py"), str(out), str(png), "1"], check=True,
                       stdout=subprocess.DEVNULL)
        record.append({"id": n, "idea": idea, "image": f"slides/{png.name}", "source": f"slides/{out.name}"})
    spec = TOPIC / "s06-design-workflow.slides.json"
    spec.write_text(json.dumps({"topic": TOPIC.name, "style": "excalidraw",
                                "source": "slides/build_slides.py: each slide one Excalidraw drawing, rendered to its PNG",
                                "slides": record}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    subprocess.run([sys.executable, str(STUDIO / "topic_slides.py"), str(TOPIC)], check=True)
    print(f"{len(record)} slides")


if __name__ == "__main__":
    main()
