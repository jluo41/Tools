# j02_evidence_value · the paper's evidence: values

layer: evidence
state: open
goal: values: one Task per group of printed numbers, each read from a returned Result
close: every one the writing Jobs quote is drawn or checked, and accepted
reads: the returned Results of the work Blocks (internal) and the discovery Blocks (external); never raw data

## Tasks

1. t01_values-sample · the sample and the main association (RQ1)
2. t02_raw-value-tables · the Values tabs: raw tables from the Runs
3. t99_paper_value_check · every printed number at once

The standard shape (haipipe-paper-evidence 0.7.0): each Task holds only `scripts/value_map.yaml`; `gen_value_runs.py`
writes the Runs, `values_ledger.py bind --propose` seeds the bindings into each Section's `evidence/proposals.md`.
Placeholders only: the values come from `work/b90_example_paper_results`.
