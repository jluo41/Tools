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
Where should the verdict deposit?
Is this an ATOMIC claim or a COMPARISON across claims?
Is the evidence primarily task-sourced or discovery-sourced?
```

## Workflow

1. Intake the input: claim gap, question, artifact, paper/application need,
   reviewer objection, insight gap, or loose idea.
2. Scan nearby `probes/*/probe.yaml` for overlap.
3. Decide:
   - attach to existing probe
   - create new probe
   - standalone/no probe needed
4. Classify probe kind:
   - `atomic` = one claim about ONE effect/comparison that a single body of
     evidence settles. Verdict is simple. Example: "Agreeableness is associated
     with higher opioid intensity in LBP."
   - `comparison` = a claim ABOUT a relationship ACROSS atomic probes' verdicts.
     It LINKs to atomic verdicts, does NOT re-derive their numbers. Example:
     "the effect concentrates where discretion is high and attenuates where low."
   Heuristic: if the verdict needs "across N cohorts x M outcomes x K methods,"
   it is a comparison sitting on TOP of atoms — split atoms out.
5. Classify probe source kind:
   - `task` = evidence comes primarily from running code/pipelines -> letter T
   - `discovery` = evidence comes primarily from literature/external -> letter D
6. If creating/revising a probe, define:
   - `kind: atomic|comparison`
   - `claim.hypothesis`
   - `claim.target_sentence`
   - `claim.falsification`
   - `claim.scope`
   - `evidence_plan.required`
   - `evidence_plan.success_criteria.support|partial|refute`
   - `source.deposit_target`
   For comparison probes, `evidence_plan.required` entries should be `atom:`
   references to atomic probe verdicts, not raw task/discovery links.
7. Write `probe.yaml`.
8. Render `status.md`.

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
