By checklist draft
==================

One CoWork method card. The CoWork workbench shows it in the shared Guide › Method; its
papers are the rows of `../../cowork-papers.md` whose `group` is `by checklist draft`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Job: How does a request to another office stay one thing, and keep moving?
move: Write the steps of a request in the Job's CHECKLIST.md in order, and draft each message inside its step (or in the Job's emails/), marked draft until the person sends it.
comes from: Haynes et al. 2009, a checklist to improve team communication
reads: the job page · the Job's CHECKLIST.md · the thread so far in emails/
returns: a draft in its checklist step or emails/<thread>.md, marked status: draft
test now: T2 reviewed draft
test in use: T3 person sends


What the literature says
------------------------

rationale: A 19-item checklist designed to improve team communication and consistency of care reduced complications and deaths in a study of eight hospitals [Haynes 2009]. A checklist step with its draft inside keeps the message next to the reason for it.
context: Checklists in surgery, a field with high-stakes handoffs [Haynes 2009].
steps: 1. Add the step. 2. Draft the message inside it. 3. Mark it draft. 4. Hand it to review. 5. The person sends and ticks the step.
strengths: A step number never changes once cited, so a later email can point at it (ours).
limitations: A checklist can become a ritual; steps that no longer matter are closed, not deleted (ours).


Applied to AI
-------------

agent: haipipe-cowork-agent (planned) drafts; no agent sends.
steps: 1. Read the job page and the thread. 2. Draft in the step. 3. Mark status: draft. 4. Stop for the reviewer.
returns: a draft message with status: draft.
verify: The draft is marked and no sent-looking copy exists before the person sends (T3).
risk: An agent may write as if the message were already sent; the draft mark is what stops that (ours).
evidence on ai: No study tests agents drafting coordination messages (ours).
skill: haipipe-cowork
