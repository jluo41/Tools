# s52 · Block UI: Work · the views, proposed

for: b17.j03.t01-s52:theme_work.work_workbench_pages.block_page @ block_ui_work
written: 2026-10-31, by the s52 agent. JL's choices are on the form
`../../runs/r03_collect_block_work_views/r03_collect_block_work_views.html`; until he answers, every pick below is a
proposal, and the Decided list on the s52 face is unchanged.

The work Block's Work section, verb **do**: what waits on you, then each Job and where its Tasks stand, then the
Block's own Runs. It never says what was found (Report, s51) and never thinks (Studio, s53).

Already decided, applied here and never asked again:

- s52-D01: where things stand lives in Work, as rows; the Report keeps one word per delivery (r01 Q6: A).
- s51-D01 to D06: the Report is the MindMap, then one view per delivery type (Skill · UI); a delivery opens from the
  tags below its sNN; planned until made; one word, its current version; no Questions on a work Block.
- b16 t01 r04 Q3 to Q6 and r07: one button, "Interaction", on every row that holds one; it pops out its list, the
  waiting item first; "🙋 Interaction" with an orange edge while a question waits, plain once nothing does.
- b10 s33-D04 and D05: the view-button-list sits under the title, one button even for one view; no count anywhere.
- haipipe-ui rule 4: a view's sections fold by their heading, open by default, the choice kept in the browser.


## The screen, as proposed

```text
Tools-SPACE / blueprints / Project-Ladder / work / b17_theme_work                 right rail: Report · Work ·
b17_theme_work  Work                                                              Studio · Interactions ·
[Progress]                                                                        Delivery · Timeline · Files
Purpose  Design questions about the work Theme as one ladder: ...
What waits on you, then each Job and where its Tasks stand.

▾ Interactions                                                         [Answer all]
   ▸ Interactions page design            waiting for you · 2026-10-31  [Answer]
   ▸ Block Report views                  waiting for you · 2026-10-31  [Answer]
   ▸ ... one folded line per waiting form at the Block or below (ten on b17)
▾ j01_work_ladder_contract
   build what b17-s01 hands over: haipipe-work's ladder section and the work scaffold, tested on a demo Block
   makes b17-s01:theme_work @ work_ladder · planned
   ⬜ open        t01_skill_section       Write haipipe-work's ladder section
   ⬜ open        t02_scaffold            Scaffold a work Block, Job, Task and Run
   ⬜ open        t03_demo_fixture        Test the scaffold on a demo Block
▾ j02_workbench_work_skill                    (the same shape)
▾ j03_work_workbench_pages
   the work theme's three pages on the focus page, each in its three sections: ...
   makes b17-s04:theme_work @ workbench_page_structure · planned
   🙋 waits on you t01_block_page          The work Block page                    [🙋 Interaction]
   🙋 waits on you t02_job_page            The work Job page                      [🙋 Interaction]
   🙋 waits on you t03_task_page           The work Task page                     [🙋 Interaction]
▾ Its own Runs
   not sent yet   r01_collect_theme_alignment   collect · Theme alignment     [Interaction]
```

The live previews of this screen, and of every option against it, are in the form's Run folder
(`option-q1-a.html` is the whole view; `scripts/build_r03_previews.py` writes them all from disk).


## (a) The view list

```text
button     opens first   one line
Progress   yes           what waits on you, then each Job with its Tasks, then the Block's own Runs
```

One view. Its one button still shows under the title, so the Purpose line never moves (b10 s33-D04). The right-rail
item keeps its words, "its Jobs" (`focus_page.render` `describe`). Work never opens first on a Block: a Block opens
on Report (haipipe-ui, the page at each level); Work opens when its rail item or a link with `section=work` is used.

Gone from Work: the **Deliverables** view (today built when a face has `## Deliverables`), because a delivery shows
in Report by its type (s51-D01) and opens from its sNN's tags (s51-D02), and no two views repeat; and the
**Questions** block that `status_html` appends under the rows, because a work Block keeps no Questions (s51-D04).


## (b) Progress, its sections in order

Every section is a heading that folds (▾ open, ▸ folded), open by default, its state kept in the browser per page.
A section with nothing in it does not show.

### 1 · Interactions (first, orange)

- **Shows**: every form waiting for you at the Block or below (the Block's `runs/`, its Jobs' `runs/`, their Tasks'
  `runs/`), one folded line each, the waiting state word orange. Folded: its title, "waiting for you · <date>",
  Answer. Opened: asked by `<the folder that holds it>` · about `<its sNN folder>` · `<its Run name>`, then its
  questions, each with its applied flag when it has one. Then every sign still open below: a face's `**Gk:** ⬜` line,
  and a Decided line "proposed by the agent" that no one has confirmed. b17 has no sign lines today, so its section
  holds forms only: ten, the Block's `r02_collect_interactions_page` and the nine j03 view forms (`r02` to `r04` in
  `t01_block_page`, `r01` to `r03` in `t02_job_page` and in `t03_task_page`).
- **Reads**: `focus_page.interactions(<Block>, root)` kept to `state == "waiting"` (each Run's `run.yaml` `status:`,
  its `question_collection.md` `# title`, `for:` line and `## QN` cards, its form's file date); sign lines as
  `focus_draft._waits` reads them; agent-proposed lines as `focus_draft.ix_waiting` reads them.
- **Empty**: the section does not show.
- **Words and buttons**: each line, Answer (its form, in the pop-out); the heading, Answer all, when two or more wait
  and the Block's `runs/answer_all.html` exists (`collect.py bundle <Block>`), opening that one page. The line's
  look is b16's folded item (`focus_draft.ix_item`, JL 261031: interactions fold), so the same record reads the same
  on both themes.
- **Changes from today**: today only the Block's own forms lead Work (any state), and a Job's form shows only as its
  row's Interaction button. Here every waiting form leads, as you asked ("what waits on you is orange and first"),
  and the row keeps its button too. The "🙋 open points wait on you" line on a Job row goes: a form names the exact
  question, an open point is not asked yet, and it stays on its sNN's face and Studio card (form Q2).

### 2 · One section per Job

- **Order**: the Block face's `## Jobs` list when it has one (the ui-block example's has one), else folder order;
  a Job's number never moves (haipipe-job).
- **Its heading**: the Job's folder name, a link to its page. Then its goal, the first line of `goal:` in
  `jNN_<job>.md`. Then one line per sNN whose delivery this Job makes: "makes `<the sNN's label>` · `<its word>`".
  The label is the workbench's (`frame.topic_label`: `b17-s01:theme_work @ work_ladder`); it opens Report ›
  `<its type>` at that delivery, as b16 ends each Work view with "Its result: Report › …". The word is that
  delivery's current version, or planned (s51-D03, D05). A Job that makes no sNN's delivery has no makes line.
  The Job's own forms (`jNN_<job>/runs/rNN_collect_*`), when it has any, put the Interaction button on the heading.
- **Its Task lines** (form Q3): one line per Task, in the order of the Job face's `## Tasks`: its state word, its
  folder name (a link to its page), its title (the words after ` · ` on the face's first line, else its goal's first
  clause), and the Interaction button when a form sits in that Task. The state word is "🙋 waits on you" (orange)
  when a form in the Task waits, "⏳ running" when a Run card under it says running, else the face's `state:` read the
  way `focus_page.state_kind` reads it (⬜ open, ⬜ not run yet, partly done, ✅ done). No 🔶, no counts.
- **Reads**: `jNN_<job>.md` (`goal:`, `## Tasks`); each `tNN_<task>/tNN_<task>.md` (first line, `state:`); each
  `tNN_<task>/runs/*/run.yaml` (`status:`); each of the Block's own sNN's `delivery/render.yaml` (`pieces: by:`
  naming a Run under this Job, the reverse of `focus_page.work_root`); the delivery's version from its `delivery/`
  folder (none made on b17, so all read planned). The sNN that sit inside a Task (s51 to s59 in j03's) are that
  Task's own topics: they show in the Studio and on the Task's page, not on this line, which would grow to ten.
- **Empty**: a Job with no Task says "No Tasks yet." under its heading; a Block with no Job and nothing waiting says
  "No Jobs yet." in place of the whole view, as today.
- **Words and buttons**: links on the Job and Task names; Interaction where a form sits; no other verb (haipipe-ui:
  at most three, and the Job's map and tree already open from Report and from its sNN's Work tag).
- **On b17**: three sections. j01 makes s01 and lists t01 to t03; j02 makes s02 and lists t01, t02; j03 makes s04 and
  lists its three page Tasks, each "🙋 waits on you" with its 🙋 Interaction button.

### 3 · Its own Runs (last)

- **Shows** (form Q5): one line per Run in the Block's own `runs/` that is not waiting for you (a waiting form is in
  Interactions, never twice): forms not sent yet, answered forms (See answers, and each answer's applied flag), soft
  Runs `run-<type>-<target>`, hard Runs `rNN_*`. Each line: its card's state word, its Run name, its type, and for a
  form its title and its Interaction button.
- **Reads**: `<Block>/runs/*/run.yaml` (`frame.runs_of`), forms through `focus_page.interactions`.
- **Empty**: does not show.
- **On b17**: one line, "not sent yet · r01_collect_theme_alignment · collect · Theme alignment". On the ui-block
  example it would show the Block's soft Run, which Work shows nowhere today.

### The page around it (unchanged, b17-s04's)

path, title-&-section ("b17_theme_work  Work"), the view-button-list (Progress), the goal-line (Purpose), the
view-caption, then the content; left rail the siblings and this Block's sNN and Jobs; right rail the sections. On a
phone both rails hide and the sections show as one `.section-line` above the view-button-list. The view-caption
changes from "Its parts." to "What waits on you, then each Job and where its Tasks stand." (a Block's
`VIEW_WORDS["progress"]`).


## (c) What it leaves to the other cells

```text
cell or owner                  keeps
s51 Block Report               the MindMap (Jobs and Tasks as a tree, no states); deliveries by type, their
                               planned look, the tags, the version word
s53 Block Studio               the sNN cards by group; each card's stage word, its tags, its Interaction button;
                               the sNN's open points
s55 Job Work                   one Job's Tasks as full rows: goal, state, output, Runs (and a Task's life words,
                               plan · build · run · read · close, if they are agreed there)
s58 Task Work                  a Task's Runs and passes, its waiting form first, Ask the agent
s54, s57                       a Job's and a Task's Report: their results
b17-s04                        what every work page shares: path, title, rails, goal-line, phone line
r02_collect_interactions_page  the right rail's Interactions page (one page answering every form)
haipipe-interaction            the Interaction button, its pop-out list and item, the form, the bundle
Delivery, Timeline (rail)      the files handed over and their sent marks; what ran when
```


## (d) Against b16's matching cell and today's pages

```text
              b16 s33 Board Work            today b17 Work (5623)        today ui-block Work (5599)   s52 proposed
views         Idea · Story · Venue ·        Progress                     Progress                     Progress
              Data flow · Paper flow ·
              Writing (Report's list)
first         Interactions: forms, sign     the Block's own forms,       nothing                      Interactions:
              lines, agent proposals         any state                                                 waiting only
rows          Writing: a section per        a row per Job: goal, a       a row per Job: goal, a       a section per Job:
              version, its Sections as      state word, an open-points   state word                   goal, makes line,
              rows with step words          line, Interaction                                         a line per Task
end           link: Its result: Report › …  nothing                      nothing                      Its own Runs
```

The same as b16: what waits leads, in a section named Interactions, one folded line per form with Answer
(`ix_item`); a Job holds its Tasks as rows inside its own section, as b16's Writing holds one section per version with
its Sections inside; every section folds by its heading; the Interaction button sits on every row that holds one and
turns orange while a question waits.

Different from b16, and why. One view, not Report's list: b16's parts are a paper's fixed parts, one topic each, so
each Report view has its work; a work Block's Report lists deliveries by type (s51-D01), and on the ui-block page
several Jobs make no typed delivery, so a list by type would split the Jobs and hide some under no button. A work
Task line carries one state word, not b16's five step words: a work Task's steps are not a fixed five, and its full
name must show (never a bare index). Each Job has its makes line in place of one "Its result" link per view.

Against today's b17 page (5623): today the Block's own two forms lead Work whatever their state, each Job is one row
with its goal and a state word, and j03 carries "9 open topics waiting on you" (the live server is older than the
disk code, which already says "🙋 open points wait on you", no count). Proposed: only waiting forms lead, from every
level; each Job lists its Tasks; the open-points line goes; the not-sent form moves to Its own Runs.

Against today's ui-block page (5599, read for structure only): the same single Progress view, a row per Job with its
goal and a state word, no Interaction button, and its Block's own soft Run shown nowhere. Proposed: each Job's
section lists its Tasks, the Jobs that make an sNN's delivery say so, and the soft Run shows in Its own Runs.


## (e) The alternatives weighed

```text
choice          options                                                         pick  on the form
the view list   A Progress alone                                                A     Q1
                B Report's list, Skill · UI (b16's s33-D01 rule)
                C Progress, then Runs (every Run below, a running one first)
                D Progress, then Deliverables (today's code, when the face has one)   decided: no
                E one view per Job series (j0N, j2N ...)                               decided: no
what leads      A Interactions: every waiting form, folded; the open-points line goes  A  Q2
                B the Block's own forms lead; a Job's form flags its row (today)
                C A, plus every sNN's open points, one line each
                D the waiting Job's section moves to the top                            decided: no
a Job's Tasks   A every Task, one line each                                     A     Q3 (s52's red question)
                B only the next Task: the one that waits, runs or comes next
                C no Task lines: the Job's state words (today)
                D the Tasks as one line of words, like b16's step words                 decided: no
a Job's head    A its goal, then the sNN it makes with its version word        A     Q4
                B A, plus its newest result: the Run and its file
                C its goal only (today)
                D the made sNN's drawing as the row's picture                           decided: no
its own Runs    A a last section, each with its card's state                    A     Q5
                B its forms lead, any state; its soft Runs nowhere (today)
                C nowhere in Work: Interactions and Timeline list them
```

Why each pick:

1. **Progress alone** (Q1): every Job in one look is what "where things stand" needs (s52-D01). B splits the Jobs by
   the type of what they make, and a work Job may make two types or none. C repeats what a Task's Work (s58) and the
   Timeline already show, at a depth a Block does not need. D repeats the Report's type views. E needs a name for a
   series that no file holds, and each Job's section already folds.
2. **Interactions lead** (Q2): you asked for what waits on you orange and first; a form is the exact question, so it
   is the thing to lead. B keeps a Job's form out of sight until you reach its row. C adds lines for points nobody has
   asked yet, many on b17 (s04 alone has six). D breaks the plan's order, so a Job is never where you left it.
3. **Every Task** (Q3): where things stand moves here whole; the old Report › Status listed every Task under its Job
   (`status_now_html`). B hides the Tasks that are not next, so you cannot see how far a Job is; C is today's single
   word. D cannot hold five full Task names on one line.
4. **The makes line** (Q4): a Job's goal says what it builds, not which sNN receives it; the line ties Work to the
   Report's delivery in one click, and the thing itself stays in Report (s51). B adds a result line that a Job page's
   Task rows already show in place (`output_of`). D is s51's own open question for the Report row's picture.
5. **Its own Runs last** (Q5): a planned form or a soft Run is work, so it belongs in Work, but nothing in it waits on
   you, so it goes last. B keeps a not-sent form above the Jobs; C loses the soft Runs from Work entirely.

Decided by me, not asked (each follows from a decision above or from a rule):

- Deliverables and the Questions block leave Work (s51-D01, D02, D04; no two views repeat).
- The open-points line goes with Q2's pick A, and stays with B or C.
- Job order is the Block face's `## Jobs`, else folder order; no series headings.
- A delivery no Job makes shows in Report (its sNN has no Work tag), not in Work: Work lists work that exists.
- Answer all shows only when the Block's bundle page exists; nothing is bundled by the page itself.
- Add a Job (haipipe-block's Work button, `run-add-<jNN>`) waits until the host can write (b17-s04, Phase B).


## The form

`../../runs/r03_collect_block_work_views/`: five questions, one per row of (e) above that is JL's; each option
that is a screen has its own preview `option-qN-x.html`, written by `../../scripts/build_r03_previews.py` from the
faces, cards and forms on disk (rerun it, never edit a preview). The nine j03 view forms are drawn waiting, as they
will be once their agents build them today.


## The code change, named for its owner (design_b02_workbench)

Once JL answers, in `servers/workbench/focus_page.py`, never edited from here:

1. `status_html`, Block branch: Interactions first (waiting items from `interactions()`, drawn as
   `focus_draft.ix_item` draws them, moved to a shared helper); then one section per Job (heading, goal, makes
   lines, Task lines); then Its own Runs; the open-points line and the appended Questions block removed.
2. A reader for what a Job makes: every sNN whose `delivery/render.yaml` names a Run under the Job, the reverse of
   `work_root`, plus the sNN that sit inside its Tasks.
3. `render`: no `deliverables` view in a work Block's Work; the Block's caption for Progress.
4. Fold by heading for these sections, as `focus_draft` does for b16's (`section.fd-sec` and its script).
