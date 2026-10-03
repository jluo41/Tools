By insight
==========

One design method card. Guide › Method shows it among its method cards; its
papers are the rows of `../design-papers.md` whose `group` is `by insight`. A claim
names its source in brackets; "(ours)" marks the workbench's own judgment.

family: Internal Insights: induction, then abduction-1; the how comes from our own
  data, as signed insights
reasoning: abduction-1 on our own induction: requirements + signed insights, the how → a
  design
move: Make each part of the design follow from a signed insight.
taxonomy: Evidence and theory-based, its evidence half [O'Cathain 2019 taxonomy].
comes from: Sackett 1996, evidence-based practice; MacLean 1991, design space analysis
reads: design requirements · internal insights: signed rows
returns: the design, one cited decision per part
test now: T1 each cited row says it
test in use: T4 against the control


What the literature says
------------------------

rationale: Practice uses the best current evidence, judged with expertise and the
  person's values [Sackett 1996]. A design's rationale can be kept as the
  questions, the options and the criteria that chose among them [MacLean 1991].
context: Clinical practice [Sackett 1996]; the design of interactive systems [MacLean
  1991]. Evidence and theory-based development, which assesses the evidence base,
  including the effectiveness of existing interventions [O'Cathain 2019
  taxonomy].
steps: Use the best current evidence with expertise and the person's values [Sackett
  1996]. Record each design question, its options and the criteria that compare
  them, alongside the design as it is made [MacLean 1991].
strengths: The record helps reasoning about the design and its later redesign and reuse,
  and carries it between designers [MacLean 1991].
limitations: No study tests the method against another (ours). The record has to be
  built alongside the design, which costs effort [MacLean 1991]. An insight
  from past designs may not carry to a new wording (ours).


Applied to AI
-------------

agent: The agent reads the design requirements and the internal insights: the signed DO
  and DO NOT rows of the InsightBoard's Wisdom pages, learned from our own data.
steps: 1. Read the signed rows. 2. For each element of the design, choose the row it
  follows. 3. Write the design. 4. Write each element's because row.
returns: The design and one because row per element; the card shows them as Design
  elements and the Evidence chain.
verify: Verify checks that each cited row says what its element claims (T1) and that no
  DO NOT row is broken.
risk: A cited row that does not support its element; an insight from past designs that
  does not carry to a new wording (ours).
evidence on AI: No study tests an AI designing by insight yet (ours).
skill: haipipe-design-by-insight (proposed)
