s01 · Overall tree structure
===========================

**Topic:** one tree from Space down to Run (Space → Project → Theme → Block → Job → Task →
Run), each level with its specials, its variants, its skills and where it shows in the
workbench. Studio topic = creation: drawn and argued here, settled in a report Question.

**Feeds:** `reports/q01_bjtr_boundary/` (what each level owns), `q02_bjtr_across_themes/`
(how each Theme fills the levels), `q05_skill_per_level/` (skills), `q07_workbench_mapping/`
(where each level shows on screen).


Files
-----

```text
s01-overall-tree-structure/
├── s01-overall-tree-structure.md   this face: what is decided, what is open
├── s01-overall-tree-structure.excalidraw   the drawing: frame 1 · The ladder (was ladder-v3-proposed)
├── s01-overall-tree-structure.png          its preview
├── build_ladder_v4.py              draws it; also holds the variant trees s11-s13 and the theme ladders draw
├── level_views.py                  the screens per Level and Space, shared by s11-s13 and the theme ladders
├── run-skill-draft.md              the Run change to haipipe-run and haipipe-project (applied 261006)
├── theme-rename-plan.md            the move to work/ and singular Theme folders (s01-D28, D29): phases
└── chat/                           one file per session (Claude Code, Codex)
```

Rebuild: `python build_ladder_v4.py` (or `../_build/make.sh`).


What the drawing holds
----------------------

```text
1 · The ladder             a node per level; specials branch right; a green "holds" arrow drops
                           to the next level; definition + variants box under each; Tools/ at the
                           far right, its skills pointing back into each level
```

The variants that were frames 2-4 are their own topics now: `../s11-block-variants/`,
`../s12-job-variants/`, `../s13-task-variants/`. The old frames 5 (Task → Run) and 6-7
(Workbench UI, Level · Space · Subspace) were removed with their builder (JL 261007); the
notes below still name them by number.


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
s01-D27 · Proposed (261007, JL: "could we call this related? It might not be limited to the
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
    `../s04-studio-and-report/` (s04-D05); drawn large in s11's two close-up frames.
s01-D31 · Proposed (261007, JL): Runs get their own studio topic, `../s05-runs/`: hard and soft, the
    Run folder, a Run's life, and the Runs panel, Runs Space and pop-out on screen. It carries on
    s01-D14 and s01-D15, which haipipe-run 0.31.0 already states.


JL's notes on ladder-v3 (261006)
--------------------------------

1. Studio drawing: tree-based, lines and boxes, more room to modify and scratch; keep the
   human's scratch.
2. `chat/`: a Claude Code or Codex session can be saved here.
3. Report drawing: make things clear, more figures and displays of the results; the human
   makes only minor changes or suggestions.
4. Each section of an agent's reply links to a Studio topic or a Question (report) topic.
   Studio for creation, Report for presentation. Worked out in `../s04-studio-and-report/`:
   a report's drawing is generated from named studio frames.
5. Frame 2, task Block, `studio/` entry: "this need to be modified". Done in v4: the entry
   now shows `sNN-<topic>/` with its face, drawing, builder and `chat/`.

6. Frame 2, task Block screen: "Scope" Space → "Block"; its "Block" subspace → "Scope" (the
   topics this Block covers); Block's subspaces = Scope / Resources / Studio (RoadMap Draw) /
   Questions. Frame 3: "Task" Space → "Job & Task". "How do we define the groups? j1N, j5N
   series?" Then: every Block workbench the same, Guide + Block + Job & Task + Delivery.
   Done in v4 as the proposed board level (frames 2-4 screens); frame 5's table still shows
   today's Spaces, read from each workbench-table.md.

Also fixed in v4: frame 1's Block skills named `haipipe-board`, which no longer exists; now
`haipipe-<family>` (each family's skill owns its board.md).


Open
----

0. Runs: applied 261006 as haipipe-run 0.31.0 and haipipe-project 0.11.0 (audit and update
   at every level); `run-skill-draft.md` records what was taken. Next: haipipe-task's ticket
   template writes `runs/<run>/`, then the move, one Block at a time.
1. Paper: is the built paper the Board's `delivery/`, or each version Job's? (red in frame 2)
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
