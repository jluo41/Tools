Function: scan-status
======================

Scan a B01-style eval task directory, update diagram/status.json, and format a human-readable txt status table. Covers both loss-eval (B1) and forecast-eval (B2) subtask types automatically.

Three artefacts produced per run:
  {task_dir}/diagram/status.json       <- machine-readable; one key per storage group
  {task_dir}/diagram/{prefix}-status.txt  <- human-readable, written by formatter

Execution is fully reproducible: re-run to pick up newly completed evaluations.


Placement convention
---------------------

scan_status.py and scan_groups.json live at the **task-group level** (B01), shared by all subtasks. The formatter script runs per subtask.

  B01_evaluation_pretrain/
  ├── scan_status.py          <- shared scanner (copy from ref/scan_status/)
  ├── scan_groups.json        <- group config (one key per model family)
  ├── B1_eval_pretrain_loss/
  │   └── diagram/
  │       ├── status.json     <- written by scan_status.py
  │       └── status.txt      <- written by status_formatter.py
  └── B2_eval_pretrain_forecast/
      └── diagram/
          ├── status.json
          └── status.txt


---

Step 0: Parse args
-------------------

  scan-status <task_dir> [storage_key] [out_txt]

    task_dir     = path to a specific B01 subtask folder
    storage_key  = optional; if given, only re-scan that one group (merge into existing JSON; useful for incremental updates)
    out_txt      = optional; path for the formatted txt output (default: {task_dir}/diagram/status.txt)

Derived:
  task_group_dir  = task_dir.parent
  scan_script     = task_group_dir / scan_status.py
  config          = task_group_dir / scan_groups.json
  SKILL_REF       = <this skill>/ref/scan_status/


---

Step 1: Check prerequisites
-----------------------------

a) scan_status.py missing from task_group_dir?
   Copy SKILL_REF/scan_status.py -> task_group_dir/scan_status.py.
   Report: "Copied scan_status.py to {task_group_dir}."

b) scan_groups.json missing from task_group_dir?
   Show the user SKILL_REF/scan_groups_template.json as a starting point.
   Explain each field:
     storage_key    = first-level key in status.json; matches the model-store subdirectory name under _WorkSpace/5-ModelInstanceStore/
     run_filter     = substring that all run names for this group contain
     parse_pattern  = regex with capture groups for parse_fields
     parse_fields   = ordered list of field names; "setup" field (optional capture group) becomes None when absent and is treated as 'phase1' in the formatter
   Ask the user to confirm / fill in group definitions. Do NOT proceed until scan_groups.json is written and confirmed.

c) scan_groups.json exists?
   Read it. Confirm the storage keys to the user before running.


---

Step 2: Run the scanner
------------------------

  cd {project_root}
  source .venv/bin/activate && source env.sh
  python {task_group_dir}/scan_status.py {task_dir} [storage_key]

  - Reads sbatch/*.sh in task_dir to discover run names.
  - Reads runs/{run_name}.sh to extract VERSIONS_STR (model version tag).
  - Checks _WorkSpace/5-ModelInstanceStore/{storage_key}/{version}/ for
    training completion (non-empty dir) and eval completion:
      B1 (loss in task name): eval_results.json present in version dir
      B2 (otherwise):         results/{run_name}/forecast.json present in task_dir
  - Writes/merges {task_dir}/diagram/status.json.
  - After scanning each group, enumerates all non-empty version dirs in
    _WorkSpace/5-ModelInstanceStore/{storage_key}/ and reports any that do
    not match a scanned run's version field as unmapped instances.
    These are stored under status.json["unmapped"][storage_key] and printed
    as WARNING lines to stdout.

If the script errors (missing _WorkSpace, bad regex, etc.), show the error
and ask the user how to proceed. Do NOT auto-fix the scan_groups.json pattern.

Ambiguity resolution — before asking the user, first try to resolve by:

  1. Reading the eval Python script (eval_pretrain_nb.py or equivalent) in task_dir
     to find where it writes results and what paths it uses.
  2. Inspecting environment variables set in runs/{run_name}.sh and env.sh
     (MODEL_STORE, OUTPUT_DIR, VERSIONS_STR, etc.) to confirm the expected paths.

If the paths are unambiguous after that inspection, proceed silently.

Only pause and ask if still unclear after the above — for example:

  a) VERSIONS_STR missing or contains multiple whitespace-separated values and the eval script doesn't clarify which version is the output target.
  b) Multiple eval result files exist for the same run (e.g. eval_results.json in both the main version dir and an other/ subdir) with no clear precedence.
  c) The storage_key matches no subdir under 5-ModelInstanceStore/ even after checking env vars.
  d) A run name passes run_filter but the parse_pattern captures nothing — the entry would be structureless and the status unreliable.

  For each unresolved case, show what was found (paths, candidates) and ask the
  user which to treat as authoritative. Do not silently pick one.


---

Step 3: Format to txt
-----------------------

  python SKILL_REF/status_formatter.py {task_dir} [out_txt]

If out_txt is not given, the formatter writes to {task_dir}/diagram/status.txt.
For named files (e.g. 03-status-forecast.txt), pass the path explicitly.


Txt format rules (MUST always appear):
.......................................

  1. Header block — always the first 3 lines:
       Status: {task_dir.name}
       ============================  (= repeated to match title length)
       Updated: {YYYY-MM-DD} (auto-updated)

  2. Legend — always present after a blank line:
       V = trained + eval done
       O = trained, eval not done
       X = not trained
       ? = run not defined in sbatch (not planned)

  3. Format selection (auto-detected by formatter):

     Multiple model_type values across groups (e.g. clm_tkn + clm_num):
       -> MERGED FORMAT: one section per sweep type, model types as columns.
          Column abbreviation: strip "clm_" prefix and uppercase
          (clm_tkn -> TKN, clm_num -> NUM).
          Column order follows MODEL_ABBR_ORDER = ['TKN', 'NUM'] in formatter.

     Single model_type:
       -> PER-GROUP FORMAT: one === model_type === section per storage group,
          with sub-sections (--- Phase 1 ---, --- Epoch Sweep ---, etc.).

  4. Merged format — sections appear in this order (omit if no entries):

     === Phase 1 ===
       Size  |  TKN  |  NUM        (no trailing |)
       ------|-------|------
       1m    |   V   |   V

     === Epoch Sweep ===
              |----------- TKN -----------|----------- NUM -----------|
       Size   | ep0.1 | ep.25 | ep.75 | ep2 | ...                    |
       -----  (all rows end with |)
       Epoch display: ep0.25 -> ep.25, ep0.75 -> ep.75 (ep0.1 unchanged)

     === Datasize ===
       Size  |---- TKN ----|---- NUM ----|
             | d10m | d100m | d10m | d100m |   (all rows end with |)

     === v3 ===
       (same layout as Phase 1)

  5. Status cell values: V, O, X, or ? (single character).
       V = trained + eval done
       O = trained, eval not done
       X = not trained
       ? = run not defined in sbatch (not planned; grid cell has no entry)

  6. Size ordering: ascending by parameter count (1m < 2m < … < 1b).

  7. Column ordering within grids: ascending numeric order derived from the
     setup values present (e.g. ep0.1 < ep0.25 < ep2; d10m < d100m).
     Exact columns depend on what runs exist — do not hardcode.

  8. Unmapped instances — appended at the bottom if status.json["unmapped"]
     contains any non-empty lists:
       === Unmapped Instances ===

       Trained versions in store with no matching sbatch run:

         {storage_key}:
           {version}
           ...

Setup classification (from JSON 'setup' field):
  None / 'phase1'    -> Phase 1 table
  ep*  (ep0.1 …)    -> Epoch Sweep
  d*   (d10m …)     -> Datasize
  'v3'               -> v3 table


---

Step 4: Show output
--------------------

Print the txt content inline so the user can verify it.
Then emit the structured tail:

  status:    ok | blocked | failed
  summary:   N entries scanned across M groups; txt written to {path}
  artifacts: [{task_dir}/diagram/status.json, {out_txt}]
  next:      re-run with a specific storage_key to update one group, or
             review the O-status entries for pending eval jobs


---

MUST NOT
---------

- Do NOT edit sbatch scripts, notebook files, or source code.
- Do NOT create scan_groups.json unilaterally — always ask the user to confirm
  the storage_key names and parse patterns before writing.
- Do NOT run scan_status.py without confirming scan_groups.json is correct.
