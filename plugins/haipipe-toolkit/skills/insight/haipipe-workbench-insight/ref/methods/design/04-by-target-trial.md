By target trial
===============

One design method card. The Insight workbench shows it in Scope › Methods › Design
methods; its papers are the rows of `../../insight-papers.md` whose `group` is
`by target trial`. A claim names its source in brackets; "(ours)" marks the workbench's
own judgment.

family: From the claim
status: future: a Knowledge question with a causal verb is designed this way once the
  board answers causal questions
move: For a causal ask on data already collected, write the protocol of the randomised
  trial that would answer it, then say how the data emulate each part.
taxonomy: Knowledge, causal inference [Hernán 2019].
comes from: Hernán 2016 emulate, target trial emulation; Hernán 2016 specifying, aligned
  start of follow-up
reads: ask · rung · the order in time of the data
returns: a protocol in two columns, target and emulation: eligibility, strategies,
  assignment, outcome, follow-up and its start, causal contrast, analysis plan, and
  the parts that cannot be emulated
test now: T1 specified · T2 agreed
test in use: T4 reproduced


What the literature says
------------------------

rationale: Causal inference from large observational databases can be seen as an
  attempt to emulate the randomised trial that would answer the question; making
  that target trial explicit organises the analysis and helps avoid common pitfalls
  [Hernán 2016 emulate]. Specifying the target trial prevents immortal time bias
  and other self-inflicted injuries [Hernán 2016 specifying].
context: Comparative effectiveness and safety research with health databases [Hernán
  2016 emulate]; 200 studies across 26 fields of medicine, 84% of them published
  from 2020 on [Hansford 2023].
steps: 1. Write the target trial's protocol: eligibility, treatment strategies,
  assignment, outcome, follow-up, causal contrast and analysis plan [Hansford 2023].
  2. Emulate each part with the data. 3. Start follow-up when eligibility is met and
  a strategy is assigned [Hernán 2016 specifying]. 4. Report the protocol and its
  emulation side by side [Cashin 2025].
strengths: In 32 trials emulated with insurance claims, agreement with the trial's
  result had a Pearson correlation of 0.82, and 0.93 in the 16 emulated most closely
  [Wang 2023].
limitations: Agreement fell to 0.53 in the 16 trials whose question-defining design
  elements could not be emulated closely [Wang 2023]. Of 200 emulation studies, 57%
  did not describe the protocol of the target trial and its emulation [Hansford 2023].


Applied to AI
-------------

agent: Routed only for a Knowledge question with a causal verb; the drafter writes the
  target trial before any task is read.
steps: 1. Write each protocol part. 2. Name the data that emulate it, or the gap. 3.
  Fix the start of follow-up. 4. Name the rivals (confounding, selection) that the
  emulation cannot rule out.
returns: The two-column protocol with its gaps, as the need's work spec.
verify: A second agent checks that each part is present and that eligibility,
  assignment and start of follow-up line up (T1, T2).
risk: An emulation that cannot reproduce a part is still reported as causal (ours).
evidence on ai: A language model pipeline turned free-text target trial descriptions
  into structured specifications and executable code, with field-level sensitivity
  of 0.83 to 0.97 on studies in a common data model [Kim 2026].
skill: haipipe-insight-by-target-trial (proposed)
