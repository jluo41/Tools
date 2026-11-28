# A12 · Every section in the section menu shows its emoji, from one table

> "for there, why no emojis? who will check this? Do you think?" (2026-11-27, on b18's section menu)
> "even it is the normal block folder, it should have the emojis, what are the check files for it?" (2026-11-27)
> "the layout of the studio, is not the same as [b17] … so we should have the band + folds. who will take care of this? I think the servers/workbench-work." (2026-11-27)

## 1. Need
The section menu reads the same on every Block: each section with its emoji, so a reader finds Studio or Interactions by its mark.

## 2. Now
Before: `focus_render.rail_sections` built a plain Block's menu from bare words (Report, Work, Studio, Interactions, Delivery), `work_frame.SHARED` built a theme Block's from words with emojis, and only Jobs carried one on both. b18 sits in `knowledge/`; `frame_base.theme_of` asks the folder name, found none, and read it as a plain Block: no emojis, and the Studio as one card at a time instead of bands and folds (A11).
Now: `page/parts_and_map/section_icons.py` holds `SECTION_ICONS` and `section_label(key, name)`; `work_frame.SHARED`, the Jobs item and `focus_shell.side_launcher` call it. `workbench-work/work_theme.claims` also takes a Block whose face says `theme: work` or `workbench: work`, so b18 opens as a work page.

## 3. Gap
Two lists each chose a section's label, and no check compared them. A theme was found by folder name alone, so a new kind of Block folder fell to the plain page without a sign.

## 4. Methods
1. Add emojis to the plain list's words: rejected, the two lists would drift again.
2. One table both lists read, plus a theme claiming Blocks by their face: chosen.
3. Map `knowledge/` to work in the shared folder table: rejected, the next new folder repeats it; the theme that owns the Block claims it.

## 5. Update
- `servers/workbench/page/parts_and_map/section_icons.py` (new): the table and `section_label`
- `servers/workbench/page/job_task_views/work_frame.py`: `SHARED` labels from the table
- `servers/workbench/page/block_index_page/focus_render.py`: the Jobs item from the table
- `servers/workbench/page/block_index_page/focus_shell.py`: every menu item through `section_label`
- `servers/workbench-work/work_theme.py`: `claims` takes `theme: work` or `workbench: work`
- `servers/workbench-work/tests/test_knowledge_claim.py` (new): b18 is work; bands, folds and emojis
The page title (h1) keeps its section word as before; screen-reader labels stay plain words.

## 6. Never again
`section_icons_check.py` fails when a section a menu can hold has no emoji in the table, and, with `--url`, when any example Block's live menu item lacks its emoji. `test_knowledge_claim.py` fails when b18 stops reading as work or its Studio loses its bands. `/hai-stack sweep` reruns them.
