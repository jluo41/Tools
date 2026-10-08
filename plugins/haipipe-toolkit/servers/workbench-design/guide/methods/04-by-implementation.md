By implementation
=================

One design method card. Guide › Method shows it among its method cards; its
papers are the rows of `../../related/papers.md` whose `group` is `by implementation`. A
claim names its source in brackets; "(ours)" marks the workbench's own judgment.

family: External Insights: abduction-1; the how comes from the literature and theory,
  other people's data
reasoning: abduction-1: requirements + what is known about delivery → a design and its
  plan for use
move: Design for real-world use from the start: who it reaches, who adopts and delivers
  it, and whether its effect lasts.
taxonomy: Implementation-based: developed with attention to its use in the real world if
  it works [O'Cathain 2019 taxonomy].
comes from: Glasgow 1999, RE-AIM: reach, efficacy, adoption, implementation, maintenance
reads: design requirements: the delivery setting · external insights: RE-AIM
returns: the design, and how it will reach people, be adopted, be delivered and last
test now: T0 rules, the delivery limits among them · T2 critique of the plan
test in use: T4 on reach as well as effect, against the control


What the literature says
------------------------

rationale: Planners should attend to external validity, so that effective interventions
  are adopted, implemented and sustained in real-world settings [O'Cathain 2019
  taxonomy]. Judging a program on fewer than all five RE-AIM dimensions wastes resources
  and leaves its public health impact short of what it could be [Glasgow 1999].
context: Health behaviour interventions [O'Cathain 2019 taxonomy]; public health and
  community-based programs [Glasgow 1999].
steps: The RE-AIM planning tool asks questions in five groups: 1. Reach to the target
  population. 2. Effectiveness. 3. Adoption by staff, settings or institutions. 4.
  Implementation. 5. Maintenance of effects over time [O'Cathain 2019 taxonomy]. Cost
  and delivery are weighed early, to cut the risk of failing in use [O'Cathain 2019
  taxonomy].
strengths: It has been used to evaluate and report a wide range of interventions, and it
  complements other approaches [O'Cathain 2019 taxonomy]. Its dimensions act at several
  levels, from the person to the organisation and the community [Glasgow 1999].
limitations: It began as a framework for reporting and evaluating, so it says little about
  how to develop an intervention [O'Cathain 2019 taxonomy]. No study tests it against
  another method (ours).


Applied to AI
-------------

agent: The agent reads the design requirements, the delivery setting among them: who
  receives the design, who delivers it, what each delivery costs, and the limits of the
  channel.
steps: 1. Name who the design must reach, and who it would miss. 2. Name who must adopt
  and deliver it, and what would stop them. 3. Write the design within those limits. 4.
  Say how its effect would last over time.
returns: The design, and its plan for reach, adoption, delivery and maintenance.
verify: Verify checks the delivery limits as rules (T0) and a reviewer agent critiques the
  plan (T2); the Exp measures reach as well as effect (T4).
risk: An agent can state a plan it cannot know to be true: reach and adoption are measured
  in use, not reasoned (ours).
evidence on AI: No study tests an AI designing for implementation yet (ours).
skill: haipipe-design-by-implementation (proposed)
