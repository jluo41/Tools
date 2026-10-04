By one main idea
================

One framing method card. The Paper workbench shows it in the shared Guide › Method,
under Framing methods; its papers are the rows of `../../paper-papers.md` whose
`group` is `by one main idea`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Framing: Which question is worth asking?
move: Give the paper one central contribution and build every part around it: the title
  says it, the abstract states it, each Section serves it.
comes from: Mensh & Kording 2017, ten simple rules for structuring papers
reads: the admitted question
returns: the paper's one contribution, in one sentence, at the top of the Story
test now: T0 asked
test in use: T5 answered


What the literature says
------------------------

rationale: Rules for structuring a paper built on how readers consume it: focus the
  paper on a single central contribution, and give each part a context, a content and a
  conclusion [Mensh 2017].
context: Scientific papers in computational biology and beyond [Mensh 2017].
steps: 1. Write the contribution in one sentence. 2. Make the title state it. 3. Check
  each Story question serves it. 4. Cut or move a question that does not.
strengths: A reader can say what the paper did after the title and abstract (ours).
limitations: Some studies honestly have two findings; the method asks which one the
  paper leads with (ours).


Applied to AI
-------------

agent: The Story agent writes the contribution line with the Story.
steps: 1. Read the admitted question. 2. Write the contribution. 3. List the questions
  under it.
returns: the Story's contribution line.
verify: Every claim answers one question under the contribution (T0).
risk: A model may list every result as a contribution (ours).
evidence on ai: No study tests agents structuring a paper around one idea (ours).
skill: haipipe-paper-story
