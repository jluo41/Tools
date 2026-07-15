---
name: haipipe-paper
description: "Run any paper-lifecycle work: parse intent (venue + stage) and route to the stage specialists. Each stage runs four phases (draft → probe → revise → check); evidence enters ONLY through the PROBE phase, which raises questions as sections in 1-probes/PPNN_<topic>.md and dispatches them through a clean agent. `enter`/`status` open the paper's open-needs dashboard. Trigger: paper, enter paper, paper status, venue, seed, resource, claims, pitch, narrative, display, section-edit, round, rebuttal, probe, evidence, 写论文, 论文流程, /haipipe-paper."
argument-hint: "[enter|status|venue|stage] [paper-path-or-args...]"
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "3.1.0"
  last_updated: "2026-07-14"
  summary: "Front door for the paper lifecycle: parse intent (venue + stage), route to the stage specialists. Each stage runs four phases (draft → probe → revise → check); the paper RAISES evidence questions as sections in 1-probes/, and each stage's PROBE phase dispatches them through a clean agent — the paper never calls the bank directly. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper (orchestrator)
====================================

User-facing entry for the paper lifecycle.
The paper lifecycle is a delivery owner: it owns this paper's angle, resources, claims, narrative, section map, displays, maturity, and dated work rounds.
Project-level evidence lives outside the paper in tasks and discoveries; when the paper hits a gap, record a delivery need (`../wiki/11-delivery-need.md`) and route to the evidence worker.

This orchestrator parses intent and dispatches to stage/specialist skills via `Skill()`.
Stage skills internally drive the DPRC phase workers (`2-phase/`); users and this router never invoke phase skills directly.
Canonical structure: `README.md` at the paper skill root + `../wiki/06-paper-skill-structure.md`.

ALWAYS read and honor `PREFERENCES.md` (this skill's own folder): portable, git-tracked global behavioral preferences that survive a machine change.
`digest` / `feedback` append flagged global prefs there (merge-or-create).

The model: stages × four phases
--------------------------------

The front door exposes STAGES, not executors.
A user advances a stage; each stage runs the same four phases:

```text
   DRAFT ──▶ PROBE ──▶ REVISE ──▶ CHECK
   write &   collect    weave in    human
   raise     evidence   the answer  gate
```

PROBE is the ONLY phase that touches the bank, and it reaches it only through a probe file and a clean-context agent — the paper session never runs bank work itself.
There is no `discover` or `task` verb: calling the bank is the PROBE's job, not the paper's.
A standalone utility question a human wants (a quick lit scan, a data check) goes to the bank's OWN door — `/haipipe-task qa` or `/haipipe-discovery qa` — typed by a person, never proxied by the paper.


Verbs
------

One block: verb, aliases and trigger keywords, then where it goes.

```
enter | status | dashboard | preload         -> haipipe-paper-enter (open-needs console; GET-OR-CREATE: a missing path offers to create the paper first, see Dispatch notes; also "enter paper", "paper status", "create paper", "new paper folder")
venue | journal | 选刊 | any venue name       -> haipipe-paper-venue (recommend + pin; MISQ/ISR/Management Science/Nature/PNAS/JAMA/NEJM/Lancet/clinical/grant/patent all land here)
seed                                         -> haipipe-paper-lifecycle seed        (also "paper seed", "why this paper")
resource | prereq | prerequisite | need      -> haipipe-paper-lifecycle resource    (venue-FREE; what must EXIST for this paper to be testable, does it exist, can it CARRY the claim -- data, model checkpoints and producing-code alike; also "do we have the data", "does the checkpoint exist", "demand", "1-resource")
claims | claim | ledger                      -> haipipe-paper-lifecycle claims      (also "claim gap", "supported", "GAP", "H1/H2/H3")
pitch                                        -> haipipe-paper-lifecycle pitch       (also "cover letter", "one-minute story", "editor's chair")
narrative | story | contract                 -> haipipe-paper-lifecycle narrative
display | figures | figures-tables           -> haipipe-paper-lifecycle display     (also "figure plan", "gallery", "preview pdf")
section-edit | section | sec | §N            -> haipipe-paper-lifecycle section-edit (per-section prose work)
table | figure | plot | diagram |
  illustration | figure1 | framework         -> haipipe-paper-lifecycle <renderer verb> (display renderer family; 做表/画图/架构图)
round | rounds                               -> haipipe-paper-round (dated work rounds; also "todo", "decisions", "applied")
probe ["<question>"] | probe | probe plan | probe run [PPNN]  -> the probe-file pool: 1-probes/PPNN_<topic>.md, one file per TOPIC, one SECTION per question (RAISE / SHOW the board / PLAN the cross-stage campaign / RUN the five-step loop; the probe FILES are the source of truth — the README's Status board regenerates from them, its Campaign section is authored by "plan"; "run" hands the pool to haipipe-paper-probe; also "evidence gap", "verify claim", "hypothesis", "probe campaign", "consolidate probes")
rebuttal                                     -> haipipe-paper-rebuttal (also "reply to reviewers", "reviewer comments", "OpenReview response", "R1 revision")
feedback "<text>" | feedback list|move       -> fn/feedback.md (resolve BEFORE other parsing)
digest [session] [--dry-run]                 -> fn/digest.md   (resolve BEFORE other parsing)
"<natural language>"                         -> infer via the keywords above, dispatch
```

**Phase-verb pass-through**: a trailing `draft | probe | revise | check` after any stage verb's args is a PHASE VERB — forward it verbatim through the lifecycle router to the stage skill (e.g. `/haipipe-paper edit 4-llmtrait revise` → section-edit drives its REVISE phase).
Stage skills stop at their human gates (DRAFT review, CHECK); the user's verb is what advances them — never advance a gate on the user's behalf.

Examples:

```
/haipipe-paper enter "examples/Project-PhyPat-Simulation/papers/Paper-PhyPatSim"
/haipipe-paper enter papers/Paper-NewIdea --org jluo41    (missing path -> confirms, then creates)
/haipipe-paper venue "physician trait -> opioid prescribing; observational CMS Medicare" --no-pin
/haipipe-paper claims
/haipipe-paper display "Table 1 + STROBE flow + subgroup forest"
/haipipe-paper probe "NEED-1: expand ex ante audit to all 20 messages"
/haipipe-paper probe run PP02
```

Routing
--------

Resolution order (first match wins):

```
1. feedback / digest first-token             -> run the fn (before any other parsing)
2. first positional matches a verb/alias     -> that target
3. keyword scan over the whole phrase        -> per the trigger keywords in the Verbs block; a named journal/venue anywhere -> venue
4. no args, cwd inside a paper root          -> enter "."
5. no args, no paper root                    -> chooser (below)
6. input but target unclear                  -> ASK; NEVER silently default a venue (venue drives pitch/narrative/display/prose, expensive to redo)
```

A paper root is any directory upward containing `STATUS.md`, `0-lifecycle/`, `0-*.tex` + `0-sections/`, or `1-compile.sh` + `0-sections/`.

Venue coupling (drives two routing rules): seed + resource + claims are venue-FREE; venue pins the journal in STATUS.md between claims and pitch AND compiles the pack into the paper's `0-lifecycle/2-venue/2-venue.md`; pitch/narrative/display/section-edit are venue-ALIGNED and consult 2-venue.md (direct `_venue/playbook-<venue>` reads = fallback when 2-venue.md is absent, or deep dives via its `[source: ...]` tags).
So: "paper" with claims done but no venue pinned -> run `venue` before pitch.
Re-targeting ("move to another journal") -> re-run `venue`; pitch re-couples (new [primary], new RQ framing); resource and claims stay unchanged (what a paper NEEDS to exist does not depend on where you send it).

Dispatch notes (only where non-obvious; everything else is `Skill("haipipe-paper-<target>")` or `Skill("haipipe-paper-lifecycle", args="<verb> ...")`):

```
enter     Path exists -> Skill("haipipe-paper-enter", args="<path>"). Path MISSING -> get-or-create:
          CONFIRM FIRST (creating a repo is outward-facing; never create off a typo). Then resolve the
          parent project (walk up, or ask). Project-* repo -> paper is REPO-BACKED: resolve --org
          (flag or ask, NEVER assume; the paper's owner may differ from the project's), follow the
          papers-inside recipe in project/haipipe-project/fn/repo-project.md, then
          Skill("haipipe-paper-lifecycle", args="folder <paper-path>"), double-bump (paper push ->
          project pointer -> workspace pointer), and continue straight into the console.
          Plain projects: folder + scaffold, then console.
probe     Operates on the flat cross-stage pool (1-probes/PPNN_<topic>.md; the README board is
          derived from it). Sub-modes are listed in the Verbs block above (raise · board · plan
          the campaign · run). It is the SAME operation at two scopes: this paper-level verb
          works the WHOLE pool (see/plan/drain every open question across all stages), while a
          stage's PROBE phase works only its own slice — the sections whose `serves:` names that
          stage — during that stage's DRAFT→PROBE→REVISE→CHECK turn. Both go through the one
          worker, haipipe-paper-probe, which runs the five-step loop MATCH-before-DISPATCH and is
          the ONLY thing that touches the bank; the umbrella and the stages never do. That worker
          follows the shared probe model (the constitution). Anatomy + campaign + model: fn/probes.md.
```

After dispatch, capture the specialist's structured tail (status / summary / artifacts / next) and present it.

Closing Block (end every reply)
--------------------------------

THE single source of truth for the closing block and the focus strip (absorbed wiki/01-focus-strip-markers 2026-07-03; every stage / enter skill inherits this section).
In a paper session, END every reply with ONE fenced `text` block: a titled top rule carrying `📄 paper · <active-stage> 🔥`, a two-line simplified tail, a plain bottom rule, then the TWO-LINE focus strip (stage + phase):

```text
── 📄 paper · seed 🔥 ─────────────────────────
status:  ok · seed             (status and active stage merged on one line; paper_root dropped)
next:    <single recommended command>
──────────────────────────────────────────────
stage:   seed 🔥  resource ✅  claims ✅  venue ✅  pitch ✅  narrative ✅  display ✅  →  section-edit 🚀  →  review ⬜
phase:   draft 🔥🚀  │  probe: cite ⬜  val --  disp --  │  revise ⬜  │  check ⬜
```

Markers: 🔥 active now (what this session works on) · 🚀 frontier (farthest the paper has ever reached) · ✅ done · ⬜ not started · `--` skipped.
Rules: EXACTLY one 🔥 and EXACTLY one 🚀 per line, never zero -- "reached" means entered, not completed, so a virgin paper working its first phase renders `draft 🔥🚀`, and any line showing 🔥 without a 🚀 somewhere is a rendering defect; they split only on loopback (the frontier slot keeps 🚀 while 🔥 moves back) and collapse to `🔥🚀` when they land on the same slot; the phase line always describes the 🔥 stage's DPRC phases; `cite`/`val`/`disp` are probe's sub-tracks (stages without them show a single `probe` slot).
Two markers because loopbacks are normal (redo seed while the frontier is section-edit): one marker cannot show both "where I am" and "how far the paper has gotten".

Render the stage line DETERMINISTICALLY with the helper (never hand-type it; it drifts): `sh "$CLAUDE_SKILL_DIR/stage-strip.sh" <paper-dir> [<session-stage>]` (the script lives IN this skill folder, next to this spec).
The phase line is rendered by the 🔥 stage's skill from its own DPRC progress.


Gate-aware: advancing `current_layer` requires an EXPLICIT approval action that the current stage is done (Stage Gate, `../1-lifecycle/ref/08-stage-gate.md`) -- by the human (copilot mode) or by a reviewer subagent standing in for the human (autopilot mode); once STATUS.md carries the gate ledger, ✅ means "approved", and the ledger records who approved (human or agent).


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

Paper work is demand-driven: a paragraph, claim, figure, or round todo may reveal that the next action is evidence work.
The enter/status path surfaces those needs before recommending more writing.
Need record schema: `../wiki/11-delivery-need.md`; paper/evidence boundary + `\needprobe{}`: `../wiki/12-evidence-routing.md`.

```
claim needs evidence / robustness / literature / a data artifact -> /haipipe-paper probe "<question>"  (a SECTION in 1-probes/; MATCH first, dispatch only what MATCH cannot close)
figure/table needs materialized output (not claim-gated)         -> /haipipe-task-for-display <need>
settled claim status (supported|refuted|inconclusive)            -> 0-lifecycle/1-claims/1-claims.md (the ONLY home of a claim's status; the probe section carries only its `a-consumer:`)
wording/section placement                                        -> the owning lifecycle stage skill
standalone utility (a HUMAN, not the paper: lit scan, data check) -> /haipipe-task qa | /haipipe-discovery qa (the bank's own door)
```

ALL evidence enters through a stage's PROBE phase; the paper never calls the bank directly.
Resolved evidence backfills into `1-claims`, `4-display`, sections, or round logs.
Evidence workers never own the paper story.

Structure Pointers
-------------------

Each area's internal contract lives with its owner; consult, never restate:

```
skill tree (0-enter / 1-lifecycle / 2-phase / 3-build-submit / 4-respond / 5-present / components / wiki)
                                   -> README.md (skill root) + ../wiki/06-paper-skill-structure.md
paper-folder layout                -> ../3-build-submit/_shared/paper-folder-anatomy.md (canonical tree, prefix semantics, maturity ladder)
lifecycle stages + venue coupling  -> ../1-lifecycle/ref/03-paper-lifecycle.md + ../1-lifecycle/ref/04-lifecycle-map.md
rounds                             -> ../wiki/07-paper-rounds.md
venue knowledge                    -> ../_venue/playbook-<venue> packs (venue is knowledge, not a pipeline)
```

Composing with Evidence Workers
--------------------------------

```
/haipipe-paper (router)
        ├─► /haipipe-paper-lifecycle    (seed -> resource -> claims -> [venue] -> pitch -> narrative -> display -> section-edit)
        ├─► /haipipe-paper-rebuttal     (any venue, post-review)
        │
        │   evidence path (a claim hits a gap):
        └─► 1-probes/PPNN_<topic>.md (one file per TOPIC, one SECTION per question)
                 └─► haipipe-paper-probe (the PROBE phase worker, run inside a stage's PROBE phase)
                          ② MATCH the bank's QA corpus ──► most sections close HERE (T2 REUSE)
                          ③ DISPATCH the `q-executor:` block, VERBATIM, only for what MATCH missed:
                               Agent(haipipe-task-orchestrator-agent)
                               Agent(haipipe-discovery-orchestrator-agent)   ← their clean context IS the wall
                          ④ POINT  target: ─► the answering QA file  tasks|discoveries/<discovery-group>/<discovery-folder>/QA/<n>-<slug>.md
                          ⑤ INTERPRET a-consumer: ─► the harvest lanes pay out

        a stage reaches the bank ONLY through its PROBE phase — no direct discover/task verb
```

