# What is NOT a probe

state: 🟡 PARTIAL
owner: JL
method: ask whether a consumer is behind the question, and hand it to the bank's own door when nobody is

## Opening
A question arrives at `/haipipe-probe` with nobody behind it; what happens to it?
It is routed to the executor's own door and no probe file is opened, because a question with no consumer is not a probe.
That test is the sharpest line the layer draws, and it is the difference between the layer and the thing it talks to.

The temptation runs the other way, which is why the rule needs stating.
Opening a probe file feels like doing the work, and it produces an artifact, and the artifact looks like progress.
But with no consumer there is no stake to strip, no stage doc to interpret the answer back into, and no reason for the answer to travel through a second file: what is left is a question for the bank, which has its own door.

**Covered elsewhere**: The skill's four verbs, as part of what the shared model ships, are `QA2`; what `status` derives is `QC3`. The loop a real probe enters is `QB1`.

## Diagram
```
   is there a CONSUMER behind this question?

        yes ─▶ it IS a probe       → the five-step loop, QB1
        no  ─▶ it is NOT a probe   → task-shaped      → /haipipe-task qa
                                   → discovery-shaped → /haipipe-discovery qa

   the routing verb ROUTES; it does not execute, and it does not
   open a file. `/haipipe-probe "<question>"` is a signpost.
```

## Aims
- [x] 🚦 The routing rule is stated, with both destinations named
- [ ] 🧪 The routing verb is exercised once, both ways
      A question with a consumer and one without, to confirm the second is handed on rather than wrapped in a probe file nobody reads.
- [ ] 🧠 JL rules what happens to a question whose consumer appears later
      Today it would be routed to the bank and then, when a consumer wants it, matched at T2 like any other answer.
      That is probably correct and it is nowhere written down.

## States
Stated in the skill and unexercised.
The routing test is the sharpest sentence in the verbs section and the one most likely to be skipped, because opening a probe file feels like doing the work.

## Files
- `SKILL.md`
  The verbs block and the routing rule.
- `haipipe-task/`, `haipipe-discovery/`
  The two doors a non-probe question is handed to.
