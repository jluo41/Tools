---
name: haipipe-application-probe
description: "Application-specific PROBE phase worker (internal). Owns the whole five-step loop from each stage Page Q-consumer through a neutral Q-executor and returned A-executor to the Page-facing A-consumer. The persisted Probe file uses the existing QX schema, binds by path to a QA file in the task/discovery bank, and dispatches only the Q-executor. DRAFT raises questions and stops. Users invoke stage skills, not this directly."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
metadata:
  argument_hint: "[from-buffer <intervention_root> [PPNN] | stage <stage-name>]"
  version: "0.3.3"
  last_updated: "2026-08-04"
  summary: "Application-specific PROBE worker layered on haipipe-board-page-probe and haipipe-probe; it runs all five steps because DRAFT authors no executor-side field."
---

Skill: haipipe-application-probe — the PROBE-phase worker for an application
============================================================================

Called by application stage skills (seed, descriptions, themes, claims, venue, pitch, narrative, display, section-edit) after DRAFT.
DRAFT raised the Q-consumer questions in the stage doc and stopped there. THIS worker owns everything probe-shaped: ①ORGANIZE each Q-consumer into an ENTRY, ②MATCH it against the bank (read-only grep), ③DISPATCH only what the ceiling allows, ④POINT, ⑤INTERPRET.

**LOAD THE PAGE LAYERS FIRST:** `../../../../board/page-types/haipipe-board-page-for-stage/SKILL.md`, then `../../../../board/page-phases/haipipe-board-page-probe/SKILL.md`, then `../../../../probe/haipipe-probe/SKILL.md`.
The persisted QX file is the application's Probe file.
Older code may call the record an entry, but that label is not another Page Type or phase.

⭐ THE MODEL IS NOT THIS FILE'S — it is `probe`'s: `../../../../probe/haipipe-probe/SKILL.md`.
Read it for the probe-file anatomy, the QA state-line contract, the cost ladder, the two LAWS, the derived states, and the checker's FAIL codes.
This file is ONLY how an application runs the loop, plus the application-side deltas `probe` does not cover.

Not user-facing: users invoke stage skills; a stage calls `Skill("haipipe-application-probe", args="from-buffer <intervention_root> [PPNN]")`.
Which rung runs which lanes, seed/claims specifics, and section-edit logic: `ref/per-stage-dispatch.md`.

The application-side deltas:
- `intervention_root` vocabulary, and the intervention's OWN registries (the T1 whitelist).
- the DIKW ladder rungs raise the questions (there is no resource stage; that is paper-only).
- harvest folds into the entry's `### a-executor` — no sidecar docs, no lanes (application delta).


Rules (follow these — the model is `probe`'s)
==============================================

The PROBE-phase rules live in `../../../../probe/haipipe-probe/SKILL.md` → **Phase rules · PROBE phase** (+ **The QA file**, **The two LAWS**). Follow those; on conflict, that file wins. Application-specific additions:
- Dispatch goes through the collector agent (`haipipe-probe-q-executor-agent`), NEVER an orchestrator called inline by this worker — results would die with the reply.
- Harvest folds into the entry's `### a-executor` — the answer's numbers/citations land INLINE there, anchored to `target:`; no sidecar docs, no `values:`/`sources:`/`displays:` lanes (application delta). See `ref/harvest-acceptance.md`.
- A claim's STATUS goes in `0-lifecycle/1c-claims/1c-claims.md`, written by the AUTHOR, NEVER in the probe file.
- No bibtex; no ad-hoc plots; no markdown tables in any probe document.

The loop below is the HOW-TO for these rules.


The loop, application-side — this worker runs ① through ⑤
==========================================================

Each step ends with a PROOF this worker MUST show in its reply; an absent proof means the step did not happen.
STEP 0 — re-invoke this skill fresh every run, even when its text is already in context (a probe once ran a 3-hour-old contract).

THE PHASE SPLIT (`probe`).
①ORGANIZE + ②MATCH happen HERE. Read the stage doc's Q-consumer and author each ENTRY: `### q-executor` (stake stripped, then FROZEN, + Deliverable/Accepted), `### q-consumer` bullets, `### bank binding` (`route`, `bank`, `target` — an existing path or `NEW <path>`). DRAFT authors none of it and never opens `1-probes/`.
This worker runs ③DISPATCH + ④POINT (COLLECT the answer from the bank, per `probe`) + ⑤INTERPRET (HARVEST it — write `### a-executor` and the stage-doc a-consumer). Collection is `probe`'s model; harvest is this worker's, and `probe` says nothing about it.


① + ② — ORGANIZE AND MATCH HERE
--------------------------------

Read the stage Page's Q-consumers, then find or create the persisted Probe files under `<intervention_root>/1-probes/PPNN_<topic>/`.
This worker writes the neutral Q-executor, audit copy, route, bank verdict, and target plan, then performs the read-only match.
DRAFT authored none of those fields.
- Resolve `project_root`: walk UP from `intervention_root` to the first ancestor containing `discoveries/`.
  Do NOT use `git rev-parse` — a repo-backed project is its own git repo. (The checker resolves the same way.)
- Read each entry's `### bank binding` (`bank` + `target`) to route it: an existing `target:` path (bank `reuse`) → the answer may already be banked, go to ④/⑤ (verify then harvest); `target: NEW …` (bank `run`/`code`/`new`) → ③ DISPATCH.
- T1 LOCAL still runs inline (application-specific): a CLOSED whitelist of the intervention's OWN registries — entries already `read` (their `### a-executor`) · `0-artifacts/` display units · `1c-claims.md` campaign rows.
  Fully answered there → write `### a-executor`, set `answered-local`, do NOT dispatch. Adopt the POINTER, never the verdict (a reused value re-verifies against its ORIGINAL source at harvest).
- DISPLAY-shaped needs are REROUTED, not collected: a question asking for a display unit that does not exist becomes a request row for the display stage; close the entry `answered-local` with `### a-executor` "rerouted to display stage".

PROOF 1: `project_root=<path>` + `ls <project_root>/discoveries/` + `ls <intervention_root>/1-probes/`, and per entry its `bank` verdict + `target:` (existing→④/⑤ or NEW→③).


③ DISPATCH — hand the NEW entries to the collector agent
--------------------------------------------------------

For each STILL-COLLECTING entry (`target: NEW`, bank `run`/`code`/`new`, not resolved by T1 LOCAL), hand the SET to the collector agent, tagging each with the PROBE-authored `route:` (task|discovery — AUTHORITATIVE, not a hint):

  ```text
  Agent(haipipe-probe-q-executor-agent, prompt="
    project_root: <from ①>
    probe_files:  <the PPNN files touched this run>
    dispatch:     <entry ids with target: NEW>, each with its route: task|discovery
  ")
  ```

The agent runs the stake-free middle in ITS OWN clean context: it sends each `### q-executor` VERBATIM to `Agent(haipipe-task-orchestrator-agent)` / `Agent(haipipe-discovery-orchestrator-agent)` (`run_in_background` for fresh work; omit the leaf for fresh — the orchestrator picks the folder and returns the path), and returns `{ entry → target: QA-path | in-flight | failed }`, having written each `target:`.
The agent does NOT re-run ②MATCH — the DRAFT `bank`/`target` already rooted each question; the agent DISPATCHES (the executor orchestrator's OWN QA-gate still dedups against an existing answer). It NEVER reads the intervention's registries, the stake, or the stage-doc Q-consumers — its clean context IS the wall; and it never authors a fresh folder (LAW 1).
The stage NEVER calls `haipipe-task-orchestrator-agent` / `haipipe-discovery-orchestrator-agent` ITSELF — the collector owns dispatch; a stage that dispatches inline lands results nowhere reviewable.

DEFERRED / ASYNC is the agent's too: an entry it cannot land synchronously comes back `in-flight` and stays `commissioned`; the NEXT PROBE run re-hands it. This worker writes NOTHING under `tasks/` or `discoveries/`, ever — no stub, no mailbox.

PROOF 3: the agent's per-entry dispatch / in-flight lines (from its return); NO orchestrator call appears in THIS worker's own transcript.


④ POINT — the agent wrote `target:`; the stage VERIFIES it on disk
------------------------------------------------------------------

The agent already wrote each resolved entry's `target:` (the FILE, never the folder). Before harvesting, VERIFY — do not trust the return blind (the state is the TARGET's state line, not the target's existence — open the file):
- `ls <project_root>/<target>` resolves, and `grep '^- state:' <target>` reads `answered` → ⑤.
- `working` → stays `commissioned`, report IN PROGRESS since `<started>` (dead past `QA_WORKING_TTL_HOURS` → re-hand to the agent next run).
- no QA-file path returned → `state: failed`, phase not green.
- a `commissioned` target that has since gone `answered` is a HARD FAIL (`commissioned-target-answered`) — harvest it now.

PROOF 4: per entry the `target:` line, the `ls` that resolves it, and `grep '^- state:' <target>`.

════════ COLLECTION (①–④) ends here — the answer is banked.
HARVEST (⑤) begins. ════════

⑤ INTERPRET — the a-executor, the stage-doc a-consumer, and the claim status
----------------------------------------------------------------------------

- Write `### a-executor` — a COPY of the answering QA file's answer, ONLY against an `answered`, non-superseded target (`probe`).
  HARVEST folds in here: write the answer's numbers / citations INLINE, each with its anchor `<value>  [→ <the entry's target QA file>]`.
  `target:` is already verified `answered` + non-superseded — that IS the fabrication anchor. No second transcription, no `values:`/`sources:`/`displays:` lane, no sidecar doc.
- Each Q-consumer this entry serves then writes its OWN a-consumer in its stage doc (station ②), anchored `[source: PP<NN>]` back to the `### a-executor` copy — the per-consumer interpretation UP into the intervention's words.
- The AUTHOR writes the claim status (`supported | refuted | inconclusive` + confidence) into `0-lifecycle/1c-claims/1c-claims.md`, flipping the C-line AND its Evidence Campaign row in the same pass — never in the probe file.
  A probe is communication, not judgment — there is no review gate; keep the overclaim check (never causal from associational evidence).
  The venue gate later reads THIS campaign against its settlement bar (light | medium | full).
- A display unit a question needs but that does not exist REROUTES to the display stage (a request row); do not invent an artifact here.
  Details: `ref/harvest-acceptance.md`.

PROOF 5: per entry the `### a-executor` line (with its inline `[→ target]` anchor), the stage-doc a-consumer it feeds, and the claim-ledger diff (if it serves a claim).


VERIFY — the checker (the stage CHECK gate re-runs the same script)
------------------------------------------------------------------

```
sh <this-skill-dir>/check-probe-cards.sh <intervention_root> [<project_root>]
```

Checks: `read` entries have resolving, non-`working`, non-superseded targets; `planned` entries FAIL (probe-not-run); `commissioned` entries carry owner/eta/blocks/cross-project with a future eta; dead vocabulary FAILs; no markdown tables in any probe file; the bank carries no consumer vocabulary (LAW 2).
The FAIL codes are `probe`'s.
Never report a green PROBE over a FAIL.

PROOF 6: the checker output, pasted.


Harvest — no sidecar (application delta)
========================================

Application keeps NO probe sub-worker skills and NO harvest sidecar docs.
Every answer's numbers / citations land INLINE in the entry's `### a-executor`, anchored to `target:`
(the answering QA file, already verified). No `values:`/`sources:`/`displays:` lanes, and no sidecar docs.
Finding stays the bank's monopoly; this worker transcribes only what the entry's `target:` already points at. Details: `ref/harvest-acceptance.md`.


Hard boundaries (application-specific; the wall + ONE-WRITER belong to `probe`)
====================================================================================

- Citations land inline in `### a-executor` — plain text, no bibtex, anchored to the source.
- Numbers trace to a source; plots come from the display/task side, never inline.
- Probe files hold `## QX<n>` entries with `###` subsections, no markdown tables.
- The dispatch is the only door — a stage that calls an evidence agent itself lands results nowhere reviewable and dies with the reply.


Return contract
===============

```
status:    ok | blocked
stage:     <stage-name>
probes:    PPNN <n> entries · T0/T1 <n> · T2 <n> · T3/T4 <n> dispatched
next:      <suggested command>
```


Reference
=========

```
../../../../probe/haipipe-probe/SKILL.md   probe — the model. Read it.
ref/per-stage-dispatch.md                  rung→lane map · seed/claims specifics · venue-scaled lanes
ref/harvest-acceptance.md                  no-sidecar harvest: write into a-executor, anchored to target
check-probe-cards.sh                       the VERIFY / stage-gate verifier (family-local fork)
../../../haipipe-application/fn/probes.md   buffer + release convention
```

Siblings: DRAFT (haipipe-application-draft) → PROBE (this) → REVISE (haipipe-application-revise) → CHECK (haipipe-application-check).
