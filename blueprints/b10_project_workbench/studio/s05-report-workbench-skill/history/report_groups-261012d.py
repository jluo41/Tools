"""s07 · Report groups across the themes: s07-report-groups-across-themes.excalidraw (haipipe-studio).

The first frame, the screens, redrawn 261012 (JL: "for each theme and the base, you should show how the report'
groups looks like"): the base and every theme's Report today, read live through frame.render, beside the proposal,
in the workbench's own colours, with red boxes and → notes for what is not built or guessed (s07-D12). Below it,
as on 261011, one dense frame, the same shape as s03 and s04: today every Block shows the paper's four Report buttons;
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
import html as H
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


# ── the UI, the most salient part (JL 261011: "make the UI to be the most salient part"; 261012: "for each theme
# and the base, you should show how the report' groups looks like"): one row per theme, the Report read live
# through frame.render on the left, the proposal on the right
SCREENS = [   # (theme, where, the Block or Job read live): "tools" is this Tools repo, "space" a SPACE beside it
    ("base", "tools", "blueprints/b10_project_workbench"),
    ("work", "space", "examples-2-lm/Proj11-CGM-Corpus/work/b02_pretrain_corpus"),
    ("cowork", "space", "examples-0-cowork/Project-Samsung/cowork/b12_epic_streaming"),
    ("paper", "space", PAPER),
    ("insight", "space", "examples-5-design/Project-Application-SMSDesign/insight/Insight-SMSR2v1/"
                         "j01_prototype-p1-basic-questions_data-SMSR2v1"),
    ("design", "space", "examples-5-design/ProjI-Insight-1-Wearable/design/Design-PreVisitChecklist"),
    ("discovery", "space", "examples-2-nn/Proj11-CGM-FM/discovery/b01_scaling_law_literature"),
    ("labeling", "space", "examples-6-labeling/Project-Labeling-ClinicalDialogue/labeling/b01_aci_bench"),
]
# the proposal per theme (s07-D03, D05, D10): starting groups (red when guessed), what stays a row above the list,
# and how the list reads; every theme also starts with Random thoughts (s07-D02)
PROPOSED = {
    "base": ([], False, "one card per Question (built)"),
    "work": (["Data", "Pilot", "Evaluation"], False, "one card per Question; a Task keeps Draft · Report"),
    "cowork": (["Needs", "Works", "Blockers"], False, "one card per Question; Timeline stays a row when a report has events"),
    "paper": (["Ideation", "Narrative", "Research questions"], False,
              "its ideas and standing Questions as cards too (b16 s05-D01)"),
    "insight": ([], False, "Data · Information · Knowledge · Wisdom stay the folds, counted for the topic picked"),
    "design": (["Goal", "Rules", "Ranking"], True, "a design Block; its Job keeps Elements · Evaluation"),
    "discovery": (["Known", "Closest", "Gap"], True, "Questions · Reports stays a row above"),
    "labeling": (["Guideline", "Agreement", "Models"], True, "one card per Question"),
}
# insight topics across D · I · K · W (JL 261012: "besides the period, we can also have the topics: with different
# topics across D I K W"), read off each Task's name; the first word that matches wins. A guess until agreed.
TOPIC_WORDS = (("demographic", "Demographics"), ("segmentation", "Demographics"), ("temporal", "Timing"),
               ("timing", "Timing"), ("sequential", "Timing"), ("medical", "Medical context"),
               ("medication", "Medical context"), ("geograph", "Place and income"), ("neighbourhood", "Place and income"),
               ("area", "Place and income"), ("cultural", "Place and income"), ("linguistic", "Wording"),
               ("sender", "Sender"), ("trust", "Sender"), ("prior", "Prior messages"), ("funnel", "Funnel"),
               ("partition", "Partitions"), ("pooling", "Partitions"), ("shape", "Data quality"),
               ("balance", "Data quality"), ("thin", "Data quality"), ("psycholog", "Behaviour"),
               ("behavio", "Behaviour"), ("contextual", "Behaviour"), ("variant", "Variants"),
               ("strategy", "Variants"), ("slate", "Variants"), ("optimization", "Variants"),
               ("personalization", "Variants"))


# what the red mark beside a proposed bar says, while the theme does not show it yet (JL 261012: "use the red box to
# circle them and give --> text to explain them")
NOT_YET = {"paper": "not built: the paper draws its own five buttons; b16 owns its list (b16 s05-D02)",
           "insight": "proposed (s07-D10): topic names guessed from the Task names",
           "design": "guessed names: learn them on one real design Block (Open 3)",
           "discovery": "guessed names: learn them on one real discovery Block (Open 3)",
           "labeling": "guessed names: learn them on one real labeling Block (Open 3)"}


def starting_of(theme):
    return list(PROPOSED[theme][0])


def spaces_beside():
    """The SPACEs beside this Tools repo: sibling folders whose Tools/ link leads here."""
    tools = L.TOOLKIT.parents[1].resolve()
    out = []
    for d in sorted(tools.parent.iterdir()):
        try:
            if d != tools and (d / "Tools").resolve() == tools:
                out.append(d)
        except OSError:
            continue
    return out


def locate(where, rel_path):
    """(root, folder) for a SCREENS row, or (None, None) when no SPACE beside Tools holds it."""
    if where == "tools":
        return L.TOOLKIT.parents[1], L.TOOLKIT.parents[1] / rel_path
    for s in spaces_beside():
        if (s / rel_path).is_dir():
            return s, s / rel_path
    return None, None


def frame_module():
    sys.path.insert(0, str(L.TOOLKIT / "servers" / "_host"))
    from host_paths import bootstrap
    bootstrap()
    from live import frame
    return frame


def clean(s):
    s = H.unescape(re.sub(r"<[^>]+>", " ", s))
    s = re.sub(r"[\U0001F000-\U0001FFFF☀-➿]️?", "", s)      # emoji: the drawing's font has none
    return re.sub(r"\s+", " ", s).strip()


def read_report(frame, root, folder):
    """What the Report shows today, top to bottom: the rows of buttons above the list (label, [(name, on)]), the
    group bar [(name, count)] when it has one, and one line saying how the list reads."""
    theme = frame.themes().get(frame.theme_of(folder, root), frame.VANILLA)
    page = re.sub(r"<script.*?</script>|<style.*?</style>", "", frame.render(theme, root, folder, "Audience Report"),
                  flags=re.S)
    head, _, main = page.split('class="frame-body', 1)[-1].partition("<div class=space-main>")
    main = main.split("<section class=runs-panel", 1)[0]
    rows = []
    for part in (head, main):
        for nav in re.findall(r'<nav class="row subs[^"]*">(.*?)</nav>', part, re.S):
            label = re.search(r"<span class=mut[^>]*>(.*?)</span>", nav, re.S)
            rows.append((clean(label.group(1)).rstrip(":") if label else "",
                         [(clean(t), "tab on" in a) for a, t in re.findall(r"<a ([^>]*)>(.*?)</a>", nav, re.S)]))
    bar = []
    if "data-group-kind=reports" in main:
        bar = [(clean(n), int(c), "fixed" if "grp-fixed" in k else "suggested" if "grp-suggested" in k else "")
               for k, n, c in re.findall(r'class="([^"]*)"[^>]*?data-studio-label="([^"]*)"[^>]*>'
                                         r'(?:<span[^>]*>[^<]*</span>)?[^<]*<span class=tag-count>(\d+)', main)]
    cards = main.count('class="topic q-card')
    folds = (re.findall(r"<summary><b>([^<]*)</b> <span class=topic-meta>(\d+)</span>", main)
             if "<div class=dikw>" in main else [])          # insight: one fold per level, D · I · K · W
    old = len(re.findall(r"""<div class=["']?q-row(?: id=["']?question-[^>]*)?["']?>""", main))   # the row list, not its head
    tables = len(re.findall(r"<tr[^>]*>\s*<td", main))
    empty = re.search(r"<p class=(?:mut|space-empty)>(.*?)</p>", main, re.S)
    if cards:
        listing = f"{cards} Question cards"
    elif folds:
        listing = "folds: " + " · ".join(f"{n.split()[0]} {c}" for n, c in folds)
    elif old:
        listing = f"{old} rows, Question │ Work │ Report: no bar"
    elif tables:
        listing = f"a table of {tables} rows: no bar"
    else:
        listing = clean(empty.group(1)) if empty else "nothing"
    return {"theme": theme.name, "rows": rows, "bar": bar, "list": listing}


def insight_topics(folder):
    """{topic: [ids]} for an insight Job: its release's questions, a topic read off each Task's name."""
    board = (folder.parent / "board.md").read_text(encoding="utf-8")
    proto = re.search(r"(?m)^prototype:\s*(\S+)", board)
    pn = re.search(r"-(p\d+)-", folder.name)
    if not proto or not pn:
        return {}
    rel = next((folder.parents[2] / proto.group(1)).glob(f"j*_{pn.group(1)}_*/release.yaml"), None)
    out = {}
    for qid, v in (yaml.safe_load(rel.read_text(encoding="utf-8"))["questions"] if rel else {}).items():
        slug = v["task"].rsplit("/", 1)[-1]
        name = next((n for k, n in TOPIC_WORDS if k in slug), "")
        if name:
            out.setdefault(name, []).append(qid)
    return out


def button(x, y, label, size=20, kind="", h=None):
    """A button sized to its words, drawn only as the workbench draws it (JL 261012: "I don't want it to be mislead
    the UI design"): kind on (the open one, blue), fixed (gray) or suggested (amber), a Report group by its kind
    (s07-D12, canvas.UI_KIND); anything else a plain button."""
    w, h = len(label) * size * 0.56 + 28, h or size + 20
    base("rectangle", x, y, w, h, INK, 3.5 if kind == "on" else 1.5, rough=0)
    if kind in ("fixed", "suggested"):
        L.els[-1].setdefault("customData", {})["ui_kind"] = kind
    text(x + 14, y + (h - size * 1.25) / 2, label, size)
    return x + w


def button_rows(x, y, w, label, items, span=None):
    """One labelled row of buttons, wrapped inside width w; returns the y below it. `span`, a list, gets the
    row's box (x0, y0, x1, y1), for a red mark around it."""
    bx, y0, right = x, y, x
    if label:
        text(x, y + 6, label + ":", 20)
        bx = x + len(label) * 11 + 26
    start = bx
    for name, kind in items:
        if bx + len(name) * 20 * 0.56 + 28 > x + w and bx > start:
            bx, y = start, y + 43
        bx = button(bx, y, name, 20, kind, 35) + 8
        right = max(right, bx)
    if span is not None:
        span.append((x, y0, right, y + 35))
    return y + 43


def red_mark(box, x, y, why):
    """A red box around what a note explains, and a red arrow to the note: this drawing's mark, not the screen's."""
    x0, y0, x1, y1 = box
    base("rectangle", x0 - 8, y0 - 6, x1 - x0 + 10, y1 - y0 + 12, RED, 2.5, rough=0)
    path([(x0 + 20, y1 + 6), (x0 + 20, y + 13), (x0 + 44, y + 13)], color=RED)
    text(x0 + 52, y, why, 20, RED)


def pane(x, y, w, draw):
    """A screen pane around what draw(x, y) puts at its top left; returns its bottom."""
    bottom = draw(x + 16, y + 14)
    base("rectangle", x, y, w, bottom - y + 6, INK, 1.5, rough=0)
    return bottom + 6


READS = {}                          # each theme's Report today, read once for ③ and ②
COL = (0, 300, 1320, 1370)          # label · today · arrow · proposed
WIDE = (1000, 1250)                 # today's pane, proposed's pane


def theme_row(frame, y, theme, where, rel_path):
    """One theme: its name and state, today's Report read live, the arrow, the proposed Report. Returns the y below."""
    root, folder = locate(where, rel_path)
    text(COL[0], y + 4, theme, 25)
    if folder is None:
        text(COL[0], y + 44, "? no Block of this theme\nbeside Tools: not read", 20, RED)
        return y + 110
    now = READS[theme] = read_report(frame, root, folder)
    name = folder.name if (folder / "board.md").is_file() else f"{folder.parent.name} {folder.name[:3]}"   # a Job: its Block
    text(COL[0], y + 42, short(name, 21), 20, INK, MONO)
    own = [(n, c) for n, c, k in now["bar"] if n not in ("Current", "Untagged") and not k]
    shown = {n.casefold() for n, *_ in now["bar"]}
    built = bool(now["bar"]) and all(g.casefold() in shown for g in starting_of(theme) + ["Random thoughts"])
    starting, guessed, listing = PROPOSED[theme]
    state = "built" if built else "half: the bar, not its groups" if now["bar"] else "not yet: no bar"
    text(COL[0], y + 76, state, 20, INK if state.startswith("built") else RED)

    def today(x, yy):
        for label, items in now["rows"]:
            yy = button_rows(x, yy, WIDE[0] - 32, label, [(n, "on" if on else "") for n, on in items])
        if now["bar"]:
            yy = button_rows(x, yy, WIDE[0] - 32, "", [(f"{n} {c}", k) for n, c, k in now["bar"]] + [("+ Group", "")])
        text(x, yy + 2, short(now["list"], 80), 20)
        return yy + 34

    def proposed(x, yy):
        rows = [r for r in now["rows"] if theme == "insight" or theme == "discovery"]     # the lenses that stay
        if theme == "paper":
            rows = [("view", [("Questions", True), ("Related Papers", False)])]
        for label, items in rows:
            yy = button_rows(x, yy, WIDE[1] - 32, label, [(n, "on" if on else "") for n, on in items])
        live = {n.casefold(): c for n, c, _ in now["bar"]}
        span = []
        if theme == "insight":
            topics = insight_topics(folder)
            yy = button_rows(x, yy, WIDE[1] - 32, "Topic", [("Current 0", "")] + [(f"{t} {len(q)}", "")
                             for t, q in topics.items()] + [("+ Group", "")], span)
        else:
            p = paper_facts() if theme == "paper" else {}
            counts = {"Ideation": p.get("ideas"), "Narrative": len(p.get("attract", [])),
                      "Research questions": p.get("rqs")} if p else {}
            kind = "fixed" if theme == "paper" else "suggested"      # the paper's kinds come from its own files
            bar = [("Current 0", "")]
            bar += [(f"{g} {live.get(g.casefold(), counts.get(g, 0))}", kind) for g in starting]
            bar += [("Random thoughts " + str(live.get("random thoughts", 0)), "suggested")]
            bar += [(f"{n} {c}", "") for n, c in own if n.casefold() not in {g.casefold() for g in starting}]
            yy = button_rows(x, yy, WIDE[1] - 32, "", bar + [("+ Group", "")], span)
        why = NOT_YET.get(theme) if not built else ""
        if why:
            red_mark(span[0], x, yy + 2, why)
        else:
            text(x, yy + 2, " · ".join(fold_names(now)) + " stay the folds, counted for the topic picked"
                 if theme == "insight" else listing, 20)
        return yy + 34

    b1 = pane(COL[1], y, WIDE[0], today)
    b2 = pane(COL[3], y, WIDE[1], proposed)
    path([(COL[2] - 30, y + 40), (COL[3] - 14, y + 40)], color=INK)
    return max(b1, b2, y + 108) + 8


def ui_frame():
    """The first frame, the largest: the Report's groups for the base and every theme, today and proposed."""
    fr = L.open_frame("The Report, with its groups: today and proposed")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    text(0, 0, "The Report's groups, theme by theme: today on the left, read live; proposed on the right", 40)
    note(0, 58, "redrawn: the base and every theme, today and proposed (JL)", "261012")
    text(COL[1], 92, "TODAY, read live through frame.render", 25)
    text(COL[3], 92, "PROPOSED", 25)
    frame = frame_module()
    y = 136
    for theme, where, rel_path in SCREENS:
        y = theme_row(frame, y, theme, where, rel_path)
    note(COL[3] + 300, 98, "insight: a Topic row across D · I · K · W (JL)", "261012")
    note(COL[3] + 300, 118, "real colours only: fixed gray, suggested amber; red marks explain (JL)", "261012")
    text(0, y + 6, "Colours as the workbench draws them: blue, the open one · gray, a group fixed by the theme · "
                   "amber, a group the theme suggests · white, the Block's own. Red boxes and → notes are this "
                   "drawing's marks, not the screen's.", 21)
    L.close_frame(fr)
    return fr


LEVELS = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}


def fold_names(now):
    """The level folds an insight Report shows today, read off the screen: Executive, Data, Information, ..."""
    return [w.rsplit(" ", 1)[0] for w in now["list"].removeprefix("folds: ").split(" · ")] \
        if now["list"].startswith("folds: ") else list(LEVELS.values())


def note(x, y, what, date="261011"):
    e = canvas.change_note(x, y, what, date, L.FRAME[0], 17)
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
