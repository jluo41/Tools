# s51 · Block UI: Report · the views proposal

written: 2026-10-31 18:56, by the s51 views agent (b17 j03, the 3 × 3)
asks JL: `../../runs/r02_collect_block_report_views/` (six questions, each option previewed; my picks ticked)
builds on: s51-D01 to s51-D06 (JL 261031, r01_collect_report_and_delivery), s52-D01

The work Block's Report section (verb: check) on the focus page (`layout=focus&section=report`), for every Block in a
Project's `work/` world: a tool Block such as b17_theme_work, and a research Block such as b11_CD_visit_pain_lbp.
Where JL has not answered yet, this file follows my pick and names the Run question that settles it (r02 Qn).

```text
b17_theme_work  Report
[MindMap] [Skill] [UI]                       ✅ view list, Q1 A
How it is built: its Jobs, what each makes, its Tasks.
root ─▶ j01 ─▶ s01 · t01 t02 t03             ✅ map by Job, Q4 A
     ─▶ j02 ─▶ s02 · t01 t02
     ─▶ j03 ─▶ s04 🙋 · t01 (s51 s52 s53) …  🙋 flags in place, Q5 A
UI view: Live pages (3 rows) ─▶ s04 row      ✅ live pages inside UI, Q1 A
a row: name · planned · For: line · tags · its planned look   Q2 C, Q6 A
```


## (a) The view list

1. **MindMap** opens first (s51-D01): how the Block is built, its Jobs, the sNN each makes, its Tasks.
2. **One view per delivery type** that the Block's own sNN carry (s51-D01, r02 Q3), named Skill, UI, Code, Draft,
   Display or Data (`frame.DELIVERY_TYPES`), in the order of the Jobs that make them; no counts on any button.
3. **Nothing else.** Status goes to Work (s52-D01); Findings, Answers and Questions go (s51-D04); Block UI, Job UI
   and Task UI become the UI view's first section, Live pages (r02 Q1).

```text
today, b17 on 5623   MindMap · Status · Findings · Answers · Questions · Block UI · Job UI · Task UI
proposed, b17        MindMap · Skill · UI
today, b11 on 5599   MindMap · Status
proposed, b11        MindMap · Data · Display        (its five sNN faces say data or display)
```

A type view shows only when one of the Block's own sNN names that `**Delivery type:**`, so a Block with no typed
sNN has MindMap alone, and the right rail's Report item stays (a Block opens on Report). The order follows the Jobs
(the first Job that makes a delivery of that type puts its type first; a type no Job makes comes last, in
`frame.DELIVERY_TYPES` order), so the buttons read like the Block's own pipeline: Skill then UI on b17, Data then
Display on b11. The right-rail line under Report changes from "read the results and check the progress" to "its map
and what it hands over", since progress now lives in Work.


## (b) Each view and its subsections

### View 1 · MindMap (opens first)

caption: "How it is built: its Jobs, what each makes, its Tasks." (replaces `VIEW_WORDS["mindmap"]`, which says
"and what each must find out": a work Block keeps no Questions)

1. **The map**: one section, no heading; drawn like the draft map (a pill, a short title, one plain paragraph box).
2. **No other section.** What waits is flagged on its node (r02 Q5); nothing is listed under the map.

The map, branch by branch (r02 Q4 A):

```text
root     the Block's folder name: b17_theme_work
level 1  each Job, in folder order: pill j01_work_ladder_contract, title "Make s01's delivery", box its goal: line
level 2  under a Job: first the sNN it makes (pill s01-work-ladder, title "work ladder", box below),
         then its Tasks (pill t01_skill_section, title, box its goal: line)
level 3  under a Task: the sNN that sit in it (s51, s52, s53 under t01_block_page), title only
last     the Block's sNN that no Job makes, one node per Studio group (_studio_groups.txt order), as today
```

1. **An sNN's box**: "<Type>, <word>." then its **Topic:** first sentence, "Delivers <For: line>", "Still open: <its
   first Open item>", with "(JL ...)" tags cut, exactly as `parts_mindmap` builds it today plus the first two words.
2. **A waiting node** (r02 Q5 A): its pill orange, followed by "🙋 waits on you"; a waiting form is a collection Run
   whose card says `status: waiting` and whose `for:` (`target:`) names the sNN.
3. **Actions**: an sNN label opens its drawing in the pop-out (✎, today's `pm-draw`); a Job or Task label opens its
   page; ▾ folds one branch; the map pans sideways, every item open (JL 261031), as today.
4. **Reads**: `board.md`; `jNN_*/jNN_*.md` (first line, `goal:`); `jNN_*/tNN_*/tNN_*.md` (first line, `goal:`);
   each `sNN-*/sNN-*.md` (first line, `**Topic:**`, `**For:**`, `**Delivery type:**`, `**Tags:**`, Open);
   `sNN-*/delivery/render.yaml` (`by:` names the Job that makes it); `sNN-*/delivery/<type>/` (the version word);
   `**/runs/r*_collect_*/run.yaml` (`status:`, `target:`).
5. **Which Job makes an sNN**: the Job folder its `delivery/render.yaml` `by:` paths start with
   (`j01_work_ladder_contract/t01_skill_section/runs/...`); else the `jNN` its `**For:**` names ("made by
   `../j01_work_ladder_contract/`"); else none, and it hangs at the end under its Studio group.
6. **Empty state**: "Nothing to map yet: no Job and no sNN." (today: "Nothing to map yet.")

### Views 2 to n · one per delivery type (b17: Skill, UI)

captions, one line each (new `VIEW_WORDS` keys):

```text
Skill     The skills it hands over, one row each.
UI        The pages it hands over, one row each; the live pages first.   (without live pages: no second clause)
Data      The data it hands over, one row each.
Display   The tables and figures it hands over, one row each.
Draft     The text it hands over, one row each.
Code      The code it hands over, one row each.
```

1. **Live pages** (UI view only, r02 Q1 A): the real work pages board.md names, one row each, before the deliveries.
2. **Deliveries**: one row per sNN of this type, the Block's own only (r02 Q3 A).
3. **No third section.** Answered forms stay behind each row's Interaction tag; status rows live in Work.

A heading shows only when a view holds two sections (UI with Live pages: "Live pages", then "Deliveries"); a view
with one section shows its rows directly. Headings fold, open by default (haipipe-ui rule 4).

**Live pages** (only on a Block whose board.md has `ui-block:`, `ui-job:` or `ui-task:`; read by
`focus_page.read_face` into `data["ui"]`, today drawn by `ui_view`):

1. **One row per line**: "Block page", "Job page", "Task page", in that order; a missing line gives no row.
2. **A row**: its name, the word "live", one line "`ui-block:` <the folder it opens>, a real page of the work theme".
3. **Its picture**: the live page small (a frame scaled down, as the interaction form shows its previews).
4. **Its action**: Open, which shows the live page full size in the pop-out (today's Block UI view, moved there).
5. **Empty state**: no ui-* line, no section; the UI view then shows its rows alone.

**Deliveries** (one row per sNN, the Studio card's shape, re-aimed at check):

1. **Picture** (r02 Q2 C): the delivery itself, small; until made, its planned look (below).
2. **Name**: its address and topic, as `frame.topic_label` prints it: `b17-s01:theme_work @ work_ladder`.
3. **One word** (s51-D05): its current version, `v2`; or `planned` (s51-D03); never its stage.
4. **One line** (r02 Q6 A): its face's `**For:**` line, up to "; made by".
5. **Tags** (s51-D02): Slide · Draw · Mind map · Work · Delivery · Interaction, each opening its pop-out.

Row details:

1. **Order**: a row that waits on you first (its Interaction tag orange, "🙋 Interaction", r02 Q5 A), then in the
   order of the Jobs that make them, then by sNN number.
2. **The version word**: the newest `-v<N>` among the files in `sNN-*/delivery/<type>/` (the thing, not the deck),
   read with `frame.version_roots` and `frame.version_label`; `planned` when that folder holds no file (a
   `delivery/` with only `render.yaml` and `deck/.gitkeep` is planned); a made file with no number reads `made`
   (haipipe-delivery asks every version to carry `-v<N>`, so a delivery saved by the rule never shows it).
3. **The planned look**: the Design part's sketch A of the sNN's own drawing (`sNN-*.excalidraw`, part 3, "A · the
   screen as proposed" in `work_ui_cells.py`), rendered once by its builder into `sNN-*.design.png`; until a
   builder writes that file, the drawing card `sNN-*.png` stands in.
4. **Once made**, the picture is the thing: ui, `delivery/ui/<piece>/index.html` in a small frame; skill, the first
   lines of `delivery/skill/<name>.md`; data, its first rows; display, the figure or the table image; draft, its first
   page render (`render/<name>-v<N>/p-1.png`); code, the first lines of its README.
5. **Tags, from what exists** (as `studio_html` today): Slide only when `sNN-*.slides.html` exists; Mind map when
   `sNN-*.mindmap.md` exists; Work when it sits in a work tree (`focus_page.work_root`); Delivery when `delivery/`
   exists; Interaction when a collection Run's `for:` names it (`focus_page.interaction_button`).
6. **Clicks**: the picture opens large in the pop-out; the name opens the face in the pop-out (as a Studio card's).
7. **Empty state**: none; a type view exists only when it has a row.

### Phone (600 px or less)

Both rails hide (haipipe-ui); each row stacks, its picture full width under its tags (`.studio-row` already does
this at 700 px); the map pans sideways; the view buttons wrap.


## (c) What this cell leaves to the other cells

1. **s52 Block Work**: where things stand (s52-D01), the full list of what waits (Q5 A leaves it there), Runs.
2. **s53 Block Studio**: sNN cards by Tags group, stage words, idea slides, talk and sketch.
3. **s54 and s57**: a Job's and a Task's own deliveries, by the same row (Q3 A puts them on their pages).
4. **b17-s04**: the path, title-&-section, rails, goal-line and phone rules every work page shares.
5. **Owners outside j03**: the focus page code (design_b02_workbench), the planned-look picture (haipipe-studio).

Whether the Block's Work shares this view list (b16 did so, s33-D01) is s52's question, not this cell's. The
right-rail sections stay with their owners: Interactions (the inbox, haipipe-interaction), Delivery (files, versions
and the sent marks in `delivery/delivery.md`, haipipe-delivery), Timeline and Files. The combined answer page for many
waiting forms (`collect.py bundle`, `runs/answer_all.html`) is haipipe-interaction's.


## (d) Compared with b16's matching cell and today's pages

```text
                    b16 s32 Board Report (paper)          b17 s51 Block Report (work)
opens on            Idea, its first part                  MindMap (s51-D01)
views               Idea · Story · Venue · Data flow ·     MindMap · one per delivery type
                    Paper flow · Draft (s32-D04 to D06)
the map             a section inside each part's view      its own first view
Status, Findings,   gone (s32-D05)                         gone (s51-D04; Status to Work, s52-D01)
Questions
a version           PDF and Word buttons per version       one word per delivery, tags open it
                    (s32-D03)                              (s51-D02, D05)
what waits          Work's views, first (s33-D01)          flagged in place; the list in Work (Q5 A)
answered forms      Interactions section per part view     behind each row's Interaction tag
```

1. **Same as b16**: no Status, Findings or Questions; one click opens a delivery; waiting work led by Work.
2. **Differs from b16**: views are delivery types, not a paper's parts; MindMap stays its own first view.
3. **Why it differs**: a paper is one delivery told in parts; a work Block hands over several separate things.
4. **Today's b17 page (5623)**: eight views; five go, three fold into UI as Live pages.
5. **Today's b11 page (5599)**: MindMap · Status becomes MindMap · Data · Display; its map already hangs one sNN per Job.

b16 moved its map inside each part's view because every part tells the same paper; a work Block's deliveries do not
share one story, so the map, which shows how the Jobs make them, earns its own first view, and JL kept it first on
r01 (17:40), after b16's r05 (17:04). b16's Report also lists the answered forms of each part as an Interactions
section; a work Block keeps its decisions on each sNN face's Decided lines, and the row's Interaction tag opens the
forms, so a second list would repeat them. b11 (read for structure only: view names and section names) shows the
rule generalises: its sNN faces carry `**Delivery type:** data` and `display`, so its Report gets Data and Display
with no change to its files.


## (e) Alternatives weighed, my pick and why

```text
choice                  options                                          pick   why
view list (r02 Q1)      live pages inside UI · kept as 3 views · gone    inside UI   they are what the UI
                                                                                    deliveries change
row picture (r02 Q2)    drawing card · first slide · the thing itself     thing   Report checks what leaves;
                                                                                    Studio shows the slide
which sNN (r02 Q3)      own only · own and every one below               own     s04 stands for s51 to s59
map level 1 (r02 Q4)    by Job · by type · by Studio group (today)       by Job  map: how; views: what
what waits (r02 Q5)     in place · plus a band · only in Work            in place   orange where you look,
                                                                                    list in Work as b16
row line (r02 Q6)       For: line · render.yaml pieces · topic line      For:    check reads what leaves
type order              Job order · fixed list · alphabetical            Job order   reads like the pipeline
rows inside a view      flat · by maker Job · by Studio tag              flat    own-only keeps it short
the one word            version · stage · render state                   version s51-D05
empty type              hidden · shown empty                             hidden  an empty place never shows
waiting band wording    one line, titles, Answer all · one row each      one line   many forms wait at once
```

1. **Live pages**: a separate view each (as today) mixes pages with types on one bar ("UI" beside "Block UI");
   dropping them loses the real page JL asked for on 261031; inside UI they sit beside the deliveries that change them.
2. **Row picture**: the drawing card shows Idea and Now (how far, which is Work's), the first slide shows the idea
   (Studio's); only the thing itself is what a check looks at, so the Report row differs from the Studio card.
3. **Which sNN**: rolled up, b17's UI view would list ten rows (s04 and s51 to s59), repeating each Task page's
   Report; own-only keeps the Block to what it hands over, and the map still shows every sNN below.
4. **Map level 1**: by type would repeat the type views (haipipe-ui: no two views repeat); by Studio group parts
   an sNN from the Job that makes it; by Job answers the map's own question, how it is built.
5. **What waits**: a band repeats Work's list on every Report view (ten titles wrap to three lines on b17 today);
   nothing at all hides it on the opening screen; flags in place show it where the reader already looks.
6. **Row line**: the pieces line is progress (built by a Run), which is Work's; the topic line is the Studio card's.
7. **Type order**: a fixed list would put Data before Skill on a tool Block; Job order matches each Block's flow.

Decided here without asking (a sensible default exists, haipipe-interaction: ask only what is the person's): type
order, rows flat, the version word's source, the empty states, the headings rule, the phone layout, the band wording.


## The code change, named for its owner (not made here)

design_b02_workbench owns `servers/workbench/focus_page.py`; this cell names the change and never edits it.

1. **`render()`**: a work Block's Report becomes MindMap plus `report_type_views(folder, root)`; no standing, findings, answers or questions keys.
2. **`report_type_views()`, new**: the Block's own sNN by `**Delivery type:**`, ordered by maker Job; each a delivery-rows view.
3. **`delivery_rows()`, new**: the row; reuses `studio_html`'s tags; adds the version word, the For: line, waiting first.
4. **`parts_mindmap()`**: no "To find out" for work; level 1 is each Job with the sNN it makes (`render.yaml` `by:`).
5. **`ui_view()`**: becomes the Live pages section of the UI view; `UI_VIEWS` stops adding three views for work Blocks.

Also, for their owners: `VIEW_WORDS` gains the type captions and the new MindMap caption; the right-rail Report
words change (`describe()`); haipipe-studio's `five_parts.py` writes `sNN-*.design.png` (the planned look); the
haipipe-ui SKILL.md Sections table (Report at a Block: "MindMap · Standing · Answers · Questions") and its rules 6 and
7 (Standing at the top of Report) follow s51-D01, s51-D04 and s52-D01 once JL answers r02.


## Files

- `result/views-proposal.md` (this cell): this proposal, written by hand
- `../scripts/build_r02_previews.py` (t01_block_page): writes the seventeen previews from b17's files
- `../runs/r02_collect_block_report_views/question_collection.md`: the six questions, my picks ticked
- `../runs/r02_collect_block_report_views/option-q1-a.html` to `option-q6-c.html`: the previews (generated)
- `../runs/r02_collect_block_report_views/r02_collect_block_report_views.html`: the form (generated by collect.py)
