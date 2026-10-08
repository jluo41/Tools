s32 · Cowork element UI
=======================

**Topic:** every kind of element the cowork theme draws, in one gallery, so the UI can be unified (JL
261007, b03 s32: "collect all types of the UI of different types of the element ... so we can unify
them"). Each element is shown three ways: as the cowork theme draws it today on the frame
(`/_board/workbench` at its Block, Job and Task levels, every Space and view), as its old CoWork page
draws it (`/_board/cowork-board`, flagged OLD in a red dashed box), and as b03's s11 (Block) and s12
(Job) cowork rows plan it. Beside each element, a "· proposed" frame: one look, b03's picks kept, with
why, a green line for what changed and a red line for what is open. It is b03's `s32-element-ui` cut
to one theme, and it adds the four elements only cowork has.

**Feeds:** `../../reports/` q01_cowork_ladder · q02_waiting_and_drafts · q03_cowork_delivery · and
b03's s32 (its Theme elements list, read from the heading below).


Files
-----

```text
s32-cowork-element-ui/
├── s32-cowork-element-ui.md              this face
├── build_s32_cowork_element_ui.py        the builder: --shoot walks the cowork pages live, then draws
├── cowork_fixture.py                     the placeholder cowork Block the shoot serves (no real one on disk)
├── shots/                                one picture per card (<element>__NN.png, proposed__<element>.png)
│                                         and facts.json (each one's page, selector, style; the walk's buttons)
├── s32-cowork-element-ui.excalidraw      the gallery: title · Theme elements · Buttons · Pick, then one
│                                         frame per element and its "· proposed" frame
├── .s32-cowork-element-ui.seed.json      the last build, so a rebuild keeps marks
└── s32-cowork-element-ui.png             its preview
```

Shoot (headless Chrome; the SPACE's host at http://127.0.0.1:5851):
`uv run --no-project --with playwright --with pillow python build_s32_cowork_element_ui.py --shoot [--base http://127.0.0.1:5851]`.
`--no-project` is needed inside the SPACE, or uv tries to build the SPACE's own environment.
Draw only (what b03's `studio/_build/make.sh` runs): `python build_s32_cowork_element_ui.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s32-cowork-element-ui.excalidraw s32-cowork-element-ui.png 0.2`.

No cowork Block is on disk in this SPACE (261008). So `--shoot` writes `cowork_fixture.py`'s Block
(the cowork theme's test Block, plus a waiting Job, soft Runs, a delivery/ and a Page Task
`t01_protocol/`; placeholders only) to a temp folder, starts a second host on it (the same
`serve.py`, a free port), shoots the frame and the old CoWork page from it, then stops it. The
SPACE's host gives the old page's every-Project list and the base's Question row on a real Block
(this Block, b13, which the frame draws with the base's rows). The walk covers every Space and view
of the Block, Job j01 (with a Task), Job j03 (done, no Task) and Task t01, and all 13 views of the old
page: 63 pages. The helpers (pick script, picture, style line, canvas writer) are imported from b03's
`build_s32_element_ui.py`; the planned screens are drawn by b03's own ladder helpers
(`build_ladder_v4.wireframe`, `level_views`), so they follow s11 · s12 on every rebuild.


What the gallery holds
----------------------

```text
element                                      cards   OLD   planned screen (b03's cowork rows)
1 · Top tabs                                   5      1    s12 · Job › Description
2 · View row                                  12      3    s12 · Job › Work Details
3 · Audience Report rows                       5      2    s11 · Block › Reports · s12 · Job › Audience Report
4 · The Space body                            23      5    s11 · Block › Jobs
5 · Tables                                    11      3    s11 · Block › Runs
6 · Rows and cards                             6      5    s11 · Block › Studio
7 · Disk · Runs panel                          7      2    s12 · Job › Runs
8 · Tags and pills                             6      5    (none: no tags)
9 · Page header                                6      3    (none: the planned screens draw no header)
10 · One item's display                        6      2    s12 · Job › Work Details
--- the cowork theme's own elements ---
11 · A Job's state: waiting on · since · next  5      2    s12 · Job › Description · s11 · Block › Jobs
12 · Timeline, checklist, emails, meetings     6      2    s12 · Job › Work Details
13 · People, resources, files                  6      2    s11 · Block › People · Resources
14 · Waiting on, drafts, done (was Check)      8      4    s11 · Block › Jobs · Delivery · s12 · Job › Delivery
                                             112     41    17 planned screens · 13 proposed shots · 14 proposed frames
```

The OLD page is the CoWork board page (`/_board/cowork-board`: Scope · Work · Check · Delivery, its
file and report pop-outs, its every-Project list). The cowork theme draws on the frame now
(`servers/workbench-cowork/cowork_theme.py`), so it retires. There is no b13 s11 · s12 · s13 yet, so
the planned screens are b03's s11-block-variants and s12-job-variants cowork rows; cowork has no s13
row (a Task is the shared Page Task, b13 Q01).


Theme elements
--------------

element · level · Space › view · base or its own and why · drawn today, or GAP: …

- top tabs · every level · the level row and the six Spaces · base · drawn
- Task ▾ greyed · Block, Job · the level row · base (no tNN_<doc>/ in the Job) · drawn
- view row · every level · every Space's views · base · drawn · GAP: casing (open · waiting · done)
- Question rows · Block · Audience Report · base (Insight's row) · GAP: a plain table, no question_cell()
- Question rows · Job · Audience Report (Block Questions citing it) · base · GAP: a plain table
- Space body · every level · every Space · base · drawn
- table · Block, Job · Scope, Resources, Jobs, Runs, Done jobs; Job, Files, Checklist · base · drawn
- rows · every level · Idea Studio · base (b03 s32-D06) · drawn
- Disk · Runs panel · every level · every Space · base · drawn (the server's Run names, b03 261008)
- tags · none · — · none (b03 s32-D09) · drawn: the frame has none
- header · every level · the top line · base · drawn
- one item · Job · Work Details › Emails · Meetings · Timeline · base pop-out · GAP: link leaves, 404
- Job state · Block, Job · Work Details › All · open · waiting · done; Description › Job · own: the header is cowork's only state · drawn
- Timeline · Job · Work Details › Timeline · own: every dated thing, newest first · drawn
- Checklist · Emails · Meetings · Job · Work Details · base table, cowork's words · drawn
- People · Block · Description › People · own: who to ask, role, who we wait on · GAP: a <pre>, not rows
- Resources · Related · Files · Block, Job · Description · base table · drawn
- Done jobs · Block · Delivery › Done jobs · base table · drawn
- Job Delivery · Job · Delivery · base · GAP: vanilla, nothing cowork (Q03)
- Page Task · Task · every Space · base Page Task views · GAP: the vanilla Task is drawn
- old CoWork page · old · /_board/cowork-board · retires · old page


Buttons with no Run name
------------------------

Every button the frame draws for cowork carries a Run name (`cowork_theme.RUN_NAMES` and the base's
own). These have none yet:

```text
button                         where                                          proposed Run
Draft a follow-up              old page › Check › Waiting on (no frame button) run-email-<slug>  (the thread's next pass)
Add a paper                    Guide › Related Paper (the CoWork Guide)       run-add-paper-<slug>
Save resource (+ Add resource) old page › Scope › Resources                   run-add-resource-<slug>
+ Add drawing                  old page › Scope › RoadMap Draw                run-draw-<sNN>
Edit · Edit drawing            frame › Idea Studio · old page › RoadMap Draw  run-draw-<sNN>  (a pass)
Close the Job                  planned: s12 Job › Delivery (not drawn yet)    run-close-<jNN>
Review the questions           frame › Block › Audience Report (no target)    run-review-questions-<bNN>
```

The old page's 14 run types (Update the Block status, Add a person, Add a resource, Draw, Open a job,
Update a job, Ask a Question, Review the questions, Write the report, Draft an email, Write meeting
notes, Draft a follow-up, Review a draft, Check a report) show bare words; each but Draft a follow-up
already has a name on the frame, which is its proposal (the drawing lists them).

Named differently by the server and b03's s12; decided (b03, 261008): the server's names win, and
b03's s12 cowork Runs rows now read them (s12 rebuilt):

```text
button                 kept (RUN_NAMES)           s12's old plan
Write meeting notes    run-meeting-<slug>         run-notes-<meeting>
Update the Job         run-face-<jNN>             run-update-job
Review a draft         run-review-email-<slug>    run-check-<thread>
Draft an email         run-email-<slug>           run-email-<thread>
```


Decided
-------

s32-D01 · Done (261008): b03's picks hold for the cowork theme: top tabs in the D · E look, the view row
    in the E look, the Question cell as the Insight row, Disk inside the Runs panel, no tags (b03 s32-D01,
    D02, D05, D08, D09). The cowork theme gives the words and the rows of its own elements only.
s32-D02 · Done (261008): the ladder levels and the old page are shot live from a placeholder Block on a
    second host (`cowork_fixture.py`), until a Project holds a cowork Block; the old page is flagged OLD,
    read off the code (`old_reason`: `cowork_theme.py` exists).
s32-D03 · Done (261008): each element also shows its planned screen, drawn by b03's shared cowork rows
    (s11 Block, s12 Job), so the gallery follows them on every rebuild.
s32-D04 · Proposed (261008): four elements are cowork's own (11 – 14): the Job's state fields, the
    Timeline, People, and today's Check split into Work Details › waiting, open run-email Runs and
    Delivery › Done jobs (b13 Q01). Each is built on the base's table and row; only People needs rows.
s32-D05 · Proposed (261008): an email, a meeting or a step opens in the frame's pop-out from its row
    (`pop()`, not `link()`); a document written in rounds opens as the Page Task.
s32-D06 · Proposed (261008): the Block and Job Audience Report take the base's Question row and
    `question_cell()` (b03 s32-D05), as the frame draws it on b13 itself (frame 3 · proposed).
s32-D07 · Done (261008, b03's ruling): where the server's Run names and b03's s12 plan differ, the
    server's win (run-email-<slug>, run-meeting-<slug>, run-face-<jNN>, run-review-email-<slug>); b03's
    s12 cowork Runs rows now read them. Draft a follow-up takes run-email-<slug>.


Open
----

1. Pick one look per element: the Pick frame lists each one, b03's picks in green, the rest in red.
2. The Block and Job Audience Report draw a plain table, not the base's row and `question_cell()`
   (`cowork_theme._question_rows`).
3. A Job's email and meeting rows link to the Page reader, which answers 404 "Not a Page" (an email is
   not a Page Face) and leaves the frame. The report link works (200) but leaves the frame too.
4. The cowork Task (`t01_protocol/`) draws the vanilla Task (Face · Folder | Folders · Evidence · Value
   | run-<type>-<target>), not the base's Page Task views (`page_task_spaces`), which Q01 names.
5. Run names: `run-review-questions` has no target, and Draft a follow-up, the planned Close the Job and
   the drawing and form buttons have no Run (the table above).
6. People shows `j00_people.md` as written; s11 plans person · role · waiting on · since rows. Whether
   `j00_people/` becomes `people.md` is JL's call (Q01 Next 1).
7. One casing in the view row (open · waiting · done, delivery/).
8. Job › Delivery is the vanilla one (Q03); no stale state on a Job row (Q02).
9. One icon: the old page is 📨, the frame 🤝. The Job and Task selects read folder names.
10. s11 plans "waiting on <person> · 3 days" as one line; the frame has waiting-on and since as two
    fields, and Timeline rows carry no state except draft ✎ (s12 plans one per row).

None of these is changed here. b03 placed 2, 3, 4, 5 and 6 in `servers/workbench-cowork/cowork_theme.py`
(question_cell() rows, pop() for email and meeting rows, page_task_spaces for the Task, the unnamed
buttons, People as rows); they wait for JL (b03, 261008).

(write here, or mark the drawing in red)
