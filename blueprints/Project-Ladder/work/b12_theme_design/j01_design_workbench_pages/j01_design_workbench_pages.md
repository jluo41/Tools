# j01 · The design pages, level by level

goal: the design theme's three pages on the focus page, each in its three sections: Block, Job and Task × Report, Work and Studio
close: all nine sNN are agreed and each names the code change for its owner (design_views.py, design_reader.py, workbench-design skill)
answers: Q02

## Topic

The design theme climbs three levels: a Block (one application, one channel, `Design-PreVisitChecklist`), a Job (one
goal × one method version × one inputs version → N designs, `j01_prepare-before-visit_goal-only`) and a Task (one step
of the method in that Job, of three types: 💡 t00 reason ideas · ✏️ one Task per design · 🏆 t99 review whole). Every
page has three sections with three aims: Report checks, Work does, Studio thinks. So the design is a 3 × 3 grid, as
the paper theme's (b16 j01) and the labeling theme's (b15 j01): one Task per level, and in each Task one sNN per
section (JL 261101: "How about you to udpate the theme_design?").

```text
                 Report · check    Work · do    Studio · think
t01 Block        s51               s52          s53
t02 Job          s54               s55          s56
t03 Task         s57               s58          s59
```

Every view is drawn as the same full screen, lettered A, B, C, and settled one letter per round; Report and Work of one
page share letters. The Task page letters the three Task types (A 💡 reason ideas, B ✏️ design, C 🏆 review whole) and
numbers each type's steps (A1 Inputs, B2 Verify …), as labeling's does. Each Task view is drawn from its run card and
method step (In → who works → Out, your part, Results, next), checked by `task_views.py`'s coverage table. The one loop
is a design's drafts (generate → verify v1 → revise → verify v2 …); no Task asks the person: a person signs only at the
Block (goals, shared rules) and the Job (Review and approve, the close). There is no Runs view: each step shows its own
Runs (JL 261101, from the labeling session).

All nine cells are drawn by `design_ui_cells.py`, copied from b15's `labeling_ui_cells.py`. The "before" every screen
replaces is s11 · s12 · s13 (the six-Space frame) and s33 (its problems). Names are the Block's folder names, already in
b12's `board.md`; no design text is drawn: the Block's designs are tailored to one demonstration participant and stay
local, and Tools is public.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_block_page · The design Block page
2. t02_job_page · A design Job page
3. t03_task_page · A design Task page, by type
