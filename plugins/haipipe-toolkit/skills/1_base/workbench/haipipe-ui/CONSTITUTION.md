# haipipe-ui · Constitution

JL's feedback on what workbench pages show, kept verbatim. It wins over SKILL.md and over any page code; where they
disagree, follow this file. Written and checked through `/hai-stack`. Page code lives in `servers/`, but its rules
live here: every session that changes a page reads this file first (root AGENTS.md § Page words).


## A01 · State shows by marks and layout, never by words or tallies

> "we don't want this, drop them" (JL 261113, on "Status:" sentences and "N of M" pills)
> "just like the layout and UI tell it" (JL 261113)

**Rule:** A page never says an item's state in words ("Status: running", "not signed yet") or shows a tally ("6 to fix", "3 of 7 written"); an emoji mark, a group, a fold or a button shows it.
**Why:** Pages carried "Status:" lines, "N of M" progress pills and check tallies that JL had to read and re-read.
**Class:** a state or count written as text in page code or in what page code renders.
**Cases:** ✅ shared section bars (`ui_parts.word_span`) · ⬜ Project faces rendered as text (a Project face "Status : Planning phase") · ⬜ Paper delivery line ("status: ready") · ⬜ every theme, every running SPACE (scanner)
**Check:** no visible "Status:"/"State:" sentence or "N of M <thing>" tally on any page a running server serves.
**Run:** `python3 plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/scripts/page_words.py --running --max 30`
**Status:** open
**Solved by:** `scripts/page_words.py`: reads every running workbench's visible text
**Report:** constitution/A01-state-by-marks.md


## A02 · No "JL 26xxxx" tags on a page

> "do not add the things like this in the UI, totally avoid this" (JL 261113, on a "JL 261113" tag in the Revise card)

**Rule:** No label, tooltip, button, banner or note a page shows carries a who-asked-when tag ("JL 261113", "(JL 261020: …)"); those live in code comments, commits and docs.
**Why:** Design tags written into code strings leaked onto pages.
**Class:** provenance text inside a string the page renders.
**Cases:** ⬜ Studio topic subtitles from faces ("(JL 261030)", Physician 5599, 5699) · ⬜ commit messages shown as Timeline data (allowed: content as written) · ⬜ every running SPACE (scanner)
**Check:** no visible `JL 2xxxxx` outside content a person wrote.
**Run:** `python3 plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/scripts/page_words.py --running --max 30`
**Status:** open
**Solved by:** `scripts/page_words.py`: flags every visible tag for triage
**Report:** constitution/A02-no-provenance-tags.md


## A03 · What waits on you pops out; an empty section is not drawn

> "if there are things for me to make decision, could they just pop out?" (JL 261114, pointing at Draft Lab)

**Rule:** What waits on the reader shows as a mark beside the item and in the 🙋 tray; a section bar carries only 🙋 N, ✓ or nothing; a section with nothing in it is not drawn, and no "nothing yet" text stands in for it.
**Why:** Pages drew empty Interaction and Delivery sections with "Nothing handed over yet" and "nothing yet" words.
**Class:** an empty-state sentence where nothing should be drawn.
**Cases:** ✅ focus_render, focus_delivery, work_frame, focus_studio (Tools 261118) · ⬜ servers not restarted since (5607, 5623, 5640, 5697, 5698, 5699) · ⬜ "Nothing asked yet" on one page
**Check:** no visible "nothing … yet" or "No subfolders." on any running page.
**Run:** `python3 plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/scripts/page_words.py --running --max 30`
**Status:** open
**Solved by:** `servers/workbench/page/block_index_page/focus_render.py` and three more: empty draws nothing
**Report:** constitution/A03-pop-out-no-empty.md


## A04 · Every link to a page lands on the focus page, never the old tabbed frame

> "the […] old style" (JL 261118, opening http://<host>:<port>/w/b12_<block>; relayed by a Project session)

**Rule:** `/w/<block>`, `/b/<block>` and any bare `/_board/workbench?path=…` address open the focus page (`layout=focus`); the old tabbed frame opens only on an explicit `layout=frame` or its own tab, sub, view or format keys.
**Why:** `home_boards.frame_url` built the short route without `layout=focus`, and `frame_view` drew the old frame for every address that did not say focus.
**Class:** an address that reaches the retired frame by default.
**Cases:** ✅ `/w/<block>` and `/b/<block>` (`frame_url`) · ✅ Block links on Home (`home_boards.py:302`) · ✅ any bare `?path=` link anywhere (`frame_view` default) · ✅ one SPACE's server checked live · ⬜ other servers until restarted
**Check:** the short route's URL carries `layout=focus`; a bare address renders the focus page; `layout=frame` still renders the old frame.
**Run:** `cd plugins/haipipe-toolkit/servers && uv run -q --python 3.13 --with pytest --with pyyaml python -m pytest -q _host/tests/test_workbench_short.py workbench/page/job_task_views/tests/test_focus_runs.py -k "route"`
**Status:** solved 261118
**Solved by:** `servers/workbench/home/home_boards.py`: `frame_url` adds layout=focus; `servers/workbench/page/block_index_page/frame_view.py`: bare address is focus
**Report:** constitution/A04-links-land-on-focus.md


# Folder icons

What each row of a file tree shows: on its left what it is, on its right what is happening to it. One table
holds every icon and mark: `servers/workbench/side_pane/files_tree/file_icons.py`.


## A05 · A file's icon comes from one table; a type with its own mark shows that mark

> "could you also give the good icon for each type of files here? what is your thoughts?" (JL 261124, Files pane)
> "this should be python icon, not this one" (JL 261124, on 🐍 beside a .py file)

**Rule:** Every file tree takes a file's icon from `file_icons.file_icon`; a type with a real mark (Python) shows that mark drawn inline, never a look-alike emoji.
**Why:** Trees drew one 📄 for every file, and the first type table gave .py a snake emoji, which is not Python's mark.
**Class:** a file icon chosen outside the one table, or an emoji standing in for a real mark.
**Cases:** ✅ Files pane (`work_files.file_node`) · ✅ Studio › Folder (`frame_folders`) · ✅ trace trees (`trace_view`) · ✅ every other server module (scanned)
**Check:** no server module but `file_icons.py` maps a suffix to an icon; .py maps to the inline Python mark.
**Run:** `uv run --quiet --python 3.13 --with pyyaml python plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/scripts/folder_icons_check.py` (add `--url <a running workbench>` to check the pane too)
**Status:** solved 261125
**Solved by:** `servers/workbench/side_pane/files_tree/file_icons.py`: one table, `FILE_MARKS` for real marks
**Report:** constitution/A05-one-icon-table.md


## A06 · The Files pane is real folders, in numbered parts, each with its path from the SPACE

> "these two are more like the topic, right? they are not the real folders, is that correct?" (JL 261124, Files pane groups)
> "for each section, could you also give the full path from this SPACE? do you get hwta I mean here>" (JL 261124)
> "we still wnat to keep the relative structure here, do you get it?" (JL 261124)

**Rule:** The Files pane shows only real folders, in numbered parts (1 · Block, 2 · UI, 3 · Skills), each part opening with its path from the SPACE root and keeping the folders' real nesting below it.
**Why:** Files showed made-up groups ("Tools · UI", "Workspace", 🧵 session marks) that looked like folders but were not on disk, and gave no path.
**Class:** a tree row that is a label rather than a folder on disk, or a part with no path.
**Cases:** ✅ Files pane on every theme (`work_files.render`, one Files for all) · ✅ a Job or Task page (opens to itself) · ✅ an empty part (not drawn) · ✅ Studio › Folder (no 🧵)
**Check:** the Files panel has "1 · Block" and a files-where path, and none of the old group labels.
**Run:** `uv run --quiet --python 3.13 --with pyyaml python plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/scripts/folder_icons_check.py` (add `--url <a running workbench>` to check the pane too)
**Status:** solved 261125
**Solved by:** `servers/workbench/side_pane/files_tree/work_files.py`: `files_part`, `flat_tree`, `own_skills`
**Report:** constitution/A06-real-folders-in-parts.md


## A07 · A trace writes its plan first, and the Files pane shows its files with their state

> "for a trace, to be recorded, what is the requirements, like we might have the plan, be clear about what to change, right? and think about what files to changed, what aims to achived, right?" (JL 261125, chat)
> "so we can have the files to be flag like before, during, and after, what is your thoughts?" (JL 261125, Files pane)
> "I want to show what files are related to this Trace, you know, could you show me the expected outcome" (JL 261125)
> "I just want one UI of this, and everytime, I work on a trace, the related files will be flagged, or ammintatied" (JL 261125, Files pane)
> "we don't wnat this as well, this will be hover over to change, do you get it" (JL 261125, grey folder titles)
> "for the information, I want to make it like, you right click it, show the informaiton, and I don't want to hover and how the information anymore" (JL 261125, the file card)
> "for the files, if they are about to be changed by this plan, could you explan and show them?" (JL 261125, Files pane)
> "maybe we remove things here, and can have a trace mode to replace [the ⊞ button], and click it, and we can show which files will be infleunces by the current trace" (JL 261125, Files pane)
> "why I find many details are gone compared to the previous version? could you work based on the previous version?" (JL 261125, trace mode preview)
> "I actaully want to have the things like the metro map" · "where is the metro map?" (JL 261125, Files pane)
> "this will be more and more, I am thinking how could you make this as a view, like I can expand it, and then the x row is the timeline, the each rwo is the file, and the dots will be the trace, and I can click the trace to see what happened" (JL 261125, Files pane switch)
> "how about they are folded, I dont want to hiden them anymore. but I wawnt them to be folded, do you get it?" · "the rule is, make it clear to see the content" (JL 261125, Files pane)
> "we will first close all the folder, collapase all the folder, and then just expand the folders which contains the related files" · "why these two are sharing now?" (JL 261125, Files pane)
> "why they are in the Also touched? You might need to double cthink about it." · "how do we handle the folder scope, right? this is also an important topic." (JL 261125, Files pane)
> "these two should be the Also Touch, ... these two will also be the also touched, can you remove them out?" (JL 261126, Files pane: workbench-design, workbench-labeling, design/workbench-design, paper/haipipe-paper)
> "for this, why I cannot see [the trace bar]" (JL 261126, b11 Studio, Files pane)
> "when I right click them, the same time, the related files will be highlighted ... and the others will be collapsed" · "How could you make them by default are collapsed?" (JL 261126, j12 Tasks, Files pane)

**Rule:** A trace (`<Block>/trace/<YYMMDD>/<HHMM>_<slug>.md`, named for its first prompt) lists every prompt that worked toward its aim, has its aim and plan (do, path, what) written before any file changes and its Check and Summary before it closes (a `do: move` line names the new place in `path:` and the old one in `what:` as `from <old>`, so a closed move leaves no + row); the Files pane is one tree, and the traces in play mark their files on it where they sit: ◌ planned, ◐ touched (a light sweeping across), ●✓ closed but not committed, ◆ not in the plan, + a file still to create (grey italic, slowly fading), a dot on a folder with marked files inside; an open trace opens the tree down to its files; what the page owns decides the parts and where a file lives decides its place: a traced file inside an owned folder sits there, and every other traced file (another server such as workbench-design, another skill such as haipipe-paper, AGENTS.md) shows under Also touched, grouped by its folder; every Block's pane has the trace bar, and a trace kept in another Block that planned or changed this Block's files joins its metro, marking only this Block's files (the bar stays, greyed, when no trace touches the Block); the pane opens with every folder closed but the way down to the page, and remembers no folder; a right-click on any element folds the pane at once to that element's folder and the code its Task's ## Files names, both highlighted, every other folder closed; one Trace button (a highlighter icon; no chips, no Timeline window) lights up one trace's files and folders, opens the tree down to them and dims the rest, never hiding a row; a funnel always means one trace (on with none picked, it picks the newest; the highlighter off turns it off) and folds what that trace left alone, never hiding it: every folder closes, only the folders holding its files open and nothing else reopens them (a folder the person opens stays), the untouched files beside its files gather under one ⋯ row that opens on a click, and the page scrolls to its first file; the tree keeps its width and scrolls sideways so a name is never cut; a metro map sits beside the tree (each visible row a file line left to right, an open folder a bare line since its files carry the stations, each trace a coloured column of stations, opening on the newest, a click on a station or time picks the trace), and a branching-line icon shows or hides it; a folder's or file's title is on its right-click card (Open, Copy path), never grey text on the row and never on hover.
**Why:** Work changed files with no record of what it meant to change, and nothing showed which files a piece of work touched.
**Class:** a change made with no plan written, or a trace whose files cannot be seen on the tree.
**Cases:** ✅ a move records its new place (1748_page_subfolders, 78 + rows gone; 1810_trace_move_path) · ✅ b17_theme_work 1051_trace_view · ✅ b17_theme_work 1110_folder_icons_rules · ✅ a Block with no trace (no switch) · ✅ many traces on one Timeline, not a button each (1418_trace_timeline) · ✅ marks on the one tree, no switch, no grey titles (1505_tree_marks) · ⬜ every prompt of the trace listed by a Stop hook (by hand today; haipipe-chat retired 261126) · ⬜ `changed:` written by the same hook (by hand today)
**Check:** every trace file has aim and plan lines with do, path and what; a closed one has Check and Summary and every `do: move` path on disk; a Block with traces shows one tree with its marks, a Timeline button, no Files/Timeline switch, and no grey titles on rows.
**Run:** `uv run --quiet --python 3.13 --with pyyaml python plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/scripts/folder_icons_check.py` (add `--url <a running workbench>` to check the pane too)
**Status:** open
**Solved by:** `servers/workbench/side_pane/files_tree/trace_view.py`: states, marks on the tree, the Trace button, the metro map; `side_pane/files_tree/file_info.py`: the right-click card; `scripts/folder_icons_check.py`
**Report:** constitution/A07-trace-plan-and-states.md


# UI previews

A UI preview is a Studio topic whose face says `**Delivery type:** ui`; its rules are in
`haipipe-studio/ref/ui-preview-topic.md`.


## A08 · A page design is looked at on an example Block's live page

> "could you just work on the real examples, and showing the UI, do you get what I mean?" (JL 261126, s07's Topic rows)
> "could we make it to be server generated? and working with blueprints/Project-Ladder/work/b01_example_work?" (JL 261126)
> "so it is the real things to be rendered, and Effect is the quick hmtl" (JL 261126)
> "these two show use the same UI, but different element to highlight, right?" (JL 261126, s11 Topic rows and Job Main)
> "for the effect, we should have the left tab as well, and we can add more effect." (JL 261126)

**Rule:** A UI preview topic has at least one live view, `data-src="/_board/workbench?path=<example Block>&amp;layout=focus…"`, origin-relative, shown under Page; an html in its `delivery/ui/` is a quick view for what the code cannot draw yet, shown under Effect, faded (`class="old"`) once its design is in the code and deleted once settled, and named for what it shows (Task states). Views of one page share one address and differ only by `mark=`, the part each outlines in red (a class, or a data attribute such as `jsub=main`). Page and Effect keep their left tabs even for one view. Each theme keeps one example Block, made only by `new_board.py`, `new_job.py` and `soft_run.py`, holding every Job and Task state and no real work.
**Why:** s07's Topic rows were a hand-drawn html whose data was a snapshot printed by a script run by hand, so the preview drifted from the real page.
**Class:** a UI preview with no live view, a view button that names a file that is not there, or two views that open one address with nothing to tell them apart (s11's Job Main opened another page instead).
**Cases:** ✅ s11-work-job-preview (Topic rows, Job Main live over b01_example_work) · ⬜ s99-guide-view (one quick view; owes its live view once the Guide section is in the code) · ⬜ the Paper theme's example (`blueprints/Project-Ladder/paper/Paper-Example`) as a live view
**Check:** every `Delivery type: ui` topic under `blueprints/` has a live view, every quick view's file exists, and no two live views share one address.
**Run:** `python3 plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/scripts/ui_preview_check.py`
**Status:** open
**Solved by:** `servers/workbench/studio/tabs/studio_tabs.py` (`page_items`: a live view as a left tab; Page and Effect split, left tabs for one view); `servers/workbench/focus-assets/focus.js` (`mark=`); `scripts/ui_preview_check.py`
**Report:** constitution/A08-preview-on-example-block.md

## A09 · Every kind of file a Block holds has one format, and every real file of it renders

> "to map the folder files to the front end, we have the code, but for the folder/ files format, do we have that? I mean do we have the code to preview the folder and file content, to make sure the generated files and folder can be rendered to the html." (JL 261126, b17)
> "you will focus on the b17, and how do you think you should propose the rule for it?" (JL 261126)

**Rule:** Each kind of file a Block holds (Block face, Job face, Task face, Run card, round, trace, Studio topic face, page spec) has one row in the format table, `blueprints/Project-Ladder/work/b17_theme_work/delivery/page-spec/file-formats.md` (where it sits, what it holds, its writer, the page code that reads it, its rule), and every real file of that kind renders on its page with its name and goal showing; a format change moves its row, its writer, its page code and the check together.
**Why:** formats were written in many places or nowhere, and nothing proved a real file drew on its page: Task rounds showed "p01" with no Run, a Block with no trace of its own showed no trace bar, and t03_pane_speed's Run files were written by hand, outside soft_run.py's format.
**Class:** a file of a known kind whose page raises, comes back empty, or drops its name or goal; a kind on disk with no row; a row whose writer or page code is gone.
**Cases:** ✅ b17_theme_work (289 files, 0 problems) · ✅ Block faces, Run cards, rounds, traces, Studio topics, page specs across blueprints/ · ⬜ cowork, discovery and labeling Job and Task pages do not show their goal (16 files; those themes' sessions) · ⬜ example files per kind (j16 t03)
**Check:** every file of every kind in the table renders through its page code with its name and goal showing; the table and the check name the same kinds.
**Run:** `PYTHONPATH=plugins/haipipe-toolkit/servers/_host python3 plugins/haipipe-toolkit/servers/workbench/checks/render_check.py`
**Status:** open
**Solved by:** `servers/workbench/checks/render_check.py` (the check); `b17_theme_work/delivery/page-spec/file-formats.md` (the table); `checks/tests/test_render_check.py` (table and script agree)
**Report:** b17_theme_work/j16_file_formats/t02_render_check/runs/run-check-render/passes/p01-1126/pass.md
