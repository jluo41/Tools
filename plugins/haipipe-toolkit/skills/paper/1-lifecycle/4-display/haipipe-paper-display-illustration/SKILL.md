---
name: haipipe-paper-display-illustration
description: "Default AI-illustration renderer of the display family: generate publication-quality academic concept figures (architecture/method/pipeline/taxonomy) through a local Codex app-server bridge that uses Codex native image generation. Use when user says \"画架构图\", \"method illustration\", \"concept figure\", \"AI 配图\", or needs an AI-rendered concept figure. If the codex-image2 bridge is unavailable, fall back to haipipe-paper-display-illustration-gemini (Gemini backend)."
argument-hint: "[description-or-method-file]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, mcp__codex-image2__generate, mcp__codex-image2__generate_start, mcp__codex-image2__generate_status, mcp__codex__codex, mcp__codex__codex-reply
metadata:
  version: "1.3.0"
  last_updated: "2026-06-22"
  summary: "Default AI-illustration renderer of the display family (Codex native image generation); Gemini backend lives in -gemini."
  changelog:
    - "1.3.0 (2026-06-22): promoted to the DEFAULT illustration renderer and renamed haipipe-paper-display-illustration (the Codex bridge is the maintained path); the Gemini backend moved to haipipe-paper-display-illustration-gemini as the named fallback."
    - "1.2.0 (2026-06-22): completed the migration -- vendored the canonical helper scripts/paper_illustration_image2.py (the 1.1.0 rename dropped it, leaving the $IMAGE2_HELPER reference dangling) and the codex-image2 MCP bridge (toolkit mcp-servers/codex-image2/). Added the Fit & Readiness section."
    - "1.1.0 (2026-06-05): renamed from paper-illustration-image2 to haipipe-paper-illustration-image2 (haipipe-paper-* name unification)."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

# Paper Illustration Image2

Generate publication-quality paper figures using **Claude as the planner/reviewer**
and a **local Codex app-server MCP bridge** as the raster renderer.

## Output: write into a display unit (not flat figures/)

When the target is a paper (a folder with `0-displays/`), the output goes into a
`0-displays/displayNN-<slug>/` unit, NOT `figures/ai_generated/`. Follow the
shared contract: `../haipipe-paper-display/ref/display-unit-output-contract.md`
(resolve/scaffold the unit, write `assets/` + `source/` + `float.tex`, compile
`preview.pdf`, set README status). For THIS renderer: asset ->
`assets/figure.png`; rebuild spec -> `source/prompt.md` (final prompt + bridge
job + score) + `source/review_log.json`. Finalize with `--display-unit <unit-dir>`
(Step 7). `figures/ai_generated/` is a fallback only when there is no paper.

## Fit & Readiness (haipipe)

**Use this for conceptual figures only** — architecture diagrams, method/pipeline
schematics, taxonomy trees. It produces an **AI raster** image.

**Do NOT use it for data displays.** Tables and result figures (descriptives,
dose-response, subgroup, etc.) must be rendered from real data by a task
(the `Z01`-style parse-then-render path) so they are reproducible and exact. An
AI raster of a data figure is unverifiable and unfit for a data-driven venue.
For deterministic vector schematics (e.g. a study-flow / CONSORT diagram), prefer
`haipipe-paper-display-diagram` (JSON -> SVG, no external service) or a
task-rendered matplotlib schematic; reach for image2 only when you want a richer
conceptual illustration than a vector spec can express, typically for a
conference/ML venue.

**Runtime dependency:** needs the `codex-image2` MCP bridge (toolkit
`mcp-servers/codex-image2/`, install per its README) plus the Codex desktop app
signed in and the `codex` CLI on PATH. If `mcp__codex-image2__*` tools are not
present, the bridge is not registered in this session — report that honestly
rather than falling back to a shell/Python bitmap.

## Core Design Philosophy

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                    MULTI-STAGE ITERATIVE WORKFLOW                        │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   User Request                                                           │
│       │                                                                  │
│       ▼                                                                  │
│   ┌─────────────┐                                                        │
│   │   Claude    │ ◄─── Step 1: Parse request, create initial prompt     │
│   │  (Planner)  │      - Extract components, labels, and data flow       │
│   │             │      - Write a paper-ready figure brief                │
│   └──────┬──────┘                                                        │
│          │                                                               │
│          ▼                                                               │
│   ┌─────────────┐                                                        │
│   │Claude/Codex │ ◄─── Step 2: Optimize layout description               │
│   │   Layout    │      - Refine component positioning                    │
│   │   Review    │      - Optimize spacing and grouping                   │
│   └──────┬──────┘                                                        │
│          │                                                               │
│          ▼                                                               │
│   ┌─────────────┐                                                        │
│   │Claude/Codex │ ◄─── Step 3: CVPR/NeurIPS style verification           │
│   │   Style     │      - Check palette, arrows, and label standards      │
│   │   Check     │      - Tighten the prompt before rendering             │
│   └──────┬──────┘                                                        │
│          │                                                               │
│          ▼                                                               │
│   ┌─────────────┐                                                        │
│   │ codex-image2│ ◄─── Step 4: Native image generation via bridge        │
│   │ MCP bridge  │      - Call generate_start / generate_status           │
│   │ + app-server│      - Accept only native imageGeneration output       │
│   └──────┬──────┘                                                        │
│          │                                                               │
│          ▼                                                               │
│   ┌─────────────┐                                                        │
│   │   Claude    │ ◄─── Step 5: STRICT visual review + SCORE (1-10)      │
│   │  (Reviewer) │      - Verify logic, labels, arrows, and aesthetics    │
│   │   STRICT!   │      - Reject unclear or non-paper-ready figures       │
│   └──────┬──────┘                                                        │
│          │                                                               │
│          ▼                                                               │
│   Score ≥ 9? ──YES──► Accept & Output                                    │
│          │                                                               │
│          NO                                                              │
│          │                                                               │
│          ▼                                                               │
│   Generate SPECIFIC improvement feedback ──► Loop back to Step 2        │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Constants

- **RENDERER = `codex-image2`** — Native image generation bridge exposed through local Codex app-server
- **OPTIONAL_TEXT_CRITIC = `mcp__codex__codex`** — Optional text-only second opinion for layout/style checks
- **MAX_ITERATIONS = 5** — Maximum refinement rounds
- **TARGET_SCORE = 9** — Minimum acceptable score (1-10)
- **OUTPUT_DIR** — for a paper: the display unit `0-displays/displayNN-slug/` (asset -> `assets/figure.png`, iterations + receipts -> `source/`). Only with no paper: the flat fallback `figures/ai_generated/`.
- **TEXT_LANGUAGE = `English`** — Default figure text language unless the user requests otherwise
- **NATIVE_IMAGE_REQUIREMENT = `strict`** — Accept only native `imageGeneration` output; reject shell/Python fallbacks
- **CANONICAL_HELPER = `python3 "$CLAUDE_SKILL_DIR/scripts/paper_illustration_image2.py"`** — Preflight, finalize (`--display-unit`), verify, repair

## CVPR/ICLR/NeurIPS Top-Tier Conference Style Guide

**What "CVPR Style" Actually Means:**

### Visual Standards
- **Clean white background** — No decorative patterns or gradients unless extremely subtle
- **Sans-serif fonts** — Arial, Helvetica, or similarly clean paper-friendly typography
- **Subtle color palette** — Use 3-5 coordinated colors, not rainbow colors
- **Print-friendly** — Must remain understandable in grayscale
- **Professional borders** — Thin to medium, clean, and consistent

### Layout Standards
- **Horizontal flow** — Left-to-right is the default for pipelines
- **Clear grouping** — Use spacing or subtle grouping boxes for related modules
- **Consistent sizing** — Similar components should have similar sizes
- **Balanced whitespace** — Avoid both cramped and overly sparse layouts

### Arrow Standards (MOST CRITICAL)
- **Thick strokes** — Arrows must remain visible after paper scaling
- **Clear arrowheads** — Large, unmistakable arrowheads
- **Dark colors** — Prefer black or dark gray arrows
- **Labeled** — Important arrows should show what flows through them
- **No crossings** — Reorganize the figure to avoid crossings where possible
- **CORRECT DIRECTION** — Arrows must point to the right target

### Visual Appeal (Academic Professional Style)

**目标：既不保守也不花哨，找到平衡点**

#### ✅ Should have
- **Subtle gradients** — Gentle same-family gradients are acceptable
- **Rounded corners** — Modern but restrained rounded blocks
- **Clear hierarchy** — Main modules larger, secondary modules smaller
- **Consistent color coding** — Stable mapping between module types and colors
- **Professional typography** — Clean labels with readable size hierarchy

#### ❌ Avoid
- ❌ Rainbow gradients
- ❌ Heavy drop shadows
- ❌ 3D perspective effects
- ❌ Glowing effects
- ❌ Decorative clip-art icons
- ❌ Slide-deck styling that feels flashy rather than paper-ready

#### ✓ Ideal effect
- Looks intentional, professional, and immediately readable
- Has moderate visual appeal without becoming decorative
- Feels appropriate for a top-tier conference paper figure
- Survives PDF scaling and grayscale printing

### What to AVOID (CRITICAL)
- ❌ Thin, hairline arrows
- ❌ Unlabeled or ambiguous connections
- ❌ Tiny unreadable text
- ❌ Flat, boring box soup with no hierarchy
- ❌ Over-decorated figures with shadows/glows/icons
- ❌ Wrong arrow directions

## Scope

| Figure Type | Quality | Examples |
|-------------|---------|----------|
| **Architecture diagrams** | Excellent | Model architecture, pipeline, encoder-decoder |
| **Method illustrations** | Excellent | Conceptual diagrams, algorithm flowcharts |
| **Conceptual figures** | Good | Comparison diagrams, taxonomy trees |

**Not for:** Statistical plots (use `/haipipe-paper-display-figure`), deterministic vector topology figures (prefer `/haipipe-paper-display-diagram`), photo-realistic scenes

## Workflow: MUST EXECUTE ALL STEPS

### Step 0: Pre-flight Check

Render this checklist explicitly before starting:

```text
📋 paper-illustration-image2 integration checklist:
   [ ] 0. Resolve/scaffold the display unit (see the contract): 0-displays/displayNN-slug/
   [ ] 1. preflight --workspace <paper-root> --json-out 0-displays/displayNN-slug/source/preflight.json
   [ ] 2. Confirm preflight JSON says ok=true before rendering
   [ ] 3. Render via mcp__codex-image2__generate_start + generate_status
   [ ] 4. Finalize into the unit: finalize --workspace <paper-root> --display-unit 0-displays/displayNN-slug --best-image <best_png> (Step 7)
   [ ] 5. Verify: verify --workspace <paper-root> --display-unit 0-displays/displayNN-slug
```

1. Resolve the target display unit (`0-displays/displayNN-slug/`); scaffold it via
   `Skill("haipipe-paper-display", "scaffold ...")` if it does not exist. Only when
   there is no paper, fall back to creating `figures/ai_generated/`.
2. Confirm the request is suitable for a raster illustration:
   - architecture diagram
   - conceptual method figure
   - workflow illustration
3. Prefer **English figure text** unless the user asked otherwise.
4. Run preflight (receipt into the unit's `source/`):

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/paper_illustration_image2.py" preflight \
  --workspace <paper-root> \
  --json-out 0-displays/displayNN-slug/source/preflight.json
```

5. If preflight is not `ok=true`, stop and say so clearly.

## Step 1: Claude Plans the Figure

Turn the user request into a **fully specified image prompt**. Include:

- figure type
- exact modules / stages
- flow direction
- labels to show
- data-flow arrows
- style constraints
- what to avoid

When the input is a method note or a paper section, summarize it first into a
clean figure brief before writing the final image prompt.

## Step 2: Layout Optimization

This step is required. Before rendering, refine the prompt into a concrete
layout plan:

- exact module order
- spacing and grouping
- relative module prominence
- arrow routing and likely collision points

If `mcp__codex__codex` is available, you may ask it for a short second-opinion
layout critique here, but Claude should still complete this step even without
Codex.

Use Codex layout critique for:

- missing components
- confusing layout
- weak flow hierarchy
- likely arrow-direction ambiguity or clutter

## Step 3: Style Verification

This step is also required. Check the prompt against the intended paper style
before rendering:

- palette is restrained and academic
- arrows are thick, dark, and readable
- labels are concise and in English unless requested otherwise
- the figure will read clearly in grayscale / print
- no glow, rainbow gradient, or slide-deck decoration slips in

If `mcp__codex__codex` is available, you may ask it for a short text-only
style audit, but do not block on it.

## Step 4: Generate Through the Bridge

Call `mcp__codex-image2__generate_start` with:

- `prompt`: the final image prompt
- `cwd`: the paper workspace (paper root)
- `outputPath`: `figures/ai_generated/figure_vN.png`. NOTE: the bridge HARD-LOCKS output under `figures/ai_generated/`; it rejects any path outside it (so you cannot render straight into the unit). Iterations render here as scratch; `finalize --display-unit` then promotes the accepted one to `0-displays/displayNN-slug/assets/figure.png` and you copy it to `source/` for provenance.
- `system`: a short instruction like `Academic paper figure. Prefer crisp English labels.`
- `timeoutSeconds`: a bounded render timeout such as `180`

Then call `mcp__codex-image2__generate_status` with bounded waits until:

- `done=true` and `status=completed`, or
- `done=true` and `status=failed`

If generation fails, report the bridge error directly instead of hiding it.

## Step 5: Review the Output

Review the generated image with a strict checklist:

- are all major components present?
- is the logical flow obvious?
- are labels readable?
- do arrows point the right way?
- does the figure look paper-ready rather than like a slide?

Score it from 1-10.

## Step 6: Refine if Needed

If score < 9, write a targeted refinement prompt:

- say exactly what was wrong
- say what to preserve
- regenerate to `figure_v2.png`, `figure_v3.png`, etc.

Keep refinement feedback concrete:

- `Increase spacing between genome scan and scoring modules`
- `Make the off-target branch thinner and secondary`
- `Use cleaner English labels: "Candidate sgRNA library", not "sgRNA library 23 bp"`

## Step 7: Finalize And Verify

When accepted, finalize INTO THE DISPLAY UNIT (the contract path; see the "Output:
write into a display unit" section above and
`../haipipe-paper-display/ref/display-unit-output-contract.md`). Pass
`--display-unit <0-displays/displayNN-slug>` so the helper writes
`assets/figure.png` + `float.tex` (with your caption + label) + `source/review_log.json`,
then compile `preview.pdf` from the paper root.

```bash
# Paper target — write into the display unit (DEFAULT for a paper):
python3 "$CLAUDE_SKILL_DIR/scripts/paper_illustration_image2.py" finalize \
  --workspace <paper-root> \
  --display-unit <paper-root>/0-displays/displayNN-slug \
  --best-image <paper-root>/0-displays/displayNN-slug/figure_vN.png \
  --caption "Paper-ready caption." --label "fig:slug" \
  --score 9 --review-summary "Accepted after strict review."

# also drop the rebuild spec the helper does not author:
#   0-displays/displayNN-slug/source/prompt.md  (final prompt + bridge job + score)

# compile the unit preview from the paper ROOT so 0-displays/ paths resolve:
pdflatex -interaction=nonstopmode -output-directory 0-displays/displayNN-slug \
  0-displays/displayNN-slug/preview.tex

python3 "$CLAUDE_SKILL_DIR/scripts/paper_illustration_image2.py" verify \
  --workspace <paper-root> --display-unit <paper-root>/0-displays/displayNN-slug \
  --json-out <paper-root>/0-displays/displayNN-slug/source/verify.json
```

Fallback (NO paper / scratch only): omit `--display-unit`; the helper writes the
flat `figures/ai_generated/{figure_final.png,latex_include.tex,review_log.json}`.

The unit's `float.tex` is `\input` by `0-lifecycle/4-display/4-display.tex`, so a
correctly filed unit appears in the combined gallery automatically.

## Key Rules

1. Never skip Step 2 or Step 3; layout and style checks are required.
2. Never skip the final visual review.
3. Never accept a figure that is logically wrong just because it looks attractive.
4. Use the `codex-image2` bridge only for **native image generation**.
5. If the bridge says native image generation is unavailable, surface that honestly.
6. Reject any shell/Python/manual bitmap fallback masquerading as image generation.
7. Keep figure text in English unless the user requested another language.
8. Prefer 1-3 strong refinement rounds over many shallow ones.
9. Use specific, actionable refinement feedback instead of vague comments.
10. Review arrow direction, label clarity, and visual hierarchy every round.
11. Accept only figures that look paper-ready, not slide-ready.
12. Always use `"$CLAUDE_SKILL_DIR/scripts/paper_illustration_image2.py" finalize --display-unit <unit>` to emit the final artifacts into the display unit.
13. Always use `"$CLAUDE_SKILL_DIR/scripts/paper_illustration_image2.py" verify --display-unit <unit>` before claiming success.

## Repair Path

If rendering succeeded but final artifacts were skipped, repair the integration
explicitly. For a paper, pass `--display-unit` so repair lands in the unit (an
existing hand-edited `float.tex` is preserved, not clobbered):

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/paper_illustration_image2.py" finalize \
  --workspace <paper-root> --display-unit <paper-root>/0-displays/displayNN-slug \
  --best-image <paper-root>/0-displays/displayNN-slug/assets/figure.png \
  --caption "..." --label "fig:slug"

python3 "$CLAUDE_SKILL_DIR/scripts/paper_illustration_image2.py" verify \
  --workspace <paper-root> --display-unit <paper-root>/0-displays/displayNN-slug
```

(No-paper fallback: omit `--display-unit` to repair into flat `figures/ai_generated/`.)

## Output Structure

Paper target (DEFAULT) — a display unit:

```text
0-displays/displayNN-slug/
├── README.md              # claim / kind / caption-job / status: rendered
├── float.tex              # caption + \label + \includegraphics{assets/figure.png}
├── preview.tex            # standalone wrapper
├── preview.pdf            # compiled from the paper root
├── assets/figure.png      # accepted image (score >= 9)
└── source/
    ├── prompt.md          # rebuild spec: final prompt + bridge job + score
    ├── review_log.json    # review notes / refinement history
    └── verify.json        # helper verification diagnostic
```

Fallback (no paper / scratch) — flat:

```text
figures/ai_generated/
├── figure_v1.png … figure_final.png   # iterations + accepted copy
├── latex_include.tex                  # LaTeX snippet
├── review_log.json
└── verify.json
```

## Model Summary

| Stage | Agent / Tool | Purpose |
|-------|--------------|---------|
| Step 0 | `python3 "$CLAUDE_SKILL_DIR/scripts/paper_illustration_image2.py" preflight` | Observable activation predicate and preflight receipt |
| Step 1 | Claude | Parse request and create the initial figure prompt |
| Step 2 | Claude (+ optional Codex critique) | Refine layout, grouping, spacing, and arrow routing |
| Step 3 | Claude (+ optional Codex critique) | Verify academic visual style before rendering |
| Step 4 | `mcp__codex-image2__generate_start` + `generate_status` | Native raster image generation through Codex app-server |
| Step 5 | Claude | Strict visual review and scoring |
| Step 7 | `python3 "$CLAUDE_SKILL_DIR/scripts/paper_illustration_image2.py" finalize --display-unit` + `verify` | Emit canonical artifacts into the display unit + verification receipt |
