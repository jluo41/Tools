# The Section workflow · W0 to W5, from an empty Section to a draft ready for the person

JL 261116: "I want to have a /haipipe-paper-draft workflow, so when I open a new secton draft, then I can run the tasks
one by one and get a close to review draft"; "the editing should be accept by AI themselves, after several rounds of no
imrpovements, or something not sure, the AI will leave the comments, and human will join".

The same method as [`section-method.md`](section-method.md) (S1 to S3, D1 to D3), put in order as six steps. Each step
is judged from a file, never from memory: `cli/section_workflow.py <Section Task>` prints the six lines and the next step.

```text
W0 examples ─▶ W1 plan 🙋 sign ─▶ W2 write ─▶ W3 rate ─▶ W4 fix ─┐
                                                ▲                 │ something kept
                                                └─────────────────┘
                                     two rounds kept nothing, or all 8+ ─▶ W5 ready 🙋
```

| Step | Who | Done when (read from disk) |
| --- | --- | --- |
| W0 Examples | the session (SKILL.md § Examples first) | the face's `examples:` names a topic with section screenshots, or says `none · <reason>` |
| W1 Plan | the session proposes, **the person signs** | the newest Draft's `approved:` holds ✅ (`page.py sign`) |
| W2 Write | haipipe-draft-writing | the Draft text has a sentence for every Structure Bullet; then `page.py adopt` and `export` |
| W3 Rate | fresh agents: `haipipe-draft-eval-paragraph-agent`, `haipipe-draft-eval-sentence-agent` | the revise record's newest Pass with a review report rated the newest Draft version |
| W4 Fix loop | writer, then `haipipe-draft-ab-reader-agent`; the AI decides | every sentence 8 or more, or settled: `AI decided:` on its Pass line (sure) or an open AI comment (not sure); no card `State: proposed` |
| W5 Ready | the session builds; **the person joins** | the Section's newest PDF under `delivery/<job>/<task>/` (its `latex/`) is newer than the Draft |

## W3, the shape of a Pass

The page reads ★ only from a report card, so each Pass in `draft/records/<stem>-revise.md` is written as:

```text
## Pass N · <YYYY-MM-DD> · on draft v<X>
### Revise review report
Reviewer: <the agents, fresh>
Standard: <rule files and their dates>
Titles:
- C<n> · title 8/10 · register 8 · first-read 8 · names 8 · <why> · Fix: none | <new title>
- C<n>.P<m> · title 7/10 · register 8 · first-read 7 · names 7 · <why> · Fix: <new title>
Sentences:
- C<n>.P<m>.S<k> · logic 8/10 · read 7/10 · ai 8/10 · <why>
```

**Titles are rated like sentences** (CONSTITUTION A02, JL 261118: "for the section name, it should be trated as the
setneces bricks as well, we should also need to evaluat ehem as well"). Every part title (`C<n>`, the Structure
Overview) and every paragraph title (`C<n>.P<m>`) gets a `Titles:` line from a fresh blind title rater (SKILL.md
§ Titles read like the text): register, first read, names what its sentences show; the score is the lowest. W4 settles
a title under 8 the same way as a sentence (a rewrite, blind A/B, `AI decided:` or `asked in Comment <n>`), and a new
title goes to the Structure Overview, § 1 and § 3 headings in one edit.

W4 adds `AI decided: <why>` or `asked in Comment <n>` to a sentence's or a title's line before its ` · Fix:` part: the page reads
whatever follows "Fix:" as a suggested rewrite.

`cli/section_workflow.py` counts a Pass as rated only with that heading, as the page does (ScalingGlucose t02_results
261118: a Pass without it showed ✅ here and no ★ on the page).
The newest Pass is the one with the highest number, wherever it sits in the file, as the page reads it
(t00_abstract 261118). Every paragraph `C<n>.P<m>` gets a `Paragraphs:` line except a P0 title paragraph: its one
sentence is a title, rated by its `Titles:` line.

## W4, the loop

0. **Grammar first** (CONSTITUTION A04, JL 261118). Run `haipipe-draft-review/cli/grammar.py <draft>` and fix every
   finding in the Draft text before the rewrites; `section_workflow.py` keeps W4 open while any is left. A grammar fix
   is a fix, not a rewrite: it needs no blind A/B and changes no meaning.
1. Each sentence under 8 gets a rewrite; a paragraph with three or more under 8 is rewritten whole (section-method D2).
   The writer keeps a results sentence's measured factor as its subject ("Error fell with scale") and never adds
   "we found that", "we saw" or "we observed": the next rater scores those ai 6 (t02_results 261118).
2. A fresh blind A/B reader judges each pair. "Easier, same meaning" is kept, and the AI writes it into the next Draft
   version itself: no card waits for the person. Anything else is dropped.
3. **The AI proposes, accepts and reviews; the person only answers comments** (CONSTITUTION A01, JL 261118: "if they
   are sure, they can just go ahead to accept the editing you proposed, if not sure, they leave the comments"). A
   sentence with no fix, or whose fix was dropped, is first rated once more by W3 on the next version: the readers'
   flags vary from round to round, and one that now scores 8 or more needs nothing (ScalingGlucose t03 Pass 6). For
   each sentence still under 8 the AI settles it one of two ways:
   - **sure**: the problem is wording only and two rounds found no easier version, or the AI's own fix is plainly
     right (a scope word, an error-not-outcome word, an interval read from the Run): the AI keeps or applies it and
     writes `AI decided: <what and why, 15 words or fewer>` at the end of that sentence's line in the Pass;
   - **not sure**: a claim, a missing fact, a story choice, a term the whole paper shares, or a rewrite the A/B reader
     marked "meaning: no": one AI comment in `draft/records/<stem>-comments.md` about that sentence only
     (section-method D3), and `asked in Comment <n>` on its Pass line. The comment brings its proposed edit
     (CONSTITUTION A03): an `### Edit` card in the newest Pass with `Answers: Comment <n>`, Option A (the AI's pick)
     and Option B (the other, or Keep), `State: proposed`; and its note is a headline then numbered lines:

     ```text
     - Note · <time> · AI: s48 is hard to read.
       1. Problem: two matches and two sets of brackets in one sentence (rated 6).
       2. Proposed: card "Edit · s48 · split the two matches", Option A.
       3. Your call: split it in two?
     ```
   No Edit card is left `State: proposed` for the person: the AI decides each card itself (written or rejected).
4. W3 rates again. Stop when every sentence is 8 or more, after two rounds in a row that kept nothing, or when the
   blind reader keeps a rewrite equal to text an earlier round replaced (the loop is going in circles; t04_methods
   261118).
5. A fact a reader caught (a wrong direction, a wrong number) and fixed after scoring is settled by the same test:
   the AI is sure when the Run file shows it (then `AI decided:` names the file); otherwise it is an AI comment so the
   person confirms it (t04_methods s49).
6. Order that worked on t04_methods: a paragraph round first (each weak paragraph rewritten whole, its numbers,
   cites and $math$ checked equal by script, blind A/B on whole paragraphs), then sentence rounds.
7. Never touched: a sentence the person checked (✓), a claim, a number, a story choice (a fact fix under 5 is the
   one exception, settled by its own test there).

## What the person sees at W5

Only the AI comments to reply to (JL 261118: "at the end, we hope that we will have the things like AI comments for me
to reply"): the AI proposed, accepted and reviewed every other edit. The open AI comments first, then each sentence the loop changed (its 🕘 history shows old and new), then a ✓ per
sentence (D4, D5). Each Pass of W3 writes a `Standard:` line naming the rule files it rated under and their dates.

## Not built yet

One Run per step (`runs/rNN_wN_<slug>/`), the 🤖 mark on AI-changed sentences, and the step line in Draft Lab. Until
then the step state comes from `cli/section_workflow.py`.
