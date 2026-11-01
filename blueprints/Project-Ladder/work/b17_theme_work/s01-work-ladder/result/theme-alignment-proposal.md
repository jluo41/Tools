# b17 theme alignment · proposal

for: b17-s01:theme_work @ work_ladder · its form: `../../runs/r01_collect_theme_alignment/` · written 2026-10-31 18:58

JL 261031: "I want you compare to others, like the theme_paper to update the theme_work as well".

This file compares b17_theme_work with b16_theme_paper (the model), b11_theme_insight and b12_theme_design, and
lightly with b10_project_workbench and b13 to b15, then proposes how b17 changes. It is a proposal only: nothing is
created, renamed or moved until JL answers the form. Words used below:

- **sNN**: a Studio topic, the folder `sNN-<topic>/` beside the Jobs or Tasks it serves; its face is `sNN-<topic>.md`.
- **band**: the number range haipipe-studio gives a kind of topic (`ref/topic-contract.md` § Numbering): s01-s09
  concepts, s11-s19 levels, s21-s29 runs and skills, s31-s39 Guide, s41-s49 Task procedures, s51-s59 server, s61-s69
  slide drafts.
- **group**: a Studio view button; a topic's groups are its face's `**Tags:**` line; `_studio_groups.txt` keeps the
  Block's groups in order.
- **face key**: a `key: value` line at the top of `board.md` (`spine:`, `ui-block:`, ...).
- **collection Run** (a form): `runs/rNN_collect_<slug>/`, a set of questions for JL with its answers (haipipe-interaction);
  its `for:` line is the address of the sNN it belongs to, and the workbench shows it on that sNN's card.


## 0 · The answer in short

1. **Keep**: s01, s04 and s51 to s59 keep their numbers; Skill group, Jobs j01 to j03 stay.
2. **Renumber**: s02-work-skills becomes s21-work-run-skill, skills and Runs together, as b16's s21.
3. **Add**: s31-work-guide, the work Guide by level, made by a new j04_work_guide.
4. **Regroup**: the bar becomes Skill, Levels, Guide, Block UI, Job UI, Task UI.
5. **Clean**: two face keys and the Questions go; four reports fold into their topics.

```text
group bar   b16 today   Structure · Levels · Run and Skill · Guide · Block UI · Job UI · Task UI
            b17 today   Skill · Interface · Navigation · Block UI · Job UI · Task UI
            b17 after   Skill · Levels · Guide · Block UI · Job UI · Task UI          (Q1 A)
topics      b17 today   s01 s02 s04 | s51-s59
            b17 after   s01 s21 s04 s31 | s51-s59                                   (Q2 A, Q3 A, Q4 A)
```

The one place b17 does not copy b16 on purpose is the Skill group: JL set it on 261031 ("Skill is now its own
Studio group, holding the topics that deliver skills"), so b16's Structure and Run and Skill fold into it for b17.
Everything else takes b16's name where b17 has the same kind of topic.


## 1 · What was read

- Faces: every `board.md` of b10 to b17; every sNN face of b10 to b17 (their Tags, Stage, For, Delivery type,
  Covers, Excluded, At, Feeds lines); `_studio_groups.txt` of b10, b16, b17; b16's and b17's `HANDOFF.md`.
- Folders: each Block's `goals/`, `runs/`, `related/`, `delivery/`, `reports/`, `_archive/`, its Jobs and Tasks.
- Forms: the answers of b16's Block Runs r01 to r06 (r03: the UI split into Block UI, Job UI, Task UI) and of b16
  j01 t01's r01, r04 to r07 (none decides a Studio group); b17 j03 t01 r01's answers (JL 261031, s51-D01 to D06);
  the cards of every b17 collection Run.
- Live pages on 5623 (Studio, Report and Work of b10 to b17), read with curl.
- Code: `servers/workbench/focus_page.py` (`read_face`, `home_section`, `render`, `studio_html`), `frame.py`
  (`_note_facts`, `topic_label`, `studio_inventory`, `studio_group_order`), `haipipe-studio/scripts/new_topic.py`
  (`face_text`, `BANDS`, `LIMITS`), `haipipe-studio/SKILL.md` and `ref/topic-contract.md`, `haipipe-run/SKILL.md`,
  `2_theme/work/haipipe-work/SKILL.md`, `servers/workbench-work/guide/guide.yaml` and `guide/method.md`.


## 2 · Side by side

### 2.1 · Face keys (`board.md`, top lines)

```text
key                 b10  b11  b12  b13  b14  b15  b16  b17
board-kind           x    x    x    x    x    x    x    x
package              -    x    x    x    x    x    x    x
theme                -    x    x    x    x    x    x    x
ui-block, ui-job     -    x    x    x    x    x    x    x
ui-task              -    x    x    -    x    x    x    x
shared-blueprint     -    x    x    x    x    x    x    x
spine, close         x    x    x    x    x    x    x    x
session              x    x    x    x    x    x    x    x
home-section         -    -    -    -    -    -    -    x     only b17: overview-report
overview-map         -    -    -    -    -    -    -    x     only b17: s04's result/b17-overview.mindmap.md
```

What the two b17-only keys do on the live page (`focus_page.home_section`, `overview_report_html`): `home-section:
overview-report` turns the Report's Findings into s04's old hand-made map (an iframe of
`s04-workbench-page-structure/result/b17-overview.mindmap.md`) and adds an **Answers** view. That is why b17's Report
today shows `MindMap · Status · Findings · Answers · Questions · Block UI · Job UI · Task UI`, one view more than
b16, b11 and b12 (`MindMap · Status · Findings · Questions · Block UI · Job UI · Task UI`). JL removed Findings,
Answers and Questions on 261031 (s51-D04, r01 Q5: "we will not have the questions"), so the two keys only feed views
that are going.

### 2.2 · Face sections

```text
section                b10  b11  b12  b13  b14  b15  b16  b17
## Topic                x    x    x    x    x    x    x    x
## Pipeline             x    x    x    x    x    x    x    x
## Deliveries           -    -    -    -    -    -    -    x     only b17; haipipe-studio asks every Block for it
## Pages                x    x    -    x    x    x    x    x
## Questions            x    x    x    x    x    x    x    x     b17's go (s51-D04)
## Related resources    x    x    -    x    x    x    x    x
## Renumbered (date)    x    -    -    -    -    -    x    -     b17 merged s03 and s32 on 261031 but wrote no note
## Blueprint home       -    x    x    x    x    x    x    x
other                                    Implementation plan, Slides (b15)
```

b17's `## Topic` and `## Pipeline` still describe the older ladder: `tasks/bNN_<topic>/`, "four Spaces (Scope · Task ·
Check · Delivery)", "the same six Spaces: Description · Idea Studio · Audience Report | Work Details | Runs ·
Delivery", "chat section -> Related question -> haipipe-report -> report Page". b16's were rewritten on 261011 for the
frame of that day. Neither says what the focus page shows today (Report · Work · Studio · Interactions · Delivery ·
Timeline · Files).

### 2.3 · Studio groups (the live bar on 5623)

```text
b10  Structure · UI · Report · Run and Skill · Guide · Server · Other
b11  Topics (no topic has a Tags line, so one button)
b12  Topics (the same)
b13  Topics (the same)
b14  Topics (the same)
b15  concept · labeling · Levels · Other
b16  Structure · Levels · Run and Skill · Guide · Block UI · Job UI · Task UI
b17  Skill · Interface · Navigation · Block UI · Job UI · Task UI
```

b17's Interface and Navigation each hold one topic, the same one (s04, `**Tags:** Interface · Navigation`), so two
buttons open the same card. b16's groups follow its bands (Structure = s01-s05, Levels = s11-s13, Run and Skill =
s21, Guide = s31), then its UI cells by level.

### 2.4 · Topics by band

```text
band                       b11               b12               b16                    b17 today
s01-s09  concepts          s01 s02 s03 s04   s01 s02 s03 s04   s01 s02 s03 s04 s05    s01 s02 s04
s11-s19  levels            s11 s12 s13       s11 s12 s13       s11 s12 s13            -
s21-s29  runs and skills   s21               s21               s21                    -  (s02 holds skills)
s31-s39  Guide (and UI)    s31 s32 s33       s31 s32 s33       s31 + s32-s40 (cells)  -
s51-s59  server            -                 -                 -                      s51-s59 (cells)
s61-s69  slide drafts      s61               s61               -                      -
Block-level topics         12                12                10                     3
(cap: 9 at a Block)
```

The numbers that mean the same thing in every theme Block: s01 the ladder (b11 to b17), s11 to s13 the three levels
(b11, b12, b16), s21 Run and skill (b11, b12, b16), s31 the Guide (b10, b11, b12, b16), s32 the element gallery (b10
to b15), s61 the slides (b11, b12). s02 to s05 mean different things in each Block: "the workbench today" in b11 to
b15, the Studio, Delivery, Related and Report views in b16 and b10. b17 matches only s01 today. Its old s03 (the
workbench today) and s32 (the element gallery) were merged into s04 on 261031 (s04-D02, JL agreed the b17 plan), so
those two numbers are retired in b17.

Over the cap of 9: b16 (10), b11 (12), b12 (12), b10 (17). b17's 3 leave room for six more.

### 2.5 · Topic face lines

```text
line                 b16 Block topics            b16 cells    b17 s01 s02 s04                       b17 cells
**Tags:**            `Structure` and so on      `Block UI`   `Skill`; s04: Interface · Navigation  `Block UI`
**Stage:**           x                           x            x                                     x
**For:** ... reader  "for the people who ..."    x            no reader; ends "made by ../jNN/"     x
**Delivery type:**   x                           x            x                                     x
**Covers:**          -                           x            -                                     x
**Excluded:**        -                           x            -                                     x
**At:**              -                           -            "b17" (s01 s02 s04)                   -
**Feeds:**           reports/ qNN                q01          reports/ qNN                          "none: a work Block keeps no Questions"
```

`**At:** b17` does nothing at Block level: `frame._note_facts` reads an At of `b\d+` as empty. It is left from b35
s01-D05 (one studio/ per Block, each topic naming its rung); topics now sit beside their Jobs, so the folder already
says where. `new_topic.py face_text` writes Covers and Excluded for every new face, and haipipe-studio's "One delivery"
rule asks a For line to name "who it is for"; b17's three Block topics and b16's ten miss Covers and Excluded.

### 2.6 · Folders

```text
folder or file            b10  b11  b12  b13  b14  b15  b16  b17
HANDOFF.md                 -    -    -    x    x    x    x    x     b16's and b17's both still say studio/ and six Spaces
_studio_groups.txt         x    -    -    -    -    -    x    x
goals/                     -    x    x    -    -    -    x    -     b16: g03 (retired 261010), g04 (ran 261007)
runs/ at the Block         x    -    -    -    -    -    x    x     b17: r01 (this form), r02 (Interactions page)
related/                   x    x    x    -    -    -    -    -     b11, b12: one meeting row each
delivery/ at the Block     -    x    x    -    -    -    -    -     b11, b12: <theme>-slides/ written by their s61
reports/                   x    x    x    x    x    x    x    x
_archive/                  -    -    -    -    -    -    x    -     b17 keeps old work in j03/_old/, s04/result/merged-*
src/                       -    -    -    -    -    -    -    new   this Run's preview script
```

### 2.7 · Jobs

```text
b16   j01_paper_workbench_pages    t01_board_page · t02_version_page · t03_section_page; three cells each (s32-s40)
b17   j01_work_ladder_contract     makes s01's delivery: t01_skill_section · t02_scaffold · t03_demo_fixture
      j02_work_skill_homes         makes s02's delivery: t01_skill_homes_table · t02_move_list_b04
      j03_work_workbench_pages     t01_block_page · t02_job_page · t03_task_page; three cells each (s51-s59)
b10 to b15                         no Jobs
```

b17 gives every Block-level topic a Job that makes its delivery (b35 s01-D14, 261031); b16 makes only its UI that
way and runs its skill plan from a goal prompt (`goals/g04-paper-skills.md`). b17's Jobs and Tasks carry
`answers: Q01,Q02,Q03` (j01, j03) and `answers: Q04` (j02), which point at the Questions that are going.


## 3 · What b17 lacks, and what only b17 has

### 3.1 · Lacks

1. **s21 Run and skill**: b11, b12, b16 have one; no b17 topic names the work Run types.
2. **s31 Guide**: b10, b11, b12, b16 have one; the work Guide still teaches Questions.
3. **s11 to s13 Levels**: b11, b12, b16; in b17, j03's three Tasks are the levels.
4. **s61 Slides**: b11, b12; every sNN already has its own deck; b16 has none.
5. **A Renumbered note**: b10, b16; b17's 261031 merges sit inside `## Deliveries`.

The rest of what b16 has and b17 lacks is left out on purpose (§ 5): goals/, related/, a Block delivery/, s02 to
s05 for the Studio, Delivery, Related and Report views, s32 (merged into s04).

The Guide is a real gap, not a copy. `servers/workbench-work/guide/guide.yaml` still says "The Task Workbench reads
one Task Block: its Jobs, Tasks and Runs, and the Questions they answer" and lists Scope, Task, Check and Delivery;
`guide/method.md`'s eight steps start with "1 · Ask the Question" and end with "8 · Check and deliver" a report.
None of that holds after s51-D04, and the focus page has no Guide at all (s04 Open 3 asks where it goes).

The Run types are a real gap too. `haipipe-run/SKILL.md`'s "Run types by Space" and its `ref/run-types-by-space.md`
still list the six Spaces' buttons, among them `Audience Report · Ask · haipipe-report · run-ask-<qNN>`. The focus
page's work Runs (hard `rNN_` tickets, soft `run-<type>-<target>`, collection `rNN_collect_<slug>`, the Tasks'
`run-design-<level>-page`) have no table that says which button makes which Run and which skill owns it.

### 3.2 · Only b17

1. **`home-section`, `overview-map`**: feed Findings and Answers, both removed by s51-D04; drop them.
2. **`## Deliveries`**: haipipe-studio asks every Block for it; keep it; b16 lacks it.
3. **`**At:** b17`**: does nothing at Block level; drop it from s01, s02, s04.
4. **A Job per delivery**: j01, j02 make s01's and s02's; keep; it replaces goal prompts.
5. **Skill group**: JL's choice of 261031; keep it.


## 4 · The proposal

### 4.1 · Studio groups (Q1, pick A)

```text
_studio_groups.txt    Skill · Levels · Guide · Block UI · Job UI · Task UI
Skill                 s01-work-ladder · s21-work-run-skill        delivery type skill
Levels                s04-workbench-page-structure                ui, what every work page shares
Guide                 s31-work-guide                              ui
Block UI · Job UI · Task UI    s51-s53 · s54-s56 · s57-s59        unchanged
```

Each face's `**Tags:**` line, with backticks as b16 writes them: s01 `` `Skill` ``, s21 `` `Skill` ``, s04
`` `Levels` `` (was `Interface · Navigation`), s31 `` `Guide` ``. The focus page draws the bar in the order the topics'
folders sort (`studio_inventory`, then the first time each tag appears), not from `_studio_groups.txt`, which only
the MindMap reads; with these tags both give the same order.

Why Levels for s04: b16's Levels group holds the topics about each level's whole page (s11 to s13); s04 is the work
topic about all three pages and what they share, the parent of the nine cells. Option B (Skill, UI, then the three
UI groups) groups strictly by delivery type, as the Report does (s51-D01), with s04 and s31 under UI; it is the
honest second choice. Option C keeps today's bar; s31 would then fall into Other.

### 4.2 · s21-work-run-skill (Q2, pick A: s02 widens and moves)

```text
number          s21 (was s02; s02 retired)
folder          s21-work-run-skill/
title           s21 · work Run and skill
Tags            `Skill`
Stage           explore
Delivery type   skill
For             a deck, and every work Run type at Block, Job and Task, the skill behind it, each skill's
                home, and the plan to update those skills, for the people who write the toolkit skills;
                made by `../j02_work_skill_homes/`
Covers          the Runs each work page's buttons make (hard rNN_ tickets, soft run-<type>-<target>,
                collection rNN_collect_<slug>), the skill that owns each, which 1_base/task skills move to
                2_theme/work, the order of the skill updates
Excluded        what each level's folder holds (s01); the screens (s04, s51-s59); the file moves themselves
                (b04, b01 j04_skill_folder)
Topic           every work Run type and the skill behind it, and which of today's skills/1_base/task skills
                make the work theme (skills/2_theme/work) and which stay in base (JL 261007), in b16's s21 shape
Feeds           none: a work Block keeps no Questions (JL 261031, r01 Q5)
Decided         s21-D01 (was s02-D01, its text unchanged)
its Job         j02_work_skill_homes, which gains t03_run_types_table · Write the Run types table
                (soft Run run-write-run-types-table); render.yaml gains the piece
                "run-types-table: haipipe-work SKILL.md's Run types table"
```

What the move touches, every file:

1. `s02-work-skills/` becomes `s21-work-run-skill/`: its face (title, `s02-D01` to `s21-D01`), `.excalidraw`, `.png`,
   `.mindmap.md` (refreshed from the face), `.ideas.md`, `.slides.json`, `slides/` (the pictures keep their names),
   `delivery/render.yaml` (its comment line; the pieces' `by:` paths stay, since j02 keeps its name), `delivery/deck/`.
   Generated, rebuilt not edited: `.mindmap.html`, `.slides.html`, `.slides.pptx`, `.s02-work-skills.seed.json`
   (becomes `.s21-work-run-skill.seed.json` on the redraw). Kept whole, as s04 keeps `merged-s03-work-workbench/`
   whole: `result/first-drawing-builder/build_s02_work_skills.py`, `result/first-drawing.excalidraw`.
2. `board.md`: `## Deliveries` (the s02 line), `## Pages`, a new `## Renumbered (261031)`.
3. `j02_work_skill_homes/j02_work_skill_homes.md`: its title "Make s02's delivery", `goal:`, `close:`, its Topic's
   address `b17-s02:theme_work @ work_skills`, and the new Task line.
4. `j02_work_skill_homes/t01_skill_homes_table/t01_skill_homes_table.md` and its
   `runs/run-write-skill-homes-table/run-write-skill-homes-table.md`: the `close:` line names `s02's delivery/`.
5. `j02_work_skill_homes/t02_move_list_b04/t02_move_list_b04.md`: "Part of j02 · Make s02's delivery".
6. `j03_work_workbench_pages/work_ui_cells.py` lines 100 and 111 (`b17-s02 · Skill homes`, `makes s02`), then
   rerun the cells it draws.
7. `s04-workbench-page-structure/build_s04_workbench_page_structure.py` line 112 (`"j02": "s02 skill"`), then rerun it.
8. Outside b17, for their owners: `Project-Packages/work/b01_haipipe-toolkit/j04_skill_folder/s01-skill-folder-changes/`
   face line 44 and its mind map line 39 (that path, `../../b17_theme_work/s02-work-skills/`, is already wrong today:
   from b01 it never reaches Project-Ladder); `Project-PageParts/work/b35_studio/s04-delivery-gallery/delivery/skill/gallery.md`
   (GENERATED by `haipipe-studio/scripts/gallery_scan.py --write`: rerun it).
9. Not touched: no collection Run names s02; closed Results that mention s02 (j03 t01 r01's previews) keep it.

Option B keeps s02 as it is and adds a new s21 for the Run types only, with its own Job (`j04_work_run_types`: t01
run types table, t02 skill update plan); two topics, two deliveries of the same type, and s02 keeps a number that
means "the workbench today" in b11 to b15. Option C adds nothing and leaves the Run types to no topic.

### 4.3 · s31-work-guide (Q3, pick A)

```text
number          s31 (never used in b17)
folder          s31-work-guide/
title           s31 · work Guide
Tags            `Guide`
Stage           explore
Delivery type   ui
For             a deck, and the work workbench's Guide, its steps cut by level (Block, Job, Task), for the
                people who build the workbench; made by `../j04_work_guide/`
Covers          the Guide's steps at each level with deliveries in place of Questions; the files it reads
                (servers/workbench-work/guide/guide.yaml, guide/method.md, guide/methods/); where the Guide
                opens on the focus page (moved here from s04 Open 3)
Excluded        each page's sections (s51-s59); the Run behind each step's button (s21)
Topic           the work Guide, rewritten for the focus page one level at a time: today it still teaches Ask
                the Question and Scope, Task, Check, Delivery (b16's s31 shape)
Feeds           none: a work Block keeps no Questions (JL 261031, r01 Q5)
its Job         j04_work_guide (new)
```

The new Job's face:

```text
# j04 · Make s31's delivery

goal: build what b17-s31 hands over: the work Guide's text, cut by level, and its place on the focus page
close: every Task's Runs are done and b17-s31 is agreed

## Topic
From b17-s31:theme_work @ work_guide: the Studio decides what the work Guide says at Block, Job and Task and where
it opens; this Job writes it into servers/workbench-work/guide/ and names the page change for design_b02_workbench.

## Tasks
1. t01_guide_text · Rewrite the work Guide by level        (soft Run run-write-guide-text)
2. t02_guide_place · Name where the Guide opens            (soft Run run-name-guide-place)
```

s31's `delivery/render.yaml`: `guide-text: servers/workbench-work/guide/guide.yaml and guide/method.md` by
`j04_work_guide/t01_guide_text/runs/run-write-guide-text`; `guide-place: the focus page's Guide` by
`j04_work_guide/t02_guide_place/runs/run-name-guide-place`. s04's Open 3 then says "where Guide appears: s31".

The options not picked, carded so JL can see them whole:

```text
Q3 B  s11-work-block · s12-work-job · s13-work-task     Tags `Levels` · ui · explore
      For   a deck, and the work Block's (Job's, Task's) page as a whole, its Report, Work and Studio with what
            is on disk under each, for the people who build the workbench; made by ../j03_work_workbench_pages/
      cost  each repeats its j03 Task face and its three cells; the Block holds 7 topics
Q3 C  s61-work-slides                                     Tags `Slides` · display · explore
      For   a deck, and the slides that explain the work theme on the ladder, for people new to the toolkit
      cost  every sNN already ends in its own deck; b16 has no s61; no Job (its deck is its own delivery/)
Q3 D  no new topic; the Guide waits on s04's Open 3
```

### 4.4 · The UI cell numbers (Q4, pick A: keep s51 to s59)

The nine cells keep s51 to s59. Two facts decide it. Nine collection Runs (j03 t01 r02 to r04, t02 r01 to r03, t03
r01 to r03) carry `for: b17.j03.t0N-s5N:...` and are being written now; once one is answered, its answer file keeps
that address for good, and the workbench finds a form's card by that address. And s32, where b16's cells start, is a
retired number in b17 (merged into s04 on 261031); haipipe-studio reuses a number only when a person asks for it back.

What B (s32 to s40, as b16) would touch:

1. Nine folders: t01 `s51-block-ui-report` to `s32-block-ui-report`, `s52-block-ui-work` to `s33-block-ui-work`,
   `s53-block-ui-studio` to `s34-block-ui-studio`; t02 s54, s55, s56 to s35, s36, s37 (job-ui-report, -work,
   -studio); t03 s57, s58, s59 to s38, s39, s40 (task-ui-report, -work, -studio). In each: the face (title, its
   Decided ids, s51-D01 to D06 among them), `build_sNN_*.py`, the drawing, its card, the mind map (rebuilt), `delivery/`,
   `result/views-proposal.md`.
2. `j03_work_workbench_pages/work_ui_cells.py`, `j03_work_workbench_pages.md` (its 3 × 3 sketch), the three Task
   faces (their `close:` lines name the cells).
3. The nine collection Runs: `run.yaml` `target:`, `question_collection.md` `for:`, a rebuild of each form (a new
   stamp), each Task's preview script.
4. `board.md` (`## Deliveries`), s04's face (a new decision line beside s04-D04, which says s51 to s59).
5. Generated: `b35_studio/s05-studio-gallery/delivery/skill/gallery.md` (rerun `gallery_scan.py`).

The band table is the one loose end of A: haipipe-studio names s51-s59 "server" (b10's s51, s52 are server topics).
That is listed for haipipe-studio's owner (§ 6), not changed here.

### 4.5 · `board.md`, line by line

```text
key or section          today                                          proposed
home-section            overview-report                                gone
overview-map            s04-.../result/b17-overview.mindmap.md         gone (the map stays in s04's result/)
spine                   "Design questions about the work Theme ..."    see below
close                   "Each recorded question has a report Page ..." see below
ui-block, ui-job, ui-task, package, theme, shared-blueprint, session   unchanged
## Topic                tasks/bNN, four Spaces, six Spaces, Questions   see below
## Pipeline             ... -> haipipe-report -> report Page           see below
## Deliveries           s01, s02, s04, s51-s59, the merge note         s01, s21, s04, s31, s51-s59; the merge note moves
## Pages                s01 and s04 only, the old drawing notes         one table, as b16's (below)
## Questions            Q01 to Q04                                     gone (s51-D04)
## Related resources    two rows, each with questions: Q01..Q03        the rows stay; questions: go; first url fixed
## Renumbered (261031)  -                                              new (below)
## Blueprint home       as b16                                         unchanged
```

Proposed lines:

```text
spine: The work Theme as one ladder: what a work Block, a work Job, a work Task and a hard Run each hold and show,
  handed over as skill pieces in haipipe-work and as the work pages of the focus page.
close: Every sNN is agreed and its Job has made its delivery: each skill piece rendered into its SKILL.md, each
  page's code change named for its owner (design_b02_workbench).
```

`## Topic`, proposed:

> The work Theme runs bounded execution work: a Task plans, builds, executes and reports, and each Run is one hard
> ticket (`rNN_<noun>_<qualifier>.sh`) with its Result and receipt. Its Block is `work/bNN_<topic>/`, a Job groups
> Tasks by series (j0N, j1N, j5N), and a work Block keeps no Questions (JL 261031, s51-D04): its page reports what it
> hands over, one view per delivery type.
>
> On the focus page (`layout=focus`) every level has the same sections, each with one verb: Report checks, Work does,
> Studio thinks, then Interactions, Delivery, Timeline and Files (haipipe-ui). This Block designs how work fills them
> at Block, Job and Task (j03's 3 × 3, s51 to s59), and what the work skills say: the ladder (s01), the skills and Runs
> (s21), the Guide (s31).
>
> Most answers here are a change to the work skills (`2_theme/work/haipipe-work`, `workbench-work`, the Task skills in
> `1_base/task`) or to the base page (`servers/workbench/focus_page.py`, owned by design_b02_workbench), not a Task
> Run. Excluded: the ladder itself and what every Theme shares (b10_project_workbench); the stage pipelines a Task
> runs (haipipe-data, -nn, -end).

`## Pipeline`, proposed:

```text
chat ─▶ sNN (face, drawing, Decided, its form) ─▶ its Job's Tasks and Runs ─▶ the sNN's delivery/
     ─▶ render_delivery.py into a SKILL.md, or the Task's code change for its owner
```

`## Pages`, proposed (b16's table, without its Q column):

```text
group     topic                           holds                                              stage    made by
Skill     s01-work-ladder                 what each work level's folder holds; the scaffold  explore  j01
Skill     s21-work-run-skill              every work Run type, its skill, each skill's home  explore  j02
Levels    s04-workbench-page-structure    what every work page shares                        shaping  j03
Guide     s31-work-guide                  the work Guide, cut by level                       explore  j04
Block UI  s51 · s52 · s53 (j03 t01)       the Block's Report, Work and Studio                explore  j03
Job UI    s54 · s55 · s56 (j03 t02)       a Job's Report, Work and Studio                    explore  j03
Task UI   s57 · s58 · s59 (j03 t03)       a Task's Report, Work and Studio                   explore  j03
```

`## Renumbered (261031)`, new:

```text
studio topic                     was
s04-workbench-page-structure     + s03-work-workbench and s32-work-element-ui, merged; kept whole in its
                                   result/merged-*; s03 and s32 retired (s04-D02)
s21-work-run-skill               s02-work-skills; s02-D01 is s21-D01; s02 retired
reports/ q01 to q04              folded into the topics they fed, result/merged-qNN-*/ (s51-D04)
```

`## Related resources`: the first url, `.../skills/2_theme/../1_base/task`, becomes `.../skills/1_base/task`.

### 4.6 · The topic faces

```text
face   change
s01    **For:** gains ", for the people who write the toolkit skills" before "; made by ../j01_work_ladder_contract/"
       **At:** b17 goes; **Covers:** and **Excluded:** are added; **Feeds:** says none (JL 261031, r01 Q5)
       **Covers:** what each work level's folder holds (Block, Job, Task, Run), the scaffold, its test on a demo Block
       **Excluded:** the skills and Runs (s21); the pages (s04, s51-s59); the ladder every theme shares (b10 s01)
       its Files list gains result/merged-q01-work-ladder/
s21    as § 4.2
s04    **Tags:** `Levels`; **For:** gains ", for the people who build the workbench"; **At:** goes
       **Covers:** what every work page shares: the path, the Purpose, the right rail's sections, the left
       rail, one item per row; **Excluded:** each section of each level (s51-s59); the Guide (s31)
       **Feeds:** says none; Open 3 says the Guide's place moved to s31
       its Files list gains result/merged-q02-plan-build-execute-report/, result/merged-q03-questions-and-runs/
s31    as § 4.3
cells  unchanged (they already follow b16's cells)
```

s01's `**Topic:**` still describes its first drawing ("First the frame 'work ladder · Q01' ... one column per Space
(Description | Idea Studio · Audience Report | Work Details | Runs · Delivery ..."); its drawing has been the
five-part drawing since 261030. Proposed: "what a work Block, Job, Task and Run folder hold, and the scaffold that
makes them (JL 261007)." Each face's mind map is refreshed from the face afterwards (`haipipe-mindmap/scripts/mindmap.py
refresh`).

### 4.7 · Jobs

```text
j01_work_ladder_contract   answers: Q01,Q02,Q03 goes; nothing else
j02_work_skill_homes       "Make s21's delivery"; + t03_run_types_table; answers: Q04 goes; name kept
j03_work_workbench_pages   answers: Q01,Q02,Q03 goes; nothing else
j04_work_guide             new (§ 4.3)
```

`answers:` links a Job to a Block Question (`frame.py` reads it; haipipe-job's face contract lists it). With no
Questions it links to nothing, so it goes, and haipipe-job's owner hears that a work Job may have none (§ 6). j02
keeps its name: it still makes the skill homes, and renaming it would touch its Tasks and `render.yaml` for a word.

### 4.8 · The reports fold into their topics

```text
reports/q01_work_ladder/                  ─▶ s01-work-ladder/result/merged-q01-work-ladder/
reports/q02_plan_build_execute_report/    ─▶ s04-workbench-page-structure/result/merged-q02-plan-build-execute-report/
reports/q03_questions_and_runs/           ─▶ s04-workbench-page-structure/result/merged-q03-questions-and-runs/
reports/q04_work_skills/                  ─▶ s21-work-run-skill/result/merged-q04-work-skills/
```

Each keeps its `.md` and `page.toml` whole, the way s04 keeps `merged-s03-work-workbench/`. q01 (123 lines) and q04
(43 lines) carry the Q01 and Q04 proposals; q02 and q03 (18 lines each) never got an answer. Then `reports/` is gone.
Each report went where its Questions were fed from: s01 fed q01, s02 fed q04, s04 fed q01 to q03.

### 4.9 · `HANDOFF.md`, rewritten

Today it says: make B J T R ready as "the six Spaces Description · Idea Studio · Audience Report | Work Details |
Runs · Delivery ... as drawn in b03 (s03 Block, s04 Job, s05 Task)", the Block holds "studio/", "3 open questions".
Proposed outline, same length:

1. **Who**: the session for b17, the work theme; read `board.md` first.
2. **Goal**: the work pages on the focus page (j03's 3 × 3, s51 to s59) and the work skills (s01 by j01, s21 by
   j02, s31 by j04); no Questions.
3. **Where**: topics beside their Jobs; forms in `runs/` and each Task's `runs/`; the base page
   `servers/workbench/focus_page.py` (design_b02_workbench); `servers/workbench-work/`; `skills/2_theme/work/`.
4. **How**: decide in the sNN (Decided, Open), ask JL by a form (haipipe-interaction), make the delivery in its
   Job, render it out; never edit a generated file; never commit.

### 4.10 · The folder, before and after

```text
OLD  b17_theme_work/                         │ NEW  b17_theme_work/
board.md                                     │ board.md                     keys, sections
HANDOFF.md                                   │ HANDOFF.md                   rewritten
_studio_groups.txt  Skill Interface Navig..  │ _studio_groups.txt           Skill Levels Guide ..UI
reports/  q01 q02 q03 q04                    │ --                           GONE, folded
runs/  r01 r02                               │ runs/  r01 r02
src/  this Run's preview script              │ src/
s01-work-ladder/                             │ s01-work-ladder/             + merged-q01
s02-work-skills/                             │ s21-work-run-skill/          MOVED, + merged-q04
s04-workbench-page-structure/                │ s04-workbench-page-structure/  + merged-q02, -q03
--                                           │ s31-work-guide/              NEW
j01_work_ladder_contract/  t01 t02 t03       │ j01_work_ladder_contract/  t01 t02 t03
j02_work_skill_homes/  t01 t02               │ j02_work_skill_homes/  t01 t02 t03  t03 NEW
j03_work_workbench_pages/  t01 t02 t03       │ j03_work_workbench_pages/  t01 t02 t03  s51-s59
--                                           │ j04_work_guide/  t01 t02     NEW
```


## 5 · Leave as it is, and why

1. **s01's number and slug**: s01 is the ladder in every theme Block.
2. **s04's number**: 20 files outside b17 name `b17-s04`: haipipe-interaction's SKILL.md (its examples) and
   `collect.py`, `frame.py`, haipipe-ui, haipipe-studio, response-format, `haipipe-run/ref/run-types-by-space.md`,
   workbench-work, `guide.yaml`, b35, b32, b16's `paper_ui_cells.py`; and two forms carry `for: b17-s04` (j03 t01 r01,
   answered; b17 `runs/r02_collect_interactions_page`, waiting). A new number would cut both forms from s04's card.
3. **s51 to s59** (Q4 A): § 4.4.
4. **The Skill group**: JL's choice on 261031.
5. **Block UI, Job UI, Task UI**: as b16 (b16 runs r03, JL 261031: "make the UI in three levels").
6. **`## Deliveries`**: haipipe-studio asks every Block for it (One topic, one idea, one delivery); b16 should gain one.
7. **A Job per sNN delivery**: j01, j02, j03, now j04 (b35 s01-D14); the newer form of b16's goal prompts.
8. **No goals/**: each Job's face and its soft Runs are the prompt; b16's g03 is retired, its g04 ran on 261007.
9. **No related/**: nothing came in from outside; haipipe-related makes it with the first meeting, paper or email.
10. **No delivery/ at the Block**: each sNN keeps its own (haipipe-studio, 261030); b11's and b12's come from s61.
11. **No s11 to s13** (Q3 A): j03's t01_block_page, t02_job_page, t03_task_page are the levels; s01 holds the disk side.
12. **No s61** (Q3 A): every sNN ends in its own deck; b16 has none.
13. **No Studio, Delivery, Related or Report topics** (b16's s02 to s05): those views are b10's (s02 to s05) and the
    cells' (s51, s53); the work theme adds nothing of its own there.
14. **`j03_work_workbench_pages/_old/t03_element_picks/`**: b16 says `_archive/<date>/`; the same idea; nothing reads either.
15. **`ui-block`, `ui-job`, `ui-task`**: b11, b12, b16 keep them; they feed the Report's Block UI, Job UI, Task UI views.
16. **The Tasks' `run-design-<level>-page`** (b16's Tasks hold forms only): where each Task's design passes go.
17. **s04's `result/`** (mocks v1 to v14, merged-s03, merged-s32, the layout builders): its own working output.


## 6 · For other owners (listed, not fixed here)

1. **b16** (design_b16_theme_paper): no `## Deliveries`; 10 Block topics, over 9; HANDOFF.md says studio/, six Spaces.
2. **b11, b12**: no Tags, so their Studio shows one "Topics" button; 12 Block topics each; no HANDOFF.md.
3. **haipipe-studio**: the band table says s51-s59 server; b17's cells sit there, b16's in s32-s40.
4. **haipipe-job**: its face contract lists `answers:`; a work Job has no Question to answer.
5. **haipipe-run**: `ref/run-types-by-space.md` still lists the six Spaces and `run-ask-<qNN>`; s21 replaces work's rows.
6. **workbench-work**: `guide/guide.yaml` and `guide/method.md` teach Questions; s31 rewrites them.
7. **b01 j04_skill_folder** (design_b04_skill_folder): s01's path to b17's s02 is wrong today, then s21.
8. **design_b02_workbench** (`focus_page.py`): the Studio bar follows topic order, not `_studio_groups.txt`.
9. **b35 galleries**: `s04-delivery-gallery` and `s05-studio-gallery` `gallery.md` are generated; rerun after renames.

On 8: a person who drags a group sideways rewrites `_studio_groups.txt` (haipipe-studio § Groups), but the focus page
builds its bar from the topics' tags in folder order (`render`, `groups = list(dict.fromkeys(...))`), so the drag shows
only in the MindMap, which does read the file (`frame.studio_group_order`).


## 7 · Alternatives weighed

```text
choice                    picked                          weighed                                 why the pick
group bar (Q1)            Skill Levels Guide + 3 UI       b16's exact bar; by type (Skill UI);    b16's names where b17 has the same kind;
                                                          today's                                 Skill is JL's
s02 and the Run types     s02 widens into s21             keep s02 + new s21; s02 only            one topic as b16; s21 means it in b11 b12 b16
(Q2)
new topics (Q3)           s31 only                        + s11-s13; + s61; none                  Guide is stale; levels are j03; decks exist
UI cell numbers (Q4)      keep s51-s59                    s32-s40 as b16                          nine forms; s32 retired
s04's number              keep                            s11 (levels band)                       20 files and two forms name it
reports                   fold into topics                delete (git keeps them); keep frozen    s04's merged-* precedent; no leftovers
goals/                    none                            g01 for s21's plan, as b16's g04        the Jobs are the prompt
j02's name                keep                            j02_work_run_skill                      a word, not worth its Tasks and render.yaml
Covers/Excluded           add to s01 s04 s21 s31          leave as b16                            new_topic.py writes them; b16 is behind
At line                   drop                            keep                                    it does nothing at Block level
```

b16's exact bar (Structure, Levels, Run and Skill, Guide, then the UI groups) was not offered on the form: it drops
the Skill group JL set on 261031, and the brief says a decided point is never asked again.


## 8 · The form

`runs/r01_collect_theme_alignment/question_collection.md`, built into `r01_collect_theme_alignment.html`; every
option has its own preview page, written by `src/build_r01_theme_alignment_previews.py`.

```text
Q1 Studio groups      A Skill, Levels, Guide + three UI groups (pick) · B Skill, UI + three · C today's
Q2 Skills and Runs    A s02 widens into s21 (pick) · B keep s02, add s21 · C s02 only
Q3 New topics         A s31 Guide (pick) · B + s11-s13 Levels · C + s61 Slides · D none
Q4 UI cell numbers    A keep s51-s59 (pick) · B s32-s40 as b16
```

The form's intro says what follows the answers without a question: the reports fold, the For lines name their
reader, no goals/.


## 9 · After JL answers

1. Save the answers (`collect.py save`), then record each in s01's Decided as `s01-DNN · ... (JL <date>, r01 QN)`.
2. Faces first: `board.md`, `_studio_groups.txt`, the s01 and s04 faces, the Jobs' `answers:` lines, `HANDOFF.md`.
3. Then the moves, one sweep: s02 to s21 with every file of § 4.2, the reports of § 4.8.
4. Then the new: s31 by `new_topic.py topic <b17> --slug work-guide --title 'work Guide' --band guide`, j04 by
   haipipe-job's scaffold, j02's t03 by `new_job.py task`.
5. Then the generated: each changed topic's drawing and mind map, s04's builder, `work_ui_cells.py`'s cells, b35's
   galleries; open b17's Studio on 5623 and check the bar and every card.
6. Flag each answer applied: `collect.py applied <run> QN --by "<what changed>"`.
