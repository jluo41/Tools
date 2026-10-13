"""s06 · excalidraw-job: s06-excalidraw-job.excalidraw (b31_excalidraw).

Four frames as stairs (b31 s01, 261013: "你不能每一个都是朝左对齐"), joined by named arrows: ① the main frame at the
origin, each next one lower and further right (canvas.stairs):
  1. the skill as a mind map (the ask, the staircase, its results, its Runs, its words, its script, what it never does);
  2. the workflow: the Job's files into job_ladder.py, then what one build does;
  3. the skill folder and the folder a Job topic lands in, as folder trees (both are real folders), and who owns what;
  4. a made-up Job drawn as a staircase (the skill's test fixture), its preview and check.py's verdict; the real
     Jobs drawn are named in the face's `first: drawn:` (Tools is public: their pictures stay in their SPACE).
Every word is a yaml block of the face; facts (version, functions, tests, the demo's checks) are read on every build.
A rebuild keeps whatever a person drew (canvas.write, a seed snapshot).

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
from draw import Drawing, T_NODE, INK, RED, W, canvas  # noqa: E402
from check import check  # noqa: E402

FACE = HERE / f"{HERE.name}.md"
SKILL = TOOLKIT / "skills/1_base/display/excalidraw-job"
EXAMPLES = HERE / "examples"


class Facts(dict):
    def __missing__(self, k):
        return "{" + k + "}"


def first_jobs(y):
    """The staircase drawn on a made-up Job (excalidraw-job's own test fixture), checked, its preview kept in
    examples/. Tools is public: a real project's drawing, with its unpublished results, is named, never copied here."""
    import tempfile
    sys.path.insert(0, str(SKILL / "scripts"))
    sys.path.insert(0, str(SKILL / "tests"))
    import job_ladder  # noqa: E402
    from test_job_ladder import CFG, job_with_results  # noqa: E402
    pic = EXAMPLES / "demo-staircase.png"
    tmp = Path(tempfile.mkdtemp())
    job = job_with_results(tmp)
    out = tmp / "studio" / "demo.excalidraw"
    out.parent.mkdir()
    job_ladder.draw_job(job, out, dict(CFG))
    r = check(out)
    fails = sum("❌" in v for f in r["rows"] for k, v in f.items() if isinstance(v, str) and k[0] in "①②③④⑤⑥⑦⑧⑨")
    rows = [f"{'✅' if not fails else '❌'} the demo Job: {r['frames']} frames, " +
            ("every check passes" if not fails else f"{fails} checks fail"),
            "its charts drawn from the demo Runs' metrics.json, into assets/"]
    rows += [str(x) for x in y["first"].get("drawn", [])]
    EXAMPLES.mkdir(exist_ok=True)
    shutil.copyfile(out.with_suffix(".png"), pic)
    (EXAMPLES / "facts.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return rows, pic


def facts():
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    src = (SKILL / "scripts/job_ladder.py").read_text(encoding="utf-8")
    tests = "".join(p.read_text(encoding="utf-8") for p in sorted((SKILL / "tests").glob("test_*.py")))
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
    d.heading("🧠 What excalidraw-job draws", "a Job as a staircase, its results as charts beside it")
    bottom = d.mind_map(y["mindmap"]["centre"], y["mindmap"]["branches"])
    f["height"] = bottom + 40
    return f


def workflow(d, y):
    f = d.frame("② The workflow: a Job on disk to a staircase", W, 1100)
    d.heading("🔁 From the Job on disk to its staircase", "in and out; then one build")
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
        "job_ladder.py": f"the staircase, {fa['n_funcs']} functions", "job_drawing.py": "readers, make, draw",
        "SKILL.md": f"rules, v{fa['version']}", "test_job_ladder.py": f"{fa['n_tests']} tests in all"})
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
    f = d.frame("④ What it draws: a made-up Job as a staircase", W, 1500)
    d.heading(y["first"]["title"], y["first"]["sub"])
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
    key = " ".join(str(y["first"]["key"]).split())
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
    placed = canvas.stairs(d.els, [ids[c] if k == 0 else (ids[c], 520) for k, c in enumerate(y["stairs"]["order"])])
    d.fid = None
    for (a, b), words in zip(zip(placed, placed[1:]), y["stairs"]["arrows"]):     # a named arrow down into each
        x = b["x"] + 300
        d.line([(x, a["y"] + a["height"] + 14), (x, b["y"] - 14)], sw=6)
        d.text(x + 24, (a["y"] + a["height"] + b["y"]) / 2 - 26, words, 40)
    d.write(HERE / f"{HERE.name}.excalidraw", "build_s06_excalidraw_job.py")
    for f in fs:
        print(f["name"], f["width"], "x", f["height"])


if __name__ == "__main__":
    main()
