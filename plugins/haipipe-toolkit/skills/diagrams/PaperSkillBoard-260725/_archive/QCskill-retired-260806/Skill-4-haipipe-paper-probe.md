# haipipe-paper-probe · v0.7.6
state: ⚫ RETIRED 260805 · split across board page-probe + probe/haipipe-probe, the door's probe/ tooling, and fn/probes.md
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

**Retired 260805 (thin-paper phase 2, QC6).** The PROBE worker split three ways. The wall and the five-step loop live on in `board/page-phases/haipipe-board-page-probe` plus the shared crossing `probe/haipipe-probe`. The family tooling moved into the door at `paper/haipipe-paper/probe/` (check-probe-cards.sh, check_topic_entries.py, topic-entry-contract.md, per-stage-dispatch.md). Its unique MATCH and dispatch mechanics merged into `paper/haipipe-paper/fn/probes.md`, and the worker folder retired to `paper/_old/workers/haipipe-paper-probe/`. The account below is the pre-fold record and stays as written.

## Opening
How does a paper-owned Q-consumer become durable, independently answerable evidence without allowing the writing session to invent or run that evidence?

This page covers the paper-side PROBE bridge.
It turns a question already anchored on an S page into an entry and interprets a landed QA artifact back into the paper, while `haipipe-probe` and the bank retain their own ownership.

## Diagram
<!-- haipipe:skill:tree:start 6e79c181dcc8bc4b paper/workers/haipipe-paper-probe -->

**What `haipipe-paper-probe` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-paper-probe/
  feedback/
    README.md                   4 ln  haipipe-paper-probe -- Feedback Inbox
  ref/
    per-stage-dispatch.md     160 ln  Per-stage dispatch reference (haipipe-paper-probe)
    topic-entry-contract.md    28 ln  Paper topic and probe-entry contract
  CHANGELOG.md                459 ln  haipipe-paper-probe — Changelog
  check-probe-cards.sh          3 ln
  check_topic_entries.py      162 ln  Verify the Paper S03/S04 nested topic-entry contract.
  SKILL.md                    235 ln  Skill: haipipe-paper-probe — the PROBE-phase worker for a paper
```

<!-- haipipe:skill:tree:end -->

```
direct topic page · ### Q-consumer register   paper-side consumer + stake
             │                                S03 discovery · S04 task
             ▼
① ORGANIZE  S03-literature/probes/L<n>-<topic>/S-Literature-<n>-<slug>.md
            S04-value/probes/V<n>-<topic>/S-Value-<n>-<slug>.md
② MATCH     route + bank verdict + target, rooted to a readable QA answer
③ DISPATCH  collector only, if depth(bank) <= authorized probe_depth
④ POINT     verify the target QA file and its state on disk
⑤ INTERPRET copy into #### a-executor → the topic register's interpretation
             │
             ▼
haipipe-probe / task / discovery     independently-owned QA artifact

The paper records what the fact means.  The executor records the fact.
```

## Content
<!-- haipipe:skill:body:start 6e79c181dcc8bc4b paper/workers/haipipe-paper-probe -->

**haipipe-paper-probe** · `0.7.6` · last shipped 2026-08-04

- folder   `paper/workers/haipipe-paper-probe/`
- tools    Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
- summary  Paper-specific PROBE worker layered on haipipe-board-page-probe and haipipe-probe, retaining Q-consumer/Q-executor and A-executor/A-consumer.

### SKILL.md



Skill: haipipe-paper-probe — the PROBE-phase worker for a paper
==============================================================

Called by paper stage skills whenever DRAFT, REVISE, or CHECK routes a consequential unknown to PROBE.
The originating phase raised or identified the Q-consumer and stopped there. THIS worker owns everything probe-shaped: ①ORGANIZE each Q-consumer into an ENTRY, ②MATCH it against the bank (read-only grep), ③DISPATCH only what the ceiling allows, ④POINT, ⑤INTERPRET.

**LOAD THE PAGE LAYERS FIRST:** `../../../board/page-types/haipipe-board-page-for-stage/SKILL.md`, then `../../../board/page-phases/haipipe-board-page-probe/SKILL.md`, then `../../../probe/haipipe-probe/SKILL.md`.
The nested S03/S04 artifact is the paper's Probe Page.
Its existing code and headings may say entry, but that label is not another Page Type or phase.

> **Where the bracket grammar was ruled.** `[Q-X-n]` is the paper's ONE join key
> from a sentence to the question that owes it, ruled on `QC2@paper` and shared by
> every marker type (`QC1@paper` citation, `QC3@paper` table, `QC4@paper` figure).
> The Q-consumer register is the canonical page-facing map, so the id written
> there and the id bracketed in prose are the same string or the sentence reports
> as `unowned`. An entry preserves that id only in `#### consumer trace`.

⭐ THE MODEL IS NOT THIS FILE'S — it is owned by `../../../probe/haipipe-probe/SKILL.md`.
Read it for the probe-file anatomy, the QA state-line contract, the cost ladder, the two LAWS, the derived states, and the checker's FAIL codes.
This file is ONLY how a paper runs the loop, plus the paper-side deltas that file does not cover.

Not user-facing: users invoke stage skills; a stage calls `Skill("haipipe-paper-probe", args="from-buffer <paper_root> [topic-id]")`.
Which stage routes where, seed/claims/resource specifics, and section-edit logic: `ref/per-stage-dispatch.md`.

The paper-side deltas:
- `paper_root` vocabulary, and the paper's OWN registries (the T1 whitelist).
- the RESOURCE stage intake and write-back (paper only).
- HARVEST, inline in ⑤.


Rules (follow these — the model is probe's)
======================================================

The PROBE-phase rules live in `../../../probe/haipipe-probe/SKILL.md` → **Phase rules · PROBE phase** (+ **The QA file**, **The two LAWS**). Follow those; on conflict, that file wins. Paper-specific additions:
- Dispatch goes through the collector agent (`haipipe-probe-q-executor-agent`), NEVER an orchestrator called inline by this worker — results would die with the reply.
- HARVEST IS INLINE, and `#### a-executor` is its only answer sink. The entry page is the consumer-side source of truth for the returned answer; the parent topic's Q-consumer register remains the source of truth for paper stake and interpretation. Phase history lives in the owning S page's `## Log`.
- RESOURCE write-back: the landed reading goes into the owning `0-lifecycle/S02-work/S-Work-*.md` resource page as the Q's `A:` (existence AND fitness AND what it KILLS).
- A claim's STATUS goes in the owning `0-lifecycle/S02-work/S-Work-*.md` claims page, written by the AUTHOR, NEVER in the probe file.
- No bibtex / no `.bib` edits; no ad-hoc plots; no markdown tables in any probe document.

The loop below is the HOW-TO for these rules.


The loop, paper-side — this worker owns ① through ⑤
=====================================================

Each step ends with a PROOF this worker MUST show in its reply; an absent proof means the step did not happen.
STEP 0 — re-invoke this skill fresh every run, even when its text is already in context (a probe once ran a 3-hour-old contract).

①ORGANIZE + ②MATCH happen HERE. Read the direct topic page's `### Q-consumer register`, and for each question author one nested entry: `#### q-executor` (stake stripped, then frozen), `#### consumer trace` (audit copy of the original wording), `#### bank binding` (route, bank verdict rooted to a specific QA answer by reading it, and target), and `#### a-executor`. DRAFT writes the Q-consumer register but never opens an entry page.
This worker delegates ③DISPATCH + ④POINT to the isolated collector, then owns ⑤INTERPRET (HARVEST into the paper's OWN registries).


① + ② — THIS WORKER AUTHORS THEM
---------------------------------

The direct topic page's `### Q-consumer register` is the input. For each Q-consumer, find or open one entry page below its route topic: `<paper_root>/0-lifecycle/S03-literature/probes/L<n>-<topic>/S-Literature-<n>-<slug>.md` for discovery, or `<paper_root>/0-lifecycle/S04-value/probes/V<n>-<topic>/S-Value-<n>-<slug>.md` for task work. ONE entry page owns ONE q-executor. The route decides the stage because Literature receives outside-project discovery and Value receives project-task evidence. The retired `1-probes/PPNN_<topic>/QXn_<slug>.md` layout is preserved only under `<paper_root>/0-lifecycle/_archive/1-probes/`. DRAFT wrote no entry page; if one exists from a previous PROBE run, read it and do not re-author it.
- Resolve `project_root`: walk UP from `paper_root` to the first ancestor containing `discoveries/`.
  Do NOT use `git rev-parse` — a repo-backed paper is its own git repo. (The checker resolves the same way.)
- Route on the TARGET, not on the verdict. They answer different questions: `bank` says what the
  bank would have to DO, `target` says whether the readable answer EXISTS yet.

```text
  target: <an existing QA path>   → ④/⑤ : verify the state line, then harvest
  target: NEW <path>              → ③   : dispatch only for bank: run | code | new
```

  `bank: reuse` requires a specific existing QA file as `target` and skips
  dispatch. If raw results exist but no readable QA file answers the question,
  the bank still owes a digest-only execution: classify it `bank: run`, point
  `target` at `NEW <path>`, and apply the normal depth-1 ceiling. LAW 1 forbids
  the consumer from writing that digest itself.
- T1 LOCAL is this worker's, at ②: root the question against the paper's own registries and set target plus `state: answered-local`, then write the entry's `#### a-executor`. The closed whitelist: entries already `read` or `answered-local` beneath `S03-literature/probes/` or `S04-value/probes/` · `displays/` units · the `.bib` · the stage's S page `## Log`.
  Fully answered there → write the `#### a-executor`, set `answered-local`, do NOT dispatch. Adopt the POINTER, never the verdict (a reused value re-verifies against its ORIGINAL source at PLACE).
- DISPLAY-shaped needs are REROUTED, not collected: a question asking for a display unit that does not exist becomes a DR row in `0-lifecycle/S05-display/_DISPLAY_REQUEST.md`; close the entry `answered-local` with the `#### a-executor` "rerouted to display stage: DRNN".
- RESOURCE (paper only): DRAFT wrote the `Q<n>` questions on
  `S-Work-0-resources.md`; this worker opens one ENTRY per question, writes the
  `Q<n> (N<n>) -> PP<NN>` backlink, and carries `blocks: N<n>` in the bank
  binding. Dispatch is governed by `--depth`, not by a DRAFT gate. Step ⑤ writes
  the `A:` back to the same Resource S page.

③ — THE CEILING GATE, run BEFORE any dispatch
----------------------------------------------

⛔ NO ENTRY IS DISPATCHED WITHOUT PASSING THIS. Read `probe_depth:` from the stage's contract
(`../../S<NN>-<group>/<key>/stage.md`, per the roster `../../haipipe-paper-stage/stages/index.yml`), or take the value the
invocation passed as `probe --depth N`, whichever is HIGHER — the invocation may raise the
contract's default, never lower it silently.

Map each entry's `bank` verdict onto the bank's own depth ladder, then compare:

```text
bank: reuse  = depth 0   results already answer it       free, nothing runs
bank: run    = depth 1   old script, new config          costs
bank: code   = depth 2   must write new code first       costs
bank: new    = depth 3   open a new task-folder          costs most

    depth(bank) <= probe_depth   →  ③ DISPATCH it
    depth(bank) >  probe_depth   →  DEFER it, and STOP for that entry
```

DEFERRING IS A CORRECT OUTCOME, NOT A FAILURE. Write it as a DECLARATION on the entry, never as
silence:

```text
**state**: deferred
**deferred**: depth-2 · needs a new script to join review text to the claims panel; nobody has
              authorized that spend. Raise with `probe --depth 2` to release it.
```

A `deferred` entry with no `**deferred**: depth-<n>` line is a bare `planned` entry in a costume,
and `check-probe-cards.sh` FAILs it as `deferred-undeclared`.

⚠️ NEVER raise the ceiling on your own initiative. `--depth` is the human act that authorizes
spend. Report in the `[PROBE]` entry in the owning S page's `## Log`
which ceiling was in force, how many entries dispatched, and how many deferred at what depth.

PROOF 1: `project_root=<path>` + `ls <project_root>/discoveries/` + `ls <paper_root>/0-lifecycle/S03-literature/ <paper_root>/0-lifecycle/S04-value/`, the `probe_depth` in force, and per entry its bank verdict, resolved depth, target, and dispatch/defer decision.


③ DISPATCH — hand the NEW entries to the collector agent
--------------------------------------------------------

For each STILL-COLLECTING entry (`target: NEW` — `bank: new | run | code` — not resolved by T1 LOCAL), hand the SET to the collector agent, tagging each with the PROBE-authored `route` (task|discovery — AUTHORITATIVE, not a hint):

  ```text
  Agent(haipipe-probe-q-executor-agent, prompt="
    project_root: <from ①>
    entry_pages:  <the nested entry pages touched this run>
    dispatch:     <entry ids with target: NEW>, each with its route: task|discovery
  ")
  ```

The agent runs in ITS OWN clean context: it sends each `q-executor` VERBATIM to `Agent(haipipe-task-orchestrator-agent)` / `Agent(haipipe-discovery-orchestrator-agent)` (`run_in_background` for fresh work; omit the leaf for fresh — the orchestrator picks the folder and returns the path), and returns `{ entry → target: QA-path | in-flight | failed }`, having written each `target`.
Under model A the agent does NOT re-run ②MATCH — this worker rooted each question at ② just above; the agent dispatches (the executor orchestrator's own QA gate still dedups against an existing answer). It NEVER reads the paper's registries, consumer traces, or paper stake — its clean context IS the wall; and it never authors a fresh folder (LAW 1).
The stage NEVER calls `haipipe-task-orchestrator-agent` / `haipipe-discovery-orchestrator-agent` ITSELF — the collector owns dispatch; a stage that dispatches inline lands results nowhere reviewable.

DEFERRED / ASYNC is the agent's too: an entry it cannot land synchronously comes back `in-flight` and stays `commissioned`; the NEXT PROBE run re-hands it. This worker writes NOTHING under `tasks/` or `discoveries/`, ever — no stub, no mailbox.

PROOF 3: the agent's per-entry dispatch / in-flight lines (from its return); NO `Agent(haipipe-task-orchestrator-agent)` call appears in THIS worker's own transcript.


④ POINT — the agent wrote `target`; the stage VERIFIES it on disk
-----------------------------------------------------------------

The agent already wrote each resolved entry's `target` (the FILE, never the folder). Before harvesting, VERIFY — do not trust the return blind (the state is the TARGET's state line, not the target's existence — open the file):
- `ls <project_root>/<target>` resolves, and `grep '^- state:' <target>` reads `answered` → ⑤.
- `working` → stays `commissioned`, report IN PROGRESS since `<started>` (dead past `QA_WORKING_TTL_HOURS` → re-hand to the agent next run).
- no QA-file path returned → `state: failed`, phase not green.
- a `commissioned` target that has since gone `answered` is a HARD FAIL (`commissioned-target-answered`) — harvest it now, do not wait for the eta.

PROOF 4: per entry the `target` line, the `ls` that resolves it, and `grep '^- state:' <target>`.

════════ COLLECTION (①–④) ends here — the answer is banked.
HARVEST (⑤) begins. ════════

⑤ INTERPRET — the a-executor, the topic register, the claim status, and HARVEST (the paper's own, not probe's)
--------------------------------------------------------------------------------------------------------------------

- Copy the QA answer into `#### a-executor` (the entry's answer source of truth), then update the parent topic's Q-consumer register with its paper-facing interpretation and the entry path. Translate the general answer up into the paper's words without overwriting the consumer stake.
  ONLY against an `answered`, non-superseded target (probe).
- The AUTHOR writes the claim status (`supported | refuted | inconclusive` + confidence + claim_type) into its owning `0-lifecycle/S02-work/S-Work-*.md` claims page, never in the probe file.
  A probe communicates evidence; the stage interprets it, and CHECK reviews the paper judgment. Keep the `claim_type` overclaim check.
- RESOURCE WRITE-BACK (an entry serving a resource `Q<n>`): write the landed reading BACK into `S-Work-0-resources.md` as the Q's `A:` line — existence AND fitness AND what it KILLS ("probably fine" is a DEFECT, not an answer).
  A BUILD-lane entry writes `A: COMMISSIONED · owner <who> · eta YYYY-MM-DD · blocks N<n> · cross-project: <path|none-found>` at booking; the async path overwrites it on landing.
  Both receipts: the entry is the probe-layer one; the Q's `A:` is what the human reads at CHECK.
- HARVEST — inline, in this worker, into the SAME `#### a-executor`. Whatever reusable material the answer carries rides along with the answer:
  - **source anchors** (literature): transcribe each into the `#### a-executor` in the QA file's own words, with its identifiers. NEVER generate bibtex; NEVER touch `.bib`. Carry provenance at TWO levels and never flatten them — `VERIFIED-by-discovery` is arXiv-level, NOT bibtex-level, so a source stays 🔍 until a human confirms it. An entry carrying only identity fields (title/authors/year) and no statement of WHAT the source found is a DEFECTIVE harvest: the reader must be able to see what each source contributes without opening the discovery folder.
  - **values** (numbers): transcribe the number AND the named source path it came from. FABRICATION GUARD: the literal value string must grep in its named source file — `grep -F '<value>' <source>` — and a value with no source hit is REJECTED. The parquet/script decides, never the prose.
  - **display units**: name the landed `displays/<unit>/` path. LINK ONLY UNITS THAT EXIST (or whose DR row is `done` with the unit path filled) — a `requested`/`accepted` DR row stays 📨 pending and is flagged for CHECK; never pre-place a `\ref` for a display that does not exist yet, or the tex compiles to `??`.
  Placing any of this INTO manuscript prose is REVISE's job (`haipipe-paper-revise-place`), not this worker's. This worker transcribes; it does not edit the manuscript.

PROOF 5: per entry the `#### a-executor` copy plus the parent Q-consumer register line, the claim-ledger diff (if it serves a claim), the `grep -A2 'Q<n>' S-Work-0-resources.md` for a resource write-back, and — for any harvested value — the `grep -F` output proving it appears in its named source.


VERIFY — the checker (the stage CHECK gate re-runs the same script)
------------------------------------------------------------------

```
sh <this-skill-dir>/check-probe-cards.sh <paper_root> [<project_root>] [--stage <key>]
```

`--stage resource` also runs the resource pass over
`S-Work-0-resources.md`: every `Q<n>` must carry an `A:`, a `-> PP<NN>`
backlink, or a DECLINED line in that page's `## Log`; an open question with no
entry fails as vacuous green.
The FAIL codes are probe's.
Never report a green PROBE over a FAIL.

PROOF 6: the checker output, pasted.


Hard boundaries (paper-specific; the wall + ONE-WRITER are probe's)
=============================================================================

- NEVER generate bibtex or touch `.bib`.
- NEVER fabricate numbers; NEVER create ad-hoc plots inline.
- NEVER edit manuscript prose. This worker transcribes into `#### a-executor`; placing anything into the manuscript is REVISE's (`haipipe-paper-revise-place`).
- NO markdown tables in probe files or any probe document — bullet lines and `###` subsections only.
- NO inline search in the PROBE phase — the dispatch is the door.
  (DRAFT may WebSearch to orient; the difference is DURABILITY, not the search verb.)
- A stage skill that calls `Agent(haipipe-task-orchestrator-agent)` or an evidence agent ITSELF bypasses this contract — results land nowhere reviewable and die with the reply.


Return contract
===============

```
status:    ok | blocked
stage:     <stage-name>
probes:    <n> nested entries · T0/T1 <n> · T2 <n> · T3/T4 <n> dispatched
harvest:   <n> entries whose a-executor carries sources/values/display paths
next:      <suggested command>
```


Reference
=========

```
../../../probe/haipipe-probe/SKILL.md   probe — the model. Read it.
ref/per-stage-dispatch.md                  per-stage routing · seed/claims/resource specifics
check-probe-cards.sh                       the VERIFY / stage-gate verifier (family-local)
ref/topic-entry-contract.md                the paper-specific S03/S04 entry shape
```

### The other files

5 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
check-probe-cards.sh              3 ln
check_topic_entries.py          162 ln  Verify the Paper S03/S04 nested topic-entry contract.
feedback/README.md                4 ln  haipipe-paper-probe -- Feedback Inbox
ref/per-stage-dispatch.md       160 ln  Per-stage dispatch reference (haipipe-paper-probe)
ref/topic-entry-contract.md      28 ln  Paper topic and probe-entry contract
```

<!-- haipipe:skill:body:end -->

## Aims
- [x] 🧭 Preserve the five-step bridge
      PROBE, not DRAFT, creates and maintains the entry.  It organizes the
      consumer question, matches before spending, dispatches through the
      collector, points to a QA file, and harvests an answer back.
- [x] 🧱 Preserve the wall between story and evidence
      This worker never runs a task or discovery orchestrator inline, writes no
      task/discovery folder, edits no manuscript prose, and creates no BibTeX.
      Its durable proof is the entry's `a-executor` copy plus the named QA path.
- [x] 💸 Preserve human spend authorization
      A bank verdict maps to a depth.  Only `depth(bank) <= probe_depth` may
      dispatch; an over-ceiling question becomes an explicit deferred entry,
      not a silently forgotten question.
- [x] ↩️ Preserve the paper-side return locations
      Resource answers write back to the Resource S page, claim status belongs
      in the claim ledger, and prose placement belongs to REVISE.  A missing
      display unit is rerouted to a Display Request row rather than collected.
- [ ] 🧪 Test reuse, dispatch, deferral, and harvest in one campaign
      A fresh-agent run should show one proof for each step and prove that an
      answered target is harvested rather than left commissioned.

## States
The paper-to-bank handoff is now visible as a path-bound five-step loop, with separate ownership for the question, the fact, and the paper's interpretation.
The remaining acceptance test is a mixed-depth campaign that exercises all four outcomes: local/reuse, dispatch, defer, and harvest.

## Log
- 260806 0130 · [REVISE-CC] retirement recorded: haipipe-board-page-probe + probe/haipipe-probe; tooling in paper/haipipe-paper/probe/; MATCH/dispatch mechanics in paper/haipipe-paper/fn/probes.md
260727 · Audited against `board.md`'s decision-only rule, which says `state:` is about the DECISION and that implementation does not gate this board. Every open item here is implementation or a test, not an undecided question, so the page was reporting itself as open because code was missing. Flipped with no ruling made.
260727 1450 · Created the paper-side PROBE skill page from `paper/phase/1-probe/haipipe-paper-probe/`.
The authored diagram keeps the five-step loop and the evidence/story ownership wall in one place.

<!-- haipipe:skill:log:start 6e79c181dcc8bc4b paper/workers/haipipe-paper-probe -->

Converted from the skill's own `CHANGELOG.md`: 56 releases.

260804 · `0.7.6` · Page PROBE layering
      - Loads the Stage Page Type, generic `haipipe-board-page-probe`, and shared `haipipe-probe` before paper deltas.
      - Names the persisted S03/S04 artifact a Probe Page and retains `entry` only for the existing checker schema.
      - Allows DRAFT, REVISE, or CHECK to route a consequential unknown into PROBE.
260727 · `0.7.5` · the section-edit gate stops being vacuously green
      - **`stage_stem()` maps `section-edit -> Sec`.** It previously derived the stem by stripping a
        trailing `s`, producing `section-edit`, and grepped `q-section-edit` — which matched NO id
        under either the old or the new scheme. Every probe entry genuinely serving this stage
        therefore failed the `--stage` filter and the gate reported a permanent green over
        unasserted work. `Sec` matches every per-unit id and collides with no other stage
        (`q-seed` does not contain `q-sec`).
      - **The checker's own id regex now accepts a per-unit token**, widened to `[A-Za-z0-9]+` at
        all 8 sites. Left letters-only it read every renamed bracket as absent and reported ten
        false `cite-unowned` / `value-unowned` defects on pages whose brackets were in the prose.
      - Effect on the MISQ paper: the gate now asserts 12 probe entries and 16 stage pages, and
        surfaces work nothing could previously see — 5 `PP03` entries whose QA files exist but were
        never harvested into `### a-executor`, and 2 `PP05` answers that landed in the bank
        unread. One real defect remains, `S-Main-5`'s 4 `\cite{TOADD}` with no bracket at all.
260726 · `0.7.4` · read questions from Board Items
      - Paper PROBE now reads recognizable `Q-<Stage>-<n>` checklist records from
        the S page's `## Items to Finish`, matching Board's first-class S-page form.
      - The review-only q-consumer copy may preserve original stake; only the
        q-executor crosses to the collector.
      - The checker now enforces terminal `concern` mechanically: exactly
        `route: none`, no bank/target field, an empty a-executor, and a real
        q-executor. It rejects stake on bank-binding or a-executor surfaces and
        validates normal route, bank, and state vocabularies.
      - Deferred declarations are read through their paper-root-qualified entry path;
        the checker no longer greps a nonexistent CWD-relative `1-probes/...` path and
        falsely reports a declared deferral as undeclared.
260726 · `0.7.3` · reuse means an existing QA answer
      - Removed the contradictory `bank: reuse` plus `target: NEW` path.
      - `reuse` now always points to a specific readable QA file and skips dispatch.
        Existing raw results without a QA digest are `run` and pass through the
        normal depth-1 authorization ceiling.
      - Removed compatibility globs for `1-probe-plans/` and lifecycle `_PROBE/`
        sidecars. The checker now recognizes only the current `1-probes/PP*/*.md`
        anatomy.
260726 · `0.7.2` · collector topology in every live reference
      - Updated the per-stage dispatch map to route a set of owed entries through
        `haipipe-probe-q-executor-agent`; only that collector calls task/discovery.
      - Replaced the stale “DRAFT-time MATCH” wording with PROBE-time MATCH.
      - Clarified the PASS 4 message so manuscript-placeholder ownership cannot be
        mistaken for a pass on still-open Q-consumers.
260726 · `0.7.1` · full-loop ownership and S-page history
      - PROBE owns ORGANIZE, MATCH, DISPATCH, POINT, and INTERPRET.
      - Resource entries are opened from `S-Work-0-resources.md`; `--depth` governs
        spend without a DRAFT gate.
      - Phase history moved from `_LOG` into the owning S page.
260726 · `0.7.0` · T1 LOCAL whitelist and DR unit paths
      Aligned with the paper-folder layout ruled 2026-07-26 on the design board (`skills/diagrams/01-haipipe-paper-260725`, face QA6): `0-sections/` to `sections/`, `0-displays/` to `displays/` (one folder per unit, the only home of an asset, no top-level `figures/`), `1-compile.sh` to `2-src/compile.sh`, and `STATUS.md` retired. Two live bindings: the T1 LOCAL whitelist (what a probe worker may read without crossing the wall) named `0-displays/` and `_LOG_<stage>.md`; both moved, the latter into the stage's S page `## Log`. And the display-link rule named `0-displays/<unit>/`.
260724 · `0.6.1`
      Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 6.1.0; older entries below keep their original numbers).
260719 · `6.1.0` · check-probe-cards.sh PASS 4: `--stage section-edit` was a VACUOUS GREEN
      ### Fixed
      PASS 4's `--stage` gate derived a doc's stage from its BASENAME alone. That works for every
      top-level stage (`1a-resource` -> `resource`), but a section doc lives at
      `0-lifecycle/5-section-edit/<section>/<section>.md` and is named for the SECTION, never for its
      owning stage — so `--stage section-edit` matched NO doc, printed NOTHING, and exited 0.
      Not a missed detection: a gate reporting success over work it never looked at. Measured on
      `Paper-Personality2Opioid-MISQ2026` — `--stage section-edit` exited 0 while 19 unowned
      placeholders sat in four section docs (4-llmtrait 3 · 5-empirical 4 · 6-results 10 ·
      7-discussion 2), every one of them invisible to the only gate that owns them. PASS 4 was added
      (D9) precisely to make those holes assert; the stage filter silenced it on the stage that
      accumulates the most of them.
      A doc now carries TWO stage names and either may match: the BASENAME (keeps per-section runs
      like `--stage results` working) and the PATH OWNER (`*/0-lifecycle/5-section-edit/*/` ->
      `section-edit`). Verified on all three scopes: section-edit 19 visible, results 1 doc, seed
      unchanged.
260719 · `6.0.1` · vocabulary: `probe`, not "the constitution"; the display reroute a-consumer is sited in the stage doc
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
      ### Changed (ruling A) — SKILL.md, 11 sites
      The frontmatter `description` and `summary`, the ⭐ model banner, the Rules header, the "CONSTITUTION v9.5.0 PHASE SPLIT" heading (now "PROBE v9.5.0 PHASE SPLIT"), the collection/harvest split sentence, the ⑤ INTERPRET heading, the `answered` target note, the FAIL-codes line, the Hard-boundaries heading, and the Reference block ("THE CONSTITUTION — the model. Read it." -> "probe — the model. Read it."). The three "not the constitution's" / "the constitution says nothing about it" phrasings now name `probe`.
      ### Changed (ruling A) — check-probe-cards.sh, 2 comment sites
      The QA-file state-line rationale comment ("the constitution, \"The QA file\" section" -> "probe/haipipe-probe/SKILL.md, \"The QA file\" section") and the `stale-old-format` rule comment ("constitution v9.5.0+" -> "probe v9.5.0+"). Comments only; no rule, regex, or FAIL code changed, and `bash -n` still passes.
      ### Changed (ruling B) — ref/per-stage-dispatch.md, the display row
      "the ENTRY closes `answered-local` with the a-consumer `rerouted to display stage: DRNN`" -> "the ENTRY closes `answered-local`, with each Q-consumer's a-consumer in its stage doc reading `rerouted to display stage: DRNN`." The concept is live but it was sited on the ENTRY; the a-consumer lives in the stage doc.
      ### Unchanged (verified LIVE, ruling B)
      The other 6 `a-consumer` sites (SKILL.md 3, ref/per-stage-dispatch.md 3) already name the stage doc explicitly — including `ref/per-stage-dispatch.md`'s "The **a-consumer** (in 0-seed.md)".
260719 · `6.0.0` · BREAKING: harvest lanes RETIRED; `### a-executor` is the sole sink; the three lane sub-workers fold in
      From the `paper/2-phase` skillset review (118 findings, 5 parallel auditors, 22/22 spot-checks passed). JL rulings D1/D3/D4, verbatim:
      ### Changed (JL: "do A.") — D1, the harvest sink
      `### a-executor` is ratified as the ONLY harvest sink. This was BROKEN ON DISK before the refactor, not by it: `ref/per-stage-dispatch.md:34` said the anchors stay in `### a-executor` while `SKILL.md:116` and `ref/harvest-acceptance.md:60,91` still wrote `_CITATION_{stage}.md`. Observable symptom: `ref/per-stage-dispatch.md:174-183` rendered `cite ⬜ / val ⬜ / disp ⬜` for every stage forever, because the files those forms test for can never exist again.
      ### Changed (JL: "A. the principle is everything now in the Questions of 1-probes and the stages's Q-consumer.") — D4, the lanes
      The `**values**:` / `**sources**:` / `**displays**:` lane lines and their `harvest: OWED` debt tokens are RETIRED, and `ref/harvest-acceptance.md` is DELETED. The mechanism had no destination left: its first instruction (`harvest-acceptance.md:11` — write `harvest: OWED` FIRST) triggers checker rule 7 (`harvest: OWED -> FAIL`), and the only legal exit was a sub-worker writing a sidecar retired on 2026-07-19. Following it as written reddened the gate with no way to clear it — which happened live in this session on `Paper-Personality2Opioid/1-probes/PP01`.
      SALVAGED, not dropped: the fabrication guard from `harvest-acceptance.md:30-32` (`grep -F '<value>' <source>`; a value with no hit in its named source is REJECTED) is now inline in ⑤ INTERPRET. It was the only mechanical anti-fabrication tooth in the bucket and losing it inside a cleanup would have been a real regression.
      ### Changed (JL: "A.") — D3, the three ⑤ residues
      `haipipe-paper-probe-citation` / `-values` / `-display` are dissolved; their genuine ⑤ INTERPRET content folds into this worker. My premise to the auditors ("none of the five phases is PROBE work") was CONFIRMED for the numbered phases and REFUTED for the skills — each hid ⑤ work where the phase numbering did not reach: citation's `## Harvest mode` (a sixth section, 85 lines, self-describing as "Called by haipipe-paper-probe at ⑤ INTERPRET"), values' Phase-3 PRECONDITION (17 lines, the QA state-line gate), display's Phase-3 LINK body (12 lines, tex links, enforced by checker rule 7). ⑤ INTERPRET now carries the surviving rules for all three payload types: source anchors (two-level provenance, never flattened; `VERIFIED-by-discovery` is arXiv-level not bibtex-level; an identity-fields-only entry is a DEFECTIVE harvest), values (the fabrication guard), and display units (LINK ONLY UNITS THAT EXIST — never pre-place a `\ref` for a pending DR row, or the tex compiles to `??`).
      The values state-line gate did NOT need porting: it existed to guard the lane skill's published DIRECT invocation form, which disappears with the skill; this worker's ④ POINT already opens the target and reads its `state:` line.
      ### Changed — the `mode: full` conditional (2 of 20 paper sites; the rest deferred per JL D5 "Leave it")
      `SKILL.md:38` and `:111` gated on `mode: full` a rule that is unconditional — the claim status lives in `1b-claims.md` in every mode. Gating an always-true rule implied `light` permitted the opposite. Restated unconditionally. This is a correctness fix that holds whether or not `mode` itself survives; the remaining 18 paper sites + 23 application sites + the 2 constitution declarations are untouched, pending the sequenced retirement (constitution → paper → application).
      Also: T1 LOCAL reassigned to DRAFT (it was claimed by both phases — `0-draft/haipipe-paper-draft/SKILL.md:35` and this file's `:62`); this worker now only writes the `### a-executor` of an `answered-local` entry. Hard boundaries gain "NEVER edit manuscript prose" (placement is `haipipe-paper-revise-place`'s). Return contract's `lanes:` line replaced by `harvest:`.
260719 · `5.3.1` · ref/per-stage-dispatch.md: seed's `_CITATION_0-seed.md` sidecar retired (satellite of haipipe-paper-seed 4.4.0)
      Satellite fix for the JL ruling recorded in `haipipe-paper-seed` 4.4.0 ("we should delete it. do not use it"). `ref/per-stage-dispatch.md` carried the retired sidecar in TWO places a seed-only edit would have missed — the per-stage table's **seed** row (line 34) and the seed-specifics paragraph (line 80). Both now route seed's returned sources onto the ENTRY's own `**sources**: harvest: OWED` lane and state that seed keeps no `_CITATION_` sidecar. Doc-only; no worker behavior changed. This is the 2026-07-10 lesson applied on purpose: after a ruling, sweep the satellites — a grep for the retired filename, not just an edit to the owning skill.
260719 · `5.3.0` · synced to constitution v9.5.0 (QX-entry probe format: serves→### q-consumer, match→bank, a-consumer→### a-executor, ## Q→## QX, dropped ## Why) + stripped ruling archaeology
      Reconciled the probe-file anatomy to the constitution's new Q-executor-entry format (`../../../../probe/haipipe-probe/SKILL.md` v9.5.0). Every probe-file reference updated: a probe ENTRY heading `## Q<n>` → `## QX<n>` (topic-local q-executor id); `- serves:` → a `### q-consumer` bullet; `- route:` / `- match:` / `- target:` / `- state:` → the four `**field**:` lines under `### bank binding` (`match` verdicts EXISTS/NONE → `bank` = reuse | run | code | new); `- q-executor:` → `### q-executor`; the probe-file `- a-consumer:` (the copied answer) → `### a-executor`; `## Why` DROPPED (the stake stays in the stage-doc Q-consumer). "section" → "entry" throughout where it means a probe-file entry. ⑤ INTERPRET now names both writes: the probe-file `### a-executor` copy AND the stage-doc a-consumer (station ②). Harvest-lane fields moved under `### bank binding` (`**values**:` / `**sources**:` / `**displays**:`). Preserved: model A (route/bank AUTHORITATIVE, this worker runs ③④⑤ and does NOT re-match), the QA state-line contract, the two LAWS, the harvest lanes, the RESOURCE intake + write-back, PROOF-per-step. Stripped ruling-archaeology citations (`(JL)`, `(JL 2026-07-10)`, version tags) from the prose; changelog history untouched.
260719 · `5.2.0` · RULES block (points at haipipe-probe's PROBE phase rules + paper deltas)
      New "Rules (follow these)" section after the intro: a short followable checklist that POINTS at the constitution's **Phase rules · PROBE phase** (+ **The QA file**, **The two LAWS**), then lists ONLY the paper deltas (collector-agent dispatch, harvest lanes + mechanical acceptance, RESOURCE write-back, claim status in 1b-claims, no bibtex/plots/tables). The loop below remains the HOW-TO. Points, not restates. Follows constitution v9.4.0 (Phase rules).
260719 · `5.1.0` · ①② MOVE TO DRAFT: this worker now runs ③④⑤ only (constitution v9.2.0, model A)
      Follows the constitution's v9.2.0 phase split (`../../../../probe/haipipe-probe/SKILL.md`): the DRAFT phase now authors the whole probe plan — each SECTION's `q-executor:`, `route:`, `match:` (rooted to a SPECIFIC bank folder), and `target:` — so ① ORGANIZE + ② MATCH happen at DRAFT, reviewed at the one DRAFT gate. This worker no longer organizes or matches; it EXECUTES the plan: ③ DISPATCH the `target: NEW` sections, ④ POINT, ⑤ INTERPRET/harvest.
      JL ruled model **A** (2026-07-19): the DRAFT `route:`/`match:` are AUTHORITATIVE — the collector agent DISPATCHES and does NOT re-match (the executor orchestrator's own QA-gate still dedups against an existing answer). The `②` section became the `① + ② — DONE AT DRAFT` precondition (read the plan, resolve project_root, run T1 LOCAL inline, route by `match:` EXISTS→harvest / NONE→dispatch). PROOF 2 retired (this worker has no step ②; PROOF N now maps 1:1 to step N). RESOURCE intake reframed: the resource stage's DRAFT opens the `serves: resource` sections + writes the `-> PP<NN>` backlink; this worker only opens missing sections on legacy-transition first touch.
      ⚠️ STILL OWED (coordinated, cross-family): the SHARED collector agent `haipipe-probe-q-executor-agent` still describes running ②MATCH — under model A it should DISPATCH only. That agent is shared with the application family; its update belongs in a joint pass. Until then it may do a harmless confirming match (leans B). Also `ref/per-stage-dispatch.md` may reference the old ① authoring.
260714 · `4.2.0` · R19 hardening (consumer side)
      Mirrors constitution `haipipe-probe` 8.3.0; IDENTICAL to `haipipe-application-probe` 4.3.0.
      - **② MATCH: R14 is SCOPED to `state: answered`.** A `working` file's `## Answer` is EMPTY BY CONSTRUCTION, so it can never pass R14's literally-answers test — and R14's remedy is DISPATCH. Read as written, the second consumer re-dispatches the run the first is still executing. A `working` file is now matched on its `# Q —` LINE: same question ⇒ HIT-IN-FLIGHT ⇒ commission + point, NO dispatch.
      - **② MATCH: `owner:` and `eta:` for a HIT-IN-FLIGHT are DERIVED from the target**, not invented at the gate: `owner:` := the target's `by:` (or `bank`), `eta:` := its `started:` + QA_CLAIM_TTL_HOURS. One clock, not two.
      - **④ POINT: the ASYNC re-resolve is now ENFORCED.** `commissioned-target-answered` FAILs a section whose answer landed and was never harvested (the in-flight path has no live return, so this is its only road to `read`); `commissioned-target-superseded` FAILs a stale target.
      - **A QA file with NO state line is MALFORMED, not legacy.** Do not bind `target:` at it (`read-target-no-state`); only its owner may complete it.
      - **check-probe-cards.sh:** new codes `qa-no-state` · `read-target-no-state` · `commissioned-target-answered` · `commissioned-target-superseded` · `commissioned-target-no-state`; the `commissioned-overdue` message now reports the target's ACTUAL state instead of asserting "no QA file" about a file that has been on disk for weeks; a missing `<paper_root>` fails fast instead of HANGING FOREVER (the `cd` was unchecked and the ancestor walk spun on `dirname "" → . → .`).
      - Fixtures re-run on BOTH copies: A (clean read→answered) PASS exit 0 · G (legit in-flight commissioned→working) PASS exit 0 · B/C/D/E/F and the four new ones FAIL exit 1.
260714 · `4.1.0` · the consumer side of the QA STATE LINE (R19/R20/R21)
      Follows constitution `haipipe-probe` 8.2.0 (JL ruling 2026-07-14; Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ PART 3b, `>> CC0714`). Vocabulary is IDENTICAL to the application twin (4.2.0) and to the task/discovery executors — the field names, the state values, the TTL constant and the FAIL codes are one set, not four.
      **The hole this closes.** Two consumers ask the same question a week apart. The first dispatches an expensive P-B-E-R run. The second, while that run is STILL GOING, sees no QA file — because a QA file was written ONCE, at REPORT, complete, and its EXISTENCE was the only signal — and dispatches THE SAME RUN AGAIN. Nothing prevented it.
      Added
      - **② MATCH reads the STATE LINE of every candidate QA file. Existence is no longer the signal.** `answered` → a T2 HIT. `working` → ⏳ IN FLIGHT: the question is ALREADY BEING ANSWERED, so the section goes `state: commissioned`, `target:` points at that QA file, and there is **NO SECOND DISPATCH**. `superseded-by:` → FOLLOW THE CHAIN to the live answer; never bind `target:` to a superseded file. No state line → LEGACY (pre-R19), treat as `answered`.
      - **④ POINT: `ls` no longer settles the section's state.** The TARGET'S state line does: absent|`working` ⇒ `commissioned` · `answered` ⇒ `answered` · superseded ⇒ re-point. A target still `working` past `QA_CLAIM_TTL_HOURS` (24) means the run is DEAD ⇒ back through ③ DISPATCH.
      - **⑤ INTERPRET is legal ONLY against a target that is `answered` and NOT superseded.** Reading a `working` file is reading an EMPTY `## Answer`; reading a superseded one is a reading that is true of an answer that is no longer true.
      - **PART 2 states the invariant out loud: ONE WRITER — the EXECUTOR, and nobody else, EVER.** "Write-once" was never the real rule; ONE WRITER was. Two writes by the same owner (the CLAIM at the qa gate's ③ decision, the COMPLETION at REPORT) is fine. This worker must NEVER create, claim, edit, complete or supersede a QA file — not even one it commissioned, not even to clear a zombie claim. A consumer-planted `working` file is the retired `_ASK/` stub wearing a `QA/` costume. Also added as a hard boundary.
      - PROOF 2 and PROOF 4 now require the `- state:` line of the file the worker branched on. A step whose proof is absent did not happen.
      **check-probe-cards.sh — FIVE NEW TEETH** (filename unchanged: 65 refs across 33 files; internals only). Each catches a bug that was SILENT before:
      - `read-target-working` — a section at `state: read` whose `target:` is a QA file that is `state: working`. The paper claims it read an UNFINISHED answer.
      - `read-target-superseded` — a section at `state: read` whose `target:` carries `superseded-by:`. **THE DAY-1/DAY-40 SILENT-FALSE-CLAIM BUG**: day 1 the task answers "no cycle column" and the paper reads it as C6-supported; day 40 a re-run finds the column and writes QA/2; the paper's `target:` still points at QA/1. Every file is internally consistent, nothing is a lie, and the claim is now FALSE. Nothing fired before.
      - `qa-working-no-started` — a `working` QA file with no `started:`: an UNEXPIRABLE claim, so every future reader defers to it forever.
      - `qa-working-expired` — a `working` QA file older than `QA_CLAIM_TTL_HOURS`: a ZOMBIE claim from a dead run.
      - `qa-answered-empty` — `state: answered` with an EMPTY `## Answer`: a LYING RECEIPT.
      Changed
      - The new state-line logic is factored into **ONE shared block (`QA_STATE`)**, called by the PASS-1 section-target test and the PASS-3 bank scan — exactly as the LAW-2 lint (`LEAK_AWK`) now is. The two hand-copied checkers had already drifted into IDENTICAL bugs once; the state block is byte-identical across both copies (verified by diff), and the TTL is referenced by NAME (`QA_CLAIM_TTL_HOURS=24`), never as a literal.
      - A QA file with no state line asserts NOTHING (legacy, pre-R19). A gate that FAILs correct work is worse than one that misses.
      Verified (fixtures under a temp project, BOTH checker copies, byte-identical output)
      - A clean: `state: read` → `state: answered` QA file with a real `## Answer`, **including the false-positive bait** (a commission naming a real path `tasks/.../C3-Visual-ForecastScaling/` and forecast horizons H1/H6) → **PASS exit 0**. The gate was not broken.
      - B `read` → `working` target → FAIL. C `read` → superseded target → FAIL. D `working`, no `started:` → FAIL. E `working`, started 3 days ago → FAIL (`72h >= QA_CLAIM_TTL_HOURS=24`). F `answered`, empty `## Answer` → FAIL. All exit 1.
      - **G LEGIT IN-FLIGHT**: `state: commissioned` section → `state: working` QA file with a FRESH `started:` → **PASS exit 0**. The change WORKS, rather than merely failing things.
      - Regression: the LAW-2 lints still fire on both surfaces — the A03-form bare-label bank leak (`- C6: … → NO`, the slash pair `C6/C7`) and a stake-disclosing commission → FAIL exit 1.
260714 · `4.0.1`
      - Reference block re-pointed at `haipipe-paper/fn/probes.md` (renamed; "plans" is retired vocabulary). No contract change.
260714 · `3.9.0` · (b) -- BOOKKEEP MINTS the resource stage's cards (the Q -> PP wire had no owner)
260714 · `4.0.0`
      - **THE PAPER PROBE WORKER WAS NEVER MIGRATED. This is that migration.** It was still v3.9.0 — the card/gateway model — while the application twin shipped v4.0.0. Its DISPATCH step issued a literal `Agent(haipipe-probe-orchestrator-agent, ...)` call to an agent that had been archived to `probe/agents/_archive/` and de-registered from every registry, and line 24 declared that call "the ONLY door". Every paper stage's PROBE phase (seed/resource/claims/pitch/narrative/display/section-edit) therefore died at DISPATCH with an unknown-agent error: no paper could acquire ANY evidence, and no paper could advance past PROBE.
      - REPLACED the 4-step procedure (BOOKKEEP -> DISPATCH -> TRANSLATE -> VERIFY) with the FIVE-STEP LOOP (ORGANIZE -> MATCH -> DISPATCH -> POINT -> INTERPRET) over `papers/<P>/1-probes/PPNN_<topic>.md` question SECTIONS. MATCH comes BEFORE dispatch: most sections should close on T2 REUSE against the bank's QA corpus, and a commission is now the EXCEPTION, not the norm (the old rule was "dispatch every card, ALWAYS, no matter how small the need").
      - **DELETED the `_ASK/` HANDOFF STUB and DEFERRED HANDOFF.** The worker used to write `_ASK/PPNN_<slug>.md` into the receiving `tasks/`/`discoveries/` folder and called it "the ONLY project-side write this worker is ever permitted". It is now permitted ZERO. That write was a direct LAW-1 / R2 violation; no verb reads `_ASK/` any more (task's `fn/asks.md` is deleted, discovery's stub-seeded input state is gone); and both banks' reviewers plus BOTH checkers now HARD FAIL an `_ASK/` folder on sight — so a paper obeying its own live worker instruction contaminated the bank and redded every downstream gate in the other buckets. The durable dead-session carrier is the `commission:` block IN the section (R6).
      - DISPATCH now uses the executor orchestrators' OWN input spelling (`action: qa` / `project:` / `question:` / `leaf:`). The v4.0 application keys (`project_root`/`qa`/`target`/`deliverable`) matched NONE of their four declared input forms — with no `action:` the qa gate is never selected, and with the leaf under the wrong key a T3 ENRICH gets opened as a NEW leaf (a fresh P-B-E-R run where a new config would have done).
      - `mode: full` now actually reaches a judgment: INTERPRET dispatches `Agent(haipipe-probe-reviewer-agent)` and lands its return in `0-lifecycle/1b-claims/1b-claims.md`. Nothing dispatched the reviewer before, so a full-mode section could never be judged.
      - PRESERVED: the PROOF-per-step enforcement, the RESOURCE STAGE INTAKE (Q -> SECTION + the `-> PP<NN>` backlink) and its WRITE-BACK (the Q's `A:`), the BUILD-lane `commissioned` state (owner/eta/blocks/cross-project; future eta PASSES, overdue HARD FAILs), the three harvest-lane sub-workers, the display-request reroute.
      - **check-probe-cards.sh: INTERNALS REWRITTEN, FILENAME KEPT** (65 refs across 33 files). It was still globbing `1-probe-plans/PP*.md` and reading a `status:` field, so on any v8-shaped paper it scanned ZERO files, printed `WARN no PP*.md cards` and exited 0 — a VACUOUS GREEN over probes that were entirely unanswered. (Verified: on a fixture with a leaked commission, a dangling target and a contaminated bank file, the old script returned EXIT=0 and found nothing.) Now: 3 passes (per-SECTION state derivation + target resolution on disk; working docs; the bank's QA/*.md), reading `- state:` and handling exactly the six derived states, with `verdicted`/`dispatched` FAILed as dead vocabulary. The paper-only RESOURCE-STAGE PASS is re-attached and re-pointed at 1-probes/.
      Adversarial review, BLOCKER 1 — the ROOT one. The new RESOURCE stage could ASK and could not be ANSWERED, because nobody minted the card:
      - the resource stage writes `Q<n>` into `0-lifecycle/1a-resource/1a-resource.md` and is FORBIDDEN to mint a PP id (JL's Q-not-PP ruling);
      - this worker's STEP 1 resolved cards from `1-probe-plans/README.md` planned items to EXISTING PPNN cards, and NEVER read `1a-resource.md` — the word "resource" did not appear in this file at all;
      - the gateway takes `correlation_id: PPNN` as an **INPUT**, so a PP id cannot be its OUTPUT.
      Nobody minted. The resource stage's PROBE phase made exactly one call (`from-buffer <paper_root>`) into an EMPTY buffer, and the CHECK gate greened over it. Empirically: `check-probe-cards.sh <Paper-CGMtoAge> --stage resource` printed `OK no cards serve stage 'resource'` and exited 0.
      Added
      - **STEP 1 (BOOKKEEP) — STAGE INTAKE: RESOURCE.** Runs first, only when the invoking stage is RESOURCE. Read `1a-resource.md`; for every `Q<n>` GATE 1 approved (present, not DECLINED in `_LOG_1a-resource.md`) that has neither an `A:` nor a `-> PP<NN>` backlink, MINT one card in `1-probe-plans/` (`serves: resource` · `blocks: N<n>` · `target: ?` · `status: planned` · `## Need` = the Q **verbatim** — a resource question is already paper-agnostic: it asks what EXISTS, never which answer is wanted, so it crosses the bridge as written). Then WRITE the `-> PP<NN>` backlink into 1a-resource.md. That backlink is the mechanical proof the question was asked, and it is what the CHECK gate tests. This is exactly JL's ruling — *"the probe stage will pick them up"* — and the stage still never mints a PP id and never picks a probe TYPE or TOPIC: the GATEWAY does that in its SWEEP.
      - **STEP 3 (TRANSLATE) — RESOURCE WRITE-BACK.** A card that `serves: resource` writes its landed takeaway back into 1a-resource.md as the Q's `A:` (existence AND fitness, and what it KILLS). A BUILD card writes its A the moment the build is BOOKED (`COMMISSIONED · owner · eta · blocks · cross-project`), and the async path overwrites it with the real answer when the receipt arrives. Both receipts are required: the card is the probe-layer one, the Q's `A:` is the consumer-facing one — 1a-resource.md is what the human reads at GATE 2, so a stage whose answers live only in cards never sees its own answers. PROOF 3 now also demands the written-back `A:`.
      - **`check-probe-cards.sh` — RESOURCE-STAGE PASS.** Fires only on `--stage resource`, only when `1a-resource.md` exists. Every `Q<n>` must carry an `A:`, or a `-> PP<NN>` backlink to a card that EXISTS ON DISK, or a DECLINED line in `_LOG`. None of the three -> `FAIL unasked-question(Q3)`. A backlink to a missing card -> `FAIL dangling-backlink`. And "no cards serve stage resource" while questions are still open no longer prints the reassuring OK — it FAILs as the VACUOUS GREEN. Same class of bug the toolkit already fixed once (a gate going green over an un-run probe, JL 2026-07-07); this time it was the gate going green over a stage that asked NOTHING.
      The ownership chain, now stated in both skills: `DRAFT asks (Q) -> GATE 1 approves -> PROBE WORKER mints the card -> GATEWAY picks type + topic -> answer lands -> TRANSLATE writes the A back into the Q`.
      Verified on a fixture with an unasked Q, an asked Q (resolving backlink) and an answered Q: the unasked one FAILs by name, the other two PASS; adding the backlink turns the run green; a dangling backlink FAILs; a DECLINED Q is exempt; papers with no `1a-resource.md` are unaffected (POSIX `sh` + `dash`, `set -u`-safe).
260714 · `3.9.0` · TRANSLATE writes `commissioned` (the BUILD lane finally has a producer)
      `check-probe-cards.sh` already enforced `status: commissioned` (owner + eta + blocks + cross-project + the C6 future-eta test) for the RESOURCE stage's BUILD lane. But NO step in this worker ever WROTE that status — STEP 2 wrote `dispatched`, STEP 3 wrote `read` / `verdicted` / `answered-local`. A real in-flight resource BUILD therefore sat at `dispatched`, which the checker FAILs as `status-dispatched(probe-not-run)`, reddening the CHECK gate on exactly the work JL ruled NON-BLOCKING, ALWAYS. The C6 anti-laundering guard could never fire, because nothing could enter the state it guards: a status only the checker could read and no producer could write.
      Changed
      - **STEP 3 (TRANSLATE) — new BUILD-LANE rule.** A card whose work is a BUILD (`task-for-data` / `task-for-algo` / `task-for-fit`, or a long acquisition such as a DUA/IRB) and whose answer has not landed lands as `status: commissioned` WITH `owner:` + `eta:` (future, YYYY-MM-DD) + `blocks:` + `cross-project:` (a sibling-project path the gateway NAMED, or `none-found` — MANDATORY on every BUILD card, JL ruling C4). A SCAN-lane card (store scan, capability grep, access-rung, literature) is unchanged: `dispatched -> read`, because it returns in minutes.
      - **STEP 3 async path** — a card with no answering report yet stays in its in-flight status honestly: SCAN `dispatched`, BUILD `commissioned`. When the receipt lands it translates like any other return (`commissioned -> read`).
      - **STEP 2 (DISPATCH)** — a BUILD-lane card is never written `dispatched` in the first place (a deferred handoff is BUILD-lane by construction: that is what "long-running" means).
      - **STEP 4 (VERIFY)** — the checker summary now states the commissioned rule: PASS with the four fields + a future eta; FAIL overdue or missing any field.
      WHY the split exists at all: `dispatched` FAILing as probe-not-run is CORRECT for a scan (a scan that has not come back in minutes did not run) and WRONG for a build (a 3-week build has not failed, it is working). `commissioned` PASSES the gate while its eta is in the future and goes HARD FAIL the instant that eta passes with no receipt — the date test is the only thing standing between this status and a laundering token.
      Companions: haipipe-probe 7.10.0 (status vocabulary + card anatomy: `commissioned` + the four fields, disk-derived like every other status) · haipipe-paper/fn/probe-plans.md (status list mirrored) · check-probe-cards.sh (enforcement already present, unchanged).
260712 · `3.8.1` · Audit repair
      - **`Agent` added to allowed-tools.** The frontmatter granted Bash/Read/Write/Edit/Grep/Glob/Skill but NOT Agent — while the skill's mandated STEP 2 is an `Agent(haipipe-probe-orchestrator-agent)` dispatch and STEP 3 dispatches harvester subagents. The worker could not legally perform its only permitted evidence door.
      - Async-harvest grep made shape-agnostic (`answers:.*\bPPNN\b`) — the literal `answers: PPNN` string never matched a multi-stub list report.
      - check-probe-cards.sh bridge pass now flags CLAIM ids (C1/C3) as well as hypothesis ids: the PAPER-AGNOSTIC rule names "H1/H2/C3" explicitly, but the regex only caught H-ids, so a stub leaking `serves: C1, C2, C3` PASSed (the live ScalingLaw stub did exactly that).
260712 · `3.8.0` · Routing: cards carry target:, TRANSLATE writes back the actual
      JL routing ruling 2026-07-12 (haipipe-probe 7.8.0 companion): the paper must record WHERE each ask is sent, and where its answer will land.
      - BOOKKEEP: the card anatomy now includes `target:` (existing `tasks/<group>/<folder>` or `discoveries/<folder>`, `NEW ...`, or `?`). `?` is fine at DRAFT and still dispatchable (the gateway's SWEEP resolves it), but a card that reached the campaign pass unresolved is reported as a planning gap, not dispatched silently.
      - DISPATCH: the Agent(...) prompt carries `target:` verbatim.
      - TRANSLATE: when the gateway's SWEEP re-routed away from the proposed target (its `handoff:` names the actual landing site), write the ACTUAL back into the card's `target:` — the card must not lie about where its evidence lives.
260712 · `3.7.0` · Both-banks layout: card pool + _ASK/ container
      JL ruling 2026-07-12 (pairs with haipipe-probe 7.7.0; supersedes the 2026-06-29 per-stage layout for PROBE CARDS only):
      - BOOKKEEP resolves cards at `<paper_root>/1-probe-plans/PPNN_*.md` -- flat cross-stage pool beside the campaign README; stage affinity = the card's `serves:` field (header `stage:` -> `serves:`), never its path. Legacy per-stage `0-lifecycle/*/_PROBE/` cards are moved into the pool on first touch (stub `from:` pointers updated).
      - Stub paths -> `<receiving folder>/_ASK/PPNN_<slug>.md` (gateway + DEFERRED HANDOFF both write into the `_ASK/` container; filename mirrors the card's).
      - check-probe-cards.sh: card loop scans `1-probe-plans/PP*.md` FIRST plus the legacy per-stage globs; bridge pass scans `_ASK/PP*.md` plus legacy flat `_ASK_*.md`; WARN message updated. Check semantics unchanged.
260712 · `3.6.0` · TRANSLATE DOWN: the dispatch plan is paper-agnostic
      JL ruling 2026-07-12 (pairs with haipipe-probe 7.6.0). The worker already called itself "the bilingual layer" at STEP 3 — but only translated on the way UP. STEP 2 said to paste `<the PP card's Need + Why + Route, verbatim>` into the gateway plan, and the card's `Why` IS the paper's stake. So the paper's private vocabulary went straight down the bridge, into the `_ASK` stub, and from there into the discovery's own artifacts.
      Changed
      - **STEP 2 DISPATCH** — `verbatim` is GONE. The plan now carries `<the PP card's Need + Route -- TRANSLATED, never the Why>`. New TRANSLATE DOWN block: strip claim/hypothesis labels (H1/H2/C3), the words seed/paper/pitch/narrative, the whole `## Why` block, and any hint of the preferred answer; re-pose the need as SELF-CONTAINED evidence questions named Q1/Q2/.... Adds `correlation_id: PPNN` to the dispatch (an opaque routing token carrying no paper semantics).
      - **STEP 3 TRANSLATE** — states the translation is TWO-WAY and that STEP 2 owns the DOWN half; STEP 3 is the UP half (evidence Q1/Q2 → paper H1/H2), landed in the card, the only bilingual document.
      - **check-probe-cards.sh** — NEW bridge pass over the execution bank: every `_ASK_*.md` under `discoveries/` and `tasks/` is grepped for consumer vocabulary and stake disclosure and FAILs on either. Previously the checker inspected only the paper bank, so a contaminated stub passed silently — which is exactly how the 2026-07-11 seed incident went green. Patterns are narrow by design: `- from:` is exempt (legitimate provenance) and "the paper" is not flagged (a discovery legitimately says "the paper reports X" about a SOURCE paper — verified no false positive).
      Fixes
      - The 2026-07-11 seed incident (`Paper-PersonalizedGlucoseModel`): both dispatched probes contaminated their discovery, which came back structured around the paper's H1/H2 and was therefore not reusable by any other paper. Re-run clean under this contract.
260711 · `3.5.0` · Worker obeys the Campaign DAG
      Changed (JL cross-stage ruling 2026-07-11; pairs with haipipe-probe 7.5.0 + haipipe-paper 2.8.0)
      - STEP 1 BOOKKEEP: 1-probe-plans/README.md split honored — `Status board` generated (cards win), `Campaign` AUTHORED (by /haipipe-paper probe plan) and OBEYED: it sets the dispatch ORDER. Gating cards first; DAG-dependent cards held until the upstream `answers:` lands (STEP 3 async grep); dispatching the whole buffer flat when a DAG exists is a defect. No Campaign section → flat buffer as before.
260711 · `3.4.0` · Deferred handoff + async harvest (two-footed bridge)
      Added (JL ruling 2026-07-11, GlucoScaling design session; pairs with haipipe-probe 7.4.0 + gateway 2.1.0)
      - STEP 2 DISPATCH: the gateway now writes an `_ASK_PPNN.md` handoff stub into the receiving tasks//discoveries/ folder before executing — noted, with PROOF 2 extended to cover the stub path from the gateway's `handoff:` return line.
      - STEP 2 DEFERRED HANDOFF mode: for long-running needs (training, multi-day runs) or a two-session workflow (one session on tasks, one on the paper), this worker writes the stub DIRECTLY and stops — its ONLY permitted project-side write; verdict-blind, write-once; a later /haipipe-task or /haipipe-discovery session picks it up. Inline-search ban untouched (a stub carries an ASK, never findings).
      - STEP 3 ASYNC PATH: every run checks each `dispatched` card for an answering report (`answers: PPNN` in report.yaml / discovery report blocks) and TRANSLATEs from the report + artifacts exactly as from a live agent return; no answer → the card stays `dispatched` honestly (waiting, not failed).
      Changed
      - STEP 1 BOOKKEEP: `1-probe-plans/README.md` is a GENERATED dashboard — when it disagrees with the cards, the cards win and the index regenerates (statuses derive from cards + stubs + answering reports).
260710 · `3.3.1`
      Fixed (fresh-agent audit, C1/M7/M11/M18)
      - ref/per-stage-dispatch.md display row rewritten for R3 (DR reroute from section/narrative; display stage is the only commissioner) + 📨 legend on section-edit row.
      - PPNN-anatomy reference gets a layout-agnostic find pattern (relative path breaks on flattened installs).
      - Whitelist display item widened: 0-displays/ units + index for existence/LINK, */source/ for numbers.
260710 · `3.3.0`
      Changed (JL 2026-07-10 display-request ruling)
      - STEP 2: display-shaped PP cards (a display unit that does not exist) are REROUTED to the 4-display inbox as DR rows and closed `answered-local` with takeaway `rerouted to display stage: DRNN` -- never dispatched to the gateway.
260710 · `3.2.0`
      Changed (JL: "maybe things are already there before... we don't need the heavy probe")
      - STEP 2 gains a mandatory LOCAL SWEEP before dispatch: closed whitelist of the paper's own registries (sibling/prior _CITATION_/_VALUES_/_EVIDENCE_, read|verdicted PP cards' refs, 0-displays/*/source/, .bib). Need answered there -> `status: answered-local (from <files>)`, no gateway call; partial -> dispatch only the remaining gap. Adopt the pointer, never the verdict (PLACE re-verifies against the original source).
      - PROOF 2 accepts sweep hit lines in place of the Agent() call for answered-local cards.
      - check-probe-cards.sh: accepts answered-local (refs resolve under project_root OR paper_root); status grep now hyphen-aware; card + working-doc globs extended one level deeper (section-level `0-lifecycle/5-section-edit/<section>/_PROBE/` cards and _CITATION_/_VALUES_ docs were previously invisible to the checker).
260707 · `3.1.0`
      Changed (Part-0 harvester ruling; JL: "they are the harveste agents to check the content and genearte the report accordingly. The don't need to restart the whole probe process, they are just one step within the whole probe" / "Yes, this is true! Pelase go ahead for it")
      - ONE-pipeline framing replaces "two route families": ACQUIRE (gateway, the only door) → HARVEST (citation/values/display, pointer-following transcribers). Paper-side may follow pointers; only the gateway may find things.
      - STEP 3 lane obligations: a return carrying harvestable content is FIRST written into the PP card as a lane line (`pick_list:`/`value_refs:`/`unit_refs:` · `harvest: OWED`), THEN the matching harvester subagent is dispatched (cheap tier, reads its worker SKILL headless — the citation-harvest pattern extended to all three lanes) and mechanically accepted; acceptance flips the line to `harvest: accepted (...)`. Fixes the seed-stage incident class (B5): a skipped harvest used to leave zero disk residue.
      - PROOF 3 extended: every lane line requires the harvester Agent call + acceptance-grep output in the reply.
      - STEP 4 / checker: check-probe-cards.sh now FAILs `status: planned|dispatched` cards (probe-not-run — the invariant three sibling docs promised, T1/B6), FAILs `harvest: OWED` lane lines, and scans working docs for bibtex/tables (B10). The CHECK gate re-runs it (wired in haipipe-paper-check 1.7.0).
260707 · `3.0.2`
      Changed
      - Hard boundaries: explicit "no inline search in the PROBE phase" -- durability is the whole point; the orchestrator dispatch is the only door. DRAFT may WebSearch for orientation; the difference is card durability (planned skeleton vs read+refs), not the search verb.
260707 · `3.0.1`
      Changed (post test-12334535 -- the v3.0 chain ran clean end-to-end in a fresh session; these four are the minor gaps the run surfaced, none a correctness hole in the enforcement)
      - check-probe-cards.sh brace-aware: refs like `.../{sources.md,notes.md,landscape.md,verdict.md}` (the shorthand agents naturally write) now expand + resolve instead of false-FAILing; also handles top-level comma lists. Regression-tested: brace card PASSes, empty-refs+table card still FAILs.
      - DISPATCH rule: when `discoveries/` is empty (or only .gitkeep) every plan is fresh -> force `run_in_background=true` on all; and never label a dispatch "background" unless the flag was actually set (test-12334535 ran three sync dispatches while PROOF 2 claimed "all background").
      - Harvest no-bibtex acceptance anchored: `grep -cE '@(article|inproceedings|...)\{'` == 0, not bare `@` (venue names like `KHD@IJCAI workshop` carry a legit `@`; bare grep false-rejected a real card).
      - Seed CHECK gate locates the checker layout-agnostically via `find ~/.claude/skills ...` (installed skills flatten the tree; the `../../../2-phase/...` relative path is unreliable there).
260706 · `3.0.0`
      Changed (rethink after the ProjC seed shortcut: rules existed but were prose-only, buried in 15-line paragraphs — the executor compressed them away and searched inline, writing tables into _PROBE/ cards with nothing landed in discoveries/)
      - Rebuilt as a 4-step procedure: BOOKKEEP → DISPATCH → TRANSLATE → VERIFY, each ending in a mandatory PROOF shown in the reply (project_root + ls, the literal Agent call, per-card refs + ls, checker output). A step without its proof did not happen.
      - NEW `check-probe-cards.sh`: deterministic verifier (read/verdicted ⇒ refs resolve under project_root; no markdown tables in any card; ≤80 lines; status:failed surfaced). Run at STEP 4 and re-run by the stage CHECK gate — two enforcement points.
      - project_root resolution corrected: walk-up to first ancestor with discoveries/ ONLY; `git rev-parse --show-toplevel` dropped (repo-backed papers are their own repos, it returns paper_root).
      - Reference prose moved out of the invocation path: `ref/per-stage-dispatch.md` (stage map, seed/claims specifics, section-edit logic, status forms) + `ref/harvest-acceptance.md` (harvest dispatch + literal acceptance greps). Main file 260 → ~150 lines.
      - Hard boundary added: NO markdown tables in PP cards / _CITATION_ / probe-discovery documents (JL standing rule).
260706 · `2.6.0`
      Changed (first pass at the same incident, prose-only — superseded by 3.0.0 same day)
      - BOOKKEEP resolves project_root + ensures PP-card anatomy by spec path, not memory; DISPATCH shows the concrete Agent input {project_root, mode, plan}; TRANSLATE makes refs MANDATORY (empty refs = failed phase, not green).
260705 · `2.5.0`
      Changed (probe folderless refactor — probes/ retired; PPNN card = single source of truth)
      - Step 0 RE-INVOKE PER RUN: every stage's PROBE phase invokes this skill fresh (test-123333333 PP02 ran from a 3-hour-old in-context copy missing same-day rules).
      - TRANSLATE: `refs:` always point directly at execution artifacts (discoveries/tasks); full-mode verdicts land in the PPNN card's `## Verdict` (gates + verdict + reasoning) and flip the claims ledger in the same pass.
      - DISPATCH: shape vocabulary aligned to gateway 2.0.0 (reused | enriched | fresh); no shape creates a probe folder.
260705 · `2.4.1`
      Changed (test-123333333: harvest synonymized the canonical status string — `retrieved ✅ (discovery, ...)` for `VERIFIED-by-discovery (...)` — and acceptance waved it through on semantic equivalence)
      - Provenance acceptance grep made LITERAL: `grep -c 'VERIFIED-by-discovery'` must equal the discovery-verified pick count; same-meaning rewordings are REJECTS. Meaning-judgment is what mechanical acceptance exists to remove; canonical strings are VERBATIM per the citation skill's spec (1.5.2).
260705 · `2.4.0`
      Changed (cost pass after test-2-2222: $24 / 28min, 54% of spend = context loading)
      - Harvest subagent dispatches on the CHEAPEST model tier (Agent model: haiku, effort low) — pure transcription guarded by mechanical acceptance; the one acceptance-reject retry escalates one tier up instead of same-tier.
260705 · `2.3.3`
      Changed (test-2-2222 harvest: cards had substance but NO authors/year/venue — the worker's own compressed re-enumeration of the citation card spec had dropped the identity bullet, the dispatch prompt followed it, acceptance didn't check identity → passed. JL: "title author 还有 venue 这些都没有呀")
      - DISPATCH-to-harvest: never paraphrase the card spec into the prompt; point the subagent at the citation skill's SKILL.md spec section (single source of truth). Spec-drift by telephone game is the named failure mode.
      - ACCEPTANCE gains two greps: identity bullet per card (a `^- ` line with `(YYYY)`; title-only card = REJECT) and status-carries-provenance (S## VERIFIED in sources.md → card must say `VERIFIED-by-discovery`; bare "unverified" = REJECT).
260705 · `2.3.2`
      Changed (test-2-2222: worker went sync on a from-scratch probe; JL's session froze 25 minutes through the 4-layer chain)
      - DISPATCH: fresh runs go `run_in_background`, hard. The "I need the return to TRANSLATE" excuse is named and voided (background return arrives, TRANSLATE runs then). Fresh-vs-reuse judged from plan content alone; when unsure, background.
260705 · `2.3.1`
      Changed (Paper-Probe-Test: an elicited AUDIT scope had no named route, so the stage hand-rolled a general-purpose web auditor)
      - DISPATCH: audit-shaped scopes (re-verify / audit / double-check the existing set) are ordinary plans for the SAME `Agent(haipipe-probe-orchestrator-agent)` dispatch — the agent answers them from the ledger (VERIFIED + method + date IS the verification). Never invent a side-channel worker because a scope has no named row.
260705 · `2.3.0`
      Changed (run-3 audit: acceptance claimed "each has anchor + finding" while `grep -c 'finding:'` returned 0)
      - TRANSLATE harvest acceptance is MECHANICAL-FOR-REAL: run the greps, never eyeball. Four checks: card count == pick_list; every new card has `- summary:` + `- finding:`; every `source_ref` S## must EXIST in the named sources.md (unresolvable anchor = REJECT — it means the agent's fresh evidence never landed); no bibtex. One reject → re-dispatch harvest with defect list (one retry), else `status: read (harvest DEFECTIVE)` surfaced in the stage reply.
      - Harvest dispatch prompt now PASSES the card-format spec explicitly (### heading + summary/finding/relevance/status/Scholar/source_ref bullets) instead of assuming the subagent infers it.
260704 · `2.2.0`
      Changed
      - TRANSLATE: citation harvest now dispatches the harvest SUBAGENT on a pick_list return, then does mechanical acceptance (produce/review split); the worker no longer transcribes source substance itself.
260704 · `2.1.0`
      Changed
      - TRANSLATE = pure transcription of the agent's anchored return (takeaways with per-line source anchors; structured sources manifest -> _CITATION_); the worker reads NO project files, may only `ls`-verify returned refs (existence, never content). Large harvests (>~20 entries / multi-discovery) run the citation worker as a subagent. DISPATCH: likely-reuse plans go synchronous, likely-fresh-discovery plans go run_in_background.
260704 · `2.0.0`
      Changed (JL ruling from the seed-test replication: 不管是啥，probe orchestrator agent 来做)
      - Worker contract narrowed to BOOKKEEP / DISPATCH / TRANSLATE. Dispatch is ALWAYS `Agent(haipipe-probe-orchestrator-agent)` — the tiny-lookup inline carve-out is removed (it was the license for the observed bypass). The worker never sweeps the project or reads discoveries/probes/insights inline; the reuse decision (enrich / reuse-directly-no-wrapper / create+gather) belongs to the agent's SWEEP in clean context. Plan `ref:` may point at a probe or a directly-reused artifact (lean option B).
260704 · `1.8.0`
      Changed
      - From-buffer reads the index then per-stage `_PROBE/` files; default dispatch = Agent(haipipe-probe-orchestrator-agent) (clean context), inline Skill only for tiny single lookups.
      - TRANSLATE step made explicit (probe is paper-unaware; this worker is the bilingual layer): light-probe takeaways backfill the PP plan file (`status: read`, `_DISCOVERY_` retired); sources in the Read output are HARVESTed by haipipe-paper-probe-citation into `_CITATION_{stage}.md`. Seed dispatch row gains `○ harvest` for citation.
260703 · `1.7.2`
      Changed
      - Evidence-routes rule extended: stage skills never dispatch discovery/task orchestrator agents or /haipipe-probe directly; this worker is the only door (bypassing it leaves no project-side probe). Seed row de-"optional"-ed: DEFAULT RUN for a new seed, skip only by explicit logged verdict.
260703 · `1.7.1`
      Fixed
      - Strip-form example corrected to `probe: cite 🔥🚀` (was a marker-less `cite ⬜` while probe is the active phase; violates the exactly-one-🔥-one-🚀 rule).
260703 · `1.7.0`
      - From-buffer entry added (JL: 不要让 haipipe-paper 直接 call /haipipe-probe，由本 worker 在 stage 的 phase 里 call): Skill(haipipe-paper-probe, args="from-buffer <paper_root> [PPNN]") reads planned items in 1-probe-plans/, applies reuse-before-create, dispatches to /haipipe-probe, writes back status/probe_ref, returns a dispatch summary. The umbrella's probe run verb now routes here; this worker is the single dispatch point.
260703 · `1.6.0`
      - phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE). This phase is now named after what it does: dispatch evidence needs through /haipipe-probe. The old name GATHER collided with probe's own internal Gather stage; the rename removes that collision.
260703 · `1.5.0`
      - probe dispatch rules. (1) mode: light DEFAULT (stops at Read, returns to caller), full only for committed verdicts (claims); escalation supported. (2) reuse-before-create: sweep 1-probe-plans/ + project probes + insight KB, ENRICH an existing probe over creating a near-duplicate. Also: _DISPLAY_{stage}.md declared the display worker's needs registry (need → unit → status), parallel to _CITATION_/_VALUES_; added /haipipe-insight to the downstream lifecycle map (probe deposits at Deposit).
260703 · `1.4.0`
      - reframed GATHER around two route families. Evidence routes through /haipipe-probe (the universal gateway; probe calls discovery/task during its own Gather). Seed = light probe → discovery (landscape/related-work/novelty, _DISCOVERY_0-seed.md takeaways). Claims = HEAVY probe + task (probe plans per GAP claim, tasks for runs/data, verdicts backfill _EVIDENCE_).
260703 · `1.3.0`
      - added the seed discovery route (superseded by 1.4.0's probe-gateway framing).
260703 · `1.2.0`
      - reframed as internal worker. Users invoke stage skills (seed, claims, pitch...), not this skill directly. Stage skills call this during their GATHER phase.
260703 · `1.1.0`
      - made stage-aware. GATHER now works for all stages, not just section-edit. Added per-stage dispatch table.
260703 · `1.0.0`
      - new hub skill for the GATHER phase.

<!-- haipipe:skill:log:end -->
