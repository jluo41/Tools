s04 · Workbench page structure: what every work page shares
===========================================================

**Tags:** `All pages`

**Stage:** shaping

**For:** a deck, and the six parts every work page shares on the focus page, the same at Block, Job and Task, as screen drafts in `delivery/ui/` (`frame/`, `interactions/`, `delivery/`, `related/`, `timeline/`, `files/`) that design_b02_workbench builds into `servers/workbench/focus_page.py`; made by `../j03_work_workbench_pages/t04_shared_parts/`, for the people who build the workbench

**Delivery type:** ui

**At:** b17

**Covers:** the frame of every work page: the path, the title-&-section, the view-button-list under the title, the goal-line (Purpose for a Block, Goal for a Job, Aim for a Task), the view-caption, the left-rail (siblings, the open page's children under it, sNN first), the right-rail (its sections, one line each), the pop-out over the page and the phone's section-line; and the right-rail's other sections: Interactions (answer), Delivery (hand over), Related (take in), Timeline (look back), Files (browse).

**Excluded:** each level's Report, Work and Studio, the content inside the frame: the nine cells at j03's three Tasks own them (s51, s52, s53 the Block; s54, s55, s56 a Job; s57, s58, s59 a Task). Also left to their owners: the form, the Interaction button and its pop-out list (haipipe-interaction); what a delivery holds and its versions (haipipe-delivery); what Related holds (haipipe-related); the code itself, `servers/workbench/focus_page.py` (design_b02_workbench); the paper's pages (b16 j01).

**Topic:** the focus page's frame and right-rail, the same on every work Block, Job and Task page; what no cell owns, around each level's Report, Work and Studio (JL 261031: "the interface and the Block UI Job UI and Task UI, there are some overlap, right?"). It began as the whole page-structure discussion (location, purpose, progress and results on one page) and narrowed on 261031 to the parts every level shares; the nine cells s51 to s59 own the rest. Its drawing is haipipe-studio's five parts, drawn by `build_s04_workbench_page_structure.py`: its Design is the frame as proposed, drawn on j03's own page (A), and the right-rail's other sections with the Interactions page's three designs (B).

**Feeds:** none: a work Block keeps no Questions (JL 261031, r01 Q5)


Files
-----

```text
s04-workbench-page-structure/
├── s04-workbench-page-structure.md            this face
├── build_s04_workbench_page_structure.py      the builder: haipipe-studio's five parts, every fact read from disk
├── s04-workbench-page-structure.excalidraw    Idea · Now · Design · Process · Delivery; the first drawing kept below
├── s04-workbench-page-structure.png           its card
├── s04-workbench-page-structure.mindmap.md    its mind map: the frame, the rail's other sections, what is open
├── s04-workbench-page-structure.ideas.md      its open ideas, one a slide
├── s04-workbench-page-structure.slides.*      its slides as cards of words; pictures only when asked
├── passes/                                    its rounds: p01-1028, p02-1029, p03-1031
├── delivery/render.yaml                       the six shared parts, each built by j03's t04_shared_parts
├── delivery/deck/                             its deck, once made
└── result/                                    its working output and its history (below)
```

In `result/`: `merged-s03-work-workbench/` (the old s03, today's workbench) and `merged-s32-work-element-ui/` (the
old s32, the element gallery), merged here 261031 and kept whole; `mock/` (the page drafts ui-draft-v5 to v14,
plan-draft, slide-style-try); `first-drawing.excalidraw` and `first-drawing-builder/` (the first drawing, kept below
the five parts); `face-history-261031.md` (this face before the narrowing, whole); `old-design-261031/` (the
five-part builder and card before the narrowing, kept whole; it no longer runs from there); `old-slides-261031/` (the six idea slides of 261029, their pictures
and deck); `old-mindmap-261031/`; the layout and plan-scratch drawings with their builders; `b17-overview.mindmap.md`
(board.md's `overview-map:`) and `overview-report.html`.

Its two forms name s04 in their `for:` line, so they show on its card:
`../j03_work_workbench_pages/t01_block_page/runs/r01_collect_report_and_delivery/` (answered 261031 17:40; its answers
are s51-D01 to D06, applied by s51) and `../runs/r02_collect_interactions_page/` (waiting: the Interactions page).


Decided
-------

s04-D01 · Keep this general page-design discussion in the work theme blueprint; retain s03 as the old reference. (User 2026-10-28)

s04-D02 · Merge s03 and s32 into s04: s03 (today's workbench) and s32 (the element gallery) deliver the same thing
as s04, the work workbench's pages; both are kept whole in `result/merged-s03-work-workbench/` and
`result/merged-s32-work-element-ui/`, and their numbers are retired (JL 261031, agreed the b17 plan).

s04-D03 · One ui delivery, made by j03: the work Block, Job and Task pages, made by j03_work_workbench_pages (Phase A
first); the code lands in `servers/workbench/focus_page.py` through its owner, design_b02_workbench; the topic sits
beside its Job, out of `studio/` (JL 261031, agreed the b17 plan).

s04-D04 · The work pages are a 3 × 3, as the paper's (b16 j01): Block, Job and Task × Report, Work and Studio, one
sNN each at j03's three Tasks (s51 to s59), drawn through `j03_work_workbench_pages/work_ui_cells.py`; s04 keeps what
every work page shares, and its pieces are the three pages (JL 261031: "I think you should focus on the things like ... b16_theme_paper ... studio ... UI and think about how you should update the work_theme's workbench UI"). JL's r01 answers are s51's Decided.

s04-D05 · Only what every work page shares: the frame (path, title-&-section, view-button-list under the title, goal-line, both rails, the pop-out) and the right-rail's other sections (Interactions, Delivery, Related, Timeline, Files), the same at Block, Job and Task; each level's Report, Work and Studio belong to the nine cells, s51 to s59 (JL 261031: "the interface and the Block UI Job UI and Task UI, there are some overlap, right?").

s04-D06 · Six pieces, the shared parts: `frame`, `interactions`, `delivery`, `related`, `timeline` and `files`, each a screen draft in `delivery/ui/`, made by j03's t04_shared_parts (`run-design-shared-parts`); the three pages are the nine cells' own `delivery/ui/`. This replaces the last clause of s04-D04, "its pieces are the three pages" (JL 261031, the same overlap).

s04-D07 · One Studio group, `All pages`, in place of `Interface` and `Navigation`; b17's groups read Skill, All pages, Block UI, Job UI, Task UI (JL 261031: the theme alignment form `../runs/r01_collect_theme_alignment/` Q1, "I agree", adjusted for this overlap).

s04-D08 · No page for a Run or an sNN: a Run is a row on its Task's Work, opened in the pop-out; an sNN is a card where it sits, opened by its tags Slide · Draw · Mind map · Work · Delivery · Interaction (JL 261031, on s01's sticky "does a Run get its own page?": "run will not get its page, and also the studio will not has its own page as well."). It settles the old Open 6.

s04-D09 · Interactions, Delivery stay on the rail: at a Block, a Job and a Task the right-rail always shows Interactions, Delivery and Files, empty or not, and Related and Timeline only when they hold something (JL 261031: "in the right rail, we should have a section named the Interaction, to show all the interaction under this page"; "we also missed the delivery here"; built in `focus_page.render`). It settles the right-rail half of the old Open 3.

s04-D10 · The frame's order, top to bottom: path, title-&-section, view-button-list, goal-line, view-caption, content; a section with one view keeps its one button, so the goal-line never moves (JL 261031, b10 r01 Q1: "if it is the view based, we will put it above the Purpose"; haipipe-ui rule 1; built in `focus_page.page_shell`). It settles the old Open 1.

s04-D11 · Left-rail changes page, right-rail section: the left-rail lists the siblings with the open page's children under it, a level's sNN first; both rails are pale short lines until hovered (JL 261028: "I don't want to make them too obvious"; JL 261030: "you should show the sNN as well, they are in the same level now"; built in `focus_page.rail_kids`). It settles the old Open 2.

s04-D12 · Two groups under every view: 📋 Review Content holds the view's own numbered sections; Around the Work holds
Studio, Interactions, Decisions, Things to Know, Checklist, Timeline, Skills and Files, unnumbered, the same under every view
(JL 261108: "View content should keep it as it is, and Shared should be the Around the work"; then, renaming the top
group: "Change the Results to the things like "Review Content"").

s04-D13 · Interactions and Decisions are two sections, each with its topics as left tabs: Interactions in the standard
look, each form a topic with its questions under it and the form on the right, the page's whole inbox under every
view; Decisions one tab per Studio topic (JL 261108: "maybe we still seperate the decision, and for both interaction and
decisions, we have the left tab to be the topics").

s04-D14 · Decisions read one row per sNN-DNN: its number, its first clause, and a tag only when its own words carry one
(Replaced, Waiting, Proposed); the full text opens under the row, and no row is called confirmed from a quote (JL
261108: "this is not readable, could you redo it?").

s04-D15 · A view named like a Studio group (Block UI, Job UI, Task UI) shows only that group's topics in Studio and
Decisions; every other view shows all of them. Proposed by the agent on JL's question (JL 261108: "is this for all the
studio, or just the studio related to this view?").

s04-D16 · Checklist's icon is 📝, as CoWork's Steps: ☑️ draws as a grey box (JL 261108: "could you have a better icon
for this?"; the agent picked 📝, since ✅ is Acceptance's and 📋 Requirements').

s04-D17 · Skills reads each skill in place: its SKILL.md under its prompt, and a button per file its folder holds,
SKILL.md first, caches left out; a frame loads only when it can be seen (JL 261108: "how could I preview all the
skills' content?"; "we also have other file, how do we show them as well?").

s04-D18 · Status shows the Jobs and Tasks first, in the 261105 look: a band per jNN (its `bands:` name, else jNN), each
Job a row with its emoji, its jNN, its name and how far ("partly · 7 Tasks · 14%"), opening to its Tasks and Runs;
Topics follow only when they group the work differently from the Jobs. One thing shows once, in one look, under one
name (JL 261108: "what I want is first showing the jobs and tasks"; "we want the style like this"; "how could we make
them to be consistent?").

s04-D19 · A Job's name is its folder's words (j01_work_ladder_contract reads "Work ladder contract"), and its emoji is
its face's `emoji:` line (JL 261108: "we want to have the job name to be the same to the job folder name"; "why not
emoji for these job?").

Previously stated requirements, recorded here on 2026-10-28:

1. Show the path first, then introduce the current Block or location.
2. Use one full-width row per item, and show one section at a time.
3. Reveal navigation names when hovering over short bars; remove the Focus mode selector.
4. Show important text and figures directly, without requiring disclosure clicks.
5. Preserve context across Project, Theme, Block, Job and Task.


Open
----

1. Which Interactions page, A, B or C: one page answers every waiting form, as A a questionnaire grouped by the page that asked, B two lanes picked by their pictures, or C a checklist with one form open at a time (my pick); and do options show their pictures inline (my pick: yes)? The form `../runs/r02_collect_interactions_page/` waits for JL.
2. An empty section on the right-rail: stay at every level, or leave? Interactions and Delivery stay today (s04-D09); Studio, Related and Timeline leave. The Job and Task forms ask it for Studio (`../j03_work_workbench_pages/t02_job_page/runs/r03_collect_job_studio_views/` Q5, `t03_task_page/runs/r03_collect_task_studio_views/` Q2; my pick in both: stay); their answer becomes one rule here.
3. The right-rail's Delivery beside the Report's type views (s51-D01): the rail keeps the files, their versions and sent marks (haipipe-delivery) and the Report the look and one word (leaning), or one place only? r01 Q1 asked it about the paper, and JL set it aside: "you will focus on the work_theme".

(write here, or mark the drawing in red)


History
-------

1. **The page-structure discussion** (261028 to 261031): Scope, the Proposals and rationale, the Drawing words, the studio layout review, the overview map prototype, the Overview and Report preview, the executive report and the navigation agreement are kept whole in `result/face-history-261031.md`; `result/build_overview_report.py` reads its executive report there.
2. **The six old Open points**: 1 (what sits below the introduction) is settled by s04-D10; 2 (siblings or children on the left) by s04-D11; 3 (which sections on the right, and Guide) by s04-D09, the Guide going to the theme alignment form (`../runs/r01_collect_theme_alignment/` Q3); 4 (which sections at each level) and 5 (what evidence backs a status) went to the nine cells, where status rows live in Work (s51-D01 to D06, s52-D01); 6 (a Run's own row or a pop-out) is settled by s04-D08.
3. **Its Design before the narrowing** (A the Block page, B the same rows at a Job and a Task, C one look per element, D the merge): `result/old-design-261031/`, its builder and its card.
4. **Its six idea slides of 261029** (what a Block is, its parts, what a Studio is, how a round leaves it, one screen of a Block, how big a Studio grows), no longer about the shared parts: `result/old-slides-261031/`, with their pictures and deck.
5. **Its mind map before** (agreed, proposal and open nodes of the page-structure discussion): `result/old-mindmap-261031/`.


Rebuild
-------

`python build_s04_workbench_page_structure.py` redraws the five parts and the card from disk: the frame's words and
the right-rail from `servers/workbench/focus_page.py`, the left-rail from b17's folders, the goal-line from j03's face,
the pieces from `delivery/render.yaml`, the three Interactions designs from
`../runs/r02_collect_interactions_page/question_collection.md`. The mind map: haipipe-mindmap
`scripts/mindmap.py render s04-workbench-page-structure.mindmap.md`. The slides: haipipe-studio
`scripts/topic_slides.py .` (cards of words until pictures are asked for).
