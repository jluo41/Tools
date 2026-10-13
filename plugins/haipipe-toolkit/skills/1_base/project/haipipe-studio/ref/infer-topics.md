Infer a Block's topics from its Jobs and Tasks
==============================================

A topic is worth a folder when it explains work the Block already does. Read the work first, then name the
topics; never start from a list of generic subjects (JL 261012: "I don't ask the questions that is meaningless
... learn how to infer the relevant studios from the existing block job and task"). b10 s10 is the design.


Read the work
-------------

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts
python $S/block_inventory.py <block>            # or --json for the whole reading
```

It reads every Job and Task face, writes nothing, and prints what repeats:

1. **Kinds**: a Task kind that recurs across Jobs (`t21_profile_glucose`, `t12_profile_cgm` → `profile`).
2. **Splits**: a face field whose few values split the Tasks (`raw-family:` 7 values over 310 Tasks); a field
   that only restates the Job (`cohort:`, `job:`) or is free text is no split.
3. **Sub-questions**: a heading ending in `?` that most Tasks of a kind answer, and how the answers spread.
4. **Stands out**: what the Openings say is missing (`no event time`), and an answer few Tasks give.


From the reading to topics
--------------------------

1. **A recurring kind is a method topic**: how that kind of Task is done, its steps and its sub-questions,
   the loader or skill it runs. One topic per kind with Tasks in two or more Jobs.
2. **A split is a topic when the method differs by its value**: the raw families each read differently;
   one topic for the split, a section per value, not a topic per value.
3. **A face section that sets a rule** (`## Raw-data safety`) joins the topic whose Tasks follow it, or is
   its own topic when no kind owns it.
4. **What stands out feeds a topic's Open list**, in red, naming the Jobs: it is a question for the Report,
   not a topic of its own (haipipe-report `ref/infer-reports.md`).
5. **Each topic names its ground** on its face: `**Topic:**` says which Tasks it explains (counts and two
   examples), so a reader can open them.
6. **No topic without work**: a subject no Task touches waits until a Job does it.



Groups, proposed with the topics
--------------------------------

`/wb update` proposes each topic's group with the topic, and the same name tags the Questions the topic feeds,
so the Studio and the Report share one bar (b10 s05-D05, D08). A person keeps or renames it with the tick.

1. **Names a subject of this Block's work**, in its own words: Profile · Handoff · Splits · Build status.
2. **Never the Block's name or a status**: `Aidatastore`, `Done`, `Open` say nothing (b10_aidatastore, 261012).
3. **One topic, usually one group**; two topics share one only when they are halves of one subject.
4. **Two to six per Block**: one per topic is fine; more than six means the subjects are cut too fine.
5. **Order**: `studio/_groups.txt` lists them in topic order, s01 first; the Report's bar follows it.
6. **s00 has none**: the background and index covers the whole Block.

The script's first guess is the Task kind or the split field (`profile` gives Profile, `raw-family` gives
Family); the agent rewords it from the work before the tick.

Worked example: b00_rawdata (261012)
------------------------------------

The reading: 14 Jobs, 310 Tasks; kinds `profile` 281 · `intake` 14 · `source` 14; split `raw-family` 7.

```text
topic                          its ground
s01-table-profile              281 profile Tasks: What is one row? · Whose data, and when? · What does each
                               column hold? · What should Source watch out for? · Where from, how read?
s02-raw-families               raw-family: welldoc_flat_csv 241 · metric_csv_bundle 26 · aireadi 20 · xml 7 ·
                               image_plus_csv 5 · excel 4 · single_flat_csv 3; raw_rules.md
s03-source-handoff             14 source Tasks: ready_for_sourcefn_review 11 · blocked 3 (j52, j53, j96)
s04-drop-intake                14 intake Tasks: the files, the family's missing tables, changed since?
```

`board.md`'s `## Raw-data safety` joins s01 (every profile Task runs `privacy-mode: metadata_only`).
`studio/raw-drop-manifest.tsv` is the drops' table, not a topic: it moves to the Block root.
