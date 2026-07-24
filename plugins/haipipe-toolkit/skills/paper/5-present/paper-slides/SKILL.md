---
name: paper-slides
description: "Turn a compiled paper into a conference talk: extract the slide-by-slide talk outline, then hand it to /haipipe-display-slides to lay out (beamer → PDF + PPTX, speaker notes, talk script). Use when user says \"做PPT\", \"做幻灯片\", \"make slides\", \"conference talk\", \"presentation slides\", \"生成slides\", \"写演讲稿\", or wants slides for a paper. Owns the SELECTION (what a talk says about a paper); the rendering belongs to display/."
argument-hint: "[paper-directory-or-talk-length]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.2.0"
  last_updated: "2026-07-24"
  summary: "Compiled paper → talk outline → dispatch to haipipe-display-slides. Owns extraction; owns no layout."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Paper → Talk

Build a talk for: **$ARGUMENTS**

## What this skill owns

**The talk's structure, not its typesetting.** Turning a paper into a talk means choosing
the beats, cutting to fit the clock, and writing what the speaker actually says — that is a
paper job, and it lives here. Laying those slides out in beamer is a generic display job.

```
paper/main.tex + sections/*.tex + figures/
        │
        │  ← this skill: pick the beats, fit the clock, write the notes
        ▼
slides/talk-outline.md  +  slides/figures/        ← the handoff
        │
        │  ← /haipipe-display-slides: beamer, compile, review, PPTX, talk script
        ▼
slides/presentation.pdf · presentation.pptx · talk-script.md
```

The outline's shape is fixed by
[`display/ref/content-plan-spec.md`](../../../display/ref/content-plan-spec.md).
Write it to that shape and the renderer needs nothing else — it never opens the paper.

## Constants

- **PAPER_DIR = `paper/`** — Directory containing the compiled paper.
- **OUTPUT_DIR = `slides/`** — Where the outline, the figures, and the rendered deck land.
- **VENUE = `NeurIPS`** — Target venue (sets the renderer's colour scheme).
- **TALK_TYPE = `oral`** — `poster-talk` (2 min) · `spotlight` (5 min) · `oral` (15 min) · `invited` (30+ min).

These go into the outline's header, where they override the renderer's defaults.

## Phase 0: Verify the paper

```bash
ls $PAPER_DIR/main.tex || ls $PAPER_DIR/main.pdf
ls $PAPER_DIR/sections/*.tex
ls $PAPER_DIR/figures/
mkdir -p $OUTPUT_DIR/figures
```

No compiled paper → stop and say so. This skill has nothing to extract from.

## Phase 1: Extract the talk outline

Read `$PAPER_DIR/sections/*.tex` and build a slide-by-slide outline.

**Beat plan** — one parametric template keyed off talk length. Each row is a beat; the
cells give the slide number(s) it occupies (`—` = beat dropped at that length). `invited`
scales the same beats up with a Related Work beat and deeper Method/Results.

| Beat | Content Source | Figure? | poster-talk | spotlight | oral |
|------|----------------|:-------:|:-----------:|:---------:|:----:|
| Title | Paper metadata | No | 1 | 1 | 1 |
| Outline | Section headers | No | — | — | 2 |
| Motivation & Problem | Introduction | Optional | 2 | 2-3 | 3-4 |
| Key Insight | Introduction (contribution) | No | — | 4 | 5 |
| Method | Method section (condensed at shorter lengths) | Yes (hero figure) | 3 | 5-6 | 6-9 |
| Results | Experiments (key results only at shorter lengths) | Yes | 4-5 | 7-9 | 10-14 |
| Analysis / Ablations | Experiments | Yes | — | — | 15-16 |
| Limitations | Conclusion | No | — | — | 17 |
| Takeaway / Conclusion | Conclusion | No | 6 (+QR) | 10 | 18 |
| Thank You + QR | — | QR code | (folded into 6) | 11 | 19 |

**For each slide, write**:

- Heading (max 8 words)
- 3-5 bullets (max 8 words each)
- `figure:` — the figure it uses, if any, copied from `$PAPER_DIR/figures/` into `$OUTPUT_DIR/figures/` (`cp`, never symlink)
- `notes:` — 2-3 sentences of what the speaker actually says; this becomes the beamer speaker note
- Its share of the clock

**Content-authoring rules**:

- **Never invent citations.** Only references that exist in the paper's bibliography.
- **Every number must be real** — each result on a slide traces to one the paper reports.
- **De-AI polish**: no *delve, pivotal, underscore, noteworthy, leverage, facilitate, harness*.

**Output**: `$OUTPUT_DIR/talk-outline.md`, in the shape defined by
[`display/ref/content-plan-spec.md`](../../../display/ref/content-plan-spec.md) — header
(title, authors, venue, talk) then one `## ` per slide with its bullets, optional
`figure:`, and `notes:`.

**🚦 Checkpoint:**

```
📊 Talk outline ready:
- Talk type: [TALK_TYPE] ([N] min) → [N] slides
- Figures used: [N] → copied into slides/figures/
- Time budget: [breakdown]

Slide-by-slide:
1. [Title]
2. [Motivation — 1.5 min]
...

Proceed to render? Or adjust the outline?
```

**⛔ STOP HERE and wait for user response.** This is the most critical checkpoint — the
outline determines the entire talk flow.

Options: **"go"** → render · **adjustments** ("merge slides 3-4", "cut the ablation") → revise · **"stop"** → keep the outline on disk.

## Phase 2: Hand off to the renderer

```
Skill(haipipe-display-slides)  with  OUTLINE=slides/talk-outline.md
                                     FIGURES_DIR=slides/figures/
```

From here the renderer owns everything: beamer layout, compile, review, speaker notes,
PPTX export, and the full talk script. If the slide count disagrees with the talk length,
fix the **outline** and re-render — do not pad or cut from the renderer side.

## Boundary

- ✅ **This skill**: what a talk says about *this paper* — beats, cuts, speaker notes.
- ❌ **Not this skill**: how the deck looks — beamer theme, frames, compile, PPTX export.
  That is [`haipipe-display-slides`](../../../display/skills/haipipe-display-slides/SKILL.md),
  and it serves any source, not just papers.
