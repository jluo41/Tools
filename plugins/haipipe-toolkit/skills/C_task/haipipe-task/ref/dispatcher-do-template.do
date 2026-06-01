// <NN>_<stage>_pipeline.do — DISPATCHER skeleton, STATA DIALECT.
// =============================================================================
// GENERIC across stages. The file name is FREE (the orchestrator calls it by
// bare name from inside the task folder). What is INVARIANT (do not change):
//   • code paths (scripts/, configs/) are TASK-FOLDER-RELATIVE
//   • the DATA root (_WorkSpace) arrives ABSOLUTE as <ws_root> — set it FIRST,
//     before the config builds any output path
//   • run with the task folder as the working dir (the orchestrator does this)
//
// What is STAGE-SPECIFIC (the two `EDIT` blocks below — fill per stage):
//   • the set of <step> tokens and which scripts/<worker>.do each maps to
//   • which output dirs to mkdir (cms/case create _WorkSpace asset dirs;
//     data writes a cross-year table; reg writes LIGHT to results/ only)
// The cms/case step lists, the BFAF feature outputs, etc. are NOT part of this
// template — see the per-stage child's fn/scaffold.md for concrete examples.
//
// Usage (from inside this task folder):
//   stata-mp -b do <NN>_<stage>_pipeline.do <config> <step> <year> <results_dir> <ws_root>
//   (data/reg have NO year axis → drop <year>, parse 4 args.)
// =============================================================================


set linesize 255


args config_file step year results_dir ws_root    // EDIT: drop `year` for data/reg

if "`config_file'" == "" | "`step'" == "" | "`year'" == "" | "`results_dir'" == "" | "`ws_root'" == "" {
    display as error "ERROR: required args missing."
    display as error "Usage: do <NN>_<stage>_pipeline.do <config> <step> <year> <results_dir> <ws_root>"
    exit 198
}

// ws_root (absolute path to _WorkSpace) MUST be visible to the config BEFORE it
// builds raw_cms / output paths.
global ws_root "`ws_root'"

capture do "configs/`config_file'.do"
if _rc != 0 {
    display as error "ERROR: Could not load configs/`config_file'.do"
    exit 198
}

global results_dir "`results_dir'"
global results_log "`results_dir'/log"

// ── EDIT 1: stage output dirs ────────────────────────────────────────────────
// Create the per-run results/log dirs (always) + this stage's heavy output dirs
// (if any). Heavy dirs are built from ${ws_root} in the config; reg has none.
foreach d in "${results_dir}" "${results_log}" /* + stage heavy dirs, e.g. "${cms_asset_path}" */ {
    capture mkdir "`d'"
}

log using "${results_log}/`step'-`year'.txt", replace text
display "Step `step' year `year' start: " c(current_time)

// ── EDIT 2: step → worker dispatch (one branch per worker in scripts/) ───────
if "`step'" == "<step_a>" {
    do "scripts/<worker-a>.do"  `year'
}
else if "`step'" == "<step_b>" {
    do "scripts/<worker-b>.do"  `year'
}
// ... add the rest of this stage's steps ...
else {
    display as error "ERROR: unknown step '`step''."
    exit 198
}

display "Step `step' year `year' end: " c(current_time)
log close
