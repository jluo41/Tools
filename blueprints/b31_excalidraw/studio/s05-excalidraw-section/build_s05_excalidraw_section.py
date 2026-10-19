"""s05 · excalidraw-draft: s05-excalidraw-section.excalidraw (b31_excalidraw).

Four frames in two acts, each a screen or less, joined by named arrows (b31 s01 principles):
  1. the skill as a mind map (columns, where its words come from, colours, depths, what it never does, its script);
  2. the workflow: the inputs into the script, then what one run does, and the guard on a hand-edited map;
  3. the skill folder and the folder its maps go into, folder trees read from disk (both are real folders);
  4. the one real paper map the skill made, its preview checked against the drawing principles.
Every word is a yaml block of the face; facts (version, functions, changelog, the sample map's counts) are read from
the skill and the sample on every build. A rebuild keeps whatever a person drew (canvas.write, a seed snapshot).

    python build_s05_excalidraw_section.py
"""
import ast
import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLKIT = (HERE / "../../../../plugins/haipipe-toolkit").resolve()
sys.path.insert(0, str(TOOLKIT / "skills/1_base/excalidraw/excalidraw-studio/scripts"))
from draw import Drawing, T_FRAME, T_SMALL, T_NODE, INK, RED, W  # noqa: E402

FACE = HERE / f"{HERE.name}.md"
SKILL = (HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-draft").resolve()
SAMPLE = HERE / "examples/paper-sections-sample"
H_MAX = 1600


class Facts(dict):
    def __missing__(self, k):
        return "{" + k + "}"


def facts():
    """Everything the drawing says that the disk already knows."""
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    version = re.search(r'version:\s*"([^"]+)"', skill).group(1)
    updated = re.search(r'last_updated:\s*"([^"]+)"', skill).group(1)
    src = (SKILL / "ref/excalidraw_section.py").read_text(encoding="utf-8")
    funcs = [n.name for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)]
    depths = re.search(r"DEPTHS\s*=\s*\(([^)]*)\)", src).group(1).replace('"', "").replace(",", " |").strip()
    n_log = len(re.findall(r"^## \d", (SKILL / "CHANGELOG.md").read_text(encoding="utf-8"), re.M))
    scene = json.loads(SAMPLE.with_suffix(".excalidraw").read_text(encoding="utf-8"))
    texts = [e for e in scene["elements"] if e["type"] == "text" and e.get("containerId")]
    boxes = [e for e in scene["elements"] if e["type"] == "rectangle"]
    n_noplan = sum("no plan yet" in e["text"] for e in texts)
    sections = [e for e in texts if re.fullmatch(r"s0\.\d+\.\d+", e["containerId"])]
    old = re.sub(r"/ref/.*", "", scene["source"]).replace("Tools/plugins/haipipe-toolkit/skills/", "")
    return Facts(version=version, updated=updated, n_funcs=len(funcs), funcs=", ".join(f + "()" for f in funcs),
                 depths=depths, n_log=n_log, sample_boxes=len(boxes), n_noplan=n_noplan, n_sections=len(sections),
                 sample_words=sum(len(e["text"].split()) for e in texts), old_source=old + "/")


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
    d.heading("🧠 What excalidraw-draft draws", "a paper's Sections as a map, read left to right; every word of the "
              "map comes from the Draft plans and Evidence Items, never typed; the six branches below are its "
              "columns, its sources, its colours, its depths, its limits and its script")
    bottom = d.mind_map(y["mindmap"]["centre"], y["mindmap"]["branches"])
    assert bottom < 1440, f"mind map needs {bottom:.0f} px"
    f["height"] = bottom + 40
    return f


def workflow(d, y):
    f = d.frame("② The workflow: plans and evidence items to the map", W, 1100)
    d.heading("🔁 From the Draft plans and Evidence Items to the map",
              "top row: what goes in and what comes out; bottom row: what one run of excalidraw_section.py does")
    d.text(40, 190, "What goes in, and what comes out", T_NODE)
    top = d.flow(y["flow_in"]["steps"], 40, 250, W - 80, gap=90, title=34, leaf=24, labels=y["flow_in"]["labels"])
    ybot = top[0][1] + top[0][3] + 110
    d.text(40, ybot - 56, "What one run does, read from main() and layout()", T_NODE)
    bot = d.flow(y["flow_run"]["steps"], 40, ybot, W - 80, gap=90, title=34, leaf=24, labels=y["flow_run"]["labels"])
    yy = bot[0][1] + bot[0][3] + 40
    d.key(40, yy, W - 80, 120, 3)
    d.para(66, yy + 22, "Key point: the map is generated, never edited by hand. Change the Draft plan or the Evidence "
           "Items and redraw; a map changed on the canvas is replaced only with --force.", W - 132, T_NODE)
    assert yy + 120 + 30 <= 1100, f"workflow needs {yy + 150:.0f} px"
    return f


def lines(d, x, y, rows, size):
    """Code lines kept as they are (a tree must not be re-wrapped)."""
    for i, ln in enumerate(rows):
        d.text(x, y + i * 34, ln, size, code=True)


def folders(d, y, fa):
    f = d.frame("③ Where it lives: its folder, where the maps land, who owns the inputs", W, 800)
    d.heading("🧰 Its folder, where the maps land, and who owns what it reads",
              "the left tree is read from disk; the middle one is where a paper map is written; the right lists "
              "who owns each input, so a wrong map is fixed at its source and redrawn, never edited")
    tree = d.folder_tree(SKILL, open_=("ref", "agents"), notes={
        "excalidraw_section.py": f"{fa['n_funcs']} functions", "openai.yaml": "Codex's card",
        "SKILL.md": f"rules, v{fa['version']}"})
    d.text(40, 190, "Read from disk: the skill folder", T_NODE)
    d.box(40, 250, 800, 30 + len(tree) * 34, INK, 2)
    lines(d, 60, 270, tree, 22)
    right = ["Paper-<name>/", "├── board.md        ## Pages: the order", "├── <group>/<stem>/",
             "│   ├── <stem>.md", "│   └── draft/", "│       ├── <stem>-draft-v<G>.<S>.md",
             "│       └── <stem>-evidence-items.md", "└── studio/", "    └── paper-sections.excalidraw"]
    d.text(880, 190, "Where a paper map is written", T_NODE)
    d.box(880, 250, 800, 30 + len(right) * 34, INK, 2)
    lines(d, 900, 270, right, 22)
    d.text(1720, 190, "Who owns each input", T_NODE)
    yy = 250
    for ln in y["owners"]:
        yy = d.para(1720, yy, "· " + ln, 800, 22) + 12
    d.key(40, 610, 1640, 170, 3)
    d.para(66, 628, "A Section map goes to <page folder>/studio/<stem>-sections.excalidraw; a paper map to "
           "<paper folder>/studio/paper-sections.excalidraw. Story > RoadMap Draw lists what is in studio/. "
           "A map someone edited on the canvas is kept unless the script is run again with --force, and every map's "
           "source field names the script that made it, so a reader can tell it was generated.",
           1590, 28)
    return f


def sample(d, y, fa):
    f = d.frame("④ What it made: the one real paper map", W, 1400)
    d.heading("🖼️ The one real map it has made: a paper map, 261003",
              f"{fa['n_sections']} Sections in three groups; {fa['sample_boxes']} boxes; checked against the drawing principles")
    h = d.picture(HERE / y["checks"]["sample"], 40, 190, 700, 1180)
    xx = 800
    d.text(xx, 190, "Checked against b31 s01's principles", T_NODE)
    yy = 250
    for ln in y["checks"]["lines"]:
        red = "❌" in ln
        yy = d.para(xx, yy, ln, W - xx - 40, 28, RED if red else INK) + 22
    yy += 30
    d.text(xx, yy, "Later, on it (s05-D02)", T_NODE)
    yy += 56
    for ln in y["checks"]["open"]:
        yy = d.para(xx, yy, ln, W - xx - 40, 28) + 22
    d.key(xx, yy + 30, W - xx - 40, 130, 3)
    d.para(xx + 26, yy + 50, "Key point: the picture is the paper's table of contents, so a reader sees where each "
           "part sits; its evidence cards are not shown by any real map yet.", W - xx - 92, T_NODE)
    return f


def main():
    y, fa = data()
    d = Drawing()
    fs = [mind_map(d, y), workflow(d, y), folders(d, y, fa), sample(d, y, fa)]
    for f in fs:
        d.fid = f["id"]
        d.badge(f)
    ids = dict(zip("①②③④", (f["id"] for f in fs)))
    a = y["acts"]
    acts = [{"name": x["name"], "frames": [ids[c] for c in x["frames"]], "arrow": x["arrow"]} for x in a]
    b = y["between"]
    d.acts(acts, between=[(ids[b["from"]], ids[b["to"]], b["label"])])
    d.write(HERE / f"{HERE.name}.excalidraw", "build_s05_excalidraw_section.py")
    for f in fs:
        print(f["name"], f["width"], "x", f["height"])


if __name__ == "__main__":
    main()
