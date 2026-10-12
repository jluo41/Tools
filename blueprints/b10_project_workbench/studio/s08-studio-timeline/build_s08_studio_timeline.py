"""s08 · Timeline: what moved when, down one axis: s08-studio-timeline.excalidraw, drawn by this builder (haipipe-studio).

Two frames in one row (JL 261011: "a real timeline ... very concise ... with a axis down", "up to down",
"different level of details", "create a new sNN for it, and show the UI"):

    ① Where a line comes from   the three things a topic already keeps, each made one event, then grouped
                                 by day and by topic; the group bar; the open points in red
    ② The Timeline on screen    the Studio's Timeline at its three levels, Days (a bubble chart) · Topics · Everything, drawn
                                 from this Block's own events, read through the server's frame.timeline_events

A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside the drawing).

    python build_s08_studio_timeline.py
"""
import datetime
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
ROOT = HERE.parents[3]                                  # Tools/: the root the workbench serves
SERVERS = ROOT / "plugins/haipipe-toolkit/servers"
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)
sys.path.insert(0, str(SERVERS / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()
from live import frame  # noqa: E402  (the workbench's own reader: the drawing shows what the screen shows)

INK, RED = canvas.INK, canvas.RED      # the studio look: black; red for an open question
SANS, MONO = canvas.FONT, canvas.CODE_FONT
els = []


def el(kind, x, y, w, h, frame=None, **extra):
    e = {"id": f"e{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
         "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [], "frameId": frame,
         "roundness": None, "seed": 1, "version": 1, "versionNonce": 1, "isDeleted": False,
         "boundElements": [], "updated": 1, "link": None, "locked": False}
    e.update(extra)
    els.append(e)
    return e


def text(x, y, s, size=20, frame=None, color=INK, font=SANS):
    lines = s.split("\n")
    return el("text", x, y, max(len(l) for l in lines) * size * (0.6 if font == MONO else 0.55),
              len(lines) * size * 1.25, frame, text=s, originalText=s, fontSize=size, fontFamily=font,
              textAlign="left", verticalAlign="top", containerId=None, autoResize=True, lineHeight=1.25,
              strokeColor=color)


def box(x, y, w, h, frame, width=1, round_=True):
    return el("rectangle", x, y, w, h, frame, strokeWidth=width, roundness={"type": 3} if round_ else None)


def line(x0, y0, x1, y1, frame, arrow=False, width=2):
    return el("arrow" if arrow else "line", x0, y0, abs(x1 - x0) or 1, abs(y1 - y0) or 1, frame,
              points=[[0, 0], [x1 - x0, y1 - y0]], strokeWidth=width, lastCommittedPoint=None,
              startBinding=None, endBinding=None, startArrowhead=None, endArrowhead="arrow" if arrow else None)


def fit(f, pad=60):
    """The frame around what is drawn in it, `pad` on every side."""
    kids = [e for e in els if e.get("frameId") == f["id"]]
    xs = [v for e in kids for v in ((e["x"], e["x"] + e["width"]) if not e.get("points") else
                                    (e["x"] + px for px, _ in e["points"]))]
    ys = [v for e in kids for v in ((e["y"], e["y"] + e["height"]) if not e.get("points") else
                                    (e["y"] + py for _, py in e["points"]))]
    f.update(x=min(xs) - pad, y=min(ys) - pad, width=max(xs) - min(xs) + 2 * pad, height=max(ys) - min(ys) + 2 * pad)
    return f


def chip(x, y, label, frame, size=20):
    w = len(label) * size * 0.55 + 18
    box(x, y, w, 32, frame)
    text(x + 9, y + 3, label, size, frame)
    return w


# ── the data: this Block's events, as the Studio's Timeline reads them ──────────────────────────
EVENTS, UNDATED = frame.timeline_events(BLOCK, ROOT)
WORD = {"decided": ("decided", "decided"), "session": ("session", "sessions"), "drawing": ("note", "notes")}


def count(items):
    n = {k: sum(e.get("n", 1) for e in items if e["kind"] == k) for k in WORD}
    return " · ".join(f"{v} {WORD[k][v != 1]}" for k, v in n.items() if v)


def by_day():
    days = {}
    for e in sorted(EVENTS, key=lambda e: e["day"]):
        days.setdefault(e["day"], {}).setdefault(e["key"], []).append(e)
    return days


def plain(html_):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html_)).replace("&#x27;", "'").replace("&quot;", '"').replace("&amp;", "&").strip()


def label(day):
    return datetime.date.fromisoformat(day).strftime("%a %d %b")


def short(s, n):
    return s if len(s) <= n else s[:n - 1].rsplit(" ", 1)[0] + " …"


# ── ① where a line comes from ───────────────────────────────────────────────────────────────────
def frame_sources():
    f = el("frame", 0, 0, 1700, 1180, name="Where a line comes from")
    fid = f["id"]
    kinds = {k: sum(e.get("n", 1) for e in EVENTS if e["kind"] == k) for k in WORD}
    text(60, 50, "Where a line comes from", 34, fid)
    text(60, 100, "nothing new is written: each topic already keeps all three", 22, fid)
    rows = [("the face", "s04-D07 · Related uses the group bar … (JL 261011)",
             f"decided · {kinds['decided']}", "dated by the first YYMMDD in it"),
            ("its Run", "runs/run-draw-s04/passes/p01-1011/",
             f"session · {kinds['session']}", "the year comes from its notes"),
            ("its drawing", "like  ✎ 261011 a group column, as the Studio's tags",
             f"note · {kinds['drawing']}", "the green change notes")]
    y = 190
    for name, sample, what, why in rows:
        box(60, y, 700, 110, fid)
        text(84, y + 16, name, 23, fid)
        text(84, y + 60, sample, 20, fid, font=MONO if "/" in sample else SANS)
        line(760, y + 55, 900, y + 55, fid, arrow=True)
        text(920, y + 22, what, 23, fid)
        text(920, y + 60, why, 20, fid)
        y += 150
    text(84, y - 20, f"{len(UNDATED)} decisions carry no date: listed under the axis (later: Later 3)", 20, fid)
    y += 60
    box(60, y, 1560, 96, fid, width=2)
    text(84, y + 14, "one event  =  day · topic · kind", 26, fid)
    text(84, y + 54, f"{len(EVENTS)} events in this Block, from {min(e['day'] for e in EVENTS)} to "
                     f"{max(e['day'] for e in EVENTS)}", 20, fid)
    line(340, y + 96, 340, y + 150, fid, arrow=True)
    y += 160
    steps = [("a dot per day", "the axis runs down: the oldest day at the top, the newest at the bottom"),
             ("a line per topic", "under its day: how many decided, sessions, notes"),
             ("its items", "each decision, session and note, in that topic's line")]
    for i, (name, why) in enumerate(steps):
        box(60, y, 470, 70, fid)
        text(84, y + 20, name, 23, fid)
        text(560, y + 22, why, 20, fid)
        if i < len(steps) - 1:
            line(295, y + 70, 295, y + 100, fid, arrow=True)
        y += 100
    text(60, y + 20, "the group bar above the topics hides a topic's lines; a day left empty hides too", 20, fid)
    text(60, y + 56, "Days · Topics · Everything: how far down the three steps the screen shows; this browser keeps it", 20, fid)
    # agreed 261011 (s08-D06): the open points wait for later, in black (JL: "close the timeline now")
    text(60, y + 110, "later, not needed now (the face's Later list):", 20, fid)
    els.append(canvas.change_note(560, y + 112, "agreed: these wait for later (JL)", "261011", fid, 17))
    els[-1]["id"] = f"e{len(els) - 1}"
    text(84, y + 142, "the newest day at the bottom: open the Timeline scrolled to it", 20, fid)
    text(84, y + 174, "a Report answered, a Run closed: dots on this axis too", 20, fid)
    text(84, y + 206, "many more topics: a chart library that zooms and pans, or a column per group", 20, fid)
    return fit(f)


# ── ② the Timeline on screen, at its three levels ─────────────────────────────────────────────────
def column_head(x, y, w, picked, fid, what):
    bx = x
    for name in ("Days", "Topics", "Everything"):
        bw = len(name) * 11 + 30
        box(bx, y, bw, 40, fid, width=3 if name == picked else 1)
        text(bx + 15, y + 8, name, 20, fid)
        bx += bw + 10
    text(x, y + 56, what, 20, fid)


def axis(x, top, bottom, fid):
    line(x, top, x, bottom, fid, arrow=True, width=3)


def dot(x, y, fid):
    text(x - 12, y - 22, "●", 34, fid)


def frame_screen():
    days = by_day()
    f = el("frame", 0, 0, 2700, 1440, name="The Timeline on screen")
    canvas.ui_frame(f, since="261012")                      # a screen: the workbench's colours (JL 261012)
    fid = f["id"]
    kinds = {k: sum(e.get("n", 1) for e in EVENTS if e["kind"] == k) for k in WORD}
    text(60, 50, "The Timeline on screen: one axis down, three levels of detail", 34, fid)
    text(60, 100, "Studio › Timeline, folded under the topics and Related; this Block's own events, read at build time", 22, fid)
    box(60, 150, 2520, 56, fid)
    text(84, 162, "▾ Timeline", 22, fid)                 # no counts in the header (JL 261011)
    e = canvas.change_note(260, 166, "no counts in the header (JL)", "261011", fid, 17)
    e["id"] = f"e{len(els)}"
    els.append(e)
    top, most = 330, 30
    # Days: the chart, a row per day down the axis, a column per topic group (the default; JL 261011: "the
    # columns can also be the topic groups") or per topic, a bubble sized by how much moved
    x0 = 60
    column_head(x0, 236, 960, "Days", fid, "Days: a bubble per group and day; columns by group or by topic")
    e = canvas.change_note(x0 + 640, 296, "columns are the topic groups (JL)", "261011", fid, 17)
    e["id"] = f"e{len(els)}"
    els.append(e)
    size = lambda items: sum(e.get("n", 1) for e in items)
    peak = max(size(items) for ts in days.values() for items in ts.values())
    day_peak = max(sum(size(items) for items in ts.values()) for ts in days.values())
    tags = {e["key"]: e.get("tags") or [] for e in EVENTS}
    names = frame.studio_group_order(BLOCK) + sorted({g for gs in tags.values() for g in gs}, key=str.casefold)
    cols = []                                           # (group, its topic keys), in the group bar's order
    for name in names:
        keys = [k for k, gs in tags.items() if name.casefold() in {g.casefold() for g in gs}]
        if keys and name.casefold() not in {c[0].casefold() for c in cols}:
            cols.append((name, keys))
    if any(not gs for gs in tags.values()):
        cols.append(("Untagged", [k for k, gs in tags.items() if not gs]))
    gsize = lambda topics, keys: sum(size(topics[k]) for k in keys if k in topics)
    gpeak = max(gsize(ts, keys) for ts in days.values() for _, keys in cols)
    ax, cx0, step = x0 + 150, x0 + 240, 120
    bar_x = cx0 + step * len(cols) - 50
    for i, (name, _) in enumerate(cols):
        text(cx0 + i * step - len(name) * 5.5, top, name, 20, fid)
    text(bar_x, top, "changes", 20, fid)
    y = top + 70
    for day, topics in days.items():
        text(x0, y - 12, label(day), 20, fid)
        dot(ax, y, fid)
        for i, (name, keys) in enumerate(cols):
            if gsize(topics, keys):
                d = round(8 + 30 * (gsize(topics, keys) / gpeak) ** 0.5)
                el("ellipse", cx0 + i * step - d / 2, y - d / 2, d, d, fid, strokeWidth=2)
        n = sum(size(items) for items in topics.values())
        w = max(round(120 * n / day_peak), 4)
        box(bar_x, y - 6, w, 12, fid, round_=False)
        text(bar_x + w + 10, y - 12, str(n), 20, fid)
        y += 64
    axis(ax, top + 40, y - 20, fid)
    text(x0, y + 20, "click topics to read them: their items show under the chart, on the same axis", 20, fid)
    e = canvas.change_note(x0, y + 54, "pick topics, read them below (JL)", "261011", fid, 17)
    e["id"] = f"e{len(els)}"
    els.append(e)
    # Topics: a line per topic under its day; the oldest days fold away to fit
    x1 = 1240
    column_head(x1, 236, 760, "Topics", fid, "Topics: a line per topic, a bar of its changes")
    shown, lines_ = [], 0
    for day in reversed(list(days)):
        need = len(days[day]) + 1
        if lines_ + need > most:
            break
        shown.insert(0, day)
        lines_ += need
    y, ax = top, x1 + 150
    if len(shown) < len(days):
        text(ax + 30, y, f"↑ {len(days) - len(shown)} earlier days", 20, fid)
        y += 40
    for day in shown:
        text(x1, y, label(day), 20, fid)
        dot(ax, y + 12, fid)
        for key, items in days[day].items():
            text(ax + 30, y, short(items[0]["name"], 30), 20, fid)
            w = max(round(150 * sum(e.get("n", 1) for e in items) / peak), 6)
            box(ax + 380, y + 6, w, 12, fid, round_=False)
            text(ax + 390 + w, y, str(sum(e.get("n", 1) for e in items)), 20, fid)
            y += 30
        y += 14
    axis(ax, top - 10, y + 10, fid)
    # Everything: each decision, session and note; only the newest day fits
    x2 = 2080
    column_head(x2, 236, 700, "Everything", fid, "Everything: each decision, session and note")
    day = max(days)
    y, ax = top, x2 + 150
    text(ax + 30, y, f"↑ {len(days) - 1} earlier days", 20, fid)
    y += 40
    text(x2, y, label(day), 20, fid)
    dot(ax, y + 12, fid)
    left = most - 2
    for key, items in days[day].items():
        if left <= 1:
            break
        text(ax + 30, y, items[0]["name"], 20, fid)
        y += 30
        left -= 1
        for e in items:
            if left <= 1:
                break
            text(ax + 54, y, short(f"{WORD[e['kind']][0]}  {plain(e['html'])}", 40), 20, fid)
            y += 30
            left -= 1
    rest = sum(1 for items in days[day].values() for _ in [0] + items) - (most - 2 - left)
    if rest > 0:
        text(ax + 54, y, f"… {rest} more lines that day", 20, fid)
        y += 30
    axis(ax, top - 10, y + 10, fid)
    return fit(f)


def main():
    out = HERE / "s08-studio-timeline.excalidraw"
    els.clear()
    a = frame_sources()
    b = frame_screen()
    canvas.grid(els, [[a["id"], b["id"]]], gap=260)
    y = a["y"] + 160                                   # -->: what comes in, drawn as the screen
    line(a["x"] + a["width"] + 20, y, b["x"] - 20, y, None, arrow=True, width=4)
    text(a["x"] + a["width"] + 30, y - 70, "drawn as", 22)
    for e in canvas.off_palette(els):                    # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, els, "build_s08_studio_timeline.py")


if __name__ == "__main__":
    main()
