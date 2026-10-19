s05 · Report: its workbench and its skill
=========================================

New on 261011, in the order JL set (JL 261011: "s02 studio, s03 delivery, and s04 related, and s05
report, and s06 run"): s02 to s04 are what the Block alone holds (Studio and Delivery, the top row's two
ends, and Related, its `related/`, shown under Description › Related; a top-row place for it is proposed
in s01-D34, not built); s05 and s06 are the Spaces row's Report and Runs, which every level keeps its
own. The Report used to share a topic with the Studio
(s04-studio-and-report, merged into s02 on 261010; its ids are now s02-D22 to s02-D30).

**Stage:** shaping

**Tags:** `Structure` · `Report`

**Topic:** the Report seen from both sides: what a report is and how a level answers its Questions,
its workbench (the Report Space on Block, Job and Task: one card per Question, opened as Logic │ Report with
the work inside the Report, b10 s32-D23)
and its skill (`/haipipe-report`). Unlike Studio, Delivery and
Related, which the Block alone holds, every level keeps its own reports, as it keeps its own Runs (s06).

**Feeds:** `reports/` q03_block_questions · q09_studio_report_on_screen


What a report is
----------------

A report is a Page that answers one Question of its level, `reports/qNN_<topic>/qNN_<topic>.md`.

1. **Question**: asked in the level's face (a Block's `board.md` `## Questions`); the Question and its
   report share one id, `qNN` (s02-D30).
2. **Work**: a Job or a Task names the Question it answers on its own face, `answers: Q01` (or one need
   of it, `Q01.E2`); a studio topic names the Questions it feeds, `**Feeds:** q01_<topic>`.
3. **Answer**: the report walks open → partial → answered, moved by its writer, never by a Run that
   finishes alone; its Opening states the answer, then Answer · Evidence · Limits · Next.
4. **Drawing**: generated from the studio frames its `## Figures` lists, never drawn by hand.

Every level reports (s09-D02): the Block in `reports/`, a Job in `jNN_<job>/reports/`, a Task in
`tNN_<task>/reports/` (s09-D08). A built pdf or docx goes to the Block's
`delivery/reports/qNN_<topic>/` (s03).


Files
-----

```text
s05-report-workbench-skill/
├── s05-report-workbench-skill.md            this face
├── build_s05_report_workbench_skill.py      the builder; marks are kept on rebuild
├── s05-report-workbench-skill.excalidraw    the story: four frames in one row, joined by arrows; In Tools below
├── s05-report-workbench-skill.png           its preview
└── .s05-report-workbench-skill.seed.json    generated snapshot for preserving marks
skill: Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-report/
       (asking: Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-report/)
```

Rebuild: `python build_s05_report_workbench_skill.py`.


In Tools
--------

Where its skill and code sit, under `Tools/plugins/haipipe-toolkit/`. The drawing's "In Tools" frame
reads the same off the disk on every build: the skill's folder as it is, its version, and each
function looked up in its file (JL 261011: "show what are the skills related folders in the Tools").

```text
skills/1_base/project/
├── haipipe-studio/     s02 Studio
├── haipipe-delivery/   s03 Delivery
├── haipipe-related/    s04 Related
├── haipipe-report/     s05 Report     ◀ this topic
└── haipipe-run/        s06 Run
servers/workbench/frame.py         question_rows · _report_cell · _answering · _opening
servers/workbench/page_reader.py   page_document, a report Page in the reader
skills/1_base/project/haipipe-report/   asks: the row, the folder
```


What the drawing holds
----------------------

```text
① Every level reports         the Studio (the centre) over Block, Job and Task, each with its own
                              reports/; what a report is; this Block's 12 Questions by state
② Work names its Question     studio topic -feeds-> Question <-answers- Job, Task, report; Q05 as the
                              example: fed by s01 and s21, two Runs on it, its report partial
③ The report says the answer  open -> partial -> answered (counts from disk); the report Page;
                              q01's drawing built from its ## Figures
④ Report Space and skill      the third row, the row heads and Q05's row as frame.py draws them; the
                              four Runs-panel buttons; /haipipe-report and the skills around it
Below                         still open (red); this Block's Questions, row by row; In Tools
```

Read from disk on every build: `board.md` `## Questions`, each report's `answer-status`, every topic's
`**Feeds:**` line (read as `frame.py` reads it), `runs/*/run.yaml` targets, q01's `## Figures`, the
Report Space through `servers/workbench/frame.py`, and the two skills' versions.


Finding (read 261011)
---------------------

1. This Block has 12 Questions and 12 reports: 9 open, 2 partial (Q05, Q10), 1 answered (Q11).
2. Q05's Work cell says "no work yet", though two Runs of this Block target it (`run-report-q05`,
   `run-check-q05`): the row lists Jobs and Tasks only, and this Block has no Jobs.
3. s32's Feeds line says `Q08 (one shared base, a theme each)`, without the folder name, so the
   Report Space does not count s32 as feeding Q08.
4. Report's third row is Ideation · Narrative · High-level logic + Low-level work · Related Questions;
   the first two list studio topics inside Report.


Decided
-------

s05-D01 · A new topic, s05-report-workbench-skill: the Report from both sides, its workbench and its
    skill, in JL's order: s02 Studio, s03 Delivery, s04 Related (held by the Block alone), s05 Report,
    s06 Run (the Spaces row, every level its own) (JL 261011).
s05-D02 · The drawing is one story in four frames joined by arrows, the report defined first, the way
    s06 defines the Run (JL 261011).

s05-D03 · Built 261012, four Opens settled: Open 3, a Question's Work cell also lists this level's own Runs whose
    run.yaml `target:` is its id (b10 Q05 reads "run-check-q05 done · run-report-q05 done"); Open 8, a bare
    `Q08` in a Feeds line is read as `q08`, so s32 counts for Q08 (both by the b10-report session in
    `servers/workbench/frame.py`, `_question_records`, `_note_facts`, `_report_page`). Opens 4 and 7 were
    settled by s07-D09: the Report's third row is gone, one card per Question under the group bar. Open 5 by
    s07-D13: every level shows its bar, and a Task with no Question lists its own Page under it.
s05-D04 · Built 261012 (JL: "Or just the two columns, for the logic and report (which contains the work as
    well). How do you think about it?"; b10 s32-D23): an opened Question card is two columns, Logic │ Report; the
    Work (its Jobs, Tasks and this level's Runs, D03) is one line in the Report, under the answer and above the
    drawing. 11 of b10's 12 Questions have no work, so the middle column stood empty; the drawing gets the width.

Carried in, decided elsewhere: every level reports (s09-D02), each in its own `reports/` (s09-D08);
Studio and Report are separate Spaces (s02-D05); the button says Report (s02-D10); `qNN` is the
Question and its report (s02-D30); a report's drawing is built from `## Figures` (s02-D23) and a
frame's name is the contract (s02-D24); checked is not a fourth state (s21-D04).


Open
----

1. What must each level's report answer? The Studio sets it, each level reports (s09 Open 2).
2. List Job and Task reports in the Block's Report, by source (s09-D08), once a Job has one?
3. Settled 261012 by s05-D03 (the level's own Runs are listed). Was: the Work column lists Jobs and Tasks only: show the level's own Runs on a Question too?
4. Settled by s07-D09 (s05-D03). Was: Ideation and Narrative, on Report's third row, list studio topics; s02-D05 keeps Studio and Report
   apart: keep them, or link out to Studio? (proposed: they move to the Studio, s07-D05)
5. Settled by s07-D13 (s05-D03). Was: a Task without Questions shows its own face as its report; s09-D08 gives a Task
   `reports/qNN_<topic>/`: which one? (proposed: a Task's Report is its own result, s07-D06)
6. When a cited studio frame changes, flag the report for review before its answer changes?
7. Settled by s07-D09 (s05-D03). Was: the third row says "High-level logic + Low-level work", the row heads "Logic · Work · Report":
   one name? (proposed: that view becomes the plain list, s07-D05)
8. Settled 261012 by s05-D03 (a bare `Q08` is read). Was: a Feeds line that names a Question without its folder name is not read (s32): read `Q08` too, or
   fix the line?

(write here, or mark the drawing in red)
