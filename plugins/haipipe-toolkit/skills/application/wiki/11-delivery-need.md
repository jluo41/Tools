# Delivery Need (application side)

How an intervention (message / checklist / dashboard / report) records a gap as a QUESTION, routes it to the right executor, and backfills when the answer returns. Application-owned; the paper skill keeps its own copy (`../../paper/wiki/11-delivery-need.md`). There is no cross-skill shared file.

The MODEL is owned by `../../probe/haipipe-probe/SKILL.md` (v8.0.0, the constitution). This page is the application-side routing view.

## How the application talks to the executors

No message bus, no shared contract file, no mailbox. Two channels carry it:

```
1. Command   a stage's DRAFT hits a gap -> it RAISES A QUESTION as a SECTION in
             1-probes/PPNN_<topic>.md. `/haipipe-application probe run` hands the
             open sections to haipipe-application-probe (the PROBE phase worker),
             which MATCHes the bank first and only then DISPATCHes the section's
             `commission` block -- VERBATIM, and nothing else -- to
               Agent(haipipe-task-orchestrator-agent)
               Agent(haipipe-discovery-orchestrator-agent)
             Stages never dispatch an evidence agent themselves.
             💀 the probe GATEWAY agent is RETIRED; there is no tier in between.

2. Disk      the question lives in the SECTION; the ANSWER lives in the bank, as
   (async)   <task-folder>/QA/<n>-<slug>.md -- written by the EXECUTOR, in general
             language. The section's `target:` POINTS at that file (binding is by
             PATH, never by id: no PP id ever crosses to the bank). The section's
             `reading:` interprets it for this intervention.
             No handshake. Two files, two writers, neither shared.
```

**Who owns which format.** The application owns the QUESTION (the `commission`, in general language) and the MEANING (the `reading`, in intervention language). The executor owns the FACT (its QA file, in general language). Each artifact's shape belongs to the skill that produces it — which is why no shared interface file is needed, and why the evidence stays reusable by every other consumer.

**The pen never crosses the wall.** The probe CAUSES a QA file; the EXECUTOR AUTHORS it. If the PROBE phase finds a bare `results/` with no readable digest, it does not write the digest — it dispatches a digest-only run. An intervention session that writes in the bank has broken LAW 1, whatever it ends up writing.

## When to raise a question

Only when the deliverable requires EVIDENCE the project does not yet have. A framing/format/tone problem stays inside the application lifecycle. A question leaves the application for an executor.

```
stage gap -> a SECTION in 1-probes/ -> MATCH the bank (most stop here) -> commission
          -> the executor's qa gate -> <task-folder>/QA/<n>-<slug>.md -> target: + reading: -> backfill
```

## Routes (v5 verbs)

```
a claim needs evidence / robustness           -> /haipipe-application probe "<question>"  (a SECTION; run binds it)
outside context / benchmark (non-claim)       -> /haipipe-application discover "<question>"
run / data artifact / display materialization -> /haipipe-application task "<contract>"  (or /haipipe-task-for-display)
a question with no intervention behind it     -> /haipipe-task qa "<q>" | /haipipe-discovery qa "<q>"
                                                 (the everyday explore verb; the QA file IS the receipt.
                                                  If it later matters to a claim, open a section whose
                                                  target: points at it — a T2 REUSE, nothing re-runs.)
the claim's STATUS once the answer lands      -> 0-lifecycle/1-claims/1-claims.md   (never a probe field)
```

## The question record

Each open question is one SECTION in a probe file (anatomy + states: `haipipe-application/fn/probes.md`). One file per TOPIC, at `1-probes/PPNN_<topic>.md`; `ls 1-probes/` is the numbering authority.

```
serves       which stage / claim of THIS intervention the question is for
target       a PATH to the answering file -- <task-folder>/QA/<n>-<slug>.md (or `NEW <task-folder>`)
state        planned | commissioned | answered | read | answered-local | failed   (DERIVED from disk)
commission   the question in GENERAL language. THE DISPATCH PAYLOAD, and nothing else is. FROZEN.
reading      what the answer MEANS for this intervention. Written at harvest.
```

Plus ONE `## Why` per FILE — the stake, in intervention vocabulary. **It is never dispatched, never copied, and never leaves the file.**

At `state: commissioned`, a BUILD-lane question (days-to-weeks work) also carries `owner:` · `eta: YYYY-MM-DD` · `blocks:` · `cross-project:`. A future eta PASSES the gate; an eta that has passed with no QA file is a HARD FAIL.

💀 Retired: `planned | dispatched | read | verdicted` as a status set · the `## Verdict` block · `_ASK/` and `_ANS/` mailboxes · the `answers:` field · per-stage `_PROBE/` folders · the `1-probe-plans/` index.

## Backfill (the return direction)

The answer lands as a QA file in the bank. INTERPRET flows FROM it:

```
- write the section's `reading:` -- what this fact MEANS for this intervention
- flip the claim in 1-claims.md: supported -> supported; refuted -> drop or reword
  (never ship a refuted claim); inconclusive -> stays weak/GAP with the caveat recorded
- THE STATUS IS WRITTEN THERE, not in the probe. There is no verdict to copy.
- if support is partial, state the supported scope and the caveat
- the executor NEVER edits application files; the application NEVER edits bank files.
  Two writers, two territories, weeks apart, lock-free.
```

The same landed QA file can serve both a paper and an application, and they may legitimately reach DIFFERENT judgments about their own claims from it. That is not a conflict — the fact is shared, the judgment is private. It is exactly what writing the answer in general language buys.
