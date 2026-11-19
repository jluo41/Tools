# Draft skills

How the draft skills work, not a part of a page: haipipe-draft, haipipe-draft-review, haipipe-draft-writing,
haipipe-paper-draft. Each topic below is one rule or tool, with its requests.

## 🔁 Topic: Section method ▸ Paragraph rewrite

A paragraph with three or more weak sentences, or one that reads patched, is rewritten whole, rated by two fresh
readers, compared blind with the old one; it loops until it holds at 7 to 8. Rule: haipipe-paper-draft
`ref/section-method.md` D2, must-check M-E10.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | "rewrite them, and reviewing them and updating them"; scores "around 7 and 8" | ScalingGlucose t01 | the rule written into section-method.md D2 and M-E10; Blind A/B ▸ Paragraph pairs and Draft Lab ▸ Paragraph before/after not built yet |

## 🧰 Topic: haipipe-draft ▸ its functions

The verbs a session calls. Proposed: check-examples, eval-structure, eval-paragraph (holds paragraph logic),
eval-sentence (holds sentence logic), eval-evidence; rewrite-sentence, rewrite-paragraph; blind-ab.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | "I think we should have check-examples, eval-structure, eval-logics, eval-paragraph, and eval-sentence, and rewrite-sentence, rewrite-paragraph, eval-evidence, etc, How do you think about it." | JL directly | proposed, logic folded into eval-paragraph and eval-sentence; waits for JL |

## 📏 Topic: Rating standard ▸ which rules a Pass was rated under

A rule file changed mid-day (sentence-logic.md 18:45, section-method.md 19:13, revise.md 17:57) and a Section
session kept rating under the morning's rules, with nothing to tell it.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | document each skill's ref files so a Section session can tell when the rating standard changed | AITC-LOI t01 | proposed: a `Standard:` line on every review Pass (rule files and their dates), and a check that says "rated under an older standard: rate again"; waits for JL |

## 🔁 Topic: Section workflow ▸ Auto draft loop

A new Section runs step by step to a draft close to review: plan, examples, write, rate, a fix loop the AI accepts
itself when the blind A/B reader keeps a rewrite, a stop after two rounds with nothing kept, comments where it is
not sure; then the person joins. Each step one command and one Run; the page reads where it stands from those Runs.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-16 | "I want to have a /haipipe-paper-draft workflow, so when I open a new secton draft, then I can run the tasks one by one and get a close to review draft" | JL directly | proposed W1 plan, W2 check-examples, W3 write, W4 rate, W5 fix loop |
| 11-16 | "the editing should be accept by AI themselves, after several rounds of no imrpovements, or something not sure, the AI will leave the comments, and human will join" | JL directly | proposed: blind A/B keeps decide the wording, two rounds with nothing kept stop the loop, unsure items become comments; a 🤖 mark on each AI-changed sentence (Draft Lab ▸ Marks) |
| 11-16 | "for the Draft Lab Workflow, could we use it and does it work now?" | JL directly | written: haipipe-paper-draft `ref/workflow.md` (W0 to W5) and `cli/section_workflow.py` (where a Section stands, the next step); not yet: a Run per step, the 🤖 mark, the step line on the page, the installed agents |
| 11-18 | W5 showed ⬜ though the PDF was current; a re-rate passed four of six dropped rewrites, so re-rate before commenting | ScalingGlucose t03_discussion | `section_workflow.py` W5 finds the PDF under `latex/` and prints what it saw; `ref/workflow.md` W4 step 3: rate once more before an AI comment |
| 11-18 | a Pass without the report heading showed ✅ in the step check and no ★ on the page; health passed while the page showed 📊❗; the writer added "we found that" | ScalingGlucose t02_results | `section_workflow.py` needs the `### Revise review report` heading; `ref/workflow.md` W3 Pass shape and W4 writer rule; health row `evidence-files` runs the page's resolver (`src/evidence_resolve.py`) |
| 11-18 | renumber left "s152-cut" in spans; a fact fixed after scoring still counted under 8; the loop circled back to replaced text | ScalingGlucose t04_methods | `src/page_ranges.py` RANGE replaces a whole broken span (test added); `ref/workflow.md` W4: fact fixes get a comment, a stop when the loop circles, paragraph round first |
| 11-18 | the step check read Pass 6 when Pass 7 sat above it; W3 counted the title paragraph C1.P0 as unrated | ScalingGlucose t00_abstract | `section_workflow.py` `newest_pass` takes the highest Pass number, as the page does; a P0 title paragraph needs no `Paragraphs:` line (tests in `tests/test_w4_decides.py`; `ref/workflow.md` W3) |
