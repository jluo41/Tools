---
name: haipipe-application-plan
description: "Planning specialist of the haipipe-application family. Given a research question, writes a structured plan-vN.yaml describing which D / I / K / W tasks are needed to answer it AND which probes (existing or new) must feed them. Used by /haipipe-application-ask at Phase 1. NO code, plan is markdown-yaml. Trigger: plan, /haipipe-application-plan, design synthesis, what tasks to run, plan-vN."
argument-hint: "[question] [--project <path>] [--revise <N>] [--feedback <text>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
  summary: "Planning specialist of the haipipe-application family."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-application-plan
=============================

Takes one research question, produces a **plan-vN.yaml** that lays out
the synthesis path: which D / I / K / W tasks would answer it, and
which probes must already be confirmed (or need to be triggered).

Used by `/haipipe-application-ask` at Phase 1. Can also run standalone.


Input
-----

- The question (text)
- Current insight base state (`insights/INDEX.md` + entries)
- Current probe state (`probes/<GROUP>_<group_slug>/<NN>_<slug>/probe.yaml`)


Output
------

```
examples/<project>/insights/sessions/plans/plan-v{N}-<slug>.yaml
```

`N` = next plan version for this question's session (revise increments).


Workflow
--------

```
Step 1: Parse args
  - <question>            required (unless --revise <N> with feedback)
  - --revise <N>          take plan-v{N-1}.yaml and rewrite based on
                          --feedback string
  - --feedback <text>     prior gate's revise feedback (verbatim copied
                          into the plan's "revise reason" field)

Step 2: Resolve project + read state
  - insight base summary (via /haipipe-insight-explore internally OR
    inline grep of insights/)
  - probes confirmed and ready

Step 3: Decompose question into phases
  - What D tasks (observations from which probes)?
  - What I tasks (which patterns to extract)?
  - What K tasks (which beliefs to elevate)?
  - What W tasks (which recommendations to derive)?

Step 4: Identify probe gaps
  - Does any planned D task require a probe not yet confirmed?
  - For each such gap: propose "trigger probe" (with proposed
    arms / claim_target). User decides via gate.

Step 5: Write plan-v{N}.yaml (atomic)
```


Plan schema (plan-v{N}.yaml)
------------------------------

DIKW is a card-labeling scheme, NOT a phase order. The plan output is
two related batches (tasks + probes) plus an `insight_yield` map
that says which DIKW cards each work item closes. Sessions do NOT
execute phase=D → phase=I → phase=K → phase=W in sequence.

```yaml
plan_version:     1
question:         "Does FiLM help on test-od?"
written_at:       <ISO>
status:           proposed | approved | superseded

# Existing KB scanned (what we already have)
existing_relevant:
  knowledge:      [K03]
  information:    [I02, I05]
  data:           [D01, D03]
  probes:    [P.A02 lhm_vs_baseline (confirmed),
              P.A04 film_test_id (confirmed)]

# Batch A — task work (produces D + I material)
task_batch:
  - id:        T1
    skill:     /haipipe-task eval
    type:      regression
    yields:    [D04, I06]
    notes:     "fit val / test-id / test-od; D = per-split stats,
                I = pattern across splits"
  - id:        T2
    skill:     /haipipe-task display
    type:      display
    yields:    [I07]
    refs:      [D04]
    notes:     "FiLM vs baseline test-od overlay plot"

# Batch B — probe work (produces K + W material)
probe_batch:
  - id:        P.A12
    skill:     /haipipe-probe plan
    new:       true
    arms:      [film_pm, baseline_pm]
    claim_target: "FiLM + param-matched yields X improvement on test-od"
    yields:    [K04, W03]
    needs:     [D04, I07]
    rationale: "K03 says FiLM not robust on test-od; need param-matched
                re-test to rule out scale confound"

# Archive — what DIKW cards insight will file at session end
insight_yield:
  D04: {layer: D, sources: [T1]}
  I06: {layer: I, sources: [T1]}
  I07: {layer: I, sources: [T2], refs: [D04]}
  K04: {layer: K, sources: [P.A12], refs: [I06, I07]}
  W03: {layer: W, sources: [P.A12], refs: [K04]}

# DAG — explicit blocking relationships
dag:
  - T1, T2 in parallel                # D04 + I06 + I07 obtained
  - P.A12 needs [D04, I07]            # then triggered
  - All yields filed → G-report

# Gate budget
gates:
  - id:         G-design
    threshold:  "all yields have a producer in task_batch or probe_batch"
  - id:         G-observe
    threshold:  "every D/I in insight_yield has artifact under tasks/.../results/"
  - id:         G-claim
    threshold:  "every K/W in insight_yield has probe.yaml.result.status == confirmed"
  - id:         G-report
    threshold:  "report.md cites the K/W in insight_yield; truly answers question"

# Revise history (filled by --revise)
revise_history:
  - version:    0
    feedback:   ""
    reason:     "initial plan"
```

Key invariants:

```
- yields is the contract — each id in yields must appear as a key
  in insight_yield.
- insight_yield key letter (D/I/K/W) MUST equal `layer` field.
- K/W cards MUST have at least one probe id in `sources`.
- D/I cards MUST have at least one task id in `sources`.
- Strategic W cards (sources = multiple K) are allowed; mark with
  `type: strategic` on the entry.
- dag never has K depending only on D (must pass through probe).
```


Definition of done
-------------------

- [ ] `applications/<kind>/<NN_slug>/plans/plan-v{N}.yaml` written, parses
- [ ] `task_batch` + `probe_batch` + `insight_yield` all populated
- [ ] Every id in any `yields:` list appears as key in `insight_yield`
- [ ] No K/W entry sources a task (must source a probe)
- [ ] dag respects layer-letter promotion rule
- [ ] On --revise: revise_history appended; feedback verbatim preserved


Risk profile
-------------

Writes one file under `insights/sessions/plans/`. Does NOT scaffold
tasks or probes — only proposes them. Actual scaffolding happens
in `/haipipe-application-ask` Phase 2 after gate approval.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "plan-v1 written for 'Does FiLM help on test-od?': 2 D, 1 I, 1 K, 1 W"
artifacts: [insights/sessions/plans/plan-v{N}-<slug>.yaml]
next:      gate review (in session context) OR direct user approval
```
