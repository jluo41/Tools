<!-- History, kept whole (2026-10-31): s04's face as it stood before s04 narrowed to what every work page shares
(s04-D05). The face now is ../s04-workbench-page-structure.md; build_overview_report.py reads its Executive report
here. Read only: nothing builds from its Tags, Decided or Open lines. -->

s04 · Workbench page structure
==============================

**Tags:** Interface · Navigation

**Stage:** shaping

**For:** a deck, and the work workbench's Block, Job and Task pages (`layout=focus`), each from its three sNN at j03 (s51 to s59); made by `../j03_work_workbench_pages/`

**Delivery type:** ui

**At:** b17

**Topic:** how a work page gives its reader location, purpose, progress and results without scattering related information. This is a design discussion, not an implemented interface. It builds on s03's existing workbench and s32's element designs.

**Feeds:** `reports/` q01_work_ladder · q02_plan_build_execute_report · q03_questions_and_runs

Scope
-----

Project → Theme → Block → Job → Task is the page hierarchy. A Run is an execution of work, shown in the owning work context. A sibling shares the current page's parent; a child sits immediately below the current page. Start the design discussion at Block level, then check how the same navigation works at the other four levels.

Agreed means a stated requirement. Proposal means a suggested design that has not been accepted. Open means a decision still needed from the page owner. Migration into this blueprint does not approve the proposed design or move its Stage.

Files
-----

- `s04-workbench-page-structure.mindmap.md`: the written structure map.
- `s04-workbench-page-structure.excalidraw`: the generated discussion drawing; since 2026-10-28 also two proposal frames: one Block page drawn as a screen (path, introduction, section, one row per Job, one row opened to its figure), and the site as the project memory (show content, show progress, do operations); and the plan to update the layout in six steps, from `servers/workbench/focus_page.py` (`layout=focus`): Phase A read only (intro, Goal & status rows, output in place, the same rows at Job and Task), Phase B operations that write back, Phase C the default switch. Placeholders only.
- `s04-workbench-page-structure.png`: the generated preview.
- `build_s04_workbench_page_structure.py`: draws the five parts (haipipe-studio `five_parts.py`): Idea, Now, Process and Delivery read from disk; Design holds one sketch per delivery piece (A Block page, B Job and Task rows, C element looks, D the merge), each made by a j03 Task; the first drawing kept whole below, its screenshot carried over (261031).
- `result/first-drawing-builder/build_s04_workbench_page_structure.py`: the first drawing's builder, kept whole; it no longer runs from there.
- `result/`: this topic's own working output (b35 s01-D10): `mock/` (the page drafts ui-draft-v1 to v14, slide-style-try; v12 drew Work › Feedback, v13 the collection Run as Work's first row, v14 a compact map beside every section, which JL rejected on 261031 ("we don't need this"): the full MindMap is Report's first view instead, every item open), `assets/`, the layout and plan-scratch drawings with their builders, `b17-overview.mindmap.md` and `overview-report.html`.
- This topic's open choices go to the page owner as collection Runs (haipipe-interaction, 261031: "it will just be the rNN under that page"): `../j03_work_workbench_pages/t01_block_page/runs/r01_collect_report_and_delivery/` asks the six Report and Delivery choices (Report or Delivery, the Report's view buttons, one delivery's view, not made yet, the Questions, MindMap and Status); its `question_collection.md` holds the questions as Markdown, its ticket is the form rendered from it, and `result/answer_collection.md` will hold the answers in the same Markdown.
- [Existing workbench](result/merged-s03-work-workbench/s03-work-workbench.md): the old s03, today's workbench, merged here 261031 and kept whole.
- [Element designs](result/merged-s32-work-element-ui/s32-work-element-ui.md): the old s32, the element gallery and its picks, merged here 261031 and kept whole.

Deployment-specific screenshots and research examples remain in their private workspace. They are not embedded in this shared blueprint.

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

Previously stated requirements, recorded here on 2026-10-28:

1. Show the path first, then introduce the current Block or location.
2. Use one full-width row per item, and show one section at a time.
3. Reveal navigation names when hovering over short bars; remove the Focus mode selector.
4. Show important text and figures directly, without requiring disclosure clicks.
5. Preserve context across Project, Theme, Block, Job and Task.

Proposals and rationale
-----------------------

- Keep the path and introduction stable across sections so the reader keeps their location.
- Use the left edge for siblings; put direct children in the content with their goals and status. This separates changing location from examining its work. The alternative is children on the left; the choice remains open.
- Put section navigation on the right. Guide may be separate help or a section; its placement is unresolved. Avoid a second copy of the same section selector above the content.
- Keep Run-type filters inside execution content. Their role differs from the breadcrumb path and the page introduction.
- Keep each Job's goal, status and output together. Place a figure with its caption, owning Task, Run and review. Finishing an execution does not alone show that the goal was accepted.

Open
----

1. What appears immediately below the introduction: a section heading, a navigation row, or Jobs with their goals and statuses?
2. Does the left edge navigate siblings or direct children?
3. Which sections belong on the right, and where should Guide appear?
4. Which sections are useful at each hierarchy level?
5. Which evidence supports a status, and how does the reader distinguish recorded status from live execution and accepted results?
6. Does a Run keep the same row as a Job and a Task, or open only as a pop-out? (from s32's ideas, 261029)

The page owner decides these questions in the discussion drawing. None is settled by this migration.

Drawing words
-------------

```yaml
drawing:
  title: Workbench page structure
  subtitle: Discussion sketch | agreed requirements, proposed content, open choices
  path: 'Project → Theme → Block → Job → Task'
  introduction: 'AGREED · Current location and its introduction'
  question: 'OPEN · What comes immediately below?'
  options: 'Section heading / navigation row / Jobs and status?'
  left: 'OPEN · Left edge'
  left_options: 'Siblings or children?'
  left_reason: 'Proposal: siblings change location; children stay with their work.'
  right: 'OPEN · Right edge'
  right_options: 'Sections / Guide?'
  right_reason: 'Proposal: one section selector; Run types stay inside execution.'
  content: 'PROPOSAL · One Job, one connected row'
  row: 'Goal → Status → Output'
  reason: 'Understand progress and inspect the result together.'
  result: 'Figure + caption + owning Task + Run + review'
  distinction: 'Execution completed ≠ goal accepted'
  rule: 'AGREED · One section · Full-width rows · Important content visible'
  hover: 'AGREED · Short bars reveal names on hover; no Focus selector'
  levels: 'OPEN · Which sections belong at each level?'
  evidence: 'OPEN · What evidence separates recorded status, live execution and accepted results?'
  owner: 'Page owner decides the red questions. This is not the implemented UI.'
```

Rebuild
-------

Run `python build_s04_workbench_page_structure.py`: it redraws the five parts and the card preview from disk
(261031). Previews of the rest: the shared `haipipe-studio/scripts/render_png.py` and `haipipe-mindmap/scripts/mindmap.py render` on their respective sources. The builder uses explicit element IDs and structural comparisons, without content hashes.


## Studio layout screenshot review

Proposal, 2026-10-28. The public blueprint Studio screenshot is used here at the
page owner's request; no private research screenshot is included.

[Open the annotated canvas](result/studio-layout-review.excalidraw).
The exact original screenshot and editable red comments explain the proposed
responsibilities: top = location and purpose; left = siblings; right = this
Block's sections, including Studio groups. Children remain in the main content.
These are proposals, not accepted navigation decisions.

The second frame embeds an image generated with the built-in image tool. It is a
visual exploration, not implemented UI. It repeats menus; the editable annotations
specify one right navigator, a plain current-section heading and group management
under overflow. Colored bars in the image are not recorded status. Show a format
link only when that artifact exists.

Sources: `result/build_studio_layout_review.py`, `result/assets/studio-current-20261028.png`,
`result/assets/studio-layout-proposal-20261028.png` and
`result/assets/studio-layout-image-prompt.txt`. Rebuild the review with its builder;
the shared canvas writer preserves human annotations.


## Overview map prototype

The page owner requested the shared `haipipe-mindmap` renderer for Overview on
2026-10-28. The first concrete example is this Block, not a global UI change.
[b17 Overview](result/b17-overview.mindmap.md) connects the four recorded design questions,
the six Studio topics and their reports. Each report still records `answer-status: open`.
The current proposal uses shared sections on the right, page-specific views below
the title, and siblings plus direct children on the left.

`mindmap.py render result/b17-overview.mindmap.md` builds the static map. Its browser
screenshot is `result/assets/b17-overview.png`, embedded in the existing
`result/studio-layout-review.excalidraw` by `result/build_studio_layout_review.py`. The canvas
image is a snapshot; the linked map retains its file links. Capture the rendered
page again after changing the map, then rebuild the review canvas.


## Overview–Report in the existing workbench · 2026-10-28

[Open the existing b17 workbench](/_board/workbench?path=blueprints%2FProject-Ladder%2Fwork%2Fb17_theme_work&layout=focus).

The working view now uses the existing workbench renderer. The Block face selects
`home-section: overview-report` and points `overview-map:` to the existing
`result/b17-overview.mindmap.md`. Overview renders that source live; Reports reads the
existing Questions register and report pages, showing recorded answer status,
acceptance criteria and any registered contributing work. The quiet navigation
rails and existing report popup are reused. No new Item records are introduced.

The standalone preview below is superseded and retained as design history.

### Earlier standalone preview

[Earlier preview](result/overview-report.html).

The preview reads this Block's existing Questions and report pages. Overview draws
one connected map; Reports and Items open the same question identities. Each item
shows its recorded answer status, acceptance condition, report extract, source
report, linked evidence and associated Studio topics. Work shows only registered
contributions. No Jobs or Run progress are invented. Delivery is explicitly not
connected in this preview. This is a design preview, not a replacement for the
shared production workbench.

Latest agreed navigation supersedes the earlier navigation alternatives above:
left and right rails stay as quiet short marks by default. Hover or keyboard focus
opens the complete panel; leaving closes it after a short delay. Left navigation
shows siblings and the current page's direct children when present. Right
navigation selects content and Studio groups. Topic representations open in a
large popup and return to the same list position on close.

The cross-Job synthesis Item remains a proposed generalization of the existing
question register: link contributing work without moving it, and keep goal
acceptance distinct from execution completion. This preview reuses Q01–Q04 to
exercise that presentation; it does not introduce a new persisted Item schema.

Sources: `result/build_overview_report.py` and `result/overview-report.template.html`. Rebuild
with the workspace Python and `result/build_overview_report.py`; never edit the generated
`result/overview-report.html` directly. Rebuilding refreshes the source snapshot.


## Executive report

### Key takeaways

The page structure now separates location, purpose and content. The breadcrumb
shows the location; every Block, Job and Task has a primary goal. The left rail
navigates siblings and direct children. The right rail selects a section, and the
buttons below the section title select a view of that section.

The agreed section structure is Overview, Work, Studio, Delivery, Timeline and
Files. Overview offers Map and Executive Report. Work offers Progress and Results.
Studio offers topic groups, with Draw, Mind map and available Slides opening the
topic's content in a popup. A separate Items or Goals navigation entry is not
needed: cross-Job outcomes can be explained in Overview with links to their work.

### Findings and evidence

The existing reports address four connected questions: the work hierarchy, the
placement of work phases, the link from questions to Run evidence, and skill
ownership. Q01 contains a draft hierarchy proposal; Q04 contains a skill-ownership
proposal. Q02 and Q03 do not yet record an answer. These sources support a design
in progress, not a claim that the whole Block is complete.

The page-layout agreement in this discussion does not close those broader
questions. In particular, the older six-Space proposal in Q01 must be reconciled
with the newly agreed navigation before it can serve as the accepted answer.
The source reports and their acceptance criteria remain the evidence for closure.

### Decisions and next steps

1. Use this page to review Map and Executive Report as two views of Overview.
2. Check the same structure on a real Job and Task, including their results.
3. Reconcile the older Q01 proposal with the agreed page structure in its owning report.
4. Record how each report traces its findings to contributing Tasks and exact Runs.
5. Resolve skill ownership before selecting an accepted version for Delivery.

### Scope of this report

This is a synthesis for b17, written from the existing question register, report
pages and the page-layout decisions agreed on 2026-10-28. Recorded question
statuses appear below. They are source records, not live execution measurements.

## Navigation agreement · 2026-10-28

The page owner accepted the distinction between page hierarchy, primary goal,
sections and views. This supersedes the earlier Items-navigation alternative in
this topic. The existing preview now demonstrates that agreement; it continues
to use the shared mind-map renderer and the same quiet left and right rails.
