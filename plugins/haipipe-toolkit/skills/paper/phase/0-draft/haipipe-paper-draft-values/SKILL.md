---
name: haipipe-paper-draft-values
description: "DRAFT-phase value auditor (internal). Walks a stage doc or section for every quantitative claim, decides which already trace to a named source, and REPORTS every remaining hole to haipipe-paper-draft — where it is, that it owes `{VAL:? <what>}`, and which `Q-<Stage>-<n>` will produce the number (or UNOWNED). READ-ONLY: the hub holds the pen for the manuscript and direct topic Q-consumer register; PROBE owns nested entries. Never re-derives, never greps the codebase, never writes anything. Users invoke stage skills (claims, section-edit...), not this skill directly."
argument-hint: "[stage-or-section] [paper-path]"
allowed-tools: Bash, Read, Grep, Glob
metadata:
  version: "0.1.1"
  last_updated: "2026-07-19"
  summary: "DRAFT-phase value auditor: find every number the prose asserts, keep the ones that trace to a named source, and report every remaining hole with the question that owes it. READ-ONLY; the hub writes. Re-derivation is CHECK's; this skill only decides what is owed and who owes it. History: ./CHANGELOG.md."
---

haipipe-paper-draft-values
===========================

The values lane of the DRAFT phase.
Called by `haipipe-paper-draft` while it drafts a stage doc or a section.

One job: **no number leaves DRAFT without a traceable origin or an owner.**


What this skill does NOT do
----------------------------

- It does NOT invent a number, ever, for any reason. An invented number is the single worst failure this bucket can ship: it is invisible in review, survives compile, and is indistinguishable from a real one.
- It does NOT re-derive. Recomputing from the parquet, re-running the regression, checking the arithmetic — that is `haipipe-paper-check-evidence`.
- It does NOT grep the codebase for a method claim. At DRAFT an unverifiable method claim becomes a question, not a search.
- It does NOT WRITE, anywhere. Not the manuscript, not the topic register, and not a nested probe entry. It walks and reports; `haipipe-paper-draft` holds the pen for the first two, and `haipipe-paper-revise-place` places landed numbers later. One writer per file — two lanes editing one sentence is a race.


AUDIT — find every quantitative claim
--------------------------------------

Walk the working `.md` and extract EVERY number the prose asserts, including the ones that do not look like data:

```
sample sizes            N = 89,364 physicians
rates and proportions   6.5% of visits
deltas and comparisons  12.9 more MME
coefficients, SEs, p    beta = 1545.3 (SE 302.8), p < 0.001
model metrics           held-out accuracy, MAE
implicit magnitudes     "roughly a third", "more than doubled", "the majority"
method claims           "Holm-Bonferroni corrected", "cluster-robust SEs",
                        "clustered at the physician" — these assert a NUMBER
                        was computed a particular way, so they are values too
```

The implicit ones matter. "More than doubled" is a numeric claim wearing prose clothes, and it fails exactly the same way.

For each, ask one question: **what named source would a stranger open to confirm it?**

```
has a source     the number appears in a named results file, a landed
                 `#### a-executor`, or a display unit's source data → keep it, and
                 write the source path beside it so REVISE and CHECK can follow it
no source        it came from memory, from an earlier draft, or from nowhere → it
                 is a hole
```


ROUTE — own every remaining hole
---------------------------------

Each sourceless number is REPORTED as one row:

```
<line>  |  <the number, quoted in its sentence>  |  {VAL:? mean MME difference, LBP cohort}  |  owed by: Q-<Stage>-<n> | UNOWNED
```

The hub writes it into the prose as `{VAL:? <what>} [Q-<Stage>-<n>]`.

Two markers, side by side, never fused — the same grammar as `\cite{TOADD} [Q-<Stage>-<n>]`. The `{VAL:?}` says what is missing; the bracket says who will bring it.

Write the `<what>` so a stranger could fill it: name the quantity, the population, and the unit. `{VAL:? x}` is a defective placeholder — nobody can answer it, including you next week.

Finding the right `[Q-<Stage>-<n>]`, cheapest first:

```
1. an EXISTING Q-consumer would produce it        → reuse its id
2. an existing entry asks it                      → add its Q-consumer mapping to the owning topic register
3. nothing would produce it                       → REPORT it to the hub as UNOWNED;
                                                     the hub raises it at Step 4b
```

A bare `{VAL:?}` with no bracket is a defect: a number nobody will ever supply.


The one rule that outranks everything here
-------------------------------------------

When the prose says one number and the source says another, **the source wins**. Never pick the majority reading across sections, and never reconcile two prose numbers against each other — both may be wrong. The parquet or the script decides.

A CSV checked into the repo may predate the canonical data. Prefer the producing task's own results directory over a convenience copy.


Done criteria
--------------

- [ ] Every number in the working `.md` is reported as either naming its source or owing `{VAL:? <what>}`
- [ ] Every `<what>` names quantity + population + unit
- [ ] Every `[Q-<Stage>-<n>]` names a Q-consumer that exists in the stage doc
- [ ] Method claims treated as values, not as prose
- [ ] Nothing invented; nothing written — the report IS the output


Siblings
---------

```
haipipe-paper-draft            the hub that calls this
haipipe-paper-draft-citation   the same shape for sources  (\cite{TOADD} [Q-<Stage>-<n>])
haipipe-paper-draft-display    the same shape for displays (a DR row in the 4-display inbox)
haipipe-paper-probe            answers the questions this skill raised; its harvest
                               greps each value against its named source before accepting it
haipipe-paper-revise-place     puts landed numbers into the prose
haipipe-paper-check-evidence   re-derives them pre-submission
```
