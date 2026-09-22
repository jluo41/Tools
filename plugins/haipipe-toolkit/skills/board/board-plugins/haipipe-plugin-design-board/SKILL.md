---
name: haipipe-plugin-design-board
description: >-
  The Board-level grain of the Design plugin: one 🎨 Design Board surface over
  a whole DesignBoard, in the same five Spaces as the Page level, one grain
  up. Goal Space is the list of design tasks from the Brief (who, their job,
  venue, how many, which Insight board, folder, status) with the form that
  adds tasks; Design Space is every Design Item; Insight Space is every
  signed page the programme draws on and who uses it; Run Space is who is
  waited on and every Run; Delivery Space is a quick list of every design. Two writes:
  add design tasks to the Brief (and open their folders), open a Design
  Folder for one line. Trigger: design board, board-level design, design
  tasks, all design items, who is waiting, /haipipe-plugin-design-board.
metadata:
  version: "0.7.2"
  last_updated: "2026-09-21"
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
candidate; "run record", never Ticket; "records check", never check_unit; no
DU and no Brief line id such as `R1`. An insight page shows as its label and
title (`full-W01 · Send salience`), never its file id `FW01`; the file keeps
`FW01` (JL 260918). The Workflow is a list of Runs: Commission,
Generate and Verify. Delivery is their ready projection; internal Steps do not
add Runs. Folders carry their full name: the group is
`2-Design/` and each Design Folder is `Design-NN-<audience>-<job>-<venue>/`
(the Board engine's `Design-` page branch), never `DS`; each part is the first three content words of that Brief cell, filler words
(with, within, a, the, of, for, or, under, …) dropped, so the name says the goal:
`Design-01-all-patients-prescription-review-sms`. A renamed folder keeps
its `Design-NN` number, and an old link finds it by that number.

## The five Spaces at board grain

Each Space includes the Design family's folded **Run types in this Space**
guide: plain name and canonical Type, bounded purpose, owner and worker
Skills, actor and prerequisites. The type catalogue is separate from a list
of current matching records, scoped by folder/item and showing each actual
Run's id, actor, status and outcome. Goal covers Commission; Design/Insight/Run
cover Commission, Generate and Verify; Delivery covers Generate/Verify for
ready items only. The historical Run ledger remains complete.

For Design Runs, Board guidance says **Shown here · read-only**, or
**Copy request → paste and send** for eligible worker work in Design Space.
Each Design Item has an expandable next-Run explanation using that folder's
human context and an **Open item controls** link to its Page-level Design
Space. There, eligible native controls say **Start here**. Commission belongs
to a person, Generate to an agent, and Verify to an independent agent, under
`haipipe-design-workflow`; Generate/Verify workers use `haipipe-design-unit`.
Each eligible item has **Copy prompt to chat** and a reviewable prompt using
its own Folder/Page/item context. It covers a new Generate/Verify or reuse of
one compatible queued Run, with its exact id, Commission and receipt paths.
Copy only changes the clipboard; the person must paste and send in chat.
The prompt rereads state, prevents duplicate allocation, preserves the human
Commission and independent Verify gates, and reports the resulting Run/receipt.
No prompt is offered for running, stale, blocked, unresolved, invalid, ready,
retired or static states, folder audit findings, missing/blocked Insight
bindings, or Commission decisions. Revisions become copyable only after the
native queue form pins feedback and base. Run and Delivery Spaces stay
read-only. Existing task-list/folder writes do not become Design Runs.

**Goal Space** answers "what has this programme promised to design, and is
each promise started?" It is the list of design tasks read from the Brief:

```text
Design tasks · from the Brief
design task                                               how many                               insight board     folder                                               status
Prescription review SMS for all patients                  10 wanted · 10 registered · 1 ready  (board default)   Design-01-all-patients-prescription-review-sms       1 ready · 9 generated
Refill review app card for patients with a refill due …   1 wanted · 1 registered · 0 ready    (board default)   Design-02-patients-refill-due-refill-review-ui-card  1 generated
Prescription review SMS for young male, age 35 or under   1 wanted                               (board default)   —                                                    no folder yet  [New Design Folder]

▸ New design tasks   subgroups (one per line) · their job · venue · how many · insight board · open folders
Insight board
DesignPlugin-Demo-260916-InsightBoard · 1 of 1 insights signed
```

Each task shows by its full name, `<job> <venue> for <who>` (the folder page's
title), linked to its Page level; the Brief's row id (`R1`) is a key in the
file and never a name on screen (JL 260918).

The list is the first Markdown table in the Brief page under `0-BR-brief/`
whose header names `audience`, `job` and `venue` together (an audience table
elsewhere in the Brief is never read as the list); `designs`, `insight`, and
`folder` columns are matched by header word too. `designs` is how many designs
the line asks for; `insight` names the Insight board the line draws from
(empty means the board's `reads:`); a folder cell of `—` is a promise not yet
kept. A Brief with no `line` column still works: its rows are numbered R1,
R2 … in order, as keys in the file, never names on screen. A folder on disk
that no line names is listed as "folders the Brief does not list".

The header above the Spaces is one line that counts the whole programme,
`Board level · 3 design tasks · 12 wanted · 11 registered · 1 ready ·
waiting on JL: 10 · on agent: 0`; a red line is added only when the records
check has findings.

**Design Space** is every Design Item across folders in one table: folder,
item, design (the title, with the design text in one line under it), state,
who is waited on.

**Insight Space** is every Insight board the programme draws on (the board's
`reads:` plus any board a Brief line names), and on each: its signed pages,
each by its title with its label under it, who signed, what the page says
(its Design Handoff `FINDING`), the rules it implies (its DO / DO NOT counsel
lines), and who uses it, grouped per folder (`Design-01 · 6 items`, linked to
that folder's Insight Space). A signed page no item uses shows "no item yet";
an unsigned page shows in red. A second table, "Other pages the designs use
(not signed insights)", lists every other page an item rests on, so nothing
an item uses is hidden. When no design rests on a signed insight, a red line
says so at the top.

**Run Space** answers "who is the programme waiting on, and what ran last?"
First the queue: every item that waits, the person's rows first (`JL · queue the review`),
then the agent's (`agent · verify`). Then every Run across folders, newest
first, with folder, original Run ID, Run type, actor and mode, status, outcome.
The queue names the next action; it does not allocate a Run. Historical
`rdNN_adopt_*` IDs remain unchanged in text, links, and tooltips, with their
Run type labeled `Adopt (historical)`. It ends with the
records check across folders.

**Delivery Space** answers "what designs do we have?" One heading per
folder (its title, linked to the folder's Delivery Space), then one table,
one row per item: item (id, linked to its card, and title) · design (the
exact draft whose independent Verify passed; failed or unverified drafts are
never listed). Hashes and receipts stay in Run Space. A folder of
screens shows as a picture gallery instead of the table. A declined item
leaves the list and is folded under "Declined, kept for the record · N". At
the top, **↓ Download all designs**: `GET /_board/design-bundle?path=<board.md>`
returns a csv with one row per ready item, columns `line, who,
their_job, venue, folder, item, title, state, text, draft_run, sha256,
render`. Every row has `state=ready` and identifies the exact verified draft.
If the candidate or its review records no longer validate against the current
files, the item shows `records invalid` and is excluded from ready counts and CSV.
This is a design handoff, not authorization to send; downstream owners decide
distribution. Failed, unverified and historically declined items are excluded. The
static twin has no download link.

## The two Board-level writes

Both go through `POST /_board/design-board-act {path, action, …}`; neither
exists on the static `board/design.html`.

**`add-tasks`** `{subgroups, job, venue, designs, insight, open}` adds one
line per subgroup to the Brief's list (ids continue `R<N>`; the `designs`,
`insight`, and `folder` columns are added to the table if the Brief lacks
them, and the section is created under a `### What to design` heading if the
Brief has no list yet), and, when `open` is yes, opens a Design Folder for
each new line. "5 subgroups, 10 messages each, from Insight board X" is one
submission. The form's Insight board picker offers only names that resolve
to an Insight board, each shown by its folder name. Refused with one plain
sentence when no subgroup, job, or venue is given, when `designs` is below 1,
or when the named Insight board does not resolve from this board (a sibling
name, or a relative path as on `reads:`); a refusal writes nothing.

**`new-folder`** `{row}` opens a Design Folder for one line whose folder
cell is empty. `row` is the parsed Brief row key returned by the snapshot,
such as `R3`; it is neither the row's display title nor an integer position.
For example, submit `{"row":"R3"}` for the row whose `id` is `R3`:

```text
2-Design/Design-NN-<audience>-<job>-<venue>/
├── Design-NN-….md                          the page (below)
└── outline/Design-NN-…-design-items.md     empty register with its header
```

The page passes the board checker from the start: `folder-kind: design`,
`state: 🔴 OPEN · no design registered yet`, `owner:` (the board's owner,
else the Brief's), and an Opening question, "Which N `<job> <venue>` designs
should we make for `<audience>`?". The plugin writes the folder's name into
that line's `folder` cell and lists the page in board.md's `## Pages`, under
its Design heading when there is one. A second click on the same line is
refused because the line already names its folder; refusals name the task by
its full name, never by `R3`. Those cells and lines are the only Brief edits
this plugin makes; the Brief's prose, needs, and signed inputs stay with
`haipipe-design-brief`. Every other action (register a Design Item, release a
Commission, queue Generate/Verify) lives on the Page level and is
reached by the link in the row.

## Reads (and owns nothing)

```text
board.md                                title · reads: · owner:
0-BR-brief/BR00-brief/BR00-brief.md     the list of design tasks
2-Design/*/<Design-NN-…>.md             each Design Folder, through design_snapshot
<Insight board>/…                       signed pages, through the Insight plugin's records
```

`reads:` names each Insight board by its sibling folder name, or by a `../`
path that stays inside the checkout, for a board in another Project (first
use: `B01_DesignBoard-AuthenUI-260917` reading
`../../Project-Application-SMSDesign/applications/A00_InsightBoard-SMSR2v1-260821`).
The board checker (`cli/check.py`) accepts both forms.

A legacy folder under `2-Design/` (`design/DU*`, `rNN_design_*`, PageX, v1)
appears on its Brief line with its refusal reason and no items, exactly as the
Page level says it; the Board level never reads it either. A `2-DS-design/DS*`
folder lies outside `2-Design/` and is not read at all. Park such a folder
under the board's `_archive/` and take its row out of `board.md` `## Pages`:
the checker judges no `_` folder, so the record keeps its bytes without asking
the board to migrate it, and only the live design tasks stay on the board.

## Boundary

Apply to a Board whose `board.md` says `board-kind: design-board` (the board
checker knows `design-board` and `insight-board` as kinds), whose folder name
carries `DesignBoard` as a `-` or `_` separated token (`RefillFraming-DesignBoard`,
`B01_DesignBoard-AuthenUI-260917`), or which holds `2-Design/`. The board
checker audits every folder that holds Design runs, including a folder with
only Commission Runs. Historical `rdNN_adopt_*` decisions remain readable for
audit, under their real ids and labeled historical; current writers do not create them.

A bare `/_board/design-board` opens the server's only DesignBoard, or, with
several, answers 200 with a list of them; a link that names no DesignBoard
answers 404 with the same list, never a dead end. A Page-level short link
`/_board/design?folder=Design-01` that fits several boards answers 404 with a
page listing each board holding that folder, one link each, never a guess;
`Design-1` reads as `Design-01`.

## Reader contract

From the Board level alone, the reader can answer:

1. What has the programme promised to design: for whom, on which venue, how
   many, from which Insight board, and is each promise started?
2. Every Design Item across the board, in one table, with its state.
3. Which signed insights exist, what they say, which items use them, and
   which other pages the designs rest on.
4. Who is the programme waiting on right now, person or agent, for which item?
5. What ran most recently, where, by whom, with what outcome?
6. Which exact drafts are ready for Delivery, board-wide? (ready counts and CSV)

See `ref/space-mapping.md` for the Space ↔ file map at board grain.
