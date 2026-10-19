"""s05 · Report: its workbench, its skill and its groups: s05-report-workbench-skill.excalidraw, one story in five
acts, each a row named at the left, a named arrow for each step (JL 261011: "s02 studio, s03 delivery, and s04
related, and s05 report, and s06 run"; s07 merged in 261012, JL: "could you merge s07 to the s05?"):

    Act 1  ① a report, from its Question to its answer (one map, in colour: where it is asked, the Work that
           answers it, open → partial → answered, its Page and drawing) --> ② the Report Space shows it,
           /haipipe-report keeps it (a screen); ① was three frames until 261012
    Act 2  the group bar is live: base, work, cowork, labeling (report_groups.py, one frame per theme)
    Act 3  their own Report today: paper, insight, design, discovery
    Act 4  ③ how a group reaches the Report --> ④ every part in one map
    Act 5  still open (red) · this Block's Questions · In Tools

Read from disk on every build: this Block's Questions (board.md ## Questions), each report's answer-status,
which studio topics feed each Question (their **Feeds:** lines, read as frame.py reads them), the Runs that
target a Question (runs/*/run.yaml), q01's ## Figures, the Report Space as servers/workbench/frame.py draws
it for this Block, and haipipe-report's version; Acts 2 to 4 read what report_groups.py says it reads. Typed,
since they are the design: ①'s steps and colours, the open points.

    python build_s05_report_workbench_skill.py [out.excalidraw]
"""
import re
import sys
import textwrap
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parent                                      # b10's studio/
BLOCK = STUDIO.parent                                     # b10_project_workbench/
TOOLS = HERE.parents[3]                                   # s05 -> studio -> b10 -> blueprints -> Tools
ROOT = TOOLS
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
SKILLS = TOOLS / "plugins/haipipe-toolkit/skills/1_base"
sys.path.insert(0, str(STUDIO / "s01-overall-tree-structure"))
sys.path.insert(0, str(SERVERS / "_host"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers: base, text, path, frames)
sys.path.insert(0, str(SKILLS / "project/haipipe-studio/scripts"))
import canvas  # noqa: E402
import report_groups as G  # noqa: E402  (Acts 2 to 4: the Report's groups across the themes, merged from s07)

TODAY = "261011"
EXAMPLE = "Q05"                                            # ②'s and ④'s row
FIGURES = "q01_bjtr_boundary"                              # ③'s report drawing
STATES = ("open", "partial", "answered")
T, SUB, BODY, HEAD, CODE = 34, 22, 22, 24, 20              # frame title · line under it · words · box titles · paths


# ── facts, read from disk ───────────────────────────────────────────────────────────────────────
def frame_module():
    from host_paths import bootstrap
    bootstrap()
    from live import frame
    return frame


def questions(frame):
    """[{id, title, report, status, fed, runs}] for every Question of this Block, in register order."""
    reports = {q.name.split("_", 1)[0].upper(): q / (q.name + ".md") for q in sorted((BLOCK / "reports").glob("q[0-9]*/"))}
    fed, unread = {}, []
    for topic, _drawings in frame._studio_topics(BLOCK):
        notes = frame._notes(topic)
        found = frame._note_facts(notes)["feeds"]
        for q in found:
            fed.setdefault(q.split("_", 1)[0].upper(), []).append(topic.name.split("-", 1)[0].split("_", 1)[0])
        line = re.search(r"\*\*Feeds:\*\*(.+)", notes.read_text(encoding="utf-8")) if notes else None
        if line and not found and re.search(r"\b[Qq]\d\d\b", line.group(1)):
            unread.append((topic.name.split("-", 1)[0], line.group(1).strip()))
    runs = {}
    for card in sorted((BLOCK / "runs").glob("*/run.yaml")):
        c = yaml.safe_load(card.read_text(encoding="utf-8")) or {}
        runs.setdefault(str(c.get("target") or "").upper(), []).append(c.get("run"))
    out = []
    for r in frame._register(frame.face(BLOCK)):
        qid = str(r["id"]).upper()
        page = (BLOCK / r["report"]) if r.get("report") and (BLOCK / r["report"]).is_file() else reports.get(qid)
        status = dict(frame._fields(page)).get("answer-status", "open") if page and page.is_file() else "open"
        out.append({"id": qid, "title": r.get("title") or "", "report": page, "status": status,
                    "fed": fed.get(qid, []), "runs": runs.get(qid, []),
                    "work": frame._answering(BLOCK, "Block", qid, ROOT) + list(r.get("work") or [])})
    return out, unread


def report_space(frame):
    """(third-row buttons, the open one, the row's three heads, Runs-panel buttons) of this Block's Report Space."""
    sp = frame.spaces_for(frame.VANILLA, "Block", BLOCK, ROOT)["Audience Report"]
    heads = re.findall(r'q-head-row"><div>([^<]*)</div><div>([^<]*)</div></div>', sp.html)   # Logic │ Report (s05-D04)
    buttons = [(k["label"], k.get("doing", ""), " · ".join(k.get("skills") or [])) for k in sp.run_types]
    return list(sp.subspaces), sp.open, list(heads[0]) if heads else [], buttons


def figures():
    """q01's ## Figures: [(topic folder, frame name)]."""
    text = (BLOCK / "reports" / FIGURES / f"{FIGURES}.md").read_text(encoding="utf-8")
    m = re.search(r"```ya?ml\n(figures:.*?)```", text, re.S)
    rows = (yaml.safe_load(m.group(1)) or {}).get("figures") or [] if m else []
    return [(Path(f["from"]).parent.name, f["frame"]) for f in rows]


def version(skill):
    m = re.search(r'version:\s*"([^"]+)"', (skill / "SKILL.md").read_text(encoding="utf-8"))
    return m.group(1) if m else "?"


# ── drawing helpers (black lines, unfilled boxes; red = open, green = changed) ───────────────────
def rect(x, y, w, h, bold=False, dashed=False):
    return L.base("rectangle", x, y, w, h, L.INK, 3 if bold else 1.5, dashed, rough=0)


def say(x, y, s, size=BODY, color=L.INK, font=L.SANS):
    L.text(x, y, s, size, color, font)
    return y + size * 1.3 * (s.count("\n") + 1)


def wrap(s, n):
    return "\n".join(textwrap.wrap(s, n))


def line(pts, arrow=True, dashed=False):
    L.path(pts, arrow=arrow, color=L.INK, dashed=dashed)


def note(x, y, what):
    """A green change note where the change is (haipipe-studio: ✎ <date> <what>)."""
    e = canvas.change_note(x, y, what, TODAY, L.FRAME[0], size=18)
    L.els.append(e)
    return e


def heading(n, title, under):
    say(0, 0, f"{n} {title}", 60)                             # a frame title is 60 px (excalidraw-studio ⑤)
    return say(0, 84, under, 24)


KEY_LINES = []                                                # (frame id, text, box): boxed after colour_ui, as G's


def key_line(fr, y, words):
    """The frame's one key point (excalidraw-studio ⑤), boxed in the slight colour once the screen is coloured."""
    say(18, y, "🔑 " + words, 30)
    KEY_LINES.append((fr["id"], L.els[-1], (0, y - 8, len(words) * 30 * 0.55 + 80, 52)))
    return y + 70


# ── ① a report, from its Question to its answer: one map, in colour ──────────────────────────────
# Act 1's own colours (JL 261012: "merging the n frames into few frames ... and by adding the colors"): one colour
# per part, the report's state in the workbench's own status colours (canvas.STATUS_UI); the key point stays in the
# one slight colour, red stays open, green a change. This topic's only: no rule for other topics.
ROLE = {"studio": ("#7048e8", "#f3f0ff"),                    # violet: the Studio, where what to report is set
        "level": ("#1971c2", "#e7f5ff"),                     # blue: a level, which keeps its own reports/
        "work": ("#0c8599", "#e3fafc"),                      # teal: the Work that answers a Question
        "open": (canvas.STATUS_UI["open"], "#f1f3f5"),       # the report's state, as the screen colours it
        "partial": (canvas.STATUS_UI["partial"], "#fff4e6"),
        "answered": (canvas.STATUS_UI["answered"], "#ebfbee"),
        "file": ("#495057", "#f8f9fa")}                      # gray: a file the skill writes
WHAT = {"open": "asked, no answer yet; its writer moves it on, never a Run that ends alone", "partial": "some Work answers part; the report says which",
        "answered": "the Opening states it; Evidence links the Results. Checked is not a fourth state: the CHECK "
                    "verdict shows beside it (s21-D04)"}


def coloured(e, role):
    e.setdefault("customData", {})["s05_colour"] = role
    return e


def cnode(x, y, w, title, body="", asks=(), role=None, size=32, key=False, code=""):
    """A step of ①: a box in its role's edge and wash (the key point in the slight colour), its title in the edge's
    colour, `code` in Cascadia, the body, then its open asks in red. Returns (x, y, w, h)."""
    edge, wash = ROLE[role] if role else (L.INK, G.KEY)
    i0, yy = len(L.els), y + 14
    t = G.wrap(title, w - 36, size)
    L.text(x + 18, yy, t, size, edge)
    coloured(L.els[-1], role or "key")
    yy += size * 1.25 * (t.count("\n") + 1) + 8
    if code:
        L.text(x + 18, yy, code, CODE, L.INK, L.MONO)
        yy += CODE * 1.25 * (code.count("\n") + 1) + 8
    if body:
        b = G.wrap(body, w - 36, BODY)
        L.text(x + 18, yy, b, BODY)
        yy += BODY * 1.25 * (b.count("\n") + 1) + 6
    for a in asks:
        b = G.wrap(a, w - 36, BODY)
        L.text(x + 18, yy, b, BODY, L.RED)
        yy += BODY * 1.25 * (b.count("\n") + 1) + 4
    h = yy - y + 12
    L.base("rectangle", x, y, w, h, edge, 3 if key else 2, rough=0)
    box = coloured(L.els.pop(), role or "key")
    box.update(backgroundColor=wash, fillStyle="solid")
    L.els.insert(i0, box)                                    # filled, so it goes under its words
    return x, y, w, h


def legend(x, y):
    """The colour key, one chip per colour, under the frame's title."""
    for role, words in (("studio", "the Studio"), ("level", "a level"), (None, "the key: the Question"),
                        ("work", "the Work"), ("open", "open"), ("partial", "partial"), ("answered", "answered"),
                        ("file", "a file")):
        edge, wash = ROLE[role] if role else (L.INK, G.KEY)
        L.base("rectangle", x, y, 40, 34, edge, 2, rough=0)
        coloured(L.els[-1], role or "key").update(backgroundColor=wash, fillStyle="solid")
        L.text(x + 52, y + 2, words, 24, edge if role in STATES else L.INK)
        coloured(L.els[-1], role or "key")
        x += 52 + len(words) * 24 * 0.55 + 46


def frame_story(qs):
    """①: where a Question is asked, the Work that answers it, the report that says the answer, its Page and its
    drawing; one map, read left to right (was ① ② ③ until 261012)."""
    fr = L.open_frame("① A report, from its Question to its answer")
    say(0, 0, "① A report, from its Question to its answer", 60)
    say(0, 84, "Asked at a level, answered by the Work, said by the report: read from disk on every build. "
               "Red is still open.", 24)
    legend(0, 138)
    W, W4, X, Y, GAP = 520, 640, (0, 660, 1320, 1980), 230, 70
    jobs = [p for p in BLOCK.glob("j[0-9]*_*/") if p.is_dir()]

    studio = cnode(X[0], Y, W, "🎨 The Studio sets it", "one per Block, the centre; it sets what each level "
                   "reports (s09-D01)", ["? what must each level's report answer? (Open 1)"], "studio",
                   code="studio/sNN-<topic>/")
    levels, y = [], studio[1] + studio[3] + 100
    for name, path in (("🧱 Block", "reports/qNN_<topic>/"), ("📦 Job", "jNN_<job>/reports/qNN_<topic>/"),
                       ("🔧 Task", "tNN_<task>/reports/qNN_<topic>/")):
        levels.append(cnode(X[0], y, W, f"{name} keeps its own", "", (), "level", size=28, code=path))
        y = levels[-1][1] + levels[-1][3] + 14
    G.arrow(studio, levels[0], "sets what each reports", side="v")
    y = say(X[0], y + 10, G.wrap("A reader goes to the level to read its report (s09-D02, s09-D08).", W), BODY) + 8
    say(X[0], y, G.wrap(f"? b10 has {len(jobs)} Jobs, so no Job or Task report yet; the Block's Report lists only "
                        "its own reports/, not Job and Task reports by source (s09-D08; Open 2)", W), BODY, L.RED)

    reports = sum(1 for q in qs if q["report"])
    quest = cnode(X[1], Y, W, "❓ The Question, qNN", f"asked in the level's face: id · title · acceptance. Its "
                  f"report shares its id (s02-D30). b10: {len(qs)} Questions, {reports} reports", key=True, size=34,
                  code="board.md ## Questions")
    feeds = cnode(X[1], quest[1] + quest[3] + 100, W, "🔗 A studio topic feeds it", "named on the topic's face, read "
                  "as frame.py reads it", (), "studio", code="sNN-<topic>.md\n**Feeds:** qNN_<topic>")
    q = next(x for x in qs if x["id"] == EXAMPLE)
    work = [str(w) for w in q["work"]] + q["runs"]          # the row's Work cell: Jobs, Tasks, then its own Runs
    example = cnode(X[1], feeds[1] + feeds[3] + 50, W, f"📌 In b10: {q['id']}", G.wrap(q["title"], W - 36), (),
                    "level", size=28,
                    code="\n".join([f"fed by  {' · '.join(q['fed']) or 'no topic'}",
                                    f"work    {' · '.join(work[:1]) or 'no work yet'}"]
                                   + [f"        {w}" for w in work[1:]]
                                   + [f"report  {q['report'].parent.name if q['report'] else 'none'}"]))
    say(X[1], example[1] + example[3] + 16, G.wrap("An id the register does not have is an error: "
                                                    "check_report.py finds it.", W), BODY)
    G.arrow(levels[0], quest, "asks")
    G.arrow(feeds, quest, "feeds", side="v")

    job = cnode(X[2], Y, W, "📦 A Job answers it", "on its own face", (), "work", code="jNN_<job>.md\nanswers: Q01")
    task = cnode(X[2], job[1] + job[3] + GAP, W, "🔧 A Task answers a part", "Q01.E2 is one need (an Evidence "
                 "Item) of Q01; it counts for Q01", (), "work", code="tNN_<task>.md\nanswers: Q01.E2, Q04")
    run = cnode(X[2], task[1] + task[3] + GAP, W, "▶️ A Run targets it", "this level's own Runs, shown in the "
                "row's Work cell (s05-D03)", (), "work", code=f"runs/<run>/run.yaml\ntarget: {EXAMPLE}")
    G.arrow(quest, job, "answered by")
    for b in (task, run):
        G.arrow(quest, b)

    states, y = [], Y
    for st in STATES:
        ids = [x["id"] for x in qs if x["status"] == st]
        states.append(cnode(X[3], y, W4, f"{st}   {len(ids)} in b10", WHAT[st], (), st, size=30,
                            key=False, code=G.wrap(" · ".join(ids), W4 - 36, CODE * 1.1) or "none"))
        y = states[-1][1] + states[-1][3] + GAP
    G.arrow(states[0], states[1], "its writer moves it", side="v")
    G.arrow(states[1], states[2], side="v")
    G.arrow(task, states[1], "read")

    page = cnode(X[3], y, W4, "📄 The report Page", "its built pdf or docx goes to the Block's "
                 "delivery/reports/qNN_<topic>/ (s03)", (), "file", size=30,
                 code="\n".join(["reports/qNN_<topic>/", "├── qNN_<topic>.md   answer-status:",
                                 "│    ## Opening: the answer, one paragraph", "│    ## Answer · Evidence · Limits",
                                 "├── qNN_<topic>.excalidraw   generated", "└── draft/   the Page flow's versions"]))
    G.arrow(states[2], page, "the Opening states it", side="v")
    figs = figures()
    drawing = cnode(X[2], page[1], W, "🖼️ Its drawing, built", "build_report_drawing.py draws the frames its "
                    "## Figures lists; change a frame, rebuild. A frame's name is the contract (s02-D24)",
                    ["? a cited frame changes: flag the report first? (Open 6)"], "file", size=30,
                    code="\n".join(f"{t.split('-')[0]} › {n}" for t, n in figs))
    G.arrow(page, drawing, "## Figures")
    note(X[2], drawing[1] + drawing[3] + 14, f"{FIGURES.split('_')[0]} now cites s06's \"Hard or soft\" and "
                                             "\"For reference\"")
    e = canvas.change_note(X[0], max(page[1] + page[3], drawing[1] + drawing[3]) + 60,
                           "①②③ merged into this one map, in colour", "261012", L.FRAME[0], size=18)
    L.els.append(e)
    L.close_frame(fr, pad=60)
    return fr


# ── ② the Report Space shows it, the skill keeps it ──────────────────────────────────────────────
def frame_screen(qs, space, versions):
    subs, opened, heads, buttons = space
    fr = L.open_frame("Workbench and skill")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    y = heading("②", "The Report Space shows it; /haipipe-report keeps it",
                "The screen as frame.py draws it for this Block, beside the skill that writes and checks each report.")
    y = key_line(fr, y + 24, "one card per Question under the group bar, opened as Logic │ Report (s05-D04)") + 20
    say(0, y, f"On screen: Block {BLOCK.name.split('_')[0]} › Report  (read from frame.py)", HEAD)
    y += 50
    x = 0
    for s in subs:                                                # a theme's row above the list, if any
        w = int(len(s) * BODY * 0.55) + 40
        rect(x, y, w, 46, bold=s == opened)
        say(x + 20, y + 10, s, BODY)
        x += w + 12
    y += 76 if subs else 10
    cw = (440, 560)
    xs = (0, cw[0] + 10)
    for c, h in zip(xs, heads):
        say(c, y, wrap(h, 34), BODY)
    y += 70
    q = next(x for x in qs if x["id"] == EXAMPLE)
    work = "Work: " + (" · ".join(map(str, q["work"] + q["runs"])) or "no work yet")   # its own Runs too (s05-D03)
    cells = [f"{q['id']} · {q['status']}\n" + wrap(q["title"], 30) + "\nfrom the Studio:\n" + " ↗ ".join(q["fed"]) + " ↗",
             (q["report"].stem + " ↗\nits answer line\n" + wrap(work, 40) + "\nits drawing, live\n"
              + f"report {q['id'].lower()} · {q['status']}") if q["report"] else "No report yet\n" + wrap(work, 40)]
    for c, w, s in zip(xs, cw, cells):
        rect(c, y, w, 250)
        say(c + 16, y + 14, s, BODY)
    y += 280
    say(0, y, "Runs panel, beside the Report Space (read from frame.py)", HEAD)
    y += 46
    for label, doing, skill in buttons:
        say(0, y, label, CODE, font=L.MONO)
        say(300, y, doing, BODY)
        say(660, y, skill, CODE, font=L.MONO)
        y += 36
    xr, yr = 1100, 260
    rect(xr, yr, 700, 470, bold=True)
    say(xr + 24, yr + 18, f"SKILL  /haipipe-report  {versions['report']}", HEAD)
    say(xr + 24, yr + 56, "skills/1_base/project/haipipe-report", CODE, font=L.MONO)
    yy = yr + 110
    for s in ["owns the row's Work link and Report cell,", "the walk, the Page's header and divisions,",
              "its figures and its check"]:
        yy = say(xr + 24, yy, s, BODY)
    yy += 24
    for s in ["build_report_drawing.py <report folder>", "check_report.py <level folder>"]:
        yy = say(xr + 24, yy, s, CODE, font=L.MONO) + 4
    yy += 20
    for s in ["Runs: run-report-<qNN> · run-figures-<qNN>", "· run-check-<qNN>"]:
        yy = say(xr + 24, yy, s, BODY)
    rect(xr, yr + 510, 700, 230)
    say(xr + 24, yr + 528, "Around it", HEAD)
    by = yr + 574
    for s in [f"haipipe-report {versions['question']} asks: the row, the folder",
              "haipipe-draft writes the report's prose",
              "haipipe-studio feeds it frames (s02)", "haipipe-delivery keeps the built files (s03)"]:
        by = say(xr + 24, by, s, BODY)
    say(0, max(y, yr + 740) + 60, "blue: the open one and the skill · gray: a button or a path · the rest as the "
                                  "screen draws it", 21)       # under it, ②'s badge
    L.close_frame(fr, pad=60)
    return fr


# ── still open, and the reference ───────────────────────────────────────────────────────────────
def face_opens():
    """[(n, words)] of the face's Open list, the settled ones left out: read on every build, never typed."""
    face = (HERE / "s05-report-workbench-skill.md").read_text(encoding="utf-8")
    block = re.search(r"(?ms)^Open\n-+\n(.*?)^\(write here", face).group(1)
    items = re.findall(r"(?ms)^(\d+)\. (.*?)(?=^\d+\. |\Z)", block)
    return [(int(n), " ".join(w.split())) for n, w in items if not w.startswith("Settled")]


def frame_open(qs, unread):
    fr = L.open_frame("Still open")
    y = say(0, 0, "Still open", T) + 20
    y = say(0, y, "the face's Open list, the settled ones left out; read on every build", SUB) + 20
    items = [f"{n}. {words}" for n, words in face_opens()]
    for tag, text in unread:
        items.append(f"{tag}'s Feeds line names a Question without its folder name ({text.strip('`. ')}), so "
                     f"the Report Space does not see it.")
    for item in items:
        y = say(0, y, wrap(item, 74), BODY, L.RED) + 16
    L.close_frame(fr, pad=60)
    return fr


def frame_reference(qs):
    fr = L.open_frame("This Block's Questions")
    y = say(0, 0, "For reference: this Block's Questions", T) + 6
    y = say(0, y, "read from board.md ## Questions, each report's answer-status, the topics' Feeds lines and runs/",
            SUB) + 30
    cx = {"id": 0, "Question": 100, "status": 900, "fed by (studio)": 1060, "Runs on it": 1430}
    for name, x in cx.items():
        say(x, y, name, HEAD)
    y += 44
    line([(0, y), (1900, y)], arrow=False)
    y += 12
    for q in qs:
        say(cx["id"], y, q["id"], CODE, font=L.MONO)
        say(cx["Question"], y, q["title"][:62] + ("…" if len(q["title"]) > 62 else ""), BODY)
        say(cx["status"], y, q["status"], BODY)
        say(cx["fed by (studio)"], y, " · ".join(q["fed"]) or "·", CODE, font=L.MONO)
        say(cx["Runs on it"], y, " · ".join(q["runs"]) or "·", CODE, font=L.MONO)
        if q["id"] == EXAMPLE:
            rect(-10, y - 6, 1920, 38, bold=True)
        y += 40
    line([(0, y), (1900, y)], arrow=False)
    L.close_frame(fr, pad=60)
    return fr


# ── the story ────────────────────────────────────────────────────────────────────────────────────
def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s05-report-workbench-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    frame = frame_module()
    qs, unread = questions(frame)
    space = report_space(frame)
    versions = {"report": version(SKILLS / "project/haipipe-report"),
                "question": version(SKILLS / "project/haipipe-report")}
    KEY_LINES.clear()
    story = [frame_story(qs), frame_screen(qs, space, versions)]     # Act 1: two frames, ① ② ③ were one idea
    themes, flow, mind = G.draw(frame)                # Acts 2 to 4, merged from s07 (JL 261012)
    G.KEYS.extend(KEY_LINES)                          # ②'s key line, boxed with the theme frames'
    below = [frame_open(qs, unread), frame_reference(qs),
             L.tools_frame("In Tools: haipipe-report",                # its skills' folders and code (JL 261011)
                           ["1_base/project/haipipe-report", "1_base/project/haipipe-report/"],
                           [("servers/workbench/frame.py", ["question_rows", "_report_cell", "_answering", "_opening"]),
                            ("servers/workbench/page_reader.py", ["page_document"])],
                           around=["haipipe-report asks: the row, the folder", "haipipe-draft writes the prose",
                                   "haipipe-studio feeds it frames (s02)", "haipipe-delivery keeps built files (s03)"],
                           note="its skills' folders and code, read from disk (JL)")]
    for fr in story + below:                          # every frame measured, as Acts 2 to 4 are (excalidraw-studio ⑥)
        G.badge(fr)
    live = [themes[t] for t in ("base", "work", "cowork", "labeling")]
    own = [themes[t] for t in ("paper", "insight", "design", "discovery")]
    G.acts([story, live, own, [flow, mind], below],
           ["Act 1 · What a report is, and where it shows",
            "Act 2 · The group bar is live: base, work, cowork, labeling",
            "Act 3 · Their own Report today: paper, insight, design, discovery",
            "Act 4 · How a group reaches it, and every part",
            "Act 5 · Still open, and for reference"],
           [["shows"], ["work adds\nthree", "cowork adds\nthree", "names\nguessed"],
            ["also draws\nits own"] * 3, ["every part,\nin one map"], []],
           [(story[0], live[0], "its Questions, in groups"), (live[0], own[0], "not on the bar yet"),
            (own[0], flow, "how a group gets there"), (flow, below[0], "what is still open")])

    top = story[0]["y"]
    L.text(0, top - 250, "s05 in one sentence: every level asks its own Questions, the Work that answers one names it, "
                         "the report says the answer, open → partial → answered ①; the Report Space shows each row "
                         "while /haipipe-report writes and checks it ②; and every theme groups them on one bar ③ ④.", 40)
    L.text(0, top - 180, "Read left to right along the arrows, act by act, then down.", BODY)
    for k, (what, when) in enumerate((("new topic, the Report from both sides, in the screen's order: s02 Studio · "
                                       "s03 Delivery · s04 Related · s05 Report · s06 Run (JL)", TODAY),
                                      ("s07 merged in: its frames are Acts 2 to 4 (JL)", "261012"),
                                      ("Act 1: four frames merged into ① and ②, in colour; ⑤ ⑥ are now ③ ④ (JL)",
                                       "261012"))):
        L.els.append(canvas.change_note(0, top - 130 + k * 26, what, when, None, size=18))
    canvas.colour_ui(L.els)                           # the screens in the workbench's colours, then the font
    canvas.apply_font(L.els)
    G.key_boxes()
    for e in canvas.off_palette(L.els):
        if not (e.get("backgroundColor") == G.KEY or {"ui_kind", "s05_colour"} & set(e.get("customData") or {})):
            print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, list(L.els), "build_s05_report_workbench_skill.py", palette=False)   # keeps the key colour


if __name__ == "__main__":
    main()
