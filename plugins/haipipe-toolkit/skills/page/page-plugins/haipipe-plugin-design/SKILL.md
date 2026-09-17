---
name: haipipe-plugin-design
description: >-
  The page-folder Design plugin: one 🎨 Design tab over a current Design
  Folder, read in time order across five Spaces. Goal Space is the ask (venue,
  who, their job, how many designs, which Insight board); Design Space is the
  Design Items with their goal, expected outcome, rules, state, and buttons;
  Insight Space is the supporting evidence per item (signed insights, what
  they say, what is still needed); Run Space is each item's Commission →
  Generate → Verify → Adopt timeline; Delivery Space is the adopted draft per
  item with its exact hash and the person's words. It reads only contract
  files and routes every write to the owning Design skills. Trigger: design
  plugin, design tab, design items, design folder, goal space, insight space,
  /haipipe-plugin-design.
metadata:
  version: "0.9.0"
  last_updated: "2026-09-16"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-design · one Design Folder in five Spaces

**LOAD `haipipe-plugin` FIRST.** It owns the shared Page Plugin contract. This
skill owns the Design category's delta: the Design Item as the row of the
page, the five Spaces that show it in time order, the contract files each
Space reads, and where a user action is routed.

## Two grains, one plugin

This skill is the **Page level**: one Design Folder. The **Board level**,
`haipipe-plugin-design-board` (`/_board/design-board`), stacks every folder's
snapshot one grain up: the Brief's lines against the folders that exist,
every Design Item with who it waits on, every Run newest first, everything
adopted. Board rows link down to the cards here; this page's header links
back up. Nothing is stored twice.

Short links, for typing or pasting: `/_board/design-board` opens the server's
only DesignBoard, and `/_board/design?folder=<Design-NN-…>[&space=…]`
redirects to this folder's full `path=` and `file=` link.

## Plain words on the surface (JL 260916)

Every word a reader sees must be understood at first glance. `Space` is the
only word for a plugin surface. Steps are called by their Run words and
nothing else: **Commission, Generate, Verify, Adopt**. On screen the contract
words are translated and the contract word, where it matters, follows in
parentheses:

| in the files | on the screen |
|---|---|
| `roster` | the Brief, a line of the Brief |
| `handoff` (a signed Wisdom page) | signed insight |
| Ticket | run record |
| candidate | draft |
| `check_unit` | records check |
| `intent` / `move` | goal |
| `stance follow · basis evidence-informed` | follows the evidence · built on evidence (follow · evidence-informed); `mode` stays in the files |

Ids are `ITEM01`, `ITEM02` (never `DI`, which reads as the Insight plugin's
Data → Information). Run slugs follow the id: `rd02_generate_item01`.

## The five Spaces, in time order

```text
🎨 Design
├── Goal Space       what we want: venue · who · their job · how many · which Insight board
├── Design Space     what we will make: one card per Design Item, with its buttons
├── Insight Space    what supports it: per item, the signed insights, what they say, what is missing
├── Run Space        what happened: per item, rd01 commission → rd02 generate → rd03 verify → rd04 adopt
└── Delivery Space   what we ship: per adopted item, the exact draft, its hash, the verifier, the words
```

The header is one line, `Page level · <folder> · ↑ Board level`. A red line
is added only when something blocks the work: the folder is legacy, or the
Insight board's page is unsigned. Nothing else lives in the header.

**Goal Space** reads the line of the Brief that names this folder
(`0-BR-brief/*/BR00-brief.md`, the first table whose header says `audience`,
columns matched by header word: `audience`, `job`, `venue`, `designs`,
`insight`, `folder`) and says the ask in one sentence:

```text
┃ 2 sms designs for full SMSR2 population, unconditioned, prescription review
venue      sms
who        full SMSR2 population, unconditioned
their job  prescription review
how many   2 wanted · 2 registered · 1 adopted
from       BR00-brief.md · line R1
Insight board
DesignPlugin-Demo-260916-InsightBoard · 1 of 1 insights signed
```

`designs` is the number the Brief asks for; `registered` and `adopted` are
counted from the register and the adopt decisions. The Insight board is the
one the line's `insight` cell names, else the owning board's `reads:` line;
a named board that is not found beside the DesignBoard shows in red. With no Brief line the Space says so
and names the file that would fill it; with no Insight board it says the
folder designs from the Brief only.

**Design Space** is one card per Design Item. A Design Item is one design
target with its own rules: one SMS, one UI card, one message pool. It plays
the role on a Design Folder that an Evidence Item plays on an Outline page:

| Outline | Design |
|---|---|
| Evidence Item `E01` | Design Item `ITEM01` |
| expectation + acceptance | goal, expected outcome + rules |
| one Page Evidence Run | rd commission → generate → verify → adopt |
| Result | draft + `checks.yaml` |
| accepted | adopted (a person's `decision.yaml`) |

```text
ITEM01 · Send the tested winner, verbatim        ✅ adopted
sms · full SMSR2 population · prescription review
┃ Hi, it's Dr. {NAME}'s office. New prescription details …      ← the design itself
adopted · rd02_generate_item01 · sha256 c93d51714b4e
goal       what this design tries to do, one sentence
why        follows the evidence · built on evidence (follow · evidence-informed)
insight    supported by FW01-send-salience ✅ · see Insight Space      (or: needs an insight · none named yet)
predict    expected: …            falsified if: …
rules      the acceptance rules
runs       rd01 Commission release · rd02 Generate pass · rd03 Verify pass · rd04 Adopt adopt
[ the buttons this state allows ]
```

The design text is the latest draft (or the adopted one, so marked); the
selected item (`?item=ITEM02`) is highlighted. Runs that name no registered
item appear below the cards as "Runs without an item", and a folded
**New Design Item** form closes the Space.

**Insight Space** is the supporting-evidence view, per item, in the Outline
sense: each Design Item names the insights it rests on (the register's
`evidence:` lines, `role · path`), and the Space shows for each one the
page, who signed it and when, what it says (the `FINDING` and `CONSEQUENCE`
lines of its Design Handoff block, or its first Opening line), and whether a
run record has pinned it by hash. An item built on evidence with no insight
named is flagged in red ("needs an insight"); a Brief-only item says no
insight is needed. Under each insight the Space lists **rules it implies**:
the page's `DO` / `DO NOT` counsel lines, so a drafter can turn every DO NOT
into an acceptance rule (`design_actions.counsel_rules`). The Space ends with **Available, unused**: signed pages on
the Insight board that no item uses yet, so the reader knows what else there
is to draw on.

**Run Space** is one timeline table per item. A Generate or Verify row folds
its `checks.yaml` (criterion · status · evidence) and, for Generate, the
draft text and its sha256. A failed row shows the recorded `failure:` in red.
A decision row quotes the person's `words:`. The Space ends with the records
check (`records check: PASS` or the list of findings), read live and never
cured.

**Delivery Space** is one card per adopted item: the adopted text as the
recipient sees it, the draft's Run, the artifact sha256, the Verify Run that
cleared it, the preview file, and the adopter's words with name and time.
Items not adopted are one line each with their state and waiting-on.

## The register

The register holds the goal, its evidence, and its rules, never its state. It
lives under `outline/` at `outline/<stem>-design-items.md`, one block per item:

```text
## ITEM01 · Send the tested winner, verbatim
type: sms
audience: full SMSR2 population, unconditioned
job: prescription review
goal: Field the salience template exactly as round 1 sent it     # what this design tries to do
stance: follow                     # follow · challenge · explore · generate
basis: evidence-informed           # brief-only · evidence-informed
mode: compose                      # compose · revise · brainstorm · theory-driven · challenge
expected: salience stays the best arm on click and authentication when re-fielded
falsified: a concurrently fielded round-2 arm beats it on click outside overlapping intervals
evidence:
- handoff · ../../../A00_InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
```

`goal`, `stance`, `basis`, `expected`, and `falsified` are the five fields of
the v2 `design_intent` (move, stance, basis, expected_effect,
failure_condition; the register says `goal` where the config says `move`); a
Commission freezes a copy of them into its config. `evidence` lines carry the
run-record roles (`evidence`, `handoff`, `inspiration`, `reference`,
`avoid`). `acceptance` is prose; the Commission compiles each line into a v2
criterion (`≤ N characters` → `max_chars`, quoted text or a `{PLACEHOLDER}`
→ `contains`, the same with `no`/`without` → `excludes`, anything else →
`semantic`). No state is typed there. Every `rdNN_*` run record names the
item it serves with `item: ITEM01`, and the tab derives the item's state by
walking its Runs in order:

```text
not commissioned → commissioned → generated | generate failed
                 → verified | verify failed → adopted | declined | hold
```

Beside the state the tab always says **who is waited on**: `agent · verify`,
`agent · revise`, `JL · adopt`, or nothing. That one column is the answer to
"what happens next" in both working modes: an agent runs Generate → Verify
(and revise) alone inside the Commission's budget; a person owns Commission
and Adopt and appears exactly where the column names them.

## What the tab reads (and owns nothing)

```text
0-BR-brief/*/BR00-brief.md              the line that names this folder (Goal Space)
board.md  reads:                        the Insight board (Goal Space, Insight Space)
outline/<stem>-design-items.md          the register (goal, evidence, rules)
runs/rdNN_<step>_<slug>.yaml            run record: item, target, actor, config ref
scripts/config/<run>.yaml               design_intent, criteria, unit
results/<run>/runtime.yaml              status, actor/worker, times, route, failure
results/<run>/result.yaml + checks.yaml verdict, artifacts, per-criterion checks
results/<run>/content/*                 the draft bytes
results/<run>/decision.yaml             release/hold · adopt/decline/revise/hold, words, draft pin
delivery/render/                        preview named by the adopt decision
```

It never infers a state from a file name, never counts files as progress,
never shows a draft that no `result.yaml` lists, and never treats a preview
as an adoption.

## Minimal by rule

The surface is text, tables, and folds. Deliberately absent: counters that
count the surface itself, static flow diagrams that read the same on every
folder, raw file listings, and any Space whose content is another Space's
(the card's `insight` row is a one-line pointer; the record lives in Insight
Space). An empty state is one sentence that names the file or Run that would
fill it.

## Actions · the two human gates and the agent queue

The tab writes through one endpoint, `POST /_board/design-act`, implemented
in `live/design_actions.py`. Each action writes exactly the contract's files
and nothing else; the button an item shows is the one its state allows:

| Item state | Button | Writes |
| --- | --- | --- |
| not commissioned | Release commission · Hold (name + words) | `rdNN_commission_*` run record, `decision.yaml`, complete receipt; config compiled from the register |
| commissioned · revise requested | Queue Generate · agent | planned `rdNN_generate_*` run record + config + receipt for `haipipe-designer-agent` |
| generated | Queue Verify · independent agent | planned `rdNN_verify_*` run record targeting the complete Generate Result |
| generate failed · verify failed | Queue revise · agent (feedback) | planned Generate run record with `base` + `feedback` inputs (a challenge bet stays in challenge mode) |
| verified | Adopt · Decline · Revise · Hold (name + words) | `rdNN_adopt_*` run record, `decision.yaml` pinning the draft hash, preview under `delivery/render/`; Revise also queues a revise Generate |
| any | New Design Item | one block appended to the register |
| several items at once | Release all · N (name + words) · Queue all · N · Adopt all verified · N (name + words) | the same per-item writes, one decision Run or planned run record per item; each button appears only when it has work |
| register short of the Brief's count | Ask the agent to draft the missing N (Goal Space) | `outline/<stem>-draft-request.md`: the goal, the insights with FINDING / CONSEQUENCE / DO / DO NOT lines, and how many items to draft; the queue runner or a Claude session appends the items with `add_item` and removes the file |

Batch buttons sit in one grey bar above the cards; a batch shares one name
and one sentence, recorded on every decision it writes. A person's name is
required on Commission and Adopt and is recorded as the
actor; the words typed are recorded verbatim in `decision.yaml`. Agent steps
are only *queued*: the tab never generates content, never judges a draft,
and never marks an agent Run complete. The caller closes a worker Run with
`design_actions.complete_run(folder, run)`: it names the real worker on the
run record before dispatch, runs the records check on the returned Result,
and writes the receipt truthfully (`complete` with the next route, or
`failed` carrying the gate's own words; a verify whose review failed the gate
shows as `verify invalid · agent · verify`, distinct from a draft that failed
review, `verify failed · agent · revise`). Adopt is refused while no complete
Verify Result exists, and `adopt` is refused when that verdict is not `pass`.
Every action re-runs the records check and returns its findings with the
receipt. Refusals come back as one plain sentence under the button.

## Running the queue without a session

`cli/design_queue.py <board dir> --list` prints every planned Generate and
Verify run record on the board and every open draft request;
`--run [--limit N]` names a worker on each record (`designer-cli-NN` /
`reviewer-cli-NN`), dispatches `claude -p` with the designer-agent brief, and
closes the run with the records check. Proven on the demo board 260917: one
Generate run drafted, checked, and closed with no session in the loop.
A worker that dies and leaves no result is put back in the queue
(`design_actions.release_worker`: the record returns to planned, the lost
worker is named on the receipt) and the runner stops instead of burning the
rest of the queue. Release and Adopt are never taken by the runner.

## Writer routing

Beyond those actions the tab has no writer. Every other intent routes to its
owner:

| User intent | Owning skill / route |
| --- | --- |
| Add or edit a Design Item | `haipipe-design` (the register) |
| Add or change a line of the Brief | `haipipe-design-brief` |
| Release or hold a Commission | `haipipe-design-workflow` → `Design.commission` (a person) |
| Generate or revise a draft | `haipipe-design-workflow` → `Design.generate` (`haipipe-design-unit`) |
| Verify a draft | `haipipe-design-workflow` → `Design.verify` (fresh reviewer) |
| Adopt, decline, revise, hold | `haipipe-design-workflow` → `Design.adopt` (a person) |
| Sign an insight | the Insight plugin, never this tab |
| Render a preview | `haipipe-application/fn/render.md` |
| Inspect Page acceptance | Page CHECK, not this plugin |

Selecting an item or a Space is local presentation state and writes nothing.

## Boundary

Apply only to a current Design Page-Folder with `folder-kind: design`. Legacy
`design/DU*`, `rNN_design_*`, PageX, and v1 shapes are named as unsupported in
the header and served with HTTP 410; nothing in them is read or reinterpreted.
Fixture material for this tab is built by
`haipipe-board/tests/fixture_design_v2.py`, which writes only contract-valid
records; the demo DesignBoard under `skills/diagrams/` is regenerated from it.

## Reader contract

From one tab, without opening a file, the reader can answer:

1. What does this folder want: for whom, on which venue, how many designs,
   drawing on which Insight board?
2. What is being designed, item by item, and what does each design say?
3. Why this design: its goal, whether it follows or challenges the evidence,
   and what it predicts and what would falsify it.
4. Which insights support each item, what they say, whether they are signed
   and pinned, what is still missing, and what else the board offers.
5. For each item: which step is it at, who acted, when, with what outcome, and
   who is it waiting on now?
6. Which exact draft (hash) was adopted, verified by whom, in whose words,
   and does the records check pass on the folder as it stands?

See `ref/space-mapping.md` for the Space ↔ file map and the state fold table.
