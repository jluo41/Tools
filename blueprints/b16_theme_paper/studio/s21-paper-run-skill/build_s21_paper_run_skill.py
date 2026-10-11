"""b16 s21 · Run and skill: s21-paper-run-skill.excalidraw, every paper Run type and the skills behind them.

JL 261007: "focus on show what are the skills and runs we have in the paper set"; then "the current skill is not
that powerful enough … make a plan to update the skills"; drawn in b12's s21-run-skill style (lines-only tables,
black, red for what is open, green for what changed). Seven frames, top to bottom:
  1. Runs by level: every run type a Space shows in s11 · s12 · s13, where it stands today (a run card, the base
     frame, on screen only, drawn only), its folder, who does it, who checks it, its skill;
  2. one version, in order: set up the Board → Story → open a version → write the Sections → release → build and
     check → send → comments, the skill under each step;
  3. the skills: each paper skill and the base skills it borrows: what it owns, the Runs that use it, how often it
     still writes an old name, what changes on the new ladder;
  3b. skill folders, before → after: today's tree read from disk, the proposed tree, and per file the change,
     what it does, why, and the plan phase that makes it;
  4. skill × Run: which skill each run type loads;
  5. Runs on disk: the Runs in the Project paper folders by type and shelf, and the Run names;
  6. the skill update plan: six phases, each skill's change and the run types it gains.

Read from disk every build: the skills in skills/2_theme/paper; the level builders' SCREENS and ROWS (imported,
never run); the run cards (paper and Page run-cards.md); the live paper workbench (paper_theme.py) and the base
frame (servers/workbench); the Runs in the Project paper folders (names only, never their content; no Board or
Section name is drawn). Typed, since they are the proposal: each skill's job and ladder change, the owner and
folder of a run type with no card yet, and the plan. What changed is a dated green line (JL 261007). The first cut
is history/build_s21_paper_run_skill-261007-v1.py. canvas.write keeps every mark a person adds through a rebuild.

    python build_s21_paper_run_skill.py [out.excalidraw]
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
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
import canvas  # noqa: E402

L.GRAY = canvas.INK                 # the studio palette (haipipe-studio 0.2.0): black, red for open, green for a change

SPACE = Path(__file__).resolve().parents[5]
TK = Path(__file__).resolve().parents[4] / "plugins" / "haipipe-toolkit"
SKILLS = TK / "skills"
PAPER = SKILLS / "2_theme" / "paper"
CARDS = PAPER / "haipipe-paper-workflow" / "ref" / "run-cards.md"
PAGE_CARDS = SKILLS / "1_base" / "page" / "haipipe-page-workflow" / "ref" / "run-cards.md"
LIVE = TK / "servers" / "workbench-paper" / "paper_theme.py"          # the paper workbench as it runs today
BASE = TK / "servers" / "workbench"                                    # the frame every theme shares
LEVELS = [("Block", "s11-paper-block/build_s11_paper_block.py"),
          ("Job", "s12-paper-job/build_s12_paper_job.py"),
          ("Task", "s13-paper-task/build_s13_paper_task.py")]

# ── the typed part (proposal, 261007) ──────────────────────────────────────────────────────────
# each paper skill: what it owns, and what changes on the new ladder ("?" = must change, red)
SKILL_JOB = {
    "haipipe-paper": ("the door; ref/paper-ladder.md; paper_ladder.py (board · version · task · run)",
                      "done 261007: one contract and one scaffold for B J T R"),
    "haipipe-paper-workflow": ("run cards by <Level> › <Space>; gates G0-G2 Board, G3-G5 version",
                               "done 261007: one card per button"),
    "workbench-paper": ("the paper theme on the shared frame; buttons from the cards",
                        "done 261007: the old page's text is ref/old-page.md"),
    "haipipe-paper-ideation": ("studio/s01-ideation/ + ideation Questions",
                               "done 261007: no Ideation Page on the ladder"),
    "haipipe-paper-story": ("a telling as a studio topic + Board Questions; ref/narrative.md",
                            "done 261007: no Story Page on the ladder"),
    "haipipe-paper-venue": ("venues/<venue>/ call.md + kit/; the shared Venue Pages",
                            "one home for both (Q02) ?"),
    "haipipe-paper-assemble": ("one version's build; the t31 letter; send to a comments report",
                               "done 261007"),
    "haipipe-paper-comments": ("comments reports; review_items.py add · route · reply",
                               "done 261007"),
    "haipipe-paper-section": ("a Section Task: Narrative row, Requirement, studio/ reports/",
                              "done 261007: ref/requirement.md")}
# old names a skill should no longer write (the ladder and Q04 replaced them, 261007)
STALE = r"Story Page|Ideation Page|A1-Story|\bB[abc]-|RD<NN>|RD\d\d-|S-<desk>|S-[A-Z][A-Za-z]+-Main|-<MMDD>-"
# the base skills a paper borrows, by what they do for it
BORROWS = [("Page workflow: every Section and letter Task",
            ["haipipe-page-workflow", "haipipe-page-context", "haipipe-page-structure", "haipipe-page-evidence",
             "haipipe-page-writing", "haipipe-page-scratch", "haipipe-page-revise", "haipipe-page-delivery",
             "haipipe-page-check"]),
           ("Ideation: the idea pool", ["haipipe-ideation", "haipipe-ideation-generate", "haipipe-ideation-test",
                                        "haipipe-ideation-select"]),
           ("supporting work: other themes' hard Runs", ["haipipe-task", "haipipe-discovery"]),
           ("shared", ["haipipe-question", "haipipe-run", "haipipe-display", "excalidraw-section", "table-papers"])]
# a run type with no card yet: its proposed owner skill (the plan gives each its card)
OWNER = {"Update the Board": "haipipe-paper",
         "Add a resource": "haipipe-paper",
         "Open a version": "haipipe-paper",
         "Open a grant": "haipipe-paper",
         "Update the Board status": "haipipe-paper",
         "Update the version": "haipipe-paper",
         "Add a venue": "haipipe-paper-venue",
         "Check the rules": "haipipe-paper-venue",
         "Add a related item": "haipipe-paper",
         "Read a paper": "haipipe-discovery",
         "Ask a Question": "haipipe-question",
         "Ask a question": "haipipe-question",
         "Generate ideas": "haipipe-paper-ideation",
         "Test idea": "haipipe-paper-ideation",
         "Review for an audience": "haipipe-paper-story",
         "Build reference.bib": "haipipe-paper-assemble",
         "Redraw the paper map": "excalidraw-section",
         "Release a Section": "haipipe-paper-workflow",
         "Add comments": "haipipe-paper-comments", "Add a letter": "haipipe-paper-section",
         "Route an item": "haipipe-paper-comments",
         "Reply to an item": "haipipe-paper-comments",
         "Write the cover letter": "haipipe-paper-assemble",
         "Check the letter": "haipipe-paper-assemble",
         "Add a Section": "haipipe-paper-section",
         "Send": "haipipe-paper-assemble",
         "Draw": "the frame", "+ Add topic": "the frame",
         "Add a method": "the frame", "Add a paper": "the frame",
         "Run": "the frame"}
# one name per run type, run-<type>-<target> (JL 261007: "unify the run to be run-xxx-xxx"); a card's own ticket
# pattern names it when it has one. Two buttons that make the same Run share one row. The only other form is a
# supporting Run of another theme: its hard rNN_ keeps its own name (run-naming.md: never renamed for the paper).
RUN_NAME = {"Update the Board": "run-update-board", "Add a venue": "run-add-venue-<venue>",
            "Check the rules": "run-check-venue-<venue>", "Add a resource": "run-add-resource-<slug>",
            "Add a related item": "run-add-related-<slug>", "Draw": "run-draw-<sNN>",
            "+ Add topic": "run-add-topic-<sNN>", "Ask a Question": "run-ask-<qNN>",
            "Ask a question": "run-ask-<qNN>", "Generate ideas": "run-generate-ideas",
            "Test idea": "run-test-idea-<idea>", "Story revise": "run-revise-story-<telling>",
            "Review for an audience": "run-review-audience-<who>", "Write the report": "run-report-<qNN>",
            "Review the report": "run-check-<qNN>", "Open a version": "run-open-version-<jNN>",
            "Open a grant": "run-open-grant-<jNN>", "Update the Board status": "run-update-status",
            "Build reference.bib": "run-build-bib", "Add a method": "run-add-method-<slug>",
            "Add a paper": "run-add-paper-<slug>", "Update the version": "run-update-version-<jNN>",
            "Redraw the paper map": "run-draw-papermap-<jNN>", "Release a Section": "run-release-section-<tNN>",
            "Add comments": "run-add-comments-<qNN>", "Add a letter": "run-add-letter-<tNN>", "Route an item": "run-route-item-<item>",
            "Reply to an item": "run-reply-item-<item>", "Write the cover letter": "run-write-letter-<tNN>",
            "Cover letter": "run-write-letter-<tNN>", "Check the letter": "run-check-letter-<tNN>",
            "Response": "run-write-response-<tNN>", "Add a Section": "run-add-section-<tNN>",
            "Draft runs": "run-<kind>-<slug> (each Section's)", "Send": "run-send-version-<jNN>",
            ("Job", "Build"): "run-build-version-<jNN>", ("Job", "Check"): "run-check-submission-<jNN>",
            "Read a paper": "rNN_<author><year>_<subject> (discovery)",
            "Task runs": "rNN_<slug> (work Task)", "Discovery runs": "rNN_<slug> (discovery Task)"}
NOT_A_RUN = {"Run"}                                   # the Runs Space's own start button, not a run type

# which Runs on disk a card counts (a stem pattern, and the shelf it sits on)
COUNTS = {"Narrative review": (r"^run-paper-narrative-", "story"), "Task review": (r"^run-paper-task-", "story"),
          "Story revise": (r"^run-(structure|scratch|section|paragraph|revise|auto-write|evidence-embed|context)-",
                           "story")}
# 2 · one version, in order: (step, skill, note)
FLOW = [("set up the Board", "-paper · -venue", "scope · venue · related"),
        ("the Story", "haipipe-paper-story", "RQs as Questions, G0-G2"),
        ("open a version", "haipipe-paper", "j0N_v<MMDD>_<desk>/"),
        ("write the Sections", "haipipe-page-*", "t0N_ · t2N_, Page Runs"),
        ("release a Section", "-paper-workflow ?", "G3, a person signs"),
        ("build · check", "-paper-assemble", "G4 submission ready"),
        ("send", "-paper-assemble ?", "with t31_ cover letter"),
        ("comments", "-paper-comments", "reports/qNN_, then G5")]
# 6 · the skill update plan: (phase, skill, what it learns, run types it gains, done when)
PLAN = [("1 · contract", "haipipe-paper",
         "one folder law for B J T R; scaffold new board · version · task · run, runs/README.md",
         "Update the Board · Open a version · Update the version · Add a resource · Board status",
         "a demo Block scaffolds and opens"),
        ("2 · cards", "haipipe-paper-workflow",
         "run-cards.md by level × the six Spaces (was Ideation · Story · Sections · Delivery); gates to levels",
         "a card for every run type in frame 1; old cards placed or retired",
         "table-workbench --check --cards"),
        ("2 · cards", "workbench-paper",
         "paper_theme.py reads run types from the cards, not typed labels; the old page retires",
         "every button names its skill, agent and sign",
         "workbench-paper and _host tests"),
        ("3 · Block", "haipipe-paper-story",
         "studio/sNN-story-<telling>/ face; RQs as Board Questions + reports/qNN_; Narrative N1-N4",
         "Story revise · Review for an audience · Narrative review",
         "TestToLearn's Story rebuilt"),
        ("3 · Block", "haipipe-paper-ideation",
         "studio/s01-ideation/ + Questions (group ideation), via haipipe-ideation-*",
         "Generate ideas · Test idea", "no Ideation Page written"),
        ("3 · Block", "haipipe-paper-venue",
         "venues/<venue>/ call.md + kit/; Related through discovery reads",
         "Add a venue · Check the rules · Add a related item", "Q02 settled"),
        ("4 · Job", "haipipe-paper-comments",
         "a script that reads and writes a comments report's ## Review Items",
         "Add a review · Route an item · Reply to an item", "j02's editor decision routed"),
        ("4 · Job", "haipipe-paper-assemble",
         "build from the version folder; cover letter from t31_; Send; reference.bib",
         "Send · Write the cover letter · Check the letter · Build reference.bib", "j02 builds and checks"),
        ("4 · Job", "haipipe-paper-workflow",
         "the version face: ## Narrative and the standing J1-J5 questions; the G3 release",
         "Release a Section", "a Section released on j02"),
        ("5 · Task", "haipipe-paper-section",
         "t0N_ · t2N_ · t3N_; reader contract; Requirement = V · W rules + rubric + SUB-*; studio/ reports/",
         "Add a Section (the rest are the Page's, carded)", "a new Section scaffolds"),
        ("6 · old words", "all nine",
         "drop Story Page, B[abc]-, RD<NN>, S-<desk>, -<MMDD>- (counts in frame 3); versions, CHANGELOGs",
         "-", "0 old names; tests pass")]

# 3b · skill folders, before → after (proposal, 261007). Each file today, by its path in 2_theme/paper/:
# (after path or "" to retire, change, why, plan phase). A file not named here is kept as it is.
# Shaped like the design theme's skill: one ladder contract in ref/, one scaffold script for every level.
FOLDERS = {
    "haipipe-paper/SKILL.md": ("haipipe-paper/SKILL.md", "rewrite",
        "routes by level: Board · version · Section", "it routes by Page type (Story, Section, Round)", "1"),
    "haipipe-paper/ref/paper-structure.md": ("haipipe-paper/ref/paper-ladder.md", "rename",
        "the B J T R tree, one face per level", "one contract per theme, named like design-ladder.md", "1"),
    "haipipe-paper/ref/page-integration.md": ("haipipe-paper/ref/page-integration.md", "edit",
        "Sections and letters are Page Tasks", "a Section is a Page Task (b03)", "1"),
    "haipipe-paper/ref/run-naming.md": ("haipipe-paper/ref/run-naming.md", "edit",
        "run-<type>-<slug>, no date; Runs per level", "dates dropped 261007; Story shelves gone", "1"),
    "haipipe-paper/ref/section-sessions.md": ("haipipe-paper/ref/section-sessions.md", "edit",
        "one session per t0N_ · t2N_ Task", "Sections are renamed t0N_", "5"),
    "haipipe-paper/scripts/version_paper.py": ("haipipe-paper/scripts/paper_ladder.py", "merge",
        "new board · version · task · run, + runs/README.md", "a scaffold for every level; today only versions",
        "1"),
    "haipipe-paper/scripts/migrate_paper.py": ("haipipe-paper/scripts/carry_over/migrate_paper.py", "move",
        "old Boards onto the ladder, once", "a carry-over, not how a paper is made", "6"),
    "haipipe-paper/scripts/rename_tasks.py": ("haipipe-paper/scripts/carry_over/rename_tasks.py", "move",
        "S-… to t0N_, RD to reports/, once", "a carry-over, not how a paper is made", "6"),
    "haipipe-paper/scripts/topics_paper.py": ("haipipe-paper/scripts/carry_over/topics_paper.py", "move",
        "Story Pages to topics + Questions, once", "a carry-over, not how a paper is made", "6"),
    "haipipe-paper/scripts/create_section_sessions.py": ("haipipe-paper/scripts/create_section_sessions.py",
        "edit", "finds Sections as t0N_ · t2N_", "it looks for S-<desk>-Main-N", "5"),
    "haipipe-paper-workflow/SKILL.md": ("haipipe-paper-workflow/SKILL.md", "rewrite",
        "gates by level: G0-G2 Board, G3-G5 version", "gates hang on Story and Round Pages", "2"),
    "haipipe-paper-workflow/ref/run-cards.md": ("haipipe-paper-workflow/ref/run-cards.md", "rewrite",
        "one card per button, by level × six Spaces", "24 designed buttons have no card", "2"),
    "haipipe-paper-workflow/ref/run-workflow.md": ("haipipe-paper-workflow/ref/run-workflow.md", "edit",
        "routes between levels", "routes between the old Pages", "2"),
    "workbench-paper/SKILL.md": ("workbench-paper/SKILL.md", "rewrite",
        "the theme on the shared frame (paper_theme.py)", "it describes the old page's four Spaces", "2"),
    "workbench-paper/ref/space-mapping.md": ("", "retire",
        "its rows move into run-cards.md", "it maps the four old Spaces", "2"),
    "workbench-paper/ref/workbench-table.md": ("workbench-paper/ref/workbench-table.md", "regenerate",
        "written from the new cards", "it must match the cards (table-workbench)", "2"),
    "haipipe-paper-story/SKILL.md": ("haipipe-paper-story/SKILL.md", "rewrite",
        "writes studio/sNN-story-<telling>/ + Questions", "Q04: no Story Page", "3"),
    "haipipe-paper-story/ref/integration.md": ("haipipe-paper-story/ref/integration.md", "rewrite",
        "a telling feeds the version's ## Narrative", "§8 moved to the version face", "3"),
    "haipipe-paper-ideation/SKILL.md": ("haipipe-paper-ideation/SKILL.md", "rewrite",
        "writes studio/s01-ideation/ + Questions", "Q04: no Ideation Page", "3"),
    "haipipe-paper-venue/SKILL.md": ("haipipe-paper-venue/SKILL.md", "rewrite",
        "writes venues/<venue>/ call.md + kit/", "the Board's Description › Venue (Q02 ?)", "3"),
    "haipipe-paper-venue/template.md": ("haipipe-paper-venue/template.md", "keep",
        "the shared Venue Page scaffold", "the bank's Venue Pages link to it here", "3"),
    "haipipe-paper-comments/SKILL.md": ("haipipe-paper-comments/SKILL.md", "edit",
        "runs its three buttons through its script", "Add a review · Route · Reply have no runner", "4"),
    "haipipe-paper-assemble/SKILL.md": ("haipipe-paper-assemble/SKILL.md", "edit",
        "builds one version folder; Send; reference.bib", "Send and reference.bib have no runner", "4"),
    "haipipe-paper-assemble/scripts/build_delivery.py": ("haipipe-paper-assemble/scripts/build_delivery.py",
        "edit", "+ send, + bib", "Send and Build reference.bib are drawn only", "4"),
    "haipipe-paper-assemble/scripts/cover_letter.py": ("haipipe-paper-assemble/scripts/cover_letter.py", "edit",
        "reads the t31_cover-letter Task", "letters are t3N_ Tasks now", "4"),
    "haipipe-paper-assemble/profiles/misq.toml": ("haipipe-paper-assemble/profiles/misq.toml", "keep ?",
        "or into venues/<venue>/kit/", "one home for a venue's rules (Q02 ?)", "3"),
    "haipipe-paper-section/SKILL.md": ("haipipe-paper-section/SKILL.md", "rewrite",
        "t0N_ names; reader contract; Requirement tab", "it still names S-<desk>-Main-N", "5"),
    "README.md": ("README.md", "edit", "the family by level", "it lists the skills by Page type", "6"),
    "venue/": ("venue/ ?", "move ?", "outside skills/, registered", "its own 821 MB repo the installer scans", "6"),
}
# the tree the plan started from (261007, before phase 1): the before side of frame 3b. Frozen, since the phases
# change the disk; the after side and each row's state are read from disk
BASELINE = """README.md tests/test_run_naming.py venue/
haipipe-paper/SKILL.md haipipe-paper/ref/page-integration.md haipipe-paper/ref/paper-structure.md
haipipe-paper/ref/run-naming.md haipipe-paper/ref/section-sessions.md haipipe-paper/ref/submission-readiness.md
haipipe-paper/scripts/audit_page_compatibility.py haipipe-paper/scripts/create_section_sessions.py
haipipe-paper/scripts/migrate_paper.py haipipe-paper/scripts/rename_tasks.py haipipe-paper/scripts/topics_paper.py
haipipe-paper/scripts/version_paper.py
haipipe-paper-assemble/SKILL.md haipipe-paper-assemble/profiles/jama-internal-medicine.toml
haipipe-paper-assemble/profiles/misq.toml haipipe-paper-assemble/ref/build.py.wrapper
haipipe-paper-assemble/ref/paper-build.toml.example haipipe-paper-assemble/scripts/build_delivery.py
haipipe-paper-assemble/scripts/cover_letter.py haipipe-paper-assemble/scripts/latex_room_to_docx.py
haipipe-paper-assemble/tests/run.sh haipipe-paper-assemble/tests/test_build_delivery.py
haipipe-paper-assemble/tests/test_latex_room_to_docx.py
haipipe-paper-comments/SKILL.md haipipe-paper-comments/agents/openai.yaml
haipipe-paper-ideation/SKILL.md
haipipe-paper-section/SKILL.md haipipe-paper-section/cli/resolve-structure.py haipipe-paper-section/cli/section-stats.py
haipipe-paper-section/ref/generic-template.md
haipipe-paper-story/SKILL.md haipipe-paper-story/agents/openai.yaml haipipe-paper-story/ref/integration.md
haipipe-paper-venue/SKILL.md haipipe-paper-venue/ref/profile-examples.md haipipe-paper-venue/template.md
haipipe-paper-workflow/SKILL.md haipipe-paper-workflow/ref/run-cards.md haipipe-paper-workflow/ref/run-workflow.md
workbench-paper/SKILL.md workbench-paper/ref/space-mapping.md workbench-paper/ref/workbench-table.md""".split()
PHASES_DONE = {"1", "2", "3", "4", "5", "6"}         # each phase run so far (g04); a row of a later phase stays "to do"
# the files only the after tree has: (path, what it is, why, plan phase)
NEW_FILES = [
    ("tests/test_paper_ladder.py", "the scaffold makes each level and opens", "the contract has teeth", "1"),
    ("haipipe-paper-story/ref/narrative.md", "Narrative N1-N4 and the audience review",
     "Spine and Design merged into Narrative (JL)", "3"),
    ("haipipe-paper-comments/scripts/review_items.py", "add · route · reply over ## Review Items",
     "the Job's three comments buttons; takes version_paper.py comments", "4"),
    ("workbench-paper/ref/old-page.md", "the retired four-Space page: what its renderers show",
     "several frame views still draw with them (pv)", "2"),
    ("haipipe-paper-venue/ref/call-template.md", "the venues/<venue>/call.md scaffold",
     "a Board's own copy of a venue's call", "3"),
    ("haipipe-paper-section/ref/requirement.md", "V · W rules, the four-axis rubric, SUB-* rows",
     "s13 made Requirement its own tab", "5")]

CHANGES = {
    "runs": ["re-cut from s11 · s12 · s13: every run type a Space shows, by level (was the cards of run-cards.md)",
             "today: card · base · screen (a button no card owns) · drawn (only in the drawing)",
             "drawn in b12's s21 style: lines-only tables (JL 261007)",
             "one name per Run, run-<type>-<target>; the button beside it; two buttons for one Run share a row "
             "(JL 261007: \"unify the run to be run-xxx-xxx\")"],
    "flow": ["new frame: one version in order, the skill under each step"],
    "skills": ["haipipe-paper-round renamed haipipe-paper-comments: reviews, meetings, coauthors → Review Items",
               "its draft (was s22) sits here: haipipe-paper-comments-draft.md",
               "Ideation and Story are run types, no Pages: studio topics + Board Questions + reports (Q04)",
               "new column: how often each skill still writes an old name"],
    "matrix": ["new frame: which skill each run type loads; ? = proposed owner, no card yet"],
    "disk": ["Sections t0N_ · t2N_ in j0N_v<MMDD>_<desk>/ count as section; reports/ in a version as comments",
             "Run names drop <MMDD>: run-<type>-<slug>, passes inside the one file (page engine 0.124.0)"],
    "folders": ["new frame: the skill folders before → after, each change with its why (JL 261007: \"a before after plan of the skill folders and what to change and why\")",
                "shaped like the design theme's skill: ref/paper-ladder.md + scripts/paper_ladder.py"],
    "done": ["base match (261007): the run cards carry a 🏷 RUN line, read here; shared buttons make the base Runs "
             "(run-face · run-add · run-draw · run-ask · run-report · run-figures · run-check · run-delivery)",
             "faces follow haipipe-board / -job: board-kind, goal, close, ## Tasks, task-kind: page; no empty folders; "
             "responds-to: (not answers:) on a version",
"phase 1 done: ref/paper-ladder.md, scripts/paper_ladder.py (board · version · next · spaces · task · run · "
             "rollback), carry_over/, review_items.py add; tests 7/7",
             "phase 2 done: run-cards.md by <Level> › <Space>, one card per button; paper_theme.py reads them "
             "(_run_cards); workbench-table check PASS; workbench-paper + _host 85/85",
             "\"Add a review\" is \"Add comments\" (the table check reads \"review\" as judging); "
             "Letters has Add a letter",
             "phase 3 done: -story (studio topic, ref/narrative.md), -ideation (s01-ideation), -venue "
             "(venues/<venue>/, ref/call-template.md; template.md kept, the bank links it)",
             "phase 4 done: review_items.py route · reply; build.py send to a comments report; the letter from "
             "t31_; Send card; J1-J5 in the workflow skill",
             "phase 5 done: -section (Narrative row, ref/requirement.md, studio/ reports/), "
             "create_section_sessions.py reads tNN_",
             "phase 6 done: 0 old names left as current in the nine skills; versions and CHANGELOGs",
             "a Board's and a version's Runs are folders, runs/run-<type>-<target>/ (run.yaml, ticket, passes/), "
             "as haipipe-run has it",
             "tests: paper 8/8 · workbench-paper + _host 86 · assemble 66 (2 known Word failures) · table check PASS"],
    "plan": ["new frame: the skill update plan (JL 261007: \"the current skill is not that powerful enough\")",
             "Q05 registered, \"Which skills and Runs make the paper theme?\" (reports/q05_skills_and_runs/); "
             "run by goals/g04-paper-skills.md, phases 1-2 first"]}


# ── helpers, as b12's s21 draws them ──────────────────────────────────────────────────────────
def table(x, y, cols, rows, size=15, row_h=34, mono=("folder", "skill")):
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


# ── facts, read from disk ──────────────────────────────────────────────────────────────────────
def callers(name):
    """Files in the toolkit outside 2_theme/paper that name a skill (the venue bank is not read)."""
    out = subprocess.run(["grep", "-rlIw", "--exclude-dir=.git", "--exclude-dir=_legacy", "--exclude-dir=venue",
                          "--exclude=CHANGELOG.md", name, str(TK)], capture_output=True, text=True).stdout.split()
    return [o for o in out if not o.startswith(str(PAPER))]


# a line that says it is about the older layout may name it (older Boards are still read and carried over)
OLDER = re.compile(r"older|still read|legacy|historical|was |were |carry_over|carry-over|retired|readable|"
                   r"grandfathered", re.I)
OWN_WORD = {"haipipe-paper-ideation": "Ideation Page"}   # a skill's own name for its topic face, defined there


def stale(d):
    """How many lines of a skill's docs still write an old name as if current: its CHANGELOG is history, an
    "Older layouts" section and a line (or the line before it) that says older or still read may name them."""
    n = 0
    for f in d.rglob("*.md"):
        if f.name in ("CHANGELOG.md", "old-page.md"):
            continue
        lines, older = f.read_text(encoding="utf-8", errors="ignore").splitlines(), False
        for i, line in enumerate(lines):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if line.startswith("#") or (line.strip() and re.fullmatch(r"[-=]{3,}", nxt.strip())):
                older = "older" in line.lower()            # a heading opens a section: is it the older layouts'?
            hits = [h for h in re.findall(STALE, line) if h != OWN_WORD.get(d.name)]
            if hits and not older and not OLDER.search(line) and not (i and OLDER.search(lines[i - 1])):
                n += 1
    return n


def find_skill(name):
    return next((p for p in SKILLS.rglob(name) if (p / "SKILL.md").is_file()), None)


def not_skills():
    """What sits in 2_theme/paper but is no skill: its files and size on disk, and whether it is its own repo."""
    rows = []
    for d in sorted(p for p in PAPER.iterdir() if p.is_dir() and not (p / "SKILL.md").exists()
                    and not p.name.startswith((".", "_"))):
        files = [f for f in d.rglob("*") if f.is_file() and ".git" not in f.relative_to(d).parts]
        mb = sum(f.stat().st_size for f in files) / 2**20
        rows.append((d.name, len(files), mb, (d / ".git").exists()))
    return rows


def cards(path):
    """The run cards of one run-cards.md: {button: {space, pattern, skill, agent, signs}}."""
    out, cur = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("🔘 BUTTON"):
            label, space, pattern = (line.split(None, 2)[2].split(" · ") + ["", "", ""])[:3]
            cur = out.setdefault(label.strip(), {"space": space.strip(), "pattern": pattern.strip()})
        elif cur is not None and line.startswith(("🧩 SKILL", "🤖 AGENT", "✍️ SIGNS", "🏷 RUN")):
            val = line.split(None, 2)[2].strip()
            cur[line.split()[1].lower()] = val.split(": ", 1)[-1]          # "Build figure / table: haipipe-display"
    return out


def run_name(pattern):
    """A card's ticket pattern as a folder name: ^(?:rp-struct-|run-structure-) → run-structure-<slug>."""
    names = re.findall(r"run-[a-z]+(?:-[a-z]+)*", pattern)
    if not names:
        return "-"
    n = names[-1].rstrip("-")
    return n + ("-<lane>" if n == "run-delivery" else "-<slug>")


def agent_exists(name):
    return any(TK.rglob(name.split()[0] + ".md"))


def designed():
    """Every run type a screen shows in s11 · s12 · s13: [(level, 'Space › view', label)], in drawing order."""
    out = []
    for level, rel in LEVELS:
        spec = importlib.util.spec_from_file_location(f"s21_{level}", HERE.parent / rel)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)                       # the builders draw only under __main__
        if hasattr(m, "SCREENS"):                        # s11, s12: (space, third, run types, recent, body, files…)
            for e in m.SCREENS:
                on = next((lb for lb, o in (e[1] or ()) if o), "")
                out += [(level, e[0] + (f" › {on}" if on and on != "All" else ""), r) for r in e[2]]
        for e in getattr(m, "ROWS", ()):                 # s13: (space, views, run types, [(view, …, [run types])…])
            out += [(level, e[0], r) for r in e[2]]
            for v in e[3]:
                for x in v:
                    if isinstance(x, list) and x and all(isinstance(s, str) for s in x):
                        out += [(level, f"{e[0]} › {v[0]}", r) for r in x]
    seen, uniq = set(), []
    for lv, where, r in out:                             # one row per (level, Space › view, run type)
        key = (lv, where, r.lstrip("? "))
        if key not in seen:
            seen.add(key)
            uniq.append((lv, where, r.lstrip("? ")))
    return uniq


def paper_runs():
    """Every Run stem in a Project paper folder, with its shelf (story · section · comments · letters · delivery)."""
    seen = set()
    for paper in SPACE.glob("examples-*/*/paper*/Paper-*"):
        for d in paper.rglob("*"):
            if d.name not in ("runs", "results") or not d.is_dir() or {"_old", "_legacy"} & set(d.parts):
                continue
            rel = d.relative_to(paper).parts
            ver = re.match(r"j\d{2}_v", rel[0]) and len(rel) > 1      # the new layout: j0N_v<MMDD>_<desk>/…
            shelf = ("story" if rel[0].startswith(("A1-Story", "studio", "j00_story")) else
                     "section" if re.match(r"B[ab]-", rel[0]) or ver and re.match(r"(t[0-2]\d_|S-)", rel[1]) else
                     "comments" if rel[0].startswith("Bc-") or ver and re.match(r"(reports|comments|RD|CM)", rel[1])
                     else "letters" if ver and re.match(r"t3\d_", rel[1]) else
                     "delivery" if "delivery" in rel[:2] else "other")
            for r in d.iterdir():
                stem = re.sub(r"\.(md|sh|yaml)$", "", r.name)
                if re.match(r"^(run-|r\d|rresponse)", stem):
                    seen.add((paper.name, rel[:-1], stem, shelf))
    return [(stem, shelf) for _, _, stem, shelf in seen], len(list(SPACE.glob("examples-*/*/paper*/Paper-*")))


def run_type(stem):
    for pat, name in [(r"^run-paper-([a-z]+)-", "run-paper-{}"), (r"^run-delivery-([a-z]+)", "run-delivery-{}"),
                      (r"^run-(auto-write|evidence-embed)-", "run-{}"), (r"^run-([a-z]+)-", "run-{}"),
                      (r"^run-([a-z-]+)$", "run-{}")]:
        m = re.match(pat, stem)
        if m:
            return name.format(m.group(1))
    return "rNN_ (hard)" if re.match(r"^r\d", stem) else stem


def paper_files():
    """Every file in 2_theme/paper today, as paths in it; venue/ is one entry; CHANGELOGs and caches are left out."""
    out = []
    for f in sorted(PAPER.rglob("*")):
        rel = f.relative_to(PAPER)
        if rel.parts[0] == "venue":
            continue
        if f.is_file() and f.name != "CHANGELOG.md" and not {"__pycache__", ".git"} & set(rel.parts):
            out.append(rel.as_posix())
    return sorted(out + (["venue/"] if (PAPER / "venue").is_dir() else []), key=by_folder)


def by_folder(p):
    """Folder order: a folder's files before the next folder, haipipe-paper/ before haipipe-paper-…/."""
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


def said(label, code):
    """A button label written as a string in the code ("Send", not the word inside another name), or as what a
    frame button named by its Run does ("doing": "ask a question")."""
    return re.search(r"[\"']" + re.escape(label) + r"[\"']", code) is not None or \
        re.search(r"[\"']doing[\"']:\s*[\"']" + re.escape(label.lower()) + r"[\"']", code) is not None


def run_rows(runs):
    """Frame 1's rows per level, each run type with where it stands today; and the tally per level."""
    paper, page = cards(CARDS), cards(PAGE_CARDS)
    live = LIVE.read_text(encoding="utf-8")
    base = "\n".join(p.read_text(encoding="utf-8") for p in BASE.glob("*.py"))
    by_level, tally, used, merged = {}, {}, set(), {}
    for lv, where, label in designed():
        if label in NOT_A_RUN:
            continue
        c = next((cs[label] for cs in ((page, paper) if lv == "Task" else (paper, page)) if label in cs), None)
        owner = OWNER.get(label, "?")
        name = ((c or {}).get("run") or RUN_NAME.get((lv, label)) or RUN_NAME.get(label)   # the card's 🏷 RUN first
                or (run_name(c["pattern"]) if c else "-"))
        if c:
            used.add(label)
            st, skill = "card", c.get("skill", "?")
            agent = c.get("agent", "?")
            agent = agent if "(new)" in agent or agent_exists(agent) else agent + " (no file) ?"
            agent = agent.replace(" (new)", " (new) ?")
            signs = c.get("signs", "?")
            pat = COUNTS.get(label)
            n = str(sum(1 for s, shelf in runs if shelf == pat[1] and re.match(pat[0], s))) if pat else "-"
        elif owner == "the frame" or said(label, base):
            st, skill, agent, signs, n = "base", owner if owner != "?" else "the frame", "-", "-", "-"
        else:
            st = "screen ?" if said(label, live) else "drawn ?"
            skill, agent, signs, n = f"{owner} ?", "?", "?", "-"
        row = merged.get((lv, name))
        if row is None:                                  # first button for this Run
            merged[(lv, name)] = row = [name, label, where, st, agent, signs, skill, n]
            by_level.setdefault(lv, []).append(row)
        else:                                            # another button, or another Space, makes the same Run
            row[1] = row[1] if label in row[1].split(" · ") else f"{row[1]} · {label}"
            row[2] = row[2] if where in row[2].split(" · ") else f"{row[2]} · {where}"
            if st == "card" and row[3] != "card":
                row[3:7] = [st, agent, signs, skill]
    for lv, rows in by_level.items():
        tally[lv] = Counter(r[3].rstrip(" ?") for r in rows)
    left = [b for b in paper if b not in used]
    return by_level, tally, left, paper


# ── the drawing ────────────────────────────────────────────────────────────────────────────────
def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s21-paper-run-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    runs, n_papers = paper_runs()
    by_level, tally, left, paper = run_rows(runs)

    # 1 · Runs by level
    fr = L.open_frame("Runs by level")
    L.text(0, 0, "Paper Runs, level by level", 30)
    L.text(0, 46, "every Run a Space's buttons make in s11 · s12 · s13, one row per Run, named run-<type>-<target> · today: card = a run card names its skill, agent "
                  "and sign · base = the shared frame · screen = a button, but no card says who runs it · drawn = only "
                  "in the drawing · red ? = open", 16, L.GRAY)
    cols = [("Run", 400), ("button", 300), ("shows in", 450), ("today", 90), ("who does it", 300),
            ("who checks", 260), ("skill", 270), ("on disk", 80)]
    y = 100
    for level in ("Block", "Job", "Task"):
        t = tally[level]
        L.text(0, y, level, 20)
        L.text(0, y + 30, "\n".join(f"{t[k]} {k}" for k in ("card", "base", "screen", "drawn") if t[k]), 14, L.GRAY)
        y = table(120, y - 4, cols, by_level[level], mono=("Run", "skill")) + 30
    L.text(0, y + 10, "cards no screen shows", 20)
    rows = [[b, paper[b]["space"], paper[b].get("skill", "?"),
             "placed: no s11-s13 screen shows it yet ?" if "›" in paper[b]["space"] else "place it in a Space ?"]
            for b in left]
    y = table(120, y + 6, [("Run", 250), ("old Space", 330), ("skill", 300), ("to do", 420)], rows) + 40
    runnable = {lv: (t["card"] + t["base"]) * 100 // max(1, sum(t.values())) for lv, t in tally.items()}
    open_ = [f"{r[1]} ({lv})" for lv in ("Block", "Job", "Task") for r in by_level[lv]
             if r[3].startswith(("screen", "drawn"))]
    L.text(0, y, "runnable today: " + " · ".join(f"{lv} {p}%" for lv, p in runnable.items()) +
           (". No card yet: " + ", ".join(open_) + "." if open_ else ". Every button has its card."), 18)
    notes(0, y + 50, ["? a screen-only button copies a prompt that no card or skill answers: the Runs panel can't "
                      "say who runs it or what is signed"] + CHANGES["runs"])
    L.close_frame(fr, pad=40)

    # 2 · one version, in order
    y = bottom() + 200
    fr = L.open_frame("one version, in order")
    L.text(0, y, "One version, in order: each step, its skill, its check", 30)
    fx, fy = 0, y + 110
    for k, (step, skill, note) in enumerate(FLOW):
        L.base("rectangle", fx, fy, 260, 64, L.INK, 1.5)
        L.text(fx + 16, fy + 18, step, 20)
        L.text(fx, fy + 80, skill, 14, L.RED if skill.endswith("?") else L.INK, L.MONO)
        L.text(fx, fy + 104, note, 14, L.RED if note.endswith("?") else L.GRAY)
        if k < len(FLOW) - 1:
            L.path([(fx + 268, fy + 32), (fx + 332, fy + 32)], color=L.INK)
        fx += 340
    lx, ox = 7 * 340 + 130, 2 * 340 + 130            # comments → a new version
    L.path([(lx, fy - 4), (lx, fy - 50), (ox, fy - 50), (ox, fy - 4)], color=L.GRAY, dashed=True)
    L.text(ox + 40, fy - 80, "a revision is a new version: j02 copies j01's written files, answers the comments", 14,
           L.GRAY)
    L.text(0, fy + 150, "a person signs the Story's gates, each Section's release, the submission and the response; "
                        "every number, figure and citation comes from work and discovery Runs, never the paper", 16,
           L.GRAY)
    notes(0, fy + 190, CHANGES["flow"])
    L.close_frame(fr, pad=40)

    # 3 · the skills
    y = bottom() + 200
    fr = L.open_frame("the skills")
    L.text(0, y, "The skills behind the Runs", 30)
    L.text(0, y + 46, "skills/2_theme/paper/ · old = times its docs still write Story Page, B[abc]-, RD<NN>, S-<desk> "
                      "or -<MMDD>- · red = changes on the new ladder", 16, L.GRAY)
    uses = Counter()
    rows_by_skill = {}
    for lv, rows in by_level.items():
        for r in rows:
            sk = r[6].rstrip(" ?")
            uses[sk] += 1
            rows_by_skill.setdefault(sk, []).append(r[0])
    rows = []
    for d in sorted(p for p in PAPER.iterdir() if (p / "SKILL.md").is_file()):
        s = (d / "SKILL.md").read_text(encoding="utf-8")
        v = re.search(r'version: "?([\d.]+)', s)
        owns, ladder = SKILL_JOB.get(d.name, ("?", "?"))
        names = sorted(set(rows_by_skill.get(d.name, [])))
        rows.append([d.name, "v" + (v.group(1) if v else "?"), f"{len(callers(d.name))}", owns,
                     (" · ".join(names)[:58] + (" …" if len(" · ".join(names)) > 58 else "")) or "-",
                     str(stale(d)), ladder])
    y2 = table(0, y + 100, [("skill", 300), ("version", 90), ("callers", 80), ("owns", 440),
                            ("Runs that use it", 560), ("old", 60), ("on the new ladder", 560)], rows)
    rows = []
    for group, names in BORROWS:
        for n in names:
            p = find_skill(n)
            rows.append([n, group if n == names[0] else "", p.parent.relative_to(SKILLS).as_posix() + "/" if p
                         else "not found ?", str(uses.get(n, 0) or "-")])
    y2 = table(0, y2 + 60, [("skill", 300), ("borrowed for", 440), ("where", 400), ("Runs", 80)], rows)
    rows = [[f"{n}/", f"{k} files · {mb:.0f} MB", "its own git repo ?" if repo else "in Tools"]
            for n, k, mb, repo in not_skills()]
    y2 = table(0, y2 + 60, [("in 2_theme/paper, no skill", 300), ("size", 220), ("kind", 300)], rows)
    notes(0, y2 + 30, ["? venue/ is its own git repo inside the skills tree the installer scans: mount it outside "
                       "skills/, and register it?",
                       "? haipipe-paper-venue (a Venue Page) or b03's venues/<venue>/ (call.md, kit/): one home (Q02)?",
                       "? an older paper-edit family is installed at user level from outside this SPACE: retire it, "
                       "or bring it into 2_theme/paper?"] + CHANGES["skills"])
    L.close_frame(fr, pad=40)

    # 3b · skill folders, before → after
    y = bottom() + 200
    fr = L.open_frame("skill folders: before → after")
    L.text(0, y, "The skill folders, before → after: what changes, and why", 30)
    L.text(0, y + 46, "skills/2_theme/paper/ · before = the tree the plan started from (261007) · after = the plan · "
                      "state = done when its phase ran and the disk agrees · a file with no row is kept as it is · "
                      "red ? = your call", 16, L.GRAY)
    before = sorted(BASELINE, key=by_folder)
    missing = [p for p in FOLDERS if p not in before]
    after = sorted({FOLDERS[p][0].rstrip(" ?") if p in FOLDERS else p for p in before} - {""} |
                   {p for p, *_ in NEW_FILES}, key=by_folder)
    verb_of = {FOLDERS[p][0].rstrip(" ?"): FOLDERS[p][1] for p in FOLDERS if FOLDERS[p][0]}
    verb_of.update({p: "new" for p, *_ in NEW_FILES})
    yb = draw_tree(0, y + 110, "before · today", tree(before, lambda p: FOLDERS[p][1] if p in FOLDERS else ""),
                   lambda p: L.RED if p in FOLDERS and FOLDERS[p][1] in ("retire", "move ?") else
                   L.INK if p in FOLDERS else L.GRAY)
    ya = draw_tree(1100, y + 110, "after · proposed", tree(after, lambda p: verb_of.get(p, "")),
                   lambda p: L.RED if verb_of.get(p, "").endswith("?") else
                   L.INK if p in verb_of else L.GRAY)
    L.path([(900, y + 200), (1040, y + 200)], color=L.INK)
    def state(old, new, phase):
        """done when its phase ran and the disk agrees: the after file is there, a moved or retired one gone."""
        on = lambda q: q and (PAPER / q.rstrip(" ?")).exists()
        ok = phase in PHASES_DONE and (on(new) if new and new != "-" else not on(old)) and \
            (not old or old == new or old == "-" or not on(old) or FOLDERS.get(old, ("",))[0] == old)
        return "done" if ok else "to do" if phase not in PHASES_DONE else "check ?"
    rows = [[p, FOLDERS[p][0] or "-", FOLDERS[p][1], FOLDERS[p][2], FOLDERS[p][3], FOLDERS[p][4],
             state(p, FOLDERS[p][0], FOLDERS[p][4])]
            for p in sorted(FOLDERS, key=lambda p: (FOLDERS[p][4], p)) if p in before]
    rows += [["-", p, "new", what, why, ph, state("", p, ph)] for p, what, why, ph in NEW_FILES]
    rows.sort(key=lambda r: r[5])
    yt = table(0, max(yb, ya) + 80, [("before", 500), ("after", 500), ("change", 110), ("what", 460),
                                      ("why", 460), ("phase", 70), ("state", 90)], rows, size=14,
               mono=("before", "after"))
    keep = len([p for p in before if p not in FOLDERS])
    notes(0, yt + 30, [f"kept as they are: {keep} files (no change word beside them in either tree)"] +
          [f"? named here but not on disk: {p}" for p in missing] + CHANGES["folders"])
    L.close_frame(fr, pad=40)

    # 4 · skill x Run
    y = bottom() + 200
    fr = L.open_frame("skill x Run")
    L.text(0, y, "Which skill each Run loads", 30)
    L.text(0, y + 46, "x = its card names the skill · x ? = proposed, no card yet", 16, L.GRAY)
    names = ["haipipe-paper", "-story", "-ideation", "-venue", "-section", "-assemble", "-comments", "-workflow"]
    full = ["haipipe-paper"] + ["haipipe-paper" + n for n in names[1:]]
    cols = [("Run", 520)] + [(n, 130) for n in names] + [("Page", 110), ("other", 260)]
    rows = []
    for lv in ("Block", "Job", "Task"):
        for r in by_level[lv]:
            sk, mark = r[6].rstrip(" ?"), "x ?" if r[6].endswith("?") else "x"
            page = sk.startswith("haipipe-page") or sk == "haipipe-display"
            rows.append([f"{lv} · {r[0]}"] + [mark if sk == f else "" for f in full] +
                        [mark if page else "", "" if sk in full or page else (sk + (" ?" if mark != "x" else ""))])
    table(0, y + 90, cols, rows, mono=("Run",))
    notes(0, bottom() + 30, CHANGES["matrix"])
    L.close_frame(fr, pad=40)

    # 5 · Runs on disk
    y = bottom() + 200
    fr = L.open_frame("Runs on disk")
    L.text(0, y, f"The Runs in the {n_papers} Project paper folders today", 30)
    L.text(0, y + 46, "run type · shelf · count; names only, no Board or Section is named", 16, L.GRAY)
    by_type = Counter((run_type(s), shelf) for s, shelf in runs)
    rows = [[t, shelf, str(k) + (" ?" if t.startswith("rNN_") else "")]
            for (t, shelf), k in sorted(by_type.items(), key=lambda x: -x[1])]
    rows += [[t, "story", "0 ?"] for t in ("run-paper-idea", "run-paper-claim", "run-paper-task",
                                           "run-paper-narrative") if not any(k[0] == t for k in by_type)]
    yb = table(0, y + 100, [("run type", 300), ("shelf", 140), ("count", 90)], rows, mono=("run type",))
    yn = table(700, y + 100, [("family", 200), ("name", 470), ("note", 470)], [
        ["Page writing", "run-<kind>-<slug>", "structure · scratch · section · paragraph · revise …"],
        ["Page evidence", "run-<value|citation|display>-<slug>", "one per Evidence Item"],
        ["Page delivery", "run-delivery-<lane>", "one fixed Run per lane"],
        ["Paper judgment", "run-paper-<idea|claim|task|narrative>-<slug>", "a review with a verdict"],
        ["compile", "delivery/runs/rNN_compile-<slug>.sh", "a hard ticket in the paper ?"],
        ["supporting", "rNN_<slug> in a work or discovery Task", "never renamed for the paper"],
        ["old, still read", "run-<kind>-<MMDD>-<slug>", "renamed by page.py run-names"]], mono=("name",))
    notes(0, max(yb, yn) + 30, ["? hard rNN_ Runs sit on Story Pages, and compile is a hard ticket in delivery/runs/: "
                                "Q01 proposes soft Runs only. Move them to a work Task, or allow a paper its builds?",
                                "? the four judgment run types (run-paper-*) have cards and buttons but no Run on disk "
                                "yet"] + CHANGES["disk"])
    L.close_frame(fr, pad=40)

    # 6 · the skill update plan
    y = bottom() + 200
    fr = L.open_frame("skill update plan")
    L.text(0, y, "The skill update plan: every button above gets an owner", 30)
    L.text(0, y + 46, "phases in the order they unblock each other: the contract and the cards first, so each later "
                      "skill has a folder to write and a card to answer; the Task last, being mostly the Page's", 16,
           L.GRAY)
    yp = table(0, y + 100, [("phase", 140), ("skill", 300), ("what it learns", 820), ("run types it gains", 720),
                            ("done when", 340)], [list(p) for p in PLAN])
    notes(0, yp + 30, CHANGES["plan"] + CHANGES["done"])
    L.close_frame(fr, pad=40)
    off = canvas.off_palette(L.els)
    if off:
        print(f"{len(off)} element(s) off the studio palette, e.g. {off[0].get('strokeColor')}")
    canvas.write(out, list(L.els), "build_s21_paper_run_skill.py")


if __name__ == "__main__":
    main()
