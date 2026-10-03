The method cards
================

Guide › Method shows this file after `design-theory.md`, as its sections 10 to 12: one
card per method, how a design is evaluated, and what the evidence says. Every method is
generate and test (Newell & Simon 1972; Simon 1969): its inputs go in, a design comes
out, a test judges it. Methods differ in which inputs they read before designing and in
what they must return with the design. The papers named here are listed, with their
journals, in Guide › Related Paper.


10 · Thirteen methods
---------------------

Each method is one card in `methods/`: its family, its reasoning, its move, which inputs
it reads, what it returns, how the design is tested and where the method comes from; then
what the literature says (its rationale, context, steps, strengths and limitations, as
O'Cathain et al. 2019 describe approaches) beside how it applies to AI (the agent, its
steps, what it returns, how a second agent verifies it, its risk, and the evidence on
AI). A card marked `status: future` is a method to add later; no task is designed that
way yet. Guide › Method shows the cards, each with its papers
(`design-papers.md`, `group` = the method).

The cards fall into six families by where the design's how comes from: Goal Only,
External Insights, Internal Insights, Both Insights, Making internal insights now and
Making internal insights next.

| family | method | card |
|---|---|---|
| Goal Only | By goal | methods/01-by-goal.md |
| Goal Only | By principle | methods/02-by-principle.md |
| External Insights | By theory | methods/03-by-theory.md |
| External Insights | By implementation | methods/04-by-implementation.md |
| Internal Insights | By insight | methods/05-by-insight.md |
| Internal Insights | By precedent | methods/06-by-precedent.md |
| Internal Insights | By revising | methods/07-by-revising.md |
| Internal Insights | By tailoring | methods/08-by-tailoring.md |
| Both Insights | By theory and insight | methods/09-by-theory-and-insight.md |
| Making internal insights now | By user test | methods/10-by-user-test.md |
| Making internal insights now | By co-design | methods/11-by-co-design.md |
| Making internal insights next | By exploring | methods/12-by-exploring.md |
| Making internal insights next | By slots | methods/13-by-slots.md |


11 · How a design is evaluated
------------------------------

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


12 · What the evidence says about the methods
---------------------------------------------

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
