# Delivery Need (application side)

How an intervention (message / checklist / dashboard / report) records an evidence gap as a QUESTION, routes it to the bank, and backfills when the answer returns. Application-owned; the paper skill keeps its own copy (`../../paper/wiki/11-delivery-need.md`). There is no cross-skill shared file. The model itself is the probe constitution's (`../../probe/haipipe-probe/SKILL.md`); this file is the application-side routing.

## How the application talks to the bank

A need is a QUESTION the intervention cannot answer itself, RAISED as a SECTION in the flat probe pool `1-probes/PPNN_<topic>.md`. No message bus, no shared contract file. Two channels carry it, and the agent (this session) is the medium:

```
1. Command   a stage's DRAFT raises the questions (a Q-consumer list); APPROVE (human)
             picks which to pursue. `/haipipe-application probe run [PPNN]` hands the
             approved set to haipipe-application-probe (the PROBE phase worker), which
             runs the five-step loop. DISPATCH goes through the stake-free collector
             Agent(haipipe-probe-q-executor-agent) — it calls the task/discovery
             orchestrators in clean context. Stages never call an orchestrator directly.
2. Disk      the question lives as a SECTION in 1-probes/PPNN_<topic>.md; its target:
   (async)   binds by PATH to a QA file the executor wrote in the bank. The section's
             a-consumer holds the answer in the intervention's words; the application
             reads it to backfill. No handshake, just read/write the same section in turn.
```

Who owns which format: the application owns the QUESTION (the section's `## Why` stake + the `q-executor`; the bank only ever sees the stake-free `q-executor`). The bank owns the ANSWER (the QA file's `## Answer`, in general language). A probe is COMMUNICATION, not judgment — it carries a question out and an answer back, and nothing else. A CLAIM's status is written by the author into `1c-claims.md`, never in the probe file.

## When to raise a question

Only when the deliverable requires EVIDENCE the project does not yet have. A framing/format/tone problem stays inside the application lifecycle. An evidence gap becomes a question bound to the bank.

```
stage gap -> a section in 1-probes/ -> haipipe-application-probe five-step loop
          -> collector -> QA file answer -> a-consumer + 1c-claims status backfill
```

## Routes (v5 verbs)

```
claim-related evidence / robustness           -> /haipipe-application probe "<question>"  (a SECTION; run dispatches)
outside context / benchmark (non-claim)       -> /haipipe-discovery <question>
run / data artifact / display materialization -> /haipipe-task <contract>  (or /haipipe-task-for-display)
```

Claim-related evidence goes through a stage's PROBE phase — the section preserves the claim-evidence chain and makes the backlog visible. Non-claim utility work goes straight to the task/discovery door; if the answer later matters, open a section whose `target:` points at the already-written QA file (a T2 REUSE — nothing re-runs).

## Question record

Each open question is one SECTION in `1-probes/PPNN_<topic>.md` (anatomy + states: `haipipe-application/fn/probes.md` and the probe constitution). One `## Why` per FILE, one SECTION per question:

```
serves       which stage / claim the question is FOR
target       a PATH to the answering QA file in the bank (`NEW <path>` while it does not exist)
state        planned | commissioned | answered | read | answered-local | failed  (DERIVED from disk)
q-executor   the question in general language, stake stripped — the ONLY thing sent to the bank, FROZEN
a-consumer   the answer in the intervention's own words, written at harvest
## Why       the STAKE, in intervention vocabulary — NEVER sent to an executor, NEVER copied anywhere
```

There is NO `## Verdict` block and NO G1/G2/G3 review gate. BUILD-lane sections (days-to-weeks work) additionally carry `owner:` · `eta:` · `blocks:` · `cross-project:`, present only at `state: commissioned`.

## Backfill (the return direction)

When the QA file lands, ⑤ INTERPRET writes the `a-consumer`; backfill flows FROM the section:

```
- write the a-consumer (the answer in the intervention's own words), ONLY against an
  answered, non-superseded target
- if the section serves a claim, the AUTHOR flips that claim's STATUS in 1c-claims.md
  (supported | weak | GAP), flipping the C-line AND its Evidence Campaign row — never in
  the probe file; keep the overclaim check (never causal from associational evidence)
- refuted / GAP evidence: drop or reword (never ship an unsupported claim); a weak/GAP
  claim stays with the caveat recorded, and the venue gate reads the campaign against its bar
- the bank NEVER edits application files; the executor writes the QA file, the worker
  harvests it, the application decides how to phrase it for its audience
```

The same landed QA answer can serve both a paper and an application; each reads the same file differently and frames it for its own audience.
