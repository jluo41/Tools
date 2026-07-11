---
name: haipipe-paper-lifecycle
description: "Orchestrator for the paper structure lifecycle (1-lifecycle). Routes to stage specialists across the venue-free/venue-aligned boundary: seed and claims are venue-FREE (don't change on retarget); venue pins the journal; pitch, narrative, display, and section-edit are venue-ALIGNED (rewrite on retarget). Also routes to display renderers: table, figure, diagram, illustration. Use when you need any structural work on a paper before or during writing. Trigger: paper structure, paper pitch, scaffold paper, paper outline, paper architecture, display layer, figure plan, section edit, /haipipe-paper-lifecycle."
argument-hint: "[function] [paper-path-or-input] [args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "2.2.0"
  last_updated: "2026-07-09"
  summary: "Router for the 1-lifecycle stage spine: folder, seed (0), claims (1) [venue-FREE] -> venue (gate) -> pitch (2), narrative (3), display (4), section-edit (5) [venue-ALIGNED], plus the display renderer family. Stage skills internally run DRAFT -> PROBE -> REVISE -> CHECK via 2-phase/ workers; this router never routes users to phase skills."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-lifecycle (orchestrator)
==============================================

User-facing entry for **paper structural work** -- everything that decides *what the paper is* before prose exists, or when the argument needs rethinking. This is the **Plan cycle** in the paper mental model (see `paper/README.md`, `../../wiki/03-paper-lifecycle.md`, and `../../wiki/04-lifecycle-map.md`).

The lifecycle has a **venue-free / venue-aligned boundary**. Seed and claims are venue-FREE (they don't change when you retarget to a different journal). Venue is the decision gate that pins the target journal in STATUS.md. Pitch, narrative, display, and section-edit are venue-ALIGNED (they rewrite when you retarget).

The orchestrator owns routing only. Each stage specialist owns its own workflow, inputs, and outputs. The orchestrator never generates narrative, outlines, figures, or diagrams itself.

```
/haipipe-paper-lifecycle                                -> dashboard (list specialists + pipeline)
/haipipe-paper-lifecycle folder <args>                  -> scaffold paper directory (haipipe-paper-folder)
/haipipe-paper-lifecycle seed <args>                    -> 0-lifecycle/0-seed/0-seed.md (venue-FREE)
/haipipe-paper-lifecycle claims <args>                  -> 0-lifecycle/1-claims/1-claims.md (venue-FREE claim ledger)
/haipipe-paper-lifecycle venue <args>                   -> STATUS.md venue pin + 0-lifecycle/2-venue/2-venue.md venue contract (decision gate)
/haipipe-paper-lifecycle pitch <args>                   -> 0-lifecycle/2-pitch/2-pitch.md (venue-ALIGNED cover letter)
/haipipe-paper-lifecycle narrative <args>               -> 0-lifecycle/3-narrative/3-narrative.md (venue-ALIGNED design contract)
/haipipe-paper-lifecycle display <args>                 -> 0-lifecycle/4-display/4-display.tex + 0-displays/ units (the only compiled stage)
/haipipe-paper-lifecycle section-edit <args>            -> 0-lifecycle/5-section-edit/{section}/ per-section editing hub
/haipipe-paper-lifecycle table <args>                   -> data-driven LaTeX tables (haipipe-paper-display-table)
/haipipe-paper-lifecycle figure <args>                  -> data-driven plots (haipipe-paper-display-figure)
/haipipe-paper-lifecycle diagram <args>                 -> deterministic vector diagrams / SVG (haipipe-paper-display-diagram)
/haipipe-paper-lifecycle illustration <args>            -> AI concept illustration, DEFAULT Codex bridge (haipipe-paper-display-illustration)
/haipipe-paper-lifecycle illustration-gemini <args>     -> AI concept illustration, Gemini fallback (haipipe-paper-display-illustration-gemini)
/haipipe-paper-lifecycle framework <args>               -> display framework mode (candidate rounds, selection, handoff)
/haipipe-paper-lifecycle "<natural language>"           -> infer function, dispatch
```

**Phase-verb pass-through**: a trailing `draft | probe | revise | check` after any stage's args is a PHASE VERB — forward it verbatim to the stage skill (e.g. `section-edit 4-llmtrait revise` → `Skill("haipipe-paper-section-edit", args="4-llmtrait revise")`). The verb picks which phase the stage drives; the stage still dispatches its internal workers.

---

Two-Axis Model (stages x phases)
---------------------------------

Stage skills are the USER-FACING surface. Internally, each stage skill drives the shared phase cycle **DRAFT -> PROBE -> REVISE -> CHECK** by dispatching the internal workers in `2-phase/` (`haipipe-paper-draft`, `haipipe-paper-probe*`, `haipipe-paper-revise*`, `haipipe-paper-check`). TWO human gates: DRAFT ends at a hard STOP for the user's structure review (`[GATE]` logged; the user's verb advances), and CHECK is the quality gate. PROBE and REVISE are agent-only between them; REVISE is proof-carrying (`workers:` line in `_LOG`). The agent never self-advances past a gate.

**This router routes users to STAGE skills only -- never to phase skills.** Phase dispatch is each stage skill's internal business. If a request sounds like a phase ("gather citations for §3", "polish the intro"), route to the owning stage skill (usually section-edit) and let it dispatch.

Stage artifacts are markdown (`N-<stage>.md` + `_LOG_`) for every stage except display, which compiles to `.tex` + PDF (you need to SEE rendered figures/tables). Stage gates and the illuminate loop are shared conventions: `../../wiki/08-stage-gate.md`, `../../wiki/09-stage-illuminate.md`.

---

Specialists
-----------

### Foundation -- what folder + what story

```
haipipe-paper-folder                  SCAFFOLD:  minimal quick scaffold (README + STATUS.md + .gitignore + empty 0-lifecycle/ 0-displays/ 1-rounds/ 1-probe-plans/); stage files absent-until-written; master tex / 0-sections / compile scripts are a later on-request upgrade. Repo+submodule wiring belongs to /haipipe-paper enter (get-or-create on a missing path).

--- VENUE-FREE (don't change on retarget) ---

haipipe-paper-seed          SEED (0):    maintain 0-lifecycle/0-seed/0-seed.md: 3 sections (Seed Question, Motivations, Tentative Claim Shape); the venue-FREE contract that keeps a paper possibility alive before evidence matures.

haipipe-paper-claims        CLAIMS (1):  maintain 0-lifecycle/1-claims/1-claims.md, the venue-FREE claim/evidence inventory (supported / weak / GAP), each row tied to an evidence source; venue-neutral H1/H2/H3; emits needs and backfills probe verdicts.

--- VENUE DECISION (pins target journal in STATUS.md) ---

haipipe-paper-venue         VENUE:       recommend + pin the best-fit venue; compiles pack knowledge into 0-lifecycle/2-venue/2-venue.md (Venue Profile + Structural Blueprint + Writing Principles + Fit Assessment, provenance header naming pack + outlet + _venue commit) -- the venue contract the aligned stages read FIRST; gate between venue-free and venue-aligned stages.

--- VENUE-ALIGNED (rewrite on retarget) ---

haipipe-paper-pitch         PITCH (2):   maintain 0-lifecycle/2-pitch/2-pitch.md, the venue-ALIGNED cover letter and one-minute story; owns Editor's Chair Test, [primary] claim designation, venue-specific RQ framing.

haipipe-paper-narrative     NARRATIVE (3): maintain 0-lifecycle/3-narrative/3-narrative.md, the venue-ALIGNED, section-mirrored, evidence-tracked story built from the claim ledger; every beat carries a readiness tag.
```

### Display -- what the reader sees (venue-ALIGNED)

```
haipipe-paper-display       DISPLAY (4): 0-lifecycle/4-display/4-display.tex + PDF (the gallery, the ONLY compiled stage) plus per-unit README.md, float.tex, and preview.pdf under 0-displays/displayNN-<slug>/. Keeps display items tied to claim, evidence source, section, and caption. Consults 2-venue.md for the display set and hero rule (Structural Blueprint display units + Writing Principles display limits; pack fallback when 2-venue.md is absent). Figure-inventory planning (one claim per figure, panel roles, main vs supplement) is folded in as its ref/figure-logic.md. Framework/architecture mode handles Figure 1 candidate rounds before final rendering.
```

### Section editing -- per-section prose work (venue-ALIGNED)

```
haipipe-paper-section-edit  SECTION-EDIT (5): per-section editing hub under 0-lifecycle/5-section-edit/. One folder per section with outline .md, _LOG changelog, _CITATION_ map, _VALUES_ registry; runs the full DRAFT -> PROBE -> REVISE -> CHECK cycle per section and syncs revised prose to 0-sections/*.tex.
```

### Display renderers -- visual assets

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
  folder         scaffold the directory
      ↓
  seed (0)       why this paper might exist (venue-FREE)
      ↓
  claims (1)     claim/evidence inventory: supported / weak / GAP, with evidence sources
                 venue-neutral H1/H2/H3 hypotheses; no [primary], no RQ framing

  VENUE DECISION
  ──────────────────────────────────────
      ↓
  venue          pin target journal in STATUS.md (gate between FREE and ALIGNED)
                 + compile 0-lifecycle/2-venue/2-venue.md, the venue contract the ALIGNED stages read first

  VENUE-ALIGNED (rewrite on retarget)
  ──────────────────────────────────────
      ↓
  pitch (2)      venue-ALIGNED cover letter: Editor's Chair Test, [primary] claim, RQ framing
      ↓
  narrative (3)  venue-ALIGNED evidence-backed arc from the claim ledger
      ↓
  display (4)    venue-ALIGNED display contract: figure/table units, sources, captions, gallery PDF
                 (renders via table / figure / diagram / illustration as needed)
      ↓
  section-edit (5)  per-section DRAFT -> PROBE -> REVISE -> CHECK in 0-lifecycle/5-section-edit/,
                    syncing venue-quality prose to 0-sections/*.tex
```

After the lifecycle spine, whole-paper build/submit tooling lives under `3-build-submit/` (`haipipe-paper-folder`, `haipipe-paper-build-*`, `haipipe-paper-edit-*` for compile checks, restructuring, submission audits).

**Retarget rule:** when the venue changes, seed and claims stay unchanged (venue-FREE). Pitch, narrative, display, and section-edit all rewrite for the new venue.

**Venue consumption rule:** the venue-aligned stages read the paper's `0-lifecycle/2-venue/2-venue.md` FIRST -- pitch: Venue Profile + Fit Assessment; narrative: Structural Blueprint beats + Writing Principles; display: Structural Blueprint display units + Writing Principles display limits; section-edit: the per-section Structural Blueprint block + Writing Principles. Direct `_venue/` pack reads are (a) the fallback when `2-venue.md` is absent (venue stage not yet run, or a pack-less venue; no pack at all = no venue inputs) and (b) deep dives following the `[source: ...]` tags recorded in `2-venue.md` into `_venue/playbook-<slug>/<journal>/...`. If `2-venue.md`'s recorded pack commit is behind the current `_venue` HEAD, stages note "venue contract stale -- consider /haipipe-paper-venue refresh" but still use `2-venue.md` (never silently re-read packs).

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
    function = "folder"    -> Skill("haipipe-paper-folder", args)

    # Display renderers carry the display- prefix; map the short verb explicitly:
    function = "table"          -> Skill("haipipe-paper-display-table", args)
    function = "figure"         -> Skill("haipipe-paper-display-figure", args)
    function = "diagram"        -> Skill("haipipe-paper-display-diagram", args)
    function = "illustration"   -> Skill("haipipe-paper-display-illustration", args)        # DEFAULT (Codex bridge)
    function = "illustration-gemini" -> Skill("haipipe-paper-display-illustration-gemini", args)  # fallback

    # Lifecycle stages keep the plain haipipe-paper-<stage> name:
    function = else        -> Skill("haipipe-paper-<function>", args)
        (seed | claims | venue | pitch | narrative | display | section-edit)

    Special: "figure-plan", "framework" -> Skill(
      "haipipe-paper-display", "framework " + args
    )
             (figure-inventory planning lives inside display;
              see haipipe-paper-display/ref/figure-logic.md)

    Special: bare section reference ("§3", "section 3", or a section name
             like "introduction" / "methods") -> Skill(
      "haipipe-paper-section-edit", args
    )
```

---

Function Keyword Map
---------------------

```
folder, scaffold, bootstrap, init, new paper dir,
  create folder, Paper-*                              -> folder

seed, paper seed, why this paper,
  paper possibility                                   -> seed       (venue-FREE)

claims, claim ledger, supported, weak, GAP,
  claim gap, evidence map, overclaim, H1, H2, H3     -> claims     (venue-FREE)

venue, which journal, where to submit, venue fit,
  recommend journal, journal selection, pick venue    -> venue      (decision gate)

pitch, paper pitch, one-minute story, hook, surprise,
  so what, story trajectory, pitch provenance,
  cover letter, editor's chair, primary claim         -> pitch      (venue-ALIGNED)

narrative, story, design contract, 3-narrative,
  claim-evidence matrix, core claim                   -> narrative  (venue-ALIGNED)

display, display layer, 0-displays, 4-display,
  ready to input, preview pdf, float.tex, caption,
  figure table contract, display contract, gallery,
  figure planner, figure inventory, panel roles,
  main vs supplement, what figures                    -> display    (venue-ALIGNED)

section-edit, section edit, edit section, editing,
  section scaffold, outline narrative, polish section,
  §N, section N, 5-section-edit, introduction, methods,
  results section, discussion section                 -> section-edit (venue-ALIGNED)

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
seed, paper-seed                                 -> seed
claims, claim, ledger                            -> claims
venue, journal, submit-to                        -> venue
pitch, paper-pitch, storycard, cover-letter      -> pitch
narrative, story, contract                       -> narrative
display, displays, disp,
  figure-plan, fp, figplan, fw                   -> display
section-edit, section, sec, edit, §N             -> section-edit
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
📐 haipipe-paper-lifecycle -- paper structural work

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
      display        4-display: display contract + units (only compiled stage; figure-inventory planning via its ref/figure-logic.md)
      section-edit   5-section-edit: per-section DRAFT->PROBE->REVISE->CHECK hub

  Display renderers (data-driven):
    table          Data-driven LaTeX tables (booktabs/stars/panels)
    figure         Data-driven plots (line/bar/scatter/heatmap/box)

  Display renderers (concept):
    diagram        Deterministic vector diagrams (JSON -> SVG)
    illustration   AI concept illustration -- DEFAULT, Codex bridge
    illustration-gemini  AI concept illustration -- Gemini fallback
    framework      Candidate framework/architecture figure planning (Figure 1 style)

  Pipeline: folder -> seed (FREE) -> claims (FREE) -> [venue] -> pitch (ALIGNED) -> narrative (ALIGNED) -> display (ALIGNED, + table/figure/diagram/illustration) -> section-edit (ALIGNED)

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

Stage skills additionally close every reply with the full closing block (simplified tail + stage line + phase line) defined in `../../haipipe-paper/SKILL.md` (Closing Block section); the stage line renders from disk via `../../haipipe-paper/stage-strip.sh`.

---

Relation to Parent Orchestrator
--------------------------------

`haipipe-paper` (in `paper/haipipe-paper/`) is the top-level paper router + Console. It resolves status and consults the paper's `0-lifecycle/2-venue/2-venue.md` for venue fit (falling back to the target's profile in `_venue/playbook-<venue>` only when no venue contract exists yet). This orchestrator (`haipipe-paper-lifecycle`) is the direct entry for structural work -- either routed from the Console or invoked by the user directly.

```
haipipe-paper (router)  -- consults 2-venue.md for venue fit (pack fallback pre-pin)
            |                (utd-is: misq/isr/ms-is; pnas; nature-portfolio; jama; clinical; grant; patent)
            v
haipipe-paper-lifecycle (this orchestrator)
  VENUE-FREE:
  |-- folder             (lives in 3-build-submit/, routed from here)
  |-- seed (0)
  |-- claims (1)
  VENUE DECISION:
  |-- venue              (pin target journal in STATUS.md)
  VENUE-ALIGNED:
  |-- pitch (2)          (cover letter: Editor's Chair, [primary], RQ framing)
  |-- narrative (3)
  |-- display (4)        (only compiled stage; renders via table / figure / diagram / illustration
  |                       + illustration-gemini fallback; planning in its ref/figure-logic.md)
  +-- section-edit (5)   (per-section hub in 0-lifecycle/5-section-edit/; internally dispatches
                          2-phase/ DRAFT->PROBE->REVISE->CHECK workers)

Every stage skill runs its phases through the shared 2-phase/ workers
(haipipe-paper-draft / -probe / -revise / -checker); users never invoke those directly.
Whole-paper build/submit tools (haipipe-paper-build-*, haipipe-paper-edit-*) live in 3-build-submit/.
```
