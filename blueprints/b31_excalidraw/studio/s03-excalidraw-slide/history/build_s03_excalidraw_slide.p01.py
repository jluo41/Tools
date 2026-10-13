"""s03 · excalidraw-slide: s03-excalidraw-slide.excalidraw (b31 Studio).

Four frames in two acts, drawn with excalidraw-studio's Drawing helpers; every word is a yaml block of the face, and
the facts (the skill's version, its functions, the drafts found and what they hold) are read from disk.
  Act 1 · What it draws:  ① a mind map of the skill   ② its workflow map, slides.py to the deck, and the drafts
  Act 2 · Where it lives: ③ its folder, a draft's folder and a deck's folder   ④ two drafts made with it, checked

    python build_s03_excalidraw_slide.py
"""
import ast
import importlib.util
import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]                                           # Tools/ (the folder holding blueprints/)
SKILL = TOOLS / "plugins/haipipe-toolkit/skills/1_base/display/excalidraw-slide"
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/display/excalidraw-studio/scripts"))
from draw import Drawing, INK, RED, W, T_SMALL, T_KEY  # noqa: E402

FACE = HERE / f"{HERE.name}.md"
OUT = HERE / f"{HERE.name}.excalidraw"
d = Drawing()


def rel(p):
    return str(Path(p).relative_to(TOOLS))


# ── facts read from disk ─────────────────────────────────────────────────────────────────────────────────────
def facts():
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    fn = [n.name for n in ast.parse((SKILL / "scripts/slide_kit.py").read_text(encoding="utf-8")).body
          if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")]
    consts = [t.id for n in ast.parse((SKILL / "scripts/slide_kit.py").read_text(encoding="utf-8")).body
              if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name) and t.id.isupper()]
    log = (SKILL / "CHANGELOG.md").read_text(encoding="utf-8")
    heads = re.findall(r"^## \[([\d.]+)\] · (\S+) · (.*)$", log, re.M)
    tests = len(re.findall(r"^\s*def test_", (SKILL / "tests/test_slide_kit.py").read_text(encoding="utf-8"), re.M))
    refs = re.findall(r"^## (.*)$", (SKILL / "ref/slide-draft.md").read_text(encoding="utf-8"), re.M)
    drafts = []
    for f in sorted((TOOLS / "blueprints").glob("*/studio/s6[0-9]-*/slides.py")):
        spec = importlib.util.spec_from_file_location("slides_" + f.parent.name, f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        top = f.parents[2]
        decks = list((top / "delivery").glob(f"*/*.pptx"))
        drafts.append({"dir": f.parent, "name": f.parent.name, "slides": len(m.SLIDES), "groups": len(m.GROUPS),
                       "fields": sorted(m.SLIDES[0]), "deck": decks[0] if decks else None,
                       "own_kit": (f.parent / "slide_kit.py").is_file(), "builder": (f.parent / "build_deck.py").is_file(),
                       "png": next(f.parent.glob("*.png"), None), "excal": next(f.parent.glob("*.excalidraw"), None)})
    rules = re.findall(r"^(\d)\. \*\*(.*?)\*\*: (.*)$", skill, re.M)
    return {"rules": rules, "version": re.search(r'version: "([\d.]+)"', skill).group(1), "funcs": fn, "consts": consts, "heads": heads,
            "tests": tests, "refs": refs, "drafts": drafts}


F = facts()


def fill(s):
    s = str(s)
    return (s.replace("<<n_funcs>>", str(len(F["funcs"]))).replace("<<funcs>>", " · ".join(F["funcs"]) + " and the colours "
                                                                  + ", ".join(F["consts"]))
            .replace("<<version>>", F["version"]))


def data():
    out = {}
    for block in re.findall(r"```yaml\n(.*?)\n```", FACE.read_text(encoding="utf-8"), re.S):
        out.update(yaml.safe_load(block))
    return out


D = data()
FRAMES = {}


def deepfill(x):
    if isinstance(x, str):
        return fill(x)
    if isinstance(x, list):
        return [deepfill(i) for i in x]
    if isinstance(x, dict):
        return {k: deepfill(v) for k, v in x.items()}
    return x


D = deepfill(D)


def tree_box(x, y, w, title, lines, size=22):
    """A real folder as a tree, in a box under its title; returns the height."""
    h = 24 + Drawing.height(title, w - 40, 30) + 12 + len(lines) * size * 1.25 + 24
    d.box(x, y, w, h, INK, 2)
    yy = d.para(x + 20, y + 20, title, w - 40, 30) + 12
    d.text(x + 20, yy, "\n".join(lines), size, code=True)
    return h


# ── ① the mind map ──────────────────────────────────────────────────────────────────────────────────────────
def frame1():
    f = d.frame("① What it draws: one mind map")
    d.heading(f"🧠 excalidraw-slide v{F['version']}: what it draws",
              f"Read from the skill's SKILL.md, ref/slide-draft.md and scripts/slide_kit.py. Each branch is one part of a "
              f"slide draft (studio topic s61 to s69): its one-line summary large, its details small. Yellow, the key point: "
              f"one source, slides.py, feeds both the drawing and the deck. Red: open.")
    bottom = d.mind_map(D["mindmap"]["centre"], D["mindmap"]["branches"])
    d.para(40, bottom + 40, "📏 The skill's six rules (SKILL.md), read in order", 1800, T_KEY)
    steps = [{"title": f"{n} {name}", "lines": [txt]} for n, name, txt in F["rules"]]
    boxes = d.flow(steps, 40, bottom + 100, W - 80, gap=70, title=26, leaf=22)
    f["height"] = max(1440, boxes[0][1] + boxes[0][3] + 40)
    d.badge(f)
    FRAMES[1] = f
    return f


# ── ② the workflow map ──────────────────────────────────────────────────────────────────────────────────────
def frame2():
    f = d.frame("② Its flow: from slides.py to the deck")
    d.heading("🔁 From slides.py to a deck, with the person in the loop",
              "One source feeds two builders; the person reads the canvas and marks it before any deck is written. "
              "Yellow, the key point: the canvas is made first, the deck only after it is agreed. Below: the drafts found on disk.")
    steps = D["flow"]["steps"]
    boxes = d.flow(steps, 40, 210, W - 80, gap=110, labels=D["flow"]["labels"])
    by = max(b[1] + b[3] for b in boxes)
    # the review loop: from the person's step back to slides.py, drawn under the boxes
    loop_y = by + 60
    xs = [b[0] + b[2] / 2 for b in boxes]
    d.line([(xs[3], by + 4), (xs[3], loop_y)], arrow=False, dashed=True, color=RED, sw=2)
    d.line([(xs[3], loop_y), (xs[0], loop_y)], arrow=False, dashed=True, color=RED, sw=2)
    d.line([(xs[0], loop_y), (xs[0], by + 6)], dashed=True, color=RED, sw=2)
    d.text(xs[0] + 40, loop_y - 36, "a change: edit slides.py, run the builder again", T_SMALL + 3, RED)
    d.key(40, loop_y + 50, 1200, 130)
    d.para(60, loop_y + 64, "🔧 never edit the drawing or the deck by hand", 1160, T_KEY)
    d.para(60, loop_y + 108, D["loop"], 1160, T_SMALL)
    # the drafts found on disk, one box each, with what they hold
    y0 = loop_y + 240
    d.para(40, y0, f"📚 {len(F['drafts'])} slide drafts found in Tools/blueprints, read from disk", 1600, T_KEY)
    bw = (W - 80 - 60 * max(len(F["drafts"]) - 1, 0)) / max(len(F["drafts"]), 1)
    for i, dr in enumerate(F["drafts"]):
        x = 40 + i * (bw + 60)
        lines = [f"{dr['slides']} slides in {dr['groups']} acts (GROUPS)",
                 "slide fields: " + ", ".join(dr["fields"]),
                 f"deck: {rel(dr['deck'])}" if dr["deck"] else "deck: none yet",
                 ("✅ own build_deck.py" if dr["builder"] else "⬜ no build_deck.py") + " · " +
                 ("its own slide_kit.py" if dr["own_kit"] else "no copy of slide_kit.py")]
        hh = 30 + 40 + sum(Drawing.height("· " + l_, bw - 40, 22) + 6 for l_ in lines) + 20
        d.box(x, y0 + 60, bw, hh, INK, 2)
        yy = d.para(x + 20, y0 + 76, "🗂️ " + dr["name"], bw - 40, 30) + 8
        for l_ in lines:
            yy = d.para(x + 20, yy, "· " + l_, bw - 40, 22) + 6
    d.para(40, y0 + 330, "❓ the skill's contract names visual, headline, caption, next and OPEN; neither draft's slides.py has "
           "them (Open 1). Each draft runs its own build_deck.py (Open 3).", W - 80, T_SMALL + 4)
    f["height"] = max(1440, y0 + 420)
    d.badge(f)
    FRAMES[2] = f
    return f


# ── ③ where it lives ────────────────────────────────────────────────────────────────────────────────────────
def frame3():
    f = d.frame("③ Where it lives: its folders")
    d.heading("📁 Where it lives: the skill, a draft and its deck",
              "Each tree is a real folder, read from disk. Yellow, the key point: the skill holds the contract and a small "
              "kit; the draft and the deck live in the topic that proposes them. Red: not in the skill yet.")
    n_ver = len(F["heads"])
    h1 = tree_box(40, 200, 760, rel(SKILL) + "/", Drawing.folder_tree(SKILL, open_=("ref", "scripts", "tests"),
                  notes={"slide-draft.md": "the contract", "slide_kit.py": "colours, check",
                         "test_slide_kit.py": f"{F['tests']} tests", "openai.yaml": ""}))
    dr = F["drafts"][-1] if F["drafts"] else None
    x2 = 40 + 760 + 200
    if dr:
        tree = Drawing.folder_tree(dr["dir"], notes={"slides.py": "the one source", "build_deck.py": "the deck writer",
                                   "slide_kit.py": "its own copy of the kit"})
        tree = [t.replace("\n", " ") for t in tree]
        h2 = tree_box(x2, 200, 760, "a draft: " + rel(dr["dir"]) + "/", tree)
        deck = dr["deck"].parent if dr["deck"] else None
        x3 = x2 + 760 + 200
        if deck:
            h3 = tree_box(x3, 200, 760, "its deck: " + rel(deck) + "/", Drawing.folder_tree(deck, notes={"svg/": "one svg a slide"}))
        d.line([(40 + 760 + 6, 330), (x2 - 6, 330)], sw=5)
        d.text(40 + 760 + 14, 262, "a draft is\nmade in a topic", 24)
        d.line([(x2 + 760 + 6, 330), (x3 - 6, 330)], sw=5)
        d.text(x2 + 760 + 14, 262, "build_deck.py\nwrites", 24)
    top = 200 + max(h1, h2 if dr else 0, h3 if dr and deck else 0) + 70
    # what the skill's own files say, read from disk
    d.line([(250, 200 + h1 + 4), (250, top - 6)], sw=5)
    d.text(266, 200 + h1 + 14, "its contract", 24)
    d.line([(700, 200 + h1 + 4), (700, top - 6)], sw=5)
    d.text(716, 200 + h1 + 14, "its history", 24)
    d.key(40, top, 560, 60 + 34 * 4)
    d.para(60, top + 14, "📜 ref/slide-draft.md sections", 520, T_KEY)
    d.para(60, top + 56, " · ".join(F["refs"]), 520, T_SMALL + 3)
    d.box(640, top, 1880, 60 + 34 * 4, INK, 2)
    yy = d.para(660, top + 14, f"🕘 CHANGELOG.md: {n_ver} versions", 1840, T_KEY)
    for ver, day, title in F["heads"]:
        yy = d.para(660, yy + 4, f"· v{ver} · {day} · {title}", 1840, T_SMALL + 3)
    d.para(40, top + 235, f"📊 now: skill v{F['version']}, {n_ver} versions in its changelog, {F['tests']} tests, {len(F['drafts'])} drafts, {sum(x['slides'] for x in F['drafts'])} slides drawn, {sum(1 for x in F['drafts'] if x['deck'])} decks written.", W - 80, T_SMALL + 4)
    d.para(40, top + 285, "❓ the skill has no deck writer: build_deck.py is copied into each draft's topic (Open 3); "
           "each draft also keeps its own slide_kit.py (Open 4).", W - 80, T_SMALL + 4)
    d.para(40, top + 335, "⬜ the skill's tests cover slide_kit.py only: " + f"{F['tests']} tests; the drawing and the deck have none.",
           W - 80, T_SMALL + 4)
    d.badge(f)
    FRAMES[3] = f
    return f


# ── ④ what it made ──────────────────────────────────────────────────────────────────────────────────────────
def frame4():
    f = d.frame("④ What it made: two drafts, checked")
    d.heading("🖼️ What it made: two slide drafts, checked against the six principles",
              "Previews as they are on disk now. A slide draft keeps its own colours and sizes by design; the lines say "
              "what each of the six principles finds in them, measured from their files.")
    shown = [dr for dr in F["drafts"] if dr["png"]][:2]
    lines = []
    for dr, (x, w, hm) in zip(shown, ((40, 900, 1100), (980, 900, 560))):
        hh = d.picture(dr["png"], x, 200, w, hm)
        d.para(x, 200 + hh + 14, f"{dr['name']}: {dr['slides']} slides", w, T_SMALL + 3)
        j = json.loads(dr["excal"].read_text(encoding="utf-8"))["elements"]
        frs = [e for e in j if e["type"] == "frame" and not e.get("isDeleted")]
        size = min(e["fontSize"] for e in j if e["type"] == "text" and not e.get("isDeleted"))
        big = max(frs, key=lambda e: e["width"] * e["height"])
        lines.append(f"{dr['name']}: {len(frs)} frames, largest {round(big['width'])} x {round(big['height'])}, "
                     f"smallest word {size:g} px")
    d.key(1920, 200, 600, 380)
    yy = d.para(1940, 214, "🔍 measured from the two drawings", 560, T_KEY)
    for ln in lines:
        yy = d.para(1940, yy + 8, "· " + ln, 560, T_SMALL + 3)
    y = 800
    for line in D["checks"]:
        h = Drawing.height(line, 1480, 24)
        d.box(980, y, 1540, h + 24, INK, 1.5)
        d.para(1000, y + 12, line, 1480, 24)
        y += h + 40
    d.para(980, y + 6, "❓ the drafts break the size and word-size limits on purpose; the skill should say so (Open 2).", 1540, T_SMALL + 4)
    return f, lines


def frame4_checks(f, lines):
    pass


f1, f2, f3 = frame1(), frame2(), frame3()
f4, lines = frame4()
frame4_checks(f4, lines)
d.badge(f4)
a = D["acts"]
ids = {"①": f1["id"], "②": f2["id"], "③": f3["id"], "④": f4["id"]}
d.acts([{"name": x["name"], "frames": [ids[i] for i in x["frames"]], "arrow": x["arrow"]} for x in a],
       between=[(ids[D["between"]["from"]], ids[D["between"]["to"]], D["between"]["label"])])
d.write(OUT, HERE.name + "/build_s03_excalidraw_slide.py")
for fr in (f1, f2, f3, f4):
    print(fr["name"], round(fr["width"]), "x", round(fr["height"]))
