"""s02 · excalidraw-report: s02-excalidraw-report.excalidraw (b31 excalidraw).

Four frames in two acts (b31 s01's principles, the helpers of excalidraw-studio's draw.py):
  Act 1 · ① the skill as one mind map, ② two workflows (a scratch, a report drawing) with their loops;
  Act 2 · ③ the skill folder as a folder tree read from disk with its facts, ④ two drawings it made, checked.
Every word is a yaml block of the face; the version, the changelog headings, the rule and helper counts, the folder
tree and the number of report drawings found are read from disk on every build.

    python build_s02_excalidraw_report.py
"""
import ast
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]
SKILLS = TOOLS / "plugins/haipipe-toolkit/skills/1_base"
sys.path.insert(0, str(SKILLS / "excalidraw/excalidraw-studio/scripts"))
from draw import Drawing, KEY, RED, W, H, T_NODE, T_TEXT, T_SMALL  # noqa: E402

FACE = HERE / f"{HERE.name}.md"
OUT = HERE / f"{HERE.name}.excalidraw"


def data():
    out = {}
    for block in re.findall(r"```yaml\n(.*?)\n```", FACE.read_text(encoding="utf-8"), re.S):
        out.update(yaml.safe_load(block))
    return out


def space_root():
    for p in [TOOLS, *TOOLS.parents, TOOLS.parent / "WellDoc-SPACE"]:
        if (p / "env.sh").is_file():
            return p
    return None


def facts(skill):
    """What the skill folder says about itself, read on every build."""
    sk = (skill / "SKILL.md").read_text(encoding="utf-8")
    ver = re.search(r'version:\s*"([^"]+)"', sk).group(1)
    upd = re.search(r'last_updated:\s*"([^"]+)"', sk).group(1)
    log = (skill / "CHANGELOG.md").read_text(encoding="utf-8")
    heads = re.findall(r"^## (\d+\.\d+\.\d+ · .*)$", log, re.M)
    rules = len(re.findall(r"^\d+\. \*\*", (skill / "ref/report-drawing.md").read_text(encoding="utf-8"), re.M))
    tree = ast.parse((skill / "ref/plot_kit.py").read_text(encoding="utf-8"))
    plots = [f.name for c in tree.body if isinstance(c, ast.ClassDef) for f in c.body
             if isinstance(f, ast.FunctionDef) and not f.name.startswith("_")]
    docs = {f.name: (ast.get_docstring(f) or "").split("\n")[0] for c in tree.body if isinstance(c, ast.ClassDef)
            for f in c.body if isinstance(f, ast.FunctionDef)}
    return ver, upd, heads, rules, plots, docs


def main():
    dt = data()
    skill = TOOLS / dt["skill"]["path"]
    ver, upd, heads, rules, plots, docs = facts(skill)
    d = Drawing()

    # ① the mind map
    f1 = d.frame("① The skill: what it draws, one mind map")
    d.heading("🧠 excalidraw-report: what it draws", f"version {ver}, updated {upd}; two modes, one canvas a person and an agent share")
    bottom = d.mind_map(dt["mindmap"]["centre"], dt["mindmap"]["branches"])
    f1["height"] = bottom + 40
    d.badge(f1)

    # ② two workflows
    f2 = d.frame("② How a drawing is made: two workflows")
    d.heading("🔁 From material to a drawing", "the script behind each step; the loop drawn closed")
    y = 180
    for fl in dt["flows"]:
        d.text(40, y, fl["name"], T_NODE)
        y += 56
        boxes = d.flow(fl["steps"], 40, y, W - 80, labels=fl["labels"], gap=110)
        by = boxes[0][1] + boxes[0][3]
        x0, x1 = boxes[-1][0] + boxes[-1][2] / 2, boxes[1][0] + boxes[1][2] / 2
        d.line([(x0, by), (x0, by + 50), (x1, by + 50), (x1, by + 4)], dashed=True, sw=3)
        d.text(x1 + 24, by + 56, "↺ " + fl["loop"], T_TEXT)
        y = by + 130
    f2["height"] = y + 10
    d.badge(f2)

    # ③ the folder
    f3 = d.frame("③ Where it lives: its folder")
    d.heading("🧰 The skill folder, read from disk", f"{skill.relative_to(TOOLS)}/")
    notes = dt["skill"]["notes"]
    tree = Drawing.folder_tree(skill, open_=tuple(dt["skill"]["open"]), notes=notes)
    d.text(60, 200, "\n".join(tree), 30, code=True)
    tx = 60
    tbottom = 200 + len(tree) * 30 * 1.25
    d.key(1100, 190, 1400, 330)
    yy = d.para(1130, 210, "What it says about itself, read now", 1340, T_NODE)
    for ln in (f"version {ver}, last updated {upd}",
               f"{len(heads)} changelog entries; the newest is {heads[0]}",
               f"{rules} numbered rules in ref/report-drawing.md",
               f"{len(plots)} plot helpers in ref/plot_kit.py: " + ", ".join(p for p in plots if p not in ("text", "rect", "line", "dot", "pill", "headline", "key", "source", "save", "frame", "base", "title"))):
        yy = d.para(1130, yy + 6, "· " + ln, 1340, 26)
    yy = d.para(1100, 560, "Newest changelog entries", 1400, T_NODE) + 6
    for h_ in heads[:5]:
        yy = d.para(1100, yy + 6, "· " + h_, 1420, 24)
    yy = d.para(1100, yy + 30, "Beside it, other skills' scripts it calls", 1400, T_NODE) + 6
    for ln in ("haipipe-studio/scripts/canvas.py: write keeps a person's marks",
               "haipipe-studio/scripts/render_png.py: the PNG preview",
               "haipipe-report/scripts/build_report_drawing.py: report drawing from studio frames",
               "excalidraw-studio/scripts/draw.py: the helpers a Studio topic builder imports"):
        ok = (SKILLS / "project" / ln.split("/scripts/")[0] / "scripts" / ln.split("/scripts/")[1].split(":")[0]).is_file() \
            or (SKILLS / "excalidraw" / ln.split("/scripts/")[0] / "scripts" / ln.split("/scripts/")[1].split(":")[0]).is_file()
        yy = d.para(1100, yy + 6, ("· " if ok else "❓ missing: ") + ln, 1420, 24)
    PLOTS = ("hbar", "compare", "share_bar", "columns", "spans", "gauge", "trend")
    yy = d.para(1100, yy + 30, "The plot helpers of ref/plot_kit.py, from their docstrings", 1400, T_NODE) + 6
    for nm in PLOTS:
        yy = d.para(1100, yy + 6, f"· {nm}: " + (docs.get(nm) or "no docstring"), 1420, 24)
    py = d.para(60, tbottom + 30, "Each script's first line, from its docstring", 1000, T_NODE) + 6
    for sc in ("add_pictures.py", "plot_kit.py", "render_excalidraw.py"):
        doc = ast.get_docstring(ast.parse((skill / "ref" / sc).read_text(encoding="utf-8"))) or "no docstring"
        py = d.para(60, py, f"· {sc} ({sum(1 for _ in (skill / 'ref' / sc).open())} lines): " + doc.split("\n")[0], 1000, 24) + 6
    heads_md = [h for h in re.findall(r"^(.+)\n-{3,}$", (skill / "SKILL.md").read_text(encoding="utf-8"), re.M) if not h.strip().startswith("#")]
    py = d.para(60, py + 24, f"SKILL.md has {len(heads_md)} sections, read now", 1000, T_NODE) + 6
    for h_ in heads_md:
        py = d.para(60, py, "· " + h_, 1000, 24) + 4
    tbottom = max(tbottom, py)
    d.para(60, max(tbottom, yy) + 20, "A scratch is seeded by a script in a Block's studio/_build/; a report drawing sits "
           "under the report's studio/, linked once from its Evidence.", 2300, 28)
    f3["height"] = max(tbottom, yy) + 110
    d.badge(f3)

    # ④ two drawings it made
    f4 = d.frame("④ What it made: two drawings, checked")
    d.heading("🖼️ Two real drawings, against the drawing principles", "a picture is not measured; each verdict is one line")
    root = space_root()
    n = 0
    road = None
    if root:
        found = sorted((root / "examples-1-data").glob("*/work/*/reports/*/*-roadmap.png"))
        n = len(found)
        road = found[0] if found else None
    studio_png = TOOLS / "blueprints/b10_project_workbench/studio/s02-studio-workbench-skill/studio-and-report.png"
    imgs = [road, studio_png]
    colw = (W - 120) / 2
    yb = 190
    for k, pic in enumerate(dt["pictures"]):
        x = 40 + k * (colw + 40)
        yy = d.para(x, yb, pic["title"], colw, T_NODE)
        cap = pic["caption"].format(n=n)
        yy = d.para(x, yy + 4, cap + " (" + pic["find"] + ")", colw, T_SMALL)
        if imgs[k] and Path(imgs[k]).is_file():
            hh = d.picture(imgs[k], x, yy + 10, colw, 780)
            yy += hh + 30
        else:
            yy = d.para(x, yy + 10, "❓ the picture is missing on disk", colw, T_TEXT)
        d.key(x - 6, yy, colw + 12, 36 + 38 * len(pic["verdicts"]), 3)
        yy += 14
        for v in pic["verdicts"]:
            yy = d.para(x + 14, yy, v, colw - 30, 28) + 6
    f4["height"] = yy + 130
    d.badge(f4)
    # what was open, moved to Later when the topic was agreed (s02-D02)
    d.para(40, f4["height"] - 100, "⏳ Later 1: do report drawings follow the drawing principles, or keep their own larger "
           "canvas? Later 2: no scratch preview is kept in any Block.", W - 80, 26)

    ids = {"①": f1["id"], "②": f2["id"], "③": f3["id"], "④": f4["id"]}
    b = dt["between"]
    d.acts([{"name": x["name"], "frames": [ids[m] for m in x["frames"]], "arrow": x["arrow"]} for x in dt["acts"]],
           between=[(ids[b["from"]], ids[b["to"]], b["label"])])
    d.write(OUT, HERE.name and "build_s02_excalidraw_report.py")
    for fr in (f1, f2, f3, f4):
        print(fr["name"], fr["width"], "x", round(fr["height"]), Drawing.kind(d.els, fr),
              Drawing.words_per_mpx(d.els, fr["id"], fr["width"], fr["height"])[0])


if __name__ == "__main__":
    main()
