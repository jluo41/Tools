"""s15 · Block Job UI Preview: Knowledge, its drawing: one zoom from the Block to a Task's folds, left to right, each
step a click. The Jobs, Tasks and Runs are read from disk on every build, so the drawing follows the Block as it grows.

    python build_s15_knowledge_job_preview.py      writes s15-knowledge-job-preview.excalidraw and its .png
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
KIT = TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts"
sys.path.insert(0, str(KIT))
from quick_draw import SEM, arrow, box, heading, life_line, text, write  # noqa: E402
from quick_draw import line as line_  # noqa: E402

BLOCK = HERE.parents[2] / "knowledge/b18_a2ui_learning"
JOB, TASK = "j01", "t01"                              # the Job and Task this preview opens
W, H, GAP, STEP = 250, 46, 14, 290


def kids(folder: Path, mark: str) -> list:
    return sorted(p for p in folder.iterdir() if p.is_dir() and p.name.startswith(mark) and p.name[1:3].isdigit())


def short(name: str, n: int = 26) -> str:
    key, _, rest = name.partition("_")
    return (f"{key} · {rest.replace('_', ' ')}")[:n]


def decades(jobs: list) -> list:
    """The Jobs as their buttons read: the newest decade first, a "|" between decades."""
    groups = {}
    for j in jobs:
        groups.setdefault(j.name[1], []).append(j)
    out = []
    for k in sorted(groups, reverse=True):
        out += (["|"] if out else []) + groups[k]
    return out


def column(cid, x, y, title, rows, picked, faded=()):
    els = text(f"{cid}_h", x, y - 40, title, 18, SEM["decision"][1])
    for i, label in enumerate(rows):
        top = y + i * (H + GAP)
        if label == "|":                                  # the line between two decades of Jobs
            els += line_(f"{cid}_div{i}", [(x + 20, top + H / 2), (x + W - 20, top + H / 2)])
            continue
        els += box(f"{cid}_{i}", x, top, W, H, label, "start" if i == picked else "none" if i in faded else "plain",
                   16, dashed=i in faded)
    return els


def build() -> list:
    jobs = decades(kids(BLOCK, "j"))
    job = next(j for j in jobs if j != "|" and j.name.startswith(JOB))
    tasks = kids(job, "t")
    task = next(t for t in tasks if t.name.startswith(TASK))
    runs = sorted(p.name for p in (task / "runs").iterdir() if p.is_dir()) if (task / "runs").is_dir() else []
    old = {i for i, j in enumerate(jobs) if j != "|" and j.name[1] < job.name[1]}   # an earlier decade reads faded
    els = heading("s15 · Knowledge Job page: a Job opened inside its Block",
                  "each step is one click; the picked one (orange) opens the next")
    y = 160
    els += box("block", 0, y, 200, 70, f"{BLOCK.name[:3]}\nJobs", "plain", 18)
    jrow = jobs.index(job)
    els += column("jobs", STEP, y, "1 · a Job", ["|" if j == "|" else short(j.name) for j in jobs], jrow, old)
    sub_rows = ["Main"] + [short(t.name) for t in tasks]
    srow = 1 + tasks.index(task)
    els += column("subs", 2 * STEP, y, "2 · Main or a Task", sub_rows, srow)
    fx, n = 3 * STEP + 10, max(len(runs), 1)
    els += text("page_h", fx, y - 40, "3 · its folds", 18, SEM["decision"][1])
    els += box("page", fx, y, 300, 120 + 26 * n, "", "none", 16)
    els += box("f1", fx + 15, y + 15, 270, 40, "▸ Goal", "plain", 15)
    els += box("f2", fx + 15, y + 65, 270, 30 + 26 * n, "", "end" if runs else "none", 15, dashed=not runs)
    els += text("f2_t", fx + 30, y + 72, "▾ Runs", 15, SEM["end"][1])
    for i, r in enumerate(runs):
        els += text(f"run_{i}", fx + 45, y + 98 + i * 26, r[:34], 13)
    mid = lambda row: y + H / 2 + (H + GAP) * row
    for i, (a, b) in enumerate([((200, y + 35), (STEP, mid(jrow))), ((STEP + W, mid(jrow)), (2 * STEP, mid(srow))),
                                ((2 * STEP + W, mid(srow)), (fx, y + 23))]):
        els += arrow(f"hop{i}", [a, b], SEM["start"][1])
    els += text("rule", STEP, y + (H + GAP) * len(jobs) + 10,
                "one line each · a line between decades\nan earlier decade reads faded", 14)
    return els + life_line("shaping", 0, y + (H + GAP) * max(len(jobs), len(sub_rows)) + 140)


if __name__ == "__main__":
    out = write(HERE / f"{HERE.name}.excalidraw", build())
    subprocess.run([sys.executable, str(KIT / "render_png.py"), str(out), str(out.with_suffix(".png"))], check=True)
    print(out, out.with_suffix(".png"))
