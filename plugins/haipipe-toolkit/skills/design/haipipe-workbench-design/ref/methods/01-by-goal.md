By goal
=======

One design method card. Guide › Method shows it among its method cards; its
papers are the rows of `../design-papers.md` whose `group` is `by goal`. A claim
names its source in brackets; "(ours)" marks the workbench's own judgment.

family: Goal Only: abduction-2; the AI invents the how and the design from the
  design requirements alone
reasoning: abduction-2, left unsaid: requirements → a design; its how is never written
  down
move: Write the design straight from the requirements; keep the first that passes the
  rules.
taxonomy: None of the eight approaches develops from the goal alone; every one adds
  people, evidence, theory or testing (ours, reading [O'Cathain 2019 taxonomy]).
comes from: Newell & Simon 1972, generate and test; Simon 1969, satisficing
reads: design requirements
returns: the design
test now: T0 rules
test in use: T4 against the control


What the literature says
------------------------

rationale: A design is found by generating designs and testing each against the goal
  [Newell & Simon 1972]; one that satisfies the goal is good enough, without a
  search for the best [Simon 1969]. A language model can write a design from
  the goal alone (ours).
context: Health awareness messages [Lim 2023], vaccination messages [Karinshak 2023],
  policy appeals [Bai 2025], marketing and political appeals [Matz 2024],
  business ideas [Boussioux 2024].
steps: Generate a design, test it against the goal, and repeat until one passes [Newell
  & Simon 1972]; stop at the first that is good enough [Simon 1969].
strengths: Across 7 studies and 17,422 people, LLM messages persuaded about as well as
  human ones [Hölbling 2025]. LLM health messages ranked higher than the
  most-retweeted human ones on quality and clarity [Lim 2023]. LLM messages
  moved policy attitudes about as much as messages by lay people [Bai 2025].
limitations: Effects vary widely between studies [Hölbling 2025]. People prefer messages
  not labelled as written by AI [Karinshak 2023]. Human crowds produced more
  novel ideas than human-guided AI [Boussioux 2024]. The design carries no
  reason a reviewer can check (ours). An intervention evaluated without
  development risks research waste: costly evaluations of flawed
  interventions [O'Cathain 2019 taxonomy].


Applied to AI
-------------

agent: The Design agent reads only the design requirements: the Design Goal's aim, who
  it is for, their job and its rules. It writes a design. It is the baseline every other
  method must beat (ours).
steps: 1. Read the design requirements. 2. Write one design. 3. Check it against the
  rules (T0). 4. Hand it to Verify, and write again if it fails.
returns: The design only: no frame, no citations.
verify: Verify checks the rules (T0); only the Exp against the control (T4) shows
  whether it works.
risk: Designs written from the same goal come out alike [Doshi & Hauser 2024]. The
  design gives no reason a reviewer can check (ours).
evidence on AI: LLM messages persuade about as well as human ones [Hölbling 2025]. They
  rated higher than the most-retweeted human messages on quality and
  clarity [Lim 2023]. Tailored to a reader from one short prompt, they
  persuaded more [Matz 2024].
skill: haipipe-design-by-goal (proposed)
