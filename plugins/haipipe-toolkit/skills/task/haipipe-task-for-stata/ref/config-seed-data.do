// CONFIG: <Spec>.do -- data pipeline config for <Cohort> cohort, <Design> design.
// Paths anchored via ${ws_root}. Cross-year stage (NO year axis).

// ==============================================================================
// INPUT: Case-pipeline output (2-Case-Store)
// ==============================================================================
global case_store         "${ws_root}/2-Case-Store"
global case_asset_name    "<case_cohort>"
global case_asset_version "<v0001_cohort_YYYYMMDD>"
global case_asset_path    "${case_store}/${case_asset_name}/${case_asset_version}"

global case_source "<VisitCohort>"
global data_year_start 2015
global data_year_end   2020

global file_cases          "CASES-BeneNpiObsdt-${case_source}"
global file_bene_year      "BENE-BeneObsdt-Year"
global file_enrollment     "BENE-BeneObsdt-Enrollment"
global file_pde_bene       "BFAF-BeneObsdt-PDE"
global file_pde_bene_oprx  "BFAF-BeneObsdt-PDE-OpioidRx"
global file_pde_npi        "BFAF-NpiObsdt-PDE"
global file_pde_npi_oprx   "BFAF-NpiObsdt-PDE-OpioidRx"
global file_pde_bn         "BFAF-BeneNpiObsdt-PDE"
global file_pde_bn_oprx    "BFAF-BeneNpiObsdt-PDE-OpioidRx"
global file_claims_bene    "BFAF-BeneObsdt-Claims"
global file_lines_npi      "BFAF-NpiObsdt-Lines"
global file_lines_bn       "BFAF-BeneNpiObsdt-Lines"
global file_outpt_bene     "BFAF-BeneObsdt-Outpatient"
global file_outpt_npi      "BFAF-NpiObsdt-Outpatient"
global file_outpt_bn       "BFAF-BeneNpiObsdt-Outpatient"

// ==============================================================================
// INPUT: External-pipeline output (0-External-Store)
// ==============================================================================
global external_store  "${ws_root}/0-External-Store"
global file_physician  "${external_store}/Physician/<PhyReview>/npi_review_data.dta"
global file_policy     "${external_store}/Policy/Policy-State-Year.dta"

// ==============================================================================
// OUTPUT PATHS
// ==============================================================================
global apply_first_visit_filter 1
global first_visit_type "<1stPair>"

global data_store         "${ws_root}/3-Data-Store"
global data_asset_name    "<Cohort_Design>"
global data_asset_version "<v001_base_synth>"
global data_asset_path    "${data_store}/${data_asset_name}/${data_asset_version}"

global data_output_dir  "${data_asset_path}"
global data_tmp_dir     "${data_output_dir}/tmp"
global data_log_dir     "${data_output_dir}/logs"
global data_output_file "${data_output_dir}/ANALYSIS-CMS-Filter.dta"

// ==============================================================================
// STEP 1: CASE FILTERS
// ==============================================================================
global filter_year_min         2016
global filter_year_max         2019
global filter_age_min          65
global filter_age_max          95

global require_coverage_180d   1
global require_rx_coverage_3mo 1
global require_survived_1y     1

global exclude_esrd    1
global exclude_cancer  1
global exclude_hospice 1

global use_justify_pain_flag      0
global justify_pain_asset_name    "case_justifypainvisits"
global justify_pain_asset_version "<v0001_justifypain_YYYYMMDD>"
global justify_pain_asset_path    "${case_store}/${justify_pain_asset_name}/${justify_pain_asset_version}"
global file_justify_cases         "CASES-BeneNpiObsdt-VisitJustifyPains"
global justify_pain_window_lower  -90
global justify_pain_window_upper  0

// ==============================================================================
// STEP 2: EXTERNAL FILTERS
// ==============================================================================
global require_mddo          1
global filter_review_min     5
global filter_review_max     100

// ==============================================================================
// STEP 3: COVARIATES TO MERGE & DERIVE
// ==============================================================================
global use_bene_year     1
global use_enrollment    1
global use_claims_bfaf            1
global use_pde_oprx_bfaf          1
global use_pde_npi_oprx_bfaf      1
global use_pde_bn_oprx_bfaf       1
global use_pde_generic_bfaf       1
global use_pde_generic_npi_bfaf   1
global use_pde_generic_bn_bfaf    1
global use_lines_npi_bfaf         1
global use_lines_bn_bfaf          1
global use_outpt_bene_bfaf        1
global use_outpt_npi_bfaf         1
global use_outpt_bn_bfaf          1
global use_physician     1
global use_policy        1

global derive_race_indicators  1
global derive_time_variables   1
global derive_specialty_groups 1
global derive_policy_treatment 1

global outcome_bfaf_window     "af7d"
global hdld_mme_threshold      50
global hdld_days_threshold     7
global daily_mme_geq90_threshold 90
global mme_high_threshold      500

// ==============================================================================
// EXECUTION
// ==============================================================================
global skip_existing 1

display "Config: data ${case_source} (${first_visit_type})"
display "  Case input:     ${case_asset_path}"
display "  External input: ${external_store}"
display "  Output:         ${data_output_dir}"
display "  Years:  ${filter_year_min}-${filter_year_max}  Age: ${filter_age_min}-${filter_age_max}"
