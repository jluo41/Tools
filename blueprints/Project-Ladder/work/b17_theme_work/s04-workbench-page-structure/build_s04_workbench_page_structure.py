"""b17-s04:theme_work @ workbench_page_structure, its drawing: haipipe-studio's five parts (scripts/five_parts.py).
Narrowed on 261031 to what every work page shares, the same at Block, Job and Task (JL 261031: "the interface and the
Block UI Job UI and Task UI, there are some overlap, right?"); each level's Report, Work and Studio are the nine cells'
(s51 to s59, drawn by j03's work_ui_cells.py). The builder before the narrowing is kept in result/old-design-261031/.

Its Design: A, the frame every work page wears, drawn on j03's own page with its parts numbered, and under it the same
frame at the three levels; B, the right-rail's other sections, one card each, then the Interactions page's three
designs from the waiting form, the open question in red. Every fact is read from disk on every build: the right-rail,
its lines, the goal-line words and the view-captions from servers/workbench/focus_page.py, each section's verb from
haipipe-ui, the left-rail from b17's folders, the goal from j03's face, the pieces from delivery/render.yaml, the three
designs from ../runs/r02_collect_interactions_page/. The first drawing stays whole below the Design, at 40%, its
screenshot kept.

    python build_s04_workbench_page_structure.py      writes the .excalidraw and its card, the .png
"""
import ast
import json
import re
import sys
import textwrap
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402  (underscore names skip the star import)
import five_parts  # noqa: E402

BLOCK = HERE.parent
J03 = BLOCK / "j03_work_workbench_pages"
FORM = BLOCK / "runs" / "r02_collect_interactions_page"
FOCUS = TOOLS / "plugins/haipipe-toolkit/servers/workbench/focus_page.py"
UI_SKILL = TOOLS / "plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/SKILL.md"
SRC = FOCUS.read_text(encoding="utf-8")
TREE = ast.parse(SRC)
OTHER = ("interactions", "delivery", "related", "timeline", "files")      # the right-rail's other sections (s04-D05)


# ── what focus_page.py says, read on every build ───────────────────────────────────────────────────────────────────
def assigned(name):
    """The literal focus_page.py assigns to `name`, at module level or inside render() (a dict indexed at once too)."""
    for node in ast.walk(TREE):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value.value if isinstance(node.value, ast.Subscript) else node.value)
    raise LookupError(f"focus_page.py assigns no {name}")


def function(name):
    return next(n for n in ast.walk(TREE) if isinstance(n, ast.FunctionDef) and n.name == name)


def rail_lines():
    """Each right-rail section's one line, from describe() inside render(); Interactions' three states in its order."""
    fn = function("describe")
    words = {}
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get" \
                and isinstance(n.func.value, ast.Dict):
            words.update(ast.literal_eval(n.func.value))
    said = [n.value for n in sorted((n for n in ast.walk(fn) if isinstance(n, ast.Constant) and isinstance(n.value, str)
                                     and " " in n.value), key=lambda n: (n.lineno, n.col_offset))]
    words["interactions"] = [s for s in said if "waits on you" in s or "asked yet" in s]
    words["studio"] = next(s for s in said if "drawings" in s)
    words["delivery_empty"] = next(s for s in said if "handed over yet" in s)
    return words


def interaction_views():
    """Interactions' view-button-list: the DictComp in render() that builds All, Needs your input, Answered."""
    for n in ast.walk(function("render")):
        if isinstance(n, ast.DictComp) and isinstance(n.generators[0].iter, ast.Tuple):
            pairs = ast.literal_eval(n.generators[0].iter)
            if any(key == "waiting" for key, _ in pairs):
                return [name for _, name in pairs]
    raise LookupError("focus_page.render builds no Interactions views")


GOAL_WORD = assigned("GOAL_WORD")                      # Purpose · Goal · Aim, by level
VIEW_WORDS = assigned("VIEW_WORDS")                    # the view-caption of each view
BELOW = assigned("below_names")                        # what a level's Work lists
ONE_VIEW = assigned("one")                             # the one button of a one-view section
RAIL = re.findall(r'rail\.append\(\("(\w+)", "([^"]+)", ""\)\)', SRC)   # the right-rail, in its order
LABEL = dict(RAIL)
OPENS = re.search(r'opens = "(\w+)" if overview and level == "(\w+)" else "(\w+)"', SRC).groups()   # report, Block, work
PROGRESS = re.search(r'work = \{"progress": \(.*?else "(\w+)"', SRC).group(1)                    # Work's first view
LINES = rail_lines()
VERB = dict(re.findall(r"(?m)^(Report|Work|Studio|Interactions|Delivery|Related|Timeline|Files)\s+(\S+(?: \S+)?)\s{2,}",
                       UI_SKILL.read_text(encoding="utf-8")))               # haipipe-ui's Sections table: one verb each
OWNER = {"interactions": "haipipe-interaction", "delivery": "haipipe-delivery", "related": "haipipe-related",
         "timeline": "the workbench", "files": "the workbench"}
WHEN = {"interactions": "always on the rail", "delivery": "always on the rail", "related": "when it holds something",
        "timeline": "when something happened", "files": "always on the rail"}                     # s04-D09


# ── b17's own folders: the left-rail and the faces ──────────────────────────────────────────────────────────────────
def field(face: Path, key: str) -> str:
    m = re.search(rf"(?m)^{key}:\s*(.+)$", face.read_text(encoding="utf-8")) if face.is_file() else None
    return m.group(1).strip() if m else ""


def has_face(p: Path, pattern: str) -> bool:
    return p.is_dir() and bool(re.match(pattern, p.name)) and (p / f"{p.name}.md").is_file()


def rail_kids(folder: Path) -> list:
    """A level's sNN first, then its Jobs or Tasks, as focus_page.rail_kids lists them."""
    kids = sorted(folder.iterdir())
    return [p for p in kids if has_face(p, r"s\d{2}[-_]")] + [p for p in kids if has_face(p, r"[jt]\d+_")]


def left_rail(page: Path) -> list:
    """(name, depth, here) down the left-rail of a page: its siblings, the open page's children under it."""
    if re.match(r"b\d+_", page.name):
        sibs = [p for p in sorted(page.parent.iterdir()) if p.is_dir() and re.match(r"b\d+_", p.name)]
    else:
        sibs = rail_kids(page.parent)
    out = []
    for s in sibs:
        out.append((s.name, 0, s == page))
        out += [(k.name, 1, False) for k in rail_kids(page)] if s == page else []
    return out


def rail_words(page: Path) -> str:
    """The left-rail of a page in a few words: its siblings by id, then the children under the open one."""
    short = lambda n: n.split("-")[0] if re.match(r"s\d{2}-", n) else n.split("_")[0]   # noqa: E731
    rows = left_rail(page)
    sibs = [short(n) for n, d, _ in rows if d == 0]
    kids = [short(n) for n, d, _ in rows if d == 1]
    sib = f"{sibs[0]} … {sibs[-1]}" if len(sibs) > 6 else " ".join(sibs)
    return f"{sib}; under {short(page.name)}: {' '.join(kids)}" if kids else sib


def form_questions():
    """The waiting form: Q1's words and its options (letter, words, my pick), Q2's words and its pick, its status."""
    text = (FORM / "question_collection.md").read_text(encoding="utf-8")
    parts = re.split(r"(?m)^## ", text)[1:]
    opts = lambda q: re.findall(r"(?m)^- \[( |x)\] ([A-Z]) · (.+)$", q)  # noqa: E731
    ask1 = re.search(r"\*\*(.+?)\*\*", parts[0]).group(1)
    ask2 = re.search(r"\*\*(.+?)\*\*", parts[1]).group(1)
    pick2 = next((w for t, _, w in opts(parts[1]) if t == "x"), "")
    status = (yaml.safe_load((FORM / "run.yaml").read_text(encoding="utf-8")) or {}).get("status", "")
    return ask1, [(letter, words, t == "x") for t, letter, words in opts(parts[0])], ask2, pick2, status


# ── the spec: Idea's words; what it hands over comes from delivery/render.yaml ────────────────────────────────────────
PIECES = [pc["code"].partition(": ")[::2] for pc in yaml.safe_load((HERE / "delivery/render.yaml").read_text())["pieces"]]
UI = HERE / "delivery" / "ui"
SPEC = {
    "title": "Workbench page structure: what every work page shares",
    "why": {"question": "why do we need s04?",
            "notes": ["the frame was\ndrawn in all\nnine cells", "path and rails:\nthe same at Block,\nJob and Task",
                      "Interactions,\nDelivery, Files:\nno cell owns them"],
            "quote": 'JL 261031: "the interface and the Block UI Job UI and\nTask UI, there are some overlap, right?"'},
    "what": {"head": "② what s04 hands over: the shared parts", "icon": "page", "name": "delivery/ui/", "type": "ui",
             "deck_why": "stays in s04's delivery/deck/, so anyone gets it in a minute",
             "parts": [("page", f"ui/{name}", why, (UI / name).exists()) for name, why in PIECES]},
    "job": J03,
    "target": "servers/workbench/focus_page.py: page_shell, render (design_b02_workbench)",
    "missing": [(f"ui/{name}", "the agreed screen draft, not drawn yet") for name, _ in PIECES if not (UI / name).exists()],
}


# ── drawing helpers ──────────────────────────────────────────────────────────────────────────────────────────────────
def window(eid, x, y, w, h, url):
    """A browser window, drawn plainly: a frame and its address bar."""
    els = [_el("rectangle", eid, x, y, w, h, INK, "#ffffff", roundness={"type": 3})]
    els += line(eid + "_bar", [(x, y + 28), (x + w, y + 28)], ROOM, 1)
    return els + [_el("ellipse", f"{eid}_d{k}", x + 10 + k * 14, y + 9, 9, 9, ROOM, ROOM) for k in range(3)] + \
        text(eid + "_url", x + 60, y + 7, url, 12, BODY)


def mark(eid, x, y, n):
    """A part's number, orange, where the part sits; the legend under the window names it."""
    return [_el("ellipse", eid, x, y, 22, 22, OR, "#fff4e6", strokeWidth=1)] + \
        text(eid + "_n", x + 11, y + 3, str(n), 12, OR, "center")


def button(eid, x, y, words, on=False, size=11):
    w = len(words) * size * 0.62 + 14
    return [_el("rectangle", eid, x, y, w, size + 11, OR if on else ROOM, "#fff4e6" if on else "#ffffff",
                roundness={"type": 3}, strokeWidth=1)] + text(eid + "_t", x + 7, y + 4, words, size, INK), w


def buttons(eid, x, y, names, size=11):
    els = []
    for k, name in enumerate(names):
        b, w = button(f"{eid}{k}", x, y, name, k == 0, size)
        els += b
        x += w + 6
    return els


def grey_lines(eid, x, y, w, n, step=16):
    """Lines standing in for text, each a little shorter than the one before, never past its left edge."""
    return [e for k in range(n) for e in line(f"{eid}{k}", [(x, y + step * k), (x + w * (1 - 0.22 * (k % 3)), y + step * k)], ROOM, 2)]


# ── A: the frame every work page wears, on j03's own page ────────────────────────────────────────────────────────────
WX, WY, WW, WH = 690, 340, 900, 470
CX = 924                                               # the content column; the left-rail sits left of it


def design_a():
    els = text("s4A", 690, 280, "A · the frame every work page wears, the same at Block, Job and Task", 18, TITLE)
    els += shapes("s4A_s", 690, 306, "delivery/ui/frame  (j03 t04)")
    rel = J03.relative_to(BLOCK.parent)
    els += window("s4w", WX, WY, WW, WH, f"…/_board/workbench?path=…/{rel.as_posix()}&layout=focus")
    # the left-rail: siblings, the open page's children under it, pale short lines until hovered (s04-D11)
    els += mark("s4m7", 704, 372, 7)
    for k, (name, depth, here) in enumerate(left_rail(J03)):
        y = 404 + 19 * k
        els += line(f"s4l{k}", [(704 + 12 * depth, y + 7), (714 + 12 * depth, y + 7)], OR if here else ROOM, 3 if here else 1)
        els += text(f"s4l{k}_t", 720 + 12 * depth, y, name, 10, OR if here else BODY)
    # the top of the page: path, title-&-section, view-button-list, goal-line, view-caption (s04-D10)
    section = LABEL[OPENS[0]] if OPENS[1] == "Job" else LABEL[OPENS[2]]   # the section a Job's page opens on
    els += mark("s4m1", 898, 378, 1) + text("s4p", CX, 382, f"… / work / {BLOCK.name} / {J03.name}", 11, BODY)
    els += mark("s4m2", 898, 406, 2) + text("s4t", CX, 402, J03.name, 20, INK)
    els += text("s4t_s", CX + len(J03.name) * 12.4 + 12, 407, section, 15, ROOM)
    els += mark("s4m3", 898, 440, 3) + buttons("s4v", CX, 440, [PROGRESS])
    goal = textwrap.shorten(field(J03 / f"{J03.name}.md", "goal"), 58, placeholder="…")
    els += mark("s4m4", 898, 474, 4) + text("s4g_w", CX, 478, GOAL_WORD["Job"], 11, ROOM) + text("s4g", CX + 36, 478, goal, 11, INK)
    els += mark("s4m5", 898, 500, 5) + text("s4c", CX, 504, VIEW_WORDS["progress"], 11, BODY)
    # the content: each level's Report, Work and Studio, the nine cells' part, never s04's
    els += [_el("rectangle", "s4body", CX, 530, 426, 250, ROOM, "#ffffff", strokeStyle="dashed", roundness={"type": 3})]
    els += mark("s4m6", 898, 534, 6) + text("s4body_t", CX + 16, 546, "content: the open view", 13, ROOM)
    els += text("s4body_w", CX + 16, 570, "each level's Report · Work · Studio\nthe nine cells' part, s51 to s59", 12, BODY)
    els += grey_lines("s4body_l", CX + 16, 622, 260, 3)
    # the pop-out: a Run, a file or a topic's part opens over the page; Close returns to the same place (s04-D08)
    els += [_el("rectangle", "s4pop", 1070, 660, 280, 120, INK, "#ffffff", roundness={"type": 3})]
    els += line("s4pop_bar", [(1070, 686), (1350, 686)], ROOM, 1)
    els += text("s4pop_t", 1080, 666, "run-design-shared-parts", 11, INK)
    els += [_el("rectangle", "s4pop_x", 1300, 664, 42, 18, ROOM, "#ffffff", roundness={"type": 3}, strokeWidth=1)]
    els += text("s4pop_x_t", 1306, 666, "Close", 10, BODY) + grey_lines("s4pop_l", 1084, 704, 230, 4, 18)
    els += mark("s4m9", 1044, 650, 9)
    # the right-rail: every section with its one line; the five after Studio are B's
    els += mark("s4m8", 1372, 372, 8)
    for k, (key, label) in enumerate(RAIL):
        y, here = 404 + 48 * k, key == section.lower()
        words = (LINES["interactions"][0] if key == "interactions" else LINES["studio"] if key == "studio"
                 else f"its {BELOW['Job']}" if key == "work"
                 else LINES["delivery_empty"] if key == "delivery" and not (J03 / "delivery").is_dir()
                 else LINES.get(key, ""))
        shown = key != "related" or (J03 / "related").is_dir()
        els += line(f"s4r{k}", [(1374, y + 8), (1386, y + 8)], OR if here else ROOM, 3 if here else 1, dashed=not shown)
        els += text(f"s4r{k}_t", 1394, y, label, 12, OR if here else INK if shown else ROOM)
        els += text(f"s4r{k}_w", 1394, y + 17, "\n".join(textwrap.wrap(words, 30)[:2]), 10, BODY if shown else ROOM)
    first = next(k for k, (key, _) in enumerate(RAIL) if key == OTHER[0])
    y0, y1 = 404 + 48 * first - 4, 404 + 48 * len(RAIL) - 10
    els += line("s4brace", [(1366, y0), (1362, y0), (1362, y1), (1366, y1)], OR, 2)
    els += arrow("s4toB", [(1592, (y0 + y1) / 2), (1624, (y0 + y1) / 2)], OR, width=2)
    # the phone: both rails hide; the right-rail becomes one section-line above the view-button-list
    PX, PY = 690, 836
    els += [_el("rectangle", "s4ph", PX, PY, 96, 176, INK, "#ffffff", roundness={"type": 3})]
    els += grey_lines("s4ph_a", PX + 10, PY + 16, 70, 1) + line("s4ph_t", [(PX + 10, PY + 30), (PX + 66, PY + 30)], INK, 3)
    for k in range(4):
        els += [_el("rectangle", f"s4ph_s{k}", PX + 9 + 20 * k, PY + 42, 17, 10, OR if k == 1 else ROOM, "#ffffff", strokeWidth=1)]
    els += [_el("rectangle", "s4ph_v", PX + 10, PY + 60, 30, 10, OR, "#fff4e6", strokeWidth=1)]
    els += grey_lines("s4ph_l", PX + 10, PY + 84, 76, 5, 15) + mark("s4m10", PX + 82, PY - 10, 10)
    # the legend: each number's part, by haipipe-ui's names
    legend = [("path", "the SPACE down to this page"), ("title-&-section", "its name, then the section"),
              ("view-button-list", "the open section's views"),
              ("goal-line", " · ".join(GOAL_WORD[lv] for lv in ("Block", "Job", "Task")) + ", by level"),
              ("view-caption", "what the open view shows"), ("content", "the open view, the cells' part"),
              ("left-rail", "change page; siblings, then children"), ("right-rail", "change section; one line each"),
              ("pop-out", "a Run, a file or a part, over the page"),
              ("phone", "the rails hide; one section-line on top")]
    for k, (name, what) in enumerate(legend):
        x, y = (812, 838 + 28 * k) if k < 5 else (1210, 838 + 28 * (k - 5))
        els += mark(f"s4k{k}", x, y, k + 1) + text(f"s4k{k}_t", x + 30, y + 3, f"{name}: {what}", 12, INK)
    # the same frame at three levels: only its words change
    pages = (("Block", BLOCK), ("Job", J03), ("Task", next(t for t in rail_kids(J03) if t.name.startswith("t"))))
    rows = [[lv, GOAL_WORD[lv], f"its {BELOW[lv]}", LABEL[OPENS[0]] if lv == OPENS[1] else LABEL[OPENS[2]], rail_words(p)]
            for lv, p in pages]
    t, _ = data_table("s4lv", 690, 1048, "the same frame at three levels: only its words change",
                      ["level", "goal-line", "Work lists", "opens on", "left-rail, on b17's own pages"],
                      [62, 84, 92, 84, 430], rows, TITLE, "#eef2ff")
    return els + t


# ── B: the right-rail's other sections, then the Interactions page's three designs ──────────────────────────────────
BX, BW = 1636, 530


def thumb(eid, x, y, letter):
    """A design of the Interactions page, small: A grouped questions over a fixed copy bar, B two lanes with pictures,
    C a checklist with one form open."""
    w, h = 166, 128
    els = [_el("rectangle", eid, x, y, w, h, INK, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_l", x + 8, y + 6, letter, 16, TITLE)
    if letter == "A":
        for g in range(2):
            gy = y + 30 + 38 * g
            els += line(f"{eid}_g{g}", [(x + 28, gy), (x + 90, gy)], INK, 2)
            els += grey_lines(f"{eid}_q{g}", x + 34, gy + 12, 110, 2, 11)
        els += [_el("rectangle", eid + "_bar", x + 6, y + h - 22, w - 12, 16, OR, "#fff4e6", strokeWidth=1)]
        els += text(eid + "_bar_t", x + 14, y + h - 21, "📋 copy all", 10, INK)
    elif letter == "B":
        els += line(eid + "_mid", [(x + w / 2, y + 28), (x + w / 2, y + h - 8)], ROOM, 1)
        els += text(eid + "_h0", x + 10, y + 30, "waits", 10, OR) + text(eid + "_h1", x + w / 2 + 8, y + 30, "answered", 10, GR)
        for k in range(4):
            els += [_el("rectangle", f"{eid}_p{k}", x + 10 + 36 * (k % 2), y + 50 + 34 * (k // 2), 30, 26, ROOM, "#f1f3f5", strokeWidth=1)]
        els += grey_lines(eid + "_a", x + w / 2 + 8, y + 54, 70, 3, 14)
    else:
        for k, ry in enumerate((y + 28, y + 88, y + 106)):           # form 1 open; 2 and 3 folded below it
            els += text(f"{eid}_n{k}", x + 10, ry, str(k + 1), 11, OR if k == 0 else BODY)
            els += line(f"{eid}_r{k}", [(x + 26, ry + 7), (x + 140, ry + 7)], INK if k == 0 else ROOM, 2 if k == 0 else 1)
        els += grey_lines(eid + "_o", x + 34, y + 46, 100, 2, 11)
        els += [_el("rectangle", eid + "_keep", x + 34, y + 66, 40, 14, GR, "#ebfbee", strokeWidth=1),
                _el("rectangle", eid + "_leave", x + 80, y + 66, 40, 14, ROOM, "#ffffff", strokeWidth=1)]
    return els


def design_b():
    els = text("s4B", BX, 280, "B · the right-rail's other sections", 18, TITLE)
    els += shapes("s4B_s", BX, 306, "ui/interactions, delivery, related, timeline, files")
    for k, key in enumerate(OTHER):
        y = 340 + 82 * k
        label = LABEL[key]
        els += [_el("rectangle", f"s4o{k}", BX, y, BW, 72, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"s4o{k}_n", BX + 14, y + 8, label, 15, TITLE)
        els += text(f"s4o{k}_v", BX + 26 + len(label) * 9.3, y + 11, VERB.get(label, ""), 13, ROOM)
        els += text(f"s4o{k}_o", BX + BW - 14 - len(OWNER[key]) * 7.44, y + 10, OWNER[key], 12, GR)
        said = " · ".join(LINES[key]) if key == "interactions" else LINES[key]
        els += text(f"s4o{k}_w", BX + 14, y + 31, said, 12, BODY)
        views = interaction_views() if key == "interactions" else [ONE_VIEW[key]]
        els += buttons(f"s4o{k}_b", BX + 14, y + 50, views, 10)
        els += text(f"s4o{k}_when", BX + BW - 14 - len(WHEN[key]) * 6.82, y + 52, WHEN[key], 11, ROOM)
    ask1, options, ask2, pick2, status = form_questions()
    y = 770
    els += text("s4i", BX, y, "the Interactions page, three designs", 15, TITLE)
    els += text("s4i_s", BX, y + 24, f"{FORM.name} · {status}", 12, OR)
    for k, (letter, words, picked) in enumerate(options):
        x = BX + 182 * k
        els += thumb(f"s4d{k}", x, y + 52, letter)
        els += text(f"s4d{k}_w", x, y + 188, "\n".join(textwrap.wrap(words.rstrip("."), 24)[:3]), 11, INK)
        if picked:                                               # my pick, boxed in orange with its caption
            els += [_el("rectangle", f"s4d{k}_pick", x - 8, y + 44, 182, 196, OR, "transparent", strokeWidth=2,
                        roundness={"type": 3})]
            els += text(f"s4d{k}_pick_t", x + 83, y + 246, "my pick", 13, OR, "center")
    els += text("s4i_q2", BX, y + 280, f"and {ask2[0].lower() + ask2[1:]} my pick: {pick2.split(':')[0].rstrip('.')}", 12, BODY)
    letters = [letter for letter, _, _ in options]
    words = textwrap.wrap("? " + ask1[0].lower() + ask1[1:].rstrip("?") + ":", 28) + \
        [", ".join(letters[:-1]) + f" or {letters[-1]}"]
    els += sticky("s4ask", BX + 265, y + 360, 330, 82, "\n".join(words), 15, -0.02, RED, RE)
    return els


def sketches():
    return design_a() + design_b()


# ── the first drawing, kept whole below ──────────────────────────────────────────────────────────────────────────────
def keep_files(out: Path, *sources: Path) -> None:
    """five_parts writes no images; carry the kept drawing's embedded pictures over, so its screenshot still shows."""
    d = json.loads(out.read_text(encoding="utf-8"))
    for src in sources:
        if src.is_file():
            d["files"].update(json.loads(src.read_text(encoding="utf-8")).get("files", {}))
    out.write_text(json.dumps(d, ensure_ascii=False) + "\n", encoding="utf-8")


def smaller(els, x0, y0, s=0.4):
    """The kept first drawing at 40% size: the viewer fits the whole canvas but never below 10% zoom, so a full-size
    old drawing (about 8,000 px tall) opened on its own frames and hid the five parts above it (261031)."""
    for e in els:
        if not e["id"].startswith("kept_") or e["id"] in ("kept_h", "kept_rule"):
            continue
        e["x"], e["y"] = x0 + (e["x"] - x0) * s, y0 + (e["y"] - y0) * s
        e["width"], e["height"] = e["width"] * s, e["height"] * s
        if "fontSize" in e:
            e["fontSize"] = max(1, round(e["fontSize"] * s))
        if "points" in e:
            e["points"] = [[px * s, py * s] for px, py in e["points"]]
    return els


if __name__ == "__main__":
    wide = max(e["x"] + e["width"] for e in sketches())          # Process and Delivery start past the Design
    shift = max(1050, int((wide - 690) * five_parts.GROW + 690 + five_parts.MOVE - 2020 + 120))

    def with_kept():
        els = sketches()
        top = max(e["y"] + e["height"] for e in els) + 120
        return els + smaller(kept_first(HERE, top), 690, top + 70)
    out = five_parts.build(HERE, SPEC, with_kept, shift)
    keep_files(out, HERE / "result" / "first-drawing.excalidraw")
