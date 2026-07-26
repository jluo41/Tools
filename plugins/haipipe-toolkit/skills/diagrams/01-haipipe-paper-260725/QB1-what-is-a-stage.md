# What is a stage?
state: 🟡 PARTIAL
owner: JL
method: keep the one-question rule; decide whether it is enforced or merely stated

## Question
What makes something a lifecycle stage rather than a task, a phase, or a folder? The working answer is one question, one artifact, one gate. What the rule is worth depends entirely on whether it is strong enough to refuse a ninth stage.

The working answer is: a stage answers exactly ONE question, produces ONE artifact, and closes at ONE human gate. That rule is what stops the lifecycle turning into a folder of chores, and it is already doing real work: it is why "compile the manuscript" is not a stage of section-edit, and why the eight stages have the shapes they do. What is unsettled is whether anything enforces it.


The way to settle it is to state the test, one question and one artifact and one gate, and then hold the eight existing stages against it rather than reasoning in the abstract. What we want is a rule strong enough to say no to a ninth stage, because a definition that admits everything is not doing any work.
## Boundary
- ✅ Covered here
  The definition of a stage, and the one-question rule.
- ↪ Covered elsewhere
  The four phases inside a stage are `QB2`; the gate is `QB3`; whether a stage may run per-unit is `QB4`.

## Diagram
```
 THE 1:1:1 RULE                     what makes a folder a STAGE

   ONE question   ──►  ONE artifact  ──►  ONE human gate
   "why might this      the seed page      CHECK: JL says yes
    paper exist?"

 THE EIGHT, AS THEY STAND
   0-seed          why might this paper exist?              venue-FREE
   1a-resource     does the evidence EXIST, can it carry?      │
   1b-claims       which claims are supported / weak / GAP?    │
   ─────────────────────────────────────────────────────────── │
   2a-venue        which outlet, and what does it demand?    ← the pin
   2b-pitch        what is it selling, in one minute?          │
   3-narrative     how do claims become an arc?             venue-ALIGNED
   4-display       what figure or table carries each claim?    │
   5-section-edit  does each section's prose do its job?       │

 THE CLEAVE THAT PROVES THE RULE
   1a-resource  "does it EXIST and can it carry a claim"   may never train
        ╎                                                   may never evaluate
   1b-claims    "what does running it SAY"                  runs the experiment
   Collapse these two and the paper loses the difference between
   HAVING EVIDENCE and HAVING A VERDICT.

 WHAT IS NOT SETTLED
   nothing checks the rule. A stage grows a second question SILENTLY,
   and the only symptom is a gate nobody can pass:
      4-display  ──►  "is the display stage done?"  across 11 assets
                      13-record checklist · never closed  (fixed in QB4)
```

## Content
### The eight questions, as they stand
```
 0-seed         why might this paper exist?
 1a-resource    what must exist for this to be testable, does it, can it CARRY the claim?
 1b-claims      which claims are supported, weak, or GAP?
 2a-venue       which outlet, and what does it demand?
 2b-pitch       what is the paper selling, in one minute, to that outlet?
 3-narrative    how do claims become a manuscript arc?
 4-display      what figure or table carries each claim?
 5-section-edit does each section's prose do its job?
```

### Why the one-question rule earns its place
Two stages cleave on it in a way that matters: resource asks whether ingredients EXIST and can carry a claim, while claims RUNS the experiment that moves a claim's status. Resource may never train or evaluate. Without one question per stage, that boundary blurs into "the data stage", and the paper loses the distinction between having evidence and having a verdict.

### What is not settled
Nothing checks it. A stage that grows a second question grows it silently, and the only symptom is a gate nobody can pass, which is what happened to the display stage before it was split.

## Items to Finish
- [x] 📝 The eight questions are written down
      `PHILOSOPHY.md` carries them as a table, and each `stage.md` repeats its own as `one_line`.
- [ ] 🧠 Rule whether the one-question rule is enforceable
      A stage whose gate cannot be answered by one human sentence has probably grown a second question. That is a検 checkable symptom; decide whether CHECK is where it is caught.
- [ ] 📐 State what disqualifies something from being a stage
      Compiling, submitting and responding to reviewers all sit outside the eight. Say why, so the next addition is argued rather than appended.

## Where we are
The rule is stated and followed; it is not enforced. The one time it broke, on display, it was caught by a human noticing a checklist that would not close.

## Files
- `PHILOSOPHY.md`
  The stage table and the design prompt.
- `stages/index.yml`
  One row per stage; the header explains what belongs in it.
