"""b17 s02 · Work skills: s02-work-skills.excalidraw, which of today's 1_base/task skills make the
work theme (2_theme/work) and which stay in base. Feeds reports/q04_work_skills.

Read from disk every build: the entries of skills/1_base/task with their skill counts, the
files outside 1_base/task that name each core skill (who calls it), and what 2_theme/work holds.
The proposed home of each entry is the one typed part (it is the proposal); open points are red.

Draws with b04's studio helpers (b04 owns skill moves) through b03's canvas.write, so a
person's marks survive a rebuild.

    python build_s02_work_skills.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'b01_haipipe-toolkit' / "j04_skill_folder" / "studio" / "_build"))
from sketch import (BLUE, GRAY, RED, SKILLS, TK, arrow, concern, legend, mono, questions_frame,  # noqa: E402
                    refs, save, skill_dirs, sticky, text, where_short)

TASK = SKILLS / "1_base" / "task"
WORK = SKILLS / "2_theme" / "work"
# the proposal: entry of 1_base/task -> its home ("?" = JL's call)
HOME = {"haipipe-task": "stays in 1_base/task (every theme calls it)",
        "haipipe-workflow": "1_base/project/ (beside haipipe-run)",
        "workbench-work": "2_theme/work/workbench-work (moved 261007)",
        "haipipe-work": "2_theme/work/haipipe-work (new door, 261007)",
        "agents": "? 2_theme/work/agents, or base (page, insight, paper call them)",
        "haipipe-page-task": "? 2_theme/work/ (the reader page of a work Task)",
        "page-types": "! leftover: holds only an empty scripts/ folder",
        "kinds": "2_theme/work/<N>_<kind>/haipipe-task-for-<kind>",
        "pipelines": "? out of the work theme (b17 excludes them): stay in base, or a theme of their own"}
PIPE = ("haipipe-data", "haipipe-nn", "haipipe-end", "haipipe-individual")


def entry_rows():
    rows = []
    for d in sorted(p for p in TASK.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))):
        skills = skill_dirs(d) if (d / "SKILL.md").exists() is False else [d]
        if d.name[0].isdigit():
            kinds = [s.name for s in skills if s.name.startswith("haipipe-task")]
            pipes = [s.name for s in skills if s.name.startswith(PIPE)]
            rows.append(f"{d.name + '/':<16}{len(kinds):>2} kind  {len(pipes):>2} pipeline")
        else:
            rows.append(f"{d.name + '/':<16}{len(skills):>2} skill" + ("s" if len(skills) != 1 else ""))
    return rows


def caller_rows():
    out = []
    for name in ("haipipe-task", "haipipe-workflow", "workbench-work", "haipipe-task-creator-agent",
                 "haipipe-task-orchestrator-agent", "haipipe-page-task"):
        hits = refs(name, TK, TASK)
        areas = [a for a in where_short(hits) if not a.endswith(".md")]
        out.append(f"{name:<32}{len(hits):>3} files  " + " ".join(areas)[:110])
    return out


def draw():
    text(0, -170, "b17 s02 · which skills make the work theme", 44)
    legend(1000, -170)
    text(0, -105, "Read from disk: skills/1_base/task today, and who outside it calls each core skill. "
                  "The homes are a proposal; red = open.", 20, GRAY)

    r1, b1 = mono(0, 0, entry_rows(), "skills/1_base/task/ today")
    held = [p.name for p in WORK.iterdir()] if WORK.is_dir() else []
    r2, b2 = mono(0, b1 + 60, held or ["(empty)"], "skills/2_theme/work/ today")

    homes = [f"{k:<18}-> {v}" for k, v in HOME.items()]
    homes = [("!" + h) if ("?" in h.split("->")[1][:3] or "!" in h.split("->")[1][:3]) else h for h in homes]
    r3, b3 = mono(r1 + 160, 0, homes, "proposed home of each entry")
    arrow(r1 + 20, 140, r1 + 140, 140, "split")

    r4, b4 = mono(r1 + 160, b3 + 80, caller_rows(), "who calls them (files outside 1_base/task)", size=14)

    y = max(b2, b4) + 80
    sticky(0, y, 520, "Rule: a theme never depends on another\ntheme. What several themes call stays\nin base.", "idea")
    sticky(560, y, 520, "So haipipe-task stays in base: insight,\ndiscovery, paper and page all call it\n(the Task folder and P-B-E-R contract).", "idea")
    sticky(1120, y, 520, "done 261007: workbench-work moved to\n2_theme/work, beside the new haipipe-work\ndoor. The task-for-* kinds wait for Q04.", "done")

    cy = y + 200
    for c in ["? Each numbered folder (1_data, 2_nn, 3_end, 4_individual) holds a work kind AND a pipeline:",
              "  splitting them leaves the same number in two places (2_theme/work/1_data and 1_base/task/1_data).",
              "? haipipe-work is a thin door (it only routes); haipipe-task keeps the Task contract in base.",
              "  Should the work Block/Job/Task contract (Q01) live in haipipe-work once it is written?",
              "? The task agents are called by page, insight and paper too: are they base agents, not work's?",
              "? inlab-human reads 1_base/task/4_individual by path: a pipeline move breaks it again.",
              "? page-types/haipipe-page-insight is an empty leftover beside 2_theme/insight/haipipe-page-insight:",
              "  delete it? (two folders with one name make a name lookup ambiguous)"]:
        cy = concern(0, cy, c) + 6

    questions_frame(0, cy + 120, [
        ("Q04 · Which skills make the work theme?\nwhat moves to 2_theme/work, what stays in base,\nand what is work's door?",
         [("done: workbench-work and\nhaipipe-work in 2_theme/work", "done"),
          ("move next: the task-for-* kinds", "idea"),
          ("stay: haipipe-task; lift haipipe-workflow\nto 1_base/project", "idea"),
          ("your call: pipelines' home\nand the task agents", "open")]),
    ])


if __name__ == "__main__":
    draw()
    save(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s02-work-skills.excalidraw", "build_s02_work_skills.py")
