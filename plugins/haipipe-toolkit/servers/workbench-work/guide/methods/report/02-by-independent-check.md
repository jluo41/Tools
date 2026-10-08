By independent check
====================

One Report method card. The Task workbench shows it in the shared Guide › Method, under the
Report methods; its papers are the rows of `../../../related/papers.md` whose `group` is
`by independent check`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Report: How does the answer reach the reader, checked?
move: The report is checked by an agent that did not write it, reading the Logic, the cited
  Results and the report; a failed check routes back to the step that owns the fault, and a
  person releases a report that passes.
comes from: Panickssery et al. 2024, self-preference; Huang et al. 2023, self-correction
reads: the Logic · the cited Results · the report
returns: CLOSE, or the step to return to and why
test now: T8 independent
test in use: T8 independent


What the literature says
------------------------

rationale: A model evaluator scores its own outputs higher than others that human raters
  judge equal [Panickssery 2024]; without outside feedback, models struggle to correct
  their own reasoning and sometimes get worse [Huang 2023].
context: Large language models used as evaluators and as self-correctors [Panickssery
  2024; Huang 2023].
steps: 1. Give the checker the Logic, the Results and the report. 2. It returns CLOSE or a
  route. 3. The route opens a Run in the step that owns the fault.
strengths: The check cannot be passed by the writer's own preference (ours).
limitations: Two agents of the same model may share blind spots; a person still signs the
  release (ours).


Applied to AI
-------------

agent: haipipe-page-check-agent, which makes nothing and cannot approve a version it
  produced.
steps: 1. Read the report. 2. Check its citations, freshness and answer against the
  Logic. 3. Return CLOSE or a route.
returns: a check receipt with its verdict and route.
verify: The checker differs from every writer of the report (T8).
risk: A checker that sees the writer's reasoning may adopt it; it reads the Logic, the
  Results and the report (ours).
evidence on ai: Self-preference [Panickssery 2024] and failed self-correction [Huang 2023]
  are why the writer never checks its own report.
skill: haipipe-page-check
