DIKW boundaries + worked examples
==================================

The canonical "what belongs in which card, where the line between them is, and
what a good one looks like." The per-type reviewers
(`card-reviewer-{data,information,knowledge,wisdom}-agent`) enforce THIS doc +
the format in `insight-md-schema.md`. The creators follow it.

The ladder (each step is a PROMOTION, not a rename):

```
  🟦 D observe   →   🟩 I pattern   →   🟨 K believe   →   🟧 W act
  one source         ≥2 D, a            a probe            a K, plus
  of facts           regularity         confirms it        an action
```

Two hard gates on the ladder:

```
1. 🟩 I → 🟨 K  REQUIRES a controlled comparison (a probe: arms × seeds × test).
   No probe → no K. A regression / observation gives strong I, NEVER K.
2. source axis:  🟦 D + 🟩 I  describe (observational — from task results /
   a confirmed probe's observations);  🟨 K + 🟧 W  prescribe (normative —
   from a confirmed D_probe claim).
```


Per-layer boundary
==================

```
🟦 D — Data — "what we observed"
  IS:      facts + numbers from ONE source, no interpretation.
  IS NOT:  a cross-source pattern (→I) · a belief (→K) · an action (→W).
  line→I:  one observation = D; the SAME effect across ≥ 2 observations = I.
  source:  a confirmed probe (probe.yaml result + metrics.json) / task results.
  style:   ## Observation (facts only) · ## Numbers (table) · ## Caveats (verbatim).

🟩 I — Information — "what patterns emerged"
  IS:      a regularity visible across ≥ 2 D cards.
  IS NOT:  a single observation (→D) · a committed belief (→K).
  line→K:  I says "the data TENDS to show X"; K COMMITS "X is true (scope, conf)".
  gate:    needs ≥ 2 D cards citing the same effect / direction.
  style:   ## Pattern statement · ## Evidence (table, ≥2 D) · ## Counter-evidence.

🟨 K — Knowledge — "what we believe is true"
  IS:      a validated belief with explicit scope + confidence; ALL counter-
           evidence listed (cherry-picking = a violation).
  IS NOT:  a pattern (→I) · an action (→W).
  ★ gate:  promotion I→K REQUIRES a controlled comparison (a probe). No probe, no K.
  source:  the CONFIRMED probe's `claim` (the probe IS that comparison); cite
           supporting I cards in the body where they exist.
  line→W:  K is the belief; W is what to DO about it.
  style:   ## Claim · ## Supporting evidence · ## Counter-evidence (ALL) ·
           ## Confidence rationale · ## Scope.

🟧 W — Wisdom — "what we should do next"
  IS:      an ACTIONABLE recommendation derived from ≥ 1 K.
  IS NOT:  a restatement of the belief (→K) · a vague "should think about X".
  line:    must pass "could I write the exact command / decision?". W decays.
  style:   ## Recommendation · ## How to act (exact step) · ## Why now · ## Decay condition.
```


Worked example — one coherent FiLM thread, cross-referenced
===========================================================

`D01 → I01 → K01 → W01`, each a complete, schema-valid card. Note how the
`sources` / `ref_by` chain links them, and how each card stays inside its
boundary (D never interprets; I needs ≥2 D; K needs the probe; W is a command).

--- 🟦 insights/D_data/D01_film_val.md ---

```markdown
---
id:        D01
layer:     D
tags:      [film, conditioning, val]
status:    active
created:   2026-05-24
updated:   2026-05-24
source_id: P.A01
headline:  "val: FiLM Δ -0.98 ± 0.27 mg/dL MAE (p=0.018, n=3)"
sources:   [P.A01]
ref_by:    [I01]
---

# D01: FiLM lowers val MAE vs baseline (n=3)

## Observation
On AIData v3, validation split, the FiLM-conditioned forecaster shows lower MAE
than the matched baseline across 3 seeds. Reported from confirmed probe P.A01.

## Numbers
| Metric  | Value              | Split | Source       |
|---------|--------------------|-------|--------------|
| MAE Δ   | -0.98 ± 0.27 mg/dL | val   | P.A01 result |
| p-value | 0.018 (paired-t)   | val   | P.A01 result |
| seeds   | 3 (all negative Δ) | val   | P.A01 result |

## Caveats
- FiLM arm has +20% params vs baseline — scale confound (verbatim from P.A01).
```

--- 🟩 insights/I_information/I01_film_indist.md ---

```markdown
---
id:        I01
layer:     I
tags:      [film, conditioning, in_dist]
status:    active
created:   2026-05-25
updated:   2026-05-25
pattern:   repeated_effect
n_obs:     2
direction: negative
sources:   [D01, D03]
ref_by:    []          # K01 sources the probe P.A01; it cites I01 as supporting evidence in its body
---

# I01: FiLM lowers MAE on in-distribution splits

## Pattern statement
Across in-distribution splits (val, test-id), FiLM lowers MAE relative to the
matched baseline — same direction in every observed seed.

## Evidence
| Source | Metric / Split | Δ            | Direction |
|--------|----------------|--------------|-----------|
| D01    | MAE / val      | -0.98 ± 0.27 | negative  |
| D03    | MAE / test-id  | -0.71 ± 0.30 | negative  |

## Counter-evidence
- No in-dist split shows a positive Δ. test-od not yet observed (see W01).
```

--- 🟨 insights/K_knowledge/K01_film_indist.md ---

```markdown
---
id:        K01
layer:     K
tags:      [film, conditioning, in_dist]
status:    active
created:   2026-05-26
updated:   2026-05-26
claim:     "FiLM conditioning improves in-distribution CGM forecasting (lower MAE)"
confidence: medium
sources:   [P.A01]
ref_by:    [W01]
---

# K01: FiLM improves in-distribution forecasting

## Claim
FiLM conditioning lowers MAE on in-distribution splits (val, test-id) versus a
matched baseline. Holds in every observed seed; established by the controlled
probe P.A01 (arms × 3 seeds, paired-t).

## Supporting evidence
- I01: repeated negative Δ across val (D01) + test-id (D03).

## Counter-evidence
- +20% params in the FiLM arm → scale confound not yet ruled out.
- test-od (out-of-distribution) not yet measured.

## Confidence rationale
medium — direction is clean and significant in-distribution, but the scale
confound blocks a clean causal claim. Param-matching (W01) would raise it to high.

## Scope
In-distribution only (val, test-id); AIData v3; current training schedule.
```

--- 🟧 insights/W_wisdom/W01_param_matched.md ---

```markdown
---
id:        W01
layer:     W
tags:      [film, conditioning, next_experiment]
status:    active
created:   2026-05-26
updated:   2026-05-26
rec:       "Run a param-matched FiLM re-test to isolate conditioning from scale"
type:      next_experiment
cost:      medium
sources:   [K01]
ref_by:    []
---

# W01: Param-matched FiLM re-test

## Recommendation
Scaffold a probe with a size-reduced baseline (matched to FiLM params) vs FiLM,
n=3 seeds, eval on val / test-id / test-od. Isolates conditioning from the +20%
param confound flagged in K01.

## How to act
    /haipipe-probe design new 12 --title "Param-matched FiLM re-test" \
        --hypothesis "FiLM in-dist benefit survives param-matching"
    /haipipe-probe bridge 12

## Why now
K01 is the strongest in-distribution belief, but its scale confound blocks a
clean paper claim and gates further FiLM work.

## Decay condition
- A param-matched result lands (this W becomes acted_on), OR
- the project pivots away from patient-feature conditioning.
```
