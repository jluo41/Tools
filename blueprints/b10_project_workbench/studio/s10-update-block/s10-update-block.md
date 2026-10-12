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
    6 Questions    per level, in the theme's kinds (s07-D03)           haipipe-question
    7 open         the workbench at the Block; the pass is a soft Run  run-update-<bNN>, its passes
    ```
s10-D02 · Proposed (JL 261012: "this should be vary depeneding what are the theme of that block"; revised the
    same day: "I don't ask the questions that is meaningless ... the questions that are closely related to the
    jobs and tasks"): the work decides steps 5 and 6, the theme only names the groups they fall in. Topics and
    Questions are inferred from what the Block's own Jobs and Tasks do and answer (s10-D05); a theme's kinds
    (s07-D03) group them and fill only what the work leaves unsaid (a paper's standing Questions, s07-D08).
    The rules of steps 1 to 4 are the same for every theme. A first draft here gave b00 one Question per
    work kind (Data · Pilot · Evaluation); it was meaningless and is replaced by s10-D04.
s10-D03 · Proposed: nothing proposed is written without a person's pick. Steps 5 and 6 list their proposals in
    the pass of `run-update-<bNN>`; a person ticks the ones to keep, and only those become `studio/sNN-*/`
    folders and register rows (as s07: the groups come with them, from the theme).
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
    the topics' names (Profile · Families · Handoff · Intake, s07-D04). Dropped: "Is every raw drop
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


Open
----

1. The door: `/wb update` (JL's word; wb opens the workbench at the end) with haipipe-project as the engine, or
   `/haipipe-project update` grown?
2. Step 2's checks: in `haipipe-project` `ref/ladder.md`'s rules (one checker for shape and today's rules), or
   a second list beside it?
3. Does `/wb update` run on a whole Project too (every Block, one report), or one Block at a time first?
4. b10 now has 17 topics, against the suggested 10: does s10 belong in haipipe-project's own design Block?

(write here, or mark the drawing in red)
