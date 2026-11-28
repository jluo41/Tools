# hai-paper-draft · Constitution

JL's feedback on paper Sections and their workflow, kept verbatim. It wins over SKILL.md; where they disagree, follow this file.


## A01 · The AI proposes, accepts and reviews; the person answers AI comments

> "for in the hai-paper-draft workflow, for the editing, if they are sure, they can just go ahead to accept the editing you proposed, if not sure, they leave the comments, at the end, we hope that we will have the things like AI comments for me to reply, for the editing, you propose, you accept, and you review." (JL 261118, chat, ScalingGlucose t02_results)

**Rule:** In W4 the AI settles every sentence still under 8 itself: when sure it keeps or applies the edit and writes `AI decided: <what and why>` on the sentence's Pass line; when not sure it writes one AI comment; no edit card is left `State: proposed` for the person.
**Why:** On t02 after two W4 rounds, 43 sentences stayed under 8 with only 5 AI comments; the old W4 rule asked for a comment on every one, which would hand JL about 40 wording questions, and older Passes still left cards proposed for him.
**Class:** an edit the AI could decide itself that is left waiting on the person, as a proposed card or a comment on wording.
**Cases:** ✅ ref/workflow.md W4 steps 3 and 5, its table row and W5 · ✅ ref/section-method.md D2 and D3 · ✅ cli/section_workflow.py W4 counts `AI decided:` and proposed cards (`w4_counts`) · ✅ tests/test_w4_decides.py · ✅ ScalingGlucose t02_results v1.22: 33 sentences AI decided, 7 asked in Comments 21 to 25, W4 ✅ · ✅ every other Section (ScalingGlucose t01, t03, t04, Appendix; AgreeableJama, LLMRec, PhyAbsence, CmsAiUse, AgreeableRx) reads the same ref/workflow.md and section_workflow.py, so W4 stays open for them until each leftover is settled · ✅ a sentence asked in a comment counts as settled (`asked in Comment N`)
**Check:** `section_workflow.py` leaves W4 open while a sentence under 8 has neither `AI decided:` nor an open AI comment, or a card is `State: proposed`.
**Run:** `cd plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-draft && python3 -m pytest -q tests/test_w4_decides.py`
**Status:** solved 261118
**Solved by:** `cli/section_workflow.py`: w4_counts; `ref/workflow.md`: W4 sure or comment
**Report:** constitution/A01-ai-decides-person-answers.md


## A02 · Titles and paragraphs are rated and settled like sentences

> "for the section name, it should be trated as the setneces bricks as well, we should also need to evaluat ehem as well." (JL 261118, Draft Lab t02_results, a screenshot of "C4 · No way of scaling helps every task")
> "I feel the whole paragraph is not close related to the C4's section name. The paragraph should support the section name, right? Chekc the paragraph logic again. I find you didn't do the paragraph level evaluation." (JL 261118, Draft Lab t02 Comment 29)

**Rule:** Every part title (C<n>), paragraph title (C<n>.P<m>) and paragraph (with a `fit` check: it supports its paragraph and part title) is rated in W3 of every round by a fresh blind title rater and settled in W4 like a sentence (rewrite, blind A/B, `AI decided:` or `asked in Comment <n>`), with a `Titles:` and a `Paragraphs:` line per unit in the Pass.
**Why:** W3 rated sentences and paragraphs only; titles were reviewed once by hand (r16, v1.19) and then changed without a score, so the page showed a ★ on every sentence and none on its heading.
**Class:** a reader-facing unit of the Section (a title, a heading, a paragraph) that the current round's rating does not score.
**Cases:** ✅ ref/workflow.md W3 Pass shape with `Titles:` · ✅ cli/section_workflow.py W3 needs a title line for every C<n> and C<n>.P<m>, W4 counts low titles · ✅ tests/test_w4_decides.py test_titles · ✅ ScalingGlucose t02 v1.22: 21 titles (r22, A/B r18_t02_titles_ab, C3.P7 renamed) and 14 paragraphs (r06 with fit) rated and settled in Pass 11 · ✅ Draft Lab shows ★ on part and paragraph headings (WorkBench-Paper-UI draft_step_titles.py, 261118) · ✅ W3 fails while a paragraph of the current version has no `Paragraphs:` line · ✅ every other Section: the same W3 check now fails until its titles are rated
**Check:** `section_workflow.py` W3 shows "N titles unrated" and stays ⬜ until each title has a `Titles:` line; W4 stays open while a title under 8 is unsettled.
**Run:** `cd plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-draft && python3 -m pytest -q tests/test_w4_decides.py`
**Status:** solved 261118
**Solved by:** `cli/section_workflow.py`: titles_in, title_counts, paragraph_counts; `ref/workflow.md`: Titles block
**Report:** constitution/A02-titles-rated-like-sentences.md


## A03 · An AI comment brings its proposed edit, in bullet points

> "for this, if you have the comments, please also leave the proposed solution, right? like what is the proposed editng card." (JL 261118, Draft Lab t02, the AI comment on C5.P10.s48)
> "I want to make this to be more readable, with the bullet points, currently it is very ahrd to read." (JL 261118, same screen)
> "Please propose the new editing card." (JL 261118, t02 Comment 22)

**Rule:** Every AI comment comes with an `### Edit` card in the newest Pass that carries `Answers: Comment <n>` and its options (A the AI's pick, B the other or Keep), and its note is a one-line headline followed by numbered lines: 1. Problem, 2. Proposed (the card's name), 3. Your call.
**Why:** The AI comments on t02 (21 to 25) were one long paragraph each and named a rewrite inside the prose, with no card to accept, so JL had to read a wall of text and could not act on it.
**Class:** an AI question to the person that carries no ready edit or is not scannable.
**Cases:** ✅ ref/workflow.md W4 step 3 (comment with card, bullets) · ✅ cli/section_workflow.py: W4 stays open while an open AI comment has no answering card (`ai_comments_without_card`), and a proposed card that answers a comment may wait · ✅ t02 Comments 21, 23, 24, 25 rewritten, 30 and 31 new, each with its card · ✅ t02 person Comments 22, 28, 29 answered with cards · ✅ Draft Lab shows a note's numbered lines as a list and the ↳ link opens the answering card (WorkBench-Paper-UI, checked on t02 261118) · ✅ Draft Lab shows each paragraph's own ¶★ beside its title ★
**Check:** `section_workflow.py` W4 names any open AI comment with no proposed card.
**Run:** `cd plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-draft && python3 -m pytest -q tests/test_w4_decides.py`
**Status:** solved 261118
**Solved by:** `cli/section_workflow.py`: ai_comments_without_card; `ref/workflow.md`: comment format
**Report:** constitution/A03-ai-comment-brings-its-edit.md


## A04 · Grammar is read before the person reads

> "can you check this problem? the writing grammar error." (JL 261118, a screenshot of the ScalingGlucose Methods page in Word with grammar underlines)
> "what was the issue, could you list the resaons for it? and could we avoid that in the future." (JL 261118, chat, /hai-stack)

**Rule:** Every Section's W4 fixes every `hai-draft-review/cli/grammar.py` finding (e-notation, opening-comma, label-noun) and every `grammar:` problem the sentence reader names; a grammar error caps read at 6, and `section_workflow.py` keeps W4 open while any machine finding is left.
**Why:** ScalingGlucose Methods went through 13 W4 rounds rating logic, read and ai; no step read grammar, so "1e-3", "the selection patients" and 16 missing opening commas reached Word, whose underline was the first grammar reader. Two raters saw "selection patients" (t04 revise.md lines 963, 1820) and wrote `Fix: none`.
**Class:** a grammar error in a paper sentence that no step of the draft loop reads, so the person finds it first.
**Cases:** ✅ ScalingGlucose t04_methods v1.18 (17 fixed earlier, s31 s164 s171 now) · ✅ ScalingGlucose t00 t01 t02 t03 t21 (0 findings) · ✅ cli/grammar.py · ✅ cli/section_workflow.py W4 · ✅ ref/workflow.md W4 step 0 · ✅ hai-draft-review ref/sentence-logic.md check 7 · ✅ ref/plain-rules.md comma note · ✅ tests/test_grammar.py · ⬜ 17 Sections in other Boards with 1 or 2 opening-comma findings, fixed by their own sessions at their next W4 (Physician: AgreeablePrescriptionDiscretion t01 t25, AgreeableOpioid-Jama t03, PersonalityPDMPMandate t00 t03 t04 t21, CMS-AI-Usage t03, LLMRecPhy-Misq t04, LLMRecPhy-Jama t21 x2; REACH and WellDoc: Grant-AITC-Dementia t04 t05; WellDoc: CGMtoHbA1c Appendix B; DrFirst: TestToLearn t03; jluo41-repo: Dissertation t06)
**Check:** grammar.py names the six sentences JL saw in Word and passes their fixed forms; W4 is ⬜ while a draft has a finding.
**Run:** `cd plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-draft && python3 -m pytest -q tests/test_grammar.py tests/test_w4_decides.py`
**Status:** open (17 Sections in other Boards wait for their W4)
**Solved by:** `hai-draft-review/cli/grammar.py`: new check; `cli/section_workflow.py`: W4 needs zero findings
**Report:** constitution/A04-grammar-read-before-the-person.md
