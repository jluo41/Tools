# haipipe-insight-bind · version history

## 0.3.0 · 2026-10-02 · The question owns its run (JL 261002)

- A run fits only if its config serves this question alone and writes exactly the proposed files and columns; otherwise the question gets its own run (a new config of a task whose code computes the proposal, or a new task). Never extend another question's run with a column or grouping.

## 0.2.0 · 2026-10-01 · Exact spec match (JL 261001)

- A compute need binds a run only when the run computes its work spec exactly (cut, unit, measure, grouping or contrast, uncertainty, rivals, output columns); otherwise the smallest change makes one match, or a new task is built from the spec. A refusal is bound to its probe run. `ref/sync_config_answers.py` rewrites each called config's `answers:` to the need ids bound to it.

## 0.1.0 · 2026-10-01 · First version (JL 261001)

- Binds each evidence need of one answering page to the narrowest result files whose columns carry its `pass:` condition, commissioning missing runs through `haipipe-task` on a person's release, and records it in the page's `answers.yaml`. The Insight workbench's "Bind the work" run.
