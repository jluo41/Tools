---
name: haipipe-display-slides
description: "Render conference presentation slides (beamer LaTeX → PDF + editable PPTX), with speaker notes and full talk script, from a TALK OUTLINE — a markdown outline plus a figures folder, per ref/content-plan-spec.md. Source-agnostic: it never opens a paper. Use when user says \"做PPT\", \"做幻灯片\", \"make slides\", \"conference talk\", \"presentation slides\", \"生成slides\", \"写演讲稿\", or hands over a talk outline to lay out. To build one from a compiled paper, run /paper-slides — it extracts the outline, then calls this."
argument-hint: "[talk-outline.md or talk-length]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, mcp__codex__codex, mcp__codex__codex-reply
metadata:
  version: "0.2.0"
  last_updated: "2026-07-24"
  summary: "Talk outline + figures/ → beamer → PDF + PPTX, with speaker notes and talk script. Renders what it is given; never reads the source it came from."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Paper Slides: From Paper to Conference Talk

Generate conference presentation slides from: **$ARGUMENTS**

## Context

This skill runs **after** Workflow 3 (`/paper-writing`).
It takes a compiled paper and generates a presentation slide deck for conference oral talks, spotlight presentations, or poster lightning talks.

Unlike posters (single page, visual-first), slides tell a **temporal story**: each slide builds on the previous one, with progressive revelation of the research narrative.
A good talk makes the audience understand *why this matters* before showing *what was done*.

## Constants

- **VENUE = `NeurIPS`** — Target venue, determines color scheme.
  Supported: `NeurIPS`, `ICML`, `ICLR`, `AAAI`, `ACL`, `EMNLP`, `CVPR`, `ECCV`, `GENERIC`.
  Override via argument.
- **TALK_TYPE = `spotlight`** — Talk format.
  Options: `oral` (15-20 min), `spotlight` (5-8 min), `poster-talk` (3-5 min), `invited` (30-45 min).
  Determines slide count and content depth.
- **TALK_MINUTES = 15** — Talk duration in minutes.
  Auto-adjusts slide count (~1 slide/minute for oral, ~1.5 slides/minute for spotlight).
  Override explicitly if needed.
- **ASPECT_RATIO = `16:9`** — Slide aspect ratio.
  Options: `16:9` (default, modern projectors), `4:3` (legacy).
- **SPEAKER_NOTES = true** — Generate `\note{}` blocks in beamer and corresponding PPTX notes.
  Set `false` for clean slides without notes.
- **OUTLINE = `talk-outline.md`** — The talk outline to render. Shape: [`ref/content-plan-spec.md`](../../ref/content-plan-spec.md).
  `venue` and `talk` declared inside the outline **override** the constants above.
- **FIGURES_DIR = `figures/`** — Folder holding every image the outline names. A `figure:` with no matching file is an error, not a guess.
- **OUTPUT_DIR = `slides/`** — Output directory for all slide files.
- **REVIEWER_MODEL = `gpt-5.4`** — Model used via Codex MCP for slide review.
- **AUTO_PROCEED = false** — At each checkpoint, **always wait for explicit user confirmation**.
- **COMPILER = `latexmk`** — LaTeX build tool.
- **ENGINE = `pdflatex`** — LaTeX engine.
  Use `xelatex` for CJK text.

> 💡 Override: `/paper-slides "paper/" — talk_type: oral, venue: ICML, minutes: 20, aspect: 4:3`

## Talk Type → Slide Count

| Talk Type | Duration | Slides | Content Depth |
|-----------|----------|:------:|---------------|
| `poster-talk` | 3-5 min | 5-8 | Problem + 1 method slide + 1 result + conclusion |
| `spotlight` | 5-8 min | 8-12 | Problem + 2 method + 2 results + conclusion |
| `oral` | 15-20 min | 15-22 | Full story with motivation, method detail, experiments, analysis |
| `invited` | 30-45 min | 25-40 | Comprehensive: background, related work, deep method, extensive results, discussion |

## Venue Color Schemes

Same as `/paper-poster`:

| Venue | Primary | Accent | Background | Text |
|-------|---------|--------|------------|------|
| NeurIPS | `#8B5CF6` | `#2563EB` | `#FFFFFF` | `#1E1E1E` |
| ICML | `#DC2626` | `#1D4ED8` | `#FFFFFF` | `#1E1E1E` |
| ICLR | `#059669` | `#0284C7` | `#FFFFFF` | `#1E1E1E` |
| CVPR | `#2563EB` | `#7C3AED` | `#FFFFFF` | `#1E1E1E` |
| GENERIC | `#334155` | `#2563EB` | `#FFFFFF` | `#1E1E1E` |

## State Persistence (Compact Recovery)

Persist state to `slides/SLIDES_STATE.json` after each phase:

```json
{
  "phase": 3,
  "venue": "NeurIPS",
  "talk_type": "spotlight",
  "slide_count": 10,
  "codex_thread_id": "019cfcf4-...",
  "status": "in_progress",
  "timestamp": "2026-03-18T15:00:00"
}
```

**On startup**: if `SLIDES_STATE.json` exists with `"status": "in_progress"` and within 24h → resume.
Otherwise → fresh start.

## Workflow

### Phase 0: Input Validation & Setup

1. **Check prerequisites**:
   ```bash
   which pdflatex && which latexmk
   ```

2. **Verify the talk outline and its figures**:
   ```bash
   ls $OUTLINE                    # the outline must exist
   ls $FIGURES_DIR                # and the folder it draws figures from
   grep -n '^figure:' $OUTLINE    # every named figure must be present below
   ```

   Check it parses into the shape in [`ref/content-plan-spec.md`](../../ref/content-plan-spec.md):
   a title header and one `## ` per slide. Then confirm every `figure:` names a file that
   is actually in `$FIGURES_DIR`.

   **⛔ If anything is missing, stop and say exactly what.** Do not go looking for a paper,
   do not infer slides from a source document. This skill renders the outline it was handed;
   filling gaps is upstream's job (`/paper-slides` for a paper).

3. **Backup existing slides**: if `slides/` exists, copy to `slides-backup-{timestamp}/`

4. **Create output directory**: `mkdir -p slides/figures`

5. **Detect CJK**: if the outline contains Chinese/Japanese/Korean, set ENGINE to `xelatex`

6. **Determine slide count**: from TALK_TYPE and TALK_MINUTES using the table above

7. **Check for resume**: read `slides/SLIDES_STATE.json` if it exists

**State**: Write `SLIDES_STATE.json` with `phase: 0`.

### Phase 1: Read the Talk Outline

The slide-by-slide decisions already happened upstream — **this skill does not choose the
talk's structure.** Parse `$OUTLINE` and carry it straight into drafting:

- **Header** — `title`, `authors`, and the overrides (`venue`, `talk`). Outline values win
  over the Constants above; the `talk:` value sets the expected slide count.
- **One `## ` per slide, in order** — each with its bullets, an optional `figure:`, and an
  optional `notes:` line that becomes the beamer speaker note.

**Do not add or drop slides.** If the outline's slide count disagrees with the expected
count for its `talk:` length, say so at the checkpoint and let the author fix the outline —
silently padding or cutting a talk is not this skill's call.

**🚦 Checkpoint:**

```
📊 Talk outline read:
- Talk type: [TALK_TYPE] ([TALK_MINUTES] min) — expected ~[N] slides
- Slides in outline: [N]
- Figures referenced: [N] (all present in FIGURES_DIR ✓)
- Slides carrying speaker notes: [N]/[N]

Slide-by-slide:
1. [Title]
2. [Motivation]
...

Proceed to drafting?
```

**⛔ STOP HERE and wait for user response.**

**State**: Write `SLIDES_STATE.json` with `phase: 1`.

### Phase 2: Slide-by-Slide Content Drafting

For each slide in the outline, draft the actual content.

**Presentation rules (enforced strictly)**:

| Rule | Rationale |
|------|-----------|
| **One message per slide** | If a slide has two ideas, split it |
| **Max 6 lines per slide** | More than 6 lines = wall of text |
| **Max 8 words per line** | Audience reads, not listens, if text is long |
| **Sentence fragments, not sentences** | "Improves F1 by 3.2%" not "Our method improves the F1 score by 3.2 percentage points" |
| **Figure slides: figure ≥60% area** | The figure IS the content; bullets are annotations |
| **Bold key numbers** | "Achieves **94.3%** accuracy" |
| **Progressive disclosure** | Use `\pause` or `\onslide` for complex slides |
| **No Related Work slide** | Unless invited talk (30+ min) |

**For each slide, produce**:
1. `\frametitle{}`
2. Content (itemize or figure + caption)
3. `\note{}` with speaker text (if SPEAKER_NOTES=true)

### Phase 3: Generate Slides LaTeX

Create `slides/main.tex` using beamer.

**Template structure**: use `ref/slides-template.tex` (full `\documentclass … \end{document}` beamer skeleton with venue-theme color hooks, footline frame numbers, and a text + figure sample frame). Substitute `VENUE_PRIMARY`/`VENUE_ACCENT`, metadata, and per-slide frames.

**Copy in the figures the outline names** (from `$FIGURES_DIR`, never symlink — `pdflatex`
cannot reliably follow symlinks across directories):
```bash
cp $FIGURES_DIR/<figure named in the outline> slides/figures/
```

**Key formatting rules**:
- Title font: ≥28pt, venue primary color
- Body font: ≥20pt
- Footnotes: ≥14pt
- No navigation symbols
- Frame numbers in bottom-right
- Clean white background (no gradients, no decorative elements)

### Phase 4: Compile Slides

```bash
cd slides && latexmk -$ENGINE -interaction=nonstopmode main.tex
```

**Error handling loop** (max 3 attempts):
1. Parse error log
2. Fix: missing package, undefined command, file not found, overfull boxes
3. Recompile

**Verification**:
```bash
# Check slide count matches outline
pdfinfo slides/main.pdf | grep Pages
```

If page count differs significantly from outline (>2 slides off), investigate.

**State**: Write `SLIDES_STATE.json` with `phase: 4`.

### Phase 5: Codex MCP Review

Send the slide outline + selected LaTeX frames to GPT-5.4 xhigh:

```
mcp__codex__codex:
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    Review this [TALK_TYPE] presentation ([TALK_MINUTES] min) for [VENUE].

    Evaluate using these criteria (score 1-5 each):

    1. **Story arc** — Does the talk build a compelling narrative? (Problem → insight → method → evidence → takeaway)
    2. **Slide density** — Any slides with too much text? (Max 6 lines, 8 words/line)
    3. **Time budget** — Is [N] slides realistic for [TALK_MINUTES] minutes?
    4. **Figure visibility** — Will figures be readable on a projector?
    5. **Opening hook** — Do slides 2-3 grab attention? (Not "In this paper, we...")
    6. **Takeaway** — Is the final message clear and memorable?
    7. **Progressive build** — Are complex ideas revealed gradually?

    Slide outline:
    [PASTE SLIDE_OUTLINE.md]

    Selected frames (LaTeX):
    [PASTE KEY FRAMES]

    Provide:
    - Score for each criterion
    - Top 3 actionable fixes
    - Overall: Ready to present? (Yes / Needs revision / Major issues)
```

Apply fixes.
Recompile if LaTeX was changed.

> ⚠️ If `mcp__codex__codex` is not available (no OpenAI API key), skip external review and proceed to Phase 6. Note the skip in `SLIDES_STATE.json`.

Save review to `slides/SLIDES_REVIEW.md`.

**State**: Write `SLIDES_STATE.json` with `phase: 5`.

### Phase 6: Speaker Notes

For each slide, ensure a `\note{}` block exists with:

1. **What to say** (2-3 complete sentences, conversational tone)
2. **Timing hint** (e.g., "spend 1 minute here", "quick — 20 seconds")
3. **Transition phrase** to the next slide (e.g., "So how do we actually implement this?
   Let me show you...")

Also generate `slides/speaker_notes.md` as a standalone backup:

```markdown
# Speaker Notes

## Slide 1: Title
[No speaking — wait for introduction]

## Slide 2: Motivation
"Thank you. So let me start with the problem we're trying to solve..."
[Time: 1.5 min]

## Slide 3: Problem Statement
"Specifically, the challenge is..."
→ Transition: "To address this, our key insight is..."
[Time: 1 min]

...
```

**State**: Write `SLIDES_STATE.json` with `phase: 6`.

### Phase 7: PowerPoint Export

Generate an editable PPTX using `python-pptx`:

```bash
python3 -c "import pptx" 2>/dev/null || pip install python-pptx
```

Write `slides/generate_pptx.py` that:

1. Creates a PPTX with correct aspect ratio (16:9 → 13.33" x 7.5"; 4:3 → 10" x 7.5")
2. For each beamer frame:
   - Creates a slide with matching layout
   - Title in venue primary color, bold
   - Bullet points with venue accent color markers
   - Figures embedded as images (from slides/figures/)
   - Speaker notes transferred to PPTX notes field
3. Title slide with special formatting (centered, larger title)
4. Thank You slide with centered text
5. Applies venue color scheme throughout

```bash
cd slides && python3 generate_pptx.py
# Output: slides/presentation.pptx
```

> ⚠️ If `python-pptx` is not installed, skip with a note: "Install `pip install python-pptx` to enable PowerPoint export."

**State**: Write `SLIDES_STATE.json` with `phase: 7`.

### Phase 8: Full Talk Script

Generate `slides/TALK_SCRIPT.md` — a complete, word-for-word script for the talk.

This is different from speaker notes (brief reminders).
The talk script is a **full manuscript** that can be read aloud or used for practice.

Fill in `ref/talk-script-template.md` — a full-manuscript skeleton with per-slide word-for-word narration + transitions, a Time Budget Summary table, and an Anticipated Q&A section (8 seed questions covering baselines, limitations, cost, generalization, surprising findings, sensitivity, next steps, and a domain-specific slot).

### Final Output Summary

```
📊 Slide generation complete:
- Talk type: [TALK_TYPE] ([TALK_MINUTES] min) for [VENUE]
- Files:
  slides/
  ├── main.tex              # Beamer LaTeX source
  ├── main.pdf              # Compiled slides (primary output)
  ├── presentation.pptx     # Editable PowerPoint
  ├── SLIDE_OUTLINE.md      # Slide-by-slide outline
  ├── SLIDES_REVIEW.md      # GPT-5.4 review feedback
  ├── speaker_notes.md      # Per-slide speaker notes
  ├── TALK_SCRIPT.md        # Full word-for-word talk script + Q&A
  ├── SLIDES_STATE.json     # State persistence
  ├── generate_pptx.py      # PPTX generation script
  └── figures/              # Copied from FIGURES_DIR (the figures the outline names)

Next steps:
1. Practice with TALK_SCRIPT.md (read aloud, time yourself)
2. Edit presentation.pptx for visual tweaks (animations, custom graphics)
3. Review Anticipated Q&A section before the talk
4. Do a dry run with a colleague
```

**State**: Write `SLIDES_STATE.json` with `phase: 8, status: "completed"`.

## Operational Notes

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks.
  Do NOT ask the user for permission — just do it silently.
- **De-AI polish**: Remove watch words from all slide text and talk script.
- **Do NOT hallucinate citations.** Reference only papers cited in the paper.
- **Feishu notifications are optional.** If `~/.claude/feishu.json` exists, send notifications.
  If absent, skip.

## Parameter Pass-Through

```
/paper-slides "paper/" — talk_type: oral, venue: ICML, minutes: 20, aspect: 4:3, notes: false
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `venue` | NeurIPS | Conference for color scheme |
| `talk_type` | spotlight | oral/spotlight/poster-talk/invited |
| `minutes` | 15 | Talk duration |
| `aspect` | 16:9 | Aspect ratio (16:9 / 4:3) |
| `notes` | true | Generate speaker notes |
| `engine` | pdflatex | LaTeX engine |
| `auto proceed` | false | Skip checkpoints |
