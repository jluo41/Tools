---
name: haipipe-plugin-design-board
description: >-
  The Board-level grain of the Design plugin: one 🎨 Design Board surface over
  a whole DesignBoard, in the same five Spaces as the Page level, one grain
  up. Goal Space is the list of design tasks from the Brief (who, their job,
  venue, how many, which Insight board, folder, status) with the form that
  adds tasks; Design Space is every Design Item; Insight Space is every
  signed page the programme draws on and who uses it; Run Space is who is
  waited on and every Run; Delivery Space is every adopted draft. Two writes:
  add design tasks to the Brief (and open their folders), open a Design
  Folder for one line. Trigger: design board, board-level design, design
  tasks, all design items, who is waiting, /haipipe-plugin-design-board.
metadata:
  version: "0.5.0"
  last_updated: "2026-09-16"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-design-board · the same plugin, one grain up

**LOAD `haipipe-plugin` and `haipipe-plugin-design` FIRST.** The Page-level
skill owns the Design Item, the register grammar, the state fold, the plain
words, and every action on one folder. This skill owns only what changes when
the reader steps up to the Board: the list of design tasks, the stack of
folders, the boards the programme draws on, and the cross-folder queue.

```text
🎨 Design, two grains of one plugin
├── Board level   /_board/design-board?path=<board.md>      this skill
│                 Goal · Design · Insight · Run · Delivery, across every folder
└── Page level    /_board/design?path=<board.md>&file=2-Design/<Design-NN-…>/<Design-NN-…>.md
                  Goal · Design · Insight · Run · Delivery, for one folder, with the buttons
```

Every Board-level row links down to the Page-level card it summarizes; the
Page-level header links back up. Nothing is stored twice: the Board level is
`design_snapshot` called once per folder and stacked.

## Plain words and full names

`Space` is the only reader-facing word (JL 260916), and every word on the
surface must be understood at first glance: "the Brief" and "a line of the
Brief", never roster; "signed insight", never handoff; "draft", never
candidate; "records check", never check_unit. Steps are Commission,
Generate, Verify, Adopt. Folders carry their full name: the group is
`2-Design/` and each Design Folder is `Design-NN-<audience>-<job>-<venue>/`
(the Board engine's `Design-` page branch), never `DS`.

## The five Spaces at board grain

**Goal Space** answers "what has this programme promised to design, and is
each promise started?" It is the list of design tasks read from the Brief:

```text
Design tasks · from the Brief
line  who                              their job            venue    how many                              insight board     folder                              status
R1    full SMSR2 population            prescription review  sms      10 wanted · 2 registered · 1 adopted  (board default)   Design-01-patient-confirm-sms       1 adopted · 1 verified
R2    patients with a refill due …     refill review        ui-card  1 wanted · 1 registered · 0 adopted   (board default)   Design-02-refill-reminder-ui        1 verified
R3    young male, age 35 or under      prescription review  sms      1 wanted                              (board default)   —                                   no folder yet  [New Design Folder]

▸ New design tasks   subgroups (one per line) · their job · venue · how many · insight board · open folders
Insight board
DesignPlugin-Demo-260916-InsightBoard · 1 of 1 insights signed
```

The list is the first Markdown table in the Brief page under `0-BR-brief/`
whose header names `audience`; `job`, `venue`, `designs`, `insight`, and
`folder` columns are matched by header word. `designs` is how many designs
the line asks for; `insight` names the Insight board the line draws from
(empty means the board's `reads:`); a folder cell of `—` is a promise not yet
kept. A folder on disk that no line names is listed as "folders the Brief
does not list". The header counts the whole programme: tasks · wanted ·
registered · adopted · waiting on the person · waiting on the agent.

**Design Space** is every Design Item across folders in one table: folder,
item, design, state, who is waited on.

**Insight Space** is every Insight board the programme draws on (the board's
`reads:` plus any board a Brief line names), and on each: its signed pages,
who signed, what the page says (its Design Handoff `FINDING`), the rules it
implies (its DO / DO NOT counsel lines), and which folder · item uses it. A signed page no item uses shows "no item yet"; an
unsigned page shows in red.

**Run Space** answers "who is the programme waiting on, and what ran last?"
First the queue: every item that waits, the person's rows first (`JL · adopt`),
then the agent's (`agent · verify`). Then every Run across folders, newest
first, with folder, step, actor and mode, status, outcome. It ends with the
records check across folders.

**Delivery Space** answers "what has this programme actually adopted?" One
card per adopted item (folder · item · text · draft hash · verifier · words ·
adopter · time), then one line naming the items not adopted and why. At the
top, **↓ Download the bundle**: `GET /_board/design-bundle?path=<board.md>`
returns one csv row per adopted draft (line · who · their job · venue ·
folder · item · title · text · sha256 · draft run · verified by · adopted by
· when · words), the hand-off a send system needs. The static twin has no
bundle link.

## The two Board-level writes

Both go through `POST /_board/design-board-act {path, action, …}`; neither
exists on the static `board/design.html`.

**`add-tasks`** `{subgroups, job, venue, designs, insight, open}` adds one
line per subgroup to the Brief's list (ids continue `R<N>`; the `designs`,
`insight`, and `folder` columns are added to the table if the Brief lacks
them, and the section is created if the Brief has no list yet), and, when
`open` is yes, opens a Design Folder for each new line. "5 subgroups, 10
messages each, from Insight board X" is one submission. Refused with one
plain sentence when no subgroup, job, or venue is given, when `designs` is
below 1, or when the named Insight board is not found beside this board;
a refusal writes nothing.

**`new-folder`** `{row}` opens a Design Folder for one line whose folder
cell is empty:

```text
2-Design/Design-NN-<audience>-<job>-<venue>/
├── Design-NN-….md                          folder-kind: design · Opening from the line, how many the Brief asks for
└── outline/Design-NN-…-design-items.md     empty register with its header
```

and writes the folder's name into that line's `folder` cell. Those cells and
lines are the only Brief edits this plugin makes; the Brief's prose, needs,
and signed inputs stay with `haipipe-design-brief`. Every other action
(register a Design Item, release a Commission, queue Generate/Verify, adopt)
lives on the Page level and is reached by the link in the row.

## Reads (and owns nothing)

```text
board.md                                title · reads:
0-BR-brief/BR00-brief/BR00-brief.md     the list of design tasks
2-Design/*/<Design-NN-…>.md             each Design Folder, through design_snapshot
<Insight board>/…                       signed pages, through the Insight plugin's records
```

A legacy folder (`design/DU*`, `rNN_design_*`, PageX, v1) appears on its
Brief line with its refusal reason and no items, exactly as the Page level
says it; the Board level never reads it either.

## Boundary

Apply to a Board whose `board.md` says `board-kind: design-board`, whose
folder name ends in `-DesignBoard`, or which holds `2-Design/`. A link that
names no DesignBoard lands on a list of the DesignBoards under the server
root, never on a dead end.

## Reader contract

From the Board level alone, the reader can answer:

1. What has the programme promised to design: for whom, on which venue, how
   many, from which Insight board, and is each promise started?
2. Every Design Item across the board, in one table, with its state.
3. Which signed insights exist, what they say, and which items use them.
4. Who is the programme waiting on right now, person or agent, for which item?
5. What ran most recently, where, by whom, with what outcome?
6. What is adopted, and what is not, board-wide?

See `ref/space-mapping.md` for the Space ↔ file map at board grain.
