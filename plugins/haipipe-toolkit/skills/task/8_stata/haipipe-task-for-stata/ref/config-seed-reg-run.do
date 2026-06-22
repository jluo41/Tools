// Per-run config -- <estimator> family, <window> window
// OLS/IV variant. For DID, add: global file_policy "${ws_root}/0-External-Store/Policy/Policy-State-Year.dta"
global ws_root : environment HAIPIPE_WS_ROOT
if "${ws_root}" == "" global ws_root "_WorkSpace"
do "configs/<Cohort>_<Pairing>.do"
global outcome_bfaf_window "<window>"
global res_dir "results/<RUNNAME>"
