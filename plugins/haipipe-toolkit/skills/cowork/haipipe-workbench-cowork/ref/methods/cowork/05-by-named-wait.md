By named wait
=============

One CoWork method card. The CoWork workbench shows it in the shared Guide › Method; its
papers are the rows of `../../cowork-papers.md` whose `group` is `by named wait`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Job: How does a request to another office stay one thing, and keep moving?
move: Record who the next move belongs to and since when; when it changes hands, change waiting-on and since in the job page header, and add the date to the Job's Timeline.md.
comes from: Herbsleb & Mockus 2003, delay in distributed work
reads: the job page header · the Job's Timeline.md
returns: updated waiting-on and since in the header, one Timeline line, a follow-up draft when the wait is ours to chase
test now: T4 wait named
test in use: T4 wait named


What the literature says
------------------------

rationale: Work items that involve people at more than one site took about two and one half times as long as colocated ones, and the number of people involved was strongly related to the calendar time [Herbsleb 2003]. A request to another office is that case, so the wait is made visible.
context: Distributed software development, measured from change records and a survey [Herbsleb 2003].
steps: 1. Note the move that just happened. 2. Set waiting-on to whoever moves next. 3. Set since to today. 4. Add the date to Timeline.md.
strengths: Check › Waiting on lists open Jobs by days waited, with no one keeping a list by hand (ours).
limitations: A date can be set wrongly; the Timeline line is the check (ours).


Applied to AI
-------------

agent: haipipe-cowork-agent (planned) updates the header and drafts the follow-up.
steps: 1. Read the job page header and Timeline. 2. Update the header. 3. Add the line. 4. Draft a follow-up if the wait is ours.
returns: the changed header lines and the Timeline line.
verify: The header's since matches the last move in Timeline.md (T4).
risk: An agent may update since without a real move; the Timeline line must name it (ours).
evidence on ai: No study tests agents tracking waits (ours).
skill: haipipe-cowork
