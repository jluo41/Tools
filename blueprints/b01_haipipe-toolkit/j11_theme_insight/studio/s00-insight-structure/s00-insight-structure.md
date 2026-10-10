s00 · Insight structure
=======================

**Topic:** the thinking behind the insight ladder (JL 261007): what an Insight Project looks like; the
Prototype as its own work Block whose Jobs are Prototype versions; the insight Board whose Jobs pin one
Prototype version and one data version; the two clocks; where a new release comes from and what
triggers it; and the Block's questions with our ideas and the choices still open.

**Feeds:** `reports/` q01_insight_ladder, q02_partitions_pooling, q03_question_gates,
q04_level_delivery, q05_register_boards (and a proposed Q06, the Prototype and data versions).


Files
-----

```text
s00-insight-structure/
├── s00-insight-structure.md            this notes file
├── build_s00_insight_structure.py      the builder; marks are kept on rebuild
├── s00-insight-structure.excalidraw    the drawing: a design scratch, placeholders only
└── s00-insight-structure.png           its preview
```

Rebuild: `python build_s00_insight_structure.py`. The Questions frame reads `../../board.md`.


What the drawing holds
----------------------

1. An Insight Project: `work/bNN_<topic>_prototype/` (the questions and their code) beside
   `insights/bNN_<topic>/` (one dataset, its versions, the answers); designs and discoveries optional;
   the data versions outside the Project.
2. The two Blocks, each a box, a definition and its tree. Prototype Block: one Job per Prototype
   version (`j01_p1`, `j02_p2`), frozen when closed; a version Job holds `release.yaml` (every live
   question, pointing to its Task here or in an earlier version) and only new or changed Tasks;
   `proposals/` is the backlog. Insight Board: one Job per pair, Prototype version × data version
   (`j03_p2_<d>v2`); its Tasks are the questions on that pair, its Runs one per partition. Arrows: the
   Board's Job uses a version by path and hash, never a copy; the Board sends proposals back.
3. Two clocks and the chain of Jobs; one clock per Job, so a change in an answer has one cause.
4. Where a new release comes from: six triggers (a level answered, a check failed, a weak answer, new
   data fields, someone asks, a paper suggests it) feed `proposals/`, then the next version Job is
   opened, worked, reviewed, signed by a person and closed; the Board then adds a Job. New data needs
   no release.
5. Questions: the register's Q01 to Q05 and a proposed Q06, each with our idea and the choice it
   waits on in a red box (black only since haipipe-studio 0.2.0, 261007).
6. The logic tree (JL 261007: "add things like this: the logic tree"), its own frame to the right: a box
   per folder, plain lines for what holds what, labelled arrows for how they relate (the Board's Job uses
   a version by path and hash; its Task runs that version's script; the Job pins a data version; its
   pages feed the answers across Jobs; the answers send proposals back; the signed handoff goes to
   Design), red dashed for what is open (when the backlog opens the next version; one clock per Job).
7. (261007, with s11 and s12) The cuts are plan: `partitions.md` and `thresholds.yaml` live in each
   Prototype release, so a new or changed cut is a new release; the Board's `meta/` keeps only the
   checker's `status.md`. The Board's `reports/qNN_<topic>/` hold the Block's own questions, a second
   D · I · K · W over the Jobs' answers.
8. (261007, JL: "we might want to propose more run-types") A frame, Run types by level: hard Runs only at
   a question Task of a Job (rNN_<partition>, rNN_cross); soft Runs at every level (Prototype: propose,
   open a release, define cuts, sign, close, ask, plan, script, reviews; Board: add a version, add a Job,
   check, read across Jobs, handoff; Job: launch, power, compare with the previous Job, close; Task:
   write, check, sign). A Job's order: launch -> power -> runs -> cross -> write -> check -> compare ->
   close. The compare rule (what "held" means) is plan, in the release's thresholds.yaml; the Job's
   `reports/vs-<prev>.md`, written by run-compare, feeds Audience Report › vs previous.


Open
----

1. One Prototype Block per insight Board, or may several Boards share one?
2. Signed releases: cut per level, per batch of proposals, or on demand?
3. One clock per Job?
4. Versions: accumulate (compare, never pool) or batches (may pool)?
5. Does a signed handoff go stale when a newer Job lands?

(write here, or mark the drawing in red)
