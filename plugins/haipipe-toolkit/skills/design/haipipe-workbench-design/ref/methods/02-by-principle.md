By principle
============

One design method card. The Design workbench shows it in the Theory of Design
Space's Design methods view; its papers are the rows of `../design-papers.md`
whose `group` is `by principle`. A claim names its source in brackets; "(ours)"
marks the workbench's own judgment.

family: Requirements only: abduction-2; the AI invents the how and the design from the
  design requirements alone
reasoning: abduction-2, made explicit: requirements → a frame, which is the how → a
  design
move: Frame what the requirements really ask, then design to that frame.
taxonomy: No category of its own; it is the first activity of human-centred design, a
  target population-centred approach [O'Cathain 2019 taxonomy].
comes from: Schön 1983, reflection-in-action; Dorst 2015, frame creation
reads: design requirements
returns: the design, its frame and its reasons
test now: T0 rules · T2 critique of the frame
test in use: T4 against the control


What the literature says
------------------------

rationale: A designer frames the situation, makes a move and reads what the situation
  says back [Schön 1983]. Problem and solution develop together [Dorst & Cross
  2001]. When only the value sought is known, design reasons to a frame [Dorst
  2011]. Good designers do not start by solving the proposed problem but by
  understanding what the real issues are, as human-centred design is summarised
  [O'Cathain 2019 taxonomy].
context: Open, complex, dynamic and networked problems in organisations, drawn from the
  practice of expert designers [Dorst 2015].
steps: Frame the situation, make a move, and reflect on what the situation says back
  [Schön 1983]. Frame creation runs in nine steps, drawn from the practice of
  expert designers [Dorst 2015].
strengths: It creates a new approach to the problem situation, not only a new solution
  [Dorst 2015]. The frame and its reasons make the design reviewable (ours).
limitations: No study tests the method against another (ours). Promoters and critics of
  design thinking still disagree on its outcomes [Micheli 2019].


Applied to AI
-------------

agent: The agent reads the design requirements and writes its frame first: what the goal
  really asks, and the principle that follows from it.
steps: 1. Write the frame and the principle, and freeze them before any draft. 2. Design
  to the principle. 3. Give the reason each part serves the frame.
returns: The design, its frame, its principle and its reasons.
verify: A reviewer agent that did not write it critiques the frame (T2) and checks the
  design follows it; Verify checks the rules (T0).
risk: A frame written after the draft only explains it away (ours); freezing the frame
  before the draft prevents it (ours).
evidence on AI: No study tests an AI designing by principle yet (ours). As algorithms
  take over creative problem-solving, human design moves toward deciding
  which problems to address [Verganti 2020].
skill: haipipe-design-by-principle (proposed)
