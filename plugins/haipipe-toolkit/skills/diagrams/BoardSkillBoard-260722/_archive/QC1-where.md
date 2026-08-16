# Where a board lives
state: ✅ SETTLED
owner: JL
method: task, project, and paper boards live under "<owning unit>/diagram/"; plugin skill-design boards share "<plugin>/skills/diagrams/"; the Board skill ships from its first-class board/ family

## Question
Where in the repo does a board's folder go, and how is it named?
The working answer has two explicit locations: a task, project, or paper uses `<owner>/diagram/`, while plugin skill-design Boards share `<plugin>/skills/diagrams/`; both use `<NN>-<topic>-<YYMMDD>`, dated on the day the Board opens and never renamed.
What turns on it is everything that points at a board: the relative paths in `## Links`, and whether a dozen boards spread across owners can be found at all.

It is hard because boards serve all kinds of owners (a plugin, a task folder, a paper), so there is no single "all boards go here" place.
Leave it and Boards will multiply and get assigned to collaborators, and once locations and names drift, nothing can be found and no other document can point at a Board reliably.
It reaches downstream to the relative paths in `## Links`, and to the directory structure when boards are shared out later (`QE1`).

## Boundary
- ✅ Covered here
  **Where the folder goes and what it is named**: under whose name it hangs, how number and date are assigned.
- ↪ Covered elsewhere
  What is **inside** the folder: that is `QA1`.
  Nor what the index page looks like: that is `QC2`.

## Diagram

```
skills/
├── diagrams/                   ← design boards: working artifacts, change daily
│   └── BoardSkillBoard-260722/
│         number  topic    date
└── board/                      ← first-class Board family
    ├── agents/
    └── haipipe-board/          ← the skill: the deliverable package
        SKILL.md  build.py  ref/

task / project / paper: <owning unit>/diagram/<NN>-<topic>-<YYMMDD>/
plugin skill design:    <plugin>/skills/diagrams/<NN>-<topic>-<YYMMDD>/
NN:                     sequence within one topic series; unrelated topics may each start at 01
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722/fig/board.excalidraw&frame=QC1

## Items to Finish
- [x] Decide where this board lives
- [x] Decide where the next board lives
- [x] Naming rule settled: the name alone identifies the board

## Where we are
JL has ruled: task, project, and paper Boards live under the **owning unit's `diagram/`**.
Boards that design skills inside one plugin use that plugin's shared **`skills/diagrams/`** collection.
This board lives at `Tools/plugins/haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722/` (JL moved it there on 260726, from the former `0_utils/diagram/`).

```
skills/
  diagrams/                 ← every board in this plugin lives here
    BoardSkillBoard-260722/ ← this board
    ../PaperSkillBoard-260725/
  board/                    ← first-class family beside paper, probe, and task
    agents/                 ← thin, clean-context Board roles
    haipipe-board/          ← the skill itself (the deliverable package)
      SKILL.md  build.py  ref/
```

The plugin-specific rule is that skill-design Boards are collected in one `diagrams/` folder at the plugin's skill root rather than nested inside the skill folder they describe.
The reason for keeping them apart from the skill has not changed: a board is a working artifact that changes daily, and a skill is a package that ships.
What did change is that boards belonging to different skills are now neighbours instead of scattered, so the plugin has one place to look.
The move also broke every relative path in `## Links`, because the folder is one level shallower than before; those were re-resolved the same day.

On 260726 JL promoted the delivery package itself from `0_utils/haipipe-board/` to `board/haipipe-board/`.
The design Board did not move.
The new `board/` level is a product-family boundary, parallel to `paper/`, `probe/`, and `task/`; it contains the callable skill and family-level agents, not the working design Board.

The rule solved something that had never been thought through: **a board is a working artifact, a skill is a deliverable package**: they do not belong in one folder.
This board used to sit inside `haipipe-board/diagram/`, which effectively shipped a daily-changing work log inside the skill.

The name stays `number-topic-date` (`BoardSkillBoard-260722`), number first, date last.
The date is fixed on opening.
The number orders Boards within one topic series: a new topic starts at `01`, while a later Board for the same topic advances to `02`; it is not a repo-wide or collection-wide unique number.

## Files
- `ref/board-form.md`
  §1 folder: location and naming rules live there.
- `SKILL.md`
  The first line of the "🗂 Shape" section (owning unit = whom this board serves).
- `board-family/`
  The first-class family containing the callable skill and shared Board agents.
- `board-agents/`
  Thin, clean-context roles owned by the Board family.

## Glossary
owning unit: the task, project, paper, or plugin a Board serves.
Task, project, and paper Boards use that unit's `diagram/`; plugin skill-design Boards use the plugin's shared `skills/diagrams/`.

## Discussion
> JL: this board should be at `Tools/plugins/haipipe-toolkit/skills/0_utils/diagram`
>> CC0722: moved. `haipipe-board/` keeps only the skill itself (`build.py` + `ref/`). The rule is recorded in "Where we are" above.
> JL: Promote Board beside paper, task, and probe, but leave the design Board in the shared `diagrams/` folder.

## Log
260726 · promoted the delivery package from `skills/0_utils/haipipe-board/` to the first-class `skills/board/haipipe-board/`; the design Board stayed at `skills/diagrams/BoardSkillBoard-260722/`
260726 · opening lead widened to three lines (JL: the openings are too short; say the question, how it is answered, and what turns on it)
260726 · JL moved every board to `skills/diagrams/`: this one from `0_utils/diagram/BoardSkillBoard-260722/`, alongside `../PaperSkillBoard-260725/`. The folder is one level shallower, so all 21 declared paths in `## Links` were re-resolved against the new location and verified to exist; `SKILL.md` and `ref/board-example.md` had their live pointers repointed
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 0919 · Renumbered Q7 → QC1; state → ✅ SETTLED, 3/3
260722 2249 · JL ruled: boards under the owning unit's diagram/, apart from the skill itself; this board moved on the spot
260722 2240 · Opened with a single hard requirement from JL: the name is "number-topic-date"
