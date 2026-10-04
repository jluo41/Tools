By independent check
====================

One delivery method card. The Page workbench shows it in the shared Guide › Method,
under Delivery methods; its papers are the rows of `../../page-papers.md` whose
`group` is `by independent check`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Delivery: How does it reach the reader, checked?
move: The Page is checked by an agent that did not write it, reading the plan, the
  evidence and the built Page; a failed check routes back to the step that owns the
  fault.
comes from: Panickssery et al. 2024, self-preference; Huang et al. 2023, self-correction
reads: the plan · the evidence trace · the built Page
returns: CLOSE, or the step to return to and why
test now: T4 independent
test in use: T4 independent


What the literature says
------------------------

rationale: A model evaluator scores its own outputs higher than others' that human
  raters judge equal, and can tell its own outputs apart [Panickssery 2024]; without
  outside feedback, models struggle to correct their own reasoning and sometimes get
  worse [Huang 2023].
context: Large language models used as evaluators and as self-correctors [Panickssery
  2024; Huang 2023].
steps: 1. Give the checker the plan, the evidence and the Page. 2. It returns CLOSE or a
  route. 3. The route opens a Run in the step that owns the fault.
strengths: The check cannot be passed by the writer's own preference (ours).
limitations: Two agents of the same model may share the same blind spots; a person still
  signs the release (ours).


Applied to AI
-------------

agent: haipipe-page-check-agent, which makes nothing and cannot approve a version it
  produced.
steps: 1. Read the Page version. 2. Check coverage, evidence, freshness and clarity. 3.
  Return CLOSE or a route.
returns: a check receipt with its verdict and route.
verify: The checker's identity differs from every producer of the version (T4).
risk: A checker that sees the writer's reasoning may adopt it; it reads the plan and the
  Page, not the writer's notes (ours).
evidence on ai: Self-preference [Panickssery 2024] and failed self-correction [Huang
  2023] are why the writer never checks its own Page.
skill: haipipe-page-check
