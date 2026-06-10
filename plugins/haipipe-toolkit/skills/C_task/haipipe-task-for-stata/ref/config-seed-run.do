// Per-run config: <Cohort> <source> <year>
// Loads source selector + shared cohort config.
// Matched to: runs/run_case_<Cohort>_<source>_<year>.ps1
do configs/_source_<source>.do
do configs/<Cohort>.do
global data_year <year>
