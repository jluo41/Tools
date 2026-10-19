s10 · Update a Block to today's rules
=====================================

New on 261012 (JL: "Suppose I have a totally new block, examples-1-data/Proj01-CGM-RawData/work/b00_rawdata
... How could I audit it and then make its structure to be correct, and then propose it sNN topics and also
the reports cross the b j t? ... This should be s10 immirgrate or update block folder? ... this should be vary
depeneding what are the theme of that block, right? I want it work like /wb update-to-date path to the
block"). s10 is free: it sits between the concept band (s01 to s09) and the levels band (s11 to s19), and
this topic is the bridge between the two.

**Tags:** `Structure` · `Run and Skill`

**Stage:** explore

**Topic:** one door, `/wb update <path>`, that takes any Block, old or new and of any theme, and brings it up to
today's rules. It audits the folder shape and today's b10 rules, plans the fix as a dry run, applies the moves
on `--apply`, then proposes the Block's studio topics and its Questions at Block, Job and Task, in its theme's
words, and opens the workbench there. b00_rawdata is the first real case.

**Feeds:** `reports/` q01_bjtr_boundary · q06_project_checker


Files
-----

```text
s10-update-block/
├── s10-update-block.md            this face
├── s10-update-block.excalidraw    two frames: b00 before and after /wb update; the steps, read on b00
├── s10-update-block.png           its preview
├── .s10-update-block.seed.json    generated snapshot for preserving marks
└── build_s10_update_block.py      the builder; reads b00 and runs the ladder audit on every build
```


Read on b00_rawdata (261012)
---------------------------

1. **Shape passes**: `haipipe-project` `scripts/ladder.py audit` finds 1 Block, 14 Jobs, 310 Tasks and 621
   Runs, all ok. The ladder's rules (`ref/ladder.md`) check folder shape only.
2. **Today's rules do not**: the face is `board.md` (`board-kind: task-block`), but `studio/` holds no sNN
   topic, only a data file (`raw-drop-manifest.tsv`, the 14 drops' table); there is no `## Questions`
   register and no `reports/` at the Block, any Job or any Task; no `related/`, `delivery/` or `runs/`. No
   check finds this today.
3. **What the work already answers** (`haipipe-studio` `scripts/block_inventory.py`, 261012): Task kinds
   profile 281 · intake 14 · source 14 across all 14 Jobs; the `raw-family:` field splits them 7 ways; every
   profile Task answers the same five sub-questions (What is one row? · Whose data is it, and when was it
   recorded? · What does each column hold? · What should Source watch out for? · Where does it come from?);
   the source Tasks say 11 drops are `ready_for_sourcefn_review` and 3 `blocked` (j52, j53, j96); 60 profile
   Openings say `no event time`, 29 `no person column`; 7 intake Tasks list tables their family lacks.
4. **Seeds are there**: `board.md` has 11 sections (Rules · Axis · Job-series numbering · Raw-drop Jobs · Task
   axis per family · Coverage and routing contract · Raw-data safety · Execution order · two dated scans ·
   an archived baseline), plus `raw_rules.md`, `family_catalog.yaml` and `TASK-TABLE.md`: what its topics
   and Questions would be made from.


Decided
-------

s10-D01 · Proposed (JL 261012): one door, `/wb update <path>` (the workbench skill's `cli/wb.py`), seven steps, each
    a dry run until `--apply`, each done by the skill that owns that part:

    ```text
    1 shape        haipipe-project ladder.py audit / update            exists; b00 passes
    2 today        the b10 rules as checks: studio/ holds sNN topics  new: the checks join ladder.md's rules
                   only; a register and reports/ where a level asks;
                   related/ delivery/ at the Block only; runs/
    3 plan         what moves, what is made, what is proposed          dry run, printed and saved
    4 apply        the moves, never a word rewritten                   --apply
    5 topics       sNN topics proposed from the face's sections       haipipe-studio new_topic
    6 Questions    per level, in the theme's kinds (s05-D07)           haipipe-report
    7 open         the workbench at the Block; the pass is a soft Run  run-update-<bNN>, its passes
    ```
s10-D02 · Proposed (JL 261012: "this should be vary depeneding what are the theme of that block"; revised the
    same day: "I don't ask the questions that is meaningless ... the questions that are closely related to the
    jobs and tasks"): the work decides steps 5 and 6, the theme only names the groups they fall in. Topics and
    Questions are inferred from what the Block's own Jobs and Tasks do and answer (s10-D05); a theme's kinds
    (s05-D07) group them and fill only what the work leaves unsaid (a paper's standing Questions, s05-D12).
    The rules of steps 1 to 4 are the same for every theme. A first draft here gave b00 one Question per
    work kind (Data · Pilot · Evaluation); it was meaningless and is replaced by s10-D04.
s10-D03 · Proposed: nothing proposed is written without a person's pick. Steps 5 and 6 list their proposals in
    the pass of `run-update-<bNN>`; a person ticks the ones to keep, and only those become `studio/sNN-*/`
    folders and register rows (as s05: the groups come with them, from the theme).
s10-D04 · Proposed, b00's own, inferred from its Jobs and Tasks (JL 261012): topics s01-table-profile (281 profile
    Tasks and their five sub-questions; `## Raw-data safety` joins it), s02-raw-families (the 7 `raw-family:`
    values and `raw_rules.md`), s03-source-handoff (14 source Tasks: 11 ready, 3 blocked), s04-drop-intake
    (14 intake Tasks). Block Questions, each answered by named Tasks and differing across the Jobs: Q01 Why are
    j52, j53 and j96 blocked from Source, and what settles each? (their source Tasks); Q02 Which tables lack an
    event time (60) or a person column (29), and can Source still read them by person and time? (those
    profile Tasks); Q03 What must the Source functions handle, family by family? (221 profile Tasks with
    something flagged, split by raw-family); Q04 Which drops lack tables of their family, and does it matter
    downstream? (7 intake Tasks). Each Job asks "Is <drop> ready for Source, and what is still open?",
    answered by its source Task's face (no new folder); each Task's report is its own face. Their groups share
    the topics' names (Profile · Families · Handoff · Intake, s05-D08). Dropped: "Is every raw drop
    inventoried?" (14 of 14 the same) and "Does each family's loader read every table?" (no Task asks it).
    `studio/raw-drop-manifest.tsv` moves beside `family_catalog.yaml` at the Block root.
s10-D05 · Proposed (JL 261012: "/haipipe-studio and /haipipe-report to learn how to infer the relevant studios from
    the existing block job and task"): the method lives in the two skills, on one reading.
    `haipipe-studio` `scripts/block_inventory.py <block>` reads every Job and Task face (writes nothing):
    recurring Task kinds, the fields that split them, the sub-questions most Tasks of a kind answer and how
    the answers spread, what stands out. `haipipe-studio` `ref/infer-topics.md` turns it into topics (a
    recurring kind is a method topic, a split one topic, no work no topic); `haipipe-report`
    `ref/infer-reports.md` into Questions by level (a Task its own; a Job what its one Task of a kind answers
    where the Jobs differ; a Block where the answers differ), kept only if named Tasks answer it and not all
    the same way. Steps 5 and 6 of `/wb update` call them. Built 261012: haipipe-studio 0.10.0, haipipe-report
    0.2.0, a test on a three-Job Block.


s10-D06 · Built (JL 261012: "is the /wb update ready to use now?" ... "examples-1-data/Proj01-CGM-RawData/work
    <--- next step, I want you to call the subagents to update the blocks here"): `/wb update <Block>` is
    workbench 1.20.0, `cli/wb_update.py` behind `cli/wb.py update`, with haipipe-project as the engine (Open 1).
    Step 2's checks are a `today:` key in haipipe-project `ref/ladder.md`, read by `ladder.py audit --today` and
    `update --today` (0.15.0; Open 2). A Project is one agent per Block (Open 3). `--apply` moves only a data
    file out of `studio/` (a drawing waits for its topic), then writes `runs/run-update-<bNN>/` with a pass
    holding `proposals.md`; the agent words it; nothing is made before a tick (D03). Not built yet: making the
    ticked lines in one command. Test: workbench `tests/test_wb_update.py`.

s10-D07 · Done (JL 261012: "could you call the subagents to work on them together?", which stood in for the
    ticks): six agents, one per Proj01 Block, made every proposed line: `new_topic.py topic` per topic (each
    face with its **Tags:** group, Topic and Open), `block_questions.py add-question --group` per Block
    Question (haipipe-report 0.7.0 added `--group` and `set-group`), a register row per Job Question in
    the Job's face, the ticks in `proposals.md`, and pass p02 of each `run-update-<bNN>`. b01's and b51's
    loose drawings moved into their topics with their builders, and each builder ran from there.
    `audit --today` then passed on all six (6 Blocks, 72 Jobs, 562 Tasks, 1073 Runs, 0 debt); today's
    `keep:` accepts `question-map.excalidraw`, which the workbench's `question_map.py` writes into `studio/`.
s10-D08 · Done (JL 261012: "could you call the new agent to evaluate them? How about each of their s00 for the
    background and index?"): six fresh read-only reviewers (haipipe-block-reviewer-agent), one per Block, scored
    what D07 made: mechanical checks clean everywhere, but 9 of 22 new Block Questions only partly grounded (a
    wrong number, a `work:` list cut short by a cap of 6, a "why" no face answers) and overlaps flagged in five Blocks.
    Six fix agents then applied every finding: numbers corrected, `work:` lists complete, two Questions and
    one topic folded (b02 Q02, b03 Q03, b03 s02; their ids never reused), b10's groups made real (Splits ·
    Build status · Inputs), Job rows made specific to each Job. Six writers wrote each Block's s00 background
    as two folder trees. Lessons for `/wb update`: no cap on `work:`; a Question's numbers are checked by
    someone who did not write them; `new_topic.py --feeds` takes `reports/q01_x` too (haipipe-studio 0.12.2).

Run on Proj01-CGM-RawData (261012)
----------------------------------

Six agents, one per Block, each ran the dry run, `--apply`, then worded its `proposals.md` from the Job and
Task faces. Nothing ticked; no topic, register row or report made. The shape audit passed on all six.

```text
Block               Tasks  topics  Block Qs  Job Qs  dropped  moved
b00_rawdata           310     4       4        1       10     studio/raw-drop-manifest.tsv to the root
b01_sourcestore       135     4       5        4        7     (drawing + builder go to s02)
b02_recordstore        32     4       4        7        6
b03_casestore          15     4       4        4        6
b10_aidatastore        11     3       3        4        5
b51_externalstore      59     6       2 new    6        -     16 loose drawings and builders go to s01-s06
```

1. **Faces carry the reading**: b00's Tasks answer `### ...?` headings, so the script found its Questions; in
   b01 to b10 most Task faces say "Not written yet" and every Job says `goal: open`, so the agents read
   configs, Openings and Run cards instead. The script found 0 Block Questions there; the agents found 3 to 5.
2. **Few Results**: b03 has 1 Result in 64 Runs, b02 1 of 11 RecordSets counted, b10 11 of 29: those gaps
   became Questions (b02 Q03, b03 Q02, b10 Q02).
3. **b51 already had 35 Questions** (ids `Q-food-1`, not `QNN`): its pass gives each a group (Food 7 ·
   Exercise 7 · Medication 8 · Insulin 8 · All events 5) and adds two.


Open
----

1. Make the ticked lines in one command (`wb.py update <Block> --keep`), or keep it the agents' step (D07)?
2. b51's register ids are `Q-food-1`, not `QNN`: rename to `QNN` on update, or let the register keep both?
3. b10 now has 17 topics, against the suggested 10: does s10 belong in haipipe-project's own design Block?

4. Q-all-6 and Q-all-7 in b51 have no report picture: `studio/_build/build_reports.py`'s ALL has no row for them.

5. The generated s00 index frame is over 2800 x 1600 on five Blocks (b01 to b10 at 3224 wide; b00, b51 over 2000 tall): `block_index.py`'s sizing, sent to its owner.

(write here, or mark the drawing in red)
