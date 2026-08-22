---
name: haipipe-display-illustration
description: "AI-illustration renderer of the display family: generate publication-quality academic concept figures (architecture/method/pipeline/taxonomy) through a local Codex app-server bridge that uses Codex native image generation. Use when user says \"画架构图\", \"method illustration\", \"concept figure\", \"AI 配图\", or needs an AI-rendered concept figure."
argument-hint: "[description-or-method-file]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, mcp__codex-image2__generate, mcp__codex-image2__generate_start, mcp__codex-image2__generate_status, mcp__codex__codex, mcp__codex__codex-reply
metadata:
  version: "0.2.2"
  last_updated: "2026-08-05"
  summary: "AI-illustration renderer that uses a Display Intake for approved narrative context and facts."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Paper Illustration Image2

Generate publication-quality paper figures using **Claude as the planner/reviewer**
and a **local Codex app-server MCP bridge** as the raster renderer.

## Output: write into a display unit

Output goes into a `displays/displayNN-<slug>/` unit per the shared contract:
`../ref/display-unit-output-contract.md`.
THIS renderer's row: asset -> `assets/figure.png`; rebuild spec -> `recipe/prompt.md`
(final prompt + bridge job + score) + `recipe/review_log.json`; finalize with
`--display-unit <unit-dir>` (Step 7).

For a new unit, read `intake/manifest.yaml` before planning the prompt.
The manifest supplies approved narrative context and any facts the illustration may state.
This renderer takes no values source for a purely conceptual image.
If the image includes a real N, percentage, coefficient, or other estimate, that fact MUST be a
declared `role: values` intake source; never let image generation invent it.
Legacy `source/` units remain valid only through the compatibility path in the shared contract.

## Fit & Readiness (haipipe)

**Use this for conceptual figures only** — architecture diagrams, method/pipeline
schematics, taxonomy trees.
It produces an **AI raster** image.

**Do NOT use it for data displays.** Tables and result figures (descriptives,
dose-response, subgroup, etc.) must be rendered from real data by a task
(the `Z01`-style parse-then-render path) so they are reproducible and exact.
An
AI raster of a data figure is unverifiable and unfit for a data-driven venue.
For deterministic vector schematics (e.g. a study-flow / CONSORT diagram), prefer
`haipipe-display-diagram` (JSON -> SVG, no external service) or a
task-rendered matplotlib schematic; reach for image2 only when you want a richer
conceptual illustration than a vector spec can express, typically for a
conference/ML venue.

**Runtime dependency:** needs the `codex-image2` MCP bridge (toolkit
`mcp-servers/codex-image2/`, install per its README) plus the Codex desktop app
signed in and the `codex` CLI on PATH.
If `mcp__codex-image2__*` tools are not
present, the bridge is not registered in this session — report that honestly
rather than falling back to a shell/Python bitmap.

## Constants

- **RENDERER = `codex-image2`** — Native image generation bridge exposed through local Codex app-server
- **OPTIONAL_TEXT_CRITIC = `mcp__codex__codex`** — Optional text-only second opinion for layout/style checks
- **MAX_ITERATIONS = 5** — Maximum refinement rounds
- **TARGET_SCORE = 9** — Minimum acceptable score (1-10)
- **OUTPUT_DIR** — for a paper: the display unit `displays/displayNN-slug/` (asset -> `assets/figure.png`, iterations + receipts -> `recipe/`).
  Only with no paper: the flat fallback `figures/ai_generated/`.
- **TEXT_LANGUAGE = `English`** — Default figure text language unless the user requests otherwise
- **NATIVE_IMAGE_REQUIREMENT = `strict`** — Accept only native `imageGeneration` output; reject shell/Python fallbacks
- **CANONICAL_HELPER = `python3 "${CLAUDE_SKILL_DIR:-.}/scripts/paper_illustration_image2.py"`** — Preflight, finalize (`--display-unit`), verify, repair

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

Aim for the balance point: neither overly conservative nor flashy.

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

**Not for:** photo-realistic scenes, or any display better served by a sibling renderer — see the sibling-routing table in `../ref/display-unit-output-contract.md`.

## Workflow: MUST EXECUTE ALL STEPS

### Step 0: Pre-flight Check

Render this checklist explicitly before starting:

```text
📋 paper-illustration-image2 integration checklist:
   [ ] 0. Resolve/scaffold the display unit (see the contract): displays/displayNN-slug/
   [ ] 1. Read intake/manifest.yaml and confirm all facts in the prompt are declared there
   [ ] 2. preflight --workspace <paper-root> --json-out displays/displayNN-slug/recipe/preflight.json
   [ ] 3. Confirm preflight JSON says ok=true before rendering
   [ ] 4. Render via mcp__codex-image2__generate_start + generate_status
   [ ] 5. Finalize into the unit: finalize --workspace <paper-root> --display-unit displays/displayNN-slug --best-image <best_png> (Step 7)
   [ ] 6. Verify: verify --workspace <paper-root> --display-unit displays/displayNN-slug
```

1. Resolve the target display unit (`displays/displayNN-slug/`); scaffold it via
   `Skill("haipipe-paper", "display scaffold ...")` if it does not exist.
   Only when
   there is no paper, fall back to creating `figures/ai_generated/`.
2. Confirm the request is suitable for a raster illustration:
   - architecture diagram
   - conceptual method figure
   - workflow illustration
3. Prefer **English figure text** unless the user asked otherwise.
4. Confirm the Intake context is complete, then run preflight (receipt into the unit's `recipe/`):

```bash
python3 "${CLAUDE_SKILL_DIR:-.}/scripts/paper_illustration_image2.py" preflight \
  --workspace <paper-root> \
  --json-out displays/displayNN-slug/recipe/preflight.json
```

5. If preflight is not `ok=true`, stop and say so clearly.

## Step 1: Claude Plans the Figure

Turn the user request into a **fully specified image prompt**.
Include:

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

This step is required.
Before rendering, refine the prompt into a concrete
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

This step is also required.
Check the prompt against the intended paper style
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
- `outputPath`: `figures/ai_generated/figure_vN.png`. NOTE: the bridge HARD-LOCKS output under `figures/ai_generated/`; it rejects any path outside it (so you cannot render straight into the unit).
  Iterations render here as scratch; `finalize --display-unit` then promotes the accepted one to `displays/displayNN-slug/assets/figure.png` and writes review provenance to `recipe/`.
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
`../ref/display-unit-output-contract.md`). Pass
`--display-unit <displays/displayNN-slug>` so the helper writes
`assets/figure.png` + `float.tex` (only from the caller-approved caption + label + placement, never
invented or changed) + `recipe/review_log.json`,
then compile `preview.pdf` from the paper root.

```bash
# Paper target — write into the display unit (DEFAULT for a paper):
python3 "${CLAUDE_SKILL_DIR:-.}/scripts/paper_illustration_image2.py" finalize \
  --workspace <paper-root> \
  --display-unit <paper-root>/displays/displayNN-slug \
  --best-image <paper-root>/figures/ai_generated/figure_vN.png \
  --caption "Paper-ready caption." --label "fig:slug" --placement "t" \
  --score 9 --review-summary "Accepted after strict review."

# also drop the rebuild spec the helper does not author:
#   displays/displayNN-slug/recipe/prompt.md  (final prompt + bridge job + score)

# compile the unit preview from the paper ROOT so displays/ paths resolve:
pdflatex -interaction=nonstopmode -output-directory displays/displayNN-slug \
  displays/displayNN-slug/preview.tex

python3 "${CLAUDE_SKILL_DIR:-.}/scripts/paper_illustration_image2.py" verify \
  --workspace <paper-root> --display-unit <paper-root>/displays/displayNN-slug \
  --json-out <paper-root>/displays/displayNN-slug/recipe/verify.json
```

Fallback (NO paper / scratch only): omit `--display-unit`; the helper writes the
flat `figures/ai_generated/{figure_final.png,latex_include.tex,review_log.json}`.

The unit's `float.tex` is `\input` by `0-lifecycle/4-display/4-display.tex`, so a
correctly filed unit appears in the combined gallery automatically.

## Repair Path

If rendering succeeded but final artifacts were skipped, repair the integration
explicitly.
For a paper, pass `--display-unit` so repair lands in the unit (an
existing hand-edited `float.tex` is preserved, not clobbered):

```bash
python3 "${CLAUDE_SKILL_DIR:-.}/scripts/paper_illustration_image2.py" finalize \
  --workspace <paper-root> --display-unit <paper-root>/displays/displayNN-slug \
  --best-image <paper-root>/displays/displayNN-slug/assets/figure.png \
  --caption "..." --label "fig:slug" --placement "t"

python3 "${CLAUDE_SKILL_DIR:-.}/scripts/paper_illustration_image2.py" verify \
  --workspace <paper-root> --display-unit <paper-root>/displays/displayNN-slug
```

(No-paper fallback: omit `--display-unit` to repair into flat `figures/ai_generated/`.)

## Output Structure

The display unit layout (asset -> `assets/figure.png`, rebuild spec -> `recipe/prompt.md`
+ `recipe/review_log.json` + `recipe/verify.json`) and the no-paper flat fallback are
the shared contract: `../ref/display-unit-output-contract.md`.
