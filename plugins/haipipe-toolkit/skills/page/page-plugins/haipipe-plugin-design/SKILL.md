---
name: haipipe-plugin-design
description: >-
  The page-folder Design plugin: one 🎨 Design tab over a current Design
  Folder, read in time order across five Spaces. Goal Space is the ask (venue,
  who, their job, how many designs, which Insight board); Design Space is the
  Design Items with their goal, expected outcome, rules, state, and buttons;
  Insight Space is the supporting evidence per item (signed insights, what
  they say, what is still needed); Run Space is each item's Commission →
  Generate → Verify timeline; Delivery Space is the ready handoff: it lists
  every design that passed Verify. It reads the contract files and writes
  only through its own buttons (a person's Commission release/hold, queued
  Generate and Verify run records, a new register block, a draft request);
  every other write routes to the owning Design
  skills. Trigger: design plugin, design tab, design items, design folder,
  goal space, insight space, /haipipe-plugin-design.
metadata:
  version: "0.11.0"
  last_updated: "2026-09-18"
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
  ready for Delivery. Board rows link down to the cards here; this page's header links
back up. Nothing is stored twice.

Folder names say the goal, `Design-NN-<audience>-<job>-<venue>`: each part is
the first three content words of that Brief cell, filler words (with, within,
a, the, of, for, or, under, …) dropped:
`Design-01-all-patients-prescription-review-sms`. A renamed folder keeps
its `Design-NN` number, and an old link finds it by that number.

The Page title is one plain phrase from the same line, `<job> <venue> for <who>`
(`Prescription review SMS for all patients`; venue words: sms → SMS, ui-card →
app card), and the Brief's `audience` cell is written in plain words (`all
patients`, never `full SMSR2 population, unconditioned`).

Short links, for typing or pasting: `/_board/design-board` opens the server's
only DesignBoard (with several it lists them), `?board=B00` names one by the
unique start of its folder name, and `/_board/design?folder=<Design-NN>[&space=…]`
redirects to this folder's full `path=` and `file=` link (`Design-1` reads as
`Design-01`). The folder finds its board when only one board holds it; add
`&board=B00` when several do. When several boards hold it and no board is
named, the link answers 404 with a page that lists each board holding the
folder, one link each; it never guesses, because two boards' `Design-01` are
unrelated designs. A folder no board holds gets the list of boards.

## Plain words on the surface (JL 260916)

Every word a reader sees must be understood at first glance. `Space` is the
only word for a plugin surface. Steps are called by their Run words and
nothing else: **Commission, Generate, Verify, Delivery**. On screen every
contract word is translated, and the contract word never appears beside it:

| in the files | on the screen |
|---|---|
| `roster` | the Brief, a line of the Brief |
| `handoff` (a signed Wisdom page) | signed insight |
| Ticket | run record |
| candidate | draft |
| `check_unit` | records check |
| `intent` / `move` | goal |
| `stance follow · basis evidence-informed` | follows the evidence · built on evidence; `mode` stays in the files |
| `FW01` (an insight page's file id) | `full-W01 · Send salience`: its label and its title |
| `R1` (a Brief line id) | the task's full name, `<job> <venue> for <who>` |

So none of these reach the screen: roster, handoff, Ticket, candidate, DU,
or a Brief line id such as `R1`. An insight page is always shown by its
on-screen label and its title (`full-W01 · Send salience`,
`young-male-I02 · …`), never by its file id `FW01`; the file keeps `FW01`
(JL 260918).

Ids are `ITEM01`, `ITEM02` (never `DI`, which reads as the Insight plugin's
Data → Information). Run slugs follow the id: `rd02_generate_item01`. The
`rdNN` number counts across the whole folder, not per item, so ITEM02's first
Run may be `rd05`.

## The five Spaces, in time order

```text
🎨 Design
├── Goal Space       what we want: venue · who · their job · how many · which Insight board
├── Design Space     what we will make: one card per Design Item, with its buttons
├── Insight Space    what supports it: per item, the signed insights, what they say, what is missing
├── Run Space        what happened: per item, its Commission → Generate → Verify runs
└── Delivery Space   what is ready: one verified design per ready item
```

The header is one line, `Page level · <folder> · ↑ Board level`. A red line
is added only when something blocks the work: the folder is legacy, or the
Insight board's page is unsigned. Nothing else lives in the header.

**Goal Space** reads the line of the Brief that names this folder
(`0-BR-brief/*/BR00-brief.md`, the first table whose header names
`audience`, `job` and `venue` together, columns matched by header word:
`audience`, `job`, `venue`, `designs`, `insight`, `folder`) and says the ask
in one sentence:

```text
┃ 10 prescription review SMS designs for all patients
venue      sms
who        all patients
their job  prescription review
how many   10 wanted · 10 registered · 1 ready
from       BR00-brief.md · design tasks
Insight board
DesignPlugin-Demo-260916-InsightBoard · 1 of 1 insights signed
```

`designs` is the number the Brief asks for; `registered` and `ready` are
counted from the register and passed Verify records, and `· N declined` is
added only when an item was declined. The Insight board is the
one the line's `insight` cell names, else the owning board's `reads:` line;
a named board that is not found beside the DesignBoard shows in red. With no Brief line the Space says so
and names the file that would fill it; with no Insight board it says the
folder designs from the Brief only.

**Design Space** is one foldable row per Design Item that opens into its
card. A Design Item is one design
target with its own rules: one SMS, one UI card, one message pool. It plays
the role on a Design Folder that an Evidence Item plays on an Outline page:

| Outline | Design |
|---|---|
| Evidence Item `E01` | Design Item `ITEM01` |
| expectation + acceptance | goal, expected outcome + rules |
| one Page Evidence Run | rd commission → generate → verify → delivery |
| Result | draft + `checks.yaml` |
| accepted | ready for Delivery (Verify verdict `pass`) |

```text
                                                                        open all · close all
▾ ITEM01 · Send the salience wording unchanged   Hi, it's Dr. {NAME}'s office. New prescr…   ✅ ready
  sms · all patients · prescription review
  ╭─ Text message ──────────────╮  WHY THIS DESIGN   Send the salience wording unchanged, so the reader
  │ Hi, it's Dr. {NAME}'s       │                    sees whose office wrote and what to review
  │ office. New prescription    │                    follows the evidence · built on evidence
  │ details require your        │  FROM INSIGHT      Data         full-D02 What the 13 variants said
  │ review: link Reply STOP …   │  TO DESIGN                        ↓
  ╰─────────────────────────────╯                    Information  full-I02 How readers took each wording
  ready for Delivery · rd02_generate_item01                         ↓
                                                     Wisdom       full-W01 Send salience ✅ signed
  (on a verified item the handoff sits                               ↓
   here, under the design:                           Also read    Carrier opt-out rules
   ▸ ready for Delivery)                                             ↓
                                                     This design  ITEM01 Send the salience wording unchanged
                                   THE BET           expected  a first-time reader can say who sent it
                                                               and what to do after one read
                                                     wrong if  a cold reader cannot name the next step
                                                               from the text alone
                                   RULES             2 of 2 pass · independent review rd03
                                                     ✓ ≤ 160 characters including the opt-out suffix
                                                     ✓ ends with 'Reply STOP to opt-out' verbatim
                                   STEPS             Commission ✓ JL → Generate ✓ → Verify ✓ → Delivery
  ↑ the design and its handoff (left, stays in view) ↑ its explanation (right, scrolls)
▸ ITEM02 · Name the visit   Hi, it's Dr. {NAME}'s office, after your visit on…   ✅ ready
```

Each item is one fixed-height row (46px): id · title · the design in one line
(a screen previews its goal) · state · who is waited on. On a phone the preview
hides and the title takes the row. A row opens into a fixed-height card
(560px) that scrolls inside, so a long list stays scannable and every card is
the same size; `open all · close all` sits above the list (JL 260918). The
card puts the design on the left and its explanation on the right. The design
stays in view (sticky) while the explanation scrolls past it. After Verify
passes, the card shows the ready-for-Delivery handoff under the design; only
Commission still has a person form. On a narrow screen the two columns stack and scroll
together.

The explanation is a bordered two-column table, a small grey label on the
left and its content on the right, one row per question, never a key-value
wall:

1. **Why this design**: the goal sentence, then the stance and basis in plain
   words (follows the evidence, challenges the evidence, explores a new
   direction, a new design; built on evidence, from the brief only). The
   contract word never appears beside them.
2. **From insight to design**: a flow of the item's evidence pages by rung,
   Data → Information → Knowledge → Wisdom → This design. Each insight page
   shows as its label and its title (`full-W01 Send salience`), linked to the
   Insight view of that page when the page lies under the server root, and
   unlinked otherwise; signed pages are marked. A source that is not an
   insight page (a screenshot, a style sheet) sits on an **Also read** rung.
   A page the register marks `avoid` carries `· avoid`.
3. **The bet**: expected · wrong if, only when the item has them.
4. **Rules**: each rule marked ✓/✗ by the Verify of the draft shown on the
   card, else by that draft's own self-check, else "not checked yet". Rule N
   is criterion `rNN`, plus `rNNb`, `rNNc` when the rule quoted several
   phrases. A hand-written config with its own criterion names shows those
   criteria in words instead. When the register changed after release, the
   line says "the register changed after release; drafts still follow the
   released goal and rules".
5. **Steps**: the item's Runs as chips in order, `✗` for a run that failed
   the records check, superseded runs skipped, ending in `next: <who is
   waited on>`.

A screen shows as its rendered picture; an SMS shows as one message bubble
on a phone, with a `link` mark where the sending system inserts the link
(just before `Reply STOP to opt-out`), so a reader sees which ask the link
follows. The design an item shows is its ready candidate, else its latest draft
while it is still in progress; a draft that failed the check is never shown,
on the card, in Delivery Space, or in the csv. `?item=ITEM02` opens that
item's card, marks its row with an accent bar, and scrolls to it. A declined
item's card is folded after the live ones under `Declined, kept for the
record · N`. Runs that name no registered item appear below the cards as
"Runs without an item", and a folded **New Design Item** form closes the
Space. The form's labels are plain (approach, built on, expected, wrong if,
insights, rules); the contract words are only the option values.

**Insight Space** is the supporting-evidence view, per item, in the Outline
sense: each Design Item names the insights it rests on (the register's
`evidence:` lines, `role · path`), and the Space shows for each one the
page by its label and title (linked to the Insight view), its role in plain
words (a `handoff` reads "signed insight"), who signed it and when, what it
says, and whether a run record has pinned it by hash. What it says is the
`FINDING` and `CONSEQUENCE` lines of its Design Handoff block; without them,
the page's first Opening line when that line states something, else the page
title. An opening question is never shown as what a page says. An item built
on evidence with no insight named is flagged in red ("needs an insight"); a
Brief-only item says no insight is needed. Under each insight the Space lists
**rules it implies**: the page's `DO` / `DO NOT` counsel lines.
`design_actions.counsel_rules` writes each DO NOT as a "does not …" rule;
quote the phrase to ban (`does not say 'urgent'`) and it compiles to an
`excludes` check, leave it unquoted and the reviewer judges it. The Space
ends with **Available, unused**: signed pages on the Insight board that no
item uses yet, so the reader knows what else there is to draw on; when every
signed insight is used it says "none · every signed insight is used by an
item". With `?item=ITEM02` the Space shows that item only, under a line
"showing ITEM02 only · show every item".

**Run Space** is one timeline table per item. A Generate or Verify row folds
its `checks.yaml` (rule · status · why), each check named by its rule in
words, never by `r03`, and, for Generate, the draft text and its sha256. A
revise Generate reads `Generate · revise of rdNN` with its feedback quoted. A
run that failed shows its `failure:` in red; a Verify whose verdict is fail
is red too, with its checks unfolded; a superseded run is grey with its
reason. A decision row quotes the person's `words:`. With `?item=` the Space
narrows the same way as Insight Space. The Space ends with the records check
(`records check: PASS` or its findings, with folder-relative paths), read
live and never cured.

**Delivery Space** is a quick handoff of what is ready: one table, one row per
item whose independent Verify passed, `item` (id, linked to its card, and
title) · `design` (the text as the recipient sees it; an SMS shows its `link`
mark, as sent). A design that has not passed Verify is not listed yet. Hashes,
receipts, and the audit trail stay in Run Space; item reasoning stays in
Design Space. A retired historical item remains folded under its record.

A **screen** (a UI design) is read as its picture. When
`delivery/render/manifest.json` lists a picture for the exact draft an item
shows (`candidate` = that Generate run), the Design Space card puts the
picture on the left, with the HTML one click away, and Delivery Space shows
the folder's screens as a picture gallery instead of the table. A picture of
an older draft is never shown for a newer one. An acceptance rule with the
word render, rendered or rendering (for example "judged on the render") and
no quoted phrase compiles to a `visual` check.

## The register

The register holds the goal, its evidence, and its rules, never its state. It
lives under `outline/` at `outline/<stem>-design-items.md`, one block per item:

```text
## ITEM01 · Send the salience wording unchanged
type: sms
audience: all patients
job: prescription review
goal: Send the salience wording unchanged, so the reader sees whose office wrote and what to review
stance: follow                     # follow · challenge · explore · generate
basis: evidence-informed           # brief-only · evidence-informed
mode: compose                      # compose · revise · brainstorm · theory-driven · challenge
expected: a first-time reader can say who sent it and what to do after one read
falsified: a cold reader cannot name the next step from the text alone
evidence:
- handoff · ../../../A00_SMSR2Full-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
```

`evidence` paths are relative to the Design Folder (the folder holding
`<stem>.md`), not to the register file. A line is `role · path` (or `role  path`
with two spaces); the roles are `evidence`, `handoff`, `inspiration`,
`reference`, and `avoid` (`base` and `feedback` are written by revise runs).

`expected` and `falsified` judge design quality: what a reader can do or
understand with the draft. They may name what a later experiment will check,
but the design phase judges design quality only, so no experiment words (arm,
allocation, power, winner, field) belong in them.

The bindings are checked when the item is added: a `challenge` stance goes
with `challenge` mode and only with it; `challenge` or `theory-driven` mode
needs both `expected` and `falsified`; `brainstorm` goes with stance `explore`
or `generate` and carries no `expected` or `falsified`. `add_item` refuses the
rest with one sentence.

`goal`, `stance`, `basis`, `expected`, and `falsified` feed the v2
`design_intent` (move, stance, basis, expected_effect, failure_condition; the
register says `goal` where the config says `move`, and the config's own `goal`
is the same goal sentence). The Commission pins its config (goal sentence,
stance, basis, mode, expected, falsified, the compiled criteria, and the raw
rule text) and the item's evidence files with sha256. It does not pin the
Brief version or venue packs. Generate and Verify copy the released config and
evidence list, so an edit to the register after release reaches only a new
Commission, which means a new item (one Commission per item). The card then
says "the register changed after release; drafts still follow the released
goal and rules".

`acceptance` is prose; the Commission compiles each line into v2 criteria:

1. `≤ N`, `at most N` or `no more than N characters` → `max_chars` N;
   `under`, `fewer than` or `less than N characters` → `max_chars` N − 1.
2. A quoted phrase or a `{PLACEHOLDER}` → `contains`; with a negative word
   before it (no, not, does not, doesn't, don't, never, without, avoid,
   excludes) → `excludes`.
3. `ends with 'X'` → `ends_with` (compared with trailing whitespace stripped);
   `starts with`, `begins with` or `opens with 'X'` → `starts_with`.
4. Otherwise, a rule with the word render, rendered or rendering → `visual`.
5. Anything else → `semantic`, judged by the reviewer.

The first rule that applies wins, in this order: a length limit, then quoted
phrases, then the render word.

A rule quoting several phrases makes `rNN`, `rNNb`, `rNNc`. A phrase with only
"or", "and" or commas before it shares the previous phrase's kind, so
`no 'urgent', 'act now' or 'hurry'` excludes all three. An apostrophe inside a
word (`it's`, `doesn't`) is never a quote mark. No state is typed in the
register. Every `rdNN_*` run record names the item it serves with
`item: ITEM01`, and the tab derives the item's state by walking its Runs in
order:

```text
not commissioned → commission open → commissioned | hold
  → generate queued → generating → generated | generate failed
  → verify queued → verifying → ready | verify failed | verify invalid
queued run out of date: a queued run whose pinned file changed since it was queued
```

The full fold, with every queued, running and open state and who each one
waits on, is in `ref/space-mapping.md`.

Beside the state the tab always says **who is waited on**. `agent` is waited
on only while a run is queued or running (`agent · generate`,
`agent · verify`, `agent · running`). Otherwise it names the person with the
step: `JL · commission`, `JL · release or hold`, `JL · queue the draft`,
`JL · queue the review`, `JL · queue a revise`, `JL · queue the review again`,
`JL · queue again`, or `JL · queue the revise`; a ready item waits on no one.
A person releases the Commission and clicks the queue buttons; an agent runs
only what is queued. The only budget is
`max_iterations: 2` inside each Generate run; nothing counts revise runs
across an item.

## What the tab reads (it owns no storage)

```text
0-BR-brief/*/BR00-brief.md              the line that names this folder (Goal Space)
board.md  reads:                        the Insight board (Goal Space, Insight Space)
outline/<stem>-design-items.md          the register (goal, evidence, rules)
outline/feedback/<run>.md               the feedback a revise Generate was queued with
outline/<stem>-draft-request.md         an open request for the agent to draft items
runs/rdNN_<step>_<slug>.yaml            run record: item, target, actor, config ref, pinned inputs
scripts/config/<run>.yaml               goal, design_intent, criteria, the rule text, unit
results/<run>/runtime.yaml              status, actor/worker, times, route, failure
results/<run>/result.yaml + checks.yaml verdict, artifacts, per-criterion checks
results/<run>/content/*                 the draft bytes
results/<run>/decision.yaml             Commission release/hold, when present
delivery/render/                        screen pictures (manifest.json), when present
```

It never infers a state from a file name, never counts files as progress,
never shows a draft that no `result.yaml` lists or that failed the records
check; a passed Verify is the Delivery gate.

## Minimal by rule

The surface is text, tables, and folds. Deliberately absent: counters that
count the surface itself, static flow diagrams that read the same on every
folder, raw file listings, and any Space whose content is another Space's
(the card's insight flow names each page by its label and title and links to
it; what each page says in full, and what is still missing, lives in Insight
Space).
The card's flow is drawn per item from its own evidence pages, so it differs
from folder to folder and is not a static diagram. An empty state is one sentence that names the file or Run that would
fill it.

## Actions · the two human gates and the agent queue

The tab writes through one endpoint, `POST /_board/design-act`, implemented
in `live/design_actions.py`. Each action writes exactly the contract's files
and nothing else. Every state that waits on a click shows its button, and the
page refuses an action the state does not show, naming the state and who is
waited on:

| Item state | Button | Writes |
| --- | --- | --- |
| not commissioned · commission open · hold (held at Commission) | Release commission · Hold (name + words) | `rdNN_commission_*` run record, `decision.yaml`, complete receipt; the config compiled from the register and the item's evidence files, pinned with sha256. One Commission per item: a second Release is refused, and a held Commission can be released later |
| commissioned · revise requested | Queue Generate · agent | planned `rdNN_generate_*` run record, a copy of the released config, and a receipt for `haipipe-designer-agent` |
| generated · verify invalid | Queue Verify · independent agent | planned `rdNN_verify_*` run record targeting the complete Generate Result; refused when that draft already has a review |
| generate failed · verify failed | Queue revise · agent (feedback) | planned Generate run record with `base` + `feedback` inputs, the feedback saved at `outline/feedback/<run>.md` (a challenge bet stays in challenge mode); refused for a draft that passed its review |
| queued run out of date | Queue again with today's insight files | the old queued run marked `superseded` (reason: the files that changed) and a fresh run that pins today's bytes; a revise keeps its base and feedback |
| ready | ready for Delivery | no decision Run; the passed Verify pins the exact candidate for handoff |
| generate queued · verify queued · generating · verifying | none ("queued for the agent") | — |
| any | New Design Item | one block appended to the register, after the binding check above |
| several items at once | Release all · N (name + words) · Queue all · N | the same per-item writes, one Commission decision or planned run record per item; each button appears only when it has work |
| register short of the Brief's count | Ask the agent to draft the missing N (Goal Space) | `outline/<stem>-draft-request.md`: the goal, the insights with FINDING / CONSEQUENCE / DO / DO NOT lines, and how many items to draft. The queue runner only lists open requests; a Claude session appends the items with `add_item` and removes the file |

The independent Verify is the Delivery gate. A passed candidate is ready
without another human decision; a failed draft or failed review can still be
revised through the normal Generate queue. The writer refuses a second open
run for one item and a second review of a draft that already has one.

`delivery/render/` is optional display material for a ready candidate (for
example a screen picture or a copied text render). It is not a decision
receipt and it never changes the Verify result.

Any form that asks for a name, words, or feedback is folded by default under
one line that names the choice (`Release or hold the commission`, `Queue a
revise, with feedback`, `For all items at once: …`); it opens on click, and is already open for the item selected with
`?item=`. A single agent-queue button needs no typing and stays in view. On a
card every form and button sits in the design column, which stays in view.
Batch buttons sit in one grey bar above the cards; a batch shares one name
and one sentence, recorded on every Commission it writes. After a click,
every item button lands back on Design Space at that item; a draft request
lands on Goal Space.

A person's name is required on Commission and is recorded as the actor; the
name field starts filled with the person already seen on this folder's
decisions, so whoever releases types their own name if it differs. The words
typed are recorded verbatim in Commission's `decision.yaml`. Agent steps are only
*queued*: the tab never generates content, never judges a draft, and never
marks an agent Run complete. `design_actions.name_worker(folder, run, actor)`
names the real worker on the run record before dispatch; the caller then
closes the worker Run with `design_actions.complete_run(folder, run)`, which
runs the records check on the returned Result and writes the receipt
truthfully:

1. **Draft fails the check**: failed, route generate; the person queues a revise with feedback.
2. **Review fails the check**: failed, route verify, even when checks are only unresolved.
3. **Review verdict fail**: complete, route generate; the person queues a revise.
4. **Review verdict pass**: complete, route delivery; the exact candidate is ready.

A review that failed the check shows as `verify invalid · JL · queue the
review again`, distinct from a draft that failed review, `verify failed · JL ·
queue a revise`. There is no HOLD route from the agent side: HOLD is a
person's decision at Commission. Delivery is not a second decision gate; it
is the read-only handoff of a passed Verify.
Every action re-runs the records check and returns its findings with the
receipt. Refusals come back as one plain sentence under the button.

The records check (`check_unit.py --folder`) holds an open run to its pins
exactly. A closed run (complete, failed, blocked) reads inputs that live
outside the Design Folder, such as Insight pages, as history, so a later edit
to an Insight page does not void it; inputs inside the folder (config,
approval, targets, artifacts) stay exact. A superseded run needs a reason and
no result.

## Running the queue without a session

`cli/design_queue.py <board dir> --list` prints every planned Generate and
Verify run record on the board and every open draft request (it lists draft
requests and never fulfils them; a Claude session drafts the items with
`add_item`). `--run [--limit N] [--dry-run]` names a worker on each record
(`designer-cli-NN` / `reviewer-cli-NN`), dispatches `claude -p` with the
designer-agent brief, and closes the run with the records check. Proven on the
demo board 260917: one Generate run drafted, checked, and closed with no
session in the loop. A queued run whose pinned files changed since it was
queued is skipped with the names of those files; the runner never re-pins in
place, and the person clicks "Queue again" on the page. A worker that dies
and leaves no result is put back in the queue
(`design_actions.release_worker`: the record returns to planned, the lost
worker is named on the receipt) and the runner stops instead of burning the
rest of the queue. Release and Queue again are never taken by the
runner.

## Writer routing

Beyond those actions the tab has no writer. Every other intent routes to its
owner:

| User intent | Owning skill / route |
| --- | --- |
| Add or edit a Design Item | `haipipe-design` (the register) |
| Add a line to the Brief, or open its folder | `haipipe-plugin-design-board` (`add-tasks`, `new-folder`) |
| Change the Brief's prose, needs, or signed inputs | `haipipe-design-brief` |
| Release or hold a Commission | `haipipe-design-workflow` → `Design.commission` (a person) |
| Generate or revise a draft | `haipipe-design-workflow` → `Design.generate` (`haipipe-design-unit`) |
| Verify a draft | `haipipe-design-workflow` → `Design.verify` (fresh reviewer) |
| Hand off a passed design | Delivery Space (read only; no second decision) |
| Sign an insight | the Insight plugin, never this tab |
| Render a preview | `haipipe-application/fn/render.md` |
| Inspect Page acceptance | Page CHECK, not this plugin |

Selecting an item or a Space is local presentation state and writes nothing.

## Boundary

Apply only to a current Design Page-Folder with `folder-kind: design`. Legacy
`2-DS-design/DS*` folders, `design/DU*` storage, `rNN_design_*` runs, PageX,
and v1 shapes are named as unsupported in the header and served with HTTP
410; nothing in them is read or reinterpreted. An old `DS` link is rewritten
to the `Design-NN` folder only when the file it names no longer exists, so a
DS folder still on disk answers 410 for itself, and a folder parked under the
board's `_archive/` (the way a closed record is retired) leaves its old links
healing to the folder that replaced it.
Fixture material for this tab is built by
`haipipe-board/tests/fixture_design_v2.py`, which writes only contract-valid
records. `--demo` rebuilds the demo DesignBoard under `skills/diagrams/`, and
refuses when the demo already holds runs (people make runs by clicking on it),
unless `--force`, which deletes those runs.

## Reader contract

From one tab, without opening a file, the reader can answer:

1. What does this folder want: for whom, on which venue, how many designs,
   drawing on which Insight board?
2. What is being designed, item by item, and what does each design say?
3. Why this design: its goal, whether it follows or challenges the evidence,
   what it expects a reader to do, and what would show that wrong.
4. Which insights support each item, what they say, whether they are signed
   and pinned, what is still missing, and what else the board offers.
5. For each item: which step is it at, who acted, when, with what outcome, and
   who is it waiting on now?
6. Which exact draft (hash) is ready for Delivery, verified by whom, and does
   the records check pass on the folder as it stands? (Run Space)
7. At a glance, what designs do we have? (Delivery Space)

See `ref/space-mapping.md` for the Space ↔ file map and the state fold table.
