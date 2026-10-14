"""s03 · Delivery: its workbench and its skill: s03-delivery-workbench-skill.excalidraw (haipipe-studio).

Told as a story left to right (JL 261012: "add the UI for the expected UI and card UI for showing the results
of the delivery, what are the current results"):

    ① Delivery today: five screens, five shapes  -->  ② expected: one Delivery for every Block
        -->  ③ one card, one result
    ④ every delivery/ on disk today      the rules: one per Block, one row per send      In Tools

① and ④ are read on every build: each Delivery screen through servers/workbench/frame.py (frame.render, the
Runs panel left out) and each Block's delivery/ off the disk, in the SPACE beside this Tools folder whose Tools/
link leads here. ② and ③ are the proposal (s03-D07, s03-D08), drawn with one real Block's files. The rules frame
(moved here from s09's frame 2 on 261010) and In Tools are as before; the 261011 builder (those two frames
only) is in history/.

A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside the drawing).

    python build_s03_delivery_workbench_skill.py
"""
import html as H
import os
import re
import sys
import textwrap
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]                                   # s03 -> studio -> b10 -> blueprints -> Tools
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
sys.path.insert(0, str(HERE.parent / "s01-overall-tree-structure"))
sys.path.insert(0, str(HERE.parent / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers)
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)
sys.path.insert(0, str(SERVERS / "_host"))

INK, RED, SANS, MONO = L.INK, L.RED, L.SANS, L.MONO
text, path, base = L.text, L.path, L.base
TODAY = "261012"
T, SUB, BODY, HEAD, CODE = 34, 22, 21, 24, 20             # frame title · line under it · words · box titles · paths

SCREENS = [  # (where, folder, what it is): one Delivery screen for each shape there is today
    ("tools", "blueprints/b11_theme_insight", "a plain Block"),
    ("space", "examples-0-cowork/Project-Samsung/cowork/b12_epic_streaming", "cowork: a folder per send"),
    ("space", "examples-0-cowork/Project-SHIFT-Study/cowork/b31_prep_ai", "cowork: delivery.md"),
    ("space", "examples-2-nn/Proj11-CGM-FM/paper/Paper-ScalingGlucose-NatSeries2026", "a paper Board"),
    ("space", "examples-2-nn/Proj11-CGM-FM/paper/Paper-ScalingGlucose-NatSeries2026/j01_v1009_nmi/t01_introduction",
     "a paper Section (a Page Task)"),
]
EXAMPLE = ("space", "examples-2-nn/Proj11-CGM-FM/paper/Paper-ScalingGlucose-NatSeries2026")   # ② and ③'s Block
OPENS = {".pdf": "PDF", ".docx": "Word", ".pptx": "deck", ".html": "web page", ".xlsx": "sheet", ".png": "image"}
KIND_ORDER = ("PDF", "Word", "deck", "web page", "sheet", "image")
NOT_RESULTS = {"history", "__pycache__", "svg", "displays", "sections", "appendices", "draft-bibliography", "figures",
               "draft-sections"}                           # pieces a build puts together, not results


def piece(f: Path):
    """A file a build makes on the way, not one a reader asks for: LaTeX's own master.pdf, a lane's -view page."""
    return f.stem == "master" or f.stem.endswith("-view")


def card(x, y, w, h, title, body, size=24, body_size=21, body_color=INK):
    base("rectangle", x, y, w, h, INK, 1.5)
    text(x + 22, y + 16, title, size)
    if body:
        text(x + 22, y + 16 + size * 1.25 + 14, body, body_size, body_color)


def note(x, y, what, date="261010"):
    e = canvas.change_note(x, y, what, date, L.FRAME[0], 17)
    e["id"] = f"e{len(L.els)}"
    L.els.append(e)


def say(x, y, s, size=BODY, color=INK, font=SANS):
    text(x, y, s, size, color, font)
    return y + size * 1.3 * (s.count("\n") + 1)


def wrap(s, n):
    return "\n".join(textwrap.wrap(s, n)) or s


def rect(x, y, w, h, bold=False, dashed=False, color=INK):
    return base("rectangle", x, y, w, h, color, 3 if bold else 1.5, dashed, rough=0)


# ── facts, read from disk and through frame.py ──────────────────────────────────────────────────
def space_root():
    """The SPACE beside this Tools folder whose Tools/ leads here and that holds the example folders."""
    for d in sorted(TOOLS.parent.iterdir()):
        try:
            if d != TOOLS and (d / "Tools").resolve() == TOOLS.resolve() and \
                    all((d / f).exists() for w, f, *_ in SCREENS if w == "space"):
                return d
        except OSError:
            continue
    return None


def frame_module():
    from host_paths import bootstrap
    bootstrap()
    from live import frame
    return frame


def strip(s):
    s = H.unescape(re.sub(r"<[^>]+>", "", s))
    s = re.sub(r"[\U0001F000-\U0001FFFF☀-➿]️?", "", s)      # emoji: the drawing's font has none
    return re.sub(r"\s+", " ", s).strip()


SCREEN_CACHE = {}


def read_screen(frame, root, folder):
    """What the Delivery screen shows today, top to bottom: the top row; the rows of buttons under it; then each
    heading, table, card, embedded result and empty note of its content (the Runs panel left out)."""
    key = folder.resolve()
    if key in SCREEN_CACHE:
        return SCREEN_CACHE[key]
    theme = frame.themes().get(frame.theme_of(folder, root), frame.VANILLA)
    page = frame.render(theme, root, folder, "Delivery")
    nav = re.search(r'<nav class="row levels">(.*?)</nav>', page, re.S)
    top = []                                          # the top row: a tab, a dropdown's first option, or a divider
    for t in re.findall(r"<a [^>]*>.*?</a>|<select.*?</select>|<span class=bar></span>", nav.group(1) if nav else "",
                        re.S):
        first = re.search(r"<option[^>]*>(.*?)</option>", t, re.S) if t.startswith("<select") else None
        top.append("|" if t.startswith("<span") else strip(first.group(1)) if first else strip(t))
    body = page.split('class="frame-body', 1)[-1]
    head, _, main = body.partition("<div class=space-main>")
    main = main.split("<section class=runs-panel", 1)[0]
    rows = [" · ".join(strip(a) for a in re.findall(r"<a [^>]*>(.*?)</a>", nav, re.S))
            for nav in re.findall(r'<nav class="row subs[^"]*">(.*?)</nav>', head, re.S)]
    items = []
    for m in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>|<table[^>]*>(.*?)</table>|<div class=st-bar>(.*?)</div>"
                         r"|<iframe[^>]*>|<p class=space-empty>(.*?)</p>", main, re.S):
        h, table, bar, empty = m.groups()
        if h is not None:
            items.append(("head", strip(h)))
        elif table is not None:
            cols = [strip(c) for c in re.findall(r"<th[^>]*>(.*?)</th>", table, re.S)]
            cells = [[strip(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
                     for r in re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.S) if "<td" in r]
            items.append(("table", cols, cells))
        elif bar is not None:
            items.append(("card", strip(bar.split("</span></span>")[0])))
        elif empty is not None:
            items.append(("empty", strip(empty)))
        else:
            items.append(("preview",))
    SCREEN_CACHE[key] = {"theme": theme.name, "top": top, "rows": rows, "items": items}
    return SCREEN_CACHE[key]


def send_rows(md: Path):
    """The rows of delivery.md's table (date · for · from · status), as dicts."""
    rows, cols = [], None
    for line in md.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cols is None:
            cols = [c.lower() for c in cells]
        elif not set("".join(cells)) <= set("-: "):
            rows.append(dict(zip(cols, cells)))
    return [r for r in rows if "status" in r]


def results(part: Path, skip=()):
    """{(folder, stem): [files]}: each file a reader opens under part, its twins (a .docx and the .pdf beside it)
    one result; build files, logs, pieces and history/ are not results; skip: folders of other parts."""
    out = {}
    if not part.is_dir():
        return out
    for f in sorted(part.rglob("*")):
        if not f.is_file() or f.name.startswith(".") or f.suffix.lower() not in OPENS or piece(f):
            continue
        if set(f.relative_to(part).parts[:-1]) & NOT_RESULTS or any(s in f.parents for s in skip):
            continue
        out.setdefault((f.parent, f.stem.removesuffix("-tracked")), []).append(f)
    return out


def main_file(files):
    """The file a card is named by: the one a reader asked for (Word before its PDF twin), then by kind."""
    return sorted(files, key=lambda f: (KIND_ORDER.index(OPENS[f.suffix.lower()]) if f.suffix != ".docx" else -1,
                                        f.name))[0]


def checks(screen, block: Path):
    """[(ok, words)]: what this screen gets right or wrong, read from what it shows."""
    items = screen["items"]
    tables = [i for i in items if i[0] == "table"]
    out = []
    shown = sum(1 for i in items if i[0] == "preview")
    out.append((bool(shown), f"{shown} result{'s' * (shown != 1)} shown inside the page" if shown
                else "no result shown: names and counts only"))
    stated = any(i[0] == "card" for i in items) or any("state" in [c.lower() for c in t[1]] for t in tables)
    out.append((stated, "each one's state shown" if stated else "no state: current or stale?"))
    md = block / "delivery" / "delivery.md"
    if md.is_file():
        n = len(send_rows(md))
        seen = any({"date", "for", "status"} <= {c.lower() for c in t[1]} for t in tables)
        out.append((seen, f"delivery.md's {n} send row{'s' * (n != 1)} " + ("shown" if seen else "not shown")))
    else:
        out.append((False, "no delivery.md: what was sent is not written down"))
    for t in tables:
        cols = [c.lower() for c in t[1]]
        if "state" in cols:
            k = cols.index("state")
            bad = [r for r in t[2] if len(r) > k and r[k] == "sent" and any(c.endswith(".py") for c in r)]
            if bad:
                out.append((False, f"{bad[0][k - 1] if k else 'build.py'} listed as a sent message"))
    return out


def shape(screen):
    items = screen["items"]
    kinds = {i[0] for i in items}
    cols = [{c.lower() for c in i[1]} for i in items if i[0] == "table"]
    if "card" in kinds:
        return "a card per lane, embedded"
    if "preview" in kinds:
        return "a preview, then tables"
    if any({"date", "state"} <= c for c in cols):
        return "a table of sends"
    if cols:
        return "a table of files"
    return "empty"


def delivery_blocks(roots):
    """[(root, block, old)]: every Block that keeps a delivery/ under the given tops, the highest delivery/ on
    each path; old = the delivery/ folders under it that a Job, Task or Section still keeps (s03-D01)."""
    found = []
    for root, top in roots:
        if not top.is_dir():
            continue
        for dirpath, dirs, _files in os.walk(top):
            here = Path(dirpath)
            dirs[:] = [d for d in dirs if not d.startswith((".", "_")) and d not in
                       ("node_modules", "history", "delivery", "archive") and len(here.relative_to(top).parts) < 7]
            if (here / "delivery").is_dir():
                found.append((root, here))
    out = []
    for root, b in found:
        if not any(o != b and o in b.parents for _, o in found):
            out.append((root, b, sum(1 for _, o in found if b in o.parents)))
    return out


# ── ① Delivery today: five screens, five shapes ─────────────────────────────────────────────────
def mini_lines(screen):
    """The screen's content as short lines: (words, size, color)."""
    out = []
    if screen["rows"]:
        for r in screen["rows"]:
            out.append((wrap("[ " + r + " ]", 40), 20, INK))
    cards, shown = [], 0
    for it in screen["items"] + [("end",)]:
        if it[0] != "card" and cards:
            out.append((wrap("cards: " + " · ".join(cards), 40), 20, INK))
            cards = []
        if it[0] != "preview" and shown:
            out.append((f"▣ {shown} result{'s' * (shown != 1)} embedded", 20, INK))
            shown = 0
        if it[0] == "head":
            out.append((it[1], 22, INK))
        elif it[0] == "table":
            out.append((wrap("table: " + " · ".join(it[1]), 40) + f"\n   {len(it[2])} row{'s' * (len(it[2]) != 1)}", 20, INK))
        elif it[0] == "card":
            cards.append(it[1] if len(it[1]) <= 26 else it[1][:24].rstrip() + "…")
        elif it[0] == "preview":
            shown += 1
        elif it[0] == "empty":
            out.append((wrap(it[1], 40), 20, INK))
    return out


def frame_today(frame, space):
    fr = L.open_frame("Delivery today")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    say(0, 0, "① Delivery today: five screens, five shapes", T)
    say(0, 58, "Each theme draws Delivery its own way; read through frame.py on this build.", SUB)
    x, top, w = 0, 150, 480
    for where, rel, what in SCREENS:
        root = TOOLS if where == "tools" else space
        folder = root / rel
        sc = read_screen(frame, root, folder)
        block = frame.chain(folder, root).get("Block", folder)
        say(x, top, what, HEAD)
        say(x, top + 36, wrap(folder.name, 38), CODE, font=MONO)
        lines = mini_lines(sc)
        y = top + 100
        rect(x, y, w, 30 + sum(s * 1.3 * (t.count("\n") + 1) + 8 for t, s, _ in lines))
        ly = y + 16
        for t, s, c in lines[:16]:
            ly = say(x + 16, ly, t, s, c) + 8
        y = ly + 30
        for ok, words in checks(sc, block):
            y = say(x, y, wrap(("✓ " if ok else "? ") + words, 40), 20, INK if ok else RED) + 6
        x += w + 40
    note(0, 110, "the five Delivery screens of today, read from frame.py (JL)", TODAY)
    L.close_frame(fr, pad=60)
    return fr


# ── ② expected: one Delivery for every Block ─────────────────────────────────────────────────────
def example_parts(frame, space):
    """The example Block's parts, by source: [(label, folder, {result: files})], the Block's own first."""
    root, block = space, space / EXAMPLE[1]
    parts = frame.delivery_parts(block)
    dirs = [frame.delivery_dir(f) for f, _ in parts]
    out = [("Block", block, results(block / "delivery", skip=dirs))] if results(block / "delivery", skip=dirs) else []
    for f, d in parts:
        own = [x for x in dirs if x != frame.delivery_dir(f) and frame.delivery_dir(f) in x.parents]
        out.append(((f.parent.name.split("_", 1)[0] + " › " if d == 2 else "") + f.name, f,
                    results(frame.delivery_dir(f), skip=own)))
    return root, block, out


def stamp(f: Path):
    size = f.stat().st_size
    words = f"{size / 1024:.1f} KB" if size < 1024 * 1024 else f"{size / 1024 / 1024:.1f} MB"
    return words + " · built " + datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")


def result_card(x, y, w, files, source, h=300, big=False):
    """One result as a card: its kind and name, size and time, where it came from, its sends, the result
    itself (a box standing for the embedded preview), its files."""
    f = main_file(files)
    rect(x, y, w, h, bold=big)
    kind = OPENS[f.suffix.lower()]
    say(x + 18, y + 14, kind, HEAD)
    say(x + 18, y + 48, wrap(f.name, int(w / 12.5)), CODE, font=MONO)
    say(x + 18, y + 48 + 26 * (len(wrap(f.name, int(w / 12.5)).split("\n"))) + 6, stamp(f) + " · from " + source, 20)
    py = y + 150
    rect(x + 18, py, w - 36, h - 150 - 56, dashed=True)
    say(x + 34, py + 14, f"the {kind} itself, embedded", 20)
    twins = " · ".join(g.suffix.lstrip(".") for g in files)
    say(x + 18, y + h - 42, f"files: {twins} ↗   Rebuild ⧉", 20)
    return f


def frame_expected(frame, space):
    fr = L.open_frame("Expected: one Delivery for every Block")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    say(0, 0, "② Expected: one Delivery for every Block", T)
    say(0, 58, "The same screen in every theme: what went out first, then each result as a card, by source (s03-D07).",
        SUB)
    root, block, parts = example_parts(frame, space)
    sc = read_screen(frame, root, block)
    W = 1640
    y0 = 140
    say(0, y0 - 2, f"drawn with {block.name}'s own delivery/, read on this build", 20)
    y = y0 + 40
    # the top row and the source row, as frame.py draws them today
    x = 16
    for label in sc["top"]:
        if label == "|":
            path([(x + 6, y + 8), (x + 6, y + 48)], arrow=False)
            x += 24
            continue
        bw = int(len(label) * 11) + 36
        rect(x, y + 6, bw, 44, bold=label == "Delivery")
        say(x + 16, y + 15, label, 20)
        x += bw + 10
    y += 70
    x = 16
    for label in (sc["rows"][0].split(" · ") if sc["rows"] else []):
        bw = int(len(label) * 11) + 36
        rect(x, y, bw, 40, bold=label == "Block")
        say(x + 16, y + 8, label, 20)
        x += bw + 10
    y += 66
    # sends: delivery.md
    say(16, y, "Sends · delivery/delivery.md", HEAD)
    y += 40
    md = block / "delivery" / "delivery.md"
    rows = send_rows(md) if md.is_file() else []
    for k, c in enumerate(("date", "for", "from", "status")):
        say(16 + k * 380, y, c, 20)
    y += 30
    path([(16, y), (W - 16, y)], arrow=False)
    y += 8
    if rows:
        for r in rows[:3]:
            for k, c in enumerate(("date", "for", "from", "status")):
                say(16 + k * 380, y, wrap(r.get(c, ""), 30).split("\n")[0], 20)
            y += 30
    else:
        say(16, y, "? no delivery.md yet: a row is added when something goes out; only a person writes sent", 20, RED)
        y += 34
    y += 24
    # results by source: the Block's own and the Job's as cards, many small parts as one row each
    say(16, y, "Results · by source", HEAD)
    y += 44
    big = [(label, f, r) for label, f, r in parts if r and " › " not in label]
    small = [(label, f, r) for label, f, r in parts if r and " › " in label]
    for label, f, res in big:
        say(16, y, f"{label} · {len(res)} result{'s' * (len(res) != 1)}", 21)
        y += 36
        cx = 16
        for files in list(res.values())[:3]:
            result_card(cx, y, 520, files, f.name)
            cx += 540
        if len(res) > 3:
            say(cx, y + 130, f"+ {len(res) - 3} more", 21)
        y += 320
    if small:
        say(16, y, f"{len(small)} smaller parts, one row each; pick one in the source row to see its cards", 21)
        y += 36
        for label, f, res in small:
            kinds = sorted({OPENS[main_file(v).suffix.lower()] for v in res.values()}, key=KIND_ORDER.index)
            newest = max((g for v in res.values() for g in v), key=lambda g: g.stat().st_mtime)
            say(16, y, label, 20, font=MONO)
            say(560, y, f"{len(res)} results · " + " · ".join(kinds), 20)
            say(1180, y, "built " + datetime.fromtimestamp(newest.stat().st_mtime).strftime("%m-%d %H:%M"), 20)
            y += 30
    y += 16
    say(16, y, "▸ Checks · the theme's own (a paper: G4 and its word limit), folded under the results", 21)
    y += 40
    rect(0, y0 + 30, W, y - y0 - 20)
    # what each part of the screen is for
    cx, cy = W + 60, y0 + 40
    say(cx, cy, "Why this order", HEAD)
    cy += 44
    for line in ("1  Delivery stays at the right end of the top row (s03-D04).",
                 "2  The source row picks a part: the Block, a Job, a Task (s03-D06).",
                 "3  Sends first: what went out, to whom, draft or sent. Only a person writes sent (s03-D05).",
                 "4  Then the results of the part picked, each one a card with the result inside (③).",
                 "5  Many small parts (a paper's Sections) fold to one row each until one is picked.",
                 "6  A theme adds its own checks under the results, never in place of them."):
        cy = say(cx, cy, wrap(line, 52), 21) + 14
    note(cx, cy + 10, "proposed: one Delivery shape for every theme (s03-D07)", TODAY)
    L.close_frame(fr, pad=60)
    return fr, parts


# ── ③ one card, one result ───────────────────────────────────────────────────────────────────────
PREVIEW_BY_KIND = [("PDF", "the page itself"), ("Word", "its PDF twin, built beside it"),
                   ("deck", "its PDF twin, or its slides as pictures"), ("web page", "the page itself"),
                   ("an email (a folder)", "its draft page, with To, Cc, Subject"), ("sheet", "its first rows"),
                   ("image", "the image"), ("anything else", "its files, listed")]
STATES = [("current", "built after every source it reads"), ("stale", "a source changed after the build"),
          ("not built", "the part exists, its files do not"),
          ("old local", "kept by a Job, Task or Section, not the Block: read only (s03-D01)")]


def frame_card(frame, space, parts):
    fr = L.open_frame("One card, one result")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    say(0, 0, "③ One card, one result", T)
    say(0, 58, "A result is a file a reader opens; its twins are one card. The card holds the result itself (s03-D08).",
        SUB)
    label, src, res = next(((lb, f, r) for lb, f, r in parts if r), ("", None, {}))
    if not res:
        say(0, 140, "? the example Block has no results to draw", BODY, RED)
        L.close_frame(fr, pad=60)
        return fr
    files = sorted(res.values(), key=lambda v: KIND_ORDER.index(OPENS[main_file(v).suffix.lower()]))[0]
    f = main_file(files)
    x, y, w, h = 0, 150, 1060, 900
    rect(x, y, w, h, bold=True)
    kind = OPENS[f.suffix.lower()]
    say(x + 28, y + 24, kind, 28)
    say(x + 28, y + 70, f.name, CODE, font=MONO)
    rect(x + w - 240, y + 22, 200, 46)
    say(x + w - 220, y + 32, "current", 22)
    say(x + 28, y + 116, stamp(f) + f" · from {src.name} ↗", 21)
    say(x + 28, y + 156, "sent: none yet · read from delivery/delivery.md", 21)
    rect(x + 28, y + 206, w - 56, 560, dashed=True)
    say(x + 60, y + 236, f"the {kind} itself, embedded: page 1, scroll for more", 22)
    for k in range(8):                                    # lines standing for the page's text
        path([(x + 60, y + 300 + k * 50), (x + w - 100 - (k % 3) * 120, y + 300 + k * 50)], arrow=False)
    say(x + 28, y + 790, " · ".join(g.relative_to(frame.delivery_dir(src)).as_posix() + " ↗" for g in files), 20,
        font=MONO)
    say(x + 28, y + 830, f"Rebuild ⧉ (copies a prompt; starts nothing)    open {src.name} ↗", 21)
    # callouts: what each part of the card is for
    cx = w + 80
    marks = [(y + 40, "①  kind and name: what a reader gets"),
             (y + 44, "②  state: current · stale · not built · old local"),
             (y + 126, "③  size, when it was built, and the part it came from; the path is the link (s03-D02)"),
             (y + 166, "④  its sends: the rows of delivery.md that name this file, draft or sent"),
             (y + 480, "⑤  the result itself, embedded, so nobody has to download it to look"),
             (y + 800, "⑥  its files, Rebuild, and the way back to its source")]
    cy = y + 10
    for ay, words in marks:
        path([(w + 6, ay + 12), (cx - 10, cy + 12)], arrow=False)          # from the card's edge, at its row
        cy = say(cx, cy, wrap(words, 50), 21) + 26
    # the rules that make a card
    cy += 20
    say(cx, cy, "Preview, by kind", HEAD)
    cy += 40
    for k, v in PREVIEW_BY_KIND:
        say(cx, cy, k, 20)
        say(cx + 280, cy, v, 20)
        cy += 30
    cy += 24
    say(cx, cy, "State, in four words", HEAD)
    cy += 40
    for k, v in STATES:
        say(cx, cy, k, 20)
        cy = say(cx + 160, cy, wrap(v, 42), 20) + 4
    cy += 20
    say(cx, cy, wrap("? stale needs to know what a result read: a Page knows (its check), a cowork build.py lists "
                     "its inputs only in words. One small list per part, written by its build?", 56), 20, RED)
    note(0, y + h + 20, "proposed: one card per result, the result inside (s03-D08)", TODAY)
    L.close_frame(fr, pad=60)
    return fr


# ── ④ every delivery/ on disk today ──────────────────────────────────────────────────────────────
def frame_results(frame, space):
    fr = L.open_frame("Every delivery/ today")
    say(0, 0, "④ Every delivery/ today", T)
    say(0, 58, "Every Block that keeps a delivery/, in this SPACE and in Tools/blueprints/, read on this build.", SUB)
    tops = [(TOOLS, TOOLS / "blueprints")]
    if space:
        tops += [(space, d) for d in sorted(space.glob("examples-*")) if d.is_dir() and "archive" not in d.name]
    cx = {"Block": 0, "theme": 700, "results": 840, "files": 960, "sends": 1060, "old delivery/": 1250,
          "the screen today": 1420, "what is missing": 1720}
    y = 130
    for name, x in cx.items():
        say(x, y, name, 21)
    y += 36
    path([(0, y), (2340, y)], arrow=False)
    y += 10
    for root, block, old in delivery_blocks(tops):
        deliv = block / "delivery"
        nfiles = sum(1 for f in deliv.rglob("*") if f.is_file() and not f.name.startswith(".")
                     and "__pycache__" not in f.parts)
        md = deliv / "delivery.md"
        sends = send_rows(md) if md.is_file() else None
        sc = read_screen(frame, root, block)
        missing = [w for ok, w in checks(sc, block) if not ok]
        rel = block.relative_to(root).as_posix()
        name = wrap(rel.replace("examples-", "ex-"), 54)
        say(cx["Block"], y, name, 20, font=MONO)
        say(cx["theme"], y, sc["theme"], 20)
        say(cx["results"], y, str(len(results(deliv))), 20)
        say(cx["files"], y, str(nfiles), 20)
        sent = "—" if sends is None else (f"{sum(r['status'] == 'sent' for r in sends)} sent · "
                                          f"{sum(r['status'] == 'draft' for r in sends)} draft")
        say(cx["sends"], y, sent, 20)
        say(cx["old delivery/"], y, str(old) if old else "—", 20, RED if old else INK)
        say(cx["the screen today"], y, shape(sc), 20)
        lines = wrap("; ".join(missing), 52) if missing else "—"
        say(cx["what is missing"], y, lines, 20, RED if missing else INK)
        y += 26 * max(lines.count("\n") + 1, name.count("\n") + 1) + 14
    path([(0, y), (2340, y)], arrow=False)
    say(0, y + 16, "results: files a reader opens (PDF, Word, deck, web page, sheet, image), twins as one; files: "
                   "everything; old delivery/: kept below the Block, against s03-D01", 20)
    note(0, y + 56, "every delivery/ on disk, read on each build (JL)", TODAY)
    L.close_frame(fr, pad=60)
    return fr


# ── the rules (261010, unchanged) ────────────────────────────────────────────────────────────────
DELIVERY_TREES = [  # (title, lines): Paper-ScalingGlucose-NatSeries2026/delivery/, read off the disk 261010
    ("named by its source (s02-D14, kept by s03-D05)", [
        ("delivery/", ""),
        ("├── delivery.md", "one row per send: date · for · from · status"),
        ("└── j01_v1009_nmi/", "links to the Job folder j01_v1009_nmi/"),
        ("    ├── latex/  word/", "the whole paper"),
        ("    ├── t00_abstract/ … t21_extended-data/", "each links to its Task folder"),
        ("    └── build.py  paper-build.toml", "how it is built"),
    ]),
]
DELIVERY_OPEN = [
    "? a send that pulls from several Blocks: its own Block, as a paper Board already is",
    "? a Report's own build (delivery/reports/qNN_<topic>/): a row in delivery.md too",
    "? Delivery rows take the Studio's groups (Current and tags)",
]


def delivery_design(x0):
    """The one frame: Jobs and Tasks make outputs, the Block keeps them, one row per send."""
    text(x0, 0, "Delivery: Jobs and Tasks make outputs, the Block keeps them, one row per send", 34)
    text(x0, 52, "The Studio's rule: one per Block, opened from every level. "
                 "Example: Proj11-CGM-FM papers/Paper-ScalingGlucose-NatSeries2026.", 21)
    makers = [("TASK  t01_introduction", "its section, built to latex/"),
              ("TASK  t02_results", "its section, built to latex/"),
              ("JOB  j01_v1009_nmi", "the whole paper: latex/ word/ pdf")]
    for i, (title, body) in enumerate(makers):
        y = 160 + i * 150
        card(x0, y, 560, 110, title, body, 23, 20)
        path([(x0 + 568, y + 55), (x0 + 702, 455)])
    text(x0 + 600, 140, "make", 20)
    card(x0 + 710, 380, 540, 150, "BLOCK  delivery/j01_v1009_nmi/", "kept once, at the Block\nJobs and Tasks keep no delivery/", 23, 20)
    note(x0 + 1270, 444, "named by its source; a send is a row", "261011")      # beside the card it describes
    path([(x0 + 980, 538), (x0 + 980, 642)])
    text(x0 + 1000, 572, "a person sends it", 20)
    card(x0 + 710, 650, 540, 130, "SENT  to NMI", "a row in delivery.md: draft → sent\nset by a person, never by a build", 23, 20)
    card(x0, 1080, 1250, 140, "SKILL  /haipipe-delivery  (skills/1_base/project)",
         "owns: the Block's delivery/, its paths, the Delivery view, sent by a person\n"
         "builds by: haipipe-draft-delivery · haipipe-paper-assemble · haipipe-design-delivery · haipipe-cowork", 23, 20)
    note(x0, 1232, "the skill haipipe-delivery is made: one owner for the Block-only rule (JL)")
    text(x0, 840, "Rules", 25)
    text(x0, 884, "Jobs and Tasks make deliveries but keep no delivery/; they keep their own Report (s09-D02)\n"
                  "every writer goes through one helper, haipipe-draft/src/common.py (s02-D14)\n"
                  "Runs and Results stay with their source; only built files land in delivery/\n"
                  "opened from Job j01, Delivery is the Block's, with j01 picked in its source row (s03-D06)\n"
                  "Delivery sits at the right end of the top row: Studio | Block · Job · Task | Delivery", 20)
    xr = x0 + 1360
    text(xr, 140, "Storage", 25)
    y = 190
    for title, lines in DELIVERY_TREES:
        text(xr, y, title, 22)
        for i, (line, meaning) in enumerate(lines):
            text(xr, y + 40 + i * 30, line, 20, INK, MONO)
            if meaning:
                text(xr + 560, y + 41 + i * 30, meaning, 20)
        y += 40 + len(lines) * 30 + 40
    card(xr, 560, 540, 230, "delivery.md  · one row per send",
         "date     for          from        status\n261009   NMI          j01_v1009   sent\n"
         "261012   co-authors   j01_v1009   draft\na resend is a row, not a copy", 22, 20)
    note(xr, 800, "dNN dropped: the path stays the link, and dNN is a design in b12", "261011")
    card(xr + 580, 560, 560, 230, "Delivery · opened from Job j01",
         "the Block's Delivery, not j01's own\n[ Paper Board ] [ j01 · v1009 nmi ] [ j01 › t00 ]\n"
         "its part: delivery/j01_v1009_nmi/ · from j01\nthe Block's own view ends with By source", 22, 20)
    note(xr + 580, 800, "from a Job or Task: the Block's Delivery, its source picked", "261011")
    for i, q in enumerate(DELIVERY_OPEN):
        text(xr, 860 + i * 36, q, 21, RED)


# ── the story ────────────────────────────────────────────────────────────────────────────────────
def main():
    out = HERE / "s03-delivery-workbench-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    frame = frame_module()
    space = space_root()
    if space is None:
        raise SystemExit("no SPACE beside Tools/ holds the example folders; ① to ④ need one")
    today = frame_today(frame, space)
    expected, parts = frame_expected(frame, space)
    one = frame_card(frame, space, parts)
    story = [today, expected, one]
    tall = max(f["height"] for f in story)
    for f in story:                                   # one strip: every chapter the same height
        f["height"] = tall
    every = frame_results(frame, space)
    fr = L.open_frame("Delivery: one per Block, one row per send")
    delivery_design(0)
    L.close_frame(fr)
    tools = L.tools_frame(                                # the skill's folder and its code (JL 261011)
        "In Tools: haipipe-delivery", ["1_base/project/haipipe-delivery"],
        [("servers/workbench/frame.py", ["delivery_parts", "_delivery_row", "delivery_by_source", "_delivery_cards"]),
         ("skills/1_base/page/haipipe-draft/src/common.py",
          ["delivery_owner", "delivery_dir", "delivery_source", "delivery_relative"])],
        around=["haipipe-draft-delivery builds a Page's lanes", "haipipe-paper-assemble builds the paper",
                "haipipe-design-delivery releases a design Job", "haipipe-cowork keeps a drafted email or reply",
                "haipipe-related keeps what came in, the twin"],
        note="its skill's folder and code, read from disk (JL)")
    canvas.grid(L.els, [[f["id"] for f in story], [every["id"], fr["id"], tools["id"]]], gap=260)

    top = story[0]["y"]
    L.FRAME[0] = None
    text(0, top - 250, "s03 in one sentence: today each theme shows Delivery its own way ①; expected, one Delivery "
                       "for every Block, what went out first, then its results by source ②; each result one card, "
                       "the result itself inside ③.", 40)
    text(0, top - 180, "Read left to right along the arrows. Below the strip: every delivery/ on disk today, the rules "
                       "(one per Block, one row per send), and In Tools.", BODY)
    for k, what in enumerate(("Delivery UI drawn as a story: today, expected, one card per result (JL)",
                              "every Block's delivery/ read on each build; the two-frame builder in history/")):
        L.els.append(canvas.change_note(0, top - 130 + k * 26, what, TODAY, None, size=18))
    for a, b, word in zip(story, story[1:], ("one shape for every theme", "zoom into one card")):
        ay = a["y"] + 180
        x0, x1 = a["x"] + a["width"] + 20, b["x"] - 20
        path([(x0, ay), (x1, ay)])
        L.els[-1]["strokeWidth"] = 3
        text(x0 + 10, ay - 44, wrap(word, 18), HEAD)
    ax = today["x"] + 200
    path([(ax, today["y"] + today["height"] + 20), (ax, every["y"] - 20)], dashed=True)
    text(ax + 20, today["y"] + today["height"] + 90, "every Block, row by row", HEAD)
    for e in canvas.off_palette(L.els):                  # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, list(L.els), "build_s03_delivery_workbench_skill.py")


if __name__ == "__main__":
    main()
