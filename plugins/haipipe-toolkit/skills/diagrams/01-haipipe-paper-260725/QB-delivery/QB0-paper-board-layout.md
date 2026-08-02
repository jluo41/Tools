# The paper board layout: every group, every page, and how a filename is built

state: 🟡 PARTIAL · the layout is drawn from a live paper; three of its rules are not yet enforced
owner: JL
method: draw the whole paper board in one place, so a reader sees the shape before opening any one concern

## Opening

What does a paper's own board look like, all of it, on one page?
A paper board is the `0-lifecycle/board.md` inside a paper, such as the MISQ one.
It is grouped by Delivery concern, so the `Delivery · Opening` group there is what QB1 rules here.
A page in that group is an S page, such as `S-Work-1-claims.md`.
The shape only goes wrong at the joins between groups, and one concern page can never show a join.
So this page draws all ten groups at once.

**Where this page sits**: it sits before QB1 and is the only page here that shows the whole board.
Every concern page carries a `What we want on the paper board` division for its own group; this one is the index those ten divisions are slices of.

**Why one page has to hold the whole thing**: the shape is only wrong in the joins.
A filename says which family wrote a page and a group says which concern owns it, and those two disagree on purpose in three places. Nobody sees that by reading one concern at a time.

**What it is measured against**: the MISQ paper, which is the only paper built far enough to show every group.
Where the design and that paper differ, the difference is named as a gap with an owner.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**This page DESIGNS; the paper board SHOWS**: it states what a paper must carry, not what one paper happens to have today.
Where the MISQ paper differs, say so as a gap with an owner, never as the definition.

**The PAPER board is the spine of every figure here**: a group name leads the line and the QB id annotates it, never the other way round (JL 260802).
**ONE PAGE, ONE LINE** (JL 260802): never put two page names on the same line to save space. A reader counting pages must be able to count lines.
This page answers what a paper carries, so a reader scanning the left edge must see the paper's own groups.

**Never restate a concern's own rules**: QB1 to QB10 own those.
This page owns only what is true ACROSS them: the group list, the filename grammar, and the joins where family and concern come apart.

**A count here is a real count**: every number on this page was read off a live paper, never estimated.
If a number cannot be read off disk, do not write one.

## Diagram

**The whole paper board**: every page a paper carries, one per line, under the group that owns it.

```text
  📁 <paper>/0-lifecycle/ ── the board is a FOLDER, not one file
     board.md is only its registry; the pages live in the subfolders
  ════════════════════════════════════════════════════════════════
  🎯 WHAT WE EXPECT a paper to carry, group by group
  ### Delivery · Opening                            ◀ ruled by QB1
      📁 0-seed/ + 2-venue/
      🌱 S-Seed-0-seed
      🎯 S-Venue-0-venue
      📣 S-Venue-1-pitch
  ### Delivery · Work                               ◀ QB2
      📁 1-work/ + 2-venue/
      📦 S-Work-0-resources
      🎯 S-Work-1-claims
      🧵 S-Venue-2-narrative                        ← family Venue
  ### Delivery · Literature                         ◀ QB3
      📁 0-seed/ + 4-main/
      🗺 S-Seed-1-literature                        ← family Seed
      📖 S-Main-2-literature                        ← family Main
  ### Delivery · Value                              ◀ QB4
      📁 delivery-value/
      📄 QV0-value-delivery                         ← a Q page, no S page
  ### Delivery · Display                            ◀ QB5
      📁 3-display/
      🗂 S-Display-Dash                             the control page
      📄 S-Display-1a-hero-concept
      📄 S-Display-1b-research-design
      📄 S-Display-2a-distribution
      📄 S-Display-2b-validation-summary
      📄 S-Display-2c-llm-measurement
      📄 S-Display-3a-funnel
      📄 S-Display-3b-descriptives
      📄 S-Display-3c-variable-operationalization
      📄 S-Display-4al2-main-regression
      📄 S-Display-4al5-main-regression
      📄 S-Display-4b-context-regression
      📄 S-Display-4c-discretion-gradient
  ### Delivery · Main                               ◀ QB6
      📁 4-main/
      🗂 S-Main-Dash                                the control page
      📄 S-Main-0-abstract
      📄 S-Main-1-introduction
      📄 S-Main-3-theory                            ← 2 is under Literature
      📄 S-Main-4-measurement
      📄 S-Main-5-empirical
      📄 S-Main-6-results
      📄 S-Main-7-discussion
      📄 S-Main-8-conclusion
  ### Delivery · Appendix                           ◀ QB7
      📁 5-appendix/
      🗂 S-Appendix-0-control                       the control page
      📄 S-Appendix-A-prompts
      📄 S-Appendix-B-validation
      📄 S-Appendix-C-variables
      📄 S-Appendix-D-iv
      📄 S-Appendix-E-robustness
      📄 S-Appendix-F-bigfive
  ### Delivery · Present                            ◀ QB8
      📁 delivery-present/
      📄 QP0-present-delivery                       ← a Q page, no S page
  ### Delivery · Build                              ◀ QB9
      📁 6-submission/
      📄 S-Submission-0-reconcile
      📄 S-Submission-1-compile
      📄 S-Submission-2-review
      📄 S-Submission-3-submit
  ### Delivery · Round                              ◀ QB10
      📁 7-round/
      📄 QR0-round-delivery
      ⚠️ one S-Round per batch, once Round is a family

  🔤 S-<Family>-<unit>-<slug>.md
     the FAMILY says who wrote it · the GROUP says who owns the rule
     ← marks the four places they differ on purpose
```

## Content

### 1 · Ten groups, three kinds of concern

**Not every concern owns a stage**: six of the ten own none.

```text
  🏗 GROUPS ITS OWN STAGES            the concern runs stages
     Delivery · Opening    seed · venue · pitch            ◀ QB1
     Delivery · Work       resource · claims · narrative   ◀ QB2
     Delivery · Display    display                         ◀ QB5
     Delivery · Main       section-edit                    ◀ QB6

  📎 GROUPS PAGES OTHER STAGES WROTE  a rule over someone else's pages
     Delivery · Literature · Appendix · Build     ◀ QB3 · QB7 · QB9

  📄 ONE Q PAGE AND A RULE            no stage, no S page, no prose
     Delivery · Value · Present · Round           ◀ QB4 · QB8 · QB10
```

🧭 Establishes the three shapes a Delivery concern can take, so an empty-looking group is read correctly.

#### 1.1 · A thin group is not an unfinished group
(QB4 Value holds one Q page, and that is its finished state)
`index.yml` declares no `value` stage, no manuscript section belongs to it, and the work it causes happens inside other pages' sentences.
Reading thin as unfinished is the mistake this division exists to stop, and the same holds for Present and for Round before a paper is reviewed.

### 2 · What a filename says, and what it does not

**Family against group**: the one join a reader gets wrong.

```text
  S-<Family>-<unit>-<slug>.md
    │         │       └── short lowercase name
    │         └────────── which unit, within the family
    └──────────────────── WHO WROTE IT, never who owns the rule

  🔀 the three places they disagree, all deliberate
     S-Seed-1-literature    family Seed    ▸ group Literature
     S-Main-2-literature    family Main    ▸ group Literature
     S-Venue-2-narrative    family Venue   ▸ group Work

  🔑 no contract spells a filename: a stage declares board_family,
     board_unit and board_slug, and stage.py resolve composes it
```

🔤 Establishes the naming grammar and the deliberate joins, so a reader stops expecting family and group to match.

#### 2.1 · The family carries a fact the group cannot
(venue-FREE against venue-ALIGNED: does a retarget rewrite this page?)
Seed, resource and claims are venue-free, and a retarget leaves them alone.
Pitch, narrative, display and section-edit are venue-aligned and rewrite when the paper changes journal, which is why narrative keeps `board_family: Venue` even though QB2 Work owns the arc.

#### 2.2 · A unit is lettered, numbered, or named, and each choice has a reason
(Appendix letters so a late unit renumbers nothing; Main numbers because order is the argument)
Appendix uses `A` to `F`: a reviewer's late request lands as `G` and nothing citing `A` moves.
Main uses `0` to `8`: a section's position is part of what it claims.
A family control page takes a name, `Dash` or `0-control`, because it is not a unit at all.

#### 2.3 · The folder on disk follows the FAMILY, never the group
(so a group that spans two families also spans two folders)
`0-lifecycle/` holds one subfolder per family: `0-seed/`, `1-work/`, `2-venue/`, `3-display/`, `4-main/`, `5-appendix/`, `6-submission/`, `7-round/`.
Every page sits in the folder its family names, so `S-Venue-2-narrative.md` is in `2-venue/` even though `Delivery · Work` owns it.
Folder and family always agree; the group is the one cut that differs, and it differs in four places.
The Q pages break the pattern: `QV0` and `QP0` sit in `delivery-value/` and `delivery-present/`, named after the CONCERN, while `QR0` sits in `7-round/`, named after the family slot. That is an inconsistency nobody has ruled.

### 3 · The three page kinds inside a group

**What can sit in a group**: and the one thing that is no longer allowed.

```text
  📄 a STAGE page        one per runs:once stage        S-Work-1-claims
  📑 PER-UNIT pages      when one unit can be approved  S-Main-0 … 8
                         while another is rejected      S-Appendix-A … F
  🗂 a CONTROL page      the family's inventory         S-Main-Dash
                         no stage writes it             S-Appendix-0-control

  🚫 NO central decision register (JL 260802)
     a decision is a Decision Now row on the page that owns it
```

🗂 Establishes what may appear in a group, and why "one stage, one page" holds in only one direction.

#### 3.1 · Every stage makes a page; not every page comes from a stage
(the control pages have no stage, and that is correct rather than missing)
`S-Main-Dash` and `S-Appendix-0-control` answer what a unit page cannot: which units this paper has, and which are gated.
`index.yml` declares no stage for either, so a reader looking for the stage behind them will not find one.

#### 3.2 · Per-unit is decided by the gate, not by size
(QC3b: "a stage is `per-unit` exactly when one unit can be approved while another is rejected")
That is why Main and Appendix split into pages and why Work's resource and claims stages should too: one resource is verified while the next is still being chased, and C1 is supported while C2 is inconclusive.
It is also why narrative stays one page, because a paper has one arc and there is nothing to approve separately.

## Aims

### A1 · 🧭 Ten groups, three kinds of concern
- A1.1 · A reader can tell a thin group from an unfinished one.
  **Done when:** each of QB4, QB8 and QB10 states on its own page that one Q page is its finished shape.

### A2 · 🔤 What a filename says, and what it does not
- A2.1 · The three family-against-group joins are stated where a reader meets them.
  **Done when:** QB3, QB2 and this page each name their join, and no page implies family and group must match.

### A3 · 🗂 The three page kinds inside a group
- A3.1 · Work's resource and claims stages split into per-unit pages with a control page each.
  **Done when:** a paper carries `S-Work-R` plus `S-Work-R1…` and `S-Work-C` plus `S-Work-C1…`, and the old single pages are their controls.
- A3.2 · The parser accepts a capital-plus-digit unit.
  **Done when:** `src/parse.py` matches `S-Work-R1-<slug>.md`, and a rebuild shows no existing page re-parsing differently.

### P · 🏁 Page-level
- P1 · Every number on this page is read off a live paper.
  **Done when:** a check resolves each count here against the MISQ board rather than trusting the prose.

## States

### A1 · 🧭 Ten groups, three kinds of concern
- ✅ A1.1 · Done 260802. QB4 `§2.2`, QB8 `§2.2` and QB10 `§2.1` each say so on their own page.

### A2 · 🔤 What a filename says, and what it does not
- ✅ A2.1 · Done 260802. QB2 `§1.3` names the narrative join, QB3 `§2.1` names the literature one, and `§2` here names all three.

### A3 · 🗂 The three page kinds inside a group
- 🔨 A3.1 · Ruled by JL on 260802, option A, and now unblocked: `stage.py resolve` composes `S-Work-R1-<slug>.md`. No paper carries the new names yet, so splitting the MISQ resource and claims pages is the remaining work.
- ✅ A3.2 · Done 260802. `src/parse.py` gained `[A-Z]\d+` ahead of `[A-Z]`, and `cli/stage.py`'s `resolve_filename()` gained the matching branch, so the read and write sides agree. Proved safe by rebuilding both boards and diffing the page list: 85 pages on this board and 47 on the MISQ paper, byte-identical before and after.

### P · 🏁 Page-level
- ⬜ P1 · Not started. Every count here was read off the MISQ board by hand on 260802, and nothing re-checks them.

## Files

📋 **Contracts** · what carries this page's rule to somewhere else

- `board.md` · the `## Pages` order this page indexes
- `QB1-opening.md` · the first concern, and the pattern the other nine follow

📥 **Input files** · what the work reads

- `../../paper/1-lifecycle/haipipe-paper-stage/stages/index.yml` · declares which stages exist, and therefore which concerns own one
- `../../board/haipipe-board/src/parse.py` · owns the filename grammar this page describes
- `../QC-engine/QC3b-page-name.md` · owns the per-unit test and the naming Law

## Law

- 🔠 **A capital plus digits is a per-unit member of a lettered series** (JL 260802). `S-Work-R` is the control page and `S-Work-R1` is one unit. In the read regex it must lead `[A-Z]`, which would otherwise consume the `R` and leave the page silently unparseable rather than rejected.
- 🔤 **A filename names the FAMILY that wrote a page; a group names the CONCERN that owns its rule.** They disagree in three places on purpose, and a reader must never infer one from the other.
- 🗂 **Every stage makes a page, and not every page comes from a stage.** A family control page has no stage and is not missing one.
- 📄 **A concern with one Q page and no S page is finished, not thin.** Value, Present and Round are all correct in that shape.
- 🔠 **In Work, the letter says the stage and the number says the unit** (JL 260802, choosing option A). `R` resource, `C` claims, `N` narrative; `S-Work-R` is the control and `S-Work-R1` is a unit. Rejected: reusing the existing `0a` and `1b` shape, which parses today with no code change but buries the stage behind a number and breaks every name if two stages ever swap order.

## Glossary

- **Paper board**: the `0-lifecycle/` FOLDER inside a paper. `board.md` is its registry and the pages live in one subfolder per family.
- **Family**: the first token of an S filename, saying which stage family authored the page.
- **Control page**: a page that inventories a family's units and that no stage writes.

## Log

260802 · JL: the paper board is a FOLDER, not just a `board.md`, and these groups are what we EXPECT rather than a report. The figure header now names the folder and says so, each group carries the subfolder its pages live in, and `§2.3` states the rule that came out of checking it: the folder follows the FAMILY exactly, so the group is the only cut that differs. Found while checking: `QV0` and `QP0` sit in folders named after the concern while `QR0` sits in one named after the family slot, and nobody has ruled that.
260802 · JL: one page, one line. The Opening, Work, Literature and Build rows had been packing two or three page names onto a line, and Display, Main and Appendix had been collapsed to a count. Every page a paper carries is now its own row, 45 of them, and the Writing Style carries the rule.
260802 · JL: the figures were skill-board led, with QB ids down the left edge and the paper's pages on the right, and the two edges did not line up. Redrawn with the PAPER board as the spine: each line starts with the group a paper carries and the QB id annotates it on the right. A Writing Style rule now holds it that way.
260802 · A3.2 closed. The unit grammar now accepts a capital plus digits on both sides: `src/parse.py` reads it and `cli/stage.py resolve_filename()` composes it. Nothing existing moved, proved by rebuilding this board and the MISQ paper board and diffing their page lists, 85 and 47, byte-identical. Found while doing it: `resolve_filename()` rejects `Dash`, which the reader accepts and `S-Main-Dash.md` uses, so the write side has been narrower than the read side for some time.
260802 · Opened on JL's ask, because nothing showed the whole paper board: each of QB1 to QB10 carried only its own group. Drawn from the MISQ paper, the only one built far enough to show every group. Three cross-concern facts landed here rather than being repeated ten times: the three kinds of concern, the family-against-group grammar with its three deliberate joins, and the three page kinds a group may hold.
260802 · JL chose option A for Work's unit naming: the letter says the stage, the number says the unit. A3.2 opened, because the parser rejects a capital-plus-digit unit today.
