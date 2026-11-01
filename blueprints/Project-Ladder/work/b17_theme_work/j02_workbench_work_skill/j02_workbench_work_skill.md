# j02 · Rewrite workbench-work for the work pages

goal: workbench-work's SKILL.md and ref/workbench-table.md teach the focus page's three work pages, a Block, a Job and a Task, each with Report (check), Work (do) and Studio (think), as j03's nine cells design them
close: both files are written from JL's answers to the nine cell forms and follow b17-s02's outline; the old Scope · Task · Check · Delivery text, the Questions and the question map are gone; the ref passes `render_workbench_table.py --check`; a fresh agent given only the skill reads b17's Block page, j03's Job page and t01_block_page's Task page right
renamed-from: j02_work_skill_homes

## Topic

From b17-s02:theme_work @ work_skills: s02's delivery is workbench-work, rewritten (s02-D02; JL 261031, pointing at
`skills/2_theme/work`: "you should update this, right?"). This Job writes it in two Tasks: t01 the SKILL.md, section
by section as s02's outline lists them (its face, Design), and t02 the ref's table, one row per page, section, view and
Run type. Each page's section follows the answers to its three cell forms in j03 (t01_block_page r02 to r04,
t02_job_page r01 to r03, t03_task_page r01 to r03). None is answered yet, so both Runs wait, planned. A Run takes one
pass per page, Block, then Job, then Task, as that page's three forms come back (s02 Open 2); the first pass also
takes out what is already decided gone (the Questions, the question map, the Scope · Task · Check · Delivery screens).

The screens are not made here: j03's cells design them and design_b02_workbench builds them in
`servers/workbench/focus_page.py`. The skill says what each page shows and what it reads from disk.

Reshaped 261031 from j02_work_skill_homes ("Make s02's delivery"), whose two Tasks wrote haipipe-work's skill-homes
table and handed b04 a move list. That question is not the focus any more (JL 261031: "I have no idea, this should not
be the things we want to focus"), so t01_skill_homes_table and t02_move_list_b04 went to `_old/`, unrun; the topic as
it was is in `../s02-work-skills/result/skill-homes-261031/`.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_skill_md · Rewrite workbench-work's SKILL.md
2. t02_workbench_table · Rewrite workbench-work's ref/workbench-table.md

