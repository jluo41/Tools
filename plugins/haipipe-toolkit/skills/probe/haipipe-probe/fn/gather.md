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
Call - create missing task/discovery work
Link - attach existing task/discovery/insight artifacts
Check - decide whether required evidence is ready for Read
```

## Workflow

1. Load `probe.yaml`.
2. Classify requested gather action:
   - `call task`
   - `call discovery`
   - `link task`
   - `link discovery`
   - `link insight`
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
7. For ambiguous links, show candidate probes/roles and ask.
8. For `check`, verify existence/readiness only; do not summarize evidence.
9. Update `status.md`.
10. Write `gather.md` only for complex attach/call decisions.

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
