# When the human can let go
state: ⏸️ ON HOLD
owner: JL
method: two signals, the guideline matching JL's judgment and the guideline no longer changing

## Question
How far does the iteration have to go before we can stop and let the loop run on its own?

JL put it as two signals: whether the guideline matches the author's (JL's) judgment, and whether the guideline is stable and no longer changing.
The difficulty is that neither signal is written as something a system can test, so today "it looks good enough" is a feeling one person has rather than a condition the loop can check.
Without a stopping rule this method has no end point and keeps spinning: every new version invites another review round, and nobody can say which round was the last one that mattered.
It also sits downstream of the other faces, because what the gate reads (the agreement numbers, the objective score) is produced elsewhere, and QC3's construct standard is one of the conditions feeding it.

## Boundary
- ✅ Covered here
  The convergence gate itself: what has to be true before a human stops reviewing every batch.
- ↪ Covered elsewhere
  How each version is examined round by round is QB2, and the standard that scores a construct is QC3, which feeds one of this gate's conditions.
  What happens after the guideline is final, labeling the remaining thousands, is QC2.

## Diagram
```
  Stopping is judged on two signals (both must hold to call it converged):
     Signal 1  the guideline matches the author's (JL's) judgment
               ⚠️ how does this become an action a system can judge? not decided
     Signal 2  the guideline is stable, it no longer changes
               ⚠️ "unchanged for several rounds in a row" means how many rounds? not decided
  ──► the system judges and records it automatically: N rounds with no change + JL's sign-off
```

## Items to Finish
- [ ] 🔢 Fix the number behind "the guideline stops changing"
      This is met when one number is written down: how many consecutive rounds with no change to the guideline count as stable.
      JL named stability as one of the two stopping signals, but the meeting never fixed the number, so "no longer changing" stays a judgement someone makes on the spot instead of a test the loop can run.
      ZD's F8 note also warns that stability is not correctness, so whichever number is chosen sits beside the other conditions rather than replacing them.
- [ ] ✍️ Turn "matches the author's judgment" into an action a system can judge
      This is met when JL's approval is expressed as something the loop can record and check, rather than a reaction to a batch.
      The first signal is the author's own judgment, which is exactly the part the meeting did not answer: the diagram carries it as JL's sign-off, but what is signed, on what, and at which point is still open.
      Until that is decided the signal cannot be reported by the system at all, so it can only be asserted by whoever was in the room.
- [ ] 🤖 Have the system judge and record both signals
      This is met when the loop can report on its own that the guideline went N rounds with no change and that JL signed off.
      Neither signal is implemented today, so nothing in the loop can say whether it is finished, and the only thing being watched is a single agreement number.
      This item cannot move before the two above it are decided, because there is nothing yet to implement.

## Where we are
Today the loop looks at one agreement number, and it is the 0.93 from QB2 that does not count.
Neither of the two stopping signals has been built.
The meeting did not finish either question: how many rounds "unchanged for several rounds in a row" means, and how "matches the author's judgment" becomes an action a system can judge.
Both are JL's calls, so this face is parked until they are made.

## Files
- `lib/converge.py`
  The convergence gate is implemented here, so a decision on this face lands in this file.
- `ref/ref-config.md`
  Holds the `convergence:` thresholds, which is where a decided number of rounds would be written down.
- `_source/note-update-v3-260721.md`
  ZD's note, whose F8 entry is the comment pinned on this face.

## Comments
- [ ] ZD 「how many consecutive rounds with no change to the guideline count as stable」 · 260721 1400
      note-update-v3 F8: stability is not correctness, and a guideline that stops changing is not thereby a right one.
      Besides stability, the convergence gate needs a small enough held-out gap plus an objective score (downstream or discriminance, see QC3).
      All three have to hold before it counts as converged.

## Log
260725 · rewritten to the current face format in English
260723 1600 · migrated from the old `[Q6]`; the two questions the meeting left unanswered were split into the checklist
