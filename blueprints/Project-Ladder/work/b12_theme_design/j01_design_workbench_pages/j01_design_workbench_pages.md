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

## Built (261101)

The six cells' Report and Work views run live on the focus page: `servers/workbench-design/design_focus.py`, asked by
`focus_page.py`'s hook `design_views` (JL 261101: "update the UI as well to make things to work"). Checked on this
SPACE's SMS design Board (`examples-5-design/Project-Application-SMSDesign/design/Design-SMSR2-Stage25-CarryOver-261008`),
where the Block's Summary opens on the one release waiting for a sign. Each letter is still at stage 1 of the design
loop: next, a live review per letter (`review/<L>-s2-rNN.md`, to 8 or more), then its agreed screen in `delivery/ui/`.
The Studio cells (s53, s56, s59) stay the base's Studio.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_block_page · The design Block page
2. t02_job_page · A design Job page
3. t03_task_page · A design Task page, by type

## Current Block frame · 2026-11-08

The Design Board now combines content and actions in Report, under Review Content followed by the shared Around the Work sections. Summary, Goals, Jobs, Rounds, Methods and MindMap remain the business views. The previous Report/Work split above is historical for the Block; Job and Task pages retain their specialist workflow. The current Block specification is `blueprints/Project-Ladder/work/b12_theme_design/ui/structure.md`, with the section matrix in `ui/block-views.md` and routed examples in `ui/view-guide.json`. Historical drawings have not been redrawn. Human approval of release is unchanged.
