---
name: haipipe-probe-read
description: "Read stage for a probe. Reads linked task/discovery/insight artifacts and writes evidence.md plus structured probe.yaml result summary. Does not judge claim support."
argument-hint: "[probe_ref]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

# Read

Read summarizes gathered evidence. It does not decide the claim.

## Questions

```text
What did the linked evidence say?
What evidence is missing?
What contradicts the hypothesis?
What is only mechanical/plumbing evidence?
What scope does the evidence actually cover?
```

## Workflow

1. Load `probe.yaml`.
2. Read linked task artifacts: reports, runtime, metrics, regression tables, or
   task-level summaries.
3. Read linked discovery artifacts: discovery yaml/markdown, sources, notes,
   verdict.
4. Read linked insight cards only as prior memory/provenance, not as primary
   execution evidence.
5. Summarize evidence by role/arm/source.
6. Record missing, malformed, contradictory, or scope-limited evidence.
7. Write `evidence.md`.
8. Write structured `probe.yaml.result`.
9. Update `status.md`.

## Files

Reads:

```text
probes/<probe>/probe.yaml
linked tasks/...
linked discoveries/...
linked insights/...
```

Writes:

```text
probes/<probe>/evidence.md
probes/<probe>/probe.yaml         result block
probes/<probe>/status.md
```

## Gate

Stop if required evidence is missing, artifacts are malformed, metric/table
contracts cannot be read, or evidence refs are ambiguous. Do not silently coerce
missing numbers to zero/NaN.
