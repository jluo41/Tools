By report from results
======================

One Report method card. The Task workbench shows it in the shared Guide › Method, under the
Report methods; its papers are the rows of `../../task-papers.md` whose `group` is
`by report from results`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Report: How does the answer reach the reader, checked?
move: Write the Question's answer from exact Results, apart from the code that made them:
  every claim names the Result it came from, and the report records when it read them.
comes from: Kery et al. 2018, the story in the notebook; Pimentel et al. 2019, notebook
  reproducibility; Rule et al. 2018, exploration and explanation
reads: the Question's Logic · its Tasks' Results
returns: the report: Opening, Answer, Evidence, Limits, Next
test now: T6 cited
test in use: T7 fresh


What the literature says
------------------------

rationale: Exploratory notebooks are messy and lose their story [Kery 2018]; most public
  notebooks do not rerun to the same results [Pimentel 2019 notebooks]; notebooks rarely
  explain the analysis they hold [Rule 2018]. So the answer is written in its own Page from
  the Results of Tickets.
context: Studies of computational notebooks in data science [Kery 2018; Pimentel 2019
  notebooks; Rule 2018].
steps: 1. Read the Logic. 2. Read the Results the work wrote. 3. Write the Opening and
  Answer, each claim citing a Result. 4. Write the Limits and Next. 5. Record when the
  Results were read.
strengths: A reader can follow any sentence down to its file (ours).
limitations: A report can cite the right file and still misread it; the check reads the
  Result too (ours).


Applied to AI
-------------

agent: haipipe-page-writing-agent writes; it does not run Tasks.
steps: 1. Read the Logic and the Results. 2. Write each part. 3. Cite each claim. 4. Record
  the reading time.
returns: the report Page with its answer-status.
verify: Every claim names a Result (T6); no cited Result is newer than the reading (T7).
risk: A model may state a number it remembers rather than one it read (ours).
evidence on ai: No study tests agent-written reports against their cited Results (ours).
skill: haipipe-page-writing
