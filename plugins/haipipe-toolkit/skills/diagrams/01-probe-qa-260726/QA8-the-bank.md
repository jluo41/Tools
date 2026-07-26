# ⑨ The bank must not know it was asked

state: 🟡 PARTIAL
owner: JL
method: define the bank by what is absent from it, so the property is checkable by looking

## Question
Why may nothing under `tasks/` or `discoveries/` mention that a probe exists?
Because an answer written for a specific asker is worth less to everyone else, so the bank writes for its own reasons.
The rule is stated as an absence, no mailbox and no back-reference, because an absence is checkable by looking and a rule about intent is not.

The asymmetry is the whole design and it is easy to erode by being helpful.
A consumer session that writes a QA digest itself, or a task folder that grows an `_ASK/` inbox, has quietly made the bank probe-aware, and from then on the answers are shaped by who asked.
An absence is checkable by looking, which a positive rule about intent would not be, and 260726 was the first day anyone actually looked.

## Boundary
- ✅ Covered here
  What the bank may not contain, LAW 2's surface, who is allowed to write a QA file, and what the asymmetry costs the consumer.
- ↪ Covered elsewhere
  The law that forbids a consumer session from writing bank files is `QA6`; the QA file's state line and its contract are `QC1`; the checker is `QC2`.
  The consumer side of the wall is `QA7`.

## Diagram
```
   tasks/<leaf>/QA/<n>-<slug>.md      discoveries/<g>/<f>/QA/<n>-<slug>.md
   ─────────────────────────────      ──────────────────────────────────
   `ls QA/` IS the index. slug only, never a PP id.
   OPTIONAL: not every task-folder carries one.

   ── stated as an ABSENCE ─────────────────────────────────────────
   ⛔ no mailbox        no _ASK/ · no _ANS/ · no inbox of any shape
   ⛔ no back-reference no answers: field pointing at a consumer
   ⛔ no probe id       no PPnn, no QX id, anywhere under a bank
   ⛔ no consumer vocab LAW 2: no claim ids, no "the paper" meaning
                        OUR paper

   ── ONE WRITER, for the whole life of the file ───────────────────
   the EXECUTOR writes twice: the CLAIM at start, the COMPLETION
   at its Report. a CONSUMER never creates, claims, edits, completes
   or supersedes one. a probe that finds a stale target re-points
   its OWN entry, never the file.

   ── measured 260726, across every project in the SPACE ───────────
   _ASK/ or _ANS/ folders                        0   ✅
   QA files under a bank                        10   (7 task, 3 disc)
   LAW 2 hits in those 10 QA files               0   ✅ one false pos.
   PP ids elsewhere under a bank                 1   ⛔ and unchecked
     tasks/Z01_…/08_agreeableness_pop_distribution/RUN_AUDIT.md:32
     "carries the PP11 bootstrap-N caveat verbatim"
```

## Content
### 1 · Stated as an absence
No mailbox, no back-reference, no probe id under `tasks/` or `discoveries/`.
`_ASK/` folders are a hard fail, and as of 260726 there are none anywhere in the SPACE, which is a change from what this page previously claimed.

### 2 · The rule's surface and the lint's surface are not the same
#### LAW 2 watches `QA/*.md`; the absence rule covers the whole bank
(and the one real violation in the SPACE sits outside the watched window)
The lint checks that QA files carry no consumer vocabulary, and on the MISQ project's 10 QA files it is clean.
The absence rule is broader: no probe id ANYWHERE under a bank.
The checker's own bank pass covers three things and no more: LAW 2's word list inside `QA/*.md`, a `pp-id-in-bank-filename` test on the QA FILENAME, and an `_ASK/` or `_ANS/` folder at two directory depths.
A grep for `PP\d\d` across every project's `tasks/` and `discoveries/` returns exactly one hit, and it is inside a `RUN_AUDIT.md` body, which is none of those three, so nothing that runs today would ever see it.

#### A word list produces false positives on legitimate prose
(one QA file trips "this paper" while referring to a paper in the literature)
`discoveries/M01_…/QA/1-construct-validity-anchor.md` reads "citing this paper does not upgrade it into construct evidence", where "this paper" is a cited source and not the consumer.
That is the correct sentence and the lint would flag it, which is the concrete case behind `QA6`'s open ruling on whether the word list is the right test.

### 3 · One writer, and why a helpful consumer is the threat
The executor owns the file for its whole life, writing twice: the claim when it starts, the completion at its Report.
The failure mode is not malice, it is helpfulness: a consumer that writes the digest itself has produced a file shaped by its own question, and every later reader inherits that shape.
So the ban is on the act rather than on the content, and it is stated for creating, claiming, editing, completing and superseding, individually, because each is a plausible way of being helpful.

### 4 · The cost is that the consumer must read
Because the answer was not written for this asker, the consumer has to read it and decide whether it answers the question.
That is `QB3`'s rule that a hit counts only if the file literally answers, and topic similarity is not evidence.

## Items to Finish
- [x] 🚧 The property is stated as an absence and is checkable by looking
- [x] 🔍 The absence is measured rather than assumed
      260726, across every project: zero `_ASK/` or `_ANS/` folders, 10 QA files, zero LAW 2 hits inside them.
      This page previously said three legacy projects still carried `_ASK/` folders; they are gone, and the claim was stale rather than wrong at the time.
- [ ] 🧹 The one probe id under a bank is landed or ruled
      `tasks/Z01_Display_PhyTraitOpioid/08_agreeableness_pop_distribution/RUN_AUDIT.md:32` quotes "the PP11 bootstrap-N caveat", putting a consumer id inside a bank file.
      Either the id is removed, or the rule is narrowed to say which files under a bank it actually covers.
- [ ] 🔍 The absence check runs routinely rather than once
      The 260726 sweep was three greps run by hand and is not part of any checker.
      This closes when a `PP\d\d` and `_ASK/` sweep across `tasks/` and `discoveries/` runs at CHECK, on the whole bank rather than only on `QA/*.md`.
- [ ] 🧠 JL rules how wide the absence rule really is
      "No probe id anywhere under a bank" and "QA files carry no consumer vocabulary" are two different rules, and only the narrower one is enforced.
      The one live violation is exactly in the gap between them, which is why the width matters rather than being a technicality.

## Where we are
The rule is ruled, the current skills honour it, and as of 260726 the bank surface has actually been looked at rather than assumed.

What the look found is better than expected on the watched surface and worse than expected off it.
Every `_ASK/` folder this page used to worry about is gone, and the 10 QA files are clean.
One consumer probe id sits in a `RUN_AUDIT.md` under a task folder, in the part of the bank no lint covers, which is not a data-cleanup item so much as evidence that the rule and its enforcement are different sizes.

## Files
- `SKILL.md`
  The asymmetry, the ban on mailboxes and back-references, the one-writer rule and LAW 2.
- `haipipe-task/`
  Owns the `qa` verb that writes these files, and the claim-then-complete flow.
- `haipipe-discovery/`
  The twin, same shape, same door.
