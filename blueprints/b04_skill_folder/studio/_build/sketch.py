"""Shared helpers for b04's studio drawings (and b17's s02-work-skills): sketch elements and
facts read from disk. A builder imports this, draws into `els`, then calls `save(out)`, which
writes through b03's canvas.write so every mark a person adds survives a rebuild.

Colours, one meaning each (JL 261007: "what does the color of red and blue mean here?"):
yellow = a question (from board.md) · green = done · blue = an idea or recommendation, and blue
text = a reply to a person's mark · pink = a choice for JL · gray = other sessions' work ·
red text = an open concern. `legend()` draws this key on every drawing.
"""
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]                                   # Tools/
SPACE = TOOLS.parent
TK = TOOLS / "plugins" / "haipipe-toolkit"
SKILLS = TK / "skills"
# b03's shared studio writer, found by its file (the Block folder has been renamed before)
BUILD = next((p.parent for p in sorted((TOOLS / "blueprints").glob("*/studio/_build/canvas.py"))
              if p.parent != HERE), TOOLS / "blueprints" / "b03_project_workbench" / "studio" / "_build")
sys.path.insert(0, str(BUILD))
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402  (the merge-safe writer)

random.seed(261007)
SANS, MONO = 6, 3
INK, GRAY, RED, BLUE, GREEN = "#1e1e1e", "#868e96", "#e03131", "#1971c2", "#2f9e44"
STICKY = {"ask": "#ffec99", "fit": "#b2f2bb", "bend": "#ffd8a8", "none": "#e9ecef", "open": "#ffc9c9",
          "idea": "#a5d8ff", "done": "#b2f2bb"}
LEGEND = [("question", "ask"), ("done", "done"), ("idea / recommendation", "idea"), ("your call", "open"),
          ("other sessions", "none")]
els = []
FRAME = [None]


# ── elements ────────────────────────────────────────────────────────────────────────────────
def base(kind, x, y, w, h, stroke=INK, bg="transparent", sw=1.5, dashed=False, rough=1):
    e = {"id": f"v{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": sw,
         "strokeStyle": "dashed" if dashed else "solid", "roughness": rough, "opacity": 100, "groupIds": [],
         "frameId": FRAME[0], "roundness": {"type": 3} if kind == "rectangle" else None,
         "seed": random.randint(1, 2**31 - 1), "version": 1, "versionNonce": random.randint(1, 2**31 - 1),
         "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False}
    els.append(e)
    return e


def text(x, y, s, size=20, color=INK, font=SANS, container=None):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * size * (0.6 if font == MONO else 0.55)
    e = base("text", x, y, w, len(lines) * size * 1.25, color, rough=0)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",
             containerId=container, autoResize=True, lineHeight=1.25)
    return e


def concern(x, y, s, size=18):
    """An open concern or question, in red text; returns its bottom."""
    e = text(x, y, s, size, RED)
    return y + e["height"]


def sticky(x, y, w, body, kind, size=18):
    """A note the person can double-click and rewrite; returns its bottom."""
    h = 28 + (body.count("\n") + 1) * size * 1.3
    r = base("rectangle", x, y, w, h, INK, STICKY[kind], sw=1)
    t = text(x + 14, y + 12, body, size, INK, container=r["id"])
    r["boundElements"] = [{"type": "text", "id": t["id"]}]
    return y + h


def legend(x, y):
    """The key, in the studio look (haipipe-studio, JL 261007): black, red = an open concern, green = a
    change. Note kinds are no longer told apart by colour, so the key names only the two marks."""
    text(x, y + 10, "red text = open concern", 15, RED)
    text(x + 230, y + 10, "green ✎ = a change we made", 15, GREEN)


def reply(x, y, s, size=17):
    """A reply to a person's mark, in blue text beside it (the comment loop)."""
    return text(x, y, s, size, BLUE)


def mono(x, y, lines, title, size=15, width=None):
    """Real lines in a rough box with a title above; a line starting with '!' is red.
    Returns (right, bottom)."""
    w = width or max(len(l) for l in lines + [title]) * size * 0.6 + 44
    text(x, y, title, 22, GRAY)
    top = y + 36
    h = 16 + len(lines) * size * 1.3 + 14
    base("rectangle", x, top, w, h, GRAY, "#f8f9fa", sw=1)
    for i, l in enumerate(lines):
        red = l.lstrip().startswith("!")
        text(x + 18, top + 14 + i * size * 1.3, l.replace("!", "", 1) if red else l, size, RED if red else INK, MONO)
    return x + w, top + h


def arrow(x0, y0, x1, y1, label="", color=GRAY, dashed=False):
    e = base("arrow", x0, y0, abs(x1 - x0) or 1, abs(y1 - y0) or 1, color, sw=2, dashed=dashed)
    e.update(points=[[0, 0], [x1 - x0, y1 - y0]], lastCommittedPoint=None, startBinding=None,
             endBinding=None, startArrowhead=None, endArrowhead="arrow")
    if label:
        text(min(x0, x1) + 8, min(y0, y1) - 28, label, 16, color)


def open_frame(name):
    FRAME[0] = None
    fr = base("frame", 0, 0, 10, 10, GRAY, rough=0)
    fr["name"], fr["roundness"] = name, None
    FRAME[0] = fr["id"]
    return fr


def close_frame(fr, pad=50):
    kids = [e for e in els if e.get("frameId") == fr["id"]]
    xs = [e["x"] for e in kids] + [e["x"] + e["width"] for e in kids]
    ys = [e["y"] for e in kids] + [e["y"] + e["height"] for e in kids]
    fr.update(x=min(xs) - pad, y=min(ys) - pad, width=max(xs) - min(xs) + 2 * pad,
              height=max(ys) - min(ys) + 2 * pad)
    FRAME[0] = None
    return fr["y"] + fr["height"]


def questions_frame(x, y, rows, width=760):
    """The Questions frame: one row per (question text, [(note, kind)]) ; red lines are concerns.
    Returns its bottom."""
    fr = open_frame("Questions")
    ry = y
    for q, notes in rows:
        bottom = sticky(x, ry, width, q, "ask")
        nx = x + width + 40
        for body, kind in notes:
            if kind == "red":
                bottom = max(bottom, concern(nx, ry + 6, body))
                nx += max(len(l) for l in body.split("\n")) * 18 * 0.55 + 50
            else:
                bottom = max(bottom, sticky(nx, ry, 440, body, kind))
                nx += 470
        ry = bottom + 60
    return close_frame(fr)


def save(out, source):
    canvas.write(Path(out), els, source)


# ── facts, read from disk ───────────────────────────────────────────────────────────────────
def git_dirs(path):
    """The entries directly under `path` (relative to Tools/) in Tools HEAD."""
    out = subprocess.run(["git", "-C", str(TOOLS), "ls-tree", "--name-only", "HEAD", path.rstrip("/") + "/"],
                         capture_output=True, text=True).stdout.split()
    return [Path(p).name for p in out]


def skill_dirs(folder):
    """Every skill folder (holding SKILL.md) under folder, skipping _/. folders and venue/."""
    return sorted(p.parent for p in folder.rglob("SKILL.md")
                  if not any(x.startswith(("_", ".")) or x == "venue" for x in p.relative_to(folder).parts))


def families(layer):
    return sorted(d for d in (SKILLS / layer).iterdir() if d.is_dir() and not d.name.startswith((".", "_")))


def refs(name, where=TK, exclude=None):
    """Files under `where` that name `name` as a word, minus those under `exclude`."""
    out = subprocess.run(["grep", "-rlIw", "--exclude-dir=.git", "--exclude-dir=node_modules", "--exclude-dir=_legacy",
                          name, str(where)], capture_output=True, text=True).stdout.split()
    return [Path(o) for o in out if not (exclude and o.startswith(str(exclude)))]


def where_short(paths):
    """Group paths by toolkit area: '2_theme/insight', 'servers/workbench-work', ..."""
    out = set()
    for p in paths:
        try:
            r = p.relative_to(TK).parts
        except ValueError:
            out.add(p.relative_to(TOOLS / "plugins").parts[0])
            continue
        out.add("/".join(r[1:3]) if r[0] == "skills" and len(r) > 3 else "/".join(r[:2]) if len(r) > 2 else r[0])
    return sorted(out)


def board_questions(block):
    md = (block / "board.md").read_text(encoding="utf-8")
    return re.findall(r"- id: (\S+)\n(?:\s+title: .+\n)?\s+question: (.+)", md)
