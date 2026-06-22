---
name: haipipe-paper-structure
description: "Orchestrator for the paper structure lifecycle (1-lifecycle). Routes to specialists: folder (scaffold), pitch (one-minute story), narrative (design contract), architecture (blueprint+minimap), plan (outline), display (figure/table contract + preview PDFs), diagram (structural audit), incubator (working docs), figure-planner (inventory), figure (plots/tables), figure-spec (vector diagrams), illustration (AI images). Use when you need any structural work on a paper before or during writing. Trigger: paper structure, paper pitch, scaffold paper, paper outline, paper architecture, display layer, figure plan, paper diagram, incubator, /haipipe-paper-structure."
argument-hint: "[function] [paper-path-or-input] [args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-06-08"
  summary: "Orchestrator for 1-lifecycle — routes to specialists covering folder scaffold, paper pitch, narrative, planning, display contracts, and figure production."
  changelog:
    - "1.0.0 (2026-06-08): created as orchestrator over all 1-lifecycle specialists."
---

Skill: haipipe-paper-structure (orchestrator)
==============================================

User-facing entry for **paper structural work** — everything that
decides *what the paper is* before prose exists, or when the argument
needs rethinking. This is the **Plan cycle (①)** in the paper mental
model (see `paper/README.md` and `ref/paper-lifecycle.md`).

The orchestrator owns routing only. Each specialist owns its own
workflow, inputs, and outputs. The orchestrator never generates
narrative, outlines, figures, or diagrams itself.

```
/haipipe-paper-structure                                -> dashboard (list specialists + pipeline)
/haipipe-paper-structure folder <args>                  -> scaffold paper directory
/haipipe-paper-structure seed <args>                    -> 0-lifecycle/0-seed/0-seed.tex
/haipipe-paper-structure pitch <args>                   -> 0-lifecycle/1-pitch/1-pitch.tex
/haipipe-paper-structure claims <args>                  -> 0-lifecycle/2-claims/2-claims.tex (claim ledger)
/haipipe-paper-structure narrative <args>               -> NARRATIVE_REPORT.md (design contract)
/haipipe-paper-structure architecture <args>            -> vNN-architecture-minimap.md (feeds minimap)
/haipipe-paper-structure plan <args>                    -> PAPER_PLAN.md (structured outline, feeds minimap)
/haipipe-paper-structure minimap <args>                 -> 0-lifecycle/5-minimap/5-minimap.tex
/haipipe-paper-structure display <args>                 -> 0-displays/README.md + ready-to-input display blocks
/haipipe-paper-structure diagram <args>                 -> ASCII structural audit (3 zoom levels)
/haipipe-paper-structure incubator <sub> <args>         -> incubator docs (display/arch/structure)
/haipipe-paper-structure figure-plan <args>             -> figure inventory + panel roles
/haipipe-paper-structure figure <args>                  -> data-driven plots + tables
/haipipe-paper-structure figure-spec <args>             -> deterministic vector diagrams (SVG)
/haipipe-paper-structure illustration <args>            -> AI illustrations (Gemini)
/haipipe-paper-structure illustration-image2 <args>     -> AI illustrations (Codex bridge, experimental)
/haipipe-paper-structure "<natural language>"            -> infer function, dispatch
```

---

Specialists
-----------

### Foundation — what folder + what story

```
haipipe-paper-folder                  SCAFFOLD:  create Paper-<Name>-<Venue><Year>/ with
                                                 0-sections, 0-displays, 1-rounds, compile
                                                 scripts, .gitignore, section stubs (IRDM/IMRD/IS)

haipipe-paper-structure-seed          SEED:      maintain 0-lifecycle/0-seed/0-seed.tex: why
                                                 this paper might exist, evidence status, open
                                                 needs (routed to probe/discover/task), plus a
                                                 promotion gate and kill criteria.

haipipe-paper-structure-pitch         PITCH:     maintain 0-lifecycle/1-pitch/1-pitch.tex, the
                                                 one-minute public-facing story for this
                                                 concrete paper, plus pitch provenance.

haipipe-paper-structure-claims        LEDGER:    maintain 0-lifecycle/2-claims/2-claims.tex, the
                                                 claim ledger (supported / weak / GAP), each row
                                                 tied to an evidence source; emits needs and
                                                 backfills probe verdicts.

haipipe-paper-structure-narrative     CONTRACT:  generate the evidence-backed arc from the claim
                                                 ledger: problem, core claim, method, figure
                                                 inventory, limitations.
```

### Architecture & Planning — what the paper says

```
haipipe-paper-structure-architecture  BLUEPRINT: versioned vNN-architecture-minimap.md (v3.1) —
                                                 config table, 5-act arc, paragraph-level
                                                 minimap with A/B options, substantial appendix
                                                 plan (~half the paper), language guide, MISQ-
                                                 format page budget (body+appendix+refs+buffer).
                                                 Tested: subagent produces consistent output.

haipipe-paper-structure-plan          OUTLINE:   PAPER_PLAN.md, section-by-section plan with
                                                 venue-specific page budgets (feeds minimap).

haipipe-paper-structure-minimap       MINIMAP:   maintain 0-lifecycle/5-minimap/5-minimap.tex:
                                                 each paragraph slot's job + evidence anchor
                                                 (claim row + display unit). Wraps architecture
                                                 and plan; owns the minimap table.

haipipe-paper-structure-display       DISPLAY:   0-displays/README.md plus per-unit
                                                 README.md, float.tex, and preview.pdf for
                                                 figures/tables. Keeps display items tied to
                                                 claim, evidence source, section, and caption.

haipipe-paper-structure-diagram       AUDIT:     ASCII diagrams at 3 zoom levels (sections /
                                                 paragraphs / sentences) for structural review
                                                 and rhetorical flow analysis

haipipe-paper-structure-incubator     INCUBATE:  three subcommands (display / arch / structure)
                                                 for creating + refining incubator LaTeX working
                                                 docs in 0-incubator/
```

### Figures & Illustrations — visual assets

```
haipipe-paper-structure-figure-planner  PLAN:    design/audit figure inventory — one claim
                                                 per figure, panel roles, main vs supplement

haipipe-paper-structure-figure          PLOT:    data-driven publication plots + tables from
                                                 experiment results (~60% of figures)

haipipe-paper-structure-figure-spec     VECTOR:  deterministic architecture/workflow/pipeline
                                                 diagrams from structured JSON → editable SVG

haipipe-paper-structure-illustration    AI-IMG:  AI illustrations via Gemini with Claude-
                                                 supervised iterative refinement

haipipe-paper-structure-illustration-image2  AI-IMG2: experimental alternative via local Codex
                                                 app-server bridge (GPT-image-style renderer)
```

---

Natural Pipeline Order
----------------------

The specialists are designed to flow in sequence, though any can be
invoked standalone. The typical first-pass order:

```
① folder         scaffold the directory
      ↓
② seed           why this paper might exist (prospectus contract)
      ↓
③ pitch          one-minute public-facing story + provenance
      ↓
④ claims         claim ledger: supported / weak / GAP, with evidence sources
      ↓
⑤ narrative      evidence-backed arc from the claim ledger
      ↓
⑥ display        display contract: figure/table jobs, sources, captions, preview PDFs
      ↓
⑦ minimap        paragraph jobs + evidence anchors (uses architecture + plan)
      ↓
⑧ figure-plan / figure / figure-spec / illustration   make the visual assets
      ↓
⑨ diagram        audit structure before handing off to Edit cycle
```

`incubator` runs in parallel at any point (scratch docs for thinking).

After ⑦, the paper folder is ready for the **Edit cycle (②)** in the
paper mental model — the hand-off goes to `4-build-submit/` and `3-write-edit/`
skills.

---

Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.

Step 2: Resolve function:
  - First positional matches a function alias?       -> dispatch target = that
  - Else scan keyword map across all positional args
  - Default if no match                              -> dashboard (inline)

Step 3: Dispatch:
    function = "folder"    -> Skill("haipipe-paper-structure-bootstrap", args)
    function = else        -> Skill("haipipe-paper-structure-<function>", args)

    Special: "figure-plan" -> Skill("haipipe-paper-structure-figure-planner", args)
             "illustration-image2" -> Skill("haipipe-paper-structure-illustration-image2", args)
```

---

Function Keyword Map
---------------------

```
folder, scaffold, bootstrap, init, new paper dir,
  create folder, Paper-*                              -> folder

seed, paper seed, why this paper, prospectus,
  kill criteria, paper possibility                    -> seed

pitch, paper pitch, one-minute story, hook, surprise,
  so what, story trajectory, pitch provenance          -> pitch

claims, claim ledger, supported, weak, GAP,
  claim gap, evidence map, overclaim                  -> claims

narrative, story, design contract, NARRATIVE_REPORT,
  claim-evidence matrix, core claim                   -> narrative

architecture, blueprint, 5-act arc,
  strategic overview, vNN-architecture                -> architecture

plan, outline, PAPER_PLAN, section plan,
  page budget, 写大纲, paper outline                   -> plan

minimap, paragraph minimap, paragraph jobs,
  evidence anchor, section map, paragraph plan        -> minimap

display, display layer, 0-displays/README.md, 0-displays,
  ready to input, preview pdf, float.tex, caption,
  figure table contract, display contract              -> display

diagram, structure audit, section map, paragraph map,
  rhetorical flow, sentence breakdown, zoom           -> diagram

incubator, incubate, scratch doc, 0-incubator,
  incubator display, incubator arch                   -> incubator

figure-plan, figure planner, figure inventory,
  panel roles, main vs supplement, what figures        -> figure-plan

figure, plot, plots, tables, data figure,
  generate figures, 画图, 作图                          -> figure

figure-spec, vector, architecture diagram, SVG,
  pipeline diagram, workflow diagram, 架构图,
  确定性矢量图                                         -> figure-spec

illustration, AI illustration, Gemini illustration,
  method illustration, 生成图表, AI绘图                 -> illustration

illustration-image2, codex illustration, codex bridge,
  experimental illustration                           -> illustration-image2
```

Function aliases (positional):
```
folder, scaffold, bootstrap, init                -> folder
seed, paper-seed, prospectus                     -> seed
pitch, paper-pitch, storycard                    -> pitch
claims, claim, ledger                            -> claims
narrative, story, contract                       -> narrative
architecture, arch, blueprint                    -> architecture
plan, outline                                    -> plan
minimap, paragraph-map, anchors                  -> minimap
display, displays, disp                          -> display
diagram, audit, map                              -> diagram
incubator, incubate                              -> incubator
figure-plan, fp, figplan                         -> figure-plan
figure, fig, plot                                -> figure
figure-spec, spec, vector, svg                   -> figure-spec
illustration, illust, ai-img                     -> illustration
illustration-image2, illust2, ai-img2            -> illustration-image2
```

---

No-Arg Mode (dashboard, inline)
---------------------------------

When invoked with no arguments, emit a compact specialist chooser:

```
📐 haipipe-paper-structure — paper structural work

  Foundation:
    folder         Scaffold Paper-<Name>-<Venue><Year>/ directory

  Lifecycle spine (0-lifecycle):
    seed           0-seed: why this paper might exist
    pitch          1-pitch: one-minute public-facing story
    claims         2-claims: claim ledger (supported / weak / GAP)
    narrative      3-narrative: evidence-backed arc
    display        4-figures-tables: display contract + units
    minimap        5-minimap: paragraph jobs + evidence anchors (uses architecture/plan)

  Planning helpers:
    architecture   Strategic blueprint (feeds minimap)
    plan           Structured outline with page budgets (feeds minimap)
    diagram        ASCII structural audit (sections / paragraphs / sentences)
    incubator      Incubator LaTeX working docs (display / arch / structure)

  Figures & Illustrations:
    figure-plan    Design figure inventory + panel roles
    figure         Data-driven plots + tables
    figure-spec    Deterministic vector diagrams (JSON → SVG)
    illustration   AI illustrations (Gemini + Claude refinement)

  Pipeline: folder → seed → pitch → claims → narrative → display → minimap → figure-plan → figure → diagram

Next: /haipipe-paper-structure <function> "<input>"
```

---

Specialist Return Contract
---------------------------

Each specialist should return a tail block:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what the specialist did
artifacts: [paths created, read, or modified]
next:      suggested next /haipipe-paper-structure command
```

---

Relation to Parent Orchestrator
--------------------------------

`haipipe-paper` (in `paper/_venue/`) is the top-level paper
router by **venue**. It dispatches to venue specialists
(`-conference`, `-journal`, `-is`) which in turn call structure
specialists as needed. This orchestrator (`haipipe-paper-structure`)
is the direct entry for structural work — either called by a venue
specialist or by the user directly.

```
haipipe-paper (venue router)
  ├─► haipipe-paper-conference ──┐
  ├─► haipipe-paper-journal   ───┤── call structure specialists as needed
  ├─► haipipe-paper-is        ──┘
  └─► haipipe-paper-create / -revise
            │
            ▼
haipipe-paper-structure (this orchestrator)
  ├─► folder
  ├─► pitch
  ├─► narrative
  ├─► architecture
  ├─► plan
  ├─► display
  ├─► diagram
  ├─► incubator
  ├─► figure-plan
  ├─► figure / figure-spec / illustration
  └─► (hands off to 4-build-submit / 3-write-edit when structure is settled)
```
