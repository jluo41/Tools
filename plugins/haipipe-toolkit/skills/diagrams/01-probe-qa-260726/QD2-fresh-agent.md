# Can a fresh agent run one probe?

state: 🔴 OPEN
owner: JL
method: hand a clean-context agent one Q-consumer and watch what it does, not what it produces

## Question
Can someone with no background read this skill and run one probe without breaking either law?
Unknown, because it has never been tried, and everything else here is an internal argument until it is.
The test watches HOW the agent works rather than what it produces, since a correct-looking file made by ignoring the contract is a failure.

The failure mode is invisible from inside, because we read every rule with the reasons already in our heads.
A correct-looking probe file produced by ignoring the contract is a failure, not a pass, so the test watches HOW the agent worked rather than only what it wrote.
The repo already makes this the gate for skill work: `CLAUDE.md` requires a fresh-agent validation before any skill change counts as done, so an untested skill is an unfinished one however good it looks to its author.

## Boundary
- ✅ Covered here
  The acceptance test for the layer, and what counts as passing.
- ↪ Covered elsewhere
  Whether any single page's prose is well written is a writing question, not this one.

## Diagram
```
   what PASSING should mean, watched rather than inferred
   ─────────────────────────────────────────────────────
   turns a Q-consumer into a q-executor with the stake gone
   greps the bank BEFORE dispatching anything             ← ② precedes ③
   reads a candidate QA file instead of matching its topic
   dispatches the q-executor VERBATIM, and nothing else
   stops at the human APPROVE gate rather than continuing
   opens the target file rather than listing it
   writes no bank file of its own, however helpful        ← LAW 1
   declares a deferral instead of leaving a bare `planned`

   the seventh is the one most likely to fail, because it is the one
   where doing the wrong thing looks like being useful.
```

## Items to Finish
- [ ] 🧪 One fresh agent runs one probe, end to end, and is watched
      Clean context, `SKILL.md` only, one real Q-consumer, no coaching.
      The record is what it DID at each of the eight lines above, not whether the file looked right.
- [ ] 📋 The run is written up on this page, verbatim where it matters
      Including whatever it did that the contract did not anticipate, which is the part worth having.
- [ ] 🧠 JL rules what a failure means
      Whether a failed run blocks the version, reopens a page, or is recorded and moved past.

## Where we are
Not started. This is the board's close condition and the only page here whose answer is not ours to decide.

## Files
- `SKILL.md`
  The whole of what the agent would be given.
