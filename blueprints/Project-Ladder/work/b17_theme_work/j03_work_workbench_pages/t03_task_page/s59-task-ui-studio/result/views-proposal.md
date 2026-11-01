# s59 · Task UI: Studio · views proposal

Proposal, 2026-10-31. One cell of b17's 3 × 3: a work Task's page × Studio (verb: think). JL's choices go to the form
`../../runs/r03_collect_task_studio_views/` (five questions, each option previewed); everything else here is decided
by me and marked so. Sources: today's code (`servers/workbench/focus_page.py`, `frame.py`), today's pages on 5623
(t03_task_page, t01_block_page, t01_skill_section), a research Task page on 5599 (structure only), b16's s40 and its
form, the sibling cells' forms (s53 `t01_block_page/runs/r04_collect_block_studio_views`, s56
`t02_job_page/runs/r03_collect_job_studio_views`), and JL's r01 answers (s51-D01 to D06).

Words used below: an **sNN** is a Studio topic folder `sNN-<topic>/`; a Task holds at most three (`new_topic.py`
`LIMITS`). A **piece** is one entry of a topic's `delivery/render.yaml` (`pieces:`, each with `code:` and `by:`); its
`by:` names the Run that makes it. A **group** is a name on a topic face's `**Tags:**` line; groups are the Studio's
view buttons (JL, decided).


## The page, as proposed

```text
t03_task_page  Studio                                     title-&-section
[Interface] [Navigation] [Task UI]                        view buttons: the shown topics' groups, Block order
Aim  a work Task's page on the focus page, ...            goal-line (b17-s04's, unchanged)
Topics tagged Interface: what this Task makes, then its own.            view-caption
▾ This Task makes
    b17-s04:theme_work @ workbench_page_structure  shaping · ui · piece: task-page     [lead slide]
    Slide · Draw · Mind map · Work · Delivery · 🙋 Interaction
▾ Ask the agent
    [ your notes, copied with the prompt ]
    Copy prompt: talk and sketch · Copy prompt: start a topic
```

The same page on its `Task UI` view shows `▾ Its topics` with s59 first (its form waits), then s57 and s58, then
`▾ Ask the agent`. A Task with nothing to show (b35's `t02_new_topic_for_line`) shows one button, `Topics`, one line
"No topic sits at t02_new_topic_for_line yet." and Ask the agent with only "Copy prompt: start a topic".


## (a) The view list

1. **Studio is on the right rail of every Task page** (form Q2, pick A), after Work: `Report · Work · Studio ·
   Interactions · Delivery · Timeline · Files` (Timeline only when it has events). Its rail line stays "drawings, mind
   maps, slides". Today it shows only when the Task holds an sNN (`focus_page.render`, line 1845).
2. **The buttons are groups**: one per group named by the `**Tags:**` of every topic this Studio shows (its own sNN and
   the Block or Job topic it makes), in the Block's `_studio_groups.txt` order (b17: Skill, Interface, Navigation,
   Block UI, Job UI, Task UI). `Other` comes last when a shown topic has no Tags. One button, `Topics`, when no shown
   topic has a group, or when nothing shows. No All, no counts (JL, decided).
3. **It opens on the first button.** If JL picks s53 Q4 A (a waiting form marks its group's button and the Studio opens
   there), the Task page follows that rule too.

What the buttons are on today's real Tasks, under this proposal:

```text
t03_task_page          Interface · Navigation · Task UI    s04 (it makes task-page) · s57 s58 s59
t01_block_page         Interface · Navigation · Block UI   s04 (it makes block-page) · s51 s52 s53
t02_job_page           Interface · Navigation · Job UI     s04 (it makes job-page) · s54 s55 s56
t01_skill_section      Skill                               s01 (it makes ladder-section)
t02_scaffold, t03_demo_fixture   Skill                     s01 (work-scaffold, demo-block)
t01_skill_homes_table, t02_move_list_b04   Skill           s02 (skill-homes-table, move-list)
b35 t02_new_topic_for_line   Topics                        nothing: the empty state
```

If JL picks s53 Q1 A (groups by delivery type: Skill and UI), each b17 Task has one button, `UI` or `Skill`.


## (b) Each view and its sections, in order

Every view (a group, `Other` or `Topics`) has the same parts in this order. Its sections are the draft page's view
sections: a heading bar each (`fd-sec`, `fd-h`), folding by its heading, open by default, the reader's choice kept in
the browser (haipipe-ui rule 4). A section with nothing in it does not show.

### 0 · View-caption (decided by me)

1. **Shows**: one line above the content: "Topics tagged Interface: what this Task makes, then its own."; on `Topics`:
   "What this Task makes, then its own topics."
2. **Reads**: the open button's name.
3. **Empty**: always shown (haipipe-ui: every view says what it shows). Today a Studio view has no caption.

### 1 · This Task makes (form Q1, pick A)

1. **Shows**: the full card of each Block or Job topic whose delivery piece this Task makes, first in the view, with one
   pill naming the piece: `piece: task-page`. On t03_task_page: s04; on t01_skill_section: s01.
2. **Reads**: every `sNN-*/delivery/render.yaml` at the Task's Block and at its Job: a `pieces:` entry whose `by:` path
   starts with this Task's folder (s04's `by: j03_work_workbench_pages/t03_task_page/runs/run-design-task-page`); the
   piece's name is its `code:` text before the colon (`task-page`), the same word as that Run's `target:`. Also a Block
   topic whose face says `**At:**` this Task (`frame._hung_here`, b35 s01-D05), shown without a piece pill.
3. **Where**: in the views of its own groups only (s04 in Interface and Navigation), as every topic: the group rule
   holds and s56 Q2 A does the same for a Job.
4. **Empty**: the section does not show.
5. **Tags and actions**: the card's tags (below); its name opens its face on the Block, its picture its slide.

### 2 · Its topics

1. **Shows**: the Task's own sNN, at most three, one card per row: a card whose form waits on you first (orange
   `🙋 Interaction`), then sNN order (decided by me: what waits is orange and first, JL's taste).
2. **Reads**: `<task>/sNN-<topic>/` beside `runs/` (`frame._studio_topics`), and an older `<task>/studio/` while one
   exists.
3. **Empty**: the section does not show. When nothing shows in the whole Studio, the view shows one line instead:
   "No topic sits at <task> yet." (form Q2, pick A).
4. **Tags and actions**: the card's tags (below).

### The card (the same in both sections)

1. **Picture** (right): the lead idea slide (the first `image` in `sNN-*.slides.json`), else `sNN-*.png`; a click opens
   the slide or the drawing in the pop-out. s57 to s59 show their five-part drawings; s04 and s01 their first slides.
2. **Name**: `b17.j03.t03-s59:theme_work.work_workbench_pages.task_page @ task_ui_studio` (`frame.topic_label`); opens
   the face, popped out.
3. **Words after the name**: its stage (`**Stage:**`, one word), its delivery type (`**Delivery type:**`), and on This
   Task makes the piece pill.
4. **One line**: today the Topic's first sentence. s53 Q3 asks whether it becomes the face's first Open item; the Task
   card follows s53's answer.
5. **Tags** (JL, r01 Q3: a delivery opens from the tags below its sNN): `Slide` (when `sNN-*.slides.html` is built) ·
   `Draw` (`sNN-*.excalidraw`) · `Mind map` (`sNN-*.mindmap.md`) · `Work` · `Delivery` (`delivery/`, its planned look
   until made, s51-D03) · `Interaction` (a collection Run whose `target:` names the topic; `🙋` and an orange edge
   while one waits, b16 r07). Every tag pops out over the page.
6. **Work on a Task page** (form Q5, pick A): opens the Run that writes this topic's delivery, popped out: for an own
   topic the Task's Run whose `run.yaml` `writes:` names its `delivery/` (s57 to s59: `run-design-task-page`, soft,
   design, queued, target task-page); for a made topic the Run its `render.yaml` `by:` names. Today it opens the whole
   Job (`work_root`: a Task's sNN gives `owner.parent`), all of j03's Tasks and Runs.
7. **Its home**: a link to an sNN from elsewhere (the left rail, a form's `for:`) opens this card in this Studio, under
   its group, outlined (`topic_home`, `.studio-row:target`; b35-s02-D05).

### 3 · Ask the agent (form Q4, pick A: the last section)

1. **Shows**: one notes box ("your notes, copied with the prompt"), then two buttons; each prompt shows on hover. Plain,
   never orange: nothing here waits on you.
2. **Copy prompt: talk and sketch** (only when a topic shows): `/haipipe-studio <task path> <sNN ids>: talk with me
   about <task>'s aim and sketch it on the topic's drawing; write no text yet; what we settle goes into the topic's
   Decided.`
3. **Copy prompt: start a topic** (always; form Q3, pick A): `/haipipe-studio <task path>: start a new topic here with
   new_topic.py (a Task holds three at most), then talk with me and sketch it.` With three own topics the button stays
   and the agent answers with the limit's rule: reuse one, or start it on the Job (decided by me: a missing button
   explains nothing).
4. **Reads**: the Task's folder path from the SPACE root, its face name, the shown sNN ids; the notes stay in this
   browser (the draft page's `fd-run` box, `focus_draft._run_rows`, line 215).
5. **Empty**: always shown; on an empty Task it holds only "start a topic".

### The `Other` and `Topics` views

1. **Other**: the same sections, holding the shown topics with no Tags.
2. **Topics**: the same sections when no shown topic has a group; the empty state when nothing shows (button `Topics`,
   caption, the one line, Ask the agent with "start a topic").


## (c) What this cell leaves to the other cells

1. **s53 (Block Studio)**: the card's look and its one line (s53 Q3), the group names (s53 Q1), where a waiting form
   also shows (s53 Q4), and sections by where each topic sits (s53 Q2). The Task page uses the same card and follows.
2. **s56 (Job Studio)**: "This Job makes" and its headings per Task. This cell's "This Task makes" is the same rule one
   level down; JL's s56 Q1 and Q4 answers should hold here too.
3. **s58 (Task Work)**: the Runs, the waiting form row, Work's own Ask the agent. Form Q4 C would move both Studio
   prompts into Work's box.
4. **s57 (Task Report)**: the Task's MindMap and its newest result.
5. **b17-s04 (every work page)**: the path, the title-&-section, the goal-line (Aim), the rail order, the pop-out.
6. **The Interactions section** keeps the inbox; a card's Interaction tag opens the same items, nothing more.
7. **haipipe-studio** owns `new_topic.py`, the limits and the face; **design_b02_workbench** writes the code (f).


## (d) Compared with b16's s40 and today's pages

```text
                     b16 s40 (Section, proposed)  work Task today            s59 (proposed)
Studio on the rail   always (a draft Task)        only with an own sNN       always (Q2)
topics shown         Block topics naming it       its own sNN                what it makes, then its own (Q1)
view buttons         This Section · Board         its own topics' groups     shown topics' groups, Block order
link up              face names jNN_/tNN_         none                       render.yaml by: (exact, per piece)
empty                "No Studio topic names …"    Studio gone; opens Work    "No topic sits at <task> yet."
start a topic        Q1: button or prompt (B)     no way                     prompt (Q3), same as s40's B
Ask the agent        a fold on top                none                       last section (Q4), plain
Work tag             (draft: none)                the Job's whole Work       the Run that makes it (Q5)
```

1. **Same as b16 s40**: Studio always on the rail, one empty line, a talk-and-sketch prompt, starting a topic by a
   copied prompt (s40's pick B), the topics from above that the page's work serves.
2. **Different from s40**: a work Task holds its own sNN (a Section holds none), so its view buttons are groups (JL
   decided this for the work theme), not scope buttons; the link up is the exact `render.yaml` `by:` per piece, not a
   face that mentions the Task's name; Ask the agent is the last section, not a fold on top (no fold arrows; pictures
   first, the Studio's first principle).
3. **Same as today**: the card, its tags, groups as buttons, the Interaction flag.
4. **Different from today**: Studio on every Task's rail; the topic it makes shows (on t03_task_page today s04 is
   absent; on t01_skill_section the Studio is absent and `section=studio` silently opens Work › Progress); a caption;
   Ask the agent; Work opens the Run, not all of j03 (today: three Tasks and thirteen Runs in one pop-out).
5. **The research Task on 5599** (structure only): its rail is Report · Work · Interactions · Timeline · Files, no Studio;
   `section=studio` opens Work. Under Q2 A it gains Studio with the empty line and the start prompt.


## (e) Alternatives weighed, my pick, why

1. **Show the topic it makes?** Full card first under "This Task makes" (**pick**, form Q1 A) · one line opening its card
   on the Block (B) · no (C) · every Block topic (dropped: the Block's Studio already lists them, and each Task would
   repeat all of them) · scope buttons This Task · Block as b16 s40 (dropped: JL decided groups are the buttons). Why:
   most Tasks hold no sNN; the topic they make is their thinking, and `render.yaml` already names it exactly.
2. **Where it sits** (mine): in its own groups' views (**pick**: the group rule, as s56 Q2 A) · a fixed section in every
   view (weighed: no extra buttons, but it repeats across views and leaves the rule).
3. **Order in a view** (mine): This Task makes, then Its topics (**pick**: s56 puts "This Job makes" first; the whole
   before its parts) · own topics first.
4. **Button order** (mine): the Block's `_studio_groups.txt` (**pick**: the Block page's order, s56 Q2 A) · the order the
   topics come in (today, line 1879).
5. **A Task with no topic**: Studio stays with one line (**pick**, Q2 A: JL keeps Interactions and Delivery on the rail
   when empty, and the empty Studio is where a topic starts) · leaves the rail (B, today).
6. **Start a topic** (s59's red question): Copy prompt (**pick**, Q3 A: a topic needs a slug, a title and a band; the
   agent writes face, mind map and drawing in one go) · a New topic button that writes the folder (B: one click, but an
   empty face, and the person still asks the agent to draw) · both (dropped: two ways to do one thing).
7. **Ask the agent**: last section (**pick**, Q4 A) · first section (B) · only in Work (C: one box per page, but the
   Studio then cannot start its own topic) · a Talk tag on each card (dropped: a seventh tag; JL fixed the tags in r01
   Q3).
8. **Work tag on a Task page**: the Run that writes its delivery (**pick**, Q5 A) · the Job's whole Work (B, today) · no
   Work tag (C).
9. **What waits** (mine, until s53 Q4 and s56 Q4 are answered): the card first with its orange `🙋 Interaction`
   (**pick**) · a line on top of the view (s56 Q4 A) · its group's button orange (s53 Q4 A). The Task page takes JL's
   answer there; asking a third time would repeat the same choice.
10. **Caption** (mine): one line per view (**pick**: haipipe-ui) · none (today).
11. **Piece pill** (mine): `piece: task-page` on a made topic (**pick**: says which part this Task makes) · none.
12. **The empty line's words** (mine): "No topic sits at <task> yet." (**pick**: says where, in plain words) · b16's "No
    Studio topic names <task> yet." (fits a Section, whose topics name it; a work Task's sit in it).


## (f) The code change, named for its owner (design_b02_workbench)

All in `plugins/haipipe-toolkit/servers/workbench/`; nothing is edited here (j03's rule).

1. `focus_page.render` (line 1845): add Studio to the rail for every Task: `if topics or draft or page_level(folder) ==
   "Task"`.
2. A new `frame.made_here(task, root)`: `(source, topic, drawings, piece)` for each `sNN-*/` at the Task's Block and Job
   whose `delivery/render.yaml` has a `by:` under the Task's folder; `focus_page.topic_rows` (line 638) adds them
   for a Task page with `facts["made"] = piece`, beside `frame._hung_here` (line 2341).
3. `focus_page.render` (line 1879): order the group buttons by `frame.studio_group_order(block)` (line 2471), then
   `Other`; `Topics` stays the one-button case (line 1911).
4. `focus_page.studio_html` (line 682): on a Task page, draw the sections This Task makes · Its topics · Ask the agent
   as `fd-sec` headings (the draft page's CSS, `focus_draft.CSS`); a waiting card first; the piece pill; the empty line
   "No topic sits at <task> yet." in place of "No Studio topics in this section."
5. `focus_page.work_root` (line 433): for a topic shown on a Task page, the Task's Run whose `run.yaml` `writes:` names
   the topic's `delivery/`, or the made topic's `by:` Run; the Work tag pops out that Run's row.
6. A view-caption for each Studio view (none today; `VIEW_WORDS` holds no group).
7. Ask the agent: `focus_draft._run_rows` (line 215) with the two prompts in (b) 3.

If JL picks Q3 B, a write-back is added too: a POST that runs `new_topic.py topic <task> --slug <slug> --title
<title> --band <band>` and refuses a fourth topic.


## The form and its previews

1. Form: `../../runs/r03_collect_task_studio_views/r03_collect_task_studio_views.html`, five questions: Q1 Made topic ·
   Q2 No topic · Q3 One click (s59's red question) · Q4 Ask the agent · Q5 Work tag.
2. Previews: `option-q1-a.html` to `option-q5-c.html` in the same Run, written by
   `../../scripts/build_r03_previews.py` from disk (names, stages, pieces, pictures, form states, Run cards); rerun it,
   never edit them.
3. Applying the answers: `run-design-task-page` writes the agreed screen into `../delivery/ui/`; the decisions go in
   s59's face `Decided` as s59-D01 onward.
