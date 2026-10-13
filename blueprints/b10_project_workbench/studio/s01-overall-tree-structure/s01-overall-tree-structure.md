s01 · Overall tree structure
===========================

**Tags:** `Structure`

**Stage:** closed

**Topic:** one tree from Space down to Run (Space → Project → Theme → Block → Job → Task →
Run), each level with its specials, its variants, its skills and where it shows in the
workbench. Studio topic = creation: drawn and argued here, settled in a report Question.
Since 261010 the ladder follows frame 2: the Block alone holds `studio/` and `delivery/`, every
level holds its own `reports/` (s01-D32).

Frame 2 was s09 (Studio sNN and Block, Job, Task, Delivery) until s09 merged in here on 2026-10-12
(s01-D37). It holds how a Block's Studio topics (`studio/sNN-<topic>/`) relate to the Block, its
Jobs and its Tasks, and how far along each topic is. From the JL meeting of 261010: the Studio is the
centre's policy paper, one copy per Block, sent down to every level; Block, Job and Task are the
province, the city and the county, each doing the work and each writing its own report. A reader
goes to the level to read its report. The Delivery is the Studio's twin: one per Block, collecting
every level's output under the Block's `delivery/`. A topic stays a draft policy until it is agreed,
so each sNN carries a stage, and the index shows the stages so the centre sees what moves and what
does not.

**Feeds:** `reports/q01_bjtr_boundary/` (what each level owns), `q02_bjtr_across_themes/`
(how each Theme fills the levels), `q05_skill_per_level/` (skills), `q07_workbench_mapping/`
(where each level shows on screen), `q03_block_questions/` and `q09_studio_report_on_screen/`
(frame 2, from s09).

**Source** (frame 2): `../../related/meetings/2026-10-10-1800 研究项目工作流程设计与结构优化.md`
([58:10] centre and province, city, county; [58:26] and [74:02] a report at every level;
[74:18] what the centre must write; [32:34] Delivery at the top level)


Files
-----

```text
s01-overall-tree-structure/
├── s01-overall-tree-structure.md   this face: what is decided, what is open
├── s01-overall-tree-structure.excalidraw   the drawing: 1 · The ladder, 2 · Studio sNN and Block, Job, Task, Delivery
├── s01-overall-tree-structure.png          its preview
├── build_ladder_v4.py              draws it; also holds the variant trees the theme ladders draw
├── studio_delivery_frame.py        frame 2, was s09's builder (merged 261012, s01-D37)
├── history/                        s09's face, drawing and builder; this face before the merge
├── level_views.py                  the screens per Level and Space, shared by s11-s13 and the theme ladders
├── run-skill-draft.md              the Run change to haipipe-run and haipipe-project (applied 261006)
├── theme-rename-plan.md            the move to work/ and singular Theme folders (s01-D28, D29): phases
└── (sessions)                      passes of ../../runs/run-draw-s01/ (s02-D27); no chat/ folder
```

Rebuild: `python build_ladder_v4.py` (or `../_build/make.sh`).


What the drawing holds
----------------------

```text
1 · The ladder             a node per level; specials branch right; a green "holds" arrow drops
                           to the next level; definition + variants box under each; Tools/ at the
                           far right, its skills pointing back into each level
2 · Studio sNN and Block,  left: the Block's Studio issues down to Block, Job and Task, each level
    Job, Task, Delivery    writes its own report, the Block's Delivery collects every level's
                           output; right: the stage of one sNN, its gate, the index (was s09)
3 · The SPACE Home index   frame 2's INDEX box drawn out: one read of the disk, the Chart and the List,
                           and the Guide's SPACE and Project buttons back to it (s01-D38, D39)
4 · The index today        the two screens as they look on 2026-10-12 (pictures, taken by hand)
```

Frames 3 and 4 are drawn by `index_frame.py` on excalidraw-studio's `draw.py` (JL 261012: "for the s01 we want to
put the index to it, the design of the index of the chart and list"); their words are this yaml block, and the two
screens are `index-chart-261012.jpg` and `index-list-261012.jpg` beside this face.

```yaml
index_drawing:
  title: "3 · The SPACE Home index: Chart and List"
  key: "One read of the disk draws both views; every Guide leads back to its SPACE and its Project."
  flow:
  - title: "📂 On disk"
    lines: ["Block, topic, Job and Task faces", "each topic's drawings"]
  - title: "🗂 chart_data"
    lines: ["one read, one tree", "SPACE → Project → Block → Job"]
  - title: "📊 Chart · Progress"
    lines: ["a ring per level", "coloured by each face's state:"]
  - title: "📋 List · Index"
    lines: ["a Block row folds open", "🧠 Studio rows · 🗂 Job rows"]
  labels: ["read by", "draws", "or, a button"]
  way_in:
  - title: "🧭 a Block's Guide"
    lines: ["[SPACE] [Project]"]
  - title: "🏠 SPACE"
    lines: ["the whole Home"]
  - title: "📁 Project"
    lines: ["that Project only"]
  way_labels: ["SPACE opens", "Project opens"]
  open:
  - "later: the chart colours each sNN by its stage (s09-D04)"
  - "later: Current, kept in one browser only"
  - "later: folds and Project order, one browser only"
  screens_title: "4 · The index today: the two screens"
  screens_sub: "Taken by hand on 2026-10-12 from WellDoc (port 5622): left, the Chart sized by Block count, coloured by each face's state:; right, the List for Project-Samsung with b11 open, its Studio rows and its Job rows."
  screens: ["index-chart-261012.jpg", "index-list-261012.jpg"]
  arrow_in: "the INDEX box, drawn out"
  arrow_on: "looks like this today"
```

The variants that were frames 2-4 became s11, s12 and s13 (Block, Job and Task variants), deleted on
2026-10-12 at JL's ask. The old frames 5 (Task → Run) and 6-7
(Workbench UI, Level · Space · Subspace) were removed with their builder (JL 261007); the
notes below still name them by number. Today's frame 2 is a different one: s09's frame, added when
s09 merged in (s01-D37).


Decided so far
--------------

Each decision keeps its id for good (`s01-DNN`), so a reply, a report or a drawing can cite it.
When one settles, its answer goes into the Question it feeds (`reports/qNN_*/`) and cites the id.

s01-D01 · A Block has two branches: `reports/` (Questions, for the audience) and its Jobs (the work).
   `studio/` and `reports/` are special Jobs.
s01-D02 · `studio/` holds topics, one folder each (`sNN-<topic>/`): a drawing, its builder, `chat/`,
   and a face `.md`. Studio is for creation.
s01-D03 · A report `reports/qNN_<topic>/` = `qNN_<topic>.md` (a light Page: Answer · Evidence ·
   Limits · Next) + `qNN_<topic>.excalidraw` + `draft/` + `page.toml`. No runs or results of
   its own; it cites Job · Task · Run. Report is for presentation.
s01-D04 · Drawings live only in `studio/` topics and in `reports/qNN_*/`; none at Job level.
s01-D05 · A tree lists only its own level's files; the children are the next box.
s01-D06 · `platforms/` and `external/` are freestyle.
s01-D07 · A workbench screen = Space tabs, the open Space's subspaces as tabs below them, the
   content, and the Runs panel on the right.
s01-D08 · Proposed (frame 6 in v3): one Block workbench, tabs = the ladder: Guide · Block · Job ·
   Task. Zoom in by picking: Block › Jobs → one Job; Job › Tasks → one Task; Task › Runs → a
   Run pop-out. Every level tab: Overview · Studio (optional drawings) | its children | Check ·
   Delivery. Delivery = what leaves this folder, rolling up (Task → Job → Block). The Task tab =
   today's page workbench. A third row of buttons groups the open list (Jobs by series, a Job's
   Tasks e.g. Main · Appendix); a Task's Runs are one plain list.
s01-D09 · Proposed: `studio/` is optional in a Job and a Task too (drawings only), not just the Block.
s01-D10 · Proposed: a paper version is a Job (`jNN_v<N>_<venue>/`); its Sections are Tasks, grouped
    Main · Appendix.
s01-D11 · (261006, replaced by s01-D14) Block, Job and Task have the same parts: face · studio/ · scripts/ · runs/ ·
    results/ · delivery/ · children. `scripts/` = code of that level's local Runs. A Job keeps
    `src/` and `sbatch/`: they mark a Job. Block and Job Runs are setup and management; only a
    Task Run is evidence. Each level's tab gets a Runs view.
s01-D12 · Proposed: the Block's face `board.md` → `bNN_<topic>.md`, like `jNN_<job>.md` and
    `tNN_<task>.md`. A Block may have `delivery/`.
s01-D13 · (261006) The screen has three rows: **Level** = the tab (Guide · Block · Job · Task);
    **Space** = the row below it, a folder or file of that Level; **Subspace** = the third row:
    a group of that Space's items (Studio types Map · Scratch · Design; question groups; Job
    series j1N; Task groups Main; Delivery types Report · Export), a view (a Page's Draft), or
    none. Items are never buttons: they are rows, stacked top to bottom (JL 261006). Studio
    rows open into the live drawing over its chat; Reports rows are Question │ Work │ Report. One column order at every Level: face · items | children |
    Check · Delivery; optional Spaces are dashed. Address = path: b03 › Reports › q02 =
    `bNN_<topic>/reports/q02_<topic>/`. Frame 7 of ladder-v3-proposed.
s01-D14 · (261006, refined by s01-D15) Block and Job hold no `scripts/` and no Runs; `runs/ · results/` with numbered
    `rNN_…` Runs are a Task's children. Soft `run-<kind>-<slug>` Runs live in the item
    they work on, at any level (once dated `run-<kind>-<MMDD>-<slug>`; the day now sits on each pass,
    `passes/pNN-<MMDD>/`: JL 261007, the page skills renamed them). `studio/ · reports/ · delivery/` may sit at Block, Job or Task.
s01-D15 · (261006) The ladder ends in passes: **Block → Job → Task → Run → pass**.
    - **Run type** is the existing term (table-workbench, haipipe-run): the button, its token
      in a name, its workbench-table row (agent · skill · signs). Run type → (Run Spec) → Run →
      pass.
    - A Run is **hard** or **soft**, decided by where its output lands. Hard `rNN_<slug>`:
      ticket `.sh` (or a runner's `.yaml`), output only in its own `result/`, evidence, a Task
      only. Soft `run-<type>-<target>`: ticket `.md`, output lands in its scope's items
      (`draft/`, `studio/`, `reports/`, `delivery/`), not evidence, at Block, Job or Task.
    - One Run, many **passes** (`passes/pNN-<MMDD>/`). Hard: one execution of the same ticket
      (a retry, a rerun); new inputs = a new `rNN`. Soft: one round of work on the same target
      (the same paragraph or section = the same Run); a new target = a new Run.
    - `results/` merges into the Run folder: `runs/<run>/` holds the ticket, `config.yaml`
      (hard), `result/` (hard, generated), `passes/` and **`run.yaml`**: the one lookup card,
      the same fields for both kinds (run · kind · type · scope · target · ticket · skill ·
      agent · signs · status · passes · writes · feeds), written only by tools.
    - Refines s01-D14: a soft Run's folder sits in the scope's `runs/` (no other folder name, no
      new term).
    - (JL 261006) One folder: every Run folder, hard and soft, sits in `runs/`.
    - (JL 261006) Page evidence is soft: a Page's display, value and citation Runs are soft
      Runs. They may run code (a plot script), and that code stays in the Page with its
      display (`displays/<fig>/recipe/ · assets/`). They only read finished hard Results from
      work or discovery Tasks: select, round, format, plot, quote. A Page computes no new
      facts: a new number needs a hard Run in a work Task. So a Page folder has no hard Runs.
    - (JL 261006) A Task is known by its name (`tNN_…` with `tNN_<task>.md`), not by what is in
      its `runs/`. Two kinds: a work Task makes facts (hard Runs); a Page Task presents them
      (soft Runs only).
    - (JL 261006, "yes to all") A soft Run's name has no date: `run-<type>-<target>`; the date
      sits in its passes. `run.yaml` is the card's name, fields as above. A hard Run may carry
      several type tags (`type: [fit, evaluate]`) while one close rule settles it; two close
      rules = two Runs. Existing Tasks move once, by a script, from `runs/<run>.sh` +
      `results/<run>/` to `runs/<run>/`; tools read both layouts until it has run. A design
      commission (release or hold) is soft: a person's decision, not evidence.
s01-D16 · Proposed (261006): insight keeps its layout: Block = the topic, with `datasets:` in its
    face; Jobs = the DIKW levels; Tasks = questions, one script each; Runs = `<dataset>_<partition>.sh`
    (one script serves every dataset, so the dataset is not a Job). On screen it keeps today's
    Insight workbench (haipipe-workbench-insight 0.16.0): Spaces Scope (Dataset · Partitions ·
    Questions) · Prototype (Meta · Data · Information · Knowledge · Wisdom · RoadMap Draw) ·
    Insight (Full · each cut · Cross; Logic · Work · Report) · Check (Gates · Checks · Runtime) ·
    Delivery (Handoff); one dataset at a time; runs and pages open in pop-outs. In the general
    model, Prototype is its children Space and Insight a view across them; a family may name its
    children Space and add one view across it.
s01-D17 · Proposed (261006, from JL's mark on the Block tree): Block and Job hold `runs/` too,
    soft Runs only (each writes into one item of its level; no evidence there). A Task's
    `runs/` holds hard and soft. Every `runs/` has a `README.md`: the run types that folder has,
    one row each (name pattern · what it writes · skill · agent), each with its Runs (name ·
    state · last pass). Tools write it from the `run.yaml` cards, never by hand; the types a
    level could start stay in the family's workbench table (the Runs Space buttons). The Block
    and Job tabs get a Runs Space, one list with no third row: `| Jobs | Runs · Delivery`.
    Drawn in frames 1-4, 6 and 7 of ladder-v3-proposed and in s11-s13.
s01-D18 · Proposed (261006, from JL's marks on s11): no Check Space. What it held goes where it
    belongs: progress (state, what a row waits on, how long, stale) shows on each row, and
    Block › Jobs opens each Job to its Tasks; a check is a Run (`run-check-<target>`) listed in
    Runs, with its button on the item it checks; a release check sits in Delivery, as today's
    page and paper workbenches already do. Every level: face · items | children | Runs ·
    Delivery. The right panel of a screen is "Run types" (the buttons); the Runs Space lists the
    Runs. A Block's `delivery/` is optional (a dashed tab); a task Block's is often empty, and
    what its Tasks released still shows "from below". Insight keeps today's Check (its seven
    gates) for now.
s01-D19 · Proposed (261006, from JL's marks on s11): a discovery Block holds the same folder as a
    task Block. A paper Board takes today's paper views into its Spaces: Studio groups
    Ideation · Spine · Design (today's Ideation, Story › Spine and RoadMap Draw); Reports groups
    Narrative · High-level logic + Low-level work · Related Papers · Related Questions; its
    children Space "Jobs & Sections", groups main · appendix · grants · slides (versions, plus
    grant and slide Jobs); Delivery groups LaTeX · Word · Cover letter · Rounds, as today, each
    made by calling the Board's own Runs (`run-delivery-latex`, `run-check-submit`). A version's
    Tasks are its Sections plus its cover letter and rebuttal (Page Tasks, group Letters), which
    the Board's Delivery shows under Cover letter and Rounds. Every Block's screens start with
    the Guide tab, so each proposed screen sits above today's. s11's drawing is JL's own copy
    now; the builder writes `s11-block-variants-proposed.excalidraw` beside it.
s01-D20 · Proposed (261006, JL's sketch of the paper Block tab): the Block tab has five Spaces, one
    per part of its folder: **Description** (the face; third row Scope · Resources · Related
    Papers, cowork adds People) · **Idea Studio** (`studio/`) · **Audience Report** (`reports/`) |
    **Work Details** (its Jobs, each open to its Tasks; third row its Job groups) | **Runs**
    (`runs/`, optional, JL's later mark) · **Delivery** (`delivery/`, optional). Runs lists the
    Block's own Runs, each with its run type (the same names as the Run types panel), and the run
    types are its third row. Insight fills the five with today's views (Scope → Description, RoadMap Draw → Idea
    Studio, Insight → Audience Report, Prototype → Work Details); today's Check is left out. The
    Task tab takes the same five (the s13 session, same day); the Job tab still uses the older
    names.
s01-D21 · Proposed (261006, JL: "where will we save the files for the papers?"): a Block's related
    papers are one table, `related-papers/related-papers.md`, in the eight columns of the
    table-papers skill (group · role · key · paper · venue · doi · why here · pdf); `group` names
    the Question or Job a paper serves. A full text sits beside it only under an open license,
    listed with its license in `related-papers/README.md`; every other paper links by DOI and is
    never copied into the SPACE. A deep read (facts, abstract, one BibTeX entry, how it was read)
    stays a discovery Task's hard Run, `rNN_<author><year>_<subject>/result/`, which the row
    links to. A paper Board builds its `reference.bib` from the table at Delivery. On screen:
    Description › Related Papers.
s01-D22 · Proposed (261006, JL's marks): the Idea Studio has no third row, on any tab: one drawing
    after another, each topic named for what it draws (`s01-paper-flow/`, `s02-ideas/`). Grouping
    belongs to the Audience Report, the ready-to-use side: a paper's concepts (Ideation · Spine ·
    Design) join its Narrative · High-level logic + Low-level work · Related Questions there. The
    Task tab takes the same six Spaces as the Block, Runs included and not optional, since a Task
    holds the hard Runs (the s13 session).
s01-D23 · Proposed (261006, JL's marks on the s11 proposal): the blockers. Every row of screens has
    a line down it before each group of Spaces, the groups of the bars in its Spaces row, through
    the proposed and today's screens: Guide | Description | Idea Studio · Audience Report | Work
    Details | Runs · Delivery on the Block rows (s11, frame 2) and the Task rows (s13, the s13
    session); Overview · Studio · Reports | its children | Runs · Delivery on the Job rows (s12),
    until the Job tab takes the same Spaces. The builders read the groups off the Spaces row, so a
    line moves when a Space does.
s01-D24 · Proposed (261006, JL: the insight DIKW levels "are in the board level, do you think in the job
    level"): a DIKW level is a Job, as the Insight Block contract already says (one Job per level,
    one Task per question), so its screens move down a tab. Block › Work Details lists the four
    DIKW levels, each open to its questions, with no third row; today's Prototype › Data · Information ·
    Knowledge · Wisdom views become each DIKW level's Job tab. That tab is the first Job tab with the
    Block's six Spaces: Description (level.md) · Idea Studio · Audience Report (the Insight table,
    this DIKW level's rows, by partition) | Work Details (its questions, with needs and script) | Runs
    (review the questions, plan the evidence, write the script; its questions' hard Runs from
    below) · Delivery (only j04_wisdom's counsel and handoff). The insight Block gets its Runs
    back (record the extract, register a cut, draw the question map, carry a board over). Today's
    screens now sit under the proposed screen doing the same job, on the Block and Job rows.
    Open: Meta stays on the Block; only Wisdom delivers; a DIKW level's slice of the question map.
s01-D25 · Proposed (261007, JL: "should we put the venue resources here?"): a paper Board's
    Description gets a fourth group, **Venue**: Scope · Venue · Resources · Related Papers, second
    like cowork's People, so the screens and the third row read in one order. Its folder is
    `venues/<venue>/`, one per venue the Board writes for, so a resubmission adds a venue and
    keeps the old one: `call.md` (dates, page and format limits, review rules, with the link and
    the date it was read) and `kit/` (the author template, as the venue ships it). Each version
    Job names its venue (`j01_v1_<venue>/`), and Delivery builds with that venue's kit
    (`paper-build.toml` names it). The face keeps one line for the current target. Run types:
    Add a venue, Check the rules.
s01-D26 · Proposed (261007, JL's marks on the s11 proposal): every Section row in a paper Board's
    Work Details (and in a version's Sections, on the Job tab) carries that Section's map,
    embedded and view only. The map is the one the excalidraw-section skill already draws,
    `S-<…>/studio/<stem>-sections.excalidraw`, generated from the Section's plan and its
    Evidence Items, so the row shows how far the Section is (each paragraph, each evidence card
    and its state), not only "done" or "check". Clicking it opens the Section's Idea Studio. A
    Section with no map yet shows an empty box; "Redraw the Section map" fills it.
s01-D27 · (261007, refined by s01-D34) Proposed (261007, JL: "could we call this related? It might not be limited to the
    paper"): `related-papers/` becomes `related/`, and Description › Related Papers becomes
    Description › Related. Its one table, `related/related.md`, takes any kind of related work
    (paper · repo · dataset · tool · project) with a `kind` column; the rest of the earlier
    related-papers rule stands: open-licensed PDFs only, every other item links out, a deep read
    stays a discovery Task's Run, and a paper Board builds `reference.bib` from its paper rows.
    Related = what the Block sits beside; Resources = what it uses. The live views keep their
    names (paper Story › Related Papers, Guide › Related Paper by table-papers): they show papers
    only, and nothing live has a `related-papers/` folder. They move when Description › Related
    is built (JL 261007).
s01-D28 · Proposed (261007, JL: "maybe still call it work? it can be all types of work"): the
    `tasks/` Theme becomes the **work** Theme, folder `work/` (singular, like `cowork/`): work
    Block · work Job · work Task. The level keeps its name, Task, in every Theme. "Work" has one
    meaning at two scopes: every Theme does work (Question → Work → Report and Work Details name
    any Theme's Jobs, Tasks and Runs), and the work Theme is the general one, for work no
    specialised Theme (discovery, cowork, paper, insight, design, labeling) takes. A work Task
    may be dry (code on data; `rNN_<slug>.sh` → `result/`) or wet (a procedure in the world, run
    by a person; a protocol ticket and a signed receipt), both hard Runs. The b03 drawings use
    the new name; skills, servers and projects keep `tasks/` until the rename is planned.
s01-D29 · Decided (261007, JL: "we make all of theme to be singular"): every Theme folder is
    singular, named for the kind of work it holds, like its skill and its board kind:
    `work/ discovery/ cowork/ paper/ insight/ design/ labeling/` (was `tasks/ discoveries/
    cowork/ papers/ insights/ designs/ labelings/`). The folder rule: singular for a kind or a
    place (a Theme, `studio/`, `delivery/`, `external/`), plural for numbered items (`reports/`
    qNN, `runs/` rNN). Watch: a Page folder's own `labeling/` lane shares the Theme's name at
    another depth. Applied in the proposal drawings; the `_build/` scratches still show the
    folders as they are on disk today, and skills, servers and projects move in one planned
    rename together with s01-D28.
s01-D30 · Proposed (261007, JL): Idea Studio and Audience Report are on every level tab (Block, Job,
    Task); Work Details, the level's children, may be empty, and a Task has none. Written up in
    `../s02-studio-workbench-skill/` (s02-D26); drawn large in s11's two close-up frames.
s01-D31 · Proposed (261007, JL): Runs get their own studio topic, `../s06-run-workbench-skill/`: hard and soft, the
    Run folder, a Run's life, and the Runs panel, Runs Space and pop-out on screen. It carries on
    s01-D14 and s01-D15, which haipipe-run 0.31.0 already states.
s01-D32 · The ladder follows b10 s09 (JL 261010): the Block alone holds `studio/` and
    `delivery/`; a Job and a Task have neither and open the Block's as shared views; every level
    keeps its own `reports/` (s09-D01, D02, D05). A studio topic carries a **Stage:** line and its
    sessions are passes of `runs/run-draw-<sNN>/`, not a `chat/` folder (s02-D27, s09-D03). On
    screen: Studio | Block · Job · Task | Delivery on top, Description | Report | Work Details |
    Runs below (s02-D18). This replaces the parts of s01-D02 (`chat/`), s01-D08 (Delivery rolling
    up Task → Job → Block), s01-D09 (a Job or Task `studio/`), s01-D14 (`studio/ · delivery/` at
    any level) and s01-D20 (six Spaces in one row) that said otherwise; frame 1 is redrawn to match.
s01-D33 · The ladder keeps its stairs, one step down and right per level (JL 261010: "keep the
    stair shape"), and is drawn denser so it reads at 50% zoom: text 1.5x (body 20 px or more), short
    gaps, the skills column moved in beside the stairs. Each green note sits beside the box it changed,
    none at the top. The stairs are wider than the 2800 px screen rule; the shape wins here.
    The variant trees s11-s13 keep their own sizes.
s01-D34 · A Block's `related/` keeps its name and holds what the Block sits beside, of any kind (JL
    261011: "to put the meeting, and related papers, etc. or some source materials"; "maybe we just use
    the related"): `meetings/` (a meeting's notes or transcript, `YYYY-MM-DD-HHMM <title>.md`), `papers/`
    (open-licensed PDFs only), `files/` (what we were sent: a draft, a form, slides), `emails/` (an
    email saved as it came, `.eml`; added by s04-D08), each made with its first item, and one table,
    `related/related.md`, one row per item (kind · date · item · link · feeds · group, the group added
    by s04-D07; kind = meeting · paper · file · email · repo · dataset · tool · project), anything not
    kept linking out. A subfolder is a group of its files (s04-D08); `/haipipe-related` owns the
    folder (s04-D09).
    What lands here is not edited again; notes about it go to a studio topic or a report. The rest of
    s01-D27 stands (a deep read stays a discovery Task's Run; a paper Board builds `reference.bib` from
    its paper rows; the paper's Related Papers view shows the paper rows only). Proposed: on screen it
    leaves Description and joins the top row, after Delivery (JL 261011: "put the related after the
    delivery at the top"), since like Studio and Delivery it is the Block's alone and every Job and Task
    reads it: Guide | Studio | Block · Job · Task | Delivery | Related, a reference shelf at the end, as a
    paper keeps its references last. Until the frame is built it stays Description › Related.
    b10's own meeting moved to `related/meetings/`. The Project root's `external/` is a different
    folder (pinned upstream code and data, s01-D06) and keeps its name.
    Related and the reports: related is what came in, a report is what the Block answers. A row's `feeds`
    names the reports (`qNN`) and topics (`sNN`) it feeds; a report cites a related item by its row, the
    way it cites a Run; a meeting that raises a question becomes a Question in the face and a `qNN`.
    Flow: related (in) → studio (think) → Jobs and Tasks (work) → reports (answer) → delivery (out). Worked out in
    `../s04-related-workbench-skill/` (s04-D01 to D05). On screen, settled by s04-D05: Related folds
    inside the Studio, under the topic cards, and the top row keeps Guide · Studio | Block · Job · Task |
    Delivery; the "after Delivery" proposal above is dropped (JL 261011).
s01-D35 · Folder names: a place is singular, a set of numbered things is plural (JL 261011: "Do we use
    reports or the report?"). Singular: `studio/`, `delivery/`, `related/` (one room, one shelf). Plural:
    `reports/` (qNN), `runs/`, `venues/`, `meetings/`, `papers/`, `files/`. So `reports/` stays: 28
    folders and 149 `qNN` reports today, read by 54 Python files. On screen every tab is singular
    (Studio, Report, Delivery, Related).
s01-D36 · A Task is a folder that may hold a draft, not a Page (JL 261011, asked in b16: "so in this
    way, we will not have the so call the task = page?"; built in b51_base_draft). Every level has a
    face .md; a folder that writes prose holds `draft/` (its logic, sentences and evidence) beside its
    face; the Page is the face and its built output. haipipe-task 1.13.0, haipipe-folder 0.8.0 and
    haipipe-draft 0.126.0 (was haipipe-page) say so. In WellDoc, 102 Task folders hold `draft/`;
    compute Tasks hold none.
s01-D37 · s09 (Studio sNN and Block, Job, Task, Delivery) is merged into s01 (JL 261012: "plesae merge the
    s09 to the s01"). Its one frame is s01's frame 2, drawn by `studio_delivery_frame.py`; its decisions
    keep their ids, s09-D01 to D09, below; its Later list is under Open. Its old face, drawing and
    builder are in `history/`. The number s09 is retired; b10 has 12 topics.
    Later the same day, at JL's ask, the number came back for a new topic, `../s09-block-folder/` (the Studio's
    Folder part, what the Block folder holds); its decisions start at s09-D10, after these. The old s09's one
    session moved to `history/run-draw-s09/`.
s01-D38 · SPACE Home's List · Index folds each Block (JL 261012: "for each block, I want them to be collapable as
    well, and show to groups of the cards, a group of studio and a group of the jobs"). A Block card starts
    folded and shows its counts (🧠 topics · 🗂 Jobs); open, it holds two groups: Studio, one row per sNN read
    as the workbench's Studio list (its folder name, tags, ↗ to the topic in the Studio, the stage pill; opened,
    its first drawing, live and read-only, loaded only then; JL 261012: "it is more like this ... and I can
    preview the content of the draw as well", replacing the first cards), and Jobs, one row per jNN the same way
    (its folder name, title and Task count, ↗ to the Job, its status; opened, its Tasks and its face, read in
    place; JL 261012, on the Job cards: "could you make it to do the same?"). The cards read the same data the Chart · Progress view draws; a search that hits a
    topic or Job opens its Block; a person's folds are remembered in the browser. This is the INDEX box of
    frame 2 (s09-D04), built in `servers/space-home/home.py`.
s01-D39 · SPACE Home shows one Project from a link, and every workbench Guide has that link (JL 261012: "could you
    make the index to be SPACE, and also I want to have a link to the Project"). The Guide's first two buttons
    are SPACE (the SPACE Home, was Index) and Project, `/?project=<Project folder>`: the Home with only the
    folder's Project. A folder outside any Project gets its SPACE bucket instead, `/?project=shared:space`
    (SPACE / Shared) or `shared:tools`, which `?project=` now takes by its key. The Guide's buttons are
    s02-D31's; the Home's filter is this topic's.
s01-D40 · Stage → closed (JL 261012: "we can close s00 and s01"). Its Open points moved to Later and none blocks it: the ladder, the
    Studio and Delivery at the Block (frame 2) and the SPACE Home index (frames 3 and 4) stand as drawn. The
    drawing's red questions became black later lines, with a green note.


From s09 (merged 2026-10-12)
----------------------------

s09 was agreed on 261011 (s09-D09). Its decisions, unchanged:

s09-D01 · The Block's Studio is the centre: one copy per Block, shared down to its Jobs and
    Tasks. It holds the plan (the drawing), the decisions, and what each level must report
    (JL meeting 261010 [58:10], [73:52]; the same rule as s02-D03 and s02-D09).
s09-D02 · Every level reports: Block, Job and Task each have their own Report, and a reader goes
    to the level to read it, as low as a Task and as high as the Block (JL meeting 261010 [58:26],
    [74:02]). This fills the Report half left open by s02-D06.
s09-D03 · Each sNN has a stage: explore · shaping · agreed · closed. A person moves it; the gate
    (red marks left, Open items, dated decisions, frame checks) only counts and never moves it
    (JL 261010).
s09-D04 · The index shows each sNN's stage and what we are working on now, so the centre sees at
    a glance what moves and what does not (JL 261010).
s09-D05 · Delivery is Block-level, the same as the Studio: only the Block holds `delivery/`. Job
    and Task outputs keep their source path under it (`delivery/jNN_<job>/tNN_<task>/<lane>/`), and
    the Job and Task views show their own part (JL 261010; confirms s02-D14 over the meeting's
    "top level across Blocks" [32:34]). Refined by s03-D06 (261011): from a Job or Task, the
    top row's Delivery opens the Block's Delivery with the open source picked, as Studio does.
s09-D06 · The topic is renamed s09-studio-block-job-task-delivery, so its name carries Delivery
    beside Block, Job and Task (JL 261010). The number s09 and its decision ids stay.
s09-D07 · Every b10 topic has a **Stage:** line under its Tags (261010, JL asked; set by Claude from
    the gate counts): 8 shaping (decisions made, open points or red marks left: s01 s02 s04 s05 s09
    s21 s31 s32), 4 explore (no decisions yet: s11 s12 s13 s51). None is agreed: agreed needs JL's
    sign. The shared Studio shows the stage as a badge before each topic's name.
s09-D08 · Each level's report lives in its own folder: a Job's in `jNN_<job>/reports/qNN_<topic>/`, a
    Task's in `tNN_<task>/reports/qNN_<topic>/`, the Block's in its `reports/` (JL 261010). This answers
    Open 1; the Block's Report view lists all three by source, as the Studio does.
s09-D09 · Stage → agreed (JL 261011: "I think for the s09, it can be closed as well"). Open 1 was settled
    by s09-D08 and Open 7 moved to s03; the other five wait under Later, and none blocks it. The
    drawing's red questions became a black later list with a green note.


JL's notes on ladder-v3 (261006)
--------------------------------

1. Studio drawing: tree-based, lines and boxes, more room to modify and scratch; keep the
   human's scratch.
2. `chat/`: a Claude Code or Codex session can be saved here.
3. Report drawing: make things clear, more figures and displays of the results; the human
   makes only minor changes or suggestions.
4. Each section of an agent's reply links to a Studio topic or a Question (report) topic.
   Studio for creation, Report for presentation. Worked out in `../s02-studio-workbench-skill/`:
   a report's drawing is generated from named studio frames.
5. Frame 2, task Block, `studio/` entry: "this need to be modified". Done in v4: the entry
   now shows `sNN-<topic>/` with its face, drawing, builder and `chat/`.

6. Frame 2, task Block screen: "Scope" Space → "Block"; its "Block" subspace → "Scope" (the
   topics this Block covers); Block's subspaces = Scope / Resources / Studio (RoadMap Draw) /
   Questions. Frame 3: "Task" Space → "Job & Task". "How do we define the groups? j1N, j5N
   series?" Then: every Block workbench the same, Guide + Block + Job & Task + Delivery.
   Done in v4 as the proposed board level (frames 2-4 screens); frame 5's table still shows
   today's Spaces, read from each workbench-table.md.

Also fixed in v4: frame 1's Block skills named `haipipe-block`, which no longer exists; now
`haipipe-<family>` (each family's skill owns its board.md).


Open
----

(none: closed 261012, s01-D40)


Later
-----

Not needed now; each comes back as a new point if it is wanted (the Open list when s01 closed, s01-D40).

0. Runs: applied 261006 as haipipe-run 0.31.0 and haipipe-project 0.11.0 (audit and update
   at every level); `run-skill-draft.md` records what was taken. Next: haipipe-task's ticket
   template writes `runs/<run>/`, then the move, one Block at a time.
1. Paper: is the built paper the Board's `delivery/`, or each version Job's? Settled 261010 by
   s01-D32: the Board's `delivery/`, a version's under `delivery/jNN_<version>/`.
1b. Insight: is a DIKW level a line of work (a Job)? a question climbing D → W = 4 Tasks? a partition =
   a Run or a Task? carry the register board over, or keep both layouts? (red in frame 2)
   Proposed in s01-D16, aligned with today's Insight workbench. Still open: does insight gain the
   Job and Task tabs, or keep its pop-outs? Its studio as Prototype › RoadMap Draw, no Reports?
1d. Level · Space · Subspace (red in frame 7): Studio types (Map · Scratch · Design · Logic)?
   Delivery types (Report · Export · Handoff)? a question's group in its qNN face or the
   register? Resources a section of the face or a folder? Reports at Task level? "view" its own
   kind or a group? Guide a Level or a side panel? Check computed, not a folder?
1c. Topic folder naming: `sNN-<topic>/` (this folder) or `sNN_<topic>/` (the earlier sketch,
   matching `qNN_<topic>/`, `bNN_<topic>/`)?
2. Theme vs Family vs Area for the level under Project.
3. `discoveries/` → `literature/`?
4. `board.md` → `bNN_<topic>.md`?
5. Where a design stage and a labeling Task show on screen (red in frames 3 and 4).
6. A skill for each design stage? (red in frame 3)
7. Groups in Job & Task: today a "group" is the Question register's `group:` field (rows are
   Questions); proposed: one table per Job, grouped by series (j0N, j1N, j5N …)?
8. Where Check goes once the Check Space is gone: Task checks in Job & Task › Check, report
   checks in Delivery › Reports? Proposed in s01-D18: no Check Space at any level. Still open:
   insight's seven gates as a column of its Insight rows?
9. Save check for plain drawings in the workbench, so a stale tab cannot overwrite a build.


Later (from s09)
----------------

Not needed now; each comes back as a new point if it is wanted.

1. What each kind of Block, Job and Task must report: the centre writes it; learn it on one real
   Block first ([74:18]).
2. Who writes the decision row that moves a stage, and whether the workbench gets a button for it.
3. Current (what we work on now) is saved in one browser; the index can only show it once it is
   a file in the Block.
4. Does the 10-topic cap count only explore and shaping topics? b10 had 16 topics on 261010, 12 on 261012.
5. A deliverable that crosses Blocks (a meeting deck): does it get its own Block, as a paper Board
   already is? (Where Delivery lives is settled by s09-D05; its design is s03's.)
