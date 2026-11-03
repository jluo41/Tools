"""b11 s05 · the insight workflow as slides, each one editable Excalidraw drawing (JL 261101: "How could you make the
slides version like that the labeling? You can try to use the excalidraw to do it").

b15 s03's deck is generated pictures; this one is drawn: one `idea-NN-<slug>.excalidraw` per slide, 1920 x 1080, each
a headline and one picture (a ladder, a grid, a chain, a loop), drawn through excalidraw-studio's draw.py, so a
person's marks survive a rebuild. Then each is rendered to its PNG, the topic's `s05-insight-workflow.slides.json`
records them, and haipipe-studio's topic_slides.py gathers them into the deck (.slides.html, .slides.pptx).
The words follow the topic's map (s05-insight-workflow-workflow.yaml) and haipipe-insight ref/insight-ladder.md.

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

INK, MUTED, BLUE, PURPLE, TEAL, ORANGE, RED, GREEN = ("#1e1e1e", "#75849a", "#1971c2", "#8563c6", "#2b8a3e",
                                                      "#d9480f", "#e03131", "#2f9e44")
FILL = {BLUE: "#e7f5ff", PURPLE: "#f3f0ff", TEAL: "#ebfbee", ORANGE: "#fff4e6", INK: "#ffffff", RED: "#fff5f5",
        MUTED: "#f8f9fa"}
W, H = 1920, 1080


class Slide(Drawing):
    def head(self, n, title, headline):
        self.box(0, 0, W, H, "#dee2e6", 1, "#ffffff")
        self.text(80, 56, f"{n:02d}", 28, MUTED)
        self.text(150, 48, title, 54, INK)
        self.para(152, 128, headline, 1600, 30, MUTED)

    def card(self, x, y, w, h, title, lines=(), color=INK, size=26, dashed=False):
        self.box(x, y, w, h, color, 2.4, FILL.get(color, "#ffffff"), dashed=dashed)
        yy = self.para(x + 24, y + 20, title, w - 48, size + 6, color)
        for ln in lines:
            yy = self.para(x + 24, yy + 8, ln, w - 48, size - 2, INK)
        return (x, y, w, h)

    def arrow(self, pts, color=BLUE, label="", lx=0, ly=0, dashed=False, size=24):
        self.line(pts, color, True, dashed, 2.6)
        if label:
            self.text(lx, ly, label, size, color)

    def foot(self, words):
        self.para(152, H - 96, words, 1600, 26, INK)


def s01(d):
    d.head(1, "What can one dataset say?", "Insight answers it a level at a time, and says how sure each answer is.")
    d.card(120, 420, 360, 300, "🗄️ one dataset", ["a frozen data folder", "its rows, its columns"], INK)
    steps = [("D · Data", "what was observed", TEAL), ("I · Information", "patterns, by cut", BLUE),
             ("K · Knowledge", "only what survives the cuts", PURPLE), ("W · Wisdom", "counsel, signed by you", ORANGE)]
    for k, (t, w_, c) in enumerate(steps):
        x, y = 640 + k * 300, 760 - k * 150
        d.card(x, y, 420, 130, t, [w_], c)
    d.arrow([(480, 570), (640, 820)], INK)
    d.card(1600, 130, 300, 130, "X · Executive", ["the plain answer"], RED)
    d.arrow([(1750, 310), (1750, 260)], RED)
    d.foot("Each level may say only what the level below supports; the Executive answer rests on all of them.")


def s02(d):
    d.head(2, "Two clocks, one Job per pair", "The plan moves in the Prototype, the data moves on the Board; each Job pins one of each.")
    d.text(700, 300, "F1 · first window", 30, MUTED)
    d.text(1200, 300, "F2 · whole record", 30, MUTED)
    d.text(260, 420, "AP1 · first plan", 30, MUTED)
    d.text(260, 680, "AP2 · adds events", 30, MUTED)
    d.card(660, 380, 380, 130, "j01", ["AP1 × F1 · start"], INK)
    d.card(1160, 380, 380, 130, "j02", ["AP1 × F2 · the data moved"], BLUE)
    d.card(1160, 640, 380, 130, "j03", ["AP2 × F2 · the code moved"], PURPLE)
    d.arrow([(1040, 445), (1160, 445)], BLUE, "data", 1060, 400)
    d.arrow([(1350, 510), (1350, 640)], PURPLE, "code", 1370, 560)
    d.card(660, 640, 380, 130, "AP2 × F1", ["not run"], MUTED, dashed=True)
    d.arrow([(860, 510), (1160, 700)], RED, "", dashed=True)
    d.text(500, 575, "✗ both clocks at once", 26, RED)
    d.foot("One clock at a time, so a changed answer has one cause: the data or the code.")


def chain(d, x, y, items, w=360, gap=70):
    boxes = []
    for k, (t, lines, c) in enumerate(items):
        bx = x + k * (w + gap)
        boxes.append(d.card(bx, y, w, 300, t, lines, c))
        if k:
            d.arrow([(bx - gap + 4, y + 150), (bx - 6, y + 150)], INK)
    return boxes


def s03(d):
    d.head(3, "A · Make the plan before any outcome is seen", "Questions, scripts and cuts are set and signed in the Prototype, then frozen.")
    chain(d, 120, 360, [("01 · Proposals", ["questions, fixes, cuts", "a batch at a time"], BLUE),
                        ("02 · Ask, plan the evidence", ["a question at its level", "its needs, each with a pass condition"], BLUE),
                        ("03 · Another agent agrees", ["the plan and the script", "by one that did not write them"], BLUE),
                        ("04 · 🙋 You set the cuts and sign", ["partitions and thresholds", "then the plan is frozen"], ORANGE)])
    d.foot("A Board runs only a signed plan; the cuts belong to it, never to the results.")


def s04(d):
    d.head(4, "B · One Run per question × cut", "Power is read before any contrast; a cut too thin is refused, and that refusal is an answer.")
    cols = ("full", "awake", "asleep", "cross")
    rows = [("D01 · what was observed", ("✅ ok", "·", "·", "·")), ("I01 · a pattern", ("✅ ok", "✅ ok", "🚫 refused", "·")),
            ("K01 · what holds", ("✅ ok", "✅ ok", "✅ ok", "pool?")), ("W01 · counsel", ("", "", "", ""))]
    x0, y0, cw = 560, 330, 300
    for j, c in enumerate(cols):
        d.text(x0 + j * cw + 20, y0, c, 30, MUTED)
    for i, (q, cells) in enumerate(rows):
        y = y0 + 70 + i * 120
        d.text(120, y + 30, q, 28, INK)
        if q.startswith("W01"):                    # no Run of its own: it cites the answers below it
            d.card(x0, y, 4 * cw - 30, 96, "no Run: it cites the answers below it", [], MUTED, 24)
        for j, cell in enumerate(cells):
            if cell == "·":
                d.text(x0 + j * cw + 20, y + 32, "not asked", 24, MUTED)
            elif cell:
                color = RED if "refused" in cell else PURPLE if "pool" in cell else TEAL if "ok" in cell else MUTED
                d.card(x0 + j * cw, y, cw - 30, 96, cell, [], color, 24)
    d.foot("run.sh reads the question and its script from the plan, the rows from the freeze, and writes only its result/.")


def s05(d):
    d.head(5, "Pool or split?", "When cuts disagree, one test across them decides whether the answer is one or two.")
    d.card(140, 360, 420, 160, "awake", ["one answer"], BLUE)
    d.card(140, 600, 420, 160, "asleep", ["another answer"], BLUE)
    d.card(760, 470, 380, 180, "Cross", ["one test of the difference"], PURPLE)
    d.arrow([(560, 440), (760, 530)], INK)
    d.arrow([(560, 680), (760, 600)], INK)
    for k, (t, w_, c) in enumerate((("POOL", "one answer for both", TEAL), ("SPLIT", "an answer per cut", ORANGE),
                                    ("UNDETERMINED", "not enough to say", MUTED))):
        d.card(1340, 300 + k * 200, 440, 160, t, [w_], c)
        d.arrow([(1140, 560), (1340, 380 + k * 200)], PURPLE)
    d.foot("A Knowledge question keeps only what survives this test.")


def s06(d):
    d.head(6, "C · Answer up the levels", "Each Task writes its page from its Runs; the levels go up in order, and X comes last.")
    lv = [("D", "observed", TEAL), ("I", "patterns", BLUE), ("K", "what holds", PURPLE), ("W", "counsel", ORANGE), ("X", "the plain answer", RED)]
    for k, (t, w_, c) in enumerate(lv):
        x = 120 + k * 350
        d.card(x, 420, 290, 220, t, [w_], c, 40)
        if k:
            d.arrow([(x - 56, 530), (x - 6, 530)], INK)
    d.foot("The page is the short answer; its answer-status walks open → partial → answered.")


def s07(d):
    d.head(7, "A second agent checks every page", "CHECK traces every number to its Run; alignment holds each answer to its question.")
    d.card(140, 400, 360, 220, "✍️ writer", ["writes the page", "from its Runs"], BLUE)
    d.card(680, 400, 360, 220, "📄 the page", ["the short answer", "how sure"], INK)
    d.card(1220, 400, 360, 220, "🔍 checker", ["another agent", "CHECK · alignment"], PURPLE)
    d.arrow([(500, 510), (680, 510)], INK)
    d.arrow([(1040, 510), (1220, 510)], INK)
    d.card(1220, 760, 360, 140, "✅ passes", ["checked: on the page"], TEAL)
    d.arrow([(1400, 620), (1400, 760)], TEAL)
    d.arrow([(1260, 400), (1260, 300), (320, 300), (320, 400)], PURPLE, "↩ returned with its reason: rewrite", 560, 250, True)
    d.foot("Nobody checks their own page.")


def s08(d):
    d.head(8, "D · What changed since the Job before?", "Each answer is held, changed, new, or dropped, and the moved clock says why.")
    d.card(120, 340, 520, 420, "j02 · AP1 × F2", ["D01 · one answer", "I01 · one answer", "K01 · one answer"], BLUE)
    d.card(840, 340, 520, 420, "j03 · AP2 × F2", ["D01 · held", "I01 · held", "K01 · changed: the code", "I06 · a new question"], PURPLE)
    d.arrow([(640, 550), (840, 550)], INK, "compare", 680, 500)
    d.card(1500, 340, 320, 200, "proposals", ["changes and gaps", "→ the next plan"], BLUE)
    d.arrow([(1360, 450), (1500, 440)], BLUE)
    d.card(1500, 600, 320, 200, "🙋 close j03", ["once every page", "is checked"], ORANGE)
    d.foot("A kept question that reruns on a code-moved Job is also a reproducibility check.")


def s09(d):
    d.head(9, "E · From answers to a signed handoff", "The Board reads across its Jobs; Design reads only a signed handoff, by its pair.")
    chain(d, 120, 380, [("closed Jobs", ["j01 · j02 · j03"], INK), ("read across", ["coverage, tracks", "the Board's questions"], BLUE),
                        ("Wisdom counsel", ["from the W answers"], PURPLE), ("🙋 you sign", ["the handoff, analysis plan × data freeze"], ORANGE)],
          w=330)
    d.card(1560, 760, 300, 140, "🎨 Design", ["reads it"], TEAL)
    d.arrow([(1700, 680), (1710, 760)], TEAL)
    d.foot("A handoff names its pair, so Design always knows which plan and which data it rests on.")


def s10(d):
    d.head(10, "Who does what", "Agents do thirteen of the sixteen steps; you act at three.")
    steps = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16"]
    you = {"04": "set cuts, sign the plan", "13": "close the Job", "16": "sign the handoff"}
    for k, s in enumerate(steps):
        x, y = 140 + (k % 8) * 210, 330 + (k // 8) * 220
        c = ORANGE if s in you else BLUE
        d.card(x, y, 170, 160, s, ["you" if s in you else "agent"], c, 30)
    d.para(140, 800, "🙋 04 set the cuts and sign the plan · 13 close each Job · 16 sign the handoff", 1600, 32, ORANGE)
    d.foot("Every other step is an agent's, and every one is checked by a second agent or a gate.")


def s11(d):
    d.head(11, "Still open", "Laying the steps beside the screens shows three gaps.")
    for k, (t, w_) in enumerate((("❓ Where is a question planned?", "steps 02 and 03 live in the Prototype; no Board or Job screen asks for a plan"),
                                 ("❓ The Board's own questions", "step 14 has no row on Board Work yet"),
                                 ("❓ A handoff before any Wisdom answer", "steps 15 and 16 wait on the counsel; the Handoff view has little to show"))):
        d.card(140, 300 + k * 220, 1640, 180, t, [w_], RED)


SLIDES = [("01", "one-dataset", "What can one dataset say?", s01), ("02", "two-clocks", "Two clocks, one Job per pair", s02),
          ("03", "make-the-plan", "A · Make the plan before any outcome", s03), ("04", "run-per-cut", "B · One Run per question × cut", s04),
          ("05", "pool-or-split", "Pool or split?", s05), ("06", "up-the-levels", "C · Answer up the levels", s06),
          ("07", "second-agent", "A second agent checks every page", s07), ("08", "what-changed", "D · What changed since the Job before?", s08),
          ("09", "handoff", "E · From answers to a signed handoff", s09), ("10", "who-does-what", "Who does what", s10),
          ("11", "still-open", "Still open", s11)]


def main():
    record = []
    for n, slug, idea, fn in SLIDES:
        d = Slide()
        fn(d)
        for i, e in enumerate(d.els):
            e["id"], e["roughness"] = f"s-05-slide{n}-{i}", 0      # "s-": a builder's own, so a rebuild redraws it
        canvas.assign_ids = lambda els: els
        out = HERE / f"idea-{n}-{slug}.excalidraw"
        d.write(out, "slides/build_slides.py")
        png = out.with_suffix(".png")
        subprocess.run([sys.executable, str(STUDIO / "render_png.py"), str(out), str(png), "1"], check=True,
                       stdout=subprocess.DEVNULL)
        record.append({"id": n, "idea": idea, "image": f"slides/{png.name}",
                       "source": f"slides/{out.name}"})
    spec = TOPIC / "s05-insight-workflow.slides.json"
    spec.write_text(json.dumps({"topic": TOPIC.name, "style": "excalidraw",
                                "source": "slides/build_slides.py: each slide one Excalidraw drawing, rendered to its PNG",
                                "slides": record}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    subprocess.run([sys.executable, str(STUDIO / "topic_slides.py"), str(TOPIC)], check=True)
    print(f"{len(record)} slides")


if __name__ == "__main__":
    main()
