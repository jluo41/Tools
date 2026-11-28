# rNN_<run> <task> - <what this Run pins: year, CMS source>. THIN ticket (cms/case): hands this Run's config to the Job's shared runner.
# Current form, in a Run folder (runs/rNN_<run>/rNN_<run>.ps1 beside config.do and run.yaml), is two lines: this comment and
#   & "$PSScriptRoot\..\..\..\src\run_<stage>_year.ps1" "$PSScriptRoot\config.do"
# The lines below make that call in either layout: a flat runs/<run>.ps1 (a Block not yet moved) hands scripts\config\<run>.do. EDIT: the runner name.
$flat = (Split-Path -Leaf $PSScriptRoot) -eq "runs"
$task = if ($flat) { Split-Path -Parent $PSScriptRoot } else { Split-Path -Parent (Split-Path -Parent $PSScriptRoot) }
$cfg  = if ($flat) { Join-Path $task ("scripts\config\" + [IO.Path]::GetFileNameWithoutExtension($PSCommandPath) + ".do") } else { Join-Path $PSScriptRoot "config.do" }
& (Join-Path (Split-Path -Parent $task) "src\run_<stage>_year.ps1") $cfg
