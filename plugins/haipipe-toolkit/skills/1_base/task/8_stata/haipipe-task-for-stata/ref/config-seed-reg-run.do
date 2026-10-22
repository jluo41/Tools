// Per-run config -- <estimator> family, <window> window. Lives at runs/rNN_<run>/config.do (a flat Block: scripts/config/rNN_<run>.do).
// OLS/IV variant. For DID, add: global file_policy "${ws_root}/0-External-Store/Policy/Policy-State-Year.dta"
global ws_root : environment HAIPIPE_WS_ROOT
if "${ws_root}" == "" global ws_root "_WorkSpace"
do "scripts/config/<Cohort>_<Pairing>.do"
global outcome_bfaf_window "<window>"
global res_dir : environment HAIPIPE_RUN_RESULT
if "${res_dir}" == "" {
    display as error "HAIPIPE_RUN_RESULT must name the resolved Result directory"
    exit 198
}
global pass_dir : environment HAIPIPE_PASS_DIR
if "${pass_dir}" == "" {
    global pass_dir "${res_dir}"
}
