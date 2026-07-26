## QX5 — binary-exposure (trait_l2) high-dose estimates, and the trait form behind the daily-dose odds ratio

### q-executor
Two things, both from the v0618 aggregated export for the low-back-pain cohort, both already inside tables the existing parser reads.
First: for the BINARY agreeableness exposure (trait_l2, score >= 0.75) at SPEC5, emit the coefficient, standard error, exact p-value, and N for each of the three high-dose flags — is_hdld, is_high_mme_daily, is_high_mme_total — so the binary-exposure set matches the binary-exposure total-MME estimate already emitted.
Second: determine definitively which trait form the daily-MME>90 logit odds ratio (odds ratio 1.40479, log-odds 0.339889, SE 0.0766696, N 765,526) was estimated on — the continuous trait_l5 or the binary trait_l2.
That second point exists because an earlier digest is internally contradictory: `tasks/Z01_Display_PhyTraitOpioid/QA/1-opioid-reg-values.md` heads its section 4 "continuous agreeableness (trait_l5)" while its own Caveats state that the logit and the IV are estimated on the binary exposure (trait_l2).
Resolve it from the logit log's own regressor line, not from either prior claim, and say which of the two statements is wrong.
Deliverable: the three binary-exposure flag rows (coef, SE, exact p, N, spec, estimator, source table path), plus a one-line verdict naming the trait form of the logit odds ratio with the log path and line that settles it, in a QA digest.
Accepted: all three rows emitted with provenance and the trait form settled | a named cell is not present in the v0618 export (name which).

### q-consumer
* **Q-Section-2** — daily-MME>90 odds ratio (high-dose binary): "the odds ratio for crossing the CDC 90-MME/day threshold, and whether it is the binary high-agreeableness contrast, so the paragraph's exposure matches the section's primary exposure."
* **Q-Section-7** — binary-exposure high-dose flags: "the three guideline-exceeding flag coefficients on the binary high-agreeableness indicator, so the high-dose paragraph reports the same exposure as the headline estimate rather than mixing the continuous score into a binary-primary section."

### bank binding
**route**: task
**bank**: code · tasks/Z01_Display_PhyTraitOpioid/01_visitlbp_1stpair/
The task EXISTS and its parser already reads the very tables that hold these cells: `main-ols_trait_l2_{is_hdld,is_high_mme_daily,is_high_mme_total}.csv` sit beside the trait_l5 versions it already emits, and the logit block lives in the same log it already opens.
Only the trait_l2 prefix and the logit regressor line are new, so this is a small additive extension, not new estimation.
Depth-2 (code), authorized; v0618 export ONLY — no CMS-server run, no record-level re-estimation; `results/_archive/` and `_old/` are superseded and must be excluded.
**target**: tasks/Z01_Display_PhyTraitOpioid/QA/4-binary-exposure-flags.md
**state**: answered

### a-executor
Both parts landed; all three binary-exposure cells are present in the v0618 export, and the logit's trait form is settled decisively rather than merely consistently.

* Binary exposure trait_l2 (score >= 0.75), SPEC5, window af14d, N 767,736 each — is_hdld coef 0.0044913, SE 0.001669, exact p 7.124e-03, t 2.69; is_high_mme_daily coef 0.0009418, SE 0.0002625, exact p 3.335e-04, t 3.59; is_high_mme_total coef 0.0037999, SE 0.0012259, exact p 1.937e-03, t 3.10. OLS linear probability, vce(cluster npi_id), 90,329 prescriber clusters. [source: tasks/Z01_Display_PhyTraitOpioid/QA/4-binary-exposure-flags.md, part 1]
* Sanity anchor — the same table family's binary mme_ttl cell reproduces at 9.343833, SE 2.543594, N 767,736, matching what QX1 already emitted. [source: same QA]
* VERDICT on the logit trait form — the odds ratio 1.40479 is estimated on the CONTINUOUS trait_l5, settled at the de-interleaved logit log line 321 whose regressor line reads `trait_l5 | .339889 .0766696 4.43`, under the block marker `Logit: is_high_mme_daily ~ trait_l5`. [source: same QA, part 2]
* The BINARY counterpart exists as a separate regression with a different value — log-odds 0.1946979, SE 0.0542613, z 3.59, N 767,561, odds ratio exp(0.1946979) = 1.21494. The .do file loops all three estimators over every outcome crossed with every trait form, so both forms are estimated for every outcome and neither is a fallback for the other. [source: same QA, part 2]

Consequences the consumer must carry.
QX1's parent QA file is internally contradictory on this point: its section-4 HEADING is right and its CAVEAT is wrong where it claims the daily-MME>90 logit is on the binary exposure; that Caveat's other half, that the IV second stage is on trait_l2, is separately correct and independently confirmed from the ivregress command echo.
QA/1 was left `answered` and NOT superseded, because all of its numbers are correct; the record of the contradiction lives in QA/4.
Three estimation samples must not be conflated: the flags are N 767,736, the continuous-score logit is N 765,526, and the binary-exposure logit is N 767,561.
ARCHIVE TRAP, relayed verbatim from the executor: `results/_archive/af14d/tables/` holds a stale `main-ols_trait_l2_*` set under IDENTICAL filenames with is_hdld SPEC5 = -0.0180 at N 150, and `results/_archive/v001_base_full_v0313/` holds an older full run at N 740,682 whose flag values are close enough to be mistaken for the live ones — any figure quoting N 740,682 or N 150 is reading an archived run and must be rejected.
