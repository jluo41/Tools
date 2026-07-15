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

TWO HALVES. ①–④ COLLECT the answer from the bank — the shared probe mechanism, per the constitution (question → answered QA file). ⑤ HARVESTS it — files the answer's artifacts into the paper's OWN registries. Collection is the constitution's model; harvest is this worker's, and the constitution says nothing about it.


① ORGANIZE — collect the DRAFT's questions into probe files, grouped by TOPIC
----------------------------------------------------------------------------

- RESOURCE INTAKE (paper only; runs FIRST, and ONLY when the invoking stage is RESOURCE).
  Read `<paper_root>/0-lifecycle/1-resource/1-resource.md`.
  For every `Q<n>` that GATE 1 approved (present, not DECLINED in `_LOG_1-resource.md`) and carries NEITHER an `A:` NOR a `-> PP<NN>` backlink, open ONE section under `1-probes/` with `serves: resource` · `blocks: N<n>` (the Q's demand link, verbatim) · `target: NEW ?` · `state: planned`, and a `q-executor:` that re-poses the Q as a self-contained evidence question.
  Then write the backlink into 1-resource.md: `**Q<n> (N<n>) -> PP<NN>**` — that backlink is the mechanical proof the question was asked, and what `check-probe-cards.sh --stage resource` tests.
  The ownership chain: the STAGE asks (Q<n>) → the HUMAN approves at GATE 1 → this worker opens the section → ② resolves or ③ commissions it → the answer lands → ⑤ writes the A back into the Q. The stage never mints a PP id.
- Resolve `project_root`: walk UP from `paper_root` to the first ancestor containing `discoveries/`. Do NOT use `git rev-parse` — a repo-backed paper is its own git repo. (The checker resolves the same way.)
- Read the DRAFT's open questions: `{VAL:?}` slots, `GAP` markers, the stage's explicit questions (for claims: every GAP/weak claim).
- Group by TOPIC; write ONE probe file per topic at `<paper_root>/1-probes/PPNN_<topic>.md`, one SECTION per question, one `## Why` per file. Next free PP number is paper-local; `ls 1-probes/` is the authority.
- Write the `q-executor` here (the constitution's T1): a SEMANTIC strip — no claim/hypothesis labels, no stage words, no `## Why`, no hint of which answer is wanted. What crosses is a self-contained evidence question a stranger could answer. Frozen once written.
- Migrate a legacy `1-probe-plans/` or per-stage `_PROBE/` probe into `1-probes/` in the new shape on first touch only.

PROOF 1: `project_root=<path>` + `ls <project_root>/discoveries/` + `ls <paper_root>/1-probes/`.


② MATCH — per question, cheapest door first (the cost ladder T0-T4 is the constitution's)
----------------------------------------------------------------------------------------

Paper-side specifics:
- T1 LOCAL — a CLOSED whitelist of the paper's OWN registries: sibling/prior `_CITATION_*.md` · `_VALUES_*.md` · `_EVIDENCE_*.md` · sections already `read` · `0-displays/` units + index · the `.bib`.
  Fully answered → write the `a-consumer`, set `answered-local`, do NOT dispatch. Partially → narrow the q-executor to the remaining gap and dispatch that. Adopt the POINTER, never the verdict: a reused value re-verifies against its ORIGINAL source at PLACE.
- T2 REUSE — `grep -rl "<terms>" <project_root>/{tasks,discoveries}/**/QA/*.md`, then READ the hits and branch on the state line (constitution). May call the qa verb in CHECK-ONLY mode (`/haipipe-task qa "<q>" --check-only`): it detects ①/② and runs nothing.
- DISPLAY-shaped needs are REROUTED, not dispatched (JL 2026-07-10): a question asking for a display unit that does not exist becomes a DR row in `0-lifecycle/4-display/_DISPLAY_REQUEST.md`; close the section `answered-local` with the `a-consumer` "rerouted to display stage: DRNN".
- Reading anything BEYOND the QA corpus (opening `results/`, a plan.yaml, the code) is bank work and breaks LAW 1. The QA corpus is a readable index the executor published FOR readers; that is why reading it is allowed.

MOST SECTIONS SHOULD LAND ON T2 — the bank fills autonomously, so most answers exist before anyone asks. A probe file whose every section is T3/T4 is a SMELL (lazy MATCH, or a starving bank) — say which, in the reply.

PROOF 2: per question the tier (T0-T4), and for T1/T2 the literal grep/ls hit lines (for T2, the QA file path READ **and its `- state:` line**).


③ DISPATCH — the q-executor goes, VERBATIM, to the executor orchestrator
-----------------------------------------------------------------------

One call per open question (batch independent ones). The keys are the orchestrators' OWN input spelling — a prompt matching none of their declared forms is undefined behaviour:

```text
Agent(haipipe-task-orchestrator-agent, run_in_background=<true for fresh>, prompt="
  action: qa
  project: <project_root, from ①>
  question: |
    <the section's `q-executor:` block, VERBATIM. Nothing else.>
  leaf: <the section's target: — an existing task-folder path, `NEW <path>`, or omit if unknown>
")
```

…or `Agent(haipipe-discovery-orchestrator-agent, ...)` for discovery-shaped work (literature, prior art, landscape). Their clean context IS the wall; they pick shape and depth and return a PATH.
- Likely-fresh work dispatches `run_in_background=true` (a sync fresh run froze a session 25 minutes); ④ runs when it returns. If `<project_root>/discoveries/` is empty, EVERY question is T4 — background them all. Report a dispatch as background only if the call actually carried the flag.
- DEFERRED DISPATCH (no agent): for a long build, leave the section `commissioned` with its BUILD-lane fields (owner/eta/blocks/cross-project) and STOP — the `q-executor` block IS the durable order; a later `/haipipe-task qa` session picks it up and a later PROBE re-run harvests it. This worker writes NOTHING project-side, ever — no stub, no mailbox.

PROOF 3: per question the literal `Agent(...)` call, or (deferred) the `commissioned` block showing owner/eta/blocks/cross-project.


④ POINT — the section's `target:` → the answering QA FILE
--------------------------------------------------------

Write the returned PATH into `target:` (the FILE, never the folder) and verify with `ls <project_root>/<target>`. A return with no QA-file path means the evidence never landed → `state: failed`, phase not green.
The section's state is the TARGET'S state line, not the target's existence (constitution) — open the file.

ASYNC PATH (MANDATORY). A `commissioned` section from an earlier session has no live return: on every run, re-resolve its `target:`, `ls` the QA file, READ its state line. `answered` → ⑤. `working` → stays `commissioned`, report IN PROGRESS since `<started>` (dead past `QA_WORKING_TTL_HOURS` → re-dispatch ③). A `commissioned` target that has since gone `answered` is a HARD FAIL (`commissioned-target-answered`) — harvest it now, do not wait for the eta.

PROOF 4: per question the `target:` line, the `ls` that resolves it, and `grep '^- state:' <target>`.

════════ COLLECTION (①–④) ends here — the answer is banked. HARVEST (⑤) begins. ════════

⑤ INTERPRET — the a-consumer, the claim status, and HARVEST (the paper's own, not the constitution's)
-------------------------------------------------------------------------------------------------

- Write the `a-consumer` (translate the general answer UP into the paper's words). ONLY against an `answered`, non-superseded target (constitution).
- `mode: full` → the AUTHOR writes the claim status (`supported | refuted | inconclusive` + confidence + claim_type) into `0-lifecycle/1-claims/1-claims.md`, never in the probe file. A probe is communication, not judgment — there is no review gate; keep the `claim_type` overclaim check (never causal from associational evidence).
- RESOURCE WRITE-BACK (`serves: resource`): write the landed reading BACK into `1-resource.md` as the Q's `A:` line — existence AND fitness AND what it KILLS ("probably fine" is a DEFECT, not an answer). A BUILD-lane section writes `A: COMMISSIONED · owner <who> · eta YYYY-MM-DD · blocks N<n> · cross-project: <path|none-found>` at booking; the async path overwrites it on landing. Both receipts: the section is the probe-layer one, the Q's `A:` is what the human reads at GATE 2.
- LANE OBLIGATIONS — record the debt in the section FIRST (`values:`/`sources:`/`displays:` … `harvest: OWED`), then dispatch the lane's SUB-WORKER (`haipipe-paper-probe-citation` / `-values` / `-display`; cheap, pointer-following) and accept MECHANICALLY per `ref/harvest-acceptance.md` (run the greps, never eyeball). Flip to `harvest: accepted (<n>, <doc>)`. An `OWED` line at the gate FAILs.

PROOF 5: per section the `a-consumer` line, the claim-ledger diff (if it serves a claim), the `grep -A2 'Q<n>' 1-resource.md` for a resource write-back, and each harvester `Agent(...)` call + its acceptance-grep output.


VERIFY — the checker (the stage CHECK gate re-runs the same script)
------------------------------------------------------------------

```
sh <this-skill-dir>/check-probe-cards.sh <paper_root> [<project_root>] [--stage <key>]
```

`--stage resource` also runs the resource pass over 1-resource.md: every `Q<n>` must carry an `A:`, a `-> PP<NN>` backlink (to a probe file that EXISTS), or a DECLINED line — none of the three FAILs as `unasked-question`, and "no section serves stage resource" while questions are open FAILs as the VACUOUS GREEN. The FAIL codes are the constitution's. Never report a green PROBE over a FAIL.

PROOF 6: the checker output, pasted.


Hard boundaries (paper-specific; the wall + ONE-WRITER are the constitution's)
=============================================================================

- NEVER generate bibtex or touch `.bib`; `_CITATION_` is plain text only.
- NEVER fabricate numbers; NEVER create ad-hoc plots inline.
- NO markdown tables in probe files, `_CITATION_`, or any probe document — bullet lines and sections only.
- NO inline search in the PROBE phase — the dispatch is the door. (DRAFT may WebSearch to orient; the difference is DURABILITY, not the search verb.)
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
