---
name: haipipe-probe-console
description: "Open a context-aware Probe Console for one active probe. Loads probe.yaml and lifecycle artifacts, renders status.md, records .probe-console.yaml, and routes follow-up free-form user input through Plan/Gather/Read/Judge/Return."
argument-hint: "[probe_ref_or_path|status|route <text>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

# Probe Console

The Probe Console is the user-facing working session for one active probe.

## Questions

```text
Which probe is active?
What claim is being tested?
What lifecycle stage is it in?
What evidence is linked?
What evidence is missing?
What can safely happen next?
What requires approval?
```

## Workflow

1. Resolve the probe from `P.0605`, `0605`, or `probes/<folder>/`.
2. Resolve the project root as the nearest directory containing `probes/`.
   In nested examples, this is the example project root, not the repo root.
3. Load `probe.yaml`.
4. Read lifecycle files if present: `status.md`, `evidence.md`, `verdict.md`, `return.md`.
   Missing `status.md` is not an error; create it when rendering the panel.
5. Validate linked task/discovery/insight refs shallowly: exists/missing only.
6. Derive lifecycle stage:
   - no `probe.yaml` contract -> Plan
   - evidence missing or refs absent -> Gather
   - evidence linked but no `evidence.md` -> Read
   - evidence exists but no `verdict.md` -> Judge
   - verdict exists but no return action -> Return
   - return complete -> closed or ready for next probe
7. Write project-root `.probe-console.yaml`.
8. Render/update `status.md`.
9. For free-form follow-up input, classify it and route:
   - claim/question/idea -> Plan
   - path/artifact/call/link/check -> Gather
   - "summarize/read/results" -> Read
   - "support/verdict/judge" -> Judge
   - "backfill/file memory/next" -> Return

## Files

Reads:

```text
probes/<probe>/probe.yaml
probes/<probe>/status.md
probes/<probe>/evidence.md
probes/<probe>/verdict.md
probes/<probe>/return.md
linked task/discovery/insight refs
```

Writes:

```text
.probe-console.yaml
probes/<probe>/status.md
```

`.probe-console.yaml` belongs at the active project root, meaning the nearest
directory containing `probes/`.

## Gate

Stop and ask if the probe ref is ambiguous, the user input could belong to more
than one probe, or a routed action would create costly/PHI work, change the
claim, declare a final verdict, or edit an upstream paper/application.

If a referenced probe exists only as a proposal in `probes/FILING.md`, ask before
creating the real probe folder. Do not link artifacts to proposal placeholders.
