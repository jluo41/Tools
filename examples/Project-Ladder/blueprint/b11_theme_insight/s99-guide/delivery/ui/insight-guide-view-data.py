"""Run from the SPACE root:
    uv run --with pyyaml --with pillow python <this file> > insight-guide-view-data.js
Print the s99 preview's data, read from the Insight Guide's own files: guide.yaml (the description, the
skills, each level's role and what it reads), method.md (the six steps), the method cards (asking, answering,
reading), related/papers.md (the papers by method), and the two drawings. Each frame of the RoadMap drawing
and the methods drawing is rendered to img/ beside this file. Nothing is typed here."""
import json, re, subprocess, sys, tempfile
from pathlib import Path

import yaml

ROOT = Path.cwd()
WB = ROOT / "plugins/haipipe-toolkit/servers/workbench-insight"
ASK = ROOT / "plugins/haipipe-toolkit/skills/1_base/project/hai-report/ref/asking-methods"
RENDER = ROOT / "plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/render_png.py"
ROADMAP = WB / "studio/insight-workbench-design.excalidraw"
METHODS_DRAW = WB / "guide/methods.excalidraw"
HERE = Path(__file__).resolve().parent
IMG = HERE / "img"


def rel(p):
    return str(p.relative_to(ROOT))


def card(f):
    t = f.read_text(errors="ignore")
    m = re.search(r"(?ms)^move:\s*(.+?)(?=^\w[\w-]*:|\Z)", t)
    return {"name": t.splitlines()[0].strip(), "move": " ".join(m.group(1).split()) if m else "", "file": rel(f)}


def steps():
    t = (WB / "guide/method.md").read_text()
    rows = []
    for ln in t.splitlines():
        m = re.match(r"^\| \*\*(\d) ([^*]+)\*\* \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|", ln)
        if m:
            n, name, board, what, where, who = (x.strip() for x in m.groups())
            rows.append({"n": n, "name": name, "board": board, "what": what, "where": where, "who": who})
    return rows


def papers():
    rows = []
    for ln in (WB / "related/papers.md").read_text().splitlines():
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c) < 7 or c[0] in ("group", "---") or not c[3]:
            continue
        rows.append({"group": c[0].split(";")[0].strip(), "role": c[1], "key": c[2] == "★",
                     "paper": c[3], "venue": c[4], "doi": c[5], "why": c[6]})
    return rows


def render(scene, out):
    with tempfile.NamedTemporaryFile("w", suffix=".excalidraw", delete=False) as f:
        json.dump(scene, f)
    subprocess.run([sys.executable, str(RENDER), f.name, str(out), "1"], check=True, capture_output=True)
    Path(f.name).unlink()


def frames(src, prefix):
    """One PNG per named frame (its own elements only), or one for a drawing with no frames."""
    d = json.loads(src.read_text())
    els = [e for e in d["elements"] if not e.get("isDeleted")]
    fr = [e for e in els if e["type"] == "frame"]
    out = []
    for i, f in enumerate(fr or [None], 1):
        keep = els if f is None else [e for e in els if e.get("frameId") == f["id"]]
        keep = [e for e in keep if e["type"] != "frame"]
        png = IMG / f"{prefix}-{i}.png"
        render({**d, "elements": keep}, png)
        out.append({"name": f["name"] if f else src.stem, "png": f"img/{png.name}",
                    "open": "/_excalidraw/?board=" + rel(src) + (f"#{f['name']}" if f else "")})
    return out


g = yaml.safe_load((WB / "guide/guide.yaml").read_text())
IMG.mkdir(exist_ok=True)
cards = {"asking": [card(f) for f in sorted(ASK.glob("0*.md"))],
         "answering": [card(f) for f in sorted((WB / "guide/methods/answer").glob("*.md"))],
         "reading": [card(f) for f in sorted((WB / "guide/methods/read").glob("*.md"))]}
DATA = {
    "description": " ".join(g["description"].split()),
    "skills": g.get("skills", []),
    "levels": {k: {"role": v["role"], "spaces": v.get("spaces", {})} for k, v in g.get("levels", {}).items()},
    "steps": steps(),
    "cards": cards,
    "papers": papers(),
    "roadmap": frames(ROADMAP, "roadmap"),
    "methods_drawing": frames(METHODS_DRAW, "methods"),
    "sources": {"guide": rel(WB / "guide/guide.yaml"), "method": rel(WB / "guide/method.md"),
                "papers": rel(WB / "related/papers.md"), "roadmap": rel(ROADMAP)},
}
print("const GUIDE = " + json.dumps(DATA, ensure_ascii=False, indent=1) + ";")
