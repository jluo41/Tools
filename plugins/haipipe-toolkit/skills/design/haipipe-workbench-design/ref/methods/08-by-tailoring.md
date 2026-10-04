By tailoring
============

One design method card. Guide › Method shows it among its method cards; its
papers are the rows of `../design-papers.md` whose `group` is `by tailoring`. A
claim names its source in brackets; "(ours)" marks the workbench's own judgment.

family: Internal Insights: abduction-1 on our own induction; the how comes from our own
  data: signed insights, past designs, or readers who try the drafts
reasoning: induction on the reader: their data → what fits them; then abduction-1 → a
  design for them
move: Fit the design to who the reader is: one design per segment now, one per reader
  later.
taxonomy: No category of its own; efficiency-based approaches use experiments to find
  tailoring to sub-groups [O'Cathain 2019 taxonomy].
comes from: Hawkins 2008, tailoring's goals and strategies; Noar 2007, the effect of
  tailoring; Nahum-Shani 2018, just-in-time adaptive interventions
reads: design requirements · internal insights: who the reader is
returns: a design per segment, the rule that assigns them, and the data each rests on
test now: T0 rules · T1 each design uses its segment's insight
test in use: T4 the tailoring rule against one design for all


What the literature says
------------------------

rationale: Individualizing a communication for its receiver is expected to raise its
  effect [Hawkins 2008]. An intervention can adapt to a person's changing state, giving
  the right support at the right time [Nahum-Shani 2018].
context: Health communication [Hawkins 2008]; tailored print health behaviour change
  interventions [Noar 2007]; mobile health [Nahum-Shani 2018]; messages tailored by a
  language model to a reader's psychological profile [Matz 2024].
steps: Choose the goal (help the message be processed, or move the behaviour's
  determinants), then the strategy: personalization, feedback or content matching
  [Hawkins 2008]. For an adaptive intervention, name the decision points, the tailoring
  variables, the options and the decision rules that join them [Nahum-Shani 2018].
strengths: Across 57 studies (N = 58,454), tailoring had a positive effect on behaviour
  change, r = .074 [Noar 2007]. Messages a language model tailored to a reader's profile
  were more persuasive than untailored ones [Matz 2024].
limitations: The effect is small, and depends on the comparison, the behaviour, the
  population and what is tailored on [Noar 2007]. Results are generally positive but not
  consistently so [Hawkins 2008]. Many adaptive interventions were built with little use
  of evidence or theory [Nahum-Shani 2018].


Applied to AI
-------------

agent: The agent reads the design requirements and the signed insights for each segment
  of readers. Tailoring to one reader would read that reader's own records, and is a
  later step (ours).
steps: 1. Name the segments the signed insights tell apart, and why they differ. 2.
  Write one design per segment from its insight. 3. Name the reader data each design
  rests on. 4. Write the rule that sends each segment its design.
returns: A design per segment, the rule that assigns them, and the data each rests on.
verify: Verify checks that each design uses its segment's insight (T1) and the rules
  (T0); the Exp tests the rule against one design for all (T4).
risk: Readers' records are protected health information: use only what the design
  needs, under the consent it was given for (ours). A segment with no reason it differs
  splits the readers for nothing (ours).
evidence on AI: Messages a language model tailored to a reader from one short prompt
  were more persuasive [Matz 2024]. No study tests an AI tailoring health messages from
  readers' records yet (ours).
skill: haipipe-design-by-tailoring (proposed)
