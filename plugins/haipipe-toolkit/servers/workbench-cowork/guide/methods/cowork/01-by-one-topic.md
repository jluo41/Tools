By one topic
============

One CoWork method card. The CoWork workbench shows it in the shared Guide › Method; its
papers are the rows of `../../../related/papers.md` whose `group` is `by one topic`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Scope: How is one coordination topic bounded?
move: Name the Block as one topic with a spine (what it is and where it stops), a close condition and the gate it waits for, so every Job, email and meeting has one home.
comes from: Malone & Crowston 1994, coordination as managing dependencies
reads: the Project's cowork/README.md · the gates already named by other Blocks
returns: the Block's board.md header: state, owner, spine, close, status, waits-for
test now: T0 bounded
test in use: T0 bounded


What the literature says
------------------------

rationale: Coordination is the work of managing dependencies between activities [Malone 1994]; a gate such as an ethics approval is a dependency, so the Block names it (waits-for) instead of leaving it in someone's head.
context: Coordination theory, across computer science and organization theory [Malone 1994].
steps: 1. Ask what one topic this is. 2. Write the spine and where it stops. 3. Write what must be true to close it. 4. Name the gate it waits for.
strengths: A reader can tell in one minute what the Block is for and what blocks it (ours).
limitations: A topic can grow past its spine; a split is a new Block, and a Block number never changes (ours).


Applied to AI
-------------

agent: haipipe-cowork-agent (planned) writes the header; the person agrees the spine and the close condition.
steps: 1. Read the Project's cowork/README.md. 2. Write the header lines. 3. Name the waits-for Block. 4. Stop for the person.
returns: the Block's board.md header.
verify: Spine, close and waits-for are all filled in (T0).
risk: An agent may write a close condition that nothing can test, such as "all done" (ours).
evidence on ai: No study tests agents bounding coordination topics (ours).
skill: haipipe-cowork
