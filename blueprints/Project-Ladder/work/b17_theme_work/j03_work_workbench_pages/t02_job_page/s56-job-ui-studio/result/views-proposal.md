# s56 · Job UI: Studio · the views, proposed

for: b17.j03.t02-s56:theme_work.work_workbench_pages.job_page @ job_ui_studio
written: 2026-10-31, by the agent, for JL's form
form: `../../runs/r03_collect_job_studio_views/r03_collect_job_studio_views.html` (five questions; my picks ticked)
previews: `../../runs/r03_collect_job_studio_views/option-q<N>-<k>.html`, written by `../../scripts/build_r03_previews.py`

A work Job's Studio shows the topics the Job makes: the Block sNN whose delivery it builds, its own sNN and its Tasks'
sNN. Its view buttons are their groups; inside a view, what waits for you comes first, then the topics, under a
heading for where each one sits. Picks marked "form" wait on JL; the rest the agent decided (section 6).


## 1. What a Job's Studio shows

1. **The topic it makes**: a Block sNN whose `delivery/render.yaml` has a `by:` line naming this Job (form Q1).
2. **Its own topics**: the Job's `sNN-*` folders, beside its Tasks; five at most.
3. **Its Tasks' topics**: each Task's `sNN-*` folders, three at most, in the face's `## Tasks` order.
4. **Not the Block's others**: they stay on the Block's Studio; the left rail links up (form Q2 B weighs this).

```text
b17_theme_work/
├── s01-work-ladder/               render.yaml by: j01_work_ladder_contract/...  ▶ j01 › Studio › Skill
├── s02-work-skills/               render.yaml by: j02_workbench_work_skill/...      ▶ j02 › Studio › Skill
├── s04-workbench-page-structure/  render.yaml by: j03_work_workbench_pages/...  ▶ j03 › Interface, Navigation
└── j03_work_workbench_pages/      no sNN of its own today
    ├── t01_block_page/   s51 s52 s53                                          ▶ j03 › Block UI
    ├── t02_job_page/     s54 s55 s56                                          ▶ j03 › Job UI
    └── t03_task_page/    s57 s58 s59                                          ▶ j03 › Task UI
```

The link from a Job to the topic it makes is already on disk, one way: `focus_page.work_root(topic)` reads the
sNN's `delivery/render.yaml` `by:` lines to give a card its Work tag. This proposal reads the same lines the other
way, so `j01_work_ladder_contract` finds `s01-work-ladder` and `j03_work_workbench_pages` finds
`s04-workbench-page-structure`. The topic keeps its own address (`b17-s04:theme_work @ workbench_page_structure`),
since an address is read from where the topic sits. Today none of this shows: `frame.studio_inventory` gives a Job
only its own and its Tasks' topics (plus Block topics whose face says `**At:**` that Job, which none of b17's does),
so j01 and j02 have no Studio on their rail, and j03 shows its Tasks' nine topics but not s04.


## 2. (a) The view list

1. **One button per group**: the groups the shown topics' `**Tags:**` lines name.
2. **The Block's order**: as in `b17_theme_work/_studio_groups.txt`, not first appearance.
3. **Other last**: the shown topics with no `**Tags:**` line; no All button.
4. **Topics alone**: the one button when no shown topic has a group, or none shows.
5. **Opens on**: the first group that holds the topic this Job makes; else the first button.

```text
page                           buttons, in order                                        opens on
j01_work_ladder_contract       Skill                                                    Skill
j02_workbench_work_skill           Skill                                                    Skill
j03_work_workbench_pages       Interface · Navigation · Block UI · Job UI · Task UI      Interface
j02_food (Project-Packages)    Topics (no topic: form Q5)                               Topics
```

The buttons sit under the title, as every section's view-button-list does, and carry no counts. A group no shown
topic names does not show, so a Job never shows the Block's empty groups. A topic tagged twice shows in both views,
as on the Block page today: s04 sits under Interface and under Navigation. Making, renaming or deleting a group stays
on the Block's Studio, which owns `_studio_groups.txt`; a Job page only reads the order. The right-rail item reads
"Studio · the topics it makes" (today "drawings, mind maps, slides").


## 3. (b) Each view and its sections

Every group view has one shape: a caption, then up to four sections, in this order. A section with nothing in it
does not show. Each section folds by its heading and opens unfolded (haipipe-ui rule 4's one exception).

1. **Caption**: one line, "The topics tagged <group>."
2. **Waiting for you**: orange and first; one line per waiting form, with Answer (form Q4).
3. **This Job makes**: the made topic's full card, when it is in this group (form Q1, Q3).
4. **The Job's own**: a heading `<job folder> · <title>`, its own topics in this group.
5. **Each Task**: a heading `<task folder> · <title>` per Task, its topics in this group.

```text
j03_work_workbench_pages  Studio
[Interface] [Navigation] [Block UI] [Job UI] [Task UI]
The topics tagged Interface.
🙋 WAITING FOR YOU   Interactions page design · about s04 · r02_collect_interactions_page   [Answer]
THIS JOB MAKES       b17-s04:theme_work @ workbench_page_structure  shaping  ui   🖼
                     Slide · Draw · Mind map · Work · Delivery · 🙋 Interaction
```

Each section, what it reads and when it is empty:

```text
section            shows                                   reads from disk                                empty
caption            what the view holds, one line           the group's name                               always shown
Waiting for you    a form's title, "about <sNN folder> ·   runs/r*_collect_*/ at the Block and below      not shown
                   <run>", Answer (opens the form in the   (focus_page.card_interactions): for: names
                   pop-out)                                the sNN, run.yaml status: waiting, no
                                                           result/answer_collection.md
This Job makes     the made topic's card                   the Block's sNN-*/delivery/render.yaml by:     not shown
                                                           lines that start with this Job's folder
<job> · <title>    the Job's own topics, sNN order         <job>/sNN-*/; the title from the Job face's    not shown
                                                           "# jNN · <title>" line
<task> · <title>   that Task's topics, sNN order           <job>/tNN_*/sNN-*/, Tasks in the Job face's    no heading
                                                           ## Tasks order; "# tNN · <title>"              for it
```

Every card is the Block Studio's card (s53 owns its look), four things and its tags:

1. **Picture**: the lead slide (`<sNN>.slides.json`'s first), else `<sNN>.png`, else "no picture yet".
2. **Name**: address @ topic, as `frame.topic_label` builds it; the made topic keeps its Block address.
3. **Two words**: its stage (`**Stage:**`) and its delivery type (`**Delivery type:**`).
4. **One line**: the first sentence of its `**Topic:**`.
5. **Tags**: Slide · Draw · Mind map · Work · Delivery · Interaction, each only when it exists.

The Interaction tag turns 🙋 and orange when a form about the topic waits (JL 261031, b16 r07). The made topic's
Work tag opens this Job's own Work tree in the pop-out; the name opens its face; the picture opens its slide.

Every view on today's b17 Jobs, and the empty case:

```text
page › view                  sections, in order
j01 › Skill                  This Job makes: b17-s01:theme_work @ work_ladder (explore, skill)
j02 › Skill                  This Job makes: b17-s02:theme_work @ work_skills (explore, skill)
j03 › Interface              Waiting: Interactions page design (b17/runs/r02_collect_interactions_page);
                             This Job makes: b17-s04:theme_work @ workbench_page_structure (shaping, ui)
j03 › Navigation             the same as Interface: s04 is tagged both
j03 › Block UI               Waiting: t01's forms once built (r02, r03, r04); t01_block_page · The work
                             Block page: s51 block_ui_report, s52 block_ui_work, s53 block_ui_studio
j03 › Job UI                 Waiting: r03_collect_job_studio_views (this form), r01 and r02 once built;
                             t02_job_page · The work Job page: s54, s55, s56
j03 › Task UI                Waiting: t03's r01 to r03 once built; t03_task_page · The work Task page:
                             s57, s58, s59
j02_food › Topics            one line: "No topic yet: none is made by j02_food, sits in it or in its Tasks."
```

No b17 Job shows Other today: every b17 topic has a `**Tags:**` line. A Job with its own topics shows the heading
`<job folder> · <title>` between "This Job makes" and its Tasks; Project-Packages' `b01_haipipe-toolkit/j04_skill_folder`
(four own topics, no Tags) is the real case, under one Topics button.

A topic's link from elsewhere (the left rail, an Interaction item) still opens its card on the page where it sits
(`focus_page.topic_home`): s04's on the Block's Studio. The Job page shows the same card again; the two are one
record, the same face and the same files.


## 4. (c) What it leaves to the other cells

1. **s53 Block Studio**: the card's look, the groups and their file, one group per level or not.
2. **s54 Job Report**: the delivery the Job makes, as a Report view; its preview lives there.
3. **s55 Job Work**: the Task rows, their Runs and state words; where things stand.
4. **s59 Task Studio**: a Task's own topics, Ask the agent, starting an sNN in one click.
5. **b17-s04**: the rail at every level, if Q5 A also holds for Block and Task.

The code lands in the base page, owned by design_b02_workbench; this cell names the change and never edits it:

```text
where                                    change
frame.studio_inventory (a Job)           add the Block sNN whose delivery/render.yaml by: names the Job, first
                                         (focus_page.work_root, read the other way); keep _hung_here for old **At:** faces
focus_page.render (Studio buttons)       groups in the Block's _studio_groups.txt order (frame.studio_group_order);
                                         open on the made topic's group
focus_page.studio_html                   sections in a view: Waiting for you (card_interactions, waiting only),
                                         This Job makes, the Job's own, each Task; headings with class focus-sub
focus_page.render (the rail)             Studio stays on a Job with no topic, with its one line (if Q5 A);
                                         describe("studio") on a Job: "the topics it makes"
frame.topic_address                      **At:** moves an address today; reconcile with "read from where it sits"
```


## 5. (d) Against b16's s37 and today's pages

1. **Same as s37**: a Job shows topics that belong to it, though they sit above.
2. **Link differs**: a paper topic names its version; a work topic's render.yaml names its Job.
3. **Views differ**: groups, not s37's "This version · Board"; the Block keeps its others.
4. **No Ask the agent**: s37 folds one on top; JL 261031 found it clutter elsewhere.
5. **Today's pages**: j01 and j02 show no Studio; j03 hides s04, the topic it makes.

```text
page                              views today                              made topic   sections
b16 s37 (form r03, waiting)       This version · Board                     shown        Ask the agent, then cards
b17 Block (5623)                  Skill · Interface · Navigation ·         n/a          none
                                  Block UI · Job UI · Task UI
j03 (5623)                        Block UI · Job UI · Task UI              missing      none
j01, j02 (5623)                   no Studio on the rail                    missing      n/a
the 5599 Job page (structure)     no Studio on the rail                    missing      n/a
this proposal, j03                Interface · Navigation · Block UI ·      first        Waiting, This Job makes,
                                  Job UI · Task UI                                      each Task
```

b16's version Studio asks one question, whether a version shows the topics that name it, then the Board's (its pick)
or only the Board's. The work Job answers the same need with a link that already exists: a paper topic says in its
face which version it is about, while a work topic's `delivery/render.yaml` names the Job whose Runs build its
delivery, and `work_root` reads it today. The views differ on purpose: JL's rule makes a Studio's groups its view
buttons (from each face's Tags), so the Job page reuses the Block page's buttons instead of a new "This Job · Block"
pair, and the Block's other topics stay on the Block page, one click up the left rail. JL's b16 note on the version's
Work (s36-D02: "for each job's view button, later we can make them to be the studio as well") is kept as form Q2 C,
not picked now, since he said "that can be later". b16's s32-D06 (the mind map and Interactions are sections inside
each view, not views) is the model for Waiting for you: a section inside each Studio view. The one Interaction
button, 🙋 and orange when a form waits (b16 t01 r04 Q3 to Q6, r07), stays on every card.

The page that today's s56 drawing proposes (`work_ui_cells.job_studio`) has the views "This Job · Block", the made
card, "No sNN sits at j01 yet" and Ask the agent. This proposal keeps the made card and drops the other three:
groups replace "This Job · Block" (still offered as form Q2 B), the empty line moves to a Job with no topic at all
(form Q5), and Ask the agent stays with the Task (s59). The 5599 Job page (`ui-job:` in board.md) was read for its
structure only: its rail has no Studio, while its left rail lists Block sNN whose names carry that Job's id, the
same gap j01 has.


## 6. (e) Alternatives weighed, and the picks

1. **Which topics**: made, own and Tasks'; not today's own-only, nor the Block's all.
2. **The link**: render.yaml `by:`; not a face's prose, nor `**At:**`, which moves the address.
3. **Made topic**: its full card first (form Q1 A); a line, or hidden, weighed.
4. **View list**: groups (form Q2 A); This Job · Block, or one view per Task, weighed.
5. **Inside a view**: headings by place (form Q3 A); a flat list weighed.

```text
choice                  pick                                 weighed and set aside                          who
which topics            made + own + Tasks'                  own + Tasks' (today); + the Block's others;    agent
                                                             the made one only
the link                render.yaml by:                      **For:** "made by" (prose); **At:** j01        agent
                                                             (moves the address); the Job goal's words
made topic              full card, "This Job makes"          one line to the Block; not shown               form Q1
view list               groups, the Block's order            This Job · Block; Makes + one per Task;        form Q2
                                                             one Topics view (ten cards on j03)
group order             _studio_groups.txt                   first appearance (today)                       agent
opens on                the made topic's group               first button; the group with a waiting form    agent
inside a view           headings by where each sits          one flat list; headings by stage               form Q3
what waits              a line on top, Answer                the card's button only; the waiting card       form Q4
                                                             first (moves nothing when all wait)
no topic                Studio stays, one line               Studio leaves the rail (today)                 form Q5
Ask the agent           none on a Job                        a Copy prompt line at the end                  agent
two groups              shown in both                        the first group only                           agent
Task heading            folder · title                       folder only; title only                        agent
```

The agent's own picks follow rules already set: the group order and the two-group duplication follow the Block page,
so a reader who knows the Block's Studio knows the Job's; opening on the made topic's group shows first what the Job
exists for; no Ask the agent on a Job follows JL 261031 on 4 · Display ("I don't think we need this") and leaves the
prompt with the Task's s59; a heading carries the folder's real name, then its face's title, so it reads both ways.
"One Topics view" was set aside because j03 would scroll through ten cards; "the waiting card first" was set aside
because on j03 every topic will have a waiting form at once, so nothing would move. The form asks only what changes
what JL sees: whether the made topic shows (the red open question), the buttons, the headings, where waiting shows,
and the empty Job.
