"""b03 scratch canvas: studio/project-scratch.excalidraw, a sketchy whiteboard for designing
the Project skills.

A prototype of concepts, not a report on any workspace: every name is a placeholder
(<project>, bNN_<topic>, <run>), every claim comes from what the skills say about their
own levels. Clusters: the ladder (six levels, what each must hold, who owns it), the anatomy
of a Block and of a Run, the Themes against the levels, the skills against the levels, how
content crosses Themes, the checker's layers, and a Questions zone: each question from
board.md, our ideas, and an empty box per question for the person's own thoughts.

The canvas is shared: every element this script draws has an id starting "s-"; a rebuild
replaces only those still at version 1, and keeps anything a person added or moved.

    python build_project_scratch.py [out.excalidraw]
"""
import json
import random
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas
import disk_facts as F          # only questions(): the Block's own register in board.md

random.seed(261005)
HAND, MONO = 6, 3                                    # Excalidraw fonts: Nunito (readable sans), Cascadia
INK, GRAY, RED, BLUE, GREEN, ORANGE = "#1e1e1e", "#868e96", "#e03131", "#1971c2", "#2f9e44", "#e8590c"
STICKY = {"fit": "#b2f2bb", "bend": "#ffd8a8", "none": "#e9ecef", "ask": "#ffec99", "open": "#ffc9c9",
          "idea": "#d0ebff"}
els = []
FRAME = [None]                                       # elements drawn now belong to this frame


def base(kind, x, y, w, h, stroke=INK, bg="transparent", sw=2, dashed=False, angle=0.0):
    e = {"id": f"s-{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": angle,
         "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": sw,
         "strokeStyle": "dashed" if dashed else "solid", "roughness": 1, "opacity": 100, "groupIds": [],
         "frameId": FRAME[0], "roundness": {"type": 3} if kind == "rectangle" else None,
         "seed": random.randint(1, 2**31 - 1), "version": 1, "versionNonce": random.randint(1, 2**31 - 1),
         "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False}
    els.append(e)
    return e


def text(x, y, s, size=22, color=INK, font=HAND, angle=0.0, container=None):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * size * (0.6 if font == MONO else 0.55)
    e = base("text", x, y, w, len(lines) * size * 1.25, color, angle=angle)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",
             containerId=container, autoResize=True, lineHeight=1.25)
    return e


def box(x, y, w, h, stroke=INK, bg="transparent", dashed=False, sw=2, angle=0.0):
    return base("rectangle", x, y, w, h, stroke, bg, sw, dashed, angle)


def sticky(x, y, w, h, body, kind, size=20):
    """A sticky note a person can double-click and rewrite: the text is bound to its note."""
    a = 0.0                                      # notes sit straight: tilt reads as crooked
    h = max(h, 40 + (body.count("\n") + 1) * size * 1.35)
    r = box(x, y, w, h, INK, STICKY[kind], sw=1, angle=a)
    t = text(x + 16, y + 14, body, size, INK, angle=a, container=r["id"])
    r["boundElements"] = [{"type": "text", "id": t["id"]}]
    return r


def arrow(pts, color=INK, sw=2, dashed=False):
    x, y = pts[0]
    rel = [[px - x, py - y] for px, py in pts]
    e = base("arrow", x, y, max(abs(p[0]) for p in rel) or 1, max(abs(p[1]) for p in rel) or 1, color, sw=sw,
             dashed=dashed)
    e.update(points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None,
             endArrowhead="arrow")


def mark(x, y, w, h, color=RED):
    """A red rectangle around the one line that matters (rectangles, not ellipses: they fit a line)."""
    base("rectangle", x, y, w, h, color, sw=2)



def mono(x, y, lines, size=15, width=None, title=None, bg="#f8f9fa"):
    """Lines in monospace inside a sketchy box; returns its bottom."""
    w = width or max(len(l) for l in lines) * size * 0.6 + 40
    top = 34 if title else 14
    box(x, y, w, top + len(lines) * size * 1.3 + 16, GRAY, bg, sw=1)
    if title:
        text(x + 14, y + 8, title, 18, GRAY)
    for i, l in enumerate(lines):
        text(x + 18, y + top + i * size * 1.3, l, size, INK, MONO)
    return y + top + len(lines) * size * 1.3 + 16


def mark_line(x, y, line, size=15, i=0, top=34):
    """A red rectangle fitted to line i of a mono() block drawn at (x, y)."""
    mark(x + 10, y + top + i * size * 1.3 - 3, len(line) * size * 0.6 + 16, size * 1.3 + 6)


# ── the concepts, as the skills state them (placeholders only) ──────────────────────────────
LEVELS = [  # level, folder, must hold, owner, what it is for
    ("Project", "<world>/<project>/", "README.md + project.yaml", "haipipe-project", "one research or software boundary"),
    ("Theme", "tasks/ discoveries/ cowork/\npapers/ insights/ designs/", "made lazily by its owner", "haipipe-project", "one kind of work"),
    ("Block", "bNN_<topic>/", "board.md: kind, spine, close,\nQuestions; studio/; reports/", "domain skill", "one topic and its Questions"),
    ("Job", "jNN_<job>/", "one line of work", "domain skill", "a line of work toward the Questions"),
    ("Task", "tNN_<task>/", "tNN_<task>.md = the Page", "haipipe-task + page", "one bounded piece, readable as a Page"),
    ("Run", "runs/<run>.*\nresults/<run>/", "runtime.yaml, run: = stem", "haipipe-run", "one commission, one identity"),
]
BLOCK_TREE = [  # a Block has two branches: the questions (for the audience) and the work
    "bNN_<topic>/",
    "├ board.md                 kind · spine · close · Questions register",
    "├ studio/                  drawings the Questions share (+ _build/)",
    "│",
    "├ reports/                 BRANCH 1 · the questions, for the audience",
    "│  └ qNN_<topic>/          one Question -> its report Page",
    "│",
    "└ jNN_<job>/               BRANCH 2 · the work that answers them",
    "   └ tNN_<task>/",
    "      ├ tNN_<task>.md       the Task is a Page",
    "      ├ runs/<run>.sh       the ticket (authored)",
    "      └ results/<run>/      the Result (generated) + runtime.yaml",
]
RUN_TREE = [
    "run:       <run>          = the stem of ticket and Result",
    "status:    planned | running | complete | failed",
    "ticket:    <task>/runs/<run>.sh",
    "result:    <task>/results/<run>/",
    "inputs:    path + sha256 of what was frozen",
    "started_at / finished_at   null until they happen",
    "address:   bNN.jNN.tNN.rNN   one id across the tree?",
]
DIALECTS = [  # haipipe-run ref/identity-and-history.md, "Address and resolver"
    ("Folder-local", "<folder>/runs/<run>.sh", "<folder>/results/<run>/"),
    ("Job-backed Task", "<job>/<task>/runs/<run>.sh", "$OUTPUT_ROOT/<task>/results/<run>/"),
    ("Page", "<page>/runs/<native-run>.md", "results/<native-run>/"),
    ("Design", "<design>/runs/rdNN_<op>_<slug>.yaml", "<design>/results/<same-stem>/"),
    ("Labeling", "<page>/runs/rlNN_<op>_<target>.yaml", "<page>/results/<same-stem>/"),
    ("Insight RI", "<instance>/runs/riNN_<slug>.yaml", "results/<ri>/vNNN/"),
]
THEMES = [  # how each Theme's own skill fills the levels
    ("tasks/", "bNN_<topic>", "jNN_<job>", "tNN_<task> (Page)", "rNN_<run>.sh"),
    ("discoveries/", "bNN_<topic>", "jNN_<job>", "tNN_<task> (Page)", "rNN_<author><year>_<subj>"),
    ("cowork/", "bNN_<topic>", "jNN_<job>", "-  no Task", "-  no Run"),
    ("papers/", "Paper-<Name>/", "?", "Story / Section Pages", "run-section-<MMDD>-<slug>"),
    ("insights/", "Insight-<Name>/", "1-Data .. 4-Wisdom", "question folder", "riNN_<slug>"),
    ("designs/", "Design-<Name>/", "?", "Design Folder (Page)", "rdNN_<op>_<slug>.yaml"),
]
SAYS = [
    ("insights", "\"Inside it there is no B-J-T-R: the level is the Job, the question folder the Task\""),
    ("cowork", "\"There is no tNN level in cowork; work that runs code is a Task Block\""),
    ("papers", "\"a paper as a graph of Board Pages\""),
    ("tasks", "\"Task Folder = Page Folder at the tNN Task level\""),
]
OWNERS = [
    "Project    haipipe-project        root, manifest, Theme folders",
    "Theme      haipipe-project        the boundary; inside: its domain skill",
    "Block      haipipe-board          board.md, studio/",
    "           haipipe-question       Questions register, reports/qNN_",
    "Job        domain skill           task, discovery, insight, design, paper, cowork",
    "Task       haipipe-task           Plan -> Build -> Execute -> Report",
    "           haipipe-page           the Task's Page face",
    "Run        haipipe-run            identity, ticket <-> Result, receipt",
    "           domain skill           its profile: what a Run of this kind does",
    "checker    haipipe-project audit  today: the root only",
]
CHECKS = [  # checker layers, from cheap to deep
    ("L1 root", "README, project.yaml, only Theme folders", "today"),
    ("L2 names", "bNN_ / jNN_ / tNN_ as each Theme's table says", "new"),
    ("L3 Block files", "board.md register <-> reports/qNN_ folders", "new"),
    ("L4 Run pairs", "ticket <-> results/<run>/, receipt run: = stem", "new"),
    ("L5 meaning", "status, acceptance, freshness", "owner skill"),
]
WORKBENCH = [  # servers/README.md, "Adding a workbench"
    "level    workbench                     what it shows",
    "Block    a Board workbench per Theme   the Block: its Questions, Jobs, Tasks",
    "Task     the Page workbench            Outline · Run Space · Delivery · Folder",
    "Run      the Runs panel                right of every Space, one card per Run",
    "",
    "Space    a stage: Guide -> setup -> work -> Delivery",
    "View     a tab inside a Space",
    "Run type a kind of Run Spec the Space can start",
    "row      Space · View · Run type · Agent · Skill · Person signs",
]
IDEAS = {
    "Q01": [("idea", "Block = topic + board.md\nJob = line of work\nTask = folder = Page\nRun = ticket + same-stem Result"),
            ("open", "Theme, or keep\nthe word world?"),
            ("open", "one address for all:\nbNN.jNN.tNN.rNN ?"),
            ("fit", "done 261005: haipipe-run\nnow in skills/1_base/project/")],
    "Q02": [("idea", "one row per Theme:\nwhich folder fills each level,\nor 'skipped by rule'"),
            ("fit", "decided 261005:\ninsights Block = Insight-<Name>\ndesigns Block = Design-<Name>\nthe Prototype goes to tasks/"),
            ("open", "insights: is the Instance\na Block of its own?"),
            ("open", "papers: is a Page\nthe Task level?"),
            ("open", "designs: what is the Job?\ncowork: skip Task + Run, OK?")],
    "Q03": [("idea", "every Theme Block:\nboard.md register +\nreports/qNN_<topic>/ + studio/"),
            ("idea", "papers: questions are the\nStory's RQ<n>, no register yet"),
            ("idea", "a Block Question is a topic;\nan insight D/I/K/W file\nis one of its asks")],
    "Q04": [("idea", "consumer binds producer's\nResult by id + hash,\nnever copies it"),
            ("idea", "papers <- tasks + discoveries\ndesigns <- signed Insight\nhandoff"),
            ("open", "insights A: call Task Runs,\nhold only the reading"),
            ("open", "insights B: own its Runs\nin each Instance")],
    "Q05": [("idea", "layers L1 -> L4 in one\nwalk, each Theme read\nthrough its table"),
            ("idea", "the Theme table is data\nthe checker reads, not\ncode per Theme"),
            ("open", "L5: read receipt meaning\ntoo, or leave it to\neach owner skill?")],
    "Q06": [("idea", "haipipe-project = door\n+ -theme -block -job\n-task -run sub-skills"),
            ("idea", "Theme owners stay:\ntask, discovery, paper,\ninsight, design, cowork"),
            ("open", "retire haipipe-board\ninto -block in steps?"),
            ("open", "haipipe-run: keep the\nname, or -project-run?")],
    "Q07": [("idea", "a workbench shows one\nlevel: Board -> Block,\nPage -> Task"),
            ("idea", "Space = stage, View = tab,\nRun type = Run Spec kind,\nRun = the ladder's Run"),
            ("idea", "one table row binds\nSpace, View, Run type,\nAgent, Skill, who signs"),
            ("open", "a Job level workbench,\nor none?")],
    "Q08": [("idea", "now: serve.py on a laptop,\nshared over Tailscale,\nBasic Auth"),
            ("idea", "lasting: an always-on\ninternal host, company\nsign-in, git pull to sync"),
            ("open", "a viewer role: no terminal,\nchat or writes (today\nACCESS_MODE is a label)"),
            ("open", "who may open it:\nthe team, or the\nwhole company?")],
}


def include(path, dx, dy, tag):
    """Copy another studio drawing onto this canvas, offset; its own file stays the source."""
    if not path.exists():
        return
    src = json.loads(path.read_text())["elements"]
    ids = {e["id"]: f"s-{tag}-{e['id']}" for e in src}
    for e in src:
        if e.get("isDeleted"):
            continue
        c = json.loads(json.dumps(e))
        c.update(id=ids[e["id"]], x=e["x"] + dx, y=e["y"] + dy, version=1, frameId=None,
                 groupIds=[f"{tag}-{g}" for g in e.get("groupIds", [])])
        if c.get("containerId"):
            c["containerId"] = ids.get(c["containerId"])
        c["boundElements"] = [dict(b, id=ids.get(b["id"], b["id"])) for b in (e.get("boundElements") or [])]
        els.append(c)


def draw():
    # ── A · the ask and the ladder ──────────────────────────────────────────────────────
    text(0, 0, "Project -> Run: one ladder for every Theme?", 50)
    sticky(0, 80, 820, 96, "\"theme (cowork, papers, discoveries, insights, ...)\n -> blocks -> jobs -> tasks (task / page folders) -> runs\"\n   the ask, 261005: one complete contract + its checker", "ask", 19)
    y0, dy = 250, 112
    text(0, y0 - 40, "THE LADDER  ·  folder · must hold · owner · what it is for", 22, GRAY)
    for i, (lvl, folder, holds, owner, why) in enumerate(LEVELS):
        y = y0 + i * dy
        box(0, y, 160, 60, BLUE, "#e7f5ff")
        text(22, y + 14, lvl, 26, BLUE)
        text(190, y + 4, folder, 15, INK, MONO)
        text(520, y + 4, holds, 16, INK)
        text(800, y + 4, owner, 16, BLUE)
        text(800, y + 30, why, 15, GRAY)
        if i < len(LEVELS) - 1:
            arrow([(80, y + 62), (80, y + dy - 2)], BLUE)
    ay = y0 + len(LEVELS) * dy + 30
    text(0, ay, "A BLOCK, opened", 22, GRAY)
    b_bottom = mono(0, ay + 34, BLOCK_TREE, 15)
    text(0, b_bottom + 30, "A RUN, its receipt", 22, GRAY)
    r_bottom = mono(0, b_bottom + 64, RUN_TREE, 15)
    mark_line(0, b_bottom + 64, RUN_TREE[0], 15, 0, top=14)
    text(720, b_bottom + 70, "the one rule every\nTheme can share:\nticket, Result and\nreceipt agree on <run>", 19, RED)
    arrow([(715, b_bottom + 90), (0 + RUN_TREE[0].__len__() * 9 + 32, b_bottom + 86)], RED)
    text(0, r_bottom + 30, "SIX RUN DIALECTS  ·  haipipe-run, ticket -> result", 22, GRAY)
    d_bottom = mono(0, r_bottom + 64, [f"{a:<16}{b:<38}{c}" for a, b, c in DIALECTS], 14)
    a_bottom = d_bottom

    # ── B · Themes against levels, skills against levels ────────────────────────────────
    bx = 1300
    text(bx, 0, "THEMES x LEVELS  ·  as each Theme's own skill describes it", 28)
    hdr = f"{'Theme':<14}{'Block':<23}{'Job':<20}{'Task':<23}{'Run'}"
    lines = [hdr] + [f"{t:<14}{b:<23}{j:<20}{k:<23}{r}" for t, b, j, k, r in THEMES]
    t_top = 54
    t_bottom = mono(bx, t_top, lines, 16, title="red = bends the ladder · ? = not defined yet · - = skipped by rule")
    for i, (th, *_rest) in enumerate(THEMES):            # mark the rows that bend the ladder
        if th in ("insights/", "papers/", "designs/"):
            mark_line(bx, t_top, lines[i + 1], 16, i + 1)
    text(bx + 1190, t_top + 10, "these three bend it: the levels exist,\nunder other names, or not yet", 17, RED)
    row_y = lambda i: t_top + 34 + i * 16 * 1.3 + 10          # middle of table line i (0 = header)
    row_end = lambda i: bx + 18 + len(lines[i]) * 16 * 0.6 + 30
    ins, des = [k + 1 for k, r in enumerate(THEMES) if r[0] in ("insights/", "designs/")]
    text(bx + 1190, t_top + 110, "prototype will go to tasks/\ninsights block will be\nInsight-<Name>", 22, INK, MONO)
    arrow([(bx + 1180, t_top + 140), (row_end(ins), row_y(ins))], INK)
    text(bx + 1190, t_top + 240, "Design will be\nDesign-<Name>", 22, INK, MONO)
    arrow([(bx + 1180, t_top + 262), (row_end(des), row_y(des))], INK)
    text(bx + 1190, t_top + 330, "so Block names come in two families:\n  bNN_<topic>     tasks/ discoveries/ cowork/\n  <Kind>-<Name>   Paper- / Insight- / Design-", 16, GRAY)
    sy = t_bottom + 24
    for th, q in SAYS:
        text(bx, sy, f"{th}: {q}", 16, GRAY)
        sy += 28
    sticky(bx, sy + 14, 560, 100, "one table, Theme x level, kept as data:\nthe skills point to it, the checker reads it", "idea", 18)
    sticky(bx + 590, sy + 14, 560, 100, "or rename until every Theme\nuses bNN / jNN / tNN / rNN?", "open", 18)
    oy = sy + 160
    text(bx, oy, "SKILLS x LEVELS  ·  who owns what", 28)
    o_bottom = mono(bx, oy + 50, OWNERS, 16)
    mark_line(bx, oy + 50, OWNERS[-1], 16, len(OWNERS) - 1, top=14)
    text(bx + 820, o_bottom - 40, "the gap: no one checks below the root", 19, RED)
    b_bottom = o_bottom

    # ── C · content across Themes, the checker's layers ─────────────────────────────────
    cx = 2820
    text(cx, 0, "HOW CONTENT CROSSES THEMES", 28)
    nodes = {"external/": (cx, 80), "discoveries/": (cx + 400, 80), "tasks/": (cx + 400, 250),
             "cowork/": (cx, 250), "insights/": (cx + 750, 400), "papers/": (cx + 1100, 165),
             "designs/": (cx + 1100, 400)}
    for name, (x, y) in nodes.items():
        box(x, y, 250, 70, INK, "#ffffff")
        text(x + 24, y + 20, name, 22, INK, MONO)
    flows = [("external/", "discoveries/", "pinned source", False), ("discoveries/", "papers/", "bind Result id + hash", False),
             ("tasks/", "papers/", "bind Result id + hash", False), ("tasks/", "insights/", "? call Task Runs", True),
             ("insights/", "designs/", "signed handoff", False), ("cowork/", "tasks/", "? tickets, people", True)]
    for a, b, label, dashed in flows:
        (ax, ay2), (bx2, by2) = nodes[a], nodes[b]
        p1, p2 = (ax + 250, ay2 + 35), (bx2 - 4, by2 + 35)        # right edge -> left edge
        arrow([p1, p2], RED if dashed else GRAY, 2, dashed=dashed)
        text((p1[0] + p2[0]) / 2 - len(label) * 4, min(p1[1], p2[1]) - 22 if p1[1] != p2[1] else p1[1] - 26,
             label, 15, RED if dashed else INK)
    text(cx, 530, "solid = the skills say so · dashed red = open (Q04)", 16, GRAY)
    ky = 600
    text(cx, ky, "THE CHECKER, IN LAYERS  ·  cheap to deep", 28)
    for i, (layer, what, who) in enumerate(CHECKS):
        y = ky + 56 + i * 84
        kind = {"today": "fit", "new": "idea", "owner skill": "none"}[who]
        sticky(cx, y, 230, 64, layer, kind, 20)
        text(cx + 260, y + 10, what, 18, INK)
        text(cx + 260, y + 36, who, 15, GRAY)
    wy = ky + 56 + len(CHECKS) * 84 + 60
    text(cx, wy, "THE WORKBENCH ON THE LADDER  ·  Q07", 28)
    c_bottom = mono(cx, wy + 50, WORKBENCH, 16)

    # ── D · the Questions zone: each question, our ideas, the person's thoughts ─────────
    top = max(a_bottom, b_bottom, c_bottom) + 140
    W, QW, IW, TX = 4220, 560, 330, 2120
    fr = base("frame", 0, top, 10, 10, "#bbbbbb")       # an Excalidraw frame, not a drawn box
    fr["name"] = "Questions · ideas"
    FRAME[0] = fr["id"]
    text(30, top + 24, "questions from board.md · blue = an idea of ours · pink = your call · "
                       "write or draw anywhere on the canvas", 18, GRAY)
    y = top + 70
    for name, x in [("question", 30), ("ideas", QW + 70)]:
        text(x, y, name, 20, GRAY)
    y += 40
    right = 0
    for q in F.questions():
        body = f"{q['id']}  {q['title']}\n" + "\n".join(textwrap.wrap(q.get("question", ""), 50)[:8])
        qh = 50 + (body.count("\n") + 1) * 18 * 1.4
        sticky(30, y, QW, qh, body, "ask", 18)
        ih = 0
        for k, (kind, txt) in enumerate(IDEAS.get(q["id"], [])):
            h = 40 + (txt.count("\n") + 1) * 17 * 1.35
            sticky(QW + 70 + k * (IW + 20), y, IW, h, txt, kind, 17)
            ih = max(ih, h)
            right = max(right, QW + 70 + (k + 1) * (IW + 20))
        rh = max(qh, ih, 150)
        y += rh + 30
    fr["width"], fr["height"] = right + 30, y - top + 10
    FRAME[0] = None

    # ── E · the ladder grid from the v2 session, copied in on every rebuild ─────────────
    gx = W + 200
    text(gx, -60, "from studio/ladder-grid.excalidraw (session v2): edit it there, it is copied here on rebuild", 18, GRAY)
    include(F.BLOCK / "studio/ladder-grid.excalidraw", gx, 0, "lg")


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else F.BLOCK / "studio/project-scratch.excalidraw"
    draw()
    canvas.write(out, els, "build_project_scratch.py")


if __name__ == "__main__":
    main()
