# ① ORGANIZE · what must the strip refuse to carry?

state: 🟡 PARTIAL
owner: JL
method: write the executor-facing question, freeze it, and keep the original beside it so the strip can be audited rather than trusted

## Opening
Turning a consumer's question into the one that crosses is the probe's core act; what must it drop, and how do we know it dropped it?
Everything that says why the asker wants to know, and by keeping the original next to the rewrite so a reviewer can compare the two.
The defence is structural rather than careful, because a stake hides in ordinary words and no amount of care catches all of them.

The rewrite is easy to do badly and the failure is invisible.
"Rescue", "we want", "the hoped-for", a claim id, or "our paper" all carry a stake, and a question can leak the wanted answer purely by what it declines to ask.
A leaked stake does not produce an error; it produces an answer shaped around one hypothesis, which reads fine to the asker and is worth nothing to the next consumer.

**Covered elsewhere**: The file the act writes into, and its four subsections, is `QA7`; where the stake legitimately lives is `QA6`, which also holds the open ruling on the word list. The T0 case, where an existing q-executor already asks it, is `QB3`'s ladder.

## Diagram
```
   Q-consumer (stage doc, KEEPS the stake)
     "does WellDoc have a cycle column? my claim C6 dies if it does"
            │
            │  ① ORGANIZE
            ▼
   find-or-open  1-probes/PP03_welldoc/QX1_cycle.md
     ### q-executor      ← written here, then FROZEN
        "Scan all 40 WellDoc CSV tables for menstrual/cycle/hormone
         columns. Report which exist, or none.
         Deliverable: QA digest + machine artifact.
         Accepted: present | absent."
     ### q-consumer      ← the ORIGINAL copied in, id and wording intact
        * Q-Claim-6 — does WellDoc have a cycle column? (C6 dies if it does)
     route: task | discovery                    ← chosen here

   FIND-or-open: if an existing q-executor already asks it, add a
   `### q-consumer` bullet and open NO new entry. that is T0 JOIN,
   and it is why one q-executor may serve several consumers.

   ── what the rewrite must carry, beyond the question ─────────────
   Deliverable:  what the executor should produce
   Accepted:     the shape of a legitimate answer   present | absent

   a question with no accepted shape is not answerable, it is a topic.
```

## Content
### 1 · Frozen, because an edited question invalidates a landed answer
#### The q-executor is written once and never revised
(editing it after dispatch means the answer on file was given to a different question)
Freezing is what makes the entry auditable later: the text next to the answer is the text that produced it.
If the question turns out to be wrong, the correct move is a new entry, not a rewrite, because the old answer is still a true answer to the old question.

#### The original is kept so the strip can be audited rather than trusted
(`### q-consumer` copies the stage-doc question in, id and wording intact)
A reviewer can then answer one question: did the strip lose anything, and did it leak anything.
Keeping only the stripped version makes that impossible, and keeping only the original means the payload is reconstructed on every run.

### 2 · The pre-gate review reads what a checker cannot
#### A fresh-context sub-agent grades the plan before the human sees it
(a creator/reviewer split, so the drafter does not grade its own work)
Per entry it checks that the q-executor is clean, answerable and specific, that `route` is set, that `bank` was judged by reading a specific candidate ON THE ANSWER, that `target` agrees with `bank`, and that each `### q-consumer` bullet copies in a real stage-doc question.
Per file it checks that no stake appears anywhere.
It runs before the human gate and never replaces it, and it is complementary to `check-probe-cards.sh`: one judges meaning, the other counts fields.

#### Two of the checker's codes belong to this step
(`stake-disclosed` and `LAW2-q-executor-leak`)
Both are word-list tests over the `### q-executor` text, and neither appears in the eleven conditions `SKILL.md` documents.
So the strip is machine-checked, weakly, by a mechanism the manual does not mention, which is `QC2`'s finding seen from this step.

## Aims
- [x] ✂️ The strip has its own subsection, frozen once written
- [x] 🪞 The original is kept beside it, so the strip is auditable
- [x] 📋 A fresh-context reviewer checklist exists and runs before the gate
- [x] 🎯 A q-executor carries `Deliverable:` and `Accepted:` lines
      Without an accepted shape a question is a topic, and topic-shaped questions are what make `QB3`'s match-on-the-answer rule unusable.
- [x] 🔎 T0 JOIN happens on real data, and the reduction is measurable
      MISQ paper, 260726: **27 consumer questions reduced to 17 q-executors**, a 37 percent collapse, with 6 entries serving more than one consumer and one serving four.
      This is the evidence that the unit was chosen correctly: numbering by consumer question would have opened 27 bank entries for 17 distinct facts.
- [ ] 🧪 A leaked stake is caught by something other than a word list
      `stake-disclosed` and `LAW2-q-executor-leak` are both word-list tests, and `QA6` records a live false positive from the same family of test.
      This closes when the ruling on `QA6` lands and this step's check follows it.

## States
The act is structurally sound and measurably doing its job.

Freezing, keeping the original beside the rewrite, and grading the result in a fresh context are three independent defences, and none of them depends on the writer being careful.
The 260726 count settled the question this step exists to answer: 27 consumer questions became 17 q-executors on the MISQ paper, so the joining the unit was chosen for is real rather than theoretical.
What is not settled is the leak test itself, which is a word list on both of its surfaces and produced a false positive the same week it produced no true ones.

## Files
- `SKILL.md`
  The four forms, the strip, and the DRAFT self-review checklist.
- `ref/probe-template.md`
  The fillable form, including the `Deliverable:` and `Accepted:` lines.
