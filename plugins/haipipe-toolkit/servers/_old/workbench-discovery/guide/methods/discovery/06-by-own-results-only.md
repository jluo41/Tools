By own Results only
===================

One Discovery method card. The Discovery workbench shows it in the shared Guide › Method; its
papers are the rows of `../../../related/papers.md` whose `group` is `by own results only`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Synthesize: How do many Results become one finding?
move: Write the Task's closing file (summary, verdict or landscape) only from the Task's own Results, and name the Run behind every sentence.
comes from: Grant & Booth 2009, search, appraisal, synthesis and analysis (SALSA) as separate steps
reads: the Task's Results: cards, facts, receipts
returns: summary.md, verdict.md or landscape.md in the Task folder
test now: T5 own Results
test in use: T5 own Results


What the literature says
------------------------

rationale: Review types separate search, appraisal and synthesis [Grant 2009], so a synthesis uses what was read and appraised in the Task, not what the writer remembers.
context: A typology of review types and their methods [Grant 2009].
steps: 1. List the Task's Results. 2. Group their Readouts by finding. 3. Write each sentence with its Run. 4. List what the Results do not settle.
strengths: No sentence rests on a paper the Task never read (ours).
limitations: A good paper outside the Task is missed until a Run is added for it (ours).


Applied to AI
-------------

agent: haipipe-discovery-creator-agent writes the synthesis; the reviewer checks it.
steps: 1. Read every Result of the Task. 2. Write the file. 3. Name the Run for each sentence. 4. Stop for the reviewer.
returns: the Task's summary.md, verdict.md or landscape.md.
verify: Every sentence names a Run of this Task (T5).
risk: An agent may add a well-known paper from memory; it adds a Run first (ours).
evidence on ai: No study tests agents synthesizing from filed Results (ours).
skill: haipipe-discovery-synthesize
