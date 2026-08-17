---
name: haipipe-page-evidence
description: >-
  The EVIDENCE phase contract for any Board Page, renamed from PROBE on 260816 because asking a question was only ONE of the three ways a claim gets its support. EVIDENCE's plain job: for every claim the Page's outline promised, put the thing that backs it on disk, in the card that holds it, with the hand that makes it named. The three kinds are a CITATION (a bibex entry a person landed), a VALUE (a probe card bound to its answering QA file), and a DISPLAY INTAKE (a frozen snapshot plus the renderer that will draw it). It changes the Page's knowledge boundary without authoring its argument. Load haipipe-page, the matching Page Type, this contract, and the shared haipipe-probe crossing protocol before the family door's tooling. Raising the card and dispatching the question are NOT here since 260817; they are page-workflows/haipipe-page-probe. Use when a dispatched question has come back, when a number needs binding to its answering QA file before it may be written, when a claim needs a figure or table and its intake must be frozen, or when an answer must return without being silently woven into prose. Trigger: page evidence, EVIDENCE phase, bind the answer, A-executor, A-consumer, evidence card, citation, value, display intake, freeze intake, name the renderer, evidence return, /haipipe-page-evidence.
metadata:
  version: "0.7.0"
  last_updated: "2026-08-17"
  summary: "EVIDENCE lands answers, proof, citations, and Display intake; it exposes a derived Evidence Bundle with owner feedback while REVISE owns final prose and Display selection."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-evidence · put the support for every promised claim on disk

Load the contracts in this order:

```text
haipipe-page
  → matching page-types/ variant, when one exists
  → haipipe-page-evidence
  → haipipe-probe                          for the VALUE kind's crossing
  → page-plugins/haipipe-plugin-bibex      for the CITATION kind
  → page-plugins/haipipe-plugin-display    for the DISPLAY INTAKE kind
  → the family DOOR's probe tooling, when the Page belongs to paper or application
```

`haipipe-probe` owns the shared crossing protocol, bank independence, and the evidence boundary.
This file owns how evidence of every kind is gathered inside a Board Page lifecycle.

## 🪪 The rename, and why the scope moved with it

This phase was `PROBE` / `haipipe-page-probe` until 260816.
Two things were wrong with that name, and only one of them was cosmetic:

```text
cosmetic     haipipe-page-probe and haipipe-probe read as the same skill.
             They are not: haipipe-probe is the crossing PROTOCOL and is now
             ONE CALLER of this phase, beside bibex and display intake.

substantive  PROBE owned 1 of the 3 things a claim needs. A page could finish
             PROBE with every question answered and still print a paragraph
             where a table was promised, because nothing owned the intake.
             That is not hypothetical: QV2-lbp-regression-results carried
             7 bound probe cards and 2 rendered displays out of 5 declared,
             and its LaTeX correctly embedded 2 (JL 260816: "you have five
             displays in the display plugins, but only two in the latex,
             why? Is it the workflow issue?"). It was.
```

⚠️ **`PROBE` is a LIVE phase again since 260817, and it is not this one.** `haipipe-page-probe` now owns raising the card and dispatching; this phase owns landing what comes back. A receipt written before 260817 whose `phase: PROBE` means EVIDENCE, and that alias holds for those receipts only.
The loop is now `OUTLINE · DRAFT · PROBE · EVIDENCE · REVISE · COMPILE · CHECK`.

DESIGN was weighed as the new name and rejected: `page-types/haipipe-page-for-design` already holds that word, and a phase called DESIGN would carry DRAFT's authority over purpose and Aims, which is the one thing this phase must never touch.

## 🧾 The three kinds, their cards, and the hands

Each kind has a card that holds it, a maker, and a human gate. None of the three gates moves here.

```text
kind             the card on disk                        MADE BY                    GATE 🧑
─────────────────────────────────────────────────────────────────────────────────────────────
📚 citation      <page>/bibex/<stem>.bib entry           a PERSON, verbatim only    `verified`
                                                         (bibex law: a machine may   field on
                                                         SUBSET or TRANSCRIBE,       the entry
                                                         never COMPOSE bibtex)
🔢 value         <page>/probe/PP<NN>-<slug>/card.md      the BANK: haipipe-task or  state: read 🧑
                                                         haipipe-discovery, answering  after `answered`
                                                         into its own QA file        + target: by PATH
🖼 display       <page>/display/<stem>-Display<N>-       this phase freezes intake/  accepted: ✅
   intake        <slug>/intake/ + README.md's            and NAMES the renderer;     in README,
                 `kind:` row                             the renderer draws it in    ticked at
                                                         REVISE                      CHECK
```

**A 🔢 card arrives already RAISED** (260817, replacing "DRAFT proposes"). `haipipe-page-probe` created it from the approved outline's mark, wrote its `serves:` backlink and dispatched its stripped question, so EVIDENCE usually opens onto a page whose value-holes are already folders.

```text
kind             who CREATES it                          who FILLS it
──────────────────────────────────────────────────────────────────────────────
🔢 value         ③ PROBE, from the outline's mark        EVIDENCE
📚 citation      a PERSON lands the entry; PROBE only     EVIDENCE binds it,
                 opens a card when the key is UNKNOWN     a person marks verified
🖼 display       EVIDENCE, and only here: the unit's      EVIDENCE
                 intake/ freezes FROM a proof/ that
                 does not exist before the answer does
```

Filling is the boundary for 🔢 and 📚; the display unit is this phase's from the first byte, because a unit that cannot yet be filled cannot honestly be declared either. DRAFT creates none of the three (`haipipe-page-draft` §🃏, 260817). Finding a card already raised is the normal case and is never a reason to create a second one: a question is asked ONCE, and a duplicate is the failure the id exists to prevent.

The three are ONE phase's work because they chain, not because they resemble each other:

```text
Q-executor ──▶ bank QA file ──▶ probe card ──▶ display intake/ ──▶ float.tex ──▶ latex · word
               "ask once, cite twice": a display's intake cites the bank by id
               and a render never invents a value (QPf5 §4)
```

Split that chain across phases and the handoff is what gets dropped, which is the QV2 failure exactly.

## 🔗 Evidence Bundle handoff

Once the three kinds have landed, EVIDENCE exposes the derived bundle for each
Outline Point. The bundle is a join, not a new artifact:

```text
C3.P1.B4
  ├─ answer/proof     Probe card, target path, proof manifest
  ├─ citation         Bibex key and verification state
  ├─ display input    frozen intake/ and named renderer
  └─ sentence         still a hole until REVISE realizes the Point
```

The Point address is the stable handoff. `serves:` is written by the Probe or
Display unit back to the frozen Point; EVIDENCE never edits the Outline to add
new ids. The bundle becomes `evidence-ready` only when every required source is
landed, and becomes `accepted` only after the human gates owned by the source
plugins and CHECK have passed. See
`../../page-plugins/haipipe-plugin-outline/ref/evidence-bundle.md` for the full
derived shape.

## 🧭 One phase, one lowercase unit, one persisted surface

Use these names and introduce no further lifecycle concept:

```text
EVIDENCE    the uppercase Page phase (PROBE, until 260816)
probe       one question and answer exchange: the VALUE kind's mechanism
QA-probe    the persisted surface for one neutral Q-executor: a hidden
            source record below the evidence page's probes/ folder, named
            <n>-<slug>.md, never a board page
```

The QA-probe ("entry" survives only as an informal alias) is a source file the evidence page points at, like a PDF; the board renders the evidence page, never the record (JL ruling B, 260806).
One conversation, two QAs: the QA-bank is the original, the QA-probe is the consumer's stub that points at it; consumer and executor name SLOTS inside them, never files, and the four slot words are capitals: Q-consumer, A-consumer, Q-executor, A-executor.
On the evidence page one `### E<n> ·` Content division owns one QA-probe (1:1), and many QA-probes may point at one QA-bank; that sharing lives at the bank (JL 260806).

## 🧱 The four forms and the wall

The wall applies to the VALUE kind: consumer and executor do not receive the same question.

```text
                 CONSUMER SIDE                    EXECUTOR SIDE
QUESTION         Q-consumer      ── strip stake ─▶ Q-executor
ANSWER           A-consumer      ◀─ interpret ─── A-executor
```

- Q-consumer is authoritative on the target Page and carries what the Page needs, why it matters, and what breaks.
- Q-executor is neutral, answerable by a stranger, and is the only question sent across the wall.
- A-executor is the returned answer anchored to its evidence source.
- A-consumer is the interpretation written for one Q-consumer.

One Q-executor may serve several Q-consumers.
That is reuse, not duplication.
The stake may appear in the Q-consumer and its audit trace, but never in the Q-executor, A-executor, dispatch payload, or bank artifact.

## 🔎 What EVIDENCE owns

On an evidence page the lifecycle runs COLLECT-first (JL 260806): a Q-consumer born on any page is COLLECTED into the owning topic's `### E0 · incoming` queue; the phase then TRANSLATES it, opening a new `### E<n>` division and its QA-probe, and the shared loop carries the rest:

```text
COLLECT      land the newly raised Q-consumer in the owning topic's E0 queue
① ORGANIZE   translate: strip the stake, write or reuse the Q-executor,      ③ PROBE
             promote E0's row into its E<n> division + QA-probe
② MATCH      read existing evidence before requesting new work               ③ PROBE
③ DISPATCH   send only the neutral Q-executor when new work is authorized    ③ PROBE
④ POINT      bind the returned answer by path (the QA-probe's target)        ④ EVIDENCE
⑤ INTERPRET  copy the A-executor back into the QA-probe, then write one      ④ EVIDENCE
             A-consumer per Q-consumer under the division's #### consumers
⑥ CARD       land the answer in its kind's card: a bibex entry for a         ④ EVIDENCE
             citation, the PP card's `state: answered` for a value, a frozen
             intake/ plus a named renderer for a display
```

**The six-step loop is ONE loop across TWO phases** (260817): ①②③ are
`haipipe-page-probe`'s, because they end when the question leaves, and ④⑤⑥ are
this phase's, because they begin when something comes back. The steps did not
change; only their owner is now written down.
Step ⑥ is what the rename bought, and it is the phase's exit condition, not an afterthought.
The family contract chooses the physical QA-probe, route vocabulary, cost ceiling, and evidence bank.
Those details do not change the phase boundary.

## 🖼 The display walk is SPLIT, and this phase owns only its first step

`haipipe-plugin-display` fixes one five-step walk per unit, and this contract does not fork it. It says which phase holds each step:

```text
① INTAKE  🧑 freeze the answer into intake/    EVIDENCE   it is the ANSWER, not the argument
② RENDER  ⚙️ the renderer writes recipe/       REVISE     the caption and which rows = ARGUMENT
③ PICK    🧑 choose among candidates/          REVISE
④ BUILD   ⚙️ assets/ · float.tex · preview.pdf REVISE
⑤ ACCEPT  🧑 README `accepted: ✅`             CHECK      the human gate, unmoved
```

So EVIDENCE never draws a table.
It freezes what the table will be drawn FROM, writes the unit's `README.md` rows (`kind:` · `claim:` · `caption-job:` · `intake:` · `fragility:` · `accepted: ⬜`), and names the renderer that owes step ②:

```text
kind: table         → haipipe-display-table
kind: figure        → haipipe-display-figure
kind: diagram       → haipipe-display-diagram
kind: tex           → haipipe-display-tex          tikz · algorithm2e · display equation
kind: illustration  → haipipe-display-illustration
```

Naming a ⬜ unit in prose is legal and useful: the chip binds a pending render and says what is owed.
Candidate rendering does not wait for release approval; a PHI-safe aggregate intake may be rendered for review while a method or provenance probe stays open.

## ✍️ The write surfaces

EVIDENCE writes beside the target prose and writes back only the Page-facing answer records:

```text
QA-probe        Q-executor · audit trace · route/binding · A-executor copy
probe/ card     PP<NN>-<slug>/card.md · state: planned → commissioned →
                answered → read 🧑 · target: (the ladder is the plugin's;
                raised/working/bound were retired 260817)
bibex/ bib      a person-supplied entry, landed verbatim, never composed
display/ unit   README.md rows + intake/ ONLY · never recipe/ · never assets/
target Page     E0 queue · E<n> division: QA-probe pointer, #### consumers
                rows (A-consumer per Q-consumer), #### answer digest ·
                evidence-based State update
target prose    never
purpose/Aims    never
```

EVIDENCE does not decide how an answer should be argued or silently replace a hole in target prose.
That landing edit belongs to REVISE while the promise stays fixed, or DRAFT if the answer changes the Page's purpose or Aims.

## 🔀 Trigger, exit, and routing

EVIDENCE starts when PROBE has raised the cards, or when REVISE or CHECK identifies a claim without support.
It may repeat, branch, reuse an existing answer, defer work above an authorized ceiling, or report that no route can answer the question.

**The exit test** is not "the answer came back". It is:

```text
every claim the outline promised has its card on disk, and every declared
display unit has a frozen intake/ and a named renderer
```

A unit folder that exists with no `intake/` is not evidence; it is a folder.
Route after the pass:

```text
cards are on disk, prose and renders are owed  → REVISE
answer changes purpose or Aims                 → DRAFT, new round
answer needs no prose or render change         → CHECK or continue current work
question remains authorized but unresolved     → EVIDENCE again or explicit defer
```

EVIDENCE is optional when the Page promises no claim it cannot already support.

## 🧾 RUN receipt

When called by RUN, read `../haipipe-page-workflow/ref/page-run-contract.md` and
return its common phase receipt. EVIDENCE's receipt must additionally identify:

```text
reason             the unsupported claim being resolved
artifacts          Q-executor / A-executor surface and Page-facing A-consumer
evidence           source bindings and the returned answer's limits
cards              one row per card landed: kind · path · state
renderers          one row per display unit whose intake froze: unit · kind ·
                   the renderer skill that owes step ② RENDER
route              EVIDENCE | REVISE | DRAFT | CHECK | HOLD
reopens_promise    true only when the answer changes purpose or an Aim
```

**A receipt with a frozen intake and no named renderer is incomplete.** That gap is
what let five declared units reach LaTeX as two, so it is a HOLD, not a pass.

The target Page's source hash may remain unchanged when EVIDENCE only writes its
declared side surface. That is not a missing version: the evidence artifacts must
still appear in the receipt. EVIDENCE never routes to CLOSE.

## 📂 Files

```text
page-workflows/haipipe-page-evidence/
├── SKILL.md            this Page-phase adapter
└── CHANGELOG.md        version history
```

Owns no scripts.
The shared crossing model is `probe/haipipe-probe`; the three cards belong to `page-plugins/haipipe-plugin-probe`, `haipipe-plugin-bibex`, and `haipipe-plugin-display`; Page Type variants live under `page-types/`; the family DOOR owns the persisted QA-probe shape and checker.
The deterministic display-lifecycle check is `haipipe-board/src/page_evidence.py`, run by `cli/check.py`.
The Board engine owns execution and audit; this phase owns only its authority and receipt.
