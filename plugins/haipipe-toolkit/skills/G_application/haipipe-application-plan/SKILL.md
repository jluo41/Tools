---
name: haipipe-application-plan
description: "Planning specialist of the haipipe-application family. Given a research question, writes a structured plan-vN.yaml describing which D / I / K / W tasks are needed to answer it AND which experiments (existing or new) must feed them. Used by /haipipe-application-ask at Phase 1. NO code, plan is markdown-yaml. Trigger: plan, /haipipe-application-plan, design synthesis, what tasks to run, plan-vN."
argument-hint: [question] [--project <path>] [--revise <N>] [--feedback <text>]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-application-plan
=============================

Two modes.

Mode 1 — **plan** (Phase 1): takes one research question, produces a
**plan-vN.yaml** that lays out the synthesis path: which D / I / K / W
tasks would answer it, and which experiments must already be
confirmed (or need to be triggered).

Mode 2 — **compose report** (Phase 4): reads SESSION_STATE.json +
the filed insight cards and writes the final `report.md` following
the DIKW-spine template at `../haipipe-application/ref/report-template.md`.
Invoked as `Skill("haipipe-application-plan", args="compose report")`.
See "Compose report mode" section below.

Used by `/haipipe-application-ask` at Phases 1 and 4. Can also run
standalone.


Input
-----

- The question (text)
- Current insight base state (`insights/INDEX.md` + entries)
- Current experiment state (`experiments/<NN>_<slug>/experiment.yaml`)


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
  - experiments confirmed and ready

Step 3: Decompose question into phases
  - What D tasks (observations from which experiments)?
  - What I tasks (which patterns to extract)?
  - What K tasks (which beliefs to elevate)?
  - What W tasks (which recommendations to derive)?

Step 4: Identify experiment gaps
  - Does any planned D task require an experiment not yet confirmed?
  - For each such gap: propose "trigger experiment" (with proposed
    arms / claim_target). User decides via gate.

Step 5: Write plan-v{N}.yaml (atomic)
```


Plan schema (plan-v{N}.yaml)
------------------------------

DIKW is a card-labeling scheme, NOT a phase order. The plan output is
two related batches (tasks + experiments) plus an `insight_yield` map
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
  experiments:    [02_lhm_vs_baseline (confirmed),
                   04_film_test_id (confirmed)]

# Batch A — C_task work (produces D + I material)
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

# Batch B — D_experiment work (produces K + W material)
experiment_batch:
  - id:        E12
    skill:     /haipipe-experiment design
    new:       true
    arms:      [film_pm, baseline_pm]
    claim_target: "FiLM + param-matched yields X improvement on test-od"
    yields:    [K04, W03]
    needs:     [D04, I07]
    rationale: "K03 says FiLM not robust on test-od; need param-matched
                re-test to rule out scale confound"

# Archive — what DIKW cards E_insight will file at session end
insight_yield:
  D04: {layer: D, sources: [T1]}
  I06: {layer: I, sources: [T1]}
  I07: {layer: I, sources: [T2], refs: [D04]}
  K04: {layer: K, sources: [E12], refs: [I06, I07]}
  W03: {layer: W, sources: [E12], refs: [K04]}

# DAG — explicit blocking relationships
dag:
  - T1, T2 in parallel                # D04 + I06 + I07 obtained
  - E12 needs [D04, I07]              # then triggered
  - All yields filed → G-report

# Gate budget
gates:
  - id:         G-design
    threshold:  "all yields have a producer in task_batch or experiment_batch"
  - id:         G-observe
    threshold:  "every D/I in insight_yield has artifact under tasks/.../results/"
  - id:         G-claim
    threshold:  "every K/W in insight_yield has experiment.yaml.result.status == confirmed"
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
- K/W cards MUST have at least one experiment id in `sources`.
- D/I cards MUST have at least one task id in `sources`.
- Strategic W cards (sources = multiple K) are allowed; mark with
  `type: strategic` on the entry.
- dag never has K depending only on D (must pass through experiment).
```


Definition of done
-------------------

- [ ] `applications/<kind>/<NN_slug>/plans/plan-v{N}.yaml` written, parses
- [ ] `task_batch` + `experiment_batch` + `insight_yield` all populated
- [ ] Every id in any `yields:` list appears as key in `insight_yield`
- [ ] No K/W entry sources a task (must source an experiment)
- [ ] dag respects layer-letter promotion rule
- [ ] On --revise: revise_history appended; feedback verbatim preserved


Compose report mode (Phase 4)
------------------------------

Triggered as `Skill("haipipe-application-plan", args="compose report")`.
Distinct from the plan mode above — no plan is written; the active
plan-v{N}.yaml + filed insight cards are READ to assemble the final
report.

Inputs (read-only):
- `applications/ask/<NN>/SESSION_STATE.json`  (data_cut, plan_version, gates)
- `applications/ask/<NN>/plans/plan-v{N}.yaml`  (insight_yield map)
- `insights/<L>_<folder>/<L>NN_*.md` for every card in insight_yield
- `data/contract.yaml` + `data/available.md`  (for Provenance section)

Output:
- `applications/ask/<NN>/report.md`  (atomic .tmp + mv)

Template:
- MUST follow `../haipipe-application/ref/report-template.md` exactly:
  header, TL;DR, per-layer blocks (D, I, K, W), empty-layer
  placeholders, "Did we answer..." section, Provenance.
- Per-card block: 5 elements (Illustration | Table | Narrative | Source).
  Illustration path comes from the card's `source_artifact` field
  (PROJECT_ROOT-relative); use "n/a — no figure produced" if the
  artifact folder contains no figure.
- Table is copied verbatim from the card body's primary table.
- Narrative is freshly composed (2-4 sentences) by interpreting the
  card's Observation + table — NOT copied wholesale from the card.

Gate hand-off:
- This mode does NOT fire G-report itself; it returns to ask Phase 4
  step E which invokes G-report against the template invariants.


Risk profile
-------------

Plan mode writes one file under `applications/<kind>/<NN_slug>/plans/`.
Compose-report mode writes one file under `applications/<kind>/<NN_slug>/report.md`.
Does NOT scaffold tasks or experiments — only proposes (plan) or
assembles (compose). Actual scaffolding happens in
`/haipipe-application-ask` Phase 2 after gate approval.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "plan-v1 written for 'Does FiLM help on test-od?': 2 D, 1 I, 1 K, 1 W"
artifacts: [insights/sessions/plans/plan-v{N}-<slug>.yaml]
next:      gate review (in session context) OR direct user approval
```
