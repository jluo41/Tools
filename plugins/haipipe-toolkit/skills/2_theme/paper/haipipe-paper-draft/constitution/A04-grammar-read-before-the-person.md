# A04 · Grammar is read before the person reads

> "can you check this problem? the writing grammar error." (JL 261118, the ScalingGlucose Methods page in Word)
> "what was the issue, could you list the resaons for it? and could we avoid that in the future." (JL 261118, chat)

## 1. Need
JL opens the Word copy of a paper and sees no grammar underline: every grammar error is found and fixed by the
draft loop before the person reads.

## 2. Now
The W3 reader gives each sentence logic, read and ai scores (haipipe-draft-review `ref/sentence-logic.md`, checks 1
to 6); none of the six checks is grammar. `section_workflow.py` W4 counted only scores under 8, AI decisions and cards.
ScalingGlucose Methods ran 13 W4 rounds (draft v1.18 state line) and still carried, in v1.17:
"a learning rate of 1e-3" (s103, and "8.0e-4" in s35), "Each share MLP" (s94), "the selection patients" (s104),
"the fitting rows" (s105), and opening phrases with no comma ("For all three traits we report", s102; s25, s59,
s101, s119 to s123, s31, s164, s171). Word underlined them; Word was the first grammar reader.

## 3. Gap
1. No grammar check: `ref/sentence-logic.md` scored logic, read, ai only; raters saw "selection patients" twice
   (t04 revise.md lines 963 and 1820) and still wrote `Fix: none`, since the term was "used before defined", not wrong.
2. Code habits copied into prose: "1e-3" came from the run configs and stayed in every rewrite option
   (revise.md lines 681 to 683, 1430 to 1431); no rule said a number in prose is a decimal.
3. Script labels as nouns: "share MLP", "selection patients", "fitting rows" are names in our scripts and Runs;
   the plain-words rules push short phrases, which favours such noun stacks.
4. Comma rules read too wide: "no comma insertions" (memory 261116) and "no transition set off by commas"
   (`ref/plain-rules.md` line 79) made writers drop the comma after an opening phrase too (v1.15 note: a rewrite
   was dropped by hand because it "put a phrase between commas").
5. PDF first: while drafting, no Word was built (memory 261116), so no grammar checker ran until JL opened Word.

## 4. Methods
1. Fix only the sentences JL saw: rejected, the next Section brings them back.
2. Ask the reader to read grammar (sentence-logic check 7) and cap read at 6: needed, but a reader missed
   these 13 times, so alone it does not hold.
3. A machine check for what a pattern can see (`cli/grammar.py`), wired into W4 so the loop cannot close: chosen,
   together with 2. It reads every sentence row of every draft; math and code are skipped.

## 5. Update
- `haipipe-draft-review/cli/grammar.py` (new): e-notation, opening-comma, label-noun findings
- `haipipe-paper-draft/cli/section_workflow.py`: W4 open while grammar findings remain
- `haipipe-paper-draft/ref/workflow.md`: W4 step 0, grammar first
- `haipipe-draft-review/ref/sentence-logic.md`: check 7 Grammar, caps read at 6
- `haipipe-draft-review/ref/plain-rules.md`: the opening comma stays
- `haipipe-paper-draft/tests/test_grammar.py` (new): JL's six sentences, bad and fixed

Cases: ✅ ScalingGlucose t04 (v1.17: 13 findings, v1.18 now 0; adopted, exported, `health --final` passes 182 of 182)
· ✅ ScalingGlucose t00 t01 t02 t03 t21 (0) · ⬜ 17 Sections in other Boards with 1 or 2 opening-comma findings,
listed in the article; their sessions see W4 ⬜ and fix them.

Run: `python3 -m pytest -q tests/test_grammar.py tests/test_w4_decides.py` → `8 passed`.
Sweep over every paper Section in every SPACE: `python3 1_base/draft/haipipe-draft-review/cli/grammar.py <draft>...`.

## 6. Never again
The writer can still make these errors, but the loop can no longer close on them: W4 stays ⬜ while grammar.py
names anything, and the reader must cap read at 6 for a grammar error it sees. The test keeps the six Word sentences
as fixed cases, so a change to grammar.py that stops catching them fails. `/haistack sweep` reruns the Run line.
What a pattern cannot see (a wrong article, a dangling modifier) still rests on the reader's check 7.
