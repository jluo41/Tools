---
name: haipipe-probe-read
description: "Read stage for a probe. The MOST PARTICIPATORY step: presents gathered results as a legible panel and STOPS for the user to internalize them. The user's reaction is the input to Judge. Does not judge claim support."
argument-hint: "[probe_ref]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

# Read

Read presents gathered evidence and STOPS for the user to internalize it.

Read is not a summary the agent writes for itself. Read is the step where the
USER absorbs what the evidence says, reacts, and that reaction becomes the input
to Judge. This makes Read the MOST participatory step in the lifecycle.

## Interaction Ownership

```text
Plan     user frames the claim (HIGH participation — user drives)
Gather   agent links/calls; user gates costly work (MEDIUM)
Read     agent presents; USER INTERNALIZES + REACTS (HIGH — the stop gate)
Judge    agent proposes verdict; user approves (MEDIUM)
Deposit  agent files; user confirms (LOW)
```

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
2. Verify Gather is complete: all participants finished running (check the
   participant roster from Gather). If not, STOP and return to Gather.
3. Read linked task artifacts: reports, runtime, metrics, regression tables, or
   task-level summaries.
4. Read linked discovery artifacts: discovery yaml/markdown, sources, notes,
   verdict.
5. Read linked insight cards only as prior memory/provenance, not as primary
   execution evidence.
6. Present evidence in a legible panel:
   - Key numbers, effect sizes, sample sizes, significance
   - Patterns, surprises, contradictions
   - Missing or scope-limited evidence
   - Organize by role/arm/source
7. Write `evidence.md`.
8. Write structured `probe.yaml.result`.
9. Update `status.md`.
10. **STOP.** Present the evidence panel to the user. Do NOT proceed to Judge.
    The user must internalize the results and react. Their reaction is the input
    to Judge.

## Verdict Language Ban

evidence.md MUST NOT contain verdict-like language. The following phrases (and
equivalents) belong in Judge, not Read:

```text
BANNED in evidence.md:
  "supported"    "not supported"    "refuted"       "confirmed"
  "validates"    "invalidates"      "proves"         "disproves"
  "the hypothesis is..."            "we can conclude..."
  direction: support/refute         (in probe.yaml result block)
```

Use neutral, descriptive language instead:

```text
ALLOWED:
  "the data shows X"              "the difference is Y pp"
  "the coefficient is Z (p=W)"   "no significant effect observed"
  "the pattern is consistent/inconsistent with..."
```

The `result:` block in `probe.yaml` records `status: read|incomplete|blocked`
and factual summaries, NOT direction or verdict.

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

Stop if:
- Gather is incomplete (not all participants finished running)
- Required evidence is missing, artifacts are malformed, metric/table contracts
  cannot be read, or evidence refs are ambiguous
- Do not silently coerce missing numbers to zero/NaN
- ALWAYS stop after writing evidence.md — this is the internalize gate
