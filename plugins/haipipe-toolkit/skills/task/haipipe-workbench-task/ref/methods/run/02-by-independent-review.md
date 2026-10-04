By independent review
=====================

One Run method card. The Task workbench shows it in the shared Guide › Method, under the
Run methods; its papers are the rows of `../../task-papers.md` whose `group` is
`by independent review`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Run: How is each Result made, and can it be made again?
move: An agent that did not write a Task's code reads it, against its plan, before the
  Ticket runs; the verdict is recorded beside the code.
comes from: Panickssery et al. 2024, self-preference; Huang et al. 2023, self-correction
reads: the plan · the worker and its config · the Ticket
returns: a code review: pass, warn or fail, each finding with its line
test now: T2 reviewed
test in use: T4 generated


What the literature says
------------------------

rationale: A model evaluator scores its own outputs higher than others that human raters
  judge equal [Panickssery 2024], and without outside feedback models struggle to correct
  their own reasoning [Huang 2023]; so the reader of the code is not its writer.
context: Large language models used as evaluators and as self-correctors [Panickssery
  2024; Huang 2023].
steps: 1. Give the reviewer the plan and the code. 2. It records its verdict and findings
  beside the code. 3. A fail goes back to Build; the Ticket runs only after a pass or warn.
strengths: A wrong filter or a silent drop is caught before it becomes a Result (ours).
limitations: Two agents of the same model may share blind spots; the review reads code, not
  the data it will meet (ours).


Applied to AI
-------------

agent: haipipe-task-reviewer-agent, read-only; it never reviews its own work.
steps: 1. Read the plan. 2. Read the worker, config and Ticket. 3. Record the verdict and
  each finding with its line.
returns: the code review beside the code it reviews.
verify: The reviewer differs from the code's author, and the review predates the Run (T2).
risk: A reviewer shown the author's reasoning may adopt it; it reads the plan and the code
  (ours).
evidence on ai: Self-preference [Panickssery 2024] and failed self-correction [Huang 2023]
  are why the author never reviews its own code.
skill: haipipe-task
