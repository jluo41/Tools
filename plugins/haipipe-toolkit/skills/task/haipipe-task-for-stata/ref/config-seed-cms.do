// CMS production config — shared globals for all years
// Source of truth for the CMS extract pipeline.
// Paths anchored via ${ws_root} (set by orchestrator .ps1).

global cms_asset_name "cms_full"
global cms_asset_version "<v0001_0130>"

global keep_vars_pde      "bene_id srvc_dt prscrbr_id prod_srvc_id days_suply_num tot_rx_cst_amt"
global keep_vars_carrier   "bene_id clm_thru_dt rfr_npi prncpal_dgns_cd icd_dgns_cd*"
global keep_vars_outpatient "bene_id clm_thru_dt at_physn_npi icd_dgns_cd* icd_prcdr_cd*"
global keep_vars_bene      "bene_id bene_birth_dt sex_ident_cd race_cd state_cd zip_cd"

global elixhauser_index 10
