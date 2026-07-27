# The QA digest: the only readable answer
state: 🟡 PARTIAL
owner: JL
method: write one file per direction explored, in general language, for nobody in particular

## Question
What does this layer hand out when someone asks it something? One file: `QA/<n>-<slug>.md` inside the task-folder that did the work, holding plain prose with `[→ results/…]` anchors back to the evidence. That is the entire readable surface of the bank, and a consumer reads it and never reaches past it.

The property that makes it worth writing is that it is addressed to nobody. It carries no claim id, no paper name and no reason anyone wanted to know, so the next question that lands on the same ground inherits it whole. A digest written for one consumer would have to be rewritten for the next, and a bank of those does not accumulate.

The awkward part is that it is written for reasons the writer decides. `SKILL.md` gives three: a question arrived, results already answered something with no digest, or a finding was judged worth digesting. That last one is entirely this layer's own judgment, which is correct and means the bank's coverage depends on a call nobody reviews.

## Boundary
- ✅ Covered here
  What a digest is for, when one is due, what it may not contain, and why it is addressed to nobody.
- ↪ Covered elsewhere
  The QA FILE CONTRACT is not ours: its `state:` line, the `started:` TTL, supersession and the checker codes are `QC1@probe` and `QC2@probe`. What may not leave besides it is `QD2`; the door a question arrives through is `QA5`; the phase that writes it is `QB5`.

## Diagram
```
   QA/<n>-<slug>.md          the ONE readable answer, per task-folder

     # Q — <the question, in general language>
     ## Answer        prose, with [→ results/<file>] anchors
     ## Caveats       what would make this wrong
     ## Not-done      what was NOT checked

     <n> = creation order, so `ls QA/` IS the index. No INDEX file.

   ── the three reasons one is DUE.  no others ───────────────
      ① a question arrived through the qa door           → QA5
      ② results/ already answered something and no
        digest existed for it
      ③ a finding was judged worth digesting             ← our own call

      a QA/ mirroring every result is NOISE. This is why 1 of 107
      folders having one is not by itself a problem.

   ── what it may NOT contain ────────────────────────────
      ✗ a claim id          C6, H3
      ✗ a consumer's name   "the paper"
      ✗ a probe id          PP03, Q-Seed-4
      ✗ any word this layer could not have produced on its own

      the test is not "is it neutral". it is: could this file have
      been written by someone who never heard of the asker?

   ── ⚠️ WE WRITE THEM. WE DO NOT RULE THEM. ─────────────────
      the state line          QC1@probe
      the checker codes       QC2@probe
      supersession + TTL      QC1@probe

      this face owns the EXECUTOR's half: when one is due, what
      goes in it, and what may not. A rule restated from ⑥ here
      will drift from ⑥ within the week.
```

## Content
### Addressed to nobody, which is what makes it reusable
The digest is the executor's own writing about its own results. That it happens to answer
somebody's question is incidental to its content, and deliberately so: a file that names the asker
has a single reader, and a bank of single-reader files is a pile of correspondence rather than a
bank.

The practical test is sharper than "keep it neutral": could this file have been written by someone
who never heard of the person who asked? If not, something crossed the wall.

### One writer, and it is this layer
A consumer never writes a QA file. The probe layer never writes one. This layer writes it, at
Report, and the invariant the family states is ONE WRITER rather than write-once: the file has a
mutable `state:` line, claimed when work starts and completed when the answer lands, and exactly
one party may touch it.

The contract for that line belongs to `01-probe-qa-260726` and is linked rather than repeated here,
because two boards stating one contract is how the two versions start to differ.

### Coverage depends on an unreviewed judgment
Reason ③, a finding worth digesting, is this layer's own call and no one checks it. That is
consistent with the design: making the bank easier to ask is the executor's own work. It also means
the bank's usefulness is set by how often that judgment gets exercised, and today the answer is 1
digest across 107 task-folders.

Low is not automatically wrong, since most folders were never asked about. It is worth knowing
rather than assuming.

## Items to Finish
- [ ] 🔍 Make the vocabulary rule checkable
      A grep for claim ids, probe ids and consumer nouns over every `QA/*.md`. The rule is stated in three documents and enforced in none. Shared with `QA5`.
- [ ] 📏 Decide whether 1 of 107 is a coverage problem
      Reason ③ is unreviewed by design. Either that is fine and the number is expected, or the bank is under-digested and something should prompt the call at Report.
- [ ] 🔗 Keep the contract on `⑥` and link it
      This face must hold only when-and-what. The state line, the TTL and the checker are `QC1@probe` and `QC2@probe`, and restating any of them here creates two authorities for one rule.
- [ ] 📝 State the three reasons in the reporter's own contract
      They live in `SKILL.md` prose. The creator agent, which actually decides at Report, does not carry them.

## Where we are
The contract exists in `fn/qa.md` and the shape is stable: `# Q`, `## Answer` with anchors,
`## Caveats`, `## Not-done`, ordered by creation so `ls` is the index.

Adoption is 1 of 107 task-folders, and no checker verifies the vocabulary rule that is the whole
point of the format.

- 260726 CC · 📏 Counted the adoption and declined to call it a bug
      One digest across the bank. Because reason ③ is a judgment nobody reviews, a low number is evidence about how often the layer writes for its future self, not proof of a defect.

## Files
- `fn/qa.md`
  The digest contract: the template, the state line, supersession, the checker codes.
- `SKILL.md`
  The three reasons a digest is due, and the vocabulary ban.
- `QC1@probe`
  The state line's own ruling. Consulted, never restated.

## Log
260726 · Created with the board.
