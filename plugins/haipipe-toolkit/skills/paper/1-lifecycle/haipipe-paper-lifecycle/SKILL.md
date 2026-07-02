---
name: haipipe-paper-lifecycle
description: "Orchestrator for the paper structure lifecycle (1-lifecycle). Routes to specialists across the venue-free/venue-aligned boundary: seed and claims are venue-FREE (don't change on retarget); venue pins the journal; pitch, narrative, display, and section-edit are venue-ALIGNED (rewrite on retarget). Also routes to display renderers: table, figure, diagram, illustration. Use when you need any structural work on a paper before or during writing. Trigger: paper structure, paper pitch, scaffold paper, paper outline, paper architecture, display layer, figure plan, /haipipe-paper-lifecycle."
argument-hint: "[function] [paper-path-or-input] [args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-06-08"
  summary: "Orchestrator for 1-lifecycle -- routes to specialists across the venue-free/venue-aligned boundary: folder, seed, claims (venue-FREE), venue (decision gate), pitch, narrative, display (venue-ALIGNED), and figure production."
  changelog:
    - "1.0.0 (2026-06-08): created as orchestrator over all 1-lifecycle specialists."
---

Skill: haipipe-paper-lifecycle (orchestrator)
==============================================

User-facing entry for **paper structural work** -- everything that decides *what the paper is* before prose exists, or when the argument needs rethinking. This is the **Plan cycle** in the paper mental model (see `paper/README.md` and `ref/paper-lifecycle.md`).

The lifecycle has a **venue-free / venue-aligned boundary**. Seed and claims are venue-FREE (they don't change when you retarget to a different journal). Venue is the decision gate that pins the target journal. Pitch, narrative, display, and section-edit are venue-ALIGNED (they rewrite when you retarget).

The orchestrator owns routing only. Each specialist owns its own workflow, inputs, and outputs. The orchestrator never generates narrative, outlines, figures, or diagrams itself.

```
/haipipe-paper-lifecycle                                -> dashboard (list specialists + pipeline)
/haipipe-paper-lifecycle folder <args>                  -> scaffold paper directory
/haipipe-paper-lifecycle seed <args>                    -> 0-lifecycle/0-seed/0-seed.md (venue-FREE)
/haipipe-paper-lifecycle claims <args>                  -> 0-lifecycle/1-claims/1-claims.md (venue-FREE claim ledger)
/haipipe-paper-lifecycle venue <args>                   -> STATUS.md venue pin (decision gate)
/haipipe-paper-lifecycle pitch <args>                   -> 0-lifecycle/2-pitch/2-pitch.md (venue-ALIGNED cover letter)
/haipipe-paper-lifecycle narrative <args>               -> NARRATIVE_REPORT.md (design contract)
/haipipe-paper-lifecycle display <args>                 -> 0-displays/README.md + ready-to-input display blocks (folds in figure-planner inventory; see its ref/)
/haipipe-paper-lifecycle table <args>                   -> data-driven LaTeX tables (haipipe-paper-display-table)
/haipipe-paper-lifecycle figure <args>                  -> data-driven plots (haipipe-paper-display-figure)
/haipipe-paper-lifecycle diagram <args>                 -> deterministic vector diagrams / SVG (haipipe-paper-display-diagram)
/haipipe-paper-lifecycle illustration <args>            -> AI concept illustration, DEFAULT Codex bridge (haipipe-paper-display-illustration)
/haipipe-paper-lifecycle illustration-gemini <args>     -> AI concept illustration, Gemini fallback (haipipe-paper-display-illustration-gemini)
/haipipe-paper-lifecycle framework <args>                -> display framework mode (candidate rounds, selection, handoff)
/haipipe-paper-lifecycle "<natural language>"            -> infer function, dispatch
```

---

Specialists
-----------

### Foundation -- what folder + what story

```
haipipe-paper-folder                  SCAFFOLD:  create Paper-<Name>-<Venue><Year>/ with 0-sections, 0-displays, 1-rounds, compile scripts, .gitignore, section stubs (IRDM/IMRD/IS)

--- VENUE-FREE (don't change on retarget) ---

haipipe-paper-seed          SEED (0):    maintain 0-lifecycle/0-seed/0-seed.md: why this paper might exist, evidence status, open needs (routed to probe/discover/task), plus a promotion gate and kill criteria.

haipipe-paper-claims        CLAIMS (1):  maintain 0-lifecycle/1-claims/1-claims.md, the venue-FREE claim/evidence inventory (supported / weak / GAP), each row tied to an evidence source; venue-neutral H1/H2/H3; emits needs and backfills probe verdicts.

--- VENUE DECISION (pins target journal in STATUS.md) ---

haipipe-paper-venue         VENUE:       recommend + pin the best-fit venue; gate between venue-free and venue-aligned stages.

--- VENUE-ALIGNED (rewrite on retarget) ---

haipipe-paper-pitch         PITCH (2):   maintain 0-lifecycle/2-pitch/2-pitch.md, the venue-ALIGNED cover letter and one-minute story; owns Editor's Chair Test, [primary] claim designation, venue-specific RQ framing.

haipipe-paper-narrative     NARRATIVE (3): generate the venue-ALIGNED evidence-backed arc from the claim ledger: problem, core claim, method, figure inventory, limitations.
```

### Display & Figures -- what the reader sees (venue-ALIGNED)

```
haipipe-paper-display       DISPLAY (4): 0-displays/README.md plus per-unit README.md, float.tex, and preview.pdf for figures/tables. Venue-ALIGNED: keeps display items tied to claim, evidence source, section, and caption. Consults venue playbook for display set and hero rule. Figure-inventory planning (one claim per figure, panel roles, main vs supplement) is folded in as ref/figure-logic.md. Framework/architecture mode handles Figure 1 candidate rounds before final rendering.
```

### Figures & Illustrations -- visual assets

```
haipipe-paper-display-table           TABLE:   data-driven LaTeX tables (booktabs/stars/panels) from an aggregated CSV/JSON

haipipe-paper-display-figure          PLOT:    data-driven publication plots from experiment results (plots only)

haipipe-paper-display-diagram         VECTOR:  deterministic architecture/workflow/pipeline diagrams from structured JSON -> editable SVG

haipipe-paper-display-illustration    AI-IMG:  DEFAULT AI concept illustration via the local Codex app-server bridge (native image gen)

haipipe-paper-display-illustration-gemini  AI-IMG (fallback):  Gemini backend with Claude-supervised refinement; use if the Codex bridge is unavailable or the user asks for Gemini
```

---

Natural Pipeline Order
----------------------

The specialists are designed to flow in sequence, though any can be invoked standalone. The typical first-pass order:

```
  VENUE-FREE (don't change on retarget)
  ──────────────────────────────────────
  folder (0)     scaffold the directory
      ↓
  seed (0)       why this paper might exist (prospectus contract)
      ↓
  claims (1)     claim/evidence inventory: supported / weak / GAP, with evidence sources
                 venue-neutral H1/H2/H3 hypotheses; no [primary], no RQ framing

  VENUE DECISION
  ──────────────────────────────────────
      ↓
  venue          pin target journal in STATUS.md (gate between FREE and ALIGNED)

  VENUE-ALIGNED (rewrite on retarget)
  ──────────────────────────────────────
      ↓
  pitch (2)      venue-ALIGNED cover letter: Editor's Chair Test, [primary] claim, RQ framing
      ↓
  narrative (3)  venue-ALIGNED evidence-backed arc from the claim ledger
      ↓
  display (4)    venue-ALIGNED display contract: figure/table jobs, sources, captions, preview PDFs
                 (figure-inventory planning folded in as its ref/figure-logic.md)
      ↓
  table / figure / diagram / illustration   make the visual assets
```

After display rendering, the paper folder is ready for per-section editing work in `0-lifecycle/5-editing/` and the **Edit cycle** skills under `3-write-edit/`. Structural audit (ASCII zoom diagrams) lives in the Edit cycle as `haipipe-paper-edit-diagram`.

**Retarget rule:** when the venue changes, claims stays unchanged (venue-FREE). Pitch, narrative, display, and section-edit all rewrite for the new venue.

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

    # Display renderers carry the display- prefix; map the short verb explicitly:
    function = "table"          -> Skill("haipipe-paper-display-table", args)
    function = "figure"         -> Skill("haipipe-paper-display-figure", args)
    function = "diagram"        -> Skill("haipipe-paper-display-diagram", args)
    function = "illustration"   -> Skill("haipipe-paper-display-illustration", args)        # DEFAULT (Codex bridge)
    function = "illustration-gemini" -> Skill("haipipe-paper-display-illustration-gemini", args)  # fallback

    # Lifecycle stages keep the plain haipipe-paper-<stage> name:
    function = else        -> Skill("haipipe-paper-<function>", args)
        (seed | claims | venue | pitch | narrative | display)

    Special: "figure-plan", "framework" -> Skill(
      "haipipe-paper-display", "framework " + args
    )
             (figure-inventory planning now lives inside display;
              see haipipe-paper-display/ref/figure-logic.md)
```

---

Function Keyword Map
---------------------

```
folder, scaffold, bootstrap, init, new paper dir,
  create folder, Paper-*                              -> folder

seed, paper seed, why this paper, prospectus,
  kill criteria, paper possibility                    -> seed       (venue-FREE)

claims, claim ledger, supported, weak, GAP,
  claim gap, evidence map, overclaim, H1, H2, H3     -> claims     (venue-FREE)

venue, which journal, where to submit, venue fit,
  recommend journal, journal selection, pick venue    -> venue      (decision gate)

pitch, paper pitch, one-minute story, hook, surprise,
  so what, story trajectory, pitch provenance,
  cover letter, editor's chair, primary claim         -> pitch      (venue-ALIGNED)

narrative, story, design contract, NARRATIVE_REPORT,
  claim-evidence matrix, core claim                   -> narrative

display, display layer, 0-displays/README.md, 0-displays,
  ready to input, preview pdf, float.tex, caption,
  figure table contract, display contract,
  figure planner, figure inventory, panel roles,
  main vs supplement, what figures                    -> display

figure-plan                                           -> display
framework, figure1, figure 1, 架构图, pipeline图             -> framework

table, tables, latex table, regression table,
  coefficient table, descriptive table, comparison table,
  做表, 生成表格, 表格                                  -> table

figure, plot, plots, data figure, line plot, bar chart,
  scatter, heatmap, box plot, generate figures, 画图, 作图  -> figure

diagram, figure-spec, vector, SVG, pipeline diagram,
  workflow diagram, 确定性矢量图                        -> diagram

illustration, AI illustration, concept figure, method
  illustration, codex illustration, AI 配图, AI绘图,
  生成图表                                              -> illustration   (DEFAULT, Codex bridge)

illustration-gemini, gemini illustration, gemini,
  nano banana, 用 gemini 画                            -> illustration-gemini
```

Function aliases (positional):
```
folder, scaffold, bootstrap, init                -> folder
seed, paper-seed, prospectus                     -> seed
claims, claim, ledger                            -> claims
venue, journal, submit-to                        -> venue
pitch, paper-pitch, storycard, cover-letter      -> pitch
narrative, story, contract                       -> narrative
display, displays, disp,
  figure-plan, fp, figplan, fw                   -> display
framework, figureone, fig1                        -> framework
table, tbl, tab                                  -> table
figure, fig, plot                                -> figure
diagram, figure-spec, spec, vector, svg          -> diagram
illustration, illust, ai-img, image2, codex      -> illustration          (DEFAULT)
illustration-gemini, gemini, illust-g, ai-img-g  -> illustration-gemini
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
    VENUE-FREE:
      seed           0-seed: why this paper might exist
      claims         1-claims: claim/evidence inventory (venue-neutral H1/H2/H3)
    VENUE DECISION:
      venue          pin target journal in STATUS.md
    VENUE-ALIGNED:
      pitch          2-pitch: cover letter + one-minute story (Editor's Chair, [primary], RQ framing)
      narrative      3-narrative: evidence-backed arc
      display        4-display: display contract + units (figure-inventory planning folded in; see ref/figure-logic.md)

  Display renderers (data-driven):
    table          Data-driven LaTeX tables (booktabs/stars/panels)
    figure         Data-driven plots (line/bar/scatter/heatmap/box)

  Display renderers (concept):
    diagram        Deterministic vector diagrams (JSON -> SVG)
    illustration   AI concept illustration -- DEFAULT, Codex bridge
    illustration-gemini  AI concept illustration -- Gemini fallback
    framework      Candidate framework/architecture figure planning (Figure 1 style)

  Pipeline: folder -> seed (FREE) -> claims (FREE) -> [venue] -> pitch (ALIGNED) -> narrative (ALIGNED) -> display (ALIGNED) -> table/figure/diagram/illustration

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

`haipipe-paper` (in `paper/haipipe-paper/`) is the top-level paper router + Console. It resolves status and consults the target's profile in `_venue/playbook-<venue>` for venue fit. This orchestrator (`haipipe-paper-lifecycle`) is the direct entry for structural work -- either routed from the Console or invoked by the user directly.

```
haipipe-paper (router)  -- consults _venue/playbook-<venue> for venue fit
            |                (misq/isr/ms-is/pnas/nature-portfolio/jama/clinical; grant; patent-*)
            v
haipipe-paper-lifecycle (this orchestrator)
  VENUE-FREE:
  |-- folder
  |-- seed (0)
  |-- claims (1)
  VENUE DECISION:
  |-- venue          (pin target journal in STATUS.md)
  VENUE-ALIGNED:
  |-- pitch (2)      (cover letter: Editor's Chair, [primary], RQ framing)
  |-- narrative (3)
  |-- display (4)    (figure-inventory planning folded in; see ref/figure-logic.md)
  |-- table / figure / diagram / illustration (+ illustration-gemini fallback)
  +-- (hands off to 5-editing/ per-section scaffolds and 3-write-edit/ skills;
       structural ASCII audit lives there as haipipe-paper-edit-diagram)
```
