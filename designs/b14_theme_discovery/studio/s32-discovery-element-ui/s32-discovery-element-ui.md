s32 · Discovery element UI
==========================

**Topic:** every kind of element the discovery theme draws, in one gallery, so the UI can be unified (JL
261007, b03 s32: "collect all types of the UI of different types of the element ... so we can unify
them"). Each element is shown three ways: as the discovery theme draws it today on the frame
(`/_board/workbench` at its Block, Job and Task levels, every Space and view), as its old pages draw it
(flagged OLD), and as b03's s11 · s12 · s13 discovery rows plan it. Beside each element, a "· proposed"
frame: one look, b03's picks kept, with why, a green line for what changed and a red line for what is
open. It is b03's `s32-element-ui` cut to one theme, and it adds the elements only discovery has, and
every discovery button with the Run name it needs.

**Feeds:** `../../reports/` q01_discovery_ladder · q02_papers_citations_bib · and b03's s32, which
reads the list under the heading below.


Files
-----

```text
s32-discovery-element-ui/
├── s32-discovery-element-ui.md              this face
├── build_s32_discovery_element_ui.py        the builder: --shoot screenshots each element live, then draws
├── shots/                                   one picture per card (<element>__NN.png, proposed__<element>.png)
│                                            and facts.json (each one's page, selector and computed style;
│                                            "_buttons": every button met and where)
├── s32-discovery-element-ui.excalidraw      the gallery: title · Theme elements · Run names · Pick, then one
│                                            frame per element and its "· proposed" frame
├── .s32-discovery-element-ui.seed.json      the last build, so a rebuild keeps marks
└── s32-discovery-element-ui.png             its preview
```

Shoot (headless Chrome; a live host serves this SPACE):
`uv run --no-project --with playwright --with pillow python build_s32_discovery_element_ui.py --shoot [--base http://127.0.0.1:5851]`.
`--no-project` is needed inside the SPACE, or uv tries to build the SPACE's own environment.
Draw only: `python build_s32_discovery_element_ui.py` (a Python with Pillow, such as the SPACE's
`.venv`), then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s32-discovery-element-ui.excalidraw s32-discovery-element-ui.png 0.2`.
b03's `studio/_build/make.sh` runs the draw step with the other `s32-*-element-ui` builders.

The drawing helpers (`PICK_JS`, `picture`, `style_line`, b03's frame helpers, the haipipe-studio canvas
writer) are imported from b03's `build_s32_element_ui.py`. b14 has no s11 · s12 · s13 of its own, so
the planned screens are the discovery rows of b03's s11-block-variants, s12-job-variants and
s13-task-variants (`build_ladder_v4.py` `VIEW_FAMILY["discovery"]`, `level_views.py`
`JOB_FAMILY_VIEWS["discovery"]`, `TASK_VARIANT_VIEWS["discovery Task"]`), drawn by b03's own
`wireframe()`; a change there shows here on the next build.

What is shot: the discovery Block with the most on disk,
`examples-2-analysis/Project-ExpAnalysis-SMSEngagement/discoveries/b01_sms_engagement_evidence/` (5
Jobs, 10 Tasks, 51 Paper Runs), at its Block, its Job `j01_smsr_literature_inquiry` and that Job's Task
`t03_novelty_check` (the one with a typed record, `verdict.md`). No discovery Block on disk registers a
Question, so the Question rows come from a small placeholder Block, written to a temp folder, rendered
by the SPACE's own Python through the discovery theme, and shown on the host's origin. The old pages:
the Discovery board page (`/_board/discovery-board`, still served), the Page workbench page a Task
link opens (`/_board/draft`), and the file route a Result Card opens through.


What the gallery holds
----------------------

```text
element                                        cards   OLD   planned screen
1 · Top tabs                                     5      2    s13 · Task › Work Details › Papers
2 · View row                                    13      3    s12 · Job › Work Details
3 · Audience Report rows                         6      1    s11 Reports · s12 Audience Report · s13 Table
4 · The Space body                              23      5    s12 · Job › Description
5 · Tables                                       9      3    s11 · Block › Runs
6 · Rows and cards                               7      3    s11 · Block › Jobs
7 · Disk · Runs panel                            7      2    s13 · Task › Runs
8 · Tags and pills                               8      2    (none: no tags)
9 · Page header                                  5      2    (none: the planned screens draw no header)
10 · One item's display                          4      2    s13 · Task › Papers
--- the discovery theme's own elements ---
11 · Paper rows                                  5      2    s13 · Task › Papers
12 · Sub-question rows                           3      1    s12 Work Details · s11 Jobs
13 · Synthesis                                   5      1    s13 Reading · Table
14 · BibTeX                                      4      1    s13 · s11 · s12 Delivery
15 · Scope and resources                         7      2    s11 Resources · s13 Description · s12 Description
16 · Intake: screened candidates                 0      0    s13 · Task › Work Details › Intake
                                               111     32    14 proposed shots · 16 proposed frames
```


Theme elements
--------------

element · level · Space › view · from the base, or the theme's own and why · drawn today (GAP = open)

- top tabs · every level · the level row and the six Spaces · the base · drawn · GAP: the Job and
  Task selects read folder names (`j01_smsr_literature_inquiry`)
- view row · Block, Task · every Space with views · the base · drawn · GAP: the Job draws no third
  row; s12 plans Description: Inquiry · Resources, Work Details: All · Search · Review · Synthesize,
  Runs: All · plan · delivery · from below
- Question rows · Block, Job · Audience Report › Questions; Job › Audience Report · the base
  (Insight's row) · GAP: `_questions` draws its own older cell (a Q01 tag, the whole question, the
  hypothesis); no Block on disk registers a Question
- Question rows (divisions) · Task · Audience Report › Table · the base row: division │ papers read │
  state (s13) · GAP: not drawn; today Synthesis · Draft
- Reports folds · Block · Audience Report › Reports · the base folding row · drawn
- Space body and Disk · Runs · every level · every Space · the base · drawn
- table · every level · Block facts, Papers, Tasks, Citations, Runs, Task Face · the base · drawn
- folding row · Block, Task · Resources, Reports, Synthesis, Notes · the base row · GAP: an open
  fold shows raw markdown in a pre, not the Page reader
- Runs panel · every level · every Space · the base; run types from the Workbench Table, named by
  `RUN_NAMES` · drawn
- tags · every level · Job, Task and Run ids, a Question id, a state · none (b03 s32-D09) · GAP: chip,
  kind, st-ok, st-warn and rp-tags drawn
- header · every level · the top line · the base · drawn
- paper row · Block, Task · Work Details › Papers, Citations · its own: a Paper Run is read by depth,
  claim and citation, which no other theme has · GAP: s13's paper · depth · claim · cite and papers
  grouped by role (Q02) not drawn; today 7 columns with a readout under each title
- Result Card · Task (pop-out) · a paper row's link · its own: one Paper Run's card, facts and Bib
  entry · GAP: it opens through the old board page's file route, not the base reader
- sub-question row · Block, Job · Work Details › Tasks; Job › Work Details · the base table with
  discovery's columns (type · Runs · to verify · synthesis) · GAP: s12's fold-open to the papers and
  its row by specialist
- synthesis · Task · Audience Report › Synthesis · its own: the typed record (summary · verdict ·
  landscape) · GAP: s13's Table · Reading not drawn
- BibTeX · Block (Task, Job planned) · Delivery › BibTeX · its own: the merged Evidence Bib · GAP:
  the Task's and the Job's Delivery show no Bib
- Scope · Admission · Records · Task · Description · its own: discovery.yaml's question, type and
  rule · GAP: today the base's Face · Folder
- Inquiry face · Job · Description › Inquiry · its own: `jNN_<inquiry>.md` (s12) · GAP: empty, no
  face on disk
- Intake · Task · Work Details › Intake · the base table of screened candidates (s13) · GAP: not
  drawn at any level
- Idea Studio · every level · Idea Studio · the base (b03 s32-D06) · drawn (this Block has no studio/)
- the Discovery board page · old · `/_board/discovery-board` · retires: the frame draws every level ·
  old page
- the Page workbench page · old · `/_board/draft`, from a Task link · retires: a Task is the Task tab
  · old page


Run names
---------

Every frame button already carries a Run name: `discovery_theme.RUN_NAMES` names the theme's (run-ask,
run-review-questions, run-report, run-check, run-find-papers, rNN_ for Read a paper, run-synthesize,
run-verify-citation, run-review, run-add-resource) and the base names run-draw, run-face and
run-delivery. The buttons with no Run name yet, with the name proposed:

```text
button              where today or planned             proposed Run
+ Add drawing       old board page (Scope › RoadMap)   run-draw-<sNN>              (the base's)
Save resource       old board page (Scope › Resources) run-add-resource-<slug>     (the theme's, named today)
Rerun               old board page (a Run card)        rNN_<author><year>_<subject> (a new pass)
Open a Job          planned s11 Block                  run-add-<jNN>               (the base's)
Plan its Tasks      planned s12 Job                    run-plan-<tNN>              (the base's)
Add a Task          planned s12 Job                    run-add-<tNN>               (the base's)
Check a Task        planned s12 Job · s13 Task         run-check-<tNN>             (the base's)
Update the inquiry  planned s12 Job                    run-face-<jNN>              (the base's)
Scope the Task      planned s13 Task                   run-face-<tNN>              (the base's)
Structure revise    planned s13 Task                   run-structure-<slug>        (the base's)
Section revise      planned s13 Task                   run-section-<slug>          (the base's)
Export BibTeX       planned s11 · s12 · s13            run-delivery-<target>       (the base's)
Build the article   planned s13 Task                   run-delivery-<target>       (the base's)
Add a paper         planned s11 Block (and Guide)      run-add-paper-<key>         discovery's own
Freeze the rule     planned s13 Task                   run-freeze-admission-<tNN>  discovery's own
Admit a candidate   planned s13 Task                   run-admit-<candidate>       discovery's own
```

On the frame, `<tNN>` and the like take the folder's own number (run-plan-t03).

`+ New Run` has no name of its own: it asks for a run type and takes that type's name. The Page
workbench's own buttons (where a Task opens today) are the Page theme's, not listed here.


Decided
-------

s32-D01 · Done (261008): b03's picks hold for the discovery theme too: top tabs in the D · E look,
    the view row in the E look, the Question cell as the Insight row, Disk inside the Runs panel, no
    tags (b03 s32-D01, D02, D05, D08, D09). The discovery theme gives the words, and the columns of
    its own elements only.
s32-D02 · Done (261008): the ladder is shot live from the discovery Block with the most on disk
    (SMSEngagement), at one Job and one Task; the Question rows from a placeholder Block until a
    discovery Block registers a Question. The old pages are flagged OLD (`old_reason`).
s32-D03 · Done (261008): each element also shows its planned screen, drawn from b03's s11 · s12 ·
    s13 discovery rows by b03's own wireframe(), so the gallery follows the level designs on every
    rebuild.
s32-D04 · Proposed (261008): six elements are the discovery theme's own (11 – 16): paper rows,
    sub-question rows, synthesis, BibTeX, scope and resources, intake. Each is a base table, row or
    fold with discovery's columns; none needs a look of its own.
s32-D05 · Proposed (261008): a paper opens in the frame's pop-out (its Result Card, read by the base
    reader), and a Task opens as its own Task tab; the Discovery board page, the file route and the
    Page workbench page stop being destinations.
s32-D06 · Done (261008, b03's ruling): where the base already names a button, discovery reuses that
    name, so one button has one name in every theme (run-add, run-plan, run-check, run-face,
    run-structure, run-section, run-delivery, run-draw). Only discovery's own buttons get new names:
    run-add-paper-<key>, run-freeze-admission-<tNN>, run-admit-<candidate>. On the frame a name takes
    the folder's own number (run-plan-t03). See the Run names list above.


Open
----

1. Pick one look per element: the Pick frame lists each one, b03's picks in green, the rest red.
2. `discovery_theme._questions` draws its own older Question cell; it should call the base's
   `question_cell()` (b03 s32-D05).
3. The theme still draws tags: `chip` for Job, Task and Run ids, `kind` for a Question id, `st-ok` /
   `st-warn` for a state, `rp-tags` (b03 s32-D09 says none).
4. The Job level has no third row and an empty Description: s12's Inquiry · Resources and its
   specialist row (Search · Review · Synthesize) are not drawn, and no Job has a
   `jNN_<inquiry>.md` face (s01 Open 1).
5. The Task's Description is the base's Face · Folder, not s13's Scope · Admission · Records; its
   Audience Report is Synthesis · Draft, not s13's Table · Reading; its Work Details has no Intake.
6. A Result Card opens through the old board page's file route (`/_board/discovery-board?show=…`);
   the base reader (`/_board/page`) instead.
7. The Bib shows only at Block › Delivery › BibTeX; the Task's and the Job's Delivery show none.
8. An open synthesis or note is raw markdown in a pre, not the Page reader.
9. The Job and Task selects read folder names; a short label through the base's option() hook.
10. The 16 unnamed buttons (Run names, above) need their names in `RUN_NAMES` or the Workbench Table
    (s32-D06).

These are the discovery theme's code (`servers/workbench-discovery/discovery_theme.py`), not the
base. They wait for JL (b03, 261008); no server code was changed here.

(write here, or mark the drawing in red)
