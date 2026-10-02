Design methods
==============

One design task can be designed in many ways. Every method is generate and test
(Newell & Simon 1972; Simon 1969): its inputs go in, a design comes out, a test judges
it. Methods differ in which inputs they read before designing and in what they must
return with the design. This holds for any artifact: a message, a screen, a form, a
policy.

The board level Theory of Design Space renders this file as its Design methods view.
The papers named here are listed, with their journals, in its Papers view.


1 · Three inputs, Design, Exp
-----------------------------

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
watches a few readers, a small Exp. The Exp then observes the result in use. Section 4
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

Only the Method step and Generate differ from one method to another: which inputs the
chosen method reads, and what it must return with the design. Every method keeps the
same requirements, the same tests and the same approval. (The Method step is not By
principle's frame: framing is one method's way of reading the requirements.)

One Design page is one design task done by one design method, and it returns N designs.
The task fixes the requirements; the method fixes which insights the page may read and
what each design must return; N is how many designs the Design Goal asks for. So a page
never mixes methods, and comparing methods takes several pages with the same task, one
page per method.


2 · Design elements
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


3 · Thirteen methods
--------------------

Each method is one card in `methods/`: its family, its reasoning, its move, which inputs
it reads, what it returns, how the design is tested and where the method comes from; then
what the literature says (its rationale, context, steps, strengths and limitations, as
O'Cathain et al. 2019 describe approaches) beside how it applies to AI (the agent, its
steps, what it returns, how a second agent verifies it, its risk, and the evidence on
AI). A card marked `status: future` is a method to add later; no task is designed that
way yet. The Design methods view shows the cards, each with its papers
(`design-papers.md`, `group` = the method).

Every method reads the design requirements, so they do not make a family. The six
families differ in where the design's how comes from, and that fixes the reasoning:

| family | reads, besides the requirements | reasoning |
|---|---|---|
| Requirements only | nothing | abduction-2: the how is invented |
| With external insights | the literature and theory | abduction-1, on other people's induction |
| With internal insights | our signed insights: past experiments, readers' records | our induction, then abduction-1 |
| With both insights | our signed insights and the literature, as equals | abduction-1 on two hows that must agree |
| Making internal insights now | data gathered while designing | induction in small loops |
| Making internal insights next | nothing more; it sends several options | the Exp does the induction |

A card that reads both kinds of insight as equals sits in With both insights; one that
leans on one kind sits with that kind. Read across, the first four families are a 2 × 2:
external insights off or on, internal insights off or on. The last two families make
internal insights rather than read them: during Design, from readers
shown the drafts, or after it, from an Exp built to tell options apart.

| family | method | card |
|---|---|---|
| Requirements only | By goal | methods/01-by-goal.md |
| Requirements only | By principle | methods/02-by-principle.md |
| With external insights | By theory | methods/03-by-theory.md |
| With external insights | By implementation | methods/04-by-implementation.md |
| With internal insights | By insight | methods/05-by-insight.md |
| With internal insights | By precedent | methods/06-by-precedent.md |
| With internal insights | By revising | methods/07-by-revising.md |
| With internal insights | By tailoring | methods/08-by-tailoring.md |
| With both insights | By theory and insight | methods/09-by-theory-and-insight.md |
| Making internal insights now | By user test | methods/10-by-user-test.md |
| Making internal insights now | By co-design | methods/11-by-co-design.md |
| Making internal insights next | By exploring | methods/12-by-exploring.md |
| Making internal insights next | By slots | methods/13-by-slots.md |

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
| Stepped or phased | a systematic set of steps | the shared loop (section 1) |
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


4 · How a design is evaluated
-----------------------------

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


5 · What the evidence says about the methods
--------------------------------------------

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

No review compares these methods head to head on one task. The method is itself a
bet: does reading more inputs before designing give better designs, and do internal
insights beat external ones? Design one task by several methods and compare them in the
Revise loop (T0 to T2) and in the Exp (T4).
