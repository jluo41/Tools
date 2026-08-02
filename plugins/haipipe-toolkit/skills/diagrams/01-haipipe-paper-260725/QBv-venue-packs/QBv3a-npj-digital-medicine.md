# npj Digital Medicine: the only outlet in this tree with a shipped paper behind it

state: 🟡 PARTIAL · 21 exemplars · 7 sections · taste ✓ · the tech-check gate is unread by any skill
owner: JL
method: state what npj Digital Medicine requires of a digital tool, and record that this repo's one published paper sits here and its layout is therefore evidence

## Opening

This desk is where a digital-health paper is supposed to land, and it is also where such a paper is most often rejected for the reason it thought was its strength. What separates a tool this desk wants from a benchmark it refuses?

**Where this page sits**: it is one outlet under `QBv3`, which owns what the Nature portfolio's five outlets share.
This page owns only what is true of `playbook-nature-portfolio/npj-digital-medicine/`.

**Why this outlet is different from every other page in this group**: `Paper-MapPhyTrait-npjDM2025` was written into it and published.
Its section layout is the closest thing this repo has to a worked example of a venue pack being satisfied, and no page currently treats it as one.

**What is unique on disk**: `tech-check.md`, the only technical gate file in the whole venue tree. Nothing in the paper lifecycle opens it.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never transcribe the section norms**: word budgets live in `npj-digital-medicine/npjdm-<section>/style.md` and are cited, never copied.

**Say what the tool lets a clinician do**: this desk's test is about clinical capability, and performance language reproduces the failure it names.

✅ `changes what a clinician can know, measure, or do`  ❌ `achieves higher accuracy`

## Diagram

**A tool validated against a clinical outcome**: not a table validated against a benchmark.

```text
  🎯 THE TEST
     "Does this digital tool or method change what a clinician
      can know, measure, or do for a patient?"

  ✅ WHAT CLEARS IT
     a digital tool validated on CLINICAL OUTCOMES
     a large real-world deployment
     novel clinically-anchored measurement
     open pipelines ── the portfolio's open-science posture

  ❌ DESK-REJECT
     a pure ML benchmark with no clinical question
     an N < 100 pilot with no validation path
     accuracy tables with no clinical utility

  🔧 tech-check.md ── the only technical gate in the venue
     tree, and read by no skill

  📚 npjdm-related-work/ ── a standalone section, shared
     with all four Nature siblings and with no other pack

  🏆 21 exemplars · and one SHIPPED paper:
     Paper-MapPhyTrait-npjDM2025
```

## Content

### 1 · The clinical anchor is the whole bar

**Three rejections, one cause**: each names a paper that measured the model instead of the care.

```text
  💥 pure ML benchmark, no clinical question
  💥 N < 100 pilot, no validation path
  💥 accuracy tables, no clinical utility
        └── all three are the SAME failure:
            the outcome variable is about the MODEL

  ✅ the fix is not better numbers, it is a different
     outcome ── which is a task-layer decision, made long
     before venue runs

  🔗 the specialty analogue: Diabetes Care rejects device
     accuracy with no clinical outcome (QBv5a)
     ── a paper failing one usually fails the other
```

🎯 Establishes the outcome variable as the gate, which puts this outlet upstream of the venue stage alongside Nature Medicine.

#### 1.1 · This is the closest desk in the tree to this repo's standing work
(so its rejections are the ones worth reading before a study is designed, not after)
Physician-trait measurement from review text is a clinically-anchored measurement claim, which is one of this desk's four fit signals.
The same work reported as classifier accuracy is one of its three rejections, on identical data.

### 2 · The shipped paper is unexploited evidence

**A published layout nobody reads back**: the pack has 21 exemplars and this repo added a 22nd without filing it.

```text
  🏆 Paper-MapPhyTrait-npjDM2025
     ── published in this outlet
     ── in the SPACE repo's examples/ProjA-PhyTraitLandScape/
     ── NOT in npj-digital-medicine/examples/

  💡 what it could settle that nothing else can
     ── whether the npjdm-<section>/style.md numbers were
        actually met by a paper this repo wrote
     ── what npjdm-related-work/ looks like when satisfied
     ── a worked example for QBv0's pack contract

  🔧 and tech-check.md, unopened, is the file that would say
     whether the submission cleared the technical gate
```

🏆 Establishes the published paper as an unused verification of the pack, which is a cheaper check than any other in this group.

## Aims

### A1 · 🎯 The clinical anchor is the whole bar
- A1.1 · The outcome-variable gate is applied at the task layer rather than discovered at venue.
  **Done when:** a digital-measurement study records its clinical outcome before a venue is shortlisted.

### A2 · 🏆 The shipped paper is unexploited evidence
- A2.1 · `Paper-MapPhyTrait-npjDM2025` is checked against this outlet's section norms.
  **Done when:** each `npjdm-<section>/style.md` number is confirmed or corrected against a paper this repo published here.
- A2.2 · `tech-check.md` is read and its gate is stated where a submission to this outlet is prepared.
  **Done when:** the only technical gate in the venue tree is reachable from the lifecycle.

## States

### A1 · 🎯 The clinical anchor is the whole bar
- ⬜ A1.1 · Not started. The three rejections are prose in `taste.md`.

### A2 · 🏆 The shipped paper is unexploited evidence
- ⬜ A2.1 · Not started. The paper is published and is not among the 21 exemplars.
- ⬜ A2.2 · Not started. `tech-check.md` is referenced by no skill in the plugin.

## Files

- `../../paper/venue/playbook-nature-portfolio/npj-digital-medicine/taste.md` · the desk signals and the one-sentence test
- `../../paper/venue/playbook-nature-portfolio/npj-digital-medicine/tech-check.md` · the venue tree's only technical gate
- `QBv5a-diabetes-care.md` · the specialty outlet whose rejection pairs with this one
- `QBv3-nature-portfolio.md` · the family this outlet belongs to

## Law

This desk buys a change in what a clinician can know, measure, or do, so its three desk-rejects are one failure with three faces: an outcome variable about the model rather than the care.
A paper this repo published into an outlet is evidence about that outlet's pack, and leaving it unfiled wastes the only verification the pack can get for free.

## Glossary

- **Clinically-anchored measurement**: a measurement claim whose validation target is a clinical outcome rather than a benchmark, one of this desk's four fit signals.
- **tech-check**: this outlet's technical gate file, unique in the venue tree and distinct from both taste and section style.

## Log

260802 · Opened with the QBv outlet pages, from `playbook-nature-portfolio/npj-digital-medicine` at `Venue-Paper@fe25a88`.
