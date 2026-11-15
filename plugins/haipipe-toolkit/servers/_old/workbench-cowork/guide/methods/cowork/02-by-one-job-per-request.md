By one job per request
======================

One CoWork method card. The CoWork workbench shows it in the shared Guide › Method; its
papers are the rows of `../../../related/papers.md` whose `group` is `by one job per request`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Job: How does a request to another office stay one thing, and keep moving?
move: Give every request to another office its own Job folder `jNN_<job>/`; its page header holds the state, who we wait on, since when and the next step, and the page says what we asked the office for and why.
comes from: Malone & Crowston 1994, dependencies; Harris et al. 2009, research IT support for clinical studies (title read only)
reads: the Block's board.md · the office's own number, if it has one
returns: a Job folder jNN_<job>/ with its page jNN_<job>.md
test now: T1 one Job
test in use: T1 one Job


What the literature says
------------------------

rationale: A request to another office is a dependency with a named owner on the other side [Malone 1994]; research IT support for clinical studies is organized around such requests [Harris 2009]. One page per request keeps its history in one place.
context: Coordination theory and research informatics support [Malone 1994; Harris 2009].
steps: 1. Write what we need and from whom. 2. Make the Job folder and its page. 3. Fill the header lines. 4. Set waiting-on and next.
strengths: Nothing about a request lives only in a mail thread (ours).
limitations: Two requests to one office can be merged by habit; each still gets its own page (ours).


Applied to AI
-------------

agent: haipipe-cowork-agent (planned) writes the Job page; the person signs the request.
steps: 1. Read the Block's header. 2. Write the Job page and header. 3. Add Timeline.md. 4. Stop for the person.
returns: jNN_<job>/jNN_<job>.md with its header lines.
verify: Every Job folder has a page with state, waiting-on, since and next (T1).
risk: An agent may invent the office's ticket number; it leaves the ticket: line empty until the office gives one (ours).
evidence on ai: No study tests agents opening coordination Jobs (ours).
skill: haipipe-cowork
