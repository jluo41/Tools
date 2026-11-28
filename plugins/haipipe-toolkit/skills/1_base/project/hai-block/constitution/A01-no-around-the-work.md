# A01 · No 🧭 Around the Work band under the Report

> "I think we will not need this anymore, things will be in the [side pane]" (JL 261124, b16_theme_paper Block)

## 1. Need
JL reads a Report view and wants it to end with its own content. The shared sections (Studio, Interactions,
Decisions, Things to Know, Checklist, Timeline, Skills, Files) belong in the ••• side pane only.

## 2. Now
`focus_render.around_work` appended `<h2 id="work-shared">🧭 Around the Work</h2>` plus `context_frame.shared(...)`
under every shared-frame Report view. Labeling drew the same band in `labeling_focus.py:118` and
`labeling_focus_frame.py:226`. On b16 Overview it showed 🧰 Skills and 📁 Files, both already in the side pane.

## 3. Gap
The band was the only on-page place a view's waiting questions showed (its 🙋 Interactions); dropping it
whole would hide what waits on the reader (hai-ui A03).

## 4. Methods
1. Delete the band only: rejected, it hides waiting questions.
2. Use `IX.view_section(view_items)`: rejected, a different item scope (paper version and design Block forms leaked).
3. Chosen: `work_frame.view_asks` keeps only the Interactions body the band used, the same scope, else nothing.

## 5. Update
- `servers/workbench/page/block_index_page/focus_render.py` (around_work): band removed, `view_asks` added
- `servers/workbench/page/job_task_views/work_frame.py`: new `view_asks`
- `servers/workbench-labeling/labeling_focus.py`, `labeling_focus_frame.py`: band replaced by `view_asks`
- tests in workbench, workbench-paper, workbench-design, workbench-labeling: expect no band

Suites: workbench 223, paper 108, design 58, labeling 85 passed. Run line exit 0. Live 5623 b16 Overview,
Plan + Results, Findings: no band.

## 6. Never again
The Run line fails if any server writer emits the band heading again; the four suites assert `NotIn` on it.
