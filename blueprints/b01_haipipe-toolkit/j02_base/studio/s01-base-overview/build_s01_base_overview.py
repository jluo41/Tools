"""b02 s01 · Base overview: s01-base-overview.excalidraw, the base layer at a glance.

Read from disk every build: each family in skills/1_base with its door, its sub-folders and
skills, where its agents are, how many tests/ folders it has and which skills have no
CHANGELOG.md; the Questions come from ../../board.md. Each later drawing (s02 to s05) answers
one Question in depth; this one is the map to start from.

Draws with b04's helpers (Tools/blueprints/b01_haipipe-toolkit/j04_skill_folder/studio/_build/sketch.py) through b03's
canvas.write, so a person's marks survive a rebuild.

    python build_s01_base_overview.py [out.excalidraw]
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
sys.path.insert(0, str(next(p for p in (BLOCK.parent).glob("*/studio/_build/sketch.py")).parent))
from sketch import (GRAY, SKILLS, concern, families, legend, mono, questions_frame, save,  # noqa: E402
                    skill_dirs, sticky, text)

BASE = SKILLS / "1_base"
WIDTH_CHARS = 74                 # a line longer than this is cut, so nothing runs past its box


def family_lines(fam):
    """The door first, then each sub-folder with its skills, then agents, tests and CHANGELOG gaps."""
    skills = skill_dirs(fam)
    top = sorted(s.name for s in skills if s.parent == fam)
    door = f"haipipe-{fam.name}"
    lines = [f"door   {door}" if door in top else "!door   none"]
    rest = [n for n in top if n != door]
    for i in range(0, len(rest), 2):
        lines.append(("top    " if i == 0 else "       ") + ", ".join(rest[i:i + 2]))
    subs = {}
    for s in skills:
        if s.parent != fam:
            subs.setdefault(s.relative_to(fam).parts[0], []).append(s.name)
    for sub in sorted(subs, key=lambda x: (int(re.match(r"\d+", x).group()) if re.match(r"\d+", x) else 99, x)):
        names = sorted(subs[sub])
        lines.append(f"{sub + '/':<14}" + ", ".join(names[:2]) + (f", +{len(names) - 2}" if len(names) > 2 else ""))
    agents = sorted({str(a.parent.relative_to(fam)) for a in fam.rglob("*-agent.md")
                     if not any(x.startswith("_") for x in a.relative_to(fam).parts)})
    n_agents = sum(1 for a in fam.rglob("*-agent.md") if not any(x.startswith("_") for x in a.relative_to(fam).parts))
    tests = sum(1 for t in fam.rglob("tests") if t.is_dir() and not any(x.startswith("_") for x in t.relative_to(fam).parts))
    no_log = [s.name for s in skills if not (s / "CHANGELOG.md").exists()]
    lines.append("")
    lines.append(f"agents {n_agents} in {', '.join(agents) or '-'}")
    lines.append(f"tests  {tests} folder(s)")
    if no_log:
        lines.append(f"!no CHANGELOG: {', '.join(no_log[:3])}" + (" ..." if len(no_log) > 3 else ""))
    cut = lambda l: l if len(l) <= WIDTH_CHARS else l[:WIDTH_CHARS - 3] + "..."
    return [cut(l) for l in lines], len(skills)


def draw():
    text(0, -170, "b02 s01 · the base layer at a glance", 44)
    legend(1300, -170)
    text(0, -105, "Read from disk: skills/1_base, one block per family. Each Question below gets its own "
                  "drawing (s02 to s05).", 20, GRAY)
    x, y, row_bottom, col = 0, 0, 0, 0
    for fam in families("1_base"):
        lines, n = family_lines(fam)
        r, b = mono(x, y, lines, f"{fam.name}/   {n} skills", size=14, width=WIDTH_CHARS * 14 * 0.6 + 44)
        row_bottom = max(row_bottom, b)
        col += 1
        x = r + 40
        if col == 4:
            x, y, col = 0, row_bottom + 60, 0
    y = row_bottom + 80

    sticky(0, y, 560, "Every base family has a haipipe-<family>\ndoor, like every theme (b04 q04).", "done")
    sticky(600, y, 560, "Rule for the layer: a theme calls base,\nnever another theme; what several themes\ncall belongs in base.", "idea")
    sticky(1200, y, 560, "Moves and renames are b04's: b02 decides,\nb04 moves and reruns its checks.", "none")

    cy = y + 200
    for c in ["? task/ (49 skills) mixes three things: the Task folder contract (haipipe-task), the kinds of work Task",
              "  (haipipe-task-for-<kind>) and the HAI-Pipe stage pipelines (data, nn, end, individual), in the same",
              "  numbered folders; 10_page sorts before 2_nn. (Q03, with b17 Q04)",
              "? page/ holds the Page engine and three workbench skills (workbench, -studio, -page) plus 9 agents in",
              "  workbench/agents: is the workbench part its own base family? (Q04, with b03)",
              "? agents sit in three families only (page, task, display), each in a different place. (Q02)",
              "? ideation/ has paper-only skills (journal fit, Nature-paper review, paper-reviewer): base, or the",
              "  paper theme? (Q03)",
              "? display/ has drawing helpers (excalidraw-report, excalidraw-section, *-to-svg) beside the renderers:",
              "  display, or 0_utils? (Q03)",
              "? Sub-folder names differ: task 1_data ... 10_page, ideation 1_generate, search 1_search,",
              "  writing 1_style / 2_evaluate. One naming rule for a family's sub-folders? (Q02)",
              "? Some skills have no CHANGELOG.md (red lines above); every theme skill has one. (Q02)"]:
        cy = concern(0, cy, c) + 6

    qs = re.findall(r"- id: (Q\d+)\n\s+title: (.+)", (BLOCK / "board.md").read_text(encoding="utf-8"))
    draws = {"Q01": "s02-base-map: base family x\nwho calls it (themes, base, servers)",
             "Q02": "s03-base-shape: one row per family:\ndoor, ref, agents, tests, CHANGELOG",
             "Q03": "s04-not-base: each candidate and\nits proposed home",
             "Q04": "s05-workbench-skills: page's three\nworkbench skills vs servers/workbench"}
    calls = {"Q03": ("your call with b17: the stage\npipelines' home", "open"),
             "Q04": ("your call with b03: a 1_base/\nworkbench/ family?", "open")}
    rows = []
    for qid, title in qs:
        notes = [(f"drawn in {draws.get(qid, '?')}", "idea")]
        if qid in calls:
            notes.append(calls[qid])
        rows.append((f"{qid} · {title}", notes))
    questions_frame(0, cy + 120, rows)


if __name__ == "__main__":
    draw()
    save(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s01-base-overview.excalidraw", "build_s01_base_overview.py")
