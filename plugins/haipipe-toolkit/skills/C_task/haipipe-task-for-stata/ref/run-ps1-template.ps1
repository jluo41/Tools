# runs/<run>.ps1 - THIN per-run entry: one file per run identity, pairs with results/<run>/
# EDIT: orchestrator name + this run's parameters. data/reg have no year axis -> drop -year.
# Keep thin: parameters only; all logic lives in the orchestrator. sbatch/ loops these files.
& "$PSScriptRoot\..\run_<stage>_year.ps1" -cfg <cfg> -year <year>
