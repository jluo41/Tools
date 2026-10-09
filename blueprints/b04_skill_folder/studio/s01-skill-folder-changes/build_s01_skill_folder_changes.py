"""b04 s01 · Skill folder changes: s01-skill-folder-changes.excalidraw, what q02 and q03 changed.

A results scratch, read from disk every build (nothing typed that the script could read):

    skills/ before -> now        the families in Tools HEAD (git ls-tree), beside the layers on disk
                                 with each family's SKILL.md count
    subjective-label -> toolkit  the plugin's top level in Tools HEAD, beside where each part lives now
    servers/ before -> now       the server folders in Tools HEAD, beside today's; who moved what
    what broke, and the fix      q02's seven kinds of broken path, one note each
    checks                       the Checks lines of reports/q02_path_fix and q03_merge_subjective_label
    Questions                    one row per question in ../../board.md, with ideas (blue) and
                                 choices for JL (pink)

It draws through b03's canvas.write, so every mark a person adds survives a rebuild.

    python build_s01_skill_folder_changes.py [out.excalidraw]
"""
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]                                   # Tools/blueprints/b04_skill_folder
TOOLS = BLOCK.parents[1]                                  # Tools/
TK = TOOLS / "plugins" / "haipipe-toolkit"
sys.path.insert(0, str(HERE.parent / "_build"))
from sketch import (BLUE, GRAY, INK, RED, arrow, close_frame, els, legend, mono, open_frame,  # noqa: E402
                    reply, save, sticky, text)


# ── facts, read from disk ───────────────────────────────────────────────────────────────────
def git_dirs(path):
    """The folders directly under `path` (relative to Tools/) in Tools HEAD."""
    out = subprocess.run(["git", "-C", str(TOOLS), "ls-tree", "--name-only", "HEAD", path.rstrip("/") + "/"],
                         capture_output=True, text=True).stdout.split()
    return [Path(p).name for p in out]


def skill_count(folder):
    return sum(1 for p in folder.rglob("SKILL.md")
               if not any(x.startswith(("_", ".")) or x == "venue" for x in p.relative_to(folder).parts))


def layers_now():
    rows = []
    for layer in ("0_utils", "1_base", "2_theme"):
        fams = sorted(d for d in (TK / "skills" / layer).iterdir() if d.is_dir() and not d.name.startswith((".", "_")))
        if layer == "0_utils":
            rows.append(f"{layer}/   {len(fams)} skills, one folder each")
            continue
        rows.append(f"{layer}/   {sum(skill_count(f) for f in fams)} skills")
        for f in fams:
            n = skill_count(f)
            rows.append(f"  {f.name + '/':<12}{n:>3}" + ("   (empty: new)" if n == 0 else ""))
    return rows


def report_checks(q, n=7):
    """The first n bullet lines of a report's Checks section, shortened."""
    md = (BLOCK / "reports" / q / f"{q}.md").read_text(encoding="utf-8")
    m = re.search(r"\nChecks\n=+\n(.*?)\n\n\n", md, re.S)
    out = []
    for line in (m.group(1) if m else "").splitlines():
        if line.startswith("- "):
            out.append(line[2:])
        elif out and line.startswith("  "):
            out[-1] += " " + line.strip()
    return [re.sub(r"`", "", b)[:96] + ("..." if len(b) > 96 else "") for b in out[:n]]


def board_questions():
    md = (BLOCK / "board.md").read_text(encoding="utf-8")
    return re.findall(r"- id: (\S+)\n\s+question: (.+)", md)


# ── the drawing ─────────────────────────────────────────────────────────────────────────────
def draw():
    text(0, -170, "b04 s01 · what changed in the skill folder", 44)
    legend(1300, -170)
    text(0, -105, "q02 path fix and q03 labeling merge, 2026-10-07. Before = Tools HEAD (git); now = disk. "
                  "Red = open concern; green ✎ = a change.", 20, GRAY)

    # 1 · skills/ before -> now
    before = [d + "/" for d in git_dirs("plugins/haipipe-toolkit/skills") if not d.endswith(".md")]
    r, b1 = mono(0, 0, before, "skills/ in Tools HEAD (one level)")
    r2, b2 = mono(r + 160, 0, layers_now(), "skills/ now: three layers")
    arrow(r + 20, 120, r + 140, 120, "mv by JL", GRAY)
    sticky(r2 + 50, 50, 430, "JL moved the families by plain mv.\nb04 fixed every path that broke\n"
                              "(see 'what broke' below).", "done")
    sticky(r2 + 50, 200, 430, "2_theme/labeling: q03 moved the\nsubjective-label plugin in.", "done")
    held = sorted(d.name for d in (TK / "skills/2_theme/work").iterdir() if d.is_dir())
    sticky(r2 + 50, 320, 430, "2_theme/work now holds:\n" + ", ".join(held or ["nothing"]) +
                              "\nthe rest: b17 Q04 (b17 s02-work-skills)", "done" if held else "open")

    # 2 · subjective-label -> toolkit
    y = max(b1, b2) + 120
    old = [d + ("/" if "." not in d else "") for d in git_dirs("plugins/subjective-label")]
    homes = {"skills": "skills/2_theme/labeling/<skill>/", "engine": "skills/2_theme/labeling/engine/",
             "fixtures": "! deleted before the move (not restored)", "diagram": "skills/2_theme/labeling/diagram/",
             "agents": "agents/<9 agents>.md", "servers": "servers/workbench-labeling/  (+ _host --only labeling)",
             ".claude-plugin": "removed (marketplace entry dropped)", "README.md": "skills/2_theme/labeling/README.md",
             "CORPUS-PREPARATION.md": "skills/2_theme/labeling/CORPUS-PREPARATION.md"}
    lines = [f"{d:<24}-> {homes.get(d.rstrip('/'), '?')}" for d in old]
    r3, b3 = mono(0, y, lines, "plugins/subjective-label/ (Tools HEAD)  ->  plugins/haipipe-toolkit/")
    sticky(r3 + 50, y + 40, 460, "Labeling is no longer optional:\nthe host imports live.labeling;\n"
                                 "serve.py --only labeling is the\nannotator-only host.", "done")
    sticky(r3 + 50, y + 230, 460, "fixtures/job-mini was already gone\nfrom the working tree. Restore it?", "open")

    # 3 · servers before -> now
    sx = max(r2 + 560, r3 + 580)
    s_before = [d + "/" for d in git_dirs("plugins/haipipe-toolkit/servers") if not d.endswith(".md")]
    rs, bs = mono(sx, 0, s_before, "servers/ in Tools HEAD")
    now = sorted(d.name + "/" for d in (TK / "servers").iterdir() if d.is_dir() and not d.name.startswith((".", "__")))
    for sub in sorted(d.name for d in (TK / "servers/workbench").iterdir()
                      if d.is_dir() and d.name not in ("assets", "__pycache__", "studio")):
        now.insert(now.index("workbench/") + 1, f"  workbench/{sub}/")
    rn, bn = mono(rs + 160, 0, now, "servers/ now")
    arrow(rs + 20, 120, rs + 140, 120)
    yy = 0
    for body, kind in [("b04: workbench-labeling/ moved in\nfrom plugins/subjective-label.", "done"),
                       ("b02 + JL: workbench-shared -> workbench\n(the base).", "none"),
                       ("b02 + JL: workbench-page -> the base's\nTask level (workbench/<task level>/).", "none"),
                       ("b02 + JL: workbench-task -> workbench-work\n(server and skill; URL task-board kept).", "none"),
                       ("haipipe-board -> space-home happened\nearlier (already in the working tree).", "none")]:
        yy = sticky(rn + 50, yy, 470, body, kind) + 20

    # 4 · what broke, and the fix (q02)
    y4 = max(b3, bs, bn, yy) + 140
    text(sx, y4 - 60, "q02 · what broke, and the fix", 26)
    kinds = [("1 fixed paths in server code", "SKILLS / 'design' / ... -> skill_dir('<skill>')"),
             ("2 parents[N] in skill code", "-> next(p ... if p.name == 'skills')"),
             ("3 globs over skills/", "'*/haipipe-*' -> '*/*/haipipe-*'"),
             ("4 written skills/<family>/", "210 rewritten with their layer"),
             ("5 bare tokens page/haipipe-page/...", "39 rewritten as 1_base/page/..."),
             ("6 relative links", "105 re-resolved from the pre-move spot"),
             ("7 paper venue submodule", ".git file, core.worktree, .gitmodules")]
    for i, (k, fix) in enumerate(kinds):
        sticky(sx + (i % 2) * 560, y4 + (i // 2) * 120, 520, f"{k}\n{fix}", "fit", 17)

    # 5 · checks, read from the reports
    c2 = report_checks("q02_path_fix")
    c3 = report_checks("q03_merge_subjective_label")
    rc, bc = mono(0, b3 + 140, [f"q02 · {c}" for c in c2] + [""] + [f"q03 · {c}" for c in c3],
                  "checks (read from reports/q02 and q03)", size=14)

    # 5b · concerns, in red text
    cy = bc + 60
    for c in ["? 'Before' is Tools HEAD: moves made earlier and never committed (haipipe-board -> space-home,",
              "  designs/tasks/bNN -> designs/bNN) already count as 'before' on disk but not in git.",
              "? Nothing is committed: the next git add must take the deletions and the new folders together,",
              "  or the history shows files vanishing.",
              "? fixtures/job-mini (labeling's sealed-test fixture) was deleted before q03 began: by whom?",
              "? Several sessions edit the same files (guide_families.py, host_registry.py, READMEs): one owner",
              "  per file, or a lock note in each Block's HANDOFF?",
              "? b04's HANDOFF.md still describes the state before q02 and q03 (history, kept as written)."]:
        cy = text(0, cy, c, 18, RED)["y"] + 28
    bc = cy

    # 6 · Questions frame: one row per board question, ideas and choices beside it
    qy = max(bc, y4 + 4 * 120) + 160
    fr = open_frame("Questions")
    rows = {"q01_skill_layers": [("workbench-page skill: keep in 1_base\n(its server is base now)", "idea"),
                                 ("frame contract: new 1_base/workbench/\nfamily? (workbench, -studio, -page)", "open"),
                                 ("servers/: stay flat, the name\nsays the layer", "idea")],
            "q02_path_fix": [("done; 37 links were broken before\nthe move and need their owners", "done"),
                             ("Pages still write structure-source:\nin the old form (count in s03): edit them?", "open")],
            "q03_merge_subjective_label": [("done; door renamed haipipe-labeling,\nworkbench-labeling lifted (261007)", "done"),
                                           ("rename the generic agents\n(moderator-agent, ...)?", "open"),
                                           ("restore fixtures/job-mini?", "open")]}
    qx, ry = 0, qy
    for qid, question in board_questions():
        bottom = sticky(qx, ry, 760, f"{qid}\n{question}", "ask")
        x = qx + 800
        for body, kind in rows.get(qid, []):
            bottom = max(bottom, sticky(x, ry, 440, body, kind))
            x += 470
        ry = bottom + 60
    sticky(qx, ry, 760, "b17 Q04 · Which skills make the work theme?\n(asked in b17_theme_work; b04 moves the files\nonce it is settled)", "ask")
    sticky(qx + 800, ry, 440, "idea: base keeps the Task folder\ncontract; work gets the lifecycle,\n"
                              "workbench-work, task-for-* kinds", "idea")
    sticky(qx + 1270, ry, 440, "your call: the ML pipeline (data ·\nnn · end · individual) into work,\nor its own theme?", "open")
    close_frame(fr)

    # replies to JL's marks (261007), in blue beside each mark
    for x, y, body in REPLIES:
        reply(x, y, body)


REPLIES = [  # (x, y, text): beside the person's mark, never over it
    (2270, 1830, "Not for the move. SMSDesign's 16 Pages resolve. SMSEngagement's 32 use the\n"
                 "Tools/plugins/... form, which never resolved (some even name workflow-phases/),\n"
                 "so their structure check was already off. The fix is editing those 32 Pages\n"
                 "to 2_theme/paper/venue/...; it turns the check on, so it is that project's call."),
    (1580, 1500, "Still used: workbench-paper links every Section to /_board/draft, the Page\n"
                 "workbench (now servers/workbench/task-page), and about 60 files name the skill.\n"
                 "It can go once the base frame's Task level shows a Page (b02 Q03): then fold\n"
                 "workbench-page into the frame contract."),
]


if __name__ == "__main__":
    draw()
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s01-skill-folder-changes.excalidraw"
    save(out, "build_s01_skill_folder_changes.py")
