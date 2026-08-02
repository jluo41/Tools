# Delivery Display: the seam between what Paper owns and what the Display layer makes

state: 🟡 PARTIAL · the seam is ruled; whether this board already crosses it is unaudited
owner: JL
method: let Paper own the visual argument, caption, placement, and gate while the Display layer owns rendering

## Opening

What does Paper own when a task or discovery result becomes a figure or table?

Four things, and only four: why the display exists, what it argues, where it lands, and whether it is accepted. Making it is somebody else's job. The Display layer at `/haipipe-display` owns the recipe, the renderer, the candidates, and promotion.

**Where this page sits**: QB4 Value hands over numbers that are better shown than stated.
This page is the seam itself, and the three series below it hold the detail: QB12 the sentence that points at a display, QB13 the float as an object, QB11 where the float lands in a section.

**Why the seam needs its own page**: without it the paper board slowly reimplements the display layer.
Every question about a figure looks like a paper question from inside a paper, so rendering rules drift onto this board one reasonable page at a time, and then two boards specify the same thing differently.

**What the seam actually decides**: not who does the work, but who is allowed to change their mind.
Paper may reject a render it does not like, and the Display layer may not decide a figure was not worth making.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**This page holds the seam and nothing else**: the six detail pages left for QB11, QB12, and QB13 on 260802, and they must not drift back.
A sentence about what a unit folder contains, or how a caption is worded, belongs on a face and not here.

**State ownership as a pair, always**: write what Paper owns AND what the Display layer owns in the same breath.
Half the pair alone reads as a land grab by whichever side is named.

## Diagram

**The seam**: four things on the paper side, everything about making on the other.

```text
        📄 PAPER OWNS                  ⚙️ DISPLAY LAYER OWNS
        ─────────────                  ─────────────────────
        why it exists                  recipe
        what it argues                 renderer
        where it lands                 candidates
        whether it is accepted         render promotion
             │                                │
             └────────── 🤝 the seam ─────────┘
                              │
      ┌───────────────────────┼───────────────────────┐
      ▼                       ▼                       ▼
  📊 QB12                 🖼 QB13                 📐 QB11
  the sentence that       the float as            where the float
  POINTS at it            an object               lands in a section

  ⚠️ drift risk: a paper board slowly reimplements the display layer,
     one reasonable-looking page at a time
```

## Content

### 1 · The delivery contract

**What Display owes**: an accepted visual argument, and a boundary that holds.

```text
  📥 CONSUMES                📤 PROJECTS TO           🚪 GATE
  display-ready         ━━▶  displays/<unit>/   ━━▶  a human accepts what
  task or discovery          float.tex               the display ARGUES
  output                     assets · labels         and the EXACT
  manuscript claims          section references      promoted render
```

📜 Establishes the ownership seam, and the one gate that is unambiguously Paper's.

| Field | Contract |
|---|---|
| Lifecycle | After Literature and Value have made the evidence inspectable. |
| Authority | `S-Display-*` for meaning and gate; the display unit for the promoted render. |
| Projects to | `displays/<unit>/float.tex`, assets, labels, and section references. |
| Skills | Paper Display stage plus the shared Display skill family. |
| Consumes | Display-ready task/discovery outputs and manuscript claims. |
| Gate | The human accepts what the display argues and the exact promoted render. |
| Open gaps | The shipping/working split inside a display unit remains open on QA6. |

#### 1.1 · Acceptance is two decisions, not one
(a reader can approve the argument and still reject the picture that makes it)
The gate names the argument and the exact promoted render separately, because they fail separately.
A figure can say the right thing from the wrong data, and it can say the right thing badly, and only one of those is fixed by re-rendering.

## Aims

### A1 · 📜 The delivery contract
- A1.1 · The paper board specifies the seam and never the rendering.
  **Done when:** no page in the QB group states a recipe, a renderer, or a promotion rule, and the display board is the only place those appear.
- A1.2 · The six detail pages sit under the series that owns their unit.
  **Done when:** QB12 holds the two pointer pages, QB13 holds the three float pages, QB11 holds placement, and this page lists no detail page of its own.

### P · 🏁 Page-level
- P1 · The shipping and working halves of a display unit are separated.
  **Done when:** QA6 rules the split, and QB13a states which files are numbered board authority and which enter the unnumbered submission half.

## States

### A1 · 📜 The delivery contract
- 🔨 A1.1 · Ruled and unaudited. The seam is stated in the Law, but QB13 records that QB13a and QB13b may be restating the display board, and only their titles have been compared.
- ✅ A1.2 · Done 260802. The six pages were re-filed by unit, and this page keeps the seam alone.

### P · 🏁 Page-level
- 🧠 P1 · Waiting on QA6, which owns the shipping and working split. QB13a already carries the two-filesystem-roles ruling, so this thaws as soon as QA6 decides.

## Files

The six detail pages left this concern for the series that owns their unit, and Display keeps the ownership seam only.

- the pointer to a display: `QB12c-sentence-display-table.md`, `QB12d-sentence-display-figure.md`, under QB12
- the float itself: `QB13a-display-folder.md`, `QB13b-requested-display.md`, `QB13c-display-caption.md`, under QB13
- where the float lands: `QB11c-display-placement.md`, under QB11, because the first citing section decides it

## Law

Paper owns why a Display exists, what it says, where it lands, and whether it is accepted. The Display layer makes it.

## Glossary

- **Display unit**: one figure or table's argument, render, caption, label, and working record.
- **Seam**: the line between the two owners, which decides who may change their mind about what.

## Log

260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered with a face figure and caption, Aims regrouped as A1/P with `Done when`, States mirrored per Aim.
260802 · The six detail pages re-filed by unit onto QB11, QB12, and QB13; Display keeps the Paper/Display ownership seam and nothing else.
260729 · Display kept as one Delivery group after Literature and Value.
