# The design lifecycle board layout: every group, every page, one page per unit
state: 🟡 PARTIAL · a proposed layout; the fixture carries only the seed today
owner: JL
method: draw the whole intervention board in one place, one page per unit, then give each group its own Content division so the figure and the prose have the same shape
session: 8c7b33f0-8ba0-424c-907d-e761014718a4

## Opening
What does an intervention's own board look like, all of it, when each unit is its own page?
An intervention board is the `0-lifecycle/board.md` inside an intervention, such as the `01_sms_young_male` fixture.
This proposal splits each rung into one page per unit, so Description becomes `S-Description-1-cohort`, `S-Description-2-arms`, and so on.
Each per-unit family sits above a control page, and this page draws all the groups at once, following the paper board's rule.

**Where this page sits**: it sits before QB1 and is the only page here that shows the whole board, grouped by Delivery concern so `Delivery · Description` is what QB2 rules; QA3 owns the migration that renders it.

**Why one page per unit**: a rung is not one thing, it is many, and one description can be accepted while the next is still being chased.
The paper board proved the test on its Display and Main groups, and QB2's earlier draft held every description as a row on one page, which cannot carry a state per description.

**How this page is laid out**: `§1` holds the rules that are true across every group, and after it comes ONE DIVISION PER GROUP, in the same order the figure draws them.
A reader who finds a group in the figure jumps to the division with the same name and learns four things: how many pages it carries, what one unit is there, what its control page holds, and what exists today.

**What it is measured against**: the `01_sms_young_male` fixture, which today carries only `S-Seed-0`, so almost every page below is PROPOSED, marked as not built.
Where the proposal and the fixture differ, the difference is named as a gap.

## Writing Style
This page DESIGNS the layout; the intervention board SHOWS it: state what an intervention must carry, not what the fixture happens to have today.
English only, one sentence per line, no em-dashes.
The intervention board is the spine of every figure: a group name leads the line and the QB id annotates it on the right, never the other way round.
ONE PAGE, ONE LINE: never put two page names on one line, so a reader counting pages counts lines.
A count is a real count: a number is read off the fixture, off a sibling QB page, or it is marked as a proposed gap, never estimated.

ONE GROUP, ONE DIVISION (JL 260802): every group the figure draws has exactly one Content division, in figure order, and no group has two or none.
The division answers the same four questions in the same order every time, because divisions that answer different questions cannot be compared, and comparing groups is the whole reason this page exists.

NEVER RESTATE A CONCERN'S OWN RULES: QB1 to QB9 own what a rung DELIVERS and what makes an entry admissible.
This page owns only how many PAGES that rung becomes and what one unit is, which is a question none of those pages asks.

THE GROUP DIVISIONS CARRY NO AIM OF THEIR OWN: no single group's page count is a durable target worth tracking, so `P1` tests them as a set instead.
An empty `### A5` group would read as an oversight rather than a choice, which is why this rule is written down.

## Diagram
**The whole intervention board**: every page it should carry, one per line, under the group that owns it, with per-unit families expanded above their control page.

```text
  📁 <intervention>/0-lifecycle/ ── the board is a FOLDER, not one file
     board.md is its registry · pages live in one subfolder per FAMILY
  ════════════════════════════════════════════════════════════════
  🎯 WHAT WE EXPECT an intervention to carry, group by group
  ### Delivery · Opening                          ◀ QB1 · §2
      🌱 S-Seed-0-seed                            ✅ built
      📍 S-Venue-0-venue
      📣 S-Pitch-0-pitch                          ← family Pitch
  ### Delivery · Description   [PER-UNIT]         ◀ QB2 · §3
      🗂 S-Description-Dash                       the control page
      📊 S-Description-1-cohort
      📊 S-Description-2-arms
      📊 S-Description-3-outcomes
      📊 S-Description-4-time-window
      📊 S-Description-5-data-quality
      📊 S-Description-6-benchmark
  ### Delivery · Themes        [PER-UNIT]         ◀ QB3 · §4
      🗂 S-Themes-Dash                            control · holds Parked
      🧩 S-Themes-1-<promoted>
      🧩 S-Themes-2-<promoted>
  ### Delivery · Claims        [PER-UNIT]         ◀ QB4 · §5
      🗂 S-Claims-Dash                            the ledger control
      ⚖️ S-Claims-1-<claim>
      ⚖️ S-Claims-2-<claim>
  ### Delivery · Advice        [PER-UNIT]         ◀ QB5 · §6
      🗂 S-Advice-Dash                            the control page
      🎯 S-Advice-1-<advice>
      🎯 S-Advice-2-<advice>
      🧵 S-Narrative-0-arc     [gated]            ← family Narrative
  ### Delivery · Display       [PER-UNIT · gated] ◀ QB6 · §7
      🗂 S-Display-Dash                           ⏭ sms skips the group
      🖼 S-Display-1-<unit>                       ⏭
  ### Delivery · Artifact      [PER-UNIT/segment] ◀ QB7 · §8
      🗂 S-Artifact-Dash                          the control page
      ✍️ S-Artifact-1-<segment>
      ✍️ S-Artifact-2-<segment>
  ### Delivery · Deploy                           ◀ QB8 · §9
      🚀 S-Deploy-0-review
      🚀 S-Deploy-1-audit
      🚀 S-Deploy-2-ship
  ### Delivery · Iterate       [per round]        ◀ QB9 · §10
      🔁 S-Round-1-<batch>
  ### machinery, present but never a stage        ◀ §11
      🔬 PPNN-<topic>                             one per 1-probes/ topic
      🧾 Gate Ledger                              a STATUS row, not a page

  🔤 S-<Family>-<unit>-<slug>.md
     FAMILY says who wrote it · GROUP says who owns the rule
     ← marks a page whose family is not the one its group is named for
     🗂 Dash = the family's control page, no stage writes it
     ✅ built · ⏭ skipped by the pinned venue · unmarked = PROPOSED
```

## Content

### 1 · The rules that hold across every group
**Three rules, then nine groups**: what a reader needs before any group division makes sense.

```text
  🧪 THE TEST      can one unit be APPROVED while its neighbour is
                   REJECTED?  yes → per-unit · no → one page
  🔤 THE NAME      S-<Family>-<unit>-<slug>.md
  🗂 THE CONTROL   S-<Family>-Dash, the family's inventory
```
📌 Establishes the one test that decides page against row, the filename grammar, and the control page, so each group division below can state its answer in a line instead of re-arguing it.

#### 1.1 · A unit earns a page when it can be approved while its neighbour is rejected
(the approve-or-reject test, which is the only thing that decides page against row)
One claim can read supported while the next reads GAP, and one segment's messages can be signed off while another's are held, so both are per-unit.
The narrative arc is one object that is accepted or not as a whole, so it stays one page however long it grows.
Size is not the test: a long unit that is approved together stays a row, and a short unit with its own gate earns a page.

#### 1.2 · The filename says family, unit and slug; the group says who rules it
(four parts, and the two that disagree on purpose)

```text
  S-<Family>-<unit>-<slug>.md
    │         │       └── short lowercase name
    │         └────────── which unit: a number, a letter, or Dash
    └──────────────────── the family that wrote the page
```
The family is the stage folder that produced the page, so `S-Narrative-0-arc` comes from `0-lifecycle/3-narrative/`.
The group is the concern that rules it, and the two come apart wherever a venue-aligned stage feeds a venue-free rung, which is why the figure marks those lines with `←`.

#### 1.3 · Dash is the control page, and the accumulating units number rather than letter
(the inventory that is not a unit, and the number-or-letter choice)
`S-<Family>-Dash` lists which units exist and which are gated, and no stage writes it, so a reader meeting a `Dash` page knows it is an inventory rather than a missing unit.
A description's order is not an argument, so a late description added as `7` renumbers nothing and numbers are fine.
A claim a reviewer forces late is safer as a letter so nothing citing `S-Claims-1` moves; this proposal uses numbers and flags the choice for JL.

### 2 · Delivery · Opening, three single pages
**Three homes, one concern**: the seed wager, the venue pin, and the promise.

```text
  📄 pages    3 · none per-unit
  🧩 a unit   there is none: each page is one statement
  🗂 control  none needed at three pages
  📍 today    S-Seed-0 built · the other two proposed
```
QB1 states that the Opening is one concern living in three folders, settled at three different moments with the whole ladder between the first two.
Each is one thing to accept or reject, so none of the three splits, and three pages need no inventory above them.

### 3 · Delivery · Description, one page per facet
**Six facets, six pages**: the count is read off QB2, not estimated.

```text
  📄 pages    6 units + 1 Dash
  🧩 a unit   one facet of the profile, filled or waived
  🗂 control  Dash lists the six and which are waived
  📍 today    1a-descriptions/ is empty · all proposed
```
QB2 sets coverage as a floor of six facets: cohort, arms, outcomes, time window, data quality, and benchmark.
Each facet is either filled with D ids or waived with a one-line why, and a waiver is banked for the next round rather than lost, which is exactly a state a page can carry and a row cannot.
That is why the count here is six and not the four an earlier draft guessed.

### 4 · Delivery · Themes, one page per promoted theme
**Promoted gets a page, Parked gets a line**: the split that keeps the group small.

```text
  📄 pages    1 per PROMOTED theme + 1 Dash
  🧩 a unit   one pattern that passed promotion into 1c
  🗂 control  Dash holds Parked, the reservoir
  📍 today    1b-themes/ is empty · all proposed
```
QB3 sweeps three lenses and banks what a round notices and drops into Parked, which the next round re-mines rather than discards.
A parked pattern has no gate of its own and is not consumed by anything, so it is a line on the Dash; promotion into the claim rung is what earns a theme its own page.
Without that split the group would grow a page for every passing thought a sweep produced.

### 5 · Delivery · Claims, one page per claim
**The ledger, split**: one page per claim so each carries its own status.

```text
  📄 pages    1 per claim + 1 Dash
  🧩 a unit   one claim, with its own supported | weak | GAP
  🗂 control  Dash is the ledger view across all claims
  📍 today    1c-claims/ is empty · all proposed
```
QB4 makes the ledger the only home of a claim's status, and a status per claim is precisely what a single shared page cannot carry.
The Dash keeps the ledger readable as one table while each claim page holds its evidence, its campaign, and the anchor its status rests on.

### 6 · Delivery · Advice, one page per entry, plus the arc
**Advice splits, the arc does not**: the group that holds two families.

```text
  📄 pages    1 per advice entry + 1 Dash + 1 narrative
  🧩 a unit   one advice entry, adopted or declined downstream
  🗂 control  Dash lists entries and who adopted each
  📍 today    1d-advice/ is empty · all proposed
```
QB5 has each downstream stage adopt or decline an entry on its own terms, and a declined entry waits for the next round rather than being discarded, so adoption is a per-entry state.
The narrative arc reads the whole 1d table and composes one thing, so `S-Narrative-0-arc` is a single page and is marked `←` because its family is Narrative while its group is Advice.
The arc is venue-gated: it exists only when the pinned venue requires the aligned stages.

### 7 · Delivery · Display, one page per unit, and the venue may delete the group
**Gated before counted**: the only group a venue can remove entirely.

```text
  📄 pages    1 per display unit + 1 Dash, or ZERO
  🧩 a unit   one panel, chart, or section with one job
  🗂 control  Dash maps claim to unit
  ⏭ gate     skipped: sms · push · reminder · checklist
             required: dashboard · ui-card · report
  📍 today    fixture is sms, so the group is SKIPPED
```
QB6 reads the gate from the intervention's `STATUS.md`, so on the `01_sms_young_male` fixture an absent Display group is correct rather than missing.
This is the one place where absent and proposed mean different things, and the figure marks it `⏭` rather than leaving it to the blanket legend.

### 8 · Delivery · Artifact, one page per segment, arms inside
**Where the page line falls**: between the segment and the arm, not below it.

```text
  📄 pages    1 per segment + 1 Dash
  🧩 a unit   one segment's message set, signed off together
  🗂 control  Dash lists segments and their status
  📍 today    0-artifacts/ is empty · all proposed
```
QB7 makes the shipped file one markdown deliverable at `0-artifacts/<slug>-v{N}.md` whose content restates what lives upstream.
A segment's messages are signed off together and independently of another segment's, so the segment is the unit and the page.

#### 8.1 · Each arm is a Content division inside the segment page
(the segment by arm matrix, cut where the scope branch already cuts it)
Inside a segment page each arm is one Content division, so the page-against-division line falls between the segment and the arm, exactly where the dataset-wide spine branches per segment.
Every arm for the segment sits on that one page, which is what lets a reviewer compare them and sign the segment off in a single pass (JL 260802, Design A; see `## Law`).

### 9 · Delivery · Deploy, three single pages
**Two audits and a gate**: three steps, none of which repeats per unit.

```text
  📄 pages    3 · none per-unit
  🧩 a unit   there is none: each page is one pass
  🗂 control  none needed at three pages
  📍 today    all proposed
```
QB8 runs review and claim audit as two passes that raise a draft to reviewed, and keeps ship behind a person, so the three pages are three steps rather than three units.
The passes run over whatever the Artifact group produced, so their count does not grow when a segment is added.

### 10 · Delivery · Iterate, one page per round
**A batch is the carrier**: the group that grows with time rather than with units.

```text
  📄 pages    1 per A/B round
  🧩 a unit   one batch, from deploy to ladder refresh
  🗂 control  none · the round folder carries the batch
  📍 today    1-rounds/ is empty · all proposed
```
QB9 keeps one A/B batch together from deploy through the ladder refresh, and the round folder is what carries it.
A round is finished or it is not, so the page is per round and never per result inside it.

### 11 · The machinery, present but never a stage
**Two things that are always there**: neither is a stage, and one is not even a page.

```text
  🔬 PPNN-<topic>    one per topic in 1-probes/ · a real page
  🧾 Gate Ledger     a stage gate row in STATUS · NOT a page
```
The probe files are pages a reader opens, so they are listed, but no stage writes them on a schedule and they are not part of the ladder.
The gate ledger is a row inside `STATUS.md`, listed here only so a reader who looks for it does not conclude the board lost it; it is never counted in the page total.

## Aims

### A1 · 🧭 The rules that hold across every group
- A1.1 · The approve-or-reject test is stated and is the only thing deciding page against row.
  **Done when:** `§1.1` gives the test and at least one worked case each way, and no group division re-argues it.
- A1.2 · The filename grammar names its parts and says where family and group come apart.
  **Done when:** `§1.2` names the parts and the figure marks every page whose family is not its group's own.
- A1.3 · The control page and the number-or-letter choice are stated.
  **Done when:** `§1.3` defines `Dash` and JL rules number or letter for the accumulating families.

### P · 🏁 Page-level
- P1 · Every group the figure draws has exactly one Content division, in figure order, answering the same four questions.
  **Done when:** the group count in the figure equals the division count after `§1`, and every such division opens with the pages, unit, control, today block.
- P2 · Built, skipped and proposed are accounted per group rather than by one blanket line.
  **Done when:** each group division's `📍 today` row names what exists, and the figure marks `✅` and `⏭` where they apply.
- P3 · The layout reads as the whole intervention board in one view, and nothing a real board carries is unlisted.
  **Done when:** a reader can count the pages of a finished intervention off the figure alone.

## States

### Decision Now
- [ ] 🗣 Adopt the per-unit page model for the accumulating rungs?
      📍 `Part` 1.1 · A unit earns a page when it can be approved while its neighbour is rejected
      🔔 `Why now` JL asked to follow the paper's rule so each unit is a page, and the layout is drawn that way but not yet ruled
      ⭐ `A · per-unit` for Description, Themes, Claims, Advice, Display, Artifact, each with a Dash control; recommended
      `B · single page` per rung with units as rows, keeping the current 1a-1d files as-is
      🛑 `Blocks` how the fixture's `0-lifecycle/` is scaffolded and how many pages a real board carries
      🤖 `If nobody answers` per-unit, with a Dash control per accumulating family
- [ ] 🗣 Do the accumulating units number or letter?
      📍 `Part` 1.3 · Dash is the control page, and the accumulating units number rather than letter
      🔔 `Why now` a claim or advice a reviewer forces late renumbers everything if the units are numbered
      ⭐ `A · numbers` matching JL's "description one, description two"; simplest, recommended for now
      `B · letters` so a late unit lands last and nothing citing an earlier one moves
      🛑 `Blocks` nothing
      🤖 `If nobody answers` numbers
- [ ] 🗣 Does the folder-stem naming rule extend past the four rungs, to pitch and narrative?
      📍 `Part` 1.2 · The filename says family, unit and slug; the group says who rules it
      🔔 `Why now` the Law ruled the stem rule for the four rungs only, and pitch and narrative each own a stage folder while the paper board files both under family Venue
      ⭐ `A · extend it` so `2-pitch/` gives `S-Pitch-0-pitch` and `3-narrative/` gives `S-Narrative-0-arc`; one folder is one family with no exceptions; drawn this way, recommended
      `B · keep the paper's grouping` with `S-Venue-1-pitch` and `S-Venue-2-narrative`, so the Opening group holds one family instead of three
      🛑 `Blocks` the filenames in `§2` and `§6`, and which lines the figure marks with `←`
      🤖 `If nobody answers` extend it
- [ ] 🗣 What does one design lifecycle board scope to, one dataset or one segment?
      📍 `Part` 8 · Delivery · Artifact, one page per segment, arms inside
      🔔 `Why now` the per-unit message split assumes the segment is the branch, which the scope choice confirms or overturns
      ⭐ `A · one dataset` with the segment as a branch from S-Claims down, so the dataset-wide rungs are shared; recommended
      `B · one segment` per board, duplicating the shared Description and Themes
      🛑 `Blocks` whether `01_sms_young_male` stays segment-scoped (a QA1 folder-granularity question)
      🤖 `If nobody answers` one dataset, segment branches at S-Claims

### A1 · 🧭 The rules that hold across every group
- 🔨 A1.1 · Drafted; the test is stated in `§1.1` with the claim and segment cases, and the group divisions cite it rather than re-argue it.
- 🔨 A1.2 · Drafted; the grammar is stated and the figure marks the two `←` lines, pending the stem-rule ruling.
- 🧠 A1.3 · Waiting on JL; `Dash` is defined and the number-or-letter choice is a Decision Now row.

### P · 🏁 Page-level
- ✅ P1 · Met; the figure draws ten groups and Content carries ten divisions after `§1`, each opening with the same four-row block.
- ✅ P2 · Met; every group division names what exists today, and the figure marks `S-Seed-0` built and the Display group skipped for the sms fixture.
- 🔨 P3 · Active; the counts for Opening, Description, Deploy and Display are read off QB1, QB2, QB6 and QB8, while Themes, Claims, Advice and Artifact stay `<placeholder>` because their counts depend on a round that has not run.

## Files

### Input files
- `../../1-QA-design/QA3-the-intervention-board/QA3-the-intervention-board.md`
  The ruling that turns `0-lifecycle/` into a board; this page proposes the pages that board carries.
- `../../board.md`
  The group registry: its `### QB · Delivery` block names the nine groups and assigns narrative to QB5's engine column.
- `../QB2-data/QB2-data.md`
  The six-facet coverage floor that `§3` counts pages from.
- `../QB6-display/QB6-display.md`
  The venue gate that lets `§7` mark the Display group skipped rather than proposed.
- `../../../PaperSkillBoard-260725/board.md`
  The paper board's own layout page, whose per-unit and control-page rules this proposal follows.
- `../../../../application/README.md`
  The ladder, the intervention-folder layout, and the maturity vocabulary.

### Contracts
- `../../../../board/haipipe-board/ref/page-template.md`
  The base every page kind varies from, including the S-page identity line each unit page carries.
- `../../../../board/haipipe-board-sentence/`
  The contract for what attaches to a row inside a page: lanes, cards, links.

## Law
- 260802 JL · ⚖️ One board group is one Content division, in figure order
      QB0's Content opens with `§1`, the rules true across every group, and then carries exactly one division per group the figure draws, answering the same four questions each time.
      The earlier shape was three cross-cutting divisions, which had no room to say what a unit IS in each group, and a unit is a different thing in Themes than in Artifact; the 1:1 shape also makes each group's page count individually citable as `QB0 §5`.
- 260802 JL · ⚖️ A message intervention uses Design A: each arm is one Content division inside a per-segment S-Artifact page, not its own page
      A reviewer sees every arm for a segment on one page and signs the segment off in a single pass, which is what makes review easy.
      Design B, one page per arm, was rejected because it scatters the arms across pages and forces a separate gate per arm; a single arm graduates to its own page only if it grows an independent A/B or compliance life, the paper board's inline-until-it-earns-a-page rule.
- 260802 JL · ⚖️ The four rung S-pages are named for their ladder folder stems
      S-Description, S-Themes, S-Claims, and S-Advice, from `1a-descriptions` through `1d-advice`; S-Opening keeps its name for the seed.
      S-Data and S-Topics were the earlier draft and were rejected, so the S-name tracks the folder and skill vocabulary rather than the DIKW gloss, which stays as the letter beside each rung; S-Advice is kept singular to match the `1d-advice` folder and normal English.

## Glossary
- **unit**: one member of a family that can be approved or rejected on its own, such as one description or one claim.
- **per-unit**: a family that gives each unit its own page, above a control page, as opposed to holding its units as rows on one page.
- **control page**: a family's inventory page, named `Dash`, that lists its units and which are gated; no stage writes it.
- **join**: a page whose family is not the one its group is named for, marked `←` in the figure, such as the narrative arc sitting in the Advice group.
- **gated**: a page or a whole group that exists only when the pinned venue requires it, marked `⏭` when the fixture's venue removes it.

## Log
260802 · Content restructured to one division per group on JL's ruling: `§1` keeps the cross-cutting rules as three paragraphs, and `§2` to `§11` carry the nine Delivery groups plus the machinery, each answering pages, unit, control, today; Aims collapsed to A1 plus P1-P3 because no single group's page count is a durable target.
260802 · Diagram corrected against its own page: the narrative arc was missing though `§1` listed it as a single-page family, `S-Theme`/`S-Claim` contradicted the Law's `S-Themes`/`S-Claims`, the four invented description names became the six facets QB2 rules, the Display group is now marked skipped for the sms fixture rather than proposed, and the marker convention moved to unmarked-means-proposed so the one built page stands out.
260802 · JL ruled Design A for messages: each arm is a Content division inside the per-segment S-Artifact page, not its own page, because it makes review easier; the ruling moved from `§3.1` to `§8.1` in the restructure and is recorded in `## Law`.
260802 · QB0 reproposed as a per-unit layout: each rung splits into one page per unit above a Dash control, following the paper board's QB0; drawn against the fixture, which carries only S-Seed-0 so the rest is proposed.
260802 · JL ruled the rung S-names S-Description, S-Themes, S-Claims, S-Advice (dropping S-Data, S-Topics); recorded in `## Law`.
260802 · QB0 created: the S-page spine, the naming map, and the Q-concern versus S-stage duality.
