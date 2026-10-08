By theory
=========

One design method card. Guide › Method shows it among its method cards; its
papers are the rows of `../../related/papers.md` whose `group` is `by theory`. A claim
names its source in brackets; "(ours)" marks the workbench's own judgment.

family: External Insights: abduction-1; the how comes from the literature and theory,
  other people's data
reasoning: abduction-1: requirements + a theory's how → a design; then deduction: the
  theory predicts the variable it moves
move: Choose a named theory, use the technique it prescribes, predict the one variable
  it moves.
taxonomy: Evidence and theory-based: published evidence combined with formal theory
  [O'Cathain 2019 taxonomy].
comes from: Bartholomew 1998, Intervention Mapping; Michie 2011, Behaviour Change Wheel
reads: design requirements · external insights: named theories
returns: the design, its mechanism, the variable it moves, a prediction
test now: T1 technique present · T3 pretest
test in use: T4 against the control


What the literature says
------------------------

rationale: Health education needs an explicit process for turning theory and evidence
  into an intervention [Bartholomew 1998]. An intervention should be linked to
  an analysis of the behaviour it targets [Michie 2011].
context: Health education programs [Bartholomew 1998]; tobacco control and obesity
  [Michie 2011]; physical activity and healthy eating [Prestwich 2013].
steps: Intervention Mapping: 1. a matrix of proximal program objectives. 2. Theory-based
  methods and practical strategies. 3. The program's design. 4. Adoption and
  implementation plans. 5. Evaluation plans [Bartholomew 1998]. Map behavioural
  determinants to behaviour change techniques; matrices built by experts let
  non-experts do it [O'Cathain 2019 taxonomy].
strengths: The behaviour change wheel joins nine intervention functions and seven policy
  categories to a model of behaviour [Michie 2011]. 93 named techniques, most
  coded with good agreement, make a technique checkable [Michie 2013]. Their
  authors report interventions developed this way that were found effective,
  for Intervention Mapping and the behaviour change wheel [O'Cathain 2019
  taxonomy].
limitations: In 190 interventions, theory use was not consistently linked to effect, and
  about 90 percent did not link all their techniques to the theory's
  constructs [Prestwich 2013]. One theory cannot explain everything relevant,
  so several may be needed [O'Cathain 2019 taxonomy].


Applied to AI
-------------

agent: The agent reads the design requirements and external insights: a closed list of
  theories and named techniques [Michie 2013].
steps: 1. Name the behaviour and what drives it [Michie 2011]. 2. Pick the intervention
  function and one technique by its code. 3. Write the design so the technique is
  present. 4. Predict the one variable it moves.
returns: The design, its theory, the technique's code, its mechanism and its prediction.
verify: A second agent, not told the code, codes the technique it finds in the design
  (T1), as human coders do [Michie 2013]; the Exp against the control (T4)
  checks the prediction.
risk: A design can name a theory it does not use: most interventions did not link their
  techniques to the theory [Prestwich 2013].
evidence on AI: No study tests an AI designing by theory yet (ours).
skill: haipipe-design-by-theory (proposed)
