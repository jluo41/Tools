# display02-discretion-gradient

## Reader Takeaway
The agreeableness->opioid signal fires in high-discretion cohorts (LBP +12.90, osteo +4.39 ***) and goes flat where prescribing is locked (headache +3.57, cancer +0.85 ns).

## Claim Supported
C3 (discretion gradient). (Beyond-the-rating / SPEC ladder now lives in Table 2.)

## Evidence Source
- PARSE-not-recompute over v0618 ALREADY-AGGREGATED regression CSVs (laptop-safe aggregate outputs; no raw .dta / micro-data read).
- R01 = `_WorkSpace/0-CMS-Store/Report-From-CMS-Server/Regression-Result-v0618/R01_Reg_TraitOpioid`.
- Per-cohort trait_l5 SPEC5 -> mme_ttl, af14d window, from `main-ols_trait_l5_mme_ttl.csv` (column (5)); 95% CI = coef +-1.96*SE:
  - LBP `D01-reg_visitlbp_1stpair/.../run_reg_visitlbp_1stpair_af14d_ols` +12.9024 (3.6768) *** N=765,701 [HIGH discretion]
  - Osteo `D04-reg_visitosteo_1stpair_v0622/.../run_reg_visitosteo_1stpair_af14d_ols` +4.3889 (1.5724) *** N=1,204,607 [HIGH discretion]
  - Headache `D03-reg_visitheadache_1stpair/.../run_reg_visitheadache_1stpair_af14d_ols` +3.5672 (3.3928) ns N=200,517 [protocolized]
  - Cancer `D02-reg_visitcancer_1stpair/.../run_reg_visitcancer_1stpair_af14d_ols` +0.8494 (0.7764) ns N=1,366,068 [guideline-indicated]
- Cross-domain placebo (caption only, binary outcome, different scale, NOT on the MME axis): T2D metformin -0.0007 ns, N~1.2M (parent-confirmed).
- Rebuild: `source/gen_discretion_gradient.py` (+ `source/paper_plot_style.py`) via the `haipipe-paper-display-figure` skill (matplotlib, reproducible; parses the CSVs at runtime, no hardcoded coefficients). Writes `assets/figure.{pdf,png}`.
- Last checked: 2026-06-24 (all 4 coefs/SEs/N re-verified against the CSVs).

## Placement
- Main; Results (Figure 4).

## Caption Job
State the gradient (LBP +12.90 / osteo +4.39 sig; headache 3.57 / cancer 0.85 ns) with 95% CIs and the discretion ordering; metformin as a one-clause cross-domain placebo aside (binary, different scale); associational throughout.

## Fragility
- 95% CIs plotted (coef +-1.96*SE from the aggregated CSV SEs).
- IV is on trait_l2 only (not trait_l5), directional-only; NOT shown here (see display04 Panel C).
- Metformin contrast is a binary prescribing outcome, deliberately kept off the MME axis and out of the image (caption only).

## Status
rendered (SINGLE clean forest panel; 95% CIs; no baked text/title/caption/metformin-box; parse-not-recompute v0618; via haipipe-paper-display-figure).
