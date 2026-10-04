By declared pipeline
====================

One Run method card. The Task workbench shows it in the shared Guide › Method, under the
Run methods; its papers are the rows of `../../task-papers.md` whose `group` is
`by declared pipeline`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Run: How is each Result made, and can it be made again?
move: Hold the work as a declared tree, Block → Job → Task → Run, each level a folder with
  its own contract, so every experiment and its outputs stay in view and nothing runs from
  loose glue code.
comes from: Sculley et al. 2015, hidden technical debt; Zaharia et al. 2018, experiment
  tracking; Shankar et al. 2022, MLOps interviews
reads: the Block's Jobs and Tasks · each Task's Tickets
returns: the tree the workbench draws, every Run in it
test now: T3 receipt
test in use: T3 receipt


What the literature says
------------------------

rationale: Glue code, pipeline jungles and untracked configuration are a hidden debt of
  analysis systems [Sculley 2015]; tracking each experiment's parameters, code and outputs
  makes them comparable [Zaharia 2018]; practitioners rely on experiment velocity,
  validation and versioning [Shankar 2022].
context: Machine learning systems in production and their tooling [Sculley 2015; Zaharia
  2018; Shankar 2022].
steps: 1. One Job per shared code and defaults. 2. One Task per contract. 3. One Run per
  config. 4. The workbench reads the tree, nothing else.
strengths: Every Run is reachable from its Question in one tree, and a stray Run shows as
  "Not under a Question" (ours).
limitations: A tree costs folders; a quick look at the data still needs a Task (ours).


Applied to AI
-------------

agent: haipipe-task-creator-agent places each new Task in its Job.
steps: 1. Find or open the Job. 2. Open the Task Folder. 3. Add the Run's config and Ticket.
returns: the Task Folder and its Tickets.
verify: Every Run has a Ticket in its Task's runs/ and a Result beside it (T3).
risk: An agent may start a script outside the tree to save time, and its output is then
  invisible (ours).
evidence on ai: No study tests this layout with agents (ours).
skill: haipipe-task
