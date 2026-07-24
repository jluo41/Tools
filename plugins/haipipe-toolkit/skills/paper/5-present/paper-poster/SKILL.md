---
name: paper-poster
description: "Turn a compiled paper into a conference poster: extract the poster-worthy content into a content plan, then hand it to /haipipe-display-poster to lay out (A0/A1 PDF + PPTX + SVG). Use when user says \"做海报\", \"制作海报\", \"conference poster\", \"make poster\", \"生成poster\", \"poster session\", or wants a poster for a paper. Owns the SELECTION (what a poster shows of a paper); the rendering belongs to display/."
argument-hint: "[paper-directory-or-venue]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.2.0"
  last_updated: "2026-07-24"
  summary: "Compiled paper → poster content plan → dispatch to haipipe-display-poster. Owns extraction; owns no layout."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Paper → Poster

Build a poster for: **$ARGUMENTS**

## What this skill owns

**The selection, not the layout.** A poster shows roughly a third of a paper; deciding
*which* third — and turning dense prose into bullets and headline numbers — is a paper
job, and it lives here. Once that plan exists, laying it out as a poster is a generic
display job.

```
paper/main.tex + sections/*.tex + figures/
        │
        │  ← this skill: read, select, condense
        ▼
poster/poster-content-plan.md  +  poster/figures/     ← the handoff
        │
        │  ← /haipipe-display-poster: tcbposter, compile, review, export
        ▼
poster/poster.pdf · poster.pptx · poster.svg
```

The plan's shape is fixed by
[`display/ref/content-plan-spec.md`](../../../display/ref/content-plan-spec.md).
Write it to that shape and the renderer needs nothing else — it never opens the paper.

## Constants

- **PAPER_DIR = `paper/`** — Directory containing the compiled paper (main.tex + sections/ + figures/).
- **OUTPUT_DIR = `poster/`** — Where the plan, the figures, and the rendered poster land.
- **VENUE = `NeurIPS`** — Target venue (sets the renderer's colour scheme).
- **POSTER_SIZE = `A0`** · **ORIENTATION = `landscape`** · **COLUMNS = 4**
  Portrait A0 should use **3** columns, never 4 — text becomes too narrow to read.

These go into the plan's header, where they override the renderer's defaults.

## Phase 0: Verify the paper

```bash
ls $PAPER_DIR/main.tex || ls $PAPER_DIR/main.pdf
ls $PAPER_DIR/sections/*.tex
ls $PAPER_DIR/figures/
mkdir -p $OUTPUT_DIR/figures
```

No compiled paper → stop and say so. This skill has nothing to extract from.

## Phase 1: Extract the content plan

Read each section from `$PAPER_DIR/sections/*.tex` and select poster-appropriate content.

**Extraction rules** — a poster shows ~30-40% of the paper:

| Paper Section | Poster Extraction | Target Length |
|---------------|-------------------|---------------|
| Abstract | **Skip** — replace with 2-4 big-number stat callouts spanning all columns | 0 words (numbers only) |
| Introduction | Motivation: 2-3 bullets + numbered contribution list (4 items) | 120-160 words |
| Method | 1 hero architecture figure + key equations + 3-5 bullets | 80-120 words |
| Experiments | Dataset details + main result figures + numeric stat tables + ablation | 150-200 words |
| Conclusion | 3-4 key findings + 2-3 next steps | 60-80 words |
| Related Work | **Skip entirely** — no space on a poster | 0 |

**Total target: 300-500 words** of prose, excluding captions and callout numbers.

> ⚠️ **No abstract paragraph on a poster.** Replace it with a stat banner — 3-4 large
> headline numbers. This is the single highest-impact change for 60-second comprehension.

**Figure selection** — rank what's in `$PAPER_DIR/figures/` and pick 3-5:

- **Tier 1 (must)**: architecture / method overview, main results plot
- **Tier 2 (if space)**: ablation chart, qualitative examples, experimental paradigm
- **Tier 3 (skip)**: appendix figures, supplementary plots, tables-as-figures

Copy the chosen ones into `$OUTPUT_DIR/figures/` (`cp`, never symlink).

**Content-authoring rules**:

- **Never invent citations.** Only references that exist in the paper's bibliography.
- **Every number must be real** — each callout and table cell traces to a result the paper reports.
- **De-AI polish**: no *delve, pivotal, underscore, noteworthy, leverage, facilitate, harness*.

**Output**: `$OUTPUT_DIR/poster-content-plan.md`, in the shape defined by
[`display/ref/content-plan-spec.md`](../../../display/ref/content-plan-spec.md) — header
(title, authors, venue, size, orientation, columns, link), `## Stat callouts`, then one
`### ` box per poster box carrying `col:`, optional `figure:` + `caption:`, optional
`stats:`, and its bullets.

**🚦 Checkpoint:**

```
📋 Poster content plan ready:
- Title: [paper title]
- Venue: [VENUE] ([POSTER_SIZE] [ORIENTATION], [COLUMNS] columns)
- Stat callouts: [N]
- Boxes: Col1=[N], Col2=[N], Col3=[N], Col4=[N]
- Figures selected: [N] → copied into poster/figures/
- Prose word count: [N] (target 300-500)

Proceed to render? Or adjust the selection?
```

**⛔ STOP HERE and wait for user response.** This is the one decision that matters — once
the plan is right, rendering is mechanical.

## Phase 2: Hand off to the renderer

```
Skill(haipipe-display-poster)  with  PLAN=poster/poster-content-plan.md
                                     FIGURES_DIR=poster/figures/
```

From here the renderer owns everything: tcbposter layout, compile, visual review, and the
PDF / PPTX / SVG exports. If it reports a box overrunning its column, fix the **plan** and
re-render — do not fight the layout from this side.

## Boundary

- ✅ **This skill**: what a poster shows of *this paper*, condensed into a content plan.
- ❌ **Not this skill**: how a poster looks — columns, cards, fonts, compile, export.
  That is [`haipipe-display-poster`](../../../display/skills/haipipe-display-poster/SKILL.md),
  and it serves any source, not just papers.
