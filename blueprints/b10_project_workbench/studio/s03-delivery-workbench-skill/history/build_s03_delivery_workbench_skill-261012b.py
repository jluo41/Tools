"""s03 · Delivery: its workbench and its skill: s03-delivery-workbench-skill.excalidraw (haipipe-studio).

Three frames, each a folder tree or a screen (JL 261012: "每一个 frame 都太像一张 slide ... 我个人更 prefer 那种 tree
结构，就像 folder tree 那样"):

    ① Background   a newcomer's frame: what Delivery is, the words it uses, where it sits
    ② the Tree     the topic itself: today's five screens, every delivery/ on disk, the rules, the proposals,
                   In Tools; red "? " leaves are still open, "✎ " leaves are changes
    ③ the screen   the expected Delivery (s03-D07) with one result card close up (s03-D08), in the workbench's colours

Read on every build: each Delivery screen through servers/workbench/frame.py (frame.render, the Runs panel left
out), every Block's delivery/ off the disk (in Tools/blueprints and in the SPACE beside Tools whose Tools/ link
leads here), the decisions and open items of this topic's face, and the skill's folder and functions. The 261011
builder (two frames) and the 261012 story builder (six frames) are in history/.

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
    ("space", "examples-0-cowork/Project-SHIFT-Study/cowork/b04_prep_ai", "cowork: delivery.md"),
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



PREVIEW_BY_KIND = [("PDF", "the page itself"), ("Word", "its PDF twin, built beside it"),
                   ("deck", "its PDF twin, or its slides as pictures"), ("web page", "the page itself"),
                   ("an email (a folder)", "its draft page, with To, Cc, Subject"), ("sheet", "its first rows"),
                   ("image", "the image"), ("anything else", "its files, listed")]
STATES = [("current", "built after every source it reads"), ("stale", "a source changed after the build"),
          ("not built", "the part exists, its files do not"),
          ("old local", "kept by a Job, Task or Section, not the Block: read only (s03-D01)")]


# ── what the face says, read off the face ────────────────────────────────────────────────────────
FACE = HERE / "s03-delivery-workbench-skill.md"


def short(s, most=150):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= most else s[:most - 1].rstrip() + "…"


def decision(n):
    """s03-DNN's first sentence, read off the face (Decided and Proposed)."""
    hit = re.search(rf"(?ms)^s03-D{n:02d} · (.*?)(?=^\S|\Z)", FACE.read_text(encoding="utf-8"))
    if not hit:
        return f"s03-D{n:02d}: not in the face"
    body = re.sub(r"\s+", " ", hit.group(1)).strip()
    body = re.sub(r"^Proposed \(JL \d+\): ", "", body)
    return short(f"s03-D{n:02d} · " + body, 190)


def open_item(n):
    """Open item n off the face, as a red leaf."""
    sec = FACE.read_text(encoding="utf-8").split("\nOpen\n----\n", 1)[-1]
    hit = re.search(rf"(?ms)^{n}\. (.*?)(?=^\d+\. |^\(write here|\Z)", sec)
    return "? " + short(hit.group(1), 200) if hit else f"? open item {n}: not in the face"


# ── In Tools, read off the disk ──────────────────────────────────────────────────────────────────
KIT = TOOLS / "plugins" / "haipipe-toolkit"
SKILL = KIT / "skills" / "1_base" / "project" / "haipipe-delivery"


def where_defined(rel, names):
    """['name  (line N)' ...]: each function looked up in its file."""
    src = (KIT / rel).read_text(encoding="utf-8").splitlines() if (KIT / rel).is_file() else []
    out = []
    for nm in names:
        k = next((i + 1 for i, ln in enumerate(src) if re.match(rf"\s*def {nm}\b", ln)), None)
        out.append(f"{nm}  (line {k})" if k else f"? {nm}: not found in {rel}")
    return out


def tools_nodes():
    ver = re.search(r'(?m)^\s*version:\s*"([^"]+)"', (SKILL / "SKILL.md").read_text(encoding="utf-8"))
    kids = sorted(p.name + ("/" if p.is_dir() else "") for p in SKILL.iterdir() if not p.name.startswith("."))
    return {"In Tools: Tools/plugins/haipipe-toolkit/": [
        {f"skills/1_base/project/haipipe-delivery/  (version {ver.group(1) if ver else '?'})": kids},
        {"servers/workbench/frame.py": where_defined("servers/workbench/frame.py", [
            "delivery_parts", "_delivery_row", "delivery_by_source", "_delivery_cards"])},
        {"skills/1_base/page/haipipe-draft/src/common.py": where_defined(
            "skills/1_base/page/haipipe-draft/src/common.py",
            ["delivery_owner", "delivery_dir", "delivery_source", "delivery_relative"])},
        ]}


# ── ① Background ─────────────────────────────────────────────────────────────────────────────────
BACKGROUND = [
    {"What this topic is about": [
        "Delivery: what a Block hands over (a paper PDF, a Word file, a deck, an email draft)",
        "seen from both sides: its workbench (the Delivery view) and its skill (/haipipe-delivery)",
        "JL 261012: \"add the UI for the expected UI and card UI for showing the results of the delivery\""]},
    {"Delivery, in one minute": [
        "Jobs and Tasks make outputs; only the Block keeps them, in its one delivery/",
        "each subfolder leads back to the Job or Task folder that made it: the path is the link",
        "a Report stays with each level (s09-D02); what is handed over lives once, at the Block (s09-D05)",
        "a send (something that went out) is one row of delivery/delivery.md"]},
    {"Words it uses": [
        "Block: one question or one paper; Job: one slot of work in it; Task: one step of a Job",
        "delivery/: the Block's one folder of built files, under their source address",
        "result: a file a reader opens (PDF, Word, deck, web page, sheet, image); its twins are one result",
        "card: one result on screen, with the result itself inside",
        "send: one row of delivery.md (date, for, from, status); only a person writes sent",
        "source row: Block · each Job and Task part, on the Delivery screen",
        "theme: the kind of Block (work, cowork, paper, insight, design, discovery, labeling)"]},
    {"Where it sits": [
        "the top row of the workbench: Studio | Block · Job · Task | Delivery (s03-D04)",
        "twin of s02-studio-workbench-skill; neighbours s04 Related, s05 Report, s06 Run",
        "code: servers/workbench/frame.py, one look for every theme",
        "feeds the reports q07_workbench_mapping and q08_workbench_base"]},
    {"How to read this drawing": [
        "① this frame, the words",
        "② the Tree: today's five screens, every delivery/, the rules, the proposals, In Tools",
        "③ the screen: the expected Delivery (s03-D07) and one result card close up (s03-D08)",
        "red ? leaves are open questions; green ✎ leaves are changes"]},
]


# ── ② the Tree ───────────────────────────────────────────────────────────────────────────────────
def screen_node(frame, space, where, rel, what):
    root = TOOLS if where == "tools" else space
    folder = root / rel
    sc = read_screen(frame, root, folder)
    block = frame.chain(folder, root).get("Block", folder)
    kinds = {}
    for it in sc["items"]:
        kinds[it[0]] = kinds.get(it[0], 0) + 1
    tables = [it for it in sc["items"] if it[0] == "table"]
    kids = [f"{sc['theme']} theme: {shape(sc)}; {len(tables)} tables, {kinds.get('card', 0)} cards"]
    kids += [("✓ " if ok else "? ") + words for ok, words in checks(sc, block)]
    return {f"{what}: {folder.name}": kids}


def disk_nodes(frame, space):
    tops = [(TOOLS, TOOLS / "blueprints")]
    if space:
        tops += [(space, d) for d in sorted(space.glob("examples-*")) if d.is_dir() and "archive" not in d.name]
    rows, kids, old_total, nores = delivery_blocks(tops), [], 0, 0
    for root, block, old in rows:
        deliv = block / "delivery"
        nfiles = sum(1 for f in deliv.rglob("*") if f.is_file() and not f.name.startswith(".")
                     and "__pycache__" not in f.parts)
        md = deliv / "delivery.md"
        sends = send_rows(md) if md.is_file() else None
        sc = read_screen(frame, root, block)
        nres = len(results(deliv))
        nores += nres == 0
        old_total += old
        sent = "no delivery.md" if sends is None else (f"{sum(r['status'] == 'sent' for r in sends)} sent, "
                                                       f"{sum(r['status'] == 'draft' for r in sends)} draft")
        rel = block.relative_to(root).as_posix().replace("examples-", "ex-")
        kids.append(f"{rel.rsplit('/', 1)[-1]} · {sc['theme']} · {nres} results · {sent}"
                    + (f" · {old} old below" if old else ""))
    return {f"Every delivery/ on disk: {len(rows)} Blocks, read on each build": kids + [
        f"{nores} of {len(rows)} hold no result a reader can open yet",
        f"? {old_total} old delivery/ folders sit below a Block, against s03-D01: move them in, paper by paper?"]}


def tree_nodes(frame, space):
    shots = [screen_node(frame, space, w, r, wh) for w, r, wh in SCREENS]
    return [
        {"Today: five screens, five shapes": ["each read live through frame.render on this build; "
                                              "✓ is what it gets right, ? what is missing"]},
    ] + shots[:3] + [shots[3], shots[4]] + [
        disk_nodes(frame, space),
        {"The rules (Decided)": [short(decision(n), 120) for n in range(1, 7)]},
        {"Proposed: one Delivery for every Block (s03-D07)": [
            short(decision(7), 120),
            "top row, source row, Sends, Results as cards, small parts one row each, checks below (frame ③)",
            open_item(3), open_item(5), open_item(9)]},
        {"Proposed: one card per result (s03-D08)": [
            short(decision(8), 120),
            "a card holds six parts: kind, state, size and source, sends, the result inside, files (frame ③)",
            {"preview, by kind": [f"{k}: {v}" for k, v in PREVIEW_BY_KIND[:4] + PREVIEW_BY_KIND[5:6]]},
            {"state, in four words": [f"{k}: {v}" for k, v in STATES]},
            open_item(6)]},
        {"Open, kept in place": [open_item(2), open_item(8),
                                 "✎ 261012 Open 1 and 4 are settled or built (s03-D05; the b16 session)"]},
        tools_nodes(),
    ]


def tree_frame(name, title, lines, nodes, width, cols):
    """One frame: a title, a few lines under it, then the folder tree (canvas.tree)."""
    fr = L.open_frame(name)
    text(0, 0, title, 34)
    y = 56
    for ln in lines:
        text(0, y, ln, 22)
        y += 32
    els, _ = canvas.tree(0, y + 8, nodes, width, fr["id"], size=20, head=24, cols=cols)
    L.els.extend(els)
    L.close_frame(fr)
    return fr


# ── ③ the screen: expected Delivery, with one card close up ──────────────────────────────────────
def example_parts(frame, space):
    """The example Block's parts, by source: [(label, folder, {result: files})], the Block's own first."""
    block = space / EXAMPLE[1]
    parts = frame.delivery_parts(block)
    dirs = [frame.delivery_dir(f) for f, _ in parts]
    out = [("Block", block, results(block / "delivery", skip=dirs))] if results(block / "delivery", skip=dirs) else []
    for f, d in parts:
        own = [x for x in dirs if x != frame.delivery_dir(f) and frame.delivery_dir(f) in x.parents]
        out.append(((f.parent.name.split("_", 1)[0] + " › " if d == 2 else "") + f.name, f,
                    results(frame.delivery_dir(f), skip=own)))
    return block, out


def stamp(f: Path):
    size = f.stat().st_size
    words = f"{size / 1024:.1f} KB" if size < 1024 * 1024 else f"{size / 1024 / 1024:.1f} MB"
    return words + " · built " + datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")


def result_card(x, y, w, files, source, h=330):
    f = main_file(files)
    rect(x, y, w, h)
    kind = OPENS[f.suffix.lower()]
    say(x + 18, y + 14, kind, HEAD)
    say(x + 18, y + 48, wrap(f.name, int(w / 12.5)), CODE, font=MONO)
    sy = y + 48 + 26 * len(wrap(f.name, int(w / 12.5)).split("\n")) + 6
    say(x + 18, sy, stamp(f).split(" · built")[0] + " · built " + stamp(f).split("built ")[1][5:], 20)
    say(x + 18, sy + 26, "from " + source + " ↗", 20)
    py = y + 175
    rect(x + 18, py, w - 36, h - 175 - 56, dashed=True)
    say(x + 34, py + 14, f"the {kind} itself, embedded", 20)
    say(x + 18, y + h - 42, "files: " + " · ".join(g.suffix.lstrip(".") for g in files) + " ↗   Rebuild ⧉", 20)


def draw_expected(frame, space, block, parts, W):
    """The expected Delivery screen at the frame's top left; returns its bottom y."""
    sc = read_screen(frame, space, block)
    y0 = 90
    say(0, y0 - 2, f"② Expected, drawn with {block.name}'s own delivery/ (s03-D07)", HEAD)
    y = y0 + 40
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
    say(16, y, "Sends · delivery/delivery.md", HEAD)
    y += 40
    md = block / "delivery" / "delivery.md"
    rows = send_rows(md) if md.is_file() else []
    cw = (W - 32) // 4
    for k, c in enumerate(("date", "for", "from", "status")):
        say(16 + k * cw, y, c, 20)
    y += 30
    path([(16, y), (W - 16, y)], arrow=False)
    y += 8
    if rows:
        for r in rows[:3]:
            for k, c in enumerate(("date", "for", "from", "status")):
                say(16 + k * cw, y, wrap(r.get(c, ""), 28).split("\n")[0], 20)
            y += 30
    else:
        say(16, y, "? no delivery.md yet: a row is added when something goes out; only a person writes sent", 20, RED)
        y += 34
    y += 24
    say(16, y, "Results · by source", HEAD)
    y += 44
    big = [(lb, f, r) for lb, f, r in parts if r and " › " not in lb]
    small = [(lb, f, r) for lb, f, r in parts if r and " › " in lb]
    cardw = (W - 32 - 40) // 3
    for label, f, res in big:
        say(16, y, f"{label} · {len(res)} result{'s' * (len(res) != 1)}", 21)
        y += 36
        cx = 16
        for files in list(res.values())[:3]:
            result_card(cx, y, cardw, files, f.name)
            cx += cardw + 20
        if len(res) > 3:
            say(16, y + 340, f"+ {len(res) - 3} more", 21)
            y += 30
        y += 350
    if small:
        say(16, y, f"{len(small)} smaller parts, one row each; pick one in the source row to see its cards", 21)
        y += 36
        for label, f, res in small:
            kinds = sorted({OPENS[main_file(v).suffix.lower()] for v in res.values()}, key=KIND_ORDER.index)
            newest = max((g for v in res.values() for g in v), key=lambda g: g.stat().st_mtime)
            say(16, y, label, 20, font=MONO)
            say(W * 0.38, y, f"{len(res)} results · " + " · ".join(kinds), 20)
            say(W * 0.78, y, "built " + datetime.fromtimestamp(newest.stat().st_mtime).strftime("%m-%d %H:%M"), 20)
            y += 30
    y += 16
    say(16, y, "▸ Checks · the theme's own (a paper: G4 and its word limit), folded under the results", 21)
    y += 40
    rect(0, y0 + 30, W, y - y0 - 20)
    return y


def draw_card(frame, parts, ox, w):
    """One result close up, six parts (s03-D08), left edge at ox."""
    src, res = next(((f, r) for lb, f, r in parts if r), (None, {}))
    say(ox, 88, "③ One card, one result (s03-D08)", HEAD)
    if not res:
        say(ox, 140, "? the example Block has no results to draw", BODY, RED)
        return
    files = sorted(res.values(), key=lambda v: KIND_ORDER.index(OPENS[main_file(v).suffix.lower()]))[0]
    f = main_file(files)
    x, y, h = ox, 140, 900
    rect(x, y, w, h, bold=True)
    kind = OPENS[f.suffix.lower()]
    say(x + 28, y + 24, "1  " + kind, 28)
    say(x + 28, y + 70, wrap(f.name, int(w / 12)), CODE, font=MONO)
    rect(x + w - 240, y + 22, 200, 46)
    say(x + w - 222, y + 32, "2  current", 22)
    say(x + 28, y + 116, wrap("3  " + stamp(f) + f" · from {src.name} ↗", int(w / 10.5)), 20)
    say(x + 28, y + 190, "4  sent: none yet · read from delivery.md", 20)
    rect(x + 28, y + 236, w - 56, 520, dashed=True)
    say(x + 60, y + 262, f"5  the {kind} itself, embedded: page 1, scroll", 21)
    for k in range(7):
        path([(x + 60, y + 330 + k * 50), (x + w - 100 - (k % 3) * 120, y + 330 + k * 50)], arrow=False)
    say(x + 28, y + 780, wrap("6  " + " · ".join(g.relative_to(frame.delivery_dir(src)).as_posix() + " ↗"
                              for g in files), int(w / 11)), 20, font=MONO)
    say(x + 28, y + 850, "Rebuild ⧉ (copies a prompt; starts nothing)", 20)


def screen_frame(frame, space):
    fr = L.open_frame("The screen: expected Delivery and one card")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    say(0, 0, "The expected Delivery, and one result card close up", T)
    block, parts = example_parts(frame, space)
    W, CW = 1500, 900
    bottom = draw_expected(frame, space, block, parts, W)
    draw_card(frame, parts, W + 60, CW)
    note(W + 60, 1070, "proposed: one Delivery shape, one card per result (s03-D07, D08; JL)", TODAY)
    L.close_frame(fr, pad=60)
    return fr


# ── the three frames ─────────────────────────────────────────────────────────────────────────────
def main():
    out = HERE / "s03-delivery-workbench-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    frame = frame_module()
    space = space_root()
    if space is None:
        raise SystemExit("no SPACE beside Tools/ holds the example folders; the tree needs one")
    ui = screen_frame(frame, space)
    bg = tree_frame("Background: what Delivery is", "Background: Delivery, for a newcomer",
                    ["The words this topic uses, and where it sits. The topic itself is the Tree; the screen "
                     "is the third frame."], BACKGROUND, 1500, 1)
    tree = tree_frame("The Tree: Delivery, its workbench and its skill", "Delivery: its workbench and its skill",
                      ["Today's five screens (read live), every delivery/ on disk, the rules, the proposals and "
                       "In Tools; red ? leaves are still open."], tree_nodes(frame, space), 2600, 3)
    canvas.grid(L.els, [[bg["id"], tree["id"]], [ui["id"]]])
    for e in canvas.off_palette(L.els):                  # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, list(L.els), "build_s03_delivery_workbench_skill.py")


if __name__ == "__main__":
    main()
