---
name: haipipe-application-probe
description: "PROBE-phase worker (internal). After DRAFT, collects the questions the draft raised into probe files — applications/<A>/1-probes/PPNN_<topic>.md, one file per topic, each question one SECTION (serves/target/state/q-executor/a-consumer) + a '## Why' that never leaves. Runs the five-step loop ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET; binds by PATH to a QA file in the task/discovery bank; dispatches the q-executor verbatim, never running bank work inline. The three harvest lanes (values/citation/display) are venue-scaled HOOKS, not sub-skills. Users invoke stage skills (seed, claims…), not this directly."
argument-hint: "[from-buffer <intervention_root> [PPNN] | stage <stage-name>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
metadata:
  version: "3.0.0"
  last_updated: "2026-07-15"
  summary: "The intervention's PROBE-phase worker — runs the five-step loop for an application. The model (anatomy, QA contract, cost ladder, LAWS, states, checker codes) is the constitution's: ../../../../probe/haipipe-probe/SKILL.md. This file is only the application-side deltas: intervention_root, the DIKW-ladder rungs, and the venue-scaled harvest hooks. History: ./CHANGELOG.md."
---

Skill: haipipe-application-probe — the PROBE-phase worker for an application
============================================================================

Called by application stage skills (seed, descriptions, themes, claims, venue, pitch, narrative, display, section-edit) after DRAFT.
It runs the probe layer's five-step loop for an intervention: collect the DRAFT's questions, bind each to an answer in the bank, harvest what comes back.

⭐ THE MODEL IS NOT THIS FILE'S — it is the constitution's: `../../../../probe/haipipe-probe/SKILL.md`.
Read it for the probe-file anatomy, the QA state-line contract, the cost ladder, the two LAWS, the derived states, and the checker's FAIL codes.
This file is ONLY how an application runs the loop, plus the application-side deltas the constitution does not cover.

Not user-facing: users invoke stage skills; a stage calls `Skill("haipipe-application-probe", args="from-buffer <intervention_root> [PPNN]")`.
Which rung runs which mode and lanes, seed/claims specifics, and section-edit logic: `ref/per-stage-dispatch.md`.

The application-side deltas:
- `intervention_root` vocabulary, and the intervention's OWN registries (the T1 whitelist).
- the DIKW ladder rungs raise the questions (there is no resource stage; that is paper-only).
- the three harvest lanes as venue-scaled HOOKS (values / citation / display), not sub-worker skills.


The five-step loop, application-side
====================================

Each step ends with a PROOF this worker MUST show in its reply; an absent proof means the step did not happen.
STEP 0 — re-invoke this skill fresh every run, even when its text is already in context (a probe once ran a 3-hour-old contract).

TWO HALVES.
①–④ COLLECT the answer from the bank — the shared probe mechanism, per the constitution (question → answered QA file).
⑤ HARVESTS it — files the answer's artifacts into the intervention's OWN registries, scaled by the pinned venue.
Collection is the constitution's model; harvest is this worker's, and the constitution says nothing about it.


① ORGANIZE — collect the DRAFT's questions into probe files, grouped by TOPIC
----------------------------------------------------------------------------

- The stage's DRAFT wrote a `Q-consumer` section (the questions the stage raises); APPROVE is the human gate that picks which ones to pursue (constitution).
  A user-issued `probe run PPNN` (or "release PP02" / "release all") IS that approval for the named card(s); a bare `from-buffer` sweep with no named card STOPS, presents the approved-question roster, and awaits the pick.
- Only APPROVED questions go on: for each, open ONE SECTION under `1-probes/` with `serves: <stage/claim>` · `state: planned` · a `target:` still `NEW ?`, and write its `q-executor:` — the same question in general language, with the STAKE stripped out.
- Resolve `project_root`: walk UP from `intervention_root` to the first ancestor containing `discoveries/`.
  Do NOT use `git rev-parse` — a repo-backed project is its own git repo.
  (The checker resolves the same way.)
- Read the DRAFT's open questions: `{VAL:?}` slots, `GAP` markers, the rung's explicit questions (for claims: every GAP/weak claim).
- Group by TOPIC; write ONE probe file per topic at `<intervention_root>/1-probes/PPNN_<topic>.md`, one SECTION per question, one `## Why` per file.
  Next free PP number is intervention-local; `ls 1-probes/` is the authority.
- The `q-executor:` is a SEMANTIC strip — no claim/campaign labels, no stage words, no `## Why`, no hint of which answer is wanted.
  What crosses is a self-contained evidence question a stranger could answer, frozen once written.
- Migrate a legacy per-stage `_PROBE/` card or a `1-probe-plans/` entry into `1-probes/` in the new shape on first touch only.

PROOF 1: `project_root=<path>` + `ls <project_root>/discoveries/` + `ls <intervention_root>/1-probes/`.


② MATCH — LOCAL first (inline), then hand the BANK to the q-executor agent
-------------------------------------------------------------------------

The cost ladder T0–T4 is the constitution's. Split it by WHO can run each door — the intervention's LOCAL doors stay here; the bank doors go to the shared agent.

LOCAL (inline — intervention-specific, only the stage can run it):
- T1 LOCAL — a CLOSED whitelist of the intervention's OWN registries: sibling/prior `_CITATION_*.md` · `_VALUES_*.md` · `_DESCRIPTIONS/DS*.md` · sections already `read` · `0-artifacts/` display units · `1c-claims.md` campaign rows.
  Fully answered → write the `a-consumer`, set `answered-local`, do NOT hand to the agent.
  Partially → narrow the q-executor to the remaining gap; only the gap goes to the agent.
  Adopt the POINTER, never the verdict: a reused value re-verifies against its ORIGINAL source at harvest.
- DISPLAY-shaped needs are REROUTED, not collected: a question asking for a display unit that does not exist becomes a request row for the display stage; close the section `answered-local` with the `a-consumer` "rerouted to display stage".

THE BANK (delegated — T2 REUSE + ③ DISPATCH + ④ POINT run in the agent's clean context):
- Collect the STILL-COLLECTING sections — state `planned` or `commissioned`, that LOCAL did not resolve — tag each with a route hint (`task | discovery`), and hand the SET to the collector:

  ```text
  Agent(haipipe-probe-q-executor-agent, prompt="
    project_root: <from ①>
    probe_files:  <the PPNN files touched this run>
    collect:      <section ids still planned/commissioned>, each with route: task|discovery
  ")
  ```

  The agent runs the stake-free middle in ITS OWN context and returns `{ section → tier, target: QA-path | in-flight | failed }`, having already written each `target:`.
  It NEVER reads the intervention's registries, the `## Why`, or the stake — its clean context IS the wall; and it never authors a fresh folder (the executor orchestrator picks it, LAW 1).
  The stage NEVER calls `haipipe-task-orchestrator-agent` / `haipipe-discovery-orchestrator-agent` ITSELF — the collector owns dispatch; a stage that dispatches inline lands results nowhere reviewable.

MOST SECTIONS SHOULD LAND ON T2 — the bank fills autonomously, so most answers exist before anyone asks.
A batch the agent returns as all-T3/T4 is a SMELL (lazy MATCH, or a starving bank) — say which, in the reply.
Reading anything BEYOND the QA corpus (opening `results/`, a plan.yaml, the code) is bank work and breaks LAW 1.

PROOF 2: the LOCAL hits (per T1-resolved section, the literal grep/ls line), and the agent's return block (per delegated section: tier + `target:`).


③ DISPATCH — owned by the collector agent, not the stage
--------------------------------------------------------

The agent you called in ② owns dispatch: it sends each MISS to `Agent(haipipe-task-orchestrator-agent)` / `Agent(haipipe-discovery-orchestrator-agent)`, the `q-executor` VERBATIM, `run_in_background` for fresh work, and omits the leaf for fresh (the orchestrator picks the folder and returns the path).
The stage NEVER calls an orchestrator itself — doing so bypasses this contract (results die with the reply).

DEFERRED / ASYNC is the agent's too: a section it cannot land synchronously comes back `in-flight` and stays `commissioned`; the NEXT PROBE run re-hands it to the agent, whose ② re-matches the now-`working`/`answered` QA file.
This worker writes NOTHING under `tasks/` or `discoveries/`, ever — no stub, no mailbox.

PROOF 3: the agent's per-section dispatch / in-flight lines (from its return); NO orchestrator call appears in THIS worker's own transcript.


④ POINT — the agent wrote `target:`; the stage VERIFIES it on disk
------------------------------------------------------------------

The agent already wrote each resolved section's `target:` (the FILE, never the folder).
Before harvesting, VERIFY — do not trust the return blind (the state is the TARGET's state line, not the target's existence — open the file):
- `ls <project_root>/<target>` resolves, and `grep '^- state:' <target>` reads `answered` → ⑤.
- `working` → stays `commissioned`, report IN PROGRESS since `<started>` (dead past `QA_WORKING_TTL_HOURS` → re-hand to the agent next run).
- no QA-file path returned → `state: failed`, phase not green.
- a `commissioned` target that has since gone `answered` is a HARD FAIL (`commissioned-target-answered`) — harvest it now.

PROOF 4: per section the `target:` line, the `ls` that resolves it, and `grep '^- state:' <target>`.

════════ COLLECTION (①–④) ends here — the answer is banked.
HARVEST (⑤) begins. ════════

⑤ INTERPRET — the a-consumer, the claim status, and HARVEST (venue-scaled)
--------------------------------------------------------------------------

- Write the `a-consumer` (translate the general answer UP into the intervention's words).
  ONLY against an `answered`, non-superseded target (constitution).
- `mode: full` → the AUTHOR writes the claim status (`supported | refuted | inconclusive` + confidence) into `0-lifecycle/1c-claims/1c-claims.md`, flipping the C-line AND its Evidence Campaign row in the same pass — never in the probe file.
  A probe is communication, not judgment — there is no review gate; keep the overclaim check (never causal from associational evidence).
  The venue gate later reads THIS campaign against its settlement bar (light | medium | full).
- LANE OBLIGATIONS — record the debt in the section FIRST, then pay it.
  Which lanes fire is decided HERE, from the pinned venue (Venue-hook contract below):
  ```text
  - values:   tasks/X03_cohort_summary/results/summary.csv · harvest: OWED   (values lane, always)
  - sources:  S01,S02,S03 · harvest: OWED                                    (citation lane, sectioned venues)
  - displays: 0-artifacts/fig-overview · harvest: OWED                       (display lane, display-unit venues)
  ```
  Then dispatch the lane's HARVESTER HOOK as a cheap subagent (pointer-following only) and accept MECHANICALLY per `ref/harvest-acceptance.md` (run the greps, never eyeball).
  Flip to `harvest: accepted (<n>, <doc>)`.
  An `OWED` line at the gate FAILs.
- RUNG 1a REDIRECT (GROW loop): a descriptions-stage `values:` lane lands in `_DESCRIPTIONS/DS<n>_<name>.md` (per-dataset profile sheet), not `_VALUES_`; same OWED/accepted bookkeeping, different home — the 1a doc itself keeps one-line D entries.

PROOF 5: per section the `a-consumer` line, the claim-ledger diff (if it serves a claim), and each harvester `Agent(...)` call + its acceptance-grep output.


VERIFY — the checker (the stage CHECK gate re-runs the same script)
------------------------------------------------------------------

```
sh <this-skill-dir>/check-probe-cards.sh <intervention_root> [<project_root>]
```

Checks: read sections have resolving, non-`working`, non-superseded targets; planned sections FAIL (probe-not-run); commissioned sections carry owner/eta/blocks/cross-project with a future eta; `harvest: OWED` lane lines FAIL; dead vocabulary (`verdicted`, `## Verdict`) FAILs; no markdown tables in any probe file; the bank carries no consumer vocabulary (LAW 2).
The FAIL codes are the constitution's.
Never report a green PROBE over a FAIL.

PROOF 6: the checker output, pasted.


Venue-hook contract (application delta: hooks, not sub-worker skills)
=====================================================================

Application keeps NO probe sub-worker skills; the three HARVEST lanes are venue-scaled hooks inside this worker.
Which lanes fire is decided at lane CREATION (⑤ INTERPRET), from the pinned venue — the checker stays presence-driven and needs no venue lookup:

- `values:` — ALWAYS eligible: any venue's artifact quotes numbers, and claims-rung verified values land regardless of venue.
- `sources:` — SECTIONED venues only (report/dashboard-like). Pre-pin stages (seed and the venue-FREE 1a–1d ladder) keep source anchors in the section's `a-consumer`; no `_CITATION_` doc exists before a sectioned venue is pinned.
- `displays:` — only if the venue's artifact has display units (panels, charts, figures). Simple venues (sms/push/reminder) have no document lanes: their PROBE phase is claims-evidence only.

When a hook fires it follows paper's sub-worker contract (`haipipe-paper-probe-citation` / `-values` / `-display`): pointer-following + collector dispatch only, mechanical acceptance greps, no inline search.
The hook transcribes only what the return points at; finding is the bank's monopoly.
Card format specs are read from their single source of truth, never paraphrased into the dispatch prompt.


Hard boundaries (application-specific; the wall + ONE-WRITER are the constitution's)
====================================================================================

- `_CITATION_` is plain text only; no bibtex, ever.
- Numbers trace to a source; plots come from the display/task side, never inline.
- Probe files and working docs hold bullet SECTIONS, no markdown tables.
- The dispatch is the only door — a stage that calls an evidence agent itself lands results nowhere reviewable and dies with the reply.


Return contract
===============

```
status:    ok | blocked
stage:     <stage-name>
probes:    PPNN <n> sections · T0/T1 <n> · T2 <n> · T3/T4 <n> dispatched
lanes:     val <status> [· cite <status> · disp <status> — only lanes the venue fires]
next:      <suggested command>
```


Reference
=========

```
../../../../probe/haipipe-probe/SKILL.md   THE CONSTITUTION — the model. Read it.
ref/per-stage-dispatch.md                  rung→mode map · seed/claims specifics · venue-scaled lanes
ref/harvest-acceptance.md                  lane dispatch + the LITERAL acceptance greps
check-probe-cards.sh                       the VERIFY / stage-gate verifier (family-local fork)
../../../haipipe-application/fn/probes.md   buffer + release convention
```

Siblings: DRAFT (haipipe-application-draft) → PROBE (this) → REVISE (haipipe-application-revise) → CHECK (haipipe-application-check).
