"""s06 · excalidraw-job: s06-excalidraw-job.excalidraw (b31_excalidraw).

Four frames in two acts, each a screen or less, joined by named arrows (b31 s01 principles):
  1. the skill as a mind map (the ask, its two frames, a Task's detail, its words, its script, what it never does);
  2. the workflow: the Job's files into job_drawing.py, then what one build does, frame by frame;
  3. the skill folder and the folder a Job topic lands in, as folder trees (both are real folders), and who owns what;
  4. the first Job it drew (Proj10 b01 s21), its preview, and check.py's verdicts on b01 s21 to s23.
Every word is a yaml block of the face; facts (version, functions, tests, the first Jobs' checks) are read on every
build. When Knowledge-Base is not beside Tools, frame 4 reads examples/ (the copy the last full build made). A rebuild
keeps whatever a person drew (canvas.write, a seed snapshot).

    python build_s06_excalidraw_job.py
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
SKILL = TOOLKIT / "skills/1_base/display/excalidraw-job"
EXAMPLES = HERE / "examples"


class Facts(dict):
    def __missing__(self, k):
        return "{" + k + "}"


def first_jobs(y):
    """check.py on each first Job drawn, and its preview copied into examples/; from examples/ when the source is away."""
    src = (ROOT / y["first"]["source"]).resolve()
    saved = EXAMPLES / "facts.json"
    pic = EXAMPLES / f"b01-{y['first']['picture'].replace('-results', '')}.png"
    if not src.is_dir():
        return json.loads(saved.read_text(encoding="utf-8")), pic
    EXAMPLES.mkdir(exist_ok=True)
    out = []
    for t in y["first"]["topics"]:
        r = check(src / t / f"{t}.excalidraw")
        fails = sum("❌" in f[p] for f in r["rows"] for p in ("①", "④", "⑤", "⑥")) + ("❌" in r["③"])
        per = " · ".join(f"{f['words']} words" if f["kind"] == "map" else f"{f['per']}/{f['floor']}" for f in r["rows"])
        out.append(f"{'✅' if not fails else '❌'} {t[:3]} · {t[4:].replace('-results', '').replace('-', ' ')}: "
                   f"{r['frames']} frames, " + ("every check passes" if not fails else f"{fails} checks fail") +
                   f": {per}")
    builder = (src / y["first"]["topics"][0] / f"build_{y['first']['topics'][0].replace('-', '_')}.py").read_text()
    out.append("its builder calls job_drawing.draw" if "job_drawing.draw" in builder else "❌ its builder is not excalidraw-job's")
    saved.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    shutil.copyfile(src / y["first"]["picture"] / f"{y['first']['picture']}.png", pic)
    return out, pic


def facts():
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    src = (SKILL / "scripts/job_drawing.py").read_text(encoding="utf-8")
    tests = (SKILL / "tests/test_job_drawing.py").read_text(encoding="utf-8")
    return Facts(version=re.search(r'version:\s*"([^"]+)"', skill).group(1),
                 n_funcs=sum(isinstance(n, ast.FunctionDef) for n in ast.parse(src).body),
                 n_tests=len(re.findall(r"^def test_", tests, re.M)),
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
    d.heading("🧠 What excalidraw-job draws", "a Job, in two frames and few words")
    bottom = d.mind_map(y["mindmap"]["centre"], y["mindmap"]["branches"])
    f["height"] = bottom + 40
    return f


def workflow(d, y):
    f = d.frame("② The workflow: a Job on disk to two frames", W, 1100)
    d.heading("🔁 From the Job on disk to its two frames", "in and out; then one build")
    d.text(40, 190, "In and out", T_NODE)
    top = d.flow(y["flow_in"]["steps"], 40, 250, W - 80, gap=90, title=34, leaf=28, labels=y["flow_in"]["labels"])
    ybot = top[0][1] + top[0][3] + 110
    d.text(40, ybot - 56, "One build", T_NODE)
    bot = d.flow(y["flow_run"]["steps"], 40, ybot, W - 80, gap=90, title=34, leaf=28, labels=y["flow_run"]["labels"])
    yy = bot[0][1] + bot[0][3] + 40
    d.key(40, yy, W - 80, 120, 3)
    d.para(66, yy + 22, "Key point: every word comes from the Job on disk; the face adds the aim and the reading.",
           W - 132, T_NODE)
    f["height"] = yy + 150
    return f


def lines(d, x, y, rows, size):
    """Code lines kept as they are (a tree must not be re-wrapped)."""
    for i, ln in enumerate(rows):
        d.text(x, y + i * 34, ln, size, code=True)


def folders(d, y, fa):
    f = d.frame("③ Where it lives: its folder, where a Job topic lands, who owns the inputs", W, 900)
    d.heading("🧰 Its folder, where a Job topic lands, and who owns what it reads",
              "the left tree is read from disk; the middle one is where make writes a Job's topic; the right lists who "
              "owns each input, so a wrong frame is fixed at its source and redrawn, never edited")
    tree = d.folder_tree(SKILL, open_=("scripts", "tests"), notes={
        "job_drawing.py": f"{fa['n_funcs']} functions", "SKILL.md": f"rules, v{fa['version']}",
        "test_job_drawing.py": f"{fa['n_tests']} tests"})
    d.text(40, 190, "Read from disk: the skill folder", T_NODE)
    d.box(40, 250, 620, 30 + len(tree) * 34, INK, 2)
    lines(d, 60, 270, tree, 22)
    right = ["<Block>/", "├── board.md        spine:, close:", "├── jNN_<job>/", "│   ├── jNN_<job>.md   goal:, close:",
             "│   └── tNN_<task>/", "│       ├── tNN_<task>.md", "│       └── runs/rNN_<run>/result/",
             "└── studio/", "    └── sNN-<jNN>-<job>/", "        ├── sNN-<jNN>-<job>.md   job: yaml",
             "        └── build_sNN_<jNN>_<job>.py"]
    d.text(700, 190, "Where a Job topic is written", T_NODE)
    d.box(700, 250, 760, 30 + len(right) * 34, INK, 2)
    lines(d, 720, 270, right, 22)
    d.text(1500, 190, "Who owns each input", T_NODE)
    yy = 250
    for ln in y["owners"]:
        yy = d.para(1500, yy, "· " + ln, W - 1540, 22) + 10
    d.text(1500, yy + 20, "Its four commands", 30)
    yy += 70
    for ln in y["commands"]:
        yy = d.para(1500, yy, "· " + ln, W - 1540, 22) + 8
    yk = max(250 + 30 + len(right) * 34, 250 + 30 + len(tree) * 34, yy) + 40
    d.key(40, yk, W - 80, 100, 3)
    d.para(66, yk + 18, "Key point: one Job, one topic of its Block, in the runs band s21 to s29; it reads the Job "
           "and writes only its own topic.", W - 132, 28)
    f["height"] = yk + 130
    return f


def first(d, y):
    rows, pic = first_jobs(y)
    f = d.frame("④ What it made: the first Jobs drawn, Proj10 b01", W, 1500)
    d.heading("🖼️ The first Jobs it drew: Knowledge-Base's Proj10 b01 s21 to s23",
              "b01_ml_foundations: three discovery Jobs (math and classic ML, RL basics, NLP before LLMs), adopted from "
              "their results topics on 261012; the picture is s21")
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
    key = ("Key point: each Job now says why it exists, what it did and what it found, in few words; before, it "
           "listed only its Runs' states.")
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
    d.write(HERE / f"{HERE.name}.excalidraw", "build_s06_excalidraw_job.py")
    for f in fs:
        print(f["name"], f["width"], "x", f["height"])


if __name__ == "__main__":
    main()
