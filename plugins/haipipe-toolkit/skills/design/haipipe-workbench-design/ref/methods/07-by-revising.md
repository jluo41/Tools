By revising
===========

One design method card. The Design workbench shows it in the Theory of Design
Space's Design methods view; its papers are the rows of `../design-papers.md`
whose `group` is `by revising`. A claim names its source in brackets; "(ours)"
marks the workbench's own judgment.

family: With internal insights: induction, then abduction-1; the how comes from our own
  data, as signed insights
reasoning: induction on one design: its result → what to change; then abduction-1 → the
  revised design
move: Take one design already tested, and change what its result says to change.
taxonomy: No category of its own: approaches refine a first version repeatedly on early
  assessments, and refinement after a formal evaluation lies outside the eight
  [O'Cathain 2019 taxonomy].
comes from: Nielsen 1993, iterative design; Kohavi 2009, online controlled experiments;
  Aamodt & Plaza 1994, revise and retain
reads: design requirements · internal insights: one past design and its result
returns: the revised design, the design it revises, and what changed and why
test now: T0 rules · T1 only the named change
test in use: T4 against the design it revises


What the literature says
------------------------

rationale: Refine a design over several versions, each tested with users; the tests
  also show what users need [Nielsen 1993]. A controlled experiment is the best design
  for a causal link between a change and what users do [Kohavi 2009]. A first version
  may be refined repeatedly on early assessments of feasibility and acceptability
  [O'Cathain 2019 taxonomy].
context: User interfaces [Nielsen 1993]; features on the web [Kohavi 2009]; the design
  of integrated circuits [Thomke 1998]; problem solving by cases in AI [Aamodt & Plaza
  1994].
steps: Test a version, find its problems, revise it, and test again, over several
  versions [Nielsen 1993]. Run each change as a controlled experiment and judge it on
  the data, not on the highest-paid person's opinion [Kohavi 2009]. Revise the reused
  solution, then retain what was learned [Aamodt & Plaza 1994].
strengths: In four case studies, usability improved by a median 38% per iteration and
  165% from the first version to the last [Nielsen 1993]. In integrated-circuit design,
  an approach that ran many prototype iterations beat the other by a factor of 2.2 in
  person-months [Thomke 1998]. Teams learned most when they listened to their
  customers' data [Kohavi 2009].
limitations: No study tests it against another method (ours). Several of the guide's
  example experiments had surprising results [Kohavi 2009], so a revision that looks
  better is not yet better (ours). Revising one design climbs to a nearby best and can
  miss a better design elsewhere (ours).


Applied to AI
-------------

agent: The agent reads the design requirements and one design the board has already
  sent, with its result in the Exp and the signed insights about it.
steps: 1. Take one past design and its result. 2. Name what the result says to change,
  and why. 3. Change that, and keep the rest word for word. 4. Name the change and the
  result it should move.
returns: The revised design, the design it revises, its result, and what changed and
  why.
verify: Verify checks that only the named change differs from the design it revises
  (T1) and checks the rules (T0); the Exp runs the revision against that design (T4).
risk: An AI can explain any result after the fact, so a reason read from one result
  needs the next Exp to hold (ours). Small revisions climb to a nearby best (ours).
evidence on AI: No study tests an AI designing by revising yet (ours).
skill: haipipe-design-by-revising (proposed)
