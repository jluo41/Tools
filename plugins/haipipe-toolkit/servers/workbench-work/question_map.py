"""question_map.py <Task Block> · draw the Block's question map into its studio/.

    .venv/bin/python Tools/plugins/haipipe-toolkit/servers/workbench-work/question_map.py \\
        <tasks/bNN_<block>>

Writes `<Block>/studio/question-map.excalidraw`, the first row of Scope › RoadMap Draw: one
frame per register group (one frame, Questions, when the register has none), and in it one row
per Question, left to right: the Question (id, title, the question), the Tasks its `work` names
(one line per Task folder, with the Jobs it runs in), and its report. A Task that serves another
Question too is marked "also" with that Question's id.

It is the Task family's twin of Insight's question map (haipipe-insight ref/question_map.py), in
the same drawing style. The drawing is generated (AGENTS.md rule 0): never edit it; change the
register in board.md and rerun this script. The workbench shows it view only and says when
board.md is newer than it. A hand sketch is its own drawing in the same studio/.
"""
import json
import random
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))   # beside task_questions.py (was studio/, 261007)
from task_questions import register, words   # noqa: E402

NAME = "question-map.excalidraw"
SOURCE = "workbench-work/question_map.py"
BLUE, INK, MUTED, RULE = "#1864ab", "#1e1e1e", "#495057", "#adb5bd"
FILLS = ("#e7f5ff", "#ebfbee", "#fff9db", "#f8f9fa", "#f3f0ff")
Q_W, W_W, R_W = 420, 620, 300                 # the three boxes of a row: Question, Work, Report
GAP, ROW_GAP, PAD, LINE = 70, 26, 32, 20       # between boxes, between rows, inside a frame, one Task line
WRAP = 46                                      # characters per line of the question


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

    def arrow(self, id_, x0, y0, x1, y1):
        e = self._base(id_, "arrow", x0, y0, abs(x1 - x0), abs(y1 - y0), stroke=BLUE, rounded=False)
        e.update(points=[[0, 0], [x1 - x0, y1 - y0]], lastCommittedPoint=None, startBinding=None,
                 endBinding=None, startArrowhead=None, endArrowhead="arrow", elbowed=False)
        return e

    def frame(self, id_, name, children, x, y, w, h):
        e = self._base(id_, "frame", x, y, w, h, stroke=RULE, rounded=False)
        e["name"] = name
        for c in children:
            c["frameId"] = id_
        return e


def questions(block: Path) -> list[dict]:
    """The register's Questions, each with its Task lines: (task folder, the Jobs it runs in)."""
    rows, _ = register((block / "board.md").read_text(encoding="utf-8"), "Questions", "questions")
    out = []
    for row in rows:
        tasks, paths = {}, set()
        for entry in row.get("work") or []:
            path = entry if isinstance(entry, str) else words((entry or {}).get("path"))
            job, _, task = path.partition("/")
            if task:
                tasks.setdefault(task, []).append(job.split("_", 1)[0])
                paths.add(path)
        report = words(row.get("report"))
        out.append({"id": words(row.get("id")), "group": words(row.get("group")) or "Questions",
                    "title": words(row.get("title")), "question": words(row.get("question")),
                    "tasks": tasks, "paths": paths, "report": Path(report).parent.name if report else ""})
    for q in out:                                   # the same Job/Task path named by another Question
        for task in q["tasks"]:
            mine = {p for p in q["paths"] if p.endswith("/" + task)}
            q.setdefault("also", {})[task] = [o["id"] for o in out if o is not q and mine & o["paths"]]
    return out


def draw(block: Path) -> dict:
    qs = questions(block)
    groups = list(dict.fromkeys(q["group"] for q in qs)) or ["Questions"]
    s = Scene(seed=len(qs) * 7919 + sum(len(q["tasks"]) for q in qs))
    s.text("title", 0, 0, f"{block.name} · question map", 30)
    s.text("lead", 0, 46, f"{len(qs)} Questions in {len(groups)} group{'s' if len(groups) != 1 else ''}. "
           "Each row reads left to right: the Question, the Tasks that answer it, its report.", 16, MUTED)
    s.text("source", 0, 72, f"Generated by {SOURCE} from the register in board.md: rerun it after the "
           "register changes, never edit this drawing.", 14, MUTED)
    y, frames = 150, []
    for g, group in enumerate(groups):
        fill, kids, top = FILLS[g % len(FILLS)], [], y
        y += PAD
        for q in (q for q in qs if q["group"] == group):
            lines = [f"{t.split('_', 1)[0]}  {t.split('_', 1)[-1]}  · {' '.join(jobs)}"
                     + (f"  · also {', '.join(q['also'][t])}" if q.get("also", {}).get(t) else "")
                     for t, jobs in q["tasks"].items()] or ["no Task: reasoning or existing evidence"]
            ask = textwrap.wrap(q["question"], WRAP)
            ask = ask[:3] if len(ask) <= 3 else ask[:2] + [ask[2].rstrip(" ,.;") + " …"]
            h = max(48 + len(ask) * 18, 24 + len(lines) * LINE, 96)
            x = PAD
            kids.append(s.rect(f"q-{q['id']}", x, y, Q_W, h, INK, fill))
            kids.append(s.text(f"q-{q['id']}-name", x + 14, y + 10, f"{q['id']}  {q['title']}", 17))
            kids.append(s.text(f"q-{q['id']}-ask", x + 14, y + 40, "\n".join(ask), 14, MUTED))
            wx = x + Q_W + GAP
            kids.append(s.rect(f"w-{q['id']}", wx, y, W_W, h, RULE if not q["tasks"] else INK, "#ffffff",
                               dashed=not q["tasks"]))
            kids.append(s.text(f"w-{q['id']}-tasks", wx + 14, y + 12, "\n".join(lines), 14, INK))
            rx = wx + W_W + GAP
            kids.append(s.rect(f"r-{q['id']}", rx, y, R_W, h, RULE if not q["report"] else INK, "#ffffff",
                               dashed=not q["report"]))
            kids.append(s.text(f"r-{q['id']}-name", rx + 14, y + 12,
                               ("report\n" + q["report"]) if q["report"] else "no report yet", 15))
            kids.append(s.arrow(f"a-{q['id']}-w", x + Q_W, y + h / 2, wx, y + h / 2))
            kids.append(s.arrow(f"a-{q['id']}-r", wx + W_W, y + h / 2, rx, y + h / 2))
            y += h + ROW_GAP
        y += PAD - ROW_GAP
        count = sum(1 for q in qs if q["group"] == group)
        frames.append((f"frame-{g}", f"{group} · {count} Question{'s' if count != 1 else ''}", kids, 0, top,
                       Q_W + W_W + R_W + 2 * GAP + 2 * PAD, max(y - top, 2 * PAD)))
        y += 60
    # frames last, over their children, as Excalidraw keeps them
    for args in frames:
        s.frame(*args)
    return {"type": "excalidraw", "version": 2, "source": SOURCE, "elements": s.elements,
            "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[0])
        return 2
    block = Path(argv[1]).resolve()
    if not (block / "board.md").is_file():
        print(f"{argv[1]}: not a Task Block (no board.md)")
        return 1
    out = block / "studio" / NAME
    out.parent.mkdir(exist_ok=True)
    scene = draw(block)
    out.write_text(json.dumps(scene, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    rows = sum(1 for e in scene["elements"] if e["type"] == "rectangle") // 3
    print(f"{rows} Questions · {sum(1 for e in scene['elements'] if e['type'] == 'frame')} groups → {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
