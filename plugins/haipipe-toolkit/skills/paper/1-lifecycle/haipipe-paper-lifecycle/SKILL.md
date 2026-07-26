---
name: haipipe-paper-lifecycle
description: "Orchestrator for the paper structure lifecycle (1-lifecycle). Routes to stage specialists across the venue-free/venue-aligned boundary: seed, resource, claims are venue-FREE; venue pins the journal; pitch, narrative, display, section-edit are venue-ALIGNED (rewrite on retarget). Also routes to display renderers: table, figure, diagram, illustration. Use for any structural work on a paper before or during writing. Trigger: paper structure, paper pitch, scaffold paper, paper outline, paper architecture, resource, display layer, figure plan, section edit, /haipipe-paper-lifecycle."
argument-hint: "[function] [paper-path-or-input] [args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "0.4.0"
  last_updated: "2026-07-26"
  summary: "Router for the 1-lifecycle stage spine: folder, seed (0), resource (1a), claims (1b) [venue-FREE] -> venue (gate) -> pitch (2), narrative (3), display (4), section-edit (5) [venue-ALIGNED], plus the display renderer family. Stage skills run DRAFT -> PROBE -> REVISE -> CHECK internally via 2-phase/ workers; this router never routes users to phase skills. Two modes: depth-first per-stage cycles for single-stage work, and GLOBAL-PASS (draft all stages breadth-first, consolidate probes once via `probe plan`, batch the handoff, harvest, then REVISE/CHECK per stage). Resource is stage 1a and claims is 1b (like 2-venue then 2-pitch within stage 2); nothing renumbers. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-lifecycle (orchestrator)
==============================================

User-facing entry for **paper structural work** -- everything that decides *what the paper is* before prose exists, or when the argument needs rethinking.
This is the **Plan cycle** in the paper mental model (see `paper/README.md`, `../ref/03-paper-lifecycle.md`, and `../ref/04-lifecycle-map.md`).

The lifecycle has a **venue-free / venue-aligned boundary**.
Seed, resource and claims are venue-FREE (they don't change when you retarget to a different journal -- what a paper NEEDS to exist does not depend on where you send it).
Venue is the decision gate that pins the target journal in `S-Venue-0-venue.md` frontmatter.
Pitch, narrative, display, and section-edit are venue-ALIGNED (they rewrite when you retarget).

The orchestrator owns routing only.
Each stage specialist owns its own workflow, inputs, and outputs.
The orchestrator never generates narrative, outlines, figures, or diagrams itself.

```
/haipipe-paper-lifecycle                                -> dashboard (list specialists + pipeline)
/haipipe-paper-lifecycle folder <args>                  -> scaffold paper directory (haipipe-paper-folder)
/haipipe-paper-lifecycle seed <args>                    -> 0-lifecycle/0-seed/0-seed.md (venue-FREE)
/haipipe-paper-lifecycle resource <args>                -> 0-lifecycle/1-work/1a-resource.md (venue-FREE prerequisite contract)
/haipipe-paper-lifecycle claims <args>                  -> 0-lifecycle/1-work/1b-claims.md (venue-FREE claim ledger)
/haipipe-paper-lifecycle venue <args>                   -> 0-lifecycle/2-venue/S-Venue-0-venue.md: the `venue:` pin in its frontmatter + the venue contract in its body (decision gate)
/haipipe-paper-lifecycle pitch <args>                   -> 0-lifecycle/2-venue/2b-pitch.md (venue-ALIGNED cover letter)
/haipipe-paper-lifecycle narrative <args>               -> 0-lifecycle/2-venue/3-narrative.md (venue-ALIGNED design contract)
/haipipe-paper-lifecycle display <args>                 -> the display pages + displays/displayNN-<slug>/ units (the only compiled stage)
/haipipe-paper-lifecycle section-edit <args>            -> 0-lifecycle/4-main/ per-section editing hub
/haipipe-paper-lifecycle table <args>                   -> data-driven LaTeX tables (haipipe-display-table)
/haipipe-paper-lifecycle figure <args>                  -> data-driven plots (haipipe-display-figure)
/haipipe-paper-lifecycle diagram <args>                 -> deterministic vector diagrams / SVG (haipipe-display-diagram)
/haipipe-paper-lifecycle illustration <args>            -> AI concept illustration, Codex bridge (haipipe-display-illustration)
/haipipe-paper-lifecycle framework <args>               -> display framework mode (candidate rounds, selection, handoff)
/haipipe-paper-lifecycle "<natural language>"           -> infer function, dispatch
```

**Phase-verb pass-through**: a trailing `draft | probe | revise | check` after any stage's args is a PHASE VERB — forward it verbatim, with the STAGE KEY leading, to the one stage skill (e.g. `section-edit 4-llmtrait revise` → `Skill("haipipe-paper-stage", args="section-edit 4-llmtrait revise")`).
The verb picks which phase the stage drives; the stage still dispatches its internal workers.

---

Two-Axis Model (stages x phases)
---------------------------------

Stage skills are the USER-FACING surface.
Internally, each stage skill drives the shared phase cycle **DRAFT -> PROBE -> REVISE -> CHECK** by dispatching the internal workers in `2-phase/` (`haipipe-paper-draft`, `haipipe-paper-probe*`, `haipipe-paper-revise*`, `haipipe-paper-check`).
TWO human gates: DRAFT ends at a hard STOP for the user's structure review (`[GATE]` logged; the user's verb advances), and CHECK is the quality gate.
PROBE and REVISE are agent-only between them; REVISE is proof-carrying (`workers:` line in `_LOG`).
The agent never self-advances past a gate.

**This router routes users to STAGE skills only -- never to phase skills.**
Phase dispatch is each stage skill's internal business.
If a request sounds like a phase ("gather citations for §3", "polish the intro"), route to the owning stage skill (usually section-edit) and let it dispatch.

Stage artifacts are markdown S pages (`S-<Family>-<n>-<slug>.md`, one family one folder) for every stage except display, which also compiles to `.tex` + PDF (you need to SEE rendered figures/tables).
Stage gates and the illuminate loop are shared conventions: `../ref/08-stage-gate.md`, `../ref/09-stage-illuminate.md`.

---

Specialists
-----------

### Foundation -- what folder + what story

Stage rows below name the STAGE KEY. All eight are driven by the single skill `haipipe-paper-stage`,
which loads that key's contract from `haipipe-paper-stage/stages/<order>-<key>/stage.md`.


```
haipipe-paper-folder                  SCAFFOLD:  minimal Board-first scaffold (README + .gitignore + 0-lifecycle/ with board.md and ONE Seed page). No STATUS.md. Everything else is absent-until-allocated; the driver tex / sections/ / 2-src/compile.sh are a later on-request upgrade via haipipe-paper-scaffold. Repo+submodule wiring belongs to /haipipe-paper enter (get-or-create on a missing path).

--- VENUE-FREE (don't change on retarget) ---

seed                    SEED (0):    maintain 0-lifecycle/0-seed/0-seed.md: 3 sections (Seed Question, Motivations, Tentative Claim Shape); the venue-FREE contract that keeps a paper possibility alive before evidence matures.

resource            RESOURCE (1a): maintain 0-lifecycle/1-work/1a-resource.md, the venue-FREE prerequisite contract: what must EXIST for this paper to be testable, does it exist, and can it CARRY the claim? Two sections only -- Demand (one N<n> per hypothesis, keyed on H<n>) and Questions (one Q<n>, and its A when the answer lands). Scope is DATA + MODELS + PRODUCING-CODE (data is the bulk, not the boundary). The stage ASKS; the probe layer ROUTES -- it mints no PP ids and picks no probe types. Cleavage: task-for-data / task-for-algo (ingredients) belong HERE; task-for-fit (train the model) + task-for-eval (evaluate) are CLAIMS'. Stage 1a; claims is 1b. Exits: proceed / reseed / park.

claims                CLAIMS (1b):  maintain 0-lifecycle/1-work/1b-claims.md, the venue-FREE claim ledger AND the home of each claim's status (supported | refuted | inconclusive); venue-neutral H1/H2/H3, each claim tied to a probe entry's answering QA file. Claims RUNS THE EXPERIMENT (train the model + evaluate); it reads the entry's `### a-executor` and writes its own a-consumer in the stage doc.

--- VENUE DECISION (pins target journal in S-Venue-0-venue.md) ---

venue                  VENUE:       recommend + pin the best-fit venue; compiles pack knowledge into 0-lifecycle/2-venue/2a-venue.md (Venue Profile + Structural Blueprint + Writing Principles + Fit Assessment, provenance header naming pack + outlet + venue commit) -- the venue contract the aligned stages read FIRST; gate between venue-free and venue-aligned stages.

--- VENUE-ALIGNED (rewrite on retarget) ---

pitch                  PITCH (2):   maintain 0-lifecycle/2-venue/2b-pitch.md, the venue-ALIGNED cover letter and one-minute story; owns Editor's Chair Test, [primary] claim designation, venue-specific RQ framing.

narrative                   NARRATIVE (3): maintain 0-lifecycle/2-venue/3-narrative.md, the venue-ALIGNED, section-mirrored, evidence-tracked story built from the claim ledger; every beat carries a readiness tag.
```

### Display -- what the reader sees (venue-ALIGNED)

```
display              DISPLAY (4): the gallery (the ONLY compiled stage) plus per-unit README.md, float.tex, and preview.pdf under displays/displayNN-<slug>/. Keeps display items tied to claim, evidence source, section, and caption. Consults S-Venue-0-venue.md for the display set and hero rule (Structural Blueprint display units + Writing Principles display limits; pack fallback when S-Venue-0-venue.md is absent). Figure-inventory planning (one claim per figure, panel roles, main vs supplement) is folded in as its figure-logic.md. Framework/architecture mode handles Figure 1 candidate rounds before final rendering.
```

### Section editing -- per-section prose work (venue-ALIGNED)

```
section-edit                SECTION-EDIT (5): one S page per section under 0-lifecycle/4-main/ (and 5-appendix/). Each page carries the outline, its state, and its own ## Log; runs the full DRAFT -> PROBE -> REVISE -> CHECK cycle per section and syncs revised prose to sections/*.tex.
```

### Display renderers -- visual assets

```
haipipe-display-table           TABLE:   data-driven LaTeX tables (booktabs/stars/panels) from an aggregated CSV/JSON

haipipe-display-figure          PLOT:    data-driven publication plots from experiment results (plots only)

haipipe-display-diagram         VECTOR:  deterministic architecture/workflow/pipeline diagrams from structured JSON -> editable SVG

haipipe-display-illustration    AI-IMG:  AI concept illustration via the local Codex app-server bridge (native image gen)
```

---

Natural Pipeline Order
----------------------

The specialists are designed to flow in sequence, though any can be invoked standalone.
The typical first-pass order:

```
  VENUE-FREE (don't change on retarget)
  ──────────────────────────────────────
  folder         scaffold the directory
      ↓
  seed (0)       why this paper might exist (venue-FREE)
      ↓
  resource (1a)   what must EXIST for this paper to be testable, does it exist, can it CARRY
                 the claim? Demand (N<n> per H<n>) + Questions (Q<n> + A). Data, models, and
                 producing-code alike. Shares the number 1 with claims; renumbers nothing.
      ↓
  claims (1b)     claim/evidence inventory: supported / weak / GAP, with evidence sources
                 venue-neutral H1/H2/H3 hypotheses; no [primary], no RQ framing

  VENUE DECISION
  ──────────────────────────────────────
      ↓
  venue          pin target journal in S-Venue-0-venue.md (gate between FREE and ALIGNED)
                 + compile 0-lifecycle/2-venue/2a-venue.md, the venue contract the ALIGNED stages read first

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
  section-edit (5)  per-section DRAFT -> PROBE -> REVISE -> CHECK in 0-lifecycle/4-main/,
                    syncing venue-quality prose to sections/*.tex
```

After the lifecycle spine, whole-paper delivery tooling lives under `3-deliver/`, routed by its own umbrella `haipipe-paper-deliver` (1-build: scaffold/restructure/conform/folder · 2-audit · 3-polish · 4-ship).

Global-pass mode (breadth-first — the whole-paper cycle)
---------------------------------------------------------

The per-stage DRAFT->PROBE->REVISE->CHECK cycle above is DEPTH-FIRST — right for maturing one stage.
For a whole paper, prefer the GLOBAL-PASS order (JL ruling 2026-07-11): probes planned stage-by-stage duplicate questions and miss shared gating dependencies; the evidence needs of a paper only become visible once every stage has a draft.

```text
① DRAFT SWEEP     draft ALL stages in pipeline order, gates only on structure
                  ({VAL:?} placeholders + GAP markers + `planned` PP skeletons fine;
                  venue still pins BEFORE the venue-ALIGNED drafts)
② PROBE-PLAN      /haipipe-paper probe plan — the cross-stage consolidation:
                  merge duplicate questions (one ENTRY, many `### q-consumer` bullets), author
                  the dispatch DAG into 1-probes/README.md Campaign section
                  [HUMAN GATE — present the campaign, stop]
③ DISPATCH BATCH  probe run — MATCH first (most sections close on T2 REUSE, for
                  free); only what MATCH cannot close is dispatched, per the DAG
                  (gating sections first). A DEPENDENT section waits until its
                  upstream section's `target:` QA FILE EXISTS ON DISK — i.e. the
                  upstream reached `state: answered`. the QA file on disk
                  is the only signal a DAG may wait on.
④ RUN             the task/discovery orchestrators run their own qa gate and
                  write <task-folder>/QA/<n>-<slug>.md (often a SEPARATE concurrent
                  session — the `### q-executor` block in the entry is the bridge,
                  and it survives a dead session with zero files bank-side)
⑤ HARVEST         a PROBE re-run re-resolves each `commissioned` entry's
                  `**target**:`, `ls` its QA file, and lands the `### a-executor`
                  + each Q-consumer's a-consumer in its stage doc
                  + the 1b-claims.md flip + the harvest lanes
                  (query-once: landed answers are read from registries, never
                  re-queried) → then REVISE + CHECK stage by stage
```

Stage gates are unchanged — a stage's CHECK still verifies ITS cards and registries; the global pass only reorders WHEN drafting and probing happen.
The campaign rules ARE the five steps above — this block is where they live.
The per-ENTRY fields a campaign row manipulates (`route:` / `bank:` / `target:` / `state:`) are owned by `probe/haipipe-probe/SKILL.md` "The probe file"; the campaign never redefines them, it only sequences which entries are dispatched and in what order.

**Retarget rule:** when the venue changes, seed, resource and claims stay unchanged (venue-FREE).
Pitch, narrative, display, and section-edit all rewrite for the new venue.

**Venue consumption rule:** the venue-aligned stages read the paper's `0-lifecycle/2-venue/2a-venue.md` FIRST -- pitch: Venue Profile + Fit Assessment; narrative: Structural Blueprint beats + Writing Principles; display: Structural Blueprint display units + Writing Principles display limits; section-edit: the per-section Structural Blueprint block + Writing Principles.
Direct `venue/` pack reads are (a) the fallback when `2a-venue.md` is absent (venue stage not yet run, or a pack-less venue; no pack at all = no venue inputs) and (b) deep dives following the `[source: ...]` tags recorded in `2a-venue.md` into `venue/playbook-<slug>/<journal>/...`.
If `2a-venue.md`'s recorded pack commit is behind the current `venue` HEAD, stages note "venue contract stale -- consider /haipipe-paper-stage venue refresh" but still use `2a-venue.md` (never silently re-read packs).

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
    function = "table"          -> Skill("haipipe-display-table", args)
    function = "figure"         -> Skill("haipipe-display-figure", args)
    function = "diagram"        -> Skill("haipipe-display-diagram", args)
    function = "illustration"   -> Skill("haipipe-display-illustration", args)        # Codex bridge

    # Lifecycle stages ALL go through ONE skill. There are no longer per-stage skills:
    function in (seed | resource | claims | venue | pitch | narrative | display | section-edit)
        -> Skill("haipipe-paper-stage", args="<function> <the rest of args>")
        The stage key is the FIRST positional. `haipipe-paper-stage` resolves it against
        stages/index.yml and loads only that stage's stages/<order>-<key>/stage.md.
        ⚠️ section-edit's unit slides right: `section-edit 4-llmtrait revise`.

    function = else        -> Skill("haipipe-paper-<function>", args)
        (the non-stage skills: enter, folder, probe, round, review, …)

    Special: "figure-plan", "framework" -> Skill(
      "haipipe-paper-display", "framework " + args
    )
             (figure-inventory planning lives inside display;
              see haipipe-paper-stage/stages/4-display/figure-logic.md)

    Special: bare section reference ("§3", "section 3", or a section name
             like "introduction" / "methods") -> Skill(
      "haipipe-paper-stage", args="section-edit …"
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

resource, prerequisite, do we have the data,
  does the checkpoint exist, can this corpus carry
  the claim, demand, what must exist, 1-resource      -> resource   (venue-FREE)

claims, claim ledger, supported, weak, GAP,
  claim gap, evidence map, overclaim, H1, H2, H3     -> claims     (venue-FREE)

venue, which journal, where to submit, venue fit,
  recommend journal, journal selection, pick venue    -> venue      (decision gate)

pitch, paper pitch, one-minute story, hook, surprise,
  so what, story trajectory, pitch provenance,
  cover letter, editor's chair, primary claim         -> pitch      (venue-ALIGNED)

narrative, story, design contract, 3-narrative,
  claim-evidence matrix, core claim                   -> narrative  (venue-ALIGNED)

display, display layer, displays/, display units,
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
  生成图表                                              -> illustration   (Codex bridge)
```

Function aliases (positional):
```
folder, scaffold, bootstrap, init                -> folder
seed, paper-seed                                 -> seed
resource, resources, prereq, prerequisite, need  -> resource
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
illustration, illust, ai-img, image2, codex      -> illustration
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
      resource       1-resource: what must EXIST for this paper to be testable (Demand + Questions)
      claims         1-claims: claim/evidence inventory (venue-neutral H1/H2/H3)
    VENUE DECISION:
      venue          pin target journal in S-Venue-0-venue.md
    VENUE-ALIGNED:
      pitch          2-pitch: cover letter + one-minute story (Editor's Chair, [primary], RQ framing)
      narrative      3-narrative: evidence-backed arc
      display        4-display: display contract + units (only compiled stage; figure-inventory planning via its figure-logic.md)
      section-edit   5-section-edit: per-section DRAFT->PROBE->REVISE->CHECK hub

  Display renderers (data-driven):
    table          Data-driven LaTeX tables (booktabs/stars/panels)
    figure         Data-driven plots (line/bar/scatter/heatmap/box)

  Display renderers (concept):
    diagram        Deterministic vector diagrams (JSON -> SVG)
    illustration   AI concept illustration -- Codex bridge
    framework      Candidate framework/architecture figure planning (Figure 1 style)

  Pipeline: folder -> seed (FREE) -> resource (FREE) -> claims (FREE) -> [venue] -> pitch (ALIGNED) -> narrative (ALIGNED) -> display (ALIGNED, + table/figure/diagram/illustration) -> section-edit (ALIGNED)

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

`haipipe-paper` (in `paper/haipipe-paper/`) is the top-level paper router + Console.
It resolves status and consults the paper's `0-lifecycle/2-venue/2a-venue.md` for venue fit (falling back to the target's profile in `venue/playbook-<venue>` only when no venue contract exists yet).
This orchestrator (`haipipe-paper-lifecycle`) is the direct entry for structural work -- either routed from the Console or invoked by the user directly.

```
haipipe-paper (router)  -- consults 2a-venue.md for venue fit (pack fallback pre-pin)
            |                (utd-is: misq/isr/ms-is; pnas; nature-portfolio; jama; clinical; grant; patent)
            v
haipipe-paper-lifecycle (this orchestrator)
  VENUE-FREE:
  |-- folder             (lives in 3-deliver/, routed from here)
  |-- seed (0)
  |-- resource (1a)       (prerequisite contract: Demand + Questions; stage 1a, claims is 1b,
  |                       as 2a-venue/ and 2b-pitch/ split stage 2)
  |-- claims (1b)
  VENUE DECISION:
  |-- venue              (pin target journal in S-Venue-0-venue.md)
  VENUE-ALIGNED:
  |-- pitch (2)          (cover letter: Editor's Chair, [primary], RQ framing)
  |-- narrative (3)
  |-- display (4)        (only compiled stage; renders via table / figure / diagram / illustration;
  |                       planning in its figure-logic.md)
  +-- section-edit (5)   (per-section hub in 0-lifecycle/4-main/; internally dispatches
                          2-phase/ DRAFT->PROBE->REVISE->CHECK workers)

Every stage skill runs its phases through the shared 2-phase/ workers
(haipipe-paper-draft / -probe / -revise / -checker); users never invoke those directly.
Whole-paper delivery tools live in 3-deliver/ (umbrella: haipipe-paper-deliver).
```
