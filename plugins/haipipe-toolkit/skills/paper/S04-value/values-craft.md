# Values craft

Craft file for the paper family's values lane, loaded by the DRAFT phase of any stage that declares it in its `stage.md` `craft:` list.
Source: converted from `workers/haipipe-paper-draft-values/SKILL.md` on 2026-08-05 (thin-paper phase 2); it is DATA, not a registered skill.

One job: **no number leaves DRAFT without a traceable origin or an owner.**

This lane is READ-ONLY. It walks and reports; the DRAFT phase holds the pen for the manuscript and the direct topic Q-consumer register, and PROBE owns nested entries.


What this lane does NOT do
---------------------------

- It does NOT invent a number, ever, for any reason. An invented number is the single worst failure this bucket can ship: it is invisible in review, survives compile, and is indistinguishable from a real one.
- It does NOT re-derive. Recomputing from the parquet, re-running the regression, checking the arithmetic — that is the check-evidence craft (`../S06-main/section-edit/check-evidence-craft.md`).
- It does NOT grep the codebase for a method claim. At DRAFT an unverifiable method claim becomes a question, not a search.
- It does NOT WRITE, anywhere. Not the manuscript, not the topic register, and not a nested probe entry. It walks and reports; the DRAFT phase holds the pen for the first two, and the revise-place craft places landed numbers later. One writer per file — two lanes editing one sentence is a race.


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


Where the rest lives
---------------------

Phase dispatch and load order are owned by `board/page-phases/` (DRAFT loads this file last, after the type contract); the sibling lanes are `../S03-literature/citation-craft.md` (sources), `../S05-display/display/draft-craft.md` (displays), `../S06-main/section-edit/revise-place-craft.md` (placement), and `../S06-main/section-edit/check-evidence-craft.md` (re-derivation); the probe loop that answers raised questions is `../haipipe-paper/probe/` (its harvest greps each value against its named source before accepting it).
