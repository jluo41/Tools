# A08 · A page design is looked at on an example Block's live page

> "could you just work on the real examples, and showing the UI, do you get what I mean?" (JL 261126, s07's Topic rows)
> "could we make it to be server generated? and working with examples/Project-Ladder/work/b01_example_work?" (JL 261126)
> "so it is the real things to be rendered, and Effect is the quick hmtl" (JL 261126)
> "How do we call this type of sNN? ... I think we also need to make it as a type, right?" (JL 261126)

## 1. Need
JL judges a page design on the page itself: the same code, real files, every Job and Task state. A
preview that is a picture of the page tells him about the picture.

## 2. Now
A UI preview topic (`**Delivery type:** ui`) lists its views on its own page `<sNN>.html`, one
`<button data-src>` each; Studio shows them as left tabs. A live view is
`/_board/workbench?path=<example Block>&layout=focus…`, under Page; a quick view is an html in
`delivery/ui/`, under Effect, faded by `class="old"` once its design is in the code. The work theme's
example Block is `examples/Project-Ladder/work/b01_example_work`, made by `new_board.py`,
`new_job.py` and `soft_run.py`: Jobs in three bands, a Job with no Task, Tasks done, running, waiting on
you and planned, a check Run with an open round, traces.

## 3. Gap
s11-work-job-preview's Topic rows was `delivery/ui/job-view-topics.html`, drawn by hand; its data was
`job-view-topics-data.js`, printed by `job-view-topics-data.py` when someone ran it. Each change to
`focus_jobs.py` left the preview behind, and JL compared a stale drawing with the real page.

## 4. Methods
1. Rerun the snapshot script before each look: rejected, it still drifts between runs.
2. Render the real page over a made-up example Block, linked from the topic's page: chosen.
3. Point previews at a real working Block: rejected, its states change and it holds real work.

## 5. Update
- `servers/workbench/studio/tabs/studio_tabs.py` `page_items`: a `/_board/workbench?` button is a left tab
- `s11-work-job-preview.html`: Topic rows and Job Main are live views over b01_example_work
- `hai-studio/ref/ui-preview-topic.md`; `hai-block/ref/board-contract.md` § Example Blocks
- `scripts/ui_preview_check.py`
Cases: ✅ s07 · ⬜ s99-guide-view (quick view only until the Guide is in the code) · ⬜ Paper-Example as a live view.

## 5b. Later the same day
- Job Main opened j11's own Job page, a different page from Topic rows. Both now open the example Block's
  Jobs with j11 picked (`group=j11`) and differ only by `mark=`: Topic rows `jobs-rows,job-ttopics,job-subs`,
  Job Main `jsub=main`. `focus-assets/focus.js` reads `mark=` (a class or a data attribute) and outlines the
  visible parts in red, again after a click.
- Effect with one view showed it full width; Page and Effect now keep their left tabs for one view
  (`studio_tabs.py`), so another effect is one more tab.
- Effects became Task states, the Tasks band alone (`only=tasks`); the three earlier designs and the old Job
  Main preview were deleted, their decisions marked "(removed 261126)".

## 6. Never again
`ui_preview_check.py` fails a UI preview topic with no live view, a view button whose file is not
there, and two live views that open the same address.
