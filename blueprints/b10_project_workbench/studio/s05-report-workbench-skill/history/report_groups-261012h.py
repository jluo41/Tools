"""s05 · Report groups across the themes: the frames build_s05_report_workbench_skill.py draws after its story
(merged from s07-report-groups-across-themes on 261012, JL: "could you merge s07 to the s05?").

Acts 2 to 4 of s05-report-workbench-skill.excalidraw (b31 s01-D01, JL 261012: "one frame should be as large as
possible, wihtin the frame, we want the workflow map or the mindmap, the frames should be well arrange to form the
narrative ... No more folder tree for the non folder items"):

    the screens: one frame per theme, its Report at Block, Job and Task today, read live through frame.render,
       beside the proposal, in the workbench's own colours, red boxes and → notes for what is not built (s05-D16)
    ⑤ a workflow map: how a group's name reaches the Report, step by step, with the group-or-lens gate
    ⑥ a mind map: every part of the topic around one centre, the open points red on their branches

Read on every build: each theme's Report through servers/workbench/frame.py (on one real Block or Job of each theme
in a SPACE beside Tools), one Block, Job and Task read live, b10's board.md register and studio/_groups.txt, each
theme file's Report settings, the paper Board's and Insight-SMSR2v1's own files. Earlier builders are in history/
(report_groups-*.py, s07's builder until 261012).
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
sys.path.insert(0, str(L.TOOLKIT / "skills/1_base/display/excalidraw-studio/scripts"))
from draw import KEY, MAP_FLOOR, FLOOR, Drawing  # noqa: E402  (excalidraw-studio: the key colour, density)

INK, RED, MONO = L.INK, L.RED, L.MONO
text, path, base = L.text, L.path, L.base
FRAME_PY = L.TOOLKIT / "servers/workbench/frame.py"

# b10's 12 Questions in its existing Studio groups (s05-D11); Q11 is open (Guide or UI)
B10_GROUPS = {"Q01": "Levels", "Q02": "Levels", "Q03": "Report", "Q04": "Structure", "Q05": "Run and Skill",
              "Q06": "Run and Skill", "Q07": "UI", "Q08": "UI", "Q09": "UI", "Q10": "Guide", "Q11": "Guide",
              "Q12": "Server"}
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
            ("control-and-timing", "Glucose control"))      # a subject read off each Task's name (s05, Paper and insight today, 5)


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


# ── the UI, the most salient part (JL 261011: "make the UI to be the most salient part"; 261012: "for each theme
# and the base, you should show how the report' groups looks like"): one row per theme, the Report read live
# through frame.render on the left, the proposal on the right
# ── one frame per theme, its Report at Block, Job and Task (JL 261012: "each theme will be a frame, and within the
# frame, we will have the report for the block, job, and task"): one real folder of each level, read live through
# frame.render on the left, the proposal on the right; a level with no folder on disk says so
THEME_LEVELS = {     # theme: [(level, where, folder or None, why none)]; "tools" is this Tools repo, "space" a SPACE
    "base": [("Block", "tools", "blueprints/b10_project_workbench", ""),
             ("Job", "tools", "blueprints/b03_inlab-human/j01_study", ""),
             ("Task", "tools", None, "no Task in any Tools Block yet")],
    "work": [("Block", "space", "examples-2-lm/Proj11-CGM-Corpus/work/b02_pretrain_corpus", ""),
             ("Job", "space", "examples-2-lm/Proj11-CGM-Corpus/work/b02_pretrain_corpus/j01_trace_to_text", ""),
             ("Task", "space", "examples-2-lm/Proj11-CGM-Corpus/work/b02_pretrain_corpus/j01_trace_to_text/"
                               "t02_sampled_windows", "")],
    "cowork": [("Block", "space", "examples-0-cowork/Project-Samsung/cowork/b12_epic_streaming", ""),
               ("Job", "space", "examples-0-cowork/Project-Samsung/cowork/b12_epic_streaming/j01_pace_request", ""),
               ("Task", "space", None, "a cowork Job holds no Tasks")],
    "paper": [("Block", "space", PAPER, ""), ("Job", "space", PAPER + "/j01_v1009_nmi", ""),
              ("Task", "space", PAPER + "/j01_v1009_nmi/t00_abstract", "")],
    "insight": [("Block", "space", "examples-5-design/Project-Application-SMSDesign/insight/Insight-SMSR2v1", ""),
                ("Job", "space", "examples-5-design/Project-Application-SMSDesign/insight/Insight-SMSR2v1/"
                                 "j01_prototype-p1-basic-questions_data-SMSR2v1", ""),
                ("Task", "space", "examples-5-design/Project-Application-SMSDesign/insight/Insight-SMSR2v1/"
                                  "j01_prototype-p1-basic-questions_data-SMSR2v1/t01_D01_extract-shape-and-quality", "")],
    "design": [("Block", "space", "examples-5-design/ProjI-Insight-1-Wearable/design/Design-PreVisitChecklist", ""),
               ("Job", "space", "examples-5-design/ProjI-Insight-1-Wearable/design/Design-PreVisitChecklist/"
                                "j01_prepare-before-visit_goal-only", ""),
               ("Task", "space", "examples-5-design/ProjI-Insight-1-Wearable/design/Design-PreVisitChecklist/"
                                 "j01_prepare-before-visit_goal-only/t00_reason-ideas", "")],
    "discovery": [("Block", "space", "examples-0-cowork/Project-SHIFT-Study/discovery/b01_shift_proposal_evidence", ""),
                  ("Job", "space", "examples-0-cowork/Project-SHIFT-Study/discovery/b01_shift_proposal_evidence/"
                                   "j31_task31_citations", ""),
                  ("Task", "space", "examples-0-cowork/Project-SHIFT-Study/discovery/b01_shift_proposal_evidence/"
                                    "j31_task31_citations/t01_ai_insulin_titration_trials", "")],
    "labeling": [("Block", "space", "examples-6-labeling/Project-Labeling-ClinicalDialogue/labeling/b01_aci_bench", ""),
                 ("Job", "space", "examples-6-labeling/Project-Labeling-ClinicalDialogue/labeling/b01_aci_bench/"
                                  "j01_aci_bench_authority_appeal", ""),
                 ("Task", "space", "examples-6-labeling/Project-Labeling-ClinicalDialogue/labeling/b01_aci_bench/"
                                   "j01_aci_bench_authority_appeal/t01_aci_bench_transcripts", "")],
}
SCREENS = [(t, levels[0][1], levels[0][2]) for t, levels in THEME_LEVELS.items()]      # each theme's Block
EMOJI = {"base": "🧭", "work": "📋", "cowork": "🤝", "paper": "📄", "insight": "🔎", "design": "🎨",
         "discovery": "🔭", "labeling": "🏷️"}


def insight_job():
    """The insight Job whose release the Topic row reads (its Tasks' names give the topics)."""
    return locate(*THEME_LEVELS["insight"][1][1:3])[1]


# the proposal per theme (s05-D07, D09, D14): its suggested groups (red when guessed), and how the list reads; every
# theme also starts with Random thoughts (s05-D06); the same groups at every level (s05-D17)
PROPOSED = {
    "base": ([], False, "one card per Question"),
    "work": (["Data", "Pilot", "Evaluation"], False, "one card per Question"),
    "cowork": (["Needs", "Works", "Blockers"], False, "one card per Question"),
    "paper": (["Ideation", "Narrative", "Research questions"], False, "its ideas and standing Questions as cards too"),
    "insight": ([], False, "one card per Question"),
    "design": (["Goal", "Rules", "Ranking"], True, "one card per Question"),
    "discovery": (["Known", "Closest", "Gap"], True, "one card per Question"),
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


def not_yet(theme, level):
    """What the red mark beside a proposed bar says while the screen does not show it yet (JL 261012: "use the red
    box to circle them and give --> text to explain them")."""
    if PROPOSED[theme][1]:
        return f"guessed names: learn them on one real {theme} Block (Open 11)"
    if theme == "insight" and level == "Job":
        return "proposed (s05-D14): a Topic row; names guessed from the Task names"
    return {("paper", "Block"): "not built: the paper draws its own five buttons; b16 owns its list (b16 s05-D02)",
            ("paper", "Job"): "not built: the version draws its own parts; its bar is proposed (s05-D17)",
            ("paper", "Task"): "not built: a Section draws its own views; its bar is proposed (s05-D17)"}.get(
        (theme, level), f"not built: {theme} draws its own Report here; its bar is proposed (s05-D17)")


def starting_of(theme, level="Block"):
    return [] if theme == "paper" and level != "Block" else list(PROPOSED[theme][0])


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
    (s05-D16, canvas.UI_KIND); anything else a plain button."""
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


READS = {}                          # each theme's Block Report today, read once for ⑤ and ⑥
COL = (0, 300, 1320, 1370)          # label · today · arrow · proposed
WIDE = (1000, 1250)                 # today's pane, proposed's pane


def level_row(fm, y, theme, level, where, rel_path, why_none, states):
    """One level of one theme: its name and state, today's Report read live, the arrow, the proposed Report.
    `states` gets (level, built or None when the level has no folder)."""
    text(COL[0], y + 4, level, 34)
    root, folder = locate(where, rel_path) if rel_path else (None, None)
    if folder is None:
        states.append((level, None))
        text(COL[0], y + 50, why_none or "not beside Tools: not read", 20)
        text(COL[1], y + 10, why_none or "", 24)
        return y + 100
    now = read_report(fm, root, folder)
    if level == "Block":
        READS[theme] = now
    text(COL[0], y + 50, short(folder.name, 21), 20, INK, MONO)
    starting = starting_of(theme, level)
    own = [(n, c) for n, c, k in now["bar"] if n not in ("Current", "Untagged") and not k]
    shown = {n.casefold() for n, *_ in now["bar"]}
    built = bool(now["bar"]) and all(g.casefold() in shown for g in starting + ["Random thoughts"]) \
        and not (theme == "insight" and level == "Job") and not PROPOSED[theme][1]
    states.append((level, built))
    state = "built" if built else "half: the bar, not its groups" if now["bar"] else "not yet: no bar"
    text(COL[0], y + 82, state, 20, INK if built else RED)

    def today(x, yy):
        for label, items in now["rows"]:
            yy = button_rows(x, yy, WIDE[0] - 32, label, [(n, "on" if on else "") for n, on in items])
        if now["bar"]:
            yy = button_rows(x, yy, WIDE[0] - 32, "", [(f"{n} {c}", k) for n, c, k in now["bar"]] + [("+ Group", "")])
        text(x, yy + 2, short(now["list"], 80), 20)
        return yy + 34

    def proposed(x, yy):
        if level != "Block":                             # at a Job or Task every row today is a lens: it stays
            rows = now["rows"]
        elif theme == "paper":
            rows = [("view", [("Questions", True), ("Related Papers", False)])]
        else:
            rows = [r for r in now["rows"] if theme in ("insight", "discovery")]
        for label, items in rows:
            yy = button_rows(x, yy, WIDE[1] - 32, label, [(n, "on" if on else "") for n, on in items])
        live = {n.casefold(): c for n, c, _ in now["bar"]}
        span = []
        if theme == "insight" and level == "Job":
            topics = insight_topics(folder)
            yy = button_rows(x, yy, WIDE[1] - 32, "Topic", [("Current 0", "")] + [(f"{t} {len(q)}", "")
                             for t, q in topics.items()] + [("+ Group", "")], span)
        else:
            p = paper_facts() if theme == "paper" and level == "Block" else {}
            counts = {"Ideation": p.get("ideas"), "Narrative": len(p.get("attract", [])),
                      "Research questions": p.get("rqs")} if p else {}
            kind = "fixed" if theme == "paper" else "suggested"      # the paper's kinds come from its own files
            bar = [("Current 0", "")]
            bar += [(f"{g} {live.get(g.casefold(), counts.get(g, 0))}", kind) for g in starting]
            bar += [("Random thoughts " + str(live.get("random thoughts", 0)), "suggested")]
            bar += [(f"{n} {c}", "") for n, c in own if n.casefold() not in {g.casefold() for g in starting}]
            yy = button_rows(x, yy, WIDE[1] - 32, "", bar + [("+ Group", "")], span)
        if not built:
            red_mark(span[0], x, yy + 2, not_yet(theme, level))
        else:
            text(x, yy + 2, PROPOSED[theme][2], 20)
        return yy + 34

    b1 = pane(COL[1], y, WIDE[0], today)
    b2 = pane(COL[3], y, WIDE[1], proposed)
    path([(COL[2] - 30, y + 40), (COL[3] - 14, y + 40)], color=INK)
    return max(b1, b2, y + 108) + 24


KEYS = []                           # (frame id, text element, box): each theme frame's key line, boxed after colour_ui


def key_line(theme, states):
    """The one key point of a theme frame (excalidraw-studio principle 5), from its levels' states."""
    live = [lv for lv, b in states if b]
    if PROPOSED[theme][1]:
        return ("the bar is live; its names are guessed (Open 11)" if any(b is False for _, b in states) and live
                else "its names are guessed: learn them on one real Block (Open 11)")
    if theme == "insight":
        return "a Topic row on the Job, across the level folds (s05-D14)"
    if theme == "paper":
        return "the paper draws its own Report; the bar under its rows is proposed (b16 owns its list)"
    if live and all(b for _, b in states if b is not None):
        none = [lv for lv, b in states if b is None]
        return f"the bar is live at {' · '.join(live)}" + (f"; no {none[0]} on disk" if none else "")
    return "the bar is proposed under the rows it draws today"


def theme_frame(fm, theme):
    """One theme: its Report at Block, Job and Task, today beside proposed, in the workbench's own colours."""
    fr = L.open_frame(f"{theme}: the Report at Block, Job and Task")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    text(0, 0, f"{EMOJI[theme]} {theme}: its Report at Block, Job and Task", 60)
    note(0, 86, "one frame per theme, Block · Job · Task (JL)", "261012")
    text(COL[1], 182, "TODAY, read live through frame.render", 30)
    text(COL[3], 182, "PROPOSED", 30)
    y, states = 236, []
    for level, where, rel_path, why in THEME_LEVELS[theme]:
        y = level_row(fm, y, theme, level, where, rel_path, why, states)
    words = "🔑 " + key_line(theme, states)
    text(18, 124, words, 30)
    KEYS.append((fr["id"], L.els[-1], (0, 116, len(words) * 30 * 0.55 + 40, 52)))
    text(0, y + 6, "blue: the open one · gray: fixed by the theme · amber: suggested by the theme · white: the "
                   "Block's own · a red box and → note: this drawing's mark, not the screen's", 21)
    L.close_frame(fr)
    return fr


LEVELS = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}


def fold_names(now):
    """The level folds an insight Report shows today, read off the screen: Executive, Data, Information, ..."""
    return [w.rsplit(" ", 1)[0] for w in now["list"].removeprefix("folds: ").split(" · ")] \
        if now["list"].startswith("folds: ") else list(LEVELS.values())


# ── ⑤ the workflow map and ⑥ the mind map (JL 261012: "one frame should be as large as possible, wihtin the frame,
# we want the workflow map or the mindmap, the frames should be well arrange to form the narrative ... No more folder
# tree for the non folder items"; b31 s01-D01): steps joined by arrows, and one centre with its branches
import textwrap  # noqa: E402

THEME_PY = {t: L.TOOLKIT / f"servers/workbench-{t}/{t}_theme.py"
            for t in ("work", "cowork", "paper", "insight", "design", "discovery", "labeling")}
# one Block, Job and Task read live for the levels (s05-D17)
BY_LEVEL = [("work", "Block", "examples-2-lm/Proj11-CGM-Corpus/work/b02_pretrain_corpus"),
            ("work", "Job", "examples-2-lm/Proj11-CGM-Corpus/work/b02_pretrain_corpus/j01_trace_to_text"),
            ("work", "Task", "examples-2-lm/Proj11-CGM-Corpus/work/b02_pretrain_corpus/j01_trace_to_text/"
                             "t02_sampled_windows"),
            ("cowork", "Job", "examples-0-cowork/Project-Samsung/cowork/b12_epic_streaming/j01_pace_request")]


def hooks(theme):
    """Which of the three Report settings a theme file sets today (Theme.report_fixed, report_groups, report_cards)."""
    src = THEME_PY[theme].read_text(encoding="utf-8") if THEME_PY[theme].is_file() else ""
    return [h for h in ("report_fixed", "report_groups", "report_cards") if re.search(rf"\b{h}\s*=", src)]


def level_lines():
    fm, out = frame_module(), []
    for theme, level, rel_path in BY_LEVEL:
        root, folder = locate("space", rel_path)
        if folder is None:
            out.append(f"? {theme} {level}: not beside Tools, not read")
            continue
        now = read_report(fm, root, folder)
        groups = [n for n, *_ in now["bar"] if n not in ("Current", "Untagged")]
        cards = re.match(r"(\d+) Question cards", now["list"])
        out.append(f"{theme} {level}: " + (f"{len(groups)} groups" if groups else "no bar")
                   + (f", {cards.group(1)} cards" if cards else ", no Questions yet"))
    return out


def theme_lines():
    """One line per theme, its state today read off its live Report (READS)."""
    out = []
    for theme, *_ in SCREENS:
        now = READS.get(theme)
        if now is None:
            out.append(f"? {theme}: not read")
            continue
        starting = PROPOSED[theme][0]
        shown = {n.casefold() for n, *_ in now["bar"]}
        if now["bar"] and all(g.casefold() in shown for g in starting + ["Random thoughts"]):
            out.append(f"✅ {theme}: " + (" · ".join(starting) if starting else "Random thoughts"))
        elif now["bar"]:
            out.append(f"? {theme}: " + " · ".join(starting) + " (guessed)")
        else:
            out.append(f"⬜ {theme}: " + {"paper": "its own five buttons (b16)", "insight": "a Topic row (D14)",
                                          "design": "Goal · Rules · Ranking (guessed)",
                                          "discovery": "Known · Closest · Gap (guessed)"}.get(theme, "not yet"))
    return out


def wrap(s, w, size=22):
    return "\n".join(textwrap.fill(p, max(10, int(w / (size * 0.55)))) for p in s.split("\n"))


def node(x, y, w, title, body="", asks=(), size=38, key=False):
    """A workflow step: a box with its title, two or three lines, and its open asks in red; `key`, the frame's key
    point in the one slight colour (excalidraw-studio principle 5). Returns (x, y, w, h)."""
    i0, yy = len(L.els), y + 16
    t = wrap(title, w - 36, size)
    text(x + 18, yy, t, size)
    yy += size * 1.25 * len(t.split("\n")) + 8
    if body:
        b = wrap(body, w - 36)
        text(x + 18, yy, b, 22)
        yy += 27.5 * len(b.split("\n")) + 6
    for a in asks:
        b = wrap(a, w - 36)
        text(x + 18, yy, b, 22, RED)
        yy += 27.5 * len(b.split("\n")) + 4
    h = yy - y + 12
    base("rectangle", x, y, w, h, INK, 3 if key else 2, rough=0)
    if key:                                              # filled, so it goes under its words
        e = L.els.pop()
        e.update(backgroundColor=KEY, fillStyle="solid")
        L.els.insert(i0, e)
    return x, y, w, h


def arrow(a, b, label="", red=False, side="h"):
    """A labelled arrow from box a to box b (x, y, w, h): right side to left side, or bottom to top."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    if side == "h":
        y1 = ay + min(ah, bh) / 2 if abs(ay - by) < 40 else ay + ah / 2
        pts = [(ax + aw, y1), (bx - 6, by + bh / 2)] if bx > ax else [(ax, y1), (bx + bw + 6, by + bh / 2)]
    else:
        pts = [(ax + aw / 2, ay + ah), (bx + bw / 2, by - 6)] if by > ay else [(ax + aw / 2, ay), (bx + bw / 2, by + bh + 6)]
    path(pts, color=RED if red else INK, dashed=red)
    if label:
        (x1, y1), (x2, y2) = pts
        if side == "h":
            text((x1 + x2) / 2 - len(label) * 6, (y1 + y2) / 2 - 32, label, 22, RED if red else INK)
        else:                                            # beside a vertical arrow, never on it
            text(x1 + 14, (y1 + y2) / 2 - 14, label, 22, RED if red else INK)


def flow_frame():
    """⑤ one workflow map: how a group's name reaches the Report and filters it."""
    fr = L.open_frame("⑤ How a group reaches the Report")
    text(0, 0, "⑤ How a group reaches the Report", 60)
    text(0, 82, "From a name to a filtered list: each box is a step, an arrow says what leads to what; red is still "
                "open; the key step is filled.", 24)
    qs = register()
    W, X = 520, (0, 700, 1400, 2100)
    theme_box = node(X[0], 150, W, "💡 The theme suggests kinds",
                     "amber, shown even when empty: work Data · Pilot · Evaluation; cowork Needs · Works · "
                     "Blockers; every theme Random thoughts",
                     ["? design, discovery, labeling: the names are guesses (Open 11)"])
    fixed_box = node(X[0], theme_box[1] + theme_box[3] + 50, W, "🔒 The Question fixes some",
                     "gray, no ×: read off the Question itself (insight's level letter) or the theme's own files "
                     "(the paper's kinds, b16)")
    own_box = node(X[0], fixed_box[1] + fixed_box[3] + 50, W, "✋ The Block adds its own",
                   "white: + Group, kept in reports/_groups.txt (b02: Corpus, Learning strategy)")
    q_box = node(X[1], 150, W, "📌 A Question gets its group line",
                 f"the register's group: line in the face; a drag onto a group writes it. b10: {len(qs)} Questions, "
                 f"{sum(1 for q in qs if B10_GROUPS.get(q[0]))} grouped",
                 ["? Q11, how a Page's logic is drawn: Guide or UI? (Open 10)"])
    gate = node(X[1], q_box[1] + q_box[3] + 90, W, "🚦 A new row: a group, or a lens?",
                "gathers Questions into one list: a group, on the bar. Shows the same Questions another way "
                "(a cut, Period, a manuscript part): a lens (s05-D09)")
    lens = node(X[1], gate[1] + gate[3] + 90, W, "🔭 A lens stays a row above",
                "insight's partitions and Period; a work Task's Draft · Report; a paper version's parts; "
                "Related Papers")
    bar = node(X[2], 150, W, "🎛️ The bar counts it",
               "Current · groups · Untagged · + Group, the Studio's own bar; a colour by kind (s05-D16); order: "
               "_groups.txt, the theme's, the Studio's",
               ["? share names with the Studio, or one list? (Open 9)"], key=True)
    topics = insight_topics(insight_job()) if insight_job() else {}
    span = lambda q: " ".join(sorted({x[0] for x in q}, key="XDIKW".find))
    insight = node(X[2], bar[1] + bar[3] + 90, W, "🔎 Insight adds a Topic row",
                   f"under Period, its own groups: {len(topics)} topics across the levels, "
                   + ", ".join(f"{t} {span(q)}" for t, q in list(topics.items())[:3]) + " ... (s05-D14)",
                   ["? topic names guessed from the Task names; a group line in question.md? (Open 15)"])
    paper = node(X[2], insight[1] + insight[3] + 90, W, "📄 The paper draws its own",
                 "five buttons today, not the bar; b16 owns its list (b16 s05-D02)",
                 ["? RQ0 or Q00 on the screen? (Open 16)"])
    lv = level_lines()
    levels = node(X[3], 150, W, "🧱 Every level shows its bar",
                  "Block, Job and Task (s05-D17). A Job with no Questions shows the Block's it answers "
                  "(answers:, or work: naming it); a Task lists its own Page")
    rows, y = [], levels[1] + levels[3] + 60
    for line in lv:
        r = node(X[3] + 40, y, W - 40, line, size=24)
        rows.append(r)
        y = r[1] + r[3] + 14
    pick = node(X[3], y + 40, W, "👆 Pick a group: the cards filter",
                "Current is kept in the browser; a name the Studio shares stays picked (s05-D08)")
    for a, lab in ((theme_box, "suggests"), (fixed_box, "fixes"), (own_box, "adds")):
        arrow(a, q_box, lab)
    arrow(q_box, gate, "a new row?", side="v")
    arrow(gate, bar, "a group")
    arrow(gate, lens, "a lens", side="v")
    arrow(q_box, bar, "counted on")
    arrow(insight, bar, "its own groups", side="v")
    arrow(paper, insight, "? not on the bar yet", red=True, side="v")
    arrow(bar, levels, "shows at")
    arrow(levels, rows[0], "read live", side="v")
    arrow(rows[-1], pick, "then", side="v")
    L.close_frame(fr)
    return fr


def branch(cx, cy, bx, by, title, leaves, left):
    """One mind-map branch: a line from the centre to its box, then a line from the box to each leaf."""
    w = max(len(title) * 19 + 50, 320)
    x = bx - w if left else bx
    base("rectangle", x, by - 36, w, 72, INK, 2, rough=0)
    text(x + 18, by - 22, title, 34)
    path([(cx, cy), (x + w + 6 if left else x - 6, by)], arrow=True, color=INK)    # the centre leads to each branch
    n = len(leaves)
    for i, leaf in enumerate(leaves):
        ly = by + (i - (n - 1) / 2) * 34
        color = RED if leaf.startswith("?") else INK
        lw = len(leaf) * 22 * 0.5
        lx = x - 50 - lw if left else x + w + 50
        path([(x if left else x + w, by), (lx + lw + 8 if left else lx - 8, ly + 14)], arrow=False, color=INK)
        text(lx, ly, leaf, 22, color)


def mind_frame():
    """⑥ one mind map: the topic's every part around one centre, the open points red on their branches."""
    fr = L.open_frame("⑥ Report groups, every part in one map")
    text(0, 0, "⑥ Report groups, every part in one map", 60)
    text(0, 82, "One centre, the key point; each branch is one part of the topic; red is still open, on the branch it "
                "belongs to.", 24)
    topics = insight_topics(insight_job()) if insight_job() else {}
    used = set(B10_GROUPS.values())                  # a name the Studio uses keeps its order, the rest follow (D08)
    order = [g for g in L_order() if g in used] + sorted(used - set(L_order()))
    tools = [t for t in THEME_PY if hooks(t)]
    left = [("🎨 Colours (D16)", ["gray: fixed by the theme", "amber: suggested by the theme", "white: the Block's own",
                                 "in a drawing, a red box and a → note"]),
            ("🧩 Themes (D07)", theme_lines() + ["? theme Blocks b11 to b17 own their lists (Open 13)"]),
            ("🔭 Lenses, not groups (D09)", ["insight: partitions, Period", "work Task: Draft · Report",
                                            "paper version: its parts", "paper: Related Papers"]),
            ("🤝 Studio and Report (D08)", ["share the names, not one list", "pick UI in the Studio: still picked",
                                           "? share names, or one list? (Open 9)"])]
    right = [("🧱 Levels (D17)", level_lines()),
             ("🔎 Insight topics (D14)", [f"{t} {len(q)}: " + " ".join(sorted({x[0] for x in q}, key="XDIKW".find))
                                         for t, q in topics.items()] + ["? the names are guesses (Open 15)"]),
             ("📌 b10's 12 Questions (D11)", [f"{g}: " + " ".join(q for q, v in B10_GROUPS.items() if v == g)
                                             for g in order] + ["? Q11: Guide or UI? (Open 10)"]),
             ("🧰 In Tools", ["frame.py: report_view, group_list", "REPORT_SUGGESTED: Random thoughts"]
              + [f"{t}_theme.py: report_groups" for t in tools] + ["canvas.UI_KIND: a drawing's colours"])]
    cx, top = 1330, 180

    def heights(side):
        return [max(80, len(leaves) * 34 + 30) for _, leaves in side]
    lh, rh = heights(left), heights(right)
    total = max(sum(lh), sum(rh)) + 40 * 3
    cy = top + total / 2
    base("ellipse", cx - 250, cy - 80, 500, 160, INK, 3, rough=0)
    L.els[-1].update(backgroundColor=KEY, fillStyle="solid")                  # the key point (principle 5)
    text(cx - 205, cy - 28, "Report groups (s05)", 44)
    for side, hs, is_left in ((left, lh, True), (right, rh, False)):
        y = top + (total - (sum(hs) + 40 * (len(hs) - 1))) / 2
        for (title, leaves), h in zip(side, hs):
            branch(cx - 250 if is_left else cx + 250, cy, cx - 360 if is_left else cx + 360, y + h / 2, title,
                   leaves, is_left)
            y += h + 40
    L.close_frame(fr)
    return fr


def badge(fr):
    """excalidraw-studio principle 6: the frame's density in its bottom right corner, by the skill's own measure
    (draw.Drawing.words_per_mpx and kind): a screen is not measured, a map's floor is 70, a text frame's 120."""
    per, words = Drawing.words_per_mpx(L.els, fr["id"], fr["width"], fr["height"])
    kind = Drawing.kind(L.els, fr)
    floor = MAP_FLOOR if kind == "map" else FLOOR
    ok = kind == "picture" or per >= floor
    color = INK if ok else RED
    x = fr["x"] + fr["width"] - 600                      # a map's top right is free; a screen's holds its note
    y = fr["y"] + fr["height"] - 100 if kind == "picture" else fr["y"] + 24
    L.FRAME[0] = fr["id"]
    base("rectangle", x, y, 560, 76, color, 1.5, rough=0)
    text(x + 18, y + 6, f"📊 {per} words per million px", 24, color)
    text(x + 18, y + 42, "🖼️ a screen: not measured" if kind == "picture" else
         f"{'✅' if ok else '❌'} a {kind} frame, floor {floor} · {words} words", 21, color)
    L.FRAME[0] = None


def acts(rows, names, across, down, gap=340):
    """excalidraw-studio principle 3: the frames in acts, a row each, named at the left, and a named arrow for each
    step: `across`, the words between neighbours in a row; `down`, (from, to, words) between acts."""
    canvas.grid(L.els, [[f["id"] for f in r] for r in rows], gap=gap)
    steps = [(fa, fb, w) for r, words in zip(rows, across) for (fa, fb), w in zip(zip(r, r[1:]), words)]
    for fa, fb, words in steps + list(down):
        if abs(fa["x"] - fb["x"]) < 10:                  # one above the other
            x = fa["x"] + fa["width"] / 2
            path([(x, fa["y"] + fa["height"] + 14), (x, fb["y"] - 14)], color=INK)
            L.els[-1]["strokeWidth"] = 6
            text(x + 24, (fa["y"] + fa["height"] + fb["y"]) / 2 - 26, words, 40)
        else:                                            # side by side
            y = fa["y"] + min(fa["height"], fb["height"]) / 2
            path([(fa["x"] + fa["width"] + 14, y), (fb["x"] - 14, y)], color=INK)
            L.els[-1]["strokeWidth"] = 6
            text(fa["x"] + fa["width"] + 30, y - 30 - 50 * words.count("\n") - 40, words, 40)
    for r, name in zip(rows, names):
        text(r[0]["x"] - 860, r[0]["y"] + 20, textwrap.fill(name, 24), 56)


def note(x, y, what, date="261011"):
    e = canvas.change_note(x, y, what, date, L.FRAME[0], 17)
    e["id"] = f"v{len(L.els)}"
    L.els.append(e)


def L_order():
    """b10's Studio group order, studio/_groups.txt."""
    f = BLOCK / "studio" / "_groups.txt"
    return [ln.strip() for ln in f.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")] if f.is_file() else []


def draw(fm):
    """The merged frames: one per theme (Block · Job · Task, JL 261012), ⑤ how a group gets there, ⑥ every part in
    one map, each with its density badge. Returns (themes, flow, mind); s05's builder places them in acts."""
    KEYS.clear()
    themes = {t: theme_frame(fm, t) for t in THEME_LEVELS}
    flow, mind = flow_frame(), mind_frame()
    for fr in list(themes.values()) + [flow, mind]:
        badge(fr)
    return themes, flow, mind


def key_boxes():
    """Each theme's key line boxed in the one slight colour, after colour_ui so the screen colours leave it be."""
    for fid, words, (_, _, w, h) in KEYS:
        L.FRAME[0] = fid
        base("rectangle", words["x"] - 18, words["y"] - 8, w, h, INK, 3, rough=0)
        box = L.els.pop()
        box.update(backgroundColor=KEY, fillStyle="solid")
        L.els.insert(L.els.index(words), box)            # under its words
    L.FRAME[0] = None
