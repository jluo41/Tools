---
name: haipipe-paper-display
description: "Plan, materialize (via task/probe), scaffold, build, audit, and insert paper display items: figures, tables, diagrams, and preview PDFs under 0-displays/. Displays are RENDERED by a paper-display task from evidence, never hand-authored in float.tex. Use for display-unit README files, ready-to-input figure/table blocks, captions, labels, standalone previews, or figure/table story-evidence contracts."
argument-hint: "[paper-dir] [--plan|--scaffold|--framework|--materialize|--build|--audit|--insert] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.6.2"
  last_updated: "2026-07-03"
  summary: "Display stage orchestrator. Plans the display set, materializes via tasks, compiles gallery PDF, and gates exit. User invokes display, not phases."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-display
======================================

Stage orchestrator for the **display** stage (stage 4, venue-ALIGNED). The user invokes this skill; it drives the phases internally.

It answers one question:

```text
What evidence artifacts does the reader need to see, and are they ready?
```

Display items are figures, tables, diagrams, and other manuscript-visible objects that carry evidence and story. A display item is not just a file. It has a job:

```
What claim does this display support?
Where does the evidence come from?
What should the reader learn in five seconds?
Where does it appear in the paper?
Is it ready to input into the manuscript?
```

Read first: `../../PHILOSOPHY.md`, `../../wiki/04-lifecycle-map.md`, `../README-display.md`.

**Done-gate: `CHECKLIST.md`** (this skill's folder) is the canonical, scannable done-gate for this stage and the home of the gallery requirements (narrative order, section + named subsection per display, venue display set, Parking section, user comment policy, elbow/icon vector rules). The paper's `4-display.tex` points here instead of restating them. Walk it before asking for the stage gate.

## Artifact Spec

**Files produced:**
- `0-lifecycle/4-display/4-display.tex` -- gallery stage document (compiles to PDF)
- `0-lifecycle/4-display/4-display.pdf` -- compiled gallery (the ONLY lifecycle stage with .tex + PDF)
- `0-lifecycle/4-display/_LOG_4-display.md` -- phase progress journal (per `../../wiki/02-comment-lifecycle.md`)
- `0-lifecycle/4-display/_PROBE/` -- probe plans spawned by display needs
- `0-displays/displayNN-<slug>/` -- per-unit folders, each containing:
  - `README.md` -- claim, source, placement, status
  - `float.tex` -- LaTeX figure/table block ready for \input
  - `preview.tex` + `preview.pdf` -- standalone review artifact
  - `assets/` -- rendered visual assets (figure.pdf, table-body.tex)
  - `source/` -- source data, metrics.json

**Content structure (4-display.tex):**
- \input{} lines for each display unit's float.tex (gallery of all figures and tables)
- `%% {USER}: ...` author comments on displays (verbatim, kept across iterations)
- Parked section for kept-but-unused display units

**Done-criteria:**
- [ ] All display units rendered (status >= rendered)
- [ ] Gallery PDF compiles from paper root
- [ ] All displays referenced in narrative (_DISPLAY_3-narrative.md)
- [ ] USER comments in 4-display.tex addressed or acknowledged
- [ ] CHECKLIST.md walked and all items pass
- [ ] No orphan displays (every unit has a claim, source, section)

## Phase Orchestration

When the user invokes `/haipipe-paper display`, this skill drives the phases in order. The user does not call phase skills directly.

```
display invoked
  |
  v
DRAFT ----> plan the display set (0-displays/README.md index),
            scaffold display-unit folders, run framework candidate
            rounds for architecture figures, write 4-display.tex
            (internally calls /haipipe-paper-draft with this artifact spec)
  |
  v
PROBE ----> route display units to task-folders for generation
            (/haipipe-task-for-display), materialize assets from
            evidence, compile per-unit preview PDFs
            (internally calls /haipipe-paper-probe-display)
  |
  v
REVISE ---> compile gallery PDF (4-display.pdf), refine captions,
            label consistency, visual quality
            (internally calls /haipipe-paper-revise)
  |
  v
CHECK ----> walk CHECKLIST.md, audit display/story/evidence
            consistency, user confirms -> advance to section-edit
            (internally calls /haipipe-paper-check)
```

Phase visibility per the Phase Transition Contract in `../../wiki/08-stage-gate.md`: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG` + phase-line 🔥 moves); skip a phase only by an explicit logged verdict (`[PROBE] skipped -- <reason>`, phase line shows `--`); CHECK is never implicit -- it opens by presenting the exit-criteria report and the approval ask.

Comment lifecycle per `../../wiki/02-comment-lifecycle.md`: `%% {USER}: ...` comments live in 4-display.tex while active, move to _LOG_4-display.md on resolve, each phase starts clean.

### DRAFT: Plan, Scaffold, and Framework

**Plan.** Create or refresh `0-displays/README.md` from the paper state.

Illuminate first (per `../../wiki/09-stage-illuminate.md`): present the current display set and ask -- which display is the hero figure? Which are main vs supplement? What visual forms (forest plot, panel, flow diagram, table)? Elicit taste before proceeding.

Inputs to read when present:

- `0-lifecycle/2-pitch/2-pitch.md`
- `0-lifecycle/3-narrative/3-narrative.md`
- existing `0-displays/`
- upstream result paths referenced by the user

Output (0-displays/README.md):

```markdown
# Display Index

| ID | Type | Role | Claim | Evidence Source | Section | Status |
|----|------|------|-------|-----------------|---------|--------|
| Fig 1 | hero figure | one-minute story | ... | ... | Introduction | planned |
```

Status vocabulary: `planned` -> `data-ready` -> `rendered` -> `input-ready` -> `inserted` -> `reviewed`.

**Scaffold.** Create a display-unit folder from an index row or user request.

Display-unit folder structure:

```text
0-displays/displayNN-slug/
  README.md
  float.tex
  preview.tex
  assets/.gitkeep
  source/.gitkeep
  versions/.gitkeep
```

One display unit can hold one or many concrete results: a main figure, a table body, appendix variants, robustness previews, and the source needed to rebuild them.

Per-unit interrogation: each display unit is interrogated by an independent subagent for inclusion (keep/merge/move-to-Supplement/cut), form, and claim mapping. Render the verdict in small font in the unit's README.md.

**Framework.** Use when the bottleneck is architecture/Figure 1 planning and you want candidate options before final rendering.

Inputs:
- user request (claim + target section + evidence contract)
- optional `0-displays` row ID and existing candidate text

Outputs:
- `0-displays/displayNN-<slug>/README.md` updated with a clear framework claim role
- candidate pack in `0-displays/displayNN-<slug>/source/framework-candidates.md`
- a selected direction in `0-displays/displayNN-<slug>/source/framework-selection.md`
- `float.tex` still points to a TODO render target (not final art)

Workflow:
1. Clarify what job this figure serves in the one-minute story and which claim it must defend.
2. Offer 3-5 candidate frameworks (ex: pipeline chain, hub-and-spoke, layered stack, audit loop, feedback cycle) with pros/cons and expected reviewer friction.
3. Record the candidates and selection criteria in `source/framework-candidates.md`.
4. After selection, hand over for the final render. **Default render target:** `/haipipe-paper-display-illustration` (the Codex bridge gives the most paper-ready CVPR-style Figure 1). Choose `/haipipe-paper-display-diagram` instead when you need a reproducible, editable vector. Fall back to `/haipipe-paper-display-illustration-gemini` if the Codex bridge is unavailable.

Reference hook: Load `Tools/references/aris/skills/paper-framework-figure-studio-pro/SKILL.md` and follow its candidate-generation loop when generating alternatives and revision passes.

**Render routing** (framework -> final art):

- Conceptual architecture/pipeline with multiple options to choose from: use `framework` first, then hand off to a renderer.
- Settled Figure 1, richest result: `/haipipe-paper-display-illustration` (Codex AI raster).
- Reproducible, editable vector: `/haipipe-paper-display-diagram` (FigureSpec JSON).
- Gemini backend fallback: `/haipipe-paper-display-illustration-gemini`.

### PROBE: Materialize and Build

**Materialize.** Turn a `planned` / `data-ready` display into a real RENDERED asset by actively calling the evidence and render workers. This phase never hand-authors a figure or pastes numbers into `float.tex`.

Routing (use `../../wiki/11-delivery-need.md`):

```text
claim has no confirmed verdict yet     -> /haipipe-probe plan from-need <need>
asset needs rendering from evidence    -> /haipipe-task-for-display <need>
```

`/haipipe-task-for-display` creates or extends a **paper-display task group** folder (e.g. `tasks/Z0N_Display_<topic>/`) and a per-display **task folder** that RENDERS the figure/table from the evidence (a probe verdict, or a parser's `metrics.json`) into:

```text
assets/figure.pdf          (graphical display: forest, dose-response curve, panel)
assets/table-body.tex      (LaTeX-native table body)
source_data.csv            (the exact numbers behind the asset)
metrics.json               (machine-readable summary, for re-derivation)
```

The task renders; the paper then backfills the rendered asset path into the display unit and points `float.tex` at it (`\includegraphics` / `\input`). A display reaches status `rendered` only when its asset exists on disk as a task output, not when numbers are typed into `float.tex`. Prefer reusing an existing display task group (extend it with a new config) over creating a new one.

**Build.** Compile standalone preview PDFs for one display item or all display items with `preview.tex`.

Rules:
- Compile from the paper root so paths match the main paper.
- Use `pdflatex -interaction=nonstopmode`.
- A successful build creates or refreshes `preview.pdf`.
- Do not modify the main paper while building previews.
- Do not treat preview success as proof that the display supports its claim.

### REVISE: Gallery and Captions

Compile the gallery PDF (`4-display.pdf`) from the paper root and refine:

- Caption accuracy: does each caption state the display's job without overclaiming?
- Label consistency: `\label{fig:slug}` / `\label{tab:slug}` matches the display index.
- Visual quality: resolution, axis labels, legend clarity, color accessibility.
- Number synchronization: panel letters, baselines, datasets match across displays and text.

`4-display.pdf` recompiled and current (a stale PDF is a defect; recompile after every edit without being asked). Compile via the paper's `./1-compile.sh`, never per-file `pdflatex`.

### CHECK: Audit and Gate

**Audit.** Check display/story/evidence consistency.

Audit questions:
- Does every `0-displays/README.md` row have a concrete claim and evidence source?
- Does every major display have a unit `README.md`?
- Does `float.tex` exist for each inserted display?
- Does `preview.pdf` compile?
- Does the caption match the actual asset/table body?
- Does the display support the exact claim made in the target section?
- Are numbers, datasets, baselines, panel letters, and labels synchronized?
- Does the display belong in main text or appendix?
- Is any display orphaned: asset exists but no index row, or index row exists but no asset/float?

Per-unit interrogation: each display unit is interrogated by an independent subagent for inclusion (keep/merge/move-to-Supplement/cut), form, and claim mapping. Render the verdict in small font in the unit's README.md.

Route failures:

| Failure | Route |
|---------|-------|
| caption typo, stale label, path issue | REVISE (edit display item) |
| `float.tex` inlines pasted numbers (no rendered asset) | PROBE: materialize (`/haipipe-task-for-display`) |
| missing asset/table body | PROBE: materialize (render via the paper-display task) |
| unsupported claim | upstream: narrative or task/probe |
| wrong figure sequence | upstream: pitch or plan (DRAFT) |
| hero figure does not sell story | upstream: pitch |

**Insert.** Insert a ready display into a section file by adding `\input{0-displays/displayNN-slug/float.tex}`.

Rules:
- Only insert displays with status `input-ready` or better.
- Insert near the paragraph whose claim the display supports.
- Do not duplicate an existing input line.
- After insertion, update `0-displays/README.md` status to `inserted`.

**Gate.** Walk `CHECKLIST.md` (this skill's folder). Present exit criteria per `../../wiki/08-stage-gate.md`. User confirms before advancing.

## Display Unit Templates

Per-unit `README.md`:

```markdown
# displayNN-slug

## Reader Takeaway
What should a reader understand in five seconds?

## Claim Supported
The exact paper claim this display supports.

## Evidence Source
- Source path:
- Producing task/probe/discovery/insight:
- Last checked:

## Placement
- Main or appendix:
- Target section:
- Called by:

## Caption Job
What the caption must explain without overclaiming.

## Fragility
What could make this display stale or misleading?

## Status
planned / data-ready / rendered / input-ready / inserted / reviewed
```

`float.tex` template for figures:

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=0.95\textwidth]{0-displays/displayNN-slug/assets/figure.pdf}
  \caption{TODO: concise caption that states the display's job without overclaiming.}
  \label{fig:slug}
\end{figure}
```

`float.tex` template for tables:

```latex
\begin{table}[t]
  \centering
  \caption{TODO: concise caption that states the table's job without overclaiming.}
  \label{tab:slug}
  \input{0-displays/displayNN-slug/assets/table-body.tex}
\end{table}
```

`preview.tex` template:

```latex
\documentclass{article}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{subcaption}
\usepackage{caption}
\begin{document}
\input{0-displays/displayNN-slug/float.tex}
\end{document}
```

## Location

```
<paper>/
+-- 0-lifecycle/4-display/
|   +-- 4-display.tex       gallery stage document
|   +-- 4-display.pdf       compiled gallery
|   +-- _LOG_4-display.md   phase progress journal
|   +-- _PROBE/             probe plans spawned by display needs
+-- 0-displays/
    +-- README.md            display index
    +-- display01-hero/
    |   +-- README.md
    |   +-- float.tex
    |   +-- preview.tex
    |   +-- preview.pdf
    |   +-- assets/
    |   +-- source/
    |   +-- versions/
    +-- displayNN-<slug>/
```

## Principles

1. **No orphan displays.** Every figure/table must have a claim, source, section, and reader takeaway.
2. **Do not bake captions into image PDFs.** `figure.pdf` is the visual asset; `float.tex` owns caption, label, and `\includegraphics`.
3. **Make display blocks ready to input.** Section files should be able to use: `\input{0-displays/display01-hero/float.tex}`.
4. **Preview separately.** `preview.pdf` is a standalone review artifact built from the same `float.tex`. It lets humans and reviewers inspect the display without compiling the whole paper.
5. **Display is a contract layer.** Figure/table generation skills may create assets, but this skill records why each display exists and whether it still supports the story.
6. **A display is materialized by a task, never hand-authored.** The asset (`assets/figure.pdf` for a figure, `assets/table-body.tex` for a table) is RENDERED by a paper-display task from evidence (a probe verdict, a parser's `metrics.json`, a result table), and `float.tex` only references it via `\includegraphics` or `\input`. Numbers typed directly into `float.tex` are a placeholder, not a display: route them through PROBE. A figure-bearing claim should be shown as a figure (forest, dose-response curve, panel), not only as a typed table.
7. **The stage doc is the gallery.** `0-lifecycle/4-display/4-display.tex` `\input`s each rendered `float.tex`, so the stage PDF doubles as the combined figures-and-tables view; do NOT make a separate `preview-all`. Compile from the paper ROOT so the `0-displays/` paths resolve. Per-unit `preview.pdf` remain as individual review artifacts.
8. **Two display kinds, both task-rendered.** (a) data-driven: a parser turns server logs/CSVs into `metrics.json`, then a render task turns that into `assets/figure.pdf` / `assets/table-body.tex` (robust parser: handle factor-variable rows, leading-dot numbers, SE/CIs). (b) schematic/flow (study-flow, data-provenance, CONSORT): a diagram render task draws the flow and annotates it with REAL Ns pulled from the data description; still a task output, never hand-drawn.
9. **Venue-ALIGNED: couple to venue.** Read STATUS `venue`; if `../../_venue/playbook-<venue>` exists, consult its `README.md` section `-> Display` for the venue's standard display set and hero rule (e.g. Table 1 + STROBE cohort-flow for clinical, the research-model figure for MISQ, the main-result multi-panel for Nature/PNAS). The `[primary]` claim's display is the hero. A venue change re-runs the display set. Also consult the playbook for display style requirements (figure count limits, table format, color guidelines).
10. **Author/USER comments live in the lifecycle file, not the units.** Author or reviewer comments on a figure/table (preferences, "too thin," "park this," ordering) go ONLY into `0-lifecycle/4-display/4-display.tex` as `%% {USER}: ...` source lines, kept verbatim across iterations. Do NOT append them to a unit's `float.tex`; units stay portable and comment-free, and the lifecycle file is the single commentary / preference log for the display set (alongside the per-display self-check verdicts and the Parked section for kept-but-unused units).

## Relationship to ARIS

ARIS treats figures/tables mostly as a production phase in Workflow 3:

```
paper-plan -> paper-figure -> paper-write
```

HAI-Pipe treats display as a manuscript layer that crosses story and evidence:

```
pitch -> narrative -> display -> section-edit
```

The difference matters. A display can fail because the plot is ugly, but it can also fail because the paper's claim, section role, or one-minute pitch changed.

## Handoff

On CHECK confirm, update `STATUS.md` (`current_layer`, `maturity: display`) and advance:

```text
promote     -> /haipipe-paper section-edit <paper-dir>
```

End the reply with the stage strip (run `../../../haipipe-paper/stage-strip.sh`).
