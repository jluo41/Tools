By snowballing
==============

One Discovery method card. The Discovery workbench shows it in the shared Guide › Method; its
papers are the rows of `../../../related/papers.md` whose `group` is `by snowballing`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Find: How do candidate papers turn up, with the search recorded?
move: From one paper already trusted, follow its reference list (backward) and the papers that cite it (forward); each step is recorded as a channel.
comes from: Wohlin 2014, guidelines for snowballing in systematic literature studies (title read only)
reads: one trusted paper · its reference list · its citing papers
returns: a list of candidate papers with the seed paper that led to each
test now: T1 search recorded
test in use: T1 search recorded


What the literature says
------------------------

rationale: Snowballing is a way to find papers that a database query misses, by following references and citations from a start set [Wohlin 2014].
context: Systematic literature studies in software engineering [Wohlin 2014].
steps: 1. Choose the seed paper. 2. List its references and its citing papers. 3. Note which seed led to which candidate. 4. Repeat with a new seed if needed.
strengths: A good paper leads to its neighbours, which a keyword search can miss (ours).
limitations: It follows the seed's own habits of citing, so a narrow seed gives a narrow list (ours).


Applied to AI
-------------

agent: haipipe-discovery-search-worker-agent follows the links and returns candidates; it opens no Run.
steps: 1. Read the seed. 2. List backward and forward links. 3. Return candidates with the seed named. 4. Stop.
returns: candidate papers with the seed named for each.
verify: Every candidate names the seed paper that led to it (T1).
risk: An agent may follow links without limit; a round count is written first (ours).
evidence on ai: No study tests agents snowballing literature (ours).
skill: haipipe-discovery-search
