By claim and warrant
====================

One story method card. The Paper workbench shows it in the shared Guide › Method,
under Story methods; its papers are the rows of `../../paper-papers.md` whose
`group` is `by claim and warrant`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Story: What do we claim, on what evidence?
move: Write each claim with its grounds (the evidence) and its warrant (why that
  evidence supports the claim), and with the qualifier and rebuttal that bound it.
comes from: Toulmin 2003, the uses of argument
reads: the Story's questions
returns: each claim with grounds, warrant, qualifier and rebuttal
test now: T1 warranted
test in use: T5 answered


What the literature says
------------------------

rationale: An assertion is justified by grounds, a warrant licensing the step from
  grounds to claim, backing for the warrant, and a qualifier and rebuttal that bound it,
  judged by the norms of its field [Toulmin 2003].
context: Argumentation theory, across fields with different standards of justification
  [Toulmin 2003].
steps: 1. State the claim. 2. Name the evidence that will ground it. 3. Write why that
  evidence would support it. 4. Write when it would not hold.
strengths: A reviewer's objection usually attacks one part: the grounds, the warrant or
  the scope; the Story shows which part to strengthen (ours).
limitations: A clean layout can make a weak warrant look strong; the warrant still has
  to be judged (ours).


Applied to AI
-------------

agent: The Story agent writes the claims; the board reviewer reviews them.
steps: 1. For each question, write its claim. 2. Fill grounds, warrant and bounds. 3.
  Review by an agent that did not write them.
returns: the Story's claims, one per question.
verify: Every claim names its evidence and its warrant (T1).
risk: A model writes confident claims without the qualifier; the rebuttal line is
  required (ours).
evidence on ai: No study tests agent-written warrants for paper claims (ours).
skill: haipipe-paper-story
