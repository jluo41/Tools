# The board map: which group answers which question
state: 🔴 OPEN
owner: JL
method: adopt the paper precedent's reading order, then state only what this board changes

## Opening
How do you read this Application design board: which layer answers which question, and which way do failures travel?
`QB5` says what advice an intervention owes, `QC1` names the route that makes it, `QF1` records the run that tried.
Start in the wrong layer and every answer reads as an opinion, because the page owning the fact is elsewhere.
This page fixes the read: Design, Delivery, Engine, Execute, and names this board's three deltas from QA0@paper.

**Where this page sits**: This is the entry face, the only page whose subject is the board itself rather than the Application system.
`QA1` takes over at the next question, which is where a given file lives across `application/` and an intervention folder.
Every other page sits inside one of the five groups this page names, and only four of those groups are layers.

**Why the order is a dependency**: Delivery can be specified before any skill exists to satisfy it.
Engine can route only to deliveries already named, and Execute can only report on a route Engine already declares.
Reversing any pair makes a page assert something its upstream has not decided yet.

**Covered elsewhere**: The rung contents belong to `QB2`-`QB5`, the venue knowledge to `QBv1`-`QBv8`, the route crosswalk to `QC1`, the stage-engine port to `QC2`, and every run record to `QF1`.
This page states the reading order and stops; a fact stated twice drifts.

## Writing Style
How this page must be written, so that whoever edits it next edits to the same rules.

**Inherited from the page contract**: the section order, the sentence rules, and the figure rules come from `haipipe-board/ref/page-template.md` and its `ref/writing-rules.md`, and are not restated here.

**Name a group by what it answers**: write "Delivery, what a consumer gets" on first use in any division.
A bare group letter means nothing to a reader who arrived from one link.

**Never restate an owned fact**: the rung contents, the venue gates, the route crosswalk, and the run records each have an owning page.
Cite the id and stop, because a copy here goes stale the day the owner changes.

**A delta is stated once, as a delta**: anything identical to QA0@paper is cited, never copied.
Only the three departures earn prose on this page.

## Diagram

**The reading order**: four layers, one venue shelf, one direction.

```text
 🧭 QA · DESIGN     what the Application system IS, and who owns its boundaries
        │ shapes
        ▼
 📦 QB · DELIVERY   what an intervention's consumers RECEIVE
        │           Opening → Data → Insight → Claims → Design
        │           → Display → Artifact → Deploy → Iterate
        │ ◀── reads ── 🎛 QBv · one page per venue-pack TARGET
        │ served by
        ▼
 ⚙️ QC · ENGINE     which reusable route MAY PRODUCE each delivery
        │ demonstrated by
        ▼
 🧪 QF · EXECUTE    what actually RAN, passed, failed, or reopened work

 🔒 the order is a dependency: Execute reports on a route Engine declares,
    for a delivery QB specified, inside boundaries QA fixed
```

## Content

### 1 · The four layers
**Who answers what**: the question each group owns, and the act it must never perform.

```text
 🗂 GROUP           ❓ ANSWERS                            🚫 NEVER DOES
 ────────────      ──────────────────────────────      ─────────────────────────
 🧭 QA Design       what the system is · who owns        author a skill
 📦 QB Delivery     what a consumer gets, per concern    write the code that makes it
 🎛 QBv Venue       what one channel gates + rewards     pick the venue (`QB1` does)
 ⚙️ QC Engine       which route may produce it           author delivery content
 🧪 QF Execute      what one bounded run did             judge whether design is right
```
📌 Establishes the five groups, the four questions, and the ownership asymmetry each group must keep.

#### 1.1 · Design owns the system and authors no skills
(QA fixes folders, boundaries, and the intervention board before anything ships)
The QA pages say what the Application system is: the folder law (`QA1`), the shipped skill roster (`QA2`), the intervention-board ruling (`QA3`), and the evidence wall (`QA4`).
A Design page may name a skill; it may never author one, because authoring belongs to the Engine's routes and the shipped `application/` tree.

#### 1.2 · Delivery specifies without code, and QBv is its shelf
(QB says what a consumer gets; QBv says what one channel demands; neither writes code)
A QB page names what an intervention's consumer receives at one concern, from `QB1` Opening through the ladder `QB2`-`QB5` to the tail `QB6`-`QB9`.
`QB1` owns which venue an intervention picks; a QBv page owns what the picked venue gates, rewards, and requires, one page per pack target.
QBv is a shelf Delivery reads, not a fifth layer: it never says who receives, only what the channel demands.

#### 1.3 · Engine maps without authoring, Execute only records
(one skill serves several deliveries; one run proves or blocks exactly one route)
`QC1` links each delivery to the Application, Probe, or Display route that may produce it, and `QC2` holds the stage-engine port; neither copies the authority it links to.
A QF record states what one bounded run did against `_fixture/`, and nothing more.
Execute never judges whether the design is right, because a run can only report on the rules it was given.

### 2 · The failure direction
**Failures travel up, fixes travel down**: where a break is filed, and where the repair lands.

```text
 🧪 QF Execute ──── failed run ─────▶ reopens 📦 QB or ⚙️ QC, the owning page
 ⚙️ QC Engine ──── no route ───────▶ reopens 📦 QB, the target was never producible
 📦 QB Delivery ── bad spec ───────▶ reopens 🧭 QA, the boundary was drawn wrong

 🔧 the fix travels back DOWN: the reopened page changes its rule,
    and the next run obeys the changed rule
 🔁 1a ⇄ 1b ⇄ 1c ⇄ 1d back-edges inside one intervention are flywheel
    routing, logged in the intervention, never filed as a board failure
```
📌 Establishes the one direction a board failure moves, and the flywheel carve-out that keeps ladder back-edges off it.

#### 2.1 · A board failure reopens the page that owns the route
(the record stays in QF; the repair lands where the rule lives)
A failed Execute record reopens the owning Delivery or Engine page and settles nothing itself, and a failed candidate never becomes an implicit promotion (QA0@paper).
A route Engine cannot declare reopens the Delivery page that asked for it, and a delivery no consumer needs reopens Design.
The fix then travels back down: the reopened page changes its rule, and the next run is judged against the changed rule.

#### 2.2 · Ladder back-edges are not board failures
(the flywheel is the intervention's own routing, recorded in the intervention)
Inside one intervention the ladder runs as a flywheel: a theme that needs a number routes back to Data, and a refuted claim routes back to Insight.
`application/README.md` rules every such back-edge a discovery event, not a failure, and the intervention's own `_LOG` records it.
Whether a repeated back-edge should also reopen the owning QB rung page is JL's to rule, and it sits in Decision Now below.

### 3 · The three deltas
**Same map, three departures**: what QA0@paper says, against what this board says.

```text
 🎛 QBv     paper: one page per JOURNAL       here: one page per venue-pack TARGET
 🪜 QB      paper: ten reader concerns        here: QB2-QB5 carry the ladder D→I→K→W
 🚪 QD/QE   paper: reserved for later         here: absent · /haipipe-board owns them
```
📌 Establishes the only three places this board departs from the paper precedent; everything else is a citation.

#### 3.1 · QBv holds venue-pack targets, not journals
(the same slot, a different unit: a channel instead of a publication)
The paper board's QBv pages each hold one journal, MISQ first; this board's `QBv1`-`QBv8` each hold one pack target under `application/venue/`: sms, email, dashboard, report, push, reminder, checklist, ui-card.
The unit changed because a journal playbook and an output modality gate different things: a journal gates prose, while a venue pack gates which stages fire and how deep claims must settle.

#### 3.2 · QB2-QB5 carry the ladder as delivery concerns
(rung = concern: Data, Insight, Claims, Design, echoing D→I→K→W)
The paper delivers knowledge, so its QB series runs Opening through Round over a single claims ledger; the application delivers wisdom, so its middle four concerns are the ladder rungs 1a-1d.
A rung page says what the consumer gets at that altitude of evidence, and the tail `QB6`-`QB9` says how it ships and comes back as fresh data.

#### 3.3 · QD and QE are absent on purpose
(the shared board substrate owns Working and Sharing)
The paper board reserved QD and QE for future paper-specific Working and Sharing content; this board deletes the slots instead.
Live Board interaction, hosting, and mounts are owned by `/haipipe-board`, and duplicating them here would give the substrate a second authority to drift from.

## Aims

### A1 · 🗂 The four layers
- A1.1 · The board is read Design, Delivery, Engine, Execute, and each group answers only its own question.
  **Done when:** no page in QA, QB, QBv, QC, or QF states a fact another group owns, and QBv stays a shelf Delivery reads rather than a fifth layer.

### A2 · ↩️ The failure direction
- A2.1 · Every board failure names the Delivery or Engine page it reopens, and no ladder back-edge is filed as one.
  **Done when:** each QF record carries a reopen target or an explicit pass, and intervention `_LOG` back-edges never appear as QF failures.

### A3 · 🔀 The three deltas
- A3.1 · The three departures from QA0@paper are stated once, here and in the registry, and nowhere grows a fourth.
  **Done when:** this page and `board.md` name the same three deltas, no page reintroduces a QD or QE group, and no QBv page turns back into a journal.

### P · 🏁 Page-level
- P1 · A fresh reader can name the owning group for a question from any layer without opening this page twice.
  **Done when:** a cold-read agent names the owning group for five questions drawn from different groups.

## States

### Decision Now
- [ ] 🗣 Does a repeated ladder back-edge inside an intervention ever reopen the owning QB rung page?
      📍 `Part 2` the failure direction, beside the rule it would amend
      🔔 `Why now` this board inherits the paper rule that a failure reopens the owning page, while `application/README.md` rules every ladder back-edge a discovery event, and the two meet exactly here
      ⭐ `A ·` adopt the paper rule verbatim, so back-edges stay intervention-internal and a QB rung page reopens only on a QF record; recommended because it keeps one writer per failure kind and the flywheel already has its own log
      `B ·` amend the rule so a back-edge that recurs across rounds also reopens the owning QB rung page, which commits every intervention log to being mirrored onto the board
      🛑 `Blocks` closing A2.1, which needs an agreed reopen rule before any QF record can honor it
      🤖 `If nobody answers` A takes effect, and QF records follow the paper rule unchanged

### A1 · 🗂 The four layers
- ⬜ A1.1 · Not audited; `board.md`'s spine and Pipeline already print the order, and whether every page stays inside its own question has not been checked.

### A2 · ↩️ The failure direction
- 🧠 A2.1 · Waiting on the Decision Now row above; until it is ruled, a QF record has no agreed line between a board failure and a flywheel back-edge.

### A3 · 🔀 The three deltas
- 🔨 A3.1 · This page and `board.md` now state the same three deltas; the guard against a fourth appearing elsewhere is not watched by any check.

### P · 🏁 Page-level
- ⬜ P1 · Never run; no cold read has been dispatched against this board.

## Files

### 📋 Contracts · what CARRIES a rule to other pages
- `board.md`
  The registry: the spine, the close condition, the five-group roster, and the `## Links` table that declares QA0@paper.

### 📥 Input files · what the work READS
- `../PaperSkillBoard-260725/1-QA-design/QA0-the-board-map/QA0-the-board-map.md`
  The precedent: the four-layer read, the ownership asymmetry, and the failure rule this page adopts as QA0@paper.
- `../../application/README.md`
  The family structure: the ladder, the flywheel, the venue gating, and the deltas-vs-paper table that division 3 cites.

## Glossary

- 🪜 **Ladder**: the venue-free evidence climb 1a-descriptions to 1b-themes to 1c-claims to 1d-advice, echoing Data, Insight, Knowledge, Wisdom; the application's stage 1.
- 🔁 **Flywheel**: the ladder's legal back-edges; downstream work that exposes an upstream gap routes back as a discovery event, not a failure.
- 🎛 **Venue pack**: one channel's knowledge folder under `application/venue/venue-<name>/`, read when the venue is pinned; the eight targets are sms, email, dashboard, report, push, reminder, checklist, ui-card.
- 🧱 **Board substrate**: the shared `/haipipe-board` engine that renders, serves, and checks every board, which is why this board carries no Working or Sharing group.

## Log

260816 · The board took the two shape rules the Board family had landed. The group folders now carry their place in `## Pages` as a leading number, `1-` through `5-QF-execute`, so the folder listing and the board read in one order. Then every page took a folder of its own, `1-QA-design/QA0-the-board-map/QA0-the-board-map.md`, the shape ruled on 260815, which is what gives a page's drawing, deck or export somewhere to live. Both moves were made by `cli/refold.py` and its sibling in the Board engine, and the check came back with nothing new: same 33 pages, no new error, no new warning. Alongside it every dead link was repaired: the paper design board had been renamed and folded, and the probe design board retired on 260804, so its ids now point at `haipipe-probe`, which carries those rulings.

260802 · Page created: adopted the four-layer read and the ownership asymmetry from QA0@paper, stated the three deltas (QBv holds venue-pack targets, QB2-QB5 carry the ladder, QD/QE absent), and raised the back-edge reopen question to JL as a Decision Now row.
