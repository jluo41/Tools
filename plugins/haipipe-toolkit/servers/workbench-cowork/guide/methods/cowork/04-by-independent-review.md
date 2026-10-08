By independent review
=====================

One CoWork method card. The CoWork workbench shows it in the shared Guide › Method; its
papers are the rows of `../../../related/papers.md` whose `group` is `by independent review`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Report: How does the answer reach the reader, checked?
move: A draft message or a report is read by an agent that did not write it; a failed review goes back to the step that owns the fault, and only a person sends or releases.
comes from: Panickssery et al. 2024, self-preference
reads: the draft or the report · the job page or the Block files it cites
returns: a review verdict: ready, or the step to return to and why
test now: T7 independent
test in use: T7 independent


What the literature says
------------------------

rationale: A model evaluator scores its own outputs higher than others that human raters judge equal [Panickssery 2024], so the writer never reviews its own draft or report.
context: Large language models used as evaluators [Panickssery 2024].
steps: 1. Give the reviewer the draft and the files it rests on. 2. It returns ready or a route. 3. The route reopens the owning step.
strengths: The review cannot be passed by the writer's own preference (ours).
limitations: Two agents of the same model may share blind spots; a person still signs the send or the release (ours).


Applied to AI
-------------

agent: haipipe-cowork-reviewer-agent (planned) for drafts; haipipe-page-check-agent for reports.
steps: 1. Read the draft or report. 2. Check it against the job page or the cited files. 3. Return ready or a route.
returns: a verdict with its route.
verify: The reviewer differs from every writer of the thing (T2, T7).
risk: A reviewer that sees the writer's reasoning may adopt it; it reads only the files (ours).
evidence on ai: Self-preference [Panickssery 2024] is why the writer never reviews its own draft.
skill: haipipe-writing
