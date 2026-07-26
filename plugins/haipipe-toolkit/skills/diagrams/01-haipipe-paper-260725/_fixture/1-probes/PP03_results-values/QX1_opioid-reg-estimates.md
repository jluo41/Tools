## QX1 — opioid-cohort regression estimates for the Results section

### q-executor
From the existing Z01_Display_PhyTraitOpioid task (which already ingests the v0618 regression export), emit the trait_l5 agreeableness estimates the Results section cites.
For low-back-pain, osteoarthritis, headache, and cancer cohorts: the coefficient, standard error, exact p-value, and N on total MME (mme_ttl) at SPEC5, plus the with-rating spec for low-back-pain.
For low-back-pain also: the three high-dose flags (is_hdld, is_high_mme_daily, is_high_mme_total) at SPEC5; the daily-MME>90 logit odds ratio; the county-leave-one-out IV first-stage F-statistic and second-stage coefficient on total MME; and the binary high-agreeableness (score>=0.75) coefficient on total MME.
Deliverable: one row per cited cell — coef, SE, exact p, N, spec, estimator, and its source table path — in a QA digest.
Accepted: every cited cell emitted with provenance | a named cell is not present in the v0618 export.

### q-consumer
* **Q-Section-2** — daily-MME>90 odds ratio (high-dose binary): "the odds ratio for crossing the CDC 90-MME/day threshold per unit of higher perceived agreeableness."
* **Q-Section-3** — gradient ns p-values (headache, cancer): "the p-values for the trait_l5 coefficient on total MME in the headache (+3.57) and cancer (+0.85) cohorts."
* **Q-Section-5** — IV first-stage F + second-stage coefficient (LBP): "the first-stage F-statistic and the second-stage coefficient on total MME from the LBP IV specification, current run."
* **Q-Section-6** — binary-trait robustness coefficient (LBP): "the LBP total-MME coefficient when the exposure is the binary high-agreeableness indicator, current run."

### bank binding
**route**: task
**bank**: code · tasks/Z01_Display_PhyTraitOpioid/
The task EXISTS and already parses the v0618 tables: per-cohort `results/claim_evidence/metrics.json` carry the main coefficients (12.9, 15.3, 0.0064 confirmed on disk), and `table_main_ols_af14d/`, `table_iv_af14d/` hold the raw tables.
But the exact ns p-values (headache/cancer are stored stars-only), the IV first-stage F + second-stage coefficient, and the daily-MME>90 logit OR are NOT yet emitted as fields — so `parse_claim_evidence.py` needs a small extension to emit the full cited set from tables it already reads. That is depth-2 (code), authorized by the user (v0618 only; never re-run the CMS-server Stata).
**target**: tasks/Z01_Display_PhyTraitOpioid/QA/1-opioid-reg-values.md
**state**: answered

### a-executor
Every requested cell is present in the v0618 aggregated export; none deferred, none absent.
Two trait forms appear: trait_l5 is the continuous score on its native 0-1 range, trait_l2 is the binary indicator (score >= 0.75); window af14d; SEs cluster on npi_id.

* Total MME (mme_ttl), continuous trait_l5, SPEC5, by cohort — low-back-pain coef 12.90242, SE 3.676822, exact p 4.50e-04, N 765,701; osteoarthritis coef 4.388944, SE 1.572450, exact p 5.25e-03, N 1,204,607; headache coef 3.567201, SE 3.392841, exact p 0.293, N 200,517 (n.s.); cancer coef 0.849434, SE 0.776446, exact p 0.274, N 1,366,068 (n.s.). [source: tasks/Z01_Display_PhyTraitOpioid/QA/1-opioid-reg-values.md, section 1]
* Low-back-pain with-rating spec (SPEC3, first spec carrying overall_score), trait_l5 — coef 15.33323, SE 3.789557, exact p 5.21e-05, N 765,701. [source: same QA, section 2]
* Low-back-pain high-dose flags, trait_l5, SPEC5 linear probability — is_hdld coef 0.0063799, exact p 9.14e-03; is_high_mme_daily coef 0.0017475, exact p 4.74e-06; is_high_mme_total coef 0.0041937, exact p 2.09e-02; all N 765,701. [source: same QA, section 3]
* Low-back-pain daily-MME>90 logit — odds ratio 1.40479 (95% CI 1.20879 to 1.63258), log-odds coef 0.339889, SE 0.0766696, z 4.43, exact p 9.29e-06, N 765,526. [source: same QA, section 4]
* Low-back-pain county leave-one-out IV (2SLS) — first-stage F 44.8884, second-stage coef on mme_ttl 1545.336, SE 302.8229, z 5.10, exact p 3.34e-07, N 759,163; endogenous variable is trait_l2, instrument agre_county_loo_zip_iv, robust SE. [source: same QA, section 5]
* Low-back-pain binary exposure (trait_l2, score >= 0.75), mme_ttl, SPEC5 — coef 9.343833, SE 2.543594, exact p 2.39e-04, N 767,736. [source: same QA, section 6]

Carried caveats that the consumer must respect.
The exact p-values were recovered at full precision from coef/SE because the estout tables store significance stars only; for the two n.s. cells the recovered p matches the Stata-logged p to three decimals, which cross-validates the method.
The IV second stage and the daily-MME>90 logit are estimated on the BINARY exposure trait_l2, not the continuous trait_l5 — this QA file's own section headings and its Caveats contradict each other on that point, and QX5 was opened to settle it from the logit log's regressor line.
A stale archived run under results/_archive/af14d carries a different low-back-pain SPEC5 coefficient (32.9345); it was NOT used, and the v0618 value 12.90242 is the one matched to the live estout table.
Superseded by nothing; the IV numbers here are extended by QX4, which reports the same estimate under all three standard-error treatments.
