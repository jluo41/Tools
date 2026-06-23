// Cohort config — <Cohort> (e.g. VisitLBP)
// Shared ICD codes, topic flags, paths.
// Loaded by per-run .do configs (which also load _source_{synth|full}.do).
// Paths anchored via ${ws_root}.

global icd_codes `" "M54.5" "M54.4" "M54.9" "'

global topic_cases      1
global topic_bene_year  1
global topic_enrollment 1
global topic_pde        1
global topic_claims     1
global topic_lines      1
global topic_outpt      1

global case_asset_name    "case_<cohort>_${cms_source}"
global case_asset_version "<v0001>"
