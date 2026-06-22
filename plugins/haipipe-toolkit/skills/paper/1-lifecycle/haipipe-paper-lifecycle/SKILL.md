---
name: haipipe-paper-lifecycle
description: "Orchestrator for the paper structure lifecycle (1-lifecycle). Routes to specialists: folder (scaffold), pitch (one-minute story), narrative (design contract), minimap (paragraph jobs + evidence anchors; folds in the architecture blueprint and plan outline), display (figure/table contract + preview PDFs; folds in figure-planner inventory), figure (plots/tables), figure-spec (vector diagrams), illustration (AI images). Use when you need any structural work on a paper before or during writing. Trigger: paper structure, paper pitch, scaffold paper, paper outline, paper architecture, display layer, figure plan, /haipipe-paper-lifecycle."
argument-hint: "[function] [paper-path-or-input] [args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-06-08"
  summary: "Orchestrator for 1-lifecycle — routes to specialists covering folder scaffold, paper pitch, narrative, planning, display contracts, and figure production."
  changelog:
    - "1.0.0 (2026-06-08): created as orchestrator over all 1-lifecycle specialists."
---

Skill: haipipe-paper-lifecycle (orchestrator)
==============================================

User-facing entry for **paper structural work** — everything that
decides *what the paper is* before prose exists, or when the argument
needs rethinking. This is the **Plan cycle (①)** in the paper mental
model (see `paper/README.md` and `ref/paper-lifecycle.md`).

The orchestrator owns routing only. Each specialist owns its own
workflow, inputs, and outputs. The orchestrator never generates
narrative, outlines, figures, or diagrams itself.

```
/haipipe-paper-lifecycle                                -> dashboard (list specialists + pipeline)
/haipipe-paper-lifecycle folder <args>                  -> scaffold paper directory
/haipipe-paper-lifecycle seed <args>                    -> 0-lifecycle/0-seed/0-seed.tex
/haipipe-paper-lifecycle pitch <args>                   -> 0-lifecycle/1-pitch/1-pitch.tex
/haipipe-paper-lifecycle claims <args>                  -> 0-lifecycle/2-claims/2-claims.tex (claim ledger)
/haipipe-paper-lifecycle narrative <args>               -> NARRATIVE_REPORT.md (design contract)
/haipipe-paper-lifecycle minimap <args>                 -> 0-lifecycle/5-minimap/5-minimap.tex (folds in architecture blueprint + plan outline; see its ref/)
/haipipe-paper-lifecycle display <args>                 -> 0-displays/README.md + ready-to-input display blocks (folds in figure-planner inventory; see its ref/)
/haipipe-paper-lifecycle figure <args>                  -> data-driven plots + tables
/haipipe-paper-lifecycle figure-spec <args>             -> deterministic vector diagrams (SVG)
/haipipe-paper-lifecycle illustration <args>            -> AI illustrations (Gemini)
/haipipe-paper-lifecycle illustration-image2 <args>     -> AI illustrations (Codex bridge, experimental)
/haipipe-paper-lifecycle "<natural language>"            -> infer function, dispatch
```

---

Specialists
-----------

### Foundation — what folder + what story

```
haipipe-paper-folder                  SCAFFOLD:  create Paper-<Name>-<Venue><Year>/ with
                                                 0-sections, 0-displays, 1-rounds, compile
                                                 scripts, .gitignore, section stubs (IRDM/IMRD/IS)

haipipe-paper-seed          SEED:      maintain 0-lifecycle/0-seed/0-seed.tex: why
                                                 this paper might exist, evidence status, open
                                                 needs (routed to probe/discover/task), plus a
                                                 promotion gate and kill criteria.

haipipe-paper-pitch         PITCH:     maintain 0-lifecycle/1-pitch/1-pitch.tex, the
                                                 one-minute public-facing story for this
                                                 concrete paper, plus pitch provenance.

haipipe-paper-claims        LEDGER:    maintain 0-lifecycle/2-claims/2-claims.tex, the
                                                 claim ledger (supported / weak / GAP), each row
                                                 tied to an evidence source; emits needs and
                                                 backfills probe verdicts.

haipipe-paper-narrative     CONTRACT:  generate the evidence-backed arc from the claim
                                                 ledger: problem, core claim, method, figure
                                                 inventory, limitations.
```

### Architecture & Planning — what the paper says

```
haipipe-paper-minimap       MINIMAP:   maintain 0-lifecycle/5-minimap/5-minimap.tex:
                                                 each paragraph slot's job + evidence anchor
                                                 (claim row + display unit). Owns the minimap
                                                 table. The architecture blueprint (5-act arc,
                                                 contribution emphasis, page budget) and the
                                                 plan outline (section-by-section venue budgets)
                                                 are now folded in as ref/architecture-blueprint.md
                                                 and ref/plan-outline.md.

haipipe-paper-display       DISPLAY:   0-displays/README.md plus per-unit
                                                 README.md, float.tex, and preview.pdf for
                                                 figures/tables. Keeps display items tied to
                                                 claim, evidence source, section, and caption.
                                                 Figure-inventory planning (one claim per figure,
                                                 panel roles, main vs supplement) is folded in as
                                                 ref/figure-logic.md.
```

### Figures & Illustrations — visual assets

```
haipipe-paper-figure          PLOT:    data-driven publication plots + tables from
                                                 experiment results (~60% of figures)

haipipe-paper-figure-spec     VECTOR:  deterministic architecture/workflow/pipeline
                                                 diagrams from structured JSON → editable SVG

haipipe-paper-illustration    AI-IMG:  AI illustrations via Gemini with Claude-
                                                 supervised iterative refinement

haipipe-paper-illustration-image2  AI-IMG2: experimental alternative via local Codex
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
                 (figure-inventory planning folded in as its ref/figure-logic.md)
      ↓
⑦ minimap        paragraph jobs + evidence anchors
                 (architecture blueprint + plan outline folded in as its ref/)
      ↓
⑧ figure / figure-spec / illustration   make the visual assets
```

After ⑦, the paper folder is ready for the **Edit cycle (②)** in the
paper mental model — the hand-off goes to `4-build-submit/` and `3-write-edit/`
skills. Structural audit (ASCII zoom diagrams) now lives in the Edit cycle as
`haipipe-paper-edit-diagram`.

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
    function = "folder"    -> Skill("haipipe-paper-bootstrap", args)
    function = else        -> Skill("haipipe-paper-<function>", args)

    Special: "figure-plan" -> Skill("haipipe-paper-display", args)
             (figure-inventory planning now lives inside display;
              see haipipe-paper-display/ref/figure-logic.md)
             "illustration-image2" -> Skill("haipipe-paper-illustration-image2", args)
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

minimap, paragraph minimap, paragraph jobs,
  evidence anchor, section map, paragraph plan,
  architecture, blueprint, 5-act arc, strategic
  overview, plan, outline, PAPER_PLAN, section plan,
  page budget, 写大纲, paper outline                   -> minimap

display, display layer, 0-displays/README.md, 0-displays,
  ready to input, preview pdf, float.tex, caption,
  figure table contract, display contract,
  figure planner, figure inventory, panel roles,
  main vs supplement, what figures                    -> display

figure-plan                                           -> display

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
minimap, paragraph-map, anchors,
  architecture, arch, blueprint, plan, outline   -> minimap
display, displays, disp,
  figure-plan, fp, figplan                       -> display
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
📐 haipipe-paper-lifecycle — paper structural work

  Foundation:
    folder         Scaffold Paper-<Name>-<Venue><Year>/ directory

  Lifecycle spine (0-lifecycle):
    seed           0-seed: why this paper might exist
    pitch          1-pitch: one-minute public-facing story
    claims         2-claims: claim ledger (supported / weak / GAP)
    narrative      3-narrative: evidence-backed arc
    display        4-display: display contract + units
                   (figure-inventory planning folded in; see ref/figure-logic.md)
    minimap        5-minimap: paragraph jobs + evidence anchors
                   (architecture blueprint + plan outline folded in; see its ref/)

  Figures & Illustrations:
    figure         Data-driven plots + tables
    figure-spec    Deterministic vector diagrams (JSON → SVG)
    illustration   AI illustrations (Gemini + Claude refinement)

  Pipeline: folder → seed → pitch → claims → narrative → display → minimap → figure

Next: /haipipe-paper-lifecycle <function> "<input>"
```

---

Specialist Return Contract
---------------------------

Each specialist should return a tail block:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what the specialist did
artifacts: [paths created, read, or modified]
next:      suggested next /haipipe-paper-lifecycle command
```

---

Relation to Parent Orchestrator
--------------------------------

`haipipe-paper` (in `paper/_venue/`) is the top-level paper
router by **venue**. It dispatches to venue specialists
(`-conference`, `-journal`, `-is`) which in turn call structure
specialists as needed. This orchestrator (`haipipe-paper-lifecycle`)
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
haipipe-paper-lifecycle (this orchestrator)
  ├─► folder
  ├─► pitch
  ├─► narrative
  ├─► display      (figure-inventory planning folded in; see ref/figure-logic.md)
  ├─► minimap      (architecture blueprint + plan outline folded in; see its ref/)
  ├─► figure / figure-spec / illustration
  └─► (hands off to 4-build-submit / 3-write-edit when structure is settled;
       structural ASCII audit now lives there as haipipe-paper-edit-diagram)
```
