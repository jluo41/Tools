s32 · Labeling element UI
=========================

**Topic:** every kind of element the labeling theme draws, in one gallery, so the UI can be unified (JL 261007,
b03 s32: "collect all types of the UI of different types of the element ... so we can unify them"). Each
element is shown three ways: as the labeling theme draws it today on the frame (`/_board/workbench` at its
Block, Job and Task levels, every Space and view), as its old board and job pages draw it (flagged OLD, red
dashed), and as b03's s11 · s12 · s13 plan it for labeling. Beside each element, a "· proposed" frame: one
look, b03's picks kept, with why, a green line for what changed and a red line for what is open. It is b03's
`s32-element-ui` cut to one theme, and it adds the six elements only labeling has.

**Feeds:** `../../reports/` q01_labeling_ladder · q02_building_scanning_gates · q03_schema_and_handoff; and
b03's s32 (its Theme elements frame reads the list below).


Files
-----

```text
s32-labeling-element-ui/
├── s32-labeling-element-ui.md               this face
├── build_s32_labeling_element_ui.py         the builder: --shoot walks the labeling pages live, then draws
├── shots/                                   one picture per card (<element>__NN.png, proposed__<element>.png)
│                                            and facts.json (each card's place, selector and computed style;
│                                            _buttons: every button met; _links: the job links' answers)
├── s32-labeling-element-ui.excalidraw       the gallery: title · Theme elements · Run names · Pick, then one
│                                            frame per element and its "· proposed" frame
├── .s32-labeling-element-ui.seed.json       the last build, so a rebuild keeps marks
└── s32-labeling-element-ui.png              its preview
```

Shoot (headless Chrome; a live host serves this SPACE):
`uv run --no-project --with playwright --with pillow python build_s32_labeling_element_ui.py --shoot [--base http://127.0.0.1:5851]`.
`--no-project` is needed inside the SPACE, or uv tries to build the SPACE's own environment.
Draw only (what b03's `studio/_build/make.sh` runs): `python build_s32_labeling_element_ui.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s32-labeling-element-ui.excalidraw s32-labeling-element-ui.png 0.2`.

Imported, not copied: b03's `build_s32_element_ui.py` (`PICK_JS`, `picture`, `style_line`, its frame helpers
and the haipipe-studio canvas writer), b03's `_build/run_names.py` (each button's Run name, read off the
server code) and b03's planned screens (`build_ladder_v4.block_views`, `level_views.proposed`,
`level_views.task_proposed`; one screen is sliced out of the labeling row, so a change there shows here on the
next build).

Walked: `examples-6-labeling/Project-Labeling-SafeResponse/tasks/` b61_response_safety (its Block,
j01_building_corpus, and j01's t01_dices350_labeling, a labeling job's Page) and b62_depression_symptoms (its
Block and its labeling job). The old pages: the labeling board page (`/_board/labeling-board`, Guide · Jobs)
and the labeling job page (`/_board/labeling`, Data · Labeling · Quality · Delivery, three views each). Both
jobs sit before the contract, so the job page's Rounds, Definition and Scanning views show their empty state.


What the gallery holds
----------------------

```text
element                                          cards   OLD   planned screen (b03, labeling)
1 · Top tabs                                        5      2    Task › Work Details › Rounds
2 · View row                                       11      4    Task › Work Details · Job › Work Details
3 · Audience Report rows                            1      0    Job › Audience Report › Scored · Block › Audience Report
4 · The Space body                                 23      5    Job › Work Details
5 · Tables                                          2      1    Block › Runs
6 · Rows and cards                                  5      4    Block › Work Details › Jobs
7 · Disk · Runs panel                               4      1    Task › Runs
8 · Tags and pills                                  3      2    (none: no tags)
9 · Page header                                     5      2    (none)
10 · One labeling job's display                     5      2    Task › Description
--- the labeling theme's own elements ---
11 · Job status and the way out                     4      1    Block › Work Details › Jobs
12 · The schema                                     3      0    Job › Description · Block › Description
13 · Label meanings and the G0 gate                 2      1    Task › Work Details › Rounds
14 · Calibration rounds                             3      2    Task › Work Details › Rounds
15 · Corpus preparation and the map                 4      2    Job › Work Details
16 · Quality and delivery                           7      4    Task › Delivery · Task › Audience Report
                                                   87     33    16 proposed frames (15 shot, tags: none)
```


Theme elements
--------------

element · level · Space › view · the base's, or its own and why · drawn today, or GAP: …

- top tabs · every level · the level row and the six Spaces · base · drawn
- top tabs · Task (old page) · Data · Labeling · Quality · Delivery · retires: they are the Task's views ·
  GAP: the job page keeps its own four Spaces while it is the write door
- view row · every level · every Space's views · base · drawn
- view row · Task · Work Details › Preparation · Embedding · Definition · Rounds · Guideline · Test ·
  Evaluation · Audit, then the base's Evidence · Value · base row, the theme's views · GAP: s13 puts
  Preparation in Description and Scan in Work Details (today in Delivery), with a Building | Scanning divider;
  Evidence and Value show the Preparation Run
- Question rows · Block · Audience Report · base (the Insight row) · drawn
- Question rows · Job · Audience Report › Scored · Building (ours vs the dataset's keys) · base row, the
  labeling words · GAP: not drawn; the Job has no reports/ and no t04 scoring Task yet
- Question rows · Task · Audience Report › Report (REPORT.md) · base (a work Task's Report) · drawn
- Space body + Disk · Runs · every level · every Space · base · drawn
- table · Block, Task · Work Details › Labeling; a job's facts · base (wf-table) · drawn
- table · Task (old page) · Data › Preparation steps · base table · GAP: its own steptable
- rows · every level · Idea Studio; Work Details › Jobs · base · drawn
- Runs panel · every level · every Space · base; buttons named run-labeling-<op>-<target> · drawn ·
  GAP: the old job page's panel names none (below)
- tags · Block, Task · the 'open ↗' chip, state spans · none (b03 s32-D09) · GAP: still drawn
- header · every level · the top line · base · drawn
- job status (no item text) · Block, Task · Block › Work Details › Labeling; each Task view · its own: a
  labeling job's status, read only · drawn · GAP: two lists at the Block (Jobs and Labeling), s11 plans one
- way out ↗ · Block, Task · every labeling view · its own until the frame hosts the gates · drawn (the
  link answers 200 since b03's fix, 261008)
- schema · Block (per Job in s12) · Description › Schema · its own: the label, as the file reads · drawn ·
  GAP: per Job in s12 (b15 Q03)
- label meanings + G0 gate · Task · Work Details › Definition · its own: the person's gate · GAP: on the old
  page only; the frame shows status
- calibration rounds · Task · Work Details › Rounds · its own: item text shows only here · GAP: on the old
  page only
- corpus preparation + map · Task (s12: the Job's t01 items) · Work Details › Preparation · Embedding · base
  table + its own map · GAP: on the old page only
- guideline · Task · Work Details › Guideline · its own: the versions G_NN · GAP: on the old page only
- test · evaluation · audit · Task · Work Details (Scanning) · base table · GAP: empty; the engine's Scanning
  Runs are not built yet
- handoff · scan · final labels · Task, rolled up to Job and Block · Delivery · base rows, the handoff its own
  (signed) · drawn as status only · GAP: no Job or Block roll-up yet
- Idea Studio · every level · Idea Studio · base (b03 s32-D06) · drawn
- the labeling board page · old · `/_board/labeling-board` · retires: Block › Work Details · old page
- the labeling job page · old · `/_board/labeling` · retires last: it is the write door · old page


Buttons with no Run name
------------------------

Read off the live pages (`shots/facts.json` `_buttons`) and b03's planned screens, named by b03's
`run_names`; the frame's Run names frame lists the same. The rule is the theme's own: a view's button is
`run-labeling-<view>-<job>`; an engine step inside a view is a pass of that view's Run; a round is its own
Run (`run-labeling-round-<NN>`).

```text
button (its words)            where                          engine op               proposed Run
Normalize source              job page › Data › Preparation  source-normalize        run-labeling-corpus-<corpus>
Choose labeling unit          job page › Data › Preparation  unit-recipe             run-labeling-corpus-<corpus>
Create candidate items        job page › Data › Preparation  unit-materialize        run-labeling-corpus-<corpus>
Check candidate items         job page › Data › Preparation  unit-check              run-labeling-corpus-<corpus>
Reserve source groups         job page › Data › Preparation  initial-group-reserve   run-labeling-corpus-<corpus>
Copy setup request            job page › Data › Preparation  —                       run-labeling-corpus-<corpus>
Discuss the label meanings    job page › Labeling › Definition definition-discussion run-labeling-definition-<job>
Draw one round                job page › Labeling › Rounds   round-prepare           run-labeling-round-<NN>
You label one round           job page › Labeling › Rounds   human-calibration       run-labeling-round-<NN>
Edit the schema               planned (s12, Job)             —                       run-labeling-schema-<jNN>
Score against the keys        planned (s12, Job)             —                       run-labeling-score-<jNN>
Render the report             planned (s13, Task)            —                       run-labeling-report-<job>
```

Clashes, fixed by b03 in `run_names.DRAWN` (261008; the drawing shows them green once they read so):

- "Set up the job" read `run-add-<jNN>`; now `run-labeling-contract-<job>` (Data › Contract).
- "Build a map" read `run-draw-<sNN>`; now `run-labeling-embedding-<job>` (Data › Embedding).
- "Measure" read `run-labeling-evaluation-<job>`; now `run-labeling-round-<NN>` (a pass of the round).

The 17 engine steps not built yet (test-reserve … dstar-materialize) show no button today; when built, each
takes its view's Run by the same rule (`OP_RUN` in the builder).


Decided
-------

s32-D01 · Done (261008): b03's picks hold for the labeling theme: top tabs in the D · E look, the view row
    in the E look, the Question cell as the Insight row, Disk inside the Runs panel, no tags (b03 s32-D01,
    D02, D05, D08, D09). The labeling theme gives the words, and the layout of its own elements only.
s32-D02 · Done (261008): the levels are shot live from b61 and b62 in Project-Labeling-SafeResponse; the
    labeling board page and the labeling job page are flagged OLD (`old_reason`, read off the code: the
    theme has `labeling_theme.py`). The job page is reached with path= starting "/", the only form its route
    accepts.
s32-D03 · Done (261008): each element shows b03's planned labeling screen, sliced out of b03's own row
    builders, so the gallery follows s11 · s12 · s13 on every rebuild (b15 has no s11 – s13 of its own).
s32-D04 · Proposed (261008): six elements are labeling's own (11 – 16). The job page's views (Definition
    with its G0 gate, Rounds, Guideline, Preparation and its map) carry over into the frame's Task views in
    base rows and tables (JL: carry over what exists); the gated actions stay engine-checked through
    `POST /_board/labeling/act`.
s32-D05 · Proposed (261008): the job page retires last, once the frame hosts its gated actions; until then it
    is the one write door and keeps its own four Spaces.
s32-D06 · Proposed (261008): every labeling button is named `run-labeling-<view>-<job>`, an engine step a pass
    of its view's Run and a round its own Run (the list above). The 12 names wait for JL (they go into
    `labeling_theme.py` RUN_NAMES); the three clashes are fixed in b03's `run_names.DRAWN` (261008).
s32-D07 · Done (261008, b03): both job links answer 200: `generated_page_url` in `labeling.py` accepts path=
    with or without a leading "/" (test in haipipe-page/tests/test_labeling.py); reshot, the title frame's
    link lines are green.


Open
----

1. Pick one look per element: the Pick frame lists each one, b03's picks in green, the proposal in red.
2. Gaps 3 – 9 and the 12 Run names belong in `labeling_theme.py` (its views and RUN_NAMES); they wait for
   JL (b03, 261008). Server code is not changed from this topic.
3. Job › Description has no Run and no face: `j01_building_corpus/` holds no `j01_building_corpus.md`.
4. Job › Audience Report draws no rows; s12 plans ours vs the dataset's keys from t04's scoring Runs.
5. Task › Work Details mixes the labeling views with the base's Evidence · Value, which show the Preparation
   Run; s13 plans Preparation in Description and Scan in Work Details with a Building | Scanning divider.
6. The Block lists its jobs twice: Work Details › Jobs (the jNN_ folders) and › Labeling (the jobs).
7. Tags: the 'open ↗' chip and the state spans go (b03 s32-D09); the state becomes a word.
8. The 12 buttons above have no Run name (the three clashes are fixed, 261008).
9. Where the schema lives: the Block today, per Job in s12 (b15 Q03).

(write here, or mark the drawing in red)
