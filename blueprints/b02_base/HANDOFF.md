You are the session for the blueprint Block Tools/blueprints/b02_base (read its board.md first). JL opened it on 2026-10-07 for the base layer of the toolkit's skills, beside b01_utils (0_utils) and the theme Blocks b11 to b17 (2_theme). Work in place in the SPACE; never commit, push, reset, clean or stash: the tree has many uncommitted changes from JL and other sessions. Chat replies follow /response-format. Record each Question's outcome in its report Page under reports/ (SPACE-relative paths), keep answer-status open until JL settles it.

The goal
--------
Describe what the base layer is, `Tools/plugins/haipipe-toolkit/skills/1_base/`, and make it clean: what each base family gives the themes, one common shape for a base family, and nothing in base that belongs to one domain or one theme. Four Questions are registered in board.md (Q01 base map, Q02 base shape, Q03 not base, Q04 the page family's workbench skills); start with Q01.

Where things are (2026-10-07)
-----------------------------
- The base layer: eight families, each with a `haipipe-<family>` door. SKILL.md counts: project 2 · task 49 · page 15 · question 4 · writing 4 · display 12 · ideation 13 · search 9.
- The layers and how they were set up: Tools/blueprints/b04_skill_folder (reports q01_skill_layers, q02_path_fix, q03_merge_subjective_label, q04_theme_shape; studio s01 to s04, s02 is the layer inventory and s04 the theme shape table).
- Already decided today: every theme has a `haipipe-<theme>` door and a top-level `workbench-<theme>`; labeling's skills are `haipipe-labeling-<thing>` grouped by Space; the work theme has `haipipe-work` and `workbench-work` in 2_theme/work, while the rest of the work skills still sit in 1_base/task (b17 Q04 decides what work takes).
- Open from today, now yours: where agents live (three ways today: real files in plugins/haipipe-toolkit/agents/, symlinks from there into a skill's agents/, agents/ folders inside skills); haipipe-workflow (proposed: beside haipipe-run in 1_base/project); the HAI-Pipe stage pipelines in 1_base/task (data, nn, end, individual; b17 excludes them from the work theme); the page family's three workbench skills.
- How code finds a skill: by folder name (servers: host_paths.skill_dir; skill code: the folder named `skills` above the file; the Page engine: src/skill_paths.py). A move by b04 therefore breaks nothing that looks a skill up by name.
- Drawing helpers: Tools/blueprints/b04_skill_folder/studio/_build/sketch.py (sticky notes, mono blocks, the Questions frame, a colour key, facts read from disk) writing through b03's canvas.write (Tools/blueprints/b03_project_workbench/studio/_build/), so a person's marks survive a rebuild. Colours, one meaning each: yellow question · green done · blue idea or recommendation (blue text = a reply to a mark) · pink JL's choice · gray other sessions · red text = open concern.

How to work
-----------
1. Design first: answer Q01 with a drawing read from disk (studio/s01-base-map: each base family x the themes and base families that call it) and its report; show JL; mark open points red.
2. A decision that moves or renames a skill is carried out by b04 (design_b04_skill_folder): send it the mapping; do not move skill folders yourself.
3. Shared code and other Blocks have owners; edit only this Block, and tell the owner (SendMessage):
   - the ladder and the base workbench's frame: design-b03-project
   - skill folder moves, renames and path fixes: design_b04_skill_folder
   - the themes: design_b11_theme_insight, design_b12_theme_design, design_b13_theme_cowork, design_b14_theme_discovery, design_b15_theme_labeling, design_b16_theme_paper, design_b17_theme_work
   - Q03's task/ split overlaps b17's Q04: agree it with design_b17_theme_work.
4. Rules: a generated file is never changed by hand (AGENTS.md rule 0); no absolute /Users/... paths in tracked files; a design drawing of a concept carries no DrFirst content; check for PHI before reading any data file.
5. Checks: when a decision changes a skill, b04 reruns its post-move checks (link checker, guide paths, old-name grep, the test suites, reinstall); say the counts and any failure that was already there.

Report to JL in chat as each Question finishes: what changed (files, one line each), the checks and their counts, what is left.
