---
name: haipipe-experiment-design
description: "Pre-run specialist of haipipe-experiment. Defines a new experiment (claim + planned arms) and links existing runs into its arms. Writes/edits experiments/<ID>.yaml under a project. Called by /haipipe-experiment orchestrator. Direct invocation works for design-scoped work."
argument-hint: "[new|link] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-experiment-design
=================================

Owns the PRE-RUN half of experiment lifecycle: define an experiment
(claim + arms) and link existing runs into arms.

Does NOT scaffold runs. Use `/haipipe-project task run` for that.


Commands
--------

```
/haipipe-experiment design new <ID> [--project <path>]
  Interactive: writes experiments/<ID>.yaml from template, asks user
  for claim / hypothesis / aggregation spec / planned arm names.

/haipipe-experiment design link <ID> <run-path> [--arm <arm-name>]
  Adds <run-path> to arms[<arm-name>] list in the yaml.
  If --arm missing: infer from arm name if there's only one with
  matching pattern, else ASK.

/haipipe-experiment design unlink <ID> <run-path>
  Removes a run from arms.

/haipipe-experiment design rename-arm <ID> <old> <new>
  Renames an arm key in the yaml.
```


Workflow — `new`
----------------

```
Step 1: Resolve project root.
  - If --project given, use it.
  - Else if cwd is inside examples/<X>, use that project.
  - Else ASK.

Step 2: Validate <ID>.
  - Convention: E + 2-digit (e.g. E01, E02, E42).
  - Must not collide with existing experiments/*.yaml.

Step 3: Collect via interactive prompts:
  - title (1 line, descriptive)
  - hypothesis (1-2 sentences, falsifiable)
  - claim_target (the sentence we'd publish if confirmed)
  - aggregation.metric (e.g. MAE_test_id, AUROC_val)
  - aggregation.statistic (mean_std | mean_std_paired_t | sign_test)
  - planned arms (names only, no run-paths yet)

Step 4: Write experiments/<ID>.yaml from template.
  Template: ../ref/experiment-yaml-schema.md (skeleton at the top).

Step 5: Emit specialist tail.
```


Workflow — `link`
------------------

```
Step 1: Resolve experiment by <ID>; refuse if not found.
Step 2: Validate <run-path> exists and contains runtime.yaml.
Step 3: Determine arm:
  - --arm explicit: use that.
  - Else inspect <run-path>'s _meta.purpose for arm hints.
  - Else ASK (show planned arms list).
Step 4: Add run-path to arms[<arm>].
Step 5: Emit specialist tail.
```


Disambiguation
---------------

  - Missing verb (just <ID> + run-path) → assume `link`.
  - Missing run-path in `link` → ASK; show available runs in project.
  - <ID> exists for `new` → refuse, suggest `link` instead.
  - <ID> doesn't exist for `link` → suggest `new` first.


Validation (always run before saving)
--------------------------------------

  - Yaml parses
  - Required fields present: id, title, hypothesis, arms, aggregation
  - arm names are unique
  - all linked run-paths exist on disk
  - all linked runs have runtime.yaml (otherwise warn)


Risk profile
-------------

CREATES / EDITS files under `examples/<project>/experiments/`. Does not
touch tasks/ or runs/. Refuses to overwrite existing yamls without
`--force`.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "Created 02_lhm_vs_baseline (3 arms planned)" / "Linked run_seed42 to arm 'baseline'"
artifacts: [experiments/02_lhm_vs_baseline/experiment.yaml]
next:      suggested: /haipipe-experiment design link 02 <next-run>
           or         /haipipe-experiment result 02 (when all arms have runs)
```
