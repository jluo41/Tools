# A04 · A page's views are bands on one page, not buttons

> "I wnat them into one view, and each previous view will be the section name." (JL 261124)

## 1. Need
One scroll shows the whole Block: Overview, Plan + Results, Findings, Delivery each as a named band.

## 2. Now
`focus_render.section_body` built only the view named by `group` and drew a `section-views` bar of buttons.

## 3. Gap
Each view lived behind a click; the ★ eval and ⓘ addresses keyed on the open button's name.

## 4. Methods
1. CSS tabs showing all panels: rejected, still one view's markup per request.
2. Chosen: `view_bands.merge` builds every view in order, drops each view's own "📋 Review Content" heading,
   wraps it in `<section class="work-section-group view-band" id="band-<key>">` with its name; empty views skipped.

## 5. Update
- `page/block_index_page/view_bands.py`: new; `page/block_index_page/focus_render.py`: merged branch; `page/block_index_page/focus_context.py`: `merged`
- `page/element_marks/section_eval.py`: ★ keyed by band (`band_at`); `page/element_marks/element_info.py`: address by band
- tests: band helpers in `focus_page_fixtures.py`; 9 test files moved from the bar to bands
Suites: workbench 225, paper 112, design 58, labeling 85, work 62, insight 69. Live: every Ladder Block, a Job and
a Task draw bands in 0.1 to 0.6 s.

## 6. Never again
`test_work_frame.py` and `test_focus_findings.py` assert bands and no view bar; the Run line reruns them.
Open: paper, design, insight, labeling and the draft Task still use buttons.


## Update 261124: core bands, other buttons

JL: "I just asked for the overview and plan and Findings to be in one view ... do you want to make them back?" on b16,
where Block UI, Job UI, Task UI, Design and Docs had also become bands (nine on one page). Now `view_bands.CORE`
(overview, mindmap, standing, findings, delivery) are the bands of one Main view; the rest are buttons after Main
(`view_bands.bar`). Verified on 5623 b16: bar = Main · Design · Block UI · Job UI · Task UI · Docs; Main holds the
overview, standing, findings, delivery bands; `group=ui-block` opens Block UI with Main beside it.
