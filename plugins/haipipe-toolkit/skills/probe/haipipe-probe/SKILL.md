---
name: haipipe-probe
description: "Evidence gateway (folderless probe). A probe is a PHASE (each stage's PROBE step) plus a GATEWAY agent, not a place: the consumer's _PROBE/PPNN card is the single source of truth for contract + receipt + verdict; execution artifacts live in discoveries/ and tasks/; probes/ folders and the Probe Console are RETIRED (2026-07-05). Two uses: (1) DIRECT ASK — /haipipe-probe \"<question or claim>\" runs ad-hoc evidence work outside any stage: dispatches the gateway agent, evidence lands project-side, anchored takeaways return in chat; (2) layer contract / PPNN card anatomy reference for stage workers. Trigger: probe, evidence gateway, find evidence for claim, PPNN card, judge claim, /haipipe-probe."
argument-hint: "[\"<question-or-claim>\" [light|full] | contract | card | status]"
allowed-tools: Bash, Read, Grep, Glob, Agent
metadata:
  version: "6.1.1"
  last_updated: "2026-07-05"
  summary: "Folderless probe layer: PROBE phase + evidence gateway agent; PPNN card = single source of truth; probes/ folders and Console retired. Skill doubles as the DIRECT-ASK front door for ad-hoc evidence work outside stages."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Skill: haipipe-probe (evidence-gateway layer, folderless)

A probe is a claim-level evidence contract that asks one question:

```text
Does the available evidence support this claim, under what scope, and with what caveats?
```

Since 2026-07-05 that contract has ONE home: the consumer's per-stage `_PROBE/PPNN_*.md` card (paper or application). There is no `probes/` folder anymore — it duplicated the card and broke single-source-of-truth (JL ruling; see ../_archive/DESIGN.md for the folder-era rationale, and ../SOP-folderless-refactor.md for the migration record).

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
       SWEEP insights/ + discoveries/ + tasks/ (all three, every time)
       shape: reused | enriched | fresh
       → Agent(haipipe-discovery-orchestrator-agent)         (external evidence)
       → Agent(haipipe-task-orchestrator-agent)              (runs/code)
       → Agent(haipipe-probe-reviewer-agent)                 (full mode: G1/G2/G3, returned)
    ← anchored takeaways + pick_list + (full) verdict
  → worker TRANSLATE lands everything in the PPNN card (+ claims-ledger flip)
```

Inside a paper/application, stage skills own the phase — users work through them. Dashboards live in `/haipipe-paper enter` (open needs) — the retired Probe Console's panel duties moved there.

## Direct ask (ad-hoc evidence work, no stage)

`/haipipe-probe "<question or claim>" [light|full]` — the standalone evidence verb for questions that belong to no paper stage yet:

```text
1. Frame the ask into a plan (claim/question + evidence needed + route) — shown
   to the user in one strip, no file written.
2. Dispatch Agent(haipipe-probe-orchestrator-agent) run_in_background with
   {project_root, mode (light default), plan}. Same gateway, same discipline:
   SWEEP, shape reused|enriched|fresh, no inline searching, fresh must land.
3. Evidence lands project-side as always (discoveries/ sources.md, tasks/) —
   the durable part is never chat-only.
4. The anchored takeaways + pick_list (+ full-mode verdict) return IN CHAT —
   the user is the consumer, so the receipt is the reply, not a card.
5. If the question later matters to a paper: the stage opens a PPNN card whose
   refs point at the already-landed artifacts (pure REUSE — nothing re-run).
```

No probes/ folder, no PPNN card, no console state is created by a direct ask; what persists is exactly what landed in the execution ledgers.

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

- `probes/<slug>/` folders, `probe.yaml`, `evidence.md`, `status.md`, `verdict.md` — legacy folders in old projects are dead history: SWEEP does not read them, nothing writes them.
- The interactive Probe Console (`.probe-console.yaml`, console panels).
- `haipipe-probe-creator-agent` (retired to `../_archive/_old/`).
- `fn/` and `ref/` folders: DELETED 2026-07-05 (folder-era procedure docs; git history keeps them). The two live pieces moved to `../agents/`: `g2_integrity_check.py` + `probe-caveats-checklist.txt`, both referenced by the reviewer agent.

## Status queries

`/haipipe-probe status` (or any status ask): derive from disk — scan `papers/*/0-lifecycle/*/_PROBE/*.md` + `1-probe-plans/README.md` for card statuses; never from a stored console state.
