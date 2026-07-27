# The creator/reviewer pair, and why it is not one agent
state: 🟡 PARTIAL
owner: JL
method: two agents, one produces and one judges, and the reviewer starts from a context it did not build

## Question
Why is every phase run by two agents rather than one careful one? Three phases of four use the same shape: a creator produces the artifact, a reviewer evaluates it, and the loop repeats on a revise verdict. That doubles the work, so the separation has to buy something a single more-careful agent could not.

It buys independence of context, and that is the whole of it. The defect the family cares about is the intent-versus-implementation mismatch, where code runs and measures the wrong thing. An author cannot reliably catch that in their own work because the misunderstanding that produced the code also produces the reading of it. A reviewer starting from a clean context has no such attachment, and that is a structural property, not a matter of being more diligent.

What is unresolved is the loop's ending. The verdicts are pass, warn, revise and fail; the documented rule is that a first warn feeds back for one retry and a second warn advances. That "advance on a repeated warn" is a decision to ship a known concern, and nothing records that it happened.

## Boundary
- ✅ Covered here
  Why the pair exists, what independence buys, the verdict ladder, and what the loop's ending costs.
- ↪ Covered elsewhere
  What each gate uniquely catches is `QB3` and `QB5`; the phase with no pair at all is `QB4`; the acceptance test for the whole package is `QE1`.

## Diagram
```
   THE TRIAD                                     task/agents/

   orchestrator-agent      the dispatch target; coordinates the pair
        │
        ├──▶ creator-agent    produces: plan · code · report
        └──▶ reviewer-agent   evaluates: IPO compliance · bugs · accuracy

   THE LOOP                              ref/task-lifecycle.workflow.js

    1  creator produces the stage's artifact
    2  reviewer evaluates ──▶ pass · warn · revise · fail
    3  first warn   ──▶ back to the creator, ONE retry
    4  second warn, or pass ──▶ advance
    5  fail ──▶ stop, a human decides

   ── the invariant ──────────────────────────────────
      the creator never reviews its own work.
      the reviewer never produces an artifact.
      break either and the pair becomes one agent with extra steps.

   ── what the separation actually buys ──────────────────
      NOT more care. A single agent can be told to be careful.
      INDEPENDENCE OF CONTEXT: the reviewer starts clean, so the
      misunderstanding that produced the code is not also doing
      the reading. That is structural and cannot be instructed.

   ── the ending nobody records ──────────────────────────
      step 4: a SECOND warn advances.
      that is a decision to ship a known concern, and it leaves
      no more trace than a clean pass did.            → Items
```

## Content
### Independence is structural, and it is the only thing being bought
It is worth being precise, because "use a reviewer" sounds like a quality practice and this is
narrower. A single agent told to review its own output re-reads with the same model of what the
code was for. If that model is what was wrong, re-reading confirms it. The second agent is not
better; it is uncontaminated, and only the second property survives being asked to try harder.

### The verdict ladder has four rungs and only three are used
`pass`, `warn`, `revise`, `fail`. `revise` loops, `fail` stops for a human, `pass` advances. The
interesting rung is `warn`, because it is the only one whose meaning depends on how many times it
has been seen: once it loops, twice it advances.

That is a reasonable way to bound a loop and it hides a decision. An artifact that advanced on a
repeated warn carries a known, named concern into the next phase, and downstream nothing can
distinguish it from an artifact that passed cleanly.

### One agent is missing from the pattern
EXECUTE has no pair, for the reasons on `QB4`. Worth stating here so the pattern's absence reads
as deliberate rather than as an oversight: three phases have a pair, one has a human.

## Items to Finish
- [x] 👥 The pair is implemented and the invariant is stated
      Creator produces, reviewer evaluates, neither does the other's job. The three agent contracts are in `task/agents/`.
- [ ] 📝 Record a warn that was advanced past
      A second warn is a decision to ship a known concern. It should appear in the artifact it advanced, so a later reader can weigh it. Today it appears nowhere.
- [ ] 🎯 Give each reviewer its phase's defect class
      `QB3` catches intent versus implementation; `QB5` catches promise versus production. The reviewer agent's own contract names neither, so it is one generic reviewer wearing three hats.
- [ ] 🔁 Rule what a second `revise` means
      The ladder bounds `warn` at two and says nothing about repeated `revise`. An infinite loop is prevented by the workflow's own limits rather than by a stated rule.

## Where we are
Implemented and in use: three agents in `task/agents/`, driven by
`ref/task-lifecycle.workflow.js`, with the creator/reviewer invariant stated in `SKILL.md`.

The two open items are both about what the loop leaves behind rather than how it runs. A warn that
was advanced past, and a reviewer that knows which defect class it owns, are the difference between
a gate and a formality.

- 260726 CC · 🧠 Stated independence as structural
      `SKILL.md` says the reviewer's independence comes from fresh-agent reasoning. Written here as the thing being bought, because a team under time pressure will otherwise collapse the pair into one careful agent and lose exactly the property that made it work.

## Files
- `agents/haipipe-task-orchestrator-agent.md`
  The dispatch target that coordinates the pair.
- `agents/haipipe-task-creator-agent.md`
  Produces plan, code, report, and the QA digest when one is due.
- `agents/haipipe-task-reviewer-agent.md`
  Evaluates all four stages; does not yet name a per-phase defect class.
- `task-lifecycle.workflow.js`
  The loop: the verdict ladder and the retry rule.

## Log
260726 · Created with the board.
