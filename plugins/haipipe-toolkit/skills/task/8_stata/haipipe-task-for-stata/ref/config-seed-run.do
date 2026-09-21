// Per-run config: <Cohort> <source> <year>
// Loads source selector + shared cohort config.
// Matched to: runs/rNN_<run>.ps1
do scripts/config/_source_<source>.do
do scripts/config/<Cohort>.do
global data_year <year>
