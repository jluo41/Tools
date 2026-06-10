// Regression config — <Cohort>_<Pairing> (e.g. LBP_NPI)
// Data path, clustering, controls.
// Output is LIGHT: coef tables land in results/, NOT _WorkSpace/.
// Paths anchored via ${ws_root}.

global data_path "${ws_root}/*-Data-Store/<asset>/<version>/ANALYSIS-CMS-Filter.dta"
global policy_path "${ws_root}/0-External-Store/<policy>"

global cluster_var "npi_id"
global controls   "age i.sex i.race_eth i.region year"
global outcome    "<outcome_var>"
global treatment  "<treatment_var>"
global instrument "<instrument_var>"
global policy_var "<policy_var>"
