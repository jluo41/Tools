Method
======

1 · The six steps
-----------------

| step | what happens | where in the workbench | who |
|---|---|---|---|
| 1 · Set the Design Task | what every design must do and keep: Aim · Requirements · Resources · Leave out | board: Design Tasks · page: Design Task | a person signs the aim and the rules |
| 2 · Pick the method | one method per Design page, from 13 in 3 families: where its rule comes from (section 2) | the board's Design Tasks views, one per family | a person chooses |
| 3 · Generate N designs | each design with its element record: where each part came from, reasoned or intuitive (section 3) | a Generate Run from the Runs panel; page: Design Item | an agent |
| 4 · Evaluate | the rules, the method and the reasons are checked, and readers pretest; a weak design goes back to step 3 or 2: the Revise loop (section 4) | a Verify Run; a card's Evaluation | a different agent |
| 5 · Release | the designs that passed are released; Delivery keeps them word for word | page: Delivery | a person |
| 6 · Run the Exp | a trial in use, against the control (section 4); its data becomes our next insight, which step 2 can read: the Learning loop | outside the workbench; the next Insight board reads the result | the experiment |

One Design page is one design task done by one design method, and it returns N designs. To
compare methods, design the same task on several pages, one page per method.

A board's own knowledge of one channel (for example an SMS board's message theories, in
the `design-theory.md` beside its `board.md`) is a resource of its design tasks.


2 · Step 2 in depth: pick the method
------------------------------------

2.1 · Three families: where the rule comes from
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

```
family              the rule comes from          induction: who learned it       abduction: the design
Goal Only           nowhere: it is invented      nobody yet; the Exp may learn   abduction-2 · create
External Insights   the literature and theory    other people, in their studies  abduction-1 · solve
Internal Insights   our own data                 us, on an Insight board or      abduction-1 · solve
                                                 from readers trying drafts
```

Every family uses all three kinds of reasoning, at different points in the loop:

- **Induction** learns the rule. Where it was learned is what tells the families apart: by
  nobody (Goal Only), by other people (External Insights), or by us (Internal Insights).
- **Abduction** makes the design. With a rule in hand it is abduction-1, problem solving: the
  design only has to find the thing. With no rule it is abduction-2: the rule must be
  invented first.
- **Deduction** checks the design, the same in every family: step 4, Evaluate, judges from
  the design and its rule whether it keeps the rules and should work (section 4).

By theory and insight reads both kinds of rule and sits with Internal Insights; it shows under
External Insights too.

2.2 · Which method when
~~~~~~~~~~~~~~~~~~~~~~~

```
Do we have a rule for this task?
├─ no ─────────────── Goal Only
│                      By goal        the fast baseline: write from the task
│                      By principle   frame what the task really asks, then write
│                      By exploring   send several different designs; the Exp picks
│                      By slots       change one part at a time; the Exp shows which works
├─ from research ──── External Insights
│                      By theory          use a named theory's technique
│                      By implementation  design for how it will really be delivered
└─ from our data ──── Internal Insights
                       By insight             follow a signed insight
                       By precedent           adapt a past design that worked
                       By revising            improve a design after its own Exp
                       By tailoring           one version per group the data shows differs
                       By theory and insight  a theory and our insight that agree
                       By user test           readers try the drafts before sending
                       By co-design           people choose among options (future)
```

2.3 · The thirteen method cards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each method is one card in `methods/`: its family, its reasoning, its move, which inputs
it reads, what it returns, how the design is tested and where the method comes from; then
what the literature says (its rationale, context, steps, strengths and limitations, as
O'Cathain et al. 2019 describe approaches) beside how it applies to AI (the agent, its
steps, what it returns, how a second agent verifies it, its risk, and the evidence on
AI). A card marked `status: future` is a method to add later; no task is designed that
way yet. Guide › Method shows the cards, each with its papers
(`../related/papers.md`, `group` = the method).

| family | method | card |
|---|---|---|
| Goal Only | By goal | methods/01-by-goal.md |
| Goal Only | By principle | methods/02-by-principle.md |
| Goal Only | By exploring | methods/12-by-exploring.md |
| Goal Only | By slots | methods/13-by-slots.md |
| External Insights | By theory | methods/03-by-theory.md |
| External Insights | By implementation | methods/04-by-implementation.md |
| Internal Insights | By insight | methods/05-by-insight.md |
| Internal Insights | By precedent | methods/06-by-precedent.md |
| Internal Insights | By revising | methods/07-by-revising.md |
| Internal Insights | By tailoring | methods/08-by-tailoring.md |
| Internal Insights | By theory and insight | methods/09-by-theory-and-insight.md |
| Internal Insights | By user test | methods/10-by-user-test.md |
| Internal Insights | By co-design | methods/11-by-co-design.md |


3 · Step 3 in depth: what a design records
------------------------------------------

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

The Design Task names the starting text's elements (Resources › Elements), and the Design
Item Space opens with an element matrix: every design read slot by slot against them, ★ where
it changed an element, with a count of how many designs changed each one. So a page shows
at a glance which elements its designs explored and which they never touched.

The methods differ in which sources their elements may draw on. By goal's elements come
from the requirements and from intuition; By theory adds external insights; By insight
adds internal ones; By theory and insight draws on both. So the record lets a comparison
of methods look inside each design: not only which design did better, but where its
elements came from.


4 · Steps 4 and 6 in depth: how a design is checked
---------------------------------------------------

4.1 · The five tests
~~~~~~~~~~~~~~~~~~~~

| test | asks | where | source |
|---|---|---|---|
| T0 Rules | keeps every constraint and acceptance rule | Revise loop: Evaluate · Verify | verification (Boehm 1984) |
| T1 Fidelity | does what its method claims it does | Revise loop: Evaluate · Verify | the technique is present; the cited row says it |
| T2 Critique | an independent expert reads it | Revise loop: Evaluate | Nielsen & Molich 1990 |
| T3 Pretest | users understand it, trust it, would act | Revise loop: Evaluate, a small Exp | Dillard et al. 2007 |
| T4 Exp | a randomized trial against the control | Learning loop: the Exp | validation |

T0 to T3 are Evaluate, in the Revise loop, before anything is sent; T4 is the Exp, in the
Learning loop. A card's `test now` line names which of T0 to T3 it gets, and its `test in
use` line what the Exp compares it with.

Verification asks: was it built right? Only validation asks: was it the right
design? Every method gets T0. A method that claims a reason gets T1 on that reason.
Each method's tests are on its card.

4.2 · What the evidence says about the methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- A named theory alone predicts nothing: in 190 health interventions, theory use
  was not reliably linked to effect, and most did not link their techniques to the
  theory (Prestwich et al. 2013). By theory needs its fidelity test.
- AI ideas make each design better and all designs more alike (Doshi & Hauser
  2024). By exploring has to force its designs apart in principle, not in wording.
- Designs made in parallel beat designs made one after another (Dow et al. 2010).
- AI-written persuasive messages are about as effective as human-written ones
  (Hölbling et al. 2025, 7 studies). By goal is a strong baseline, not a weak one.
- How effective users rate a message correlates with its effect on their attitude
  at about r = .41 (Dillard et al. 2007, 40 studies). T3 is a useful filter, not a
  verdict.
- Tailoring helps, but little: across 57 studies its effect was r = .074 (Noar et
  al. 2007). By tailoring needs a reason each segment differs.
- Revising a tested design pays: in four case studies each iteration improved
  usability by a median 38% (Nielsen 1993). By revising compounds, round by round.

No review compares these methods head to head on one task, so which method gives better
designs is still an open question: does reading more before designing give better designs,
and do our own insights beat the literature? Design one task by several methods, check them
in Evaluate (T0 to T2), and let the Exp (T4) answer.


5 · Why it works
----------------

5.1 · Design makes a situation better
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Herbert Simon (1969): "Everyone designs who devises courses of action aimed at changing
existing situations into preferred ones." In plain words: designing is making a situation
better than it is now (凡是想办法把现状变成更好状态的人，都在做设计).

```
now                           design                    better
few people click the link ──▶  write a new message ──▶  more people click it
```

A design is good enough when it keeps every rule and should work; it is never provably the
best one (Simon calls this satisficing, 满意即可).

5.2 · Four kinds of reasoning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In plain words, every case has three parts:

```
the thing      +   the rule          →   the result
(a message)        (why it works)        (what happens)
```

Each kind of reasoning knows some parts and fills in the blank, like a sum:

```
Deduction     2  ×  3  =  ?        know the thing and the rule, find the result
Induction     2  ?  3  =  6        know the thing and the result, find the rule
Abduction-1   ?  ×  3  =  6        know the rule and the result, find the thing
Abduction-2   ?  ?  ?  =  6        know only the result, find the thing AND the rule
```

The same four with text messages:

```
Deduction     We wrote a message that names the doctor. We know naming the doctor
              gets more clicks. So we expect this message to get more clicks.
Induction     We sent 20 messages and counted the clicks. The ones that named the
              doctor got more. So we learn the rule: naming the doctor gets more clicks.
Abduction-1   We want more clicks. We know naming the doctor helps. So we write a
              message that names the doctor.
Abduction-2   We want more clicks. We know no rule that helps. So we must invent a
              rule ("make it feel like a follow-up to the visit") and then write a
              message that follows it.
```

The same four with a bowl of soup (✓ known, ? what we look for):

```
1. Deduction 演绎推理 · predict
   [thing ✓] + [rule ✓]  ──▶  [result ?]
   I added salt + salt makes things salty  ──▶  so the soup will be salty

2. Induction 归纳推理 · learn a rule
   [thing ✓] + [rule ?]  ──▶  [result ✓]
   5 bowls had salt ...  ──▶  all 5 were salty  →  rule: salt makes soup salty

3. Abduction-1 溯因推理 1 · solve
   [thing ?] + [rule ✓]  ──▶  [result ✓]
   I want salty soup, and I know salt works  →  so I add salt

4. Abduction-2 溯因推理 2 · create
   [thing ?] + [rule ?]  ──▶  [result ✓]
   I want my guests to feel happy, and I know no rule for it
   →  first invent a rule: "hot soup feels warm and caring"  →  then make hot soup
```

The only difference between 3 and 4: in 3 the rule is already known; in 4 it must be
invented first.

So only abduction makes the design. The other two support it, one before and one after:

```
induction            abduction             deduction             the Exp       induction
learn the rule  ──▶  make the design  ──▶  check the design  ──▶  real test ──▶ learn again
(Insight board)      (step 3, Generate)    (step 4, Evaluate)    (step 6)      (next round)
```

Learn, make, check: one loop uses all three, and the Exp's real results start the next round.


Reference
---------

R1 · Terms and people
~~~~~~~~~~~~~~~~~~~~~

| term | 中文 | read more |
|---|---|---|
| Deduction | 演绎推理 | [Wikipedia](https://en.wikipedia.org/wiki/Deductive_reasoning) · [中文维基](https://zh.wikipedia.org/wiki/演绎推理) |
| Induction | 归纳推理 | [Wikipedia](https://en.wikipedia.org/wiki/Inductive_reasoning) · [中文维基](https://zh.wikipedia.org/wiki/归纳推理) |
| Abduction | 溯因推理 | [Wikipedia](https://en.wikipedia.org/wiki/Abductive_reasoning) · [中文维基](https://zh.wikipedia.org/wiki/溯因推理) |

| person | 中文 | what they gave | read more |
|---|---|---|---|
| Charles Sanders Peirce | 查尔斯·桑德斯·皮尔士 | the three kinds of reasoning, abduction among them | [Wikipedia](https://en.wikipedia.org/wiki/Charles_Sanders_Peirce) · [中文维基](https://zh.wikipedia.org/wiki/查尔斯·桑德斯·皮尔士) |
| Herbert A. Simon | 赫伯特·西蒙 (司马贺) | "Everyone designs who devises courses of action aimed at changing existing situations into preferred ones" (1969): designing is making a situation better than it is now, good enough rather than provably best | [Wikipedia](https://en.wikipedia.org/wiki/Herbert_A._Simon) · [中文维基](https://zh.wikipedia.org/wiki/赫伯特·西蒙) |
| Kees Dorst | 基斯·多斯特 * | abduction-1 and abduction-2, for design (2011) | [profile](https://profiles.uts.edu.au/Kees.Dorst) · [the paper](https://doi.org/10.1016/j.destud.2011.07.006) |
| Norbert Roozenburg | 诺伯特·罗森堡 * | two kinds of abduction (1993): explanatory, guess the cause of a fact ("the grass is wet, so it rained"); innovative, invent a thing that would bring a wanted result, which is design | [the paper](https://doi.org/10.1016/S0142-694X(05)80002-X) |

* no standard Chinese name; ours. The Chinese for abduction-1 and abduction-2 (溯因推理 1
and 2) is ours too: Chinese has one word for abduction, and Dorst's split has no
settled translation.

R2 · The reasoning table, compact
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

```
              you know                    you look for                in plain words
Deduction     the thing + the rule        the result                  predict what will happen
Induction     the thing + the result      the rule                    learn a rule from cases
Abduction-1   the result + the rule       the thing                   solve: build to a known rule
Abduction-2   only the result             the thing AND the rule      create: invent the rule, then the thing
```

Dorst 2011, after Peirce: three kinds of reasoning, and abduction in two forms. An
Insight board works on the second row: from what was sent and what happened, it learns
the rule. The third row, abduction-1, solves a problem whose rule is known; picking the
best of a fixed set of options comes closest to it: selection, not design.

Design in the full sense is the last row, abduction-2. Only the result is known; neither the
thing nor the rule that would make it work is. There is no list of options to pick from: the
designer first invents a rule, then makes things from it.

Simon 1969: design changes an existing situation into a preferred one. It
satisfices: good enough within the constraints, never provably best.

R3 · Inputs, process, output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

R6 names these inputs by where they come from: the design
requirements (Aim and Constraints, the Design Task), internal insights (Resources learned
from our own data) and external insights (Resources from the literature and theory).
Each method reads the requirements and some of the insights; the test is the Exp, whose
data becomes the next internal insights.

R4 · The theory behind each step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

R5 · What to attend to, and what not to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Attend to:

- the value: what should change for the person
- the frame: which principle should create that value
- the variables: name them before making drafts
- hard constraints: an option that breaks one is not a design
- spread: options that differ in principle, not in surface
- the prediction (a deduction): write it before the test
- a test that can tell the options apart

Do not:

- choose only among what was tried before
- treat a prediction as knowledge
- polish details past what a test can detect
- split by audience without a reason it differs
- gather knowledge that changes no design
- narrow before the options are explored

These hold for any artifact: a message, a screen, a form, a policy.

R6 · The loop in full
~~~~~~~~~~~~~~~~~~~~~

```
Design requirements ────┐
  the Design Task: what │
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
what it must not break (its rules). They are the Design Task, approved by a person.
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
watches a few readers, a small Exp. The Exp then observes the result in use. Section 4.1
numbers the five tests T0 to T4.

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

R7 · The health-intervention taxonomy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
| Stepped or phased | a systematic set of steps | the shared loop (section 1, R6) |
| Intervention-specific | an approach made for one kind of intervention | a board's design requirements and its channel's knowledge |
| Combination | existing approaches formally combined | By exploring, which may run any of the others |

Five methods have no category of their own: By goal (no approach develops from the goal
alone), By principle (the first activity of human-centred design), By precedent
(adaptation, which the overview places outside the eight), By revising (refinement, which
every approach does; after a formal evaluation it lies outside the overview) and By
tailoring (which efficiency-based approaches find by experiment).

The same overview finds 18 actions in seven domains, which the shared loop follows
(ours): Conception and Planning are the design requirements (the Design Task); Designing
and Creating are the Method step and Generate; Refining is Evaluate, the Revise loop;
Documenting is the Delivery; Planning for future evaluation is the Exp, the Learning loop. To choose an approach it asks six questions: what the
intervention intends, its context, the developers' values, the team's skills and
experience, which approaches have produced effective interventions, and the resources
available. Its authors did not compare the approaches' success, the strengths it lists
are mostly their authors' own, and no criteria exist for judging an approach's quality.
