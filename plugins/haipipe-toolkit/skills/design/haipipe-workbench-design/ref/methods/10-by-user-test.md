By user test
============

One design method card. Guide › Method shows it among its method cards; its
papers are the rows of `../design-papers.md` whose `group` is `by user test`. A
claim names its source in brackets; "(ours)" marks the workbench's own judgment.

family: Making internal insights now: induction in small loops; the AI learns from
  readers while it designs
reasoning: abduction, deduction and induction in small loops: draft, show readers,
  learn, revise
move: Show drafts to readers, real or simulated, and revise on what they do.
taxonomy: Target population-centred: based on the views and actions of the people who
  will use it [O'Cathain 2019 taxonomy].
comes from: Gould & Lewis 1985, user-centred design; ISO 9241-210, human-centred design;
  Yardley 2015, person-based approach
reads: design requirements · reader profiles
returns: the design, and what users did each round
test now: T3 is the method itself
test in use: T4 against the control


What the literature says
------------------------

rationale: Focus on users early and continually, measure their use, and design
  iteratively [Gould & Lewis 1985]. Base the design on the views and actions of
  the people who will use it [Yardley 2015].
context: Interactive computer systems [Gould & Lewis 1985]; digital health interventions
  [Yardley 2015]; tobacco education campaigns [Noar 2018]; language models
  standing in for survey respondents [Argyle 2023].
steps: Focus on users early, measure their use, and design iteratively: simulate,
  prototype, test, change and test again [Gould & Lewis 1985]. Run qualitative
  research with users at every stage, from planning to feasibility testing and
  implementation [Yardley 2015]. Test early versions on small samples with
  think-aloud interviews, videos or diaries, then on a more diverse population
  [O'Cathain 2019 taxonomy].
strengths: Qualitative research with users at every stage shows the context the design
  will be used in [Yardley 2015]. Thinking aloud changes thought only when it
  asks for what would not otherwise be attended to [Ericsson & Simon 1980].
  Conditioned on real backstories, a language model reproduced the answers of
  human subgroups [Argyle 2023]. Its authors report person-based interventions
  that were effective in randomised trials [O'Cathain 2019 taxonomy].
limitations: The principles are not intuitive to designers [Gould & Lewis 1985].
  Measures of perceived message effectiveness vary widely [Noar 2018], and
  readers' ratings correlate with attitude change at about .41 [Dillard
  2007]. Directed feedback between rounds raised average quality but not the
  best entries [Wooten & Ulrich 2016]. The iterative cycle can be hard to run
  quickly in practice [O'Cathain 2019 taxonomy].


Applied to AI
-------------

agent: The agent reads the design requirements and profiles of the people it is for, and
  runs simulated readers built from them.
steps: 1. Build simulated readers from real profiles [Argyle 2023]. 2. Show them the
  draft and record what they understand and would do. 3. Revise. 4. Repeat, then
  pretest with real readers (T3).
returns: The design, and what readers did in each round.
verify: A pretest with real readers (T3) before the Exp (T4).
risk: Simulated readers are not validated for this population (ours). Readers' ratings
  track attitude change only at about .41 [Dillard 2007].
evidence on AI: A language model conditioned on real backstories reproduced the answers
  of human subgroups [Argyle 2023]. Generative agents simulate believable
  human behaviour [Park 2023].
skill: haipipe-design-by-user-test (proposed)
