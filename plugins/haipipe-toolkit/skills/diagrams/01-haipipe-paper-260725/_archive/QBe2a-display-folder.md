# The Display as a split unit: one identity living in two filesystem roles

state: 🟡 PARTIAL
owner: JL
method: keep one display identity while separating authoritative rebuild work from the journal-facing projection

## Opening

What is one Display unit made of, and which half goes to the journal?

A unit is one figure or table with a single stable id. A projection is the small journal-facing copy of it. The workspace is everything used to rebuild it and never shipped. One object, two filesystem roles, and the id is what keeps them the same object.

**Where this page sits**: QBe2 heads the float series, and `QA3@display` already ruled why a unit has both a page and a folder: a page decides, a folder renders, and neither replaces the other.
`QB2@display` owns what the Intake inside `source/` carries, `QB4@display` owns how `candidates/` is promoted, QBe2b owns who asked for the render, QBe2c owns the caption and label inside `float.tex`, and QBe3c owns where the float lands.

**Why the earlier ruling was incomplete**: "move the whole folder" treated a unit as one kind of thing.
It is not. One unit holds machinery and deliverable bytes in the same place, and a rule that moves both either ships the workspace or strands the float.

**What the split actually buys**: the delete test becomes answerable member by member.
The numbered tree is excluded from the journal cut, and the unnumbered tree must compile by itself, so every file in a unit has exactly one correct home.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Say "one identity, two roles", never "two folders"**: two folders is what it looks like on disk, and it invites the reading that there are two units.
The id is the thing that makes them one, so the sentence has to lead with it.

**Apply the delete test member by member, never in the aggregate**: "working state stays numbered" is unfalsifiable.
Naming `README.md`, `source/`, `candidates/`, `versions/`, `preview.*` on one side and `float.tex` plus selected `assets/` on the other is checkable.

**Never let a rebuild sound like a promotion**: a renderer may rebuild candidates inside the workspace freely, and only an explicit Display promotion may replace submission bytes.

## Diagram

**One id, two trees**: what stays numbered, and what the journal receives.

```text
  📁 0-lifecycle/3-display/                        🔢 NUMBERED · authority
  ├── S-Display-1b-research-design.md                 AUTHORITY + GATE
  └── workspace/S-Display-1b-research-design/
      ├── README.md · source/                         rebuild contract
      ├── candidates/ · versions/                     selection history
      └── preview.tex · preview.pdf                   isolated review
                        │
                        │  🚨 explicit Display promotion only
                        ▼
  📤 displays/S-Display-1b-research-design/         🔓 UNNUMBERED · shipped
  ├── float.tex                                       caption + label + include
  └── assets/                                         the SELECTED render only

  🔑 ONE stable S id binds the two ── they are one unit, not two
  🧪 delete test: the numbered tree is cut from the journal;
     the unnumbered tree must compile ALONE
```

## Content

### 1 · One identity, two projections

**The anatomy, from the units that exist**: eight members, each with one correct home.

```text
  🔢 NUMBERED, working state          🔓 UNNUMBERED, deliverable
  ──────────────────────────          ──────────────────────────
  S-Display-N-<slug>.md               float.tex     ← what \input reaches
  README.md                           assets/       ← only the selected
  source/                                             file(s) the float
  candidates/                                          reaches
  versions/
  preview.tex · preview.pdf

  ⚖️ both prior rulings preserved:
     work lives with the Board · the submission projection is
     unnumbered and self-contained
```

📐 Establishes the unit's anatomy and the projection boundary that runs through it.

#### 1.1 · The delete test is what makes the boundary checkable
(a rule stated over the whole unit cannot be tested; a rule stated per member can)
`float.tex` is deliverable because it is what `\input` reaches, and `assets/` is deliverable only for the files that float reaches.
Everything else is numbered working state, and the test for any new member is simply whether the unnumbered tree still compiles without it.

#### 1.2 · What the split does not change
(the id and the label are exactly the things that must survive it)
The unit id, the label, and every manuscript `\ref{}` stay stable across the split.
A renderer may rebuild candidates inside the workspace as often as it likes, and only an explicit Display promotion may replace the selected submission bytes.

## Aims

### A1 · 📐 One identity, two projections
- A1.1 · The anatomy is fixed from the units that exist rather than invented.
  **Done when:** all eight members are named with one home each: page, README, source, candidates, versions, preview, float, and selected assets.
- A1.2 · The split is ruled and applied on a real paper.
  **Done when:** page and workspace sit under `0-lifecycle/3-display/`, and `float.tex` plus selected `assets/` sit under unnumbered `displays/<unit>/`.
- A1.3 · QA6 agrees with the split.
  **Done when:** QA6 names `displays/` as the submission projection rather than the home of working state.
- A1.4 · Retired flat buckets stay archived.
  **Done when:** no `_old/` or `_old2/` bucket is an active owner of any unit.

### P · 🏁 Page-level
- P1 · Every projected unit is complete enough to compile.
  **Done when:** no active unit is missing its `float.tex`, and Paper projection G4 stops blocking on an absent display input.

## States

### A1 · 📐 One identity, two projections
- ✅ A1.1 · Done. Eight members, each with one home, measured from the units on the MISQ paper.
- ✅ A1.2 · Done 260730. The split is implemented on the MISQ paper.
- ✅ A1.3 · Done. QA6 now names `displays/` as the submission projection.
- 🔨 A1.4 · Active. The retired flat buckets are archived, and the standing risk is that `_old/` or `_old2/` quietly becomes an active owner again.

### P · 🏁 Page-level
- 🔨 P1 · Active, one live defect. `displays/S-Display-4a-main-regression/float.tex` is absent, which is precisely why Paper projection G4 correctly blocks.

## Files

- `displays/` · journal-facing unit projections, each active unit holding only `float.tex` and selected `assets/`
- `0-lifecycle/3-display/` · `S-Display-*` authority pages plus `workspace/` rebuild state
- `0-lifecycle/3-display/build-displays.py` · projects selected display bytes into the unnumbered submission tree
- `QB-delivery/QB9-build.md` · the concern whose G4 blocks on the one incomplete projection

## Law

- One Display unit has one identity and two filesystem roles.
  Board authority and rebuild state stay numbered; only the selected `float.tex` and assets enter the unnumbered journal projection.

## Glossary

- **Projection**: the small unnumbered copy of a unit that the journal receives, which must compile without anything numbered.
- **Workspace**: the numbered rebuild state of a unit, which a renderer may rewrite freely and which is never shipped.

## Log

260803 · Left `QB · Delivery` for the new `QBe · Delivery Element` group, and `QB13a` became `QBe2a`, then took its place in the unit-size order ruled the same day (JL 260803: sentence, display, section); the old id resolves as a declared alias in `board.md ## Links`.
260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered with a face figure and caption, Aims regrouped as A1/P with `Done when`, States mirrored per Aim, and a Glossary written for the first time.
260802 · Became QB13a under the float series, which is where the unit as an object belongs.
260730 · Reconciled the 260727 whole-folder move with QA6's submission cut: split authority/workspace from the journal-facing projection and recorded the one incomplete projected unit.
