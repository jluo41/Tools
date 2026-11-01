# j01 · The insight pages, level by level

goal: the insight theme's three pages on the focus page, each in its three sections: Board, Job and Task × Report, Work and Studio
close: all nine sNN are agreed and each names the code change for its owner (insight_theme.py, insight_views.py, workbench-insight skill)
answers: Q01

## Topic

The insight theme climbs three levels: a Board (one dataset and its data freezes, `insight/Insight-<dataset>/`), a Job
(one analysis plan × one data freeze, `j03_p2_<d>v2`) and a Task (one question at one DIKW level, `t10_K01_<slug>`),
whose hard Runs are one per cut (`r01_full`, `r02_<cut>`, `r04_cross`). Every page has three sections with three aims:
Report checks, Work does, Studio thinks. So the design is the same 3 × 3 grid as the paper theme's (b16 j01) and the
labeling theme's (b15 j01): one Task per level, and in each Task one sNN per section (JL 261101: "Please understand the
above two sessions and then work on the insights").

```text
                 Report · check    Work · do    Studio · think
t01 Board        s51               s52          s53
t02 Job          s54               s55          s56
t03 Task         s57               s58          s59
```

The numbers are labeling's (s51 to s59), so the same number names the same cell in both Blocks; b11's s32 and s33 were
already taken. Every view is drawn as the same full screen, lettered A, B, C, and settled one letter per round; Report
and Work of one page share letters. The Job page letters the DIKW levels (B Data to E Wisdom), as labeling's Task page
letters its types. All nine cells are drawn by `insight_ui_cells.py`, copied from b15's `labeling_ui_cells.py`.

The "before" every screen replaces is the focus page as served on 261101: at all three levels it is the base's vanilla
page (Report = MindMap · Status, Work = Progress with "no state recorded"), with no insight content; the insight content
still lives on the old five-Space page (s02). Names are placeholders: a real Board holds one person's health data, and
Tools is public.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_board_page · The insight Board page
2. t02_job_page · An insight Job page
3. t03_task_page · An insight Task page

## Round 2 notes

- Every Prompt box is the shared part `servers/workbench/ui_parts.py` `prompt_box` (Theme_Labeling, 261101): head
  "✍️ Prompt · <step> · <asks>" with Copy prompt, the grey prompt text, the person's fields, and the line "Run this
  in the Claude session <session>". The drawings draw the same four parts (b15's `labeling_ui_cells.py` `k_prompt`),
  so the Studio cells' "Ask the agent · Copy prompt" rows become that box.
- The round 1 reviews' fixes (each cell's `review/cell-s1-r01.md`): your signs first on Work, the same grid on Work,
  the answer in the large slot, the Task's cut × step grid, numbered heading bars with the bottom helpers.
