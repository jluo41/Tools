# A03 · An AI comment brings its proposed edit, in bullet points

> "for this, if you have the comments, please also leave the proposed solution, right? like what is the proposed editng card." · "I want to make this to be more readable, with the bullet points, currently it is very ahrd to read." (JL 261118, Draft Lab t02, the AI comment on C5.P10.s48)

## 1. Need
JL reads an AI comment and acts on it at once. The comment should give the problem, the proposed edit as a card he can accept, and one question, in short numbered lines.

## 2. Now
AI comments were one `- Note · … · AI: …` line, often 60 words, with the rewrite hidden in the prose. No card answered them. The page parser (page/element_marks/item_cards.py:71) reads only that one line.

## 3. Gap
The workflow (W4 step 3) asked only for "one plain question". Nothing required a card or a format, and nothing failed when they were missing.

## 4. Methods
1. A shorter prose question: rejected, because JL still has to write the edit himself.
2. A comment plus an `### Edit` card that carries `Answers: Comment N`, and a note in numbered lines: chosen. The page already links answering cards (↳).
3. Page: show the numbered lines as a list and open the card inline (WorkBench-Paper-UI, asked).

## 5. Update
- ref/workflow.md: W4 step 3 gives the format and an example.
- cli/section_workflow.py: `ai_comments_without_card` keeps W4 open while an AI comment has no card. A proposed card that answers a comment may wait.
- tests/test_w4_decides.py: 5 passed.
- t02 comments and cards:
  - Comments 21, 23, 24 and 25 rewritten in numbered lines, each with a card.
  - Comments 30 and 31 added, with cards.
  - JL's Comments 22, 28 and 29 answered, with cards.
- Page (WorkBench-Paper-UI): numbered note lines show as a list, the ↳ link opens the card, and checked on t02 (Comment 24 shows Problem, Proposed, Your call and its card).

## 6. Never again
W4 cannot show ✅ while an AI comment has no proposed card, and every AI comment the workflow writes follows the example in ref/workflow.md.
