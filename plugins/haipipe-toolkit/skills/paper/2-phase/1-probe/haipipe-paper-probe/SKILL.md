---
name: haipipe-paper-probe
description: "PROBE-phase worker (internal). After DRAFT, collects the questions the draft raised into probe files — papers/<P>/1-probes/PPNN_<topic>.md, one file per topic, each question one SECTION (serves/target/state/q-executor/a-consumer) + a '## Why' that never leaves. Runs the five-step loop ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET; binds by PATH to a QA file in the task/discovery bank; dispatches the q-executor verbatim, never running bank work inline. Users invoke stage skills (seed, claims, pitch…), not this directly."
argument-hint: "[from-buffer <paper_root> [PPNN] | stage <stage-name>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
metadata:
  version: "5.0.0"
  last_updated: "2026-07-15"
  summary: "The paper's PROBE-phase worker — runs the five-step loop for a paper. The model (anatomy, QA contract, cost ladder, LAWS, states, checker codes) is the constitution's: ../../../../probe/haipipe-probe/SKILL.md. This file is only the paper-side deltas. History: ./CHANGELOG.md."
---

Skill: haipipe-paper-probe — the PROBE-phase worker for a paper
==============================================================

Called by paper stage skills (seed, resource, claims, pitch, narrative, display, section-edit) after DRAFT.
It runs the probe layer's five-step loop for a paper: collect the DRAFT's questions, bind each to an answer in the bank, harvest what comes back.

⭐ THE MODEL IS NOT THIS FILE'S — it is the constitution's: `../../../../probe/haipipe-probe/SKILL.md`.
Read it for the probe-file anatomy, the QA state-line contract, the cost ladder, the two LAWS, the derived states, and the checker's FAIL codes.
This file is ONLY how a paper runs the loop, plus the paper-side deltas the constitution does not cover.

Not user-facing: users invoke stage skills; a stage calls `Skill("haipipe-paper-probe", args="from-buffer <paper_root> [PPNN]")`.
Which stage runs which mode and lanes, seed/claims specifics, and section-edit logic: `ref/per-stage-dispatch.md`.

The paper-side deltas:
- `paper_root` vocabulary, and the paper's OWN registries (the T1 whitelist).
- the RESOURCE stage intake and write-back (paper only).
- the three harvest lanes as SUB-WORKER SKILLS (citation / values / display).


The five-step loop, paper-side
==============================

Each step ends with a PROOF this worker MUST show in its reply; an absent proof means the step did not happen.
STEP 0 — re-invoke this skill fresh every run, even when its text is already in context (a probe once ran a 3-hour-old contract).

TWO HALVES.
①–④ COLLECT the answer from the bank — the shared probe mechanism, per the constitution (question → answered QA file).
⑤ HARVESTS it — files the answer's artifacts into the paper's OWN registries.
Collection is the constitution's model; harvest is this worker's, and the constitution says nothing about it.


① ORGANIZE — collect the DRAFT's questions into probe files, grouped by TOPIC
----------------------------------------------------------------------------

- RESOURCE INTAKE (paper only; runs FIRST, and ONLY when the invoking stage is RESOURCE).
  Read `<paper_root>/0-lifecycle/1-resource/1-resource.md`.
  For every `Q<n>` that GATE 1 approved (present, not DECLINED in `_LOG_1-resource.md`) and carries NEITHER an `A:` NOR a `-> PP<NN>` backlink, open ONE section under `1-probes/` with `serves: resource` · `blocks: N<n>` (the Q's demand link, verbatim) · `target: NEW ?` · `state: planned`, and a `q-executor:` that re-poses the Q as a self-contained evidence question.
  Then write the backlink into 1-resource.md: `**Q<n> (N<n>) -> PP<NN>**` — that backlink is the mechanical proof the question was asked, and what `check-probe-cards.sh --stage resource` tests.
  The ownership chain: the STAGE asks (Q<n>) → the HUMAN approves at GATE 1 → this worker opens the section → ② resolves or ③ commissions it → the answer lands → ⑤ writes the A back into the Q.
  The stage never mints a PP id.
- Resolve `project_root`: walk UP from `paper_root` to the first ancestor containing `discoveries/`.
  Do NOT use `git rev-parse` — a repo-backed paper is its own git repo.
  (The checker resolves the same way.)
- Read the DRAFT's open questions: `{VAL:?}` slots, `GAP` markers, the stage's explicit questions (for claims: every GAP/weak claim).
- Group by TOPIC; write ONE probe file per topic at `<paper_root>/1-probes/PPNN_<topic>.md`, one SECTION per question, one `## Why` per file.
  Next free PP number is paper-local; `ls 1-probes/` is the authority.
- Write the `q-executor` here (the constitution's T1): a SEMANTIC strip — no claim/hypothesis labels, no stage words, no `## Why`, no hint of which answer is wanted.
  What crosses is a self-contained evidence question a stranger could answer.
  Frozen once written.
- Migrate a legacy `1-probe-plans/` or per-stage `_PROBE/` probe into `1-probes/` in the new shape on first touch only.

PROOF 1: `project_root=<path>` + `ls <project_root>/discoveries/` + `ls <paper_root>/1-probes/`.


② MATCH — LOCAL first (inline), then hand the BANK to the q-executor agent
-------------------------------------------------------------------------

The cost ladder T0-T4 is the constitution's. Split it by WHO can run each door — the paper-specific LOCAL doors stay here; the bank doors go to the shared agent.

LOCAL (inline — paper-specific, only the stage can run it):
- T1 LOCAL — a CLOSED whitelist of the paper's OWN registries: sibling/prior `_CITATION_*.md` · `_VALUES_*.md` · `_EVIDENCE_*.md` · sections already `read` · `0-displays/` units + index · the `.bib`.
  Fully answered → write the `a-consumer`, set `answered-local`, do NOT hand to the agent.
  Partially → narrow the q-executor to the remaining gap; only the gap goes to the agent.
  Adopt the POINTER, never the verdict: a reused value re-verifies against its ORIGINAL source at PLACE.
- DISPLAY-shaped needs are REROUTED, not collected (JL 2026-07-10): a question asking for a display unit that does not exist becomes a DR row in `0-lifecycle/4-display/_DISPLAY_REQUEST.md`; close the section `answered-local` with the `a-consumer` "rerouted to display stage: DRNN".

THE BANK (delegated — T2 REUSE + ③ DISPATCH + ④ POINT run in the agent's clean context):
- Collect the STILL-COLLECTING sections — state `planned` or `commissioned`, that LOCAL did not resolve — tag each with a route hint (`task | discovery`; you know the question's nature, so the agent never guesses), and hand the SET to the collector:

  ```text
  Agent(haipipe-probe-q-executor-agent, prompt="
    project_root: <from ①>
    probe_files:  <the PPNN files touched this run>
    collect:      <section ids still planned/commissioned>, each with route: task|discovery
  ")
  ```

  The agent runs the stake-free middle in ITS OWN context and returns `{ section → tier, target: QA-path | in-flight | failed }`, having already written each `target:`.
  It NEVER reads the paper's registries, the `## Why`, or the stake — its clean context IS the wall; and it never authors a fresh folder (the executor orchestrator picks it, LAW 1).
  The stage NEVER calls `haipipe-task-orchestrator-agent` / `haipipe-discovery-orchestrator-agent` ITSELF — the collector owns dispatch; a stage that dispatches inline lands results nowhere reviewable.

MOST SECTIONS SHOULD LAND ON T2 — the bank fills autonomously, so most answers exist before anyone asks.
A batch the agent returns as all-T3/T4 is a SMELL (lazy MATCH, or a starving bank) — say which, in the reply.
Reading anything BEYOND the QA corpus (opening `results/`, a plan.yaml, the code) is bank work and breaks LAW 1 — and it is the agent's corpus to read, not the stage's.

PROOF 2: the LOCAL hits (per T1-resolved section, the literal grep/ls line), and the agent's return block (per delegated section: tier + `target:`).


③ DISPATCH — owned by the collector agent, not the stage
--------------------------------------------------------

The agent you called in ② owns dispatch: it sends each MISS to `Agent(haipipe-task-orchestrator-agent)` / `Agent(haipipe-discovery-orchestrator-agent)`, the `q-executor` VERBATIM, `run_in_background` for fresh work, and omits the leaf for fresh (the orchestrator picks the folder and returns the path).
The stage NEVER calls an orchestrator itself — doing so bypasses this contract (results die with the reply).

DEFERRED / ASYNC is the agent's too: a section it cannot land synchronously comes back `in-flight` and stays `commissioned`; the NEXT PROBE run re-hands it to the agent, whose ② re-matches the now-`working`/`answered` QA file. This worker writes NOTHING under `tasks/` or `discoveries/`, ever — no stub, no mailbox.

PROOF 3: the agent's per-section dispatch / in-flight lines (from its return); NO `Agent(haipipe-task-orchestrator-agent)` call appears in THIS worker's own transcript.


④ POINT — the agent wrote `target:`; the stage VERIFIES it on disk
------------------------------------------------------------------

The agent already wrote each resolved section's `target:` (the FILE, never the folder). Before harvesting, VERIFY — do not trust the return blind (the state is the TARGET's state line, not the target's existence — open the file):
- `ls <project_root>/<target>` resolves, and `grep '^- state:' <target>` reads `answered` → ⑤.
- `working` → stays `commissioned`, report IN PROGRESS since `<started>` (dead past `QA_WORKING_TTL_HOURS` → re-hand to the agent next run).
- no QA-file path returned → `state: failed`, phase not green.
- a `commissioned` target that has since gone `answered` is a HARD FAIL (`commissioned-target-answered`) — harvest it now, do not wait for the eta.

PROOF 4: per section the `target:` line, the `ls` that resolves it, and `grep '^- state:' <target>`.

════════ COLLECTION (①–④) ends here — the answer is banked.
HARVEST (⑤) begins. ════════

⑤ INTERPRET — the a-consumer, the claim status, and HARVEST (the paper's own, not the constitution's)
-------------------------------------------------------------------------------------------------

- Write the `a-consumer` (translate the general answer UP into the paper's words).
  ONLY against an `answered`, non-superseded target (constitution).
- `mode: full` → the AUTHOR writes the claim status (`supported | refuted | inconclusive` + confidence + claim_type) into `0-lifecycle/1-claims/1-claims.md`, never in the probe file.
  A probe is communication, not judgment — there is no review gate; keep the `claim_type` overclaim check (never causal from associational evidence).
- RESOURCE WRITE-BACK (`serves: resource`): write the landed reading BACK into `1-resource.md` as the Q's `A:` line — existence AND fitness AND what it KILLS ("probably fine" is a DEFECT, not an answer).
  A BUILD-lane section writes `A: COMMISSIONED · owner <who> · eta YYYY-MM-DD · blocks N<n> · cross-project: <path|none-found>` at booking; the async path overwrites it on landing.
  Both receipts: the section is the probe-layer one, the Q's `A:` is what the human reads at GATE 2.
- LANE OBLIGATIONS — record the debt in the section FIRST (`values:`/`sources:`/`displays:` … `harvest: OWED`), then dispatch the lane's SUB-WORKER (`haipipe-paper-probe-citation` / `-values` / `-display`; cheap, pointer-following) and accept MECHANICALLY per `ref/harvest-acceptance.md` (run the greps, never eyeball).
  Flip to `harvest: accepted (<n>, <doc>)`.
  An `OWED` line at the gate FAILs.

PROOF 5: per section the `a-consumer` line, the claim-ledger diff (if it serves a claim), the `grep -A2 'Q<n>' 1-resource.md` for a resource write-back, and each harvester `Agent(...)` call + its acceptance-grep output.


VERIFY — the checker (the stage CHECK gate re-runs the same script)
------------------------------------------------------------------

```
sh <this-skill-dir>/check-probe-cards.sh <paper_root> [<project_root>] [--stage <key>]
```

`--stage resource` also runs the resource pass over 1-resource.md: every `Q<n>` must carry an `A:`, a `-> PP<NN>` backlink (to a probe file that EXISTS), or a DECLINED line — none of the three FAILs as `unasked-question`, and "no section serves stage resource" while questions are open FAILs as the VACUOUS GREEN.
The FAIL codes are the constitution's.
Never report a green PROBE over a FAIL.

PROOF 6: the checker output, pasted.


Hard boundaries (paper-specific; the wall + ONE-WRITER are the constitution's)
=============================================================================

- NEVER generate bibtex or touch `.bib`; `_CITATION_` is plain text only.
- NEVER fabricate numbers; NEVER create ad-hoc plots inline.
- NO markdown tables in probe files, `_CITATION_`, or any probe document — bullet lines and sections only.
- NO inline search in the PROBE phase — the dispatch is the door.
  (DRAFT may WebSearch to orient; the difference is DURABILITY, not the search verb.)
- A stage skill that calls `Agent(haipipe-task-orchestrator-agent)` or an evidence agent ITSELF bypasses this contract — results land nowhere reviewable and die with the reply.


Return contract
===============

```
status:    ok | blocked
stage:     <stage-name>
probes:    PPNN <n> sections · T0/T1 <n> · T2 <n> · T3/T4 <n> dispatched
lanes:     cite <status> │ val <status> │ disp <status>
next:      <suggested command>
```


Reference
=========

```
../../../../probe/haipipe-probe/SKILL.md   THE CONSTITUTION — the model. Read it.
ref/per-stage-dispatch.md                  stage→mode map · seed/claims specifics · section-edit
ref/harvest-acceptance.md                  lane dispatch + the LITERAL acceptance greps
check-probe-cards.sh                       the VERIFY / stage-gate verifier (family-local)
```
