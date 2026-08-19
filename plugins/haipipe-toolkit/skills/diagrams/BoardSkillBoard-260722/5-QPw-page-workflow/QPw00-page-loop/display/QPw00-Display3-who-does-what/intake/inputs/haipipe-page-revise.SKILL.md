---
name: haipipe-page-revise
description: >-
  The REVISE phase contract for any Board Page. REVISE improves the realization of the current round while the Page's purpose and Aims stay fixed; it may add, delete, move, or rewrite, so edit shape never distinguishes it from DRAFT. REVISE is also where the page BECOMES ITS ARTIFACTS: it runs the display walk's render/pick/build steps on every unit EVIDENCE froze, cites each unit by id in the prose, and rebuilds latex/ and word/ so the deliverable a person opens matches the source. Load haipipe-page first, then the matching Page Type, then this contract, and finally the stage's declared family craft files. Use when incorporating landed evidence or feedback, rendering a frozen display intake, rebuilding the PDF or docx, improving structure or prose under fixed Aims, deciding whether a change instead requires a new DRAFT round, or preserving an unanswered hole rather than inventing its answer. Trigger: page revise, REVISE phase, fixed Aims, rewrite, add paragraph, delete section, move argument, land answer, render the display, rebuild the pdf, rebuild the docx, candidate diff, /haipipe-page-revise.
metadata:
  version: "0.4.2"
  last_updated: "2026-08-18"
  summary: "REVISE now owns the display walk's RENDER/PICK/BUILD steps and the latex + word rebuild (JL 260816): a landed answer that never became a float leaves the deliverable behind the source."
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
④ RENDER     draw every display unit whose intake EVIDENCE froze, cite it by id
⑤ BUILD      rebuild latex/ and word/ so the deliverable matches the source
```

The order is conditional, not a claim that every REVISE follows EVIDENCE.
If no answer landed, begin with the first applicable step.

An unanswered hole remains visible and keeps its id.
Never estimate, infer from nearby prose, quietly drop the sentence, or remove the marker merely to make the Page look finished.

## 🏗 The page becomes its artifacts here, or it never does

REVISE holds three of the display walk's five steps, and both projections. Nothing downstream builds them for it (JL 260816).

```text
step                                          owner       what it produces
────────────────────────────────────────────────────────────────────────────────────
① INTAKE  🧑 freeze the answer                EVIDENCE    intake/ + the named renderer
② RENDER  ⚙️ the renderer writes recipe/      REVISE      the build script or .tex source
③ PICK    🧑 choose among candidates/         REVISE      the winner
④ BUILD   ⚙️ assets/ · float.tex · preview    REVISE      the citable float
⑤ ACCEPT  🧑 README `accepted: ✅`            CHECK       the release decision
```

**Call the renderer the unit's `kind:` row names** (`haipipe-display-table` · `-figure` · `-diagram` · `-tex` · `-illustration`), or `haipipe-display` as the door when the kind is not yet clear. The renderer owns `recipe/` end to end; REVISE never hand-writes into it.

**Cite each unit by its short id in the sentence that makes the claim.** The citation's home is the prose (`Display3`, `Display5`), not a list at the bottom, because the projections inherit the citation: LaTeX embeds the unit's float after the citing paragraph and Word embeds the rasterized figure with its `(Figure n)` and a 🖼 comment. A unit nobody cites is a unit neither projection places.

**Rebuild both projections at the end of the pass**, and read what came out:

```text
latex/   POST /_board/latex   → <page>/latex/<stem>.tex + .pdf
word/    the word plugin      → <page>/word/<stem>.docx + its PDF twin
```

A pass that changed a claim, a number, or a unit and did not rebuild leaves the source and the deliverable disagreeing, and the person who finds that is the reader.
**Rendering is not release.** A PHI-safe aggregate intake may be rendered and cited as a labelled candidate while a method or provenance question stays open; only step ⑤'s human tick releases it.

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
`../haipipe-page-workflow/ref/phase-cards.md` §⑤, with ⑥ folded in. That file states every phase in the SAME fields, so one phase can be read next to another; this contract states the reasoning behind them.

**The Board page that argues this contract** is `QPw5-revise` on `BoardSkillBoard-260722`, created 260818 when JL ruled one page per workflow step. Its `## Law` rows and its `### Decision Now` carry what this contract leaves open.
