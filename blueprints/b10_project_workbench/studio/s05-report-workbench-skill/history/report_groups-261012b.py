"""s07 · Report groups across the themes: s07-report-groups-across-themes.excalidraw (haipipe-studio).

Three frames, each a folder tree (JL 261012: "每一个 frame 都太像一张 slide ... 我个人更 prefer 那种 tree 结构"):
① Background, the words and where the topic sits; ② the Tree, the topic itself, theme by theme, red ? leaves where
it is still open; ③ the screens, each theme's Report today beside the proposal (JL 261012: "for each theme and the
base, you should show how the report' groups looks like").

Read on every build: each theme's Report through servers/workbench/frame.py (frame.render, on one real Block or
Job of each theme in a SPACE beside Tools), b10's board.md register and studio/_groups.txt, each theme file's
Report hooks, the paper Board's and the insight Boards' own files. The proposal (starting groups, the insight
topics' names) is typed: it is what s07 proposes, not what the disk holds yet. The 261011 builder (four frames)
is in history/.

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

# b10's 12 Questions in its existing Studio groups (s07-D07); Q11 is open (Guide or UI)
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


# ── ① Background and ② the Tree (JL 261012: "每一个 frame 都太像一张 slide ... 我个人更 prefer 那种 tree 结构，就像
# folder tree 那样"): at most three frames, each a folder tree (canvas.tree); open questions are red leaves in place
THEME_PY = {t: L.TOOLKIT / f"servers/workbench-{t}/{t}_theme.py"
            for t in ("work", "cowork", "paper", "insight", "design", "discovery", "labeling")}
LEVELS = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}


def hooks(theme):
    """Which of the three Report hooks a theme file sets today (Theme.report_fixed, report_groups, report_cards)."""
    src = THEME_PY[theme].read_text(encoding="utf-8") if THEME_PY[theme].is_file() else ""
    return [h for h in ("report_fixed", "report_groups", "report_cards") if re.search(rf"\b{h}\s*=", src)]


def today_words(now):
    """Today's Report in one line: the rows above, the bar, the list."""
    parts = [(f"{label}: " if label else "") + " · ".join(n for n, _ in items) for label, items in now["rows"]]
    if now["bar"]:
        parts.append("bar " + " · ".join(f"{n} {c}" for n, c, _ in now["bar"]))
    return "today: " + "; ".join(parts + [now["list"]])


def by_level(ids):
    """D02 · I02 I12 · K05: one topic's ids, grouped by level letter."""
    out = {}
    for q in ids:
        out.setdefault(q[0], []).append(q)
    return " · ".join(" ".join(v) for _, v in sorted(out.items(), key=lambda kv: "XDIKW".find(kv[0])))


def fold_names(now):
    """The level folds an insight Report shows today, read off the screen: Executive, Data, Information, ..."""
    return [w.rsplit(" ", 1)[0] for w in now["list"].removeprefix("folds: ").split(" · ")] \
        if now["list"].startswith("folds: ") else list(LEVELS.values())


def theme_nodes(reads):
    """One branch per theme: today (read live), proposed, what stays a row, and what is still open, in red."""
    p, n = paper_facts(), insight_facts()
    out = []
    for theme, where, rel_path in SCREENS:
        root, folder = locate(where, rel_path)
        now = reads.get(theme)
        if now is None:
            out.append({f"{theme}": [f"? no Block of this theme beside Tools: {rel_path.rsplit('/', 1)[-1]} not read"]})
            continue
        starting, guessed, listing = PROPOSED[theme]
        shown = {n_.casefold() for n_, *_ in now["bar"]}
        built = bool(now["bar"]) and all(g.casefold() in shown for g in starting + ["Random thoughts"])
        state = "built" if built else "half built" if now["bar"] else "not on the bar"
        kids = []
        if theme == "base":
            kids += ["✎ 261011 built and live: b10's 12 Questions carry their group: lines (s07-D07, D09)",
                     "✎ 261012 built: Random thoughts, suggested (amber), on every theme's bar (s07-D02, D12)"]
        elif theme == "work":
            kids += (["✎ 261012 built: Data · Pilot · Evaluation suggested (amber, work_theme.py report_groups), "
                      "then the Block's own (Corpus, Learning strategy; b51: Food, Insulin)"] if hooks(theme) else
                     ["? work_theme.py sets no Report hook: Data · Pilot · Evaluation are not shown yet"])
            kids += ["a Task keeps Draft · Report as a lens; under Report, its own bar (s07-D13)",
                     "? b17_theme_work has not said which groups are the work theme's own (Open 5)"]
        elif theme == "cowork":
            kids += (["✎ 261012 its Block is on the bar: the base's cards (cowork_theme.py leaves the Report to "
                      "report_view); a report with an event table adds Questions · Timeline above, a lens"]
                     if now["bar"] else
                     ["today it draws its own list (question_rows): All plus a group's timeline when a Block has "
                      "group: lines",
                      "? move cowork's Block Report onto report_view, its timeline kept as a lens?"])
            kids += (["✎ 261012 built: Needs · Works · Blockers suggested (amber); its Job shows the Block's "
                      "Questions whose work: names it, as cards under the bar (s07-D13)"] if hooks(theme) else
                     ["? cowork_theme.py sets no Report hook: Needs · Works · Blockers are not shown yet"])
            kids += ["? b13_theme_cowork has not answered (Open 5)"]
        elif theme == "paper":
            kids += [f"today its buttons are already kinds of question: {p['ideas']} ideas, {len(p['attract'])} "
                     f"standing, the Story's {p['rqs']} research questions",
                     "proposed: they move onto the bar, renamed Research questions and Random thoughts; "
                     "Related Papers stays a row (it reads related/)",
                     "its version Job's manuscript parts are lenses; b16 owns the paper's list (b16 s05-D02)",
                     "? RQ0 or Q00 on screen (b16 s05 Open 5; Open 8 here)"]
        elif theme == "insight":
            topics = insight_topics(folder)
            kids += ["proposed (s07-D10, JL 261012): a Topic row under Period, the group bar; the level folds ("
                     + " · ".join(fold_names(now)) + ") stay, each counting only the topic picked",
                     "partitions and Period stay rows: the same Questions on another cut or time (lenses)",
                     {f"{folder.parent.name}: {len(topics)} topics across the {sum(map(len, topics.values()))} "
                      "Questions of release p1, read off each Task's name": [f"{t} {len(q)}: {by_level(q)}"
                                                                             for t, q in topics.items()]},
                     f"{n['board']} the same way: " + " · ".join(f"{s} {len(q)}" for s, q in n["subjects"].items()),
                     "? the topic names are guessed from the Task names: agree them",
                     "? a topic's group: line goes in each question.md of the Prototype, so every Board of it "
                     "shares it (Open 7)"]
        elif theme == "design":
            kids += ["today's Block is an older Design Folder board; a design ladder Block reads as the base",
                     "its Job keeps Elements · Evaluation: lenses",
                     "? Goal · Rules · Ranking are guessed: learn them on one real Block (Open 3)"]
        elif theme == "discovery":
            kids += ["Questions · Reports stays a row above",
                     "? Known · Closest · Gap are guessed: learn them on one real Block (Open 3)"]
        elif theme == "labeling":
            kids += ["? Guideline · Agreement · Models are guessed: learn them on one real Block (Open 3)"]
        out.append({f"{theme}  ·  {short(folder.name, 30)}  ·  {state}": kids})
    return out


# one Block, Job and Task of a theme, read live for the tree's level branch (s07-D13)
BY_LEVEL = [("work", "Block", "examples-2-lm/Proj11-CGM-Corpus/work/b02_pretrain_corpus"),
            ("work", "Job", "examples-2-lm/Proj11-CGM-Corpus/work/b02_pretrain_corpus/j01_trace_to_text"),
            ("work", "Task", "examples-2-lm/Proj11-CGM-Corpus/work/b02_pretrain_corpus/j01_trace_to_text/"
                             "t02_sampled_windows"),
            ("cowork", "Job", "examples-0-cowork/Project-Samsung/cowork/b12_epic_streaming/j01_pace_request")]


def level_nodes():
    fm, out = frame_module(), []
    for theme, level, rel_path in BY_LEVEL:
        root, folder = locate("space", rel_path)
        if folder is None:
            out.append(f"? {level} {rel_path.rsplit('/', 1)[-1]}: not beside Tools, not read")
            continue
        now = read_report(fm, root, folder)
        groups = [n for n, *_ in now["bar"] if n not in ("Current", "Untagged")]
        out.append(f"{'✎ 261012 ' if groups else '? '}{theme} {level} {short(folder.name, 22)}: "
                   + (f"{len(groups)} groups on its bar" if groups else "no bar") + f" · {short(now['list'], 40)}")
    out.append("a Job without Questions shows the Block's it answers (answers:, or work: naming it)")
    return out


def tree_nodes(reads):
    qs = register()
    title_of = {q: t for q, t, _ in qs}
    order = [g for g in L_order() if g in set(B10_GROUPS.values())]
    p = paper_facts()
    built = [t for t in THEME_PY if hooks(t)]
    return [
        {"The bar, built 261011 (s07-D01, D09; workbench 1.19.0 and 1.19.1)": [
            "one folding card per Question under the group bar, the Studio's own code (frame.group_list)",
            "a drag writes the Question's group: line in board.md's ## Questions",
            {"three hooks a theme fills": ["report_fixed: its fixed groups, no ×",
                                           "report_groups: its starting groups, shown even empty",
                                           "report_cards: its own cards (ideas, standing Questions)"]},
            f"? themes that set a hook today: {', '.join(built) or 'none of the seven'}"]},
        {"Where a group's name comes from, and its colour (s07-D02, D12)": [
            "fixed, gray: from the Question itself or the theme's own files, no × (report_fixed, report_cards)",
            "suggested, amber: the theme's kinds of question, shown even when empty (report_groups)",
            "added, white: + Group, the Block's own subjects (Corpus, Pilot; Food, Insulin)",
            "Random thoughts: in every theme, what a reviewer, coauthor or partner asked",
            "? one name in every theme, or the theme's word (paper: Reviewers)? (Open 4)"]},
    ] + theme_nodes(reads) + [
        {"A row above the list is a lens, and stays (s07-D05)": [
            "a group gathers rows into one list: it goes on the bar",
            "a lens shows the same Questions another way: a cut, a period, a manuscript part",
            "insight: partitions and Period are lenses, its topics a group (JL 261012)"]},
        {"Every level has its bar (s07-D13, JL 261012), read live": level_nodes()},
        {"Studio and Report share names, not one list (s07-D04)": [
            "pick UI in the Studio: it stays picked in the Report",
            "Related keeps its own groups, its subfolders (s04-D08)",
            "? share the names (recommended; the watcher agreed 261011), or one list? (Open 1)"]},
        {"Standing Questions (s07-D08)": [
            "paper Board: will it attract the " + " · ".join(p["attract"]) + "; each version: "
            + " · ".join(p["standing"])]},
        {"b10's 12 Questions in its Studio groups (s07-D07), read from board.md": [
            " · ".join(f"{g} " + " ".join(q for q, v in B10_GROUPS.items() if v == g) for g in order)]
         + ["? Q11, how a Page's logic is drawn: Guide or UI? (Open 2)"]},
        {"In Tools: Tools/plugins/haipipe-toolkit/": [
            {"skills/1_base/question/haipipe-question/": ["the register: a Question's group: line"]},
            {"skills/1_base/project/haipipe-report/": ["the Report itself (s05)"]},
            {"servers/workbench/frame.py": ["report_view · group_list · _register_set_groups · question_rows"]},
            {"servers/workbench-<theme>/<theme>_theme.py": [
                "Report hooks set: " + (", ".join(f"{t} {'+'.join(hooks(t))}" for t in THEME_PY if hooks(t))
                                        or "none of the seven (read on this build)")]}]},
    ]


BACKGROUND = [
    {"What this topic is about": [
        "How a Report groups its Questions, in every theme: the row of group buttons above the Report's list",
        "s05 is the Report itself; this topic is only its groups",
        "JL 261011, on b10's Report: \"these group names should be predefined and also can be added if we want?\""]},
    {"The Report, in one minute": [
        "a report answers one Question of its level, in reports/qNN_<topic>/",
        "the Report Space sits in the Spaces row: Description · Report · Work · Runs",
        "it lists one card per Question: Logic │ Work │ Report",
        "every level keeps its own Report (s09-D02): Block, Job and Task"]},
    {"Words it uses": [
        "group: a name that gathers Questions into one list; a Question's register group: line",
        "the bar: Current · the groups · Untagged · + Group, as the Studio shows its topics",
        "fixed group: comes from the Question itself, insight's Data · Information · Knowledge · Wisdom",
        "starting group: a theme's kinds of question, shown even when empty",
        "lens: the same Questions shown another way (a cut, a period, a manuscript part); a row above",
        "standing Question: asked on every Board, with no register line",
        "theme: the kind of Block (work, cowork, paper, insight, design, discovery, labeling); base: none"]},
    {"Where it sits": [
        "b10 keeps the rule and the table; each theme Block, b11 to b17, its own list (Open 5)",
        "code: servers/workbench/frame.py, one look for Studio, Related and Report",
        "feeds the Questions q03_block_questions and q09_studio_report_on_screen"]},
    {"How to read this drawing": [
        "① this frame, the words",
        "② the Tree: the topic, theme by theme; red ? leaves are still open",
        "③ the screens: each theme's Report today, read live, beside the proposal"]},
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
    ui = ui_frame()                                      # ③ first: it reads each theme's Report for ② too
    bg = tree_frame("Background: what a Report's groups are", "Background: a Report's groups, for a newcomer",
                    ["The words this topic uses, and where it sits. The topic itself is the Tree; the screens "
                     "are the third frame."], BACKGROUND, 1500, 1)
    tree = tree_frame("The Tree: Report groups across the themes", "Report groups across the themes",
                      ["What is built, what each theme shows today (read live) and what is proposed; red ? "
                       "leaves are still open."], tree_nodes(READS), 2600, 3)
    canvas.grid(L.els, [[bg["id"], tree["id"]], [ui["id"]]])
    for e in canvas.off_palette(L.els):                  # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, list(L.els), "build_s07_report_groups_across_themes.py")


if __name__ == "__main__":
    main()
