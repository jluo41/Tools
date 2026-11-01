---
mindmap: 1
title: s01 · Displays as they are: 260 units against six wants · structured
built: from-topic .
---

# s01 · Displays as they are: 260 units against six wants <!-- root #8cc74b -->

**Stage:** explore

- For <!-- @for #f78806 -->
  - a deck, and an inventory of every … <!-- @for/0 #7010dc -->
    a deck, and an inventory of every display unit on disk measured against six wants, for whoever decides what a display should be
- Delivery type <!-- @delivery-type #58a44f -->
  - data <!-- @delivery-type/0 #a17c9a -->
- Topic <!-- @topic #7e13bd -->
  - What a display is today, measured on … <!-- @topic/0 #d68aa8 -->
    What a display is today, measured on disk on 261016, so JL can decide what display should be.
  - A display unit is one folder holding … <!-- @topic/1 #d4fe67 -->
    A display unit is one folder holding one figure or table (`Display<N>-<slug>/`, or any folder whose README has an `accepted:` line).
  - We walked WellDoc-SPACE, DrFirst-SPACE, Physician-SPACE, REACH-SPACE and … <!-- @topic/2 #571bd4 -->
    We walked WellDoc-SPACE, DrFirst-SPACE, Physician-SPACE, REACH-SPACE and Knowledge-SPACE (not `.git`, `.venv`, `node_modules` or each SPACE's `Tools` link) and found 335 units: 263 named `Display<N>-...` (the "about 260" of the b34 face), 67 older ones whose name has a section prefix before `Display<N>`, and 5 with another name.
  - We then scored the six wants from … <!-- @topic/3 #b05f77 -->
    We then scored the six wants from the b34 face (`board.md`, Topic) against the 335 rows.
  - A home is where a unit lives: … <!-- @topic/4 #c005bc -->
    A home is where a unit lives: a Page Result payload (`results/<run>/payload/<unit>/`), the old display lane (`evidence/display/`, `display/`, `displays/`), or a delivery copy (`delivery/latex/displays/`).
- Feeds <!-- @feeds #ffe8e9 -->
  - `board.md` (the six wants and the Close … <!-- @feeds/0 #eb00d6 -->
    `board.md` (the six wants and the Close of b34); no report yet (`reports/` is empty).
- Files <!-- @files #6ce6c5 -->
  - [py] [build_s01_display_inventory.py](build_s01_display_inventory.py) <!-- @files/0 #0b52ea -->
  - delivery/ <!-- @files/1 #404761 -->
  - [csv] [inventory.csv](inventory.csv) <!-- @files/2 #bf378a -->
  - [md] [s01-display-inventory.md](s01-display-inventory.md) <!-- @files/3 #053bda -->
- Findings <!-- @findings #ca9b7e -->
  - **The population.** 335 units <!-- @findings/0 #71e9dc -->
  - Of the 93 payload units, 23 (Physician … <!-- @findings/1 #d9a91a -->
    Of the 93 payload units, 23 (Physician 22, REACH 1) live under a work Run (`work/.../runs/<run>/result/units/.../payload/`), not under a paper Page. So a fourth address already exists.
  - **The six wants, scored.** Counts are over … <!-- @findings/2 #9dbb5f -->
    **The six wants, scored.** Counts are over all 335 rows unless said. "Source units" are the 239 that are not delivery copies.
  - **Reproducible from recipe and data: partly met, … <!-- @findings/3 #4a6562 -->
    **Reproducible from recipe and data: partly met, 131 of 335.** A unit counts when it has both a `recipe/` folder
  - and an `intake/` folder (88 old lane, … <!-- @findings/4 #6e8d64 -->
    and an `intake/` folder (88 old lane, 43 payload, 0 delivery copies). 165 have a recipe or a legacy `source/` folder. 170 have no recipe at all: they are a carried asset (a PDF or `table-body.tex`) with a README saying so. Examples: met, `Physician-SPACE/_WorkSpace/paper-preview/Paper-AgreeablePrescriptionDiscretion-260928/Bb-MISQ-Appendix/S-MISQ-Appendix-B-Validation/results/re-display-01_model-performance/payload/Display1-model-performance`; absent, `DrFirst-SPACE/examples-4-learning/Project-ExpLearn-SMSDesign/paper/Paper-TestToLearn-MS2026/j01_v0429_mansci/t26_regression-robustness/results/run-display-0930-main-effects/payload/Display1-table-main-effects-260516` (README: "carried submitted asset, not accepted").
  - **Names the evidence it is built on: … <!-- @findings/5 #ee96bb -->
    **Names the evidence it is built on: mostly absent, 57 of 335 name any data, 0 say `built_on`.** 29 have an
  - `intake/manifest.yaml` with an origin (all Physician), 28 … <!-- @findings/6 #63ee45 -->
    `intake/manifest.yaml` with an origin (all Physician), 28 have a README `source:` line (all DrFirst), 278 name nothing. `built_on` (the field that would point to evidence cards) is in zero units; the field is new. By home, payload units do best (42 of 93 name a source), the old lane 15 of 146, delivery copies 0 of 96. Example: `Physician-SPACE/examples-3-nlp/Project-LLMRec-Physician/work/b01_physician_ground_truth/j03_physician_directory_pages/t04_virtual_site_three_platforms/runs/r46_package_frozen_report_displays/result/units/E55-DISPLAY-release-summary/payload/t04_virtual_site_three_platforms-Display1-release-summary` (manifest names its origin).
  - **One home vs duplicates: absent as a … <!-- @findings/7 #e9e300 -->
    **One home vs duplicates: absent as a rule, 134 source units have a delivery copy.** All 96 delivery copies have a
  - source twin (same name, same paper), so … <!-- @findings/8 #c8ec5f -->
    source twin (same name, same paper), so delivery is already only a copy, but 134 sources are matched to them (some sources have several copies) and 105 of the 239 source units have none yet. Worse, the source itself is split: of 165 distinct (paper, unit name) pairs among source units, 52 exist in two or more source homes (for example the old lane and a payload folder, or a live paper and its `_old/` or `paper-preview/` twin), and 62 names have 2+ source copies. Example: `DrFirst-SPACE/.../Paper-PhyTraitNudging-IS/delivery/latex/displays/S-ISR-Appendix-C-Balance-and-Selection/Display1-balance-pvalues` copies `.../Bb-ISR-Appendix/S-ISR-Appendix-C-Balance-and-Selection/draft/evidence/display/Display1-balance-pvalues`.
  - **A person's acceptance recorded: nearly absent, 3 … <!-- @findings/9 #ebc9cf -->
    **A person's acceptance recorded: nearly absent, 3 rows, 1 display.** 3 READMEs carry `accepted: ✅`, and they are
  - the same unit three times: `Display1-hero-concept` ("JL … <!-- @findings/10 #5668f0 -->
    the same unit three times: `Display1-hero-concept` ("JL 260907 · in chat: OK, 这很好", in the paper-preview copy, the live paper's `_archive/legacy-outline-evidence/` copy, and an `_old/` copy). 93 units have an open `accepted: ⬜` line (44 say only "review"; 24 say JL ticks after the values are checked against a Run receipt), and 239 have no `accepted:` line at all, including all 102 DrFirst units and all 96 delivery copies. The only `accepted: ✅` unit also sits in archive or `_old/` folders, so no live display is accepted today.
  - **Linked from the sentence that cites it: … <!-- @findings/11 #a8da45 -->
    **Linked from the sentence that cites it: partly met, by name only.** 320 of 335 units are named somewhere in
  - their own paper (plans, logs, Page text); … <!-- @findings/12 #3e163c -->
    their own paper (plans, logs, Page text); 204 are named in a Page face or draft (not a log, outline table or README). That is a text mention, not a box on the sentence and not a card. 103 READMEs have a `serves:` line (the section that prints it), the only backlink the unit itself carries. Example: the plan table `DrFirst-SPACE/.../Paper-SuitableMessageForRx-JAMANO/Ba-JAMANO-Main/S-JAMANO-Main-3-Results/outline/S-JAMANO-Main-3-Results-evidence-items.md` lists Display1 to Display5 as `DISPLAY` items, each with the claim sentence it supports.
  - **A missing display flagged as a proposal: … <!-- @findings/13 #f8be02 -->
    **A missing display flagged as a proposal: partly present, never as a proposal.** 15 `*-evidence-items.md`
  - tables (WellDoc 11, DrFirst 4) hold 43 … <!-- @findings/14 #b14b6b -->
    tables (WellDoc 11, DrFirst 4) hold 43 `DISPLAY` item rows. 24 carry `✅ preview.pdf` and an empty `⬜` acceptance mark; the 19 WellDoc rows name a unit (`unit Display1-...`), but only 6 of the 43 rows point at a unit folder that exists under that exact name. So a planned display is visible in plain tables, and some are not built, but nothing says "proposed by evidence" and nothing can be ticked to create it. Only 4 unit READMEs use the word "proposed" (a candidate render waiting), 8 say "Open needs". Example: `WellDoc-SPACE/examples-3-pred/Proj21-CGM-Pred/paper/Paper-CGMtoHbA1c/Bb-DC-Appendix/S-DC-Appendix-C-Supplementary-Figures/draft/S-DC-Appendix-C-Supplementary-Figures-evidence-items.md` (E01 and E02 `DISPLAY` rows name units `Display1-tir-...` and `Display2-bootstrap-...`).
  - **Not covered, said plainly.** "Names its data" … <!-- @findings/15 #ba5a04 -->
    **Not covered, said plainly.** "Names its data" read only manifests and README `source:` lines; a recipe script that reads a CSV by path would not count. "Linked" is a text search for the unit name, so a slug mentioned in a log counts as less than a box. 107 of the 335 rows are archived or `_old/` copies (96 delivery copies overlap that count partly); the same counts over the 147 live, non-delivery units are: recipe + intake 71, names a source 51, `accepted: ⬜` 65, 0 accepted, named in a Page 88. Knowledge-SPACE has no display units at all.
- Decided <!-- @decided #55615a -->
  - (none yet: a decision is one line, … <!-- @decided/0 #11353b -->
    (none yet: a decision is one line, s01-D01 · <what was decided> (<who> <date>))
- Open <!-- @open #cf9b77 -->
  - Should the 3 homes collapse to one? … <!-- @open/0 #4aee83 -->
    Should the 3 homes collapse to one? 96 delivery copies are fine as copies; the old lane (146) and the work-Run
  - payloads (93) both hold sources <!-- @open/1 #e4ac40 -->
    payloads (93) both hold sources. Which is the single home: `display/` in the Task, or the Page Result payload?
  - What counts as a display's data source: … <!-- @open/2 #1f6f95 -->
    What counts as a display's data source: a manifest origin, a README `source:` line, or only `built_on` evidence
  - cards? <!-- @open/3 #82ccd7 -->
    cards? Today 57 of 335 name one, so the strict rule makes 278 units "unsourced" on day one.
  - Do the 170 carried assets with no … <!-- @open/4 #03cfd5 -->
    Do the 170 carried assets with no recipe (old PDFs and `table-body.tex` from submitted papers) have to be rebuilt,
  - or are they allowed as "carried, accepted … <!-- @open/5 #4d132e -->
    or are they allowed as "carried, accepted by JL" units, since they are what was already sent?
  - Acceptance: no live display has a ✅ <!-- @open/6 #62fadb -->
    Acceptance: no live display has a ✅. Does JL tick each of the 147 live units, tick per paper at CHECK, or accept
  - the ones a paper already submitted in … <!-- @open/7 #1db9e2 -->
    the ones a paper already submitted in one pass?
  - Do the 107 archived and `_old/` units … <!-- @open/8 #da0c56 -->
    Do the 107 archived and `_old/` units stay in the count, or leave the display inventory (87 are old-lane
  - copies, and the only 3 accepted rows … <!-- @open/9 #375fe5 -->
    copies, and the only 3 accepted rows are all in them)?
  - The 43 planned `DISPLAY` rows in the … <!-- @open/10 #abfaac -->
    The 43 planned `DISPLAY` rows in the evidence-items tables: should they be read as proposals (a missing unit
  - flagged for JL to tick), replacing those … <!-- @open/11 #6ec271 -->
    flagged for JL to tick), replacing those tables, or should the evidence skill's `proposals.md` own them?
  - Agree its **For:** line and **Delivery type:** … <!-- @open/12 #2c67d5 -->
    Agree its **For:** line and **Delivery type:** (data), proposed by the agent 261030?
