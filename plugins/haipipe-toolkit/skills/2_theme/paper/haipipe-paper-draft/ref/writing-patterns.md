The writing patterns found on a paper and the co-authors' patterns, with the sentence-by-sentence and easier-to-read checks; moved from SKILL.md.

## 📝 Writing patterns found on ScalingGlucose (261111-261112)

Each came from JL on Paper-ScalingGlucose-NatSeries2026, in the shape of a Board's `writing-patterns.md`: the
pattern, JL's words, our sentence, the fix, and the check that holds it where one can.

1. **Paragraphs of 4 to 7 sentences.** JL: "unless having good reason, we might make sure they are between 4~7
   sentences". Ours: Introduction P3 had 10, P5 had 13. Fix: split at the natural turn (10 into 4 + 6, 13 into
   6 + 6); the Abstract is exempt, and a `reason:` line under the heading accepts an exception (§ Paragraphs of 4
   to 7 sentences). Check: `page.py health` row `paragraph`, checklist W7, anti_slop `paragraph-length`.
2. **Titles reviewed blind.** JL: "you should call the subagent to review them to make sure they are academic and
   human understandable". Ours: 50 of 80 titles rewritten after review. Fix: a blind reviewer scores each title,
   label, arc and reader question; under 8 is rewritten in § 1 and § 3 together (§ Titles read like the text).
3. **No money metaphors.** JL: "I don't know why here we use the word of 'buy'". Ours: "Here we measure what scale
   buys for each use". Fix: name the measured quantity, "where scale reduces error", "how scale changes error for
   each task". Check: anti_slop `title-metaphor` (titles, labels, arcs) and `money-metaphor` (prose; a literal paid
   claim is not flagged).
4. **No in-group shorthand in titles.** Ours: "rolled forward", "head", "route", "grid", "roadmap", "use". Fix:
   "recursive rollout", "linear head on the frozen model", "the way data were added", "model sizes and
   configurations", "study design", "downstream task". Check: anti_slop `in-group-shorthand` (titles only).
5. **The research questions stated together.** JL: "where are the two questions? i didn't see it." Fix: ask them
   as questions with "?", one right after the other ("First, …? Second, …?"), never split by other sentences.
   No automatic check; the cold read looks for it.
6. **No post-hoc "We expected …" in the Introduction.** JL: "do we really have evidence for this?" Ours: an
   `[Expect]` Bullet with `Evidence: none`. Fix: ask the question, give the known prior result with its citation,
   leave the answer to the Results. Check: `page.py health` row `expect` (an Introduction's `[Expect]` Bullet whose
   Evidence line says none).
7. **The title paragraph holds the title.** JL: "could you put the title here?" Ours: C1.P0's Bullet read "The
   paper's title." Fix: write the paper's title in the `[Title]` Bullet. Check: `page.py health` row `title`.
8. **The whole paper's structure before a Section's plan.** The version's `## Narrative` is signed (`page.py
   sign-narrative`) and shown in Report › Structure beside the Board Story § 8 (the shared title, story and
   claims); a Section's plan follows its row. Check: `page.py health` rows `narrative` and `row`.
9. **Examples as one drawing per Section.** Each example paper is one area of the examples drawing (its screenshot,
   then its logic as a mind map), drawn by `excalidraw-read ref/section_screens.py draw <topic>` and read beside
   our own plan in Report › Structure (frame jump per paper).

## 🧑‍🤝‍🧑 Co-authors' patterns, every sentence, and the easier-to-read check (JL 261110)

JL 261110: "will you add it and update it to the /haipipe-paper?"; "ask the agent to read each sentences to see
whether it is easier to understand". When co-authors return a round (a Word file pulled by `word_round.py pull`,
their comments, a meeting), the paper keeps what they want and checks every sentence against it:

1. **The patterns live on the Board**: `<Board>/writing-patterns.md`, numbered `### N. <pattern>` with their own
   words, our sentence, theirs, the fix and its support; the Writing view shows it as "Writing patterns to avoid".
   The generic tells are `haipipe-draft-review` `ref/ai-tells.md` § 5; this file holds the paper's own.
2. **Their text is theirs**: a sentence that carries a co-author's tracked insertion is never rewritten; it gets a
   Review card with a suggestion. Their own sentences keep their register (a semicolon included); our rewrites still
   follow the house rules: no semicolons, no transition set off by commas, no longer than the original. Run
   `haipipe-draft-review` `cli/anti_slop.py audit` on the rewrites, before the easier-to-read check (JL 261110:
   the first round's kept rewrites scored worse than the originals on it, 26 against 19, and ran 9% longer).
3. **Every paragraph, then every sentence, is reviewed** (JL 261115: "review the paragraph level logics, to check
   whether the logic is correct or not"). First one blind reviewer per Section reads each paragraph as an argument
   (`haipipe-draft-review` `ref/paragraph-logic.md`: order with no A-B-A return, every conclusion resting on named
   sentences, no claim wider than its findings, no missing step); a move or a missing step is a Section question the
   person signs before any sentence changes. Then one blind reviewer per Section (never the writer), reading the round's newest
   text, scores each sentence 1 to 10 against `ai-tells.md` § 5, the Board's patterns and the comments in that
   Section; under 8 gets a rewrite that keeps every number, citation and claim. A round is a Job on the Board, not a
   `reports/` folder (JL 261110: "we will no long using the reports/ plesae use the job or studio"):
   `jNN_review_<who>_v<MMDD>/` (face `for: <writing Job>`), its Tasks `t01_sentence_review` (the comments as
   received in `result/feedback/`, the reviews in `result/review/review-<section>.md`), `t02_readability_check`,
   `t03_paragraph_logic` (`result/logic-<section>.md`, run before the sentence review although numbered after it,
   since it was added later) and `t04_tracked_word` (a round made before 261115 may hold it as `t03_tracked_word`). A Job named with "review" is never read as a writing version.
4. **The easier-to-read check**: before a rewrite becomes a Revise card's default, a fresh reader (not the
   reviewer, not the writer) reads it in place: the sentence before, then the original and the rewrite in random
   order as A and B, then the sentence after. It answers two questions per pair: which one is easier to
   understand on a first read, and do both say the same thing (numbers, citations, claim strength). A rewrite
   that is not easier, or that changes the meaning, is not proposed as written: it goes back to the reviewer, or the
   original stays. The pairs, the readers' verdicts, the key and the unblinded verdict per sentence are
   `t02_readability_check`'s Result.
5. **Back to the co-authors as tracked changes**: accepted cards are adopted into the Section, and the same edits
   go onto a copy of the co-authors' own latest file as tracked changes by the person who answers them
   (`excalidraw-draft/ref/track_changes.py` `write_tracked`): their comments and tracked changes stay. The edits are
   `t04_tracked_word/scripts/edits.yaml` (find, new, why), its Run writes `delivery/<writing Job>/word-tracked/`, the
   send's third paper beside the PDF and the Word file (JL 261110: "the Word-Change-Track, which is based on the
   previous change tracks from professors and you add the changes as well"). It is written locally;
   `word_round.py push` sends it only on the person's word.
