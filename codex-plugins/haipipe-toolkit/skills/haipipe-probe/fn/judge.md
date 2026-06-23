---
name: haipipe-probe-judge
description: "Judge stage for a probe. Reads probe.yaml, evidence.md, and linked raw artifacts; runs structural, integrity, and semantic checks; writes verdict.md plus structured probe.yaml verdict state. Decides what the evidence honestly supports."
argument-hint: "[probe_ref] [--structural|--integrity|--claim]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Task
---

# Judge

Judge decides what the evidence supports. It is the claim-commitment gate.

Read answers:

```text
What did the evidence say?
```

Judge answers:

```text
What claim can we honestly make?
```

## Questions

```text
Is the comparison structurally valid?
Is the evidence honest and traceable?
Does the evidence support the target claim?
What scope is supported?
What caveats must travel with the claim?
What next evidence is needed if support is partial/no/blocked?
```

## Workflow

1. Load `probe.yaml`.
2. Require `evidence.md` or enough linked evidence to read directly.
3. Run structural check - delegate to `probe-structural-reviewer-agent` (Task)
   when available, else do inline (builder != judge: a fresh reviewer, not the planner):
   - required evidence exists
   - the compared roles are comparable
   - task results match intended contrast
   - discovery verdicts are accounted for
   - caveats cover obvious confounds
4. Run integrity check - delegate to `probe-integrity-auditor-agent` (Codex, Task)
   when available, else inline. Pass PATHS only so the builder can't rationalize:
   - provenance of outcome/ground truth
   - metric/table definition consistency
   - no phantom result claims
   - claim scope matches evidence scope
   - no leakage or invalid split if applicable
5. Run semantic claim check - delegate to `claim-verifier-agent` (Codex, Task);
   integrity=fail blocks this gate:
   - yes / partial / no / blocked
   - confidence high / medium / low
   - supported scope
   - unsupported scope
   - required caveats
   - next evidence needs
6. Write `verdict.md`.
7. Write structured `probe.yaml.verdict`.
8. Update `status.md`.

## Files

Reads:

```text
probes/<probe>/probe.yaml
probes/<probe>/evidence.md
linked tasks/...
linked discoveries/...
linked insights/...          prior memory only
```

Writes:

```text
probes/<probe>/verdict.md
probes/<probe>/probe.yaml         verdict block
probes/<probe>/status.md
```

Optional long sidecars:

```text
probes/<probe>/INTEGRITY_AUDIT.md
probes/<probe>/CLAIMS_FROM_RESULTS.md
```

Use optional sidecars when an independent reviewer output is long enough that
embedding it directly in `verdict.md` would make the main human artifact hard to
scan.

## Verdict Schema

Use this structure in `probe.yaml`:

```yaml
verdict:
  status: yes | partial | no | blocked
  confidence: high | medium | low
  structural: pass | warn | fail
  integrity: pass | warn | fail
  supported_scope: ""
  unsupported_scope: ""
  caveats: []
  next_needs: []
  judged_at: ""
```

## Gate

Stop if integrity fails, required evidence is missing, the claim would overreach
the evidence, or the verdict would commit a yes/no conclusion that needs user
approval under Copilot policy.
