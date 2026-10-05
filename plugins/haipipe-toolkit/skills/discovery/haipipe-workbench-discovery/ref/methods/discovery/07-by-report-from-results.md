By report from Results
======================

One Discovery method card. The Discovery workbench shows it in the shared Guide › Method; its
papers are the rows of `../../discovery-papers.md` whose `group` is `by report from results`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Answer: How does the answer reach the reader, checked?
move: Write the Question's report Page (Answer, Evidence, Limits, Next) from the Block's own Results, each claim naming its Run.
comes from: Page et al. 2021, PRISMA 2020, reporting what was found and from where (title read only)
reads: the Block's syntheses and Results · the Question
returns: a report Page in reports/qNN_<topic>/
test now: T6 cited
test in use: T6 cited


What the literature says
------------------------

rationale: A reporting guideline asks for the results of each synthesis and the certainty of the evidence [Page 2021]; the Page keeps both next to the claim by naming the Run.
context: Reporting of systematic reviews [Page 2021].
steps: 1. Read the Block's syntheses. 2. Write the Answer. 3. Name each Run under Evidence. 4. Write Limits and Next.
strengths: A reader can follow any claim back to a paper (ours).
limitations: A report is only as wide as the Runs behind it (ours).


Applied to AI
-------------

agent: haipipe-page-writing-agent writes the Page; haipipe-page-check-agent checks it.
steps: 1. Read the Results. 2. Write the Page. 3. Name the Runs. 4. Stop for the checker.
returns: reports/qNN_<topic>/qNN_<topic>.md.
verify: Every claim names a Run that exists (T6).
risk: An agent may write a confident Answer over thin evidence; Limits says how thin (ours).
evidence on ai: No study tests agents writing evidence reports from filed Results (ours).
skill: haipipe-page-writing
