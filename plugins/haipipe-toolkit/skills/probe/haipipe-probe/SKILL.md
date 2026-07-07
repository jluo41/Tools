---
name: haipipe-probe
description: "Evidence gateway (folderless probe). A probe is the general-purpose EXPLORE + GATHER verb for paper/application stages: sweep what the project already knows (insights D/I/K/W, discoveries, tasks), commission what it lacks, and optionally judge a claim (full mode). Not claim-specific — any evidence question (dataset profile, field norms, run result, claim verdict) enters here. The consumer's _PROBE/PPNN card is the single source of truth for contract + receipt + (full mode) verdict; execution artifacts live in discoveries/ and tasks/. Two uses: (1) DIRECT ASK — /haipipe-probe \"<question>\" runs ad-hoc evidence work outside any stage; (2) layer contract / PPNN card anatomy reference for stage workers. Trigger: probe, evidence, explore, gather, find evidence, PPNN card, /haipipe-probe."
argument-hint: "[\"<question>\" [light|full] | contract | card | status]"
allowed-tools: Bash, Read, Grep, Glob, Agent
metadata:
  version: "7.1.1"
  last_updated: "2026-07-06"
  summary: "Probe = general-purpose explore+gather verb (not claim-specific). PPNN card = single source of truth. Light = explore+gather (most needs); full = +judge (claims only, via haipipe-probe-review). Folderless. v7.1: refs REQUIRED once read — takeaways with empty refs = inline-evidence shortcut = status:failed. v7.1.1: card formatting — bullet lines only, no tables, ≤80 lines (mechanically enforced by the paper worker's check-probe-cards.sh)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Skill: haipipe-probe (evidence gateway, folderless)

A probe is the general-purpose **explore + gather** verb for paper and application stages:

```text
What does the project already know about this question,
what is missing, and (full mode only) does it support this claim?
```

Not claim-specific: a probe question can be a dataset profile ("how big is our cohort"), a field-norm survey ("what scales do LLM-sim studies use"), a run-result summary, or a claim verdict. Light mode (the default, most needs) explores and gathers; full mode adds a governed judgment step (G1/G2/G3 via haipipe-probe-review).

The evidence contract has ONE home: the consumer's per-stage `_PROBE/PPNN_*.md` card (paper or application). There is no `probes/` folder (JL ruling 2026-07-05; see ../_archive/DESIGN.md for the folder-era rationale).

## Layer boundaries (unchanged)

```text
task      executes internal work (code, scripts, data processing)
discovery checks outside evidence (literature, prior art; Review type owns
          project-side judgment artifacts: verdict.md / landscape.md)
insight   stores judged knowledge (D/I/K/W cards)
probe     the EXPLORE+GATHER verb: plans (card), sweeps (gateway), dispatches
          (discovery/task agents), reads (anchored return) — owns no files.
          Full mode adds judging via haipipe-probe-review (reviewer agent)
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
       → Agent(haipipe-probe-reviewer-agent)                 (full mode: runs Skill(haipipe-probe-review)
                                                              — G1/G2/G3, judgment returned)
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
- refs: <discoveries/L##_.../sources.md · tasks/T##_...>      ← REQUIRED once read; direct, no wrapper

## Need / ## Why / ## Route        ← the order (written at BOOKKEEP)
## Takeaways                       ← the receipt (anchored lines, written at TRANSLATE)
## Verdict                         ← full mode only (landed by TRANSLATE from the gateway return)
- verdict: supported | refuted | inconclusive · judged-by · date
- G1 structural ✅/❌ · G2 integrity ✅/❌ · G3 claim ✅/❌
- <one-paragraph reasoning tying refs to the claim>
```

`refs:` is EMPTY at BOOKKEEP and REQUIRED once the card reaches `status: read` (or
`verdicted`): it points at the durable project-side artifacts the gateway created
(`discoveries/.../sources.md`, `tasks/...`). Takeaways with an empty `refs:` mean the
evidence never landed project-side — the card is `status: failed`, not `read`. This is
the single invariant that separates a real probe from an inline-evidence shortcut.

Formatting: bullet lines only — NO markdown tables anywhere in a PP card (a table is
pasted findings, i.e. the shortcut), and a card stays under ~80 lines. Both are
enforced mechanically by the paper worker's `check-probe-cards.sh`.

Light mode stops at `read` (no committed verdict). Full mode is for claims-stage committed verdicts; the claims ledger (1-claims.md) flips its C-section status in the same TRANSLATE. How the verdict content is produced (gates, thresholds, vocabulary) is the sibling skill's spec: `../haipipe-probe-review/SKILL.md` — this file only owns where it LANDS.

## Retired machinery (do not resurrect)

- `probes/<slug>/` folders, `probe.yaml`, `evidence.md`, `status.md`, `verdict.md` — legacy folders in old projects are dead history: SWEEP does not read them, nothing writes them.
- The interactive Probe Console (`.probe-console.yaml`, console panels).
- `haipipe-probe-creator-agent` (retired to `../_archive/_old/`).
- `fn/` and `ref/` folders: DELETED 2026-07-05 (folder-era procedure docs; git history keeps them). The two live pieces now live with the judgment skill at `../haipipe-probe-review/`: `g2_integrity_check.py` + `probe-caveats-checklist.txt`.

## Status queries

`/haipipe-probe status` (or any status ask): derive from disk — scan `papers/*/0-lifecycle/*/_PROBE/*.md` + `1-probe-plans/README.md` for card statuses; never from a stored console state.
