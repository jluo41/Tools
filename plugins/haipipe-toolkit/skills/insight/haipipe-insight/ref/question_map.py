"""question_map.py <Prototype board> · draw the Prototype's question map into its studio/.

    .venv/bin/python Tools/plugins/haipipe-toolkit/skills/insight/haipipe-insight/ref/question_map.py \\
        <insights/Prototype-Insight-<Topic>>

Writes `<Prototype>/studio/question-map.excalidraw` (prototype-contract.md § The Prototype):
one frame per rung, Data · Information · Knowledge · Wisdom, one box per live question (id,
name, the short question), and one arrow per reuse, from the question whose result is reused
to the question that reuses it (a `cite` need's `from: <L><NN>.E<n>`). A question that reuses
nothing on the board and that nothing reuses has a dashed box. Retired questions are left out;
each frame's name counts them.

The drawing is generated (AGENTS.md rule 8): never edit it, change a question file and rerun
this script. The workbench shows it view only and says when a question file is newer.
A hand sketch is its own drawing in the same studio/.
"""
import json
import random
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_question import RUNG_DIR, front, live_needs, question_folders   # noqa: E402

NAME = "question-map.excalidraw"
SOURCE = "haipipe-insight/ref/question_map.py"
RUNG = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
BLUE, GREEN, INK, MUTED, RULE = "#1864ab", "#2b8a3e", "#1e1e1e", "#495057", "#adb5bd"
FILL = {"D": "#f8f9fa", "I": "#e7f5ff", "K": "#ebfbee", "W": "#fff9db"}
BOX_W, BOX_H, BOX_GAP = 380, 96, 24          # one question box
COL_GAP, PAD = 240, 32                        # room between frames for the arrows
WRAP = 44                                     # characters per line of the short question


def questions(proto: Path) -> tuple[list[dict], dict[str, int]]:
    """Live questions in climbing order, each with the ids it reuses; and the retired count per rung."""
    live, retired = [], {k: 0 for k in RUNG}
    for folder in question_folders(proto):
        q, _ = front(folder / f"{folder.name}.md")
        letter = folder.name[0]
        if q.get("retired"):
            retired[letter] += 1
            continue
        uses = []
        for n in live_needs(q).values():
            src = n.get("from")
            if n.get("kind") == "cite" and isinstance(src, str) and src.split(".")[0] not in uses:
                uses.append(src.split(".")[0])
        live.append({"id": str(q.get("id") or folder.name[:3]), "letter": letter,
                     "name": str(q.get("name") or folder.name[4:]), "question": str(q.get("question") or ""),
                     "uses": uses})
    return live, retired


class Scene:
    def __init__(self, seed: int):
        self.rng, self.elements = random.Random(seed), []

    def _base(self, id_, type_, x, y, w, h, stroke=INK, bg="transparent", dashed=False, rounded=True):
        e = {"id": id_, "type": type_, "x": x, "y": y, "width": w, "height": h, "angle": 0,
             "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": 2,
             "strokeStyle": "dashed" if dashed else "solid", "roughness": 0, "opacity": 100,
             "groupIds": [], "frameId": None, "roundness": {"type": 3} if rounded else None,
             "seed": self.rng.randint(1, 2**31 - 1), "version": 1,
             "versionNonce": self.rng.randint(1, 2**31 - 1), "isDeleted": False,
             "boundElements": [], "updated": 1, "link": None, "locked": False}
        self.elements.append(e)
        return e

    def text(self, id_, x, y, s, size=16, color=INK):
        lines = s.split("\n")
        e = self._base(id_, "text", x, y, max(len(l) for l in lines) * size * 0.56, len(lines) * size * 1.25,
                       stroke=color, rounded=False)
        e.update(text=s, originalText=s, fontSize=size, fontFamily=8, textAlign="left", verticalAlign="top",
                 containerId=None, autoResize=True, lineHeight=1.25)
        return e

    def rect(self, id_, x, y, w, h, stroke=INK, bg="transparent", dashed=False):
        return self._base(id_, "rectangle", x, y, w, h, stroke, bg, dashed)

    def arrow(self, id_, points, color):
        x, y = points[0]
        rel = [[px - x, py - y] for px, py in points]
        e = self._base(id_, "arrow", x, y, max(abs(p[0]) for p in rel), max(abs(p[1]) for p in rel),
                       stroke=color, rounded=False)
        e.update(points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None,
                 startArrowhead=None, endArrowhead="arrow", elbowed=False)
        return e

    def frame(self, id_, name, children, x, y, w, h):
        e = self._base(id_, "frame", x, y, w, h, stroke=RULE, rounded=False)
        e["name"] = name
        for c in children:
            c["frameId"] = id_
        return e


def draw(proto: Path) -> dict:
    live, retired = questions(proto)
    ids = {q["id"] for q in live}
    edges = [(src, q["id"]) for q in live for src in q["uses"] if src in ids]
    linked = {a for e in edges for a in e}

    s = Scene(seed=len(live) * 7919 + len(edges))
    s.text("title", 0, 0, f"{proto.name} · question map", 30)
    s.text("lead", 0, 46, f"{len(live)} live questions · {len(edges)} reuse links. An arrow runs from a question "
           "to the question that reuses its result. A dashed box reuses nothing here and nothing here reuses it.", 16, MUTED)
    s.text("source", 0, 72, f"Generated by {SOURCE} from the question files: rerun it after a question changes, "
           "never edit this drawing.", 14, MUTED)

    top, box = 150, {}
    frames = []
    for col, letter in enumerate(RUNG):
        fx = col * (BOX_W + 2 * PAD + COL_GAP)
        rung = [q for q in live if q["letter"] == letter]
        kids = []
        for row, q in enumerate(rung):
            x, y = fx + PAD, top + PAD + row * (BOX_H + BOX_GAP)
            alone = q["id"] not in linked
            kids.append(s.rect(f"q-{q['id']}", x, y, BOX_W, BOX_H, RULE if alone else INK, FILL[letter], dashed=alone))
            kids.append(s.text(f"q-{q['id']}-name", x + 14, y + 10, f"{q['id']}  {q['name']}", 17))
            short = textwrap.wrap(q["question"], WRAP)
            short = short[:2] if len(short) <= 2 else [short[0], short[1].rstrip(" ,.;") + " …"]
            if short:
                kids.append(s.text(f"q-{q['id']}-ask", x + 14, y + 40, "\n".join(short), 14, MUTED))
            box[q["id"]] = (x, y, col)
        h = max(1, len(rung)) * (BOX_H + BOX_GAP) - BOX_GAP + 2 * PAD
        name = f"{RUNG[letter]} · {len(rung)} question{'s' if len(rung) != 1 else ''}"
        if retired[letter]:
            name += f" · {retired[letter]} retired"
        frames.append((f"frame-{RUNG[letter].lower()}", name, kids, fx, top, BOX_W + 2 * PAD, h))

    for n, (src, dst) in enumerate(edges):
        sx, sy, sc = box[src]
        dx, dy, dc = box[dst]
        if sc == dc:                                     # same rung: out on the right side and back in
            out = sx + BOX_W + 28 + 10 * (n % 4)
            pts = [[sx + BOX_W, sy + BOX_H / 2], [out, sy + BOX_H / 2], [out, dy + BOX_H / 2], [dx + BOX_W, dy + BOX_H / 2]]
            s.arrow(f"use-{src}-{dst}", pts, GREEN)
        else:
            s.arrow(f"use-{src}-{dst}", [[sx + BOX_W, sy + BOX_H / 2], [dx, dy + BOX_H / 2]], BLUE)

    # frames last, over their children, as Excalidraw keeps them
    for args in frames:
        s.frame(*args)
    return {"type": "excalidraw", "version": 2, "source": SOURCE, "elements": s.elements,
            "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[0])
        return 2
    proto = Path(argv[1]).resolve()
    if not any((proto / d).is_dir() for d in RUNG_DIR.values()):
        print(f"{argv[1]}: not a Prototype board (no rung folder)")
        return 1
    out = proto / "studio" / NAME
    out.parent.mkdir(exist_ok=True)
    scene = draw(proto)
    out.write_text(json.dumps(scene, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n_box = sum(1 for e in scene["elements"] if e["type"] == "rectangle")
    n_use = sum(1 for e in scene["elements"] if e["type"] == "arrow")
    print(f"{n_box} questions · {n_use} reuse links → {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
