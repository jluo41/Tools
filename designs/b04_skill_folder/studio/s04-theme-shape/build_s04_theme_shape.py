"""b04 s04 · Theme shape: s04-theme-shape.excalidraw, whether every theme folder has the same
shape: its door skill, its workbench skill, its server, its agents and its design Block.

Read from disk every build: for each theme in skills/2_theme (and the two base families with a
workbench, page and task), whether haipipe-<theme> exists, where workbench-<theme> sits, whether
servers/workbench-<theme> exists, where its agents are, and which designs/bNN_theme_<theme>
Block designs it. A cell that breaks the common shape is red.

    python build_s04_theme_shape.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "_build"))
from sketch import (GRAY, SKILLS, TK, TOOLS, board_questions, concern, families, legend, mono,  # noqa: E402
                    questions_frame, save, sticky, text)

DOOR = {}  # a theme whose door is not haipipe-<theme> (labeling's was subjective-label until 261007)


def row(theme, fam):
    door = fam / DOOR.get(theme, f"haipipe-{theme}")
    door_s = (("! " if theme in DOOR else "") + door.name) if door.is_dir() else "! none"
    wb = [p for p in fam.rglob(f"workbench-{theme}") if (p / "SKILL.md").exists()]
    if wb:
        depth = len(wb[0].relative_to(fam).parts)
        wb_s = ("! " if depth > 1 else "") + wb[0].relative_to(fam).as_posix()
    else:
        wb_s = "! none"
    srv = "servers/workbench-" + theme if (TK / "servers" / f"workbench-{theme}").is_dir() else "! none"
    own = sorted({p.parent.relative_to(fam).as_posix() for p in fam.rglob("*-agent.md")})
    door_name = DOOR.get(theme, f"haipipe-{theme}")
    linked = [p for p in (TK / "agents").glob("*-agent.md") if p.is_symlink() and fam in p.resolve().parents]
    real = [p for p in (TK / "agents").glob("*-agent.md") if not p.is_symlink()
            and (door_name in p.read_text(errors="ignore") or p.name.startswith(f"haipipe-{theme}"))]
    parts = ([", ".join(own)] if own else []) + ([f"{len(linked)} linked"] if linked else []) \
        + ([f"! {len(real)} files in toolkit agents/"] if real else [])
    ag = " + ".join(parts)
    design = sorted(d.name for d in (TOOLS / "designs").glob(f"b*_theme_{theme}"))
    return [theme, fam.relative_to(SKILLS).as_posix(), door_s, wb_s, srv, ag or "-", design[0] if design else "! none"]


def table():
    rows = []
    for f in families("2_theme"):
        empty = not any(f.rglob("SKILL.md"))
        held = SKILLS / "1_base" / "task" if f.name == "work" and empty else f   # work's skills still in 1_base/task
        r = row(f.name, held)
        if held != f:
            r[1] = "! " + held.relative_to(SKILLS).as_posix() + " (2_theme/work empty)"
        rows.append(r)
    head = ["theme", "skills family", "door", "workbench skill", "server", "agents", "design Block"]
    w = [max(len(str(r[i]).replace("! ", "")) for r in rows + [head]) + 2 for i in range(len(head))]
    out = ["".join(h.ljust(w[i]) for i, h in enumerate(head)), ""]
    for r in rows:
        bad = any("! " in str(c) or str(c).startswith("!") for c in r)
        out.append(("!" if bad else "") + "".join(str(c).replace("! ", "").ljust(w[i]) for i, c in enumerate(r)))
    return out, rows


def draw():
    lines, rows = table()
    text(0, -170, "b04 s04 · is every theme folder the same shape?", 44)
    legend(1000, -170)
    text(0, -105, "Read from disk: each theme's door, workbench skill, server, agents and design Block. "
                  "A red row breaks the common shape.", 20, GRAY)
    r, b = mono(0, 0, lines, "one row per theme")
    sticky(r + 50, 0, 520, "The common shape: skills/2_theme/<theme>/\nhaipipe-<theme> (door) + workbench-<theme>\n"
                           "at the family top; servers/workbench-<theme>;\ndesigns/bNN_theme_<theme>.", "idea")
    sticky(r + 50, 190, 520, "Theme Blocks b11 to b17 design each theme\n(ladder, workbench); b04 only moves files.", "none")
    sticky(r + 50, 330, 520, "done 261007 (JL): labeling is haipipe-labeling-*\ngrouped by Space (1_data ... 4_delivery),\n"
                             "workbench at the family top; work has\nhaipipe-work and workbench-work.", "done")
    cy = b + 80
    for c in ["? work: its task-for-* kinds, agents and haipipe-page-task are still in 1_base/task (b17 Q04)",
              "? agents live three ways: real files in toolkit agents/ (insight, labeling), symlinks from",
              "  agents/ into a skill's agents/ (page, task), and agents/ folders inside skills that the",
              "  installer finds by itself (discovery, display, paper): one rule for all?",
              "? the 9 labeling agents keep generic names (moderator-agent, sampler-agent, ...): rename",
              "  them labeling-...-agent now that they share agents/ with every theme?",
              "? page and task are base families with a workbench, while cowork, design, discovery, insight,",
              "  labeling and paper are themes: which servers are base and which are themes, written once?"]:
        cy = concern(0, cy, c) + 6

    qs = dict(board_questions(BLOCK))
    questions_frame(0, cy + 120, [
        (f"Q04 · {qs.get('q04_theme_shape', 'theme shape')[:60]}...",
         [("one rule: agents in the theme's\nskills/<theme>/agents/, linked by\nthe installer", "idea"),
          ("one rule for agents?", "open")]),
        (f"Q03 · {qs.get('q03_merge_subjective_label', 'labeling merge')}",
         [("done: haipipe-labeling door,\nworkbench-labeling lifted", "done"),
          ("rename the labeling agents?", "open")]),
    ])


if __name__ == "__main__":
    draw()
    save(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s04-theme-shape.excalidraw", "build_s04_theme_shape.py")
