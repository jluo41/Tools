# Outline: agree the shape of a page before a word of it is written
state: 🟡 IN PROGRESS · the phase ships; its gate has never been ticked by a person · open: 5
owner: CC
method: state what the phase may decide, what it may not touch, and the single tick that ends it; every rule here names the failure that bought it
session: ec8c7879-3e0f-484e-a3fe-b41b1bfb50fc

## Opening
What may a page promise, and who agrees to that before anyone pays for the prose?

OUTLINE is phase ① of the loop and the cheapest gate on the board: its whole output fits on one screen and a person can reject it in ten seconds.
It agrees the SHAPE, which sections, which paragraphs, which bullets, and what each bullet still owes, and it writes no prose, lands no card, and dispatches no question.
It became a phase on 260817 because one phase owning both "agree the shape" and "write the page" let a single done-report cover both, and the plan ended up pasted into a page's own `## Content` where it went stale at the next edit.
`QPw00` owns the loop this phase opens; `haipipe-plugin-outline` owns the file and its 🧭 tab; this page owns only the phase.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A phase is named by its authority, never by its edit shape**: adding a section to the PLAN is OUTLINE and adding a section to the PAGE is DRAFT, and the two are different files.
Any sentence here that distinguishes the phase by what it typed rather than by what it was allowed to decide is wrong.

**Every rule names the failure that bought it**: this phase exists because of `QC1-visitlbp`, so a rule with no incident behind it is a guess and reads like one.
Say the page, the date, and what shipped broken.

**The plugin's file is the authority on the file**: when this page and `haipipe-plugin-outline` disagree about addressing, marks, or versions, the plugin wins and this page is wrong.
So describe the phase here and never restate the file's shape, because a copy drifts.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
The phase in one view: what it decides, what it must not touch, and the one thing that lets it exit.

```text
🧭 OUTLINE · phase ① of 7
┌────────────────────────────────────────────────────────────────────┐
│ OWNS   the SHAPE                                                   │
│        which sections · which paragraphs · which bullets            │
│        and what each bullet still OWES                              │
│ MAY DO add · delete · move · rewrite, freely, while unapproved       │
│ 🚫 MAY write prose · land a card · dispatch a question ·             │
│    NOT   invent a division the Page Type does not allow             │
└────────────────────────────────────────────────────────────────────┘
                              │
              <page>/outline/<stem>-outline-v<N>.md
                       approved: ⬜  ──▶  ✅
                       🚧 a person, never a machine
                              │
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
   ✅ approved                                  ⬜ not yet
   ──▶ ② DRAFT                                  stay in OUTLINE,
       purpose · Aims · the promise              or HOLD if the
                                                 person is away

   ⛔ never straight to EVIDENCE or REVISE: a shape nobody
      approved is not something to gather evidence for
```
📌 The six bullet marks are `🎯 aim · ✅ have · 📚 cite · 🔢 value · 🖼 display · 🧮 proof`, and their meanings belong to `haipipe-plugin-outline`, not here.

## Content

### 1 · OUTLINE owns the shape and nothing that fills it
**The authority test**: the phase decides what the page will be made of, and is forbidden every act that would start making it.

```text
decision                                          OUTLINE?
─────────────────────────────────────────────────────────────
"this page needs a fourth division"                 ✅ yes
"this bullet owes a number we do not have"          ✅ yes
"this bullet's number is 0.42"                      🚫 no · EVIDENCE
"here is the sentence that division opens with"     🚫 no · DRAFT/REVISE
"raise PP04 and ask the bank"                       🚫 no · PROBE
```
📌 The test is authority, not effort: a one-word bullet edit is OUTLINE and a one-word prose edit is not.

#### 1.1 · An operation does not identify the phase
(the same verb belongs to two phases, and only the target file tells them apart)
Adding a section to the plan is OUTLINE; adding a section to the page is DRAFT.
Every phase in this loop may add, delete, move, and rewrite, so a diff can never name the phase that produced it.
`QPw00 §6` carries that rule for the whole loop and this division is its instance.

#### 1.2 · The Page Type constrains the shape before OUTLINE proposes one
(a plan that invents a division its Page Type forbids is the defect, not the type)
Every Page Type declares how its outline arrives, in an `outline:` block in its own frontmatter.
The three modes are `fixed`, where the type lists the divisions outright and the plan fills them, `grammar`, where the type fixes a closed first-word set and the plan chooses how many of each, and `resolved`, where the outline lives outside the type and must be resolved before a variant is chosen.
When a Page Type genuinely does not fit the subject, the mismatch is recorded as a finding against that type and the plan is fixed, never the type quietly reshaped.

### 2 · The gate is cheap on purpose, and that is the whole argument
**The cost asymmetry**: the same change costs one line before the prose exists and costs the prose afterwards.

```text
                                    BEFORE prose      AFTER prose
change a section list                 one line          the prose
reorder two divisions                 one line          every cross-reference
drop a bullet nobody wanted            one line          the paragraph + its
                                                        cards + its display

⏱ a plan a person can reject in TEN SECONDS belongs in front of every
   expensive phase, rather than folded into one
```
📌 This is why the phase is worth a gate at all: the gate is nearly free and the thing it protects is not.

#### 2.1 · The incident that made it a phase
(`QC1-visitlbp` on CMSRegBoard, 260817)
DRAFT owned both "agree the shape" and "write the page", so one done-report covered both acts.
The outline table was pasted into the page's own `## Content`, where it immediately went stale at the next edit, and nobody was told because the report had already said done.
The split gives each act its own report, and the plan its own file that cannot be mistaken for content.

### 3 · One file, one tick, and no machine may write it
**The deliverable**: a versioned plan on disk, and a human tick that is the only exit.

```text
<page>/outline/<stem>-outline-v<N>.md          AUTHORED · versioned
                                              read on the 🧭 tab
        approved: ⬜  ──────▶  approved: ✅
                                🚧 a PERSON, never a machine

why no machine: what the tick judges is whether this is the RIGHT plan,
and no mechanical check reaches that question. it is the same reason no
machine writes `accepted: ✅` on a display render.
```
📌 The file's `C<n>.P<n>.B<n>` addressing, its six marks, and its version rules are stated once in `haipipe-plugin-outline` and never restated here.

#### 3.1 · The tick is one of the board's four human ticks
(`approved:` here, `verified` per bibex entry, `accepted: ✅` per display unit, and the Page Type's ruling at CHECK)
All four share one property: a machine may compute everything around them and may not write them.
`QPw00g` is the open question of putting all four on one surface, because today they sit in three phases and N separate files.

### 4 · Before the tick it is a working document, after it is frozen
**The two regimes**: an unapproved plan needs no record at all, and an approved one is never corrected in place.

```text
✍️ UNAPPROVED    discuss it · rewrite it · DELETE a wrong bullet
                 no version, no record, nobody agreed to it yet
🔒 APPROVED      frozen · correct as of that date
✍️ v2            `supersedes: v1` · and v1 is KEPT, not corrected
```
📌 `v2` does not mean `v1` was wrong (JL 260817): it means `v1` was right then and the work has since moved, which is exactly why the old version survives.

#### 4.1 · Why a superseded plan is kept rather than fixed
(the same reason a sentence is archived rather than deleted)
A kept `v1` says what was agreed at the time, so the record stays evidence of a decision instead of a description of the present.
Correcting `v1` in place would leave the board unable to say what anybody actually approved.

### 5 · A hole is the phase working, not the phase failing
**The mark rule**: naming what is owed is the deliverable; supplying it is another phase's job.

```text
✅  - B2 · the five coefficients at each rung        🔢 PP02
    names what is owed. PROBE dispatches it, EVIDENCE lands it.

🚫  - B2 · the five coefficients are stable
    asserts an answer nobody has. that is not a plan, it is a guess.

⛔ OUTLINE marks the hole and STOPS.
   it does not raise the card, ask the bank, or write the sentence.
```
📌 A plan that already knows every answer was written after the fact, which is the tell this rule exists to catch.

#### 5.1 · The mark is the proposal, so nothing lands on disk here
(ruled 260817, and it is why the card waits for phase ③)
A card raised at ① would be a second copy of the mark, and a card raised at ② could not carry its own stake, because the stake is an Aim and Aims are written at DRAFT.
So the mark stays a line in the plan until PROBE turns it into `probe/PP<NN>-<slug>/`.
`QPw00 §🃏` carries the one-hole-five-phases rule that this division opens.

#### 5.2 · One mark is not one card
(many bullets may share a single card, and that is reuse rather than duplication)
`PP04` on `QC1-visitlbp` serves three bullets, and its `serves:` line names all three.
A question is asked once, and the card id exists precisely to prevent the duplicate.

## Aims

### A1 · 🧭 OUTLINE owns the shape and nothing that fills it
- A1.1 · The authority test is written so a reader can classify any edit without reading the diff.
  Done when five decisions are classified in the division and each names the phase that owns it.
- A1.2 · The Page Type's `outline:` block is honoured by every plan on this board.
  Done when a checker rejects a plan naming a division its Page Type does not declare.

### A2 · 💸 The gate is cheap on purpose, and that is the whole argument
- A2.1 · The cost asymmetry is stated as a comparison a reader can check, not as an assertion.
  Done when the before-and-after costs are shown side by side for three kinds of change.

### A3 · 🚧 One file, one tick, and no machine may write it
- A3.1 · The tick has been exercised by a person on a real page at least once.
  Done when one `<page>/outline/<stem>-outline-v<N>.md` on any board carries `approved: ✅` with a name and a date.

### A4 · 🔒 Before the tick it is a working document, after it is frozen
- A4.1 · A superseded plan is kept rather than corrected, on every board.
  Done when a `v2` exists somewhere with `supersedes: v1` and `v1` still on disk.

### A5 · 🕳 A hole is the phase working, not the phase failing
- A5.1 · No approved plan on this board asserts a value it does not have.
  Done when every 🔢 bullet in every approved plan names a mark rather than a number.

## States
### Decision Now
- [ ] 🗣 Rule whether an UNAPPROVED plan may be deleted with no record at all
      📍 `Part` §4, the two regimes
      🔔 `Why now` the contract says an unapproved plan needs no record, and the board's own habit is that nothing is deleted, only archived, so two rules that both hold today disagree here
      ⭐ `A ·` keep the contract: before the tick nobody agreed to anything, so there is nothing to preserve and the cheap gate stays cheap
      `B ·` archive every version including unapproved ones, which makes the plan auditable but puts a record cost on the phase whose whole argument is that it is nearly free
      🛑 `Blocks` A4.1, and the plugin's version rules
      🤖 `If nobody answers` A takes effect, because it is what the shipped contract says today

### A1 · 🧭 OUTLINE owns the shape and nothing that fills it
- ✅ A1.1 · Met. Five decisions are classified in `§1` and each names its owning phase.
- ⬜ A1.2 · Not started. No checker reads a Page Type's `outline:` block against a plan yet.

### A2 · 💸 The gate is cheap on purpose, and that is the whole argument
- ✅ A2.1 · Met. Three kinds of change are costed before and after the prose in `§2`.

### A3 · 🚧 One file, one tick, and no machine may write it
- ⬜ A3.1 · Not started. The phase ships at `haipipe-page-outline` 0.1.1 and no page on any board carries an `approved: ✅` outline file.

### A4 · 🔒 Before the tick it is a working document, after it is frozen
- 🧠 A4.1 · Waiting on the Decision Now row above, which decides what happens to an unapproved version.

### A5 · 🕳 A hole is the phase working, not the phase failing
- ⬜ A5.1 · Not measurable yet, because no approved plan exists to measure.

## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `page-workflows/haipipe-page-outline/SKILL.md`
  The phase contract itself, at 0.1.1, and the authority on its procedure.
- `page-plugins/haipipe-plugin-outline/SKILL.md`
  The file's own shape: `C<n>.P<n>.B<n>` addressing, the six marks, and the version rules. It wins over this page on all three.
### 📥 Input files · what the work READS
- `<page>/outline/<stem>-outline-v<N>.md`
  The plan this phase produces, and the only file it writes.
### 📤 Output files · what a BUILD writes
- `board/QPw/QPw1-outline.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QPw00 §6](5-QPw-page-workflow/QPw00-page-loop/QPw00-page-loop.md)
  Read the rule that an operation never names a phase before classifying any edit as OUTLINE.
- `continues · DRAFT` · [QPw2 §1](5-QPw-page-workflow/QPw2-draft/QPw2-draft.md)
  The phase this one exits into, and the phase that writes the Aim a mark's stake will need.
- `reads · ALL` · [QPf12 §1](4-QPf-page-folder/QPf12-outline/QPf12-outline.md)
  The outline plugin's own page: the file, the 🧭 tab, and the addressing this page must not restate.

## Law
- 260817 JL · 🚧 **OUTLINE is a phase, not a step inside DRAFT**: agreeing the shape and writing the page get separate reports
  One phase owning both let a single done-report cover both acts, and `QC1-visitlbp` pasted its outline table into `## Content` where it went stale unannounced.
  The option rejected was keeping it inside DRAFT with a stricter report, which loses because the two acts have different gates and only one of them is nearly free to redo.
- 260817 JL · 🔒 **`v2` does not mean `v1` was wrong**: a superseded plan is kept, never corrected
  `v1` was right on its date and the work has since moved, so correcting it in place would destroy the record of what anyone approved.
- 🚧 **No machine writes `approved:`**: the tick judges whether this is the right plan, and no check reaches that question
  It is the same law that keeps `accepted: ✅` out of a machine's hands on a display unit.
- 🕳 **OUTLINE marks the hole and stops**: it never raises the card, asks the bank, or writes the sentence
  A plan that already knows every answer was written after the fact.

## Glossary
- 🧭 **outline**: the versioned plan of a page's shape, at `<page>/outline/<stem>-outline-v<N>.md`, read on the 🧭 tab.
- 📌 **mark**: the symbol on a plan bullet saying what that bullet still owes, one of 🎯 aim, ✅ have, 📚 cite, 🔢 value, 🖼 display, 🧮 proof.
- 🎯 **Point**: one content unit of the plan, addressed `C<n>.P<n>.B<n>`, and the stable join key every later phase writes back to.
- 🚧 **the gate**: the `approved:` line on the outline file, the only exit this phase has.

## Log
- 260818 · [DRAFT-CC] page created on JL's ruling that each workflow step gets its own page, one of `QPw1` to `QPw6`. Written from `haipipe-page-outline` 0.1.0, which shipped 260817 when JL ruled OUTLINE out of DRAFT. Five divisions: the authority test, the cost asymmetry that argues the gate, the file and its single human tick, the unapproved-versus-frozen regimes, and the hole rule. The `v2 does not mean v1 was wrong` ruling and the no-machine-writes-the-tick law were carried in as `## Law` rows rather than restated in prose. One thing the contract leaves open became the Decision Now row: it says an unapproved plan needs no record, while this board's own habit is that nothing is deleted, only archived.
