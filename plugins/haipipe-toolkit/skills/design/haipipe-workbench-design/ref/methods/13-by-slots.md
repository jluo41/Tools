By slots
========

One design method card. Guide › Method shows it among its method cards; its
papers are the rows of `../design-papers.md` whose `group` is `by slots`. A claim
names its source in brackets; "(ours)" marks the workbench's own judgment.

family: Goal Only: abduction-2; the design reads only the task, so the how is invented,
  or several hows are sent and the Exp picks
reasoning: abduction on one slot at a time; the Exp's factorial data does the induction,
  slot by slot
move: Split the artifact into slots, list the options for each, change one slot at a
  time.
taxonomy: Efficiency-based: components are tested in experimental designs to find the
  active ones [O'Cathain 2019 taxonomy].
comes from: Zwicky 1969, morphological box; Suh 1990, axiomatic design; Collins 2018,
  MOST
reads: design requirements · the artifact's slots
returns: the options per slot, and the one slot changed
test now: T0 rules · T1 one slot only
test in use: T4 factorial


What the literature says
------------------------

rationale: Split a problem into its variables and combine the options of each [Zwicky
  1969]; give each requirement its own design parameter [Suh 1990]; test
  components in factorial experiments and keep those that work [Collins 2018].
context: Engineering design from functions to parts [Pahl & Beitz 1984]; behavioural and
  biomedical interventions [Collins 2018]; product design from conjoint data
  [Balakrishnan 1996]. Multiphase optimization, fractional factorial experiments
  and micro-randomised trials [O'Cathain 2019 taxonomy].
steps: List the problem's variables and the options of each, then examine their
  combinations [Zwicky 1969]. Test the components in factorial experiments and keep
  those that work [Collins 2018]. MOST runs in three phases: 1. Preparation, a model
  built from theory, literature and existing data. 2. Optimisation, a randomised
  experiment on the components (fractional factorial, sequential multiple-assignment or
  micro-randomised). 3. Evaluation, a standard randomised trial [O'Cathain 2019
  taxonomy]. Fractional factorial designs find the active components, their
  interactions, the best doses and tailoring to sub-groups [O'Cathain 2019 taxonomy].
strengths: Each slot's effect can be estimated on its own [Collins 2018]. A modular
  design cuts the cost of testing [Loch 2001]. Changing one slot makes the
  difference between designs exact (ours).
limitations: No study tests the method against another (ours). It assumes slots act
  apart; a slot whose effect depends on another is missed when one changes at
  a time (ours).


Applied to AI
-------------

agent: The agent splits the base design (the Design Goal's starting text) into slots,
  such as the sender, the action, the reason and the closing.
steps: 1. Split the base design into slots. 2. List the options for each slot, within
  the rules. 3. Change one slot and keep the others word for word. 4. Name the slot
  and the option changed.
returns: The options per slot, the one slot changed, and the design.
verify: Verify checks that only the named slot differs from the base (T1), as the card's
  Design elements show word by word, and checks the rules (T0).
risk: An AI asked to change one slot rewords others too (ours); the word diff catches
  it.
evidence on AI: No study tests an AI designing by slots yet (ours). Search over
  attribute-based product designs is old [Balakrishnan 1996].
skill: haipipe-design-by-slots (proposed)
