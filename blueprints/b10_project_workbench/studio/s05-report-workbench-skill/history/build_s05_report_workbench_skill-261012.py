"""s05 · Report: its workbench and its skill: s05-report-workbench-skill.excalidraw, one story read left to right
(JL 261011: "s02 studio, s03 delivery, and s04 related, and s05 report, and s06 run"; drawn the way s06 is):

    ① every level reports  -->  ② work names its Question  -->  ③ the report says the answer  -->  ④ the Report
                                                                                                   Space shows it,
                                                                                                   /haipipe-report
                                                                                                   keeps it
    still open (red)            this Block's Questions (reference)

Read from disk on every build: this Block's Questions (board.md ## Questions), each report's answer-status,
which studio topics feed each Question (their **Feeds:** lines, read as frame.py reads them), the Runs that
target a Question (runs/*/run.yaml), q01's ## Figures, the Report Space as servers/workbench/frame.py draws
it for this Block, and haipipe-report's version. Typed, since they are the design: the level tree of ①, the
link rule of ②, the walk of ③, the open points.

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
    heads = re.findall(r'q-head-row"><div>(.*?)</div><div>(.*?)</div><div>(.*?)</div>', sp.html)
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
    say(0, 0, f"{n} {title}", T)
    return say(0, 58, under, SUB)


def card(x, y, w, h, title, body, bold=False, code=""):
    rect(x, y, w, h, bold=bold)
    say(x + 22, y + 16, title, HEAD)
    yy = y + 58
    if code:
        yy = say(x + 22, yy, code, CODE, font=L.MONO) + 4
    if body:
        say(x + 22, yy, body, BODY)


# ── ① every level reports ────────────────────────────────────────────────────────────────────────
def frame_levels(qs):
    fr = L.open_frame("Every level reports")
    y = heading("①", "Every level reports",
                "The Studio, at the Block, sets what to report; Block, Job and Task each answer their own Questions.") + 40
    card(520, y, 640, 130, "STUDIO   the centre, one per Block", "", bold=True, code="studio/sNN-<topic>/")
    say(1180, y + 30, "(s09-D01)", BODY)
    say(1180, y + 74, "↓ sets what each level reports", BODY)
    top = y + 130 + 90
    levels = [("BLOCK", "reports/qNN_<topic>/"), ("JOB", "jNN_<job>/reports/qNN_<topic>/"),
              ("TASK", "tNN_<task>/reports/qNN_<topic>/")]
    for i, (lv, path) in enumerate(levels):
        x = i * 570
        line([(840, y + 130), (x + 270, top)])
        card(x, top, 540, 130, f"{lv}   its own Questions", "", code=path)
    y = top + 160
    y = say(0, y, "A reader goes to the level to read its report (s09-D02, s09-D08).", BODY) + 40
    say(0, y, "What a report is", HEAD)
    y += 46
    for k, s in enumerate(["a Page that answers one Question: reports/qNN_<topic>/qNN_<topic>.md",
                           "the Question and its report share one id, qNN (s02-D30)",
                           "the Question is asked in the level's face: board.md ## Questions, for a Block",
                           "its built pdf or docx goes to the Block's delivery/reports/qNN_<topic>/ (s03)"], 1):
        y = say(0, y, f"{k}  {s}", BODY) + 4
    y += 36
    say(0, y, f"This Block today, read from board.md and reports/: {len(qs)} Questions, "
              f"{sum(1 for q in qs if q['report'])} reports", HEAD)
    y += 56
    for i, st in enumerate(STATES):
        ids = [q["id"] for q in qs if q["status"] == st]
        x = i * 570
        rect(x, y, 540, 120, bold=st == "answered")
        say(x + 22, y + 16, f"{st}   {len(ids)}", HEAD)
        say(x + 22, y + 60, wrap(" · ".join(ids), 40) or "none", CODE, font=L.MONO)
    y += 150
    jobs = [p for p in BLOCK.glob("j[0-9]*_*/") if p.is_dir()]
    say(0, y, wrap(f"? this Block has {len(jobs)} Jobs, so no Job or Task report yet; and the Block's Report lists "
                   "only its own reports/, while s09-D08 says it lists Job and Task reports by source too (not built).",
                   120), BODY, L.RED)
    L.close_frame(fr, pad=60)
    return fr


# ── ② work names its Question ────────────────────────────────────────────────────────────────────
def frame_link(qs):
    fr = L.open_frame("Work names its Question")
    y = heading("②", "Work names its Question",
                "A Job or a Task says on its own face which Question it answers; a studio topic says which it feeds.") + 40
    cols = (0, 640, 1240)
    for c, h in zip(cols, ("feeds it", "the Question", "answers it")):
        say(c, y, h, HEAD)
    y += 50
    card(0, y, 560, 120, "STUDIO TOPIC", "", code="sNN-<topic>.md\n**Feeds:** qNN_<topic>")
    card(640, y + 90, 520, 150, "QUESTION  qNN", "board.md ## Questions:\nid · title · acceptance", bold=True)
    card(1240, y, 560, 120, "JOB", "", code="jNN_<job>.md\nanswers: Q01")
    card(1240, y + 160, 560, 120, "TASK", "", code="tNN_<task>.md\nanswers: Q01.E2, Q04")
    card(1240, y + 320, 560, 120, "REPORT", "", code="reports/q01_<topic>/\nanswer-status: partial")
    line([(565, y + 60), (635, y + 150)])
    for yy in (y + 60, y + 220, y + 380):
        line([(1235, yy), (1165, y + 165)])
    say(1240, y + 450, "Q01.E2 = one need (an Evidence Item) of Q01; it counts for Q01.", BODY)
    y += 520
    q = next(x for x in qs if x["id"] == EXAMPLE)
    say(0, y, f"In this Block: {q['id']} · {q['title']}", HEAD)
    y += 50
    rows = [("fed by", " · ".join(q["fed"]) or "no topic"),
            ("Jobs and Tasks", " · ".join(str(w) for w in q["work"]) or "none (this Block has no Jobs)"),
            ("Runs on it", " · ".join(q["runs"]) or "none"),
            ("report", f"{q['report'].relative_to(BLOCK) if q['report'] else 'none'} · {q['status']}")]
    for k, (a, b) in enumerate(rows):
        say(0, y + k * 36, a, BODY)
        say(260, y + k * 36, b, CODE, font=L.MONO)
    y += 4 * 36 + 30
    if q["runs"] and not q["work"]:
        y = say(0, y, wrap(f"? its Work cell on screen says \"no work yet\": the row lists Jobs and Tasks, not this "
                           f"level's own Runs on {q['id']} ({', '.join(q['runs'])}).", 110), BODY, L.RED) + 10
    say(0, y, "An id the register does not have is an error: check_report.py finds it.", BODY)
    L.close_frame(fr, pad=60)
    return fr


# ── ③ the report says the answer ─────────────────────────────────────────────────────────────────
PAGE = [("reports/qNN_<topic>/", ""),
        ("├── qNN_<topic>.md", "answers: · answer-status: · results-read:"),
        ("│     ## Opening", "states the answer, in one paragraph"),
        ("│     ## Answer · Evidence · Limits · Next", ""),
        ("├── qNN_<topic>.excalidraw", "generated from ## Figures, never by hand"),
        ("└── draft/", "the Page flow's versions")]


def frame_answer(qs):
    fr = L.open_frame("The report says the answer")
    y = heading("③", "The report says the answer",
                "open → partial → answered; its writer moves it, never a Run that finishes alone.") + 50
    bw, gap = 420, 90
    for i, st in enumerate(STATES):
        x = i * (bw + gap)
        n = sum(1 for q in qs if q["status"] == st)
        what = {"open": "asked, no answer yet", "partial": "some Work answers part;\nthe report says which",
                "answered": "the Opening states it;\nEvidence links the Results"}[st]
        card(x, y, bw, 150, f"{st}   ({n} here)", what, bold=st == "answered")
        if i < 2:
            line([(x + bw + 8, y + 75), (x + bw + gap - 8, y + 75)])
    say(0, y + 170, "checked is not a fourth state: the Page's CHECK verdict shows beside answered (s21-D04).", BODY)
    y += 240
    say(0, y, "The report Page", HEAD)
    y += 46
    for k, (path, what) in enumerate(PAGE):
        say(0, y + k * 32, path, CODE, font=L.MONO)
        if what:
            say(640, y + k * 32 + 1, what, BODY)
    y += len(PAGE) * 32 + 40
    say(0, y, f"Its drawing, from studio frames: {FIGURES}", HEAD)
    y += 46
    for k, (topic, name) in enumerate(figures()):
        say(0, y + k * 32, f"{topic}  ›  \"{name}\"", CODE, font=L.MONO)
    n = len(figures())
    line([(1100, y + n * 16), (1240, y + n * 16)])
    card(1250, y - 20, 470, 130, "build_report_drawing.py", "one drawing, generated;\nchange a frame, rebuild")
    y += n * 32 + 20
    note(0, y, "q01 now cites s06's \"Hard or soft\" and \"For reference\"")
    y += 50
    say(0, y, wrap("A frame's name is the contract: rename a studio frame and every report citing it fails its "
                   "build with the names it finds (s02-D24).", 110), BODY)
    L.close_frame(fr, pad=60)
    return fr


# ── ④ the Report Space shows it, the skill keeps it ──────────────────────────────────────────────
def frame_screen(qs, space, versions):
    subs, opened, heads, buttons = space
    fr = L.open_frame("Workbench and skill")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    y = heading("④", "The Report Space shows it; /haipipe-report keeps it",
                "One row per Question; its four buttons name haipipe-question and haipipe-report.") + 40
    say(0, y, f"On screen: Block {BLOCK.name.split('_')[0]} › Report  (read from frame.py)", HEAD)
    y += 50
    x = 0
    for s in subs:                                                # the third row
        w = int(len(s) * BODY * 0.55) + 40
        rect(x, y, w, 46, bold=s == opened)
        say(x + 20, y + 10, s, BODY)
        x += w + 12
    y += 76
    cw = (330, 300, 360)
    xs = (0, cw[0] + 10, cw[0] + cw[1] + 20)
    for c, w, h in zip(xs, cw, heads):
        say(c, y, wrap(h, 22), BODY)
    y += 70
    q = next(x for x in qs if x["id"] == EXAMPLE)
    cells = [f"{q['id']} · {q['status']}\n" + wrap(q["title"], 22) + "\nfrom the Studio:\n" + " ↗ ".join(q["fed"]) + " ↗",
             "no work yet" if not q["work"] else "\n".join(map(str, q["work"])),
             (q["report"].stem + " ↗\nits answer line\nits drawing, live\n" + f"report {q['id'].lower()} · {q['status']}")
             if q["report"] else "No report yet"]
    for c, w, s in zip(xs, cw, cells):
        rect(c, y, w, 210)
        say(c + 16, y + 14, s, BODY, L.RED if s == "no work yet" else L.INK)
    y += 240
    say(0, y, "Runs panel, beside the Report Space (read from frame.py)", HEAD)
    y += 46
    for label, doing, skill in buttons:
        say(0, y, label, CODE, font=L.MONO)
        say(300, y, doing, BODY)
        say(660, y, skill, CODE, font=L.MONO)
        y += 36
    xr, yr = 1100, 140
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
    for s in [f"haipipe-question {versions['question']} asks: the row, the folder",
              "haipipe-draft writes the report's prose",
              "haipipe-studio feeds it frames (s02)", "haipipe-delivery keeps the built files (s03)"]:
        by = say(xr + 24, by, s, BODY)
    L.close_frame(fr, pad=60)
    return fr


# ── still open, and the reference ───────────────────────────────────────────────────────────────
def frame_open(qs, unread):
    fr = L.open_frame("Still open")
    y = say(0, 0, "Still open", T) + 20
    items = [
        "What must each level's report answer? The Studio sets it, each level reports (s09 Open 2).",
        "List Job and Task reports in the Block's Report, by source (s09-D08), once a Job has one?",
        "The Work column lists Jobs and Tasks only: show the level's own Runs on a Question too?",
        "Ideation and Narrative, on Report's third row, list studio topics; s02-D05 keeps Studio and "
        "Report apart: keep them, or link out to Studio? (proposed: to the Studio, s07-D05)",
        "A Task without Questions shows its own face as its report; s09-D08 gives a Task "
        "reports/qNN_<topic>/: which one? (proposed: its own result, s07-D06)",
        "When a cited studio frame changes, flag the report for review before its answer changes?",
        "The third row says \"High-level logic + Low-level work\", the row heads \"Logic · Work · Report\": "
        "one name? (proposed: the view becomes the plain list, s07-D05)",
    ]
    for tag, text in unread:
        items.append(f"{tag}'s Feeds line names a Question without its folder name ({text.strip('`. ')}), so "
                     f"the Report Space does not see it.")
    for k, item in enumerate(items, 1):
        y = say(0, y, wrap(f"{k}. {item}", 74), BODY, L.RED) + 16
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
                "question": version(SKILLS / "question/haipipe-question")}
    story = [frame_levels(qs), frame_link(qs), frame_answer(qs), frame_screen(qs, space, versions)]
    tall = max(f["height"] for f in story)
    for f in story:                                   # one strip: every chapter the same height
        f["height"] = tall
    below = [frame_open(qs, unread), frame_reference(qs),
             L.tools_frame("In Tools: haipipe-report",                # its skills' folders and code (JL 261011)
                           ["1_base/project/haipipe-report", "1_base/question/haipipe-question"],
                           [("servers/workbench/frame.py", ["question_rows", "_report_cell", "_answering", "_opening"]),
                            ("servers/workbench/page_reader.py", ["page_document"])],
                           around=["haipipe-question asks: the row, the folder", "haipipe-draft writes the prose",
                                   "haipipe-studio feeds it frames (s02)", "haipipe-delivery keeps built files (s03)"],
                           note="its skills' folders and code, read from disk (JL)")]
    canvas.grid(L.els, [[f["id"] for f in story], [f["id"] for f in below]], gap=260)

    top = story[0]["y"]
    L.text(0, top - 250, "s05 in one sentence: every level asks its own Questions ①, the Work that answers one names it "
                         "②, the report says the answer, open → partial → answered ③, and the Report Space shows each "
                         "row while /haipipe-report writes and checks it ④.", 40)
    L.text(0, top - 180, "Read left to right along the arrows. Below the strip: what is still open, and this Block's "
                         "twelve Questions.", BODY)
    for k, what in enumerate(("new topic, the Report from both sides, in the screen's order: s02 Studio · s03 "
                              "Delivery · s04 Related · s05 Report · s06 Run (JL)",)):
        L.els.append(canvas.change_note(0, top - 130 + k * 26, what, TODAY, None, size=18))
    for a, b, word in zip(story, story[1:], ("asks", "answers", "shows")):
        ay = a["y"] + 180
        x0, x1 = a["x"] + a["width"] + 20, b["x"] - 20
        line([(x0, ay), (x1, ay)])
        L.els[-1]["strokeWidth"] = 3
        L.text(x0 + 30, ay - 44, word, HEAD)
    first, ref = story[0], below[1]
    ax = max(first["x"] + first["width"] - 300, ref["x"] + 200)
    line([(ax, first["y"] + first["height"] + 20), (ax, ref["y"] - 20)], dashed=True)
    L.text(ax + 20, first["y"] + first["height"] + 90, "every Question", HEAD)
    for e in canvas.off_palette(L.els):
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, list(L.els), "build_s05_report_workbench_skill.py")


if __name__ == "__main__":
    main()
