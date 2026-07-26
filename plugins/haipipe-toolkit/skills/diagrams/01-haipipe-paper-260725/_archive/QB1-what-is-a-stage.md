# What is a stage?
state: 🟡 PARTIAL
owner: JL
method: keep the one-question rule; decide whether it is enforced or merely stated

## Question
What makes something a lifecycle stage rather than a task, a phase, or a folder? The working answer is one question, one artifact, one gate, and this face is where that answer is wired to everything else on the board: a stage is the object every other QB face describes one part of, and reading it should tell you which part you want.

The working answer is: a stage answers exactly ONE question, produces ONE artifact, and closes at ONE human gate. That rule is what stops the lifecycle turning into a folder of chores, and it is already doing real work: it is why "compile the manuscript" is not a stage of section-edit, and why the eight stages have the shapes they do. What is unsettled is whether anything enforces it.


The way to settle it is to state the test, one question and one artifact and one gate, and then hold the eight existing stages against it rather than reasoning in the abstract. What we want is a rule strong enough to say no to a ninth stage, because a definition that admits everything is not doing any work.
## Boundary
- ✅ Covered here
  The definition of a stage, and the one-question rule.
- ↪ Covered elsewhere
  The four phases inside a stage are `QB2`; the gate is `QB8`; whether a stage may run per-unit is `QB12`.

## Diagram
```
   ONE STAGE, WHOLE. Every part names the face that rules it.

   ┌───────────────────────────────────────────────────────────────────┐
   │ IDENTITY                    key · order · title                    │
   │   one_line                  THE one question it answers   → QB1    │
   │   board_family/unit/slug    which S page it writes        → QB10   │
   └───────────────────────────────────────────────────────────────────┘
                                    │
   ┌────────────────────────────────▼──────────────────────────────────┐
   │ THE FOUR PHASES              phases: [draft, probe, revise, check] │
   │                                                          → QB2     │
   │   DRAFT   raises questions, invents nothing              → QB3     │
   │      │      writes prose + \cite{TOADD} [Q-X-n]          → QB6     │
   │      ▼                                                             │
   │   PROBE   the one door evidence enters by                → QB4     │
   │      │      probe_depth: 0   the spending ceiling         → QB5     │
   │      │      probes: 1-probes/PPNN_<topic>/    ──▶ ⑤ the wall       │
   │      ▼                                                             │
   │   REVISE  substitutes only LANDED answers, comments why  → QB7     │
   │      │                                                             │
   │      ▼                                                             │
   │   CHECK   gates: [check]   ONE human yes                 → QB8     │
   │             done_criteria · closed_when                            │
   └────────────────────────────────┬──────────────────────────────────┘
                                    │
   ┌────────────────────────────────▼──────────────────────────────────┐
   │ WHAT IT PRODUCES                                                   │
   │   artifact:   the S page on ⑧, and the page IS the product → QB9   │
   │   generated:  0-sections/*.tex · float.tex, on ⑦ · one way → QB11  │
   │   artifact_fallback:  for papers older than the restructure        │
   └───────────────────────────────────────────────────────────────────┘
                                    │
   ┌────────────────────────────────▼──────────────────────────────────┐
   │ HOW IT VARIES                                                      │
   │   runs: once | per-unit      the grain, decided by the gate → QB12 │
   │   venue_free | venue_aligned  survives a retarget, or not  → QB13  │
   │   needs_paper                 can it run on a bare topic           │
   └───────────────────────────────────────────────────────────────────┘

   ── who it talks to, and through what ──────────────────────────────
      ③ /haipipe-board    create-page.py calls stage.py to make the page
                          Board owns the filename, Paper the Content jobs
                                                          → QA4 QA8 QA9
      ⑤ /haipipe-probe    PROBE crosses the wall; the answer is POINTED
                          at, never copied                        → QA5
      upstream/downstream · handoff   craft orientation only. The
                          authoritative dependency is the PAGE's
                          `requires:`, never these.                → QA8

   ── the test, and the only one that matters ────────────────────────
      ONE question · ONE artifact · ONE gate.
      A thing with two questions is two stages. A thing with no gate
      is a phase. A thing with no artifact is a folder.
      Its worth is whether it can refuse a NINTH stage, and it has
      never been asked to.
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

### The contract is the stage
There is no stage object anywhere in the code. A stage IS its `stage.md` frontmatter: twenty-eight declared fields, read by a router that loads exactly one of them per invocation. Every concept this group argues about is one of those fields, which is why the diagram above is also a field map.

That is worth saying plainly because it changes what a ruling means here. Settling `QB12`'s grain question is not an idea; it is a change to `runs:`. Settling `QB5` is a change to `probe_depth:`. A face on this board that cannot name the field it would change has not finished its work.

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

## Log
260726 · Rebuilt as the anchor of QB: one stage drawn whole, every field naming the face that rules it. Added the observation that there is no stage object in the code, only 28 contract fields, so a face that cannot name the field it would change has not finished.
