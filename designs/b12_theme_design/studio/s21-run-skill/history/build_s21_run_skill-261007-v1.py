"""b12 s21 · Run and skill: s21-run-skill.excalidraw: every design Run, and the skills behind them.

JL 261007: "s21 should be s21-run-skill. It should include both runs and skills." Four frames:
  1. Runs by level: each Run of the Block, the Job and the Task: hard or soft, its folder, who does it,
     who checks it, its skill, and the Space it shows in;
  2. one Job, in order: set up (goal · method · inputs) → generate N → verify each → revise ↺ → compare → release, the
     skill under each step and the person's marks;
  3. the skills: each one, what it owns, which Runs use it, and what changes on the new ladder;
  4. skill × Run: which skill each Run loads.

Every design Run is named `run-<type>-<target>/` (JL 261007: "unify the name to be run-xxx-xxx"): a hard
Run keeps its own result/, a soft Run writes into its level's own folders; `kind:` in its run.yaml says
which. A repeat on the same target is told apart by what it reads (`run-verify-d<NN>-v<k>`, the draft
version), never by a counter. The Run types are
the design theme's (servers/workbench-design/design_theme.py: BLOCK_RUNS, JOB_RUNS, TASK_RUNS) and the
scaffold's (skills/2_theme/design/haipipe-design/scripts/design_ladder.py). Placeholders only; lines,
ink and gray, red for what is open. canvas.write keeps every mark a person adds through a rebuild.

    python build_s21_run_skill.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
B03 = HERE.parents[2] / "b03_project_workbench" / "studio"
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
import build_ladder_v4 as L  # noqa: E402
import canvas  # noqa: E402

# ── 1 · Runs by level ──────────────────────────────────────────────────────────────────────────
RUN_COLS = [("Run", 330), ("kind", 80), ("what it does", 250), ("who does it", 250), ("who checks", 250),
            ("skill", 270), ("shows in", 300)]
RUNS = [("Block", [   # every Block Run is soft (JL 261007)
            ("run-add-goal-<goal>", "soft", "add a goal", "designer agent", "a person signs", "haipipe-design-goal", "Description › Goals"),
            ("run-setup-rules", "soft", "set up shared rules", "designer agent", "a person signs", "haipipe-design-goal", "Description › Rules"),
            ("run-add-inputs-i<N>", "soft", "add an inputs version", "designer agent", "manifest sha256", "haipipe-design", "Description › Inputs"),
            ("run-add-job-j<NN>", "soft", "launch a Job", "designer agent", "-", "haipipe-design", "Map · Work Details"),
            ("run-add-observed-e<NN>", "soft", "add the Exp's data", "designer agent", "manifest sha256", "haipipe-design", "Predicted vs observed"),
            ("run-score-e<NN>", "soft", "score the predictions", "another agent", "-", "haipipe-design", "Predicted vs observed"),
            ("run-propose-questions", "soft", "propose questions", "designer agent", "another agent agrees", "haipipe-question", "Questions"),
            ("run-report-q<NN>", "soft", "write a report", "designer agent", "another agent checks", "haipipe-page", "Questions"),
            ("run-propose-method-<slug>", "soft", "propose a method", "designer agent", "a person", "haipipe-design-unit", "Methods (the registry)"),
            ("run-draw-s<NN>", "soft", "draw a topic", "designer agent", "-", "excalidraw-report", "Idea Studio")]),
        ("Job", [
            ("run-setup-goal-j<NN>", "soft", "set up the goal", "designer agent", "signed at the Block", "haipipe-design-goal", "Description › Goal"),
            ("run-setup-method-j<NN>", "soft", "set up the method", "designer agent", "-", "haipipe-design", "Description › Method"),
            ("run-setup-inputs-j<NN>", "soft", "set up the inputs", "designer agent", "manifest sha256", "haipipe-design", "Description › Inputs"),
            ("run-open-designs-j<NN>", "soft", "open the design Tasks", "designer agent", "-", "haipipe-design", "Work Details"),
            ("run-freeze-predictions-j<NN>", "soft", "freeze predictions", "a person", "-", "haipipe-design-delivery ?", "Performance"),
            ("run-release-j<NN>", "soft", "release", "designer agent", "a person signs", "haipipe-design-delivery ?", "Delivery")]),
        ("Task", [
            ("run-reason-ideas", "hard", "t00 · reason ideas (②)", "designer agent", "each step's from in the manifest", "haipipe-design-unit", "Reason ideas"),
            ("run-generate-d<NN>", "hard", "tNN · generate (③)", "designer agent", "check_unit.py", "haipipe-design-unit", "Design display"),
            ("run-verify-d<NN>-v<k>", "hard", "tNN · verify (④)", "reviewer agent ?", "the result itself", "haipipe-design-unit", "Design display"),
            ("run-revise-d<NN>", "soft", "tNN · revise", "designer agent", "the next verify", "haipipe-design-unit", "Design display"),
            ("run-rank-designs", "hard", "t99 · rank (⑤)", "reviewer agent ?", "-", "haipipe-design-unit", "Review whole")])]

# ── 2 · one Job, in order ───────────────────────────────────────────────────────────────────────
FLOW = [("set up ×3", "goal · method · inputs", "the goal signed at the Block"),
        ("t00 reason", "haipipe-design-unit", "ideas I01 – I15"),
        ("tNN generate", "haipipe-design-unit", "one design per idea"),
        ("tNN verify", "haipipe-design-unit", "another agent"),
        ("t99 rank", "haipipe-design-unit", "keep the top N"),
        ("release", "haipipe-design-delivery ?", "a person signs")]

# ── 3 · the skills ──────────────────────────────────────────────────────────────────────────────
SKILLS = [("haipipe-design", "the door: the ladder contract (design-ladder.md) and its scaffold",
           "launch a Job · set up · open designs",
           "SKILL.md still names the Design Folder; method-folders.md makes the method the Job ?"),
          ("haipipe-design-unit", "one bounded unit from a frozen ticket: generate, revise, verify",
           "reason · generate · verify · revise · rank", "steps ② – ⑤, each a hard Run in its Task; method cards in methods/"),
          ("haipipe-design-goal", "the design input: aim, venue, rules, resources, leave out",
           "add a goal · set up rules · set up the goal", "the goal signed once, at the Block"),
          ("haipipe-design-brief", "the Brief Folder: why the app, for whom, the designs it allows",
           "(none on the new ladder)", "merges into the Block's goal list (decided)"),
          ("haipipe-design-workflow", "the Run list and its routes: set up, generate, verify",
           "(no Run of its own)", "becomes the Run graph per level ?"),
          ("? haipipe-design-delivery", "? the hand-off: designs.json (its schema) · designs.md · screens/",
           "freeze predictions · release", "? new, like haipipe-page-delivery"),
          ("workbench-design", "the served face; the Guide (method.md, papers)",
           "shows every Run, starts none", "design_theme.py on the shared frame; old pages retire ?"),
          ("venue/* (8)", "style profiles: sms, email, push, reminder, report, ui-card …",
           "read by generate (part 1, see input)", "-"),
          ("haipipe-designer-agent", "the agent that runs one design Run ticket",
           "every agent step above", "? a reviewer agent of its own for ④ ⑤, which also predicts"),
          ("shared: haipipe-run · haipipe-question", "the Run folder contract · the Block's questions",
           "every Run · reports/", "-"),
          ("proposed: by-<method> (13)", "the Guide's cards say a skill per method",
           "generate, by method", "one unit skill reading registered method cards (M01 …)")]
SKILL_COLS = [("skill", 330), ("owns", 560), ("Runs that use it", 420), ("on the new ladder", 640)]


def table(x, y, cols, rows, size=15, row_h=34):
    """A lines-only table: a header, then one row each; a cell ending in "?" is red. Returns its bottom."""
    w = sum(cw for _, cw in cols)
    cx = x
    for name, cw in cols:
        L.text(cx + 8, y + 8, name, size - 1, L.GRAY)
        cx += cw
    L.path([(x, y + row_h), (x + w, y + row_h)], arrow=False, color=L.INK)
    for i, row in enumerate(rows):
        ry = y + row_h * (i + 1)
        cx = x
        for (name, cw), cell in zip(cols, row):
            font = L.MONO if name in ("Run", "skill") else L.SANS
            L.text(cx + 8, ry + 8, cell, size, L.RED if cell.endswith("?") else L.INK, font)
            cx += cw
        L.path([(x, ry + row_h), (x + w, ry + row_h)], arrow=False, color=L.GRAY)
    return y + row_h * (len(rows) + 1)


def bottom():
    return max(e["y"] + e.get("height", 0) for e in L.els)


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s21-run-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None

    # 1 · Runs by level
    fr = L.open_frame("Runs by level")
    L.text(0, 0, "Design Runs, level by level", 30)
    L.text(0, 46, "every Run = run-<type>-<target>/ · hard: its own result/ · soft: writes into its level's "
                  "folders · red ? = open", 16, L.GRAY)
    L.text(0, 74, "✎ 261007  one name for every Run, run-<type>-<target> (JL); hard or soft is its kind: and its "
                  "result/, a repeat names what it reads (-v<k>), never a counter (was rNN_<type>_<target> for hard)",
           16, L.GREEN)
    y = 130
    for level, rows in RUNS:
        L.text(0, y, level, 20, L.RED if level == "Method" else L.INK)
        y = table(120, y - 4, RUN_COLS, rows) + 30
    L.close_frame(fr, pad=40)

    # 2 · one Job, in order
    y = bottom() + 200
    fr = L.open_frame("one Job, in order")
    L.text(0, y, "One Job, in order: each step, its skill, its check", 30)
    fx, fy = 0, y + 80
    for k, (step, skill, note) in enumerate(FLOW):
        L.base("rectangle", fx, fy, 260, 64, L.INK, 1.5)
        L.text(fx + 16, fy + 18, step, 20)
        L.text(fx, fy + 80, skill, 14, L.INK, L.MONO)
        L.text(fx, fy + 104, note, 14, L.RED if note.endswith("?") else L.GRAY)
        if k < len(FLOW) - 1:
            L.path([(fx + 268, fy + 32), (fx + 332, fy + 32)], color=L.INK)
        fx += 340
    rx = 3 * 340                                   # revise loops back to verify
    L.path([(rx + 130, fy - 4), (rx + 130, fy - 40), (rx - 340 + 130, fy - 40), (rx - 340 + 130, fy - 4)],
           color=L.GRAY, dashed=True)
    L.text(rx - 160, fy - 66, "weak -> revise -> verify again", 14, L.GRAY)
    L.text(0, fy + 150, "a person signs the goal once, at the Block; then the compare and the release; "
                        "verify is never by the agent that generated", 16, L.GRAY)
    L.close_frame(fr, pad=40)

    # 3 · the skills
    y = bottom() + 200
    fr = L.open_frame("the skills")
    L.text(0, y, "The skills behind the Runs", 30)
    L.text(0, y + 46, "skills/2_theme/design/ · the agent in haipipe-design/agents/ · red = changes on the "
                      "new ladder", 16, L.GRAY)
    table(0, y + 100, SKILL_COLS, SKILLS)
    L.close_frame(fr, pad=40)

    # 4 · skill x Run
    y = bottom() + 200
    fr = L.open_frame("skill x Run")
    L.text(0, y, "Which skill each Run loads", 30)
    names = ["haipipe-design", "haipipe-design-unit", "haipipe-design-goal", "haipipe-design-delivery", "other"]
    cols = [("Run", 340)] + [(n, 260) for n in names]
    rows = []
    for level, runs in RUNS:
        for r in runs:
            skill = r[5].rstrip(" ?")
            rows.append([r[0]] + ["x" if skill == n else "" for n in names[:-1]]
                        + ["" if skill in names else skill])
    table(0, y + 70, cols, rows)
    L.close_frame(fr, pad=40)
    canvas.write(out, list(L.els), "build_s21_run_skill.py")


if __name__ == "__main__":
    main()
