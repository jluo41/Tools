# Idea Block and the Paper Board

Topics about where a paper's idea lives once ideas are their own Blocks (hai-ideation 2026-11-24, done in the
Codex session "Paper theme design": a direction Block, one Job per idea, Tasks that assess it, a selected Job hands off
to a Paper Board).

## 💡 Topic: Idea Block ▸ the Paper Board has no Ideation view

```text
BEFORE                                         PLAN
Audience Report: Ideation · Narrative · ...    Audience Report: Narrative · ...
paper/<Paper>/s01-ideation/ (candidates)       <Project>/ideation/b01_<direction>/jNN_<idea>/
Generate ideas · Test idea buttons on Paper    those buttons on the Idea Board
                                               Paper Narrative opens with "from <Block> jNN" link
```

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-24 | "how do you now think you can update skill content accordingly. So for the UI, we will don't have hte idea view anymore, right?" | JL | plan below; nothing changed yet |

Questions:

1. Which skill files say the Paper Board holds its own candidate ideas? hai-paper (scaffold makes s01-ideation/),
   hai-paper-ideation (owns the s01 portfolio), hai-paper-workflow ref/run-cards.md (Generate ideas, Test idea
   on the Paper's Audience Report), workbench-paper (Ideation view).
2. Which server files draw it? paper_theme_report.py (AUDIENCE "Ideation", `_ideation_rows`), paper_story_read.py
   `ideation()`, paper.py `ideation_topic()`, paper_spaces.py `_ideation_panel`, paper_theme_work.py.
3. What happens to the 20 papers that have an sNN-ideation/ today? Each Project's candidates move into one Idea Block
   of that Project (one Job per idea, the chosen one linked to its Paper); a scoped migration, one Project at a time.

Plan (in order):

1. Migrate one Project first (Project-Personality-OpioidRx: 4 papers from one direction), by hai-ideation's
   migration rule (identity and path map, receipts kept). Check that its Idea Block reads well.
2. Skills: hai-paper's scaffold stops making s01-ideation/ and writes `ideation-origin.yaml` on handoff;
   hai-paper-ideation shrinks to the handoff and the legacy migration; run-cards move the idea buttons to the
   Idea Board; workbench-paper's CONSTITUTION gets the article "a Paper shows its idea's origin, not candidates".
3. Server: drop Ideation from AUDIENCE; Narrative opens with one line, the source Idea Job as a link; Related
   Papers stays.
4. A Paper without an origin and with a legacy sNN-ideation/: the check names it ("migrate its ideas"), the page
   shows nothing for it.

State: open.

## 💡 Topic: Idea Block ▸ an Idea Block in paper/ draws as its own Block

```text
BEFORE                                          AFTER
paper/Idea-CGM-Pred: 📄 Paper Board             💡 Idea Block
Support blocks · Writing views                  one Ideas view: mark · Idea Job · question · went to
j01_hba1c: Structure · "No story yet"           💡 Idea Job: its Question · Claim · Where it came from
```

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-24 | "No more ideation theme" (JL); Idea-CGM-Pred showed "Block type 📄 Paper Board" and Paper views; the type came from the paper/ folder, not `board-kind: ideation-block` | Paper-Idea Report | new `servers/workbench-paper/idea_block.py` (`is_idea_block`, `idea_jobs`, Ideas table, Job face view); hooks in `focus_identity.page_type`, `focus_themes.paper_board_report` / `paper_job_views`, `paper_focus.report_views` / `skill_rows`, `board_read.is_version` (an Idea Job is no version), `focus_render` (an Idea Job's view alone) |

Marks, no state words: ✅ selected, ⬜ open, ⏸ deferred, ❌ eliminated (the row faded, its question struck). The rail
lists Paper-CGMtoHbA1c as a sibling Block (no indent), as every Block's rail does, not under the Idea Block; left as is.
Check: 5602 restarted; Idea-CGM-Pred shows 💡 Idea Block and the three rows (j01 ✅ → Paper-CGMtoHbA1c), j01_hba1c
its face, Paper-CGMtoHbA1c and its j11 version unchanged. State: fixed. Guard:
`servers/workbench-paper/tests/test_idea_block.py` (3); paper suite 111, workbench suite 223 pass.

## 🔬 Topic: Idea Block ▸ an assessment Task shows its reading

```text
BEFORE                                          AFTER
t01_prior_work: MindMap · Plan + Results        💡 Assessment Task · Assessment
Aim line and the Run only                       face body: Where it stands · Next
"inconclusive", "Nsugbe" nowhere on the page    Novelty: i03_20261124.yaml · c01 inconclusive low ...
Receipt: [`x.yaml`](x.yaml) printed as text     a link (page_reader: code span as link text)
```

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-24 | a Task (task-type: ideation) under an Idea Job drew with the work-Task frame; its "Where it stands" verdicts and receipt link were hidden | Paper-Idea Report | `idea_block.task_views` and `receipt_rows` (a linked `kind: idea-novelty-check` receipt: claim, verdict, confidence); hook first in `paper_tasks.views`; type `💡 Assessment Task`; `page_reader._md_inline` reads `[`code`](href)` as a link everywhere |

Check: 5602 restarted; t01_prior_work shows its face and c01/c02 inconclusive low, c03 unverified none, the receipt
link answers 200; t02_minimum_experiment shows "The experiment". State: fixed. Guard: `test_idea_block.py` (4); paper
suite 112, workbench suite 223 pass.
