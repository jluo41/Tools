# Paper Lifecycle — layered convergence, not a line

This document explains the full paper-skill mental model: how a paper moves
from a seed idea to submission, revision, and presentation, and how feedback
loops back to the right earlier layer.

The key rule:

> A paper moves forward through pitch, narrative, architecture, plan, draft, and
> review; feedback loops back to the earliest layer that explains the failure.

The lifecycle is therefore not a linear pipeline. It is a forward path with
diagnosis-driven loopbacks.

## The forward path

```
0. Seed
   initial idea, author intuition, literature impression, rough direction
      ↓
1. Paper Folder
   create the concrete manuscript container
      ↓
2. Paper Pitch
   one-minute public-facing story for this paper
      ↓
3. Evidence-Backed Narrative
   claim/evidence/limitation contract
      ↓
4. Architecture / Minimap
   5-act arc, contribution emphasis, section minimap
      ↓
5. Paper Plan
   section, figure, citation, and page-budget execution plan
      ↓
6. Build Skeleton
   conforming paper folder, section files, display folders, compile scripts
      ↓
7. Write Draft
   LaTeX realization of the pitch/narrative/plan
      ↓
8. Edit Cycle
   comment-first content, values, citation, consistency, format, typeset passes
      ↓
9. Review Gate
   decide whether the failure is local, structural, evidential, or story-level
      ↓
10. Submit
   package the manuscript for the venue
      ↓
11. Respond / Revise
   reviewer response and revision, often reopening earlier layers
      ↓
12. Present
   slides, poster, talks, and other communication artifacts
```

## Layer model

The stages group into five layers. Loopback should target the layer that caused
the failure, not the stage where the failure was noticed.

| Layer | Stages | Owns | Main files |
|-------|--------|------|------------|
| Story layer | `0 Seed`, `2 Paper Pitch` | What a random reader should understand in one minute | `0-pitch/PAPER_PITCH.md`, `0-pitch/PITCH_LOG.md`, `0-pitch/archive/` |
| Evidence contract layer | `3 Evidence-Backed Narrative` | What the paper can honestly claim | `NARRATIVE_REPORT.md`, claim/evidence tables |
| Paper shape layer | `4 Architecture`, `5 Paper Plan`, `6 Build Skeleton` | How the story becomes a paper-shaped artifact | `vNN-architecture-minimap.md`, `PAPER_PLAN.md`, `0-sections/`, `0-display/`, `1-compile.sh` |
| Text realization layer | `7 Write Draft`, `8 Edit Cycle` | How the paper is written and polished | `0-sections/*.tex`, `0-*.bib`, edit comments, diff packages |
| External gate layer | `9 Review`, `10 Submit`, `11 Respond`, `12 Present` | How the paper survives audiences outside the author loop | review reports, `1-feedback/`, rebuttal drafts, submission bundles, slides/posters |

## Stage map

| Stage | Purpose | Primary skill | Typical inputs | Files changed | Gate / next decision |
|-------|---------|---------------|----------------|---------------|----------------------|
| 0. Seed | Start from intuition, review, or rough idea | none, author notes, upstream project work | author judgment, literature review, project direction | usually none, or notes outside paper folder | Is there enough direction to create a paper container? |
| 1. Paper Folder | Create a concrete manuscript home | `haipipe-paper-structure folder` → `haipipe-paper-structure-bootstrap` | paper name, venue, format | `0-*.tex`, `0-*.bib`, `0-pitch/`, `0-sections/`, `0-display/`, `1-feedback/`, `1-compile.*` | Fill the one-minute story before writing prose |
| 2. Paper Pitch | Maintain the one-minute story and its provenance | `haipipe-paper-structure pitch` | seed idea, review, discoveries, tasks, probes, insights, author decisions | `0-pitch/PAPER_PITCH.md`, `0-pitch/PITCH_LOG.md`, `0-pitch/archive/*.md` | Is the story understandable, compelling, and honest about fragility? |
| 3. Evidence-Backed Narrative | Expand pitch into evidence-backed claim contract | `haipipe-paper-structure narrative` | `PAPER_PITCH.md`, `CLAIMS_FROM_RESULTS.md`, `AUTO_REVIEW.md`, results, logs | `NARRATIVE_REPORT.md` | Do all claims trace to evidence and limitations? |
| 4. Architecture / Minimap | Decide the paper-shaped strategy | `haipipe-paper-structure architecture` | pitch, narrative, venue constraints, key numbers | `vNN-architecture-minimap.md` | Does the 5-act arc match the pitch and evidence? |
| 5. Paper Plan | Create the writing execution map | `haipipe-paper-structure plan` | pitch, narrative, architecture, figure needs, citations | `PAPER_PLAN.md` | Can the plan fit the venue and preserve the pitch? |
| 6. Build Skeleton | Materialize or repair the folder structure | `haipipe-paper-build-scaffold`, `haipipe-paper-build-restructure`, `haipipe-paper-build-check` | plan, venue, existing folder | `0-sections/`, wrappers, display dirs, compile scripts | Does the folder conform and compile structurally? |
| 7. Write Draft | Realize the plan in LaTeX | `haipipe-paper-create`, `haipipe-paper-edit-write` | pitch, narrative, plan, section playbooks | `0-sections/*.tex`, `0-*.bib`, display references | Does the draft carry the same story? |
| 8. Edit Cycle | Improve draft via comment-first passes | `haipipe-paper-edit`, edit topic skills, `haipipe-paper-edit-weaving` | draft, comments, audits, reviewer notes | inline comments, accepted prose changes, diffs | Are problems local or do they expose deeper structure? |
| 9. Review Gate | Route failures to the right earlier layer | claim audit, citation audit, proof checker, reviewer skills | draft, PDF, pitch, narrative, plan | audit reports, review notes | Local → edit; structural → plan/architecture; evidential → narrative/research; story → pitch |
| 10. Submit | Build venue-ready package | compile/submission audit skills | clean draft, venue requirements | submission bundle, final PDFs | External review starts |
| 11. Respond / Revise | Convert reviews into revision plan and response | `haipipe-paper-rebuttal`, `paper-rebuttal`, `rebuttal-response` | reviewer comments, submitted manuscript, pitch/narrative | `1-feedback/`, response letter, revised sections | Which layer did reviewers actually challenge? |
| 12. Present | Cash the paper into talks/posters/slides | `paper-slides`, `paper-poster` | accepted/submitted paper, pitch, figures | slides, poster, presentation artifacts | Presentations may reveal pitch problems for future versions |

## Loopback diagnosis

Loopback is chosen by diagnosis, not chronology.

| Symptom | Return to | Why |
|---------|-----------|-----|
| Sentence awkward, paragraph clumsy | `8 Edit Cycle` | Local prose issue |
| Number mismatch or stale metric | `8 Edit Cycle` plus values audit | Evidence exists, realization is wrong |
| Citation missing or unsupported | `8 Edit Cycle` plus citation audit | Local support needs correction |
| Paragraph has no point | `5 Paper Plan` | Paragraph job was not specified or no longer fits |
| Section feels unnecessary | `4 Architecture / Minimap` | Paper-shaped argument is wrong |
| Figure does not support its claimed point | `4 Architecture` or `5 Paper Plan` | Figure job or placement is wrong |
| Hero figure does not sell the paper | `2 Paper Pitch` or `4 Architecture` | Public story or paper-shaped strategy is wrong |
| Abstract and introduction disagree | `2 Paper Pitch` | The paper has multiple public stories |
| Contribution emphasis feels wrong for venue | `2 Paper Pitch` or `4 Architecture` | Audience and framing mismatch |
| Core claim too strong | `3 Evidence-Backed Narrative` | Claim/evidence contract needs downgrade |
| Claim unsupported | `3 Narrative`, then outside paper to discovery/task/probe | The paper cannot fix missing evidence by wording |
| Reviewer asks for missing experiment | Outside paper to `tasks/` or `probes/`, then `3 Narrative` | New evidence must enter before prose changes |
| Reviewer rejects framing | `2 Paper Pitch` | The one-minute story failed |
| Too much content for page budget | `5 Paper Plan` or `4 Architecture` | Allocation and main-vs-appendix decisions are wrong |
| Paper will not compile | `6 Build Skeleton` or typeset edit | Physical artifact is broken |
| Revision changes the central claim | `2 Pitch` and `3 Narrative` | Story and evidence contract both changed |
| Whole idea no longer viable | `0 Seed` | Start a new paper, merge into another paper, or stop |

## Important loopback patterns

### Edit loop

Use for local fixes:

```
8 Edit Cycle → 9 Review Gate → 8 Edit Cycle
```

Examples: awkward wording, wrong citation key, stale number, format issue,
overfull boxes.

### Plan loop

Use when the draft is locally correct but the section-level job is wrong:

```
5 Paper Plan → 7 Write Draft → 8 Edit Cycle → 9 Review Gate → 5 Paper Plan
```

Examples: paragraphs lack jobs, Results order is confusing, figure sequence is
not aligned with claims.

### Architecture loop

Use when the paper-shaped argument is wrong:

```
4 Architecture → 5 Plan → 7 Draft → 9 Review Gate → 4 Architecture
```

Examples: wrong contribution emphasis, wrong main-vs-appendix split, weak 5-act
arc, venue strategy mismatch.

### Narrative loop

Use when evidence and claims do not match:

```
3 Narrative → 4 Architecture → 5 Plan → 7 Draft → 9 Review Gate → 3 Narrative
```

If evidence is missing, leave the paper system:

```
3 Narrative → discovery/task/probe → insight/result → 3 Narrative
```

### Pitch loop

Use when the paper cannot be explained clearly in one minute:

```
2 Pitch → 3 Narrative → 4 Architecture → 5 Plan → 7 Draft → 9 Review Gate → 2 Pitch
```

Examples: weak hook, unclear surprise, no so-what, wrong audience, abstract and
intro selling different papers.

### Reviewer loop

Respond/revise is not terminal. It is the strongest loopback source:

```
11 Respond / Revise
  ├─ minor comments       → 8 Edit Cycle
  ├─ method critique      → 3 Narrative / 5 Plan
  ├─ missing experiment   → discovery/task/probe → 3 Narrative
  ├─ wrong contribution   → 2 Pitch / 4 Architecture
  └─ venue mismatch       → 2 Pitch / 4 Architecture
```

## File-change invariants

- `0-pitch/` changes when the public-facing story changes.
- `NARRATIVE_REPORT.md` changes when claims, evidence, or limitations change.
- `vNN-architecture-minimap.md` changes when contribution emphasis, 5-act arc,
  page budget, or section strategy changes.
- `PAPER_PLAN.md` changes when the execution outline changes.
- `0-sections/*.tex` changes when prose changes.
- `0-display/` changes when visual evidence changes.
- `1-feedback/` changes when external comments, rebuttal, or revision process
  artifacts arrive.

## Short version

```
Pitch is the story kernel.
Narrative is the evidence-backed contract.
Architecture is the paper-shaped strategy.
Plan is the writing execution map.
Draft is the LaTeX realization.
Review decides which earlier layer is broken.
```
