# s53 · Block UI: Studio · the views, proposed

for: b17.j03.t01-s53:theme_work.work_workbench_pages.block_page @ block_ui_studio · written 2026-10-31 · agent work, not
agreed. JL's four choices are on the form `../../runs/r04_collect_block_studio_views/` (my picks ticked, each option
previewed by `../../scripts/build_r04_previews.py`); everything below is drawn under those picks (Q1 A, Q2 A, Q3 A,
Q4 A), and part (e) keeps every alternative.

The work Block's Studio section, verb think, on the focus page (`?path=<block>&layout=focus&section=studio`): one card
per sNN topic, the Block's own and its Jobs' and Tasks' (`frame.studio_inventory`), its groups as the view buttons.
Sample: b17_theme_work itself, twelve sNN, three at the Block and nine at j03's three Tasks.


## (a) The view list

```text
right rail        Report · Work · Studio · Interactions · Delivery · Timeline · Files      (unchanged)
Studio's views    Skill · UI   (· Other last, only while some topic has no Tags line)
opens on          the first group where a form waits for you (its button "🙋 UI", orange)
                  else the first group in _studio_groups.txt (Skill)
```

1. **Skill**: the topics that deliver a skill; on b17, s01 work_ladder and s02 work_skills.
2. **UI**: the topics that deliver a screen; on b17, s04 workbench_page_structure and s51 to s59.
3. **Other**: topics whose face names no group; shown only when one exists, always last (haipipe-ui).

A group is a name on each face's **Tags:** line (decided). On a work Block every sNN hands over one delivery of one
type (b35 s01-D02, board.md ## Deliveries), so its group is its type: `Skill`, `UI`, later `Code`, `Draft`,
`Display`, `Data` (`frame.DELIVERY_TYPES`). The Report's views are the same names (s51-D01: MindMap, then one view per
delivery type), so Report › UI and Studio › UI hold the same topics seen two ways: the Report checks what each hands
over (its current version, its planned look), the Studio thinks about it (its open question, its drawing).

Button order: `b17_theme_work/_studio_groups.txt` (`frame.studio_group_order`), then any tag the file does not list,
then Other. A group in the file with no topic gets no button; the file keeps its place. No button carries a count.


## (b) Each view and its sections

Every view has the same shape, top to bottom:

```text
view-caption     one line: what this view shows
section          one per place a topic sits: the Block itself, then each Job, then each Task, in folder order;
                 a section that holds a waiting card comes first
  card           one per topic: a card whose form waits first (orange edge), then sNN order
```

### View 1 · Skill

- **Caption**: "The topics that deliver a skill, each with its drawing, slides and mind map."
- **Section `b17_theme_work`** (heading words: `b17_theme_work`, then "this Block", muted)
  - shows: s01 work_ladder, s02 work_skills, one card each
  - reads: `b17_theme_work/s01-work-ladder/s01-work-ladder.md` and `s02-work-skills/s02-work-skills.md` (their
    **Tags:** say Skill), and each topic folder's files (the card, below)
  - empty: a group with no Block-level topic draws no such section; its first section is its first Job or Task
  - actions: the heading folds the section (▾ open by default, ▸ folded; the reader's choice kept in the browser,
    haipipe-ui rule 4)
- **One section per Job or Task holding a Skill topic**: none on b17 today (j01 and j02 hold no sNN).

### View 2 · UI

- **Caption**: "The topics that deliver a screen, each with its drawing, slides and mind map."
- **Section `b17_theme_work`** ("this Block"): s04 workbench_page_structure. Reads
  `s04-workbench-page-structure/s04-workbench-page-structure.md`.
- **Section `j03 · t01_block_page`** ("The work Block page", from the Task face's `# t01 · The work Block page`):
  s51 block_ui_report, s52 block_ui_work, s53 block_ui_studio. Reads
  `j03_work_workbench_pages/t01_block_page/s5N-*/s5N-*.md`.
- **Section `j03 · t02_job_page`** ("The work Job page"): s54 job_ui_report, s55 job_ui_work, s56 job_ui_studio.
- **Section `j03 · t03_task_page`** ("The work Task page"): s57 task_ui_report, s58 task_ui_work, s59 task_ui_studio.
- Heading actions: ▾ folds; the place's name opens that Job's or Task's own page (`?path=…/t01_block_page&layout=focus`).
- Empty: a place with no UI topic draws no section.

### View 3 · Other (only while a topic has no Tags line)

- **Caption**: "Topics with no group yet; a group is a name on the face's Tags line."
- **Sections**: by place, as above.
- Empty: the button does not show.

### The card, in every view

1. **Picture**: the lead idea slide (`sNN-<topic>.slides.json`, its first `image`, e.g. `slides/idea-01-rungs-one-shape.png`),
   else the drawing's preview `sNN-<topic>.png`, else "no picture yet"; it opens Slide, else Draw (decided, haipipe-ui
   Rows 4).
2. **Label**: `b17-s04:theme_work @ workbench_page_structure`, or for a Task's sNN
   `b17.j03.t01-s51:theme_work.work_workbench_pages.block_page @ block_ui_report` (`frame.topic_label`, b35 s01-D03);
   it opens the face in the pop-out.
3. **Stage word**: explore · shaping · agreed · closed, from **Stage:**.
4. **Type word** (**Delivery type:**): only when it differs from the open group's name; under Skill and UI it would
   repeat the button.
5. **One line** (Q3 A): the word "Open" (red, as the drawings mark open points) and the face's first numbered Open item;
   when the Open list has no numbered item (s01's is prose), the **Topic:** line's first sentence without its trailing
   ";". `code` is drawn as code.
6. **Tags**, each popping out over the page (r01 Q3, b16 r04): Slide (`sNN-<topic>.slides.html`) · Draw
   (`sNN-<topic>.excalidraw`) · Mind map (`sNN-<topic>.mindmap.md`) · Work (the Job its `delivery/render.yaml` names
   with `by:`, else the Job it sits in) · Delivery (`delivery/`) · Interaction (every collection Run whose run.yaml
   `target:` names this sNN, `focus_page.interactions`). A tag whose file is missing does not show (s51 to s59 have
   no deck yet, so no Slide).
7. **Waiting**: a card whose form waits (run.yaml `status: waiting`) has an orange edge and "🙋 Interaction"
   (interaction_button's style) and leads its section (Q4 A).
8. **Anchor** `#sNN-<topic>`: any link to an sNN (the left rail, an old `?path=…/sNN-…` link) opens this card,
   outlined, in its group (b35 s02-D05).

### Empty states and edges

- No topic at all: Studio leaves the right rail (a section with nothing in it does not show).
- A link names a group that no longer exists: the Studio opens on the first group.
- Phone (600 px or less): the rails hide, the buttons wrap, a card stacks its picture under its words (focus.css).
- Above the cards: nothing; the caption, then the first section. No "Ask the agent" bar: JL called it clutter outside a
  draft's Plan, Write and Revise steps (`focus_draft.ASK_STEPS`; JL 261031 on 4 · Display: "I don't think we need
  this"). Starting an sNN with one click is s59's open question; its answer would apply here too.


## (c) What it leaves to the other cells

- **s51 block_ui_report**: the MindMap, each delivery's one word (its current version) and its planned look (s51-D01
  to D05). The Studio card shows the stage word, never the version word.
- **s52 block_ui_work**: the Job rows and where each stands (s52-D01); a waiting form on its Job's row.
- **s54 to s56 (the Job page), s57 to s59 (the Task page)**: their own Report, Work and Studio. s56 settles whether a
  Job's Studio shows the Block's sNN it makes; s59 whether a Task's Studio has Ask the agent and a one-click new topic.
- **b17-s04 workbench_page_structure**: what every page shares: path, title-&-section, the place of the
  view-button-list, the rails, the pop-out, foldable sections.
- **haipipe-studio**: the topic folder, the label, the picture rule, the five-part drawing (`work_ui_cells.py`), and the
  group op that writes **Tags:** and `_studio_groups.txt`.
- **haipipe-interaction**: the Interaction button and its pop-out list; the right rail's Interactions section lists
  every form at this page or below.


## (d) Compared with today's pages and b16's s34

Today, b17's Studio on 5623 (read 2026-10-31):

- Buttons Skill · Interface · Navigation · Block UI · Job UI · Task UI; it opens on Skill; s04 shows under both
  Interface and Navigation (its Tags: `Interface · Navigation`).
- The button order comes from the topics' tags in topic order (`focus_page.py` line 1879, `groups =
  list(dict.fromkeys(...))`), not from `_studio_groups.txt`; the two agree today by chance. `parts_mindmap` already
  reads the file (`frame.studio_group_order`, line 1246).
- No view-caption under the buttons: the Studio branch of `render()` writes none, against haipipe-ui rule 6 ("Every
  view says what it shows in one line above its content").
- One flat list per group in sNN order, no section headings.
- The card line is the Topic's first sentence cut after its first ";" or ".", so it ends in ";" ("The Block's Studio:
  its topics by group;"); backticks show raw (s02).
- The type word sits on every card.
- A waiting form shows only on its card's Interaction button (orange since b16 r07).
- s51 to s59 have no deck, so no Slide tag, and their pictures are the same five-part template: nine thumbnails look
  alike. A lead slide per cell, or a picture cropped to each Design, would tell them apart (`work_ui_cells.py` is j03's;
  not edited here).

b16's s34 board_ui_studio, the paper Board's Studio:

- **Same**: the same code (`focus_page.studio_html`), the same card and tags, the Interaction button, no All, Other last.
- **Its groups**: Structure · Levels · Run and Skill · Guide · Block UI · Job UI · Task UI. Its own form (b16 t01
  `runs/r03_collect_board_ui_studio`, still waiting) asks "Story, Plan, Related, Ideation, then Other" or "the Block's
  own groups from _groups.txt", its pick the second.
- **Differs, the view list**: b16's Report and Work share one list, the paper's parts (s32-D04 to D06, s33-D01: "here
  the work and report should share the same view list"), with the mind map and Interactions as sections inside each
  part's view. b17's Report list is by delivery type (s51-D01), so the Studio takes the same names: b16's rule, one
  list across sections, applied to the work theme's list.
- **Differs, the sections**: a work Block rolls up its Tasks' sNN (j03 holds nine), so place headings matter more here
  than on a paper Board, whose topics mostly sit at the Board.
- **Why**: design the work theme, not the paper (s51-D06).


## (e) Alternatives weighed

1. **View list** (form Q1). A · Skill and UI, by delivery type (pick: the Report's names; s04 once; two buttons).
   B · one group per level, s04 once: Skill, Interface, Block UI, Job UI, Task UI (each view short; keeps b16's
   level groups). C · as tagged today, six, s04 twice. D · groups derived from **Delivery type:** with no Tags line
   (not asked: JL decided groups come from each face's Tags; a Tags line can still name a group that is no type).
2. **Sections in a view** (Q2). A · by where each topic sits (pick: each heading names its folder). B · one list,
   as today. C · by stage (on b17 one heading would hold nine of ten). D · a "Waits on you" section on top (not asked:
   with nine cells' forms waiting it would hold nine cards and empty the place sections).
3. **Card line** (Q3). A · the first Open item (pick: Studio thinks; the label already says what the topic is).
   B · the Topic's first sentence, as today. C · the Covers line (only the j03 cells have one; s01, s02, s04 do not).
4. **Waiting flag** (Q4). A · the group's button too, the Studio opening there, the card first (pick: what waits on
   JL is orange and first). B · the card's button only, as today. C · the group's button flagged, the Studio still
   opening on the first group (a stable landing, one more click).
5. **Opening view when nothing waits**: the first group in `_studio_groups.txt` (decided here) over the group last
   opened in this browser (two readers would land on two views; the five-second test needs one).
6. **An empty group**: no button (decided here) over a button with an empty view.
7. **The type word**: dropped when it names the open group (decided here) over always shown.
8. **The card label**: the full address (decided, b35 s01-D03) over a short `s51 @ block_ui_report` under a place
   heading.
9. **Above the cards**: nothing (decided here) over an Ask the agent bar or a "+ Topic" line (s59's question).
10. **A mind map per group on top of each view**: not taken; the Report's MindMap draws the Block's parts, and no two
    views repeat.


## The code change, named for its owner

Owner: design_b02_workbench, in `servers/workbench/focus_page.py`; this cell never edits it.

1. `render()`, Studio: buttons from `frame.studio_group_order(folder)`, then tags not listed, then `OTHER`; no button for
   an empty group; open on the first group where a card's form waits, else the first button.
2. A group button where a card's form waits reads "🙋 <group>" in `interaction_button`'s orange.
3. `studio_html()`: a view-caption per group (one line per delivery type, else "The topics tagged <group>."); one
   section per place (heading `j03 · t01_block_page` and the Task's title, ▾ folding, open by default, kept in the
   browser; its name opens that page); waiting sections and cards first; the type word only when it differs from the
   group.
4. The card line: "Open" and the face's first numbered Open item, else the Topic's first sentence without its trailing
   ";"; `code` rendered.
5. If JL keeps Q1 A: s04 and s51 to s59 retag `UI` and `_studio_groups.txt` becomes Skill, UI (the Studio's group op,
   or by hand), and s53's Decided records each answer; that is the applying Run's work (`run-design-block-page`).
