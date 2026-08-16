# haipipe-paper · v0.7.0
state: 🟡 PARTIAL · account written; the acceptance test is open in Items
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

**Now the one door (0.5.0, 260805).** Thin-paper phase 2 folded `haipipe-paper-enter`, `haipipe-paper-lifecycle`, and `haipipe-paper-stage` into this one skill: it owns `stages/index.yml` resolution, `create-page.py`, the `probe/` tooling, and `ref/` directly. Page work is handed to `haipipe-page` (WORK ON / RUN); `board/page-phases/` own DPRC. Each stage.md gained `checker:` and `craft:` fields, honored by `haipipe-page-for-stage` 0.5.0; the workers dissolved to stage data files.

## Opening
Why does the Paper family need one public front door, rather than asking a writer to know the lifecycle, stage, phase, delivery, and evidence workers in advance?

This page tests whether `haipipe-paper` makes the first decision correctly: which paper is in scope and which kind of work the request actually asks for.
It should make the route legible without becoming a second implementation of any specialist.

## Diagram
<!-- haipipe:skill:tree:start a07100b50455f7a8 paper/haipipe-paper -->

**What `haipipe-paper` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-paper/
  fn/
    compile.md                     238 ln  Door verb: compile (LaTeX target to verified PDF)
    conform.md                     126 ln  Door verb: conform (paper-folder conformance audit)
    diffpdf.md                     255 ln  Door verb: diffpdf (tracked-changes PDF against a baseline)
    digest.md                      172 ln  Digest (condense the session into routed feedback)
    feedback.md                    245 ln  Feedback (capture skill feedback, route at capture, fix later)
    folder.md                      165 ln  Door verb: folder (paper-folder scaffold)
    probes.md                      191 ln  Paper probe routing
    project.md                     109 ln  Door verb: project (S pages to isolated LaTeX candidates)
    to-overleaf.md                 243 ln  Door verb: to-overleaf (two-way Overleaf sync)
    to-word.md                     164 ln  Door verb: to-word (one stage page to a coauthor .docx)
  probe/
    check-probe-cards.sh             3 ln
    check_topic_entries.py         171 ln  Verify the Paper S03/S04 nested QA-probe contract.
    per-stage-dispatch.md          160 ln  Per-stage dispatch reference (paper PROBE)
    topic-entry-contract.md         32 ln  Paper evidence-page and QA-probe contract
  ref/
    diffpdf/
      class-presets.md             154 ln  Class Presets
      compile-pipelines.md          50 ln  Compile Pipelines
      known-bugs.md                186 ln  Known Bugs
    03-paper-lifecycle.md          109 ln  Paper Lifecycle
    04-lifecycle-map.md            158 ln  Paper Lifecycle Map
    08-stage-gate.md               234 ln  Stage Gate Protocol
    09-stage-illuminate.md          69 ln  Illuminate + Elicit Protocol
    comment-protocol.md            105 ln  Comment Protocol
    enter-console.md               102 ln  Paper Console (the enter/status procedure)
    paper-folder-anatomy.md        246 ln  haipipe-paper/ref : paper folder anatomy
    paragraph-indexing.md          109 ln  2-phase / shared — paragraph indexing
    prose-quality.md                48 ln  Prose Quality Rules (Universal)
    sentence-format.md              71 ln  2-phase / shared — sentence format
    tex-file-anatomy.md            105 ln  2-phase / shared — tex file anatomy
  scripts/
    diffpdf/
      templates/
        config.sh.tpl               30 ln
        README.md.tpl               69 ln
        silenced-changes.txt.tpl    27 ln
      detect-paper-class.sh        139 ln
      make-diff.sh                 245 ln
      silence-minor-changes.pl     143 ln
    project/
      agents/
        openai.yaml                  4 ln
      references/
        projection-manifest.md      79 ln  Projection manifest v1
      scripts/
        project_runtime.py        1235 ln  Manifest-driven, gated Markdown-to-LaTeX projection runtime.
        test_project_runtime.py    218 ln  Disposable safety and determinism tests for project_runtime.
      project.py                     8 ln  CLI entry point for the paper door's project-verb runtime (fn/project.md).
    to-word/
      build-both.sh                 54 ln
      docx2pdf.py                  239 ln  docx2pdf.py -- render a .docx we generated into a PDF, comments and all.
      md2docx.py                  1228 ln  md2docx.py -- one stage page's ## Content becomes a .docx whose APPARATUS
      md2tex.py                    184 ln  md2tex.py -- one or more stage pages become LaTeX sections, and a paper.
    check_structure.sh             273 ln
  stages/
    CONTRACT.md                    226 ln  The stage contract form
    index.yml                       41 ln
    section-kinds.yml               90 ln
  CHANGELOG.md                     375 ln  haipipe-paper — Changelog
  check-contracts.py               209 ln  Check every stage contract against stages/CONTRACT.md, and against a real paper.
  create-page.py                   445 ln  Create one paper lifecycle S page through the Board's shell primitive.
  section-stats.py                 302 ln  Measure an S page's prose FORM and print the structure block for `## Diagram`.
  SKILL.md                         699 ln  Skill: haipipe-paper (the door)
```

<!-- haipipe:skill:tree:end -->

**How S01-S10 and the board skills work together** (JL 260806, "that is the Diagram I want"): two figures, the shelves then the flow.

```
[1/2] 🗺 THE THREE SHELVES · who owns what

  📄 PAPER FAMILY                🧩 BOARD FAMILY                 🏦 THE BANK
  skills/paper/                  skills/board/                   tasks/ · discoveries/
  ─────────────────────────      ─────────────────────────       ──────────────────
  haipipe-paper  THE DOOR        haipipe-board   build · serve   task-folders
    stages/index.yml (roster)                    check · status  discovery folders
    create-page.py · probe/      haipipe-page  THE ENGINE  QA/<n>-<slug>.md
  S01-opening … S10-round/         page-types/  ten: for-stage,    the answer files
    stage.md  CONTRACT+CRAFT       for-literature, for-value,      everything else
    template.md · craft .md        for-display, for-section …      points at them
    checker scripts                page-phases/ DRAFT PROBE
  venue/  knowledge packs                       REVISE CHECK
                                  sentence · routing · 3 agents

  the WIRE: each stage.md is read DOWN by the door (which stage, which
  phases, which craft) and read BACK UP by for-stage (chain, gate, venue).
  The board never names LaTeX; the paper never restates page logic.
```

```
[2/2] 🔁 ONE CALL, END TO END

  JL: /haipipe-paper claims          (or: work on <page> · probe · enter)
   │
   ▼ 📄 DOOR
   ① stages/index.yml ── verb → stage key ("claims", row 1b)
   ② S02-work/claims/stage.md ── load exactly ONE:
        phases:[draft,probe,revise,check] · gates:[check] · probe_depth:0
        checker: probe/check-probe-cards.sh · craft:[citation, values]
   ③ page missing? create-page.py → board stage.py → S-Work-C-claims.md born
   │
   ▼ 🧩 ENGINE  (haipipe-page takes the page)
   ④ TYPE from the filename   S-Work-C → for-stage
        (register route: → for-literature/-value · page-type: → for-display…)
   ⑤ PHASE by the authority test   promise→DRAFT · unknown→PROBE ·
                                   realize→REVISE · judge→CHECK
   ⑥ load order  base → type → phase → the stage's craft: files
   │
   │        PROBE crosses the wall ─────────────────────────────────┐
   │   Q-consumer (stake, stays on the S page)                      ▼
   │   q-executor → probes/L<n>|V<n> entry ──▶ 🏦 orchestrator agents
   │   the entry's a-executor COPIES the answer in ◀───────────────── QA file
   │   the S page only POINTS at the entry; its A-consumer states
   │   what the answer MEANS for the stake · QA file = the true home
   │
   ⑦ CHECK  run the declared checker → fresh judge → human gate [CHECK-JL]
   ⑧ finish  build.py rebuilds the board · Log gains its [PHASE-actor] line

  🚫 the door never writes stage prose · the engine never touches the bank
     directly · the bank never learns the stake. Three shelves, one wire.

  the LOOP CLOSES outside the shelves: ⑧'s rebuilt board/ site renders in
  JL's browser; a click or comment there lands back on the .md through
  serve.py's live layer, and the next call starts from what the reader did.
  The full both-doors wiring, drawn once for the whole system: Skill-6 [1/2].
```

**Click-through**: every box in the figures, as the real file (paths verified 260806).

- 📄 The door and its tools
  [haipipe-paper/SKILL.md](../../paper/haipipe-paper/SKILL.md) · the roster [index.yml](../../paper/haipipe-paper/stages/index.yml) · the page creator [create-page.py](../../paper/haipipe-paper/create-page.py) · the probe checker [check-probe-cards.sh](../../paper/haipipe-paper/probe/check-probe-cards.sh)
- 📄 One stage as data (the claims example from figure 2)
  contract + craft [stage.md](../../paper/S02-work/claims/stage.md) · its skeleton [template.md](../../paper/S02-work/claims/template.md) · craft it declares: [citation-craft.md](../../paper/S03-literature/citation-craft.md) and [values-craft.md](../../paper/S04-value/values-craft.md)
- 🧩 The engine
  the base [haipipe-page/SKILL.md](../../board/haipipe-page/SKILL.md) · the stage type [for-stage/SKILL.md](../../board/page-types/haipipe-page-for-stage/SKILL.md) · the four phases [draft](../../board/page-workflows/haipipe-page-draft/SKILL.md), [probe](../../board/page-workflows/haipipe-page-probe/SKILL.md), [revise](../../board/page-workflows/haipipe-page-revise/SKILL.md), [check](../../board/page-workflows/haipipe-page-check/SKILL.md)
- 🧩 The wall and the run
  the topic-entry core [topic-entry-contract.md](../../board/haipipe-board/ref/topic-entry-contract.md) · the RUN receipts contract [page-run-contract.md](../../board/page-workflows/haipipe-page-workflow/ref/page-run-contract.md) · the rebuild [build.py](../../board/haipipe-board/cli/build.py)

## Content
<!-- haipipe:skill:body:start a07100b50455f7a8 paper/haipipe-paper -->

**haipipe-paper** · `0.7.0` · last shipped 2026-08-06

- folder   `paper/haipipe-paper/`
- tools    Bash, Read, Write, Edit, Grep, Glob, Skill
- summary  Single door for the Board-first paper lifecycle, and the paper family's ONLY registered skill (thin-paper phase 3). S03/S04 are evidence pages (JL 260806): head route: key, one E<n> Content division per Q-executor conversation with #### consumers + #### answer digest, E0 incoming queue, hidden QA-probe records with capital slot headings. History: ./CHANGELOG.md.

### SKILL.md



Skill: haipipe-paper (the door)
================================

User-facing entry for the paper lifecycle, and since 2026-08-05 the ONLY paper router: the old enter/lifecycle/stage routers are retired to `../_old/` and their jobs are internal steps of this one skill.
**The paper family registers exactly ONE skill (this one); everything else is data**: stage contracts under `stages/` + the `SNN-*/` folders, craft files, `fn/` verb procedures, `scripts/` tooling, and `venue/` packs. Since 2026-08-06 (thin-paper phase 3) the former folder/conform, build (compile · diffpdf · project · to-overleaf · to-word), and round/rebuttal skills are `fn/` procedures and the `round` stage of this door; their folders live in `../_old/phase3-260806/`.
The paper lifecycle is a delivery owner: it owns this paper's angle, resources, claims, narrative, section map, displays, maturity, and dated work rounds.
Project-level evidence lives outside the paper in tasks and discoveries; when the paper hits a gap, record a delivery need (see "Delivery Need Routing" below) and route to the evidence worker.

Page logic is NOT restated here: once the stage's S page exists, this door hands it to `haipipe-page` (WORK ON to repair, RUN with a packet to drive it); the `board/page-phases/` contracts own DRAFT, PROBE, REVISE, and CHECK.
The stage's LaTeX-side craft lives in data files each `stage.md` declares under `craft:`; the phase contracts load them after the type contract.
Canonical structure: `../README.md` at the paper skill root.

Read and honor `PREFERENCES.md` (this skill's own folder) WHEN PRESENT: portable, git-tracked global behavioral preferences that survive a machine change. The file does not exist until the first `feedback` flags a global preference (`fn/feedback.md` merge-or-creates it); its absence is normal, never a stall.
`digest` / `feedback` append flagged global prefs there (merge-or-create).

The model: stages × declared phases
------------------------------------

The front door exposes STAGES, not executors.
A stage runs the ordered `phases:` list in its own `stage.md`. Most current
stages declare all four slots:

```text
   DRAFT ──▶ PROBE ──▶ REVISE ──▶ CHECK
   write &   collect    weave in    human
   raise     evidence   the answer  gate
```

PROBE is the ONLY phase that touches the bank, and it reaches it only through a probe file and a clean-context agent — the paper session never runs bank work itself.
Venue currently declares `draft → probe → check`, so its REVISE slot is shown
as `--`. Never invent a phase that the stage did not declare.
There is no generic `discover` or `task` lifecycle verb: a claim-bearing bank need goes through
PROBE, not an inline paper run. The narrow display exception is a missing, non-claim display-ready
aggregate; it is recorded in the Display request and goes to `haipipe-task-for-display`.
A standalone utility question a human wants (a quick lit scan, a data check) goes to the bank's OWN door — `/haipipe-task qa` or `/haipipe-discovery qa` — typed by a person, never proxied by the paper.

Venue coupling: seed + resource + claims are venue-FREE (what a paper NEEDS to
exist does not depend on where you send it); Venue pins the journal on
`0-lifecycle/S01-opening/S-Open-Venue.md`'s `state:` line; pitch, narrative,
display, and section-edit are venue-ALIGNED and consult that page first, with
direct venue-pack reads as fallback when it is absent. Re-targeting re-runs
`venue`; pitch re-couples (new [primary], new RQ framing); resource and claims
stay unchanged. The stage order is `stages/index.yml`'s row order:

```text
folder -> seed -> resource -> claims -> [venue pins] -> pitch -> narrative ->
display (+ renderers) -> section-edit (per section) -> build verbs (fn/) ->
round (per dated round)
```

Maturity is read from artifacts, never assumed, and is orthogonal to the current
stage (ladder: `ref/paper-folder-anatomy.md`). The frontier is DERIVED from each
S page's own `state:` and gate receipt; nothing stores it, so re-running an
early stage is ordinary, not an anomaly (`ref/08-stage-gate.md`).

Verbs
------

One block: verb, aliases and trigger keywords, then where it goes. Stage keys, `enter`, and every fn verb are INTERNAL steps of this skill: no target in this block is a `Skill()` dispatch except the four Display renderers.

```
enter | status | dashboard | preload         -> the CONSOLE step below (open-needs console; GET-OR-CREATE: a missing path offers to create the paper first; also "enter paper", "paper status", "create paper", "new paper folder")
venue | journal | 选刊 | any venue name       -> STAGE step, key venue (recommend + pin; MISQ/ISR/Management Science/Nature/PNAS/JAMA/NEJM/Lancet/clinical/grant/patent all land here)
seed                                         -> STAGE step, key seed        (also "paper seed", "why this paper")
resource | prereq | prerequisite | need      -> STAGE step, key resource    (venue-FREE; what must EXIST for this paper to be testable, does it exist, can it CARRY the claim -- data, model checkpoints and producing-code alike; also "do we have the data", "does the checkpoint exist", "demand", "1-resource")
claims | claim | ledger                      -> STAGE step, key claims      (also "claim gap", "supported", "GAP", "H1/H2/H3")
pitch                                        -> STAGE step, key pitch       (also "cover letter", "one-minute story", "editor's chair")
narrative | story | contract                 -> STAGE step, key narrative
display | figures | figures-tables           -> STAGE step, key display     (also "figure plan", "gallery", "preview pdf")
section-edit | section | sec | §N            -> STAGE step, key section-edit (per-section prose work; also "introduction", "methods", "results section")
table | figure | plot | diagram |
  illustration | figure1 | framework         -> STAGE step, key display first (allocate/bind the unit); then commission the matching Display renderer (haipipe-display-table · -figure · -diagram · -illustration, which stay independently registered skills)
folder | scaffold                            -> INTERNAL fn: load fn/folder.md (Board-first scaffold; the get-or-create branch of `enter` cites it)
conform | structure audit | delete test      -> INTERNAL fn: load fn/conform.md (report-only; runs scripts/check_structure.sh)
build | restructure | project | projection |
  audit | review | claim-audit | reviewer | optimizer |
  polish | consistency | format | typeset |
  compile | diffpdf | overleaf | ship | deliver  -> INTERNAL fns, human-triggered: compile -> fn/compile.md · diffpdf -> fn/diffpdf.md · overleaf -> fn/to-overleaf.md · word -> fn/to-word.md · project/projection -> fn/project.md (tooling under scripts/). (The deliver umbrella and the audit/polish leaf verbs are retired to ../_old/, see ../_old/README.md)
round | rounds                               -> STAGE step, key round (dated work rounds; also "todo", "decisions", "applied")
probe ["<question>"] | probe | probe plan | probe run [topic-id]  -> the topic-entry pool: one nested QA-probe (the entry record) per Q-executor, under its S03 Literature or S04 Value topic (RAISE / SHOW / PLAN / RUN the five-step loop; anatomy + loop: fn/probes.md)
rebuttal                                     -> STAGE step, key round (the Response division of the active round; craft: ../S10-round/rebuttal-craft.md; also "reply to reviewers", "reviewer comments", "OpenReview response", "R1 revision")
feedback "<text>" | feedback list|move       -> fn/feedback.md (resolve BEFORE other parsing)
digest [session] [--dry-run]                 -> fn/digest.md   (resolve BEFORE other parsing)
"<natural language>"                         -> infer via the keywords above, dispatch
```

**Phase-verb pass-through**: a trailing `draft | probe | revise | check` after any stage verb's args is a PHASE VERB — it names which declared phase the page work drives (e.g. `/haipipe-paper section-edit 4-llmtrait revise` → the section's page runs its REVISE phase).
Stage runs stop only at the human gates declared in `gates:`. All current
stages declare `[check]`: DRAFT, PROBE, and (when declared) REVISE run
unattended, then CHECK asks for explicit approval. Never invent or auto-advance
a gate.

Examples:

```
/haipipe-paper enter "examples/Project-PhyPat-Simulation/papers/Paper-PhyPatSim"
/haipipe-paper enter papers/Paper-NewIdea --org jluo41    (missing path -> confirms, then creates)
/haipipe-paper venue "physician trait -> opioid prescribing; observational CMS Medicare" --no-pin
/haipipe-paper claims
/haipipe-paper display "Table 1 + STROBE flow + subgroup forest"
/haipipe-paper probe "NEED-1: expand ex ante audit to all 20 messages"
/haipipe-paper probe run literature-1
```

Routing
--------

Resolution order (first match wins):

```
1. feedback / digest first-token             -> run the fn (before any other parsing)
2. first positional matches a verb/alias     -> that target
3. keyword scan over the whole phrase        -> per the trigger keywords in the Verbs block; a named journal/venue anywhere -> venue
4. a PAGE id or page path on the paper's board (S-<Family>-…, Q…, or a .md
   under 0-lifecycle/) with no stage verb    -> a stage page resolves its stage key first (board_family/unit)
                                                and runs the STAGE step; any other page hands to
                                                haipipe-page WORK ON directly, phase verb passed through.
                                                "work on <page>" is always legal at this door.
5. no args, cwd inside a paper root          -> enter "."
6. no args, no paper root                    -> chooser (below)
7. input but target unclear                  -> ASK; NEVER silently default a venue (venue drives pitch/narrative/display/prose, expensive to redo)
```

A paper root is any directory upward containing `the S pages`, `0-lifecycle/`, `0-*.tex` + `sections/`, or `2-src/compile.sh` + `sections/`.

The STAGE step (one door, one stage file)
------------------------------------------

Every lifecycle stage runs through these steps, inside this skill.

**Step 1 — resolve the stage.**
Read `stages/index.yml` (this skill's folder). This is the ONLY file that enumerates all stages, and it is deliberately
small. Match the verb against each row's `key`; if it is not a key, match the user's phrasing against
`triggers`. Ambiguous or absent → list the keys and ask; never guess a stage.

**Step 2 — load exactly ONE stage.**
Read `stages/<dir>/stage.md`: the contract (frontmatter) plus craft (body). The `dir:` values are
relative to the SOURCE tree; from an installed (flattened) skill they do not resolve, so locate the
one stage.md with `find -L` over the source tree, scoped to the stage key (`-path '*<key>*'`) so no
other stage file is ever surfaced. The same flatten caveat applies to `craft:` and `checker:` paths.

⛔ NEVER read the other stages' `stage.md` files. Loading all eight is a 7.5x context regression
over the per-stage skills this replaces, and it is the specific failure mode this layout exists to
avoid. One invocation, one stage file.

**Step 2a — ensure this stage's Board page exists.**
This door is the only public creator for paper lifecycle pages. Resolve the page by the
selected contract's stable `board_family` + `board_unit`; do not store or guess a literal
filename. If the page is absent, create its Board shell and stage-specific Content scaffold with:

```sh
python3 create-page.py <stage-key> <paper-root>
```

`create-page.py` (this skill's folder) selects the stage template, then calls
`haipipe-board/cli/stage.py new` for the filename, face grammar, listing under Pages, and managed
Stage Contract. It does not draft the research substance. For a dynamic `runs: per-unit` page,
pass `--family`, `--unit`, `--slug`, and `--directory`; Section-edit also requires
`--section-kind`, which resolves the exact template from the Venue page's `Section Styles`
record (or its declared generic fallback). `--template` is a repair/testing override. Do not
create a sidecar request or handoff file; unfinished work stays in the page's `## Aims`, with
its current fact in `## States`.

**Step 3 — hand the page to the page layer.**
Phase driving is NOT this door's: with the page resolved, call `haipipe-page` (WORK ON to
repair one page; RUN with a raw-material packet to drive it through its declared phases). The
`board/page-phases/` contracts own DRAFT, PROBE, REVISE, and CHECK; the shared probe model is
`probe/haipipe-probe/SKILL.md` and the paper-side loop is `fn/probes.md`.
Two declarations in the stage.md feed that hand-off:

```text
craft:     data files the DRAFT/REVISE phases load LAST, after the type
           contract (the dissolved workers/ leaves live on as these files)
checker:   the script CHECK runs before judging (see Step 4)
```

- `phases:` is a LIST, not a type. venue declares `[draft, probe, check]`. Run what the stage
  declares; never pad a list to four.
- INVARIANT: `phases` always ends with `check`. That is the human gate.
- `runs: per-unit` means the phase list runs once PER UNIT (section-edit's grain; the unit is
  positional 2, after the stage key).
- `gates:` declares this stage's HUMAN stops, the same way `phases:` declares its phases. The
  default is `[check]` — ONE gate, at the end. DRAFT, PROBE and REVISE run unattended.
  Never open a gate a stage did not declare, and never skip one it did.
- `commissions:` names worker skills this stage hands units to (display → the four renderers).
  Those workers stay independently registered and are invoked by name.
- Board mapping: after any phase changes the artifact, sync the resolved S face in the same
  turn (`state:`, `## Aims`, `## States`, `## Log`), then rebuild the board. The S face's
  `requires:` / `style-from:` / `provides:` are board contracts; refresh the managed
  `## Stage Contract` span with `haipipe-board/cli/stage.py`, and run explicit `stage.py sync`
  before CHECK if the board reports a stale contract.

**Step 3a — the PROBE ceiling.**
`probe_depth:` is what makes a single CHECK gate safe: PROBE may only dispatch work whose cost
sits at or below the ceiling, so an unattended run cannot spend.

```text
depth  bank:    what it takes                        cost
  0    reuse    results already answer it            free — nothing runs
  1    run      old script, new config               costs
  2    code     must write new code first            costs
  3    new      open a new task-folder               costs most
```

The ladder is the bank's own (`task/haipipe-task/fn/qa.md`, "How deep"), and the consumer's
`bank:` verdict maps onto it 1:1. The rule is one line:

```text
dispatch when depth(bank) <= probe_depth, else DEFER the entry
```

Default is `0`, so a plain run HARVESTS and never orders. Raise it for one invocation:

```text
/haipipe-paper <stage> <paper> probe             ceiling 0 — harvest only, free
/haipipe-paper <stage> <paper> probe --depth 1   also allow reruns of existing code
/haipipe-paper <stage> <paper> probe --depth 3   unsealed — may open new task-folders
```

⚠️ `--depth` AUTHORIZES SPEND. Passing it is the human act that a removed DRAFT gate used to be.
Report what each raise actually dispatched; never raise it on your own initiative.
⚠️ Depth is a proxy for KIND of work, not AMOUNT: a depth-1 rerun over a large cohort can cost
far more than a depth-2 script that counts rows.

**Step 4 — Checker before CHECK.**
Before the CHECK gate judges, run the script the stage.md declares on its `checker:` line
(path relative to the skills root, arguments included). For the probe-consuming stages the
declared default is this door's own probe checker, scoped to the stage key:

```sh
sh paper/haipipe-paper/probe/check-probe-cards.sh <paper_root> --stage <stage-key>
```

`--stage <key>` IS PART OF THE COMMAND. Without it the checker globs the whole paper and this
stage's gate inherits every other stage's open work. CONVENTION: a stage.md's `checker:` line
carries script + flags only and OMITS `<paper_root>`; the caller always inserts the paper root as
the first positional after the script path, exactly as the template above shows. Installed skills flatten the tree, so when
the relative path does not resolve, locate the script with `find -L` over the installed skill
roots (`-L` matters: installed skills are symlinks). The vacuous-green test fires when NO entry
serves this stage while the stage doc still has unanswered Q-consumer blocks. Never report a
green gate over a checker FAIL.

**Global-pass mode (whole-paper cycle).** The per-stage cycle is DEPTH-FIRST; for a whole paper
prefer the GLOBAL PASS (JL ruling 2026-07-11), because stage-by-stage probes duplicate questions
and miss shared gating dependencies:

```text
① DRAFT SWEEP     draft ALL stages in pipeline order, no human stop (placeholders fine;
                  venue still pins BEFORE the venue-ALIGNED drafts)
② PROBE-PLAN      probe plan — merge duplicate questions, author the dispatch DAG
                  [HUMAN GATE — present the campaign, stop]
③ DISPATCH BATCH  probe run — MATCH first; dispatch only what MATCH cannot close, per
                  the DAG; a dependent entry waits until its upstream QA file EXISTS
④ RUN             the task/discovery orchestrators write <task-folder>/QA/<n>-<slug>.md
⑤ HARVEST         a PROBE re-run lands A-executors + per-consumer A-consumer rows +
                  the S02 claims-page flips, then each stage runs its remaining phases
```

Stage gates are unchanged; the global pass only reorders WHEN drafting and probing happen. The
per-entry fields (`route:` / `bank:` / `target:` / `state:`) are owned by
`probe/haipipe-probe/SKILL.md`.

Rebuild the Board after every write
------------------------------------

Ruled 2026-07-26 (design board `QA1`, `QA4`): `enter` leaves the human LOOKING at `board.html`,
so a stale board is a DEFECT, not an inconvenience. **Two directions, both mandatory.**

```text
AFTER a write   rebuild, or the browser shows the previous version
BEFORE a read   RE-READ the page off disk: a human comment or a `>` lane may have
                arrived through serve.py. Never cache a page across a phase boundary.
```

Three entry points, paths relative to THIS skill folder:

```bash
python3 ../../board/haipipe-board/cli/build.py <paper-root>/0-lifecycle   # after every write; ~1s, idempotent
python3 ../../board/haipipe-board/cli/watch.py <paper-root>/0-lifecycle   # once per session, own terminal
python3 ../../board/haipipe-board/cli/serve.py                            # the live layer, port 5599; NEVER file://
```

Calling is not owning: `haipipe-board` owns the build, the filename rule, the html and the
write-back; this door calls it and renders nothing.

**The build's marker report IS the content check.** `build.py` prints one line per unresolved
marker in the paper's `.tex`; surface it after every rebuild:

```text
broken    \citep{key} not in the .bib → compiles to [?]. HUMAN-ONLY fix: an agent never writes bibtex.
unowned   \cite{TOADD} or {VAL:?} with no [Q-…] bracket, or a \ref{} with no \label
          → a hole no question will ever fill (the placeholder grammar exists to prevent this, QB6)
uncited   a display unit's \label referenced by NO section → route to the Display stage
```

A paper's `0-lifecycle/board.md` must declare `dialect: paper` and `paper-root: ..`, or these
markers render as plain text and the report is empty and useless.

The CONSOLE step (enter / status)
----------------------------------

`enter` opens a concrete paper folder as the Paper Console: resolve the root (walk up for
`0-lifecycle/board.md` · `0-lifecycle/` · `<paper>.tex` + `sections/`; STATUS.md is retired and
is NOT a signature), derive current state from disk (never from stored status), CALL
`haipipe-board` on `<paper-root>/0-lifecycle/` (build.py, then serve.py pushes the URL to the
browser), record only the active paper identity in `.paper-console.yaml`, and route later
free-form input through the lifecycle in copilot mode.

The BOARD is the panel; the terminal prints exactly this, in this order, and stops:

```markdown
📋 <board URL>          ← FIRST. If the push failed, say so and print the URL anyway.

<paper-folder-name> · <venue: from S-Open-Venue.md> · frontier: <stage>
<one sentence from the pitch page's lead, or "Pitch not yet written — run /haipipe-paper pitch.">

## Open Needs
  - <gap> -> <route>       one line each, route per Delivery Need Routing

## Recommended Next
  <the single highest-leverage command>
```

Never fall back to `file://`, and never report success when only the build succeeded. The full
console procedure (read order, frontier predicates and the Golden Rule, diagnosis rules, the
resource exemption, copilot policy, `.paper-console.yaml` fields) is `ref/enter-console.md`;
read it when running the console, and re-derive everything from disk on every action.

**Missing path = get-or-create (the ONLY way papers are created).** When the given path does not
exist, do NOT fail. CONFIRM FIRST (creating a repo is outward-facing; never create off a typo),
then resolve the parent project (walk up, or ask). Project-* repo -> paper is REPO-BACKED:
resolve --org (flag or ask, NEVER assume; the paper's owner may differ from the project's),
follow the papers-inside recipe in `project/haipipe-project/fn/repo-project.md`, scaffold per
`fn/folder.md` (the folder verb, run internally), double-bump (paper push -> project pointer
-> workspace pointer), and continue straight into the console. Plain projects: folder +
scaffold, then console. One command from nothing to dashboard.

After dispatch to any specialist skill, capture its structured tail (status / summary / artifacts / next) and present it.

Closing Block (end every reply)
--------------------------------

THE single source of truth for the closing block (every stage / console reply inherits this section).
This is the explicit enclosing-skill exception defined by `haipipe-board`:
Paper calls Board, but a Paper reply emits this ONE composed block rather than
also appending Board's direct-session `status.py` strip. The `board:` line below
preserves the active Board/page attachment. A direct `/haipipe-board` session
still uses Board's own strip.

**The BOARD is the paper's face; the closing block is the session's.** Ruled
2026-07-26 (`QA1`, `QA4`): the closing block stopped carrying a 9-stage strip, which was a worse
copy of the board's own spine, and now carries the URL instead.

In a paper session, END every reply with ONE fenced `text` block: a titled top
rule carrying `📄 paper · <active-stage> 🔥`, the two-line tail, a plain bottom
rule, then the board URL and the PHASE line:

```text
── 📄 paper · seed 🔥 ─────────────────────────
status:  ok · seed             (status and active stage merged on one line)
next:    <single recommended command>
──────────────────────────────────────────────
board:   http://100.121.165.84:5599/b/haipipe-paper/<page-id>
phase:   draft 🔥🚀  │  probe ⬜  │  revise ⬜  │  check ⬜
```

The `board:` line is deep-linked to the page this session is working, so one
click lands on it. If the push to the browser failed, say so on that line and
print the URL anyway; never report success when only the build succeeded.

The PHASE line survives the strip's retirement because it is the only thing here
the board does NOT show: a page's `state:` is its gate status, not the live DPRC
progress of a run in flight.

Markers: 🔥 active now · 🚀 frontier (farthest the paper has ever reached) · ✅ done · ⬜ not started · `--` skipped.
Rules: the phase line always has the four display slots
`draft | probe | revise | check` and exactly one `probe` slot. A phase omitted
from the active stage's `phases:` list is `--`, not pending. Probe entries carry
their own evidence type; the closing block never revives retired
`cite`/`val`/`disp` sub-tracks. EXACTLY one 🔥, never zero.

Gate-aware: closing a stage and advancing to the next requires an EXPLICIT approval action that the current stage is done (Stage Gate, `ref/08-stage-gate.md`) -- by the human (copilot mode) or by a reviewer subagent standing in for the human (autopilot mode); once the S page carries the gate ledger, ✅ means "approved", and the ledger records who approved (human or agent).


Comment lifecycle
------------------

THE single source of truth for inline comments across ALL paper skills. Every phase contract, lifecycle stage, and orchestrator follows this convention. The full format spec (actor ids, the two marks, anchoring, the S-page `## Log` format, round invariants) is `ref/comment-protocol.md`; this section carries the lifecycle and its binding rules.

**Loaded-context rule.** This section is not in context at every skill
invocation, so it cannot bind behavior by itself. Every skill that touches
working files must INLINE its binding subset: never delete/reword `> USER:`;
reply `> CC:` underneath; only the user resolves; move resolved threads
verbatim into the owning S page's `## Log`; make surgical edits only. The stage
contracts carry that block as "Comment rules (binding)".

Two formats, one namespace of actor ids (asked, never assumed):

```text
outline .md    > USER: comment      /      > CC: response underneath
.tex           %% {<actor>-<topic>-vMMDD}: <finding> | <suggestion> ========> {AU vMMDD}: accept
```


- 0.1 · The lifecycle
      Comments come from three places:
      1. **Inline in the working file**: `> USER:` comments (outline) or `%% {USER}:` comments (tex)
      2. **Session (chat)**: direction, reasoning, taste decisions -- agent writes these into the file as `> USER:` (quoting what the user said)
      3. **`> CHECK:` comments**: seeded by the CHECK worker at every flagged report
         item's exact spot. The human replies `> USER:` under each; after resolution,
         the whole thread moves into the owning S page's `## Log`. Direction is the
         reverse of `> USER:` -- agent asks, human rules.
      ```
      1. User adds comment in the .md file (or says it in session, agent writes it in)
      2. CC responds underneath
      3. Work happens, content changes
      4. User confirms resolved
      5. Comment thread MOVES to the owning S page's ## Log
         (with -> applied / -> rejected / -> deferred)
      6. Working file stays clean
      ```
      Rules:
      1. **Comments live in the working document while active.** They sit next to the content they discuss.
      2. **Agent never removes a comment.** Only the user confirming resolution triggers the move.
      3. **Resolved comments move to the owning S page's `## Log`**, grouped by
         phase and date. The comment thread is preserved verbatim.
      4. **Session comments that represent decisions** are written into the working document so they enter the same lifecycle. Ephemeral chat that is not a decision disappears with the session.
      5. **Active comments may cross internal phase boundaries.** DRAFT, PROBE, and
         REVISE are not human gates in the current stage contracts. CHECK reviews
         unresolved threads and either resolves them or restarts the appropriate
         phase.
      Resolved threads land in the owning S page's `## Log`, newest first,
      non-destructively, under a dated heading (`### 2026-07-03 10:14 — [DRAFT] resolved comments`);
      the full format and the why is `ref/comment-protocol.md`.

- 0.2 · REVISE phase: no comment-first
      REVISE is the exception. REVISE passes apply changes directly (no comment-first round). They leave `%% {CC-<pass>}: <why>` comments explaining non-trivial changes. These comments are for CHECK to review, not for a human reply cycle. The human reviews in CHECK and can add `> USER:` comments to restart REVISE. When a tex comment-first round IS used, its two-round invariants are in `ref/comment-protocol.md`.
      No-Arg Chooser
      ---------------
      When no paper root is found, do not fan out.
      Emit a compact chooser (one line per entry; the Verbs block carries the detail):
      ```
      📄 haipipe-paper: no paper detected. Pick an entry:
        venue       /haipipe-paper venue "<topic or paper-path>" [--no-pin]
        enter       /haipipe-paper enter "<paper-path>" [--org <owner>]   (missing path -> offers to create it)
        section-edit | rebuttal | probe    (see /haipipe-paper help text above)
      ```
      Specialist Return Contract
      ---------------------------
      Each specialist returns a tail block:
      ```
      status:    ok | blocked | failed
      summary:   2-3 sentences on what the specialist did
      artifacts: [paths created, read, or modified]
      next:      suggested next command
      ```
      Delivery Need Routing
      ----------------------
      THE single source of truth for how the paper records a gap as a need, routes it to the right evidence worker, and backfills when the answer returns. Paper-owned; the application skill keeps its own copy. There is no cross-skill shared file.
      Core rule: the paper owns the STORY and the JUDGMENT; the EXECUTORS (task and discovery) own the EVIDENCE, and the probe is the map between them.
      Paper work is demand-driven: a paragraph, claim, figure, or round todo may reveal that the next action is evidence work.
      The enter/status path surfaces those needs before recommending more writing.

- 0.3 · How paper talks to probe
      No message bus, no shared contract file. Two channels carry it, and the agent (this session) is the medium:
      ```
      1. Command   paper hits a claim gap -> the agent runs
                   /haipipe-paper probe "<question>" (opens one nested QA-probe in the
                   owning S03 or S04 topic). PROBE owns the whole five-step loop, MATCH
                   before DISPATCH (fn/probes.md).
      2. Disk      paper writes the need on its owning S page or claim ledger; the executor
         (async)   writes the answer as <task-folder>/QA/<n>-<slug>.md; the entry's
                   `**target**:` points at that FILE, its `#### A-executor` copies the answer
                   in, and the owning E<n> division's `#### consumers` rows record each A-consumer. No
                   handshake — binding is by PATH, and the file on disk IS the state.
      ```
      Who owns which format: the evidence page owns the paper NEED and its E<n> divisions; the QA-probe owns the neutral Q-executor and returned answer; the EXECUTOR owns the QA-bank, the original (`# Q` / `## Answer` / `## Caveats` / `## Not-done`, general language, anatomy in `probe/haipipe-probe/SKILL.md`). A claim's status is the paper's alone and lives in its claims page. That is why no shared interface file is needed: each artifact's shape belongs to the layer that produces it.

- 0.4 · When to record a need
      Only when the problem is EVIDENCE, not wording. A wording/structure problem loops back inside the paper lifecycle (claims / pitch / narrative / display / section-edit). A need leaves the paper for an evidence worker, and it travels the loop above: paper GAP -> a Q-consumer COLLECTED into the evidence page's E0 queue -> PROBE translates it into an E<n> division and MATCHes its QA-probe -> DISPATCH only what MATCH could not close -> the answering QA-bank file -> `#### A-executor` -> the A-consumer row under `#### consumers` -> the paper backfills its claim page. Do NOT route through a project-level narrative layer (there isn't one).

- 0.5 · Routes
      ```
      claim needs evidence / robustness / literature / a data artifact -> /haipipe-paper probe "<question>"  (a nested S03/S04 entry; PROBE does MATCH first, and dispatches only what MATCH cannot close)
      figure/table lacks its verified display-ready aggregate           -> /haipipe-task-for-display <need>
      figure/table has a verified aggregate and needs a paper asset     -> the display stage → Intake → matching Display renderer
      settled claim status (supported|refuted|inconclusive             -> 0-lifecycle/S02-work/S-Work-C-claims.md (the ONLY home of a claim's status; the
        + confidence + claim_type)                                        probe entry carries only the `#### A-executor` copy of the bank's
                                                                          answer)
      wording/section placement                                        -> the owning lifecycle stage
      standalone utility (a HUMAN, not the paper: lit scan, data check) -> /haipipe-task qa | /haipipe-discovery qa (the bank's own door)
      ```
      Two entry rules (who the delivery calls):
      - a CLAIM need (a claim's status is at stake) -> raise a question ENTRY and let the PROBE phase route it. The paper never calls a raw compute agent for a claim-bearing need, and never executes bank work inline (LAW 1).
      - a pure RENDER need (no claim at stake, e.g. re-render a figure) -> return to the Paper Display stage; it reuses the approved Intake and commissions the renderer. Call `/haipipe-task-for-display` only when the display-ready aggregate itself is missing or must change.
      ALL evidence enters through a stage's PROBE phase; the paper never calls the bank directly.
      Resolved evidence backfills into claims, display, sections, or round logs.
      Evidence workers never own the paper story.

- 0.6 · Need record and backfill
      Each open need is one row on its owning Board/S page (fields: `need_id · gap · kind · route · state open|commissioned|returned · backfill`); claim needs live on `0-lifecycle/S02-work/S-Work-C-claims.md`.
      The answer is a FILE: the executor's `<task-folder>/QA/<n>-<slug>.md`. The probe entry's `**target**:` points at it and `#### A-executor` copies its answer in. The owning E<n> division records what it means for this paper on its `#### consumers` rows. On backfill:
      ```
      - write the claim's status in 0-lifecycle/S02-work/S-Work-C-claims.md — supported |
        refuted | inconclusive, + confidence + claim_type. THAT ledger is
        the only home of a claim's status.
      - if the evidence narrows the claim, narrow the claim wording in the claims page
      - the executor NEVER edits paper prose: it returns a FACT, and the paper decides
        what the fact means and how to phrase it
      ```
      Multiple papers can cite the SAME QA file in discoveries/ + tasks/, each through its own QA-probe and evidence page — the FACT is shared, the JUDGMENT is not.

- 0.7 · Autonomous drain (the "keep going" loop)
      The console is a derive-from-disk, resumable loop body. To drive a delivery to done:
      ```
      LOOP until (no open needs) OR (gate hit) OR (only server-blocked left):
        1. enter    derive frontier + open needs from disk (the queue)
        2. pick     the next actionable need (skip server-blocked)
        3. route    claim -> a question ENTRY (the PROBE phase dispatches it) ;
                    missing aggregate -> task-for-display ; render -> Display → Intake → renderer ; prose -> edit
        4. execute  write the artifact locally, or wait for the dispatched QA file
        5. backfill update the slot/display/entry; mark the need returned
        6. -> 1
      ```
      State lives on disk in the Board/S pages, claim ledger, probe entries, and their target files, so a fresh session re-enters and continues. A local need (render, parse, draft, backfill) drains immediately; a need requiring a NEW server run (Stata on PHI) is server-blocked: schedule a poll and resume when results land.
      ```
      AUTO (no asking):  local render/parse, backfill claims/displays, draft a stage tex,
                         compile previews, parse logs, status/ledger updates
      PAUSE + surface:   trigger a server/PHI run; declare a final yes/no answer;
                         settle a claim's status in S-Work-C-claims.md; compile-to-submit;
                         destructive round / git ops
      ```
      The loop runs AUTO unattended and stops at the first PAUSE gate, reporting what it hit.
      Evidence Routing Protocol
      --------------------------
      When paper-lifecycle work hits a claim or wording whose support needs NEW evidence, data/variable inspection, or an analysis that does not exist yet, the paper layer must NOT dig into data, scripts, do-files, logs, or variable definitions. Stop. Hand off. Mark the gap. Keep writing.

- 0.8 · The `\needprobe{}` macro
      When a claim lacks evidence, mark it in the `.tex` with a visible red caveat:
      ```latex
      \newcommand{\needprobe}[1]{\textcolor{red}{\textbf{[NEED PROBE]} #1}}
      ```
      Add this macro to the lifecycle preamble (or the paper's shared command file). Use it inline wherever the gap lives:
      ```latex
      \needprobe{Is the intensive margin about patients already on opioids?}
      ```
      The red flag renders in the compiled PDF so the gap is obvious to every coauthor. Remove it when the answer lands (the entry's `**target**` resolves and its `#### A-executor` is written) and the claim is backfilled with supported text.

- 0.9 · Handoff protocol
      When paper work surfaces an evidence gap, do the following INSTEAD of investigating the data yourself:
      ```
      a. STOP investigating the data. Do not grep do-files, re-derive variables, or
         design the estimation.
      b. MARK the claim with \needprobe{description of what needs settling}.
      c. RECORD a delivery NEED (per Delivery Need Routing above): the claim under test
         and what an answer would have to establish.
      d. RAISE it as a Q-consumer question. The stage's PROBE phase opens the entry,
         MATCHes it against the bank, and dispatches only what MATCH cannot
         close. The paper TRIGGERS; it never runs the analysis (LAW 1).
      e. BACKFILL: when the answering QA file lands, PROBE writes the entry's
         `#### A-executor`, the owning E<n> division records the A-consumer, the
         claim's status flips in its claims page, and the \needprobe{} flag comes out.
      ```

- 0.10 · The `probe` verb
      ```
      /haipipe-paper probe <need-description>
      ```
      opens one nested QA-probe in the right S03/S04 topic. The PROBE phase is what dispatches it — through `Agent(haipipe-probe-q-executor-agent)` to `Agent(haipipe-task-orchestrator-agent)` or `Agent(haipipe-discovery-orchestrator-agent)`, carrying the QA-probe's `#### Q-executor` block and nothing else. The paper stays a story layer; the executor does the work. Anatomy + campaign + the paper-side loop: `fn/probes.md`.
      A HEAVY probe (reading a lot of code/logs, e.g. cohort construction from Stata do-files) is
      dispatched with `run_in_background=true` so the paper session keeps doing paper work: mark the
      beat `\needprobe{}`, raise the entry, fold the returned report into Methods when it lands.

- 0.11 · Construction as a first-class beat
      Dataset/cohort CONSTRUCTION is a first-class narrative/Methods beat, not a one-line "Setting"
      aside: the inclusion/exclusion funnel, the unit definition, the exposure -> outcome linkage, and
      how each outcome, flag, and control variable is computed. Each may trigger its own
      `\needprobe{}` if no answering QA file covers it. The EXECUTOR (not the paper) reads the
      do-files, inspects the data, and returns the description.
      Layout
      -------
      ```text
      haipipe-paper/
      ├── SKILL.md            this file: the paper family's ONLY registered skill
      ├── create-page.py      the public creator; composes Board shell + stage scaffold
      ├── check-contracts.py  stage-contract form checker (run after any contract edit)
      ├── section-stats.py    section-size reporter
      ├── stages/             index.yml (small, always read) · CONTRACT.md · section-kinds.yml;
      │                       each row's dir: points at the stage's own folder under ../SNN-*/
      ├── probe/              check-probe-cards.sh · check_topic_entries.py ·
      │                       topic-entry-contract.md · per-stage-dispatch.md
      ├── ref/                cross-stage references (08-stage-gate.md, paper-folder-anatomy.md,
      │                       prose-quality.md, enter-console.md, diffpdf/ presets+bugs, …)
      ├── fn/                 probes.md · feedback.md · digest.md · folder.md · conform.md ·
      │                       compile.md · diffpdf.md · project.md · to-overleaf.md · to-word.md
      └── scripts/            check_structure.sh (conform) · diffpdf/ (make-diff.sh + templates) ·
                              project/ (project.py + runtime) · to-word/ (md2docx.py + siblings)
      ```
      Adding a stage = one folder + one row in `index.yml`. Adding a build verb = one `fn/` file
      (+ tooling under `scripts/`). No new skill, no version bump, no `description` edit.
      Structure Pointers
      -------------------
      Each area's internal contract lives with its owner; consult, never restate:
      ```
      skill tree (S01–S10 / venue)               -> ../README.md (skill root: skill-tree layout and routing)
      paper-folder layout                        -> ref/paper-folder-anatomy.md (canonical tree and maturity ladder)
      lifecycle stages + venue coupling          -> stages/CONTRACT.md + stages/index.yml
      stage gate + phase transitions             -> ref/08-stage-gate.md
      rounds                                     -> ../S10-round/round/stage.md (the Rounds contract; rebuttal craft beside it)
      venue knowledge                            -> ../venue/playbook-<venue> packs (venue is knowledge, not a pipeline)
      ```
      Composing with Evidence Workers
      --------------------------------
      ```
      /haipipe-paper (the door)
              ├─► STAGE step        seed -> resource -> claims -> [venue] -> pitch ->
              │                     narrative -> display -> section-edit -> round (pages
              │                     driven via haipipe-page)
              ├─► fn/ verbs         folder · conform · compile · diffpdf · project ·
              │                     to-overleaf · to-word (human-triggered, tooling in scripts/)
              │
              │   evidence path (a claim hits a gap):
              └─► S03-literature/probes/ or S04-value/probes/ — one QA-probe per Q-executor
                       │   PROBE runs ① ORGANIZE + ② MATCH ──► most entries close at MATCH (T2 REUSE)
                       └─► ③ DISPATCH the `#### Q-executor` VERBATIM, only for what MATCH missed:
                                Agent(haipipe-probe-q-executor-agent)   ← its clean context IS the wall
                                     ├─► Agent(haipipe-task-orchestrator-agent)
                                     └─► Agent(haipipe-discovery-orchestrator-agent)
                           ④ POINT **target** ─► the answering QA file
                           ⑤ INTERPRET ─► `#### A-executor` ─► `#### consumers` A-consumer rows

              a stage reaches the bank ONLY through its PROBE phase — no direct discover/task verb
      ```
### The other files

50 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
check-contracts.py                 209 ln  Check every stage contract against stages/CONTRACT.md, and against a real paper.
create-page.py                     445 ln  Create one paper lifecycle S page through the Board's shell primitive.
fn/compile.md                      238 ln  Door verb: compile (LaTeX target to verified PDF)
fn/conform.md                      126 ln  Door verb: conform (paper-folder conformance audit)
fn/diffpdf.md                      255 ln  Door verb: diffpdf (tracked-changes PDF against a baseline)
fn/digest.md                       172 ln  Digest (condense the session into routed feedback)
fn/feedback.md                     245 ln  Feedback (capture skill feedback, route at capture, fix later)
fn/folder.md                       165 ln  Door verb: folder (paper-folder scaffold)
fn/probes.md                       191 ln  Paper probe routing
fn/project.md                      109 ln  Door verb: project (S pages to isolated LaTeX candidates)
fn/to-overleaf.md                  243 ln  Door verb: to-overleaf (two-way Overleaf sync)
fn/to-word.md                      164 ln  Door verb: to-word (one stage page to a coauthor .docx)
probe/check-probe-cards.sh           3 ln
probe/check_topic_entries.py       171 ln  Verify the Paper S03/S04 nested QA-probe contract.
probe/per-stage-dispatch.md        160 ln  Per-stage dispatch reference (paper PROBE)
probe/topic-entry-contract.md       32 ln  Paper evidence-page and QA-probe contract
ref/03-paper-lifecycle.md          109 ln  Paper Lifecycle
ref/04-lifecycle-map.md            158 ln  Paper Lifecycle Map
ref/08-stage-gate.md               234 ln  Stage Gate Protocol
ref/09-stage-illuminate.md          69 ln  Illuminate + Elicit Protocol
ref/comment-protocol.md            105 ln  Comment Protocol
ref/diffpdf/class-presets.md       154 ln  Class Presets
ref/diffpdf/compile-pipelines.md    50 ln  Compile Pipelines
ref/diffpdf/known-bugs.md          186 ln  Known Bugs
ref/enter-console.md               102 ln  Paper Console (the enter/status procedure)
ref/paper-folder-anatomy.md        246 ln  haipipe-paper/ref : paper folder anatomy
ref/paragraph-indexing.md          109 ln  2-phase / shared — paragraph indexing
ref/prose-quality.md                48 ln  Prose Quality Rules (Universal)
ref/sentence-format.md              71 ln  2-phase / shared — sentence format
ref/tex-file-anatomy.md            105 ln  2-phase / shared — tex file anatomy
scripts/check_structure.sh         273 ln
scripts/diffpdf/detect-paper-class.sh   139 ln
scripts/diffpdf/make-diff.sh       245 ln
scripts/diffpdf/silence-minor-changes.pl   143 ln
scripts/diffpdf/templates/README.md.tpl    69 ln
scripts/diffpdf/templates/config.sh.tpl    30 ln
scripts/diffpdf/templates/silenced-changes.txt.tpl    27 ln
scripts/project/agents/openai.yaml     4 ln
scripts/project/project.py           8 ln  CLI entry point for the paper door's project-verb runtime (fn/project.md).
scripts/project/references/projection-manifest.md    79 ln  Projection manifest v1
scripts/project/scripts/project_runtime.py  1235 ln  Manifest-driven, gated Markdown-to-LaTeX projection runtime.
scripts/project/scripts/test_project_runtime.py   218 ln  Disposable safety and determinism tests for project_runtime.
scripts/to-word/build-both.sh       54 ln
scripts/to-word/docx2pdf.py        239 ln  docx2pdf.py -- render a .docx we generated into a PDF, comments and all.
scripts/to-word/md2docx.py        1228 ln  md2docx.py -- one stage page's ## Content becomes a .docx whose APPARATUS
scripts/to-word/md2tex.py          184 ln  md2tex.py -- one or more stage pages become LaTeX sections, and a paper.
section-stats.py                   302 ln  Measure an S page's prose FORM and print the structure block for `## Diagram`.
stages/CONTRACT.md                 226 ln  The stage contract form
stages/index.yml                    41 ln
stages/section-kinds.yml            90 ln
```

<!-- haipipe:skill:body:end -->

## Aims
- [x] 🧭 Establish the entry boundary
      The public command resolves intent and a paper root, then dispatches to
      a named owner.  Its purpose is routing, not content generation.
- [x] 🚦 Record the non-guessing rules
      An unclear venue must be asked, not silently selected.  A phase request
      goes through its stage, and a bank need goes through PROBE rather than a
      direct task or discovery call.
- [ ] 🧪 Exercise the no-argument and ambiguous-intent branches
      A fresh-agent run should prove that the chooser, paper-root detection,
      and venue ambiguity all stop at the intended boundary.

## States
The route and its ownership boundary are now visible on the Board.
What has not yet been independently exercised here is the front door's difficult negative behavior: declining to guess an ambiguous venue or bypass a stage.

## Log
- 260806 0130 · [REVISE-CC] card synced to the 0.5.0 one-door fold; enter/lifecycle/stage absorbed, workers dissolved to stage data
260727 · Audited against `board.md`'s decision-only rule, which says `state:` is about the DECISION and that implementation does not gate this board. Every open item here is implementation or a test, not an undecided question, so the page was reporting itself as open because code was missing. Flipped with no ruling made.
260727 1430 · Created the Paper front-door page from `paper/haipipe-paper/`.
The authored record captures route ownership; the managed spans carry the current shipped instructions and release history.

<!-- haipipe:skill:log:start a07100b50455f7a8 paper/haipipe-paper -->

Converted from the skill's own `CHANGELOG.md`: 39 releases.

260806 · `0.7.0` · S03/S04 become evidence pages (JL's final design)
      JL's evidence-page ruling (260806, "exactly what I want") executed across the
      paper projection:
      - the topic page is an EVIDENCE PAGE: `route: outward|inward` in its metadata
        head (the type key; the `### Q-consumer register` marker is retired), and
        Content organized BY EXECUTOR: one `### E<n> · <question>` division per
        Q-executor conversation (🔗 QA-probe pointer, `#### consumers` rows with
        per-consumer A-consumer + row state, `#### answer digest`), plus the
        standing `### E0 · incoming` collect queue
      - naming final: QA-bank (the executor's original) and QA-probe (the paper's
        stub); the four slot words are capitals everywhere including heading slots
        (`#### Q-executor` / `#### A-executor`; `consumer trace` and `bank binding`
        stay lowercase)
      - `probe/topic-entry-contract.md`, `probe/per-stage-dispatch.md`,
        `fn/probes.md`, `stages/CONTRACT.md`, `ref/enter-console.md`, the S01/S02
        stage files, the S03/S04 craft files and READMEs swept to the new shape
      - `S03-literature/template.md` + `S04-value/template.md` rewritten to the
        division shape with the head route: line; `entry-template.md` RENAMED
        `qa-probe-template.md` in both folders, in the record shape
      - `probe/check_topic_entries.py`: topics detected by the head route: key,
        digit-first `<n>-<slug>.md` record names enforced (the stale S-prefix
        filename rule fixed), capital slot headings canonical
      - MISQ 2026 migrated as the proving paper: 8 evidence pages restructured into
        E divisions, 28 QA-probes kept their names and gained capital slots; board
        checker baseline held at 11 ERRORs
260806 · `0.6.1` · probe entries are hidden probe QAs (ruling B)
      JL ruling B (260806: "an entry is a source file the topic page points at, like a
      PDF; the board renders the topic page, never the entry") plus its naming
      addendum (one conversation, two QAs: the bank QA is the original, the probe QA
      is the paper's copy that points at it):
      - `probe/topic-entry-contract.md` and `fn/probes.md` now name the nested file a
        probe QA (the entry record), state the digit-first naming law
        `probes/L<nn>|V<nn>-<topic>/<n>-<slug>.md` with `<n>` restarting at 1 per
        drawer, and say why the name hides it from the board's page sweep.
      - `SKILL.md`, `fn/folder.md`, and `ref/comment-protocol.md` wording sweep:
        entry page -> probe QA; the executor's file is the bank QA, the original.
      - Stage data updated in place (unversioned folders): `S03-literature/` and
        `S04-value/` `entry-template.md` rewritten to the record shape (# title +
        `requires:` + the four slots, no page frame, no Log), `template.md` example
        pointers and both READMEs moved to the `<n>-<slug>.md` naming.
260806 · `0.6.0` · ONE registered skill (thin-paper phase 3)
      JL ruling 260806 ("只保留一个 skill, 就是 haipipe-paper"): the paper family now registers
      exactly ONE skill, this door; everything else is data. The nine remaining registered
      siblings retired to `../_old/phase3-260806/`, their jobs absorbed as internal steps:
      - `haipipe-paper-folder` -> `fn/folder.md` (the scaffold procedure; `enter`'s
        get-or-create branch cites it).
      - `haipipe-paper-conform` -> `fn/conform.md`; its mechanical checker moved to
        `scripts/check_structure.sh` and the `conform` verb runs it. The delete-test RULE
        text lives in the fn.
      - The five S09-build skills became human-triggered door verbs, one fn each:
        `haipipe-paper-compile` -> `fn/compile.md` · `haipipe-paper-diffpdf` ->
        `fn/diffpdf.md` (toolkit at `scripts/diffpdf/`, class presets + known bugs at
        `ref/diffpdf/`) · `haipipe-paper-project` -> `fn/project.md` (runtime at
        `scripts/project/`) · `haipipe-paper-to-overleaf` -> `fn/to-overleaf.md` ·
        `haipipe-paper-to-word` -> `fn/to-word.md` (exporter at `scripts/to-word/`).
      - `haipipe-paper-round` + `haipipe-paper-rebuttal` became STAGE DATA: the new `round`
        stage (`../S10-round/round/stage.md` + `template.md`, per-unit, one dated round per
        page, `board_family: Round`) with the reviewer-response craft distilled to
        `../S10-round/rebuttal-craft.md` and loaded via the stage's `craft:` list. New row
        in `stages/index.yml` after section-edit (triggers: round, rebuttal, 返修,
        reviewer response); the checker is the door's own
        `probe/check-probe-cards.sh --stage round`.
      - Verbs table updated: folder/conform/build rows now name their fn files; round and
        rebuttal route to the STAGE step, key round. `fn/feedback.md` inboxes repointed
        (fn verbs -> the door's own fallback; round/rebuttal -> `S10-round/round/feedback/`).
      - Reference sweep: `../README.md`, `ref/04-lifecycle-map.md`,
        `ref/paper-folder-anatomy.md`, `ref/diffpdf/compile-pipelines.md`, moved scripts'
        self-references, `skills/STRUCTURE.md`, haipipe-project's `project-structure.md`,
        and haipipe-application-round's description all repointed to door verbs / fn paths.
        Boards under `diagrams/` deliberately left for the main session.
260805 · `0.5.0` · the ONE door (thin-paper phase 2)
      - Absorbed the three routers into this skill and retired them to `../_old/`:
        `haipipe-paper-stage` (stage resolution via stages/index.yml, create-page.py,
        the one-stage-file rule, the PROBE ceiling with the --depth spend-authority
        warning kept word-for-word, checker-before-CHECK, rebuild-after-write and
        re-read-before-read), `haipipe-paper-enter` (the console procedure, compressed;
        detail in the new `ref/enter-console.md`), and `haipipe-paper-lifecycle`
        (stage ordering, maturity rule, global-pass mode, phase-verb pass-through).
      - Phase driving is NOT restated: the door ensures the S page exists and hands it
        to `haipipe-page` (WORK ON / RUN); `board/page-phases/` own DPRC.
      - `workers/` dissolved: page rules stayed in board/, the LaTeX craft became
        stage data files declared by each stage.md `craft:` list
        (S03 citation-craft.md · S04 values-craft.md · S05 draft-craft.md ·
        S06 revise-place/revise-results/check-evidence-craft.md ·
        S09-build/proof-checker/ as a craft pack), and the probe tooling moved into
        this skill's `probe/` (check-probe-cards.sh, check_topic_entries.py,
        topic-entry-contract.md, per-stage-dispatch.md); the probe worker's unique
        deltas merged into `fn/probes.md`.
      - Moved in from the retired stage router: `stages/` (index.yml, CONTRACT.md,
        section-kinds.yml), `create-page.py` (BOARD_STAGE repointed to
        board/haipipe-board/cli/stage.py), `check-contracts.py`, `section-stats.py`,
        and `ref/` (joined by the ex `workers/REF/` files). The comment protocol's
        format detail moved to `ref/comment-protocol.md`; the door keeps the binding
        lifecycle rules.
260730 · `0.4.6` · explicit projection routing
      - Added `project` and `projection` to delivery routing so gated S-page content
        reaches `haipipe-paper-project` rather than an implicit submission overwrite.
260727 · `0.4.5` · Display Intake routing
      - Separates a missing display-ready aggregate (task-for-display) from a paper-facing render (Paper Display → Intake → renderer).
      - Removes the stale direct re-render-to-task route, so an existing verified aggregate is never mistaken for a paper asset.
260726 · `0.4.4` · one evidence dispatch topology
      - Synchronized the active Paper probe reference and behavioral preference with
        the runtime chain: Paper PROBE performs ORGANIZE/MATCH, the isolated
        q-executor collector performs DISPATCH/POINT, and task/discovery remain
        behind that collector.
      - Removed the last active instruction that told a Paper worker to dispatch
        directly to task/discovery.
      - Corrected active probe-entry globs to the topic-folder anatomy
        `1-probes/PP*/*.md`.
      - Removed active migration instructions for old probe sidecar paths; the Paper
        contract now exposes only the current topic-folder anatomy.
260726 · `0.4.3` · stage declarations are authoritative
      - Replaced the universal four-phase/two-gate story with each stage's
        `phases:` and `gates:` declarations; current stages gate only at CHECK and
        Venue omits REVISE.
      - Moved phase/comment history from `_LOG` sidecars into owning S pages.
      - Corrected probe ownership: DRAFT raises Q-consumers; PROBE authors entries
        and owns ORGANIZE through INTERPRET.
      - Removed the unsupported `argument-hint` frontmatter key so the user-facing
        orchestrator passes the current `skill-creator` validator.
260726 · `0.4.2` · one composed tail, one probe phase
      - Declared Paper as Board's canonical enclosing-skill case: Paper emits one
        closing block with the active Board deep link and never appends the direct
        Board `status.py` strip.
      - Restored the four-slot DPRC line (`draft | probe | revise | check`) and
        removed the retired `cite` / `val` / `disp` probe sub-tracks.
260726 · `0.4.1` · derived state has one home
      - Replaced the stale `current_layer` gate wording with the actual stage-closing approval action.
      - Removed remaining `STATUS` references from delivery routing; open needs and resumable state live on Board/S pages, the claim ledger, probe entries, and their target files.
260726 · `0.4.0` · the Closing Block carries the board URL, not a stage strip
      Implements the single-door ruling (design board `skills/diagrams/01-haipipe-paper-260725`, faces `QA1` + `QA4`, JL 2026-07-26): **`/haipipe-paper` is the single thing a human types**, and it CALLS `haipipe-board` to build and open the paper's `0-lifecycle/`. `haipipe-board` remains its own door for boards that are not inside a paper. Calling is not owning: `haipipe-board` still owns the format, the build, the filename rule, the html and the write-back.
      - **The `stage:` line and `stage-strip.sh` are RETIRED.** The strip was specified in the 260622 feedback as reading `STATUS.md current_layer`, with the stated precondition that a stale value would make it lie. `STATUS.md` is retired and the board renders the spine, so the strip has neither a source nor a job. It was a worse copy of something the human already has open.
      - **A deep-linked `board:` line replaces it**, pointing at the page this session is working, so one click lands on it.
      - **The `phase:` line survives, and the reason is stated.** It is the only thing in the closing block the board does NOT show: a page's `state:` is its gate status, not the live DPRC progress of a run in flight. The stage line was derivable from the board and therefore redundant; the phase line is not.
260724 · `0.3.2`
      Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 3.2.1; older entries below keep their original numbers).
260719 · `3.2.1` · vocabulary: `probe` (not "the constitution"); entry/`### a-executor` naming
      Two vocabulary rulings from JL, both dated 2026-07-19, applied across `paper/`.
      **Ruling A — the `probe` nickname.** JL: "宪法 don't use this name, just use `probe`." Every "THE CONSTITUTION" / "the constitution" / "the probe constitution" naming `probe/haipipe-probe/SKILL.md` is replaced by `probe` or by the actual path, whichever reads better at the site. A nickname already in the repo is still a nickname.
      **Ruling B — the `a-consumer:` probe-file field.** `- a-consumer:` as a FIELD IN A PROBE FILE was replaced by the entry's `### a-executor`; `check-probe-cards.sh` HARD FAILs it under the `stale-old-format` rule. The a-consumer CONCEPT is untouched and still named a-consumer: it is the per-consumer interpretation written in the STAGE DOC (station ②), anchored `[source: PP<NN>]`. Prose that said "the probe section carries its `a-consumer:`" was wrong twice over — probe files hold ENTRIES, not sections, and what an entry carries is `### a-executor`.
      Current model, for reference:
      ```
      QA file (bank)  ->  the ENTRY's `### a-executor`  (probe file: the copy, single source of truth)
                      ->  each Q-consumer's a-consumer  (STAGE DOC: what it MEANS for this consumer)
                      ->  stage content                 (REVISE weaves it in, discharges the bracket)
      ```
      Written under JL's NO TOMBSTONES rule (2026-07-19): "不需要留退役告示,直接抹除任何痕迹" then "follow this rule to do all the following changes." The docs state only the current contract; this CHANGELOG carries the history.
      ### Changed — SKILL.md
      - The `probe` verb block: "That worker follows the shared probe model (the constitution)" -> "...the shared probe model owned by `probe/haipipe-probe/SKILL.md`".
      - Same block: a stage's PROBE phase works "the sections whose `serves:` names that stage" -> "the entries whose `### q-consumer` bullets name that stage". `serves:` is one of the three strings `check-probe-cards.sh` HARD FAILs (`stale-old-format`), so the umbrella was describing a slice the checker rejects. Found during this pass, not on the reported list.
      ### Changed — fn/probes.md
      - Three "constitution" references retitled: the model owner line ("v9.5.0, the constitution" -> "v9.5.0"), the anatomy pointer ("the constitution's \"The probe file\" section" -> "`probe/haipipe-probe/SKILL.md` -> \"The probe file\""), and the loop header ("constitution v9.5.0" -> "probe v9.5.0").
      ### Unchanged (verified LIVE, ruling B)
      Every `a-consumer` in SKILL.md (7 sites) and fn/probes.md (2 sites) already named the stage-doc concept — "each Q-consumer's a-consumer (in the stage doc)", "each stage doc's a-consumer", "a-consumer in its stage doc (station ②)". This file was already on the current model; nothing was rewritten.
260719 · `3.2.0`
      Changed (JL 2026-07-19, paper/2-phase refactor — the sidecar model is retired: `1-probes/` is the only consumer-side source of truth, `_LOG_<stage>.md` the only sidecar)
      - **Retired sidecars swept out of the router.** `Used in: … _CITATION_, _VALUES_` (the two-comment-formats section) → section `.md` files and `1-probes/PP*.md` entries. `fn/probes.md` legacy-migration rule: the "Stage-owned working docs (`_CITATION_`, `_VALUES_`, `_EVIDENCE_`, `_DISPLAY_`) do NOT move" clause named four documents nobody writes; replaced with the live statement of what IS the source of truth.
      - **Dissolved lane skills swept out.** `fn/feedback.md` routed `citation, bibtex, references` to `haipipe-paper-probe-citation`; now `haipipe-paper-draft-citation` — citation holes are DRAFT's to open, not PROBE's. `fn/probes.md` step ⑤ said "the harvest lanes pay out"; harvest is INLINE in ⑤ and `### a-executor` is its only sink, so it now names what actually rides along (source anchors, values, display-unit paths).
      - **Composing with Evidence Workers diagram** redrawn to the current phase split: DRAFT authored ①ORGANIZE + ②MATCH (most entries close at MATCH, T2 REUSE); PROBE runs ③④⑤ and dispatches through `Agent(haipipe-probe-q-executor-agent)`, which fans out to the task/discovery orchestrators — the router previously showed PROBE calling those orchestrators directly, which is precisely the inline dispatch the collector exists to prevent.
      - **Evidence Routing Protocol** re-rooted: `\needprobe{}` comes out when the entry's `**target**` resolves and its `### a-executor` is written (was `target:` + `a-consumer:` — and `a-consumer:` as a probe-file field is a format `check-probe-cards.sh` HARD FAILs). Handoff step (d) attributes MATCH to DRAFT; step (e) states the real backfill chain: PROBE writes `### a-executor` → each Q-consumer writes its a-consumer in the stage doc → 1b-claims.md flips → the flag comes out.
      - **Vocabulary**: probe `SECTION` → `## QX<n>` ENTRY across the description, summary, verb line, Delivery Need Routing, and the `probe` verb; `fn/probes.md`'s no-tables rule now says a probe file holds ENTRIES.
260719 · `3.1.1`
      - WIKI RETIREMENT — three shared docs absorbed here, each now with exactly ONE home (the wiki folder is deleted; every referrer points at the section, nothing is duplicated):
        - **Comment lifecycle** (was `02-comment-lifecycle.md`, 18 referrers) — new section after the Closing Block: actor ids (never hardcode initials), the two formats (blockquote `.md` / `%% {}` tex), the two marks + `========>` reply separator, anchoring, the 6-step lifecycle + 5 rules, `_LOG` format (newest-at-top, non-destructive insert, date + HH:MM headings), the REVISE no-comment-first exception, and the round invariants table. The loaded-context rule is kept: this section is BACKGROUND, so every skill touching working files still INLINES its binding subset.
        - **Delivery Need Routing** (was `11-delivery-need.md`, 11 referrers) — MERGED into the existing section rather than added beside it: how paper talks to probe (command + disk channels), when to record a need, routes, the need-record schema, backfill, and the autonomous-drain loop with its AUTO/PAUSE autonomy policy.
        - **Evidence Routing Protocol** (was `12-evidence-routing.md`, 4 referrers) — new section directly under Delivery Need Routing: the `\needprobe{}` macro, the 5-step handoff protocol, the `probe` verb, background dispatch for heavy probes, and construction-as-a-first-class-beat.
      - Structure pointers repointed: skill tree -> `../README.md` (which absorbed `06-paper-skill-structure.md`); rounds -> `../0-enter/haipipe-paper-round/SKILL.md` (which absorbed `07-paper-rounds.md`).
260714 · `3.1.0`
      - `fn/probe-plans.md` RENAMED to `fn/probes.md` ("plans" is retired vocabulary); the verb table and Dispatch notes re-point at it.
      - Dispatch notes: "Verdicts backfill into 1-claims / sections / round logs" -> the answer lands as a section's `reading:`, and the CLAIM's status flips in `0-lifecycle/1b-claims/1b-claims.md` (the only home of a claim's status). "Buffer convention" -> "Probe-file convention".
260714 · `2.11.0`
260714 · `3.0.0`
      - The `probe` verb is re-pointed at the PROBE-FILE POOL (`1-probes/PPNN_<topic>.md`, one file per TOPIC, one SECTION per question). Before this, every `/haipipe-paper probe` invocation was routed into the dead card/stub model: the routing table sent it to `1-probe-plans/` cards, the `no args SHOW` mode derived statuses from `_ASK/` stubs (which R2 forbids from ever existing, so it would always report zero dispatches even with commissions in flight), and the diagram routed the verdict to the retired gateway.
      - `fn/probe-plans.md` REWRITTEN (legacy filename kept, same precedent as check-probe-cards.sh). It was fully pre-v8: cards in `1-probe-plans/`, the status set `planned | dispatched | verdicted` (two of which are DELETED states), and `dispatch Agent(haipipe-probe-orchestrator-agent) -- ALWAYS, no matter how small the need` — the exact opposite of R13. It now carries the 1-probes/ convention, MATCH-before-DISPATCH, and direct dispatch to the two executor orchestrators.
      - PREFERENCES.md — the highest-authority text in the bucket, loaded on every paper session — re-stated in v8 terms. It MANDATED the retired 4-step procedure and named the archived gateway agent, so a session would obey it, dispatch a nonexistent agent, fail, and (because the preference explicitly forbids substituting an inline scan) have no legal fallback. The INTENT is preserved verbatim: never fake a probe with a web scan.
      - The evidence-routing table's `settled judgment -> the PP card's ## Verdict` route now points at `0-lifecycle/1b-claims/1b-claims.md`, the ONLY home of a claim's status (R7).
      JL resource ruling (pairs with haipipe-paper-resource 1.0.0 + haipipe-paper-lifecycle 2.4.0): RESOURCE registered as a venue-FREE stage between seed and claims. New verb `resource | prereq | prerequisite | need` -> `haipipe-paper-lifecycle resource` -> `0-lifecycle/1a-resource/1a-resource.md`: what must EXIST for this paper to be testable, does it exist, and can it CARRY the claim (data, model checkpoints, and producing-code alike). The stage ASKS (Q<n>) and the probe gateway ROUTES (mints the PP, picks the type) -- so no new probe lane and no new namespace. Venue-coupling prose now reads seed + resource + claims as venue-FREE and unchanged on retarget; the closing-block stage-strip example and the Composing diagram both carry `resource`. resource SHARES the number 1 with claims (precedented: 2a-venue/ and 2b-pitch/ already share 2); nothing renumbers.
260712 · `2.10.0`
      JL routing ruling (haipipe-probe 7.8.0 companion): `probe plan` (the campaign consolidation pass) gains a ROUTE step — resolve every card's `target:` (the receiving task-folder / discovery folder; `NEW ...` when it must be created; `?` only with a stated reason). The campaign pass is the right moment because it is the only one where the whole evidence campaign is visible at once: two cards routed at the same task-folder are a hint they should merge, and a card with no plausible home is a hint the need is under-specified. DRAFT-buffered skeletons may leave `target: ?` — the paper often does not yet know what the project holds.
260712 · `2.9.0`
      JL both-banks layout ruling (pairs with haipipe-probe 7.7.0; supersedes the 2026-06-29 per-stage layout for PROBE CARDS only):
      - PPNN cards live FLAT in `1-probe-plans/PPNN_<slug>.md` beside the campaign README -- one cross-stage pool, `serves:` carries stage affinity, the whole campaign is one `ls`. The `probe "<text>"` BUFFER sub-mode files new cards there; `probe plan` reads all cards from the pool.
      - Execution-bank stubs live in `_ASK/` containers (`<receiving folder>/_ASK/PPNN_<slug>.md`), filename mirroring the card's.
      - `fn/probe-plans.md` rewritten: location + migration direction reversed (legacy per-stage `_PROBE/` cards move INTO the pool on first touch); card anatomy defers to the probe layer's SKILL.md.
260711 · `2.8.0`
      Added (JL cross-stage ruling 2026-07-11; pairs with haipipe-probe 7.5.0)
      - `probe plan` sub-mode: the CAMPAIGN consolidation pass, run after a cross-stage draft sweep — read all stage drafts + all _PROBE/ cards, merge duplicate needs (one card, many serves:), author the dispatch DAG (gating first, refutation-capable early, dependents wait, query-once) into the Campaign section of 1-probe-plans/README.md; Status board stays generated. Campaign is a HUMAN GATE like DRAFT — present and stop; the user's verb advances to "run".
260711 · `2.7.1`
      Changed (two-footed-bridge ruling, JL 2026-07-11; pairs with haipipe-probe 7.4.0)
      - `1-probe-plans/README.md` demoted everywhere it is mentioned (description, probe verb row, probe dispatch note) to a GENERATED index: the per-stage `_PROBE/` cards are the single source of truth; the index regenerates from cards + `_ASK` stubs + answering reports and is never hand-maintained; on disagreement, cards win.
260709 · `2.7.0`
      Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
      - Phase-verb pass-through documented in the routing table: trailing `draft|probe|revise|check` forwards through the lifecycle router to the stage skill; stage skills stop at their human gates and the user's verb advances them.
260708 · `2.6.0`
      Changed (venue lockfile wiring)
      - Venue coupling rule updated: venue stage compiles the pack into `0-lifecycle/2a-venue/2a-venue.md`; the venue-ALIGNED stages consult 2a-venue.md first, with direct `_venue/playbook-<venue>` reads demoted to fallback (2a-venue.md absent) or deep dives via its `[source: ...]` tags.
260704 · `2.5.0`
      Changed (probe-plan location unified, JL 2026-06-29 per-stage ruling wins over the flat buffer)
      - Probe plans live in per-stage `_PROBE/` folders; `1-probe-plans/README.md` is a thin cross-stage index (numbering authority). Verb line, dispatch note, evidence-path map, and fn/probe-plans.md all updated; PP statuses gain `read` (light probe returned, takeaways backfilled into the plan file). `_DISCOVERY_{stage}.md` retired.
      - Legacy layout migration rule (fn/probe-plans.md): flat 1-probe-plans/PPNN files move into their source_stage's _PROBE/ on first touch; legacy _DISCOVERY_ folds into the plan file + citation harvest, then deletes; the move is logged in the stage _LOG.
260703 · `2.4.1`
      Fixed
      - Marker rule tightened from "at most one 🔥 and one 🚀 per line" to EXACTLY one of each, never zero (live seed run rendered `draft 🔥` with no 🚀 anywhere). "Reached" defined as entered-not-completed, so a virgin paper's first phase renders `draft 🔥🚀`; a line with 🔥 but no 🚀 is a rendering defect.
260703 · `2.4.0`
      - create verb RETIRED, absorbed into enter as GET-OR-CREATE (JL: 直接去掉create，enter的时候没有就call create): a missing path CONFIRMS first (repo creation is outward-facing, never off a typo), then runs the same flow (org resolved per invocation, papers-inside recipe, folder scaffold, double-bump) and continues straight into the console. Verbs block, dispatch notes, examples, chooser, argument-hint updated; lifecycle + folder-skill + lifecycle-map cross-references repointed. The create flow itself is unchanged and was validated live (Paper-PhyPatSim run) before the re-homing.
260703 · `2.3.0`
      - stage-strip.sh moved from the shared-reference folder INTO this skill folder (co-located with the Closing Block spec it renders; JL: 为什么 strip 在 wiki 里有这里也有); all 8 references repointed, no strip content left outside this folder.
      - Resolved > JL: / > CC: comment threads archived below verbatim and removed from SKILL.md (comment lifecycle: working doc stays clean, resolved threads move to the log). Companion changes landed in their owners: 08-stage-gate.md Gate Modes (copilot|autopilot) + APPROVAL step + ledger Actor column + Stage Exit Invariant; haipipe-paper-check 1.4.0 (Gate Modes + invariant); haipipe-paper-probe 1.7.0 (From-buffer entry).
      ### Archived comment threads (verbatim)
      **@ Verbs / Dispatch notes**
      > CC: write/edit 的老路由目标 haipipe-paper-edit-write / edit-weaving 在重构后已不存在（对应能力并入 2-phase/2-revise workers，由 stage 内部调用）。我把 write/edit/polish 这些词全部路由到 section-edit stage 了，对吗？还是这组动词干脆退休不再出现在 Verbs 块里？
      > JL: 是的，旧词不要再出现了，省的误导
      > CC: 已退休全部旧词（write/edit/polish/draft/写初稿/整篇润色），section-edit 行只留 section-edit|section|sec|§N。
      > JL: 好，done
      **@ Closing Block (end every reply)**
      > JL: 这个应该有两层吧 一个是stage，一层是phase
      > JL: <--- 这里可以弄的再简单一些吗。比如paper root不要了，然后status和current layer放到一起。
      > JL: 我们是不是也有其他的file也在讲这个，要不把他调到这里，我们single source of truth
      > CC: 三条都已落：两层 strip（stage+phase）、tail 简化为 status·stage + next 两行、01-focus-strip-markers 语义并入本节并删除原文件（enter skill 的引用已改指这里），此节即唯一出处。
      > JL: 我想说你这个跟wiki里的strip的关系是什么，会冲突吗？
      > CC: 不再冲突：wiki 里剩的只是渲染脚本，现已把 10-stage-strip.sh 也搬进本 skill（./stage-strip.sh，与 spec 同住），8 处引用全部改指，wiki 里已无任何 strip 内容。
      **@ Gate-aware (Closing Block)**
      > JL: 你要想着我们有两个mode，一个co-pilot 在check phase的时候，人加上comments，一个是auto pilot，在check的时候，call一个subagent，然后让他给comments 你想想这个我们怎么做。但是是的，必须要有一个judgment，就是这个gate-aware，进入下一个stage要非常的明白，要有confirm，要有一个approval的动作（人或者代替人的subagent）
      > CC: 方案在 chat 里：CHECK 增加 mode=copilot|autopilot，autopilot 派 reviewer subagent 给 comments + approve/revise verdict，gate ledger 记 approval actor；你点头后我改 08-stage-gate.md + haipipe-paper-check。
      > JL: 可以的，你整吧。
      > CC: 已整：08-stage-gate.md 加 Gate Modes 节 + APPROVAL 步骤 + ledger 增 Actor 列；haipipe-paper-check 加 Gate Modes 节（autopilot 派 fresh reviewer subagent 落 > REVIEWER: comments + verdict；bibtex 等人类专属项标 DEFERRED 进 human queue，绝不静默放行）。
      **@ Composing with Evidence Workers**
      > CC: 原文这张图上游还列了 /idea-discovery /run-probe /auto-review-loop /result-to-claim 四个入口，skill 清单里已找不到，我删了。如果它们有新名字（或还想保留占位），告诉我补回。
      **@ Composing with Evidence Workers**
      > CC: 原文头部还有一处孤立引用（"读 lifecycle 参考时也读 ../1-lifecycle/haipipe-display-figure/SKILL.md"），看不出为什么单点名 figure 渲染器，我也删了。有特殊用途的话说一声。
      **@ Composing with Evidence Workers**
      > JL: 我们要不要把所有的wiki的内容也都移到这里来。然后随后把wiki的东西删掉。skill最好还是self-contained
      > CC: 建议不整体搬：共享 reference folder 本就在 paper 家族内部（家族级 self-contained），02/04/08/10 各有 5-10 个 skill 共用，搬进 umbrella 会让每次调用重新变胖；折中方案已执行 01-focus-strip-markers（并入本文件）+ 单消费者页可逐个并入唯一消费者，详见 chat。
      **@ Composing with Evidence Workers**
      > JL: 这个的话，我在想，还都是有haipipe-paper-probe 来进行probe calling？不要让haipipe-paper直接call了，他在一个stage的一个phase的阶段来call。
      > CC: 已改：umbrella 不再直连 /haipipe-probe，probe run 交给 haipipe-paper-probe（stage 的 PROBE phase worker）消费 1-probe-plans/ 再向下分发；Verbs 行、dispatch note、上图已同步。
      > JL: 好，再确认一下。
      > CC: 已确认并补齐另一端合同：haipipe-paper-probe 新增 "From-buffer entry" 节（from-buffer <paper_root> [PPNN]：读 planned 项 → reuse-before-create → 分发 /haipipe-probe → 回写 status/probe_ref → 返回 dispatch summary），两端调用签名一致。
260703 · `2.2.0`
      - JL in-file comment round applied (> JL: / > CC: threads kept in SKILL.md): (1) retired write/edit/polish/draft alias words entirely (省得误导); (2) closing block now TWO-LINE focus strip (stage + phase) with the simplified tail (status·stage merged, paper_root dropped, next only); (3) 01-focus-strip-markers ABSORBED into the Closing Block section as the single source of truth (file deleted; enter skill + 10-stage-strip.sh + the shared-reference index repointed; numbering gap kept); (4) umbrella no longer calls /haipipe-probe directly -- probe run hands 1-probe-plans/ to haipipe-paper-probe (the PROBE phase worker inside a stage's phase), composing diagram + dispatch note + description updated; (5) gate-aware line now names the two approval modes (copilot human / autopilot reviewer subagent), full design pending JL confirm (08-stage-gate.md + check skill).
260703 · `2.1.0`
      - Dedup rewrite (JL: "会有比较重复的地方吗", same treatment as discovery 2.6.0): say each thing ONCE. Command table + keyword map + positional aliases + Routing Step 2 (the same dispatch stated 4 times) merged into one Verbs block + one 6-rule Routing pass; feedback/digest full spec (written twice + fn/) reduced to one pointer section; create recipe (written twice + owner fn) reduced to one dispatch note; probe/venue-coupling/folder-tree/skill-tree restatements replaced by pointers to their owners (fn/probe-plans.md, 03-paper-lifecycle.md, paper-folder-anatomy.md, 06-paper-skill-structure.md). ~545 -> ~200 lines.
      - Stale fixes swept in: 2-claims -> 1-claims backfill refs; 3-narrative.tex -> .md; phantom top-level 2-section-edit/ dir removed from the skill tree (real homes: 1-lifecycle/5-section-edit + 2-phase/); write/edit rerouted to section-edit (old targets haipipe-paper-edit-write/-weaving no longer exist); stage list gained section-edit; "phase skills" wording corrected to stage skills (DPRC phases are internal); retired upstream workflow names dropped from the composing diagram.
      - Three open questions embedded as > CC: markers for JL review (write/edit verb fate, retired upstream workflow names, dropped display-figure reference).
260703 · `2.0.2`
      - create verb added to the front door (JL: should be /haipipe-paper create, not a sub-skill invocation): routes to haipipe-paper-lifecycle folder; repo-backed inside Project-* repos per project/haipipe-project/fn/repo-project.md papers-inside recipe; --org resolved per invocation (paper owner may differ from project owner). Retired prospectus verb/aliases removed (seed replaced it); haipipe-paper-bootstrap specialist entry replaced by haipipe-paper-folder; paper-folder contract tree fixed to current spine (1-claims, 2-pitch, 5-section-edit, .md early stages).
260703 · `2.0.1`
      - phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; phase workers probe/ and revise/).
260622 · `2.0.0`
      - cross-cutting protocol wiring. All stage skills now reference ../1-lifecycle/ref/08-stage-gate.md (confirm-before-advance), ../1-lifecycle/ref/09-stage-illuminate.md (Socratic taste elicitation), 13-tex-quality.md (self-contained compilable tex), 12-evidence-routing.md (\needprobe macro + probe handoff). Stage strip end-of-reply convention enforced. Enter dashboard restructured (pitch summary first). 22 feedback items addressed.
260622 · `1.5.0`
      - probe buffer (1-probe-plans/). Claim-related evidence needs accumulate as probe plans during lifecycle work, then batch-dispatch to /haipipe-probe. Probe is the universal evidence gateway for claims; it calls task/discover during Gather. Direct task/discover verbs kept for non-claim utility work. See fn/probe-plans.md.
260622 · `1.4.0`
      - added probe/discover/task verbs as evidence-worker dispatchers. Paper orchestrator can now route directly to /haipipe-probe, /haipipe-discovery, /haipipe-task with project context resolved from the paper path. Paper stays story layer; evidence workers do the work.
260621 · `1.3.0`
      - renamed paper working-memory layer from feedback to rounds; added lifecycle, rounds, and skill-structure references.
260621 · `1.2.0`
      - made paper lifecycle the delivery-side owner of story/claims and routed GAP/NEED items through the shared delivery-need interface.
260621 · `1.1.0`
      - added enter/status paper-session loader routing.
260531 · `1.0.0`
      - baseline metadata added.

<!-- haipipe:skill:log:end -->
