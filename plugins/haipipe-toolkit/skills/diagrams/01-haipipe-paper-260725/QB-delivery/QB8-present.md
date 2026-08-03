# Delivery Present: slides and posters that project the paper and never become it

state: ✅ RULED
owner: JL
method: project the accepted paper argument into audience-facing slides and posters without changing manuscript authority

## Opening

What belongs under Present, and what stays owned by the paper?

Present holds audience-facing projections: a slide deck and a poster. A projection is built from accepted pages and never becomes a source anyone edits back. The risk is the deck: it is the version people actually see, so a claim added there quietly outruns the paper.

**Where this page sits**: QB5 Display owns the reusable visual units and their promoted assets.
This concern takes those and the accepted argument, and turns them into something an audience sits through.

**Why the risk runs one way**: nobody edits a paper to match a slide, and everybody edits a slide to land in a room.
So a slide can overclaim without anything catching it, which is the one failure this concern exists to gate.

**What the gate tests**: audience fit, and that no slide or poster claim exceeds what the paper supports.
That second half is the one a person has to check, because no build can compare a spoken claim to a written one.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `../01-boardform-260722/QB-delivery/QB4-overall.md` and are not restated here.

**This page DESIGNS; the paper board SHOWS**: `### 2` states what a paper must carry for this concern, not what one paper happens to have today.
Where the MISQ paper differs, say so as a gap with an owner, never as the definition.

**Always write the direction**: the paper projects to the deck, never the reverse.
A sentence that lets a deck feed the paper has conceded the only thing this concern protects.

## Diagram

**One direction, two audiences**: what feeds a projection, and what a person must check.

```text
   ✍️ ACCEPTED PAPER                    🎤 PROJECTIONS
   ─────────────────                    ──────────────
   narrative · claims · values   ━━━━▶  📊 slides
   promoted display units        ━━━━▶  🖼 poster

   🚪 a human accepts audience fit AND verifies that no slide or
      poster claim exceeds the paper
   🚫 nothing here ever becomes manuscript source
   ⚡ the deck is the version people SEE, so overclaiming here is
      the failure that costs most and reports itself least
```

## Content

### 1 · The delivery contract

**What Present owes**: an audience-facing projection that says no more than the paper does.

```text
  📥 CONSUMES                📤 PROJECTS TO           🚪 GATE
  accepted narrative    ━━▶  paper slides       ━━▶  a human accepts
  claims · values            paper poster            audience fit, and
  displays                                           no claim exceeds
                                                     the paper
```

📜 Establishes what a projection may be built from, and the one thing a person must check before it is shown.

| Field | Contract |
|---|---|
| Lifecycle | After enough Main/Display content exists to present coherently. |
| Authority | The accepted S pages and Display units, not the slide deck. |
| Projects to | Paper slides and poster artifacts. |
| Skills | Present/slide/poster projection skills. |
| Consumes | Accepted narrative, claims, values, and displays. |
| Gate | A human accepts audience fit and verifies no slide/poster claim exceeds the paper. |
| Open gaps | Present needs concrete skill pages when its first cross-paper contract is tested. |

#### 1.1 · A projection is judged against the paper, not against the room
(a deck that lands beautifully and overstates one result has failed this gate)
Audience fit is the easy half and a presenter can judge it alone.
The half that needs the gate is whether every claim on a slide is one the paper already supports, because the pressure in a talk is always toward the stronger sentence.

### 2 · What we want on the paper board

**The group we are designing**: one Q page, and no S page at all.

```text
  🎯 WHAT WE WANT a paper to carry for this concern
  ### Delivery · Present
        📄 QP0-present-delivery.md   a Q page: how THIS paper projects
        🚫 no S page                 nothing is authored per-unit here

  ⚡ this concern owns NO STAGE ── `../../paper/route/haipipe-paper-stage/stages/index.yml` has no `present` key
  🔑 the artifacts live OUTSIDE 0-lifecycle/
     5-present/paper-slides/ · 5-present/paper-poster/
  🔗 same shape as QB4 Value: one Q page, a rule, no prose of its own
```

🎯 Establishes what a paper board must show for this concern, and why one Q page is the whole of it.

#### 2.1 · The artifacts sit outside the lifecycle folder, and that is deliberate
(a deck is a deliverable, and `0-lifecycle/` is working machinery)
Slides and posters live under `5-present/`, not under `0-lifecycle/`, because they are things a person hands to an audience.
The board page records how this paper projects; the deck itself is the product, and the delete test says the numbered tree can go while the deck must not.

#### 2.2 · One Q page, because the rule does not vary by deck
(a paper may have several talks, and they all obey the same gate)
A conference talk, a job talk, and a poster are three projections of one accepted argument.
Each is built the same way and each faces the same check, so the concern needs one page stating the rule rather than one page per event.

#### 2.3 · Where the MISQ paper stands against this
(the group is built as designed, and no cross-paper contract has been tested yet)
`Delivery · Present` holds `QP0-present-delivery.md` and no S page.
The open gap is that Present has no concrete skill pages, and it will not get them until a first cross-paper contract is actually exercised.

## Aims

### A1 · 📜 The delivery contract
- A1.1 · Slides and posters sit in one projection family under Present.
  **Done when:** no board opens a separate slide group, and both artifacts are governed by this concern's gate.
- A1.2 · A projection never becomes manuscript source.
  **Done when:** no deck or poster file is read by the paper build, and every claim on one traces to an accepted page.

### A2 · 🎯 What we want on the paper board
- A2.1 · A paper board shows this concern as one group holding one Q page.
  **Done when:** `Delivery · Present` lists a present-delivery Q page, and no S page is created for a concern that authors no prose.

## States

### A1 · 📜 The delivery contract
- ✅ A1.1 · JL confirmed on 260729 that Present includes slides and that no separate slide group is needed.
- ✅ A1.2 · Ruled and carried in the Law: Present contains slides and posters, they project the paper, and they do not become manuscript source.

### A2 · 🎯 What we want on the paper board
- ✅ A2.1 · Built as designed on the MISQ paper: `Delivery · Present` holds `QP0-present-delivery.md` and no S page.

## Files

📋 **Contracts** · what carries this page's rule to somewhere else

- `board.md` · the `## Pages` order and the Board Map row for this concern
- `QB5-display.md` · owns the promoted display units a projection reuses

📥 **Input files** · what the work reads

- `../../display/skills/haipipe-display-slides/SKILL.md` · the slide renderer this concern commissions
- `../../display/skills/haipipe-display-poster/SKILL.md` · the poster renderer

## Law

- Present contains slides and posters. They project the paper; they do not become manuscript source.
  A projection is accepted only when a human has checked both audience fit and that no claim on it exceeds the paper.

## Glossary

- **Present**: audience-facing projections of the accepted paper argument.
- **Projection**: an artifact built from accepted pages that is never edited back into them.

## Log

260802 · Migrated to the QB4 page contract and given `### 2 · What we want on the paper board`. It is the second concern with no S page, the same shape as QB4 Value, and its artifacts sit outside `0-lifecycle/` because a deck is a deliverable rather than working machinery.
260729 · JL kept the name Present and confirmed that it includes slides.
