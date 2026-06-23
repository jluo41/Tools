DIKW boundaries + worked examples
==================================

The canonical "what belongs in which card, where the line between them is, and
what a good one looks like." The per-type reviewers
(`card-reviewer-{data,information,knowledge,wisdom}-agent`) enforce THIS doc +
the format in `insight-md-schema.md`. The creators follow it.

The one cut the whole model turns on:

```
  in-sample DESCRIPTION                 out-of-sample GENERALIZATION
  ─────────────────────────             ─────────────────────────────
  🟦 D  what one dataset looks like      🟨 K  does the pattern hold beyond
  🟩 I  what pattern is IN that data           this sample (population / future)
                                         🟧 W  what to do, given K's confidence
```

D and I describe a sample. They do not claim anything beyond it. K is the leap:
it claims a pattern generalizes, and it carries the confidence of that leap. W
acts on K, tuning how bold or cautious the action is to K's confidence.

The ladder (each step is a PROMOTION, not a rename):

```
  🟦 D describe      →   🟩 I describe      →   🟨 K generalize     →   🟧 W act
  one dataset's          a pattern inside        does it hold beyond     a K-backed action,
  shape (named data)     that same dataset       the sample (+conf)      risk-tuned to conf
```


The two rules that define the model
====================================

```
1. DATASET RULE (D, I).  Every D and every I names the dataset it describes
   (frontmatter `dataset:`). D and I are statements ABOUT one dataset. A D or I
   that cannot name its dataset is malformed. I cites the D card(s) describing
   the same dataset.

2. GENERALIZATION RULE (K).  The inferential quantities — p-value, confidence
   interval, significance, confidence level — live at K, NEVER at D or I. They
   are not descriptions of the sample; they are claims about whether the
   sample's pattern generalizes. Wherever you see a p-value or a confidence
   level, you are looking at a K, not an I.
```

A direct consequence: a single regression output is SPLIT across two layers.

```
regression / model fit produces:
  coefficient, direction, magnitude, in-sample shape   →  🟩 I  (the pattern in this dataset)
  p-value, CI, significance stars, a confidence level  →  🟨 K  (does it generalize)
```

What decides the layer is the KIND of claim, not which tool emitted the number.
A point estimate that describes the sample is I. An inferential statement that
the estimate holds beyond the sample is K.


K has no admission gate
=======================

The old model gated I→K behind "a controlled-comparison probe" (no probe, no K).
That gate is removed. K is not a privilege earned by an experiment; K is simply
the layer where a generalization claim is recorded, together with how much we
believe it.

```
- A high-confidence claim ("X generalizes, p<.001, holds across every subgroup") is K.
- A low-confidence claim ("X might generalize, but only in aggregate, weak") is K.
- A negative claim ("X does NOT generalize here, ns") is K — failed generalization
  is knowledge too.
- An uncertain claim is STILL recorded. Low confidence is a value of the
  `confidence` field, not a reason to withhold the card.
```

`confidence` is the load-bearing field of a K card. It is never dropped and
never implied. Every K states its confidence explicitly (high / medium / low /
contested), and the body justifies it.

Two tiers of generalization — confidence should reflect which one you have:

```
  statistical generalization   p<.05 / CI excludes the null  → holds in the
                               population the sample was drawn from, UNDER the
                               model's assumptions. Often medium on its own.
  robust generalization        the pattern survives across subgroups, cohorts,
                               time windows, specifications → stronger, earns
                               higher confidence. This is the cross-subgroup
                               consistency check, not just one p-value.
```

A lone p-value is the weaker tier: it generalizes to the population under iid-ish
assumptions, not literally to future or external data. Robustness across
subgroups is what pushes confidence toward high.


The causal axis (orthogonal to confidence)
===========================================

A K answers two SEPARATE questions, and a card must not let one stand in for the
other:

```
confidence  (generalization): does the pattern hold beyond the sample?   high/med/low
claim_type  (causation):      is it a CAUSAL effect, or only an association?  causal/associational
```

These are independent. A cleanly significant, subgroup-robust association can be
high-confidence AND still `associational`. A weak-instrument 2SLS coefficient that
"reaches significance" is NOT causal — weak-IV is not identification; that K stays
`associational` and says so.

```
claim_type: associational   the DEFAULT. Records a population-level association.
                            p<.05 / robustness raise its `confidence`, NOT its causal status.
claim_type: causal          allowed ONLY when `## Generalization basis` names a valid
                            identification: an RCT, a strong+valid instrument (first-stage
                            F well above weak-IV thresholds, exclusion argued), RDD,
                            DiD with parallel-trends shown, etc. State the strategy and
                            its assumptions; if any fails, downgrade to associational.
```

Rule of thumb: confidence is about the SAMPLE-to-population leap; claim_type is
about the correlation-to-causation leap. Never upgrade claim_type because
confidence is high, and never lower confidence just because a claim is only
associational.


Documentation is not a separate step
=====================================

Every K gets written down regardless of its confidence. "Document it" does not
add a layer or a gate; it is just the rule that a weak or negative K is recorded
the same as a strong one. The archive's value is that it holds what we tried and
what did not generalize, not only the wins. Withholding a low-confidence K is how
an archive starts lying by omission.


Per-layer boundary
==================

```
🟦 D — Data — "what this dataset looks like"
  IS:      the composition / structure / profile of ONE named dataset: sample
           size, units, variable definitions, distributions, coverage, balance
           across arms or groups, missingness, how the cohort was constructed.
  IS NOT:  a pattern between variables (→I) · a generalization (→K) · an action (→W).
           NO p-value, NO CI, NO significance — those are K.
  names:   `dataset:` (required) + `source_id` (the artifact that produced the
           profile: `task:<id>`, `probe:<id>`, `discover:<id>`, `lit:<citekey>`).
  line→I:  D says what the data IS; I says what pattern is found IN it.
  style:   ## Profile (facts about the dataset) · ## Numbers (counts/shares, no
           inference) · ## Caveats (verbatim).

🟩 I — Information — "the pattern inside one dataset"
  IS:      an in-sample regularity within ONE named dataset: an association, a
           direction, a magnitude, a contrast, a shape. Descriptive of the
           sample at hand.
  IS NOT:  a profile of the data (→D) · a claim it generalizes (→K). NO p-value,
           NO CI, NO confidence level — the moment you assert it holds beyond the
           sample, you are at K.
  names:   `dataset:` (required, same dataset as its D) + `sources:` cite the D
           card(s) for that dataset.
  line→K:  I says "in THIS data, X and Y move together, Δ=...". K says "X→Y
           generalizes beyond this sample (scope, confidence)".
  style:   ## Pattern statement · ## Evidence (in-sample Δ / direction, NO p/CI)
           · ## Counter-evidence.

🟨 K — Knowledge — "does the pattern generalize (and how sure are we)"
  IS:      a generalization claim: the in-sample pattern is asserted to hold
           beyond the sample — to the population, to other cohorts, to future
           data — WITH an explicit confidence. Includes negative claims ("does
           not generalize") and low-confidence claims.
  IS NOT:  an in-sample pattern (→I) · an action (→W).
  NO gate: K does NOT require a probe or an experiment. It requires a
           generalization basis (the inferential evidence) and an honest
           confidence. The basis can be a significance test, a CI, robustness
           across subgroups, or a vetted external claim.
  source:  the I card(s) whose pattern is claimed to generalize, plus the
           inferential basis that produced p / CI / confidence. Cite the
           dataset(s) through the I chain.
  confidence: REQUIRED, explicit, justified. high / medium / low / contested.
           A negative K ("X does not generalize, ns") sets confidence to what the
           null supports and states the null in the headline so a reader never
           mistakes it for an effect.
  line→W:  K is the belief (with its confidence); W is what to DO about it.
  style:   ## Claim · ## Generalization basis (p / CI / robustness here) ·
           ## Counter-evidence (ALL) · ## Confidence rationale · ## Scope.

🟧 W — Wisdom — "what to do, tuned to K's confidence"
  IS:      an ACTIONABLE recommendation derived from ≥1 K, whose aggressiveness
           is set by the cited K's confidence.
  IS NOT:  a restatement of the belief (→K) · a vague "should think about X".
  reads conf: high-confidence K → a bold action is warranted. low-confidence K →
           a conservative / hedged action, a small pilot, a "do not yet do X", or
           a flag to gather more evidence. A low-confidence K is still actionable;
           it just changes the posture.
  records: the source K, its confidence AT THE TIME, and WHY that confidence
           justifies this posture (provenance), so a later reader can audit the
           decision.
  line:    must pass "could I write the exact command / decision?". W decays.
  style:   ## Recommendation · ## How to act (exact step) · ## Risk posture (why
           this boldness, given the K confidence) · ## Why now · ## Decay condition.
```


Worked example — one regression, split across I and K, then acted on
=====================================================================

`D01 → I01 → K01 → W01`, each a complete, schema-valid card. Note how the SAME
regression produces an I (the in-sample estimate) and a K (the generalization),
how every D/I names its dataset, and how the p-value lives only at K.

--- 🟦 insights/D_data/D01_cohortA_profile.md ---

```markdown
---
id:        D01
layer:     D
tags:      [cohortA, opioid, profile]
status:    active
created:   2026-06-22
updated:   2026-06-22
dataset:   VisitOsteo_1stPair_af14d
source_id: probe:P.0622-AO-OST
headline:  "VisitOsteo 1st-pair: N=1,204,607 encounters, 2015-2020 Medicare"
sources:   [probe:P.0622-AO-OST]
ref_by:    [I01]
---

# D01: VisitOsteo first-pair cohort profile

## Profile
The osteoarthritis first-pair cohort: Medicare encounters 2015-2020, one row per
first physician-patient pair. Built by the Z01 display task from the v0618 CMS run.

## Numbers
| Metric                                | Value              | Source                         |
|---------------------------------------|--------------------|--------------------------------|
| encounters (N)                        | 1,204,607          | Z01 metrics.json               |
| trait coverage (Agreeableness scored) | review-inferred    | Z01 metrics.json               |
| window                                | af14d              | run config                     |

## Caveats
- Review-inferred Agreeableness; cohort restricted to first pairs.

## Change log
- 2026-06-22 — created from probe:P.0622-AO-OST.
```

--- 🟩 insights/I_information/I01_osteo_assoc.md ---

```markdown
---
id:        I01
layer:     I
tags:      [cohortA, opioid, agreeableness]
status:    active
created:   2026-06-22
updated:   2026-06-22
dataset:   VisitOsteo_1stPair_af14d
pattern:   statistical_regularity
direction: positive
sources:   [D01]
ref_by:    [K01]
---

# I01: In osteo, agreeableness and opioid intensity move together

## Pattern statement
Within the VisitOsteo first-pair dataset, higher perceived Agreeableness
co-occurs with higher total MME. The SPEC5 point estimate is +4.39 (continuous
trait), concentrated on the intensive margin. This is a description of THIS
sample, not a claim about other data.

## Evidence
| Source | Metric / Split                 | Δ or Value         | Direction  |
|--------|--------------------------------|--------------------|------------|
| D01    | SPEC5 trait_l5 on mme_ttl      | +4.39              | positive   |
| D01    | margin                         | intensive >> ext.  | positive   |

## Counter-evidence
- No in-sample sign reversal across the spec progression.
```

--- 🟨 insights/K_knowledge/K01_osteo_generalizes.md ---

```markdown
---
id:        K01
layer:     K
tags:      [cohortA, opioid, agreeableness]
status:    active
created:   2026-06-22
updated:   2026-06-22
claim:     "Agreeableness->opioid intensity generalizes in the osteo population (assoc., medium)"
confidence: medium
sources:   [I01]
ref_by:    [W01]
---

# K01: The osteo association generalizes to its population (associational)

## Claim
The positive Agreeableness→opioid-intensity association found in the osteo sample
(I01) holds in the population the sample was drawn from. Associational, not causal.

## Generalization basis
- Statistical: SPEC5 coefficient significant at p<.001, cluster(npi_id) SE.
- Robustness (partial): same sign and significance across the spec progression.
- NOT yet tested: cross-cohort transfer (a separate, higher K).

## Counter-evidence
- Causal identification fails: the IV is weak (first-stage F~1.1 under physician
  clustering), non-identifying. The claim is associational only.

## Confidence rationale
medium — statistically clean in-population, but no causal identification and no
cross-cohort robustness yet. A cross-cohort consistency check would raise it.

## Scope
US Medicare VisitOsteo first-pair 2015-2020; review-inferred Agreeableness; OLS
SPEC5 cluster(npi_id); total MME outcome. Population-level association.

## Change log
- 2026-06-22 — created from I01 (osteo in-sample pattern) + the SPEC5 inference.
```

--- 🟧 insights/W_wisdom/W01_interaction_test.md ---

```markdown
---
id:        W01
type:      Insight Wisdom
layer:     W
title:     "Test the cross-cohort gradient as a slope, not an eyeball"
description: "K01 generalizes in-population but not yet across cohorts; test it."
tags:      [cohortA, opioid, next_experiment]
status:    active
created:   2026-06-22
updated:   2026-06-22
rec:       "Run a trait x discretion-tier interaction to test cross-cohort generalization"
rec_type:  next_experiment
cost:      medium
sources:   [K01]
ref_by:    []
---

# W01: Test the discretion gradient as a slope

## Recommendation
Pool the cohorts (or interact trait × discretion-tier) and test the interaction
coefficient directly, so "discretion-gated" becomes a tested slope rather than
four coefficients read side by side.

## How to act
    /haipipe-probe plan new --title "trait x discretion-tier interaction" \
        --claim "the trait->opioid slope declines with clinical discretion"

## Risk posture
K01 is medium-confidence (in-population only, no cross-cohort robustness yet). So
this is a conservative next step: a confirmatory test before any cross-cohort
claim is published, NOT a green light to assert the gradient. The medium
confidence is exactly why we test rather than assert.

## Why now
The cross-cohort story is the load-bearing claim, and it currently rests on an
eyeballed ordering. The interaction test is the cheapest way to earn the higher
(robust) tier of confidence.

## Decay condition
- A pooled interaction estimate lands, OR the project drops the cross-cohort framing.
```


Negative and uncertain K — record them, do not withhold
========================================================

```
negative ("does not generalize")  → a valid K. confidence is whatever the null
    supports. Headline MUST state the null ("ns; no association on the primary
    outcome") so it is never mistaken for an effect. Example:
      "K07: agreeableness->opioid does NOT generalize to cancer (ns on total MME,
       p>=.10); a weak high-dose tail survives — record both."
low-confidence ("might generalize, weak")  → a valid K. Set confidence: low and
    say in the rationale exactly what is missing (no robustness, single
    specification, small effect). It still drives a CONSERVATIVE W.
contested  → use when two credible analyses disagree; set status: contested and
    cite both sides in counter-evidence.
```

The point of recording weak and negative K is that W can use them: a low or
negative K is what justifies a cautious action, a "do not do X yet", or a request
for more evidence. An archive that only keeps strong K cannot support cautious
decisions.


Two granularity calls the layers leave open
============================================

```
1. NULL results and the I layer.  For a non-significant result, the I card (the
   in-sample point estimate, e.g. "+3.57, ns-flag-not-here") is OPTIONAL — file it
   only if the bare magnitude is itself reusable. The load-bearing record of a null
   is the NEGATIVE K ("does not generalize, ns"). Never let a null masquerade as an
   I "pattern"; if you skip the null I, go straight to the negative K.

2. Per-population K vs cross-population K.  These are DIFFERENT reusable units and
   both are valid:
     - per-population K: "the pattern generalizes IN dataset X's population"
       (one I, one significance basis). Confidence usually medium (statistical tier).
     - cross-population K: "the pattern holds ACROSS datasets / subgroups / time"
       (several I, a robustness basis). This is the robust tier and earns higher
       confidence. It is NOT a restatement of the per-population K — it is the
       stronger, separately-reusable belief.
   File the cross-population K whenever a robustness reading exists. File the
   per-population K when that single-dataset generalization is itself cited
   downstream; otherwise merging the weak per-population nulls into one negative
   cross-population K is acceptable (apply `card-granularity.md`).

   K->K SYNTHESIS EDGE. A cross-population (synthesis) K MAY list its sibling
   per-population K cards in `sources` (alongside the I cards it generalizes). This
   same-layer K->K edge is LEGITIMATE, not a layer-skip: the synthesis K aggregates
   the per-population verdicts into a higher belief. Two rules: (a) it must add a
   NEW reusable belief (the cross-population regularity), never merely restate one
   sibling; (b) keep the graph symmetric — every sibling K it sources lists the
   synthesis K in its `ref_by`.
```
