# hai-block · Constitution

JL's feedback on the Block, Job and Task focus pages (the Block -> Job -> Task relationship on screen), kept verbatim.
It wins over SKILL.md and over any page code; where they disagree, follow this file. Written and checked through
`/hai-stack`. Page-wide rules live in `skills/1_base/workbench/hai-ui/CONSTITUTION.md`; read both before changing a
Block, Job or Task page.


## A01 · No 🧭 Around the Work band under the Report

> "I think we will not need this anymore, things will be in the [side pane]" (JL 261124, on the 🧭 Around the Work band with 🧰 Skills and 📁 Files, b16_theme_paper Block)

**Rule:** A Report view ends with its 📋 Review Content; Studio, Interactions, Decisions, Things to Know, Checklist, Timeline, Skills and Files open from the ••• side pane, and only the view's own 🙋 Interactions fold stays on the page when it holds something.
**Why:** The ••• ball and right side pane now hold every right-rail section, so the band repeated them at the bottom of every view.
**Class:** a page writer that appends the shared right-rail sections under a view's content.
**Cases:** ✅ shared frame: work, blueprint, paper, design, draft (`focus_render.around_work`) · ✅ labeling Block/Job (`labeling_focus.py`) · ✅ labeling Task (`labeling_focus_frame.task_shell`) · ✅ tests in workbench, paper, design, labeling
**Check:** no page writer emits a `🧭 Around the Work` heading; a waiting question in a view still shows in that view.
**Run:** `! grep -rnE "🧭 Around the Work</h2>|\"Source Markdown\"" plugins/haipipe-toolkit/servers --include='*.py' | grep -v /tests/`
**Status:** solved 261124
**Solved by:** `work_frame.view_asks`: the view's own Interactions only
**Report:** constitution/A01-no-around-the-work.md


## A02 · No "Open this page's Markdown" line

> "why we have this? I don't think this is necesary." (JL 261124, on the "Open this page's Markdown" footer link)

**Rule:** A focus page carries no footer link to its own Markdown face; the face opens from 📁 Files in the side pane.
**Why:** Every focus page and Studio topic page ended with that link; Files already reaches the same file.
**Class:** a page writer that passes a "Source Markdown" link into the page footer.
**Cases:** ✅ Block/Job/Task focus page (`focus_render.crumbs_goal_source`) · ✅ labeling pages (`labeling_focus_frame.task_shell`) · ✅ Studio topic Delivery (`focus_shell.py`, by Chat-Block-Folder-Icon)
**Check:** no writer builds a "Source Markdown" link.
**Run:** `! grep -rnE "🧭 Around the Work</h2>|\"Source Markdown\"" plugins/haipipe-toolkit/servers --include='*.py' | grep -v /tests/`
**Status:** solved 261124
**Solved by:** `source = ""` in the three writers
**Report:** constitution/A02-no-markdown-footer.md


## A03 · No goal-line under the title

> "Purpose / Design the work theme: Block, Job and Task pages with results and actions together in Report, shared Studio and supporting sections, and the skills that support each level. <---- we can delete this as well." (JL 261124, b16_theme_paper Block)

**Rule:** A Block, Job or Task page shows no Mission/Purpose/Goal line under its title; the goal lives in the Overview's 🎯 Goal fold. Only a draft Task keeps its Aim line, the reader question no fold shows.
**Why:** The goal sentence sat under the title on every page and repeated the 🎯 Goal fold.
**Class:** a page writer that fills the goal-line (`.focus-goal`) for a non-draft page.
**Cases:** ✅ shared frame (`focus_render.crumbs_goal_source`) · ✅ labeling (`labeling_focus_frame.task_shell`) · ✅ Studio topic page "Topic" line (`focus_shell.static_page`, Chat-Block-Folder-Icon) · ✅ draft Task Aim kept by design
**Check:** a non-draft focus page carries no `class="focus-goal"`.
**Run:** `cd plugins/haipipe-toolkit/servers/workbench && PYTHONPATH=../_host uv run --quiet --python 3.13 --with pytest --with pyyaml python -m pytest tests/test_focus_faces.py -q -p no:cacheprovider`
**Status:** solved 261124
**Solved by:** `goal_html` empty unless a draft Aim
**Report:** constitution/A03-no-goal-line.md


## A04 · The core views are bands of one Main view; the other views keep buttons

> "I wnat them into one view, and each previous view will be the section name." (JL 261124) · "for the band, I want to change the [Overview · Plan + Results · Findings · Delivery buttons] the things here to the band" (JL 261124) · "It is not wright, I just asked for the overview and plan and Findings to be in one view, and Others should be in the same view as well ... [Block UI, Job UI bands] for things here, do you want to make them back?" (JL 261124)

**Rule:** A work-shaped Block, Job or Task Report has one Main view whose 📋 bands are Overview, Plan + Results, Findings and Delivery (`view_bands.CORE`), in order, each holding its own numbered folds; every other view (Design, Block UI, Job UI, Task UI, Docs, Project UI) keeps its own button after Main. An empty core view is not drawn; an old `group=<core view>` link opens Main and scrolls to `#band-<view>`.
**Why:** Four buttons hid three quarters of the work behind clicks; but merging every view also buried the UI matrices and Docs (b16 ran nine bands).
**Class:** a Report that shows one view at a time behind a view-button-list.
**Cases:** ✅ work, blueprint, discovery, cowork (`focus_render.section_body` + `view_bands.merge`) · ✅ ★ AI-eval keys by band (`section_eval.band_at`) · ✅ ⓘ addresses by band (`element_info.py`) · ⬜ paper, design, insight, labeling, draft Task (their own view sets)
**Check:** a work Block's Report opens on Main (`aria-current` Main) with `view-band` sections only for core views; `ui-*`, `design`, `docs` are buttons.
**Run:** `cd plugins/haipipe-toolkit/servers/workbench && PYTHONPATH=../_host uv run --quiet --python 3.13 --with pytest --with pyyaml python -m pytest tests/test_work_frame.py tests/test_focus_findings.py tests/test_focus_ui_views.py tests/test_focus_faces.py -q -p no:cacheprovider`
**Status:** open (the other themes keep their buttons until JL says)
**Solved by:** `view_bands.split/merge/bar`: core bands, other buttons
**Report:** constitution/A04-views-as-bands.md


## A05 · The section word beside the title is the sections menu; the 📁 ball is Files

> "how could we make this work, that when I click this [Report], I can choose different things, like Studio, things to know, etc. How do you think? I will keep [the 📁 ball] maybe to be just the file it self." (JL 261125)
> "When I choose studio, will it show it in the main page? Now I want in the right panel. we will just show the files. do you get it?" (JL 261125)

**Rule:** The grey section word after a page's title (• Report, a small dot on its left and no caret) is a button that opens the sections menu under it (Report, Studio, Interactions, Decisions, Things to Know, Checklist, Timeline, Skills); a pick opens that section in the main page, never in the side pane. The 📁 ball opens and closes the Files pane alone, with no menu; the side pane holds Files only.
**Why:** The ball held every section behind one icon at the screen's edge; the word beside the title already names the section, so it is where a reader looks to change it.
**Class:** a page whose section switcher hides behind an icon instead of the section's own name.
**Cases:** ✅ every focus page (`focus_shell.page_shell` `.h1-pick`, `focus.js` side launcher) · ✅ labeling pages (same shell) · ✅ tests in workbench and labeling
**Check:** the title's section word is a `button.h1-pick` controlling `#side-menu`; the ball opens Files straight away.
**Run:** `cd plugins/haipipe-toolkit/servers/workbench && PYTHONPATH=../_host uv run --quiet --python 3.13 --with pytest --with pyyaml python -m pytest tests/test_focus_faces.py tests/test_focus_status_map.py -q -p no:cacheprovider`
**Status:** solved 261125
**Solved by:** `focus.js`: `showMenu(pick)` under the word; a pick goes to the main page; ball = Files
**Report:** constitution/A05-section-word-menu.md

## A06 · A Job is a fixed workflow a command can close; a Studio topic is free design a person closes

> "What I think is job is more AI-auto, and studio will be human driven. I am not sure" (JL 261125, chat)
> "so I think the job should be coding heavy, right? and no much design things, it is like the fixed workflow, they are in the job, and studio will be free style things. I can think and design." (JL 261125, chat)

**Rule:** A Job (jNN) is coding-heavy work on a fixed workflow (Tasks, Runs, tests) that an agent can run to the end, and its `close:` is a check a command or a test can answer; a Studio topic (sNN) is free-style thinking and design that the person drives (drawings, slides, previews, choices), closed when the person picks. A close that waits on a person (agreed, signed, approved) belongs to the sNN; the Job starts from what that topic hands over.
**Why:** b17's j03 closed on "all nine sNN ... are agreed", so a Job did design and JL could not tell a Job from a Studio topic.
**Class:** a Job whose end is a person's agreement, or design work filed as a Job.
**Cases:** ✅ b17 j01_work_ladder_contract · ✅ b17 j03_work_workbench_pages · b11 j01_insight_workbench_pages (removed 261126) · ⬜ b12 j01_design_workbench_pages · ⬜ b15 j01_labeling_workbench_pages · ⬜ b16 j01_paper_workbench_pages · ⬜ b35 j01_studio_delivery_type · ⬜ b35 j02_studio_pages · ⬜ new_job.py's close prompt
**Check:** no Job face's `close:` waits on a person.
**Run:** `python3 plugins/haipipe-toolkit/skills/1_base/project/hai-block/scripts/job_close_check.py`
**Status:** open (the ⬜ Blocks belong to their theme sessions)
**Solved by:** `scripts/job_close_check.py`; b17 j01 and j03 closes rewritten as checks
**Report:** constitution/A06-job-is-a-workflow.md
