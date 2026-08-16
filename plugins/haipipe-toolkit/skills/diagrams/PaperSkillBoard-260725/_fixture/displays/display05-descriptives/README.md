# display05-descriptives

## Reader Takeaway
Who is in the five analytic cohorts and how Agreeableness, prescribing, and key patient characteristics distribute across them — the comparability check behind the C0 data anchor.

## Claim Supported
C0 — the data anchor (cohort descriptives / Table 1), now multi-cohort.

## Evidence Source
- Source: v0618 aggregated data-pipeline logs (`Report-From-CMS-Server`), PARSED not recomputed.
- Probe: `probes/0624_cohort-descriptives` (P.0624-CD) — see its `evidence.md` for the full gathered panel + funnel + comparability read + osteo caveat.
- Cohorts: LBP (N=773,566), Cancer (1,385,300), Headache (203,426), T2D (1,208,934), Osteo (~1.21M, PARTIAL).
- Asset: `assets/table-body.tex` (tabular); `float.tex` (table env + caption + funnel/notes).
- Last checked: 2026-06-24.

## Placement
- Main; Results / Methods (Table 1).

## Caption Job
Describe the five cohorts side by side; state N + build funnel and the exposure/outcome summary without interpreting. Outcome rows are not read across the opioid/T2D boundary.

## Fragility
- Osteo is PARTIAL — regression-stage logs only (no data-pipeline build folder in this export), so it carries no build funnel and its N is the regression N. Flagged with `$^{\dagger}$` in-table. A comparable osteo funnel needs a server-side osteo data-pipeline re-export.
- Osteo fills sourced from the D04 af14d_ols `run-1-ols-progressive.txt`: White % = mean `bene_race_white` = 0.870 (87.0), age (mean+SD), female, LIS, dual, Agreeableness from `summarize`; **Any opioid Rx % = 6.99 from `tab is_opioid_rx`** (added fill pass 2). Osteo `Unique patients` and `HDLD %` are NOT summarized at the regression stage (no `summarize is_hdld`, no patient-distinct count; only the npi cluster count ~97,027 is available, shown as physicians) → RED `TODO`.
- **Three-state cells now (fill pass 2):** every in-domain cell is a sourced number, `n/a` (cross-domain), or a RED `\textcolor{red}{\textbf{TODO}}` — there are no plain `--` left for classified cells. RED-TODO = genuinely absent from every aggregated v0618 export, pending a server descriptives re-export. The TODO inventory: Headache+T2D age SD; T2D White %; Osteo+T2D Black %; Osteo HDLD %; Osteo unique-patients; and the 6 per-condition comorbidity prevalences for Cancer/Headache/T2D (their logs summarize only `comorbid_count`, not the 22-flag per-condition set — that exists only for LBP+Osteo). Requires `\usepackage{xcolor}` (preview + gallery load it).
- Fill pass 2 newly recovered: **Cancer age SD = 6.98** (D02 af14d_ols `summarize $BENE_DEMO`) and **Osteo Any opioid Rx % = 6.99** (D04 `tab is_opioid_rx`). See `probes/0624_cohort-descriptives/evidence.md` "Fill pass 2" section.

## Status
gathered (multi-cohort Table 1 built from logs, fill pass 2 applied; probe at the Read gate, not yet judged). Zero plain `--` remain; remaining gaps are explicit RED TODOs (server descriptives re-export needed). Cancer age SD + Osteo any-opioid-Rx % newly filled from auxiliary reg logs.
