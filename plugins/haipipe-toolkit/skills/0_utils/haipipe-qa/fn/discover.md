fn/discover -- Scan target scope, collect all issues
=====================================================

Procedure
---------

### Step 0 -- Resolve target

Parse the target path. Determine scope:
- task-folder: scan that folder's .do, .ps1, configs/, scripts/, runs/
- task-group: scan all task-folders inside
- single file: focused checks on that file only

### Step 1 -- Detect stage/type

Read the target to determine which check categories apply:
- Has `data_pipeline*.do` or `scripts/1-filter-case/` -> data stage (categories A-L)
- Has `scripts/run-*-*.do` worker pattern -> reg stage (categories A, B, E, F-I, M, N)
- Has `case_pipeline.do` -> case stage (categories A, B, F-I)
- Has `*_cms_pipeline.do` -> cms stage (categories B, F-I)

### Step 2 -- Run applicable checks

For each applicable category, run the checks. Collect findings.

**A. Naming parity**
- Extract CC variable names from: A02 cc_defs, case bene-bt-year.do, C01 full-variables.do,
  regression BENE_CONDITION
- Compare all four lists -- any mismatch is an issue
- Check against ground truth: A00_cms_raw_description mbsf_cc_summary schema

**B. Config consistency**
- For paired configs (synth/full): diff globals, flag any that differ unexpectedly
- For source selectors: verify shared config uses ${data_source} / ${phy_review_dir}
- Check thin wrappers load correct chain

**C. Data types**
- For CC variables: bare = flag (double %1.0g), _ever = date (long %d), _mid = flag
- Flag any code that treats dates as flags (binarization with ==3 on _ever)

**D. Binarization**
- Check full-variables.do binarization targets only bare CC names, not _ever
- Verify adaptive logic: `if r(max) > 1 replace = (==3)` only on flags

**E. Variable coverage**
- List all variables referenced in regression BENE_CONDITION / BENE_DEMO / etc.
- Check each exists in the ANALYSIS output (via ds in log or direct Stata check)

**F-I. Encoding, paths, SSC, STATATMP**
- Standard Gate 2 checks from cms-server-checklist.md
- Delegate to the checklist machine checks

**J. Source parity**
- Verify synth and full configs produce same variable set
- Check case_asset_version filled (no TODO placeholders for planned runs)

**K. Row plausibility**
- From logs: row count after each filter step
- Flag if any step drops to 0 or drops > 90%

**L. Merge completeness**
- From logs: check ds output after each merge
- Flag if expected columns are absent

**M. Outcome variance**
- From logs or data: check DV has >1 unique value
- Flag if DV is constant (would crash regression)

**N. Control consistency**
- Extract BENE_CONDITION from every regression script in the task group
- Flag any script that differs from the majority pattern

### Step 3 -- Write QA_ISSUES.md

Write all findings to `<target>/QA_ISSUES.md` using the issue format from SKILL.md.
Sort by severity (BLOCKER first, then WARN, then INFO).
Number sequentially: Q1, Q2, Q3, ...

### Step 4 -- Report summary

```
QA Discovery: <target>
  BLOCKER: N issues
  WARN:    N issues
  INFO:    N issues
  Total:   N issues

Ready for walkthrough: /haipipe-qa walkthrough <target>
```
