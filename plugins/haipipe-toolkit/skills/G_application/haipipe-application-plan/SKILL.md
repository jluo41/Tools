---
name: haipipe-application-plan
description: "Planning specialist of the haipipe-application family. Given a research question, writes a structured plan-vN.yaml describing which D / I / K / W tasks are needed to answer it AND which experiments (existing or new) must feed them. Used by /haipipe-application-ask at Phase 1. NO code, plan is markdown-yaml. Trigger: plan, /haipipe-application-plan, design synthesis, what tasks to run, plan-vN."
argument-hint: [question] [--project <path>] [--revise <N>] [--feedback <text>]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-application-plan
=============================

Takes one research question, produces a **plan-vN.yaml** that lays out
the synthesis path: which D / I / K / W tasks would answer it, and
which experiments must already be confirmed (or need to be triggered).

Used by `/haipipe-application-ask` at Phase 1. Can also run standalone.


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

```yaml
plan_version:     1
question:         "Does FiLM help on test-od?"
written_at:       <ISO>
status:           proposed | approved | superseded

# Existing knowledge scanned
existing_relevant:
  knowledge:      [K03]
  patterns:       [P02, P05]
  observations:   [O01, O03]

# Experiments needed (existing or new)
experiments_needed:
  confirmed:                         # already confirmed, just read
    - id:     02_lhm_vs_baseline
      use:    "source for D-task on val performance"
    - id:     04_film_test_id
      use:    "source for D-task on test-id performance"
  to_trigger:                        # new experiments to scaffold
    - proposed_id:    12_param_matched_film_test_od
      claim_target:   "FiLM + param-matched shows X improvement on test-od"
      arms:
        - baseline
        - film_test_od
      rationale:      "K03 says FiLM not robust on test-od; need
                       param-matched re-test to rule out confound."

# Phase plan
phases:
  D:
    - task:     write_observation_for_02
      input:    experiments/02_lhm_vs_baseline/
      output:   insights/D_observations/O{NN}_*.md
      skill:    /haipipe-insight-data 02
    - task:     write_observation_for_04
      input:    experiments/04_film_test_id/
      output:   insights/D_observations/O{NN}_*.md
      skill:    /haipipe-insight-data 04
  I:
    - task:     extract_film_pattern
      input:    [O*]
      output:   insights/I_patterns/P{NN}_*.md
      skill:    /haipipe-insight-information --scope ...
  K:
    - task:     update_or_create_film_knowledge
      input:    [P*]
      output:   insights/K_knowledge/K{NN}_*.md (may update K03)
      skill:    /haipipe-insight-knowledge --scope ...
  W:
    - task:     derive_action
      input:    [K*]
      output:   insights/W_wisdom/W{NN}_*.md
      skill:    /haipipe-insight-wisdom --scope ...

# Gate plan
gates:
  - after:      D
    threshold:  "all planned O entries written"
  - after:      I
    threshold:  "at least 1 P entry citing ≥ 2 O entries"
  - after:      K
    threshold:  "K updated or written, counter-evidence engaged"

# Revise history (filled by --revise)
revise_history:
  - version:    0
    feedback:   ""
    reason:     "initial plan"
```


Definition of done
-------------------

- [ ] `insights/sessions/plans/plan-v{N}-<slug>.yaml` written, parses
- [ ] All planned phases have at least one task
- [ ] experiments_needed list complete (no implicit dependencies)
- [ ] On --revise: revise_history appended; feedback verbatim preserved


Risk profile
-------------

Writes one file under `insights/sessions/plans/`. Does NOT scaffold
tasks or experiments — only proposes them. Actual scaffolding happens
in `/haipipe-application-ask` Phase 2 after gate approval.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "plan-v1 written for 'Does FiLM help on test-od?': 2 D, 1 I, 1 K, 1 W"
artifacts: [insights/sessions/plans/plan-v{N}-<slug>.yaml]
next:      gate review (in session context) OR direct user approval
```
