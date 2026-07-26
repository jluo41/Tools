# How prose carries what it does not yet know
state: 🟡 PARTIAL
owner: CC
method: keep typed placeholders; make each one name the question that owes it

## Question
What does a sentence say while the evidence it needs is still being fetched?

A draft cannot wait for evidence and must not invent it. So the prose carries typed placeholders: a slot that names what is missing and, crucially, which question will fill it. That pairing is what makes a half-finished paper auditable instead of merely unfinished.

## Boundary
- ✅ Covered here
  The placeholder grammar and its lifecycle from DRAFT to REVISE.
- ↪ Covered elsewhere
  The question a placeholder names is a probe entry, `QD1`; whether it may be dispatched is `QD2`; the settled sentence attachment grammar is `QBa4`.

## Content
### The grammar
```
 \cite{TOADD} [Q-Section-n]   a source is owed; that question will produce the key
 {VAL:? what}  [Q-Section-n]   a number is owed
 \citep{key}                   settled: the key greps in the paper's .bib
```
An unverified number is never written as a number, and a citation is never invented. That is the rule the whole thing exists to enforce.

### Born from content, dies into content
A placeholder is dropped in at DRAFT by the sentence that needs it, and discharged at REVISE by the worker that substitutes the landed answer. It is not a TODO list living beside the prose; it is inside the sentence that owes it, which is why it cannot be forgotten separately from the claim it supports.

### The refinement now available
The board's sentence apparatus lets a sentence carry typed `>` lanes beneath it, so the placeholder can stay minimal in the prose while everything known about it, the candidate source, its state, the probe path, sits in the lane. That splits "where it goes" from "what we know about it", which is what makes the prose readable while owing three citations.

## Items to Finish
- [x] 🏷 Typed placeholders exist and are enforced by the drafting rules
      No invented keys, no invented numbers.
- [x] 🔗 Each placeholder names its owing question
      The `[Q-Section-n]` bracket sits beside the slot, never fused into it.
- [ ] 📐 Rule the relationship to sentence lanes
      `QBa4` now owns whether a minimal inline anchor is complemented by a typed provenance lane.
- [ ] 🔎 Decide what a CHECK does with a surviving placeholder
      A placeholder that reaches CHECK is either a blocking defect or accepted debt. Today it is judged case by case.

## Where we are
The grammar is implemented and used across the MISQ paper. The lane refinement is live on three pages of that paper's board as a trial, unruled.

## Files
- `stages/5-section-edit/template.md`
  The placeholder rules, inline as drafting guidance.
- `../../2-phase/2-revise/haipipe-paper-revise-place/`
  The worker that discharges them.
