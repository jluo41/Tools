// Analysis spec — <Spec> (e.g. lbp_synth_v1)
// Filter params, merge rules, variable definitions.
// Cross-year stage: NO year axis.
// Paths anchored via ${ws_root}.

global case_source  "case_<cohort>_<source>"
global case_version "<v0001>"

global data_asset_name    "<data_store_name>"
global data_asset_version "<v0001>"

global filter_first_visit 1
global filter_age_min     18
global filter_age_max     99

global physician_traits_path "${ws_root}/0-External-Store/<traits>"
global policy_path           "${ws_root}/0-External-Store/<policy>"
