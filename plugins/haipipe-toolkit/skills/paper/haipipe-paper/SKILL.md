---
name: haipipe-paper
description: "THE one door for paper-lifecycle work: parse intent (venue + stage), resolve the stage contract from stages/index.yml, ensure the S page exists, and hand the page to haipipe-board-page. Each stage runs the ordered phases declared by its stage.md and stops only at its declared gates; evidence enters ONLY through PROBE, which turns the S page's Q-consumer questions into probe entries and runs them through clean agents. `enter`/`status` open the paper's first-class Board (get-or-create on a missing path). Trigger: paper, enter paper, paper status, venue, seed, resource, claims, pitch, narrative, display, section-edit, round, rebuttal, probe, evidence, 选刊, 写论文, 论文流程, /haipipe-paper."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.7.0"
  last_updated: "2026-08-06"
  summary: "Single door for the Board-first paper lifecycle, and the paper family's ONLY registered skill (thin-paper phase 3). S03/S04 are evidence pages (JL 260806): head route: key, one E<n> Content division per Q-executor conversation with #### consumers + #### answer digest, E0 incoming queue, hidden QA-probe records with capital slot headings. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper (the door)
================================

User-facing entry for the paper lifecycle, and since 2026-08-05 the ONLY paper router: the old enter/lifecycle/stage routers are retired to `../_old/` and their jobs are internal steps of this one skill.
**The paper family registers exactly ONE skill (this one); everything else is data**: stage contracts under `stages/` + the `SNN-*/` folders, craft files, `fn/` verb procedures, `scripts/` tooling, and `venue/` packs. Since 2026-08-06 (thin-paper phase 3) the former folder/conform, build (compile · diffpdf · project · to-overleaf · to-word), and round/rebuttal skills are `fn/` procedures and the `round` stage of this door; their folders live in `../_old/phase3-260806/`.
The paper lifecycle is a delivery owner: it owns this paper's angle, resources, claims, narrative, section map, displays, maturity, and dated work rounds.
Project-level evidence lives outside the paper in tasks and discoveries; when the paper hits a gap, record a delivery need (see "Delivery Need Routing" below) and route to the evidence worker.

Page logic is NOT restated here: once the stage's S page exists, this door hands it to `haipipe-board-page` (WORK ON to repair, RUN with a packet to drive it); the `board/page-phases/` contracts own DRAFT, PROBE, REVISE, and CHECK.
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
                                                haipipe-board-page WORK ON directly, phase verb passed through.
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
Phase driving is NOT this door's: with the page resolved, call `haipipe-board-page` (WORK ON to
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

### The lifecycle

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

### REVISE phase: no comment-first

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

### How paper talks to probe

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

### When to record a need

Only when the problem is EVIDENCE, not wording. A wording/structure problem loops back inside the paper lifecycle (claims / pitch / narrative / display / section-edit). A need leaves the paper for an evidence worker, and it travels the loop above: paper GAP -> a Q-consumer COLLECTED into the evidence page's E0 queue -> PROBE translates it into an E<n> division and MATCHes its QA-probe -> DISPATCH only what MATCH could not close -> the answering QA-bank file -> `#### A-executor` -> the A-consumer row under `#### consumers` -> the paper backfills its claim page. Do NOT route through a project-level narrative layer (there isn't one).

### Routes

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

### Need record and backfill

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

### Autonomous drain (the "keep going" loop)

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

### The `\needprobe{}` macro

When a claim lacks evidence, mark it in the `.tex` with a visible red caveat:

```latex
\newcommand{\needprobe}[1]{\textcolor{red}{\textbf{[NEED PROBE]} #1}}
```

Add this macro to the lifecycle preamble (or the paper's shared command file). Use it inline wherever the gap lives:

```latex
\needprobe{Is the intensive margin about patients already on opioids?}
```

The red flag renders in the compiled PDF so the gap is obvious to every coauthor. Remove it when the answer lands (the entry's `**target**` resolves and its `#### A-executor` is written) and the claim is backfilled with supported text.

### Handoff protocol

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

### The `probe` verb

```
/haipipe-paper probe <need-description>
```

opens one nested QA-probe in the right S03/S04 topic. The PROBE phase is what dispatches it — through `Agent(haipipe-probe-q-executor-agent)` to `Agent(haipipe-task-orchestrator-agent)` or `Agent(haipipe-discovery-orchestrator-agent)`, carrying the QA-probe's `#### Q-executor` block and nothing else. The paper stays a story layer; the executor does the work. Anatomy + campaign + the paper-side loop: `fn/probes.md`.

A HEAVY probe (reading a lot of code/logs, e.g. cohort construction from Stata do-files) is
dispatched with `run_in_background=true` so the paper session keeps doing paper work: mark the
beat `\needprobe{}`, raise the entry, fold the returned report into Methods when it lands.

### Construction as a first-class beat

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
        │                     driven via haipipe-board-page)
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
