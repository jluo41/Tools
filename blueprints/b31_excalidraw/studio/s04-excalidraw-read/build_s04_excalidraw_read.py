"""s04 · excalidraw-read: a paper read onto a canvas, and a file we revise (haipipe-studio).

Four frames in two acts (rows named at the left, a named arrow for each step), the words from this topic's face:
  Act 1 · What it draws
    ① the skill as a mind map: its read mode, revise mode, scripts, rules, link to our paper, shared canvas;
    ② the read mode as a workflow, from the PDF to the canvas, scripts named; the revise mode points to b31 s21;
  Act 2 · Where it lives and what it made
    ③ its folder as a folder tree (a real folder, read from disk), its scripts and versions read from disk;
    ④ three canvases its revise mode made on 2026-10-11, their previews and a check against the drawing principles.
The version, commands, relations, folder, versions and canvas facts are read from disk on every build. A rebuild
keeps whatever a person drew (canvas.write, a seed snapshot beside the drawing).

    python build_s04_excalidraw_read.py
"""
import ast
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]                                    # .../Tools (the folder with plugins/ and blueprints/)
SKILLS = TOOLS / "plugins/haipipe-toolkit/skills/1_base"
sys.path.insert(0, str(SKILLS / "excalidraw/excalidraw-studio/scripts"))
from draw import Drawing, KEY, RED, INK, W, H, T_SMALL, T_TEXT, T_KEY  # noqa: E402

FACE = HERE / f"{HERE.name}.md"
READ = TOOLS / "plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-read"
REVISE = READ.parent / "excalidraw-draft"     # the revise mode, its own skill since 261013


def ref(py):
    """A script in excalidraw-read's ref/, or, for the revise mode, in excalidraw-draft's."""
    return next((d / "ref" / py for d in (READ, REVISE) if (d / "ref" / py).is_file()), READ / "ref" / py)
STUDIO_SCRIPTS = SKILLS / "project/haipipe-studio/scripts"
SPACE = TOOLS.parent / "WellDoc-SPACE"                      # where the SHIFT cowork canvases live (checkout beside Tools)
d = Drawing()


# ── words and facts ──────────────────────────────────────────────────────────────────────────────────────────
def data():
    out = {}
    for block in re.findall(r"```yaml\n(.*?)\n```", FACE.read_text(encoding="utf-8"), re.S):
        out.update(yaml.safe_load(block))
    return out


def opens():
    """The face's Later points (its open points until s04-D02 agreed the topic), numbered, as plain strings."""
    tail = FACE.read_text(encoding="utf-8").split("\nLater\n", 1)[1]
    return [re.sub(r"^\d+\.\s*", "", p.strip()) for p in re.findall(r"^\d+\..*(?:\n(?!\d+\.|\()[^\n]+)*", tail, re.M)]


def commands(script):
    src = ref(script).read_text(encoding="utf-8")
    names = re.findall(r'add_parser\("(\w+)"', src)
    for grp in re.findall(r"for name in \(([^)]*)\)", src):
        names += re.findall(r'"(\w+)"', grp)
    return names


def facts():
    skill = (READ / "SKILL.md").read_text(encoding="utf-8")
    ver = re.search(r'version:\s*"([^"]+)"', skill).group(1)
    versions = re.findall(r"^## (\d+\.\d+\.\d+) · (\S+) · (.*)$", (READ / "CHANGELOG.md").read_text(encoding="utf-8"), re.M)
    rel = re.search(r"RELATIONS = \(([^)]*)\)", (READ / "ref/read_paper.py").read_text(encoding="utf-8")).group(1)
    return {"version": ver, "versions": versions, "relations": re.findall(r'"(\w+)"', rel),
            "read_cmds": commands("read_paper.py"), "revise_cmds": commands("read_revise.py")}


def first_doc_line(py):
    doc = ast.get_docstring(ast.parse(ref(py).read_text(encoding="utf-8"))) or ""
    return doc.split("\n\n")[0].replace("\n", " ")


def fill(s, fx):
    return (s.replace("{read_paper_commands}", "read_paper.py: " + ", ".join(fx["read_cmds"]))
             .replace("{read_revise_commands}", "read_revise.py: " + ", ".join(fx["revise_cmds"]))
             .replace("{relations}", "five relations: " + ", ".join(fx["relations"])))


# ── frame ① the skill as a mind map ──────────────────────────────────────────────────────────────────────────
def mind(c, fx):
    f = d.frame("① What the skill draws: one mind map")
    d.heading(f"🧠 excalidraw-read {fx['version']}: one file read onto a canvas",
              "Read mode takes a paper's PDF; revise mode takes a file we change. Both shoot the real pages, highlight "
              "the words that matter, and keep a person's marks across rebuilds. Yellow, the key point: the skill's whole job.")
    m = c["mindmap"]
    branches = [{**b, "leaves": [fill(x, fx) for x in b["leaves"]]} for b in m["branches"]]
    bottom = d.mind_map(m["centre"], branches)
    f["height"] = bottom + 40
    return f


# ── frame ② the read mode as a workflow ──────────────────────────────────────────────────────────────────────
def workflow(c, fx, op):
    f = d.frame("② The read mode: from a PDF to the canvas")
    d.heading("🔄 Read mode: one PDF to one canvas, five steps",
              "Scripts named in each step (ref/read_paper.py). A quote is found by its words, so a shot is the real page with "
              "the words under a marker. Yellow, the key point: the reading, written by an agent, is the only judgment.")
    fl = c["flow"]
    boxes = d.flow(fl["steps"], 40, 200, W - 80, gap=70, title=32, leaf=23, labels=fl["labels"])
    y = max(b[1] + b[3] for b in boxes) + 70
    # what the canvas holds, four frames
    half = (W - 80 - 60) / 2
    d.text(40, y, "🖼️ The canvas it draws: four frames", T_KEY)
    yy = y + 50
    for cf in c["canvas_frames"]:
        d.text(40, yy, cf["name"], 26)
        yy = d.para(330, yy, cf["what"], half - 330, 23) + 14
    # the pointer to the revise mode
    px = 40 + half + 60
    p = c["pointer"]
    h = 70 + sum(d.height("· " + ln, half - 60, 24) + 8 for ln in p["lines"]) + d.height(p["title"], half - 60, 30)
    d.box(px, y, half, h, INK, 3, dashed=True)
    yy = d.para(px + 30, y + 22, p["title"], half - 60, 30) + 12
    for ln in p["lines"]:
        yy = d.para(px + 30, yy, "· " + ln, half - 60, 24) + 8
    # the points moved to Later (s04-D02), in place
    oy = max(yy, y + h + 70)
    ys = max(oy + 10, y + 50 + 4 * 90)
    for k in (0, 2):
        ys = d.para(px, ys, "⏳ later: " + re.sub(r"^❓\s*", "", op[k]), half, 22) + 10
    f["height"] = max(ys, yy) + 50
    return f


# ── frame ③ its folder ───────────────────────────────────────────────────────────────────────────────────────
def folder(c, fx):
    f = d.frame("③ Where it lives: its folder", 2400, 1100)
    fo = c["folder"]
    d.heading("📁 Where it lives: a skill folder, read from disk",
              "A real folder, so a folder tree. Yellow, the key point: the two modes' scripts and their yaml specs sit in ref/.", 1900)
    tree = Drawing.folder_tree(READ, open_=tuple(fo["open"]), most=8, notes=fo["notes"])
    th = len(tree) * 24 * 1.25
    d.key(40, 196, 1100, th + 70, 3)
    d.text(70, 226, "\n".join(tree), 24, code=True)
    y = 196 + th + 100
    d.para(40, y, "Its helpers are not in this folder:", 1100, 26)
    y += 40
    for a in fo["also"]:
        y = d.para(60, y, "· " + a, 1080, 22) + 8
    y = d.para(40, y + 20, fo["why"], 1100, 24)
    # what each script says about itself, read from its docstring, and its latest versions
    x, y2 = 1220, 196
    d.text(x, y2, "What each script says about itself (its docstring)", T_KEY)
    y2 += 48
    for py in ("read_paper.py", "read_revise.py", "track_changes.py"):
        n = len(ref(py).read_text(encoding="utf-8").splitlines())
        d.text(x, y2, f"{py} · {n} lines", 24, code=True)
        y2 = d.para(x + 20, y2 + 32, first_doc_line(py), 1100, 22) + 14
    y2 += 14
    d.text(x, y2, f"Its last versions (CHANGELOG.md, now {fx['version']})", T_KEY)
    y2 += 48
    for v, day, title in fx["versions"][:5]:
        y2 = d.para(x, y2, f"{v} · {day} · {title}", 1130, 22) + 8
    f["height"] = max(1100, y + 50, y2 + 50)
    return f


# ── frame ④ what it made ─────────────────────────────────────────────────────────────────────────────────────
def checks(path):
    """The drawing principles, one line each, for one canvas, read from its .excalidraw."""
    j = json.loads(Path(str(path) + ".excalidraw").read_text(encoding="utf-8"))
    els = [e for e in j["elements"] if not e.get("isDeleted")]
    frames = [e for e in els if e["type"] == "frame"]
    texts = [e for e in els if e["type"] == "text"]
    wide = [f for f in frames if f["width"] > 2800 or f["height"] > 1600]
    small = sum(1 for t in texts if t.get("fontSize", 20) < 20)
    folder_tree = sum(1 for t in texts if "├──" in str(t.get("text", "")))
    dens = Drawing.density_of(str(path) + ".excalidraw")
    kinds = ", ".join(sorted({k for _, _, k in dens}))
    return [
        ("①", f"{len(frames)} frames; " + ("all within 2800 x 1600" if not wide else
         f"⚠️ {len(wide)} over 2800 x 1600 (widest {int(max(f['width'] for f in wide))} px)")),
        ("②", f"frame kinds: {kinds}; side-by-side pictures, not a map"),
        ("③", f"{len(frames)} frames in one story; no acts, no named arrows"),
        ("④", "no folder tree" if not folder_tree else f"⚠️ {folder_tree} folder trees"),
        ("⑤", "no slight colour" + (f"; ⚠️ {small} words under 20 px (notes, by design)" if small else "; words 20 px or more")),
        ("⑥", "words per Mpx " + ", ".join(f"{p}" for n, p, k in dens if k != "picture") + " (a picture is not measured)"),
    ]


def made(c, op):
    f = d.frame("④ What it made: three canvases", W, 1230)
    d.heading("🖼️ What it made: three revise-mode canvases, 2026-10-11",
              "Previews of the SHIFT cowork Blocks b04, b03 and b02 (the top of each), checked against the drawing principles, one "
              "line each. A picture is not measured. Yellow, the key point: each canvas is as tall as the file it reads.", 1900)
    gap = 50
    cw = (W - 80 - 2 * gap) / 3
    low = 0
    tmp = Path(tempfile.mkdtemp(prefix="s04-crop-"))
    from PIL import Image
    for i, cv in enumerate(c["canvases"]):
        path = SPACE / cv["path"]
        x = 40 + i * (cw + gap)
        png = Path(str(path) + ".png")
        if not png.is_file():
            d.para(x, 200, f"❓ {cv['block']}: preview not found", cw, 24, RED)
            continue
        im = Image.open(png)
        crop = tmp / f"{cv['block']}.png"
        im.crop((0, 0, im.width, min(im.height, 3300))).save(crop)
        d.text(x, 190, f"{cv['block']}  ({im.width} x {im.height} px)", 28)
        ph = d.picture(crop, x, 240, cw, 700)
        y = 240 + ph + 30
        for mark, line in checks(path):
            y = d.para(x, y, f"{mark} {line}", cw, 21) + 6
        low = max(low, y)
    ky = low + 30                                          # the key point below the lowest column, never over it
    d.key(40, ky, W - 80, 100, 3)
    d.para(66, ky + 20, "A revise canvas is one tall picture per section, read down; it was made by read_revise.py draw.", W - 130, T_KEY)
    d.para(66, ky + 130, "⏳ later: " + re.sub(r"^❓\s*", "", op[1]), W - 130, 21)
    f["height"] = max(f["height"], ky + 200)
    return f


def main():
    c = data()
    fx = facts()
    op = opens()
    fs = {}
    for mark, fn in (("①", lambda: mind(c, fx)), ("②", lambda: workflow(c, fx, op)),
                     ("③", lambda: folder(c, fx)), ("④", lambda: made(c, op))):
        f = fn()
        d.badge(f)
        fs[mark] = f
    d.fid = None
    d.acts([{"name": a["name"], "frames": [fs[m]["id"] for m in a["frames"]], "arrow": a["arrow"]} for a in c["acts"]],
           between=[(fs[c["between"]["from"]]["id"], fs[c["between"]["to"]]["id"], c["between"]["label"])])
    out = HERE / f"{HERE.name}.excalidraw"
    d.write(out, "build_s04_excalidraw_read.py")
    subprocess.run([sys.executable, str(STUDIO_SCRIPTS / "render_png.py"), str(out), str(out.with_suffix(".png"))], check=False)
    for mark, f in fs.items():
        per, words = Drawing.words_per_mpx(d.els, f["id"], f["width"], f["height"])
        print(mark, f"{int(f['width'])}x{int(f['height'])}", Drawing.kind(d.els, f), per, "words/Mpx")


if __name__ == "__main__":
    main()
