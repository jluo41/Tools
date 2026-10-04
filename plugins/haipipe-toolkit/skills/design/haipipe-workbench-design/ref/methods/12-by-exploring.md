By exploring
============

One design method card. Guide › Method shows it among its method cards; its
papers are the rows of `../design-papers.md` whose `group` is `by exploring`. A
claim names its source in brackets; "(ours)" marks the workbench's own judgment.

family: Goal Only: abduction-2; the design reads only the task, so the how is invented,
  or several hows are sent and the Exp picks
reasoning: several abductions at once, each from a different how; the Exp's data does
  the induction
move: Make several designs that differ in principle, and compare them side by side.
taxonomy: No category of its own; an action in user-centred and digital approaches
  [O'Cathain 2019 taxonomy].
comes from: Sobek 1999, set-based design; Dow 2010, parallel prototyping
reads: design requirements · any insights, internal or external
returns: several designs, each naming what it tries
test now: T0 rules each · T2 to rank
test in use: T4 to choose


What the literature says
------------------------

rationale: Keep several options alive until a test decides between them [Sobek 1999].
  Designing one option after another can fix the designer on it [Dow 2010].
  Divergent thinking first, then convergent, to find the strongest solutions
  [O'Cathain 2019 taxonomy].
context: Web advertisements [Dow 2010]; short stories written with AI ideas [Doshi &
  Hauser 2024]; group idea generation [Girotra 2010]; testing in product
  development [Loch 2001].
steps: Create several prototypes and get feedback on them together, not one after
  another [Dow 2010]. Keep several design options open until tests narrow them
  [Sobek 1999]. Make several rough, cheap prototypes first and narrow them to one
  after feedback, rather than settle on one too soon [O'Cathain 2019 taxonomy].
strengths: Parallel designs beat serial ones on click-through and expert ratings, and
  were more diverse [Dow 2010]. Working alone first, then together, found
  better best ideas [Girotra 2010]. Asking the AI for an output unlike the last
  beat independent generation [Boussioux 2024].
limitations: AI ideas made stories better and more alike [Doshi & Hauser 2024]. Noisy
  tests make parallel testing less attractive [Loch 2001]. Each design tested
  costs, set against the value of the best [Dahan 2001].


Applied to AI
-------------

agent: The agent reads the design requirements and any insights, internal or external,
  and makes several designs at once.
steps: 1. Name the principles to try, each different. 2. Write one design per principle,
  each unlike the last [Boussioux 2024]. 3. Have a reviewer agent rank them (T2).
  4. Send the best few to the Exp (T4).
returns: Several designs, each naming the principle it tries.
verify: Each design passes the rules (T0); critique ranks them (T2); the Exp
  chooses (T4).
risk: AI designs converge [Doshi & Hauser 2024]; designs that differ only in wording
  test nothing (ours).
evidence on AI: Asking the AI for an output unlike the last beat independent generation
  [Boussioux 2024]. AI ideas made each story better and all stories more
  alike [Doshi & Hauser 2024].
skill: haipipe-design-by-exploring (proposed)
