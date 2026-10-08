By one paper per Run
====================

One Discovery method card. The Discovery workbench shows it in the shared Guide › Method; its
papers are the rows of `../../../related/papers.md` whose `group` is `by one paper per run`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Read: How does one paper become one filed Result?
move: Give each paper its own ticket runs/rNN_<author><year>_<paper>.sh and a Result of the same name holding the card, facts, receipt and one-entry BibTeX.
comes from: Page et al. 2021, PRISMA 2020, reporting items for each included study (title read only)
reads: one candidate paper · the Task's Question
returns: a Run and its same-name Result: card, facts, receipt, one-entry .bib
test now: T2 one paper
test in use: T2 one paper


What the literature says
------------------------

rationale: A reporting guideline for systematic reviews asks that each included study be described one by one [Page 2021]; one Run for one paper keeps each claim next to its source.
context: Reporting of systematic reviews [Page 2021].
steps: 1. Resolve the one paper. 2. Name the Run with its number, author, year and short title. 3. Read it and write the Result files. 4. Mark what is unverified.
strengths: A claim in a report can be traced to one Result and one paper (ours).
limitations: Many papers mean many Runs; the Block's table is how they are listed (ours).


Applied to AI
-------------

agent: haipipe-discovery-creator-agent writes the Run and its Result; a link that names many papers is split into many Runs.
steps: 1. Resolve the Subject. 2. Allocate the Run name. 3. Write card, facts, receipt, .bib. 4. Stop for the checker.
returns: rNN_<...>.sh and results/rNN_<...>/ with four files.
verify: Run and Result share one name, and the Run has one Subject (T2).
risk: An agent may read two papers in one Run to save time; the checker counts Subjects (ours).
evidence on ai: No study tests agents reading one paper per ticket (ours).
skill: haipipe-discovery-review
