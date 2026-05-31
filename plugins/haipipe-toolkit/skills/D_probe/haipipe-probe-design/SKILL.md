---
name: haipipe-probe-design
description: "Pre-run specialist of haipipe-probe. Defines a new probe (claim + planned arms) and links existing runs into its arms. Writes/edits probes/<GROUP>_<group_slug>/<NN>_<slug>/probe.yaml under a project. Called by /haipipe-probe orchestrator. Direct invocation works for design-scoped work."
argument-hint: "[new|link] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-probe-design
=================================

Owns the PRE-RUN half of probe lifecycle: define a probe
(claim + arms) and link existing runs into arms.

Does NOT scaffold runs. Use `/haipipe-project task run` for that.


Commands
--------

```
/haipipe-probe design new <slug> [--project <path>] [--group A] [--group-title <slug>] [--id NN]
  Interactive: writes probes/<GROUP>_<group_slug>/<NN>_<slug>/probe.yaml
  from template, asks user for claim / hypothesis / aggregation spec /
  planned arm names.

/haipipe-probe design link <probe> <run-path> [--arm <arm-name>]
  Adds <run-path> to arms[<arm-name>].runs in the yaml.
  If --arm missing: infer from arm name if there's only one with
  matching pattern, else ASK.

/haipipe-probe design unlink <probe> <run-path>
  Removes a run from arms.

/haipipe-probe design rename-arm <probe> <old> <new>
  Renames an arm key in the yaml.
```


Workflow — `new`
----------------

```
Step 1: Resolve project root.
  - If --project given, use it.
  - Else if cwd is inside examples/<X>, use that project.
  - Else ASK.

Step 2: Allocate / validate identity.
  - Canonical source ref: `P.<GROUP><NN>`, e.g. `P.A01`.
  - Canonical folder: `probes/<GROUP>_<group_slug>/<NN>_<slug>/`.
  - YAML `id:` is the canonical source ref, not `E02` or flat `P02`.
  - If `--group` is omitted, ASK or choose the default group from `probes/INDEX.md`.
  - If `--id NN` is omitted, use the next unused 2-digit NN within that group.
  - Must not collide with an existing probe folder in that group.

Step 3: Collect via interactive prompts:
  - title (1 line, descriptive)
  - hypothesis (1-2 sentences, falsifiable)
  - claim_target (the sentence we'd publish if confirmed)
  - aggregation.metric (e.g. MAE_test_id, AUROC_val)
  - aggregation.statistic (mean_std | mean_std_paired_t | sign_test)
  - planned arms (names + optional task_type / run_specs; no run-paths yet)

Step 4: Write probes/<GROUP>_<group_slug>/<NN>_<slug>/probe.yaml from template.
  Template: ../ref/probe-yaml-schema.md (skeleton at the top).

Step 5: Emit specialist tail.
```


Workflow — `link`
------------------

```
Step 1: Resolve probe by `P.A01`, `A01`, `A/01_<slug>`, or folder path; refuse if not found.
Step 2: Validate <run-path> exists and contains runtime.yaml.
Step 3: Determine arm:
  - --arm explicit: use that.
  - Else inspect <run-path>'s _meta.purpose for arm hints.
  - Else ASK (show planned arms list).
Step 4: Add run-path to arms[<arm>].runs.
Step 5: Emit specialist tail.
```


Disambiguation
---------------

  - Missing verb (just <probe> + run-path) → assume `link`.
  - Missing run-path in `link` → ASK; show available runs in project.
  - group+slug/NN exists for `new` → refuse, suggest `link` instead.
  - target doesn't exist for `link` → suggest `new` first.


Validation (always run before saving)
--------------------------------------

  - Yaml parses
  - Required fields present: id, title, hypothesis, arms, aggregation
  - arm names are unique
  - all linked `arms.*.runs` paths exist on disk
  - all linked runs have runtime.yaml (otherwise warn)


Risk profile
-------------

CREATES / EDITS files under `examples/<project>/probes/`. Does not
touch tasks/ or runs/. Refuses to overwrite existing probe folders without
`--force`.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "Created P.A01 lhm_vs_baseline (3 arms planned)" / "Linked run_seed42 to arm 'baseline'"
artifacts: [probes/A_baseline_controls/01_lhm_vs_baseline/probe.yaml]
next:      suggested: /haipipe-probe design link P.A01 <next-run>
           or         /haipipe-probe result P.A01 (when all arms have runs)
```
