# j01 · The cowork pages, level by level

goal: the cowork theme's three pages on the focus page, each in its three sections: Block, Job and Task × Report, Work and Studio
close: all nine sNN are agreed and each names the code change for its owner (cowork_theme.py, workbench-cowork skill)
emoji: 🤝
answers: Q01

## Topic

The cowork theme climbs three levels: a Block (one topic coordinated with people, `cowork/bNN_<topic>/`), a Job (one
line of work, `jNN_<job>/`, with its Timeline, checklist, emails and meetings) and a Task (one document written in
rounds, `tNN_<task>/`, whose Runs collect a person's answers and write each round). Every page has three sections with
three aims: Report checks, Work does, Studio thinks. So the design is the same 3 × 3 grid as the paper (b16 j01), work
(b17 j03), labeling (b15 j01) and insight (b11 j01) themes': one Task per level, and in each Task one sNN per section
(asked 261108: give the cowork theme Block its UI drawings, drawn from the live cowork pages).

```text
                 Report · check    Work · do    Studio · think
t01 Block        s51               s52          s53
t02 Job          s54               s55          s56
t03 Task         s57               s58          s59
```

The numbers are the other themes' (s51 to s59), so the same number names the same cell in every theme Block; b13's
s01, s02 and s32 were already taken. Every view is drawn as the same full screen, lettered A, B, C, and settled one
letter per round; Report and Work of one page share letters. All nine cells are drawn by `cowork_ui_cells.py`, copied
from b11's `insight_ui_cells.py`.

The screens are the focus page as served on 261108, on the theme's own public example
(`cowork/b01_example_data_request`, every role, date and number made up): the Block and a Job show MindMap · Status ·
Findings, a Task MindMap · Status. Findings holds what only cowork has: 👥 People, ✉️ Messages and ⏳ Next move. Work
repeats each Report view under 📊 Results, after ⚙️ Process where the page has a step (the Block's Status and
Findings); a Job and a Task have none today, and the one step each plainly lacks is drawn red, a proposal (the Job's
next move, the Task's v3). Studio is one view, Topics, at every level.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_block_page · The cowork Block page
2. t02_job_page · A cowork Job page
3. t03_task_page · A cowork Task page
