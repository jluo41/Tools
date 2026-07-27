# Can a fresh agent run a stage?
state: 🔴 OPEN
owner: JL
method: hand a clean-context agent one stage and watch what it does, not what it produces

## Question
Can someone with no background read this skill and run one stage correctly, end to end? This is the acceptance test for everything else on this board. It has never been passed, and until it is, every other page here is a design rather than a result.

This is the acceptance test for the whole design. Everything else on this board is an internal argument; this is the only question whose answer is not ours to decide, because the failure mode is invisible from the inside: we read every contract with the context already in our heads.


The approach is to watch the process rather than grade the output: did it find the right entry, follow the intended path, stop at the right gate. What we want is the one thing no amount of design discussion can give us, which is evidence that the whole thing works for someone who was not in the room when it was decided.
```
   ── THREE LEVELS, not two.  only the third needs a stranger ─────

   ① MECHANICAL          facts about files      the author MAY run
        every path resolves · every contract parses · checker exits 0

   ①ʹ END-TO-END         the skill's own        the author MAY run
        procedure, walked against a REAL subject, as written

   ② BEHAVIOURAL         what a stranger DOES   the author may NOT
        does it trigger · follow the workflow · stop at the gates

   ── why ①ʹ deserves its own name ────────────────────────────────
      260726: the venue pin was ruled into a `venue:` frontmatter key
      that haipipe-board's parser cannot read. It was specified in 12
      places. EVERY mechanical check passed: paths resolved, all 8
      contracts parsed, the checker exited clean. Both documents were
      internally consistent and the pair was wrong.

      It surfaced within hours, by walking enter's own frontier
      predicates against the MISQ paper. That is ①ʹ, it costs minutes,
      it is not contaminated because it produces facts, and it caught
      what ① structurally cannot.

   ── run on 2026-07-26 ───────────────────────────────────────────
      ①   ✅  8 contracts form ok · conform exit 1, 56 findings
      ①ʹ  ✅  once, unplanned, and it found the day's worst defect
      ②   ⬜  never. 20 skills rewritten, the door untested.

      the acceptance question is already sharp, because a ruling made
      it sharp: given /haipipe-paper enter <path>, a fresh agent must
      end up LOOKING at a board without ever hearing the word
      `haipipe-board`. If it types the second skill, the single-door
      ruling is not implemented, whatever the files say.
```
## Boundary
- ✅ Covered here
  The acceptance test for the skill, and what counts as passing.
- ↪ Covered elsewhere
  Whether the prose of any one contract is well written is a writing question, not this one.

## Diagram
```
 THE ONLY QUESTION ON THIS BOARD WHOSE ANSWER IS NOT OURS

   every other face   an internal argument we can settle
   this one           the failure mode is INVISIBLE FROM THE INSIDE,
                      because we read every contract with the context
                      already in our heads

 THE TEST WATCHES THE PROCESS, NOT THE ARTIFACT
   a correct-LOOKING artifact produced by ignoring the contract
   is a FAILURE. The next paper will not be so lucky.

 WHAT PASSING MEANS
   ① picks the right stage from a plain request
   ② runs DRAFT without fetching evidence
   ⑦ raises questions rather than answering them
   ⑧ respects probe_depth, defers what it may not spend
   ③ stops at CHECK and ASKS, rather than writing the gate line   ◄ ⚠️
   ④ writes the artifact where the contract says, and nowhere else

   ③ is the one most likely to fail, because it is the only one that
   requires an agent to STOP when it could continue.

 THE EVIDENCE WE ALREADY HAVE
   260725  a clean-context agent created a missing Seed page, paged it,
           and stopped before DRAFT.
           ✅ validates the CREATOR boundary (QA8)
           ✗ did not exercise the four phases, the probe ceiling,
             or the CHECK gate.  NOT the acceptance test.
   MISQ    one real stand-in gate has already happened: an agent wrote
           the line saying a gate passed.                       ⚠️
           one data point saying this test would FAIL TODAY on ③,
           which is exactly QB3d's open item.
```

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
One real stand-in gate has happened on the MISQ paper. That is one data point suggesting this test would fail today on the gate line, which is exactly `QB3d`'s open item.
`QA9` now defines the page-first runner this acceptance test should exercise.

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
