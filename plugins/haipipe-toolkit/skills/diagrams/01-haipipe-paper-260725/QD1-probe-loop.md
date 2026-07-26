# How a question leaves the paper and comes back
state: 🟡 PARTIAL
owner: CC
method: keep the five steps; keep the stake inside the paper

## Question
How does a paper get an answer to something it is not allowed to find out itself?

The paper may not run code or read the literature. It raises a question, hands it to a layer that can, and binds the answer back by path. The design question is what travels in each direction, because that is what decides whether the answering layer can be trusted to answer honestly.

## Boundary
- ✅ Covered here
  The five-step loop and what crosses the boundary in each direction.
- ↪ Covered elsewhere
  What a dispatch is allowed to cost is `QD2`; what the prose holds while waiting is `QD3`.

## Content
### The five steps
```
 ① ORGANIZE   one entry file per question, in 1-probes/PPNN_<topic>/
 ② MATCH      grep the bank's existing answers; most questions close here, free
 ③ DISPATCH   hand the executor-facing question, verbatim, to task or discovery
 ④ POINT      record the path of the answering QA file
 ⑤ INTERPRET  read the answer back into the stage, and discharge the placeholder
```

### The rule that makes the answer trustworthy
The entry file separates the question into a `q-executor` half and a `q-consumer` half. Only the executor half is dispatched, and it carries no stake: no claim id, no hypothesis, no indication of which answer would be convenient. The stake stays in the paper.

That is the whole point. An executor that knows the paper needs a significant result is an executor whose answer cannot be relied on, and the separation is what makes the answer evidence rather than agreement.

### What is unsettled
Step ⑤ is the weakest link. An answer that lands but is never woven back leaves the paper carrying a placeholder and a closed probe at the same time.

## Items to Finish
- [x] 🚪 One door, five steps
      Implemented in the PROBE worker; entries live in the paper, answers in the bank.
- [x] 🧱 The stake stays home
      Only the stake-free half is dispatched.
- [ ] 📐 Define when ⑤ is complete
      An answer is interpreted when it is woven into the prose AND its placeholder is discharged. Today those are two separate acts and nothing checks that both happened.
- [ ] 🔎 Decide what happens to a question the bank refuses
      Refusal is a real outcome; the loop currently describes only answers.

## Where we are
Steps ① to ④ are implemented and used. Step ⑤ is done by hand and is where the loop leaks.

## Files
- `haipipe-probe/`
  The probe layer's own skill: anatomy, the five steps, the QA state contract.
- `PHILOSOPHY.md`
  Evidence routing and the boundaries.
