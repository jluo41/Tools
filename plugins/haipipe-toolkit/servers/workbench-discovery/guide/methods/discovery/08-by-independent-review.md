By independent review
=====================

One Discovery method card. The Discovery workbench shows it in the shared Guide › Method; its
papers are the rows of `../../../related/papers.md` whose `group` is `by independent review`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Answer: How does the answer reach the reader, checked?
move: A card or a report is read by an agent that did not write it; a failed review goes back to the step that owns the fault, and only a person releases.
comes from: Panickssery et al. 2024, self-preference
reads: the card or report · the Results it cites
returns: a review verdict: ready, or the step to return to and why
test now: T4 independent
test in use: T7 released


What the literature says
------------------------

rationale: A model evaluator scores its own outputs higher than others that human raters judge equal [Panickssery 2024], so the writer never reviews its own card or report.
context: Large language models used as evaluators [Panickssery 2024].
steps: 1. Give the reviewer the card or report and the files it rests on. 2. It returns ready or a route. 3. The route reopens the owning step.
strengths: The review cannot be passed by the writer's own preference (ours).
limitations: Two agents of the same model may share blind spots; a person still signs (ours).


Applied to AI
-------------

agent: haipipe-discovery-reviewer-agent for cards and Runs; haipipe-page-check-agent for reports.
steps: 1. Read the card or report. 2. Check it against the Results. 3. Return ready or a route.
returns: a verdict with its route.
verify: The reviewer differs from every writer of the thing (T4, T7).
risk: A reviewer that sees the writer's reasoning may adopt it; it reads only the files (ours).
evidence on ai: Self-preference [Panickssery 2024] is why the writer never reviews its own work.
skill: haipipe-discovery-review
