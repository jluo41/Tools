"""Build cowork-workbench-design.excalidraw, the CoWork Workbench design drawing.

The drawing is generated: change this file, then run it (a generated file changes only through its generator):

    .venv/bin/python Tools/plugins/haipipe-toolkit/servers/workbench-cowork/studio/cowork-workbench-design.py

It follows the Task workbench drawing (servers/workbench-task/studio/), same sizes, colours and
grammar. One workbench is one CoWork Block. Part 1: the working Spaces, their views, the runs of
each in order and the skill of each run, read from the Workbench Table. Part 2: the Work Space as
the workbench shows it: the Jobs view, a row per Job, and the Runs panel on the right.
Part 3: where each part lives on disk.

The Parts are named Excalidraw frames. Guide › RoadMap Draw opens this file as
"Workbench design" (workbench-shared guide_families.py, family cowork). A frame name is an
address: keep it.
"""
import json
import random
import sys
import time
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_suffix(".excalidraw")
random.seed(261003)
NOW = int(time.time() * 1000)
E = []

BLUE, GREEN, INK, MUTED, RULE, PANEL = "#1864ab", "#2b8a3e", "#1e1e1e", "#495057", "#ced4da", "#f8f9fa"


def base(id_, type_, x, y, w, h, stroke=INK, bg="transparent", dashed=False, rounded=True):
    return {"id": id_, "type": type_, "x": x, "y": y, "width": w, "height": h, "angle": 0,
            "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": 2,
            "strokeStyle": "dashed" if dashed else "solid", "roughness": 0, "opacity": 100,
            "groupIds": [], "frameId": None, "roundness": {"type": 3} if rounded else None,
            "seed": random.randint(1, 2**31 - 1), "version": 1,
            "versionNonce": random.randint(1, 2**31 - 1), "isDeleted": False,
            "boundElements": [], "updated": NOW, "link": None, "locked": False}


def text(id_, x, y, s, size=16, color=INK, mono=False):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * size * (0.6 if mono else 0.56)
    e = base(id_, "text", x, y, w, len(lines) * size * 1.25, stroke=color, rounded=False)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=3 if mono else 8,
             textAlign="left", verticalAlign="top", containerId=None, autoResize=True,
             lineHeight=1.25)
    E.append(e)


def rect(id_, x, y, w, h, stroke=INK, bg="transparent", dashed=False):
    E.append(base(id_, "rectangle", x, y, w, h, stroke, bg, dashed))
    return E[-1]


def button(id_, x, y, w, h, label, sel=False, size=17, dashed=False):
    stroke = BLUE if sel else INK
    r = rect(id_, x, y, w, h, stroke, "#e7f5ff" if sel else "transparent", dashed)
    tw, th = len(label) * size * 0.56, size * 1.25
    t = base(id_ + "-text", "text", x + (w - tw) / 2, y + (h - th) / 2, tw, th, stroke=stroke, rounded=False)
    t.update(text=label, originalText=label, fontSize=size, fontFamily=8, textAlign="center",
             verticalAlign="middle", containerId=id_, autoResize=True, lineHeight=1.25)
    r["boundElements"] = [{"id": id_ + "-text", "type": "text"}]
    E.append(t)


def line(id_, x, y, w, color=RULE):
    e = base(id_, "line", x, y, w, 0, stroke=color, rounded=False)
    e.update(points=[[0, 0], [w, 0]], lastCommittedPoint=None, startBinding=None,
             endBinding=None, startArrowhead=None, endArrowhead=None)
    E.append(e)


def arrow(id_, x, y, points, color):
    e = base(id_, "arrow", x, y, max(p[0] for p in points), max(abs(p[1]) for p in points), stroke=color,
             rounded=False)
    e.update(points=points, lastCommittedPoint=None, startBinding=None, endBinding=None,
             startArrowhead=None, endArrowhead="arrow", elbowed=False)
    E.append(e)


def chips(key, x, y, labels, sel, size=16, h=40):
    """A row of buttons, each as wide as its label (Spaces, views)."""
    for n, label in enumerate(labels):
        w = max(96, int(len(label) * size * 0.56) + 32)
        button(f"{key}-{n}", x, y, w, h, label, sel=n == sel, size=size)
        x += w + 10
    return x


FW, GAP = 1176, 32
X = [48 + i * (FW + GAP) for i in range(4)]

# ---- title -----------------------------------------------------------------------
text("title", 48, 24, "CoWork Workbench · design", 34)
text("subtitle", 48, 74, "One workbench, one CoWork Block: one coordination topic. Its Jobs (one line of work each, usually a request to one office), "
     "emails, meetings and design notes, and the Questions answered by report Pages. Nothing here sends a message.", 18, MUTED)

# ---- part 1 · Space → view → runs in order → skill (from the Workbench Table) ---
P1 = 150
F1 = len(E)
text("p1-title", 48, P1, "1 · Spaces, views, runs in order, and the skill of each run", 28)

_PLUGIN = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_PLUGIN / "skills" / "0_utils" / "table-workbench" / "ref"))
from render_workbench_table import read_table  # noqa: E402

TABLE = _PLUGIN / "skills" / "cowork" / "haipipe-workbench-cowork" / "ref" / "workbench-table.md"
SPACE_TEXT = {   # what each Space asks, and what it hands on: prose the table does not hold
    "Scope": ("What is this Block, who is in it, and where does it stop?",
              "hands on: the spine and the gate → Work"),
    "Work": ("Which requests, messages, meetings and Questions move the Block?",
             "hands on: drafts and waits → Check › Drafts, Waiting on"),
    "Check": ("Who are we waiting on, which drafts are not sent, which reports can be trusted?",
              "hands on: a failed check routes back; a passed one → Delivery"),
    "Delivery": ("Which answers are ready to leave the Block?",
                 "hands on: a released report; a done Job stays listed"),
}


def map_from_table(rows):
    spaces = []
    for r in rows:
        if r["Level"] != "board" or r["Space"] == "Guide":    # Guide is shared: its runs are named below
            continue
        if not spaces or spaces[-1][0] != r["Space"]:
            spaces.append((r["Space"], []))
        views = spaces[-1][1]
        if not views or views[-1][0] != r["View"]:
            views.append((r["View"], []))
        views[-1][1].append(r)
    out = []
    for space, views in spaces:
        n, subs = 0, []
        for view, runs in views:
            items = []
            for r in runs:
                control = r["Run type"] == "none" or r["Agent"] == "none"
                if not control:
                    n += 1
                signs = "" if r["Person signs"] == "none" else f" · signs {r['Person signs']}"
                note = "a view, no run" if control else f"agent {r['Agent'].replace(' (new)', '*')}{signs}"
                items.append(("·" if control else str(n), "(read only)" if control else r["Run type"],
                              "" if control else r["Skill"].replace(" (new)", "*"), note))
            subs.append((view, items))
        asks, hands = SPACE_TEXT.get(space, ("", ""))
        out.append((f"{space} Space", asks, subs, hands))
    return out


ROWS = read_table(TABLE)
MAP = map_from_table(ROWS)
GUIDE_RUNS = [r for r in ROWS if r["Level"] == "board" and r["Space"] == "Guide" and r["Run type"] != "none"]


def height(subs):
    y = 120
    for _sub, runs in subs:
        y = max(y + 56, y + sum(62 if note else 44 for *_x, note in runs) + 12)
    return y


BH = max(height(subs) for _t, _a, subs, _h in MAP) + 76
for i, (title, asks, subs, hands) in enumerate(MAP):
    x0, y0 = X[i], P1 + 56
    rect(f"m{i}-box", x0, y0, FW, BH)
    text(f"m{i}-title", x0 + 24, y0 + 22, title, 28)
    text(f"m{i}-asks", x0 + 24, y0 + 64, asks, 19, BLUE)
    line(f"m{i}-rule", x0 + 24, y0 + 100, FW - 48)
    y = y0 + 120
    for n, (sub, runs) in enumerate(subs):
        button(f"m{i}-sub{n}", x0 + 24, y, 200, 40, sub, size=17)
        ry = y
        for k, (num, run, skill, note) in enumerate(runs):
            ctl = num == "·"
            text(f"m{i}-sub{n}-run{k}", x0 + 248, ry + 4, "%s  %-22s" % (num, run), 19, MUTED if ctl else INK, mono=True)
            text(f"m{i}-sub{n}-skill{k}", x0 + 640, ry + 4, skill, 17, MUTED if ctl else GREEN, mono=True)
            if note:
                text(f"m{i}-sub{n}-note{k}", x0 + 640, ry + 30, note, 14, MUTED)
            ry += 62 if note else 44
        y = max(y + 56, ry + 12)
    text(f"m{i}-hands", x0 + 24, y0 + BH - 52, hands, 16, MUTED)
for i in range(len(MAP) - 1):
    arrow(f"m-link{i}", X[i] + FW + 2, P1 + 116, [[0, 0], [GAP - 4, 0]], BLUE)
text("m-rules", 48, P1 + 56 + BH + 28,
     "Drawn from haipipe-workbench-cowork/ref/workbench-table.md. The number is the order inside a Space; "
     "· marks a view with no run; * marks a planned skill or agent.\n"
     "No agent sends a message: the person signs every send. A judging run names a different agent from the one that made the thing.\n"
     "Guide, shared by every workbench, holds the method and the papers: "
     + " · ".join(f'{r["View"]} → {r["Run type"]} ({r["Skill"]})' for r in GUIDE_RUNS) + ".", 17)

# ---- part 2 · the Work Space as the workbench shows it ---------------------------
P2 = P1 + 56 + BH + 150
F2 = len(E)
text("p2-title", 48, P2, "2 · The Work Space, Jobs view: a row per Job; its Runs panel on the right", 28)
Y0, W2 = P2 + 56, 4 * FW + 3 * GAP
rect("ws-box", 48, Y0, W2, 1010)
text("ws-head", 72, Y0 + 22, "<Block title>", 30)
text("ws-band", 72, Y0 + 64, "<Project> / cowork / bNN_<topic> · its spine, one line", 16, MUTED)
chips("ws-space", 72, Y0 + 100, ["Guide", "Scope", "Work", "Check", "Delivery"], 2, size=19, h=50)
chips("ws-view", 72, Y0 + 168, ["Jobs", "Questions", "Emails", "Meetings"], 0, size=15, h=38)

CW = 3000                                          # the table; the Runs panel takes the rest
cx, cy = 72, Y0 + 236
rect("q-table", cx, cy, CW, 690)
text("q-group", cx + 20, cy + 16, "Jobs · 3 open", 22)
heads = ["job · office number", "what we asked for", "waiting on · since", "next step", "page"]
colx = [0, 330, 1050, 1620, 2400]
for n, head in enumerate(heads):
    text(f"q-head{n}", cx + 24 + colx[n], cy + 60, head, 16, MUTED)
line("q-rule0", cx, cy + 92, CW)
rows = [("j02_cloud_group · IT-1042", "a cloud storage group for the wearable data", "IT office · 2026-10-09 (3 days)",
         "send the v3 diagram and the IRB wording", "j02_cloud_group/j02_cloud_group.md   ⧉"),
        ("j03_storage_plan · none yet", "approval of the storage plan", "us · 2026-10-02 (10 days)",
         "draft the amendment", "j03_storage_plan/j03_storage_plan.md   ⧉"),
        ("j04_access_list · IT-1051", "named people on the access list", "IT office · 2026-10-05 (7 days)",
         "ask for the group's expected date", "j04_access_list/j04_access_list.md   ⧉")]
for r, vals in enumerate(rows):
    y = cy + 112 + r * 70
    for n, v in enumerate(vals):
        text(f"q-r{r}c{n}", cx + 24 + colx[n], y, v, 17, INK if n < 4 else BLUE)
    line(f"q-rule{r + 1}", cx, y + 52, CW)
text("q-more", cx + 24, cy + 340, "Timeline  2026-10-09  IT office replied: group created, access list next\n"
     "Checklist  - [x] 1 open the Job      - [ ] 2 send the v3 diagram (draft in emails/)   - [ ] 3 meet the IT office",
     17, MUTED, mono=True)
text("q-note", cx + 24, cy + 430, "Each row reads the header of a job page (state, waiting-on, since, next). Rows with waiting on = us show first on Check › Waiting on, longest wait at the top.\n"
     "A draft is a file in a Job's emails/ whose name has 'draft' or whose header says status: draft; it is listed on Check › Drafts.",
     16, MUTED)

rx = cx + CW + 40
WORK_RUNS = [r for r in ROWS if r["Space"] == "Work" and r["Run type"] != "none"]   # the panel's buttons
rect("runs", rx, cy, W2 - CW - 88, max(768, 110 + 50 * len(WORK_RUNS)), bg=PANEL)
text("runs-title", rx + 20, cy + 20, "Runs  ◂", 22)
PICK = next((r for r in WORK_RUNS if r["Run type"] == "Open a job"), WORK_RUNS[0])
for n, r in enumerate(WORK_RUNS):
    button(f"runs-type{n}", rx + 20, cy + 70 + n * 50, 260, 40, r["Run type"], sel=r is PICK, size=15)
dx = rx + 300
rect("runs-detail", dx, cy + 70, W2 - CW - 88 - 320, 650, bg="#ffffff")
text("runs-detail-t", dx + 16, cy + 84, PICK["Run type"], 17)
text("runs-skill", dx + 16, cy + 114, f'Skill {PICK["Skill"]} · agent {PICK["Agent"]}', 13, GREEN, mono=True)
text("runs-prompt", dx + 16, cy + 150, "Prompt  [Copy]\n/haipipe-cowork: open a job for <need> in <block>", 14, MUTED)
text("runs-list", dx + 16, cy + 230, "Runs of the picked row\nopen a job         done   ⧉\n"
     "update a job       done   ⧉", 14, INK, mono=True)
text("runs-note", dx + 16, cy + 360, "Status lives here, never in the table.\nPicking a Job row narrows the list.\n"
     "Copy hands the prompt to a session;\nnothing here starts a run or sends a message.", 14, MUTED)
text("ws-notes", 72, Y0 + 1020 - 50, "A row is one Job. Questions are Logic │ Work │ Report rows whose Work cites Block files; "
     "Emails and Meetings are newest first. A job page, a draft, a report and a drawing open in one pop-out. No status in the table.",
     16, MUTED)

# ---- part 3 · where things live --------------------------------------------------
P3 = Y0 + 1010 + 150
F3 = len(E)
text("p3-title", 48, P3, "3 · Where things live: the Block folder", 28)
tree = ("cowork/bNN_<topic>/\n"
        "├── board.md                      header · text · Questions register · Related resources\n"
        "├── j00_people/                    who to ask for help (state: 📇 REFERENCE)\n"
        "├── jNN_<job>/                     one line of work, usually one request to one office\n"
        "│   ├── jNN_<job>.md               header: state · waiting-on · since · next · ticket · url\n"
        "│   ├── Timeline.md · CHECKLIST.md dates; numbered steps with their draft messages\n"
        "│   └── emails/ · meetings/ · design/ · materials/    only when needed\n"
        "├── studio/                        drawings and decks (generated ones by studio/_build/)\n"
        "├── reports/qNN_<topic>/           one report Page per Question\n"
        "│   ├── qNN_<topic>.md · page.toml\n"
        "│   └── runs/                      the Page's own runs (check)\n"
        "└── _old/                          replaced material; do not use")
rect("tree-box", 48, P3 + 56, W2, 440)
text("tree", 80, P3 + 84, tree, 20, INK, mono=True)
text("tree-notes", 80, P3 + 56 + 440 + 24,
     "Guide's Method and Related Paper live with the skill (haipipe-workbench-cowork/ref/), the same for every Block. "
     "Office files, recordings and anything over 5 MB stay local through cowork/.gitignore.", 17, MUTED)


# ---- frames ------------------------------------------------------------------------
def bounds(e):
    if e.get("points"):
        xs, ys = [e["x"] + p[0] for p in e["points"]], [e["y"] + p[1] for p in e["points"]]
        return min(xs), min(ys), max(xs), max(ys)
    return e["x"], e["y"], e["x"] + e["width"], e["y"] + e["height"]


def frame(id_, name, start, end, pad=40):
    """One named Excalidraw frame around E[start:end]; Guide opens a frame by its name."""
    box = [bounds(e) for e in E[start:end]]
    f = base(id_, "frame", min(b[0] for b in box) - pad, min(b[1] for b in box) - pad,
             max(b[2] for b in box) - min(b[0] for b in box) + 2 * pad,
             max(b[3] for b in box) - min(b[1] for b in box) + 2 * pad, rounded=False)
    f["name"] = name
    for e in E[start:end]:
        e["frameId"] = id_
    return f


END = len(E)
E += [frame("frame-skills", "Spaces, runs and skills", F1, F2),
      frame("frame-workbench", "The workbench", F2, F3),
      frame("frame-folders", "Where things live", F3, END)]

OUT.write_text(json.dumps({"type": "excalidraw", "version": 2, "source": "haipipe-cowork-workbench-design",
                           "elements": E, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
                           "files": {}}, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(E), "elements →", OUT.name)
