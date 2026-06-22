---
name: haipipe-probe-return
description: "Return stage for a probe. Sends a judged verdict back to its source or memory: paper/application/rebuttal/insight/next need. Writes return.md and structured probe.yaml return state."
argument-hint: "[probe_ref] [--target <path-or-kind>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

# Return

Return delivers a judged verdict to the place that needed it.

Return is not Report. Report makes a result inspectable. Return sends a verdict
with caveats back to paper, application, reviewer response, insight memory, or a
next evidence need.

## Questions

```text
Where should this verdict go?
What exact claim sentence can be reused?
What caveats must travel with it?
Should memory be filed?
Should this become a next probe need instead?
```

## Workflow

1. Load `probe.yaml` and `verdict.md`.
2. Resolve return target from `probe.yaml.return_target`, CLI args, or user
   instruction.
3. Prepare the returned verdict:
   - claim sentence
   - supported scope
   - caveats
   - confidence
   - next need if partial/no/blocked
4. If target is paper/application/rebuttal, ask before editing.
5. If target is insight memory, call the appropriate insight skill only after
   the verdict is judged and approved for filing.
6. Write `return.md`.
7. Write structured `probe.yaml.return`.
8. Update `status.md`.

## Files

Reads:

```text
probes/<probe>/probe.yaml
probes/<probe>/verdict.md
return target
```

Writes:

```text
probes/<probe>/return.md
probes/<probe>/probe.yaml         return block
probes/<probe>/status.md
```

May create/edit with approval:

```text
insights/K_knowledge/...
insights/W_wisdom/...
paper/application/rebuttal target
```

## Gate

Stop if no return target exists, the verdict is not judged, confidence/caveats
are insufficient, or the action would edit upstream text or file accepted memory
without explicit approval.
