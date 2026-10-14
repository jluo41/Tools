"""s03 · Delivery: its workbench and its skill: s03-delivery-workbench-skill.excalidraw (haipipe-studio).

Three frames (haipipe-studio 0.13.0; JL 261012: "we can have both tree and box, and -->"). ① and ② come from the
face's `frames:` yaml through topic_map.draw_frames; this builder fills the live trees into it:

    ① Background   a newcomer's folder tree: what Delivery is, the words it uses, where it sits
    ② the boxes    parts with a why line and a tree each, joined by named arrows; today's five screens, the
                   delivery/ on disk and the skill's folder are read live; a ❓ leaf is an open point
    ③ the screen   the expected Delivery (s03-D07) with one result card close up (s03-D08), in the workbench's colours

Read on every build: each Delivery screen through servers/workbench/frame.py (frame.render, the Runs panel left
out), every Block's delivery/ off the disk (in Tools/blueprints and in the SPACE beside Tools whose Tools/ link
leads here), the decisions and open items of this topic's face, and the skill's folder and functions. The older
builders (261011, 261012, 261012b) are in history/.

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
import topic_map  # noqa: E402  (frames from the face's yaml)
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
            "delivery_parts", "delivery_by_source", "_delivery_cards"])},
        {"skills/1_base/page/haipipe-draft/src/common.py": where_defined(
            "skills/1_base/page/haipipe-draft/src/common.py",
            ["delivery_owner", "delivery_dir", "delivery_source", "delivery_relative"])},
        ]}


# ── ② the boxes' live trees: facts read off the disk and through frame.py ─────────────────────────
def screens_tree(frame, space):
    """The screens box: one leaf per Delivery screen, with its checks counted, read through frame.render."""
    leaves, missing = [], set()
    for where, rel, what in SCREENS:
        root = TOOLS if where == "tools" else space
        folder = root / rel
        sc = read_screen(frame, root, folder)
        block = frame.chain(folder, root).get("Block", folder)
        chk = checks(sc, block)
        good = sum(1 for ok, _ in chk if ok)
        missing |= {w for ok, w in chk if not ok and w.startswith(("no delivery.md", "no result", "no state"))}
        cards = sum(1 for it in sc["items"] if it[0] == "card")
        mark = "✅" if good == len(chk) else ("🔶" if good else "⬜")
        leaves.append(f"{mark} {what}: {shape(sc)}; {good} of {len(chk)} checks")
    return leaves


def disk_tree(frame, space):
    """The delivery/ box's live branch: how many Blocks keep a delivery/, read on each build."""
    tops = [(TOOLS, TOOLS / "blueprints")]
    if space:
        tops += [(space, d) for d in sorted(space.glob("examples-*")) if d.is_dir() and "archive" not in d.name]
    rows, themes, nores, nomd, old_total = delivery_blocks(tops), {}, 0, 0, 0
    for root, block, old in rows:
        theme = read_screen(frame, root, block)["theme"]
        themes[theme] = themes.get(theme, 0) + 1
        nores += len(results(block / "delivery")) == 0
        nomd += not (block / "delivery" / "delivery.md").is_file()
        old_total += old
    return {f"📂 on disk now: {len(rows)} Blocks keep a delivery/": [
        " · ".join(f"{n} {t}" for t, n in sorted(themes.items(), key=lambda kv: -kv[1])),
        f"🔶 {nores} of {len(rows)} hold no result a reader can open yet",
        f"⬜ {nomd} of {len(rows)} have no delivery.md",
        f"❓ {old_total} old delivery/ folders sit below a Block: move them in?"]}


def tools_tree():
    """The skill box: the skill's folder, its version and each function looked up in its file."""
    ver = re.search(r'(?m)^\s*version:\s*"([^"]+)"', (SKILL / "SKILL.md").read_text(encoding="utf-8"))
    kids = sorted(p.name + ("/" if p.is_dir() else "") for p in SKILL.iterdir() if not p.name.startswith("."))
    return [
        f"🧰 haipipe-delivery/ v{ver.group(1) if ver else '?'}: " + " · ".join(kids),
        {"🖥️ servers/workbench/frame.py": where_defined("servers/workbench/frame.py", [
            "delivery_parts", "delivery_by_source", "_delivery_cards"])},
        {"🧱 haipipe-draft/src/common.py": where_defined(
            "skills/1_base/page/haipipe-draft/src/common.py", ["delivery_owner", "delivery_dir", "delivery_source"])},
    ]


def live_frames(frame, space):
    """The face's frames: structure from its yaml, the live trees filled in by box id."""
    frames = topic_map.frames_of(FACE)
    for fr in frames:
        for b in fr.get("boxes") or []:
            if b["id"] == "screens":
                b["tree"] = screens_tree(frame, space) + (b.get("tree") or [])
            elif b["id"] == "delivery":
                b["tree"] = (b.get("tree") or []) + [disk_tree(frame, space)]
            elif b["id"] == "skill":
                b["tree"] = tools_tree()
    return frames


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
    frame = frame_module()
    space = space_root()
    if space is None:
        raise SystemExit("no SPACE beside Tools/ holds the example folders; the tree needs one")
    els = []
    topic_map.draw_frames(els, live_frames(frame, space), "s03")      # ① and ② from the face's yaml
    L.els.clear()
    L.FRAME[0] = None
    ui = screen_frame(frame, space)                                    # ③ the screen, drawn here
    els += L.els
    canvas.grid(els, [[e["id"] for e in els if e["type"] == "frame"]])
    for e in canvas.off_palette(els):                                  # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, els, "build_s03_delivery_workbench_skill.py")
    from render_png import render
    render(out, out.with_suffix(".png"))


if __name__ == "__main__":
    main()
