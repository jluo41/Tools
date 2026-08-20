---
name: haipipe-page-evidence
description: >-
  The EVIDENCE phase contract for any Board Page, renamed from PROBE on 260816 because asking a question was only ONE of the three ways a claim gets its support. EVIDENCE's plain job: for every claim the Page's outline promised, put the thing that backs it on disk, in the card that holds it, with the hand that makes it named. The three kinds are a CITATION (a bibex entry a person landed), a VALUE (a probe card bound to its answering QA file), and a DISPLAY INTAKE (a frozen snapshot plus the renderer that will draw it). It changes the Page's knowledge boundary without authoring its argument. Load haipipe-page, the matching Page Type, this contract, and the shared haipipe-probe crossing protocol before the family door's tooling. Raising the card and dispatching the question are NOT here since 260817; they are page-workflows/haipipe-page-probe. Use when a dispatched question has come back, when a number needs binding to its answering QA file before it may be written, when a claim needs a figure or table and its intake must be frozen, or when an answer must return without being silently woven into prose. Trigger: page evidence, EVIDENCE phase, bind the answer, A-executor, A-consumer, evidence card, citation, value, display intake, freeze intake, name the renderer, evidence return, /haipipe-page-evidence.
metadata:
  version: "0.11.0"
  last_updated: "2026-08-18"
  summary: "0.8.0 withdraws 0.7.3: the 🧮 proof mark it was written about is retired, so three marks meet three lanes. EVIDENCE lands answers, citations, and Display intake; it exposes a derived Evidence Bundle with owner feedback while REVISE owns final prose and Display selection."
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
The loop since 260819 runs `OUTLINE · PROBE · EVIDENCE` as a converging PREPARE loop, then `DRAFT · REVISE (COMPILE folded in) · CHECK`.

DESIGN was weighed as the new name and rejected: `page-types/haipipe-page-for-design` already holds that word, and a phase called DESIGN would carry DRAFT's authority over purpose and Aims, which is the one thing this phase must never touch.

## 🔁 EVIDENCE routes BACK to OUTLINE (260819)

```text
  ┌── PREPARE · repeat until self-consistent ─────────────┐
  │   🧭 OUTLINE ──▶ 📮 PROBE ──▶ 🃏 EVIDENCE             │
  │       ▲                            │                  │
  │       └──── this phase's answer changes the plan ──────┤
  └──────────────────────┬────────────────────────────────┘
                         ▼ 🚧 the plan's four-check gate
                     ✏️ DRAFT
```

**An answer is not a confirmation.** This phase's output goes to the PLAN first,
and the plan decides whether it still wants what it asked for. Two cases from
260819, both on `QPw00-page-loop`: a division the plan wanted scored 0 of 4 on the
split tests and was folded away, and a count of 17 was recomputed as 13.

**So EVIDENCE never routes to DRAFT.** It routes to ① OUTLINE, whose four checks
(coverage · address · value · shape) are the only thing that ends the loop.

## 🧱 Two stages, and the prose is in neither

EVIDENCE is not one act. It is MAKE, then BIND, and both happen inside the plugin folders (JL 260819: "先在对应的 plugins 上，把 display、citation、values 都先弄好；弄好之后，再把 evidence 加到正文上").

```text
  ① MAKE   build the thing in the folder that owns it
           📚 the bibex entry      🧮 the card's answer pulled into proof/
           🖼 the unit drawn: intake · recipe · assets · preview.pdf

  ② BIND   make it POINTABLE, so a sentence can name it and be checked
           📚 the key resolves in bibex/     `verified` 🧑
           🧮 `target:` names the answering QA file by PATH   `read:` 🧑
           🖼 the unit is previewable and its intake is frozen

  ─────────────── the page's prose starts HERE, and this phase stops ───────────
  ⑤ REVISE the sentence that uses it, the caption, the projections
```

**Nothing in either stage touches the page's `## Content`.** That is the whole boundary: this phase changes what the page KNOWS, and REVISE changes what it SAYS. A phase that both landed the answer and wrote the sentence could not be audited, because the only evidence that the answer came first would be its own report.

**A person's tick belongs to stage ②, not stage ①.** `verified` and `read:` are what turn a made thing into a bindable one, and they are the reason a page cannot quote a number nobody has read. `accepted: ✅` is the exception and stays at CHECK, because what it judges is the drawn artifact as a reader meets it.

## 🧾 The three kinds, their cards, and the hands

**Three kinds are marked and three arrive here**, one lane each
(`haipipe-plugin-outline` §📐):

```text
  📚 citation   ─▶  bibex/ entry              `verified` 🧑
  🧮 value      ─▶  probe/PP<NN>/             state: read 🧑
  🖼 display    ─▶  display/<unit>/intake/    accepted: ✅ 🧑
```

⛔ **A fourth mark, 🧮 proof, existed from 260817 to 260819 and is RETIRED.** The GLYPH was revived hours later as the VALUE mark (JL: "🧮 maybe this one?"), so 🧮 below means value, never proof.
0.7.3 stated a four-marks-three-lanes rule against it; that rule is withdrawn.
JL 260819: "我从开始到最后都没有说 proof，我一直说 probe". Going to a task or
discovery folder for the evidence behind a claim IS a probe, which is 🧮.

Each kind has a card that holds it, a maker, and a human gate. None of the three gates moves here.

```text
kind             the card on disk                        MADE BY                    GATE 🧑
─────────────────────────────────────────────────────────────────────────────────────────────
📚 citation      <page>/bibex/<stem>.bib entry           a PERSON, verbatim only    `verified`
                                                         (bibex law: a machine may   field on
                                                         SUBSET or TRANSCRIBE,       the entry
                                                         never COMPOSE bibtex)
🧮 value         <page>/probe/PP<NN>-<slug>/card.md      the BANK: haipipe-task or  state: read 🧑
                                                         haipipe-discovery, answering  after `answered`
                                                         into its own QA file        + target: by PATH
🖼 display       <page>/display/<stem>-Display<N>-       this phase freezes intake/, accepted: ✅
   intake        <slug>/intake/ + README.md's            NAMES the renderer, and     in README,
                 `kind:` row                             DRAWS it: RENDER · PICK ·   ticked at
                                                         BUILD are here (260819)     CHECK
```

**A 🧮 card arrives already RAISED** (260817, replacing "DRAFT proposes"). `haipipe-page-probe` created it from the approved outline's mark, wrote its `serves:` backlink and dispatched its stripped question, so EVIDENCE usually opens onto a page whose value-holes are already folders.

```text
kind             who CREATES it                          who FILLS it
──────────────────────────────────────────────────────────────────────────────
🧮 value         ② PROBE, from the plan's 📮 mark        EVIDENCE
📚 citation      a PERSON lands the entry; PROBE only     EVIDENCE binds it,
                 opens a card when the key is UNKNOWN     a person marks verified
🖼 display       EVIDENCE, and only here: the unit's      EVIDENCE
                 intake/ freezes FROM a proof/ that
                 does not exist before the answer does
```

Filling is the boundary for 🧮 and 📚; the display unit is this phase's from the first byte, because a unit that cannot yet be filled cannot honestly be declared either. DRAFT creates none of the three (`haipipe-page-draft` §🃏, 260817). Finding a card already raised is the normal case and is never a reason to create a second one: a question is asked ONCE, and a duplicate is the failure the id exists to prevent.

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
① ORGANIZE   translate: strip the stake, write or reuse the Q-executor,      ② PROBE
             promote E0's row into its E<n> division + QA-probe
② MATCH      read existing evidence before requesting new work               ② PROBE
③ DISPATCH   send only the neutral Q-executor when new work is authorized    ② PROBE
④ POINT      bind the returned answer by path (the QA-probe's target)        ③ EVIDENCE
⑤ INTERPRET  copy the A-executor back into the QA-probe, then write one      ③ EVIDENCE
             A-consumer per Q-consumer under the division's #### consumers
⑥ CARD       land the answer in its kind's card: a bibex entry for a         ③ EVIDENCE
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

## 🖼 The display walk, and this phase DRAWS

`haipipe-plugin-display` fixes one five-step walk per unit. This contract says which phase holds each step, and four of the five are here (JL 260819: "这个不应该是 evidence 里的这个 display 开始画图吗？REVISE 主要 work 还是 work 在这个 sentence 上面去").

```text
① INTAKE  🧑 freeze the material into intake/   EVIDENCE
② RENDER  ⚙️ the renderer writes recipe/        EVIDENCE
③ PICK    🧑 choose among candidates/           EVIDENCE
④ BUILD   ⚙️ assets/ · float.tex · preview.pdf  EVIDENCE
⑤ ACCEPT  🧑 README `accepted: ✅`              CHECK      the human gate, unmoved
```

**Why it moved, 260819.** Steps ② to ④ sat in REVISE until then, on the reasoning that a caption and a choice of rows are ARGUMENT, and argument is REVISE's. The reasoning was right about the caption and wrong about the drawing, and the asymmetry it produced is what exposed it:

```text
  📚 citation   returns a bib key            a thing the page can use
  🧮 value      returns a number + its run   a thing the page can use
  🖼 display    returned an intake folder    🚨 NOT a thing the page can use
```

Two of the three lanes landed evidence and the third landed raw material, so a page could report `3 of 3 lanes complete` with nothing drawn. A lane that performs one step out of five is not a lane.

**What REVISE keeps**, and it is the argument half:

```text
  the SENTENCE that cites the unit by id                  REVISE
  the CAPTION that ties the figure to THIS page's claim   REVISE may rewrite
  the unit's own `claim:` row, factual, what it shows     EVIDENCE
```

So the wall still holds: EVIDENCE may draw the figure and may not say what it proves. Choosing which rows a table shows is EVIDENCE's when the choice is legibility and REVISE's when the choice is emphasis; where that line falls on one unit is argued on `QPw4d-display`.

**Which intake a unit waits on depends on its KIND**, and no phase contract said so before 260819:

```text
  data kind     table · figure                intake freezes FROM a probe card's
                                              proof/ ── so it WAITS for an answer
  concept kind  diagram · tex · illustration  intake freezes a listing of source
                                              files ── nothing to wait for
```

A concept unit can therefore be built the moment its sources exist. A data unit cannot exist before its card is answered, which is the rule `haipipe-page-probe` §🧭 states as "EVIDENCE creates it".

The renderer is named from the `kind:` row:

```text
kind: table         → haipipe-display-table
kind: figure        → haipipe-display-figure
kind: diagram       → haipipe-display-diagram
kind: tex           → haipipe-display-tex          tikz · algorithm2e · display equation
kind: illustration  → haipipe-display-illustration
```

## ✍️ The write surfaces

EVIDENCE writes beside the target prose and writes back only the Page-facing answer records:

```text
QA-probe        Q-executor · audit trace · route/binding · A-executor copy
probe/ card     PP<NN>-<slug>/card.md · state: planned → commissioned →
                answered → read 🧑 · target: (the ladder is the plugin's;
                raised/working/bound were retired 260817)
bibex/ bib      a person-supplied entry, landed verbatim, never composed
display/ unit   README.md rows · intake/ · recipe/ · assets/ · preview.pdf
                (RENDER · PICK · BUILD are this phase's since 260819;
                the `accepted:` tick stays ⑦ CHECK's)
target Page     E0 queue · E<n> division: QA-probe pointer, #### consumers
                rows (A-consumer per Q-consumer), #### answer digest ·
                evidence-based State update
target prose    never
purpose/Aims    never
```

EVIDENCE does not decide how an answer should be argued or silently replace a hole in target prose.
That landing edit belongs to REVISE while the promise stays fixed, or DRAFT if the answer changes the Page's purpose or Aims.

## 🔁 Landing values creates fold debt (260819)

A card whose `## Values` lands does not finish the job: the ASKING bullet in
the plan still reads as a bare question. The next ① OUTLINE fold owes it the
answer, appended to that same bullet with each value id quoted inline
(`haipipe-page-outline` 0.6.0 §有问有答). This phase's return therefore lists
every card it landed, so the fold knows exactly which bullets owe answers.

## 🔀 Trigger, exit, and routing

EVIDENCE starts when PROBE has raised the cards, or when REVISE or CHECK identifies a claim without support.
It may repeat, branch, reuse an existing answer, defer work above an authorized ceiling, or report that no route can answer the question.

**The exit test** is not "the answer came back". It is:

```text
every claim the outline promised has its card on disk, and every declared
display unit is DRAWN and previewable: frozen intake/, recipe/, assets/,
and a preview.pdf a person can open
```

A unit folder that exists with no `intake/` is not evidence; it is a folder.
Route after the pass:

```text
whatever came back                             → ① OUTLINE, always
question remains authorized but unresolved     → EVIDENCE again, or a named HOLD
no route can answer it                         → HOLD, with the reason
```

⚠️ **This block said `→ REVISE` and `→ DRAFT` until 260819**, which is the same
contract disagreeing with its own §🔁 written the same day. The stale half was
found by the display agent rebuilding `QPw00-Display2`: it derived the route
relation from the contracts and had to choose between two blocks in this file.
An answer goes to the PLAN, and the plan's four-check gate is the only thing that
ends the PREPARE loop.

EVIDENCE is optional when the Page promises no claim it cannot already support.

## 🧾 RUN receipt

When called by RUN, read `../haipipe-page-workflow/ref/page-run-contract.md` and
return its common phase receipt. EVIDENCE's receipt must additionally identify:

```text
reason             the unsupported claim being resolved
artifacts          Q-executor / A-executor surface and Page-facing A-consumer
evidence           source bindings and the returned answer's limits
cards              one row per card landed: kind · path · state
renderers          one row per display unit drawn: unit · kind · the renderer
                   skill that ran RENDER · PICK · BUILD here (260819)
route              EVIDENCE | OUTLINE | HOLD
reopens_promise    true only when the answer changes purpose or an Aim
```

**A receipt with a frozen intake and no preview.pdf is incomplete.** That gap is
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

**This phase in six fields** (❓ asks · 📥 reads · 📤 writes · 🚪 exits · ✋ tick · 🔀 routes):
`../haipipe-page-workflow/ref/phase-cards.md` §③, all three lanes. That file states every phase in the SAME fields, so one phase can be read next to another; this contract states the reasoning behind them.

**The Board page that argues this contract** is `QPw4-evidence` on `BoardSkillBoard-260722`, created 260818 when JL ruled one page per workflow step. Its `## Law` rows and its `### Decision Now` carry what this contract leaves open.
