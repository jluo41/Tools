---
name: haipipe-probe-gather
description: "Gather stage for a probe. Calls missing task/discovery work, links existing task/discovery/insight artifacts, and checks whether the evidence set is ready to read."
argument-hint: "[call|link|check] [probe_ref] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Task
---

# Gather

Gather acquires evidence. It does not interpret evidence.

## Questions

```text
What evidence do we need?
Does it already exist?
If missing, should we call task or discovery?
If existing, which probe should it link to?
Is the evidence set ready to read?
```

## Actions

```text
Call    - create missing task/discovery work
Link    - attach existing task/discovery/insight artifacts
Extract - link an existing artifact + run a small extraction script on it
          (lighter than a full task lifecycle; heavier than a plain link)
Check   - decide whether required evidence is ready for Read
```

## Workflow

1. Load `probe.yaml`.
2. Classify requested gather action:
   - `call task`
   - `call discovery`
   - `link task`
   - `link discovery`
   - `link insight`
   - `extract` (link + small extraction script)
   - `check`
3. For `link`, apply `ref/probe-attach.md` first:
   - strong match to active probe -> attach to active probe
   - strong match to another existing probe -> propose that probe
   - claim-bearing but no existing probe -> propose a new probe
   - standalone/non-claim evidence -> log as standalone
   Ask before creating a new probe, changing claim scope, or attaching to a
   non-active probe.
4. For `call task`, invoke the appropriate task skill/procedure and write a
   requested task ref. Task owns Plan/Build/Execute/Report.
5. For `call discovery`, invoke discovery and write a requested discovery ref.
6. For accepted `link`, validate that the artifact exists, infer role if possible, and
   add it to `evidence_refs`.
7. For `extract`, the lightweight link+extract path:
   a. Link the source artifact to `evidence_refs` as in step 6.
   b. Write a small extraction script (no config, no IPO contract) alongside
      the source data — NOT in a separate task folder.
   c. Run the script. The reviewer spot-checks the output (abbreviated Gate 2,
      not a full RUN_AUDIT).
   d. Mark the evidence_ref as `status: extracted` with the output path.
   Use extract when the work is too small for a full task lifecycle (< ~50 lines)
   but too complex for a plain link (needs filtering, subsetting, or ranking).
8. For ambiguous links, show candidate probes/roles and ask.
9. For `check`, verify existence/readiness only; do not summarize evidence.
10. Update `status.md`.
11. Write `gather.md` only for complex attach/call decisions.

## Gather Done

Gather is done when ALL participating tasks AND discoveries have FINISHED
RUNNING (not merely declared as refs) and every linked artifact resolves on
disk. "Called but still running / pending" = Gather NOT done.

At the Gather->Read boundary, emit a **participant roster**: one block naming
which tasks and discoveries actually ran. This manifest IS the boundary marker
and becomes the handoff to Read.

```text
--- Gather complete ---
Participants:
  tasks:
    - tasks/R01_Regression_TraitOpioid/D01_... (role: high_discretion_regression) ✅
    - tasks/R01_Regression_TraitOpioid/D21_... (role: low_discretion_regression) ✅
  discoveries:
    - discoveries/D0605_personality-opioid-prior-art (role: prior_art_check) ✅
```

## Fan-Out Model

One probe legitimately references N discoveries AND N tasks. This is the
intended model, not an edge case.

When a Gather call spans multiple distinct sub-questions or sub-literatures,
split into N discovery topic-folders (one question per folder, each its own
verdict), not one umbrella folder.

## Naming Rule

Name discovery and task folders by TOPIC, never by stage/action verb:

```text
GOOD: risk-attitude-practice-intensity, personality-opioid-prior-art
BAD:  field-scan, search, review, data-collection
```

"field-scan" is a stage name (what you DO); "risk-attitude-practice-intensity"
is a topic name (what it is ABOUT). The topic must be intelligible without
reading the folder contents.

## Files

Reads:

```text
probes/<probe>/probe.yaml
candidate tasks/...
candidate discoveries/...
candidate insights/...
```

Writes:

```text
probes/<probe>/probe.yaml         evidence_refs, calls, gather status
probes/<probe>/status.md
probes/<probe>/gather.md          optional
```

May create through other skills:

```text
tasks/...
discoveries/...
```

## Gate

Stop before costly computation, PHI/full-data runs, ambiguous artifact
assignment, changing claim scope, or creating work not covered by the evidence
plan.

If `probes/FILING.md` contains a placeholder such as `P.06xx_trait-diabetes`,
that is a proposal, not an existing probe. Ask before materializing it into a
real `probes/<MMDD>_<slug>/` folder and only then link artifacts.
