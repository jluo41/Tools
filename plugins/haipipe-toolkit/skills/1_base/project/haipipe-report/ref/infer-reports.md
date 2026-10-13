Infer a Block's Questions and reports from its Jobs and Tasks
=============================================================

A Question earns its place only when the Block's own Jobs and Tasks answer it (JL 261012: "I don't ask the
questions that is meaningless ... we might want to ask the questions that are closely related to the jobs and
tasks"). Read the work, find where its answers differ, and ask about that; never start from a theme's generic
list. The theme's kinds only name the groups the Questions fall in (b10 s05-D07). b10 s10 is the design.


Read the work
-------------

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts
python $S/block_inventory.py <block>            # the same reading haipipe-studio infers topics from
```

Its "candidate" lines are a start, not the answer: each names the sub-question and the Tasks behind it; the
agent words the Question from what those Tasks say.


Which Questions, at which level
-------------------------------

1. **A Task** asks the sub-questions its own face answers (`### 1 · What is one row?`); its report is its
   face (s05-D10). Nothing new is registered.
2. **A Job** asks what one Task of a kind in every Job answers for that Job and does not answer the same way
   everywhere: `Is the dataset ready for Source?` (each Job's source Task). Its report is that Task's face,
   linked from the Job's register row (`work: tNN_<task>`), not a new folder.
3. **A Block** asks where the answers differ across its Jobs, and what that means for the next step:
   - a status the Jobs do not share (`ready 11 · blocked 3`): why the few differ, and what settles them;
   - a gap many Tasks report (`no event time` in 60 tables): which, and whether the next Block can still use them;
   - a sub-question answered "none" by part of a kind (`What should Source watch out for?`: none in 59 of 280).
   Its report is a new `reports/qNN_<topic>/`, citing the Tasks (haipipe-question makes the row and folder).


The test before a Question is kept
----------------------------------

1. **Answered by named work**: it lists the Tasks (or the Job's Task) whose faces hold the answer, and the
   heading in them. None: drop it.
2. **Not answered the same everywhere**: a sub-question every Task answers identically (`Every file has a
   place`, 14 of 14) is settled; it is a line in a topic, not a Question.
3. **About this Block's next step**: what a reader, or the next Block, decides from it.
4. **In the Block's words**: drops, tables, families, Source; not "Data · Pilot · Evaluation".
5. **Grouped after**: its groups come from the Block's subjects and the theme's kinds (s05-D05, D06).


Worked example: b00_rawdata (261012)
------------------------------------

```text
level  Question                                                       answered by
Block  Q01 Why are j52, j53 and j96 blocked from Source, and what      3 source Tasks: "Is the dataset ready
           settles each?                                               for Source?" · "What is still open?"
Block  Q02 Which tables have no event time or no person column, and    60 + 29 profile Tasks: their Opening,
           can Source still read them by person and time?               "Whose data is it, and when …?"
Block  Q03 What must the Source functions handle, family by family?   221 profile Tasks: "What should Source
                                                                       watch out for?", split by raw-family 7
Block  Q04 Which drops lack tables of their family, and does it        7 intake Tasks: "Which tables of the
           matter downstream?                                          family does it lack?"
Job    Is <drop> ready for Source, and what is still open?            each Job's source Task (14)
Task   its own sub-questions                                           its face
```

Dropped, and why: "Is every raw drop inventoried?" (14 of 14 intake Tasks answer it the same way: settled);
"Does each family's loader read every table?" (no Task asks it; the profile Tasks read every file, 280 of 280).
