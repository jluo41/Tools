---
name: haipipe-display-illustration
description: "AI-illustration renderer of the display family: generate publication-quality academic concept figures (architecture/method/pipeline/taxonomy) through a local Codex app-server bridge that uses Codex native image generation. Use when user says \"画架构图\", \"method illustration\", \"concept figure\", \"AI 配图\", or needs an AI-rendered concept figure."
argument-hint: "[description-or-method-file]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, mcp__codex-image2__generate, mcp__codex-image2__generate_start, mcp__codex-image2__generate_status, mcp__codex__codex, mcp__codex__codex-reply
metadata:
  version: "0.2.2"
  last_updated: "2026-08-05"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Paper Illustration Image2

Generate publication-quality paper figures using **Claude as the planner/reviewer**
and a **local Codex app-server MCP bridge** as the raster renderer.

## Output: write into a display unit

The caller supplies the unit path per the shared contract:
`../ref/display-unit-output-contract.md`. For a Page DISPLAY Result, this is
`<page>/results/<re-run>/payload/<unit>/`; View and other callers supply their own
path. The bridge renders scratch candidates under `<work-root>/figures/ai_generated/`;
only a caller-approved candidate is finalized into the supplied unit. This
renderer never chooses the unit destination.

THIS renderer's row: asset -> `assets/figure.png`; rebuild spec -> `recipe/prompt.md`
(final prompt + bridge job + score) + `recipe/review_log.json`.

One invocation that produces one bounded illustration unit may be one Run in the parent Workflow.
Image generation, review rounds, retries, and finalization are internal Steps; the caller owns
candidate selection, promotion, and any `accepted:` decision.

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
- **TARGET_SCORE = 9** — Internal refinement target (1-10); never selects, promotes, or accepts an image
- **OUTPUT_DIR** — final asset and recipe go to the caller-supplied unit; the bridge's locked scratch candidates stay under `<work-root>/figures/ai_generated/`.
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

## Procedure: MUST EXECUTE ALL STEPS

A caller-directed invocation that produces one bounded display unit is one Run in its parent's
Workflow. Pre-flight, planning, image generation, candidate review, finalization, and verification
are Steps inside that Run; retries do not create new Runs.

### Step 0: Pre-flight Check

Render this checklist explicitly before starting:

```text
📋 paper-illustration-image2 integration checklist:
   [ ] 0. Resolve the caller-supplied display unit: <unit-dir>
   [ ] 1. Read intake/manifest.yaml and confirm all facts in the prompt are declared there
   [ ] 2. preflight --workspace <work-root> --json-out <unit-dir>/recipe/preflight.json
   [ ] 3. Confirm preflight JSON says ok=true before rendering
   [ ] 4. Render via mcp__codex-image2__generate_start + generate_status
   [ ] 5. After caller approval, finalize into the unit: finalize --workspace <work-root> --display-unit <unit-dir> --best-image <best_png> (Step 7)
   [ ] 6. Verify: verify --workspace <work-root> --display-unit <unit-dir>
```

1. Use the unit path supplied by the Page, View, Paper, or other caller. If the
   unit does not exist, return the missing path so its owner can create it; do
   not create a Paper-specific or parallel display folder.
2. Confirm the request is suitable for a raster illustration:
   - architecture diagram
   - conceptual method figure
   - workflow illustration
3. Prefer **English figure text** unless the user asked otherwise.
4. Confirm the Intake context is complete, then run preflight (receipt into the unit's `recipe/`):

```bash
python3 "${CLAUDE_SKILL_DIR:-.}/scripts/paper_illustration_image2.py" preflight \
  --workspace <work-root> \
  --json-out <unit-dir>/recipe/preflight.json
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
- `cwd`: the caller-supplied workspace root
- `outputPath`: `figures/ai_generated/figure_vN.png`. The bridge locks output under this scratch folder; it rejects paths outside it. Iterations stay here until the caller approves one, then `finalize --display-unit <unit-dir>` copies it into the unit and writes review provenance under `recipe/`.
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

Record an internal 1-10 quality score. It helps prioritize revisions and never
stands in for caller review or promotion.

## Step 6: Refine if Needed

If score < 9, write a targeted refinement prompt and repeat Step 4:

- say exactly what was wrong
- say what to preserve
- regenerate to `figure_v2.png`, `figure_v3.png`, etc.

Keep refinement feedback concrete:

- `Increase spacing between genome scan and scoring modules`
- `Make the off-target branch thinner and secondary`
- `Use cleaner English labels: "Candidate sgRNA library", not "sgRNA library 23 bp"`

The score is advisory. When the candidate is ready for a decision, show the
current image and review notes to the caller. Do not promote it until the caller
explicitly approves that candidate.

## Step 7: Promote after caller approval, then verify

After the caller explicitly approves promotion, finalize INTO THE DISPLAY UNIT
at the caller-supplied path (see `../ref/display-unit-output-contract.md`). Pass
`--display-unit <unit-dir>` so the helper writes
`assets/figure.png` + `float.tex` (only from the caller-approved caption + label + placement, never
invented or changed) + `recipe/review_log.json`,
then compile `preview.pdf` from the caller's asset-reference base.

```bash
# Write into the caller-supplied display unit:
python3 <skill-dir>/scripts/paper_illustration_image2.py finalize \
  --workspace <work-root> \
  --display-unit <unit-dir> \
  --best-image <candidate-image-path> \
  --caption "Paper-ready caption." --label "fig:slug" --placement "t" \
  --score <internal-score> --review-summary "Caller approved candidate <candidate-id> for promotion."

# also drop the rebuild spec the helper does not author:
#   <unit-dir>/recipe/prompt.md  (final prompt + bridge job + internal score)

# compile from the caller's asset-reference base; write preview.pdf into the unit:
WORK_ROOT=/path/to/caller-asset-reference-base
UNIT_DIR=/path/to/caller-supplied-unit
(cd "$WORK_ROOT" && pdflatex -output-directory "$UNIT_DIR" "$UNIT_DIR/preview.tex")

python3 <skill-dir>/scripts/paper_illustration_image2.py verify \
  --workspace <work-root> --display-unit <unit-dir> \
  --json-out <unit-dir>/recipe/verify.json
```

Standalone scratch use is outside a HAI-Pipe display unit. If explicitly
requested, omit `--display-unit`; the flat output remains a scratch candidate
and carries no Page Result, caller promotion, or accepted decision.

The caller owns the Page or Paper projection. After promotion, return the unit
path, the compiled preview, and review notes. The caller records any `accepted:`
decision; the renderer never ticks it.

## Repair Path

If rendering succeeded but final artifacts were skipped, repair the integration
explicitly.
Pass `--display-unit` so repair lands in the caller's unit (an existing
hand-edited `float.tex` is preserved, not clobbered):

```bash
python3 "${CLAUDE_SKILL_DIR:-.}/scripts/paper_illustration_image2.py" finalize \
  --workspace <work-root> --display-unit <unit-dir> \
  --best-image <candidate-image-path> \
  --caption "..." --label "fig:slug" --placement "t"

python3 "${CLAUDE_SKILL_DIR:-.}/scripts/paper_illustration_image2.py" verify \
  --workspace <work-root> --display-unit <unit-dir>
```

If this is an explicitly standalone scratch request, omit `--display-unit`; that
output remains outside Page, View, and Paper acceptance.

## Output Structure

The display unit layout (asset -> `assets/figure.png`, rebuild spec -> `recipe/prompt.md`
+ `recipe/review_log.json` + `recipe/verify.json`) is the shared contract:
`../ref/display-unit-output-contract.md`.
