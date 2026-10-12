s09 · Studio sNN and Block, Job, Task, Delivery
===============================================

**Tags:** `Structure`

**Stage:** agreed

**Topic:** how a Block's Studio topics (`studio/sNN-<topic>/`) relate to the Block, its Jobs
and its Tasks, and how far along each topic is. From the JL meeting of 261010: the Studio is the
centre's policy paper, one copy per Block, sent down to every level; Block, Job and Task are the
province, the city and the county, each doing the work and each writing its own report. A reader
goes to the level to read its report. The Delivery is the Studio's twin: one per Block, collecting
every level's output under the Block's `delivery/`. A topic stays a draft policy until it is agreed,
so each sNN carries a stage, and the index shows the stages so the centre sees what moves and what
does not.

**Feeds:** `reports/` q03_block_questions · q09_studio_report_on_screen

**Source:** `../../related/meetings/2026-10-10-1800 研究项目工作流程设计与结构优化.md`
([58:10] centre and province, city, county; [58:26] and [74:02] a report at every level;
[74:18] what the centre must write; [32:34] Delivery at the top level)


Files
-----

```text
s09-studio-block-job-task-delivery/
├── s09-studio-block-job-task-delivery.md          this face
├── s09-studio-block-job-task-delivery.excalidraw  one frame: Studio and Delivery at the Block, the levels, the stage
├── s09-studio-block-job-task-delivery.png         its preview
└── build_s09_studio_block_job_task_delivery.py    the builder (the person's marks are kept)
```


Decided
-------

s09-D01 · The Block's Studio is the centre: one copy per Block, shared down to its Jobs and
    Tasks. It holds the plan (the drawing), the decisions, and what each level must report
    (JL meeting 261010 [58:10], [73:52]; the same rule as s02-D03 and s02-D09).
s09-D02 · Every level reports: Block, Job and Task each have their own Report, and a reader goes
    to the level to read it, as low as a Task and as high as the Block (JL meeting 261010 [58:26],
    [74:02]). This fills the Report half left open by s02-D06.
s09-D03 · Each sNN has a stage: explore · shaping · agreed · closed. A person moves it; the gate
    (red marks left, Open items, dated decisions, frame checks) only counts and never moves it
    (JL 261010).
s09-D04 · The index shows each sNN's stage and what we are working on now, so the centre sees at
    a glance what moves and what does not (JL 261010).
s09-D05 · Delivery is Block-level, the same as the Studio: only the Block holds `delivery/`. Job
    and Task outputs keep their source path under it (`delivery/jNN_<job>/tNN_<task>/<lane>/`), and
    the Job and Task views show their own part (JL 261010; confirms s02-D14 over the meeting's
    "top level across Blocks" [32:34]). Refined by s03-D06 (261011): from a Job or Task, the
    top row's Delivery opens the Block's Delivery with the open source picked, as Studio does.
s09-D06 · The topic is renamed s09-studio-block-job-task-delivery, so its name carries Delivery
    beside Block, Job and Task (JL 261010). The number s09 and its decision ids stay.
s09-D07 · Every b10 topic has a **Stage:** line under its Tags (261010, JL asked; set by Claude from
    the gate counts): 8 shaping (decisions made, open points or red marks left: s01 s02 s04 s05 s09
    s21 s31 s32), 4 explore (no decisions yet: s11 s12 s13 s51). None is agreed: agreed needs JL's
    sign. The shared Studio shows the stage as a badge before each topic's name.
s09-D08 · Each level's report lives in its own folder: a Job's in `jNN_<job>/reports/qNN_<topic>/`, a
    Task's in `tNN_<task>/reports/qNN_<topic>/`, the Block's in its `reports/` (JL 261010). This answers
    Open 1; the Block's Report view lists all three by source, as the Studio does.
s09-D09 · Stage → agreed (JL 261011: "I think for the s09, it can be closed as well"). Open 1 was settled
    by s09-D08 and Open 7 moved to s03; the other five wait under Later, and none blocks it. The
    drawing's red questions became a black later list with a green note.


Open
----

(none: agreed 261011, s09-D09)


Later
-----

Not needed now; each comes back as a new point if it is wanted.

1. What each kind of Block, Job and Task must report: the centre writes it; learn it on one real
   Block first ([74:18]).
2. Who writes the decision row that moves a stage, and whether the workbench gets a button for it.
3. Current (what we work on now) is saved in one browser; the index can only show it once it is
   a file in the Block.
4. Does the 10-topic cap count only explore and shaping topics? b10 has 16 topics now.
5. A deliverable that crosses Blocks (a meeting deck): does it get its own Block, as a paper Board
   already is? (Where Delivery lives is settled by s09-D05; its design is s03's.)

(write here, or mark the drawing in red)
