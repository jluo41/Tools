"""b12 s21 · Run and skill: s21-run-skill.excalidraw, every design Run and the skills behind them.

JL 261007: "s21 should be s21-run-skill. It should include both runs and skills"; then "the current skill is not
that powerful enough … make a plan to update the skills"; "a before after plan of the skill folders and what to
change and why"; "unify the name to be run-xxx-xxx"; and, pointing at b16's s21-paper-run-skill, "this one is much
better, follow it". Drawn in that shape (lines-only tables, ink and gray, red for what is open, green for what
changed). Seven frames, top to bottom:
  1. Runs by level: every Run a screen shows in s11 · s12 · s13, one row per Run named run-<type>-<target>, how each
     level drawing spells it today, where it stands (a run card, the live workbench, drawn only), who does it, who
     checks it, its skill, and how many of its old-layout Runs are on disk; then the cards no screen shows;
  2. one Job, in order: set up the Block → launch a Job → set up ×3 → reason → generate · verify → rank → release →
     the Exp scored, the skill under each step;
  3. the skills: each design skill and the base skills it borrows: what it owns, the Runs that use it, how often it
     still writes an old name, what changes on the new ladder;
  3b. skill folders, before → after: today's tree read from disk, the proposed tree, and per file the change,
     what it does, why, and the plan phase that makes it;
  4. skill × Run: which skill each Run loads;
  5. Runs on disk: the Runs in the Project design folders by type and layout;
  6. the skill update plan: six phases, each skill's change and the Runs it gains.

Read from disk every build: the skills in skills/2_theme/design; the level builders' SCREENS and BANDS (imported,
never run); the run cards (haipipe-design-workflow/references/run-cards.md); the live design workbench
(design_theme.py) and the base frame (servers/workbench); the Runs in the Project design folders (names only, never
their content; no Board or design is named). Typed, since they are the proposal: one name per Run, each Run's owner
after the plan, each skill's job and ladder change, the folder moves, and the plan. The first cut is
history/build_s21_run_skill-261007-v1.py. canvas.write keeps every mark a person adds through a rebuild.

    python build_s21_run_skill.py [out.excalidraw]
"""
import importlib.util
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True                    # importing the level builders leaves no __pycache__ behind
HERE = Path(__file__).resolve().parent
DESIGNS = Path(__file__).resolve().parents[3]
B03 = DESIGNS / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio"
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
import build_ladder_v4 as L  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402

SPACE = Path(__file__).resolve().parents[5]
TK = Path(__file__).resolve().parents[4] / "plugins" / "haipipe-toolkit"
SKILLS = TK / "skills"
DESIGN = SKILLS / "2_theme" / "design"
CARDS = DESIGN / "haipipe-design-workflow" / "references" / "run-cards.md"
LIVE = TK / "servers" / "workbench-design" / "design_theme.py"        # the design workbench as it runs today
BASE = TK / "servers" / "workbench"                                    # the frame every theme shares
LEVELS = [("Block", "s11-design-block/build_s11_design_block.py"),
          ("Job", "s12-design-job/build_s12_design_job.py"),
          ("Task", "s13-design-task/build_s13_design_task.py")]

# ── the typed part (proposal, 261007) ──────────────────────────────────────────────────────────
# one name per Run, run-<type>-<target> (JL 261007: "unify the name to be run-xxx-xxx"): each level drawing's own
# spelling (r01_reason_15, run-reason-t00, run-add-goal-g01 …) is matched here and folded into one row. A repeat on
# the same target names what it reads (-v<k>, the draft version), never a counter.
CANON = [(r"^r\d\d_reason_|^run-reason-", "run-reason-t00"),
         (r"^r\d\d_rank_|^run-rank-", "run-rank-t99"),
         (r"^r\d\d_generate_|^run-generate-", "run-generate-d<NN>"),
         (r"^r\d\d_verify_|^run-verify-", "run-verify-d<NN>-v<k>"),
         (r"^run-revise", "run-revise-d<NN>"),
         (r"^run-freeze-prediction", "run-freeze-predictions-j<NN>"),
         (r"^run-setup-goal", "run-setup-goal-j<NN>"), (r"^run-setup-method", "run-setup-method-j<NN>"),
         (r"^run-setup-inputs", "run-setup-inputs-j<NN>"), (r"^run-open-designs", "run-open-designs-j<NN>"),
         (r"^run-release", "run-release-j<NN>"), (r"^run-close", "run-close-j<NN>"),
         (r"^run-add-goal", "run-add-goal-<goal>"), (r"^run-setup-rules", "run-setup-rules"),
         (r"^run-add-inputs", "run-add-inputs-i<N>"), (r"^run-add-job", "run-add-job-j<NN>"),
         (r"^run-add-observed", "run-add-observed-e<NN>"), (r"^run-score", "run-score-e<NN>"),
         (r"^run-propose-questions", "run-propose-questions"), (r"^run-report", "run-report-q<NN>"),
         (r"^run-propose-", "run-propose-method-<slug>"), (r"^run-draw", "run-draw-s<NN>"),
         (r"^run-plan-test", "run-plan-test-<app>")]
# each Run after the plan: (kind, what it does, who does it, who checks, skill, today's button or None)
# skill "?" = proposed, no card yet (red); a skill that does not exist yet is marked "(new)"
RUN = {
    "run-add-goal-<goal>": ("soft", "add a goal to the goal list", "designer agent", "a person signs",
                            "haipipe-design-goal", "Add design tasks"),
    "run-setup-rules": ("soft", "set up the shared rules", "designer agent", "a person signs",
                        "haipipe-design-goal", "Set shared rules"),
    "run-add-inputs-i<N>": ("soft", "add an inputs version", "designer agent", "manifest sha256",
                            "haipipe-design-goal", "Gather resources"),
    "run-add-job-j<NN>": ("soft", "launch a Job: goal × method × inputs", "designer agent", "-",
                          "haipipe-design", "Add a goal × method"),
    "run-add-observed-e<NN>": ("soft", "add the Exp's per-arm totals", "designer agent", "manifest sha256",
                               "haipipe-design-method", None),
    "run-score-e<NN>": ("soft", "score each arm's design", "another agent", "-", "haipipe-design-method", None),
    "run-propose-questions": ("soft", "propose the Block's questions", "designer agent", "another agent agrees",
                              "haipipe-question", None),
    "run-report-q<NN>": ("soft", "write a question's report", "designer agent", "another agent checks",
                         "haipipe-page", None),
    "run-propose-method-<slug>": ("soft", "propose a method or a version", "designer agent", "a person signs",
                                  "haipipe-design-method", None),
    "run-draw-s<NN>": ("soft", "draw a topic", "designer agent", "-", "excalidraw-report", None),
    "run-plan-test-<app>": ("soft", "plan the Exp", "?", "?", "outside the theme ?", "Plan the test"),
    "run-setup-goal-j<NN>": ("soft", "pin the signed goal", "designer agent", "signed at the Block",
                             "haipipe-design-goal", "Frame the aim"),
    "run-setup-method-j<NN>": ("soft", "pin a method version", "designer agent", "-",
                               "haipipe-design-method", None),
    "run-setup-inputs-j<NN>": ("soft", "build inputs/ + manifest (①)", "designer agent", "manifest sha256",
                               "haipipe-design-goal", None),
    "run-open-designs-j<NN>": ("soft", "open t01 – tNN from ideas.yaml", "designer agent", "-",
                               "haipipe-design", "Add a design"),
    "run-close-j<NN>": ("soft", "close the Job", "designer agent", "a person", "haipipe-design-workflow", None),
    "run-freeze-predictions-j<NN>": ("soft", "freeze each kept design's prediction", "a person", "-",
                                     "haipipe-design-delivery", None),
    "run-release-j<NN>": ("soft", "release the kept designs", "designer agent", "a person signs",
                          "haipipe-design-delivery", "Passed review"),
    "run-reason-t00": ("hard", "② reason ideas: ideas · chains", "designer agent",
                       "each step's from in the manifest", "haipipe-design-unit", None),
    "run-generate-d<NN>": ("hard", "③ one design, its elements", "designer agent", "check_unit.py",
                           "haipipe-design-unit", "Generate"),
    "run-verify-d<NN>-v<k>": ("hard", "④ T0 – T2 on draft v<k>", "reviewer agent", "the result itself",
                              "haipipe-design-unit", "Verify"),
    "run-revise-d<NN>": ("soft", "the next draft, from feedback", "designer agent", "the next verify",
                         "haipipe-design-unit", None),
    "run-rank-t99": ("hard", "⑤ rank N + 5, keep N, predict", "reviewer agent", "-",
                     "haipipe-design-unit", None)}
# the level a Run belongs to, where a higher level's screen also shows it (s12 lists its Tasks' Runs)
HOME = {"run-reason-t00": "Task", "run-generate-d<NN>": "Task", "run-verify-d<NN>-v<k>": "Task",
        "run-revise-d<NN>": "Task", "run-rank-t99": "Task"}
# today's old-layout Run on disk that each new Run replaces (its count shows in frame 1)
OLD_EQUIV = {"run-generate-d<NN>": "run-design-generate", "run-verify-d<NN>-v<k>": "run-design-verify",
             "run-setup-goal-j<NN>": "run-design-commission"}
# a card no new Run takes over: what to do with it
CARD_TODO = {"Commission": "retire: the Job's three setup Runs pin what it pinned ?",
             "Add a paper": "keep: Guide › Related Paper (the frame)",
             "Pin the venue": "into run-setup-rules: the venue is a shared rule ?",
             "Set the rules": "into run-setup-rules ?", "Add a theory": "into run-add-inputs-i<N> ?",
             "Set what to leave out": "into run-setup-rules ?", "Map variables": "into the method's ① ?"}
# each design skill: what it owns, and what changes on the new ladder ("?" = must change, red)
SKILL_JOB = {
    "haipipe-design": ("the ladder's door; contract; scaffold; run-add-job · run-open-designs",
                       "done 261007: rewritten; the older Design Folder in ref/legacy/"),
    "haipipe-design-brief": ("older boards only: the Brief Folder", "kept as legacy; retire after the carry-over ?"),
    "haipipe-design-goal": ("goal list · shared rules · inputs versions · a Job's inputs/ fence",
                            "done 261007: rewritten; make_inputs.py"),
    "haipipe-design-method": ("the registry M01 – M05 and versions; the scorecard; the Exp scored",
                              "done 261007: new; pin_method.py · score_exp.py"),
    "haipipe-design-unit": ("one method step: reason ② · generate ③ · verify ④ · rank ⑤",
                            "done 261007: rewritten; check_unit.py --ladder-result"),
    "haipipe-design-workflow": ("Runs by level, routes, run cards, a design's state",
                                "done 261007: rewritten; project_predictions.py"),
    "haipipe-design-delivery": ("release · frozen predictions · designs.json", "done 261007: new; release.py"),
    "workbench-design": ("the theme on the shared frame: six Spaces × three levels",
                         "SKILL done 261007; the views still type their buttons ?")}
NEW_SKILLS = []
# old names a skill should no longer write (s11 – s13 replaced them, 261007)
STALE = (r"Design Item|\bCommission\b|Design-<NN>|Design-NN|Design-\d\d|run-design-|_by-|\brd\d\d_|rNN_|"
         r"2-Design|0-BR-brief|ITEM\d\d")
# the base skills a design borrows, by what they do for it
BORROWS = [("shared Run and question contracts", ["haipipe-run", "haipipe-question"]),
           ("a Block question's report", ["haipipe-page"]),
           ("drawings in Idea Studio", ["excalidraw-report"]),
           ("the signed insight a design reads", ["haipipe-insight"]),
           ("papers behind the methods", ["haipipe-discovery"]),
           ("the Workbench Table check", ["table-workbench"])]
# 2 · one Job, in order: (step, skill, note)
FLOW = [("set up the Block", "-goal", "goal signed · rules · inputs i<N>"),
        ("launch a Job", "haipipe-design", "run-add-job-j<NN>"),
        ("set up ×3", "-goal · -method ?", "goal · method m<k> · inputs/ ①"),
        ("t00 reason", "-unit", "② ideas I01 – I15"),
        ("tNN generate · verify", "-unit", "③ ④ another agent checks"),
        ("t99 rank", "-unit", "⑤ keep N, predict"),
        ("release", "-delivery ?", "a person signs; predictions frozen"),
        ("the Exp scored", "-method ?", "scorecard → next version")]
# 6 · the skill update plan: (phase, skill, what it learns, Runs it gains, done when)
PLAN = [("1 · contract", "haipipe-design",
         "design-ladder.md as s11 – s13 draw it; scaffold Block · Job · t00 · tNN · t99, every Run run-<type>-<target>",
         "run-add-job · run-open-designs · run-close", "a demo Block scaffolds; 0 _by- names"),
        ("2 · inputs", "haipipe-design-goal",
         "the goal list (the Brief merged in), shared rules, inputs versions, a Job's inputs/ + manifest.yaml",
         "run-add-goal · run-setup-rules · run-add-inputs · run-setup-goal · run-setup-inputs",
         "j03's inputs/ builds and checks"),
        ("2 · methods", "haipipe-design-method (new) ?",
         "registered M01 – M05, each named by its Guide type; versions m<k> with ① – ⑤, sees:, T0 – T3; the scorecard",
         "run-setup-method · run-propose-method · run-add-observed · run-score", "M04 m2 pins; an Exp scores"),
        ("3 · worker", "haipipe-design-unit",
         "reason ② and rank ⑤ beside generate and verify; the Ticket pins method + inputs; modes.md retires",
         "run-reason-t00 · run-generate · run-verify · run-revise · run-rank-t99", "one demo Job runs t00 → t99"),
        ("3 · worker", "agents",
         "the designer agent reasons, generates, revises; a reviewer agent verifies and ranks",
         "-", "verify is never by the agent that generated"),
        ("4 · Runs", "haipipe-design-workflow",
         "run-cards.md by level × six Spaces; routes; a design's state; Commission retires",
         "a card for every Run in frame 1", "every ladder Run carded (frame 1)"),
        ("4 · Runs", "haipipe-design-delivery (new) ?",
         "the release, the frozen predictions, designs.json and its schema, screens/",
         "run-freeze-predictions · run-release", "a demo Job releases"),
        ("5 · screens", "workbench-design",
         "design_views.py reads its buttons from the cards; the Guide reads the method registry; design_reader.py's "
         "METHODS from the registry; the old page stays for old boards", "every button names its skill, agent and sign",
         "workbench-design tests"),
        ("6 · old words", "all",
         "carry the old boards over; the Brief retires; old refs into legacy/; versions 0.4.0 → 0.5.0 ?",
         "-", "0 old names (frame 3)")]

# 3b · skill folders, before → after (proposal, then applied 261007). BEFORE is the tree as it was on the morning of
# 261007 (frozen here, since the skills have changed since); "done" is read from disk. Each file of BEFORE:
# (after path or "" to retire, change, what, why, plan phase). A file not named here is kept as it is.
BEFORE = ["haipipe-design/SKILL.md", "haipipe-design/agents/haipipe-designer-agent.md", "haipipe-design/ref/design-ladder.md",
          "haipipe-design/ref/method-folders.md", "haipipe-design/scripts/design_ladder.py",
          "haipipe-design-brief/SKILL.md", "haipipe-design-brief/agents/openai.yaml",
          "haipipe-design-goal/SKILL.md", "haipipe-design-goal/agents/openai.yaml",
          "haipipe-design-unit/SKILL.md", "haipipe-design-unit/references/modes.md",
          "haipipe-design-unit/references/unit-contract.md", "haipipe-design-unit/scripts/check_unit.py",
          "haipipe-design-unit/scripts/rename_runs.py", "haipipe-design-unit/scripts/render_screen.py",
          "haipipe-design-unit/tests/make_scenario.py", "haipipe-design-unit/tests/test_render_screen.py",
          "haipipe-design-unit/tests/test_unit.py",
          "haipipe-design-workflow/SKILL.md", "haipipe-design-workflow/references/run-cards.md",
          "haipipe-design-workflow/references/run-profile.md",
          "workbench-design/SKILL.md", "workbench-design/ref/design-board-space-mapping.md",
          "workbench-design/ref/design-board.md", "workbench-design/ref/space-mapping.md",
          "workbench-design/ref/workbench-table.md", "venue/"]
FOLDERS = {
    "haipipe-design/SKILL.md": ("haipipe-design/SKILL.md", "rewrite",
        "the door: Block · Job · Task · Run, routes", "it owned one old Design Folder", "1"),
    "haipipe-design/ref/design-ladder.md": ("haipipe-design/ref/design-ladder.md", "rewrite",
        "the three levels as s11 – s13 draw them", "it was s01's ladder: _by-, 3-part method.md", "1"),
    "haipipe-design/scripts/design_ladder.py": ("haipipe-design/scripts/design_ladder.py", "rewrite",
        "jNN_<goal>_<method>/ · t00 · tNN · t99 · run-<type>-<target>", "it wrote _by- and rNN_ names", "1"),
    "haipipe-design/ref/method-folders.md": ("haipipe-design/ref/legacy/method-folders.md", "move",
        "the old 2-Design-M<NN>-<slug>/ groups", "read only, until the old boards carry over", "1"),
    "haipipe-design/agents/haipipe-designer-agent.md": ("haipipe-design/agents/haipipe-designer-agent.md", "rewrite",
        "reason · generate · revise", "verify and rank go to a reviewer agent (s13)", "3"),
    "haipipe-design-brief/SKILL.md": ("haipipe-design-brief/SKILL.md", "legacy",
        "older boards only; the goal list replaced it", "older boards still read it; retire after the carry-over", "6"),
    "haipipe-design-goal/SKILL.md": ("haipipe-design-goal/SKILL.md", "rewrite",
        "goal list · rules · inputs versions · inputs/", "it wrote one design-goal.md per old board", "2"),
    "haipipe-design-unit/SKILL.md": ("haipipe-design-unit/SKILL.md", "rewrite",
        "one method step: reason · generate · verify · rank", "it only generated or verified one item", "3"),
    "haipipe-design-unit/references/unit-contract.md": ("haipipe-design-unit/references/unit-contract.md", "edit",
        "§ Ladder first; the v2 Ticket kept below", "Commission pinned it; the ladder pins by the Job", "3"),
    "haipipe-design-unit/references/modes.md": ("haipipe-design-unit/references/legacy/modes.md", "move",
        "compose · brainstorm · challenge …", "a method version says how ③ works", "3"),
    "haipipe-design-unit/scripts/check_unit.py": ("haipipe-design-unit/scripts/check_unit.py", "edit",
        "+ --ladder-result: every step's Result, the fence", "② and ⑤ write Results too", "3"),
    "haipipe-design-workflow/SKILL.md": ("haipipe-design-workflow/SKILL.md", "rewrite",
        "Runs by level, routes, a design's state", "it routed Commission → Generate → Verify", "4"),
    "haipipe-design-workflow/references/run-profile.md": ("haipipe-design-workflow/references/run-profile.md",
        "rewrite", "the 22 Run types, run-<type>-<target>", "3 types, run-design-<step>-<MMDD>-<slug>", "4"),
    "haipipe-design-workflow/references/run-cards.md": ("haipipe-design-workflow/references/run-cards.md",
        "rewrite", "30 ladder cards; the older 13 kept below", "the old page's parser still reads the older ones", "4"),
    "workbench-design/SKILL.md": ("workbench-design/SKILL.md", "rewrite",
        "six Spaces × Block · Job · Task", "it described the old page's Spaces", "4"),
    "workbench-design/ref/design-board-space-mapping.md":
        ("workbench-design/ref/legacy/design-board-space-mapping.md", "move",
         "the old board's file map", "the old board keeps its screens", "4")}
# the files only the after tree has: (path, what it is, why, plan phase)
NEW_FILES = [
    ("haipipe-design/tests/test_ladder_scaffold.py", "the scaffold, and that the workbench reads it",
     "the contract has teeth", "1"),
    ("haipipe-design/ref/legacy/design-folder.md", "the old SKILL.md body, word for word", "older boards keep it", "1"),
    ("haipipe-design/scripts/carry_over/design_ladder_by_method.py", "the first ladder's _by- scaffold",
     "the workbench's older test reads it", "1"),
    ("haipipe-design/scripts/carry_over/carry_over.py", "an old board onto the ladder, once",
     "every design board on disk is in the old layout", "6"),
    ("haipipe-design/agents/haipipe-design-reviewer-agent.md", "verify ④ · rank ⑤ · the fence check",
     "s13 decided: ④ ⑤ are always another agent", "3"),
    ("haipipe-design-goal/ref/inputs.md", "the eight parts of ①; manifests", "s12: the design sees only inputs/", "2"),
    ("haipipe-design-goal/scripts/make_inputs.py", "freeze iN; build a Job's inputs/", "the fence is built, not typed",
     "2"),
    ("haipipe-design-goal/ref/legacy/design-goal-older.md", "the old design-goal.md contract", "older boards keep it",
     "2"),
    ("haipipe-design-method/SKILL.md", "the registry, versions, scorecard", "a method has its own clock (s00)", "2"),
    ("haipipe-design-method/methods/MNN-<slug>/method.md", "M01 – M05, each named by its Guide type",
     "a Job pins a registered method", "2"),
    ("haipipe-design-method/methods/MNN-<slug>/m<k>.md", "one version: ① – ⑤, sees:, T0 – T3",
     "s12: a Job pins M04 m2", "2"),
    ("haipipe-design-method/scripts/pin_method.py", "run-setup-method: inputs/method.md + sha",
     "a method is copied by its sha, never edited", "2"),
    ("haipipe-design-method/scripts/score_exp.py", "observed/eNN → scores.csv → scorecard",
     "s11: the Exp lands once per Block", "2"),
    ("haipipe-design-unit/references/reason.md", "② t00: ideas.yaml · chains.yaml", "no worker for ② before", "3"),
    ("haipipe-design-unit/references/rank.md", "⑤ t99: ranking.csv, keep N", "no worker for ⑤ before", "3"),
    ("haipipe-design-workflow/scripts/project_predictions.py", "ranking → prediction.yaml + kept | dropped",
     "a hard rank writes only its result/", "4"),
    ("haipipe-design-delivery/SKILL.md", "release · frozen predictions · designs.json",
     "s12 decided: one owner for the file another system reads", "4"),
    ("haipipe-design-delivery/scripts/release.py", "a Job's kept designs → Job and Block delivery/",
     "release is a Run, not a hand copy", "4")]

CHANGES = {
    "runs": ["re-cut from s11 · s12 · s13: every Run a screen shows, by level (was typed by hand)",
             "one name per Run, run-<type>-<target> (JL 261007: \"unify the name to be run-xxx-xxx\"); "
             "'as drawn' keeps each level drawing's spelling, red where it still reads rNN_",
             "today: card · screen · drawn, read from run-cards.md and design_theme.py; on disk: the old-layout Runs it "
             "replaces",
             "drawn in b16's s21-paper-run-skill shape (JL 261007: \"this one is much better\")"],
    "flow": ["the Block's set-up, the Exp and the scorecard joined the Job's steps"],
    "skills": ["new columns: version · callers · how often each skill still writes an old name",
               "two new skills proposed: haipipe-design-method, haipipe-design-delivery (s12's decision)"],
    "matrix": ["new: which skill each Run loads after the plan; x ? = a skill that does not exist yet"],
    "disk": ["new frame: the Runs in the Project design folders today, by type and layout"],
    "folders": ["new frame: the skill folders before → after, each change with its why (JL 261007: \"a before "
                "after plan of the skill folders and what to change and why\")"],
    "plan": ["new frame: the skill update plan (JL 261007: \"the current skill is not that powerful enough\")",
             "applied phases 1 – 4 (JL 261007: \"go ahead and apply them\"): 95 tests pass, one Job runs end to end; "
             "phase 5's views and phase 6's carry-over are next"]}


# ── helpers, as b16's s21 draws them ──────────────────────────────────────────────────────────
def table(x, y, cols, rows, size=15, row_h=34, mono=("Run", "skill")):
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
            font = L.MONO if name in mono else L.SANS
            L.text(cx + 8, ry + 8, cell, size, L.RED if cell.endswith("?") else L.INK, font)
            cx += cw
        L.path([(x, ry + row_h), (x + w, ry + row_h)], arrow=False, color=L.GRAY)
    return y + row_h * (len(rows) + 1)


def notes(x, y, lines, date="261007"):
    """Open points in red ("?"), then what changed, in green and dated; returns the bottom."""
    for k, n in enumerate(lines):
        if n.startswith("?"):
            L.text(x, y + k * 26, n, 16, L.RED)
        else:
            L.text(x, y + k * 26, f"✎ {date}  {n}", 16, L.GREEN)
    return y + len(lines) * 26


def bottom():
    return max(e["y"] + e.get("height", 0) for e in L.els)


def clip(s, n):
    return s if len(s) <= n else s[:n - 2] + " …"


# ── facts, read from disk ──────────────────────────────────────────────────────────────────────
def callers(name):
    """Files in the toolkit outside 2_theme/design that name a skill."""
    out = subprocess.run(["grep", "-rlIw", "--exclude-dir=.git", "--exclude-dir=_legacy", "--exclude=CHANGELOG.md",
                          name, str(TK)], capture_output=True, text=True).stdout.split()
    return [o for o in out if not o.startswith(str(DESIGN))]


def stale(d):
    """How many times a skill's docs still write an old name (its CHANGELOG is history, not read)."""
    return sum(len(re.findall(STALE, f.read_text(encoding="utf-8", errors="ignore")))
               for f in d.rglob("*.md") if f.name != "CHANGELOG.md")


def find_skill(name):
    return next((p for p in SKILLS.rglob(name) if (p / "SKILL.md").is_file()), None)


def not_skills():
    """What sits in 2_theme/design but is no skill: its files and size on disk, and whether it is its own repo."""
    rows = []
    for d in sorted(p for p in DESIGN.iterdir() if p.is_dir() and not (p / "SKILL.md").exists()
                    and not p.name.startswith((".", "_"))):
        files = [f for f in d.rglob("*") if f.is_file() and ".git" not in f.relative_to(d).parts]
        kb = sum(f.stat().st_size for f in files) / 2**10
        rows.append((d.name, len(files), kb, (d / ".git").exists()))
    return rows


def cards(path):
    """The run cards of one run-cards.md: {button: {space, pattern, skill, agent, signs}}."""
    out, cur = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("🔘 BUTTON"):
            label, space, pattern = (line.split(None, 2)[2].split(" · ") + ["", "", ""])[:3]
            cur = out.setdefault(label.strip(), {"space": space.strip(), "pattern": pattern.strip()})
        elif cur is not None and line.startswith(("🧩 SKILL", "🤖 AGENT", "✍️ SIGNS")):
            cur[line.split()[1].lower()] = line.split(None, 2)[2].strip()
    return out


def said(label, code):
    """A button label written as a string in the code ("Verify", not the word inside another name)."""
    return re.search(r"[\"']" + re.escape(label) + r"[\"']", code) is not None


def canon(raw):
    """A level drawing's spelling of a Run, as its one name; an unknown spelling is returned red."""
    name = re.sub(r"^\?\s*", "", raw)
    name = re.sub(r"^t(\d\d|NN) › ", "", name)
    return next((c for pat, c in CANON if re.match(pat, name)), name + " ?")


def designed():
    """Every Run a screen shows in s11 · s12 · s13: [(level, 'Space › view', raw name, drawing)], in drawing order."""
    out = []
    for level, rel in LEVELS:
        spec = importlib.util.spec_from_file_location(f"s21_{level}", HERE.parent / rel)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)                       # the builders draw only under __main__
        tag = rel.split("-", 1)[0]
        screens = list(getattr(m, "SCREENS", ()))        # s11, s12: (space, third, runs, recent, body, files…)
        for band in getattr(m, "BANDS", ()):             # s13: (task, title, tab, screens)
            screens += [(e[0] if not band[0] else f"{band[0]} › {e[0]}", *e[1:]) for e in band[3]]
        for e in screens:
            on = next((lb for lb, o in (e[1] or ()) if o), "")
            where = e[0] + (f" › {on}" if on and on not in ("All", "Task") else "")
            out += [(level, where, r, tag) for r in e[2]]
    return out


def design_runs():
    """Every Run stem in a Project design folder, with its layout: Design-NN · 2-Design-M<NN> · the ladder."""
    seen, boards = set(), set()
    for root in SPACE.glob("examples-*/*/designs"):
        for d in root.rglob("runs"):
            parts = d.relative_to(root).parts
            if not d.is_dir() or any(p.startswith("_") for p in parts):
                continue
            boards.add((root, parts[0]))
            shelf = ("ladder" if any(re.match(r"j\d\d_", p) for p in parts) else
                     "method groups" if any(p.startswith("2-Design-M") for p in parts) else
                     "Design-NN" if any(p.startswith("Design-") for p in parts) else "board")
            for r in d.iterdir():
                stem = re.sub(r"\.(md|sh|yaml)$", "", r.name)
                if stem.startswith(("run-", "rd", "r0", "r1")):
                    seen.add((d, stem, shelf))
    return [(stem, shelf) for _, stem, shelf in seen], len(boards)


def run_type(stem):
    m = re.match(r"^(run-design-[a-z]+|run-[a-z]+(?:-[a-z]+)?)", stem)
    return m.group(1) if m else ("rNN_ (hard)" if re.match(r"^r\d", stem) else stem)


def design_files():
    """Every file in 2_theme/design today, as paths in it; venue/ is one entry; CHANGELOGs and caches are left out."""
    out = []
    for f in sorted(DESIGN.rglob("*")):
        rel = f.relative_to(DESIGN)
        if rel.parts[0] == "venue":
            continue
        if f.is_file() and f.name != "CHANGELOG.md" and not {"__pycache__", ".git"} & set(rel.parts):
            out.append(rel.as_posix())
    return sorted(out + (["venue/"] if (DESIGN / "venue").is_dir() else []), key=by_folder)


def by_folder(p):
    """Folder order: a folder's files before the next folder, haipipe-design/ before haipipe-design-…/."""
    return p.rstrip("/").split("/")


def tree(paths, tag=lambda p: ""):
    """A plain folder tree of paths, one line per folder and file: [(line, path or None)]."""
    lines, seen = [], set()
    for p in paths:
        parts = p.rstrip("/").split("/")
        for k in range(len(parts)):
            key = "/".join(parts[:k + 1])
            if key in seen:
                continue
            seen.add(key)
            leaf = k == len(parts) - 1
            name = parts[k] + ("/" if not leaf or p.endswith("/") else "")
            lines.append(("    " * k + name + ("   " + tag(p) if leaf and tag(p) else ""), p if leaf else None))
    return lines


def draw_tree(x, y, title, lines, color):
    L.text(x, y, title, 20)
    for k, (line, p) in enumerate(lines):
        L.text(x, y + 40 + k * 22, line, 14, color(p) if p else L.INK, L.MONO)
    return y + 40 + len(lines) * 22


def run_rows(runs):
    """Frame 1's rows per level, each Run with where it stands today; the tally per level; the unused cards."""
    old = cards(CARDS)
    ladder = [(m.group(1), m.group(2)) for m in re.finditer(r"(?m)^🔘 BUTTON\s+(.+?) · \w+ › [^·]+ · (\^run-\S+)", CARDS.read_text(encoding="utf-8"))]
    old = {k: v for k, v in old.items() if "›" not in v["space"]}         # the older board's cards only
    live = LIVE.read_text(encoding="utf-8")
    on_disk = Counter(run_type(s) for s, _ in runs)
    by_level, merged, used = {}, {}, set()
    for lv, where, raw, tag in designed():
        name = canon(raw)
        lv = HOME.get(name, lv)
        row = merged.get(name)
        spelt = re.sub(r"^(\?\s*)?(t\w\w › )?", "", raw)
        spelt = f"{spelt} ({tag})" if re.match(r"^r\d\d_", spelt) else ""
        if row is None:                                  # first screen that shows this Run
            kind, does, who, checks, skill, button = RUN.get(name.rstrip(" ?"), ("?", "?", "?", "?", "?", None))
            sample = re.sub(r"<[^>]+>", "x01", name.rstrip(" ?"))
            card = next((c for c in ladder if re.match(c[1], sample)), None)
            if button and button in old:
                used.add(button)
            if card:
                st, button = "card", card[0]
            elif button and said(button, live):
                st = "screen"
            else:
                st = "drawn ?"
            skill = skill + " ?" if "(new)" in skill and not skill.endswith("?") else skill
            n = on_disk.get(OLD_EQUIV.get(name, ""), 0)
            merged[name] = row = [name, [], kind, where, st, button or "-", who, checks, skill,
                                  f"{n} old" if n else "0"]
            row.append(lv)
            by_level.setdefault(lv, []).append(row)
        elif where not in row[3].split(" · "):          # another Space, or another level, shows the same Run
            row[3] = f"{row[3]} · {where}"
        if spelt and spelt not in row[1]:                # a level drawing still spells it rNN_
            row[1].append(spelt)
    for rows in by_level.values():
        for r in rows:
            r[3] = clip(r[3], 52)
            r[1] = clip(" · ".join(r[1]), 40) + " ?" if r[1] else "-"
    tally = {lv: Counter(r[4].rstrip(" ?") for r in rows) for lv, rows in by_level.items()}
    left = [b for b in old if b not in used and b not in [RUN[k][5] for k in RUN if RUN[k][5]]]
    return by_level, tally, left, old


# ── the drawing ────────────────────────────────────────────────────────────────────────────────
def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s21-run-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    runs, n_boards = design_runs()
    by_level, tally, left, old = run_rows(runs)

    # 1 · Runs by level
    fr = L.open_frame("Runs by level")
    L.text(0, 0, "Design Runs, level by level", 30)
    L.text(0, 46, "every Run a screen shows in s11 · s12 · s13, one row per Run, named run-<type>-<target> · as drawn = "
                  "a level drawing's own spelling where it differs · today: card = a ladder run card names it · screen = the "
                  "live workbench has the button · drawn = only in the drawing · on disk = old-layout Runs it replaces "
                  "· red ? = open", 16, L.GRAY)
    cols = [("Run", 360), ("as drawn", 420), ("kind", 70), ("shows in", 480), ("today", 90), ("button", 220),
            ("who does it", 230), ("who checks", 270), ("skill", 330), ("on disk", 90)]
    y = 100
    for level in ("Block", "Job", "Task"):
        t = tally.get(level, Counter())
        L.text(0, y, level, 20)
        L.text(0, y + 30, "\n".join(f"{t[k]} {k}" for k in ("card", "screen", "drawn") if t[k]), 14, L.GRAY)
        y = table(120, y - 4, cols, [r[:10] for r in by_level.get(level, [])]) + 30
    L.text(0, y + 10, "older-board cards no ladder Run takes over", 20)
    rows = [[b, old[b]["space"], old[b].get("skill", "?"), CARD_TODO.get(b, "place it in a Space ?")] for b in left]
    y = table(120, y + 50, [("card", 250), ("old Space", 160), ("skill", 300), ("to do", 560)], rows,
              mono=("skill",)) + 40
    runnable = {lv: t["card"] * 100 // max(1, sum(t.values())) for lv, t in tally.items()}
    L.text(0, y, "carded today: " + " · ".join(f"{lv} {p}%" for lv, p in runnable.items()) +
           " (261007, after the skills were applied: was Block 30% · Job 42% · Task 40%, all old buttons)", 18)
    notes(0, y + 50, ["? a drawn-only Run copies no prompt and names no agent: the Runs panel can't say who runs it",
                      "? s12 and s13 still spell the hard Runs rNN_<type>_<target>: rename them in their builders"]
          + CHANGES["runs"] +
          ["one name for every Run, run-<type>-<target> (JL); hard or soft is its kind: and its result/, a repeat "
           "names what it reads (-v<k>), never a counter (was rNN_<type>_<target> for hard)"])
    L.close_frame(fr, pad=40)

    # 2 · one Job, in order
    y = bottom() + 200
    fr = L.open_frame("one Job, in order")
    L.text(0, y, "One Job, in order: each step, its skill, its check", 30)
    fx, fy = 0, y + 110
    for k, (step, skill, note) in enumerate(FLOW):
        L.base("rectangle", fx, fy, 280, 64, L.INK, 1.5)
        L.text(fx + 16, fy + 18, step, 20)
        L.text(fx, fy + 80, skill, 14, L.RED if skill.endswith("?") else L.INK, L.MONO)
        L.text(fx, fy + 104, note, 14, L.RED if note.endswith("?") else L.GRAY)
        if k < len(FLOW) - 1:
            L.path([(fx + 288, fy + 32), (fx + 352, fy + 32)], color=L.INK)
        fx += 360
    vx = 4 * 360 + 140                                 # revise loops inside generate · verify
    L.path([(vx + 40, fy - 4), (vx + 40, fy - 40), (vx - 40, fy - 40), (vx - 40, fy - 4)], color=L.GRAY, dashed=True)
    L.text(vx - 120, fy - 66, "fails → run-revise → verify v<k+1>", 14, L.GRAY)
    lx, ox = 7 * 360 + 140, 2 * 360 + 140              # the scorecard → a new method version → a new Job
    L.path([(lx, fy + 130), (lx, fy + 170), (ox, fy + 170), (ox, fy + 130)], color=L.GRAY, dashed=True)
    L.text(ox + 40, fy + 180, "a method version that loses becomes a proposal; its next version is a new Job, never an "
                              "edit", 14, L.GRAY)
    L.text(0, fy + 230, "a person signs the goal once at the Block, then the release; verify and rank are never by the "
                        "agent that generated; the Exp is outside the theme, its totals come back to the Block", 16,
           L.GRAY)
    notes(0, fy + 270, CHANGES["flow"])
    L.close_frame(fr, pad=40)

    # 3 · the skills
    y = bottom() + 200
    fr = L.open_frame("the skills")
    L.text(0, y, "The skills behind the Runs", 30)
    L.text(0, y + 46, "skills/2_theme/design/ · callers = files elsewhere in the toolkit that name it · old = times its "
                      "docs still write Design Item, Commission, Design-NN, run-design-, _by-, rNN_ … · red = changes "
                      "on the new ladder", 16, L.GRAY)
    uses = {}
    for rows in by_level.values():
        for r in rows:
            uses.setdefault(r[8].replace(" (new)", "").rstrip(" ?"), []).append(r[0])
    rows = []
    for d in sorted(p for p in DESIGN.iterdir() if (p / "SKILL.md").is_file()):
        s = (d / "SKILL.md").read_text(encoding="utf-8")
        v = re.search(r'version: "?([\d.]+)', s)
        owns, ladder = SKILL_JOB.get(d.name, ("?", "?"))
        names = " · ".join(sorted(set(uses.get(d.name, []))))
        rows.append([d.name, "v" + (v.group(1) if v else "?"), f"{len(callers(d.name))}",
                     f"{len(s.splitlines())}", owns, clip(names, 64) or "-", str(stale(d)), ladder])
    for name, owns, ladder in NEW_SKILLS:
        names = " · ".join(sorted(set(uses.get(name, []))))
        rows.append([name + " ?", "-", "-", "-", owns, clip(names, 64) or "-", "-", ladder])
    y2 = table(0, y + 100, [("skill", 330), ("version", 90), ("callers", 80), ("lines", 70), ("owns", 520),
                            ("Runs that use it", 620), ("old", 60), ("on the new ladder", 640)], rows)
    rows = []
    for group, names in BORROWS:
        for n in names:
            p = find_skill(n)
            rows.append([n, group, p.parent.relative_to(SKILLS).as_posix() + "/" if p else "not found ?",
                         str(len(uses.get(n, [])) or "-")])
    y2 = table(0, y2 + 60, [("skill", 330), ("borrowed for", 440), ("where", 400), ("Runs", 80)], rows)
    rows = [[f"{n}/", f"{k} files · {kb:.0f} KB", "its own git repo ?" if repo else "in Tools · kept as it is"]
            for n, k, kb, repo in not_skills()]
    y2 = table(0, y2 + 60, [("in 2_theme/design, no skill", 330), ("size", 220), ("kind", 300)], rows)
    notes(0, y2 + 30, ["decided: the method registry is haipipe-design-method/methods/ (its own clock); s12's note and "
                       "design_reader.py's comment still say haipipe-design-unit/methods/",
                       "? the design family is pinned at 0.4.0 and only a person may change it: 0.5.0 for this "
                       "rewrite?",
                       "applied: the skills rewritten to the ladder; old-name counts above are what is left (legacy refs "
                       "keep the older board's words on purpose)"] + CHANGES["skills"])
    L.close_frame(fr, pad=40)

    # 3b · skill folders, before → after
    y = bottom() + 200
    fr = L.open_frame("skill folders: before → after")
    L.text(0, y, "The skill folders, before → after: what changes, and why", 30)
    L.text(0, y + 46, "skills/2_theme/design/ · before = the morning of 261007 · after = the plan · done = on disk now · "
                      "a file with no row below is kept as it is · red ? = not done yet", 16, L.GRAY)
    before = BEFORE
    missing = [p for p in FOLDERS if p not in before]
    after = sorted({FOLDERS[p][0].rstrip(" ?") if p in FOLDERS else p for p in before} - {""} |
                   {p for p, *_ in NEW_FILES}, key=by_folder)
    verb_of = {FOLDERS[p][0].rstrip(" ?"): FOLDERS[p][1] for p in FOLDERS if FOLDERS[p][0]}
    verb_of.update({p: "new" + (" ?" if w.endswith("?") else "") for p, w, *_ in NEW_FILES})
    yb = draw_tree(0, y + 110, "before · today", tree(before, lambda p: FOLDERS[p][1] if p in FOLDERS else ""),
                   lambda p: L.RED if p in FOLDERS and FOLDERS[p][1] == "retire" else
                   L.INK if p in FOLDERS else L.GRAY)
    ya = draw_tree(1100, y + 110, "after · proposed", tree(after, lambda p: verb_of.get(p, "")),
                   lambda p: L.RED if verb_of.get(p, "").endswith("?") else
                   L.INK if p in verb_of else L.GRAY)
    L.path([(900, y + 200), (1040, y + 200)], color=L.INK)
    def done(after):                                   # the after file is on disk (a pattern: any match)
        pat = re.sub(r"<[^>]+>", "*", after).replace("MNN", "M??")
        return "✓" if after and any(DESIGN.glob(pat)) else "⬜ ?"
    rows = [[p, FOLDERS[p][0] or "-", FOLDERS[p][1], FOLDERS[p][2], FOLDERS[p][3], FOLDERS[p][4], done(FOLDERS[p][0])]
            for p in FOLDERS if p in before]
    rows += [["-", p, "new", what, why, ph, done(p)] for p, what, why, ph in NEW_FILES]
    rows.sort(key=lambda r: r[5])
    yt = table(0, max(yb, ya) + 80, [("before", 560), ("after", 600), ("change", 110), ("what", 470),
                                      ("why", 520), ("phase", 70), ("done", 70)], rows, size=14,
               mono=("before", "after"))
    keep = len([p for p in before if p not in FOLDERS])
    notes(0, yt + 30, [f"kept as they are: {keep} files (no change mark beside them in either tree)"] +
          [f"? named here but not on disk: {p}" for p in missing] + CHANGES["folders"] +
          ["shaped like b16's paper plan: one ladder contract in ref/, one scaffold script for every level"])
    L.close_frame(fr, pad=40)

    # 4 · skill x Run
    y = bottom() + 200
    fr = L.open_frame("skill x Run")
    L.text(0, y, "Which skill each Run loads, after the plan", 30)
    L.text(0, y + 46, "x = the skill exists today · x ? = a skill the plan makes (new)", 16, L.GRAY)
    names = ["haipipe-design", "-goal", "-method", "-unit", "-workflow", "-delivery"]
    full = ["haipipe-design"] + ["haipipe-design" + n for n in names[1:]]
    cols = [("Run", 520)] + [(n, 140) for n in names] + [("other", 300)]
    rows = []
    for lv in ("Block", "Job", "Task"):
        for r in by_level.get(lv, []):
            sk = r[8].replace(" (new)", "").rstrip(" ?")
            mark = "x ?" if "(new)" in r[8] else "x"
            rows.append([f"{lv} · {r[0]}"] + [mark if sk == f else "" for f in full] +
                        ["" if sk in full else r[8]])
    table(0, y + 90, cols, rows, mono=("Run",))
    notes(0, bottom() + 30, CHANGES["matrix"])
    L.close_frame(fr, pad=40)

    # 5 · Runs on disk
    y = bottom() + 200
    fr = L.open_frame("Runs on disk")
    L.text(0, y, f"The Runs in the {n_boards} Project design boards today", 30)
    L.text(0, y + 46, "run type · layout · count; names only, no Board or design is named", 16, L.GRAY)
    by_type = Counter((run_type(s), shelf) for s, shelf in runs)
    rows = [[t, shelf, str(k) + (" ?" if t.startswith("run-design-") else "")]
            for (t, shelf), k in sorted(by_type.items(), key=lambda x: -x[1])]
    rows += [["any run-<type>-<target>", "ladder", "0 ?"]] if not any(s == "ladder" for _, s in by_type) else []
    yb = table(0, y + 100, [("run type", 330), ("layout", 200), ("count", 90)], rows, mono=("run type",))
    yn = table(800, y + 100, [("form", 220), ("name", 470), ("note", 520)], [
        ["today, old layout", "run-design-<step>-<MMDD>-<slug>", "commission · generate · verify, in a Design-NN"],
        ["older, renamed once", "rdNN_<step>_…", "rename_runs.py (moves to carry_over/)"],
        ["drawn, s12 · s13", "rNN_<type>_<target>", "hard Runs in the level drawings ?"],
        ["new, every Run", "run-<type>-<target>", "hard: result/ · soft: its level's folders"],
        ["a repeat", "run-verify-d<NN>-v<k>", "names the draft it read, never a counter"]], mono=("name",))
    notes(0, max(yb, yn) + 30, ["? no design board uses the new ladder yet: every Run on disk is the old layout's; the "
                                "carry-over (phase 6) moves them, or they stay as read-only history"] + CHANGES["disk"])
    L.close_frame(fr, pad=40)

    # 6 · the skill update plan
    y = bottom() + 200
    fr = L.open_frame("skill update plan")
    L.text(0, y, "The skill update plan: every Run above gets an owner", 30)
    L.text(0, y + 46, "phases in the order they unblock each other: the contract first, so every later skill has a "
                      "folder to write; then what a design reads, the worker, the Runs and release, the screens; old "
                      "words last", 16, L.GRAY)
    status = {"haipipe-design": "✓", "haipipe-design-goal": "✓", "haipipe-design-method (new) ?": "✓",
              "haipipe-design-unit": "✓", "agents": "✓", "haipipe-design-workflow": "✓",
              "haipipe-design-delivery (new) ?": "✓", "workbench-design": "SKILL ✓ · views ⬜ ?", "all": "⬜ ?"}
    rows = [[*p[:2], p[2], p[3], p[4], status.get(p[1], "⬜ ?")] for p in PLAN]
    for r in rows:
        r[1] = r[1].replace(" (new) ?", " (new)")
    yp = table(0, y + 100, [("phase", 140), ("skill", 330), ("what it learns", 900), ("Runs it gains", 640),
                            ("done when", 380), ("status", 230)], rows)
    notes(0, yp + 30, CHANGES["plan"])
    L.close_frame(fr, pad=40)
    canvas.write(out, list(L.els), "build_s21_run_skill.py")


if __name__ == "__main__":
    main()
