"""s01 · Drawing principles: s01-drawing-principles.excalidraw (excalidraw-studio's own topic).

Five frames in two acts, each frame as large as one screen, joined by named arrows; the drawing follows the
principles it states and is drawn with excalidraw-studio's helpers (scripts/draw.py):
  Act 1 · What a drawing must do, and where that lives:
    ① the principles, one mind map: the centre, the seven asked for, the standing rules, each with its summary;
    ④ the skill folders: excalidraw-studio, haipipe-studio and the four excalidraw skills, read from disk;
    ⑤ s00, a Block's index: what block_index.py reads and draws, and what it proposes (sNN, jNN), b31's own live;
  Act 2 · How a drawing is checked, and four that were:
    ② the checks in seven stages, one short line each, who checks it read live, the loop back to the builder;
    ③ four drawings from 261012, checked: b10 s05's tree pass and s05 restored (both drawn as s07), s52 (the one to copy), s51 before/after.
Every word is a yaml block of the face; facts it can read are read on every build; a person's marks are kept.
Few words in each map, none of them small (principle ⑦): the detail stays in the face.

    python build_s01_drawing_principles.py
"""
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLKIT = (HERE / "../../../../plugins/haipipe-toolkit").resolve()
sys.path.insert(0, str(TOOLKIT / "skills/1_base/excalidraw/excalidraw-studio/scripts"))
from draw import H, INK, MAP_WORDS, RED, SMALL, T_SMALL, T_TEXT, W, Drawing, canvas  # noqa: E402
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
PW, PT, PS, PO = 1000, 46, 32, SMALL                  # a principle's box; its title, summary, open point (⑦: none small)


def principle_open(b):
    """The one line under a principle's summary: its open point, red; its other leaves stay in the face (⑦)."""
    return [str(x) for x in b.get("leaves", []) if str(x).startswith("❓")][:1]


def principle_height(b):
    return 18 + d.height(b["title"], PW - 48, PT) + 8 + d.height(b.get("summary", ""), PW - 48, PS) + 10 + \
        sum(d.height(x, PW - 48, PO) + 4 for x in principle_open(b)) + 16


def principle_box(b, x, y, h):
    asked = str(b.get("by", "")).startswith("asked")
    d.box(x, y, PW, h, INK, 3.5 if asked else 1.5)
    yy = d.para(x + 24, y + 16, b["title"], PW - 48, PT) + 8
    if b.get("summary"):
        yy = d.para(x + 24, yy, b["summary"], PW - 48, PS) + 10
    for ln in principle_open(b):
        yy = d.para(x + 24, yy, ln, PW - 48, PO) + 4


def principles(data_):
    """The Excalidraw principles as one mind map: the centre, the seven asked for and the two standing rules around it,
    each its title and its one-line summary in big words, so they read with the whole drawing zoomed out."""
    m = data_["mindmap"]
    f = d.frame("① The Excalidraw principles")
    d.heading("📐 The Excalidraw principles",
              "Bold: asked 261012. Thin: rules that stand. Red: open. Yellow: the key point.")
    asked = [b for b in m["branches"] if str(b.get("by", "")).startswith("asked")]
    rest = [b for b in m["branches"] if b not in asked]
    half = (len(asked) + 1) // 2
    left, right = asked[:half] + rest[:1], asked[half:] + rest[1:2]
    top, gap = 200, 26
    hs = {id(b): principle_height(b) for b in left + right}
    col_h = max(sum(hs[id(b)] for b in col) + gap * (len(col) - 1) for col in (left, right))
    f["height"] = max(H, top + col_h + 80)
    lx, rx = 40, W - 40 - PW
    cx, cw = lx + PW + 60, rx - 60 - (lx + PW + 60)
    ch = 300
    cy = top + col_h / 2 - ch / 2
    d.key(cx, cy, cw, ch, 5)                                          # the key point: the centre
    d.para(cx + 28, cy + 40, m["centre"], cw - 56, 44)                # the frame's title already names it
    for col, x, side in ((left, lx, "l"), (right, rx, "r")):
        y = top
        for b in col:
            h = hs[id(b)]
            principle_box(b, x, y, h)
            sx = cx - 4 if side == "l" else cx + cw + 4                # from the centre to each principle
            ex = x + PW + 6 if side == "l" else x - 6
            d.line([(sx, cy + ch / 2), (ex, y + min(46, h / 2))], sw=3)
            y += h + gap
    d.para(lx, f["height"] - 56, "✎ 261012 ⑦ added; each principle's details stay in the face; no point open (closed)", PW, 24,
           canvas.GREEN)
    return f


# ── ② the checks, one workflow map of stages ───────────────────────────────────────────────────────────────
STAGES = {"build": "⚙️ Build", "size": "🖼️ Size and density", "inside": "🗺️ Inside a frame", "story": "📖 The story",
          "look": "🔍 The look", "write": "💾 Write", "agree": "👤 A person agrees"}
SCRIPTS = TOOLKIT / "skills/1_base/excalidraw/excalidraw-studio/scripts"
CT, CL = 38, SMALL                                    # a stage's title, a check's line (⑦: none small)


def check_by(by):
    """Who checks it, read live: a canvas.py function or a script that exists, a person, or nobody yet."""
    if by.startswith("canvas."):
        return (f"✅ {by}", INK) if hasattr(canvas, by.split(".", 1)[1]) else (f"❓ {by} is gone", RED)
    if by.endswith(".py") and "<" not in by:                          # excalidraw-studio's own script
        return (f"✅ {by}", INK) if (SCRIPTS / by).is_file() else (f"❓ {by} is gone", RED)
    return {"person": ("👤 a person", INK), "none": ("❓ no check yet", RED)}.get(by, (f"⚙️ {by}", INK))


def check_line(c):
    return (f"{c['guards']} " if c.get("guards") and c["guards"] != "all" else "") + c["step"]


def stage_height(title, rows, w):
    return 16 + d.height(title, w - 32, CT) + 12 + \
        sum(d.height(check_line(c), w - 32, CL) + 4 + d.height(who, w - 32, CL) + 18 for c, who, _ in rows) + 10


def checks(data_):
    f = d.frame("② Checking a drawing: one workflow map")
    d.heading("🔁 Checking a drawing against them, stage by stage",
              "Each check: the principle it guards, and who checks it, read live. Red: no check yet.")
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
        y = d.para(x + 16, top + 16, STAGES.get(n, n), bw - 32, CT) + 12
        for c, who, color in rows_of[n]:
            y = d.para(x + 16, y, check_line(c), bw - 32, CL) + 4
            y = d.para(x + 16, y, who, bw - 32, CL, color) + 18
    for a, b in zip(xs, xs[1:]):
        d.line([(a + bw + 3, top + 70), (b - 3, top + 70)], sw=3)
    bus = top + bh + 60
    d.line([(xs[1] + bw / 2, bus), (xs[-2] + bw / 2, bus)], arrow=False, dashed=True, color=RED, sw=2)
    for x in xs[1:-1]:
        d.line([(x + bw / 2, top + bh + 4), (x + bw / 2, bus)], arrow=False, dashed=True, color=RED, sw=2)
    fix_w, fix_y = 1100, bus + 70
    d.key(xs[0], fix_y, fix_w, 170)                                     # the key point
    d.para(xs[0] + 22, fix_y + 18, "🔧 fix the builder, rebuild", fix_w - 44, 40)
    d.para(xs[0] + 22, fix_y + 82, data_["loop"], fix_w - 44, 30)
    d.line([(xs[1] + bw / 2, bus), (xs[1] + bw / 2, fix_y - 6)], sw=3, color=RED)
    d.line([(xs[0] + 40, fix_y - 6), (xs[0] + 40, top + bh + 6)], sw=3)
    d.text(xs[1] + bw / 2 + 14, bus - 42, "a check fails", 30, RED)
    f["height"] = max(H * 0.75, fix_y + 170 + 70)
    return f


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
    y = d.para(40, bottom + 30, "✏️ " + ba["name"] + ": nine small frames, redrawn as four in one story",
               W - 80, 30) + 20
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
    """What check.py says of a drawing on this build: a map's words against ⑦, a text frame's density against ⑥, and
    how many ❌ it finds in all; (None, None) when the drawing is not beside this Block."""
    if not Path(path).is_file():
        return None, None
    r = check_drawing(path)
    maps = [f for f in r["rows"] if f["kind"] == "map"]
    texts = [f for f in r["rows"] if f["kind"] == "text"]
    if maps:
        ok = all(f["⑦"].startswith("✅") for f in maps)
        line = f"{'✅' if ok else '❌'} ⑦ {min(f['words'] for f in maps)} to {max(f['words'] for f in maps)} words a " \
               f"map frame (at most {MAP_WORDS}), most of them small" if not ok else \
               f"✅ ⑦ at most {max(f['words'] for f in maps)} words a map frame, few small"
    elif texts:
        ok = all(f["⑥"].startswith("✅") for f in texts)
        line = f"{'✅' if ok else '❌'} ⑥ {min(f['per'] for f in texts)} to {max(f['per'] for f in texts)} words per " \
               f"million px, {'over' if ok else 'under'} the text floor of {texts[0]['floor']}"
    else:
        return None, None
    fails = sum(str(f[p]).startswith("❌") for f in r["rows"] for p in ("①", "②", "④", "⑤", "⑥", "⑦")) + \
        r["③"].startswith("❌")
    return line, f"check.py today: {fails} ❌ in its {r['frames']} frames" if fails else \
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
    per = 3                                                            # six kinds since excalidraw-task (b31 s07)
    rows = -(-len(others) // per)
    gw = (cw - 40 * (per - 1)) / per
    gh = (hh - 30 - gy - 40 * (rows - 1)) / rows
    d.text(cx + 8, gy - 74, "beside it, the other drawing kinds (b31 s02 to s07)", T_SMALL)
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
              "Its own shape, drawn by block_index.py. Yellow: nothing is made before a person ticks it.")
    boxes = d.flow(s["steps"], 40, 196, W - 80, gap=90, title=36, leaf=SMALL, labels=s.get("labels", []))
    x0, y0, w0, h0 = boxes[-1]
    x1 = boxes[0][0]
    by = y0 + h0 + 50                                                  # the loop: the next build shows it made
    d.line([(x0 + w0 / 2, y0 + h0 + 4), (x0 + w0 / 2, by), (x1 + 60, by), (x1 + 60, y0 + h0 + 6)], sw=3)
    d.text(x1 + 80, by + 8, "the next build shows it made", SMALL)
    props, jobs = s00_face(BLOCK)                                       # b31's own, read from its s00 face
    made = {p.name[:3] for p in (BLOCK / "studio").iterdir() if p.is_dir() and re.match(r"s\d\d[-_]", p.name)}
    jobs_made = {p.name[:3] for p in BLOCK.iterdir() if p.is_dir() and re.match(r"j\d\d_", p.name)}
    py, half = by + 110, (W - 80 - 80) / 2

    def proposal(x, y, head):
        """One proposal not made yet: red and dashed until a person ticks it; what it asks stays in s00's face."""
        y1 = d.para(x + 16, y + 10, head, half - 32, SMALL, RED)
        d.box(x, y, half, y1 - y + 14, RED, 2, dashed=True)
        return y1 + 30

    y = d.para(40, py, f"📋 b31's s00 proposes {len(props)} topics (sNN), {sum(p['id'] in made for p in props)} made",
               half, 34) + 14
    y = d.para(40, y, "✅ " + " · ".join(p["id"] for p in props if p["id"] in made), half, SMALL) + 20
    for p in props:
        if p["id"] not in made:
            y = proposal(40, y, f"⬜ {p['id']} · {p.get('title', '')} · {p.get('status', 'proposed')}")
    jx = 40 + half + 80
    yj = d.para(jx, py, f"🧱 and {len(jobs)} Job{'' if len(jobs) == 1 else 's'} (jNN), "
                        f"{sum(j['id'] in jobs_made for j in jobs)} made", half, 34) + 14
    for j in jobs:
        if j["id"] in jobs_made:
            yj = d.para(jx, yj, f"✅ {j['id']}_{j.get('slug', '')}", half, SMALL) + 10
        else:
            yj = proposal(jx, yj, f"⬜ {j['id']}_{j.get('slug', '')} · {j.get('title', '')}")
    bi = TOOLKIT / "skills/1_base/project/haipipe-studio/scripts/block_index.py"   # does s00 draw them? read live
    src = bi.read_text(encoding="utf-8") if bi.is_file() else ""
    yj = d.para(jx, yj + 6, "✅ block_index.py draws them in 💡 what we propose next" if "proposals_frame" in src else
                "✅ block_index.py draws them, a red dashed row each" if "job_proposals" in src else
                "❓ block_index.py does not draw proposed Jobs yet", half, SMALL) + 10
    d.para(40, max(y, yj) + 30, "🗂️ s00's own shape: " + " · ".join(s.get("own_shape", [])), W - 80, SMALL)
    f["height"] = max(H * 0.75, max(y, yj) + 30 + 90)
    return f


def main():
    out = HERE / f"{HERE.name}.excalidraw"
    data_ = data()
    fs = {}
    for draw in (principles, checks, examples, skills, s00):
        f = draw(data_)
        d.badge(f)                                       # principle 6 or 7: measured once the frame is drawn
        fs[f["name"][0]] = f
    acts = [{"name": a["name"], "frames": [fs[m]["id"] for m in a["frames"]], "arrow": a.get("arrow")}
            for a in data_["acts"]]
    b = data_.get("between") or {}
    d.acts(acts, between=[(fs[b["from"]]["id"], fs[b["to"]]["id"], b["label"])] if b else [])
    d.write(out, "build_s01_drawing_principles.py")


if __name__ == "__main__":
    main()
