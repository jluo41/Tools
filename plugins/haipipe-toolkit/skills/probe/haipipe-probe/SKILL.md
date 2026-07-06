---
name: haipipe-probe
description: "Evidence-gateway layer doc (folderless probe). A probe is a PHASE (each stage's PROBE step in paper/application DPRC) plus a GATEWAY agent (haipipe-probe-orchestrator-agent), not a place: the consumer's per-stage _PROBE/PPNN card is the single source of truth for contract + receipt + verdict, and execution artifacts live in discoveries/ and tasks/. The old Probe Console and probes/ folders are RETIRED (2026-07-05). Invoke this skill only to consult the layer contract or the PPNN card anatomy; evidence work itself is dispatched by stage workers, never interactively here. Trigger: probe, evidence gateway, PPNN card, claim evidence, judge claim, /haipipe-probe."
argument-hint: "[contract|card|status]"
allowed-tools: Bash, Read, Grep, Glob
metadata:
  version: "6.0.0"
  last_updated: "2026-07-05"
  summary: "Folderless probe layer: PROBE phase + evidence gateway agent; PPNN card = single source of truth; probes/ folders and the Probe Console retired. This SKILL.md is the layer contract doc, not an interactive console."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Skill: haipipe-probe (evidence-gateway layer, folderless)

A probe is a claim-level evidence contract that asks one question:

```text
Does the available evidence support this claim, under what scope, and with what caveats?
```

Since 2026-07-05 that contract has ONE home: the consumer's per-stage `_PROBE/PPNN_*.md` card (paper or application). There is no `probes/` folder anymore — it duplicated the card and broke single-source-of-truth (JL ruling; see ../SOP-folderless-refactor.md until archived, and ../DESIGN.md).

## Layer boundaries (unchanged)

```text
task      executes internal work (code, scripts, data processing)
discovery checks outside evidence (literature, prior art; Review type owns
          project-side judgment artifacts: verdict.md / landscape.md)
insight   stores judged knowledge (D/I/K/W cards)
probe     the PROBE phase + the gateway: plans (card), dispatches (gateway),
          reads (anchored return), judges (reviewer, full mode) — owns no files
```

## How evidence work actually runs

```text
stage DRAFT finds a gap
  → stage's PROBE phase: Skill(haipipe-paper-probe) worker   (BOOKKEEP: writes PPNN card)
    → Agent(haipipe-probe-orchestrator-agent)                (gateway, clean context, bg)
       SWEEP discoveries/ tasks/ insights/ (+ legacy probes/ read-only)
       shape: reused | enriched | fresh
       → Agent(haipipe-discovery-orchestrator-agent)         (external evidence)
       → Agent(haipipe-task-orchestrator-agent)              (runs/code)
       → Agent(haipipe-probe-reviewer-agent)                 (full mode: G1/G2/G3, returned)
    ← anchored takeaways + pick_list + (full) verdict
  → worker TRANSLATE lands everything in the PPNN card (+ claims-ledger flip)
```

Users never invoke evidence work through this skill; stage skills own the phase. Dashboards live in `/haipipe-paper enter` (open needs) — the retired Probe Console's panel duties moved there.

## PPNN card anatomy (the single source of truth)

```markdown
# PPNN — <need title>
- stage: <stage> · mode: light | full · status: planned | dispatched | read | verdicted
- claim: <the claim this evidence serves, or the orientation question>
- refs: <discoveries/L##_.../sources.md · tasks/T##_...>      ← direct, no wrapper

## Need / ## Why / ## Route        ← the order (written at BOOKKEEP)
## Takeaways                       ← the receipt (anchored lines, written at TRANSLATE)
## Verdict                         ← full mode only (landed by TRANSLATE from the gateway return)
- verdict: supported | refuted | inconclusive · judged-by · date
- G1 structural ✅/❌ · G2 integrity ✅/❌ · G3 claim ✅/❌
- <one-paragraph reasoning tying refs to the claim>
```

Light mode stops at `read` (no committed verdict). Full mode is for claims-stage committed verdicts; the claims ledger (1-claims.md) flips its C-section status in the same TRANSLATE.

## Retired machinery (do not resurrect)

- `probes/<slug>/` folders, `probe.yaml`, `evidence.md`, `status.md`, `verdict.md` — legacy folders on disk are read-only history; SWEEP may read them for reuse, nothing writes them.
- The interactive Probe Console (`.probe-console.yaml`, console panels).
- `haipipe-probe-creator-agent` (in `agents/_old/`).
- `fn/` and `ref/` files in this folder are folder-era procedure docs: LEGACY, kept for the G-gate definitions and schema history they carry (`fn/judge.md`, `fn/g2_integrity_check.py` remain referenced by the reviewer agent). Do not load them for new work except where the reviewer agent points.

## Status queries

`/haipipe-probe status` (or any status ask): derive from disk — scan `papers/*/0-lifecycle/*/_PROBE/*.md` + `1-probe-plans/README.md` for card statuses; never from a stored console state.
