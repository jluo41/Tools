By named channel
================

One Discovery method card. The Discovery workbench shows it in the shared Guide › Method; its
papers are the rows of `../../../related/papers.md` whose `group` is `by named channel`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Find: How do candidate papers turn up, with the search recorded?
move: Search one named channel at a time (a database, a preprint server, a citation graph) and record its query, its date and how many candidates it returned; file nothing yet.
comes from: Rethlefsen et al. 2021, PRISMA-S, a checklist for reporting literature searches
reads: the Task's question · the channel's own search help
returns: a list of candidate papers per channel, with query, date and count
test now: T1 search recorded
test in use: T1 search recorded


What the literature says
------------------------

rationale: Literature searching is often poorly reported, and guidance for reporting it has been diverse [Rethlefsen 2021]; a recorded query and date let anyone repeat the search.
context: Reporting of searches in systematic reviews and related review types [Rethlefsen 2021].
steps: 1. Pick the channel. 2. Write the query. 3. Run it and note the date. 4. List the candidates and the count.
strengths: A missing paper can be traced to a channel that was never searched (ours).
limitations: Channels differ in coverage, and no list of channels is complete (ours).


Applied to AI
-------------

agent: haipipe-discovery-search-worker-agent returns candidates only; it never judges relevance or opens a Run.
steps: 1. Take one channel. 2. Run the query. 3. Return candidates with identity. 4. Stop.
returns: candidate papers with query, date and count, as text.
verify: Each channel names query, date and count (T1).
risk: An agent may report a paper it never saw in the channel; each candidate carries a link (ours).
evidence on ai: No study tests agents searching channels for this loop (ours).
skill: haipipe-discovery-search
