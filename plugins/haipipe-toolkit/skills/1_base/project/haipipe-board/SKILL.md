---
name: haipipe-board
description: >-
  Owns the Block level: a Block's face `board.md` (title, board-kind, spine, close, optional
  workbench:, Topic, and where its Questions register and resources go), its six Spaces at
  Block level and the buttons it owns there (Update the description, Add a Job, Build the
  delivery), a new-Block scaffold, and how a theme claims a Block (Theme.claims, a
  `workbench:` field) before its Theme folder decides. Use to create a Block, edit or check
  its face, add a Job to it, or say which theme reads it. Trigger: block, new block, board.md,
  block face, spine, close, board-kind, add a job, which theme, claims, /haipipe-board.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-10-07"
  # version history: ./CHANGELOG.md
---

# /haipipe-board · one Block, its face and its Spaces

A Block is one topic in a Project's Theme folder, `bNN_<topic>/`, with its face `board.md`.
It holds Jobs, its shared studio topics, its Questions and their reports, its soft Runs and
its delivery. This skill owns the face and the Block level of the frame; the folder's shape
is `haipipe-project`'s, and each theme adds its words over the face.

```text
<Project>/<theme folder>/bNN_<topic>/
├── board.md             the face: # bNN · <title> · board-kind · spine · close · Topic
├── studio/ reports/     Idea Studio (haipipe-studio) · Audience Report (haipipe-question, haipipe-report)
├── runs/ delivery/      soft Runs (haipipe-run) · what it hands on
└── jNN_<job>/           its Jobs (haipipe-job)
```

**Special boards** (JL 261008: "Paper, Insight, (and Prototype), and Design, these four are the special boards; in
the future, the Labeling will be the same"). A theme's own Board is named by its kind, not `bNN_`:

```text
<Project>/papers/Paper-<Slug>/                 a paper Board          (haipipe-paper)
<Project>/insights/Insight-<name>[-<YYMMDD>]/  an insight Board       (haipipe-insight)
<Project>/tasks/Prototype-bNN-<Topic>/         an insight Prototype   (haipipe-insight)
<Project>/designs/Design-<name>[-<YYMMDD>]/    a design Block         (haipipe-design)
<Project>/labelings/Labeling-<name>/           a labeling Board, later (haipipe-labeling)
```

The name is a label: every reader knows the Block by its `board.md` (its `board-kind:`, or `workbench:`), and its
Jobs and Tasks keep `jNN_` and `tNN_`. A `bNN_<topic>` folder of these themes stays readable; every other theme's
Block is `bNN_<topic>/`. `new_board.py` makes a `bNN_` Block; a special board is made by its theme's scaffold.

Read `ref/board-contract.md` before creating or editing a face: the fields, the six Spaces,
the buttons, which theme reads a Block.

(Not the board skill deleted on 261005, which built a static `board/` site; that site is
retired and never rebuilt. The name is reused for the Block level, b03 s21.)


Create a Block
--------------

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-board/scripts
python $S/new_board.py <Project>/tasks --slug <topic> --title '<title>' [--questions] [--dry-run]
```

1. **Number**: the next free `bNN` in the Theme folder, or `--nn`; a taken one is refused.
2. **Kind**: the Theme folder's default `board-kind`, or `--kind`.
3. **Face only**: `board.md`; no empty folder until its first content.
4. **Questions**: `--questions` adds an empty register; add each with `haipipe-question`.
5. **Check**: `haipipe-project audit <block>` for its shape.


The buttons it owns
-------------------

| Space | Button | Run | does |
|---|---|---|---|
| Description | Update the description | `run-face-<bNN>` | edit the face's fields and Topic |
| Work Details | Add a Job | `run-add-<jNN>` | `haipipe-job`'s `new_job.py <block>` |
| Delivery | Build the delivery | `run-delivery-<target>` | the theme's delivery rule (decided 261007: stays here) |

The other Spaces' buttons are their skills': Idea Studio `haipipe-studio`, Audience Report
`haipipe-question` and `haipipe-report`, Runs `haipipe-run`. The full table, every level:
`haipipe-run`'s `ref/run-types-by-space.md`.


Which theme reads it
--------------------

```text
Theme.claims(block)  ─▶  its Theme folder  ─▶  vanilla
```

A theme that reads a Block by what it holds says so with `claims=` on its `Theme(...)`; the
frame asks every theme's claim before the Theme folder decides. To have a theme read a Block
kept elsewhere, give the face that theme's field (`workbench: <theme>`); never move a Block
only for its screen.


Boundary
--------

| Owner | Owns |
|---|---|
| `haipipe-project` | the Project root, the Theme folders, the ladder's shape and its audit |
| `haipipe-board` | the Block face, its Block-level Spaces and buttons, the scaffold, theme claims |
| `haipipe-job` | the Jobs inside it |
| `haipipe-question` · `haipipe-report` | its Questions register · their reports |
| `haipipe-studio` | its studio topics |
| theme skills | their own Block template and fields over this one (work: `haipipe-task` `ref/block-board-template.md`) |
| `servers/workbench/frame.py` | drawing the Spaces |


Files
-----

```text
haipipe-board/
├── SKILL.md
├── CHANGELOG.md
├── agents/openai.yaml
├── ref/board-contract.md     the face, the Spaces, the buttons, theme claims
├── scripts/new_board.py      the new-Block scaffold
└── tests/test_new_board.py
```
