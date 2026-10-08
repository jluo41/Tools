By one topic
============

One Discovery method card. The Discovery workbench shows it in the shared Guide › Method; its
papers are the rows of `../../../related/papers.md` whose `group` is `by one topic`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Scope: How is one literature topic bounded?
move: Name the Block as one reading topic with a spine (what it covers and where it stops) and a close condition, then give each inquiry its own Job.
comes from: Grant & Booth 2009, review types differ in how they search, appraise and synthesize
reads: the Project's discoveries/README.md · the Questions the Block must answer
returns: the Block's board.md header and one Job folder for each inquiry
test now: T0 bounded
test in use: T0 bounded


What the literature says
------------------------

rationale: Review types differ in their search, appraisal and synthesis [Grant 2009], so the Block says which kind of reading it is doing and where it ends before any paper is read.
context: A typology of 14 review types, with examples from health and health information [Grant 2009].
steps: 1. Ask what one topic this is. 2. Write the spine and where it stops. 3. Write what must be true to close it. 4. Open one Job for each inquiry.
strengths: A reader can tell in one minute what the Block covers and when it is done (ours).
limitations: A topic can grow past its spine; a split is a new Block, and a Block number never changes (ours).


Applied to AI
-------------

agent: haipipe-discovery-orchestrator-agent writes the header; the person agrees the spine and the close condition.
steps: 1. Read the Project's discoveries/README.md. 2. Write the header lines. 3. Open the Jobs. 4. Stop for the person.
returns: the Block's board.md header and its Job folders.
verify: Spine, close condition and one inquiry per Job are all written (T0).
risk: An agent may write a close condition nothing can test, such as "read everything" (ours).
evidence on ai: No study tests agents scoping a literature topic (ours).
skill: haipipe-discovery
