---
name: haipipe-paper-probe
description: "PROBE-phase worker (internal). Owns the WHOLE five-step loop: reads the stage doc's Q-consumer and ①ORGANIZEs each question into an ENTRY FILE in papers/<P>/1-probes/PPNN_<topic>/ — one q-executor per `QXn_<slug>.md` file (`## QX<n>` + `### q-executor` / `### q-consumer` / `### bank binding` / `### a-executor`; the stake stays behind in the stage-doc Q-consumer), ②MATCHes it against the bank with a read-only grep, ③DISPATCHes only what the stage's probe_depth ceiling allows, ④POINTs each target, ⑤INTERPRETs the answer back. ①② moved here from DRAFT on 2026-07-20, when the DRAFT gate they had been merged into was removed; DRAFT now raises questions and nothing else. Binds by PATH to a QA file in the probe-unaware task/discovery bank; dispatches the q-executor verbatim, never running bank work inline. Users invoke stage skills (seed, claims, pitch…), not this directly."
argument-hint: "[from-buffer <paper_root> [PPNN] | stage <stage-name>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
metadata:
  version: "6.1.0"
  last_updated: "2026-07-19"
  summary: "The paper's PROBE-phase worker — runs ①ORGANIZE→②MATCH→③DISPATCH→④POINT→⑤INTERPRET for a paper (all five; ①② came back here from DRAFT on 2026-07-20). The model (anatomy, QA contract, cost ladder, LAWS, states, checker codes) is owned by ../../../../probe/haipipe-probe/SKILL.md. This file is only the paper-side deltas. History: ./CHANGELOG.md."
---

Skill: haipipe-paper-probe — the PROBE-phase worker for a paper
==============================================================

Called by paper stage skills (seed, resource, claims, pitch, narrative, display, section-edit) after DRAFT.
DRAFT raised the Q-consumer questions in the stage doc and stopped there. THIS worker owns everything probe-shaped: ①ORGANIZE each Q-consumer into an ENTRY, ②MATCH it against the bank (read-only grep), ③DISPATCH only what the ceiling allows, ④POINT, ⑤INTERPRET.

⭐ THE MODEL IS NOT THIS FILE'S — it is owned by `../../../../probe/haipipe-probe/SKILL.md`.
Read it for the probe-file anatomy, the QA state-line contract, the cost ladder, the two LAWS, the derived states, and the checker's FAIL codes.
This file is ONLY how a paper runs the loop, plus the paper-side deltas that file does not cover.

Not user-facing: users invoke stage skills; a stage calls `Skill("haipipe-paper-probe", args="from-buffer <paper_root> [PPNN]")`.
Which stage routes where, seed/claims/resource specifics, and section-edit logic: `ref/per-stage-dispatch.md`.

The paper-side deltas:
- `paper_root` vocabulary, and the paper's OWN registries (the T1 whitelist).
- the RESOURCE stage intake and write-back (paper only).
- HARVEST, inline in ⑤.


Rules (follow these — the model is probe's)
======================================================

The PROBE-phase rules live in `../../../../probe/haipipe-probe/SKILL.md` → **Phase rules · PROBE phase** (+ **The QA file**, **The two LAWS**). Follow those; on conflict, that file wins. Paper-specific additions:
- Dispatch goes through the collector agent (`haipipe-probe-q-executor-agent`), NEVER an orchestrator called inline by this worker — results would die with the reply.
- HARVEST IS INLINE, and `### a-executor` is its ONLY sink. `1-probes/` is the only consumer-side source of truth; `_LOG_<stage>.md` is the only sidecar.
- RESOURCE write-back: the landed reading goes back into `1a-resource.md` as the Q's `A:` (existence AND fitness AND what it KILLS).
- A claim's STATUS goes in `0-lifecycle/1b-claims/1b-claims.md`, written by the AUTHOR, NEVER in the probe file.
- No bibtex / no `.bib` edits; no ad-hoc plots; no markdown tables in any probe document.

The loop below is the HOW-TO for these rules.


The loop, paper-side — DRAFT authored ①②; this worker runs ③④⑤
==============================================================

Each step ends with a PROOF this worker MUST show in its reply; an absent proof means the step did not happen.
STEP 0 — re-invoke this skill fresh every run, even when its text is already in context (a probe once ran a 3-hour-old contract).

PROBE v9.5.0 PHASE SPLIT.
①ORGANIZE + ②MATCH happen HERE. Read the stage doc's Q-consumer, and for each question author its ENTRY: the `### q-executor` (stake stripped, then FROZEN), the `### q-consumer` bullet copying the original wording, and the `### bank binding` — `route`, the `bank` verdict rooted to a SPECIFIC bank folder by READING it, and `target` (an existing path, or `NEW <path>`). DRAFT authors none of this; it never opens `1-probes/`.
This worker runs ③DISPATCH + ④POINT (COLLECT the answer from the bank, per `probe/haipipe-probe/SKILL.md`) + ⑤INTERPRET (HARVEST it into the paper's OWN registries). Collection is probe's model; harvest is this worker's, and probe says nothing about it.


① + ② — THIS WORKER AUTHORS THEM
---------------------------------

The stage doc's Q-consumer is the input. For each `## Q-<Stage>-<n>` block, find-or-open its ENTRY FILE `<paper_root>/1-probes/PPNN_<topic>/QXn_<slug>.md` (one q-executor per file; the folder is the topic) and author it. DRAFT wrote none of this and never opened `1-probes/`; if an entry is already there from a previous PROBE run, read it and do not re-author it.
- Resolve `project_root`: walk UP from `paper_root` to the first ancestor containing `discoveries/`.
  Do NOT use `git rev-parse` — a repo-backed paper is its own git repo. (The checker resolves the same way.)
- Route on the TARGET, not on the verdict. They answer different questions: `bank` says what the
  bank would have to DO, `target` says whether the readable answer EXISTS yet.

```text
  target: <an existing QA path>   → ④/⑤ : verify the state line, then harvest
  target: NEW <path>              → ③   : dispatch, whatever the bank verdict says
```

  ⚠️ `bank: reuse` + `target: NEW` IS THE COMMON CASE, not a contradiction. It means the results
  ALREADY answer the question but nobody has written the readable digest yet. It still requires
  ③ DISPATCH, because LAW 1 forbids a consumer authoring a bank file — the executor writes it, at
  its qa gate's ② DIGEST, from artifacts already on disk. That is depth 0: cheap, nothing runs, and
  it passes any ceiling. Do not mistake it for `answered` and skip the dispatch; do not mistake it
  for expensive and defer it.
- T1 LOCAL is this worker's, at ②: root the question against the paper's OWN registries and set `target` + `state: answered-local`, then write the entry's `### a-executor`. The CLOSED whitelist: entries already `read` or `answered-local` in `1-probes/` · `0-displays/` units + index · the `.bib` · `_LOG_<stage>.md`.
  Fully answered there → write the `### a-executor`, set `answered-local`, do NOT dispatch. Adopt the POINTER, never the verdict (a reused value re-verifies against its ORIGINAL source at PLACE).
- DISPLAY-shaped needs are REROUTED, not collected: a question asking for a display unit that does not exist becomes a DR row in `0-lifecycle/4-display/_DISPLAY_REQUEST.md`; close the entry `answered-local` with the `### a-executor` "rerouted to display stage: DRNN".
- RESOURCE (paper only): the resource stage's DRAFT opened one probe ENTRY per `Q<n>` it drafted, and the human then APPROVED that set at GATE 1 — so by the time this worker runs, every entry it sees is GATE-1-approved (present, not DECLINED in `_LOG_1a-resource.md`) — its `### q-consumer` names that resource `Q<n>`, `**blocks**: N<n>` under `### bank binding` — and wrote the `**Q<n> (N<n>) -> PP<NN>**` backlink into `1a-resource.md`, the mechanical proof `check-probe-cards.sh --stage resource` tests. The ownership chain: the STAGE DRAFT asks (Q<n>) + opens the entry → the HUMAN approves at GATE 1 (the DRAFT gate) → this worker ③ dispatches / ④ points → ⑤ writes the A back. The stage never mints a PP id. If a legacy DRAFT left the intake undone, this worker opens the missing entries on first touch (transition only).

③ — THE CEILING GATE, run BEFORE any dispatch
----------------------------------------------

⛔ NO ENTRY IS DISPATCHED WITHOUT PASSING THIS. Read `probe_depth:` from the stage's contract
(`../../../1-lifecycle/haipipe-paper-stage/stages/<order>-<key>/stage.md`), or take the value the
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
spend; a stage that removed its DRAFT gate has no other one. Report in the `[PROBE]` _LOG entry
which ceiling was in force, how many entries dispatched, and how many deferred at what depth.

PROOF 1: `project_root=<path>` + `ls <project_root>/discoveries/` + `ls <paper_root>/1-probes/`, the `probe_depth` in force, and per entry its `bank` verdict + resolved depth + `target` (dispatched / deferred).


③ DISPATCH — hand the NEW entries to the collector agent
--------------------------------------------------------

For each STILL-COLLECTING entry (`target: NEW` — `bank: new | run | code` — not resolved by T1 LOCAL), hand the SET to the collector agent, tagging each with the DRAFT-authored `route` (task|discovery — AUTHORITATIVE, not a hint):

  ```text
  Agent(haipipe-probe-q-executor-agent, prompt="
    project_root: <from ①>
    probe_files:  <the PPNN files touched this run>
    dispatch:     <entry ids with target: NEW>, each with its route: task|discovery
  ")
  ```

The agent runs in ITS OWN clean context: it sends each `q-executor` VERBATIM to `Agent(haipipe-task-orchestrator-agent)` / `Agent(haipipe-discovery-orchestrator-agent)` (`run_in_background` for fresh work; omit the leaf for fresh — the orchestrator picks the folder and returns the path), and returns `{ entry → target: QA-path | in-flight | failed }`, having written each `target`.
Under model A the agent does NOT re-run ②MATCH — THIS worker rooted each question at ② just above; the agent DISPATCHES (the executor orchestrator's OWN QA-gate still dedups against an existing answer). It NEVER reads the paper's registries, the `### q-consumer` copies, or the stake — its clean context IS the wall; and it never authors a fresh folder (LAW 1).
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

⑤ INTERPRET — the a-executor, the a-consumer, the claim status, and HARVEST (the paper's own, not probe's)
--------------------------------------------------------------------------------------------------------------------

- Copy the QA answer into `### a-executor` (the probe-file single source of truth), then each Q-consumer writes its own a-consumer in its stage doc (station ②, anchored `[source: PP<NN>]`) — translate the general answer UP into the paper's words.
  ONLY against an `answered`, non-superseded target (probe).
- The AUTHOR writes the claim status (`supported | refuted | inconclusive` + confidence + claim_type) into `0-lifecycle/1b-claims/1b-claims.md`, never in the probe file — unconditionally.
  A probe is communication, not judgment — there is no review gate; keep the `claim_type` overclaim check (never causal from associational evidence).
- RESOURCE WRITE-BACK (an entry serving a resource `Q<n>`): write the landed reading BACK into `1a-resource.md` as the Q's `A:` line — existence AND fitness AND what it KILLS ("probably fine" is a DEFECT, not an answer).
  A BUILD-lane entry writes `A: COMMISSIONED · owner <who> · eta YYYY-MM-DD · blocks N<n> · cross-project: <path|none-found>` at booking; the async path overwrites it on landing.
  Both receipts: the entry is the probe-layer one, the Q's `A:` is what the human reads at GATE 2.
- HARVEST — inline, in this worker, into the SAME `### a-executor`. Whatever reusable material the answer carries rides along with the answer:
  - **source anchors** (literature): transcribe each into the `### a-executor` in the QA file's own words, with its identifiers. NEVER generate bibtex; NEVER touch `.bib`. Carry provenance at TWO levels and never flatten them — `VERIFIED-by-discovery` is arXiv-level, NOT bibtex-level, so a source stays 🔍 until a human confirms it. An entry carrying only identity fields (title/authors/year) and no statement of WHAT the source found is a DEFECTIVE harvest: the reader must be able to see what each source contributes without opening the discovery folder.
  - **values** (numbers): transcribe the number AND the named source path it came from. FABRICATION GUARD: the literal value string must grep in its named source file — `grep -F '<value>' <source>` — and a value with no source hit is REJECTED. The parquet/script decides, never the prose.
  - **display units**: name the landed `0-displays/<unit>/` path. LINK ONLY UNITS THAT EXIST (or whose DR row is `done` with the unit path filled) — a `requested`/`accepted` DR row stays 📨 pending and is flagged for CHECK; never pre-place a `\ref` for a display that does not exist yet, or the tex compiles to `??`.
  Placing any of this INTO manuscript prose is REVISE's job (`haipipe-paper-revise-place`), not this worker's. This worker transcribes; it does not edit the manuscript.

PROOF 5: per entry the `### a-executor` copy + the stage-doc a-consumer line, the claim-ledger diff (if it serves a claim), the `grep -A2 'Q<n>' 1a-resource.md` for a resource write-back, and — for any harvested value — the `grep -F` output proving it appears in its named source.


VERIFY — the checker (the stage CHECK gate re-runs the same script)
------------------------------------------------------------------

```
sh <this-skill-dir>/check-probe-cards.sh <paper_root> [<project_root>] [--stage <key>]
```

`--stage resource` also runs the resource pass over 1a-resource.md: every `Q<n>` must carry an `A:`, a `-> PP<NN>` backlink (to a probe file that EXISTS), or a DECLINED line — none of the three FAILs as `unasked-question`, and "no entry serves stage resource" while questions are open FAILs as the VACUOUS GREEN.
The FAIL codes are probe's.
Never report a green PROBE over a FAIL.

PROOF 6: the checker output, pasted.


Hard boundaries (paper-specific; the wall + ONE-WRITER are probe's)
=============================================================================

- NEVER generate bibtex or touch `.bib`.
- NEVER fabricate numbers; NEVER create ad-hoc plots inline.
- NEVER edit manuscript prose. This worker transcribes into `### a-executor`; placing anything into the manuscript is REVISE's (`haipipe-paper-revise-place`).
- NO markdown tables in probe files or any probe document — bullet lines and `###` subsections only.
- NO inline search in the PROBE phase — the dispatch is the door.
  (DRAFT may WebSearch to orient; the difference is DURABILITY, not the search verb.)
- A stage skill that calls `Agent(haipipe-task-orchestrator-agent)` or an evidence agent ITSELF bypasses this contract — results land nowhere reviewable and die with the reply.


Return contract
===============

```
status:    ok | blocked
stage:     <stage-name>
probes:    PPNN <n> entries · T0/T1 <n> · T2 <n> · T3/T4 <n> dispatched
harvest:   <n> entries whose a-executor carries sources/values/display paths
next:      <suggested command>
```


Reference
=========

```
../../../../probe/haipipe-probe/SKILL.md   probe — the model. Read it.
ref/per-stage-dispatch.md                  per-stage routing · seed/claims/resource specifics
check-probe-cards.sh                       the VERIFY / stage-gate verifier (family-local)
```
