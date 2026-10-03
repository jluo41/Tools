By rung
=======

One design method card. The Insight workbench shows it in the shared Guide › Method › Design
methods; its papers are the rows of `../../insight-papers.md` whose `group` is
`by rung`. A claim names its source in brackets; "(ours)" marks the workbench's own
judgment.

family: From the goal: the ask decides the design before any data is read
move: Place the question on its DIKW rung first; the rung decides which claim the answer
  may make and which words of the ask are refused.
taxonomy: Data and Information are description; Knowledge is prediction or causal
  inference; Wisdom is a decision that uses them [Hernán 2019] (the mapping is ours).
comes from: Ackoff 1989, data to wisdom; Rowley 2007, the DIKW hierarchy
reads: ask · the DIKW ladder
returns: the rung, the claim it allows, the words it refuses or routes up
test now: T0 covered · T2 agreed
test in use: T4 reproduced


What the literature says
------------------------

rationale: Data, information, knowledge, understanding and wisdom form a hierarchy in
  which each level builds on the one below [Ackoff 1989]. The hierarchy is widely
  taken for granted in information science, and textbooks agree and dissent on
  how each level is defined [Rowley 2007]. The type of a question (descriptive,
  exploratory, inferential, predictive, causal, mechanistic) decides which analysis
  can answer it [Leek 2015].
context: Information management and knowledge management [Rowley 2007]; data science,
  sorted into description, prediction and causal inference [Hernán 2019];
  observational health research, where the words that link exposure to outcome are
  read as causal to different degrees [Haber 2022].
steps: 1. Write the ask. 2. Name its rung: what was observed (Data), a derived pattern
  such as a rate or a contrast (Information), a claim of why or of what will happen
  (Knowledge), advice on what to do (Wisdom). 3. Name the claim the rung allows. 4.
  Refuse a causal verb at Data or Information, or route it to a Knowledge question
  that states its causal goal openly instead of hiding it behind the word
  association [Hernán 2018].
strengths: Separating description, prediction and causal inference shows which tasks
  need causal knowledge from outside the data [Hernán 2019]. A refused word is
  visible on the page, so a reader sees what the answer does not claim (ours).
limitations: The hierarchy is argued to be unsound, with a central logical error and an
  inductivist backdrop [Frické 2009]. Word rules alone do not keep a claim on its
  rung: over half of reviewers rated "association" as having some causal
  implication, and action recommendations often implied more causality than the
  linking sentence [Haber 2022].


Applied to AI
-------------

agent: A drafter agent reads only the ask and the ladder, not the existing tasks or
  results.
steps: 1. Tag the rung. 2. List each content word of the ask. 3. Mark any causal verb
  (causes, drives, makes, because) on a Data or Information ask. 4. Refuse it, or
  route it to a Knowledge question.
returns: The rung, the claim it allows and a refusal list, written on the question's
  register row.
verify: A second agent, given the ask and not the drafter's tag, tags the rung and the
  causal words (T2); the two tags must agree, and every content word must be
  covered or refused (T0).
risk: A model trained on published prose may carry its causal drift into the ask
  (ours): 32.4% of conclusions of observational studies used some direct causal
  language [Yu 2019].
evidence on ai: A BERT classifier sorted research conclusion sentences into no
  relationship, correlational, conditional causal and direct causal with accuracy
  0.90 [Yu 2019]. No study tests an agent placing a question on its rung (ours).
skill: haipipe-insight-question
