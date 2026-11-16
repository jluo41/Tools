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
2. **S2 · Compare with the venue's examples.** Same journal, same article type (the venue's examples, haipipe-paper-draft
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
   **Paragraph rewrite (JL 261115: "just totally using the loop of /haipipe-paper-draft to rewrite them, and reviewing
   them and updating them ... Currently, it is so hard to read").** When a paragraph has three or more sentences under 8,
   or reads as a patched list after a round of sentence cards, stop carding it: the writer rewrites the paragraph whole
   (grouping, order, hand-offs; plan, evidence targets and numbering move in the same edit), two fresh readers rate its
   sentences and the paragraph again, and one blind reader compares old and new paragraph as an unlabeled pair (easier,
   same meaning). Keep the new paragraph only when it wins; otherwise go back toward the old wording. Repeat until the
   paragraph and its sentences hold at 7 to 8 or more ("the sentence and paragraph score should be around 7 and 8"),
   then hand the person only the few cards they must decide. A paragraph the person ticked is never rewritten.
3. **D3 · Highlight for the person.** What the loop could not settle is marked on the page: a claim, a story choice, a
   missing fact. These are the only items the person must read first; the loop never decides them.

   **Fix or comment, then the person, then the next loop (JL 261116: "if you find the issue, then fix them, if you
   cannot fix it, then you create a comment and state what is the problem, and then I will work on that sentences,
   and then we do next loop").** Each round, for every sentence the raters put under 8: when a wording fix or a move
   inside the Section can solve it without a new fact, write the fix, run the blind A/B check, and apply it when it is
   kept. When it cannot be fixed that way (a missing fact, a number the reader cannot check, a paper-wide term, a story
   choice, or a fix the A/B reader rejected), write a page comment on that sentence in
   `draft/records/<stem>-comments.md` (`### Comment <n> · <address>`, `State: open`, one `- Note · <time> · AI: <the
   problem, one plain question>` line, about that sentence only). The person answers or edits those sentences on the
   page; the next round starts from their answers, replies under each comment, and rates again.
4. **D4 · The person's feedback.** The person comments and decides on the page (Draft Lab cards and comments); the
   text is updated from it, each change shown as a card.
5. **D5 · The person checks every sentence.** A ✓ per sentence, by the person only. A checked sentence gets no new
   proposal or score until its words change.

## The version's Narrative (JL 261115)

The version Job's Narrative is the starting version. Once a Section is drafting, its own plan is the truth for that
Section. While Sections draft, a Narrative row that differs from a Section plan, or a Story row that changed since a
sign, is one quiet note on the version Job page: never a health FAIL, never a re-sign (must-check M-D09). When the
Sections are good, one Job-level step rebuilds the Narrative rows (moves, displays, claims) from the Section plans:
`page.py sync-narrative <version Job>` proposes them as a diff, the Story claims follow from the same pass, and JL
signs once (M-D19). The version then moves on.

```text
Narrative v0 ─▶ each Section drafts against its own plan (no re-sign) ─▶ Sections good
           ─▶ sync-narrative: new rows as a diff ─▶ JL signs once ─▶ next step
```

## Beside both loops

- **Evidence.** Each CITE is verified by a person against the paper itself; each VALUE is bound by its value id to the
  pinned value Run (haipipe-paper-evidence). Neither is decided by a reviewer's score.
- **Displays.** Each display passes its own review (haipipe-display) and its caption names the current numbering.

## Where a Section stands

Not shown on the page. A Draft Lab line of the eight steps was tried on 2026-11-15 and deleted the same day: three
steps (S1, S2, D3) leave no record to read, and D4 counted cards but not open comments, so it was wrong on 3 of 8 for
ScalingGlucose t01 (JL agreed: a wrong state reads worse than none; must-check M-D16). Ask the Section session, or
read its records; a step line comes back only when every step leaves a record it can be read from.
