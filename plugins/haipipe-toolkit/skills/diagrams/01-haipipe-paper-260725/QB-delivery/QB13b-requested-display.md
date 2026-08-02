# A display someone asked for: who pulls the trigger, and what the result may overwrite

state: 🟡 PARTIAL
owner: JL
method: name the one commissioner, keep rendering off the spending ladder, and let no render touch what the manuscript shows

## Opening

Who may invoke a renderer, what does it cost, and what may the result overwrite?

Commissioning means handing the work to a separately registered worker skill rather than doing it in the stage. Candidate mode means the result lands beside the live asset instead of on top of it. Together they let a render be attempted at any time without ever destroying a display a person already accepted.

**Where this page sits**: `QA1@display` settles which LAYER owns which part of a display, and QB13a settles which half of a unit ships.
Neither says who may TRIGGER a render, which is a different question with a real safety property attached.
The spending ladder itself is QC4b, and what makes a result auditable afterwards is `QD6`.

**Why this face exists at all**: the rule answering it was written inside a stage template, which is the last place a reader would look for an authorization rule.
When that template was rewritten on 260726 the rule went with it, and it had to be reconstructed from the removed text and from `commissions:` in the stage contract.

**The safety property in one line**: a render lands in `candidates/` and touches nothing else.
Promotion into `assets/` is a decision the caller makes, so no invocation, however casual, can silently change what the manuscript shows.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Keep owning and triggering apart**: `QA1@display` answers who owns which part and QB13a answers which half ships.
This page answers who may pull the trigger, and conflating the three is what left the authorization rule homeless in the first place.

**State the cost rule as a contrast, never alone**: "a render does not spend" means nothing without "a bank question does".
The rule only lands when both halves are on the page.

**Name the live MISQ case whenever the protection is claimed**: `S-Display-2` is the running proof that the gap the rule creates is visible rather than silent.

## Diagram

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

## Content

### 1 · The commissioning asymmetry

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

#### 1.1 · The workers stay outside the contract on purpose
(a renderer that only works inside a paper stage is a renderer nobody else can use)
The four are registered skills invoked by name rather than steps inside `4-display`.
That keeps them callable with no paper at all, which is the whole reason the asymmetry was worth having.

### 2 · A render is not a bank question

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

#### 2.1 · Per-invocation authorization is stricter than a budget, not looser
(a budget lets an unwanted render through as long as there is room; a gate does not)
Because the user may strike any render at the gate before it runs, every render is individually authorized.
That is why not spending against `probe_depth` is safe rather than a loophole.

### 3 · What a render may touch

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

#### 3.1 · Migration is not promotion
(a provenance repair looks like a render decision and must not be allowed to act as one)
Moving an old unit from `source/` to `intake/` and `recipe/` may organize a verified source and record a rebuild path.
It may not replace `assets/`, retarget `float.tex`, or recategorize a candidate as current, because those remain explicit REVISE decisions owned by the caller.

## Aims

### A1 · 🧭 The commissioning asymmetry
- A1.1 · Rendering is commissioned rather than performed inside the stage.
  **Done when:** the four renderers are separately registered skills invoked by name, and the stage declares them in `commissions:`.
- A1.2 · Whether a non-display stage may commission a render is ruled.
  **Done when:** the answer is written on this face rather than implied by section-edit's `displays: file-only`.

### A2 · 💰 A render is not a bank question
- A2.1 · The cost rule lives where a worker will read it.
  **Done when:** that a render does not spend against `probe_depth` is stated somewhere a fresh agent finds without being told, rather than in a template that can be rewritten away.

### A3 · 🛡 What a render may touch
- A3.1 · A render cannot replace the live asset.
  **Done when:** candidate mode is in the generic output contract, and `assets/`, `float.tex`, and status are untouched until the caller promotes.

## States

### A1 · 🧭 The commissioning asymmetry
- ✅ A1.1 · Implemented and held. The four renderers are separate registered skills, and `4-display/stage.md` declares `commissions:`.
- 🧠 A1.2 · Waiting on JL. Section-edit currently FILES a display request and never creates one, which is a ruling on this question living in the section-edit contract rather than here.

### A2 · 💰 A render is not a bank question
- ⬜ A2.1 · Not started, and it has already been lost once. The rule was carried in the display stage template's "Render and sweep" section and went with the 260726 rewrite; it is reconstructed on this page and still has no home a worker reads.

### A3 · 🛡 What a render may touch
- ✅ A3.1 · Implemented and demonstrated. Candidate mode is in the generic output contract, and MISQ `S-Display-2` shows an accepted candidate C beside a v1 `assets/figure.pdf`, with the compiled paper still showing the older figure.

## Files

- `paper/1-lifecycle/haipipe-paper-stage/stages/4-display/stage.md` · declares `commissions:` and the commissioning asymmetry
- `display/ref/display-unit-output-contract.md` · candidate mode, and the rule that promotion belongs to the caller
- `paper/1-lifecycle/haipipe-paper-stage/stages/5-section-edit/stage.md` · `displays: file-only`, the existing partial answer to who else may commission
- `QB13a-display-folder.md` · which half of a unit ships, which this page must not re-decide

## Law

- A commissioned render lands in `candidates/` and touches `assets/`, `float.tex`, and the unit's status never.
  Promotion of a winner into `assets/` and demotion of losers into `versions/` is a REVISE decision made by the caller, never by the renderer.
  A render is the display stage's own step rather than a bank question, so it does not spend against `probe_depth`, and the user may strike any render at the gate before it runs.

## Glossary

- **Commissioning**: handing work to an independently registered worker skill invoked by name, rather than performing it inside the stage.
- **Candidate mode**: the write boundary that lets a render be attempted at any time by landing it beside the live asset instead of on top of it.

## Log

260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered into three divisions with face figures and captions, Aims regrouped as A1/A2/A3 with `Done when`, States mirrored per Aim, and a Glossary written for the first time. Two stale self-references repaired: the Scope line and the Diagram both named this page's own id for the renderer's output contract and for part ownership, and now name `display/ref/display-unit-output-contract.md` and `QA1@display`.
260802 · Became QB13b under the float series.
260727 · Retitled into the QD paradigm and renumbered QB5e -> QB5d. The face is unchanged; what changed is that the group now reads as one object seen four ways, the way QC does, so a reader meets the faces in the order the work happens: someone asks for a display, a folder comes back, the paper writes a caption on it, and it is placed in a section.
260727 · Renumbered QD5 -> QB5e when the QD group was cut from eight faces to four. It is the ONLY face of the old group that survived, because it is the only one that asked a consumer question: the other seven asked who owns rendering, what a renderer accepts, which renderer to pick, how formats project, and how provenance runs, and `/haipipe-display` now has a board that rules all of them. Its two open items are unchanged and are still the two that matter: whether a stage other than display may commission, and where the cost rule is written so a worker reads it.
260726 · Opened. The cost rule and the candidate-mode protection were carried in the display stage template's "Render and sweep" section, which was replaced when the template became per-asset. Reconstructed here from the removed text and from `commissions:` in the stage contract.
