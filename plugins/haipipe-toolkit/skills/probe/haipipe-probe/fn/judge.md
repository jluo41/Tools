---
name: haipipe-probe-judge
description: "Judge stage for a probe. Reads probe.yaml, evidence.md, and linked raw artifacts; runs structural, integrity, and semantic checks; writes verdict.md plus structured probe.yaml verdict state. Decides what the evidence honestly supports."
argument-hint: "[probe_ref] [--structural|--integrity|--claim]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
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
3. Run the 3 gates through `haipipe-probe-reviewer-agent` (one Agent dispatch runs
   G1+G2+G3 with full cross-gate context; builder != judge - the planner never
   grades its own claim). If agent dispatch is unavailable, run the same gates
   inline with fresh-reviewer reasoning. Walk `ref/probe-caveats-checklist.txt`
   before committing any verdict; each YES becomes a caveat.
   G1 structural - is the comparison valid?
   - required evidence exists
   - the compared roles are comparable
   - task results match intended contrast
   - discovery verdicts are accounted for
   - caveats cover obvious confounds
4. G2 integrity - is the evidence honest? Deterministic, no LLM judgment:
   run `python fn/g2_integrity_check.py <probe_folder>` (traces every number in
   evidence.md to the source CSVs). Thresholds: >95% verified = pass, 80-95% =
   warn (caps G3 confidence at medium), <80% = fail (BLOCKS G3). If the script
   cannot run, check numbers against source files manually:
   - provenance of outcome/ground truth
   - metric/table definition consistency
   - no phantom result claims
   - claim scope matches evidence scope
   - no leakage or invalid split if applicable
5. G3 semantic claim check - integrity=fail blocks this gate:
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
