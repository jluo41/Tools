Theory of Design
================

How to design anything, not only a message: an aim, constraints and resources go
in; there is no list of options to pick from. So the designer frames a principle,
generates options, predicts, checks, chooses and tests. The result is new knowledge.

Guide › Method (the Design family's shared Guide) shows this file as its sections 1 to 9,
then the method cards (`design-methods.md`, sections 10 to 12); the papers are in Guide ›
Related Paper. Both are general. A
board's knowledge of one channel (for example an SMS board's message theories, in the
`design-theory.md` beside its `board.md`) is a resource of its Design Goal, not shown
here.

Sources are named as the drawing lists them and still need checking before they
are cited in a paper.


1 · The design problem: abduction
---------------------------------

```
              you know         you look for
Deduction     what + how       the result         predict
Induction     what + result    the how            explain
Abduction-1   result + how     the what           solve
Abduction-2   the result       the what AND       create
              (the value)      the how            both
```

Dorst 2011, after Peirce: three kinds of reasoning, and abduction in two forms.
Insight works on the second row: from what was sent and what happened, explain how it
worked. The third row, abduction-1, solves a problem whose how is known; picking the
best of a fixed set comes closest to it: selection, not design. Round 1 was run that
way: 1 of 13 written texts.

Design in the full sense is the last row, abduction-2. Only the value is known; neither the artifact nor the
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

Section 6 names these inputs by where they come from: the design
requirements (Aim and Constraints, the Design Goal), internal insights (Resources learned
from our own data) and external insights (Resources from the literature and theory).
Each method reads the requirements and some of the insights; the test is the Exp, whose
data becomes the next internal insights.


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
Resources     Guide › Method · the Design Goal's Resources
1 Frame       a card's Rationale: the rows it acts on (because), their Evidence chain
2 Generate    a Generate Run, from the Runs panel
3 Predict     a card's Evaluation › Expected effect: expected, and wrong if
4 Check       a Verify Run, by a fresh reviewer
5 Choose      page Delivery Space: the designs that passed
6 Test        the send, outside the workbench
Knowledge     the next Insight board reads the result
```


6 · The shared loop: three inputs, Design, Exp
----------------------------------------------

```
Design requirements ────┐
  the Design Goal: what │
  it must do and keep   │
                        │
Internal insights ──────┼──▶ Design ───────────────────────────────────────▶ Exp
  learned from our own  │    Method ─▶ Generate ─▶ Evaluate ─▶ Ready         a trial in use,
  data, and signed      │      ▲          ▲           │        a person      against the
                        │      │          └── rule ───┤        approves      control
External insights ──────┘      └────── weak reason ───┘                       │
  the literature and       Revise loop: back until Evaluate passes            │
  theory, cited                                                               │
                                                                              │
  Learning loop: the Exp's data becomes the next internal insights ◀──────────┘
```

Every design reads the design requirements: what it must do (the aim, and for whom) and
what it must not break (its rules). They are the Design Goal, approved by a person.
Insights supply the how. Internal insights are learned from our own data, past
experiments or the readers' own records, and signed on an InsightBoard. External
insights are other people's data already turned into knowledge: the literature and
theory, each cited. The Exp is the experiment that tests the design in use, against the
control; what it records is new internal data.

The three kinds of reasoning sit in fixed places (Dorst 2011, after Peirce). Induction
makes an insight: from what was sent and what happened, the how. Design is abduction:
from the requirements (the result wanted) and an insight (the how), the design (the
what). With no insight it is abduction-2, which must invent the how as well; with one it
is abduction-1. Evaluate is the evaluation inside Design, before anything is sent: the
rules, a critique and a pretest. The rules and the critique are deduction, judging from
the design and its how whether it keeps the rules and should work; the pretest already
watches a few readers, a small Exp. The Exp then observes the result in use. Section 11
numbers the five tests T0 to T4.


Only the Method step and Generate differ from one method to another: which inputs the
chosen method reads, and what it must return with the design. Every method keeps the
same requirements, the same tests and the same approval. (The Method step is not By
principle's frame: framing is one method's way of reading the requirements.)

One Design page is one design task done by one design method, and it returns N designs.
The task fixes the requirements; the method fixes which insights the page may read and
what each design must return; N is how many designs the Design Goal asks for. So a page
never mixes methods, and comparing methods takes several pages with the same task, one
page per method.



7 · The two loops
-----------------

Two loops run through the format, after the three cycles of design science research
(Hevner 2007): a tight Design Cycle of building and evaluating, inside a Relevance Cycle
that takes requirements from the setting and returns the artifact to field testing.

- The Revise loop (inner) is Method, Generate and Evaluate, repeated until the design
  passes. A broken rule sends it back to Generate, since only the writing is wrong; a
  weak reason (the critique finds it does not hold, or the pretest finds readers would
  not act) sends it back to Method, since the method or its inputs were wrong. It runs
  in minutes, as many times as it needs, and gives back a revised design.
- The Learning loop (outer) starts when a person approves the design at Ready. The Exp
  tests it in use, and its data becomes the next internal insights, which the next
  Design reads. It runs once a round, over weeks, and gives back an insight.

The external insights take Hevner's third cycle, the Rigor Cycle: grounding from the
literature comes in, and what a round learns can go back to it once it is published.


8 · Design elements
-------------------

A design is made of elements, and each is chosen on its own. For a message they are its
sender, its greeting, the news, the ask, the reason, the link and the opt-out. The
choices differ in where they come from and in how they were made, so every Generate can
record them, one entry per element, in an `elements.yaml` beside the design (the run
contract's element record), and the card's Design elements fold shows it:

| field | says | values |
|---|---|---|
| element | the part's role in the design | sender, greeting, news, ask, reason, link, opt-out |
| words | the element as written | the text itself |
| from | the input it rests on | requirements · internal · external · intuition |
| source | the rule, insight row or theory | none for intuition |
| thinking | how it was chosen | reasoned (System 2) · intuitive (System 1) |
| because | the reason, for a reasoned element | one sentence |
| alternatives | the options weighed | when there were any |

Two kinds of thinking choose an element (Evans & Stanovich 2013, who call them Type 1
and Type 2). Intuition is fast and arrives as a sudden idea; reasoning is slow, weighs
options and can be written down as a because. Design uses both. The workbench works
mostly in System 2, so a reasoned element writes its because, and an intuitive one is
recorded as a labeled hunch with no source. A hunch is welcome as an idea and never
counts as warrant: if it works, the Exp's data becomes the internal insight, not the
hunch. Keeping each question, its options and the criteria that chose among them is
design space analysis (MacLean 1991); the record keeps the observable choice, not a
private chain of thought.

The Design Goal names the starting text's elements (Resources › Elements), and the Design
Space opens with an element matrix: every design read slot by slot against them, ★ where
it changed an element, with a count of how many designs changed each one. So a page shows
at a glance which elements its designs explored and which they never touched.

The methods differ in which sources their elements may draw on. By goal's elements come
from the requirements and from intuition; By theory adds external insights; By insight
adds internal ones; By theory and insight draws on both. So the record lets a comparison
of methods look inside each design: not only which design did better, but where its
elements came from.


9 · The six families, and the health-intervention taxonomy
-----------------------------------------------------------

Every method reads the design requirements, so they do not make a family. The six
families differ in where the design's how comes from, and that fixes the reasoning:

| family | reads, besides the requirements | reasoning |
|---|---|---|
| Goal Only | nothing | abduction-2: the how is invented |
| External Insights | the literature and theory | abduction-1, on other people's induction |
| Internal Insights | our signed insights: past experiments, readers' records | our induction, then abduction-1 |
| Both Insights | our signed insights and the literature, as equals | abduction-1 on two hows that must agree |
| Making internal insights now | data gathered while designing | induction in small loops |
| Making internal insights next | nothing more; it sends several options | the Exp does the induction |

A card that reads both kinds of insight as equals sits in Both Insights; one that
leans on one kind sits with that kind. Read across, the first four families are a 2 × 2:
external insights off or on, internal insights off or on. The last two families make
internal insights rather than read them: during Design, from readers
shown the drafts, or after it, from an Exp built to tell options apart.

The health-intervention literature sorts the same ground into eight approaches by the
rationale their authors state (O'Cathain et al. 2019, from approaches published after
2007). Each card names its category on its `taxonomy` line, and every category has a
place here:

| O'Cathain category | what it means | where it is here |
|---|---|---|
| Partnership | the people it is for share every decision | By co-design (future) |
| Target population-centred | based on the views and actions of the people who use it | By user test |
| Evidence and theory-based | published evidence combined with formal theory | By theory (external), By insight (internal), By theory and insight (both) |
| Implementation-based | planned for real-world use if it works | By implementation |
| Efficiency-based | components tested in experiments to keep the active ones | By slots; its tailoring to sub-groups, By tailoring |
| Stepped or phased | a systematic set of steps | the shared loop (section 6) |
| Intervention-specific | an approach made for one kind of intervention | a board's design requirements and its channel's knowledge |
| Combination | existing approaches formally combined | By exploring, which may run any of the others |

Five methods have no category of their own: By goal (no approach develops from the goal
alone), By principle (the first activity of human-centred design), By precedent
(adaptation, which the overview places outside the eight), By revising (refinement, which
every approach does; after a formal evaluation it lies outside the overview) and By
tailoring (which efficiency-based approaches find by experiment).

The same overview finds 18 actions in seven domains, which the shared loop follows
(ours): Conception and Planning are the design requirements (the Design Goal); Designing
and Creating are the Method step and Generate; Refining is Evaluate, the Revise loop;
Documenting is the Delivery; Planning for future evaluation is the Exp, the Learning loop. To choose an approach it asks six questions: what the
intervention intends, its context, the developers' values, the team's skills and
experience, which approaches have produced effective interventions, and the resources
available. Its authors did not compare the approaches' success, the strengths it lists
are mostly their authors' own, and no criteria exist for judging an approach's quality.
