s02 · work skills: workbench-work
=================================

**Tags:** `Skill`

**Stage:** explore

**For:** a deck, and workbench-work's `SKILL.md` and `ref/workbench-table.md` (`skills/2_theme/work/workbench-work/`), rewritten for the three work pages on the focus page (a Block, a Job and a Task, each with Report, Work and Studio), for the people who open a work page and the agents who read it with them

**Delivery type:** skill

**Covers:** what workbench-work's SKILL.md says, section by section, as the outline below lists it, each section named after the cell it comes from: the work pages and how to open one; the parts every work page shares (b17-s04's, named, not redrawn); the sNN card and its tags; for the Block, the Job and the Task page, what Report, Work and Studio show and what each reads from disk; what waits on you and the state words; the older layouts that still open; and its `ref/workbench-table.md`, one row per page, section, view and Run type.

**Excluded:** the screens themselves (j03's nine cells s51 to s59 design them; design_b02_workbench builds them in `servers/workbench/focus_page.py`); what every work page shares (b17-s04 designs it; this skill only names it); the work theme's door and its ladder (haipipe-work, b17-s01); a page for a Run or a Studio topic (none: a Run is a row on its Task's Work, a topic a card where it sits); s02's earlier question, which `1_base/task` skills move to the work theme and the move list for b04 (history, in `result/skill-homes-261031/`).

**Topic:** workbench-work, the skill that opens and reads a work page. Today its SKILL.md still teaches the old Scope · Task · Check · Delivery screens, the Questions and the retired question map (JL 261031, pointing at `skills/2_theme/work`: "you should update this, right?"). It should teach the focus page's three work pages, a Block, a Job and a Task, each with Report (check), Work (do) and Studio (think), as j03's nine cells s51 to s59 design them. Its Design is the skill's new outline, each section naming the cell it comes from; `../j02_workbench_work_skill/` writes it once JL answers the cells' forms.

**Feeds:** none: a work Block keeps no Questions (JL 261031, r01_collect_report_and_delivery Q5)


Files
-----

```text
s02-work-skills/
├── s02-work-skills.md               this face; its Design block is the skill's new outline
├── build_s02_work_skills.py         the builder: haipipe-studio's five parts (five_parts.py), its Design the outline
├── s02-work-skills.excalidraw       the five parts: Idea · Now · Design · Process · Delivery
├── s02-work-skills.png              its card
├── s02-work-skills.mindmap.md       its mind map: the outline, section by section
├── s02-work-skills.ideas.md         its open ideas, one per slide; the deck is a scratch, pictures when asked
├── s02-work-skills.slides.json      the deck's record, from the ideas; .slides.html and .slides.pptx are generated
├── delivery/                        deck/ and render.yaml: SKILL.md and ref/workbench-table.md, each by its j02 Run
└── result/
    ├── first-drawing.excalidraw     the first drawing, kept whole; its builder in first-drawing-builder/
    ├── skill-homes-261031/          the face, mind map, render.yaml and five-part drawing as they were until 261031
    └── old-slides-261031/           the three idea pictures, the deck and its ideas as they were until 261031
```

Rebuild: `python build_s02_work_skills.py` (it writes the drawing and its card from this face, `delivery/render.yaml`,
j02's Task faces and Run cards, the cells' form cards and today's SKILL.md), then `topic_slides.py .` for the deck.


Design
------

The skill's new outline, one section per page (Open 1 asks whether it is one per section instead). Each section names
the cell or topic it comes from; a page's section is written from its three cells' answered forms (Open 2). The builder
draws this block; j02's Runs follow it.

```yaml
outline:
  skill: skills/2_theme/work/workbench-work/SKILL.md
  sections:
  - {name: "The work pages", from: "s02-D03", says: "three pages, each Report · Work · Studio; no page for a Run or an sNN"}
  - {name: "Open a page", from: "b17-s04", says: "?path=<folder>&layout=focus&section=…; a Block opens on Report"}
  - {name: "What every page shares", from: "b17-s04", says: "path, title-&-section, view-button-list, goal-line, both rails"}
  - {name: "The sNN card and its tags", from: "s51 · s53", says: "picture, address, one word, one line; Slide · Draw · Mind map · Work · Delivery · Interaction"}
  - {name: "The Block page", task: t01_block_page, cells: [s51, s52, s53]}
  - {name: "The Job page", task: t02_job_page, cells: [s54, s55, s56]}
  - {name: "The Task page", task: t03_task_page, cells: [s57, s58, s59]}
  - {name: "What waits, and the state words", from: "s52 · s55 · s58", says: "a waiting form orange and first; the words ⏳ ✅ ⬜ 🙋 ❗ only"}
  - {name: "The older layouts", from: "today's SKILL.md", says: "the workflow layout and the classic page, a paragraph each (Open 3)"}
  - {name: "Boundary", from: "today's SKILL.md", says: "it only shows; focus_page.py is design_b02_workbench's"}
  cells:
    s51: {section: Report, form: t01_block_page/runs/r02_collect_block_report_views, says: "MindMap, then a view per delivery type"}
    s52: {section: Work, form: t01_block_page/runs/r03_collect_block_work_views, says: "what waits, each Job and its Tasks, its own Runs"}
    s53: {section: Studio, form: t01_block_page/runs/r04_collect_block_studio_views, says: "a button per group; cards by where they sit"}
    s54: {section: Report, form: t02_job_page/runs/r01_collect_job_report_views, says: "MindMap, then its type: the delivery, its pieces"}
    s55: {section: Work, form: t02_job_page/runs/r02_collect_job_work_views, says: "what waits, a row per Task with its Runs"}
    s56: {section: Studio, form: t02_job_page/runs/r03_collect_job_studio_views, says: "what waits, This Job makes, each Task's topics"}
    s57: {section: Report, form: t03_task_page/runs/r01_collect_task_report_views, says: "MindMap, then its type: a row per current Run"}
    s58: {section: Work, form: t03_task_page/runs/r02_collect_task_work_views, says: "what waits, Runs by role, Ask the agent"}
    s59: {section: Studio, form: t03_task_page/runs/r03_collect_task_studio_views, says: "This Task makes, its topics, Ask the agent"}
  today:
    "The workflow layout, and updating an older Block": "The older layouts"
    "Open": "Open a page"
    "Spaces and Views": "gone: the Block, Job and Task pages"
    "RoadMap Draw": "gone: the question map is retired"
    "Continue with a session": "Boundary"
  ref:
    file: skills/2_theme/work/workbench-work/ref/workbench-table.md
    columns: [Level, Space, View, Run type, Agent, Skill, Person signs, Folder]
    rows:
    - [task, Work, Runs, Plan a Task, haipipe-task-creator-agent, haipipe-task, none, "runs/run-plan-<tNN>/"]
    - [task, Work, Runs, Check a Task, haipipe-task-reviewer-agent, haipipe-task, none, none]
    - [task, Studio, "<group>", Talk and sketch, haipipe-studio-agent (new), haipipe-studio, none, "sNN-<topic>/"]
```


Decided
-------

s02-D01 · Its delivery is one skill piece: the skill-homes table in haipipe-work SKILL.md, made by j02_work_skill_homes; the file moves are b04's, sent to it as a list (j02 t02); the topic sits beside its Job, out of `studio/` (JL 261031, agreed the b17 plan). Replaced by s02-D02 (261031).

s02-D02 · Its delivery is workbench-work, rewritten: its `SKILL.md` and `ref/workbench-table.md` teach the focus page's work pages; the skill homes and the move list for b04 are not the focus any more and stay as history in `result/skill-homes-261031/` (JL 261031, on s01 and s02: "I have no idea, this should not be the things we want to focus"; pointing at `skills/2_theme/work`: "you should update this, right?").

s02-D03 · Three work pages, each with three sections: a work Block, Job and Task each get a page with Report (check), Work (do) and Studio (think), designed by j03's nine cells s51 to s59; a Run gets no page (a row on its Task's Work, opened in the pop-out), and neither does a Studio topic (a card where it sits, opened by its tags) (JL 261031: "run will not get its page, and also the studio will not has its own page as well").

s02-D04 · The skill drops the Questions: a work Block keeps none, so Findings, Answers, Questions and the question map leave its text; Report is the MindMap, then one view per delivery type; a delivery opens from the tags below its sNN; status rows live in Work (JL 261031, r01_collect_report_and_delivery Q2: "we groups things by the types, not the full name"; Q5: "we will not have the questions"; s51-D01 to D05, s52-D01).

s02-D05 · The drawing hands over the skill files: its "what s02 hands over" reads `delivery/render.yaml`, so it names `SKILL.md` and `ref/workbench-table.md`, never the For line (JL 261031: "why for the s02, we don't have the skill as the output?").

s02-D06 · Its Studio group is Skill, beside s01 (JL 261031, `../runs/r01_collect_theme_alignment` Q1: A, "I agree"; adjusted for the overlap: Skill, All pages, Block UI, Job UI, Task UI).


Open
----

1. One section per page (The Block page, The Job page, The Task page, each with its Report, Work and Studio), or one per section (Report, Work, Studio, each with its three pages)? Leaning: one per page, as j03's three Tasks build them, with the rules every page shares written once before them.
2. When does the skill change: once, after all nine cell forms are answered, or one pass per page as its three forms come back (Block: t01_block_page r02 to r04; Job: t02_job_page r01 to r03; Task: t03_task_page r01 to r03)? Leaning: page by page; the first pass also takes out what is already decided gone.
3. The older layouts: the workflow layout (Goal · Plan · Execution · Results, which LLMRec b01 and b02 open on) and the classic page (Scope · Task · Check · Delivery): one short paragraph each until b17-s04's Phase C makes the focus page the default, or dropped now? Leaning: a paragraph each.

(write here, or mark the drawing in red)


History
-------

Until 261031 this topic asked which `1_base/task` skills make the work theme and which stay in base (Q04), and its
delivery was haipipe-work's skill-homes table and a move list for b04 (s02-D01). JL set that aside on 261031 (s02-D02).
Kept, never deleted: its face, mind map, render.yaml and five-part drawing as they were, in `result/skill-homes-261031/`;
its first drawing and builder, in `result/first-drawing.excalidraw` and `result/first-drawing-builder/`; its
three idea pictures, its deck and their ideas, in `result/old-slides-261031/`. Its Job was renamed the same day, from
j02_work_skill_homes to `../j02_workbench_work_skill/`, its two Tasks (t01_skill_homes_table, t02_move_list_b04) moved,
unrun, to that Job's `_old/`.

The theme alignment form (`../runs/r01_collect_theme_alignment/`, Q2) proposed widening s02 into s21, work Run and
skill; JL kept the pick (A) with the note "I don't understand this, why we have two columns? I think w e should jus
have one columns for each of them." Topic numbers and folder names stay as they are this round; the main session
renames later.
