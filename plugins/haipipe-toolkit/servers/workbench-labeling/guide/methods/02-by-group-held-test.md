By group-held test
==================

One labeling method card. Guide › Method shows it among its step's cards; its papers are
the rows of `../labeling-papers.md` whose `group` is `by group-held test`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Step 1 · Prepare: which items exist, and which are held back
move: Hold whole source groups back for the test, before the Contract, so nothing from a
  test group is ever seen in development.
comes from: Kapoor 2023, leakage; Søgaard 2021, random splits
reads: the items · their groups
returns: a sealed test set and its custodian
test now: T3 sealed
test in use: T4 independent


What the literature says
------------------------

rationale: Leakage between training and test is a common cause of overstated results in
  machine-learning science [Kapoor 2023], and random splits overstate performance compared
  with harder splits [Søgaard 2021].
context: Machine-learning evaluation across fields [Kapoor 2023]; NLP benchmarks [Søgaard
  2021].
steps: 1. Group the items by source. 2. Draw whole groups into the test. 3. Seal them and
  name the custodian.
strengths: The test measures judging new sources, not remembering old ones (ours).
limitations: Fewer items stay for development when groups are large (ours).


Applied to AI
-------------

agent: sampler-agent, with the custodian
steps: 1. Read the group frame. 2. Draw groups with a fixed seed. 3. Seal the test and
  record its counts only.
returns: the sealed test status, its counts and seed
verify: no group appears on both sides (T3)
risk: A test seen by any agent while writing the guideline is no longer a test; only
  counts are shown (ours).
evidence on ai: Leaked tests overstate models [Kapoor 2023].
skill: haipipe-labeling-preparation
