# A01 · The AI proposes, accepts and reviews; the person answers AI comments

> "for in the hai-paper-draft workflow, for the editing, if they are sure, they can just go ahead to accept the editing you proposed, if not sure, they leave the comments, at the end, we hope that we will have the things like AI comments for me to reply, for the editing, you propose, you accept, and you review." (JL 261118, chat, ScalingGlucose t02_results)

## 1. Need
JL wants the Section workflow to end with only the AI's questions for him. Every edit the AI is sure of is proposed, accepted and reviewed by the AI. He replies to AI comments and nothing else.

## 2. Now
ref/workflow.md W4 step 3 said "Only a sentence still under 8 gets an AI comment", so every leftover sentence became a question. section_workflow.py counted W4 done only when `under 8 <= open AI comments`. On t02 v1.22 that was 43 under 8 and 5 comments, so the honest end would be about 40 wording questions for JL. Older Passes also kept Edit cards `State: proposed` that waited for him (t02 revise record: one still proposed).

## 3. Gap
No way existed to record "the AI is sure and settled this", so a wording-only leftover had two exits: a comment to JL, or W4 never closing.

## 4. Methods
1. Comment every leftover: rejected, it hands JL the AI's work.
2. Lower the pass mark to 7: rejected, it hides real problems and changes the raters' scale.
3. An `AI decided:` mark on the Pass line for what the AI is sure of, a comment only when not sure, and no proposed card: chosen. The decision and its reason stay on disk and show in the record.

## 5. Update
- ref/workflow.md: W4 step 3 (sure or comment), step 5 (fact fixes by the same test), the table row, and W5 (only AI comments to reply).
- ref/section-method.md: D2 ends with the AI deciding every card, and D3 is for the AI's not-sure items only.
- cli/section_workflow.py: `w4_counts()` counts open, AI-decided and proposed; W4 waits on proposed cards.
- tests/test_w4_decides.py: 2 passed.
- SKILL.md: points at CONSTITUTION.md.
- Cases: ✅ t02_results v1.22, Pass 11: 33 AI decided, 7 asked in Comments 21 to 25, W4 ✅. ✅ Every other Section uses the same workflow file and status script.
- Run: `python3 -m pytest -q tests/test_w4_decides.py` → 2 passed. `section_workflow.py` on t02: "W4 0 under 8 open, 40 settled, 5 open AI comments".

## 6. Never again
W4 cannot show ✅ while a card waits on the person or a sentence under 8 is neither decided nor asked. The decision is written beside the score, so the next session sees it and does not reopen it. The test is rerun by `/hai-stack sweep`.
