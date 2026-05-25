---
name: haipipe-application-ask
description: "Question-driven workflow of the haipipe-application family. Takes one research question, scans the existing insight base for an answer, optionally triggers new experiments via haipipe-experiment when knowledge is missing, then runs D → I → K → W synthesis to update the project's insights/. Can call /haipipe-experiment (design + bridge) to materialize new arms when needed. Use when the user asks a research question that may or may not be answerable from existing knowledge. Trigger: ask, insight session, /haipipe-application-ask, question-driven analysis."
argument-hint: [question] [--project <path>] [--rounds N] [--auto]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Task
---

Skill: haipipe-application-ask
===============================

The **question driver**. Takes one research question and orchestrates
its resolution end-to-end: scan existing insights → trigger experiments
if needed → synthesize new insights → answer.

This is the only skill in the haipipe-application family that can call
**outside** E_insight (specifically: /haipipe-experiment to scaffold
new arms). All other haipipe-insight-* skills are pure markdown
synthesizers.


Mirror of D_experiment's loop, at a different level
---------------------------------------------------

```
/haipipe-experiment loop <ID>     iterates ONE experiment thread until claim ✅
/haipipe-application-ask <question>  iterates ACROSS threads until question answered
```


Phases
------

```
Phase 0 — SCAN INSIGHTS
  Read examples/<project>/insights/INDEX.md + relevant K/I entries.
  Does the existing knowledge base already answer the question?
    yes  → emit answer, end (with citation trail)
    no   → continue to Phase 1
    partial → present what we know; ask user: dig deeper or accept?

Phase 1 — PLAN
  Skill("haipipe-application-plan", args="<question> --project <path>")
  → writes a plan-vN.yaml describing what D / I / K / W tasks would
    answer the question, AND which experiments (existing or new) are
    needed as inputs.

Phase 2 — EXPERIMENT (conditional)
  If plan requires experiments NOT yet confirmed:
    For each missing experiment:
      Skill("haipipe-experiment-design", args="new <new_ID> --auto")
      Skill("haipipe-experiment-bridge",  args="<new_ID>")
        → bridge invokes Run Script Reviewer, sanity, deploy, link
      Wait for result.status to flip to confirmed.

  If plan can be served by existing confirmed experiments:
    skip to Phase 3.

Phase 3 — D-PHASE  (Observations)
  For each planned D task:
    Skill("haipipe-insight-data", args="<exp_id>")
  → writes insights/D_observations/O{NN}_*.md

  Gate: Skill("haipipe-application-gate", args="D")
    revise → back to Phase 1 with feedback
    approve → continue

Phase 4 — I-PHASE  (Patterns)
  Skill("haipipe-insight-information", args="--scope <O*>")
  → writes insights/I_patterns/P{NN}_*.md

  Gate: revise / approve

Phase 5 — K-PHASE  (Knowledge)
  Skill("haipipe-insight-knowledge", args="--scope <P*>")
  → writes insights/K_knowledge/K{NN}_*.md (may update existing K entries)

  Gate: revise / approve

Phase 6 — W-PHASE  (Wisdom)
  Skill("haipipe-insight-wisdom", args="--scope <K*>")
  → writes insights/W_wisdom/W{NN}_*.md
    (typically a "do this next" recommendation)

  Gate: revise / approve

Phase 7 — LOG SESSION
  Append a Q&A record to insights/sessions/<DATE>_<slug>.md:
    - question, scanned_entries, new_experiments, new/updated insights,
      final answer, git_sha.
  The new K/W entries written in earlier phases ARE the structured answer;
  the sessions/ log is the lightweight Q&A record pointing to them.
  (External-facing report / message / UI synthesis is NOT done here —
   route to /haipipe-application instead.)
```


Commands
--------

```
/haipipe-application-ask <question>
  Full flow starting from Phase 0.

/haipipe-application-ask continue
  Resume the last in-progress session (state in insights/sessions/_active.yaml).

/haipipe-application-ask status
  Print last session's phase + outstanding gate.
```


Constants
---------

```
AUTO_MODE        --auto         Skip all gate ASK prompts; accept gate
                                proposals verbatim. Same semantics as
                                haipipe-task's AUTO_MODE.
MAX_EXPERIMENTS  default 3      Cap on new experiments triggered per session.
                                Exceeding asks user to confirm continuation.
MAX_ROUNDS       default 4      Cap on revise→re-plan cycles before STOP.
```


Stop conditions
---------------

```
✅ answered       Phase 0 found existing answer, OR full pipeline produced one
🟡 budget        MAX_EXPERIMENTS or MAX_ROUNDS hit
🔴 blocked       gate rejected and user has no path forward
🛑 paused        user invoked /haipipe-application-ask pause
```


Session log file
-----------------

```
examples/<project>/insights/sessions/<YYYY-MM-DD>_<slug>.md

# Q01: <question one-liner>

- question:           "<full question>"
- asked_at:           <ISO>
- scanned_entries:    [K03, I02, ...]
- new_experiments:    [12_param_matched_film, ...]    (or [] if none)
- new_or_updated:     [O05 created, K03 updated, ...]
- final_answer:       "<one-paragraph>"
- citation_trail:     [K03 → I02 → O05, O07]
- git_sha:            <sha of HEAD when session completed>
- duration:           <wallclock>
```


Boundary
--------

```
haipipe-application-ask    bridges INSIGHT base ↔ EXPERIMENT base via /haipipe-experiment
haipipe-experiment-loop    iterates ONE experiment thread
haipipe-experiment-bridge  scaffolds tasks for ONE experiment

Session NEVER writes tasks/ directly — it always goes through
/haipipe-experiment to keep the one-way dependency (experiments → tasks)
clean.
```


Risk profile
-------------

WRITES heavily to insights/. May TRIGGER:
- New experiments via Skill("haipipe-experiment-design new" + "bridge")
  → these in turn scaffold tasks under tasks/ and run GPU jobs
- Existing K/W entries may be UPDATED (rewriting); D / I / P entries
  are append-only

Calls external LLM (Codex MCP) indirectly via experiment-bridge's
Run Script Reviewer and review-claim. Budget accordingly via
MAX_EXPERIMENTS.


Specialist tail
---------------

```
status:    ok | blocked | failed | answered | budget | paused
summary:   "Q01 answered via K03 (existing) + new experiment 12"
artifacts: [insights/sessions/<DATE>_<slug>.md,
            insights/D_observations/O*.md (new),
            insights/I_patterns/P*.md (new),
            insights/K_knowledge/K*.md (new/updated),
            insights/W_wisdom/W*.md (if any),
            experiments/<NN>_<slug>/ (if new experiments scaffolded)]
next:      review final K/W + sessions/<DATE>.md log; if an external
           artifact (message/ui/report) is wanted, /haipipe-application
```
