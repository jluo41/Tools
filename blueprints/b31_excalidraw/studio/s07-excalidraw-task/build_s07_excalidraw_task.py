"""s07 · excalidraw-task: s07-excalidraw-task.excalidraw (b31_excalidraw).

Four frames in two acts, each a screen or less, joined by named arrows (b31 s01 principles, ⑦ few words):
  1. the skill as a mind map (the ask, the idea frame, a frame per video, the checks, its words, its script, its limits);
  2. the workflow: the Task page and the face into task_drawing.py, then make, write, draw, check;
  3. the skill folder and the folder a Task topic lands in, as folder trees (both are real folders), and who owns what;
  4. the first Task it drew (Proj10 b01 s24), its preview, and check.py's verdicts on every Task topic in b01 and b51.
Every word is a yaml block of the face; facts (version, functions, tests, the Task topics' checks) are read on every
build. When Knowledge-Base is not beside Tools, frame 4 reads examples/ (the copy the last full build made). A rebuild
keeps whatever a person drew (canvas.write, a seed snapshot).

    python build_s07_excalidraw_task.py
"""
import ast
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = (HERE / "../../../..").resolve()                                   # the Tools SPACE
TOOLKIT = ROOT / "plugins/haipipe-toolkit"
sys.path.insert(0, str(TOOLKIT / "skills/1_base/display/excalidraw-studio/scripts"))
from draw import Drawing, T_NODE, INK, RED, W  # noqa: E402
from check import check  # noqa: E402

FACE = HERE / f"{HERE.name}.md"
SKILL = TOOLKIT / "skills/1_base/display/excalidraw-task"
EXAMPLES = HERE / "examples"


class Facts(dict):
    def __missing__(self, k):
        return "{" + k + "}"


def task_topics(block: Path) -> list[Path]:
    """The Block's topics whose face names a Task (`task:` yaml, excalidraw-task's)."""
    return [p for p in sorted((block / "studio").glob("s*/")) if p.is_dir() and
            re.search(r"```yaml\s*\ntask:", (p / f"{p.name}.md").read_text(encoding="utf-8")
                      if (p / f"{p.name}.md").is_file() else "")]


def first_tasks(y):
    """check.py on every Task topic of the first Blocks, and one preview copied into examples/; from examples/ when the
    source is away."""
    src = (ROOT / y["first"]["source"]).resolve()
    saved = EXAMPLES / "facts.json"
    pic = EXAMPLES / f"b01-{Path(y['first']['picture']).name}.png"
    if not src.is_dir():
        return json.loads(saved.read_text(encoding="utf-8")), pic
    EXAMPLES.mkdir(exist_ok=True)
    out = []
    for b in y["first"]["blocks"]:
        topics = task_topics(src / b)
        failing = []
        for t in topics:
            r = check(t / f"{t.name}.excalidraw")
            if any("❌" in f[p] for f in r["rows"] for p in ("①", "④", "⑤", "⑥", "⑦")) or "❌" in r["③"]:
                failing.append(t.name[:3])
        span = f"{topics[0].name[:3]} to {topics[-1].name[:3]}" if topics else "none"
        out.append(f"{'✅' if not failing else '❌'} {b[:3]}: {len(topics)} Task topics ({span}), " +
                   ("every check passes" if not failing else f"failing: {', '.join(failing)}"))
    saved.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    p = src / y["first"]["picture"]
    shutil.copyfile(p / f"{p.name}.png", pic)
    return out, pic


def facts():
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    src = (SKILL / "scripts/task_drawing.py").read_text(encoding="utf-8")
    tests = "".join(t.read_text(encoding="utf-8") for t in (SKILL / "tests").glob("test_*.py"))
    return Facts(version=re.search(r'version:\s*"([^"]+)"', skill).group(1),
                 n_funcs=sum(isinstance(n, ast.FunctionDef) for n in ast.parse(src).body),
                 n_tests=len(re.findall(r"def test_", tests)),
                 n_log=len(re.findall(r"^## \[", (SKILL / "CHANGELOG.md").read_text(encoding="utf-8"), re.M)))


def data():
    out = {}
    for block in re.findall(r"```yaml\n(.*?)\n```", FACE.read_text(encoding="utf-8"), re.S):
        out.update(yaml.safe_load(block))
    f = facts()

    def fill(x):
        if isinstance(x, str):
            return x.format_map(f)
        if isinstance(x, list):
            return [fill(i) for i in x]
        if isinstance(x, dict):
            return {k: fill(v) for k, v in x.items()}
        return x
    return fill(out), f


def mind_map(d, y):
    f = d.frame("① What it draws: the skill as one mind map", W, 1440)
    d.heading("🧠 What excalidraw-task draws", "a Task: its idea, then each video")
    bottom = d.mind_map(y["mindmap"]["centre"], y["mindmap"]["branches"])
    f["height"] = bottom + 40
    return f


def workflow(d, y):
    f = d.frame("② The workflow: a Task page to its frames", W, 1100)
    d.heading("🔁 From the Task page to its frames", "in and out; then one pass")
    d.text(40, 190, "In and out", T_NODE)
    top = d.flow(y["flow_in"]["steps"], 40, 250, W - 80, gap=90, title=34, leaf=28, labels=y["flow_in"]["labels"])
    ybot = top[0][1] + top[0][3] + 110
    d.text(40, ybot - 56, "One pass", T_NODE)
    bot = d.flow(y["flow_run"]["steps"], 40, ybot, W - 80, gap=90, title=34, leaf=28, labels=y["flow_run"]["labels"])
    yy = bot[0][1] + bot[0][3] + 40
    d.key(40, yy, W - 80, 120, 3)
    d.para(66, yy + 22, "Key point: the page keeps the full text; the face holds the short words a frame can show.",
           W - 132, T_NODE)
    f["height"] = yy + 150
    return f


def lines(d, x, y, rows, size):
    """Code lines kept as they are (a tree must not be re-wrapped)."""
    for i, ln in enumerate(rows):
        d.text(x, y + i * 34, ln, size, code=True)


def folders(d, y, fa):
    f = d.frame("③ Where it lives: its folder, where a Task topic lands, who owns the inputs", W, 900)
    d.heading("🧰 Its folder, where a Task topic lands, and who owns what it reads",
              "the left tree is read from disk; the middle one is where make writes a Task's topic; the right lists who "
              "owns each input, so a wrong frame is fixed at its source and redrawn, never edited")
    tree = d.folder_tree(SKILL, open_=("scripts", "tests"), notes={
        "task_drawing.py": f"{fa['n_funcs']} functions", "SKILL.md": f"rules, v{fa['version']}",
        "test_task_drawing.py": f"{fa['n_tests']} tests"})
    d.text(40, 190, "Read from disk: the skill folder", T_NODE)
    d.box(40, 250, 620, 30 + len(tree) * 34, INK, 2)
    lines(d, 60, 270, tree, 22)
    right = ["<Block>/", "├── jNN_<job>/", "│   └── tNN_<task>/", "│       ├── tNN_<task>.md   the page",
             "│       └── runs/rNN_<run>/", "└── studio/", "    └── sNN-tNN-<task>/",
             "        ├── sNN-tNN-<task>.md   task: yaml", "        └── build_sNN_tNN_<task>.py"]
    d.text(700, 190, "Where a Task topic is written", T_NODE)
    d.box(700, 250, 760, 30 + len(right) * 34, INK, 2)
    lines(d, 720, 270, right, 22)
    ym = 250 + 30 + len(right) * 34 + 24
    d.text(700, ym, "The face's short words", 30)
    ym += 50
    for ln in y["limits"]:
        ym = d.para(700, ym, "· " + ln, 760, 22) + 8
    d.text(1500, 190, "Who owns each input", T_NODE)
    yy = 250
    for ln in y["owners"]:
        yy = d.para(1500, yy, "· " + ln, W - 1540, 22) + 10
    d.text(1500, yy + 20, "Its three commands", 30)
    yy += 70
    for ln in y["commands"]:
        yy = d.para(1500, yy, "· " + ln, W - 1540, 22) + 8
    yk = max(ym, 250 + 30 + len(tree) * 34, yy) + 40
    key = "Key point: one Task, one topic of its Block; it reads the page and writes only its own topic."
    kh = Drawing.height(key, W - 132, 28) + 36                        # as tall as its words, no padding
    d.key(40, yk, W - 80, kh, 3)
    d.para(66, yk + 18, key, W - 132, 28)
    f["height"] = yk + kh + 24
    return f


def first(d, y):
    rows, pic = first_tasks(y)
    f = d.frame("④ What it made: the first Tasks drawn, Proj10 b01 and b51", W, 1500)
    d.heading("🖼️ The first Tasks it drew: Knowledge-Base's Proj10 b01 and b51",
              "the picture is b01 s24: entropy, cross-entropy and KL, its idea and then its six videos")
    h = d.picture(pic, 40, 190, 1500, 1100)
    xx = 1600
    d.text(xx, 190, "check.py on each, at this build", T_NODE)
    yy = 250
    for ln in rows:
        yy = d.para(xx, yy, ln, W - xx - 40, 26, RED if ln.startswith("❌") else INK) + 18
    yy += 24
    d.text(xx, yy, "Later, on them", T_NODE)
    yy += 56
    for ln in y["first"]["open"]:
        yy = d.para(xx, yy, ln, W - xx - 40, 26, RED if ln.startswith("❓") else INK) + 18
    key = ("Key point: each Task now says what each video told, in few words; before, a Job listed only its Runs' "
           "states.")
    kh = Drawing.height(key, W - xx - 92, T_NODE) + 48
    d.key(xx, yy + 24, W - xx - 40, kh, 3)
    d.para(xx + 26, yy + 44, key, W - xx - 92, T_NODE)
    f["height"] = max(190 + h, yy + 24 + kh) + 40
    return f


def main():
    y, fa = data()
    d = Drawing()
    fs = [mind_map(d, y), workflow(d, y), folders(d, y, fa), first(d, y)]
    for f in fs:
        d.fid = f["id"]
        d.badge(f)
    ids = dict(zip("①②③④", (f["id"] for f in fs)))
    acts = [{"name": a["name"], "frames": [ids[c] for c in a["frames"]], "arrow": a["arrow"]} for a in y["acts"]]
    b = y["between"]
    d.acts(acts, between=[(ids[b["from"]], ids[b["to"]], b["label"])])
    d.write(HERE / f"{HERE.name}.excalidraw", "build_s07_excalidraw_task.py")
    for f in fs:
        print(f["name"], f["width"], "x", f["height"])


if __name__ == "__main__":
    main()
