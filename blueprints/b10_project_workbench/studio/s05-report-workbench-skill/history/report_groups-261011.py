"""s07 · Report groups across the themes: s07-report-groups-across-themes.excalidraw (haipipe-studio).

One dense frame, the same shape as s03 and s04: today every Block shows the paper's four Report buttons;
proposed, the Report gets the Studio's group bar, its names from the theme (starting groups) and the
Block (+ Group), a Question's group its register `group:` line; the table across the seven themes; and
b10's own 12 Questions grouped. New on 261011 (JL: "I asked you to have the report groups across the
themes ... Please add it as the s07"). Then the "In Tools" frame, as s02 to s06 draw it.

Read from disk on every build: frame.py's AUDIENCE_VIEWS and WHO_ASKS, b10's board.md register (ids and
titles), each report's answer-status, and studio/_groups.txt. The proposal itself (the starting groups,
b10's mapping) is typed: it is what s07 proposes, not what the disk holds yet.

A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside the drawing).

    python build_s07_report_groups_across_themes.py
"""
import ast
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]                                   # b10_project_workbench
sys.path.insert(0, str(HERE.parent / "s01-overall-tree-structure"))
sys.path.insert(0, str(HERE.parent / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers)
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)

INK, RED, MONO = L.INK, L.RED, L.MONO
text, path, base = L.text, L.path, L.base
FRAME_PY = L.TOOLKIT / "servers/workbench/frame.py"

# the proposal (s07-D03): theme, its groups on the bar, what stays a row above the list; guessed rows red.
# Paper and insight revised 261011 from their real Reports (JL: "think about what is the current things looks like")
THEMES = [
    ("work", "Data · Pilot · Evaluation", "Task: Draft · Report", False),
    ("discovery", "Known · Closest · Gap", "Questions · Reports", True),
    ("cowork", "Needs · Works · Blockers", "", False),
    ("paper", "Ideation · Narrative · Research questions · Random thoughts", "Related Papers; version parts", False),
    ("insight", "Data · Information · Knowledge · Wisdom (fixed) + subjects", "partitions · readings", False),
    ("design", "Goal · Rules · Ranking", "Elements · Evaluation", True),
    ("labeling", "Guideline · Agreement · Models", "", True),
    ("every one", "Random thoughts", "", False),
]
# b10's 12 Questions in its existing Studio groups (s07-D07); Q11 is open (Guide or UI)
B10_GROUPS = {"Q01": "Levels", "Q02": "Levels", "Q03": "Report", "Q04": "Structure", "Q05": "Run and Skill",
              "Q06": "Run and Skill", "Q07": "UI", "Q08": "UI", "Q09": "UI", "Q10": "Guide", "Q11": "Guide",
              "Q12": "Server"}
OPEN = [
    "? share the names (s07-D04, recommended), or one list for Studio and Report",
    "? Q11, how a Page's logic is drawn: Guide or UI",
    "? discovery, design, labeling: learn their kinds on one real Block each",
    "? \"Random thoughts\" in every theme, or the theme's word (paper: Reviewers)",
    "? each theme Block (b11 to b17) owns its own list; b10 keeps the rule (paper: yes)",
]


def card(x, y, w, h, title, body="", size=23, body_size=20, body_color=INK):
    base("rectangle", x, y, w, h, INK, 1.5)
    text(x + 22, y + 16, title, size)
    if body:
        text(x + 22, y + 16 + size * 1.25 + 14, body, body_size, body_color)


def code_tuple(name):
    """A tuple of strings assigned at the top of frame.py (`NAME = ("a", "b")`), read, never typed."""
    hit = re.search(rf"^{name}\s*=\s*\(([^)]*)\)", FRAME_PY.read_text(encoding="utf-8"), re.M)
    return re.findall(r'"([^"]+)"', hit.group(1)) if hit else []


def register():
    """b10's Questions from board.md's ## Questions yaml: id, title, the report's answer-status."""
    text_ = (BLOCK / "board.md").read_text(encoding="utf-8")
    block = re.search(r"(?ms)^## Questions\s*\n.*?```ya?ml\n(.*?)```", text_).group(1)
    rows = []
    for q in yaml.safe_load(block)["questions"]:
        report = BLOCK / (q.get("report") or "")
        state = "open"
        if report.is_file():
            hit = re.search(r"(?m)^answer-status:\s*(\w+)", report.read_text(encoding="utf-8"))
            state = hit.group(1) if hit else "open"
        rows.append((q["id"], q["title"], state))
        if q.get("group"):                               # built 261011: the register now holds the groups
            B10_GROUPS[q["id"]] = str(q["group"]).split(",")[0].strip()
    return rows


def short(s, most=40):
    return s if len(s) <= most else s[:most - 1].rstrip() + "…"


def report_groups(x0):
    """The one frame: today's buttons, the proposed bar, where names come from, across themes, b10."""
    qs = register()
    text(x0, 0, "Across the themes: where a Report's groups come from", 34)
    text(x0, 52, "The screens above, as rules: the four sources of a group's name, each theme's groups, by level, "
                 "and b10's 12 Questions.", 21)

    order = [g for g in L_order() if g in set(B10_GROUPS.values())]
    # ── where the names come from ──
    text(x0, 130, "Where a group's name comes from", 25)
    sources = [("FIXED", "from the Question\ninsight: D · I · K · W"),
               ("THEME", "starting groups\nTheme.report_groups"),
               ("BLOCK", "+ Group, its subjects\nreports/_groups.txt"),
               ("QUESTION", "its group: line\ndrag a row to set it")]
    for i, (title, body) in enumerate(sources):
        x = x0 + i * 290
        card(x, 180, 280, 130, title, body)
        path([(x + 140, 318), (x0 + 575, 378)])
    note(x0 + 120, 196, "added (JL)")
    card(x0, 386, 1150, 110, "THE REPORT BAR  Current · groups · Untagged · + Group",
         "the Studio's code (frame.group_list), a third kind beside studio and related")
    text(x0, 516, "the Studio shares the names, not the list: pick UI there, UI stays picked here (s07-D04)", 20)

    # ── across the themes ──
    xr = x0 + 1270
    text(xr, 130, "Across the themes (s07-D03, D05)", 25)
    note(xr + 470, 137, "paper, insight: read from their Reports (JL)")
    cols = (0, 150, 820)
    for c, head in zip(cols, ("theme", "groups on the bar", "stays a row above the list")):
        text(xr + c, 180, head, 20)
    path([(xr, 212), (xr + 1240, 212)], arrow=False, color=INK)
    for i, (theme, groups, keep, guessed) in enumerate(THEMES):
        y = 226 + i * 36
        text(xr + cols[0], y, theme, 20)
        text(xr + cols[1], y, groups + ("  ?" if guessed else ""), 20, RED if guessed else INK)
        text(xr + cols[2], y, keep, 20)
    text(xr, 226 + len(THEMES) * 36 + 10, "red: guessed, no register on disk · a lens (a cut, a reading, a part) "
                                           "stays a row (s07-D05)", 20)

    # ── by level ──
    y = 590
    text(xr, y, "By level (s07-D06)", 25)
    for i, line in enumerate(["Block   its own register, the bar",
                              "Job     the Block's Questions it answers (answers: Q05), same groups",
                              "Task    its own result: no Questions, no bar (s09-D02)"]):
        text(xr, y + 46 + i * 32, line, 20, INK, MONO)

    # ── b10's 12 Questions, grouped (titles read from board.md) ──
    y = 760
    text(xr, y, "b10's 12 Questions in its Studio groups (s07-D07)", 25)
    title_of = {qid: t for qid, t, _ in qs}
    for i, g in enumerate(order):
        ids = [q for q, v in B10_GROUPS.items() if v == g]
        text(xr, y + 46 + i * 32, g, 20)
        text(xr + 190, y + 46 + i * 32, " · ".join(f"{q} {short(title_of.get(q, ''), 24)}" for q in ids), 20)
    yo = y + 46 + len(order) * 32 + 30
    for i, q in enumerate(OPEN):
        text(xr, yo + i * 32, q, 20, RED)
    e = canvas.change_note(xr + 720, yo + 3, "watcher agrees: names, not one list", "261011", L.FRAME[0], 17)
    e["id"] = f"v{len(L.els)}"
    L.els.append(e)
    note(xr + 760, yo + 4 * 32 + 3, "b16 s05-D02: the paper keeps its own words")


# ── the paper and insight Reports as they are today, read off the real Boards (JL 261011) ──────────
SPACE = next((p for p in (L.TOOLKIT.parents[2] / "WellDoc-SPACE", L.TOOLKIT.parents[1].parent)
              if (p / "examples-2-nn").is_dir()), None)           # the SPACE beside Tools, relative to this file
PAPER = "examples-2-nn/Proj11-CGM-FM/paper/Paper-ScalingGlucose-NatSeries2026"
OLD_PAPERS = ("examples-2-nn/Proj32-CGM-Event-FixLenVec/paper/Paper-AnchorPK-ML4H2026",
              "examples-1-data/ProjB-Bench-1-FairGlucose/paper/Paper-FairGlucose-preprint")
INSIGHT = "examples-5-design/ProjI-Insight-1-Wearable"
PAPER_PY = L.TOOLKIT / "servers/workbench-paper/paper_theme.py"
VIEWS_PY = L.TOOLKIT / "servers/workbench-insight/insight_views.py"
SUBJECTS = (("sleep", "Sleep"), ("walk", "Walking"), ("stress", "Stress and heart"), ("event", "Events"),
            ("glucose-control", "Glucose control"), ("glucose-by-hour", "Glucose control"),
            ("control-and-timing", "Glucose control"))      # a subject read off each Task's name (s07 finding 5)


def names_in(path, name):
    """A tuple assigned at the top of a module (`NAME = (...)`), read by Python's own parser, never typed:
    its strings, or each inner tuple's first string."""
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == name for t in node.targets):
            return [v[0] if isinstance(v, tuple) else v for v in ast.literal_eval(node.value)]
    return []


def register_of(board):
    hit = re.search(r"(?ms)^## Questions\s*\n.*?```ya?ml\n(.*?)```", (board / "board.md").read_text(encoding="utf-8"))
    return (yaml.safe_load(hit.group(1)) or {}).get("questions") or [] if hit else []


def paper_facts():
    b = SPACE / PAPER
    regs = register_of(b)
    ideas = {m for f in (b / "studio").glob("s*-ideation/*.md") for m in re.findall(r"IDEA-\d\d", f.read_text(encoding="utf-8"))}
    rqs = {m for f in (b / "studio").glob("s*-story-*/*.md") for m in re.findall(r"\bRQ\d+\b", f.read_text(encoding="utf-8"))}
    groups = sorted({str(q.get("group") or "") for q in regs})
    olds = [(Path(o).name, len(register_of(SPACE / o))) for o in OLD_PAPERS if (SPACE / o / "board.md").is_file()]
    return {"name": b.name, "register": len(regs), "groups": groups, "ideas": len(ideas), "rqs": len(rqs),
            "views": names_in(PAPER_PY, "AUDIENCE"), "version": names_in(PAPER_PY, "VERSION_AR"),
            "attract": names_in(PAPER_PY, "ATTRACT"), "standing": names_in(PAPER_PY, "STANDING"), "olds": olds}


def insight_facts():
    proto = sorted((SPACE / INSIGHT / "work").glob("Prototype-*/j*_p*"))[-1]
    qs = yaml.safe_load((proto / "release.yaml").read_text(encoding="utf-8"))["questions"]
    parts = yaml.safe_load((proto / "partitions.md").read_text(encoding="utf-8").split("---")[1])["partitions"]
    by_level = {lv: [q for q in qs if q.startswith(lv)] for lv in "DIKW"}
    subjects = {}
    for q, v in qs.items():
        slug = v["task"].rsplit("/", 1)[-1]
        name = next((n for k, n in SUBJECTS if k in slug), "")
        if name:
            subjects.setdefault(name, []).append(q)
    board = next((SPACE / INSIGHT / "insight").glob("Insight-*"))
    return {"board": board.name, "release": proto.name, "levels": by_level, "parts": [p["name"] for p in parts],
            "readings": names_in(VIEWS_PY, "READINGS"), "periods": names_in(VIEWS_PY, "PERIODS"),
            "subjects": subjects, "register": len(register_of(board))}


def today_frame():
    """Paper and insight, as their Reports are today, and what each part becomes (s07-D02, D03, D05, D08)."""
    fr = L.open_frame("Paper and insight Reports today")
    text(0, 0, "Paper and insight: what their Reports show today, and what each part becomes", 34)
    text(0, 52, "Read from paper_theme.py, insight_views.py and the real Boards. A group goes on the bar; a lens "
                "stays a row above the list (s07-D05).", 21)
    note(0, 88, "new: read before designing (JL)")
    if SPACE is None:
        text(0, 140, "? the WellDoc SPACE is not beside Tools on this computer: nothing to read", 21, RED)
        L.close_frame(fr)
        return fr
    p, n = paper_facts(), insight_facts()
    # ── paper ──
    text(0, 140, f"PAPER  {p['name']}", 25)
    text(0, 184, "Board, today's buttons", 20, INK, MONO)
    text(380, 184, "what each reads", 20, INK, MONO)
    text(990, 184, "becomes", 20, INK, MONO)
    reads = {"Ideation": (f"{p['ideas']} ideas and their verdicts + group: ideation", "group  Ideation"),
             "Narrative": (f"{len(p['attract'])} standing: will it attract the " + " · ".join(p["attract"]),
                           "group  Narrative"),
             "High-level logic + Low-level work": (f"the Story's {p['rqs']} research questions = Q00..Q{p['rqs'] - 1:02d}",
                                                   "group  Research questions"),   # its Feeds:, by id (b16 s05-D01)
             "Related Questions": (f"0 here: all {p['register']} in one group, " + ", ".join(p["groups"]),
                                   "group  Random thoughts"),
             "Related Papers": ("the Story's paper table (no related/ yet)", "lens   stays a row")}
    for i, v in enumerate(p["views"]):
        what, becomes = reads.get(v, ("", ""))
        y = 222 + i * 40
        text(0, y, short(v, 30), 20, INK, MONO)
        text(380, y + 1, what, 20, RED if what.startswith("0 here") else INK)
        text(990, y + 1, becomes, 20, INK, MONO)
    y = 222 + len(p["views"]) * 40 + 20
    card(0, y, 1240, 96, f"PROPOSED  Current · Ideation {p['ideas']} · Narrative {len(p['attract'])} · "
                         f"Research questions {p['rqs']} · Random thoughts 0 · + Group",
         "and one row above the list: Related Papers (it reads related/, not Questions)", 21, 20)
    y += 130
    text(0, y, "Version Job: " + " · ".join(p["version"]), 20)
    text(0, y + 34, "  the parts of the manuscript: lenses, they stay; its Questions view holds the standing", 20)
    text(0, y + 64, "  " + " · ".join(p["standing"]) + " (s07-D08)", 20, INK, MONO)
    text(0, y + 104, "Section Task: Table · Reading · Questions · Comments, lenses, no bar", 20)
    text(0, y + 144, "older Boards: " + " · ".join(f"{nm.split('-')[1]} {k}" for nm, k in p["olds"]) +
         " register Questions: only ideas, claims, rounds", 20, RED)
    # ── insight ──
    xi = 1340
    text(xi, 140, f"INSIGHT  {n['board']} (plan C), release {n['release'].split('_')[1]}", 25)
    rows = [("row 2", " · ".join(n["parts"]), "lens   one cut at a time"),
            ("row 3", " · ".join(n["readings"]), "lens   other columns"),
            ("body", " · ".join(f"{lv} {len(q)}" for lv, q in n["levels"].items()) + " folds, by the id's letter",
             "fixed  groups D · I · K · W"),
            ("Job", "partitions, then " + " · ".join(n["periods"]), "lens   stays"),
            ("Task", "Table · Reading", "lens   no bar")]
    for i, (where, what, becomes) in enumerate(rows):
        y = 184 + i * 40
        text(xi, y, where, 20, INK, MONO)
        text(xi + 90, y + 1, what, 20)
        text(xi + 760, y + 1, becomes, 20, INK, MONO)
    levels = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
    bar = ("Current · " + " · ".join(f"{levels[lv]} {len(q)}" for lv, q in n["levels"].items()) + " ·\n"
           + " · ".join(f"{s} {len(q)}" for s, q in n["subjects"].items()) + " · + Group")
    card(xi, 400, 1200, 130, "PROPOSED  fixed levels, then subjects added", bar, 23, 20)
    text(xi, 556, "its subjects cut across the levels (read off each Task's name):", 20)
    for i, (s_, q) in enumerate(n["subjects"].items()):
        text(xi + 24, 592 + i * 30, f"{s_:<17} {' · '.join(q)}", 20, INK, MONO)
    yq = 592 + len(n["subjects"]) * 30 + 20
    text(xi, yq, f"its board.md register holds {n['register']} Questions: they live in the Prototype's release.yaml", 20)
    text(xi, yq + 32, "? a subject's group: line goes in each question.md (s07 Open 7)", 20, RED)
    # ── the rule ──
    yr = max(y + 200, yq + 100)
    text(0, yr, "The rule (s07-D05): what a Report's second and third rows hold today", 25)
    for i, (kind, what, where) in enumerate([
            ("group", "gathers rows into one list: Related Questions, Ideation, Narrative", "on the bar"),
            ("fixed", "comes from the Question itself: insight's level letter", "a fixed group, no ×"),
            ("lens", "the same Questions another way, or another part: cuts, readings, Draft-Main",
             "stays a row")]):
        text(0, yr + 46 + i * 32, f"{kind:<6} {what}", 20, INK, MONO)
        text(1070, yr + 47 + i * 32, "→ " + where, 20)
    L.close_frame(fr)
    return fr


# ── the UI, the most salient part (JL 261011: "make the UI to be the most salient part ... when I see it in
# the highlevel, I cannot get the main point"): the Report screen today and proposed, for b10, a paper, an insight
TOP = {"b10": "Guide · Studio  |  Block · Job ▾ · Task ▾  |  Delivery",
       "paper": "Guide · Studio  |  Paper Board · Version ▾ · Section ▾  |  Delivery",
       "insight": "Guide · Studio  |  Insight Board · Job ▾ · Task ▾  |  Delivery"}
MARKS = [("①", "the group bar: the Studio's and Related's own code (s07-D01)"),
         ("②", "fixed groups come from the Question itself, no × (s07-D02)"),
         ("③", "a view that reads differently stays a row above the bar (s07-D05)"),
         ("④", "+ Group adds the Block's own subjects (s07-D02)"),
         ("⑤", "a standing Question sits in its group (s07-D08)")]


def button(x, y, label, size=20, kind="", h=None):
    """A button sized to its words; kind: on (selected), picked, fixed (a double line), new (dashed), red."""
    w, h = len(label) * size * 0.56 + 28, h or size + 20
    color = RED if kind == "red" else INK
    base("rectangle", x, y, w, h, color, 3.5 if kind in ("on", "picked") else 1.5, dashed=kind == "new", rough=0)
    if kind == "fixed":
        base("rectangle", x + 4, y + 4, w - 8, h - 8, INK, 1, rough=0)
    text(x + 14, y + (h - size * 1.25) / 2, label, size, color)
    return x + w


def mark(x, y, n):
    text(x, y, n, 30)


def screen(x, y, w, top, bar, views=(), state="", rows=(), today=False, work=True):
    """One workbench screen with the Report open: its top row, its work row, the rows that stay above (views),
    the group bar drawn largest (bar: lines of (label, kind)), then Question │ Work │ Report rows. Returns where
    each bar line and view row ends, for the numbered marks."""
    at = {"views": [], "bar": []}
    text(x + 24, y + 18, top, 20)
    bx = x + 24
    for lab in ("Description", "Report", "Work", "Runs") if work else ():    # the Studio hides the work row
        bx = button(bx, y + 56, lab, 20, "on" if lab == "Report" else "") + 12
    yy = y + (118 if work else 60)
    for name, items in views:
        text(x + 24, yy + 8, name, 20)
        bx = x + 24 + len(name) * 11 + 16
        for lab, kind in items:
            bx = button(bx, yy, lab, 20, kind) + 8
        at["views"].append((bx, yy))
        yy += 54
    for line in bar:
        bx = x + 24
        for lab, kind in line:
            bx = button(bx, yy, lab, 20 if today else 23, kind, 42 if today else 50) + 10
            if kind == "fixed":
                at.setdefault("fixed", (bx, yy))
        at["bar"].append((bx, yy))
        yy += 54 if today else 64
    if state:
        text(x + 24, yy + 4, state, 20)
        yy += 44
    for left, work, right, standing in rows:
        base("rectangle", x + 24, yy, w - 48, 62, INK, 1, rough=0)
        text(x + 40, yy + 18, left, 20)
        text(x + 24 + (w - 48) * 0.50, yy + 18, work, 20)
        text(x + 24 + (w - 48) * 0.72, yy + 18, right, 20)
        if standing:
            at["standing"] = (x + w - 20, yy + 10)
        yy += 72
    base("rectangle", x, y, w, yy - y + 10, INK, 2, rough=0)
    return at


def paper_rows():
    """The paper screen's three rows, read off the Board: its first idea and its verdict, one standing
    Narrative Question, its first research question."""
    b = SPACE / PAPER
    idea = re.search(r"(?m)^(IDEA-\d\d)\s+(.+?)\s{2,}\S*\s*([A-Z]+)",
                     (b / "studio/s01-ideation/s01-ideation.md").read_text(encoding="utf-8"))
    regs = register_of(b)
    rq = next((q for q in regs if q["id"] == "Q01"), regs[0] if regs else {"id": "Q01", "title": "?"})
    who = names_in(PAPER_PY, "ATTRACT")
    return [(f"{idea.group(1)}  {short(idea.group(2), 30)}", "how it was tested",
             idea.group(3).lower() + "   [Ideation]", False),
            (f"Will it attract the {who[1] if len(who) > 1 else 'reviewer'}?", "the Story's Evidence",
             "not judged   [Narrative]", True),
            (f"{rq['id']}  {short(rq['title'], 30)}", "Task Roadmap work", "open   [Research questions]", False)]


def ui_frame():
    """The first frame, the largest: the Report screen, today and proposed (s07-D01 to D08)."""
    fr = L.open_frame("The Report, with its groups: today and proposed")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    text(0, 0, "The Report gets the Studio's group bar: the theme brings its groups, the Block adds its own", 40)
    text(0, 62, "Today every theme shows the paper's four buttons. Proposed, for b10, a paper Board and an insight "
                "Board, read from their files (s07-D01 to D08).", 22)
    note(0, 104, "the screens first, the main point at a glance (JL)")
    qs = register()
    views, title_of = code_tuple("AUDIENCE_VIEWS"), {q: t for q, t, _ in qs}
    counts = {st: sum(1 for *_, s_ in qs if s_ == st) for st in ("answered", "partial", "open")}
    # ── b10 today ──
    text(0, 150, "TODAY  b10's Report: the paper's four buttons, on every theme", 25)
    screen(0, 196, 780, TOP["b10"], [[(v, "red") for v in views[:2]], [(v, "") for v in views[2:4]]],
           rows=[("Question 1", "no work yet", "", False), (short(title_of.get("Q01", ""), 30), "", "", False)],
           today=True)
    text(0, 616, "red: these two list studio topics, not Questions", 21, RED)
    path([(800, 420), (880, 420)], color=INK)
    L.els[-1]["strokeWidth"] = 4
    # ── b10 proposed ──
    order = [g for g in L_order() if g in set(B10_GROUPS.values())]
    sizes = {g: sum(1 for v in B10_GROUPS.values() if v == g) for g in order}
    text(900, 150, "BUILT  b10, live: its Studio's groups on one bar (s07-D07, D09)", 25)
    note(1640, 156, "built and live on b10 (JL)")
    bar = [[("Current 0", "")] + [(f"{g} {sizes[g]}", "") for g in order] + [("+ Group", "new")]]   # as live
    rows = [(f"{q}  {short(t, 34)}", "its Jobs and Runs", f"{st}   [{B10_GROUPS.get(q, '')}]", False)
            for q, t, st in qs if st != "open"][:3]
    at = screen(900, 196, 1660, TOP["b10"], bar, rows=rows,
                state=f"answered {counts['answered']} · partial {counts['partial']} · open {counts['open']}")
    mark(at["bar"][0][0] + 4, at["bar"][0][1] + 4, "①")
    # ── paper proposed ──
    p = paper_facts()
    y2 = 680
    text(0, y2, "PROPOSED  a paper Board: its own four kinds stay (s07-D03, b16 s05-D01)", 25)
    pbar = [[("Current 0", ""), (f"Ideation {p['ideas']}", ""), (f"Narrative {len(p['attract'])}", ""),
             (f"Research questions {p['rqs']}", ""), ("Random thoughts 0", ""), ("+ Group", "new")]]
    at = screen(0, y2 + 46, 1240, TOP["paper"], pbar, views=[("view", [("Questions", "on"), ("Related Papers", "")])],
                rows=paper_rows())
    mark(at["views"][0][0] + 6, at["views"][0][1] + 2, "③")
    mark(at["bar"][0][0] + 2, at["bar"][0][1] + 4, "④")
    mark(at["standing"][0] - 34, at["standing"][1] - 4, "⑤")
    # ── insight proposed, Sleep picked ──
    n = insight_facts()
    levels = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
    ibar = [[("Current 0", "")] + [(f"{levels[lv]} {len(q)}", "fixed") for lv, q in n["levels"].items()]
            + [("Random thoughts 0", "")],
            [(f"{s_} {len(q)}", "picked" if s_ == "Sleep" else "") for s_, q in n["subjects"].items()]
            + [("+ Group", "new")]]
    rel = next((SPACE / INSIGHT / "work").glob("Prototype-*/" + n["release"])) / "release.yaml"
    slugs = yaml.safe_load(rel.read_text(encoding="utf-8"))["questions"]
    irows = [(f"{q}  " + slugs[q]["task"].rsplit("/", 1)[-1].split("_", 2)[-1].replace("-", " "),
              "the runs on this cut", f"[{levels[q[0]]} · Sleep]", False) for q in n["subjects"].get("Sleep", [])]
    text(1320, y2, "PROPOSED  an insight Board: fixed levels, subjects added, Sleep picked", 25)
    at = screen(1320, y2 + 46, 1240, TOP["insight"], ibar,
                views=[("cut", [(c, "on" if c == "full" else "") for c in n["parts"]]),
                       ("reading", [(r, "on" if r == "Findings" else "") for r in n["readings"]])], rows=irows)
    mark(at["bar"][0][0] + 4, at["bar"][0][1] + 4, "②")
    mark(at["views"][1][0] + 6, at["views"][1][1] + 2, "③")
    mark(at["bar"][1][0] + 4, at["bar"][1][1] + 4, "④")
    # ── the marks, in words ──
    yl = max(e["y"] + e["height"] for e in L.els if e.get("frameId") == fr["id"]) + 26
    for i, (n_, words) in enumerate(MARKS):
        text((i % 3) * 860, yl + (i // 3) * 44, f"{n_}  {words}", 21)
    L.close_frame(fr)
    return fr


def note(x, y, what):
    e = canvas.change_note(x, y, what, "261011", L.FRAME[0], 17)
    e["id"] = f"v{len(L.els)}"
    L.els.append(e)


def L_order():
    """b10's Studio group order, studio/_groups.txt."""
    f = BLOCK / "studio" / "_groups.txt"
    return [ln.strip() for ln in f.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")] if f.is_file() else []


def main():
    out = HERE / "s07-report-groups-across-themes.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    ui = ui_frame()
    fr = L.open_frame("Across the themes: where groups come from")
    report_groups(0)
    L.close_frame(fr)
    today = today_frame()
    tools = L.tools_frame(
        "In Tools: haipipe-report", ["1_base/project/haipipe-report/", "1_base/project/haipipe-report"],
        [("servers/workbench/frame.py", ["question_rows", "group_list", "studio_group_op", "_group_members"])],
        around=["each theme's Report row: servers/workbench-<theme>/<theme>_theme.py",
                "haipipe-studio: the group bar's first home (s02)", "haipipe-related: its own groups (s04)",
                "b16 s05-paper-report: the paper's own list"])
    canvas.grid(L.els, [[ui["id"]], [fr["id"], today["id"]], [tools["id"]]])
    for e in canvas.off_palette(L.els):                  # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, list(L.els), "build_s07_report_groups_across_themes.py")


if __name__ == "__main__":
    main()
