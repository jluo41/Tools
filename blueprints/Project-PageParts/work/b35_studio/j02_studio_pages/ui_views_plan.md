# Plan · the view lists of the nine UI cells (b35 j02, JL 261031)

JL 261031: "you need to propose different UI's view list and view's subsection and propose them and make detailed
interaction, and later I will give you the feedback and you will continue ... propose them as complete as possible ...
call multiple subagent and each agent focus on one single topic ... I will just check in the interaction section".

## What JL gets

Nine forms, one per cell, all listed under b35's right-rail **Interactions** (All). Each form proposes, for one level
(Block, Job, Task) and one section (Report, Work, Studio):

1. **Q1 · View list**: the view-button-list under the title, two to four complete options (A to D), each with a live
   HTML preview of the page with that bar, its first view open.
2. **Q2 to Q5 · one per view** of the proposed list (the ticked option of Q1): what that view holds, its subsections
   top to bottom, two to four options, each with a live preview.
3. **Q6 · Clicks** (optional): what a click on an item in this section does (pop-out, card, page, nothing), with a
   preview when it can be shown.

At most six questions per form (collect.py check). My pick is ticked in each, with its `Why X:` line.

## The nine topics, one agent each

```text
cell  level  section  form Run (under j02_studio_pages/)                       the real page today (5623)
s11   Block  Report   t02_block_page/runs/r01_collect_block_report_views         b35_studio        MindMap · Status
s12   Block  Work     t02_block_page/runs/r02_collect_block_work_views           b35_studio        Progress
s13   Block  Studio   t02_block_page/runs/r03_collect_block_studio_views         b35_studio        one button per Tag
s14   Job    Report   t03_job_page/runs/r01_collect_job_report_views             j02_studio_pages  MindMap · Status
s15   Job    Work     t03_job_page/runs/r02_collect_job_work_views               j02_studio_pages  Progress
s16   Job    Studio   t03_job_page/runs/r03_collect_job_studio_views             j02_studio_pages  one button per Tag
s17   Task   Report   t04_task_page/runs/r01_collect_task_report_views           t02_block_page    MindMap · Status
s18   Task   Work     t04_task_page/runs/r02_collect_task_work_views             t02_block_page    Progress
s19   Task   Studio   t04_task_page/runs/r03_collect_task_studio_views           t02_block_page    one button per Tag
```

Live page: `http://100.121.165.84:5623/_board/workbench?layout=focus&path=blueprints/Project-PageParts/work/b35_studio[/j02_studio_pages[/t02_block_page]]&section=<report|work|studio>[&group=<view>]`

## Read first (every agent)

- The form format and its limits: `plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-interaction/SKILL.md`.
- How a page reads (five rules, one verb per section, the view-button-list): `skills/1_base/workbench/haipipe-ui/SKILL.md`.
- The cell's own face (its Rules and Open): `<task>/s1N-<level>-ui-<section>/s1N-<level>-ui-<section>.md`.
- What the code does today: `plugins/haipipe-toolkit/servers/workbench/focus_page.py` (`render`, the `overview`, `work`,
  `studio_views` and `rail` dictionaries).
- The sibling cells already decided by JL: b17 `blueprints/Project-Ladder/work/b17_theme_work/j03_work_workbench_pages/`
  (s51 to s59, s51-D01 to D06: Report views by delivery type, no Questions, one word per delivery) and b16
  `blueprints/Project-Ladder/work/b16_theme_paper/j01_paper_workbench_pages/` (the paper's 3 × 3).

## JL's standing rules for every option

- The view-button-list sits under the title, above the Purpose; one button when a section has one view.
- No counts anywhere ("Don't add N topics, N jobs"); status marks are only ⏳ ✅ ⬜ 🙋.
- One item per row, never a grid. As concise as possible. Show the real thing, never a redesign of it.
- Report checks (results, progress), Work does (children, Runs), Studio thinks (sNN cards, drawings, mind maps).
- The Studio is never a report. Each sNN has one idea and one delivery; a Block at most 9 sNN, a Job 5, a Task 3.
- Reader words in English, no em-dashes, real names (real sNN, Jobs, Tasks, Runs from b35).

## How each preview is made

Start from the real page's HTML (`curl` the live URL), keep its look and its inline CSS, and change only the bar and
the content area to show the option. Save it in the Run folder as `q<N>-<key>.html` (for example `q1-a.html`), and
link it indented under its option: `  [preview](q1-a.html)`. No external scripts; no data the page does not have.

## Rules for the agents

- Write only inside your own Run folder. Never edit focus_page.py, a face, another Run, or a server; never restart one.
- `collect.py check <run>` must print ok, then `collect.py build <run>`; open the form on 5623 and check each preview.
- Return the questions, their options and the picks in under 300 words.
