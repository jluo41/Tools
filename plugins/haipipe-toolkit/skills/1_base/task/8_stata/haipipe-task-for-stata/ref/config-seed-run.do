// Per-run config: <Cohort> <source> <year>
// Loads source selector + shared cohort config.
// Lives at runs/rNN_<run>/config.do, beside its ticket rNN_<run>.ps1 (a flat Block: scripts/config/rNN_<run>.do).
do scripts/config/_source_<source>.do
do scripts/config/<Cohort>.do
global data_year <year>
