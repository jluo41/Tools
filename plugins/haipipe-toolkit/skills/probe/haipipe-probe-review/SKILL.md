---
name: haipipe-probe-review
description: "Claim-level judgment process for the folderless probe layer — the G1/G2/G3 rulebook. G1 structural (is the comparison valid), G2 integrity (is the evidence honest; deterministic g2_integrity_check.py), G3 claim (does the evidence support the claim → supported | refuted | inconclusive). Normally invoked HEADLESS by haipipe-probe-reviewer-agent, which the gateway dispatches in full mode only; the judgment is RETURNED as text and the consumer's TRANSLATE lands it in the stage _PROBE/PPNN card's ## Verdict. Writes NO files. Trigger: judge claim, probe verdict, G1 G2 G3, structural check, integrity audit, probe review."
argument-hint: "\"<claim>\" --refs <evidence artifact paths>   (complete spec only; normal path = gateway full mode)"
allowed-tools: Read, Grep, Glob, Bash
metadata:
  version: "1.0.0"
  last_updated: "2026-07-06"
  summary: "The G1/G2/G3 judgment process spec, extracted from the reviewer agent so the flow is a governed SKILL (JL 2026-07-06); the agent is a thin dispatch shell that calls this headless."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Skill: haipipe-probe-review (claim-level Judge, G1/G2/G3)

One question, three gates:

```text
Does this evidence mix support that claim — structurally valid (G1),
honestly grounded (G2), and sufficient for a committed verdict (G3)?
```

This is the SECOND review tier. Per-layer reviewers (discovery-reviewer, task-reviewer, card-reviewers) judge "is this artifact well-made"; this process judges "does this evidence MIX support this claim" — across discoveries/ + tasks/ + insights/ at once. The two tiers never merge (产审分离: whoever assembled the evidence does not grade it).

## Who runs this

```text
normal   Agent(haipipe-probe-reviewer-agent)  ← dispatched by the gateway, FULL mode only;
         the agent invokes this skill headless and returns its output verbatim
direct   /haipipe-probe-review "<claim>" --refs <paths>  — only with a complete spec
         (claim + on-disk evidence refs). No sweep, no evidence gathering here:
         if refs are missing, the answer is "dispatch the gateway first".
```

Light mode never judges — no committed verdict, this skill is not invoked.

## Input spec

```text
claim:  the exact sentence to judge (and, implicitly, what would refute it)
refs:   evidence artifact paths on disk — discoveries/<...>/sources.md,
        verdict.md / landscape.md, tasks/<...>/results/..., insight cards
```

## The three gates (sequential; G2 gates G3)

If integrity fails, the claim verdict is `inconclusive` (blocked), not `refuted`.

### G1 — Structural: is the comparison valid?

Read the referenced artifacts, then check:

```text
[ ] every evidence ref resolves to a real file on disk (unresolvable → name it; cannot judge)
[ ] the roles / contrast being compared are apples-to-apples
[ ] the linked task/discovery results actually match the claim's intended comparison
[ ] caveats cover the detectable confounds (./probe-caveats-checklist.txt)
[ ] any Review-type discovery verdict.md / landscape.md is accounted for
```

Return `G1: ✅` or `G1: ❌ <reason>`.

### G2 — Integrity: is the evidence honest?

Five fraud-pattern categories:

```text
A. Ground-truth provenance       — every number traces to a real source file?
B. Metric/definition consistency — same metric name means the same computation?
C. Phantom results               — any cited result that does not appear in the source?
D. Scope-language mismatch       — does the claim overstate what the evidence covers?
E. Individual/split leakage      — any leakage across train/test or across individuals?
```

Run the deterministic checker (no LLM judgment in the integrity audit):

```bash
python <skills>/probe/haipipe-probe-review/g2_integrity_check.py <evidence artifact paths>
```

Thresholds: **>95% verified** → `✅ pass` · **80–95%** → `⚠️ warn` (caps G3 confidence at `medium`) · **<80%** → `❌ fail` (blocks G3). If the script is unavailable, fall back to manual checking: read the source files and confirm each cited number appears there.

Return `G2: ✅ pass` | `⚠️ warn <reason>` | `❌ fail <reason>`.

### G3 — Claim: does the evidence support the claim?

Only if G2 did not fail. Then:

```text
1. Re-read the claim and what would refute it.
2. Re-read the source artifacts (not a summary of them).
3. Assess: does the evidence meet the bar for support?
4. Separate supported scope from unsupported scope.
5. List the required caveats.
6. Set confidence: high | medium | low, with justification (a G2 warn caps this at medium).
```

Verdict vocabulary is the PPNN card's (anatomy: `../haipipe-probe/SKILL.md`):

```text
supported     the evidence meets the bar (partial support = supported + an explicit unsupported scope)
refuted       the evidence meets the bar for the OPPOSITE / falsification
inconclusive  the evidence does not decide it — also the result when G2 failed (blocked)
```

## Return contract (text, never a file)

```text
gates:      G1 <✅/❌> · G2 <✅/⚠️/❌> · G3 <✅/❌>
verdict:    supported | refuted | inconclusive
confidence: high | medium | low
scope:      supported "<...>"  /  unsupported "<...>"
caveats:    [ ... ]
reasoning:  one paragraph tying the evidence refs to the claim
judged-by:  haipipe-probe-review · <date>
```

The gateway carries this return; the consumer's TRANSLATE lands it in the stage `_PROBE/PPNN` card's `## Verdict` section and flips the claims ledger in the same pass.

## Hard boundaries

- Writes NOTHING — no verdict.md, no probe.yaml, no card, no consumer files. The judgment is the return.
- Gathers NOTHING — no searches, no task runs, no sweep; judging given refs only.
- Deposits NOTHING — insight K-cards and claims-ledger flips belong to the consumer side.
