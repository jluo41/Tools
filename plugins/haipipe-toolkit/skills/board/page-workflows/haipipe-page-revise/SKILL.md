---
name: haipipe-page-revise
description: >-
  The REVISE phase contract for any Board Page: improve the realization of the
  current round while purpose and Aims stay fixed. Also where the page becomes
  its artifacts — cites each drawn unit by id, writes the caption, and
  rebuilds latex/ and word/. Trigger: page revise, REVISE phase, fixed Aims,
  land answer, rebuild the pdf, rebuild the docx, /haipipe-page-revise.
metadata:
  version: "0.5.0"
  last_updated: "2026-08-18"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-revise · make the current promise work

Load the contracts in this order:

```text
haipipe-page
  → matching page-types/ variant, when one exists
  → haipipe-page-revise
  → family craft: the stage's declared craft files, when the Page belongs to paper or application
```

What is REVISE's alone: the Page may change a great deal here while its promise may not move at all.
Its risk is the quiet swap: a revision that redefines what the Page is for while calling itself an improvement, which is why the fixed purpose and Aims are the phase's one test.
The moment the promise stops fitting, the work is a new DRAFT round and says so.

**REVISE may arrive fused to DRAFT, as the WRITE cycle**: when the promise is unchanged, the same
context that just performed DRAFT continues into this phase and appends this
phase's own receipt step (page-run-contract.md §The fused DRAFT+REVISE pass). The
contract below applies unchanged; only the boot is shared.

## ⚡ Brief

```text
Q          improve the realization while purpose and Aims stay fixed, and
           make the page BECOME its artifacts: cite each drawn unit by id,
           caption it for this page's claim, rebuild latex/ and word/
WRITES     per §✍️: Opening · Diagram · Content (under fixed Aims) ·
           States · Files · Log; never an Aim's intent

WALLS
  same promise after the change, or it is not REVISE: a purpose or Aim
    move is a new DRAFT round
  draws nothing: RENDER, PICK, BUILD are EVIDENCE's; the sentence, the
    caption, and the rebuild stay here
  never estimates, infers, or quietly drops an unanswered hole; it stays
    visible and keeps its id
  a drawn unit cited by nobody is not success (`display-rendered-not-cited`)
  both projections are rebuilt here, or the page is `projection-stale`
  never closes a human gate, never routes to CLOSE
  when an answer landed, the order is ① LAND ② ARGUE ③ SOUND ④ CITE ⑤ BUILD
  CANDIDATE mode only on explicit author request; DIRECT is the default

READ ECONOMY
  read fully ONLY the target page, the plan, and this brief
  trust the plan's Answered:/Drawn: values as written; re-read only cards
    whose line ends `· recount`, plus one spot-check (haipipe-page-draft §📖)
  batch shell calls; scope cli/check.py output to your page with grep
  never paste board-wide output or compile logs into your context; the
    board doors return compact JSON, use them

ROUTES (§🔀)
  fixed promise now works and is ready to judge → CHECK
  another claim turns out to have no support    → EVIDENCE
  purpose or Aims must change                    → DRAFT, new round
  more work under the same promise               → REVISE again

FUSED    REVISE may arrive fused to DRAFT (the WRITE cycle): the same
         context continues from DRAFT and appends this phase's own receipt
         step; only the boot is shared (../haipipe-page-workflow/ref/
         page-run-contract.md §The fused DRAFT+REVISE pass)

RECEIPT  one phase receipt per pass, shape in §🧾 below; field law:
         ../haipipe-page-workflow/ref/page-run-contract.md
         §Receipt step, field by field
```

Open the full contract below only where this brief does not settle your case; the full text wins every conflict.

## 🔒 The authority test

REVISE changes the Page while holding its purpose and Aims fixed.

```text
same promise after the change       → REVISE
purpose or Aim must change          → DRAFT, new round
an unsupported claim blocks the edit → EVIDENCE, then route again
```

The size, age, and operation of the edit do not decide the phase.
Adding a paragraph, deleting a section, moving an argument, and rewriting the Opening may all be REVISE when the current promise still describes the result.

REVISE may occur directly after DRAFT, after EVIDENCE, after CHECK feedback, or repeatedly.
It is not defined as the third step of a rigid sequence.

## ✍️ What REVISE may write

Subject to the base and matching Page Type:

```text
🧭 Opening      revise when the same purpose needs clearer expression
🖼 Diagram      revise when the same subject needs a better whole-page view
📚 Content      add · delete · move · rewrite under fixed Aims
🎯 Aims         do not change their intent inside REVISE
📍 States       update from visible evidence produced by the work
📎 Files        update continuations made stale by the revision
🗃 Log          record the pass, evidence used, and remaining gaps
```

An administrative correction to an Aim record may preserve its meaning.
Changing what the Aim promises is DRAFT even when the textual diff is small.

## 🧵 Land evidence before polishing affected prose

When EVIDENCE landed a card, revise in this order:

```text
① LAND       read A-consumer and its A-executor source, then discharge the owned hole
② ARGUE      test accuracy, warrant, sequence, and claim strength
③ SOUND      improve voice and readability after the final facts are present
④ CITE       cite every drawn display unit by id, and caption it for this page
⑤ BUILD      rebuild latex/ and word/ so the deliverable matches the source
```

The order is conditional, not a claim that every REVISE follows EVIDENCE.
If no answer landed, begin with the first applicable step.

An unanswered hole remains visible and keeps its id.
Never estimate, infer from nearby prose, quietly drop the sentence, or remove the marker merely to make the Page look finished.

## 🏗 The page becomes its artifacts here, or it never does

REVISE holds both projections and the citing sentence. It no longer holds the drawing (JL 260819).

```text
① INTAKE  🧑 freeze the material               EVIDENCE    intake/ + the renderer
② RENDER  ⚙️ the renderer writes recipe/       EVIDENCE    the build script or .tex
③ PICK    🧑 choose among candidates/          EVIDENCE
④ BUILD   ⚙️ assets/ · float.tex · preview     EVIDENCE    the citable float
⑤ ACCEPT  🧑 README `accepted: ✅`             CHECK       the human tick
```

**Why the three steps left, 260819.** They sat here on the reasoning that a caption and a choice of rows are argument. That was right about the caption and wrong about the drawing, and it made one of EVIDENCE's three lanes return raw material while the other two returned something usable: a citation lands a key, a value lands a bound number, and a display landed an unrendered folder.

**What REVISE keeps of a display**, and it is the argument half:

```text
  the SENTENCE that cites the unit by id                   REVISE
  the CAPTION that ties the figure to THIS page's claim    REVISE
  the unit's own `claim:` row, factual, what it shows      EVIDENCE
```

A unit that is drawn and cited by nobody is not this phase's success; the citing sentence is what makes it reach a reader, and `cli/check.py` reports `display-rendered-not-cited` against exactly that.

**Rendering is not release.** A PHI-safe aggregate intake may be drawn and cited as a labelled candidate while a method or provenance question stays open; only step ⑤'s human tick releases it.

**Both projections are rebuilt here.** `latex/` and `word/` are derived, and a page whose source moved without a rebuild reports `projection-stale`. Nothing downstream builds them for it (JL 260816).


## 🪞 Direct and candidate modes

```text
DIRECT      default · change the Page and record why a non-trivial change was made
CANDIDATE   explicit author request only · leave the Page unchanged and place a
            reviewable proposal in the Page Type's sentence or comment surface
```

Candidate mode is review material, not a completed revision.
The Page returns to direct REVISE after the author chooses.

The family craft files own prose, markup, or artifact-specific quality rules.
This contract owns only the phase boundary and routing.

## 🔀 Exit and routing

```text
fixed promise now works and is ready to judge → CHECK
another claim turns out to have no support    → EVIDENCE
purpose or Aims must change                    → DRAFT, new round
more work under the same promise               → REVISE again
```

REVISE never closes a human gate on its own.

## 🧾 RUN receipt

When called by RUN, read `../haipipe-page-workflow/ref/page-run-contract.md` and
return its common phase receipt. REVISE's receipt must additionally state:

```text
reason             which fixed Aim the revision now serves
artifacts          every target or continuation changed in this pass
evidence           landed answer, feedback, or close-reading evidence used
route              REVISE | EVIDENCE | DRAFT | CHECK | HOLD
reopens_promise    true only when revision discovered that purpose/Aims changed
```

A successful content change produces a new source/render version. REVISE may
suggest CHECK, but it never labels that version approved and never routes to
CLOSE. If it routes to DRAFT, the controller increments the round exactly once.

## 📂 Files

```text
page-workflows/haipipe-page-revise/
├── SKILL.md            this phase contract
└── CHANGELOG.md        version history
```

Owns no scripts.
The base is `haipipe-page`; Page Type variants live under `page-types/`; prose and artifact craft files remain in their owning families.
The Board engine owns execution and audit; this phase owns only its authority and receipt.

**This phase in six fields** (❓ asks · 📥 reads · 📤 writes · 🚪 exits · ✋ tick · 🔀 routes):
`../haipipe-page-workflow/ref/phase-cards.md` §WRITE, with COMPILE folded in. That file states every phase in the SAME fields, so one phase can be read next to another; this contract states the reasoning behind them.

**The Board page that argues this contract** is `QPw5-revise` on `BoardSkillBoard-260722`, created 260818 when JL ruled one page per workflow step. Its `## Law` rows and its `### Decision Now` carry what this contract leaves open.

## ✅ Exit checklist: the official-document sweep

Before this phase returns, run the board checker scoped to the page and clear
every `content-attribution` line your pen owns: no bare date codes, no person
named as authority, in `## Content` or Diagram prose. A flagged line inside a
frozen display transcription is LISTED for the display walk, never edited
here.
