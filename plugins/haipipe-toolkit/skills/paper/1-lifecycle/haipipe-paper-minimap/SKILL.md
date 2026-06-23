---
name: haipipe-paper-minimap
description: "Create or update the paper folder's 0-lifecycle/5-minimap/5-minimap.tex: the paragraph minimap that maps each section's paragraphs to a job and an evidence anchor (claim row + display unit). Folds in the architecture blueprint (5-act arc, page budget) and plan outline (venue constants, section skeletons) as ref/ material, and owns the minimap table. Use for paragraph minimap, paragraph jobs, evidence anchor, section map, architecture-minimap, paper plan, 5-minimap."
argument-hint: "[paper-dir]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-06-22"
  summary: "Maintain 0-lifecycle/5-minimap/5-minimap.tex as the paragraph job + evidence-anchor map."
  changelog:
    - "1.1.0 (2026-06-22): absorbed the retired architecture + plan skills as ref/ material (architecture-blueprint.md, plan-outline.md, architecture-examples/); dropped the two Skill() wrapper calls."
    - "1.0.0 (2026-06-22): baseline."
---

Skill: haipipe-paper-minimap
======================================

Maintain the **minimap** of a concrete paper folder: the last stage of the
lifecycle spine before prose. It answers one question:

```text
What job does each paragraph do, and what evidence anchors it?
```

The minimap is the bridge from the claim/display contract to `0-sections/`.
Every paragraph slot names its job and points to the claim row and display unit
that anchor it, so writing realizes the spine instead of inventing new claims.

This skill owns the minimap table and folds in two reference blueprints for the
heavy design work (merged here from the retired architecture and plan skills):

```text
ref/architecture-blueprint.md   5-act arc, contribution emphasis, main-vs-appendix, page budget
ref/plan-outline.md             section/figure/citation outline, venue constants
ref/architecture-examples/      worked examples (incl. the MISQ2026 opioid paper)
```

Read first: `../../PHILOSOPHY.md`, `../../ref/lifecycle-map.md`. For paragraph
ID conventions see `../../3-write-edit/_shared/paragraph-indexing.md`.

Location
--------

```text
<paper>/0-lifecycle/5-minimap/5-minimap.tex   standalone-compilable stage contract
```

Principles
----------

1. Every paragraph slot has a one-line job. A slot with no job is a defect.
2. Every slot names an evidence anchor: a `2-claims` row, a `0-displays` unit,
   or explicitly `none` (framing/transition).
3. The minimap follows the architecture arc and plan outline; if it disagrees,
   fix the upstream stage, do not let the minimap drift.
4. The minimap is a map, not prose. Do not write section text here.

Workflow
--------

### Step 1: Resolve paper folder

Accept the paper root or any path inside it (look upward for `0-lifecycle/`).

### Step 2: Gather upstream design

If the arc or outline is missing or stale, derive it here using the folded-in
blueprints before writing the table:

```text
ref/architecture-blueprint.md       5-act arc, contribution emphasis, page budget
ref/plan-outline.md                 section/figure/citation outline, venue FORMATTING constants
../../_venue/playbook-<venue>/README  "-> Minimap": venue SECTION structure + abstract shape (if a pack exists for STATUS venue)
```

When a `../../_venue/playbook-<venue>` pack exists for STATUS `venue`, its `-> Minimap`
mapping sets the section skeleton and abstract shape (e.g. clinical IMRAD + structured
abstract, MISQ theory-forward IMRAD). `plan-outline.md` venue constants stay for the
formatting and page budget; the pack supplies the section structure.

### Step 3: Write the minimap

Body table:

```latex
\section*{Paragraph Minimap}

\begin{tabular}{p{0.16\linewidth}p{0.30\linewidth}p{0.26\linewidth}p{0.18\linewidth}}
\toprule
Section / Para & Paragraph job & Evidence anchor & Display \\
\midrule
Intro P1 & motivate the problem & none & none \\
Results P1 & state core finding & C1 (2-claims) & display01-hero \\
\bottomrule
\end{tabular}
```

Cross-check: every `supported` claim in `2-claims` should be carried by at least
one paragraph, and every planned display in `4-display` should appear in
at least one slot.

### Step 4: Handoff

Report the minimap summary (slot count, unanchored slots, uncarried claims) and
the next command:

```text
write the draft -> /haipipe-paper write <paper-dir>
```

Update `STATUS.md` (`current_layer`, `maturity: section-map`).
