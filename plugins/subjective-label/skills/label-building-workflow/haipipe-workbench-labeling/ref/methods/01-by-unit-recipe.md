By unit recipe
==============

One labeling method card. Guide › Method shows it among its step's cards; its papers are
the rows of `../labeling-papers.md` whose `group` is `by unit recipe`. A claim names its
source in brackets; "(ours)" marks the workbench's own judgment.

family: Step 1 · Prepare: which items exist, and which are held back
move: Freeze, before any item exists, what one item is: the reply to judge, the turns
  shown as its context, and the group it belongs to.
comes from: Pustejovsky 2012, the annotation specification
reads: the raw corpus · the question
returns: a versioned recipe and the items it makes
test now: T3 sealed
test in use: T5 audit


What the literature says
------------------------

rationale: An annotation project starts by fixing what is annotated and how, before any
  label, so every annotator judges the same unit [Pustejovsky 2012].
context: Text annotation for machine learning [Pustejovsky 2012].
steps: 1. Pick the target turn. 2. Fix the context window. 3. Fix the group. 4. Write the
  recipe down, versioned.
strengths: Every item, round and test means the same thing (ours).
limitations: A unit chosen badly, too short to judge, is costly to change later (ours).


Applied to AI
-------------

agent: corpus-preparer-agent (new)
steps: 1. Read the corpus's transcripts. 2. Propose the unit. 3. Materialize and check the
  items.
returns: the recipe, the items and a check receipt
verify: a checker agent confirms counts, unique ids and that no context runs past the
  target
risk: An agent can pick the unit that is easiest to make, not the one the question needs;
  the person signs the recipe (ours).
evidence on ai: No study tests agents choosing the labeling unit (ours).
skill: subjective-label-preparation
