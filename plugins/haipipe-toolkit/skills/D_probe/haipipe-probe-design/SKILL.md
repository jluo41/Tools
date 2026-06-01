---
name: haipipe-probe-design
description: "Pre-run specialist of haipipe-probe. Defines a new probe (claim + planned arms) and links existing runs into its arms. Writes/edits probes/<MMDD>_<slug>/probe.yaml under a project. Called by /haipipe-probe orchestrator. Direct invocation works for design-scoped work."
argument-hint: "[new|link] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.2.0"
  last_updated: "2026-06-01"
  summary: "Pre-run specialist of haipipe-probe."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-06-01): new probe identity uses direct `probes/MM-NN_slug/` folders and `P.MM-NN` refs."
    - "1.2.0 (2026-06-01): probe identity switches to date-based `MMDD` folders + `P.MMDD` refs; `design new` takes `--date MMDD` (default today), same-day collisions get a letter suffix."
---

Skill: haipipe-probe-design
=================================

Owns the PRE-RUN half of probe lifecycle: define a probe
(claim + arms) and link existing runs into arms.

Does NOT scaffold runs. Use `/haipipe-project task run` for that.


Commands
--------

```
/haipipe-probe design new <slug> [--project <path>] [--date MMDD]
  Interactive: writes probes/<MMDD>_<slug>/probe.yaml
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
  - Canonical source ref: `P.<MMDD>`, e.g. `P.0601`.
  - Canonical folder: `probes/<MMDD>_<slug>/`.
  - YAML `id:` is the canonical source ref, not `E02` or flat `P02`.
  - `MMDD` is the creation date: `MM` = month, `DD` = day.
  - If `--date MMDD` is omitted, use today's local month+day (`MMDD`).
  - If a probe folder already exists for that `MMDD`, append the next free
    lowercase letter suffix (`0601` → `0601b` → `0601c` → ...), scanning both
    active `probes/<MM>*` and archived `probes/<YYYY>-archive/<MM>*` folders
    for the current year.
  - Must not collide with an existing active or archived probe folder for
    that `MMDD` (or `MMDD<suffix>`).

Step 3: Collect via interactive prompts:
  - title (1 line, descriptive)
  - hypothesis (1-2 sentences, falsifiable)
  - claim_target (the sentence we'd publish if confirmed)
  - aggregation.metric (e.g. MAE_test_id, AUROC_val)
  - aggregation.statistic (mean_std | mean_std_paired_t | sign_test)
  - planned arms (names + optional task_type / run_specs; no run-paths yet)

Step 4: Write probes/<MMDD>_<slug>/probe.yaml from template.
  Template: ../ref/probe-yaml-schema.md (skeleton at the top).

Step 5: Emit specialist tail.
```


Workflow — `link`
------------------

```
Step 1: Resolve probe by `P.0601`, `0601`, or folder path; refuse if not found.
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
  - MMDD+slug already exists for `new` → refuse (or allocate the next letter
    suffix); suggest `link` instead.
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
summary:   "Created P.0601 framing_loss-aversion (3 arms planned)" / "Linked run_seed42 to arm 'baseline'"
artifacts: [probes/0601_framing_loss-aversion/probe.yaml]
next:      suggested: /haipipe-probe design link P.0601 <next-run>
           or         /haipipe-probe result P.0601 (when all arms have runs)
```
