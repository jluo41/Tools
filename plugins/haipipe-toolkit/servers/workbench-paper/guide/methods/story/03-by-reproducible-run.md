By reproducible run
===================

One story method card. The Paper workbench shows it in the shared Guide › Method,
under Story methods; its papers are the rows of `../../../related/papers.md` whose
`group` is `by reproducible run`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Story: What do we claim, on what evidence?
move: Every number the paper reports comes from a recorded Run: its code, config, inputs
  and receipt, so the analysis can be run again.
comes from: Sandve et al. 2013, ten simple rules for reproducible computational research
reads: Task Runs · their receipts
returns: a report per question whose evidence names exact Results
test now: T3 reproduced
test in use: T3 reproduced


What the literature says
------------------------

rationale: Reproducibility is a minimum standard for a computational claim, and it needs
  a record of how every result was produced, without manual steps [Sandve 2013].
context: Computational research across fields [Sandve 2013].
steps: 1. Run analysis only through a Ticket. 2. Keep the code, config and receipt with
  the Result. 3. Cite the Result, never a copied number.
strengths: A reviewer's request to change an analysis is a new Run, not an edit to a
  table (ours).
limitations: Reproducing a Run shows it computes what it says, not that the analysis is
  the right one (ours).


Applied to AI
-------------

agent: The Task orchestrator runs the Ticket; only the Ticket writes the Result.
steps: 1. Plan the Task. 2. Review its code. 3. Run the Ticket. 4. Report from its
  Results.
returns: results/<run>/ with runtime.yaml.
verify: Every evidence item names a Run with a receipt (T3).
risk: An agent may patch a table by hand; generated files are never edited (ours).
evidence on ai: No study tests agent-run analyses for reproducibility in this setting
  (ours).
skill: haipipe-task
