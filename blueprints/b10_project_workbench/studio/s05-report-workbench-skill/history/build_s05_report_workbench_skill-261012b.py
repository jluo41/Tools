"""s05 · Report: its workbench and its skill: s05-report-workbench-skill.excalidraw (haipipe-studio).

Three frames, each a folder tree (JL 261012: "每一个 frame 都太像一张 slide ... 我个人更 prefer 那种 tree 结构"):
① Background, a newcomer's frame; ② the Tree, the whole topic as one folder tree (every level reports, work names
its Question, the report says the answer, the Report Space, the skill in Tools, the Questions by state, red ?
leaves where it is still open); ③ the Report Space screen, in the workbench's colours (canvas.ui_frame).
The 261011 builder (four frames in a row, plus three below) is in history/.

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

TODAY = "261012"
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


# ── folder-tree helpers ──────────────────────────────────────────────────────────────────────────
def rect(x, y, w, h, bold=False, dashed=False):
    return L.base("rectangle", x, y, w, h, L.INK, 3 if bold else 1.5, dashed, rough=0)


def say(x, y, s, size=BODY, color=L.INK, font=L.SANS):
    L.text(x, y, s, size, color, font)
    return y + size * 1.3 * (s.count("\n") + 1)


def wrap(s, n):
    return "\n".join(textwrap.wrap(s, n))


def tree_frame(name, title, lines, nodes, width, cols):
    """One frame: a title, a line or two under it, then the folder tree (canvas.tree)."""
    fr = L.open_frame(name)
    L.text(0, 0, title, 34)
    y = 56
    for ln in lines:
        L.text(0, y, ln, 22)
        y += 32
    els, _ = canvas.tree(0, y + 8, nodes, width, fr["id"], size=20, head=24, cols=cols)
    L.els.extend(els)
    L.close_frame(fr)
    return fr


def skill_folder(skill):
    """A skill's folder as it is on disk: [name, {dir: [files]}] children for canvas.tree."""
    kids = []
    for p in sorted(skill.iterdir()):
        if p.name.startswith((".", "__")):
            continue
        if p.is_dir():
            kids.append({p.name + "/": [c.name for c in sorted(p.iterdir()) if not c.name.startswith((".", "__"))][:6]})
        else:
            kids.append(p.name)
    return kids


def where(fn, file):
    """'fn  (file)' when `def fn` is in the file, else a red ? leaf."""
    text = file.read_text(encoding="utf-8") if file.is_file() else ""
    return f"{fn}  ({file.name})" if re.search(rf"def {re.escape(fn)}\b", text) else f"? {fn} not found in {file.name}"


# ── ① Background ─────────────────────────────────────────────────────────────────────────────────
def background(qs):
    jobs = [p for p in BLOCK.glob("j[0-9]*_*/") if p.is_dir()]
    return [
        {"What this topic is": [
            "the Report seen from both sides: its workbench (the Report Space) and its skill",
            "a report is a Page that answers one Question of its level",
            "unlike Studio, Delivery and Related, every level keeps its own reports (as it keeps its Runs, s06)"]},
        {"The words": [
            "Question: asked in a level's face (a Block's board.md ## Questions), id qNN",
            "Work: a Job or a Task that says answers: Q01, or one need of it, Q01.E2",
            "Report: reports/qNN_<topic>/qNN_<topic>.md, answer-status open, partial or answered",
            "Report Space: the screen with one folding card per Question under a group bar",
            "/haipipe-report: the skill that writes, checks and draws a report"]},
        {"Where it sits": [
            "in the Spaces row, after s02 Studio, s03 Delivery, s04 Related; before s06 Run",
            {"Block / Job / Task": ["reports/qNN_<topic>/", "jNN_<job>/reports/qNN_<topic>/",
                                    "tNN_<task>/reports/qNN_<topic>/"]},
            f"this Block today: {len(qs)} Questions, {len(jobs)} Jobs, so no Job or Task report yet"]},
    ]


# ── ② the Tree ───────────────────────────────────────────────────────────────────────────────────
def tree_nodes(qs, unread, space, versions):
    subs, opened, heads, buttons = space
    q = next(x for x in qs if x["id"] == EXAMPLE)
    by_state = [{f"{st}  ({sum(1 for x in qs if x['status'] == st)})":
                 [f"{x['id']}  {x['title']}"[:70] for x in qs if x["status"] == st]} for st in STATES]
    figs = [f"{t}  >  \"{n}\"" for t, n in figures()]
    fn = SERVERS / "workbench/frame.py"
    still = [
        "? What must each level's report answer? The Studio sets it, each level reports (s09 Open 2).",
        "? List Job and Task reports in the Block's Report, by source (s09-D08), once a Job has one?",
        "? Show the level's own Runs on a Question in its Work cell too?",
        "? Ideation and Narrative list studio topics inside Report; s02-D05 keeps Studio apart: link out?",
        "? A Task without Questions shows its own face as its report: which reports/qNN_<topic>/ then?",
        "? When a cited studio frame changes, flag the report for review before its answer changes?",
    ]
    for tag, text in unread:
        still.append(f"? {tag}'s Feeds line names a Question without its folder name ({text.strip('`. ')}), "
                     "so the Report Space does not see it.")
    return [
        {"1 Every level reports": [
            {"Studio (the centre, s09-D01)": ["sets what each level reports"]},
            {"Block": ["reports/qNN_<topic>/"]}, {"Job": ["jNN_<job>/reports/qNN_<topic>/"]},
            {"Task": ["tNN_<task>/reports/qNN_<topic>/"]},
            "the Question and its report share one id, qNN (s02-D30)",
            "built pdf or docx goes to the Block's delivery/reports/qNN_<topic>/ (s03)",
            "? the Block's Report lists only its own reports/; s09-D08 says Job and Task reports too (not built)"]},
        {"2 Work names its Question": [
            {"studio topic": ["**Feeds:** qNN_<topic>"]},
            {"Job": ["answers: Q01"]}, {"Task": ["answers: Q01.E2, Q04"]},
            {f"{q['id']}  {q['title']}"[:60]: [
                "fed by: " + (" · ".join(q["fed"]) or "no topic"),
                "Jobs and Tasks: " + (" · ".join(str(w) for w in q["work"]) or "none (this Block has no Jobs)"),
                "Runs on it: " + (" · ".join(q["runs"]) or "none"),
                "report: " + (f"{q['report'].relative_to(BLOCK)} · {q['status']}" if q["report"] else "none"),
                *([f"? its Work cell says \"no work yet\": the row lists Jobs and Tasks, not the Runs on "
                   f"{q['id']} ({', '.join(q['runs'])})"] if q["runs"] and not q["work"] else [])]},
            "an id the register does not have is an error: check_report.py finds it"]},
        {"3 The report says the answer": [
            {"open": ["asked, no answer yet"]},
            {"partial": ["some Work answers part; the report says which"]},
            {"answered": ["the Opening states it; Evidence links the Results"]},
            "checked is not a fourth state: the CHECK verdict shows beside answered (s21-D04)",
            {"reports/qNN_<topic>/": ["qNN_<topic>.md  (answers: · answer-status: · results-read:)",
                                      "  ## Opening, Answer, Evidence, Limits, Next",
                                      "qNN_<topic>.excalidraw  (generated from ## Figures)", "draft/"]},
            {f"drawing of {FIGURES}, from studio frames": figs + ["build_report_drawing.py: change a frame, rebuild"]},
            "a frame's name is the contract: rename it and every report citing it fails its build (s02-D24)",
            "✎ 261011 q01 now cites s06's \"Hard or soft\" and \"For reference\""]},
        {"4 The Report Space (frame 3)": [
            {"one folding card per Question": ["under a group bar: Current, the groups, Untagged, + Group (s07-D09)"]},
            {"open card, Logic · Work · Report": [h for h in heads] or ["row heads read from frame.py"]},
            {"Runs panel buttons": [f"{b[0]}  {b[1]}  ({b[2]})" for b in buttons]}]},
        {"5 In Tools": [
            {f"haipipe-report  {versions['report']}": skill_folder(SKILLS / "project/haipipe-report")},
            {f"haipipe-report  {versions['question']}": skill_folder(SKILLS / "project/haipipe-report")[:5]},
            {"servers/workbench/": [where(f, fn) for f in ("question_rows", "_report_cell", "_answering", "_opening")]
                                   + [where("page_document", SERVERS / "workbench/page_reader.py")]},
            "haipipe-draft writes the prose; haipipe-studio feeds frames (s02); haipipe-delivery keeps built files (s03)"]},
        {f"6 This Block's {len(qs)} Questions": by_state},
        {"7 Still open": still},
    ]


# ── ③ the Report Space, as it looks ──────────────────────────────────────────────────────────────
def screen_frame(qs, frame):
    sp = frame.spaces_for(frame.VANILLA, "Block", BLOCK, ROOT)["Audience Report"]
    html = sp.html
    nav = re.search(r"<nav.*?</nav>", html, re.S)
    groups = re.findall(r'data-studio-label="([^"]+)"[^>]*>.*?</span>.*?<span class=tag-count>(\d+)</span>',
                        nav.group(0), re.S) if nav else []
    cards = re.findall(r'<span class="q-dot (\w+)" title="\w+"></span><span class=related-head><b>(.*?)</b>'
                       r'.*?<span class=topic-meta>(.*?)</span>', html, re.S)
    fr = L.open_frame("The Report Space on screen")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    say(0, 0, f"Block {BLOCK.name.split('_')[0]} > Report  (read from servers/workbench/frame.py)", 34)
    say(0, 56, "One folding card per Question, under a group bar; the Runs panel sits beside it.", 22)
    x, y = 0, 120
    for label, n in groups + [("Untagged", ""), ("+ Group", "")]:
        t = f"{label} {n}".strip()
        w = int(len(t) * BODY * 0.58) + 40
        rect(x, y, w, 46, bold=label == "Current")
        say(x + 20, y + 10, t, BODY)
        x += w + 12
    y += 80
    for dot, title, meta in cards[:6]:
        rect(0, y, 1500, 64)
        say(24, y + 8, f"{dot}   {title}", BODY)
        say(24, y + 36, re.sub("<.*?>", "", meta), 18, L.MONO and L.INK)
        y += 76
    say(0, y + 4, f"... {len(cards)} cards in all; Q05 opened below", BODY)
    y += 50
    q = next(x for x in qs if x["id"] == EXAMPLE)
    rect(0, y, 1500, 330, bold=True)
    for c, h in zip((24, 520, 1000), ("Logic · the question", "Work · the Jobs, Tasks and Runs", "Report · what it says")):
        say(c, y + 14, h, HEAD)
    cells = [f"{q['id']} · {q['status']}\n" + wrap(q["title"], 34) + "\nfrom the Studio:\n" + " · ".join(q["fed"]),
             "no work yet" if not q["work"] else "\n".join(map(str, q["work"])),
             (q["report"].stem + "\nits answer line, its drawing, live\n" + f"report {q['id'].lower()} · {q['status']}")
             if q["report"] else "No report yet"]
    for c, s in zip((24, 520, 1000), cells):
        say(c, y + 60, s, BODY, L.RED if s == "no work yet" else L.INK)
    y += 370
    say(0, y, "Runs panel, beside the Report Space", HEAD)
    y += 44
    for b in sp.run_types:
        say(0, y, b["label"], CODE, font=L.MONO)
        say(340, y, b.get("doing", ""), BODY)
        say(720, y, " · ".join(b.get("skills") or []), CODE, font=L.MONO)
        y += 36
    L.close_frame(fr, pad=60)
    return fr


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s05-report-workbench-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    frame = frame_module()
    qs, unread = questions(frame)
    space = report_space(frame)
    versions = {"report": version(SKILLS / "project/haipipe-report"),
                "question": version(SKILLS / "project/haipipe-report")}
    ui = screen_frame(qs, frame)
    bg = tree_frame("Background: the Report", "Background: the Report, for a newcomer",
                    ["What the topic is about, the words it uses, and where it sits. The topic itself is the Tree."],
                    background(qs), 1500, 1)
    tree = tree_frame("The Tree: Report, workbench and skill", "The Report: its workbench and its skill",
                      ["Every level reports, work names its Question, the report says the answer, the Space shows "
                       "it, the skill keeps it; red ? leaves are still open."],
                      tree_nodes(qs, unread, space, versions), 2600, 4)
    canvas.grid(L.els, [[bg["id"], tree["id"]], [ui["id"]]])
    for e in canvas.off_palette(L.els):
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, list(L.els), "build_s05_report_workbench_skill.py")


if __name__ == "__main__":
    main()
