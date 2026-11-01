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
its workbench (the Report Space on Block, Job and Task: one row per Question, Logic │ Work │ Report)
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
├── s05-report-workbench-skill.excalidraw    three frames: Background (a tree), the Report as boxes joined by arrows, the screen
├── s05-report-workbench-skill.png           its preview
├── .s05-report-workbench-skill.seed.json    generated snapshot for preserving marks
└── history/                                 the 261011 and 261012 builders, faces, drawings and previews (-261012b: trees only)
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


The drawing's frames
--------------------

The three frames: ① and ② come from this block (haipipe-studio 0.13.0, `scripts/topic_map.py`); ③, the screen, is
drawn by the builder. The builder splices what it reads from disk into the `{{...}}` leaves and `{nq}`, `{nj}`.

```yaml
frames:
- title: "🧭 Background: the Report, for a newcomer"
  intro: What the topic is about, the words it uses, and where it sits.
  cols: 2
  tree:
  - "📝 What this topic is":
    - "🔎 the Report seen from both sides: its workbench (the Report Space) and its skill"
    - 📄 a report is a Page that answers one Question of its level
    - 🔁 unlike Studio, Delivery and Related, every level keeps its own reports (as it keeps its Runs, s06)
  - "🔤 The words":
    - "📌 Question: asked in a level's face (a Block's board.md ## Questions), id qNN"
    - "🧱 Work: a Job or a Task that says answers: Q01, or one need of it, Q01.E2"
    - "📝 Report: reports/qNN_<topic>/qNN_<topic>.md, answer-status open, partial or answered"
    - "🗂️ Report Space: the screen with one folding card per Question under a group bar"
    - "🧰 /haipipe-report: the skill that writes, checks and draws a report"
  - "📍 Where it sits":
    - 🧭 in the Spaces row, after s02 Studio, s03 Delivery, s04 Related; before s06 Run
    - "🏗️ Block / Job / Task":
      - 📝 reports/qNN_<topic>/
      - 📝 jNN_<job>/reports/qNN_<topic>/
      - 📝 tNN_<task>/reports/qNN_<topic>/
    - "📊 this Block today: {nq} Questions, {nj} Jobs, so no Job or Task report yet"
- title: "🗺️ The Report: from Question to answer"
  intro: A Question is asked, work answers it, the report says the answer, the Space shows it, the skill keeps it.
  boxes:
  - id: studio
    at: [0, 0]
    title: 🧠 Studio topics
    why: the thinking that raises a Question
    most: 1
    tree:
    - "✅ a Feeds: line on a topic's face names q01_<topic>"
    - ✅ a bare Q08 in a Feeds line is read too (s05-D04)
    - "{{fed}}"
    - "❓ a Feeds line naming a Question the Space cannot read is flagged"
  - id: question
    at: [1, 0]
    title: 📌 Question
    why: asked in the level's face, one id qNN with its report
    most: 1
    tree:
    - "{{states}}"
    - "❓ what must each level's report answer? The Studio sets it (s09 Open 2)"
  - id: work
    at: [2, 0]
    title: 🧱 Work
    why: Jobs, Tasks and Runs that answer a Question
    most: 1
    tree:
    - "📋 Job face: answers: Q01"
    - "📋 Task face: answers: Q01.E2, Q04"
    - 🏃 the level's own Runs whose run.yaml target is the Question (s05-D04)
    - "{{work}}"
  - id: report
    at: [3, 0]
    title: 📝 Report
    why: the Page that says the answer, moved by its writer
    most: 1
    tree:
    - "⬜ open: asked, no answer yet"
    - "🔶 partial: some Work answers part"
    - "✅ answered: the Opening states it"
    - "📄 reports/qNN_<topic>/qNN_<topic>.md: Opening, Answer, Evidence, Limits, Next"
    - "✅ checked is not a fourth state (s21-D04)"
    - "❓ list Job and Task reports in the Block's Report, by source (s09-D08)?"
  - id: code
    at: [0, 1]
    title: 🖥️ servers/workbench/
    why: the code that draws the Report Space
    most: 1
    tree:
    - "{{code}}"
  - id: space
    at: [1, 1]
    title: 🗂️ Report Space
    why: one folding card per Question at every level
    most: 1
    tree:
    - ✅ Block, Job and Task each show their cards (s07-D13)
    - "🎚️ the group bar":
      - "⬜ white: the Block's own group (s07-D12)"
      - "🔘 gray: fixed by the theme"
      - "🟧 amber: suggested by the theme (Random thoughts in every theme)"
    - "{{buttons}}"
  - id: figures
    at: [2, 1]
    title: 🖼️ Report drawing
    why: the picture of the answer, built never drawn
    most: 1
    tree:
    - "📄 qNN_<topic>.excalidraw, built from ## Figures"
    - "{{figures}}"
    - ✅ a frame's name is the contract (s02-D24)
    - "❓ when a cited studio frame changes, flag the report for review?"
  - id: skills
    at: [3, 1]
    title: 🧰 Skills
    why: the one owner of each step, in Tools
    most: 1
    tree:
    - "{{skills}}"
  arrows:
  - {from: studio, to: question, label: feeds}
  - {from: work, to: question, label: answers}
  - {from: work, to: report, label: fills}
  - {from: question, to: space, label: one card each}
  - {from: report, to: figures, label: draws}
  - {from: code, to: space, label: draws}
  - {from: skills, to: report, label: writes and checks}
```

What the drawing holds
----------------------

```text
① Background         a tree: what the topic is, the words it uses, where it sits
② The Report         8 boxes, each with an emoji title, a why line and its own tree, joined by named
                     arrows: Studio topics feed Question; Work answers it and fills the Report; the
                     Question gets a card in the Report Space; the Report draws its drawing; the
                     Skills write and check the Report; servers/workbench/ draws the Space.
                     Open points are red ❓ leaves in the box they belong to.
③ The Report Space   the screen as frame.py draws it, in the workbench's colours: the group bar (white
                     the Block's own, gray fixed, amber suggested), one card per Question, Q05 opened
                     with its Runs, the Runs panel
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

s05-D03 · Decided (JL 261012, through the b10 watcher: "go ahead and do all"): the drawing is three frames, each a folder tree: ① Background, ② the Tree, ③ the Report Space screen; the old frames are folded in; the old builder, face and preview are in history/.
s05-D04 · Built 261012, four Opens settled: Open 3, a Question's Work cell also lists this level's own Runs whose
    run.yaml `target:` is its id (b10 Q05 reads "run-check-q05 done · run-report-q05 done"); Open 8, a bare
    `Q08` in a Feeds line is read as `q08`, so s32 counts for Q08 (both by the b10-report session in
    `servers/workbench/frame.py`, `_question_records`, `_note_facts`, `_report_page`). Opens 4 and 7 were
    settled by s07-D09: the Report's third row is gone, one card per Question under the group bar. Open 5 by
    s07-D13: every level shows its bar, and a Task with no Question lists its own Page under it.
s05-D05 · Decided (JL 261012, through the b10 watcher): the drawing is boxes with trees joined by named arrows, an emoji on every node (haipipe-studio 0.13.0); the old builder, face and preview are in history/ (-261012b).

Carried in, decided elsewhere: every level reports (s09-D02), each in its own `reports/` (s09-D08);
Studio and Report are separate Spaces (s02-D05); the button says Report (s02-D10); `qNN` is the
Question and its report (s02-D30); a report's drawing is built from `## Figures` (s02-D23) and a
frame's name is the contract (s02-D24); checked is not a fourth state (s21-D04).


Open
----

1. What must each level's report answer? The Studio sets it, each level reports (s09 Open 2).
2. List Job and Task reports in the Block's Report, by source (s09-D08), once a Job has one?
3. Settled 261012 by s05-D04 (the level's own Runs are listed). Was: the Work column lists Jobs and Tasks
   only: show the level's own Runs on a Question too?
4. Settled by s07-D09 (s05-D04). Was: Ideation and Narrative, on Report's third row, list studio topics; s02-D05 keeps Studio and Report
   apart: keep them, or link out to Studio? (proposed: they move to the Studio, s07-D05)
5. Settled by s07-D13 (s05-D04). Was: a Task without Questions shows its own face as its report; s09-D08 gives a Task
   `reports/qNN_<topic>/`: which one? (proposed: a Task's Report is its own result, s07-D06)
6. When a cited studio frame changes, flag the report for review before its answer changes?
7. Settled by s07-D09 (s05-D04). Was: the third row says "High-level logic + Low-level work", the row heads "Logic · Work · Report":
   one name? (proposed: that view becomes the plain list, s07-D05)
8. Settled 261012 by s05-D04 (a bare `Q08` is read). Was: a Feeds line that names a Question without its
   folder name is not read (s32): read `Q08` too, or fix the line?

(write here, or mark the drawing in red)
