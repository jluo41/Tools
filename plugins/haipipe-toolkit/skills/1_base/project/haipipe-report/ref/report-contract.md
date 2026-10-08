# The report contract · Question │ Work │ Report

Read for anything about a Question's answer: the row the Audience Report draws, how
work links to a Question, where a Question stands, the report Page, its figures and its
check. Asking the Question (its size, id, register row, folder) is `haipipe-question`;
writing the Page's prose is `haipipe-page`. This reference was moved here from
`haipipe-question/ref/block-questions.md` (b03 s21, 261007); the words are kept.

## The row

Every level (a Block, a Job, a Task) shows its Questions in Audience Report as one row
each, three cells across (JL 261007: "to define the question - work - report workflow in
the Audience report").

```text
Question                         Work                               Report
the register row                 the Jobs and Tasks that answer it   reports/qNN_<topic>/qNN_<topic>.md
id · title · group · status      a face's answers: <id>              title · Opening's first paragraph
the studio topics that feed it   (or a need, answers: <id>.E<n>)     its one drawing · answer-status
(**Feeds:** in a topic's face)   then the register's work:           report qNN · <status>
owner: haipipe-question (ask)    owner: the theme's work skills;     owner: haipipe-report
       haipipe-report (status)          haipipe-report the link
```

1. **Question cell**: the face's `## Questions` register row (`haipipe-question`), its
   answer-status from the report, and each studio topic whose face says
   `**Feeds:** qNN_<topic>` (`haipipe-studio`).
2. **Work cell**: each Job or Task under this level whose face says `answers: <id>`,
   then the register row's own `work:` entries, in that order. Each opens its folder.
3. **Report cell**: the report Page's title (opens the Page), the first paragraph of its
   Opening, its drawing as a thumbnail, and `report <qNN> · <answer-status>`.
4. **A report not yet registered** still gets its row; the check calls it an error until a
   register row names it.
5. **A Task with no register** shows its own face as its report: a Task's Page is its answer.

The frame draws this row (`servers/workbench/frame.py` `question_rows`); a theme may draw
its own row over it but reads the same three sources.

## The link rule

Work links to a Question from the work's side: a Job or Task face carries

```text
answers: Q01                    # one Question
answers: Q01, Q04               # several
answers: QK10.E1                # one need of a Question: <id>.E<n> links to <id>
```

1. **On a face**: the line sits in the Job's or Task's face header, beside its other fields.
2. **Ids are the register's**: `Q` and two or more digits, or `Q-<word>-<number>`; a theme
   may use its own prefix (`QK10`). An id the level's register does not have is an error.
3. **A need**: `<id>.E<n>` names the Evidence Item `E<n>` a Task supplies; it counts for its
   Question. The need's own contract is the Page's (`haipipe-page`).
4. **The register's `work:`** also links (a path from the Block), for work whose face cannot
   say it; a face's `answers:` is preferred, so the link lives with the work.
5. **The report's own `answers:`** names its Question; a report that answers several names each.

## The walk

```text
open  ─▶  partial  ─▶  answered
asked     some Work     the report states the answer from exact Results
```

1. **open**: asked, no answer yet. `haipipe-question` creates the report frame in this state.
2. **partial**: some Work answers part of it; the report says which part.
3. **answered**: the Opening states the answer; Evidence links the exact Results or Pages.
4. **Who moves it**: the report's writer (Write the report), never the frame, never a Run's
   completion alone. `results-read:` is set when the evidence was actually read.
5. **No fourth state** (decided, b03 s21, 261007): "checked" is not a state of the answer. A
   check judges one version of the report Page; the walk says where the answer stands. The
   Page's own CHECK verdict is shown beside `answered`, so one fact lives in one place.

`answer-status` is independent of the Page's native `state:` and of execution completion.

## The report Page

```text
reports/qNN_<topic>/
├── qNN_<topic>.md          the report Page: header lines, Opening, Content, ## Figures
├── page.toml               registers the Page with the Page reader
├── qNN_<topic>.excalidraw  its one drawing, generated from ## Figures (or drawn in studio/)
├── qNN_<topic>.png         the drawing's preview
└── studio/                 this report's own drawings, when it draws them by hand
```

The Report is a `haipipe-page` Page, with its normal Opening, Content, Draft, evidence
records, adoption, CHECK and release. Load `haipipe-page` before writing it. Do not apply
the executable Task Page grammar or `folder-kind: task` to this report Folder. No new
Folder kind is needed for an ordinary report Page.

For a manually created report, register it with the ordinary Page manifest:

```toml
version = 1
source = "q01_comparable_conditions.md"
title = "Comparable conditions"
```

The `source` must match the report Folder's same-stem Markdown. Registration enables the
existing Page workbench; it does not record writing or approval.

Three header lines:

- `answers: Q01` (comma-separated ids if a report answers multiple Questions).
- `answer-status: open | partial | answered` describes the Question's answer.
- `results-read: <ISO-8601 time with timezone>` records when its linked evidence was
  actually read. Set it after the reading, never merely on save.

Opening states the current answer in plain language. For the compact reading in the
workbench, use these Content division names (normal Page numbered paragraphs, Draft
Bullets and evidence bindings still apply):

1. **Answer**: reasoning and interpretation supporting Opening.
2. **Evidence**: Markdown links to exact Result files or source Pages. Resolve file links
   relative to the report Folder, e.g.
   `../../j01_<job>/t01_<task>/runs/r01_<slug>/result/metrics.json`.
3. **Limits**: remaining uncertainty, missing evidence or scope boundaries.
4. **Next**: the concrete action to continue; an answered Question may instead state the
   downstream use or that no further action is needed.

Write through the Page flow: plan Structure and evidence needs, draft, adopt when
authorized, then the owning CHECK/release gates. The scaffold contains no answer, accepted
Content, fabricated receipt or completed review. Do not type final prose directly into
generated Content.

The workbench reads Opening and these Content divisions. It shows declared answer status
and Page state separately. Linked local evidence newer than `results-read` is flagged for
review without rewriting the report. External links and unlinked changes cannot be
freshness-certified by this projection; use the Page's own evidence and CHECK workflow for
closure.

A report Folder is reading material, not an executable `tNN` Task. It gets no BJTR address
and creates no Job, native `rNN`, or Task workflow. The Task Page already explains its own
Task; a report synthesizes the answer to a Question and may reference several Tasks.
Reference original Results and Task Pages; do not copy them into another result registry.

## Report kinds

| kind | folder | header | register row |
|---|---|---|---|
| answer (default) | `reports/qNN_<topic>/` | `answers:` · `answer-status:` | `group:` free |
| comments batch | `reports/qNN_<kind>-<MMDD>/` (`<kind>`: the theme's batch kinds) | adds `page-type: comments` | `group: comments` |

A batch's `<kind>` is its theme's: a paper's are `haipipe-paper-comments`' (review · editor ·
coauthor · meeting · advisor, e.g. `q01_editor-decision-<MMDD>`); a theme with none of its own
uses feedback · meeting · sent.

A comments batch (a round of reviewer or co-author comments) is a report of type comments
in the level it answers, never a Task (b16, JL 261007: "comments … are a special type of
report … in the reports/"). It keeps the same row, walk and check; its Answer is the
response to each comment.

## Figures and the drawing

One Question, one drawing (JL 261005). When the report's pictures already exist as frames
of the level's studio drawings, the report drawing is generated, never drawn by hand: the
report's `.md` lists its figures under `## Figures`.

````markdown
## Figures

```yaml
figures:
- from: ../../studio/s01-<topic>/s01-<topic>.excalidraw
  frame: "1 · <frame name>"
  caption: <what this figure shows>
```
````

`from` is relative to the report folder; `frame` is the frame's exact name in that drawing.

```bash
python <haipipe-report>/scripts/build_report_drawing.py <reports/qNN_topic/> [--width 3000]
python <haipipe-studio>/scripts/render_png.py <reports/qNN_topic/qNN_topic.excalidraw> <….png>
```

The build copies each frame (with the person's marks, without their red comment notes),
scales it to one width, straightens it, and stacks the figures under a heading frame with a
source line each. The frame's name is the contract: rename a studio frame and the build
names the frames it can find. To change a figure, change the studio drawing; to change the
choice, change the list; then rebuild. The drawing is generated output: nobody edits it.

A report drawn by hand (no `## Figures`) follows `excalidraw-report`'s report mode
(`ref/report-drawing.md`: answer and strongest evidence first, plot kit, embedded figures).

## The check

```bash
python <haipipe-report>/scripts/check_report.py <level folder> [--json]
```

It reads one level's rows as the workbench does and reports, exit 1 on any error:

```text
error  answer-status is not open · partial · answered
error  a face's answers: names a Question this level's register does not have
error  a report's answers: does not name its own Question
error  an answered report with no Opening, or with no Evidence link
error  a report folder no register row names
error  a register that is not valid yaml
warn   partial or answered without results-read:
warn   a ## Figures drawing missing, or older than the .md or a source drawing
warn   answered with no Work and no Evidence link (reasoning only: say so in Limits)
```

The check is mechanical. Judging whether the answer is right is the report Page's CHECK,
in a fresh context by an agent that wrote none of it (`haipipe-page-check-agent`).

## The buttons

| Button (Audience Report) | Run (soft, in the level's `runs/`) | does |
|---|---|---|
| Ask a Question | `run-ask-<qNN>` | `haipipe-question`: register row, folder, open frame |
| Write the report | `run-report-<qNN>` | the Page flow over Opening · Answer · Evidence · Limits · Next; moves the walk |
| Rebuild report drawing | `run-figures-<qNN>` | `build_report_drawing.py`, then its preview |
| Check a report | `run-check-<qNN>` | `check_report.py`, then the Page's CHECK in a fresh context |

Each is a soft Run: one Run per target, one pass per round (`haipipe-run`).

## Routing the word report

- `haipipe-task report <tNN folder>` is P-B-E-R: `workflow/report.yaml` and execution
  audit, as defined in its `fn/stage-report.md`.
- "Report for Q01 / answer this Block Question" uses this reference and the report's Page
  workflow. It can lead to a request for Task work when evidence is missing, but does not
  execute work implicitly.
- The workbench is a reading/editing surface over these owners. Run completion alone never
  marks a Question answered or a report Page released.
