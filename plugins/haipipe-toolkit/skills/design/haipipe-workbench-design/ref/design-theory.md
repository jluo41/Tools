Theory of Design
================

How to design anything, not only a message: an aim, constraints and resources go
in; there is no list of options to pick from. So the designer frames a principle,
generates options, predicts, checks, chooses and tests. The result is new knowledge.

The board level Theory of Design Space renders this file. A board may add its own
domain knowledge (for example message theories) in `design-theory.md` beside its
`board.md`; that file is shown below this one, in the same format.

Sources are named as the drawing lists them and still need checking before they
are cited in a paper.


1 · The design problem: abduction
---------------------------------

```
              you know         you look for
Deduction     what + how       the result         predict
Induction     what + result    the how            explain
Abduction     result + how     the what           choose
Design        the result       the what AND       create
              (the value)      the how            both
```

Dorst 2011, after Peirce. Insight works on the second row: from what was sent and
what happened, explain how it worked. Picking the best of a fixed set is the third
row: selection, not design. Round 1 was run that way: 1 of 13 written texts.

Design is the last row. Only the value is known; neither the artifact nor the
principle that would make it work is. There is no option set to search: the
designer frames a principle, then makes options from it.

Simon 1969: design changes an existing situation into a preferred one. It
satisfices: good enough within the constraints, never provably best.


2 · Inputs, process, output
---------------------------

```
INPUT
Aim          the value wanted, for whom
Constraints  what every design must keep
Resources    knowledge, data, theory, past designs,
             budget (arms, time, people)

PROCESS
1 Frame      name the principle that should create the value
2 Generate   new options from that principle, one variable each
3 Predict    the expected effect, before any test (expected / wrong if)
4 Check      constraints and quality, judged by a fresh reviewer
5 Choose     a set that spans the variables
6 Test       cheap, built to tell the options apart

OUTPUT
Artifact     the design itself
Rationale    frame, theory, rule
Bet          what should happen, and when it is wrong
Test plan    what the test will decide
Knowledge    the result, back into Resources
```

Check judges quality: does it keep the constraints? Only the test judges value:
did it create what we aimed at?


3 · The theory behind each step
-------------------------------

```
step       theory                                   what it tells you
Frame      Schön 1983, reflection-in-action         frame, make a move, read what the result says back
           Dorst & Cross 2001, co-evolution         problem and solution change together
Generate   Hatchuel & Weil 2003, C-K theory         designing grows both concepts and knowledge
           Zwicky 1969, morphological analysis      split into variables, combine the options of each
Structure  Suh 1990, axiomatic design               one parameter per requirement: change one variable at a time
Predict    Gero 1990, function-behaviour-structure  compare the behaviour you expect with what the structure will do
Choose     Simon 1969, satisficing                  good enough within constraints
           Sobek, Ward & Liker 1999, set-based      keep several options alive until a test decides
Process    Design Council 2005, Double Diamond      widen, then narrow, twice: the problem, then the solution
           Rittel & Webber 1973, wicked problems    no final formulation; every release is itself a test
```

In C-K terms: Knowledge is K, Design is C. A design is a concept K cannot yet
decide; the test decides it, and its answer is new K.


4 · What to attend to, and what not to
--------------------------------------

Attend to:

- the value: what should change for the person
- the frame: which principle should create that value
- the variables: name them before making drafts
- hard constraints: an option that breaks one is not a design
- spread: options that differ in principle, not in surface
- the bet: write the prediction before the test
- a test that can tell the options apart

Do not:

- choose only among what was tried before
- treat a prediction as knowledge
- polish details past what a test can detect
- split by audience without a reason it differs
- gather knowledge that changes no design
- narrow before the options are explored

These hold for any artifact: a message, a screen, a form, a policy.


5 · How the Design Workbench follows the theory
-----------------------------------------------

```
theory        workbench
Aim           board: Design Tasks Space · page: Design Goal Space
Constraints   the design task's "every design keeps" rules
Resources     Theory of Design Space · each card's Supporting work
1 Frame       a card's Rationale: the rule it follows (because)
2 Generate    a Generate Run, from the Runs panel
3 Predict     a card's Expectation: expected, and wrong if
4 Check       a Verify Run, by a fresh reviewer
5 Choose      page Delivery Space: the designs that passed
6 Test        the send, outside the workbench
Knowledge     the next Insight board reads the result
```
