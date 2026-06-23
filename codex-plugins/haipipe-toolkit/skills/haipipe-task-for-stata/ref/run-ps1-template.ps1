# runs/<run>.ps1 - THIN per-run entry for ORCHESTRATED stages (cms/case).
# EDIT: orchestrator name + this run's parameters.
# NOTE: data/reg are SELF-ORCHESTRATING -- use ref/run-data-runner-template.ps1 instead.
& "$PSScriptRoot\..\run_<stage>_year.ps1" -cfg <cfg> -year <year>
