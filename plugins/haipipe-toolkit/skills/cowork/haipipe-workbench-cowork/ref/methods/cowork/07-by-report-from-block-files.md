By report from block files
==========================

One CoWork method card. The CoWork workbench shows it in the shared Guide › Method; its
papers are the rows of `../../cowork-papers.md` whose `group` is `by report from block files`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Report: How does the answer reach the reader, checked?
move: Answer a Question with a report Page written from the Block's own files (job pages, Timeline, design notes, meeting notes), each claim citing the file it came from.
comes from: Wilson et al. 2017, good enough practices
reads: the Question's Logic · the Block files it cites
returns: the report Page: Answer, Evidence, Limits, Next
test now: T6 cited
test in use: T7 independent


What the literature says
------------------------

rationale: Keeping inputs, work and outputs apart and writing down what was done makes work understandable to others and to yourself later [Wilson 2017]; a report that cites the exact file keeps that link.
context: Practices for scientific computing, applied here to coordination files [Wilson 2017].
steps: 1. Read the Question's Logic. 2. Pick the files that answer it. 3. Write Answer, Evidence, Limits, Next. 4. Cite the file for each claim.
strengths: A reader can follow every claim back to a file (ours).
limitations: A cited file can change after the report; the check reads the file again (ours).


Applied to AI
-------------

agent: haipipe-page-writing-agent writes; haipipe-page-check-agent checks.
steps: 1. Read the Logic and the files. 2. Write the report. 3. Cite each claim. 4. Stop for the checker.
returns: reports/qNN_<topic>/qNN_<topic>.md.
verify: Every claim names a file that exists (T6).
risk: An agent may state an answer the files do not hold; the check reads each cited file (ours).
evidence on ai: No study tests agents reporting from coordination files (ours).
skill: haipipe-page-writing
