## 1.17.1 · 2026-10-23 · Carry-over reuses a report already written; a carved Section's words move into its Draft

- New `scripts/carry_over/import_fragments.py` (dry run, apply, verify, retire, rollback), found carrying
  Paper-MessageTradeOffEgm onto the ladder: its 19 Sections kept their words only in an old Page-local
  `delivery/latex/<stem>.tex` with no `% GENERATED from` mark, so `page.py export` refused to build Block Delivery and
  the rename to `tNN_` would have orphaned them. It writes each Section a Draft (a division per `\section` or
  `\subsection`, a paragraph per LaTeX paragraph, a Bullet per source line, § 3 as written, `content-format: latex`)
  or fills a planned Draft's empty § 3 (the n-th sentence to the n-th Bullet, a comment or `\begin` line riding with
  the next); `--verify` checks with md2tex's own reader that the LaTeX lane prints each fragment again; `--retire`
  moves the old lane into the run's keep folder. On that Board all 19 rebuilt fragments equal the carved ones and the
  assembled draft is 65 pages, as before. Test: `tests/test_import_fragments.py`. `ref/paper-ladder.md` names the step.

- `scripts/carry_over/topics_paper.py` opened a second report for a question that already had one: a Board whose
  `reports/q01_<name>/` said `answers: RQ1` before the carry-over got a new `q02_<name>/` for the same Question 1, and
  every later question shifted by one. A report that already `answers:` a question of the current telling (`RQ1`,
  `Q01`, `Question 1`) is now that question's report: the question takes its number, the report keeps its words and
  folder, its `answers:` names the Board Question, and its links follow the move. Test:
  `tests/test_carry_over.py::ReportAlreadyWrittenTest`.

## [1.17.2] — 2026-10-26

Shorter description (527 -> 328 characters): what it does, when to use it, its trigger words; aliases and old command names kept (diagnostics/descriptions/261026.yaml). (describe 261026)

Door for hidden helpers (workflow): they leave the skill listing (`disable-model-invocation: true`) and this door reads their SKILL.md by path. (door 261026)

## 1.17.0 · 2026-10-23 · A paper's work folder, its j21 display Job and the display plan

- JL 261023: "for the paper, they will also have a work folder, one work folder to provide the content
  for the paper folder"; "one of the block's job will be the j21_paper_displays"; "this should be a plan, and should be
  proposed to the author to think about how to draw them". The display Job is `j21_paper_displays`
  (`j21_<venue>_displays` with several venues); its face opens with a display plan the authors agree before any
  Run draws; Sections write numbers only after the drawn displays pass review and are accepted.

## 1.16.0 · 2026-10-22 · A paper is a paper Board plus a work Block

- § Evidence and Page boundary (JL 261022: "for /haipipe-paper, we should have a paper block and a work block to
  provide the displays and E-work, right?"): the paper Board writes, its work Block computes; the work Block's
  display Job `jNN_paper_displays` draws every picture, a paper display unit only frames it, and the version face
  names the Block in `work-block:`. Rules in haipipe-paper-evidence 0.2.0.

## 1.15.2 · 2026-10-21 · Carry-over for a hyphenated desk, and the name sweep

- `scripts/carry_over/rename_tasks.py` renamed no Section of Paper-AgreeableOpioid-Jama: its patterns took the desk as
  one token, and `S-JAMA-IM-Main-1-Introduction` holds a hyphen in its desk. The desk token now allows hyphens
  (`S-JAMA-IM-…` → `t01_introduction`), and the MISQ and npjDM names still map as before.
- New `scripts/carry_over/sweep_names.py` (dry run, apply, rollback): after the three carry-over scripts, it reads their
  records and replaces the old names in the hand-written files they skip on purpose (`draft/records/`,
  `draft/previous/`, Run tickets), longest first, so the rename covers every hand-written file (AGENTS.md rule 7). It
  skips generated and sealed output, any line naming the predecessor Board, and board.md's `## Log`. A Story child
  archived before the move is named by its `_archive/` home, not by `studio/`.
- `ref/paper-ladder.md` names the step after `rename_tasks.py`.

## 1.15.1 · 2026-10-20 · 4 · Display in a Section's steps

- A Section's steps table gains 🖼 4 · Display (its Tables and Figures, numbered for the paper, within the venue's
  limit; haipipe-display · haipipe-paper-evidence); Revise is 5 · Revise.

## 1.15.0 · 2026-10-20 · A Section, step by step (JL 261020, b32 s41)

- JL 261020: "Update the /haipipe-paper and /haipipe-draft and then apply it to" the version's Work. New
  `### A Section, step by step`: a Section Task is worked in haipipe-draft's six steps (Studio · 1 · Plan · 2 · Write ·
  3 · Evidence · 4 · Revise · Delivery), with the paper's own owner on each; 3 · Evidence's prompt is
  `/haipipe-paper-evidence <task>`.
- The workbench table: the version's Work shows each Section's six step chips, a click each into that tab; a Section's
  Work is the six step tabs (the SUB-* rows in 1 · Plan); Report, Description and Delivery keep the rest.
- A Section's Scratch is typed in 1 · Plan, and 2 · Write drafts `## 3 · Draft` from §1 and its Scratch; the person types
  in the boxes of 1 · Plan, 2 · Write and 4 · Revise (JL 261020, built in the Paper-LLMRecPhy-Jama session).

## 1.14.0 · 2026-10-19 · The plan after the story: haipipe-paper-plan

- The owner and routing tables name `haipipe-paper-plan`, the paper's s03-paper-dataflow and s04-paper-workflow (JL
  261019: "plan for the data flow and plan for the paper flow"); a fresh-agent test found the door did not route to it.

## 1.13.0 · 2026-10-19 · A Section is a draft Task: haipipe-paper-draft and haipipe-paper-evidence

- The Section owner is `haipipe-paper-draft` (was `haipipe-paper-section`, kept as an alias), and the new
  `haipipe-paper-evidence` owns what backs each Section and one evidence ledger per version (JL 261019: "it is
  like we have the paper to combine the evidence and draft together to make a draft task, right?"; "okay,
  please go ahead and do it"). The owner table and the routing table name both.

## 1.12.5 · 2026-10-19 · Related work is its own owner, haipipe-paper-related

- The owner table and `ref/paper-ladder.md` name `haipipe-paper-related`: `studio/s10-related-work-map/` and
  s11-s19, one topic per type of closest work (JL 261019: "it is different from the literature").

## 1.12.4 · 2026-10-15 · New Sections say task-type: draft (b32_draft s03-D04)

- `scripts/paper_ladder.py` writes `task-type: draft` in a new Section's face (was `task-kind: page`);
  `ref/paper-ladder.md` names it.

## 1.12.3 · 2026-10-14 · rename_tasks.py reads FairGlucose's older names

- `rename_tasks.py`: unnumbered Main Pages (back matter, `S-npjDM-Main-DataAvailability`) become `t0N_` after the last Section, in compile-order order; Rounds named `RD01-positioning-2026-05-14` become `reports/qNN_positioning-0514`; CamelCase titles split (`t21_dataset-statistics`). Tested on a copy of Paper-FairGlucose-preprint: 75 renames, three PDFs unchanged.

## 1.12.2 · 2026-10-13 · Carry-over scripts, run on Paper-AgreeablePrescriptionDiscretion

- Second Board moved with `scripts/carry_over/` (Physician-SPACE, the MISQ paper, version `j01_v0929_misq`); two faults fixed at the source:
- `migrate_paper.py` and `rename_tasks.py` `move()`: tracked files another session deleted without committing made `git mv` fail with "bad source" on the whole folder; the deletion of those files is staged first (`drop_deleted`), so uncommitted work no longer blocks a move, as the docstring promises. `topics_paper.py` uses the same helper.
- `git()` in both: a moment's `index.lock` held by another process (an editor, a server) is waited out (up to 10 s) instead of failing a move halfway with no moves map written.
- Found, not fixed here: `topics_paper.py` reads Story questions only as `#### N · Question N` blocks, so a Story whose §3 is an RQ table makes no Board Questions; `topics_paper.py` left `paper-build.toml` `order =` on the old Story path instead of the version face; a Section's `story-row:` came out as `<version> ## Narrative / <stem> + draft/<story>-outline-v0.2.md ()`.

## 1.12.1 · 2026-10-11 · Related's subfolders are its groups; emails/

- b10 s04-D08, D09 (JL 261011, sent by b10_BluePrint-ProjectWorkbench-dNN): a subfolder of `related/` is a group of its files, so `meetings/x.md` is in the meetings group without a group cell; a new subfolder `emails/` keeps an `.eml` as it came; the new base skill `haipipe-related` (1_base/project, 0.1.0) owns `related/`, `related.md`, its groups and the Related view.
- `ref/paper-ladder.md`: the `related/` lines name `/haipipe-related`, list `emails/`, put the columns in its order (kind · date · item · link · feeds · group) and say a row's groups are its subfolder first, then its group cell.
- SKILL.md's workbench table: Studio › Related groups by subfolder, then the group cell; `haipipe-related` is its first owner.

## 1.12.0 · 2026-10-11 · Studio, Related and Delivery are the Board's (b10)

- b10_project_workbench settled who owns what for every Block (s09-D01, D02, D05; s04-D01): Studio, `related/` and `delivery/` are the Block's alone, and every level keeps its own `reports/` and `runs/`. JL 261011 (b16): "do you think we want to update the skills as well?"
- `scripts/paper_ladder.py`: `spaces` gives a version `reports/` and `runs/` only, no `studio/`; `next` copies a Section's face and `draft/`, no longer its `studio/` (an older Section's topics stay where they are and show in the Board's Studio). New test lines in `tests/test_paper_ladder.py`.
- `ref/paper-ladder.md`: the screen is the shared frame's two rows (`Guide · Studio | Paper Board · Version ▾ · Section ▾ | Delivery`, Related folded inside Studio, then `Description | Report | Work | Runs`); the tree drops the version's and the Section's `studio/`, names the Board's `related/` folders, and keeps a comments batch's meeting notes in `related/meetings/`; the build lands in `delivery/jNN_<version>/`. `group` is every related row's column (b10 s04-D07), not a paper-only one.
- SKILL.md's workbench table: Studio, Studio › Related and Delivery rows for the Board's shared views; Description is Scope · Venue · Resources. Studio › Related groups its rows by `related/` subfolder and opens each on its file; the cards by question are Report › Related Papers.

## 1.11.1 · 2026-10-09 · The carry-over scripts, run on ScalingGlucose

- First Board moved with `scripts/carry_over/` (Paper-ScalingGlucose-NatSeries2026, branch `v1009-paper-ladder`); four faults found and fixed at the source:
- `topics_paper.py`: a §3 block is a question only when "Question" is followed by its number, so "#### 3.7 · Question logic" stays in the Story as words (it was taken for an 8th question and cut out).
- `topics_paper.py`: a question keeps the number its telling gave it (Question 3 → Q03, Question 0 → Q00), so "Q3" in the Story's tables and the meeting notes still names it; a taken number gets the next free one.
- `migrate_paper.py` and `topics_paper.py`: with no `story-current:` in board.md, the version tells the Story its build's `order =` names (else the only telling); `topics_paper.py` writes `story-current:` and the face's `tells:`, and takes §8 out of the Story only when a version receives it (before, §8 stayed put and the version got no `## Narrative`).
- `topics_paper.py`: each Section's `story-row: <Story> §8.N / <stem>` follows its row to `<version> ## Narrative / <stem>` (paper_ladder.py task's shape), the bound Story version kept under the topic's name.
- `topics_paper.py`: the rest of what a tool finds by a Story's stem (`draft/`, `draft/records/`, `draft/previous/`) follows its new name, as `rename_tasks.py` does for Tasks; `StoryA-…-context.md` stayed under the old name in `studio/s02-…/draft/records/`.
- New `tests/test_carry_over.py`: a Board shaped like ScalingGlucose's before the move; fails on the 1.11.0 scripts, passes now.

## 1.11.0 · 2026-10-07 · One ladder contract, one scaffold (b16 Q05)

- JL 261007: "the current skill is not that powerful enough"; "a before after plan of the skill folders and what to change and why"; "unify the run to be run-xxx-xxx". Shaped like the design theme's skill (`ref/design-ladder.md`, `scripts/design_ladder.py`), as drawn in Tools/designs b16 s21 (frame "skill folders: before → after") and run by b16's goal g04, phase 1.
- `ref/paper-structure.md` → `ref/paper-ladder.md`: the Board · version · Task · Run tree, each level's folder, face, scaffold command and Runs, the naming invariants, the source and delivery law, and the older layouts. Every live mention follows.
- New `scripts/paper_ladder.py`: `board`, `version`, `next`, `spaces`, `task`, `run`, `rollback` (with `--dry-run`). `next` and `spaces` are the retired `version_paper.py`'s `new` and `spaces`; `rollback` still reads its `.paper-version-N.yaml` records. `task` makes a Section, the Abstract or a letter (`t3N_`, `section_kind: letter`) with the reader-contract header and its own `studio/` and `reports/`. `run` writes a Board's or a version's soft Run, `runs/run-<type>-<target>.md`; a Section's Runs stay the Page workflow's.
- `version_paper.py comments` → `haipipe-paper-comments/scripts/review_items.py add`.
- `migrate_paper.py`, `rename_tasks.py`, `topics_paper.py` → `scripts/carry_over/`: one-time moves of older Boards, unchanged and still reversible.
- SKILL.md routes by level (a ladder table), and its workbench table names level › Space › view as the paper workbench shows them, no longer the four old tabs.
- Family test `tests/test_paper_ladder.py`: every level is made, `next` copies only written files, a comments batch becomes a report, and rollback restores the Board byte for byte.
- Board and version soft Runs follow the shared Run contract (`haipipe-run`): `paper_ladder.py run` calls the shared writer, `haipipe-run/scripts/soft_run.py new`, which makes `runs/run-<type>-<target>/` with its `run.yaml` card (skill, agent and signs from the paper's run card whose pattern names it) and its ticket; `soft_run.py pass` adds its passes. A Section's Runs stay the Page engine's.
- `scripts/create_section_sessions.py`: Sections are the newest version's `t0N_` (Main) and `t2N_` (Appendix, A = t21) Tasks, in its face's compile order; an older Board's `S-` pages are still read.
- Matched to the project skills (haipipe-block, -job, -report, -studio, -run): the Board face carries `board-kind: paper-board`; a version face has `goal:`, `close:` and an ordered `## Tasks` list, kept by `paper_ladder.py task`; a Section face has `task-kind: page`; `board` and `version` write faces only (a Space folder comes with its first item); a version answering a comments report says `responds-to:`, since `answers:` names Question ids.

## 1.10.0 · 2026-10-07 · The Story as studio topics and Questions (b16 Q04)

- JL 261007: "the stories will be merged into the studio sNN and report qNN, all the questions will be grouped as different topics"; "story and ideation can be called, in that view". On the ladder a paper Board is b03's shape. Ideation is `studio/s01-ideation/`. Each telling is `studio/sNN-story-<desk>-<idea>/` (identity, pitch, stakes, the roadmaps; `feeds:` its Questions). Each research question is a Board Question (`board.md ## Questions`, `group:` its telling) with `reports/qNN_<question>/`. The current telling's Section Narrative and compile order are its version face's `## Narrative`, which the build reads. `ref/paper-structure.md` draws it; the docs that drew `j00_story/` point there.
- New `scripts/topics_paper.py <board> --dry-run | --apply | --rollback`: Story and Ideation Pages into topics and reports, keeping the words. The question blocks become reports, and §8 moves to the version. It also moves board.md's Story group and story-current, the build's order, the links, and a loose drawing with its builder into a topic. The old texts are kept in `.paper-topics-N/` for an exact rollback.
- New `scripts/version_paper.py <board> spaces | new | comments | rollback` (with `--dry-run`):
  - `spaces` gives a version `studio/`, `reports/` and `runs/`.
  - `new --from <version> --date MMDD` starts the next version from an earlier one (JL: "j02 will make a copy of it and we will modify based on that"). It copies each Section's own writing (its face, `draft/` without records, `studio/`); results, runs and delivery are not copied. It also copies the build inputs, its order pointed at the new face, and links to anything not copied point back at the original.
  - `comments <batch> --to <version>` files a review batch as `reports/qNN_<kind>-<MMDD>/` with `page-type: comments` and a `group: comments` row in that version's Questions; every source that names it follows.
- `migrate_paper.py`, `topics_paper.py` and `version_paper.py` match only live run records, so a rolled-back record is never picked again, and a new run never reuses a rolled-back number.
- First Board: an example Project's paper Board. 6 studio topics and 6 reports; j01 is the sent version (its Sections kept); j02 starts as a copy of j01's writing and answers the editor's decision. Each step was rehearsed on a copy (apply, checks, rollback back to the identical tree).

## 1.9.0 · 2026-10-07 · A comments batch is a report

- A comments batch is not a Task: it is a report of type comments, `reports/qNN_<kind>-<MMDD>/` in the version that answers it (or the Board, for a meeting), its face `page-type: comments` (JL 261007: "comments … are a special type of report … it should be in the reports/ but you can say its type is the Comments"). `t3N_` is for letters only: t31 cover letter, t32 response. `ref/paper-structure.md` and haipipe-paper-comments 1.1.0 say so.
- `scripts/rename_tasks.py` moves an old `RD<NN>-…` batch into the version's `reports/`, numbered after the reports already there, and names it by its new stem everywhere; a relative path link changes depth and is left for a person.

## 1.8.0 · 2026-10-07 · Dated versions, Tasks by series

- A version is `jNN_v<MMDD>_<desk>/`, named for the day it is sent, and its Tasks by series: `t00_abstract`, `t0N_<title>` Main in reading order, `t2N_<title>` Appendix (A = t21), `t3N_<title>` letters and comment batches (JL 261007: "no more S-xxx … just use MMDD"). `ref/paper-structure.md` and the Section, assemble, comments and run-naming docs say so; `S-<desk>-…` and `RD<NN>-…` names stay readable.
- New `scripts/rename_tasks.py <board> --date MMDD --dry-run | --apply | --rollback`: renames one version and its Pages (folder, face, the files named for the Page) and every source line that names them (board.md, the Story's rows and compile order, faces, plans, paper-build.toml, .gitignore). Generated and history files are not edited; a Page's delivery is rebuilt by `page.py export`. `<board>/.paper-tasks.yaml` records every rename and edit for rollback; roll it back before `.paper-moves.yaml`.
- The readers follow: paper.py (`is_section`, `is_batch`, `part_of`, `task_num`; the desk from the version face), paper_theme.py (Section dispatch, comment pages, `level_patterns`), build_delivery.py and cover_letter.py.
- First version renamed: one example Board (76 renames, 378 line edits).

## 1.7.0 · 2026-10-07 · The paper on the ladder (b16 g03)

- `ref/paper-structure.md` shows both layouts, the ladder first: `j00_story/` (the Story Job: Story00 and Story<Letter> Pages) and one version Job per send, `jNN_v<N>_<desk>/`, holding its face (`jNN_v<N>_<desk>.md`: send · desk · venue · state · tells · `## Questions`), its Main and Appendix Sections (the part is in the stem), its review batches (`RD<NN>-…`, `CM<NN>-…`) and its own `delivery/`. Today's `A1-Story/` · `B<x>-<desk>-…/` · `delivery/` layout is still read. The other paper docs that draw the old layout carry one line pointing there.
- New `scripts/migrate_paper.py <board> --dry-run | --apply | --rollback`: moves one Board onto the ladder, folders only (no Page stem changes). It rewrites board.md's `## Pages` headings, paper-build.toml's `[pages]` paths (`main = appendix = ".."`, with haipipe-paper-assemble 0.10.0) and the folder names in its comments, each relative Markdown link whose source or target moved (never in a generated or history file), and adds a `.gitignore` twin for a moved anchored line. It writes the version's face. Tracked paths go by `git mv`, untracked by a plain move, and nothing is committed. `<board>/.paper-moves.yaml` keeps every move and line edit, the pre-move `git status`, and what `--rollback` reverses.
- First Board moved: one paper Board of an example Project (21 moves, 20 line edits, one face). It was rehearsed on a copy first (apply, checks, rollback back to the identical tree).

## 1.6.0 · 2026-10-03 · A Report per Story question, in reports/

- `ref/paper-structure.md`: the paper root gains `reports/qNN_<topic>/qNN_<topic>.md`, one Report Page per Story question, a board-level folder beside `studio/` and not a Page group (JL 261003: "should we have the reports folder in the paper board as well"; "just like the studio and reports, like other board level folder"). Same shape as a Task Block's reports (`answers: RQ<n>`, `answer-status: open | partial | answered`, Opening = the answer).
- A Report is the G2 record: Story › High-level logic + Low-level work gains a Report column (haipipe-workbench-paper 0.23.0), and a hypothesis shows ✅ only when its question's Report says answered, else 📝.
- First Report: Paper-MessageTradeOffEgm `reports/q01_each_message_average/` (partial: E01 reproduced exactly; 1b's clustered variance not yet checked).

## 1.5.1 · 2026-10-02 · Related Papers says why we keep a paper

- "What the person sees": the Related Papers card now shows why the paper is kept (P-board `keep`, `bears on`; haipipe-paper-story 0.18.0) and the paper's logic beside its work (`logic-work.yaml`; haipipe-discovery 0.21.0, haipipe-workbench-paper 0.21.0).

## 1.5.0 · 2026-09-30 · The door names what the Workbench shows

- New table "What the person sees": each Paper Workbench tab (Ideation; Story › Spine, RoadMap Draw, High-level logic + Low-level work, Related Papers; Sections; Delivery › LaTeX, Word, Cover letter, Rounds) and the skill that owns it, so a person naming a tab reaches its owner (JL 260930, "go ahead and update them accordingly", on aligning the paper skills with the Workbench).
- Story parts are §N or their name, never C1-C8 (haipipe-paper-story 0.17.0), here and in `ref/page-integration.md`, `ref/paper-structure.md`, `ref/section-sessions.md` and `ref/run-naming.md`; the Task review Spec is `paper.judgment.task`; "canonical" and "obligation" are gone (AGENTS rule 9).
- `ref/paper-structure.md` and the family README show `studio/`, the folder Story › RoadMap Draw reads.

## 1.4.4 · 2026-09-29 · outline/ to draft/ in current-layout prose (JL 260929)

- Paths that describe the current Page layout say `draft/`: the plan `draft/<stem>-draft-v<G>.<S>[.<E>].md`, records `draft/records/`, `draft/previous/`, `draft/skill/`, the Evidence Markdown `draft/<stem>-evidence-items.md`, `draft/evidence/bibex/` and `draft/evidence/materials/` (JL 260929: "it should be draft"). Mentions of legacy Pages, retired `outline/evidence/` lanes and the migration keep `outline/`, as do the OUTLINE stage, the Outline table and the `outline:` grammar key.
- `scripts/audit_page_compatibility.py`: a Page-root `evidence/` is told its records belong under `draft/evidence/`.

## 1.4.3 · 2026-09-29 · Per-page Appendix pairs

- `scripts/create_section_sessions.py`: an Appendix that keeps one older Codex thread per page now gets one call-peer pair per page, `<Short>-Appendix-<letter>`, with the new Appendix Claude session, as `ref/section-sessions.md` already said; before, it got no pair at all. `codex_name()` reads the thread's name from the Codex session index for the pair. Found on Paper-CGMtoHbA1c (three pairs registered by hand); checked on a stubbed two-appendix paper.

## 1.4.2 · 2026-09-28 · Keep existing Codex threads (JL 260928)

- `ref/page-integration.md`, `ref/run-naming.md`: a Page Delivery Run is one fixed Run per lane (`run_delivery_<lane>`), not `rdNN_<target>`; `RD<NN>` stays the Round Page id (JL 260928).
- `scripts/create_section_sessions.py`: an Appendix unit whose pages each name their own live `codex-session:` counts as having Codex (`one per page`); the plan no longer creates one new thread and writes it over all pages, nor binds the whole unit to the first page's pair. `ref/section-sessions.md`: look for a paper's existing Codex threads and bind them before creating. Found on Paper-TimeEventDM-ISR2026, whose 13 per-page Codex threads from 260917 were missed.

## 1.4.1 · 2026-09-28 · No content hashes (JL 260928)

- `ref/page-integration.md`, `ref/run-naming.md`: the Ideation sync and Page projection receipts carry the revision number only, and a reused Result is named by path and version; no `source_hash`, output hash or hash pin. `scripts/audit_page_compatibility.py` no longer accepts `sha256:` as a Story binding: `story-row:` needs `+ <Story version>`.

## 1.4.0 · 2026-09-28

- Add `/haipipe-paper sessions` (JL 260928): once the Story's §8 compile order fixes the
  Sections, `scripts/create_section_sessions.py` gives each unit (a Main Section Page, and the
  whole Appendix group as ONE unit by default, `--appendix each` to split) a named Claude session
  `<Short>-<unit>` and a named Codex thread `<Short>-<unit>-Codex`, pairs them (identity-only
  call-peer), writes `session:` and `codex-session:` into each page header, gives both a read-only
  first turn with five scope rules, and stops the Claude session after that turn so `/resume` can
  open it. Codex threads are made through `codex app-server` (`thread/start`, `thread/name/set`,
  `turn/start`) so the Codex app lists them by name; `codex exec` threads are unlisted and unnamed.
  An existing Claude↔Codex pair is bound, not duplicated. Plan-only by default; `--apply` creates.
  A Claude session is the unit's own only when its saved name is `<Short>-<unit>`, so a
  `session:` copied in from a predecessor paper is replaced, not reused (found by a fresh-agent
  plan-only run on the JAMA paper). The prefix is recorded in `board.md` as `session-prefix:` on
  the first `--apply` and read from there afterwards. Contract: `ref/section-sessions.md`.
- A Section Run has two bookends the author calls (JL 260928): only the Section's Draft file
  changes in between; records and one log entry are written at the close; Content adoption and
  the web → LaTeX → Word lanes follow on request; assembly sees a mid-Run Section's previous
  export. Contract lives in `haipipe-draft-workflow` 0.65.0 (`interactive-writing-run.md` §🔖).

## 1.3.0 · 2026-09-21

- Add the sourced 21-point submission-readiness overlay to the G4 gate, with
  section-owned and whole-paper criterion rows that reuse the shared rubric.

## 1.2.0 · 2026-09-20

- Route Paper/Page requests through the current owner contracts and shared Ideation specialists. Publish the Run Spec inventory, conditional skill map and legacy path compatibility.

## 1.1.0 · 2026-09-13

- Add the Paper–Page integration boundary for Page 0.89: Paper owns the
  journey and composition while the shared Page owns the Page Face, lifecycle,
  Page Runs, Evidence Workspace, release, and CHECK.
- Replace the current Page-local writing identity with the Page-owned
  `rp00_mermaid-structure` / `rpNN_pNN[-pNN]` rule; delegated work remains in
  the owner-native Task lane and historical identities remain read-only.
- Add the Page integration reference for Page-global paragraph addresses,
  Page release, G3/G4 admission, and source/projection boundaries.

## 1.0.3 · 2026-09-08

- Follow Page's paragraph-writing Ticket interface for Content; Paper Evidence/Display pm/pa/pr naming is unchanged.

# CHANGELOG · haipipe-paper

## 1.0.2 · 2026-09-08

- Add the Paper Run naming authority: new Paper-local Evidence/Display Runs
  use semantic `pm-`/`pa-`/`pr-` ids tied to Main/Appendix/Round Page names;
  Page-local Division Writing keeps `rNN_page-division-writing_cNN`.
- Mark `pjNNtNNrNN` Paper Run files as read-only historical dialect; no
  ordinary Paper work renames or bulk-migrates them.

## 0.8.1 · 260907

- P1 is Story: phase figure, one-liner, routing row, `/haipipe-paper story`
  verb (`seed` alias kept), completion check. Routes to `haipipe-paper-story`.

## 0.8.0 · 260907

- Paper folder scaffold rewritten (JL 260907): page groups and `board.md` at
  the paper root (`paper-root: .`), no `0-paperboard/`; `A1-Story` holds the
  pool plus one `Story<NN>-<idea-slug>/` per idea with its roadmap and
  narrative children nested inside; `delivery/` (factory: paper-build.toml,
  latex/, word/) replaces the hand-edited desk room. The room law of 260824 is
  replaced by the delivery law: pages own the words, `delivery/` is regenerated
  whole from their `<page>.tex` fragments and never hand-edited.
- Round folders hold `sent/` · `feedback/` · `released/`.
- Phase figure, Seed/Roadmap/Narrative one-liners, routing row, assembly
  figure and completion checks follow. `Paper-AgreeablePrescription` is the
  first repo on this layout; every earlier layout is grandfathered.

## 0.7.1 · 260904

- Keep the shared Outline presenter at the Page surface and load only its exact
  material refs inside concrete Paper Page phases.

## 0.7.0 · 260904

- Separate family-entry routing from the concrete Page RUN order.
- Replace the active Probe/PageX/workbench-lane model with one shared Outline
  workbench and typed VALUE/CITE/DISPLAY local Results over Supporting/local Runs.
- Add CONTEXT to the Paper Page loop and update status/folder/desk-room
  language to current evidence identities.

## 0.6.0 · 260901
- Active Section Page IDs are full semantic names: `S-<desk>-Main-<section-name>` and `S-<desk>-Appendix-<section-name>`. Reading order belongs in the Board Map, not in an opaque ordinal. Legacy `S<D><NN>` and `SA<NN>` identifiers are archive-only compatibility forms.

## 0.5.0 · 260831
- One letter per B group (JL 260831 "Ba to be Main, Bb to be Appendix, Bc to be Round"): first desk Ba-<desk>-Main · Bb-<desk>-Appendix · Bc-<desk>-Round, a second desk continues at Bd; shared-letter (0.4.x) and combined-group layouts grandfathered. Live: Ba-MISQ-Main/Bb-MISQ-Appendix/Bc-MISQ-Round, Ba-JAMA-IM-Main/Bb-JAMA-IM-Appendix.

## 0.4.1 · 260831
- Desk name keeps its capitals in group folders (JL: "make MISQ capitalized"): Ba-MISQ-Main/-Appendix/-Round; only the arrival letter is lowercase. MISQ board also capitalized the desk in Story03-narrative-MISQ and RD01-MISQ-feedback-20260825; desk rooms (1-misq2026/) and venue bank ids (QBv1-misq) keep their own conventions.

## 0.4.0 · 260831
- Desk layer split three ways (JL 260831 "I want to make Ba-misq into three page groups"): B<x>-<desk>-Main (S<D> units) · B<x>-<desk>-Appendix (SA units) · B<x>-<desk>-Round (RD pages); page tokens unchanged; a combined B<x>-<desk> group is grandfathered.

## 0.3.0 · 260831
- Story ids replace SD/NA (JL 260831 "I don't like the SD... make sure to be self explained"): one A1-Story group holds P0-P3, the venue-free head (Story00-ideation, Story01-seed, Story02-roadmap) plus one Story<NN>-narrative-<desk> per desk (Story03 first); the A2-NA-narrative group and the SD/NA tokens are retired to the grandfathered list.

## 0.2.1 · 260831
- Group-name grammar caught up with the SA ruling (JL 260831): appendix token is `SA` (Section-Appendix), never `A<D>`; the collision rule now retires desk letter `A`; the grandfathered legacy list names `A<D>` instead of `SA`. haipipe-paper-workflow 0.6.1 and haipipe-page-for-section 0.5.5 already carried it; this door was the leftover.

## 0.2.0 — 2026-08-31

- **workflow-phases/ replaces page-types/** (JL 260831: "replace page-types to
  be workflow-phases"): the six journey-phase contracts are now
  `workflow-phases/haipipe-paper-{ideation,seed,roadmap,narrative,section,round}`,
  each carrying its P-number and gates in a `## 🧭 Journey phase` block while
  still owning its `page-type:` key. Venue is a library lane, not a phase, so
  `haipipe-paper-venue` moved to the family top level beside the `venue/`
  bank submodule. Routing table and family map updated; page keys unchanged,
  so no board page changes.

## 0.1.0 — 2026-08-28

- First versioned door (backfilled row): routing, journey figure, assembly
  contract pointer, G6 gate, folder scaffold.
