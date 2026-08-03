# Delivery-Display: Folder, Render, Caption

state: 🟡 PARTIAL · the three faces are absorbed into one page; the display-board overlap audit is open and may cut this page to its caption half
owner: JL
method: hold the float as its own unit, keep only the half the paper owns, and never restate the Display layer

## Opening

What does the paper own about a float, between the renderer finishing and a sentence pointing at it?

A float is one figure or table as a delivered object: its identity, its files, its caption, and its label. A caption is an argument written in the author's voice. A label is the anchor every citing sentence depends on. Neither is produced by a renderer.

**Where this page sits**: `QB5` Display holds the ownership seam against `/haipipe-display`, and this page holds the object itself.
`QBe3 §5` holds where the float lands, because that is decided by the first citing section.

**Why neither neighbour can hold it**: a float is not a section, since it has no outline and no paragraph order.
It is not a sentence either: `QBe1`'s `### 6` and `### 7` specify the POINTER, and a pointer says nothing about what it points at.
Between the two sits an object with its own identity, its own two filesystem roles, and its own authored text, which is why it is numbered second in this group.

**Why one page and not four**: on 260803 the three faces became `### 3` to `### 5`, so a reader meets a unit's folder, its renderer boundary and its authored text in one pass.
The three were written weeks apart under the Display concern and each carried its own version of the ownership line.

**The risk this page carries openly**: the display board may already own two of these three divisions.
Only the titles have been compared, so this is a risk and not a finding, and the audit is `A2.1` below.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `../01-boardform-260722/QB-delivery/QB4-overall.md` and are not restated here.

**Demonstrate before explaining**: `### 1` is a test sheet, and `_fixture/displays/` holds two real units to run it on.
A rule added here has to survive being checked against those units, not only described.

**Name the parts, not the retired faces**: the folder, the render request, and the caption and label are this page's `### 3` to `### 5`.
`### 3`` to `### 5``, and the older `QB13a` to `QB13c` and `QB5c`/`QB5d`/`QB5e`, still resolve through `board.md`'s alias map; nothing new is written with them.

**Specify owning, never making**: `QB5`'s Law splits them, and this is the easiest page on the board to cross that line.
A division here that says how a renderer works is a division in the wrong board, whatever it is titled.

**Keep the caption and the label apart**: they arrive together and fail differently.
A weak caption is a writing problem; a changed label silently breaks every sentence that cited it.

**State an unverified overlap as unverified**: while the audit is open, any claim that a division here is this board's authority must say that only titles have been compared.

## Diagram

**The float between its neighbours**: what this series owns, and what the two beside it own.

```text
        ⚙️ Display layer MAKES it
                 │
                 ▼
   ┌───────────────────────────────┐
   │  🖼 THE FLOAT AS AN OBJECT     │
   │                               │
   │  🗂 identity + two file roles │ ← `### 3`
   │  🎨 who may render it         │ ← `### 4`
   │  ✍️ caption  · an argument    │ ← `### 5`
   │  🔖 label    · a promise      │ ← `### 5`
   └───────────────┬───────────────┘
                   │ the LABEL is what a sentence may point at
        ┌──────────┴──────────┐
        ▼                     ▼
   📊 QBe1 §6 / QBe1 §7      📐 QBe3 §5
   the pointer            where it lands

   ⚠️ UNVERIFIED: the display board may already own `### 3` and `### 4`
      (titles compared, bodies not)
```

## Content

### 1 · Try it yourself: two real units, and the failure they are both in

**Before you click**: press `expand all` on `## Content`, because a chip inside a folded division is not painted, so a click on it lands on the page behind it and nothing opens. That is the first thing to check when a chip looks dead (measured 260803).

**The test sheet**: what to open, what to look for, and what the build already says is wrong.

```text
📂 OPEN THESE · both are real units, in this board's own fixture
   _fixture/displays/display05-descriptives/        a TABLE unit
   _fixture/displays/display02-discretion-gradient/ a FIGURE unit
   each carries  float.tex · assets/ · candidates/ · preview.pdf · README.md

👀 LOOK FOR THE TWO ROLES, WHICH IS §4's WHOLE SUBJECT
   which files are numbered working machinery the board reads
   which files enter the unnumbered half a journal receives
   preview.pdf is float.tex COMPILED STANDALONE, so it carries the caption
     and the numbering the paper's own class sets

🚫 THIS MUST REFUSE YOU
   a division here explaining how the picture was drawn: that belongs to the
   Display layer, and QB5's Law is the test
📥 OR DOWNLOAD THE UNIT ITSELF · this is the whole of what a display is
   display05  preview.pdf   147 KB  float.tex COMPILED · the table as the paper sets it
              float.tex     3.6 KB  the wrapper: caption, label, \input of the body
              assets/table-body.tex  4.0 KB  the rows, which the task layer computed
   display02  preview.pdf    65 KB  the figure as the paper sets it
              assets/figure.png     84 KB  the promoted picture
              candidates/C-enriched.png  157 KB  a candidate nobody promoted
```

🧪 Establishes the object as something to open rather than read about, and starts from the failure the two fixture units are already in.

#### 1.1 · 📊 The table unit, as a sentence points at it
(click the chip; the panel arrives from `float.tex`, `assets/` and `preview.pdf`, which is all one unit is)
Cohort descriptives are reported in Table~\ref{tab:descriptives}.

#### 1.2 · 🖼 The figure unit, as a sentence points at it
(same grammar, different kind, and the kind comes from the unit's own `float.tex` rather than from a guess)
The discretion gradient across cohorts is plotted in Figure~\ref{fig:discretion-gradient}.

#### 1.3 · ⚠️ Both are cited by no section, and the build says so
(a float that exists, is built, and that no sentence points at is the normal state of a display)
Every build of this board prints `uncited` for `fig:discretion-gradient` and for `tab:descriptives`.
The two chips above are this page pointing at them, which is not the manuscript pointing at them.
That gap is what makes `### 6`'s label a promise nobody has called in yet.

#### 1.4 · The units are the fixture, not a mock-up
(they are real folders with real files, which is why the uncited warning is real too)
`board.md` declares `paper-root: _fixture`, so every display rule on this page is checked against those two units when the board builds.
A rule that cannot be checked against them is a rule this page cannot claim to have tested.

### 2 · Why the float is its own unit

**Neither neighbour fits**: what each of the two adjacent series would have to pretend.

```text
   ❌ as a SECTION          ❌ as a SENTENCE         ✅ as its OWN unit
   ──────────────           ───────────────          ─────────────────
   no outline               the pointer is not       one identity
   no paragraph order       the thing pointed at     two file roles
                                                     authored caption
                                                     a label others depend on

  📂 AND IT HAS TWO SOURCES, NOT ONE (JL 260803)
     🗂 displays/<unit>/       DISK · float.tex, assets, candidates, preview
     📄 S05-display/S-Display-*  THE PAPER · what it argues, and whether the
                                 author accepts it
     disk answers whether it is BUILT · the S05 page answers whether it may
     be LEANED ON, and only one of those two ever reaches a chip's colour
```

🖼 Establishes why this series exists between QBe1 and QBe3 rather than inside either.

#### 2.1 · The unit has two sources of truth, and they disagree
(JL 260803, after the MISQ paper regrouped its lifecycle into `S01-opening` to `S10-round`)
A float is the one element in this group whose evidence sits in two places at once.
`displays/<unit>/` on disk says whether it is built; `S05-display/S-Display-*` says whether the paper may lean on it.
A chip goes green off DISK, so a unit whose own S05 page says blocked can still render as ready, which is `A4.1` on this page.
`QBe1` has no such split: a citation has one source and a value has one run.

#### 2.2 · One unit, one identity, two filesystem roles
(the ruling `### 3` already carries, and the reason the object needs a page at all)
Board authority and rebuild state stay numbered working machinery.
Only the selected `float.tex` and its assets enter the unnumbered submission half, so one object lives in two places on purpose.

#### 2.2 · The caption and the label fail differently
(they are authored in the same moment and are not the same kind of thing)
A caption is an argument in the author's voice, and a weak one costs a reader some effort.
A label is a promise, and changing one silently breaks every sentence that cited it, which is why `### 5` cannot treat them as one topic.

### 3 · The overlap this series has not audited

**Title against title**: what the display board already runs, beside what this series claims.

```text
   📋 display board 01-haipipe-display-260727    📋 this series
   ──────────────────────────────────────────    ──────────────────────
   QB1 unit-contract                    ≟        `### 3` display-folder
   QB3 recipe-and-render                ≟        `### 4` requested-display
   QB4 candidates-and-promotion         ≟        `### 4` requested-display
   QB5 wrapper-and-placement            ≟        QBe3 §5 display-placement

   ⚠️ only the TITLES were compared ── this is a RISK, not a finding
   🚫 until the audit runs, do not cite `### 3` or `### 4` as this board's authority
```

⚠️ Establishes the open duplication risk, so that a reader is never misled about which board rules a float.

#### 3.1 · The audit's outcome decides whether this series keeps three faces
(if the display board already owns making, what is left here is the authored text alone)
QB5's Law says Paper owns why a display exists, what it argues, where it lands, and whether it is accepted.
Anything in `### 3` or `### 4` that specifies how a render is produced fails that test and belongs on the display board, leaving `### 5` as the clear survivor.

### 4 · The unit folder: one identity in two filesystem roles

**What one unit folder holds**: the working half the board reads, and the shipping half a journal receives.

A unit is one figure or table with a single stable id. A projection is the small journal-facing copy of it. The workspace is everything used to rebuild it and never shipped. One object, two filesystem roles, and the id is what keeps them the same object.

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

🗂 Establishes what one display unit is made of, and which half of it a journal ever sees. Absorbed from `QBe2a` on 260803; its full design history stays in `_archive/QBe2a-display-folder.md`.

#### 1 · One identity, two projections

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

##### 1.1 · The delete test is what makes the boundary checkable
(a rule stated over the whole unit cannot be tested; a rule stated per member can)
`float.tex` is deliverable because it is what `\input` reaches, and `assets/` is deliverable only for the files that float reaches.
Everything else is numbered working state, and the test for any new member is simply whether the unnumbered tree still compiles without it.

##### 1.2 · What the split does not change
(the id and the label are exactly the things that must survive it)
The unit id, the label, and every manuscript `\ref{}` stay stable across the split.
A renderer may rebuild candidates inside the workspace as often as it likes, and only an explicit Display promotion may replace the selected submission bytes.

### 5 · A display someone asked for: who pulls the trigger

**Who may pull the trigger**: the boundary between asking for a render and performing one.

Commissioning means handing the work to a separately registered worker skill rather than doing it in the stage. Candidate mode means the result lands beside the live asset instead of on top of it. Together they let a render be attempted at any time without ever destroying a display a person already accepted.

**Who may pull the trigger**: the asymmetry, the cost, and the write boundary.

```text
 🧭 THE COMMISSIONING ASYMMETRY
   every other stage   does the work itself, or asks the bank and waits
   4-display           COMMISSIONS a named worker
                         -display-table | -figure | -diagram | -illustration
   the four stay INDEPENDENTLY REGISTERED skills, invoked by name,
   deliberately outside the stage's contract, because they must be
   usable with no paper at all

 💰 A RENDER IS NOT A BANK QUESTION ── this is what decides the cost
   ┌────────────────────────────────────────────────────────────┐
   │ a BANK question ━━▶ task / discovery · costs ·             │
   │                     capped by probe_depth                  │
   │ a RENDER        ━━▶ the display stage's OWN step ·         │
   │                     NOT dispatched · does not spend        │
   │                     against probe_depth: 0                 │
   └────────────────────────────────────────────────────────────┘
   PROBE runs a render on the USER'S VERB, and the user may strike any
   render at the gate before it runs: explicit and PER-INVOCATION
   rather than budgeted

 🛡 WHAT A RENDER MAY TOUCH
   candidates/  ✅ a commissioned render lands here, always
   assets/      ⛔ never       float.tex  ⛔ never       the status ⛔ never
   promotion into assets/ and demotion into versions/ is a REVISE
   decision made by the CALLER, never by the renderer
```

🎨 Establishes who may commission a render and what a result may overwrite, which is the closest this page comes to the Display layer's side of the seam. Absorbed from `QBe2b` on 260803; its full design history stays in `_archive/QBe2b-requested-display.md`.

#### 1 · The commissioning asymmetry

**One stage out of eight**: display hands its work to named workers.

```text
  🏗 other stages   do the work, or ask the bank and wait
  🎨 display        COMMISSIONS a named worker
                      -display-table | -display-figure
                      -display-diagram | -display-illustration

  🔑 the four are INDEPENDENTLY REGISTERED skills, invoked by name,
     deliberately NOT part of the display stage's contract
     ━━▶ because they must be usable with no paper at all
```

🧭 Establishes display as the only commissioning stage, and why its workers sit outside its contract.

##### 1.1 · The workers stay outside the contract on purpose
(a renderer that only works inside a paper stage is a renderer nobody else can use)
The four are registered skills invoked by name rather than steps inside `4-display`.
That keeps them callable with no paper at all, which is the whole reason the asymmetry was worth having.

#### 2 · A render is not a bank question

**What decides the cost**: the contrast that gives the rule its meaning.

```text
  🏦 a BANK question    goes to task or discovery
                        costs, and is capped by probe_depth

  🎨 a RENDER           is the display stage's OWN step
                        not dispatched to the bank
                        does not spend against probe_depth: 0

  🚪 PROBE runs a render on the USER'S VERB
     the user may strike any render at the gate BEFORE it runs
     ━━▶ authorization is explicit and PER-INVOCATION, not budgeted
```

💰 Establishes the cost rule, which is the one that had no home and was lost with a template.

##### 2.1 · Per-invocation authorization is stricter than a budget, not looser
(a budget lets an unwanted render through as long as there is room; a gate does not)
Because the user may strike any render at the gate before it runs, every render is individually authorized.
That is why not spending against `probe_depth` is safe rather than a loophole.

#### 3 · What a render may touch

**Candidate mode**: the single write boundary, and the live proof it holds.

```text
  ✅ candidates/    a commissioned render lands here, always
  ⛔ assets/        never     ⛔ float.tex   never     ⛔ status   never

  🚨 promotion into assets/ and demotion into versions/ is a REVISE
     decision made by the CALLER, never by the renderer

  🔬 live on MISQ ── S-Display-2
     candidate C accepted, sitting in candidates/
     assets/figure.pdf is still v1
     the compiled paper still shows the OLD figure
     ━━▶ the gap is VISIBLE rather than silent. That is what the rule buys.
```

🛡 Establishes the write boundary that makes commissioning safe, and the case that demonstrates it.

##### 3.1 · Migration is not promotion
(a provenance repair looks like a render decision and must not be allowed to act as one)
Moving an old unit from `source/` to `intake/` and `recipe/` may organize a verified source and record a rebuild path.
It may not replace `assets/`, retarget `float.tex`, or recategorize a candidate as current, because those remain explicit REVISE decisions owned by the caller.

### 6 · The caption and the label: an argument, and a promise

**The two things authored together**: a caption that argues, and a label that promises.

Two things, and neither is the renderer's. A caption is prose in the paper's voice, doing work the picture cannot. A label is the anchor every `\ref{}` depends on. They arrive together and they are not the same kind of thing at all.

**Two fields, two jobs**: and what each one breaks when it is wrong.

```text
  ✍️ THE CAPTION                      🔖 THE LABEL
  ─────────────                       ────────────
  prose, in the paper's voice         a stable promise
  names what the reader should        every \ref{} in every section
  take away                           depends on it
                                      survives a re-render, a promotion,
  🚫 restating the axis labels          a change of renderer, a change
     spends a float and says            of file path
     nothing
  👁 it is the only part of a         🚫 two units may NEVER declare
     display most readers read           the same label

  💥 a weak caption   ━━▶ costs a reader effort
  💥 a changed label  ━━▶ BREAKS every citing sentence, silently
```

✍️ Establishes the paper's own authored text on a display, and why the two things authored in the same moment fail differently. Absorbed from `QBe2c` on 260803; its full design history stays in `_archive/QBe2c-display-caption.md`.

#### 1 · Two fields, two different jobs

**What each owes**: the caption argues, the label promises.

```text
   the CAPTION does work the PICTURE CANNOT
        ┌──────────────────────────────────────┐
        │ ✅ what the reader should take away  │
        │ ❌ a description of what is drawn    │
        └──────────────────────────────────────┘

   the LABEL is the ONLY part other files depend on
        ┌──────────────────────────────────────┐
        │ a sentence points at the UNIT,       │
        │ never at a file  ── QBe1 §6's Law      │
        └──────────────────────────────────────┘
```

✍️ Establishes the two fields as separate topics with separate failure modes.

##### 1.1 · The caption is the most-read part of a display
(most readers read it and never study the picture, which sets how much work it has to do)
A caption that restates the axis labels has spent a float and said nothing.
It is the one place the paper gets to say what the picture is FOR, and skipping that wastes the most expensive object on the page.

#### 2 · Where they are supposed to be authored

**The ruled home, and the actual one**: twelve pages, zero blocks.

```text
  📜 QB5@display names the home:
     a  ### Wrapper  block on the matching S-Display-N page

  📊 on this paper
     12 display pages carry  ### What it shows  +  Registry id
      0 carry  ### Wrapper                              ⚠️

  ━━▶ every caption and label was authored directly into
      displays/*/float.tex ── the file the ruling says a renderer
      may only SERIALIZE into

  💥 the cost: a caption with NO decision record
     nothing says who approved this wording, or what the earlier one was
```

🏠 Establishes the gap between the ruled home for these fields and where they actually live today.

##### 2.1 · Drift here removes review, not just tidiness
(a field with no decision record cannot be reviewed, only overwritten)
Authoring into `float.tex` puts the caption in a file that a re-render may legitimately rewrite.
There is no history, no approver, and no earlier version, so a disagreement about wording has nothing to point at.

#### 3 · What a label promises, stated so it can be broken

**One live violation**: two units, one section, and a reference that resolves to nothing.

```text
  🔒 two consequences of a label being a promise
     ① renaming one is a BREAKING CHANGE across the manuscript
     ② two units may NEVER declare the same label

  ⚠️ this paper breaks ② today
     displays/Table/table1-agreeableness-distribution
        └── \label{tab:distribution}
     display09-agreeableness-distribution
        └── \label{tab:agreeableness-distribution}

     §4 \inputs the FIRST and \cites the SECOND
     ━━▶ the section cites a label that nothing it reaches declares
```

🔒 Establishes the label's promise in a form that can be violated, together with the violation currently in the paper.

##### 3.1 · The legacy folder is the live breach
(it matters because the symptom looks like a display problem and is really a duplicate-label problem)
The older `Table/` folder and `display09` describe the same table under two labels.
A reader chasing the `??` in §4 finds a missing float, when what is actually wrong is that two units claim one name.

## Aims

### A1 · 🧪 Try it yourself: two real units, and the failure they are both in
- A1.1 · Every rule on this page is checked against a unit that exists.
  **Done when:** a reader opens both fixture units, finds the two file roles in them, and sees the uncited warning the build already prints.

### A2 · Why the float is its own unit
- A2.1 · The float is filed as its own unit rather than as loose faces under the Display concern.
  **Done when:** the three float divisions sit on this page, and `QB5` lists no detail page of its own.
- A2.2 · The caption and the label are specified as two things.
  **Done when:** `### 6` states separately what a caption owes a reader and what a label owes every citing sentence.

### A3 · The overlap this series has not audited
- A3.1 · The claimed overlap with the display board is resolved by reading, not by title.
  **Done when:** each of `### 4` to `### 6` is either confirmed as paper-owned or replaced by a pointer to the display board page that owns it.

### A4 · 🗂 The unit folder: one identity in two filesystem roles
- A4.1 · The anatomy is fixed from the units that exist rather than invented.
- A4.2 · The working and shipping split is ruled and applied on a real paper.
- A4.3 · `QA6` agrees with the split.
- A4.4 · Every projected unit is complete enough to compile.
  **Done when:** each of the four is checked against `_fixture/displays/`, and `QA6` carries the same split in its own words.

### A5 · 🎨 A display someone asked for: who pulls the trigger
- A5.1 · Rendering is commissioned rather than performed inside the stage.
- A5.2 · Whether a non-display stage may commission a render is ruled.
- A5.3 · A render cannot replace the live asset.
  **Done when:** the three read as one boundary rather than three, and none of them says how a renderer works.

### A6 · ✍️ The caption and the label: an argument, and a promise
- A6.1 · What a caption must accomplish for this venue is stated as a test rather than as advice.
- A6.2 · A label is ruled a breaking change, and no two units may share one.
  **Done when:** `### 6` carries a caption test a reader can apply, and the label rule is enforced by something other than care.

### P · 🏁 Page-level
- P1 · Nothing on this page specifies how a render is made.
  **Done when:** a reader applying `QB5`'s Law to each division finds no sentence about recipes, renderers, or promotion.

## States

### A1 · 🧪 Try it yourself: two real units, and the failure they are both in
- 🔨 A1.1 · Active. Both units are real folders under `_fixture/displays/` and the uncited warning prints on every build; whether a reader can follow the sheet is what is being asked.

### A2 · Why the float is its own unit
- ✅ A2.1 · Done 260802, and completed 260803 when the three faces became divisions of this page.
- ⬜ A2.2 · Not started. `### 6` arrived from a 🔴 face and is the thinnest division here.

### A3 · The overlap this series has not audited
- ⬜ A3.1 · Not started, and it is the item that matters most here. All four display-board pages it would be measured against are ✅ SETTLED while `### 4` and `### 5` are not, which is a reason to run it soon rather than a finding.

### A4 · 🗂 The unit folder: one identity in two filesystem roles
- 🔨 A4.1 · Carried in from the archived face, where it was ruled against the units that exist.
- 🔨 A4.2 · Carried in, applied on the MISQ paper.
- 🧠 A4.3 · Waiting on `QA6`, which owns the shipping and working split.
- 🔨 A4.4 · Carried in and unverified against the fixture.

### A5 · 🎨 A display someone asked for: who pulls the trigger
- 🔨 A5.1 · Carried in.
- ⬜ A5.2 · Not started.
- 🔨 A5.3 · Carried in.

### A6 · ✍️ The caption and the label: an argument, and a promise
- ⬜ A6.1 · Not started.
- ⬜ A6.2 · Not started.

### P · 🏁 Page-level
- 🔨 P1 · Active and unverified. `### 4`'s ruling is about file roles rather than rendering, which is the right side of the line; `### 5` has not been read against `QB5`'s Law.

## Files

### 🗄 Archived · the faces this page absorbed on 260803
- `_archive/QBe2a-display-folder.md` · became `### 4`. Its measurements and history stay there rather than being rewritten.
- `_archive/QBe2b-requested-display.md` · became `### 5`.
- `_archive/QBe2c-display-caption.md` · became `### 6`.
