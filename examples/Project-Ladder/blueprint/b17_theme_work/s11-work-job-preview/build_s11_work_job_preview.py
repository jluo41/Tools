"""b17-s11:theme_work @ job_page_view, its drawing: one zoom from the Block to a Task's folds, left to right, each step
a click (JL 261125: "we select Job in the view bottom and that job can have its own sub view buttom list, and then each
task view buttom can have a list of task folder ... task then can have the fold"). The Jobs, Tasks and Runs are read
from disk on every build, so the drawing follows j03 as it grows.

    python build_s11_work_job_preview.py      writes s11-work-job-preview.excalidraw and its .png
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
KIT = TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts"
sys.path.insert(0, str(KIT))
from quick_draw import SEM, arrow, box, heading, life_line, text, write  # noqa: E402
from quick_draw import line as line_, dot as dot_, TITLE as TITLE_, BODY as BODY_  # noqa: E402

BLOCK = HERE.parent
JOB, TASK = "j11", "t02"                                 # the Job and Task the drawing opens: the one that builds this view


def kids(folder: Path, mark: str) -> list:
    return sorted(p for p in folder.iterdir() if p.is_dir() and p.name.startswith(mark) and p.name[1:3].isdigit())


def short(name: str, n: int = 26) -> str:
    key, _, rest = name.partition("_")
    rest = rest.replace("_", " ")
    return (f"{key} · {rest}")[:n]


def column(cid, x, y, title, rows, picked, w=250, h=46, gap=14, sem_on="start", faded=()):
    els = text(f"{cid}_h", x, y - 40, title, 18, SEM["decision"][1])
    for i, label in enumerate(rows):
        if label == "|":                                  # the line between two decades of Jobs
            els += line_(f"{cid}_div{i}", [(x + 20, y + i * (h + gap) + h / 2), (x + w - 20, y + i * (h + gap) + h / 2)])
            continue
        els += box(f"{cid}_{i}", x, y + i * (h + gap), w, h, label, sem_on if i == picked else "none" if i in faded else "plain",
                   16, dashed=i in faded)
    return els


def decades(jobs: list) -> list:
    """The Jobs as their buttons read: the newest decade first (j1N before j0N), a "|" between decades."""
    groups = {}
    for j in jobs:
        groups.setdefault(j.name[1], []).append(j)
    out = []
    for k in sorted(groups, reverse=True):
        out += (["|"] if out else []) + groups[k]
    return out


def row(cid, x, y, labels, picked=-1, faded=(), size=13, h=30, switch="", words=False):
    """One row of view buttons as they read on the page; "|" is the line between groups."""
    els = []
    for i, lab in enumerate(labels):
        if lab == "|":
            els += line_(f"{cid}_d{i}", [(x + 4, y + 2), (x + 4, y + h - 2)])
            x += 14
            continue
        if lab.startswith("~"):                           # a decade's topic: a small grey word inside the row
            els += text(f"{cid}_w{i}", x, y + 8, lab[1:], 11)
            x += len(lab) * 11 * 0.62 + 8
            continue
        w = len(lab) * size * 0.62 + 22
        if words:                                         # a topic: a word, the picked one underlined (as on the page)
            els += text(f"{cid}_{i}", x, y + 6, lab, size, TITLE_ if i == picked else BODY_)
            if i == picked:
                els += line_(f"{cid}_u{i}", [(x, y + h - 4), (x + w - 22, y + h - 4)], TITLE_, 2)
            x += w + 4
            continue
        els += box(f"{cid}_{i}", x, y, w, h, lab, "plain" if i == picked else "none", size, dashed=i in faded)
        x += w + 8
    if switch:                                            # the mark that switches flat and topics; its hover names it
        els += box(f"{cid}_sw", x + 6, y + 6, h - 12, h - 12, "", "decision", 10)
        els += text(f"{cid}_swt", x + h + 2, y + 8, switch, 12, SEM["decision"][1])
    return els


def panel(cid, x, y, w, title, folds):
    """The picked view's content: its bands and folds in a frame, the open dot on the top-right corner."""
    els = box(cid, x, y, w, 40 + 44 * len(folds), "", "none")
    els += text(cid + "_h", x + 14, y + 10, title, 14, SEM["decision"][1])
    for i, f in enumerate(folds):
        els += box(f"{cid}_f{i}", x + 14, y + 36 + 44 * i, w - 28, 34, f, "end" if "Runs" in f else "plain", 13)
    return els + dot_(cid + "_open", x + w, y, 6)


def wire(y0: float) -> list:
    """The UI itself, twice: FEW is b17 today; MANY is the same rule when Jobs and Tasks grow, a decade becoming a
    topic button (board.md's bands: names it) above the Jobs, and a Task decade above the Tasks."""
    jobs = [j for j in decades(kids(BLOCK, "j")) if j != "|"]
    job = next(j for j in jobs if j.name.startswith(JOB))
    tasks = kids(job, "t")
    pick = next(i for i, t in enumerate(tasks) if t.name.startswith(TASK))
    jl = []
    for j in decades(kids(BLOCK, "j")):
        jl.append("|" if j == "|" else short(j.name, 30))
    faded = {i for i, j in enumerate(decades(kids(BLOCK, "j"))) if j != "|" and j.name[1] < job.name[1]}
    els = text("few_h", 0, y0, "FEW · b17 today: Jobs, then Main and the Tasks, then the picked one's folds", 18, TITLE_)
    els += row("few_j", 0, y0 + 40, jl, 0, faded)
    els += row("few_t", 0, y0 + 82, ["Main"] + [short(t.name, 24) for t in tasks], 1 + pick)
    els += panel("few_p", 0, y0 + 130, 760, f"{short(tasks[pick].name, 30)}",
                 ["1 · Goal", "2 · Requirements", "1 · Runs", "2 · Interactions (waits on you)"])
    x, y0 = 0, y0 + 130 + 40 + 44 * 4 + 70               # MANY under FEW, so the rows never meet
    els += text("many_h", x, y0, "MANY · four rows: Job topic, Job view, Task topic, Task view; full names", 18, TITLE_)
    els += row("many_g", x, y0 + 40, ["Workbench · j1N", "Paper · j2N", "Earlier · j0N"], 0, {2}, words=True)
    els += row("many_j", x, y0 + 82, ["j11 · Workbench page", "j12 · Side pane", "j13 · Tools", "j14 · Home", "j15 · Guide"], 0)
    els += row("many_s", x, y0 + 124, ["Main"], 0) + row("many_s2", x + 70, y0 + 124, ["Build · t0N", "Check · t1N"], 0, words=True)
    els += row("many_t", x, y0 + 166, ["t01 · Read the brief", "t02 · Plan the page", "t03 · Draw the views", "t04 · Build the frame",
                                       "t05 · Wire the marks"], 1)
    els += panel("many_p", x, y0 + 214, 760, "t02 · Plan the page", ["1 · Goal", "1 · Runs", "2 · Interactions"])
    return els


def build() -> list:
    jobs = decades(kids(BLOCK, "j"))
    job = next(j for j in jobs if j != "|" and j.name.startswith(JOB))
    tasks = kids(job, "t")
    task = next(t for t in tasks if t.name.startswith(TASK))
    runs = sorted(p.name for p in (task / "runs").iterdir() if p.is_dir()) if (task / "runs").is_dir() else []
    shown = runs or ["no Run yet"]
    old = {i for i, j in enumerate(jobs) if j != "|" and j.name[1] < job.name[1]}   # an earlier decade reads faded
    els = heading("s11 · Job page view: a Job worked on inside its Block",
                  "each step is one click; the picked one (orange) opens the next")
    y, step = 160, 290
    els += box("block", 0, y, 200, 70, "b17\nJobs", "plain", 18)
    jrow = jobs.index(job)
    els += column("jobs", step, y, "1 · a Job", ["|" if j == "|" else short(j.name) for j in jobs], jrow,
                  faded=old)
    sub_rows = ["Main"] + [short(t.name) for t in tasks]
    srow = 1 + tasks.index(task)
    els += column("subs", 2 * step, y, "2 · Main or a Task", sub_rows, srow)
    fx, fy = 3 * step + 10, y
    els += text("page_h", fx, fy - 40, "3 · its folds", 18, SEM["decision"][1])
    els += box("page", fx, fy, 300, 90 + 26 * len(shown) + 70, "", "none", 16)
    els += box("f1", fx + 15, fy + 15, 270, 40, "▸ Goal", "plain", 15)
    els += box("f2", fx + 15, fy + 65, 270, 30 + 26 * len(shown), "", "end", 15)
    els += text("f2_t", fx + 30, fy + 72, "▾ Runs", 15, SEM["end"][1])
    for i, r in enumerate(shown):
        els += text(f"run_{i}", fx + 45, fy + 98 + i * 26, r[:34], 13)
    els += box("f3", fx + 15, fy + 80 + 26 * len(shown) + 30, 270, 40, "▸ Interactions (waits on you)", "decision", 15)
    hop = [((200, y + 35), (step, y + 23 + 60 * jrow)),
           ((step + 250, y + 23 + 60 * jrow), (2 * step, y + 23 + 60 * srow)),
           ((2 * step + 250, y + 23 + 60 * srow), (fx, y + 23))]
    for i, (a, b) in enumerate(hop):
        els += arrow(f"hop{i}", [a, b], SEM["start"][1])
    els += text("dots", fx, fy + 90 + 26 * len(shown) + 90, "• open the Task on its own page (top-right dot)", 14)
    els += text("rule", step, y + 60 * len(jobs) + 10, "one line each · a line between decades\nan earlier decade or a closed Job reads faded", 14)
    ly = y + 60 * max(len(jobs), len(sub_rows)) + 140
    return els + life_line("shaping", 0, ly) + wire(ly + 160)


if __name__ == "__main__":
    out = write(HERE / f"{HERE.name}.excalidraw", build())
    subprocess.run([sys.executable, str(KIT / "render_png.py"), str(out), str(out.with_suffix(".png"))], check=True)
    print(out, out.with_suffix(".png"))
