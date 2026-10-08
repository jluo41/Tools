By contract first
=================

One Run method card. The Task workbench shows it in the shared Guide › Method, under the
Run methods; its papers are the rows of `../../../related/papers.md` whose `group` is
`by contract first`. A claim names its source in brackets; "(ours)" marks the workbench's
own judgment.

family: Run: How is each Result made, and can it be made again?
move: Write the Task's contract before its code: what it reads, what it returns and how the
  return is checked; the code is written to the contract, never the contract to the code.
comes from: Leek & Peng 2015, the question's type; Nosek et al. 2018, preregistration;
  Chambers & Tzavella 2021, registered reports
reads: the Question's Logic · the Job's shared code and defaults
returns: the Task's plan: inputs, outputs, required Result files, checks
test now: T1 planned
test in use: T3 receipt


What the literature says
------------------------

rationale: The type of question decides which analysis can answer it [Leek 2015];
  fixing the hypothesis and analysis before results are seen separates confirmation from
  exploration [Nosek 2018], and judging a study on its question and method before its
  results is what registered reports do [Chambers 2021].
context: Data analysis and the reform of research practice [Leek 2015; Nosek 2018;
  Chambers 2021].
steps: 1. Read the Question's Logic. 2. Name what the Task reads and returns. 3. Name the
  Result files a complete Run must write. 4. Have another agent agree the plan.
strengths: A Task's output can be checked against something written before it existed
  (ours).
limitations: A plan can be too narrow for what the data shows; the plan is versioned, and a
  change is a new plan, not an edit to the Result (ours).


Applied to AI
-------------

agent: haipipe-task-creator-agent writes the plan; haipipe-task-reviewer-agent agrees it.
steps: 1. Read the Question and the Job's defaults. 2. Write the plan. 3. Name the required
  Result files. 4. Stop for the reviewer.
returns: the Task Folder's plan and its required Result files.
verify: The Ticket's required Result list matches the plan (T3).
risk: An agent may write the plan after the code, so the plan describes what was done
  rather than what was asked (ours).
evidence on ai: No study tests contract-first planning by agents on analysis Tasks (ours).
skill: haipipe-task
