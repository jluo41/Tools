# Can a fresh agent run a stage?
state: 🔴 OPEN
owner: JL
method: hand a clean-context agent one stage and watch what it does, not what it produces

## Question
Can someone with no background read this skill and run one stage correctly, end to end?

This is the acceptance test for the whole design. Everything else on this board is an internal argument; this is the only question whose answer is not ours to decide, because the failure mode is invisible from the inside: we read every contract with the context already in our heads.

## Boundary
- ✅ Covered here
  The acceptance test for the skill, and what counts as passing.
- ↪ Covered elsewhere
  Whether the prose of any one contract is well written is a writing question, not this one.

## Content
### Why the test has to watch the process
The repository's own rule for skill work is that a fresh agent must be watched for HOW it works, not only what it produces: did it trigger the right stage, follow the phases, stop at the gate, and respect the boundaries. A correct-looking artifact produced by ignoring the contract is a failure, because the next paper will not be so lucky.

### What passing should mean here
```
 picks the right stage from a plain request
 runs DRAFT without fetching evidence
 raises questions rather than answering them
 respects probe_depth and defers what it may not spend
 stops at CHECK and asks, rather than writing the gate line itself
 writes the artifact where the contract says, and nowhere else
```
The fifth is the one most likely to fail, because it is the one that requires an agent to stop when it could continue.

### What we know already
One real stand-in gate has happened on the MISQ paper. That is one data point suggesting this test would fail today on the gate line, which is exactly `QB3`'s open item.
`QG4` now defines the page-first runner this acceptance test should exercise.

On 2026-07-25, a clean-context agent followed the revised skill to create a missing Seed Board page, pages it, and stop before DRAFT. That validates the new creator boundary only; it did not exercise the four phases, probe ceiling, or CHECK gate and therefore is not the acceptance test below.

## Items to Finish
- [ ] 🧪 Run the test on one stage
      Clean context, plain request, watch the process. Section-edit on a scratch copy is the obvious candidate, since it is the most complex stage.
- [ ] 📝 Record what it got wrong, before fixing anything
      The findings are the value; fixing first destroys the evidence.
- [ ] 🔁 Re-run after the fixes
      The repository rule is that the loop repeats until a clean-context agent behaves as designed.

## Where we are
The Board-first creator slice has passed a clean-context test. The full-stage acceptance test remains unrun; Section Edit is still the intended hard case.

## Files
- `../../../../CLAUDE.md`
  The repository's fresh-subagent validation rule.
- `stages/5-section-edit/stage.md`
  The hardest stage, and therefore the right one to test.
