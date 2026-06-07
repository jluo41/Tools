set linesize 255
// <NN>_<stage>_pipeline.do - one step, one year. Args: <config> <step> <year> <results_dir> <ws_root>
// Steps: <step_a> | <step_b> | ... | summary   (data/reg: no year axis -> 4 args)

args config_file step year results_dir ws_root

if "`config_file'" == "" | "`step'" == "" | "`year'" == "" | "`results_dir'" == "" | "`ws_root'" == "" {
    display as error "Usage: do <NN>_<stage>_pipeline.do <config> <step> <year> <results_dir> <ws_root>"
    exit 198
}

// ws_root first: the config builds output paths from it
global ws_root "`ws_root'"

capture do "configs/`config_file'.do"
if _rc != 0 {
    display as error "ERROR: could not load configs/`config_file'.do"
    exit 198
}

global results_dir "`results_dir'"
global results_log "`results_dir'/log"

foreach d in "${results_dir}" "${results_log}" /* + stage heavy dirs, e.g. "${cms_asset_path}" */ {
    capture mkdir "`d'"
}

log using "${results_log}/`step'-`year'.txt", replace text
display "Step `step' year `year' start: " c(current_time)

if "`step'" == "<step_a>" {
    do "scripts/<worker-a>.do" `year'
}
else if "`step'" == "<step_b>" {
    do "scripts/<worker-b>.do" `year'
}
else {
    display as error "ERROR: unknown step '`step''."
    exit 198
}

display "Step `step' year `year' end: " c(current_time)
log close
