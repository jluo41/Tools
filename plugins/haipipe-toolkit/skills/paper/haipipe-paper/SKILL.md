---
name: haipipe-paper
description: "Run any paper-lifecycle work. Use `/haipipe-paper enter <paper-path>` or `/haipipe-paper status [paper-path]` to preload an open-needs paper dashboard from STATUS.md, 0-lifecycle, 1-rounds, 0-displays, 0-sections, and git state. Paper lifecycle owns paper-specific story, angle, claims, narrative, displays, minimap, maturity, and dated work rounds; open GAP/NEED items can call probe/discover/task/insight directly through the shared delivery-need interface. Also parses intent (venue + phase) and dispatches to specialists for writing/revising/rebutting papers targeting ICLR, NeurIPS, ICML, Nature, PNAS, MISQ, ISR. Trigger: paper, enter paper, paper status, open needs, claim gap, figure table gap, round, paper round, work round, write paper, paper pipeline, paper writing, draft paper, revise paper, polish tex, rebuttal, reply to reviewers, 写论文, 论文流程, /haipipe-paper."
argument-hint: "[enter|status|venue|phase] [paper-path-or-args...]"
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "1.3.0"
  last_updated: "2026-06-21"
  summary: "Run any paper-lifecycle work."
  changelog:
    - "1.3.0 (2026-06-21): renamed paper working-memory layer from feedback to rounds; added lifecycle, rounds, and skill-structure references."
    - "1.2.0 (2026-06-21): made paper lifecycle the delivery-side owner of story/claims and routed GAP/NEED items through the shared delivery-need interface."
    - "1.1.0 (2026-06-21): added enter/status paper-session loader routing."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-paper (orchestrator)
====================================

User-facing entry for the paper lifecycle. The paper lifecycle is a delivery
owner: it owns this paper's angle, claims, narrative, section map, displays,
minimap, maturity, and dated work rounds. Project-level evidence lives outside
the paper in probes, discoveries, tasks, and insights.

When the paper hits a gap, record or surface a delivery need and route directly
to the relevant evidence worker. Do not route through a project-level narrative
layer. Use `../ref/delivery-need.md` when creating or interpreting
GAP/NEED records.

This orchestrator parses intent and dispatches to the right venue specialist
via `Skill()`. Lifecycle phase skills (pitch, claims, narrative, display,
write, compile, revise, review, present) are called by the specialist, not by
this orchestrator directly.

For the canonical paper structure, read `README.md` at the paper skill root.

Stage Strip (end every reply)
------------------------------

In a paper session, END every reply with the lifecycle stage strip so the user
always sees which stage we are in. Place it as the VERY LAST line of the reply,
AFTER the machine-readable return-contract tail (`status` / `paper_root` /
`current_layer` / `next`). It is the closing line, not the opening one. Spine
order is fixed:

```text
seed -> pitch -> claims -> narrative -> display -> minimap -> write/edit -> review
```

Read `current_layer` from the paper's `STATUS.md`. Mark each stage ✅ before
current, ▶️ at current, ⬜ after current; arrows sit before `write/edit` and
`review`. One line, e.g.:

```text
seed ✅  pitch ✅  claims ✅  narrative ✅  display ✅  minimap ✅  →  write/edit ▶️  →  review ⬜
```

Render it DETERMINISTICALLY with the helper (never hand-type it; it drifts):

```sh
sh "$CLAUDE_SKILL_DIR/../ref/stage-strip.sh" <paper-dir>   # walks upward for STATUS.md
```

Closing-block format. End every reply with ONE fenced `text` block: a TITLED top
rule, the return-contract tail, a plain bottom rule, then the strip as the last
line. Use box-drawing `─` (U+2500) for the rules (no corners, no side borders).
The top rule carries the label `📄 paper · <current_layer> ▶️`:

    ── 📄 paper · claims ▶️ ───────────────────────
    status:        ok|blocked|failed
    paper_root:    <path>
    current_layer: <layer>
    next:          <single recommended command>
    ──────────────────────────────────────────────
    seed ✅  pitch ✅  claims ▶️  narrative ⬜  display ⬜  minimap ⬜  →  write/edit ⬜  →  review ⬜

The strip line still comes from the helper; only its framing (titled top rule +
bottom rule) is added here. Every stage / enter skill inherits this closing block.

Gate-aware: advancing `current_layer` to the next stage requires an EXPLICIT user
confirm that the current stage is done (the Stage Gate). Once `STATUS.md` carries
the gate confirmation ledger, ✅ means "user-confirmed", not merely "before
current". See `../ref/delivery-need.md` (autonomy policy) and the Stage Gate
feedback.

Read these references when the task touches lifecycle shape, rounds, or skill
organization:

```text
ref/paper-lifecycle.md
ref/paper-rounds.md
ref/lifecycle-map.md
ref/paper-skill-structure.md
../1-lifecycle/haipipe-paper-display-figure/SKILL.md
```

```
/haipipe-paper                              -> enter current paper if detectable; else dashboard
/haipipe-paper enter "<paper-path>"         -> preload open-needs paper session dashboard
/haipipe-paper status ["<paper-path>"]      -> same as enter; path optional
/haipipe-paper venue ["<topic|paper>"] [--no-pin]  -> recommend + pin best-fit journal (-> haipipe-paper-venue)
/haipipe-paper <stage> ["<input>"]          -> seed|pitch|claims|narrative|display|minimap (-> haipipe-paper-lifecycle)
/haipipe-paper write|edit ["<input>"]       -> draft / polish prose (-> 3-write-edit)
/haipipe-paper rebuttal "<paper-path>"      -> dispatch to rebuttal specialist
/haipipe-paper prospectus "<project-or-paper>"  -> create/inspect paper-prospectus folder
/haipipe-paper feedback "<text>"            -> capture skill feedback to feedback/ (`feedback list` shows open)
/haipipe-paper "<natural language>"         -> infer intent from keywords, dispatch
```

Examples:
```
/haipipe-paper venue "examples/ProjB-PhyTrait-OpioidRx/paper/Paper-Personality-Opioid-MedJournal"
/haipipe-paper venue "physician trait -> opioid prescribing; observational CMS Medicare" --no-pin
/haipipe-paper enter "examples/ProjB-PhyTrait-OpioidRx/paper/Paper-Personality-Opioid-MedJournal"
/haipipe-paper status
/haipipe-paper claims          (designate the venue-coupled primary claim)
/haipipe-paper display "Table 1 + STROBE flow + subgroup forest"
/haipipe-paper prospectus "examples/ProjC-LLMRecPhysicain/paper/Paper-LLMPhysicianRanking"
/haipipe-paper rebuttal "paper/"
```

---

Specialists
-----------

```
haipipe-paper-enter       Status-aware paper session loader
                          (read STATUS.md + lifecycle/rounds/displays/sections/git,
                           report current layer, maturity, open needs, open gates, next commands)
haipipe-paper-bootstrap
                          Paper folder bootstrap, including prospectus mode
                          (STATUS.md + sparse 0-lifecycle, no manuscript obligations)
                          and manuscript mode (full 0-/1-prefix tex scaffold)
haipipe-paper-venue       Venue-first front door: analyze the topic/paper, recommend
                          the best-fit journal from the _venue/playbook-* packs, and
                          pin STATUS venue (run before claims; owns label->pack map)
haipipe-paper-lifecycle   Stage orchestrator (seed→pitch→claims→narrative→display→minimap)
3-write-edit/*            Prose: write / edit / polish
                          (haipipe-paper-edit-write drafts, -edit-weaving polishes;
                           replaces the retired -create / -revise pipelines)
haipipe-paper-rebuttal    Submission rebuttal pipeline (venue-agnostic)
                          (parse reviews → strategy → draft → coverage check)

Venue is knowledge, not a pipeline. Consult _venue/playbook-<venue>
(misq / isr / ms-is / pnas / nature-portfolio / jama / clinical-medicine;
 grant; patent-*) for what the target rewards. The retired -conference /
-journal / -is workflow shells folded into the lifecycle + _venue/README.md.
```

---

Venue Keyword Map
------------------

```
venue, which journal, where to submit, venue fit,
recommend journal, journal selection, pick venue, 选刊, 投哪,
MISQ, ISR, Management Science, UTD-IS, Nature, PNAS,
JAMA, NEJM, Lancet, clinical, grant, patent             -> venue (haipipe-paper-venue)
rebuttal, reply, response, OpenReview response,
reviewer comments, review-response, R1 revision        -> rebuttal
enter, status, dashboard, preload, session,
paper status, enter paper, aware mode                   -> enter
round, rounds, paper round, work round, latest round,
todo, decisions, applied                                -> round
prospectus, paper prospectus, topic appears, project seed,
paper seed, paper folder, bootstrap folder              -> structure-bootstrap
write, draft tex, from narrative, new paper,
scaffold paper, 写初稿                                  -> write (haipipe-paper-edit-write)
edit, polish, polish tex, paragraph polish,
walk sections, whole-paper revision, 整篇润色           -> edit (haipipe-paper-edit-weaving)
```

Venue/task aliases (positional):
```
venue, journal, misq, isr, msis, nature,
pnas, jama, clinical, grant, patent, 选刊  -> venue
rebuttal, reply, response, rev             -> rebuttal
enter, status, dashboard, preload          -> enter
prospectus, folder, bootstrap                  -> structure-bootstrap
write, draft, new, scaffold                -> write
edit, polish, walk                         -> edit
```

Lifecycle stage verbs (positional), forwarded to the stage procedures:
```
seed                                       -> structure seed
pitch                                      -> structure pitch
venue, journal                             -> haipipe-paper-venue (recommend + pin; before claims)
claims, claim, ledger                      -> structure claims
narrative                                  -> structure narrative
display, figures, figures-tables           -> structure display
table, tables                              -> structure table       (haipipe-paper-display-table)
figure, plot                               -> structure figure      (haipipe-paper-display-figure)
diagram, figure-spec, vector               -> structure diagram     (haipipe-paper-display-diagram)
illustration, ai-img                       -> structure illustration (default, Codex bridge)
illustration-gemini, gemini                -> structure illustration-gemini (fallback)
figure1, framework                         -> structure framework   (display framework mode)
minimap                                    -> structure minimap
round, rounds                              -> round (haipipe-paper-round)
```

Note: `write` and `edit` (formerly `create`/`revise`) route to
`3-write-edit`. The venue is pinned once by `venue` (-> haipipe-paper-venue)
into STATUS, and each stage consults the matching `_venue/playbook-<venue>` pack.

---

Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.

Step 2: Resolve venue/task:
  - First positional matches a venue/task alias?      -> dispatch target = that
  - First positional is "enter" or "status"            -> target = enter
  - First positional is a lifecycle stage verb
    (seed/pitch/claims/narrative/display/table/figure/diagram/
    illustration/illustration-gemini/figure1/framework/
    minimap)                                          -> target = structure <verb>
  - First positional is "round" or "rounds"            -> target = round
  - First positional is "feedback"                     -> target = feedback (utility verb)
  - Else scan keyword map across all positional args.
  - Phrase contains "reply to reviewers" / "rebuttal"
    / review-related verbs                            -> target = rebuttal
  - Phrase contains "enter paper" / "paper status" /
    "preload" / "dashboard" / "aware mode"             -> target = enter
  - Phrase contains "paper prospectus" / "topic appears" /
    "project seed" / "paper folder" / "bootstrap
    folder"                                           -> target = structure-bootstrap
  - Phrase contains "draft tex" / "new paper" /
    "scaffold" / "from narrative"                     -> target = write (haipipe-paper-edit-write)
  - Phrase contains "polish" / "edit" / "walk
    sections" / "paragraph polish"                    -> target = edit (haipipe-paper-edit-weaving)
  - Topic names a journal/venue (MISQ/ISR/Nature/PNAS/
    JAMA/clinical/ICLR/NeurIPS/grant/patent) or asks
    "which journal / where to submit"                 -> target = venue (haipipe-paper-venue)
  - Default if a 0-lifecycle/3-narrative exists with no
    venue hint                                        -> ASK (don't guess)

Step 3: Decide handling:
  - No args and current directory is a paper root
    (`STATUS.md`, `0-lifecycle/`, or `0-*.tex` +
    `0-sections/`)                                    -> target = enter, args="."
  - No args and no paper root                         -> usage dashboard (inline)
  - venue/task resolved, no other args                -> dispatch with "(none)"
  - venue + input/args                                -> dispatch with full args
  - input but no venue                                -> ASK which venue

Step 4: Dispatch:
    If target = enter:
      Skill("haipipe-paper-enter", args="<remaining_args or .>")
    Else if target = structure-bootstrap:
      Skill("haipipe-paper-bootstrap", args="<remaining_args>")
    Else if target = "structure <verb>":
      Skill("haipipe-paper-lifecycle", args="<verb> <remaining_args>")
    Else if target = round:
      Skill("haipipe-paper-round", args="<remaining_args>")
    Else if target = feedback:
      Read fn/feedback.md and run it inline: capture "<text>" to feedback/ as one
      dated file, or `feedback list` to print open items. This orchestrator
      handles feedback directly; no sub-skill, no fix attempted on the spot.
    Else:
      Skill("haipipe-paper-<target>", args="<remaining_args>")

Step 5: Capture the specialist's structured tail (status / summary /
        artifacts / next), present it.
```

---

No-Arg Mode (status first, then usage dashboard)
------------------------------------------------

When invoked with no arguments, first check whether the current directory is
inside a paper root. A paper root is any directory upward containing one of:

- `STATUS.md`
- `0-lifecycle/`
- `0-*.tex` plus `0-sections/`
- `1-compile.sh` plus `0-sections/`

If a paper root is found, dispatch:

```
Skill("haipipe-paper-enter", args="<detected-paper-root>")
```

Only if no paper root is found, do not fan out. Emit a compact venue chooser:


```
📄 haipipe-paper: no paper detected. Pick an entry:

  venue       recommend + pin the best-fit journal for a topic or paper.
              Analyzes fit across the _venue/playbook-* packs, writes STATUS venue.
              Start here if the venue is undecided (venue-first).
              /haipipe-paper venue "<topic or paper-path>" [--no-pin]

  prospectus  scaffold an early paper folder (seed-only, no manuscript obligations).
              /haipipe-paper prospectus "<project-or-paper>"

  enter       open an existing paper's console (status, open needs, frontier).
              /haipipe-paper enter "<paper-path>"

  write|edit  draft / polish prose for an existing folder (3-write-edit).
  rebuttal    parse reviews + draft a rebuttal (any venue, post-review).

Next: /haipipe-paper <entry> "<input>"
```

---

Disambiguation Rules
---------------------

  - Venue unclear / undecided → run `venue` (haipipe-paper-venue) to recommend and
    pin. Do NOT default to a venue silently: venue choice drives style, page limit,
    and structure decisions that are expensive to redo.
  - User says "paper" with no venue pinned + has a narrative → run `venue` first.
  - User says "rebuttal" + provides paper path → dispatch to rebuttal immediately
    (rebuttal is venue-agnostic).
  - Re-targeting ("move this paper to another journal") → run `venue` to re-pin;
    `2-claims` then re-couples to the new target. Do NOT chain blindly.

---

Specialist Return Contract
---------------------------

Each specialist should return a tail block:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what the specialist did
artifacts: [paths created, read, or modified]
next:      suggested next command (often a lifecycle stage skill like
           /haipipe-paper-minimap, /haipipe-paper-display-figure, /haipipe-paper-edit-write, or a re-invocation
           of /haipipe-paper for a different phase)
```

---

Delivery Need Routing
---------------------

Paper work is demand-driven. A paper paragraph, claim, figure, table, or
round todo item may reveal that the next action is a probe, discovery, task,
display unit, or insight. The `enter/status` path must surface those needs
before recommending more writing.

Use this shared reference when interpreting or creating need records:

```
../ref/delivery-need.md
```

Routing hints:

```
claim needs a verdict or robustness check       -> /haipipe-probe plan from-need <need>
claim needs outside literature/context          -> /haipipe-discover <question>
claim/display needs a run or data artifact      -> /haipipe-task <contract>
figure/table needs materialized output          -> /haipipe-task-for-display <need>
closed evidence needs reusable meaning/caveat   -> /haipipe-insight <artifact>
wording/section placement needs paper work      -> paper lifecycle stage/edit skill
```

The paper backfills resolved evidence into `2-claims`, `4-display`,
`5-minimap`, sections, or round logs. Evidence workers do not own the paper
story.

Relation to Lifecycle Stage Skills, Sections, and Components
-------------------------------------------------------------

The orchestrator and the venue profiles in `_venue/` operate at the workflow
level. Underneath, skills are grouped to mirror the lifecycle spine. The
canonical tree is in `README.md` and `ref/paper-skill-structure.md`; the
stage-to-procedure map is in `ref/lifecycle-map.md`. In brief:

```
0-enter/        haipipe-paper-enter (Paper Console)
1-lifecycle/    haipipe-paper-lifecycle (orchestrator) + one skill per stage:
                -{seed,pitch,claims,narrative,display,minimap}
                display renderers: -display-table (LaTeX tables), -display-figure
                (data plots), -display-diagram (vector SVG), -display-illustration
                (AI concept art, default Codex bridge) + -display-illustration-gemini (fallback)
                (architecture blueprint + plan outline are now folded into
                 -minimap, figure-planner into -display; see their ref/)
2-rounds/       haipipe-paper-round (enter/new/triage/apply/close)
3-write-edit/   haipipe-paper-edit (orchestrator) + write* + edit topic subs +
                the self-review audit cluster (-edit-claim-audit, -edit-reviewer,
                -edit-proof-checker, -edit-submission-audit, -edit-manual-review-*,
                -edit-check-reference) + sections/ per-section playbooks
4-build-submit/ haipipe-paper-folder (scaffold) + -build-{scaffold,restructure,check}
5-respond/      paper-rebuttal, rebuttal-response
6-present/      paper-slides, paper-poster
components/     citation (audit/verifier/guide), compile, diff (cross-cutting)
```

Per-section playbooks live in `3-write-edit/sections/` and are read by the
write/edit/review skills when they target a specific `.tex` under `0-sections/`.
Components are cross-cutting: figures and citations are touched during
write/review. Power users can invoke any skill directly by its slash command;
the orchestrator is the right entry when you do not yet know the stage or venue.

Paper-folder contract
----------------------

All paper skills assume their input is a paper folder following the
layout:

```
<paper>/
├── STATUS.md                               paper state, maturity, active round
├── 0-<paper>.tex / .bib                    master shell
├── 0-Supplementary-<paper>.tex             optional SI master
├── 0-lifecycle/                            tex-first lifecycle spine
│   ├── 0-seed/0-seed.tex
│   ├── 1-pitch/1-pitch.tex
│   ├── 2-claims/2-claims.tex
│   ├── 3-narrative/3-narrative.tex
│   ├── 4-display/4-display.tex
│   └── 5-minimap/5-minimap.tex
├── 0-sections/                             manuscript prose .tex files
├── 0-displays/                             display units, one folder per figure/table family
│   ├── display01-<slug>/
│   ├── display02-<slug>/
│   └── displayNN-<slug>/
├── 1-rounds/                               dated paper work rounds
│   ├── latest.md
│   └── vYYMMDD/
│       ├── README.md
│       ├── discussion.md
│       ├── decisions.md
│       ├── todo.md
│       └── applied.md
├── 1-config.yaml                           paths + metric definitions
├── 1-compile.sh                            build script
├── 1-diff/vs-<ref>/                        diff packages
└── 1-review/{A-E,DECISIONS.md,HANDOFF.md}/ active review session pipeline
```

A revision **session** = a git branch (e.g. `review_v0325`); paper
skills are branch-agnostic at the file level.

---

Composing with Other Workflows
-------------------------------

```
/idea-discovery       → IDEA_REPORT.md
/run-probe       → experiment results
/auto-review-loop     → AUTO_REVIEW.md
/result-to-claim      → CLAIMS_FROM_RESULTS.md
/haipipe-paper-narrative     → 0-lifecycle/3-narrative/3-narrative.tex
        │
        ▼
/haipipe-paper        ← you are here (router)
        │
        ├─► /haipipe-paper-lifecycle   (seed→…→minimap structural spine)
        ├─► /haipipe-paper-edit-write  (narrative+plan → fresh tex prose)
        ├─► /haipipe-paper-edit-weaving (existing tex → polish)
        ├─► /haipipe-paper-rebuttal    (any venue, post-review)
        └─► consult _venue/playbook-<venue>  (what the target rewards)
```

---

## Feedback

`/haipipe-paper feedback "<text>"` captures a complaint / confusion / wish about THIS
skill into `feedback/` (one dated file per item, `status: open`) to fix in a
later revision pass. `/haipipe-paper feedback list` shows the open items. This is
feedback about the tool, not the work it produces. Route a `feedback` first-token
here before other parsing. Full convention: `feedback/README.md`.
