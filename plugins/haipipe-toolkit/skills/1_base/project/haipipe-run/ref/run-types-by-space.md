# Run types by Space · every button of the frame and its skill

Read when a workbench button starts work, when a theme adds a button, or when you need
the Run a button makes and the skill that owns it. Each Run button of the base frame
(`servers/workbench/frame.py`: `vanilla()` for Block, Job and Task, `page_task_spaces()`
for a Page Task) names its skill in a `skills:` field on its run type, as the Page's run
cards (`run-cards.md`) already do (b03 s21, 261007). This table is the same list in words.

Rules:

1. **One skill per button**: the button's `skills:` names it; the agent loads it first.
2. **The level's skill**: Update the description, Add a Job or Task, and Build the delivery
   belong to the level they sit on (`haipipe-board` · `haipipe-job` · `haipipe-task`).
3. **The shared Spaces**: Idea Studio is `haipipe-studio`, Audience Report is
   `haipipe-question` (asking) and `haipipe-report` (the rest), Runs is `haipipe-run`.
4. **Soft Run names**: `run-<type>-<target>`, no date; a new round is a pass
   (`passes/pNN-<MMDD>/`). `scripts/soft_run.py` writes the card.
5. **A theme's button** names its own skill the same way; a theme that keeps a vanilla
   button keeps its skill.
6. **A button is named by its Run** (JL 261007: "for all the soft run, the name of them will be
   run-xxxx-xxx"): the Runs panel shows `run-<type>-<target>` as the button's name, what it does
   in small under it. A target the open folder fixes is filled in (`run-face-b03`,
   `run-build-t02`); one still to choose stays a placeholder (`run-draw-<sNN>`, `run-ask-<qNN>`).
   Buttons that make the same Run are one button: Idea Studio's add, redraw and save-a-session
   are all `run-draw-<sNN>`, a new topic a new Run, the rest its passes. Its cards are its Runs,
   one per topic, each with its passes (and older `chat/` sessions until they move into passes).
   A hard Run keeps its own name (`rNN_<slug>`). The panel code: `frame.run_type(name, doing, ...)`.

## Block · Job · Task

The button's name is the Run column; "what it does" is the small line under it.

| Space | What it does | Skill | Run (the button's name) | Levels |
|---|---|---|---|---|
| Description | Update the description | `haipipe-board` | `run-face-<bNN>` | Block |
| Description | Update the description | `haipipe-job` | `run-face-<jNN>` | Job |
| Description | Update the description | `haipipe-task` | `run-face-<tNN>` | Task · Page Task |
| Idea Studio | add a topic · redraw it · save this session, each a pass | `haipipe-studio` | `run-draw-<sNN>` (one button) | every level |
| Audience Report | Ask a Question | `haipipe-question` | `run-ask-<qNN>` | every level (a Page Task: Ask a question) |
| Audience Report | Write the report | `haipipe-report` | `run-report-<qNN>` | every level |
| Audience Report | Rebuild report drawing | `haipipe-report` | `run-figures-<qNN>` | Block · Job · Task |
| Audience Report | Check a report | `haipipe-report` | `run-check-<qNN>` | Block · Job · Task |
| Work Details | Add a Job | `haipipe-board` | `run-add-<jNN>` | Block |
| Work Details | Add a Task | `haipipe-job` | `run-add-<tNN>` | Job |
| Work Details | Build the Task | `haipipe-task` | `run-build-<tNN>` | Task |
| Runs | Run | `haipipe-run` | `run-<type>-<target>` or `rNN_<slug>` | every level (hard Runs in a work Task only) |
| Delivery | Build the delivery | `haipipe-board` | `run-delivery-<target>` | Block |
| Delivery | Build the delivery | `haipipe-job` | `run-delivery-<target>` | Job |
| Delivery | Build the delivery | `haipipe-task` | `run-delivery-<target>` | Task |

## Page Task (its own views; skills from the Page's run cards)

| Space | What it does (the card) | Skill | Run (the button's name) | Opens in |
|---|---|---|---|---|
| Work Details | Scratch | `haipipe-page-scratch` | `run-scratch-<target>` | Draft-Scratch |
| Work Details | Structure revise | `haipipe-page-structure` | `run-structure-<slug>` | Draft-Scratch |
| Work Details | Evidence embed | `haipipe-page-evidence` | `run-<value\|display\|citation>-<slug>` | Draft-Scratch |
| Work Details | Section revise | `haipipe-page-writing` | `run-section-<slug>` | Draft-Revise |
| Work Details | Paragraph revise | `haipipe-page-writing` | `run-paragraph-<slug>` | Draft-Revise |
| Work Details | Revise edits | `haipipe-page-revise` | `run-revise-<target>` | Draft-Revise |
| Work Details | Auto write | `haipipe-page-writing` | `run-section-<slug>` | Draft-Revise |
| Work Details | Bind / update citation | `haipipe-page-evidence` | `run-citation-<slug>` | Evidence-Citation |
| Work Details | Build figure / table | `haipipe-display` | `run-display-<slug>` | Evidence-Display |
| Work Details | Bind / update value | `haipipe-page-evidence` | `run-value-<slug>` | Evidence-Value |
| Delivery | Build | `haipipe-page-delivery` | `run-delivery-<target>` | Delivery |
| Delivery | Check | `haipipe-page-check` | `run-check-<page>` | Delivery |

The Page's run names are its own (`haipipe-page`'s run families); the card for each is in
the Page's `run-cards.md`, which is where these skills are read from. The panel shows the Run's
name (`frame.PAGE_RUN_NAMES`) and the card's label under it.

## A theme's own buttons

A theme names its own buttons in `Theme.run_names` ({its words: the Run}, in `<theme>_theme.py`);
the frame shows the Run as the button and the theme's words under it. Named so far (261007):

```text
paper       each button names its Run itself (paper_theme.py)
work        Plan a Task run-plan-<tNN> · Build the Task run-build-<tNN> · Run a Task rNN_<slug> ·
            Check a Task run-check-<tNN> · Write the report run-report-<qNN> ·
            Review the Task code run-review-code-<tNN>
discovery   Add a resource run-add-resource-<slug> · Ask a Question run-ask-<qNN> ·
            Review the questions run-review-questions · Write the report run-report-<qNN> ·
            Check a report run-check-<qNN> · Find papers run-find-papers-<tNN> ·
            Read a paper rNN_<author><year>_<subject> · Synthesize a Task run-synthesize-<tNN> ·
            Verify a citation run-verify-citation-<slug> · Review a Run run-review-<run>
labeling    Prepare a corpus run-labeling-corpus-<corpus> · Open a labeling job run-labeling-open-<job> ·
            each view run-labeling-<view>-<job> (contract, preparation, embedding, definition,
            guideline, test, evaluation, audit, handoff, scan, final) · Rounds run-labeling-round-<NN>
cowork      Update the Block status / a job / the Job run-face-<bNN|jNN> · Open a job run-add-<jNN> ·
            Add a person / resource / file / entry run-add-<what>-<slug> · Draft an email
            run-email-<slug> · Write meeting notes run-meeting-<slug> · Review a draft
            run-review-email-<slug> · and the shared Ask, report, check, draw names
insight     Prepare extract run-add-version-<d>vM · Ask run-ask-<L><NN> · Carry a board over
            run-carry-<board> · Register a cut run-set-cuts-p<N> · Review the questions
            run-review-questions-p<N> · Plan the evidence run-plan-evidence-<L><NN> · Write / Review the
            script run-write-script- / run-review-script-<L><NN> · Draw the question map
            run-map-questions · Report run-write-<tNN> · Pool or split run-pool-<tNN> · Data and
            Information runs rNN_<partition> · Mechanical check run-check-alignment-<tNN> · Answer
            review run-check-<tNN> · Handoff draft run-draft-handoff (b11 s21)
design      Add a goal × method run-add-job-j<NN> · Set shared rules run-setup-rules · Plan the test
            run-plan-test-<app> · and the ladder's own: run-setup-goal-j<NN>, run-generate-d<NN>,
            run-verify-d<NN>-v<k>, run-revise-d<NN>, run-release-j<NN> (b12 s21)
```

## Guide

| Space | Button | Skill | Run | Levels |
|---|---|---|---|---|
| Guide | (none: read only) | `workbench-<theme>` | none | every level |

## Settled and handed over (b03 s21, 261007)

1. **Delivery at Block and Job** (decided): stays in each level skill (`haipipe-board`,
   `haipipe-job`); no `haipipe-delivery` until a theme's Block delivery needs one.
2. **Checked** (decided): not a fourth answer state; the report Page's CHECK verdict is shown
   beside answered (`haipipe-report`).
3. **Folder moves** (handed to the skill-folder design Block, b04): where these skills finally
   sit, and any renames, are b04's call.
