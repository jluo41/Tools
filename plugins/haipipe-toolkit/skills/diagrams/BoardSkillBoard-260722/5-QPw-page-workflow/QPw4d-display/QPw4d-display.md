# Display: the lane that freezes what a figure will be drawn from, and hands the drawing on
state: 🟡 IN PROGRESS · the lane ships; 4 units board-wide and every intake is UNFROZEN · open: 5
owner: CC
method: hold the five-step walk in one view, say which phase owns each step, and keep this lane to step ① only; every count comes from check.py rather than from memory
session: ec8c7879-3e0f-484e-a3fe-b41b1bfb50fc

## Opening
When a page promises a table or a figure, what does EVIDENCE actually do about it?
The 🖼 display lane does one thing: it FREEZES the snapshot the figure will be drawn from.
It writes `intake/`, writes the unit's README rows, and names the renderer that owes the drawing.
It never draws, so one unit outlives three phases.
It is also the one lane that cannot start early.

**Who owns the rest**: rendering, choosing among candidates and building the float belong to `QPw5 REVISE`, and the human `accepted: ✅` belongs to `QPw6 CHECK`.
**Why it cannot start early**: an `intake/` freezes FROM a `proof/`, and no `proof/` exists until a value answer has landed, so a plan carries only a bare 🖼 mark until then.
**Where it came from**: this face was split from `QPw4` on 260818, by JL's ruling that each evidence kind gets its own page.

## Writing Style
How this page must be written. Read it before editing, and edit to it.
- **Say which phase owns each step.** The unit outlives the phase, so a step named without its owner is the defect this page exists to prevent.
- **Every count comes from `check.py`, never from memory.** This lane's failures are all counts, so a recalled number is the failure repeating itself.
- **Language and sentences.** English only, one sentence per line, no em-dashes.

## Diagram
**The display lane**: one unit, five steps, three phases, and this lane owns step ① alone.

```text
🖼 DISPLAY · lane 3 of 3 in 🃏 EVIDENCE
┌──────────────────────────────────────────────────────────────────────┐
│ 📁 lands in   <page>/display/<stem>-Display<N>-<slug>/  plugin QPf5   │
│ ✋ hand       this lane freezes intake/ and NAMES the renderer         │
│ 🚦 exit test  intake/ frozen from a proof/ AND a renderer named        │
└──────────────────────────────────────────────────────────────────────┘

  the five-step walk, and who owns each step:
  ① INTAKE  🧑 freeze the answer into intake/     🃏 EVIDENCE  ← THIS LANE
  ② RENDER  ⚙️ the renderer writes recipe/        🖊 REVISE
  ③ PICK    🧑 choose among candidates/           🖊 REVISE
  ④ BUILD   ⚙️ assets/ · float.tex · preview.pdf  🖊 REVISE
  ⑤ ACCEPT  🧑 README `accepted: ✅`              ✅ CHECK

  the renderer is chosen by the unit's `kind:` row, one to one:
  table → haipipe-display-table        tex → haipipe-display-tex
  figure → haipipe-display-figure      illustration → haipipe-display-illustration
  diagram → haipipe-display-diagram

  three INDEPENDENT counts, and only the third is a person's:
  declared   the unit folder exists
  rendered   a winning asset AND preview.pdf both exist
  accepted   a person ticked the README
  🚫 declared > rendered does not pass

  💾 on this board today, from check.py:
     4 units carry `display-intake-unfrozen`
     QPf5-Display1 · QPf5-Display2 · QPw00-Display1 · QPw00-Display2
     ⚠️ every one RENDERED, and every one traces back to nothing
```
📌 A printed number in a figure whose `intake/` was never frozen traces back to nothing, and the render being correct does not fix that.

## Content

### 1 · This lane freezes, and never draws
**The step rule**: the unit is born here and finished elsewhere.

```text
this lane WRITES     intake/  and the README rows:
                     kind: · claim: · caption-job: · intake: ·
                     fragility: · accepted: ⬜
🚫 NEVER WRITES      recipe/  · candidates/ · assets/ · float.tex
                     those are the renderer's, called at REVISE
```
📌 Naming the renderer is part of freezing the intake: an intake with no named renderer leaves step ② with no owner, which is how a declared unit reaches LaTeX as nothing.

#### 1.1 · The caption and which rows to show are ARGUMENT, not intake
(so they belong to REVISE, not here)
The intake is the ANSWER and the caption is the claim made about it, and the phase boundary sits exactly between them.
That is why `caption-job:` is a job written here and a caption written there.

### 2 · The unit cannot be declared before an answer exists
**The ordering rule**: `intake/` freezes FROM a `proof/`, and a `proof/` needs a landed value.

```text
🧭 OUTLINE   the plan carries a bare 🖼 mark            nothing on disk
🔢 the value lane lands an answer and pulls proof/
🖼 THEN this lane creates the unit folder and freezes it
```
📌 A page shipped "1 display declared, 0 unit folders on disk" on 260817 by declaring a unit nothing could fill, which is the incident this rule exists for.

#### 2.1 · A declared unit with no claim row is litter, not a proposal
(`display-declared-no-claim`, routed to DRAFT)
Nothing then says what the unit would show, so no renderer can draw it and no reader can miss it.
`QPf6-Display1-latex-proof` on this board is exactly that today, and it is one of the two errors `check.py` reports against `QPf6`.

### 3 · Rendering is not release
**The tick rule**: a labelled candidate may be rendered and cited while a question about it stays open.

```text
🟢 allowed   render and cite a PHI-safe aggregate intake as a labelled
             candidate while a method or provenance probe is still open
🔴 not       `accepted: ✅`, which is a person's and belongs to CHECK
             ⚠️ and it REVERTS when intake/ changes: `display-accept-stale`
```
📌 It is one of the five person-reserved ticks on this board and one of the two that go backward, the other being a probe card's `read:`.

### 4 · The lane does not wait for the others, but it does need one answer
**The parallel rule**: what this lane depends on is one landed answer, never another lane's schedule.

```text
📚 citation   this lane depends on it not at all
🔢 value      this lane depends on its OUTPUT, not on its schedule:
              one landed answer is enough to freeze one intake
```
📌 So no lane waits for another to FINISH, which is the qualification that makes the parallel claim true rather than merely convenient.

### 5 · The display unit IS an evidence card, and card names three shapes
**The one-word-three-shapes rule**: all three EVIDENCE kinds have a card on disk, and no two of them are the same kind of object (JL 260818: "the display will be one evidence card as well").

```text
kind          its card on disk                          lives under probe/ ?
──────────────────────────────────────────────────────────────────────────────
📚 citation   bibex/<stem>.bib · ONE ENTRY               ❌ no. A line in a file.
🔢 value      probe/PP<NN>-<slug>/card.md                ✅ yes, and it is the
              + consumer/ executor/ proof/                  ONLY one that does
🖼 display    display/<stem>-Display<N>-<slug>/          ❌ no. A folder with a
              intake/ + README.md                            README as its face
```
📌 So `haipipe-page-evidence` §🧾 is right that the display has a card, and a reader who expects that card under `probe/` will not find it: the word `card` covers a bib ENTRY, a probe FOLDER, and a display FOLDER, and only the middle one has a `PP<NN>` id.

#### 5.1 · This lane's card is DOWNSTREAM of a value card, never a peer
(its `intake/` freezes FROM a probe card's `proof/`, which is why this lane cannot start early)
A page can hold a value card with no display, and it can never hold a display with no answer behind it.
So the display card is the only one of the three that another card must exist first for.
That is the same fact as `§2`, stated in card terms rather than in phase terms.

#### 5.2 · Three shapes is why the status table needs three columns
(`cli/pagestatus.py` counts 📚 · 🔢 · 🖼 separately)
There is no one place on a page that says "this page has 6 evidence cards, 2 landed".
Each kind is counted by reading its own folder, and a page with a verified citation, no answered value and no frozen intake reads as three different numbers rather than one.
A single count would need a fourth file that copies the other three, and a copy drifts.

## Aims
### A1 · 🖼 This lane freezes, and never draws
- ⬜ A1.1 · No EVIDENCE run has written into a unit's `recipe/` or `assets/`.
  Done when a receipt audit finds no EVIDENCE receipt whose artifacts include a recipe or an asset.
  **Now:** Not measurable yet. `_runs/page/` holds five receipts and none is an EVIDENCE receipt, so there is nothing to audit.
- ⬜ A1.2 · Every frozen intake names its renderer.
  Done when every `intake/manifest.yaml` on this board carries a `kind:` row resolving to one of the five renderer skills.
  **Now:** Not met. Four units on this board have no frozen `intake/inputs/` at all, so none of the four can name a renderer for a snapshot it does not have.
### A2 · ⏱ The unit cannot be declared before an answer exists
- ⬜ A2.1 · No unit on this board is declared with an unfrozen intake.
  Done when `cli/check.py` reports zero `display-intake-unfrozen` findings.
  **Now:** Not met. `cli/check.py` reports `display-intake-unfrozen` on FOUR units: `QPf5-Display1`, `QPf5-Display2`, `QPw00-Display1`, `QPw00-Display2`.
- ⬜ A2.2 · No unit folder exists without a `claim:` row.
  Done when `cli/check.py` reports zero `display-declared-no-claim` findings.
  **Now:** Not met. `cli/check.py` reports one `display-declared-no-claim`, on `QPf6-Display1-latex-proof`.
### A3 · 🚫 Rendering is not release
- ✅ A3.1 · No `accepted: ✅` on this board binds a render that has since changed.
  Done when `cli/check.py` reports zero `display-accept-stale` findings.
  **Now:** Met today. `cli/check.py` reports zero `display-accept-stale` findings, though trivially: no unit on this board carries an `accepted: ✅` at all.


### A5 · 🃏 The display unit IS an evidence card, and card names three shapes
- 🔨 A5.1 · Every page's three card kinds are countable from disk without a fourth file.
  Done when `cli/pagestatus.py` reports 📚 · 🔢 · 🖼 per page and no page carries a summary file that restates them.
  **Now:** Partly met. `cli/pagestatus.py` reports the three columns and no page carries a summary file, but the fn is not yet wired as a verb of `haipipe-page`, so nothing calls it on a schedule.
- ⬜ A5.2 · No display unit exists whose intake did not come from a named probe card's `proof/`.
  Done when every `intake/manifest.yaml` on this board names the `PP<NN>` its snapshot was frozen from.
  **Now:** Not met, and not measurable: `intake/manifest.yaml` has no field for the `PP<NN>` it froze from, so the link is not merely unwritten, it has nowhere to be written.


## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `page-plugins/haipipe-plugin-display/SKILL.md`
  The unit folder, its README rows, and the five-step walk this page splits across phases. It wins over this page on all three.
- `page-workflows/haipipe-page-revise/SKILL.md`
  The phase that owns steps ② ③ ④, and the one that rebuilds the projections the unit is embedded in.
### 🧪 Checks · what CATCHES a page breaking a rule
- `haipipe-board/src/page_evidence.py`
  Computes the display findings. It emits TEN rule ids and the contract's table routes eight of them.
### 📤 Output files · what a BUILD writes
- `board/QPw/QPw4d-display.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.
### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `continues · ALL` · [QPw4 §4](5-QPw-page-workflow/QPw4-evidence/QPw4-evidence.md)
  The contract page these three lane faces belong to, and the walk split it summarizes.
- `continues · REVISE` · [QPw5 §3](5-QPw-page-workflow/QPw5-revise/QPw5-revise.md)
  The phase that draws what this lane freezes, and that rebuilds both projections.
- `reads · ALL` · [QPf5 §1](4-QPf-page-folder/QPf5-display/QPf5-display.md)
  The display plugin's unit contract and its five-step walk.

## Law
- 🖼 **This lane freezes and never draws**: `intake/` and the README rows only
  `recipe/`, `candidates/`, `assets/` and `float.tex` belong to the renderer, called at REVISE, and a hand-edited recipe is a render nobody can reproduce.
- ⏱ **A unit is born at EVIDENCE and no earlier**: its intake freezes from a proof that needs a landed answer
  Declaring a unit nothing can fill is how a page shipped "1 display declared, 0 unit folders on disk" on 260817.
- 🚫 **Rendering is not release**: a labelled candidate may be rendered and cited while its provenance question stays open
  Only `accepted: ✅` releases it, that tick is a person's, and it reverts when the intake changes.
- 📦 **Folder count is never completed work**: declared, rendered and accepted are three independent counts
  A version whose declared count exceeds its rendered count does not pass.

## Glossary
- 🖼 **unit**: the folder at `<page>/display/<stem>-Display<N>-<slug>/`, cited in prose by its short id.
- 🧊 **intake**: the frozen snapshot the figure will be drawn from, plus the named renderer that owes the drawing.
- 🎨 **renderer**: the skill named by the unit's `kind:` row, one of five, which owns `recipe/` end to end.
- ✋ **accepted: ✅**: the human tick at step ⑤, administered by CHECK, which reverts when the intake changes.

## Log
- 260818 · [DRAFT-CC] created as a lane face of `QPw4` on JL's ruling, given three times before it was executed. Every count on this page was read from `cli/check.py` in the same session rather than recalled, which matters because the earlier summary of this lane on `QPw4` said TWO unfrozen intakes when the real number is FOUR, and an independent reviewer caught it. The page keeps to step ① and names the owner of every other step, since the unit outliving the phase is this lane's whole difficulty.

- 260818 1420 · [DRAFT-CC] `§5` added on JL's ruling "the display will be one evidence card as well". It is already law in `haipipe-page-evidence` §🧾, and what the law does not say out loud is that the three kinds have three DIFFERENT shapes: a bib ENTRY, a `probe/PP<NN>` FOLDER, and a `display/<unit>` FOLDER, with only the middle one carrying a `PP<NN>` id. `§5.1` adds that this lane's card is downstream of a value card rather than a peer, and `§5.2` names the cost: three shapes need three columns in `cli/pagestatus.py`, because a single count would need a fourth file that copies the other three.
- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0