---
name: haipipe-probe-deposit
description: "Deposit stage for a probe. Settles a judged verdict into durable memory / backfills the source it served: paper/application/rebuttal/insight/next need. Writes deposit.md and structured probe.yaml deposit state."
argument-hint: "[probe_ref] [--target <path-or-kind>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

# Deposit

Deposit settles a judged verdict into the place that needed it, so the knowledge
durably accrues instead of evaporating.

Deposit is not Report. Report makes a result inspectable. Deposit settles a
verdict with caveats into paper, application, reviewer response, insight memory,
or a next evidence need.

## Questions

```text
Where should this verdict settle?
What exact claim sentence can be reused?
What caveats must travel with it?
Should memory be filed?
Should this become a next probe need instead?
```

## Workflow

1. Load `probe.yaml` and `verdict.md`.
2. Resolve deposit target from `probe.yaml.deposit_target`, CLI args, or user
   instruction.
3. Prepare the deposited verdict:
   - claim sentence
   - supported scope
   - caveats
   - confidence
   - next need if partial/no/blocked
4. If target is paper/application/rebuttal, ask before editing.
5. If the verdict is a keep-worthy belief, ALWAYS propose the insight handoff in
   the structured-tail `next:` — the literal `/haipipe-insight review <probe-folder>`
   command (review is proposal-only / ungated; it writes INSIGHT_REVIEW.yaml). Do
   NOT silently skip it; this is what keeps the probe->insight loop from being
   forgotten. `apply` (which files cards) stays gated on user approval.
6. Write `deposit.md`.
7. Write structured `probe.yaml.deposit`.
8. Update `status.md`.

## Files

Reads:

```text
probes/<probe>/probe.yaml
probes/<probe>/verdict.md
deposit target
```

Writes:

```text
probes/<probe>/deposit.md
probes/<probe>/probe.yaml         deposit block
probes/<probe>/status.md
```

May create/edit with approval:

```text
insights/K_knowledge/...
insights/W_wisdom/...
paper/application/rebuttal target
```

## Gate

Stop if no deposit target exists, the verdict is not judged, confidence/caveats
are insufficient, or the action would edit upstream text or file accepted memory
without explicit approval.
