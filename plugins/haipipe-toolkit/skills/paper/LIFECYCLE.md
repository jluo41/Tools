# Paper Lifecycle — layered convergence, not a line

This document explains the full paper-skill mental model: how a paper moves
from a seed idea to submission, revision, and presentation, and how feedback
loops back to the right earlier layer.

For a comparison with the ARIS autonomous research workflow reference in
`references/aris`, see `ARIS_COMPARISON.md`.

For a script-style walkthrough from topic to paper, including the project-paper
handshake, see `LIFECYCLE_WALKTHROUGH.md`.

The key rule:

> A paper moves forward through pitch, narrative, architecture, plan, draft, and
> review; feedback loops back to the earliest layer that explains the failure.

The lifecycle is therefore not a linear pipeline. It is a forward path with
diagnosis-driven loopbacks.

## The forward path

```
0. Topic appears
   project seed, discovery direction, or early paper prospectus
      ↓
1. Paper Folder
   create or attach a paper repo/submodule; start in prospectus or manuscript mode
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
5a. Display Contract
   figure/table jobs, evidence sources, captions, labels, preview PDFs
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
| Prospectus/story layer | `0 Topic appears`, `1 Paper Folder`, `2 Paper Pitch` | Whether the topic is only a project direction, a paper prospectus, or a paper seed; then what a random reader should understand in one minute | `lifecycle/stage00_topic-appears/current.md`, `lifecycle/stage01_create-paper-folder/current.md`, `lifecycle/stage02_seed-pitch/current.md`; manuscript mode may mirror to `0-pitch/` |
| Evidence contract layer | `3 Evidence-Backed Narrative` | What the paper can honestly claim | `lifecycle/stage03_evidence-backed-narrative/current.md`, claim/evidence tables |
| Paper shape layer | `4 Architecture`, `5 Paper Plan`, `5a Display Contract`, `6 Build Skeleton` | How the story becomes a paper-shaped artifact | `lifecycle/stage04_architecture-minimap/current.md`, `lifecycle/stage05_paper-plan/current.md`, `lifecycle/stage05a_display-contract/`, `0-sections/`, `1-compile.sh` |
| Text realization layer | `7 Write Draft`, `8 Edit Cycle` | How the paper is written and polished | `0-sections/*.tex`, `0-*.bib`, edit comments, diff packages |
| External gate layer | `9 Review`, `10 Submit`, `11 Respond`, `12 Present` | How the paper survives audiences outside the author loop | review reports, `1-feedback/`, rebuttal drafts, submission bundles, slides/posters |

## Stage map

| Stage | Purpose | Primary skill | Typical inputs | Files changed | Gate / next decision |
|-------|---------|---------------|----------------|---------------|----------------------|
| 0. Topic appears | Classify a topic as project seed, paper prospectus, or paper seed | none, author notes, upstream project work | author judgment, literature review, project direction, task/probe/insight state | usually none; completion means a decision to stay in project discovery or start a paper prospectus repo | Is there enough direction to create a paper prospectus container? |
| 1. Paper Folder | Create or attach a concrete paper repo/submodule, usually under `examples/<Project>/paper/` | `haipipe-paper-structure folder --mode prospectus|manuscript` → `haipipe-paper-structure-bootstrap` | paper name, parent project, optional GitHub repo, maturity mode | prospectus mode: `README.md`, `lifecycle/stage00_topic-appears/current.md`, `lifecycle/stage01_create-paper-folder/current.md`; manuscript mode: `0-*.tex`, `0-*.bib`, `0-pitch/`, `0-sections/`, `0-display/`, `1-feedback/`, `1-compile.*` | Prospectus mode: hand off to project narrative; manuscript mode: fill the one-minute story before writing prose |
| 2. Paper Pitch | Maintain the one-minute story and its provenance | `haipipe-paper-structure pitch` | seed idea, review, discoveries, tasks, probes, insights, author decisions | `lifecycle/stage02_seed-pitch/current.md`; manuscript mode may mirror to `0-pitch/` | Is the story understandable, compelling, and honest about fragility? |
| 3. Evidence-Backed Narrative | Expand pitch into evidence-backed claim contract | `haipipe-paper-structure narrative` | pitch, claims from results, review notes, results, logs | `lifecycle/stage03_evidence-backed-narrative/current.md` | Do all claims trace to evidence and limitations? |
| 4. Architecture / Minimap | Decide the paper-shaped strategy | `haipipe-paper-structure architecture` | pitch, narrative, venue constraints, key numbers | `lifecycle/stage04_architecture-minimap/current.md` | Does the 5-act arc match the pitch and evidence? |
| 5. Paper Plan | Create the writing execution map | `haipipe-paper-structure plan` | pitch, narrative, architecture, figure needs, citations | `lifecycle/stage05_paper-plan/current.md` | Can the plan fit the venue and preserve the pitch? |
| 5a. Display Contract | Make figures/tables ready as story-evidence objects | `haipipe-paper-structure display` | pitch, narrative, architecture, plan, results, figure/table needs | `lifecycle/stage05a_display-contract/current.md`, `lifecycle/stage05a_display-contract/displays/`; manuscript mode may mirror to `0-display/` | Does each display have a claim, source, reader takeaway, caption, label, and input path? |
| 6. Build Skeleton | Materialize or repair the folder structure | `haipipe-paper-build-scaffold`, `haipipe-paper-build-restructure`, `haipipe-paper-build-check` | plan, venue, existing folder | `lifecycle/stage06_build-skeleton/current.md`, plus `0-sections/`, wrappers, display dirs, compile scripts | Does the folder conform and compile structurally? |
| 7. Write Draft | Realize the plan in LaTeX | `haipipe-paper-create`, `haipipe-paper-edit-write` | pitch, narrative, plan, section playbooks | `lifecycle/stage07_write-draft/current.md`, `0-sections/*.tex`, `0-*.bib`, display references | Does the draft carry the same story? |
| 8. Edit Cycle | Improve draft via comment-first passes | `haipipe-paper-edit`, edit topic skills, `haipipe-paper-edit-weaving` | draft, comments, audits, reviewer notes | `lifecycle/stage08_edit-cycle/current.md`, inline comments, accepted prose changes, diffs | Are problems local or do they expose deeper structure? |
| 9. Review Gate | Route failures to the right earlier layer | claim audit, citation audit, proof checker, reviewer skills | draft, PDF, pitch, narrative, plan | `lifecycle/stage09_review-gate/current.md`, audit reports, review notes | Local → edit; structural → plan/architecture; evidential → narrative/research; story → pitch |
| 10. Submit | Build venue-ready package | compile/submission audit skills | clean draft, venue requirements | `lifecycle/stage10_submit/current.md`, submission bundle, final PDFs | External review starts |
| 11. Respond / Revise | Convert reviews into revision plan and response | `haipipe-paper-rebuttal`, `paper-rebuttal`, `rebuttal-response` | reviewer comments, submitted manuscript, pitch/narrative | `lifecycle/stage11_respond-revise/current.md`, `1-feedback/`, response letter, revised sections | Which layer did reviewers actually challenge? |
| 12. Present | Cash the paper into talks/posters/slides | `paper-slides`, `paper-poster` | accepted/submitted paper, pitch, figures | `lifecycle/stage12_present/current.md`, slides, poster, presentation artifacts | Presentations may reveal pitch problems for future versions |

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
| Figure/table has no clear claim, source, caption, or input path | `5a Display Contract` | Display is not ready to enter the manuscript |
| Display preview fails to compile | `5a Display Contract` or display production skill | The display block is not ready to input |
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
| Whole idea no longer viable | `0 Topic appears` | Reclassify as project-only, start a new paper prospectus, merge into another paper, or stop |

## Paper prospectus rule

Early paper folders are allowed, but they must declare their maturity. The
preferred HAI-Pipe pattern is:

```
examples/<Project>/paper/Paper-<Slug>/    # Git submodule when a remote repo exists
  README.md
  lifecycle/
    README.md
    stage00_topic-appears/current.md
    stage01_create-paper-folder/current.md
```

`lifecycle/stage00_topic-appears/current.md` is not an abstract, pitch, outline,
or manuscript plan. It is the constraint file for discovery: tentative question,
paper-shaped unknown, current evidence status, discovery constraints, narrative
handoff, inquiry tracks, and promotion gate.
`lifecycle/stage01_create-paper-folder/current.md` hands the prospectus to the
project narrative layer, which then decides whether to trigger discover, probe,
task, or insight work.

Do not create `0-sections/`, `0-display/`, LaTeX wrappers, or compile scripts
until the prospectus is promoted to an active paper seed. Promotion requires a
stable narrative claim shape and evidence from discovery/tasks/probes/insights.
In short:

> Paper repo can start early; manuscript obligations start late.

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

### Display loop

Use when figures/tables exist but are not paper-ready display objects:

```
5a Display Contract → 7 Draft → 8 Edit Cycle → 9 Review Gate → 5a Display Contract
```

Examples: display lacks a claim, caption overclaims, `float.tex` is missing,
`preview.pdf` fails, a table's numbers changed without section prose changing,
or a figure exists but no section owns it.

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

- `lifecycle/stage00_topic-appears/current.md` changes when the paper-shaped
  discovery direction changes before the paper has a supported seed.
- `lifecycle/stage01_create-paper-folder/current.md` changes when the paper
  prospectus's open questions are handed to narrative, converted into
  discover/probe/task/insight work, resolved, or superseded.
- `lifecycle/stage02_seed-pitch/current.md` changes when the public-facing story
  changes.
- `lifecycle/stage03_evidence-backed-narrative/current.md` changes when claims,
  evidence, or limitations change.
- `lifecycle/stage04_architecture-minimap/current.md` changes when contribution
  emphasis, 5-act arc, page budget, or section strategy changes.
- `lifecycle/stage05_paper-plan/current.md` changes when the execution outline
  changes.
- `lifecycle/stage05a_display-contract/current.md` and its `displays/` folder
  change when figure/table jobs, sources, placement, readiness, captions, or
  preview status change.
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
