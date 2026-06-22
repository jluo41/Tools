---
name: haipipe-paper-structure-minimap
description: "Create or update the paper folder's 0-lifecycle/5-minimap/5-minimap.tex: the paragraph minimap that maps each section's paragraphs to a job and an evidence anchor (claim row + display unit). Wraps the architecture (blueprint) and plan (outline) skills and owns the minimap table. Use for paragraph minimap, paragraph jobs, evidence anchor, section map, architecture-minimap, paper plan, 5-minimap."
argument-hint: "[paper-dir]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-06-22"
  summary: "Maintain 0-lifecycle/5-minimap/5-minimap.tex as the paragraph job + evidence-anchor map."
---

Skill: haipipe-paper-structure-minimap
======================================

Maintain the **minimap** of a concrete paper folder: the last stage of the
lifecycle spine before prose. It answers one question:

```text
What job does each paragraph do, and what evidence anchors it?
```

The minimap is the bridge from the claim/display contract to `0-sections/`.
Every paragraph slot names its job and points to the claim row and display unit
that anchor it, so writing realizes the spine instead of inventing new claims.

This skill owns the minimap table and reuses two existing skills for the heavy
design work:

```text
haipipe-paper-structure-architecture   5-act arc, contribution emphasis, main-vs-appendix
haipipe-paper-structure-plan           section/figure/citation/page-budget outline
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

If the arc or outline is missing or stale, call the wrapped skills first:

```text
Skill("haipipe-paper-structure-architecture", args="<paper-dir>")
Skill("haipipe-paper-structure-plan", args="<paper-dir>")
```

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
one paragraph, and every planned display in `4-figures-tables` should appear in
at least one slot.

### Step 4: Handoff

Report the minimap summary (slot count, unanchored slots, uncarried claims) and
the next command:

```text
write the draft -> /haipipe-paper write <paper-dir>
```

Update `STATUS.md` (`current_layer`, `maturity: section-map`).
