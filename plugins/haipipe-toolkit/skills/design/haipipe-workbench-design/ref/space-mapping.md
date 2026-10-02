Design workbench: Space to file map and the state fold (Page level)
=====================================================================

This is the Page level of the Design workbench, as served in 0.14.0.
One Design Folder is one design task, so its designs share one aim.
The page has three Spaces: Design Goal, Design, and Delivery
(input, process, output). It is served by `servers/workbench-design/design.py`
at `/_board/design?path=<board.md>&file=2-Design/<folder>/<folder>.md`.
`design-board-space-mapping.md` is the same map one grain up.


The three Spaces
----------------

| Space (tab, `space=`) | Reads | Shows | Writes through |
| --- | --- | --- | --- |
| Design Goal Space (`goal`) | the board's `design-goal.md` beside `board.md`; the venue profile `skills/design/venue/venue-<venue>/README.md`; the Brief line whose `folder` names this folder (`0-BR-brief/*/BR00-brief.md`); the register's acceptance lines | the design task in one sentence (N venue designs for who), then the design input as column tables: Aim, Venue, Rules, Resources, Leave out | `haipipe-design-brief` (the Brief and `design-goal.md`), `haipipe-design` (the register) |
| Design Space (`design`) | the register `draft/<stem>-design-items.md`; its `evidence:` lines and the pages they name; `runs/run-design-*.yaml`; `results/*/runtime.yaml`, `result.yaml`, Commission `decision.yaml`, checks; the candidate Result's `render_manifest` | the task block, then one card per design, with its two folds and its buttons; declined items folded after the live ones; the records check | `haipipe-design` (register), `haipipe-design-workflow` (Commission, Generate, Verify) |
| Delivery Space (`delivery`) | the register (id, title); each item's candidate whose independent Verify passed; its `render_manifest` | each ready design word for word, or a folder of screens as pictures; declined items folded; the task csv link | none (read only) |

**Design Goal Space.** `design-goal.md` has five blocks: Aim, Venue, Rules,
Resources, Leave out. Each block is a title underlined with `---` or `===`.
Each line is `key: value <- source`. A value of `?` shows as "not stated".
A section titled `Task · <folder>` overrides a line for this one folder.
The Venue table shows the venue profile default beside this task's value.
The defaults are the `- **Key:** value` lines under the profile's
`## Constraints`. Aim adds "their job" and "how many" from the Brief line:
wanted, registered, ready, and declined when above 0. Rules adds the
acceptance lines every live design keeps. The Brief line is the first
Markdown table whose header names `audience`, `job` and `venue` together.
Its `designs` and `folder` columns are matched by header word.
When designs are missing, the Space offers "Ask the agent to draft the
missing N" (action `draft-request`). An open request shows instead.

**Design Space.** The task block comes first: who, their job, the venue,
how many, and the rules every design keeps. Then one card per design.
The card is named "Design N"; the files say `ITEMNN`. Its closed row has
three columns, and the open card keeps them:

- Design: number, title and state; open, the SMS and its Design Runs.
- Rationale: what it rests on; open, the design move, the Evidence chain from the
  `because:` rows, and the Design elements with what supports each.
- Evaluation: the acceptance count; open, Acceptance, Review notes and Expected effect.

An opened card shows the design on the left, kept in view. An SMS shows
as a bubble on a phone; a screen shows as its picture. The right side
explains it: why this design, because, from insight to design, the bet,
and the rules (pass or fail). Each card holds two folds:

- **Insight pages · N**: the register's `evidence:` lines and the pages they
  name. Per page: label and title, `signed:`, and what it says (the Design
  Handoff `FINDING`, then `CONSEQUENCE`, and the DO / DO NOT rules it
  implies), and whether the run record pins it. An item built on evidence
  with no page named shows a red line.
- **Runs · N**: every Run of the item, with Run type, who, when, status,
  outcome (verdict n/m) and next. Checks, feedback and draft text fold
  inside. Failed runs and fail verdicts show red; superseded runs grey.

The buttons sit under the design. The item's state licenses them:
**Release commission** and **Hold** (a person, with a name and one
sentence), **Queue Generate · agent**, **Queue Verify · independent agent**,
**Queue revise · agent** (with feedback), and **Queue again** for a stale
queued Run. They post to `/_board/design-act`. An eligible item also has
**Copy prompt to chat**; copying only changes the clipboard. "open all"
and "close all" fold every card. There is no bar that acts on every item.

**Delivery Space.** One row per design whose independent Verify passed:
the text word for word, with the `{LINK}` slot placed where the system puts
the link. A folder of screens shows as a picture gallery. A declined item
folds under "Declined, kept for the record · N". The link
"↓ This design task's designs · N · csv" is
`/_board/design-bundle?path=<board.md>&folder=<folder>`. Verify pass means
ready for Delivery. Receipts stay in the card's Runs fold.

**Header.** `Page level · <folder> · ↑ Board level`. A red line shows only
for a legacy folder or a blocked Insight binding.


The Runs panel
--------------

Every Space has a Runs panel on the right. It is the shared panel the
Paper and Page workbenches use (`live.runs_panel`). Its run types come from
`skills/design/haipipe-design-workflow/references/run-cards.md`. Each card
names a button, an agent, a skill, what the person signs, and a prompt.
The Workbench Table is `ref/workbench-table.md`; the cards and the table
must agree. The panel lists each matching run below its type, matched by
the card's pattern `run-design-(commission|generate|verify)-*`. Delivery lists
only runs whose outcome is pass. The panel starts nothing. **Copy** hands
the prompt to a Claude or Codex session.

Page cards: Frame the aim, Pin the venue, Set the rules, Gather resources,
Set what to leave out (Goal); Map variables, Add a design, Commission,
Generate, Verify (Design); Passed review, Plan the test (Delivery).


Plain words
-----------

| in the files | on the screen |
|---|---|
| `roster` | the Brief, a line of the Brief |
| `handoff` | signed insight |
| Ticket | run record |
| candidate | draft |
| `check_unit` | records check |
| `intent` / `move` | goal |
| `ITEM02` | Design 2 |
| stance | follows the evidence / challenges the evidence / explores a new direction / a new design |
| basis | built on evidence / from the brief only |
| mode | never on screen; it stays in the files |
| `FW01` (an insight page's file id) | its label and title, `full-W01 · Send salience` |
| `R1` (a Brief line id) | the task's full name, `<job> <venue> for <who>` |

The contract word never appears beside its plain word, in parentheses or
otherwise.


State fold
----------

Walk an item's Runs in `sequence:` order; the last row wins. A superseded Run is
skipped.

| Run seen | status / outcome | item state | waiting on |
|---|---|---|---|
| none | | not commissioned | you · commission |
| Commission | no decision yet | commission open | you · release or hold |
| Commission | release | commissioned | you · queue the draft |
| Commission | hold | commission held (a new release decision is offered) | you · release or hold |
| Generate | planned | generate queued | agent · generate |
| Generate | planned, a pinned file changed since | queued run out of date | you · queue again |
| Generate | running | generating | agent · running |
| Generate | complete | generated | you · queue the review |
| Generate | failed (the draft failed the records check) | generate failed | you · queue a revise |
| Verify | planned | verify queued | agent · verify |
| Verify | planned, a pinned file changed since | queued run out of date | you · queue again |
| Verify | running | verifying | agent · running |
| Verify | complete · pass, exact Result pins still valid | ready | none |
| Verify | previously passed, candidate or review records changed | records invalid | you · inspect the named records |
| Verify | complete · unresolved | verify unresolved | the named owner · resolve the gap |
| Verify | complete · fail | verify failed | you · queue a revise |
| Verify | failed (the review itself failed the records check) | verify invalid | you · queue the review again |
| any | blocked | blocked | you · resolve `<Run id>`: `failure:` |

A step that needs a click says "you", never a name. "agent" is waited on
only while a Run is queued or running. A blocked Run shows its reason and
repair owner, never a Release button. A worker hold diagnostic is not a
human Hold decision. Each Run's `results/<stem>/runtime.yaml` is its
receipt. Historical `run-design-adopt-*` records stay readable under their real
ids: adopt reads as ready, decline as declined. Current writers never
create them, and the server refuses the old Adopt actions.


Query aliases
-------------

`?space=` accepts `goal | design | delivery` (default `goal`). Old values
still resolve: `frame, plan, brief, ask` open Goal; `intent, draft, items`
open Design; `insight, signal, evidence, insights` and `run, runs, shape,
workflow, runtime, create, review` open Design (the retired Insight and
Run Spaces); `launch, commit` open Delivery. `?item=ITEM02` opens that
card in Design Space, marks it, and scrolls to it. After a button click the
page lands back on Design Space at that item; a draft request lands on
Design Goal Space. The retired `?flow=` parameter is ignored.


Retired
-------

Retired in 0.14.0, kept here in one line each so old notes read right:

- Insight Space and Run Space: their content is the card's two folds.
- Five Spaces: the page has three.
- The "Run types in this Space" guide: replaced by the Runs panel.
- The "New Design Item" form: a design is added from the Runs panel.
- The Insight board line in the header.
- Content hashes: the csv has no hash column.
