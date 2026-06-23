---
name: haipipe-probe-plan
description: "Plan stage for a probe. Turns user input, claim gaps, questions, or artifacts into a testable claim and evidence contract. Writes or revises probe.yaml and status.md."
argument-hint: "[new|revise|from-need|from-artifact] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

# Plan

Plan defines the claim and evidence needed to test it.

## Questions

```text
What claim or evidence need are we testing?
What would support, weaken, or refute it?
What evidence is required?
Does this belong to an existing probe or a new probe?
Where should the verdict return?
```

## Workflow

1. Intake the input: claim gap, question, artifact, paper/application need,
   reviewer objection, insight gap, or loose idea.
2. Scan nearby `probes/*/probe.yaml` for overlap.
3. Decide:
   - attach to existing probe
   - create new probe
   - standalone/no probe needed
4. If creating/revising a probe, define:
   - `claim.hypothesis`
   - `claim.target_sentence`
   - `claim.falsification`
   - `claim.scope`
   - `evidence_plan.required`
   - `evidence_plan.success_criteria.support|partial|refute`
   - `source.deposit_target`
5. Write `probe.yaml`.
6. Render `status.md`.

## Files

Reads:

```text
user input / source need
probes/*/probe.yaml
source paper/application/insight if supplied
```

Writes:

```text
probes/<MMDD_slug>/probe.yaml
probes/<MMDD_slug>/status.md
```

## Gate

Stop if the claim is unfalsifiable, duplicates an existing probe, the source is
unclear, or the user must choose between attaching to an existing probe and
creating a new probe.
