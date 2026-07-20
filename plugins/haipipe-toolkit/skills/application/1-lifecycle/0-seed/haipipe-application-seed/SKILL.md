---
name: haipipe-application-seed
description: "Stage 0 of the intervention lifecycle (venue-FREE). Answers 'why might this intervention work?' Documents the opportunity, expected impact, audience, channel hunch, mechanism hypothesis. Output: 0-lifecycle/0-seed/0-seed.md + _LOG_0-seed.md (+ 1-probes/ feasibility questions). Markdown only. Modeled on haipipe-paper-seed. Trigger: seed, opportunity, why this intervention, /haipipe-application seed."
argument-hint: "[intervention-path] [intent...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "4.3.0"
  last_updated: "2026-07-18"
  summary: "Seed stage (stage 0, venue-FREE ROOT of the DIKW ladder) — states why this intervention might work before evidence is mature: opportunity, impact, audience, channel hunch, mechanism. DRAFT may WebSearch to orient; PROBE is FEASIBILITY-light (novelty + external-data obtainable); internal-data needs FORWARD to the ladder as [FORWARD -> CLAIMS] pointers. History: ./CHANGELOG.md."
---

Skill: haipipe-application-seed
================================

Stage **0** of the intervention lifecycle: the venue-FREE ROOT the whole DIKW ladder grows from.
It answers one question — why might this intervention work? — and keeps that possibility alive before the evidence is mature.

```text
0-seed            why this might work (the opportunity)   <- THIS STAGE
1a-descriptions   what the data looks like
1b-themes         what patterns/topics emerge
1c-claims         what generalizes (the ledger)
1d-advice         what the evidence advises (the deliverable)
```

The user invokes this skill; it drives DRAFT → PROBE → REVISE → CHECK internally via the `2-phase/` workers.
Read first: `../../../PHILOSOPHY.md`.


## What's special: three things make a seed a seed

**1. Venue-FREE, and the root every rung above depends on.**
The channel hunch (sms / push / in-app / dashboard / email) is context, not a commitment — the venue is pinned AFTER the ladder via `/haipipe-application venue`, and the seed survives that retargeting untouched.
Seed writes `[FORWARD -> CLAIMS]` pointer lines in `_LOG_0-seed.md` for any internal-data need it surfaces (the token stays `CLAIMS` for grep-stability); rung 1a CONSUMES them at its DRAFT open, and an unconsumed pointer fails the 1a gate.

**2. Its probes are FEASIBILITY only — "can this intervention exist at all?"**
Two shapes, both light and both `discovery`-side: is the angle NOVEL (landscape / prior interventions / 查新), and is the EXTERNAL data OBTAINABLE (benchmarks, field norms, outside labeled data)?
Profiling OUR OWN cohort/engagement data is `task` work that belongs to rung 1a — never a seed probe; it leaves as a FORWARD pointer (need + why, no card).
This bounds the seed's cost to the feasibility question and stops it doing ladder evidence work early.

**3. DRAFT may search; PROBE must dispatch.**
Inline WebSearch is legitimate DRAFT fuel — orientation that becomes prose AND buffered `state: planned` question skeletons — but it is NEVER evidence.
The PROBE phase must ALWAYS run the real worker; an inline result has no project-side ledger, so the PROBE phase did not happen.
The invariant is section STATE: `planned` (DRAFT) vs `read` with a resolving `target:` (PROBE), mechanically enforced by the probe checker.


## The four phases, in seed

```text
DRAFT   settle the five content sections with the user (haipipe-application-draft); MAY WebSearch to
        ORIENT (crowded space? prior interventions? benchmark rates?) — weave the result into prose AND
        buffer the feasibility questions as `state: planned` sections; register internal-data needs as
        [FORWARD -> CLAIMS] pointers in _LOG_0-seed.md
PROBE   one worker call — feasibility only (novelty + external-data obtainable); the five-step
        loop raises each question as a SECTION in 1-probes/ and COLLECTS. Inline search is FORBIDDEN here.
        Routing mechanics + seed specifics: ../../../2-phase/1-probe/haipipe-application-probe/SKILL.md
REVISE  tighten wording; weave probe takeaways into Opportunity/Mechanism; the Q-consumer section holds the questions (haipipe-application-revise)
CHECK   exit criteria below → Gate Ledger row; the gate RUNS the probe checker (haipipe-application-check)
```

Seed RECEIVES its feasibility evidence, never PRODUCES it inline: it raises questions; `haipipe-application-probe` binds them via the stake-free collector `Agent(haipipe-probe-q-executor-agent)`, never an orchestrator directly.
If the intervention folder does not exist, route to `/haipipe-application enter <path>` (get-or-create owns scaffolding).
Migrate a legacy per-stage `_PROBE/` card into `1-probes/` in the new shape on first touch only.


## The artifact

`0-lifecycle/0-seed/0-seed.md` — full skeleton in `ref/seed-template.md`:

```text
Opportunity            2-3 sentences: what gap exists, what behavior we want to change
Expected impact        directional estimate ("increase refill adherence by 5-15pp")
Audience               who receives it — a specific subset, not "everyone"
Channel hunch          sms | push | in-app | dashboard | email — a HUNCH, not the venue pin
Mechanism hypothesis   one sentence: why this audience + this content might respond
Q-consumer             feasibility questions raised (novelty + external-data), one `## Q-Seed-<n>` block each
```

Each Q-consumer question is one `## Q-Seed-<n>` block with the same three fields, in order: `Ask` (what it asks), `Why` (which content section above raised it + what breaks if the answer is "no"), `Answer` (`__TO_BE_FILLED__` until the probe resolves; at INTERPRET, the one-line takeaway + the QA-file path). The id carries the stage name (`Seed-`) so the flat probe pool shows which stage raised the question. State is deliberately minimal — a question is OPEN while `Answer` reads `__TO_BE_FILLED__`, ANSWERED once it does not; no `state:` field lives in the seed doc (that machinery belongs to the `1-probes/` file, written at APPROVE).

Sidecar: `_LOG_0-seed.md` (phase journal + the `[FORWARD -> CLAIMS]` pointers).
Formatting: `=====` title / `-----` section rules; content sections use no `#`, Q-consumer questions use `## Q-Seed-<n>`; one sentence per line.
Venue-FREE: the seed survives retargeting; the channel hunch is context, not a commitment.

Done: all five content sections carry real content (not placeholders); Audience and channel hunch are specific; the Q-consumer section raises at least the novelty/landscape question as a `## Q-Seed-<n>` block (Ask/Why/Answer), with internal-data needs appearing only as `[FORWARD -> CLAIMS]` pointers; the probe checker exits clean at the gate.


## Exits

```text
promote -> /haipipe-application ladder   run the 1a-1d sweep (or `descriptions` to start rung-by-rung)
```

End every reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
