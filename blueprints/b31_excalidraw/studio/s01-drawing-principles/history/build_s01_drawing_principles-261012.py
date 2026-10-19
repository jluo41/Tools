"""s01 · Drawing principles: s01-drawing-principles.excalidraw (excalidraw-studio's own topic).

Five frames in two acts, each frame as large as one screen, joined by named arrows; the drawing follows the
principles it states and is drawn with excalidraw-studio's helpers (scripts/draw.py):
  Act 1 · What a drawing must do, and where that lives:
    ① the principles, one mind map: the centre, the six asked for, the standing rules, each with its summary;
    ④ the skill folders: excalidraw-studio, haipipe-studio and the four excalidraw skills, read from disk;
    ⑤ s00, a Block's index: what block_index.py reads and draws, and what it proposes (sNN, jNN), b31's own live;
  Act 2 · How a drawing is checked, and four that were:
    ② the checks in seven stages, read live from canvas.py, the loop back, each drawing's density;
    ③ four drawings from 261012, checked: b10 s05's tree pass and s05 restored (both drawn as s07), s52 (the one to copy), s51 before/after.
Every word is a yaml block of the face; facts it can read are read on every build; a person's marks are kept.

    python build_s01_drawing_principles.py
"""
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLKIT = (HERE / "../../../../plugins/haipipe-toolkit").resolve()
sys.path.insert(0, str(TOOLKIT / "skills/1_base/excalidraw/excalidraw-studio/scripts"))
from draw import FLOOR, H, INK, KEY, MAP_FLOOR, RED, T_KEY, T_NODE, T_SMALL, T_TEXT, W, Drawing, canvas  # noqa: E402
from check import check as check_drawing  # noqa: E402

FACE = HERE / f"{HERE.name}.md"
BLOCK = HERE.parents[1]
d = Drawing()


def data():
    """Every yaml block of the face, merged."""
    out = {}
    for block in re.findall(r"```yaml\n(.*?)\n```", FACE.read_text(encoding="utf-8"), re.S):
        out.update(yaml.safe_load(block))
    return out


# ── ① the Excalidraw principles: the first frame, read zoomed out ──────────────────────────────────────────
PW, PT, PS, PL = 1000, 46, 32, 22                     # a principle's box; its title, summary and detail sizes


def principle_lines(b):
    """What a principle's box shows: its title and summary large, at most two details small, its open point red."""
    leaves = [str(x) for x in b.get("leaves", [])]
    opens = [x for x in leaves if x.startswith("❓")]
    return [x for x in leaves if not x.startswith("❓")][:2] + opens[:1]


def principle_height(b):
    return 18 + d.height(b["title"], PW - 48, PT) + 8 + d.height(b.get("summary", ""), PW - 48, PS) + 10 + \
        sum(d.height("· " + x, PW - 48, PL) + 4 for x in principle_lines(b)) + 16


def principle_box(b, x, y, h):
    asked = str(b.get("by", "")).startswith("asked")
    d.box(x, y, PW, h, INK, 3.5 if asked else 1.5)
    yy = d.para(x + 24, y + 16, b["title"], PW - 48, PT) + 8
    if b.get("summary"):
        yy = d.para(x + 24, yy, b["summary"], PW - 48, PS) + 10
    for ln in principle_lines(b):
        yy = d.para(x + 24, yy, ln if ln.startswith("❓") else "· " + ln, PW - 48, PL) + 4


def principles(data_):
    """The Excalidraw principles as one mind map: the centre, the six asked for and the two standing rules around it,
    each its title and its one-line summary in big words, so they read with the whole drawing zoomed out."""
    m = data_["mindmap"]
    f = d.frame("① The Excalidraw principles")
    d.heading("📐 The Excalidraw principles",
              "How every Studio topic's drawing reads, held by the skill excalidraw-studio. Bold: the six asked for "
              "(261012). Thin: rules that stand. Red: still open. Yellow, the key point: the centre.")
    asked = [b for b in m["branches"] if str(b.get("by", "")).startswith("asked")]
    rest = [b for b in m["branches"] if b not in asked]
    left, right = asked[:3] + rest[:1], asked[3:6] + rest[1:2]
    top, gap = 200, 26
    hs = {id(b): principle_height(b) for b in left + right}
    col_h = max(sum(hs[id(b)] for b in col) + gap * (len(col) - 1) for col in (left, right))
    f["height"] = max(H, top + col_h + 40)
    lx, rx = 40, W - 40 - PW
    cx, cw = lx + PW + 60, rx - 60 - (lx + PW + 60)
    ch = 300
    cy = top + col_h / 2 - ch / 2
    d.key(cx, cy, cw, ch, 5)                                          # the key point: the centre
    yy = d.para(cx + 28, cy + 30, "📐 The Excalidraw principles", cw - 56, 44) + 14
    d.para(cx + 28, yy, m["centre"], cw - 56, 30)
    for col, x, side in ((left, lx, "l"), (right, rx, "r")):
        y = top
        for b in col:
            h = hs[id(b)]
            principle_box(b, x, y, h)
            sx = cx - 4 if side == "l" else cx + cw + 4                # from the centre to each principle
            ex = x + PW + 6 if side == "l" else x - 6
            d.line([(sx, cy + ch / 2), (ex, y + min(46, h / 2))], sw=3)
            y += h + gap
    return f


# ── ② the checks, one workflow map of stages ───────────────────────────────────────────────────────────────
STAGES = {"build": "⚙️ Build", "size": "🖼️ Size and density", "inside": "🗺️ Inside a frame", "story": "📖 The story",
          "look": "🔍 The look, zoomed out", "write": "💾 Write", "agree": "👤 A person agrees"}


def check_by(by):
    """Who checks it, read live: a canvas.py function that exists, a person, or nobody yet."""
    if by.startswith("canvas."):
        return (f"✅ {by}", INK) if hasattr(canvas, by.split(".", 1)[1]) else (f"❓ {by} is gone", RED)
    return {"person": ("👤 a person", INK), "none": ("❓ no check yet", RED)}.get(by, (f"⚙️ {by}", INK))


def limits():
    out = [f"a frame at most {canvas.FRAME_MAX[0]} x {canvas.FRAME_MAX[1]} px (FRAME_MAX)",
           f"words {canvas.TEXT_MIN} px or more (TEXT_MIN)",
           f"a text frame {FLOOR} words or more per million px (SPARSE_MIN); a map frame {MAP_FLOOR} (draw.py)"]
    if hasattr(canvas, "frame_limit"):
        topic = canvas.frame_limit(Path("studio/s07-x/s07-x.excalidraw"))
        index = canvas.frame_limit(Path("studio/s00-background-and-index/s00-background-and-index.excalidraw"))
        out.append(f"frame count: {index or 'no limit'} for s00, {topic or 'no limit'} for a topic (frame_limit)")
    return out


def stage_height(title, rows, w):
    hh = 16 + d.height(title, w - 32, T_NODE if len(title) < 14 else 30) + 12
    for c, who, _ in rows:
        hh += d.height(c["step"], w - 32, 24) + 4 + (d.height(f"guards {c['guards']}", w - 32, 20) + 4
                                                      if c.get("guards") else 0) \
            + (d.height("caught today: " + str(c.get("caught", "")), w - 32, 20) if c.get("caught") else 0) \
            + d.height(who, w - 32, 20) + 20
    return hh + 10


def checks(data_):
    f = d.frame("② Checking a drawing: one workflow map")
    d.heading("🔁 Checking a drawing against them, stage by stage",
              "A builder draws from disk; then each stage of checks in order. Each check names the principle it guards "
              "and who checks it: a canvas.py function (read live: it exists or not), a person, or nobody yet, in red. "
              "Yellow, the key point: a failed check goes back to the builder, never to the drawing by hand.")
    groups = {}
    for c in data_["checks"]:
        groups.setdefault(c["stage"], []).append(c)
    names = list(groups)
    gap, top = 34, 200
    bw = (W - 80 - gap * (len(names) - 1)) / len(names)
    rows_of = {n: [(c, *check_by(str(c["by"]))) for c in groups[n]] for n in names}
    bh = max(stage_height(STAGES.get(n, n), rows_of[n], bw) for n in names)
    xs = [40 + i * (bw + gap) for i in range(len(names))]
    for n, x in zip(names, xs):
        red = any(color == RED for _, _, color in rows_of[n])
        d.box(x, top, bw, bh, RED if red else INK, 3 if red else 2)
        title = STAGES.get(n, n)
        y = d.para(x + 16, top + 16, title, bw - 32, T_NODE if len(title) < 14 else 30) + 12
        for c, who, color in rows_of[n]:
            y = d.para(x + 16, y, c["step"], bw - 32, 24) + 4
            if c.get("guards"):
                y = d.para(x + 16, y, f"guards {c['guards']}", bw - 32, 20) + 4
            if c.get("caught"):
                y = d.para(x + 16, y, "caught today: " + str(c["caught"]), bw - 32, 20, INK)
            y = d.para(x + 16, y + 2, who, bw - 32, 20, color) + 20
    for a, b in zip(xs, xs[1:]):
        d.line([(a + bw + 3, top + 70), (b - 3, top + 70)], sw=3)
    bus = top + bh + 50
    d.line([(xs[1] + bw / 2, bus), (xs[-2] + bw / 2, bus)], arrow=False, dashed=True, color=RED, sw=2)
    for x in xs[1:-1]:
        d.line([(x + bw / 2, top + bh + 4), (x + bw / 2, bus)], arrow=False, dashed=True, color=RED, sw=2)
    fix_w, fix_y = 560, bus + 56
    d.key(xs[0], fix_y, fix_w, 150)                                     # the key point
    d.para(xs[0] + 18, fix_y + 14, "🔧 fix the builder, rebuild", fix_w - 36, T_KEY)
    d.para(xs[0] + 18, fix_y + 62, data_["loop"], fix_w - 36, T_SMALL)
    d.line([(xs[1] + bw / 2, bus), (xs[1] + bw / 2, fix_y - 6)], sw=3, color=RED)
    d.line([(xs[0] + 40, fix_y - 6), (xs[0] + 40, top + bh + 6)], sw=3)
    d.text(xs[1] + bw / 2 + 14, bus - 36, "a check fails", 24, RED)
    mx, mw = xs[0] + fix_w + 60, 620
    y = d.para(mx, fix_y - 10, "📏 Limits in canvas.py and draw.py today, read live", mw, 26) + 8
    for r in limits():
        y = d.para(mx + 10, y, "· " + r, mw - 10, 20) + 3
    y = d.para(mx, y + 12, "❓ Checked by no code", mw, 26, RED) + 8
    for c in data_["checks"]:
        if str(c["by"]) in ("person", "none") and c.get("guards") not in ("all", ""):
            y = d.para(mx + 10, y, f"· {c['guards']}: {c['step']}", mw - 10, 20) + 3
    cx0 = mx + mw + 60
    density_chart(cx0, fix_y - 10, W - 40 - cx0, H - 30 - (fix_y - 10), data_)
    return f


def density_chart(x, y, w, h, data_):
    """Principle 6, measured: each drawing's frames, words per million px, against the floor of its kind."""
    d.para(x, y, f"📊 Density per frame, words per million px (text {FLOOR}, map {MAP_FLOOR})", w, 26)
    sources = [("s01", HERE / f"{HERE.name}.excalidraw"),
               ("s51", (HERE / data_["before_after"]["after"]).resolve())]
    sources += [("s" + re.search(r"/s(\d\d)-", e["drawing"]).group(1), (HERE / e["drawing"]).resolve())
                for e in data_["examples"] if e.get("drawing")]
    rows = []
    for tag, path in sources:
        dens = Drawing.density_of(path)
        if len(dens) <= 5:
            rows += [(f"{tag} · {n}", v, k) for n, v, k in dens]
        else:                                            # many frames: one row, lowest to highest
            vs = [v for _, v, k in dens if k != "picture"] or [v for _, v, _ in dens]
            rows.append((f"{tag} · {len(dens)} frames, {min(vs)} to {max(vs)}; median", sorted(vs)[len(vs) // 2],
                         "map" if sum(k == "map" for *_, k in dens) * 2 >= len(dens) else "text"))
    if not rows:
        return
    label_w, top = 520, y + 56
    scale_max = max(max(v for _, v, _ in rows), FLOOR * 2)
    bar_w = w - label_w - 80
    rh = max(30, min(44, (h - 110) / len(rows)))
    for i, (name, v, k) in enumerate(rows):
        yy = top + i * rh
        floor = MAP_FLOOR if k == "map" else FLOOR
        ok = k == "picture" or v >= floor
        d.text(x, yy + 2, ("🖼️ " if k == "picture" else "🗺️ " if k == "map" else "") +
               ((name[:36] + "…") if len(name) > 37 else name), 20)
        bw_ = max(4, bar_w * v / scale_max)
        d.el("rectangle", x + label_w, yy + 6, bw_, rh - 12, strokeColor=INK if ok else RED, strokeWidth=1,
             backgroundColor=KEY if ok and k != "picture" else "transparent", fillStyle="solid", roundness=None)
        d.text(x + label_w + bw_ + 10, yy + 2, str(v), T_SMALL, INK if ok else RED)
    for floor, tag in ((FLOOR, "text"), (MAP_FLOOR, "map")):
        fx = x + label_w + bar_w * floor / scale_max
        d.line([(fx, top - 6), (fx, top + len(rows) * rh)], arrow=False, dashed=True, color=RED, sw=2)
        d.text(fx + 6, top - 32, f"{tag} {floor}", T_SMALL, RED)
    d.text(x, top + len(rows) * rh + 8, "🗺️ a map frame · 🖼️ a picture or screen, not measured · s01: its last build",
           T_SMALL)


# ── ③ four drawings from 261012, checked ────────────────────────────────────────────────────────────────────
def examples(data_):
    f = d.frame("③ Four drawings from 261012, checked")
    d.heading("🧪 Four drawings from 261012, checked against the principles",
              "Their previews as they were that day (kept in examples/), one verdict per principle; red breaks one; the ⑥ "
              "line measured from the drawing. Yellow, the key point: b10 s52, the one to copy. Below, b10 s51 before and "
              "after.")
    ex = data_["examples"]
    gap = 60
    pw = (W - 80 - gap * (len(ex) - 1)) / len(ex)
    top, pic_h = 196, 330
    bottom = 0
    for i, e in enumerate(ex):
        x = 40 + i * (pw + gap)
        if e.get("key"):
            d.key(x - 14, top - 10, pw + 28, 56, 1)
        y = d.para(x, top, e["name"], pw, 30)
        y = d.para(x, y + 2, e["when"], pw, T_SMALL) + 10
        y += d.picture(HERE / e["image"], x, y, pw, pic_h) + 14
        for v in e["verdict"]:
            y = d.para(x, y, v, pw, 23) + 6
        six, now = today((HERE / e["drawing"]).resolve()) if e.get("drawing") else (None, None)
        if six:
            y = d.para(x, y, six, pw, 23) + 6
        if now and e.get("since"):                         # what changed since that day, in green, read live
            y = d.para(x, y + 4, f"{e['since']} · {now}", pw, 23, canvas.GREEN) + 6
        bottom = max(bottom, y)
    ba = data_["before_after"]
    six, now = today((HERE / ba["after"]).resolve())
    y = d.para(40, bottom + 30, "✏️ " + ba["name"] + ": nine small frames, redrawn as four in one story" +
               ("" if six and six.startswith("✅") else "; each is too thin"), W - 80, 30) + 20
    hb = H - 40 - y
    rows = -(-len(ba["before"]) // 2)
    sw_, sh_ = 240, (hb - 76 - (rows - 1) * 8) / rows
    for i, name in enumerate(ba["before"]):
        r, c = i % rows, i // rows
        x, yy = 40 + c * (sw_ + 12), y + r * (sh_ + 8)
        d.box(x, yy, sw_, sh_, INK, 1)
        d.para(x + 10, yy + 4, name, sw_ - 20, T_SMALL)
    d.para(40, y + hb - 64, ba["before_note"], 2 * sw_ + 12, T_SMALL, RED)
    ax = 40 + 2 * sw_ + 12 + 180
    d.line([(40 + 2 * sw_ + 12 + 24, y + hb / 2 - 20), (ax - 24, y + hb / 2 - 20)], sw=5)
    d.text(40 + 2 * sw_ + 12 + 30, y + hb / 2 - 66, "redrawn", 28)
    vw2 = 540
    ph = d.picture(HERE / ba["image"], ax, y, W - 40 - ax - vw2 - 30, hb - 110)
    dens = Drawing.density_of((HERE / ba["after"]).resolve())
    ly = d.para(ax, y + ph + 16, ("its frames now: " + " → ".join(n for n, _, _ in dens)) if dens else
                "❓ s51's drawing is not beside this Block: not read", W - 40 - ax - vw2 - 30, T_TEXT)
    d.para(ax, ly + 6, ba["after_note"], W - 40 - ax - vw2 - 30, T_SMALL)
    vy = y
    for v in ba["verdict"]:
        vy = d.para(W - 40 - vw2, vy, v, vw2, 26) + 10
    if six:
        vy = d.para(W - 40 - vw2, vy, six, vw2, 26) + 10
    if now and ba.get("since"):
        d.para(W - 40 - vw2, vy + 4, f"{ba['since']} · {now}", vw2, 26, canvas.GREEN)
    return f


def today(path):
    """What check.py says of a drawing on this build: its ⑥ line against the floor of each frame's kind, and how
    many ❌ it finds in all; (None, None) when the drawing is not beside this Block."""
    if not Path(path).is_file():
        return None, None
    r = check_drawing(path)
    rows = [f for f in r["rows"] if f["kind"] != "picture"]
    if not rows:
        return None, None
    ok = all(f["⑥"].startswith("✅") for f in rows)
    kinds = {f["kind"] for f in rows}
    floor = f"the {kinds.pop()} floor of {rows[0]['floor']}" if len(kinds) == 1 else "the floor of its kind"
    six = f"{'✅' if ok else '❌'} ⑥ {min(f['per'] for f in rows)} to {max(f['per'] for f in rows)} words per million px, " \
          f"{'over' if ok else 'under'} {floor}"
    fails = sum(str(f[p]).startswith("❌") for f in r["rows"] for p in ("①", "②", "④", "⑤", "⑥")) + r["③"].startswith("❌")
    return six, f"check.py today: {fails} ❌ in its {r['frames']} frames" if fails else \
        f"check.py today: all {r['frames']} frames pass"


# ── ④ the skill folders that hold them: real folders, so folder trees ───────────────────────────────────────
NOTES = {"canvas.py": "the writer and its checks", "render_png.py": "the preview", "new_topic.py": "a topic, a session",
         "topic_map.py": "s00's tree and boxes", "block_index.py": "s00, a Block's index", "draw.py": "the helpers"}


def version(folder):
    hit = re.search(r"(?m)^\s*version:\s*\"?([\d.]+)", (folder / "SKILL.md").read_text(encoding="utf-8")) \
        if (folder / "SKILL.md").is_file() else None
    return hit.group(1) if hit else "?"


def sections(folder):
    md = folder / "SKILL.md"
    t = md.read_text(encoding="utf-8") if md.is_file() else ""
    heads = re.findall(r"(?m)^#{2,3}\s+(.+?)\s*$", t) + re.findall(r"(?m)^(\S[^\n]{2,60})\n[-=]{3,}\s*$", t)
    return [re.sub(r"[`*]", "", h_) for h_ in heads if not h_.startswith("#")]


def skill_box(s, x, y, w, h, open_=(), most=8, heads=14, title=34, grow=False):
    """One skill folder in a box; `grow`: the box as tall as its words (the yellow one ran out of its box)."""
    folder = TOOLKIT / "skills" / s["path"]
    if s.get("key"):
        e = d.key(x, y, w, h, 3)                                       # the key point
    else:
        e = d.box(x, y, w, h, INK, 2)
    yy = d.para(x + 22, y + 16, f"🧰 {s['name']} {version(folder)}", w - 44, title)
    yy = d.para(x + 22, yy + 2, s["why"], w - 44, T_SMALL) + 6
    secs = sections(folder) if heads else []
    if secs:
        yy = d.para(x + 22, yy, "SKILL.md: " + " · ".join(secs[:heads]) + (" …" if len(secs) > heads else ""),
                    w - 44, 20) + 10
    t = d.text(x + 22, yy, "\n".join(Drawing.folder_tree(folder, open_, most, NOTES)), 20, INK, code=True)
    yy += t["height"] + 12
    for hold in s.get("holds", []):
        yy = d.para(x + 22, yy, "· " + hold, w - 44, T_SMALL) + 4
    if s.get("since"):                                                 # a green line on what changed
        yy = d.para(x + 22, yy + 4, s["since"], w - 44, T_SMALL, canvas.GREEN) + 4
    if grow:
        e["height"] = max(h, yy - y + 16)
    return (x, y, w, e["height"])


def skills(data_):
    f = d.frame("④ The skill folders that hold them")
    d.heading("🧰 Where the principles live: the skill folders",
              "Real folders, so drawn as folder trees (principle ④), each read from disk with its version. Yellow, the "
              "key point: excalidraw-studio, the skill that holds how a Studio drawing reads.")
    ss = data_["skills"]
    new = next(s for s in ss if s.get("key"))
    studio = next(s for s in ss if s["name"] == "haipipe-studio")
    others = [s for s in ss if s is not new and s is not studio]
    hh = f["height"] = 1600                                            # FRAME_MAX: five kinds since b31 s06
    cx, cw = 920, W - 40 - 920
    nh = skill_box(new, cx, 196, cw, 420, open_=("scripts",), most=4, heads=7, grow=True)[3]
    st = skill_box(studio, 40, 196, 760, hh - 30 - 196, open_=("scripts", "ref"), most=7)
    d.line([(cx - 6, 196 + 210), (st[0] + st[2] + 6, 196 + 210)], sw=3)
    d.text(st[0] + st[2] + 12, 196 + 220, "keeps\nthe topic", T_SMALL + 3)
    gy = 196 + nh + 80
    per = 3                                                            # five kinds since excalidraw-job (b31 s06)
    rows = -(-len(others) // per)
    gw = (cw - 40 * (per - 1)) / per
    gh = (hh - 30 - gy - 40 * (rows - 1)) / rows
    d.text(cx + 8, gy - 74, "beside it, the other drawing kinds (b31 s02 to s06)", T_SMALL)
    for i, s in enumerate(others):
        x = cx + (i % per) * (gw + 40)
        y = gy + (i // per) * (gh + 40)
        skill_box(s, x, y, gw, gh, open_=(), most=0, heads=0, title=30)
        d.text(x + gw - 10 - len(s.get("link", "")) * T_SMALL * 0.55, y - 30, s.get("link", ""), T_SMALL)   # above its box
    return f


# ── ⑤ s00, a Block's index, and what it proposes ────────────────────────────────────────────────────────────
def s00_face(block):
    md = block / "studio/s00-background-and-index/s00-background-and-index.md"
    t = md.read_text(encoding="utf-8") if md.is_file() else ""

    def get(key):
        m = re.search(rf"```yaml\n({key}:.*?)\n```", t, re.S)
        return (yaml.safe_load(m.group(1)) or {}).get(key) if m else None
    return get("studio_proposals") or [], get("job_proposals") or []


def s00(data_):
    f = d.frame("⑤ s00, a Block's index, and what it proposes")
    s = data_["s00"]
    d.heading("🗂️ s00, a Block's index: what it shows, and what it proposes",
              "The one drawing with its own shape. haipipe-studio's block_index.py reads the Block on disk and its s00 "
              "face, then draws the plan, the background and the index; proposed topics (sNN) and Jobs (jNN) stay red "
              "and dashed until a person ticks them. Yellow, the key point: nothing proposed is made before it is ticked.")
    boxes = d.flow(s["steps"], 40, 196, W - 80, gap=70, title=28, leaf=20, labels=s.get("labels", []))
    x0, y0, w0, h0 = boxes[-1]
    x1 = boxes[0][0]
    by = y0 + h0 + 50                                                  # the loop: the next build shows it made
    d.line([(x0 + w0 / 2, y0 + h0 + 4), (x0 + w0 / 2, by), (x1 + 60, by), (x1 + 60, y0 + h0 + 6)], sw=3)
    d.text(x1 + 80, by + 8, "the next build shows it made, in the index", T_SMALL)
    props, jobs = s00_face(BLOCK)                                       # b31's own, read from its s00 face
    made = {p.name[:3] for p in (BLOCK / "studio").iterdir() if p.is_dir() and re.match(r"s\d\d[-_]", p.name)}
    jobs_made = {p.name[:3] for p in BLOCK.iterdir() if p.is_dir() and re.match(r"j\d\d_", p.name)}
    py = by + 100
    half = (W - 80 - 80) / 2

    def proposal(x, y, head, lines, done):
        """One proposal: its line, then what it should give; red and dashed until a person ticks it."""
        y0 = y
        y = d.para(x + 14, y + 6, head, half - 40, 25) + 4
        for ln in ([] if done else lines):
            y = d.para(x + 14, y, ln, half - 40, 21) + 2
        if not done:
            d.box(x, y0, half, y - y0 + 10, RED, 2, dashed=True)
        return y + (18 if not done else 2)

    y = d.para(40, py, f"📋 b31's s00 proposes these topics (sNN): {len(props)} in all, "
                       f"{sum(p['id'] in made for p in props)} made", half, 30) + 16
    for p in props:
        done = p["id"] in made
        y = proposal(40, y, f"{'✅' if done else '⬜'} {p['id']} · {p.get('title', '')}" +
                     ("" if done else f" · {p.get('status', 'proposed')}"),
                     [f"❓ {p.get('question', '')}", "→ " + str(p.get("output", ""))] +
                     ([f"❓ only if {p['condition']}"] if p.get("condition") else []), done)
    jx = 40 + half + 80
    yj = d.para(jx, py, f"🧱 and these Jobs (jNN): {len(jobs)} proposed, {sum(j['id'] in jobs_made for j in jobs)} made",
                half, 30) + 16
    for j in jobs:
        done = j["id"] in jobs_made
        yj = proposal(jx, yj, f"{'✅' if done else '⬜'} {j['id']}_{j.get('slug', '')} · {j.get('title', '')}",
                      ["→ " + str(j.get("finish", "")), "rests on " + ", ".join(j.get("topics") or [])], done)
    bi = TOOLKIT / "skills/1_base/project/haipipe-studio/scripts/block_index.py"   # does s00 draw them? read live
    src = bi.read_text(encoding="utf-8") if bi.is_file() else ""
    yj = d.para(jx, yj + 6, "✅ block_index.py draws them in their own frame, 💡 what we propose next, a red dashed "
                "box each, until made" if "proposals_frame" in src else
                "✅ block_index.py draws proposed topics and Jobs, a red dashed row each, until made"
                if "job_proposals" in src else "❓ block_index.py does not draw proposed Jobs (job_proposals) yet",
                half, 22) + 10
    d.para(40, max(y, yj) + 24, "🗂️ s00's own shape: " + " · ".join(s.get("own_shape", [])), W - 80, 23)
    return f


def main():
    out = HERE / f"{HERE.name}.excalidraw"
    data_ = data()
    fs = {}
    for draw in (principles, checks, examples, skills, s00):
        f = draw(data_)
        d.badge(f)                                       # principle 6: measured once the frame is drawn
        fs[f["name"][0]] = f
    acts = [{"name": a["name"], "frames": [fs[m]["id"] for m in a["frames"]], "arrow": a.get("arrow")}
            for a in data_["acts"]]
    b = data_.get("between") or {}
    d.acts(acts, between=[(fs[b["from"]]["id"], fs[b["to"]]["id"], b["label"])] if b else [])
    d.write(out, "build_s01_drawing_principles.py")


if __name__ == "__main__":
    main()
