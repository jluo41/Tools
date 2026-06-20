// Regression config -- <Cohort>_<Pairing> (shared across OLS/IV/DID runs)
// Data path + version only. Controls/outcomes live in worker .do scripts.
global reg_cohort   "<Cohort>_<Pairing>"
global data_version "<version>"
global data_file    "${ws_root}/<N>-Data-Store/${reg_cohort}/${data_version}/ANALYSIS-CMS-Filter.dta"
global res_root     "results"
