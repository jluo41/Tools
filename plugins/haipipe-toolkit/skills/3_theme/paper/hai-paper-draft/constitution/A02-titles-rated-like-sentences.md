# A02 · Titles and paragraphs are rated and settled like sentences

> "for the section name, it should be trated as the setneces bricks as well, we should also need to evaluat ehem as well." (JL 261118, Draft Lab t02_results)
> "I feel the whole paragraph is not close related to the C4's section name. The paragraph should support the section name, right? Chekc the paragraph logic again. I find you didn't do the paragraph level evaluation." (JL 261118, t02 Comment 29)

## 1. Need
JL reads part titles, paragraph titles and paragraphs on the page as bricks, like sentences. Each one needs a score, a reason, and a decision, and a paragraph must support the titles above it.

## 2. Now
W3 in ref/workflow.md rated sentences, and paragraphs once (r05 on v1.20). Titles were reviewed by hand once (r16 on v1.19). section_workflow.py checked only sentence lines. Pass 11 on t02 v1.22 had no title lines and no paragraph lines, and the page showed ★ on sentences only.

## 3. Gap
No step required titles or paragraphs to be rated on the current version, and no check failed when they were not. Paragraph logic also had no check for whether a paragraph supports its part title.

## 4. Methods
1. Rate titles once at the start: rejected, because titles and paragraphs change in every round.
2. Make W3 require a `Titles:` and a `Paragraphs:` line for every unit of the current version, and have W4 settle them like sentences: chosen.
3. Page: a ★ on each heading (draft_step_titles.py, by WorkBench-Paper-UI).

## 5. Update
- ref/workflow.md: the Pass shape now has `Titles:` lines, plus a W3 note.
- cli/section_workflow.py: titles_in, title_counts and paragraph_counts. W3 lists any unrated title or paragraph, and W4 counts the low ones.
- tests/test_w4_decides.py: 5 passed.
- t02 v1.22, Pass 11:
  - 21 titles rated (r22), a blind A/B (r18_t02_titles_ab) renamed C3.P7, and 6 kept by the AI.
  - 14 paragraphs rated with a `fit` check (r06). s45 fixed, 6 kept, and 6 asked in Comments 21, 22, 25, 29, 30 and 31, each with a card.
- Draft Lab: a heading ★, by WorkBench-Paper-UI.

## 6. Never again
W3 shows ⬜ with "N titles or paragraphs unrated" until each unit of the current Draft is rated, so a round cannot skip them. Paragraph ratings check that each paragraph supports its titles (`fit`). `/hai-stack sweep` reruns the tests.
