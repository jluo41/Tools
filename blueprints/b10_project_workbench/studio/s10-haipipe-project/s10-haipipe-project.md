s10 · haipipe-project: a Project's root, its update door, and the skill behind each button
=========================================================================================

Merged on 261012 (JL: "could we merge s21 and s10? I think we need to rename it to s10_haipipe-project ... to
explain this skill, cuold you use /excalidraw-studio to describe it?"): s10 (Update a Block to today's rules) and
s21 (Project Run and skill) are one topic now, about the haipipe-project skill. The folder is `s10-haipipe-project/`,
with a hyphen like every other topic folder (s01 Open 1c). s21's number is retired, never reused, and its decisions
keep their ids (s21-D01 to s21-D07) below, so the files that cite them stay true.

**Tags:** `Structure` · `Run and Skill`

**Stage:** explore

**Topic:** what the haipipe-project skill is and does. It owns a Project's root (README.md, project.yaml, which
Theme folders exist and which skill owns each) and checks the shape of every level below it (Block → Job → Task →
Run → pass). Its update door, `/wb update <Block>`, brings any Block, old or new and of any theme, up to today's
rules. Every Run button of the base frame names the one skill that does its work.

**Feeds:** `reports/` q01_bjtr_boundary · q05_skill_per_level · q06_project_checker · q08_workbench_base


Files
-----

```text
s10-haipipe-project/
├── s10-haipipe-project.md            this face; its yaml is the drawing's words
├── s10-haipipe-project.excalidraw    the drawing: three acts, four frames (excalidraw-studio)
├── s10-haipipe-project.png           its preview
├── build_s10_haipipe_project.py      the builder, on excalidraw-studio's draw.py; reads the skill folders and
│                                     frame.py's buttons on every build
└── history/                          s10's and s21's faces, drawings and builders before the merge; q05's
                                      figure still reads s21_project-run-skill.excalidraw there
```

Rebuild: `python build_s10_haipipe_project.py`.


Drawing
-------

Three acts, read top to bottom (excalidraw-studio's principles): what the skill owns, how it updates a Block,
and who does each button's work. A frame's facts that can be read from disk (versions, folders, buttons) are read
on every build; the words are here.

```yaml
drawing:
  root:
    title: "① haipipe-project: a Project's root, and the shape of every level below"
    sub: "One Project is one research or software boundary. The skill owns its root and checks the shape below it; what sits inside a Theme belongs to that Theme's own skill."
    centre: "{skill} owns a Project's root and checks the shape below it"
    branches:
    - title: 📁 The root
      summary: two files make a Project
      leaves:
      - "README.md: the human entry"
      - "project.yaml: profile (research · software · hybrid) and git_mode (workspace · submodule)"
      - "no empty Theme folder: its owner makes it with the first real file"
      - "note/: the inbox; each note or thought names its next Block and sNN"
    - title: 🗂 The Theme folders, each with its owner
      summary: the root says who owns each folder and never writes inside one
      leaves:
      - "work/ haipipe-task · discovery/ haipipe-discovery · cowork/ haipipe-cowork"
      - "paper/ haipipe-paper · design/ haipipe-design · insight/ haipipe-insight"
      - "labeling/ subjective-label · ideation/ haipipe-ideation"
      - "platforms/ and external/: a link only"
    - title: 🪜 The ladder below, shape only
      summary: "Block → Job → Task → Run → pass, in one table"
      leaves:
      - "ref/ladder.md: each level's face, folders, children and Run names"
      - "scripts/ladder.py audit and update, at any level"
      - "a today: key holds b10's rules as checks (s10-D06)"
      - "content, such as a Page's sections or a ticket's body, stays its owner's"
    - title: ⌨️ Six commands
      summary: "new · repo · audit · update · feedback · digest"
      leaves:
      - "audit: read only, every finding and the step that fixes it"
      - "update: a dry run; --apply runs each step and audits again after it"
      - "new and repo: README.md and project.yaml, a repo kept as a submodule"
    - title: 🛡️ The safe update law
      summary: nothing moves that a person has not seen first
      leaves:
      - "a dry run unless --apply, and it never commits"
      - "never moves a submodule, a Result bank or a large code tree"
      - "an old layout is declared as debt, not hidden"
    - title: ↩️ What it returns
      summary: "status: ok · debt · blocked · failed"
      leaves:
      - "summary: what was made, reconciled or found"
      - "artifacts: the paths it changed or read"
      - "next: the safest next step"
  folder:
    title: "② The skill as a folder in Tools/"
    sub: "haipipe-project and its family in skills/1_base/project/, read from disk on every build; each reaches Claude through ~/.claude/skills/<name>."
    key: "fn/ says what each command does, ref/ holds the contracts, scripts/ does the work: a command runs the same for a person and for an agent"
    flow_title: "⚙️ one command, through the folder"
    flow:
    - title: "/haipipe-project audit <Block>"
      lines: ["a person or an agent asks"]
    - title: fn/audit.md
      lines: ["what the command does, step by step"]
    - title: scripts/ladder.py audit
      lines: ["reads ref/ladder.md's one table"]
    - title: findings, each with its fix
      lines: ["status ok · debt · blocked · failed"]
    flow_labels: [reads, runs, prints]
    notes:
      fn/: one page per command
      audit.md: "audit: read only, findings and fixes"
      update.md: "update: the dry run, then --apply"
      project.md: "new: README.md and project.yaml"
      repo-project.md: "repo: a Project kept as a submodule"
      feedback.md: "feedback: capture a note"
      digest.md: "digest: harvest a session"
      ladder.md: the ladder table, read by ladder.py
      project-structure.md: the root contract
      code-structure.md: a software Project's code
      ladder.py: audit and update below the root
      project.py: new, repo and the list
      audit_projects.py: the root's checks
      rename_themes.py: "the Theme rename (s01-D28)"
      link_check.py: links after a move
      probe_tickets.py: tickets after a move
      test_project_update.py: update on a test Project
  update:
    title: "③ /wb update <Block>: any Block brought up to today's rules"
    sub: "The update door is the workbench's cli/wb.py update, with haipipe-project as its engine. Each step is a dry run until --apply, and each is done by the skill that owns that part (s10-D01, s10-D06)."
    steps:
    - title: "1 · shape"
      lines: ["haipipe-project ladder.py audit", "faces, folders, Run names"]
    - title: "2 · today"
      lines: ["the today: rules in ladder.md", "studio/ holds sNN topics only", "reports/ where a level asks"]
    - title: "3 · plan"
      lines: ["what moves, what is made", "printed and saved"]
    - title: "4 · apply"
      lines: ["--apply moves files", "never rewrites a word"]
    - title: "5 · topics"
      lines: ["haipipe-studio infers sNN", "from what the Jobs and Tasks do"]
    - title: "6 · Questions"
      lines: ["haipipe-report infers qNN", "per level, in the theme's groups"]
    - title: "7 · open"
      lines: ["the workbench at the Block", "a pass of run-update-<bNN>"]
    labels: [then, then, "--apply", propose, propose, open]
    loop:
    - title: "🙋 a person ticks"
      lines: ["only ticked lines are made (s10-D03)"]
    - title: "🧱 agents make them"
      lines: ["new_topic.py and add-question (s10-D07)"]
    - title: "🔍 fresh reviewers score"
      lines: ["9 of 22 Questions only partly grounded (s10-D08)"]
    - title: "🛠️ fix agents apply"
      lines: ["numbers, work lists, overlaps folded"]
    loop_labels: [then, then, then]
    loop_back: "audit --today again, until it passes"
    result: "Run on Proj01-CGM-RawData, 261012: 6 Blocks, 72 Jobs, 562 Tasks, 1073 Runs, 0 debt after the loop"
    open:
    - "❓ s10 Open 1: make the ticked lines in one command (wb.py update <Block> --keep), or keep it the agents' step?"
    - "❓ s10 Open 2: b51's ids are Q-food-1, not QNN: rename them on update, or keep both?"
  buttons:
    title: "④ Every Run button names the one skill that does its work"
    sub: "Read from the base frame (servers/workbench/frame.py) on every build: a button names a skill, the skill opens one Run, the Run writes one folder, and its Space shows it (s21-D01, s21-D02)."
    skills: [haipipe-block, haipipe-studio, haipipe-report, haipipe-job, haipipe-task, haipipe-run, haipipe-project, haipipe-delivery]
    about:
      haipipe-block: "the Block's face, its Questions, a new Block (was haipipe-board, s21-D07)"
      haipipe-job: "the Job's face and its Tasks in order"
      haipipe-task: "the Task, left untouched on purpose (s21-D01)"
      haipipe-studio: "these sNN topics, their drawings and sessions"
      haipipe-report: "a Question's report Page: open → partial → answered (s21-D04)"
      haipipe-run: "every Run's folder, card and passes"
      haipipe-project: "the root and the shape: audit and update"
      haipipe-delivery: "what leaves the Block"
    open:
      haipipe-delivery: "❓ s21 Open 1: delivery has its own skill now; re-decide s21-D03"
      haipipe-report: "❓ s21 Open 2: what must each level's report answer?"
      haipipe-run: "❓ s21 Open 3: where does a batch launch go, if a Job holds soft Runs only?"
  acts:
  - name: "Act 1 · What it owns"
    frames: [root, folder]
    arrow: lives in
  - name: "Act 2 · How it updates a Block"
    frames: [update]
  - name: "Act 3 · Who does each button's work"
    frames: [buttons]
  between:
  - [root, update, brings a Block up to today with]
  - [update, buttons, "each step is one skill's, as each button is"]
```


Decided
-------

s10-D10 · Decided (JL 261016: "in the project level, we will have the note folder, that the other AI session will
    just write the quick note ... should ask the AI to try to go one step further"; "change the notes to note";
    "sometimes the random thoughts will be helpful"): a Project's `note/` is its one inbox, at the Project level.
    Any session writes `note/YYMMDD-<slug>.md`, a finding, a gap or a random thought; its `next:` names the Block
    and the Job or sNN topic it feeds (or `new Block`; a thought's best guess marked `?`). No Block-level
    `s99-note`. Written in haipipe-project 0.16.0 (`ref/project-structure.md` § note/, `ROOT_DIRS` in
    `audit_projects.py`) and in Knowledge-SPACE `AGENTS.md` § Quick notes; the 14 old `notes/` folders renamed.

s10-D09 · Decided (JL 261012): s10 and s21 merge into `s10-haipipe-project`, a topic about the haipipe-project
    skill, drawn with excalidraw-studio's `draw.py` in three acts. s21's number is retired; its decisions keep their
    ids. Its old drawing stays in `history/` for q05's figure.

From s10 (Update a Block to today's rules, 261012):

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

From s21 (Project Run and skill, 261007 to 261012):

s21-D01 · Proposed (JL 261007): the base skills are one per level and one per shared Space; each theme keeps
    its own skills over them, as its `<theme>_theme.py` does over the frame.

```text
              Description    Studio          Report            Work            Runs          Delivery
Block    ─▶   haipipe-block  haipipe-studio  haipipe-report    haipipe-block   haipipe-run   haipipe-block ?
Job      ─▶   haipipe-job    haipipe-studio  haipipe-report    haipipe-job     haipipe-run   haipipe-job ?
Task     ─▶   haipipe-task   haipipe-studio  haipipe-report*   haipipe-task    haipipe-run   haipipe-delivery (ref/page-delivery.md)
Guide    ─▶   workbench-<theme>
```

    - haipipe-block (new; the deleted one's name): the Block's face and question register, its Spaces, a
      new-Block scaffold, how a theme claims a Block (`Theme.claims`).
    - haipipe-job (new): the Job's face, its Tasks in order, a new-Job scaffold, a theme's own Job names.
    - haipipe-task: not touched (JL 261007: "you should not touch the haipipe-task"); the Task level's
      buttons name it as they are. `skills/1_base/task/` keeps every folder: the task kinds (1_data …
      10_evidence), agents, page-types, haipipe-task, haipipe-workflow, haipipe-page-task.
    - haipipe-studio (new): `studio/sNN-<topic>/` at any level, its face and builders that keep marks, the
      numbering (s0x concepts · s1x levels · s2x runs and skills · s3x Guide · s5x server), sessions as passes
      of `run-draw-<sNN>`; takes the scratch mode of excalidraw-report and `canvas.py` · `render_png.py`.
    - haipipe-report (new; JL 261007: "to define the question - work - report workflow in the Audience
      report"): the Question │ Work │ Report row at any level, what each cell reads, how work links to a
      question (`answers:` on a Job or Task face, a need id like `QK10.E1`), the walk open → partial →
      answered (→ checked, proposed), the report Page (Opening · Answer · Evidence · Limits · Next), its
      `## Figures` and drawing; a comments batch is a report kind (b16). haipipe-report keeps the asking.
    - haipipe-run (extended): names without `<MMDD>`, `run.yaml` as the Runs Space reads it, a Run type table
      per Space that names each button's skill.

s21-D02 · Proposed: every frame button names its skill (a `skills:` field on its run type), as the Page's run
    cards already do; `Update the description` → the level's skill, `Add a topic` → haipipe-studio,
    `Write the report` → haipipe-report, `Run` → haipipe-run.

s21-D03 · Decided (261007): Block and Job delivery stay in their level skills (haipipe-block,
    haipipe-job), following the theme's delivery rule; a Page Task's is haipipe-delivery (ref/page-delivery.md)'s. No
    haipipe-delivery until a theme's Block delivery needs more than the level skill holds. Reason: no
    Block or Job delivers anything yet, so a separate skill would have nothing to build.

s21-D04 · Decided (261007): "checked" is not a fourth answer state. The walk stays open → partial →
    answered; the report Page's own CHECK verdict (run-check-<qNN>) is shown beside answered.
    Reason: the walk says where the answer stands, a check judges one version of the Page; one fact
    lives in one place.


s21-D05 · Decided (JL 261010): s21 is drawn as one story, four frames joined by arrows, each with its
    sentence; the reference table sits below the story, off its path. The 261007 tables (the skill folders
    before and after, the update plan) were finished work and stay in history/.
s21-D06 · Decided (JL 261011: "we also need to show what is the skill folder looks like ... in the Tools/
    what are the folders related to this"): a frame under ② shows each skill as its folder in `Tools/`,
    read from disk on every build, with the example's skill (`haipipe-report/`) opened file by file; an
    arrow from ② says "each skill is one folder in Tools/".
s21-D07 · Decided (JL 261012: "yes, rename haipipe-board to haipipe-block"): the Block's skill is named
    after its level, haipipe-block beside haipipe-job and haipipe-task (2.1.0). `aliases: [haipipe-board]`
    keeps the old name working; haipipe-board-reviewer-agent is now haipipe-block-reviewer-agent. The face
    file stays `board.md` for now: renaming it touches every Block and every reader, a separate step.


Read on b00_rawdata (s10, 261012)
---------------------------------

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


Run on Proj01-CGM-RawData (s10, 261012)
---------------------------------------

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


Finding (s21, read 261010, the folders 261011)
----------------------------------------------

42 of 42 buttons name their skill: Block 9 · Job 9 · Task 9 · Page Task 15 (on 261007: 12 of 49), 21
rows once a button is counted once across levels. Every level has a Description button and a Studio
button; the Studio one opens the Block's shared Studio. Work Details is called Work on screen. (An earlier
read showed no Description button: the probe folders had no face; fixed 261010.)

In `Tools/` (261011): the buttons name 15 skills. Five of them are among the seven in
`plugins/haipipe-toolkit/skills/1_base/project/`; `haipipe-report` is in `1_base/project/` and `haipipe-task` in `1_base/task/`; the Page Task's seven draft skills in `1_base/draft/workflow-runs/`, and `haipipe-display`
in `1_base/display/`. Each reaches Claude
through a link, `~/.claude/skills/<name>`. `haipipe-delivery` (0.2.2) is there but no button names it, and
it holds only its `SKILL.md`: the Block's and Job's Delivery buttons name `haipipe-block` and `haipipe-job`
(Open 1).


Built (s21, 261007)
-------------------

✎ 261007 the five skills exist and every frame button names one (phases 1-4); phase 5 moved `canvas.py`,
`render_png.py` and `build_report_drawing.py` into the skills; folder moves went to b04. The full record,
with each phase, is `history/s21_project-run-skill-261007.md (in this folder's history/)`.


Open
----

s10 1. Make the ticked lines in one command (`wb.py update <Block> --keep`), or keep it the agents' step (D07)?
s10 2. b51's register ids are `Q-food-1`, not `QNN`: rename to `QNN` on update, or let the register keep both?
s10 3. b10 had 17 topics on 261012 (13 after the merges), against the suggested 10: does s10 belong in haipipe-project's own design Block?
s10 4. Q-all-6 and Q-all-7 in b51 have no report picture: `studio/_build/build_reports.py`'s ALL has no row for them.
s21 1. s21-D03 kept delivery in the level skills because no Block or Job delivered yet. Now every output is
    stored in Block/delivery/ (s02-D14) and Delivery has its own skill, haipipe-delivery: re-decide D03.
s21 2. What must each level's report answer? The Studio sets it, each level reports (meeting 261010).
s21 3. A Job holds soft Runs only: where does a batch launch, run-launch-<group>, go? (s06 open 2)

s10's Open 5 (the s00 index over 2800 x 1600) is settled: since haipipe-studio 0.13.6 the index is one column,
2720 wide, and only its height grows.

(write here, or mark the drawing in red)
