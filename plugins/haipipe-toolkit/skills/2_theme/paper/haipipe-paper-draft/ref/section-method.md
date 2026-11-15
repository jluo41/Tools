# Working a Section · the structure loop, the draft loop, evidence beside them

JL set this method on 2026-11-15 (ScalingGlucose t01_introduction, passed on by the Board). Every Section session
follows it, so no Board message has to tell each one. The worked example is ScalingGlucose `t01_introduction`:
structure loop done at Draft v1.2; draft loop round 1 done (`t03 r02`, `t01 r05`, `t02 r05_t01_blind_ab`, then v1.3).
Each step has a must-check row (haipipe-paper `ref/must-check.md`, M-E01 to M-E09) that says how it is checked.

```text
structure loop   S1 check ─▶ S2 compare with the venue ─▶ S3 new Draft version (story change: versions, JL picks)
draft loop       D1 rate ─▶ D2 auto loop ─▶ D3 highlight for the person ─▶ D4 person's feedback ─▶ D5 person checks all
beside both      E  each CITE verified by a person · each VALUE bound to its pinned value Run · displays
```

## The structure loop

1. **S1 · Check the structure.** Each paragraph's job (the move it makes in the Section) and each sentence's slot in
   it, read from the Draft's Structure Overview and § 3 (`page.py structure <task>` prints it).
2. **S2 · Compare with the venue's examples.** Same journal, same article type (the venue's examples, haipipe-paper
   § Examples first): number of paragraphs, words, how it opens, how the questions and the results are stated.
   Write down each difference that matters.
3. **S3 · Update the structure as a new Draft version.** A change that keeps the story goes in. A change that alters
   the story (what the Section claims, the order of the argument) is proposed as 2 to 4 versions, and JL picks.

## The draft loop

1. **D1 · Rate.** Fresh reviewers who never wrote the text rate every paragraph (haipipe-draft-review
   `ref/paragraph-logic.md`) and every sentence (`ref/sentence-logic.md`: logic, read, ai). A pass is 8 or more.
2. **D2 · Auto loop.** Each item under 8 gets a rewrite; fresh blind A/B readers judge each pair; only "easier and the
   same meaning" is kept (a pair saying `meaning: no` is never adopted, nor is a later pair carrying its words); the
   kept rewrites are adopted as the next Draft version; what changed is rated again. Repeat until nothing kept changes.
3. **D3 · Highlight for the person.** What the loop could not settle is marked on the page: a claim, a story choice, a
   missing fact. These are the only items the person must read first; the loop never decides them.
4. **D4 · The person's feedback.** The person comments and decides on the page (Draft Lab cards and comments); the
   text is updated from it, each change shown as a card.
5. **D5 · The person checks every sentence.** A ✓ per sentence, by the person only. A checked sentence gets no new
   proposal or score until its words change.

## Beside both loops

- **Evidence.** Each CITE is verified by a person against the paper itself; each VALUE is bound by its value id to the
  pinned value Run (haipipe-paper-evidence). Neither is decided by a reviewer's score.
- **Displays.** Each display passes its own review (haipipe-display) and its caption names the current numbering.

## Where a Section stands

The eight steps are the Section's state, shown as one line per Section (Draft Lab), each step with its mark:
`S1 ✅ S2 ✅ S3 ✅ · D1 ✅ D2 ✅ D3 🙋 D4 ⬜ D5 ⬜`. A step is done when its record exists: S3 a new Draft version, D1 a
review Run at the current version, D2 an adopted version after a blind A/B Run, D3 the highlight list, D4 the person's
cards decided, D5 every sentence ✓ at its current words.
