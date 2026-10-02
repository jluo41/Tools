Design methods
==============

An inquiry is designed before any data is read. A design says what is asked, what would
answer it, where it is asked and how strong the answer must be. It is written down first
so that the answer cannot shape the question: a plan fixed before the outcome is seen
separates testing a prediction from fitting a story to results already in hand (Nosek et
al. 2018). Methods differ in which part of the design they fix first: the rung and the
goal, the claim and its target quantity, or the population and its power. Discovery
methods (the other view) say how an answer is found once the design is agreed; these say
how the design itself is made.

The Scope Space renders this file as its Methods › Design methods view. The papers named here
are listed, with their journals, in its Papers view (`insight-papers.md`).


1 · The shared loop
-------------------

```
Ask ─────────▶ Method ──────▶ Spec ─────────────▶ Agree ──────────▶ Run ─────────▶ Page
the question,  choose one,    one work spec per    a different        one run for     the answer at
its words and  fix what it    evidence need,       agent, that did    one question,   its rung, with
its rung       fixes first    written before any   not draft it,      its code reads  its spec and
                              task is read         agrees the spec    the spec        any deviation
                                                                                         │
                       a refused word or an underpowered partition is a new Ask ◀────────┘
```

Only the Method step differs from one method to another: which part of the design it
fixes first and what it must return. Every method keeps the same Ask, the same Spec
fields, the same agreement and the same tests. The Spec is written by a drafter that has
not read the existing tasks, so it says what the question needs, not what is already
built; only then is a task searched, and an existing output is reused only when it is
identical to the spec.


2 · Seven methods
-----------------

Each method is one card in `methods/design/`: its move, what it reads before designing,
what it returns, how the design is tested and where the method comes from; then what the
literature says (its rationale, context, steps, strengths and limitations) beside how it
applies to AI (the agent, its steps, what it returns, how a second agent verifies it, its
risk, and the evidence on AI). The cards fall into three families by what the design
fixes first: the goal (1 and 2), the claim (3 to 5), or the population it is asked on (6
and 7). A card marked `status: future` is a method to add later; no question is designed
that way yet. The Design methods view shows the cards, each with its papers
(`insight-papers.md`, `group` = the method).

| family | method | card |
|---|---|---|
| From the goal | By rung | methods/design/01-by-rung.md |
| From the goal | By goal-question-metric | methods/design/02-by-goal-question-metric.md |
| From the claim | By estimand | methods/design/03-by-estimand.md |
| From the claim | By target trial | methods/design/04-by-target-trial.md |
| From the claim | By analysis plan | methods/design/05-by-analysis-plan.md |
| From the population | By partition and power | methods/design/06-by-partition-and-power.md |
| From the population | By protocol reuse | methods/design/07-by-protocol-reuse.md |

The workbench's hard rules each come from one of these methods (ours). **One run, one
question** is By analysis plan: a run that answers several questions lets its choices
drift toward whichever one comes out. **Every word of the ask is covered** by a need or
refused: By goal-question-metric, where every measure has a question and every question a
goal. **Propose before search** (the spec is drafted before any task is read) is By
analysis plan applied to code: the plan is fixed before what exists can shape it.
**Reuse only on an identical output** is By protocol reuse: the same protocol, unchanged,
or it is a new study. **A causal ask is refused at Data and Information** is By rung, and
a causal ask that is kept goes to Knowledge, where By target trial says what it needs.
The partition list and the power rule, decided before any outcome is seen, are By
partition and power; whether partitions differ is its cross-partition heterogeneity
question, never a comparison of p-values.


3 · How a design is tested
--------------------------

| test | asks | when | source |
|---|---|---|---|
| T0 Covered | every content word of the ask maps to a need or a refusal | now · Spec | requirements traceability (Gotel & Finkelstein 1994) |
| T1 Specified | each need names partition, unit, measure, grouping, uncertainty, rivals, output | now · Spec | analysis plan content (Gamble et al. 2017; Chan et al. 2013) |
| T2 Agreed | a different agent that did not draft the spec agrees it | now · Agree | review before results (Chambers 2013) |
| T3 Powered | each partition's minimum detectable effect is at most the smallest effect that matters | now · Agree | power analysis (Cohen 1992; Lakens 2022) |
| T4 Reproduced | the same protocol on another dataset gives a comparable answer | in use | replication across samples (Open Science Collaboration 2015) |

T0 to T3 are judged on the design alone, before any outcome is read; only T4 needs a
second dataset. A spec that fails T0 or T1 goes back to its drafter; a partition that
fails T3 keeps its question but gives no answer there. Each method's tests are on its
card.


4 · What the evidence says about the methods
--------------------------------------------

- Fixing the plan first changes what is found: large heart, lung and blood trials that
  showed a benefit fell from 17 of 30 before 2000 to 2 of 25 after, when outcomes had to
  be registered in advance (Kaplan & Irvin 2015). Registered Reports, reviewed before
  results exist, had 44% positive results against 96% in the standard literature (Scheel
  et al. 2021).
- A plan is not kept by itself: of 27 preregistered studies, 2 had no deviations and 9
  disclosed none of theirs (Claesen et al. 2021). A deviation log is part of the design.
- Freedom in the analysis inflates false positives far past the nominal rate (Simmons et
  al. 2011), and choices that depend on the data are a problem even with no fishing
  (Gelman & Loken 2014). 29 teams given the same data and question reported odds ratios
  from 0.89 to 2.93 (Silberzahn et al. 2018).
- Subgroup claims rarely hold: of 117 in trial abstracts, 39% had a significant
  interaction test, and the 5 that were tested again all failed to corroborate (Wallach
  et al. 2017). Small samples make a significant result less likely to be true (Button et
  al. 2013).
- The question is often unclear: of 255 trials in leading journals, none stated every
  part of its estimand (Cro et al. 2022).
- One protocol on many databases does not give one answer: holding the design fixed,
  estimates ran from a significant decrease to a significant increase in risk across 10
  databases for 21% of drug-outcome pairs (Madigan et al. 2013).
- Language model agents given open research questions were often limited to basic
  analyses (Gu et al. 2024, BLADE). Models drafting statistical analysis plans scored
  67% to 72% on statistical items and sometimes invented sensitivity analyses (Jafari et
  al. 2026, a preprint).

No study compares these design methods head to head, or tests an agent that drafts a
spec without reading the existing tasks. The workbench is itself a bet: does a spec
written blind, agreed by a second agent and powered per partition before any outcome is
read give answers that reproduce on the next dataset (T4) more often than a design built
from the tasks already in hand?
