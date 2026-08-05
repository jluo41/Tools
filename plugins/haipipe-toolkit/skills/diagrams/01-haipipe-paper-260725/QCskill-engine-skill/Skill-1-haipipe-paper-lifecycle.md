# haipipe-paper-lifecycle · v0.5.5
state: 🟡 PARTIAL · account written; the acceptance test is open in Items
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
How does the paper lifecycle keep the Markdown state a writer changes, the first-class Board a human reads, and the venue-free to venue-aligned sequence from drifting apart?

This page is about the structural router and its seam with `haipipe-board`.
It is not a second account of a stage's research content or the Board renderer itself.
Its Seed → Work → Venue sequence below is the Engine's explicit execution pipeline. The Delivery index reads Opening (including Venue) → Work; that reader-facing grouping does not silently reorder stage dependencies.

## Diagram
<!-- haipipe:skill:tree:start 5883bf6a7b5edf8d paper/haipipe-paper-lifecycle -->

**What `haipipe-paper-lifecycle` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-paper-lifecycle/
  feedback/
    2026-06-22_lifecycle-bootstrap-produced-comment-only-tex.md    25 ln  When bootstrapping lifecycle stages for two new papers (Paper-SMSandTiming-IS and Paper-AdaptiveFollowUp-IS),
    2026-06-22_lifecycle-tex-must-use-edit-content-format.md    24 ln  然后lifecycle的paper里，生成这个tex的时候，要符合 Tools/plugins/haipipe-toolkit/skills/paper/3-write-edit/haipipe-paper-edit-c
    2026-06-22_lifecycle-tex-self-contained-not-fragments.md    11 ln  When bootstrapping lifecycle layers, the skill wrote the .tex files as fragments (no \documentclass, no \begin
    2026-06-22_lifecycle-tex-sentence-format.md    27 ln  Reporter (JL): lifecycle 的 paper 里,生成这个 tex 的时候,要符合
    README.md                            9 ln  haipipe-paper-lifecycle — Feedback Inbox
  CHANGELOG.md                         155 ln  haipipe-paper-lifecycle — Changelog
  SKILL.md                             518 ln  Skill: haipipe-paper-lifecycle (orchestrator)
```

<!-- haipipe:skill:tree:end -->

```
paper-stage request
      │
      ▼
haipipe-paper-lifecycle
      ├── venue-FREE: seed → resource → claims
      ├── venue: pin the contract
      ├── venue-ALIGNED: pitch → narrative → display → section-edit
      └── renderers / folder routes when the verb names one
      │
      ▼ after every S-page write
haipipe-board build 0-lifecycle/ ──▶ board/ site + marker report
      │                                broken / unowned / uncited
      └── link the current Board page in the composed Paper session
```

## Content
<!-- haipipe:skill:body:start 5883bf6a7b5edf8d paper/haipipe-paper-lifecycle -->

**haipipe-paper-lifecycle** · `0.5.5` · last shipped 2026-07-26

- folder   `paper/haipipe-paper-lifecycle/`
- tools    Bash, Read, Grep, Glob, Skill
- summary  Router for the lifecycle spine and display family. Each stage runs its declared phases and gates, rebuilds the first-class Board after writes, and returns into the canonical Paper closing block. History: ./CHANGELOG.md.

### SKILL.md



Skill: haipipe-paper-lifecycle (orchestrator)
==============================================

User-facing entry for **paper structural work** -- everything that decides *what the paper is* before prose exists, or when the argument needs rethinking.
This is the **Plan cycle** in the paper mental model (see `paper/README.md`, `../ref/03-paper-lifecycle.md`, and `../ref/04-lifecycle-map.md`).

The lifecycle has a **venue-free / venue-aligned boundary**.
Seed, resource and claims are venue-FREE (they don't change when you retarget to a different journal -- what a paper NEEDS to exist does not depend on where you send it).
Venue is the decision gate that pins the target journal on `S-Venue-0-venue.md`'s `state:` line.
Pitch, narrative, display, and section-edit are venue-ALIGNED (they rewrite when you retarget).

The orchestrator owns routing only.
Each stage specialist owns its own workflow, inputs, and outputs.
The orchestrator never generates narrative, outlines, figures, or diagrams itself.

```
/haipipe-paper-lifecycle                                -> dashboard (list specialists + pipeline)
/haipipe-paper-lifecycle folder <args>                  -> scaffold paper directory (haipipe-paper-folder)
/haipipe-paper-lifecycle seed <args>                    -> 0-lifecycle/0-seed/S-Seed-0-seed.md (venue-FREE)
/haipipe-paper-lifecycle resource <args>                -> 0-lifecycle/1-work/S-Work-0-resources.md
/haipipe-paper-lifecycle claims <args>                  -> 0-lifecycle/1-work/S-Work-1-claims.md
/haipipe-paper-lifecycle venue <args>                   -> 0-lifecycle/2-venue/S-Venue-0-venue.md: the pin on its `state:` line + the venue contract in its body (decision gate)
/haipipe-paper-lifecycle pitch <args>                   -> 0-lifecycle/2-venue/S-Venue-1-pitch.md
/haipipe-paper-lifecycle narrative <args>               -> 0-lifecycle/2-venue/S-Venue-2-narrative.md
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
Internally, each stage skill dispatches the ordered `phases:` declared by that
stage's `stage.md` through the shared workers in `2-phase/`
(`haipipe-paper-draft`, `haipipe-paper-probe`,
`haipipe-paper-revise`, `haipipe-paper-check`). Most current stages declare
DRAFT → PROBE → REVISE → CHECK; Venue declares DRAFT → PROBE → CHECK.
Every current stage declares one human gate, CHECK. Earlier phases run
unattended; phase records and REVISE worker provenance live in the owning S
page's `## Log`.
The agent never self-advances past a gate.

**This router routes users to STAGE skills only -- never to phase skills.**
Phase dispatch is each stage skill's internal business.
If a request sounds like a phase ("gather citations for §3", "polish the intro"), route to the owning stage skill (usually section-edit) and let it dispatch.

Stage artifacts are markdown S pages (`S-<Family>-<n>-<slug>.md`, one family one folder) for every stage except display, which also compiles to `.tex` + PDF (you need to SEE rendered figures/tables).
Stage gates and the illuminate loop are shared conventions: `../ref/08-stage-gate.md`, `../ref/09-stage-illuminate.md`.

---

Specialists
-----------


- 0.1 · Foundation -- what folder + what story
      Stage rows below name the STAGE KEY. All eight are driven by the single skill `haipipe-paper-stage`,
      which loads that key's contract from `haipipe-paper-stage/stages/<order>-<key>/stage.md`.
      ```
      haipipe-paper-folder                  SCAFFOLD:  minimal Board-first scaffold (README + .gitignore + 0-lifecycle/ with board.md and ONE Seed page). No STATUS.md. Everything else is absent-until-allocated; the driver tex / sections/ / 2-src/compile.sh are a later on-request upgrade via haipipe-paper-scaffold. Repo+submodule wiring belongs to /haipipe-paper enter (get-or-create on a missing path).

      --- VENUE-FREE (don't change on retarget) ---

      seed                    SEED (0):    maintain 0-lifecycle/0-seed/0-seed.md: 3 sections (Seed Question, Motivations, Tentative Claim Shape); the venue-FREE contract that keeps a paper possibility alive before evidence matures.

      resource            RESOURCE (1a): maintain S-Work-0-resources.md, the venue-FREE prerequisite contract: what must EXIST for this paper to be testable, does it exist, and can it CARRY the claim? The stage ASKS; PROBE ROUTES within its depth ceiling.

      claims                CLAIMS (1b): maintain the S02 Work claims page, the venue-FREE claim ledger and home of each claim's status (supported | refuted | inconclusive); venue-neutral H1/H2/H3, each claim tied to an entry's answering QA file. Claims reads the entry's `#### a-executor`; the parent topic register records the paper interpretation.

      --- VENUE DECISION (pins target journal in S-Venue-0-venue.md) ---

      venue                  VENUE:       recommend + pin the best-fit venue on S-Venue-0-venue.md, the venue contract aligned stages read first.

      --- VENUE-ALIGNED (rewrite on retarget) ---

      pitch                  PITCH (2):   maintain 0-lifecycle/2-venue/2b-pitch.md, the venue-ALIGNED cover letter and one-minute story; owns Editor's Chair Test, [primary] claim designation, venue-specific RQ framing.

      narrative                   NARRATIVE (3): maintain 0-lifecycle/2-venue/3-narrative.md, the venue-ALIGNED, section-mirrored, evidence-tracked story built from the claim ledger; every beat carries a readiness tag.
      ```

- 0.2 · Display -- what the reader sees (venue-ALIGNED)
      ```
      display              DISPLAY (4): the gallery (the ONLY compiled stage) plus per-unit README.md, float.tex, and preview.pdf under displays/displayNN-<slug>/. Keeps display items tied to claim, evidence source, section, and caption. Consults S-Venue-0-venue.md for the display set and hero rule (Structural Blueprint display units + Writing Principles display limits; pack fallback when S-Venue-0-venue.md is absent). Figure-inventory planning (one claim per figure, panel roles, main vs supplement) is folded in as its figure-logic.md. Framework/architecture mode handles Figure 1 candidate rounds before final rendering.
      ```

- 0.3 · Section editing -- per-section prose work (venue-ALIGNED)
      ```
      section-edit                SECTION-EDIT (5): one S page per section under 0-lifecycle/4-main/ (and 5-appendix/). Each page carries the outline, its state, and its own ## Log; runs the full DRAFT -> PROBE -> REVISE -> CHECK cycle per section and syncs revised prose to sections/*.tex.
      ```

- 0.4 · Display renderers -- visual assets
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
                       the claim? Resource Description + Q-consumer, keyed on H<n>. Data, models,
                       and producing-code alike. Shares the number 1 with claims; renumbers nothing.
            ↓
        claims (1b)     claim/evidence inventory: supported / weak / GAP, with evidence sources
                       venue-neutral H1/H2/H3 hypotheses; no [primary], no RQ framing

        VENUE DECISION
        ──────────────────────────────────────
            ↓
        venue          pin target journal in S-Venue-0-venue.md (gate between FREE and ALIGNED)
                       + maintain S-Venue-0-venue.md, the venue contract the ALIGNED stages read first

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
      The per-stage declared phase cycle above is DEPTH-FIRST — right for maturing one stage.
      For a whole paper, prefer the GLOBAL-PASS order (JL ruling 2026-07-11): probes planned stage-by-stage duplicate questions and miss shared gating dependencies; the evidence needs of a paper only become visible once every stage has a draft.
      ```text
      ① DRAFT SWEEP     draft ALL stages in pipeline order; no human stop
                        ({VAL:?} placeholders + GAP markers + Q-consumer questions are fine;
                        venue still pins BEFORE the venue-ALIGNED drafts)
      ② PROBE-PLAN      /haipipe-paper probe plan — the cross-stage consolidation:
                        merge duplicate questions (one q-executor entry, many topic-register mappings),
                        author the dispatch DAG from the nested S03/S04 entry pages
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
                        `**target**:`, `ls` its QA file, and lands the `#### a-executor`
                        + the parent topic register's interpretation + the S02 claims-page flip
                        + the harvest lanes
                        (query-once: landed answers are read from registries, never
                        re-queried) → then run each stage's remaining declared phases
      ```
      Stage gates are unchanged — a stage's CHECK still verifies ITS cards and registries; the global pass only reorders WHEN drafting and probing happen.
      The campaign rules ARE the five steps above — this block is where they live.
      The per-ENTRY fields a campaign row manipulates (`route:` / `bank:` / `target:` / `state:`) are owned by `probe/haipipe-probe/SKILL.md` "The probe file"; the campaign never redefines them, it only sequences which entries are dispatched and in what order.
      **Retarget rule:** when the venue changes, seed, resource and claims stay unchanged (venue-FREE).
      Pitch, narrative, display, and section-edit all rewrite for the new venue.
      **Venue consumption rule:** aligned stages read
      `0-lifecycle/2-venue/S-Venue-0-venue.md` first. Direct pack reads are fallback
      when it is absent and deep dives through its `[source: ...]` tags. If its
      recorded pack commit is stale, note that and keep using the S page until Venue
      is explicitly refreshed.
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
            resource       1-resource: what must EXIST for this paper to be testable
                                      (Resource Description + Q-consumer)
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
      Board Refresh (every verb that writes an S page ends here)
      ----------------------------------------------------------
      Ruled 2026-07-26 (design board `QA1`, `QA4`): **`/haipipe-paper` is the single thing a human types**, and `enter` leaves them LOOKING at `board.html` in a browser. So a stale board is a
      DEFECT, not an inconvenience: the human is reading a picture of a paper that no longer exists.
      Every verb routed from here that writes an S page ends by rebuilding.
      `haipipe-board` lives outside this family, at `skills/board/haipipe-board/`. Three entry
      points, and the paths are relative to THIS skill folder:
      ```bash
      # 1. REBUILD — after every write. Idempotent, ~1s, safe to over-run.
      python3 ../../../board/haipipe-board/cli/build.py <paper-root>/0-lifecycle

      # 2. WATCH — run once per session in its own terminal, then stop thinking about it.
      #    Polls mtimes and rebuilds on any .md change. This is what makes it SMOOTH:
      #    it also closes the browser's "Sync to md" gap, where a human's comment lands
      #    in the markdown but board.html stays stale until someone runs Python.
      python3 ../../../board/haipipe-board/cli/watch.py <paper-root>/0-lifecycle

      # 3. SERVE — the live layer, port 5599. The human reads
      #    http://127.0.0.1:5599/<repo-relative-path>/0-lifecycle/board.html
      #    NEVER file:// — the live layer is dead there and it is not the same page.
      python3 ../../../board/haipipe-board/cli/serve.py
      ```
      Calling is not owning. `haipipe-board` owns the build, the filename rule, the html and the
      write-back; this router calls it and renders nothing.

- 0.5 · The build's marker report IS the content check
      `build.py` prints one line per unresolved marker it found in the paper's `.tex`. That report is
      not noise to be scrolled past: it is the only thing in the family that cross-checks the prose
      against the `.bib` and against the display units. **Surface it after every rebuild.** Three
      categories, and each is a different defect:
      ```text
      broken    \citep{key} that is NOT in the .bib
                → it compiles to a bare [?]. HUMAN-ONLY fix: an agent never writes bibtex.

      unowned   \cite{TOADD} or {VAL:?} carrying no [Q-…] bracket,
                or a \ref{} resolving to no \label anywhere
                → a hole no question will ever fill, and a ?? in the PDF. The
                  placeholder grammar exists to prevent exactly this (QB6).

      uncited   a display unit's \label referenced by NO section
                → the unit was built and never used, or the section that should
                  cite it has not been written yet. Route to the Display stage.
      ```
      Worked example, `Paper-Personality2Opioid-MISQ2026` on 2026-07-26: 40 pages built, and 22
      markers — 1 broken, 12 unowned, 9 uncited. The 9 uncited are every display unit but one, which
      says the display layer ran ahead of the sections, not that the displays are wrong. That reading
      is the point: the report tells you WHICH LAYER is behind.

- 0.6 · Two lines in board.md that make the chips resolve
      A paper's `0-lifecycle/board.md` must carry both, or `\citep{}`, `{VAL:?}` and `[Q-…]` render as
      plain text and the marker report above is empty and useless:
      ```yaml
      dialect: paper            # opt in to resolving markers at build time
      paper-root: ..            # where the .bib, displays/, and nested topic entries live
      ```
      That one-line seam is the entire paper-specific surface of a generic tool (`QA4`). A board that
      does not declare it renders byte-identical and pays nothing.

- 0.7 · When the build or the push fails
      ```text
      ✅  say what failed, print the path or URL anyway, continue
      ✗   report success when only part of it worked
      ✗   hand-edit board.html — it is generated, always
      ```
      The URL travels over the VS Code IPC socket, and `open` acts on the machine the agent runs on,
      which is not necessarily where the human is sitting. Hand over the URL; do not assume you can
      show it.
      Specialist Return Contract
      ---------------------------
      Each specialist returns this structured payload to its caller:
      ```
      status:    ok | blocked | failed
      summary:   2-3 sentences on what the specialist did
      artifacts: [paths created, read, or modified]
      next:      suggested next /haipipe-paper-lifecycle command
      ```
      The payload is not a second user-visible tail. A direct lifecycle invocation and
      a parent-routed invocation both end with the ONE composed Paper closing block
      defined in `../../haipipe-paper/SKILL.md`: status/next, the active Board deep
      link, and the four-slot phase display line. Omitted declared phases appear as
      `--`. The active stage and gate are derived
      from Board/S pages and artifacts; there is no stage-strip script or status
      cache.
      ---
      Relation to Parent Orchestrator
      --------------------------------
      `haipipe-paper` (in `paper/haipipe-paper/`) is the top-level paper router + Console.
      It resolves status and consults `S-Venue-0-venue.md` for venue fit, falling back
      to the venue pack only when that contract does not exist.
      This orchestrator (`haipipe-paper-lifecycle`) is the direct entry for structural work -- either routed from the Console or invoked by the user directly.
      ```
      haipipe-paper (router)  -- consults S-Venue-0-venue.md for venue fit
                  |                (utd-is: misq/isr/ms-is; pnas; nature-portfolio; jama; clinical; grant; patent)
                  v
      haipipe-paper-lifecycle (this orchestrator)
        VENUE-FREE:
        |-- folder             (lives in 3-deliver/, routed from here)
        |-- seed (0)
        |-- resource (1a)       (prerequisite contract: Resource Description + Q-consumer;
        |                       stage 1a, claims is 1b,
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

      Every stage skill runs its declared phases through the shared 2-phase/ workers
      (haipipe-paper-draft / -probe / -revise / -check); users never invoke those directly.
      Whole-paper delivery tools live in 3-deliver/ (umbrella: haipipe-paper-deliver).
      ```
### The other files

5 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
feedback/2026-06-22_lifecycle-bootstrap-produced-comment-only-tex.md    25 ln  When bootstrapping lifecycle stages for two new papers (Paper-SMSandTiming-IS and Paper-AdaptiveFollowUp-IS),
feedback/2026-06-22_lifecycle-tex-must-use-edit-content-format.md    24 ln  然后lifecycle的paper里，生成这个tex的时候，要符合 Tools/plugins/haipipe-toolkit/skills/paper/3-write-edit/haipipe-paper-edit-c
feedback/2026-06-22_lifecycle-tex-self-contained-not-fragments.md    11 ln  When bootstrapping lifecycle layers, the skill wrote the .tex files as fragments (no \documentclass, no \begin
feedback/2026-06-22_lifecycle-tex-sentence-format.md    27 ln  Reporter (JL): lifecycle 的 paper 里,生成这个 tex 的时候,要符合
feedback/README.md                   9 ln  haipipe-paper-lifecycle — Feedback Inbox
```

<!-- haipipe:skill:body:end -->

## Aims
- [x] 🧱 Make the lifecycle boundary explicit
      The lifecycle router selects a structural owner.  It does not draft the
      narrative, decide a claim, render Board HTML, or call a phase worker as a
      user-facing shortcut.
- [x] 🔄 Preserve the Board-refresh obligation
      Every S-page-writing route rebuilds the generated `0-lifecycle/board/` site and surfaces
      the marker report.  `haipipe-board` still owns rendering and write-back.
- [x] 🧭 Preserve venue coupling
      Seed, resource, and claims are venue-FREE; Venue pins the contract;
      pitch, narrative, display, and section-edit are venue-ALIGNED and must
      re-read that contract when the venue changes.
- [ ] 🧪 Test the board-refresh failure path
      Verify that a failed build or browser push is reported as partial rather
      than being mistaken for a successful lifecycle update.

## States
The page now records the lifecycle's two non-negotiable joins: the venue boundary controls what must be rewritten, and every S-page write refreshes the Board the human is reading.
The failure-reporting branch remains to be exercised independently.

## Log
260727 · Audited against `board.md`'s decision-only rule, which says `state:` is about the DECISION and that implementation does not gate this board. Every open item here is implementation or a test, not an undecided question, so the page was reporting itself as open because code was missing. Flipped with no ruling made.
260727 1435 · Created the lifecycle-router page from `paper/haipipe-paper-lifecycle/`.
Its authored workflow makes the Board refresh and marker-report seam inspectable.

<!-- haipipe:skill:log:start 5883bf6a7b5edf8d paper/haipipe-paper-lifecycle -->

Converted from the skill's own `CHANGELOG.md`: 20 releases.

260726 · `0.5.5` · one Resource vocabulary
      - Updated lifecycle maps to the stage-owned `Resource Description` +
        `Q-consumer` artifact instead of the retired Demand/Questions rows.
260726 · `0.5.4` · current frontmatter contract
      - Removed the unsupported `argument-hint` key so the lifecycle router passes
        the current `skill-creator` validator.
260726 · `0.5.3` · declared phases, one CHECK gate
      - Router documentation now follows each stage's declared phase list.
      - Removed the stale DRAFT gate and `_LOG` provenance contract.
      - Updated live S-page and display-renderer routes.
260726 · `0.5.2` · return into one disk-derived Paper tail
      - Removed the reachable instruction to render a retired stage strip from
        `STATUS.md`.
      - Specialist results are internal payloads; the user sees one composed Paper
        closing block with the active Board link and four-slot DPRC phase line.
260726 · `0.5.1` · the venue pin reads the `state:` line, not an invented frontmatter key
      Found by running the skill against `Paper-Personality2Opioid-MISQ2026` rather than by reading it.
      Yesterday's `STATUS.md` retirement moved the venue pin to "`S-Venue-0-venue.md` frontmatter, `venue:`". That field does not parse. `haipipe-board`'s face grammar is a CLOSED whitelist (`src/parse.py:145`): `state|owner|method|session|requires|style-from|provides|contract-source-hash`. A `venue:` key is invisible to the board, so the frontier predicate failed on the only real paper, and the fix was never going to be "add the key" — the whitelist is `haipipe-board`'s, ruled on its own board.
      The pin needed no new field. It was already on the page's own `state:` line: `state: ✅ PINNED · MISQ 2026`. Corrected in 12 places across the stage contract, the console, the router, the two refs, the anatomy spec and `restructure`.
      Recorded on design-board face `QA4` as the third cross-package gap of the day, with the rule it produced: **`haipipe-paper` may not invent a face-grammar key.** It uses a key that already parses, or it goes to the board's own board and asks.
260726 · `0.5.0` · the router calls haipipe-board, and surfaces its marker report
      New `Board Refresh` section. Before this the router had **zero** references to `haipipe-board`, `build.py` or `board.html`: it dispatched every stage verb, each of which writes an S page, and none of them ever rebuilt the board the human is looking at.
      - **The three entry points, with paths that resolve from this folder**: `build.py` (after every write, idempotent, ~1s), `watch.py` (once per session, polls mtimes, and closes the browser's "Sync to md" gap where a human's comment lands in the markdown but `board.html` stays stale until someone runs Python), `serve.py` (the live layer on 5599; never `file://`).
      - **The build's marker report is documented as the content check**, because nothing else in the family cross-checks prose against the `.bib` and the display units. Its three categories decoded: `broken` (a `\citep{}` not in the `.bib`, HUMAN-ONLY to fix), `unowned` (a placeholder with no `[Q-…]`, or a `\ref{}` with no `\label` — a `??` in the PDF), `uncited` (a display unit no section references). Worked example from `Paper-Personality2Opioid-MISQ2026`: 40 pages, 22 markers, 1/12/9, where the 9 uncited say the display layer ran ahead of the sections rather than that the displays are wrong.
      - **The two `board.md` lines that make chips resolve at all** (`dialect: paper`, `paper-root: ..`). Without them the markers render as plain text and the report above is empty and useless.
      - **Failure rules**: say what failed and print the path anyway; never hand-edit `board.html`; `open` acts on the machine the agent runs on, not necessarily where the human is sitting.
      Implements the single-door ruling (design board faces `QA1` + `QA4`, JL 2026-07-26). Calling is not owning: `haipipe-board` still owns the build, the filename rule, the html and the write-back.
260726 · `0.4.0` · the router names paths that exist
      Aligned with the paper-folder layout ruled 2026-07-26 on the design board (`skills/diagrams/01-haipipe-paper-260725`, face QA6): `0-sections/` to `sections/`, `0-displays/` to `displays/` (one folder per unit, the only home of an asset, no top-level `figures/`), `1-compile.sh` to `2-src/compile.sh`, and `STATUS.md` retired. 14 path corrections across the verb table, the skill roster, the stage descriptions and the two ASCII maps. The router is where a reader learns what a verb produces, so every wrong path here is a wrong expectation set before the work starts.
      Notable: the `haipipe-paper-folder` roster line described the old three-empty-container scaffold including `STATUS.md`; it now describes the Board-first one.
260724 · `0.3.1`
      Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 3.1.1; older entries below keep their original numbers).
260719 · `3.1.0` · the claims router line and ⑤ HARVEST now name the real probe artifacts
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
      ### Changed — the claims router line (ruling B)
      "each claim tied to a probe section's answering QA file ... it reads the section's `a-consumer:`, not a probe verdict" -> "each claim tied to a probe entry's answering QA file ... it reads the entry's `### a-executor` and writes its own a-consumer in the stage doc". The trailing "not a probe verdict" was a ban-list naming a dead thing and is gone per the NO TOMBSTONES rule; the checker owns that enforcement.
      ### Changed — the global-pass ⑤ HARVEST step (ruling B)
      The step said a PROBE re-run "re-resolves each `commissioned` section's target:, `ls` its QA file, and lands the `a-consumer:`". It now re-resolves each `commissioned` **entry's** `**target**:` and lands the `### a-executor` **plus** each Q-consumer's a-consumer in its stage doc. Both sinks are now named, which is the contract clarification behind the minor bump: an agent following the old line would have written the answer into the probe file under a field the checker HARD FAILs.
      Also in that block: "the q-executor block in the section is the bridge" -> "the `### q-executor` block in the entry is the bridge".
260719 · `3.0.1` · retired sidecars erased from the router and the shared `ref/` docs
      This skill owns the shared `1-lifecycle/ref/` reference docs, and both of the load-bearing ones still described the retired sidecar model as the current contract — so an agent consulting the lifecycle map or the stage-gate table would scaffold files nothing reads, and would gate on their existence.
      JL ruling on the removal style, 2026-07-19: "不需要留退役告示，直接抹除任何痕迹" / "follow this rule to do all the following changes."
      Changed (SKILL.md)
      - The section-edit specialist line described the per-section folder as "outline .md, _LOG changelog, _CITATION_ map, _VALUES_ registry" → "outline .md and _LOG changelog".
      Changed (`../ref/04-lifecycle-map.md`)
      - `1-claims` Writes — `+ _LOG + _EVIDENCE_` → `+ _LOG`.
      - `3-narrative` Writes — `+ _LOG + _DISPLAY_` → `+ _LOG`, plus the DR rows it files in `0-lifecycle/4-display/_DISPLAY_REQUEST.md` (the display stage owns that file and its statuses).
      - `5-section-edit` Writes — `(outline .md, _LOG, _CITATION_, _VALUES_)` → `(outline .md, _LOG)`.
      Changed (`../ref/08-stage-gate.md`)
      - The section-edit exit question no longer requires a scaffold containing `_CITATION_ + _VALUES_`; it asks for `outline + _LOG`, and adds the check that actually matters now — every `\cite{TOADD}` / `{VAL:?}` carries its `[Q-<Stage>-<n>]` anchor bracket.
      Untouched (deliberately)
      - Every `mode: light | full` reference — deferred to a separate review.
      - `_DISPLAY_REQUEST.md` — alive.
260714 · `2.4.0`
260714 · `3.0.0`
      - PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
      - CAMPAIGN DAG DEADLOCK FIXED: step ③ told a dependent card to 'wait for `answers:`' — a field DELETED from both banks, so the wait could never end. A dependent SECTION now waits until its upstream section's `target:` QA FILE EXISTS ON DISK (state: answered). Step ③ also now MATCHes before dispatching.
      Added (JL resource ruling 2026-07-14; pairs with haipipe-paper-resource 1.0.0 + haipipe-paper 2.11.0)
      - RESOURCE registered as a lifecycle stage everywhere this router enumerates stages: the verbs block (`resource <args>` -> `0-lifecycle/1a-resource/1a-resource.md`), the Specialists list (`haipipe-paper-resource  RESOURCE (1)`), the Natural Pipeline Order, the Routing Logic stage set, the Function Keyword Map + positional aliases, the no-arg dashboard, and the parent-orchestrator diagram.
      - Venue boundary prose now reads seed + resource + claims as venue-FREE (what a paper NEEDS to exist does not depend on where you send it); the Retarget rule says the same.
      - resource SHARES the number 1 with claims, deliberately -- precedented on disk by 2a-venue/ and 2b-pitch/. No other stage renumbers; `stage-strip.sh` strips the digit and keys on the bare name `resource`.
260711 · `2.3.0`
      Added (JL cross-stage ruling 2026-07-11; pairs with haipipe-probe 7.5.0 + haipipe-paper 2.8.0)
      - "Global-pass mode (breadth-first — the whole-paper cycle)" section after the Natural Pipeline Order: ① DRAFT SWEEP all stages (placeholders/GAPs fine; venue still pins before the ALIGNED drafts) → ② PROBE-PLAN (`/haipipe-paper probe plan`, campaign consolidation, HUMAN GATE) → ③ HANDOFF BATCH per the DAG → ④ RUN (task/discovery sessions — often a separate concurrent session) → ⑤ HARVEST (query-once) then REVISE/CHECK per stage. Depth-first per-stage cycles remain valid for single-stage work; stage gates unchanged.
260709 · `2.2.0`
      Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
      - Phase-verb pass-through: trailing `draft|probe|revise|check` after stage args forwards verbatim to the stage skill.
      - Two-axis section updated: TWO human gates (DRAFT structure review + CHECK), REVISE proof-carrying, agent never self-advances (was "CHECK is the only human-involved phase").
260708 · `2.1.0`
      Changed
      - Routing description adopts venue lockfile semantics: venue stage compiles 0-lifecycle/2a-venue/2a-venue.md (the venue contract with pack+outlet+commit provenance); new Venue consumption rule -- aligned stages read 2a-venue.md FIRST (pitch: Venue Profile + Fit Assessment; narrative: Blueprint beats + Writing Principles; display: display units + limits; section-edit: per-section Blueprint block), packs only as fallback when 2a-venue.md is absent or as deep dives via its [source] tags; stale provenance -> "venue contract stale" note, never silent pack re-reads.
260703 · `2.0.3`
      Fixed
      - Closing-line rule updated: stage skills close with the FULL closing block (simplified tail + stage line + phase line) per the umbrella Closing Block section, not just the stage strip line.
260703 · `2.0.2`
      - haipipe-paper-folder specialist description updated to the minimal quick scaffold (absent-until-written; manuscript machinery on request; repo wiring belongs to /haipipe-paper create); seed description corrected to the 3-section contract; retired prospectus / kill-criteria keywords removed from the maps.
260703 · `2.0.1`
      - phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers 2-phase/1-probe/haipipe-paper-probe*, 2-phase/2-revise/haipipe-paper-revise*).
260703 · `2.0.0`
      - lifecycle reordered to the current spine (claims (1) before pitch (2), venue as the decision gate between them); minimap stage removed; section-edit added as stage 5 (per-paper folder renamed 5-editing -> 5-section-edit); two-axis restructure documented (stage skills x DRAFT->GATHER->POLISH->CHECK phases via 2-phase/ workers, CHECK the only human-involved phase); folder dispatch fixed to haipipe-paper-folder; shared conventions repointed to the numbered shared-reference docs.
260608 · `1.0.0`
      - created as orchestrator over all 1-lifecycle specialists.

<!-- haipipe:skill:log:end -->
