# j01 · The labeling pages, level by level

goal: the labeling theme's three pages on the focus page, each in its three sections: Block, Job and Task × Report, Work and Studio
close: all nine sNN are agreed and each names the code change for its owner (labeling_theme.py, task_labeling.py, workbench-labeling skill)
answers: Q01

## Topic

The labeling theme climbs three levels: a Block (one dataset, `b01_dices350`), a Job (one dataset × one label,
`j01_dices350_response_safety`, its `schema.yaml`) and a Task (one step of that Job, of six types: 📦 items ·
📏 ground truth · 🧭 meaning · 🛠 expression · 🔍 scanning · 📊 score, s13). Every page has three sections with three aims:
Report checks, Work does, Studio thinks. So the design is a 3 × 3 grid, as the paper theme's
(b16 j01): one Task per level, and in each Task one sNN per section (JL 261031: "please go ahead and update them").

```text
                 Report · check    Work · do    Studio · think
t01 Block        s51               s52          s53
t02 Job          s54               s55          s56
t03 Task         s57               s58          s59
```

Every view is drawn as the same full screen, lettered A, B, C, and settled one letter per round; Report and Work
of one page share letters. The Task page is the one that differs from paper: a labeling Task has six types, so its
Report and Work letter the types (A 📦 items to F 📊 score) and number each type's steps (A1 Data, A2 Items …).
Each view is drawn from its step slide (In → who works → Out, your part, Results), checked by task_views.py's
coverage table; 🧭 meaning and 🛠 expression are the two loops, and only meaning asks the person.
All nine cells are drawn by `labeling_ui_cells.py`, copied from b16's `paper_ui_cells.py`. The "before" every
screen replaces is s02 (the Labeling workbench as built today). Names are placeholders: Tools is public.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_block_page · The labeling Block page
2. t02_job_page · A labeling Job page
3. t03_task_page · A labeling Task page, by type

