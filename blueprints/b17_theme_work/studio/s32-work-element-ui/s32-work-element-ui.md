s32 · Work element UI
=====================

**Topic:** every kind of element the work theme draws today, as it draws it, side by side, so the work theme
takes the one look per element that b03 picks for every theme (b03 `s32-element-ui`, JL 261007: "collect all
types of the UI of different types of the element ... so we can unify them"). The versions are shot live from
the frame (`/_board/workbench`) at a work Block, one of its Jobs and one of its Tasks, every Space and every
view, and from the old pages, flagged OLD. Under each element, the planned screen; beside it, its proposed
look: b03's picks, a short why, a green line for what changed and a red line for what is open.

**Feeds:** `reports/` q01_work_ladder (each level's elements) · q03_questions_and_runs (a Run's display and
link); b03 Q08 (one shared base, a theme each) and b03's s32 (its Theme elements frame reads the list below).


Files
-----

```text
s32-work-element-ui/
├── s32-work-element-ui.md          this face: Topic · Feeds · Files · Decided · Open, and the Theme elements
├── build_s32_work_element_ui.py    the builder: --shoot walks the work pages live, then draws the gallery
├── shots/                          one screenshot per element version, facts.json (place, places seen, style,
│                                   and "_buttons": every Runs-panel button met and where)
├── s32-work-element-ui.excalidraw  the gallery: title · Pick · Buttons, then one frame per element, its planned
│                                   screen under it and its "· proposed" frame beside it
└── s32-work-element-ui.png         its preview
```

Shoot (a live host on this SPACE, headless Chrome):
`uv run --no-project --with playwright --with pillow python build_s32_work_element_ui.py --shoot [--base http://127.0.0.1:5851]`
(`--no-project`: the SPACE's own project does not build under uv). Draw only: `python build_s32_work_element_ui.py`
(b03's `studio/_build/make.sh` runs it with the other theme galleries). Preview:
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py
s32-work-element-ui.excalidraw s32-work-element-ui.png 0.12`.

The picture helpers (picture, style line, the pick script, the canvas writer) are imported from b03's
`build_s32_element_ui.py`; the planned screens are drawn by b03's `_build/screens.py`, from b03 s11's work
Block screens (`WORK_BLOCK`), b03 s13's work Task (`level_views.py`) and this Block's s01 Job row. This Block
has no s11 · s12 · s13 of its own, so those are the level designs read.


What the gallery holds
----------------------

```text
element                         versions   on old pages   planned screen
1 · Top tabs                          5          2         b03 s13 · Task › Description
2 · View row (third row)             12          7         b03 s13 · Task › Work Details
3 · Audience Report rows              4          1         b03 s11 · Block › Audience Report
4 · The Space body                   25          7         b17 s01 · Job › Work Details
5 · Tables                            3          2         b03 s11 · Block › Work Details
6 · Rows and cards                    8          6         b03 s11 · Block › Idea Studio
7 · Disk · Runs panel                 5          2         b03 s13 · Task › Runs
8 · Tags and pills                    8          7         (none: no tags)
9 · Page header                       6          3         (none: the planned screens draw no header)
10 · One item's display               5          2         b17 s01 · the Run pop-out
11 · The work theme's own elements   15          3         b03 s13 · Task › Delivery; b17 s01 · Job › Runs
                                     96         42         + 9 proposed shots · 10 planned screens
```

Walked: the work Block b18 in Project-Algorithm-Design (five Questions with report Pages, three Jobs, each a
Task with `scripts/`, `runs/`, `notebooks/`, `CODE_REVIEW.md`), its Job j02 and Task j02 › t01; and one Task of
the raw-data Block (b00 › j51 › t01) that also holds `draft/` and `workflow/`. The old pages: the old work Block
page (`/_board/work-board`: Scope · Task · Check · Delivery and their views), one Run's page on it
(`?task=…&run=…`, from a Run id on a Question row), and a Task's Page workbench page (`/_board/draft`, the old
page's Task Page link). A "distinct" element is one card per look met (its first place, "+N more places"),
told apart by its class and computed style.


Decided
-------

s32-D01 · b03's picks hold for the work theme (261008, b03 s32-D01 · D02 · D05 · D08 · D09): top tabs in the
    D · E look and the view row in the E look, both drawn by the base frame, the work theme giving its words
    only (Block · Job ▾ · Task ▾); every Question row is Question │ Work │ Report with the Question cell as the
    Insight row (label pill "Question N" + state dot, slug, one sentence); Disk inside the Runs panel; no tags;
    every soft Run button named run-<type>-<target>.

s32-D02 · Today's frame already draws the work theme's top tabs, view row, header, Space body, tables, Idea
    Studio rows and Disk · Runs panel in the picked looks at every level (green "kept" on frames 1, 2, 4, 5, 6,
    7, 9); the Block's Audience Report already draws the Insight row and is the proposal for every level.

s32-D03 · Old pages are flagged OLD in red, in a red dashed box (b03 s32-D03): the old work Block page (the
    work theme draws on the frame, `work_theme.py`), its Run page, and the Page workbench page a Task opened.

s32-D04 · Proposed: a Task opens as the Task tab, a hard Run (rNN_) in the frame's pop-out (its card, ticket,
    config, result/ and passes, as s01's Run row); the old Run page and `/_board/draft` stop being
    destinations (frame 10 · proposed, b03 s32-D10).

s32-D05 · Proposed: the work theme's own elements are base tables and rows with its words: the Jobs by series
    (j0N · j1N · j5N), a Job's Tasks with their Plan · Build · Run · Report state, a Task's Plan, Review, Code
    and Notebooks, its Runs by type, its Delivery as cards (Reports · Exports). None needs a look of its own.

s32-D06 · Done (261008, b03 in the base, from this list): a theme's own view wins over a Page view of the
    same name, so a work Task's Audience Report › Draft is the work theme's draft/ list again, not the Page's
    Draft in an iframe; and a theme's Run names take the folder's own tag (run-plan-t01 · run-build-t01 ·
    run-review-code-t01 · run-check-t01), a Task's report button is run-write-t01. Reshot: frames 2 and 7
    and the Buttons frame carry the green notes.


Theme elements
--------------

element · level · Space › view · base or its own and why · drawn today, or GAP: …

- top tabs · all levels · the level row and the six Spaces · base · drawn
- Job ▾ · Task ▾ select · Job, Task · the level row · base, the options grouped by Job series (j0N · j1N · j5N) · GAP: folder names, not grouped
- view row · all levels · every Space with views · base · drawn
- view row · Task · Scope · Plan | Report · Draft | Code · Review · Notebooks | runs by type · base, the work theme's words (b03 s13 1, 1d) · GAP: the Page views (Folder · Evidence · Value · Page Runs · Lanes) are still added to every work Task's row
- Question rows · Block · Audience Report, one row per Question · base (the Insight row, b03 s32-D05) · drawn
- Question rows · Job · Audience Report, the Block's Questions this Job's Tasks feed · base, a filter (s01 Open 2) · GAP: empty, a Job has no reports/ and no filter
- Question rows · Task · Audience Report › Report, Question │ Work │ Report (b03 s13 1b) · base row · GAP: one line, "the report is its face"
- draft list · Task · Audience Report › Draft, the Task's draft/ · its own: the Task's draft notes · drawn (b03 fix, s32-D06) · GAP: lists draft/*.md only; a draft/ holding records/ reads "Nothing here yet"
- Space body · all levels · every Space · base · drawn · GAP: Work Details › Evidence · Value, Runs › Page Runs and Delivery › Lanes embed the old Page workbench in its own look
- table · Block · Work Details, the Jobs · base · GAP: no Job series third row, no state (s01)
- table · Job · Work Details, the Tasks with Plan · Build · Run · Report · base · GAP: title and Runs count only
- table · Task · Work Details › Code · Notebooks (file · bytes) · base · drawn
- Plan · Task · Description › Plan, the face's Plan section · its own: the plan as written · drawn
- Review · Task · Work Details › Review, CODE_REVIEW.md · its own: one link to the review · drawn
- rows · all levels · Idea Studio, one topic per row · base (b03 s32-D06) · drawn
- Job → Task → Run tree · Block · Work Details › Jobs ▾ Tasks (the old page drew it in each Question row) · base rows, opened in place · GAP: no tree on the frame; the Work column lists ids
- Disk · Runs panel · all levels · every Space · base · drawn
- Runs table · Block, Job · Runs, its own soft Runs and ☐ from below its Tasks' hard Runs · base · GAP: no "from below"; the panel offers only run-<type>-<target>
- Runs table · Task · Runs › All · run · build · report (hard rNN_, soft run-) · base, third row by type · GAP: the types are read off disk (All · run); a row opens nothing
- Run pop-out · Run · a hard Run: card · ticket · config · result/ · passes · base pop-out (s01 Run row) · GAP: none; the result shows only on the old Run page
- Delivery cards · Task · Delivery: Reports · Exports, no third row (b03 s13 1b) · base cards · GAP: a Files table and the old Page's Lanes
- Delivery · Block, Job · Delivery, optional: its own and from below · base · GAP: no "from below"
- Job face · Job · Description, jNN_<job>.md (goal · state · task_groups) · base · GAP: no face on disk, "No face file", no button
- tags · all levels · none (b03 s32-D09) · GAP: 1 kind drawn on the frame (the Report cell's rp-tags), 7 on the old pages
- header · all levels · the title line · base · drawn
- one item's display · Task, Run · a Task is the Task tab; a Run opens in the pop-out · base · GAP: a Run's row opens nothing; the old Run page and /_board/draft still answer


Buttons with no Run name
------------------------

Every Runs-panel button met on the work pages (and on the planned screens) that names no run-<type>-<target>,
with the Run proposed for it; also in the drawing's "Buttons with no Run name" frame, built from facts.json.

```text
button                     where                                          proposed Run
Ask a Question             the old work Block page                        run-ask-<qNN>
Review the questions       the old work Block page                        run-review-questions-<bNN>
Add a resource             the old work Block page                        run-add-resource-<slug>
Draw the question map      the old work Block page                        run-draw-<sNN>
Draw                       the old work Block page                        run-draw-<sNN>
Plan a Task                the old work Block page                        run-plan-<tNN>
Review the plan            the old page; planned b03 s13 Task › Descr.    run-review-plan-<tNN>
Build the Task             the old work Block page                        run-build-<tNN>
Review the Task code       the old work Block page                        run-review-code-<tNN>
Run a Task                 the old work Block page                        rNN_<slug> (hard)
Report the Run             the old page; planned b03 s13 Task › A.R.      run-write-<tNN>
Plan the report            the old work Block page                        run-plan-report-<qNN>
Write the report           the old work Block page                        run-report-<qNN>
Check a Task               the old work Block page                        run-check-<tNN>
Check a report             the old work Block page                        run-check-<qNN>
Build the report           the old work Block page                        run-delivery-<qNN>
Rerun                      the old work Block page (a Run card)           a new pass of rNN_<slug>
Context                    a Task's Page workbench page                   run-context-<slug>
Structure revise           a Task's Page workbench page                   run-structure-<slug>
Evidence embed             a Task's Page workbench page                   run-evidence-<slug>
Bind / update citation     a Task's Page workbench page                   run-citation-<slug>
Build                      a Task's Page workbench page                   run-delivery-<target>
Review the shared code     planned b17 s01 · Job › Description, Runs      run-review-code-<jNN>
run-<type>-<target>        the frame · Block › Runs, Job › Runs           its types: Block run-report-<qNN> …;
                           (a generic name, not one Run)                  Job run-plan-<jNN> · run-launch-<jNN>
```

Fixed in the base by b03 (261008, s32-D06), green on the drawing: the work Run names carry the Task's tag
(run-plan-t01 · run-build-t01 · run-review-code-t01 · run-check-t01); a Task's Write the report is
run-write-t01 (was run-report-<qNN>); the planned Release is run-release-<target> (was the design theme's
run-release-j<NN>).


Open
----

1. Pick the work looks the b03 picks leave open (the Pick frame): Space body, tables, rows and cards, header,
   one item's display, the theme's own elements.
2. The GAP lines above are the work theme's code (`servers/workbench-work/work_theme.py`) or the base's
   (`servers/workbench/frame.py`: the Page views, the Runs third row, "from below"); told to design-b03-project
   (261008) so b03's s32 tracks them. No server code is changed here.
3. A work Task's other Page views (Folder · Evidence · Value · Page Runs · Lanes) are the old Page workbench
   in an iframe; Lanes stands where the planned Delivery cards (Reports · Exports) go. Keep them for a Task
   that is a Page, or drop them for a work Task (b03 s13 1d)?
4. The Job ▾ and Task ▾ selects and the Block's Jobs table: group by the Job series read from the face
   (`job_groups:`), never hard-coded (s01 Open 7).
5. A hard Run's display: the frame's pop-out (card · ticket · config · result/ · passes) replaces the old Run
   page; who builds it, the base (every theme's Runs table) or the work theme?
6. The button names in "Buttons with no Run name" are proposals until b03 and the work skills
   (`haipipe-task`, `haipipe-run`) agree them.

(write here, or mark the drawing in red)
