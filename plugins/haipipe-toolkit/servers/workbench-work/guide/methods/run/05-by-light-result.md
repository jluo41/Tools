By light result
===============

One Run method card. The Task workbench shows it in the shared Guide › Method, under the
Run methods; its papers are the rows of `../../../related/papers.md` whose `group` is
`by light result`. A claim names its source in brackets; "(ours)" marks the workbench's own
judgment.

family: Run: How is each Result made, and can it be made again?
move: A Result keeps the receipt, metrics, small tables, figures and pointers; heavy output
  (a model, an array, a row-level table) goes to its own store, and the Result keeps a
  pointer to it.
comes from: Wilson et al. 2017, good enough practices; Wilkinson et al. 2016, FAIR
reads: the Run's outputs and their sizes
returns: a light Result and a pointer to the heavy store
test now: T5 light
test in use: T5 light


What the literature says
------------------------

rationale: Raw data, code and results are kept apart, and what was done is written down
  [Wilson 2017]; outputs are findable and reusable when they sit at stable paths with
  metadata [Wilkinson 2016].
context: Everyday scientific computing and data stewardship [Wilson 2017; Wilkinson
  2016].
steps: 1. The Ticket writes light files into the Result. 2. It writes heavy files to the
  Run's store. 3. It writes the pointer into the Result.
strengths: A Result can be read, cited and kept in version control; the heavy files stay
  findable through the pointer (ours).
limitations: A pointer can outlive its store; the store's path is checked when read (ours).


Applied to AI
-------------

agent: the Ticket itself, run by haipipe-task-orchestrator-agent.
steps: 1. Route each output by size and kind. 2. Write the pointer.
returns: the Result and its pointer file.
verify: No Result file is over the size limit, and each pointer resolves (T5).
risk: An agent may copy a large file into the Result to make a figure work (ours).
evidence on ai: No study tests this split with agents (ours).
skill: haipipe-task
