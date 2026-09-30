## 0.20.0 · 2026-09-30 · A run opens its results in a pop-out

- High-level logic + Low-level work: each run line under a work item's R is a link that opens the run's results in a pop-out over the page (JL 260930: "for a run, how could we have a popout window to show the results of that run's results"); a Task run's card in the Runs panel gains "Open the results ↗" (`runs_panel.py`: an optional `_open` on a row). Esc or a click outside closes it; "Open in its own tab ↗" keeps it.
- `GET /_board/run-result?task=&run=` (`serve.py` route, `render_run_result` and `run_files` in `paper.py`): receipt, summaries (with a small Markdown renderer that draws tables and escapes HTML), figures, the first 50 rows of each table, other files, and links to the run script, executed notebook and Task page. A run's files are its `results/<run>/`, else the files in a shared `results/` named after it, else those whose path holds every word of its name, else all of `results/`, and the page says which. Checked on Paper-ScalingGlucose-NatSeries2026 in headless Chrome: `run_6a2_f01` (Question 3 · Weaker further ahead?) opens its horizon-fairness figure; `b04.j02.t02`'s card opens its figure and two tables. Test: `test_a_run_opens_its_results`.
- A task's runs open below it, one level in (b 0, j 16px, t 32px, runs 48px), with the `▸ 3 runs · no receipts` toggle kept on the task line (JL 260930: "make the run below the t02 … follow the same indentation as b and j and t"; they opened to the right of the task name). `paper.py`: `_bjtr` wraps a task that has runs in `details.bj-tr`.
- A task's name under a work item is plain text, no longer a link: it opened the raw Task Markdown (JL 260930, on `t02 hero_figure`: "I don't think this is useful, could you remove this link?"). With runs, a click on the task line opens its runs. A Discovery task keeps its link: it opens the Discovery board in Outline, a rendered page.
- A result `.md` with no Markdown mark (no heading, table row or bullet) is plain text laid out by line and shows as written in `<pre>` (JL 260930: "How to handle this markdown render?", on `fit_summary.md`, whose lines had been joined into one paragraph); in real Markdown a single line break now stays.

## 0.19.0 · 2026-09-30 · The skill names the Story parts as the screen does

- Story parts are §N or their name (a Task Roadmap row, a Discovery Roadmap row, a Section Narrative row), never C6/C7/C8; C1, C2 … are claim ids only (JL 260930, "go ahead and update them accordingly", on aligning the paper skills with this workbench; haipipe-paper-story 0.17.0). `paper.py` comments follow, and the G3 line on screen now reads "N of M Section Narrative rows have a Section page".
- The Story Space box lists all four tabs (Spine, RoadMap Draw, High-level logic + Low-level work, Related Papers); the Storage tree shows `studio/`, which RoadMap Draw reads.
- "The four Workbench obligations" is "the four Workbench duties"; the Task review Spec is `paper.judgment.task`; "canonical" is gone (AGENTS rule 9).
- `audit_paper_views.py` also drives Delivery › Cover letter: nineteen routes, not sixteen.
- RoadMap Draw gets a Runs-panel card, `Redraw` (haipipe-paper-workflow `ref/run-cards.md`).

# CHANGELOG · haipipe-workbench-paper

## 0.18.1 · 2026-09-30 · No group labels in a question block

- High-level logic + Low-level work drops the group labels Hypotheses, Potential claims and Potential contributions on the left (JL 260930: "Hypotheses <--- could we just remove this … of no information") and Foundation work, "shared by all 7 questions" and This question's work on the right (JL 260930: "same to this, remove this"). Every item's pill already names its kind; a gap now separates the groups (`.lw-g`). An empty group shows its kind's pill over "none yet" or the Story's `- none: …` reason. A Question 0's Tasks label stays: its pills name the task alone.
- A contribution gets a pill like a claim's (JL 260930: "we can have the contribution label as well, just as the claim and hypothesis"): Contribution 1a, 1b, coded by its order in the question. `paper.py`: `_q_block`. Tests: `test_paper_workbench.py`; the design drawing's Story card matches.
- A picked question, hypothesis or work item no longer draws the 3px blue left bar, and work a picked hypothesis lights no longer draws its faint one (JL 260930: "I don't want this as well"). No fill replaces it (turned down in 0.14.1): an open item shows the pick, and the Runs panel names it. The Sections Space row keeps its bar, its only mark.

## 0.18.0 · 2026-09-30 · A question block may list its tasks

- High-level logic + Low-level work: a question block's **Tasks** group (haipipe-paper-story 0.16.0) is drawn first on the left under a "Tasks" label, each task with its kind as the pill (Pretraining, Downstream) and its short name in bold; a block with tasks leaves out its empty Hypotheses, Potential claims and Potential contributions groups (JL 260930: "what is the pretraining task, and also the downstream task, we haven't specified them"). `paper.py`: `_GROUP`, `question_blocks`, `story_tree`, `_q_block`, `.lw-k-task`.

## 0.18.0 · 2026-09-30 · Story › RoadMap Draw

- A Story tab between Spine and High-level logic + Low-level work, named by JL: "RoadMap Draw", `#story/roadmap-draw` (`#story/roadmap` still sends old links of the retired Roadmap tab to the logic view) (JL 260930: "I also want to have a view of subspace to show the excalidraw draw which will be saved here: …/studio"). It embeds the server's Excalidraw, editable, on a drawing in `<paper>/studio/`: the Story's own `<Story stem>.excalidraw` if it exists, else the first drawing there, else the Story's own, new; with several drawings, each is a button above the canvas; the iframe sends no referrer, as the Draw panel's does, because Excalidraw refuses a same-site embed ("I'm not a pretzel!"); "Open full screen ↗" opens it alone. `paper.py`: `roadmap_html`, `STORY_TABS`, `.rd-*` CSS and the switch handler.
- `servers/workbench-studio/xcal.py`: `mint_board_scene` writes a plain empty scene the first time a Board's `studio/<name>.excalidraw` is opened, as a Page's `studio/draw/` scene already was, so the first stroke has a file to save into. Opening a drawing never saves it; only a stroke does (haipipe-board 1.1.5, `xcal-boot.js`).
- Tests: `test_paper_workbench.py` (tab order, the lazy canvas, the switcher, nothing written on render), `test_linked_live.py` (minting only beside a `board.md`); `audit_paper_views.py` visits `story/roadmap-draw`; the design drawing gains the tab.

## 0.17.0 · 2026-09-30 · A work item is its stage, a short name, and a plain line

- High-level logic + Low-level work: a work item's closed line reads like a question's: the stage pill with the §7/§6 row's `name` cell beside it, then the row's `question` cell, one plain sentence, on the next line (JL 260930: "make the same to the left … the Label, + Short names, and a new line to explain what it is"; before, the pill stood beside a long question that wrapped). A row with no `name` cell draws as before. `paper.py`: `_work_rows` reads `name`, `_work_item` adds `<div class="lw-wtext">`.
- Paper-ScalingGlucose-NatSeries2026 StoryA: §7 T1-T12 and §6 D1-D6 gain names (Which training data?, One law for all?, Has anyone found this? …) and plain sentences; Question 3 is Different Prediction Horizon (haipipe-paper-story 0.15.0).

## 0.16.1 · 2026-09-30 · Related Papers on Paper-CGMtoHbA1c

- A related-paper card names an accepted manuscript as "accepted-manuscript PDF" (was plain "PDF"), and a group first author keeps its whole name ("AI-READI Consortium et al.", was "Consortium et al."). `paper.py`: the `kind` map and `_first_author`.
- Paper-CGMtoHbA1c's Related Papers tab now has 13 cards (JL 260930: "why I didn't see any paper", then "mainly related to the Diabetes Care" and "focus on the most recent paper"): 10 Diabetes Care papers from 2023-2026 plus the 2018 GMI paper that defines the benchmark, and 3 from other journals that the study answers directly; 1 with a PDF. The rows are StoryA §5.3's new P-board over Proj21-CGM-Pred `discoveries/b01_hba1c_estimation_literature/`. Tests: `test_paper_workbench.py` 13 pass; `audit_paper_views.py` 0 flagged on two papers at 1360px.

## 0.16.0 · 2026-09-30 · Story › Related Papers: plain cards, the PDF inside

- A third Story tab after High-level logic + Low-level work, `#story/related` (JL 260930: "create a new subspace after High-level logic + Low-level work … make each paper to be a card that I can read the original pdf"). The paper's target venue comes first, under "At <venue>" (JL 260930: "我们选 paper 一定要选一个 venue 的"), and other venues follow under "Other venues" (JL 260930: "this is not limited to NMI"). Inside each, four bands: Closest to this paper, For one research question, Background, Cautions and framing. The rows are the Story's §5.3 P-board (haipipe-paper-story 0.14.0).
- A closed card is two plain lines (JL 260930: "these papers card are not good, too messy, not readable … no need to show all the details in the card front face"): the title, then first author, year and short venue, with the question and a 📄 when the PDF is inside; a band's cards are rows in one box. Open: why it matters, links to the PDF, the publisher page and the Paper Run, the abstract folded, and the PDF embedded, loaded only when the card opens (`data-pdf`, since the page's `lazy()` loads every `data-src` in a shown pane and was loading all the PDFs at once).
- No facts line under the why line (JL 260930, on "P3 · for RQ1 · 📄 PDF · read: abstract · not cited yet · Nature Machine Intelligence 7, 1823–1833 (2025) · Article": "this is not relevant and could be removed"); a "cited in …" match against the Section Pages' Evidence Bibs was built for it and removed with it.
- `paper.py`: `story()` reads `P` rows; `related_html`, `_role_bands`, `_paper_card`, `_short_venue`, `paper_card_data`, `_disc_run`, `_yaml_block`, `_first_author` and `venue_name` are new. Tests: `test_paper_workbench.py` 13 pass (new: `test_related_papers_are_venue_cards_with_their_pdf`); board suite 800 pass; `audit_paper_views.py` 0 flagged at 1360px (`story/related` added to its routes).
- On Paper-ScalingGlucose-NatSeries2026: 45 papers, 38 with a PDF; 15 in Nature Machine Intelligence (Discovery b01.j01.t01 and b01.j02.t01), 30 from other venues (b01.j03.t01 and b01.j03.t02).

## 0.15.0 · 2026-09-30 · Questions start closed; Stories named in the tree

- Question blocks in High-level logic + Low-level work start closed (JL 260930: "could you make the questions to be hidden by default"). The closed line shows only the question; a tally line was tried and removed the same day (JL 260930: "I don't think this is useful"). "Not under a question" also starts closed.
- board.md `story-current: <Story stem>` limits the tree to that one Story (found on Paper-TestToLearn-MS2026: StoryA the submitted paper and StoryC its redesign both numbered their questions from 1). A Story-name row above each Story's questions was tried and removed the same day (JL 260930: "I don't think we need this"). Without the line every Story is drawn, so other papers do not change.
- `paper.py`: `_q_block` drops `open`; `logic_work_html` reads `story-current`; the click handler comment follows the new default. Tests: `test_paper_workbench.py` 12 pass (the RQ1 anchor no longer expects `open`); `audit_paper_views.py` 0 flagged on Paper-TestToLearn-MS2026 at 1360px and 2000px.

## 0.14.1 · 2026-09-30 · No color fills: a stripe marks the pick

- A picked work item, hypothesis, question or Sections row keeps a clear background; only its 3px left stripe marks it (JL 260930: "we don't need to have the color fill the whole card, make it transparent … I don't want to make it too colorful"). The group bands (Hypotheses, Potential claims, Potential contributions, Foundation work, This question's work) keep their colored label and left stripe with no fill. A work item lit by a picked hypothesis shows a faint stripe instead of a tint, and hovering a work item colors its question line instead of filling the whole card. `paper.py` CSS only. Tests: `test_paper_workbench.py` 12 pass; `audit_paper_views.py` 0 flagged on two papers at 1360px.

## 0.14.0 · 2026-09-29 · Colored group bands; every work item folds

- Group labels are colored bands with a left stripe, replacing faint grey caps (JL 260929: "这东西感觉有点浅浅的 … 变得更显眼一些，或者说你加上一些条纹，把它分隔开"): Hypotheses and This question's work blue, Potential claims green, Potential contributions orange, Foundation work gray with "shared by all 5 questions" in its band. An old `.lw-k` rule from the earlier inline "Contribution" label was overriding the group style; it is gone.
- Every work item folds, closed by default (JL 260929: "右边那些 results 也是可以 click 的，也是可以 collapse 的，就跟上面一样"). Its closed line keeps the stage, the question, "for Hypotheses …", "also for Questions …" and a size from the folder scan ("2 tasks · 992 runs", "built outside tasks/", "no folder yet"). Opening a work item selects it for the Runs panel; picking a hypothesis lights and opens the work that tests it.
- Each question's header row has a light background and a rule below it.
- `paper.py`: `_band` draws a group band; `_work_item` always folds and `_item_folders` returns the size; the separate Foundation/This question sub-labels and the "Potential work" caption are gone. Tests: `test_paper_workbench.py` 12 pass; `audit_paper_views.py` 0 flagged on three papers at 1360px and 2000px.

## 0.13.1 · 2026-09-29 · Text starts below the label

- A hypothesis's or claim's pill (with a hypothesis's mark at the right) sits on its own line, and its `Short name: sentence` starts on the next line at full width (JL 260929: "could you make the text start from the next line after the label?"). `paper.py`: `_hyp_line` and the claim rows use `.lw-top` + `.lw-body`. Tests: `test_paper_workbench.py` 12 pass; `audit_paper_views.py` 0 flagged at 1360px and 2000px.

## 0.13.0 · 2026-09-29 · Foundation inside each question; 1a, 1b; short names

- No separate "Work every question stands on" block (JL 260929: "just the research questions … the question level foundation work … and it can be shared"). Each question's Potential work starts with Foundation (§7 rows marked `every question`), folded, "shared by all 5 questions", then This question.
- Hypotheses and claims are labelled by question (Hypothesis 1a, Claim 1a; JL 260929) and read `Short name: one sentence`, the name in bold (JL 260929: "short-phrase-name: explanation"). Contributions follow the same form.
- "also for Questions …" marks work another question lists on the same folders; a row narrowed to different folders there (each question's own figures) is not tagged.
- `paper.py`: `_CODE` reads 1a codes; a claim's C1 alias is parsed and kept off the screen; `_label`, `_nx` and `_also` are new; `_shared_block` is gone. Tests: `test_paper_workbench.py` 12 pass; `audit_paper_views.py` 0 flagged on three papers at 1360px and 2000px.

## 0.12.0 · 2026-09-29 · The question is the block; the work follows the logic

- Each question is one block with the question across the top (JL 260929: "the question is the main block"). Left: Hypotheses, Potential claims (each "from Hypothesis N"), Potential contributions (each "rests on Claims …"). Right: Potential work, each piece named as the question it answers (JL 260929: "name them in the question format"), its stage pill, "for Hypotheses 1 and 2", and its B → J → T → R below. Work runs top to bottom in stage order: data, training, evaluation, results, analysis, figures, then Discovery (JL 260929: "the work should follow the logics").
- A new first block, "Work every question stands on", holds the §7 rows marked `every question` (on Paper-ScalingGlucose-NatSeries2026: the training set, built outside tasks/ in `examples-1-data/ProjB-Bench-1-FairGlucose`; the patient count; the model grid in `b01 j01_pretrain`; the scores in `b01 j03_evaluate`).
- Picking a hypothesis lights the work that tests it; picking a work item selects its row for the Runs panel.
- `paper.py`: `question_blocks()` reads the four groups (haipipe-paper-story 0.12.0); `_work_rows()` reads each §7/§6 row's question and stage; `story_tree()` joins hypotheses, claims, contributions and work; `_q_block`, `_shared_block`, `_rest_block`, `_work_item` and `_item_folders` draw them. `_row_ids` now also reads H and C ids (a Bullet address such as `C1.P1.B1` still is not one). The "shared by" cells and `_work_cell` are gone: each question lists its work once.
- Tests: `test_paper_workbench.py` 12 pass; `audit_paper_views.py` 0 flagged on three papers at 1360px and 2000px.

## 0.11.1 · 2026-09-29 · Plain words, shared work shown once

- Each hypothesis shows its statement as plain text under its line, and each question its contribution; the Details lines are gone from the tab (JL 260929: "could we remove the details and just replace it with the plain text, and we can understand what is this about"). The answer state, tests, role and "if it fails" stay in the Story file.
- Hypotheses in a row that rest on the same work share one row and one work cell, headed "shared by Hypotheses 1 and 2" (JL 260929: "the two hypothesis linking to the same thing … the work can support one or the other"). It replaces "same as Hypothesis 1". On Paper-ScalingGlucose-NatSeries2026, Hypotheses 1 and 2 both read the scaling-law fit in `b04.j01` (t01 collects the grid's results, t02 fits the law): the model-size exponent answers the first, the data exponent the second.
- `paper.py`: `_hyp_line` draws a pickable line (pill · phrase · mark, statement below); `_q_block` groups consecutive hypotheses by the folders their work reaches; `_details` and `_work_words` are gone. Tests: `test_paper_workbench.py` 12 pass; `audit_paper_views.py` 0 flagged on three papers at 1360px and 2000px.

## 0.11.0 · 2026-09-29 · One tree, split down the middle

- Story › High-level logic + Low-level work is one tree read left to right (JL 260929: "Question -- then hypothesis / claims -- then right part low level works, in the right part, we have B J T R. left and right they are still under the same tree, but visually separated"). Left: one block per question (JL: "each question is a block"), its hypotheses under it, each one clean line: `Hypothesis N` (or `Claim N` once every E-row testing it is established), a short phrase, one mark. Right, beside each hypothesis: B → J → T → R, one line per level, runs folded (`▸ 3 runs · no receipts`, open to each run ticket and its receipt). The §7/§6 rows are not drawn; their words, the tests, the role and "if it fails" sit under Details. A hypothesis whose folders equal the previous one's says "same as Hypothesis 1". "Not under a question" ends the tree: E-rows no question names, §7/§6 rows no question reaches, claimed folders no row names.
- `servers/workbench-paper/paper.py`: `question_blocks()` reads StoryA's new §3 blocks (haipipe-paper-story 0.11.0); `story_tree()` makes every join (question → hypothesis → the E-rows it tests → the §7/§6 rows those E-rows name, either end → folders) and gives the Runs panel its keys (a supporting run is keyed to every hypothesis, E-row and question above its row); `_q_block`, `_rest_block`, `_work_cell`, `_bjtr` and `_runs_fold` draw it. A Story that still writes the RQ table gets one hypothesis per E-row. `story_links`, `_chain_cards`, `_loose_cards`, `_bjt_tree`, `_block_cards`, `_disc_cards` and their helpers are gone.
- Clicking a hypothesis row selects it for the Runs panel (again to clear); the question keeps first-click-selects, next-click-closes.
- Tests: `test_paper_workbench.py` 12 pass (`test_logic_work_tree_reads_question_blocks` replaces the claim-tree test; the render test covers a Story still on the RQ table).

## 0.10.0 · 2026-09-29 · High-level logic + Low-level work: one tree, question to folder

- Story › Questions and Story › Roadmap are one tab (JL 260929: "Questions --> Claims, and then Claims (With Tasks Discovery Questions + BJTR folders) … this will show the whole picture of the paper"). One card per §3 RQ holds a fold per §5 claim (E-row); each claim holds a fold per §7 Task and §6 Discovery question that backs it; each of those holds its BJTR folders. Rows the RQ names that no claim holds follow in the card under "For the whole question". Claims with no RQ, rows under no RQ (grouped by their `Q` when the Story has a Q table) and folders no row names come last. The tab is named High-level logic + Low-level work (`#story/logic-work`; JL 260929: "High-Level Logic + Low Level Work"); the Questions and Roadmap tabs are gone, and `#story/questions`, `#story/roadmap`, `#story/tasks` and `#run/supporting` land on it.
- Every row names its level in its pill (JL 260929, names proposed first and then approved): `Question RQ1`; `Hypothesis E5` or `Claim E2` (one §5 E-row, `Claim` only once its support state says "established": Paper-CGMtoHbA1c's `✅ stated · ⬜ unbacked` stays a Hypothesis); `Task T1`; `Discovery D1`; `Folder b04.j01`. On Paper-ScalingGlucose-NatSeries2026 all ten E-rows read Hypothesis: none is reproduced locally yet.
- `servers/workbench-paper/paper.py`: `story_links()` makes every join, reading a link from either end (an E-row naming `T2`, or a T row naming `E1-E4`; ranges name each id; an Evidence Item id such as `E01-CITE-…` and a Bullet address such as `C1.P1.B1` are not row ids). `_chain_cards`, `_claim_fold`, `_work_fold` and `_loose_cards` replace `_rq_cards`, `_claim_card`, `_task_cards`, `_dd_cards` and `_question_cards`. Claims and rows are borderless folds (the RQ is the only card); a job's pill carries its whole address (`b04.j01`); a C6 row's Discovery jobs are the same folds (`_disc_tree`).
- Runs panel: the first click on a fold selects it, the next closes it and hands the selection to the fold or card above. A supporting run is keyed to every claim and RQ above its row, so picking RQ1 or E1 shows the Task runs behind it. Claim review, Task review, Task runs and Discovery runs all show on this tab (haipipe-paper-workflow 1.6.2 `run-cards.md`, `views logic-work`; `paper_run_types()` now reads a hyphen in a view name).
- A question's card header shows the question only. Its answer state (StoryA RQ1: "🔨 fitted (pretrain-loss) · C1 WEAK: the CI's upper edge sits at the imposed bound (2.0), not the point estimate · ⬜ unbacked locally") moved under Details (JL 260929: "I don't need this, this is confusing").
- A question's and a claim's own Details sit right under its heading, so they never stack with its last row's Details.
- Tests: `test_paper_workbench.py` 12 pass (`test_questions_is_one_tree_from_question_to_folder` replaces the general-question Roadmap test). `audit_paper_views.py` walks 16 routes (Roadmap removed): 0 flagged on Paper-ScalingGlucose-NatSeries2026 at 1360px. `studio/paper-workbench-design.py` redrawn with the tree.

## 0.9.1 · 2026-09-29 · Each Appendix page shows its own pair

- Delivery › Word › Preview shows the Word output (JL 260929: "for the word, why we cannot preview it"): the PDF twin `<stem>.pdf` beside the `.docx` in a frame, under one line naming the `.docx`, its size and time, and a note when the twin is older than the `.docx`. The twin is drawn by the paper build: `haipipe-paper-assemble/scripts/build_delivery.py` now runs the Page workbench's `exporters/docx2pdf.py` on `main_docx` and `supplement_docx` and records them in `build-manifest.json` `outputs` (`docx_pdf`, `supplement_docx_pdf`). Without a twin the file row says so.
- Runs panel (`servers/workbench-page/runs_panel.py`, shared with the Page workbench): a run type with no run yet shows `No runs yet.` and the skill that does its work (JL 260929: "why I cannot see the relative skills?"). Before, the skill appeared only on a run or on + New Run.
- Story › Roadmap: Block → Job → Task are borderless folds (JL 260929: first "we only have the structure for block. No jobs", then "套这么多感觉跟棺材一样" about nested cards, then "我想让它能够合上去" about a flat table). The block and each job are a fold with an arrow, pill, name and counts, open by default and closed with one click; a job opens to its one task table. No card, frame or table sits around a job (`_bjt_tree`). A Task or Discovery question's header carries only its id and question: the address and "allocated · 2/2 levels exist" are gone (JL 260929: "完全都没有用 … 干扰人思考"). SKILL.md says to write every §7 address in full: Paper-CGMtoHbA1c's `b01 j01, j02, j03` claimed only j01. `audit_paper_views.py`: 0 of 17 views flagged at 1360px and 2000px; `test_paper_workbench.py` asserts the folds.
- Card headers (`.item-summary`): the status column is `fit-content(34%)` and wraps (40% under 620px). It was `auto` with `white-space:nowrap`, so a long state took its full width and squeezed the headline to a strip (Paper-CGMtoHbA1c Story › Questions: RQ2 wrapped to six lines beside "largely (normoglycemia covered on all 8 metrics; prediabetes only partly)"). `audit_paper_views.py` at 1360px: 0 of 17 views flagged.
- `servers/workbench-paper/paper.py`: Sections › Narrative finds a page's call-peer pair by its `session:` and `codex-session:` ids together first. The Appendix pages share one Claude session and each keeps its own Codex thread, so the Claude id alone gave every Appendix page the last pair registered (Paper-CGMtoHbA1c showed `CGM2HbA1c-Appendix-C` three times). Tests: `test_paper_workbench.py`, 12 pass.

## 0.9.0 · 2026-09-29 · The cover letter in Delivery; the Roadmap tree

- An opened T or D question shows its BJTR folders first, already open (JL 260929: "I want to make the bjtr be the most important things"); the row's own text (design, contrast, result form, branches, depends on, feeds) folds under a closed Details line; the Task home rows that repeated the folders are gone.
- Delivery gains a fourth tab, Cover letter (JL 260929: the cover letter is one more delivery item). It
  reads `build-manifest.json` `cover_letter`, which haipipe-paper-assemble 0.9.0's run-delivery-coverletter
  writes from the submission Round page's Cover letter division: Preview shows the letter PDF, Artifacts
  its files, Checks each letter check and whether it is ready, with Open ↗ to the Round page. The fixed
  run run-delivery-coverletter shows under the `paper.coverletter` card (views cover). The letter no
  longer repeats in the LaTeX and Word tabs.
- Story › Roadmap is a tree when the Story has a §6 `Q` table: general question → its T and D rows (by
  their `Q` column) → their folders; a row with no Q comes last; a range address such as
  `b03.j02.t01–t03` names each task; selecting a Q filters the Runs panel to its runs.
- New buttons with skills: Select idea (Ideation, haipipe-ideation-select), Page check (Sections,
  haipipe-page-check).

## 0.8.0 · 2026-09-28 · Question first; every run names its skill

- Story › Roadmap is question first: a §7 T row or §6 D row card holds the folder that answers it;
  folders no question names are listed last, down to the task. The separate Task home and Discovery
  home lists are gone. `no address yet` reads `no folder yet`.
- The Story's §6 and §7 rows lead with a short plain question and a folder column; B1–B4 became
  T1–T4 (the header always said T; B was the old Block Board id).
- Runs panel: every Paper run card has a `🧩 SKILL` line (`paper_run_types` reads it); Supporting
  runs split into Task runs (haipipe-task) and Discovery runs (haipipe-discovery).
- Sections › Evidence cards show the item's real state (`Result ready` when its Local Run Result
  is on disk, instead of `contract only` on every card), type-first names (Evalue03) and its
  Supporting Runs.
- `studio/paper-workbench-design.py` now generates `studio/paper-workbench-design.excalidraw`
  (AGENTS.md rule 6). Part 1 answers the main question: each Space, its sub-spaces, their runs in
  order, and the skill of each run; it also draws the next step, Q1–Q5 general questions above T
  and D, and a Delivery › Cover letter sub-space.

## 0.7.1 · 2026-09-28

- `ref/space-mapping.md`: `deliver.<page>.<format>` reruns the lane's one fixed Delivery Run (`run_delivery_<lane>`); no receipt (JL 260928).
- The Narrative card's Session row reads the Section Page's own `session:` and
  `codex-session:` lines (written by `/haipipe-paper sessions`) and joins a call-peer pair by
  that exact Claude session id, before the old exact-name lookup. It shows the pair name,
  `claude <id>` and `codex <id> · <date>`; a page with no session still reads `no session · plan`.

## 0.7.0 · 2026-09-27

- The Paper Workbench follows the Page workbench (JL 260927: "make it aligned"; the drawing is
  `servers/workbench-paper/studio/paper-workbench-design.excalidraw`). Four Spaces: Ideation ·
  Story (Spine, Questions, Roadmap) · Sections (Main, Appendix × Table, Narrative, Evidence) ·
  Delivery (LaTeX, Word × Preview, Artifacts, Checks; Rounds). Each Space has its content on the
  left and its own Runs panel on the right, the Page's `runs_panel.py` markup; buttons come from
  `haipipe-paper-workflow/ref/run-cards.md`. Opening a card or clicking a row selects it for the panel.
- Gone: the Setup Space (a §8 row with no Page reads `not set up`; the Codex session sits on the
  Section's Narrative card), the Run Space (its runs are in the Runs panels; gates show where they
  happen), the Workflow map and folder tree (docs only), the backend Markdown cards, `⧉ chat` and
  `⧉ Copy Run request`, tallies, briefs and hint lines. Old `#setup/…`, `#run/…` and view routes
  still land on the view that holds their content.
- Sections Space is new: the compile order joined to each Section Page (draft version, state,
  Open ↗ to its workbench), the §8 narrative cards, and the hero Displays and Values; a selected
  Section shows its Narrative review and its own Draft, Evidence and Delivery runs.
- Shared with the Page workbench (`servers/workbench-page/runs_panel.py`): a type's count follows
  the selected target and view, and the panel opens on a type that has runs there; `panel_markup`
  is the reusable half of `panel_html`; judgment runs show as `run-idea`, `run-claim`, `run-task`,
  `run-narrative`.
- `tests/audit_paper_views.py` walks the seventeen new routes and flags a view with no Runs panel.
- Rosters and Stories in other shapes now read: a `### Label · folder · what it holds` heading, or one
  with no folder (the page is found by its own folder name), and §8 rows written as records
  (`**S-<id> (N) · job**` + `- **Field**: value` lines) beside the table form. A desk name may carry
  a hyphen (`S-JAMA-IM-Main-1-Introduction`). Paper-AgreeableOpioid-Jama showed no Story before.

## 0.6.0 · 2026-09-22

- Story Space reads legacy numbered Story pages (`Story01-seed`, `Story02-roadmap`,
  `Story03-narrative-MISQ`) as Stories beside the current `Story<Letter>`; before, a board
  with only numbered Stories showed "no Story yet" and none of their cards or Runs (JL 260925).
- Story Space: the `Claims & Hypothesis` view is now `Research Questions`
  (`#story/questions`; `#story/claims` still lands there). The card grain is
  the §3 research question; its §5 propositions (the claims) sit inside as
  nested cards, each keeping its `claim-En` id, `C5 · En` source stamp and
  rclaim Discussion row. Before, one card per claim repeated the same question
  in every card that shared it (JL 260922: combine them, do not rename claims
  to research questions). E-rows whose RQ cell names no §3 row are kept in one
  last card. `servers/workbench-paper/paper.py`: `_rq_cards` + `_claim_card`
  replace `_claim_cards`; E/RQ columns are found by header name when the table
  has a header row, else by the positional convention.

- Ideation Space: an Idea Card leads with the Idea's **Research Question** (its title
  drops to the subline); without one the title leads and the subline says `no Research
  Question written yet`, with a row naming the empty field. The plan's Bullets are a
  collapsed `writing plan` at the end of the card, never the lead (JL 260922: "the
  ideation should be the research question, which can trigger the reader to think").
- Ideation Space: the line above the Idea pool cards (`Story00-ideation · state … · plan
  … · approved: …`) is gone (JL 260922: "I don't want this"). The page and its plan
  remain named in the Space's backend Markdown footer.

## 0.5.0 · 2026-09-22

- Renamed with the vocabulary: `plugin` now means only a Claude Code plugin
  (`plugins/haipipe-toolkit`), a **lane** is a folder on disk, a **workbench** is
  a served tab and its contract. This skill was `haipipe-plugin-paper`; it pairs by name with
  `servers/workbench-paper`.

## 0.4.1 · 2026-09-21

- Add separate `⧉ Copy Run request` clipboard controls to bound Paper judgment
  entries for admitted Ideas, claims, Task Roadmap rows, and §8 narratives.
  Prompts carry the exact Page/target, instantiated Spec, Run Type, owner,
  prerequisites, family-filtered matching Ticket/Result/status, expected
  receipt, and next permitted owner action.
- Keep `⧉ chat` as source-grounded discussion context. Run-request controls
  only copy text; they never send, start, allocate, or write. Leave unsupported
  Page, Evidence, Support, Delivery, Compile, and Response entries prompt-free.

## 0.4.0 · 2026-09-21

- Expand the Run map with reader-facing names, Run Types/Specs, bounded
  work, owner/worker Skills, actors, prerequisites, and per-Space role/entry.
- Keep controls distinct from Specs and actual native Runs. Preserve source-
  grounded copy-to-chat as discussion context; identify the separate Run-
  request prompt control as not built.
- Cite the map's Markdown when copying selected map text and avoid repeating
  folder chips across the normalized Spec × Space entries.

## 0.3.0 · 2026-09-20

- Align the Space/folder map with the Run Specs and explicit controls. Present all five Spaces and owner-native receipts without allocating wrapper Runs.

## 0.2.2 · 2026-09-18

- Reading polish from a full audit (all twenty Space views of both papers,
  driven in real Chrome over CDP at 1360px and 2000px: no page overflow, no
  leaking view, nothing past the right edge): no type under 12px (the `⧉ chat`
  control, kind pills, sub labels, gate ids and bullet ids were 10 to 11px); a
  closed card shows its whole headline instead of clipping a claim or an idea
  with an ellipsis; a card subline that repeats the `where` label (the RQ on a
  claim card) is dropped; a long name clipped deep in the folder tree carries
  its full name as a tooltip. The audit is kept as a tool:
  `board/haipipe-board/tests/audit_paper_views.py --base … --paper …`.
- Cold-read fixes (a fresh agent was handed a pasted `⧉ copy to chat` snippet
  and asked to act on it, dry run; its friction log): the §7 card resolved
  only the FIRST address on a row while the claim counted them all, so
  `task_home()` now resolves every address and the card shows each; SKILL.md
  gains the address grammar and the `Task: bNN.jNN.` suffix convention, the
  two words CLAIMED and ADDRESSED, the writer rule (a traceability edit is
  made directly in the `source:` file; an edit that changes what the paper
  says routes to its owning skill), the `#<space>/<view>` route table, where
  the reader-facing origin comes from, and what to take from `haipipe-workbench`;
  stale `four Spaces` wording swept from SKILL.md, `servers/workbench-paper/paper.py` and the
  test; the Task-home brief no longer says nothing is typed (the claim is).

## 0.2.1 · 2026-09-18

- Workflow map × Folder tree (JL): `ref/space-mapping.md` gains a second table,
  `Folder tree × Run-Type`, one row per folder slot of the paper (board ·
  story00 · story · main · appendix · round · delivery · tasks · discoveries)
  with what it holds and the Run-Types acting there. Run Space › Workflow map
  now adds a `folder on this board` column to the map and, under it, draws the
  REAL folder tree of the paper as a nested collapsible explorer in two boxes
  (the paper folder; the project homes: claimed Task-home blocks and Discovery
  inquiries), each box two aligned columns: the bare tree on the left, the
  works on the right as one edged cell per row (counts on every folder; each
  slot's Run-Type chips on its first folder) and nothing else. The tree is
  complete: every folder opens down to its files (three levels below a page
  folder, two below a Task or Discovery task; 40 files per folder, the rest a
  count) (JL: a tree, not a table; concise and clean, the works to the right,
  readable at 1360px, the project homes in another box; the `holds` text and
  an explanation table were both tried on the tree and dropped: less is
  more); slots with no folder yet are named under the boxes. The card states
  its backend Markdown. Nothing is created from the view.
- Every Space ends with a `backend Markdown` card listing the files it read
  (JL: every word on the web must come from some Markdown): Markdown pages and
  outline files, the engine receipts (runtime.yaml, discovery.yaml,
  build-manifest.json, paper-build.toml), the task and discovery homes, and the
  space map. The workbench's own labels and hints remain in `servers/workbench-paper/paper.py`.

## 0.2.0 · 2026-09-16

- The route is live: `servers/workbench-paper/paper.py` renders Setup,
  Ideation, Story, and Run from the Board's Markdown on every open, on any
  board.md with `dialect: paper`. No per-paper file, no Links key.
- Retire the 0.1.0 `console/` prototype (static `data.js`, one paper only)
  and its `paper-workbench` Links key; `board-console` alias stays readable.
- Codex sessions are per Section Page (JL): one row per Main/Appendix page,
  none for Ideation, Story, or Supporting; a row is a plan until a pair
  manifest with exactly that name exists.
- Ideation reads the Ideas (ranked) table, else the plan's `Idea <n>:`
  divisions, so a P0 board with no Content still lists its ideas. Each idea
  is one collapsed Idea Card shaped like Outline's Evidence cards (JL: open
  and hide it); the detail holds Bullets, Notes, Evidence lines, bound
  Evidence Items, table fields, and the division link.
- Gates G0–G5 read named files; the Workflow map is projected from
  `ref/space-mapping.md`. Type scale and chips follow `servers/workbench-page/outline.py`.
- Story Space is five card lists (JL: judge, not write): Claims & Hypothesis
  (§5 joined to §3), Task Roadmap, Sections (§8), and hero Evidence Items
  (Main-page DISPLAY + Abstract VALUE), beside Spine. Spine shows the Story's
  §1 Identity, §2 Pitch and §4 Stakes content, not a division list (JL).
- Task Roadmap opens with the project's Task home, examples/<Project>/tasks/
  or task/ (JL: check the existing folder): one collapsed card per bNN block,
  its jobs and a task table (addr · task · develops · runs · state) read off
  the folder on every load, in both Task shapes (a task folder under the job
  with its own runs/ results/ scripts/, or the flat runs/<task>/ layout). §7
  rows follow; a row joins the tree only through a bNN[.jNN[.tNN]] address in
  one of its cells and otherwise reads `no address yet`. It also shows on a
  board with no Story yet.
- A paper claims its part of the Task home (JL: b05, b06 are another study's):
  board.md `blocks: b00.j04 b02.j01 b02.j02 b03 b04` plus every §7 address.
  Claimed blocks expand; a claim at job level hides the block's other jobs;
  unclaimed blocks are named once in a muted tail; no claim shows the whole
  home and says so. `task-home:` may name the folder outright.
- Discovery needs link to the Discovery home (JL): examples/<Project>/
  discoveries/ (or `discovery-home:`) is scanned bNN board → jNN inquiry →
  tNN Discovery Task Page; each D-row's address (b01.j04) becomes an Outline
  link into that Discovery Board, one card per inquiry lists its Task Pages
  with question · runs · status · outcome · confidence from discovery.yaml,
  and each card's feeds row names the D-rows that claim it. Claim with
  `discoveries:` + §6 addresses; MISQ StoryA §6 rows D1–D6 now carry
  `Discovery: b01.j01` … `b01.j06`.
- Setup's Board and Folder & Page views are one table (folder · role · state ·
  pages) with the desk named, and no generated `delivery/` row.
- Delivery Space (JL: the whole paper's delivery was missing): Manuscript ·
  Sections · Displays · Checks · Rounds & Venue, read from delivery/
  (paper-build.toml, build-manifest.json, display-register.md, the outputs and
  word-feedback/), the compile order with every page's fragment and lanes, and
  the Bc-<desk>-Round pages. Chip order was Setup · Ideation · Story · Delivery ·
  Run (superseded below); a board with no delivery/ shows `G4 open` and the finish rule.
- Run Space rebuilt by run type (JL: like the Outline Run workspace, Supporting
  Runs as a BJTR tree): Page Runs (RP · RD · judgment), Evidence Runs (each
  Evidence Item joined to its Local Run), Supporting Runs (the addresses on
  `Supporting Runs:` lines drawn Block › Job › Task › Run per owner, Execution
  and Discovery, each Run resolved to its ticket and receipt with its users).
  Chip order is now Setup · Ideation · Story · Run · Delivery. Run ids keep
  their dotted targets (`rp-scratch-01_C1.P1`).
- `⧉ copy to chat` (JL: it was only readable): every card, Spine row and text
  selection copies a chat-ready snippet that cites its Markdown `source:` and
  row ref; cards carry `data-src` / `data-ref`. It writes nothing and the page
  makes no request. Storage now states the law: Markdown is the only truth
  source; JSON/TOML/YAML read are engine receipts, shown and never edited.
- Evidence Items: a `#### E…` heading is a retired item; an item ends at any
  heading, so a retired block no longer overwrites the live item above it.
- Reading pass (JL: larger, and cell edges instead of text nested in text):
  label/value rows are one `_kv()` table with borders and a shaded label cell;
  a row with no label, or whose value is a table or a tree, spans the full
  width; every grid table has cell edges and a shaded header; base type is
  16px; long Story prose is set one sentence per line (`prose()`, display
  only); an open card shows its whole title. Every card's
  Discussion row joins the judgment Run whose ticket `target:` names the row
  (ridea · rclaim · rtask · rnarra; run-naming.md §8).
- Tooth: `board/haipipe-board/tests/test_paper_workbench.py`.

## 0.1.0 · 2026-09-16

- First contract: four Spaces over a static per-paper `console/` behind
  `/_board/paper`.
