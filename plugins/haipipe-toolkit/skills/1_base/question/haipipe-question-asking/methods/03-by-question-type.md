By question type
================

One question-asking method card (`haipipe-question-asking`). The Insight workbench shows it in
the shared Guide › Method, step 1; its papers are the rows of that workbench's
`servers/workbench-insight/related/papers.md` whose `group` is `by question type`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Question-asking
move: Name the question's type first (descriptive, exploratory, inferential, predictive,
  causal or mechanistic), then compute only the analysis that type allows.
taxonomy: Names one of the six types [Leek 2015] and one of the three tasks [Hernán
  2019].
comes from: Leek 2015, six question types; Hernán 2019, three data science tasks
reads: question · its level · the six types
returns: the question's type and task, the analysis it allows, and the words it refuses
test now: T4 spec · T6 a different agent names the same type
test in use: T8 the same analysis gives the same answer on another partition


What the literature says
------------------------

rationale: Mistaking the type of question is the most common error in data analysis
  [Leek 2015]. Description, prediction and causal inference need different data,
  assumptions and analytics, so the task is named first [Hernán 2019].
context: Data analysis in general [Leek 2015]; the health and social sciences, where
  causal questions are common [Hernán 2019].
steps: 1. Ask whether the aim is to summarise, to find patterns, to generalise, to
  predict for a unit, to learn what changing one thing does, or how it does it
  [Leek 2015]. 2. Map the type to description, prediction or causal inference
  [Hernán 2019]. 3. Choose the analysis the type allows. 4. Refuse the words a
  higher type would need: a descriptive answer says no "because" (ours).
strengths: It fixes the claim an answer may make before the answer is seen (ours). It
  makes explicit that a causal analysis also needs subject-matter knowledge
  [Hernán 2019].
limitations: The type says which analysis, not how to run it: turning a question into a
  model has its own steps, such as sub-hypotheses, proxy variables and the model
  [Jun 2022]. How strong an answer must be, and for which quantity, is a Design
  method (estimand, analysis plan) (ours).


Applied to AI
-------------

agent: The agent reads the question and its level, and names the type before it reads any
  task (ours).
steps: 1. Name the type, with its reason. 2. Name the task. 3. Write the analysis the type
  allows into the work spec [Hernán 2019]. 4. List the refused words.
returns: The type, the task, the analysis allowed and the refused words, on the
  question's register row.
verify: A different agent, not shown the first answer, names the type; a disagreement goes
  back to the question (T6).
risk: Analysts fix on implementation and fit the analysis to familiar approaches, even
  when sub-optimal [Jun 2022]; an agent can fit the question to the tools it has
  (ours).
evidence on AI: 257 data analysis questions were put into closed form so that 34 LLMs
  could be scored automatically [Hu 2024]; closed questions are the easy end of the
  types (ours).
skill: haipipe-insight-evidence-plan
