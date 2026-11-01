# s57 · Task UI: Report · views proposal

b17.j03.t03-s57:theme_work.work_workbench_pages.task_page @ task_ui_report · written 2026-10-31 18:52 EDT · its choices
for JL are the form `../../runs/r01_collect_task_report_views/` (Q1 to Q5); its previews are written by
`../../scripts/build_r01_previews.py`.

A work Task's page, Report section (verb: check). A work Task makes one result through its Runs: a hard `rNN_` Run
keeps `result/` (`RUN-REPORT.md`, `tables/`, `runtime.yaml`), a soft `run-<type>-<target>` Run writes into something
else and keeps `passes/pNN-MMDD/` (haipipe-run SKILL.md, Hard and soft Runs). The Report shows that result; where each
Run stands lives in Work (s58).

Applied, not asked (JL's decisions, b17 r01 and the brief): MindMap first; then one view per delivery type, never per
name (s51-D01); a delivery opens from its tags (s51-D02); not made yet shows its planned look, marked planned (s51-D03);
no Findings, Answers or Questions (s51-D04); one word on each result, its current version (s51-D05); status rows live
in Work (r01 Q6); the map draws like the draft map (pill, short title, one plain paragraph box).


## (a) The view list

Buttons in the view-button-list, under the title, in this order:

1. **MindMap** (opens first): the Task as a map: its Aim, its topics, and what each Run found.
2. **The Task's type** (one button, named by its delivery type: `Skill`, `UI`, `Code`, `Draft`, `Display` or `Data`,
   frame.py `DELIVERY_TYPES`): its result, one row per current Run, the thing itself small, its parts behind tags.

A Task is one computation with one output contract (haipipe-task `ref/task-folder.md`, What earns a Task), and an
sNN's delivery is "one clean thing of one type" (haipipe-studio SKILL.md, One topic, one idea, one delivery, JL
261030). So a Task has one type and two buttons:

```text
b17 j01 t01_skill_section        MindMap · Skill     its Run writes haipipe-work SKILL.md (b17-s01 is skill)
b17 j03 t03_task_page            MindMap · UI        its sNN s57 · s58 · s59 each deliver a screen (ui)
b35 j01 t01_skill_section        MindMap · Skill     run-write-skill-section wrote haipipe-studio SKILL.md
a fit or regression Task         MindMap · Data      its hard Runs' result/: RUN-REPORT.md, tables/
```

Leaves today's Task Report: `Status` (it moves to Work, r01 Q6). Never added: `Findings`, `Answers`, `Questions`
(s51-D04); a view per Run name (s51-D01); `Delivery` (a right-rail section, not a view).

Where the type is read from, first match wins:

1. An sNN whose `delivery/render.yaml` names one of this Task's Runs in a piece's `by:` gives its `**Delivery type:**`
   (b17-s01 `delivery/render.yaml`: `ladder-section` by `j01_work_ladder_contract/t01_skill_section/runs/run-write-ladder-section`,
   and s01 is `skill`; b17-s04's `task-page` piece by `t03_task_page/runs/run-design-task-page`, and s04 is `ui`).
2. Else this Task's own sNN (three at most, b35 s01-D12) give theirs (t03_task_page: s57, s58, s59 are `ui`).
3. Else what its Runs wrote: a hard Run's `result/` is `data`; a soft Run's `writes:` is `skill` for a `SKILL.md`,
   `ui` for a `delivery/ui/`, `code` for `scripts/` or a `.py`, `draft` for `draft/`, `display` for `displays/`.
4. No type found and nothing made: the Report is MindMap alone.


## (b) Each view, its subsections in order

### View 1 · MindMap (opens first)

Its view-caption: "The Task as a map: its aim, its topics, and what each Run found." Drawn by the map renderer the
Block and Job use (`focus_page.parts_mindmap`, haipipe-mindmap), every item open, as the draft map draws a sentence.

1. **The Task (root)**
   - shows: a pill with the Task's folder name (`t01_skill_section`), its short title (the face's first line after
     ` · `), one box: its Aim and its close, one plain paragraph.
   - reads: `tNN_<task>/tNN_<task>.md`, its first line, `goal:` and `close:`.
   - empty: never; every Task has a face (no face: the folder name alone).
   - tags and actions: the pill opens the face (Source Markdown, the pop-out).
2. **Its topics** (only when the Task holds an sNN)
   - shows: one node per sNN in the Task folder, three at most: a pill with its folder name (`s57-task-ui-report`), its
     title, one box: its Topic line, "Delivers" its For line, "Still open" its first Open point (today's
     `topic_nodes`).
   - reads: `sNN-<topic>/sNN-<topic>.md` (`**Topic:**`, `**For:**`, `## Open`).
   - empty: the branch is left out.
   - tags and actions: ✎ on the pill opens its drawing (`sNN-<topic>.excalidraw`), as today.
3. **Its Runs, by role**
   - shows: one role node per role present, in this order: 🔨 make, 🔁 fix, 🔎 check, 📋 describe, 📊 figures,
     🧾 evidence, 📤 publish, 🧪 trial (role nodes only when two or more roles); under it one leaf per current Run: a
     pill with its version word (`r02` for a hard Run, `p01-1030` for a soft Run's newest pass, `planned` when nothing
     is made), the Run's folder name, one box: what it found.
   - the box: a hard Run's `result/headline.txt`, else `result/runtime.yaml` `headline:` or `summary:`; a soft Run's
     newest `passes/pNN-MMDD/pass.md` `## Summary`; a planned Run's ticket `ask:` (its `rNN_<slug>.sh` header or
     `run-<type>-<target>.md`).
   - reads: `runs/*/run.yaml` (`role`, `kind`, `status`, `passes`) through `frame.runs_of`, and the files above.
   - left out: collection Runs (`type: collect`, their Result is a person's answers: the Interactions section) and
     superseded Runs (`status: superseded`; pruned once unread, haipipe-run Keep only meaningful Runs).
   - empty: "Nothing to map yet." (today's words) when the Task has no sNN and no Run.
   - tags and actions: a leaf's pill opens that Run's result in the pop-out, the same page its row opens.

### View 2 · the Task's type (for example `Skill` or `Data`)

Its view-caption: "What this Task makes, one row per Run: the thing itself, its version, its parts." Its sections
are the roles present, a heading each, folding by the heading and open by default (haipipe-ui rule 4); one role, no
heading.

1. **🔨 make** (with 🔁 fix): the result itself; one row per current make or fix Run, newest first.
2. **🔎 check** and **📋 describe**: what audits or describes it (an audit's verdict, a Table Card).
3. **📊 figures**, **🧾 evidence** and **📤 publish**: what draws it, or hands it to a page or a delivery.
4. **🧪 trial**: tries before the full Run (smoke, preview), last.

One row per current Run, full width, one item per row:

1. **Head**: the Run's folder name (`r02_fit_fold00`, `run-write-skill-section`); on the right its one word, its
   current version: `r02` for a hard Run (a new version is a new Run), `p01-1030` for a soft Run (a new round is a
   pass), `planned` when nothing is made yet.
2. **Its line**: what it found, the same words as its map box (above).
3. **The thing, small**:
   - a hard Run: the first table in `result/tables/`, its first rows; else the first `result/*.png`; else the first
     paragraph of `result/RUN-REPORT.md`.
   - a soft Run: the thing it wrote, as it reads now: its `writes:` file at the part its newest pass changed (a
     `SKILL.md` section by its `<!-- render bNN-sNN <piece> -->` block, a screen in `delivery/ui/`, a file list for
     code).
   - not made yet: its planned look, marked planned: the piece's planned look from its sNN (its deck's first slide,
     `slides/idea-01-*.png`, or its `delivery/<type>/` draft), else its ticket's `ask:`.
   - a failed Run: its reason, `result/runtime.yaml` `failure:` (a truthful failure is a Result, haipipe-run).
4. **Tags** (at most three, each opens in the pop-out): a hard Run: `RUN-REPORT` · `Tables` · `Figures`, each only when
   its file exists (`result/RUN-REPORT.md`, `result/tables/`, `result/*.png` or `result/describe/`); a soft Run: its
   file (`SKILL.md`) · its pass (`p01-1030`, opening `passes/p01-1030/pass.md`) · `Ticket`.

- reads: `runs/<run>/run.yaml`, `result/headline.txt`, `result/runtime.yaml`, `result/RUN-REPORT.md`,
  `result/tables/`, `result/*.png`, `result/describe/`, `passes/pNN-MMDD/pass.md`, each `writes:` file, and the sNN
  `delivery/render.yaml` and `slides/` for a planned look.
- left out: collection Runs (Interactions), superseded Runs, the receipt's facts (status, started and finished,
  the passes list: Work), `heavy.yaml` pointers (Files).
- empty: every Run planned: each row shows its planned look, marked planned; no Run at all: one line, "Nothing made
  yet."
- actions: open only (Report checks; b16 s38's pick for the Section: read only, Accept and Reject stay in Work).


## (c) What s57 leaves to the other cells

- s58 · Task UI: Work: each Run's receipt row (status, started and finished from `result/runtime.yaml`, its passes
  list), what waits (a waiting form 🙋 first and orange, a Run to press), the Interaction button, a pass's whole record
  (ask, summary, changed, before and after), the ticket and config, Ask the agent.
- s59 · Task UI: Studio: its sNN cards (three at most) and their tags (Slide · Draw · Mind map · Work · Delivery).
- s54 · Job UI: Report: each Task's result, rolled up under the Job's type views.
- b17-s04: what every work page shares: path, title-&-section, view-button-list, the Aim goal-line, both rails, and the
  Interactions, Delivery, Timeline and Files sections.
- The Delivery section: what leaves the Task (`delivery/`) and whether it was sent.
- The Files section: `heavy.yaml` pointers and the folder itself.


## (d) Compared

**b16's matching cell, s38 · Section UI: Report** (`b16_theme_paper/j01_paper_workbench_pages/t03_section_page`):

1. Same: MindMap first; the Report reads only (s38 r01 Q1, its pick: Accept and Reject stay in Work); the map draws
   like the draft map.
2. Different: s38's second view is `Text` (sentences beside their cards), since a Section's result is prose; s57's is
   the result's type, since a work Task's result is what its Runs wrote.
3. Different: s38 keeps `Status` (MindMap · Text · Status) and asks whether to share Work's step list (r01 Q2, still
   waiting); s57 drops Status (r01 Q6) and keeps its own list, since Work's list is s58's.
4. Different: a Section's map is its paper content (JL 261031, b32 s42); s57 picks the Task's Runs, with the content
   map as Q5's other option.

**Today's real pages**:

1. Tools, b17 `j01_work_ladder_contract/t01_skill_section` (5623): Report is `MindMap · Status`; the map shows
   `Runs › [queued] run-write-ladder-section`; Status lists the Run with its status, no result.
2. The private research SPACE's Task page (5599, read for structure only): Report is `MindMap · Status`, Status a
   Runs list; Work › Progress shows a Run's output only from `result/figure.png` or `preview.png` with
   `headline.txt` (`focus_page.output_of`), so `RUN-REPORT.md` and `tables/` never show, and a soft Run's pass shows
   nowhere.
3. Kept: MindMap first. Changed: Status leaves; one type view puts the result in place, which answers the cell's Idea
   (a Report listed receipts, not results; the newest result was clicks away; a soft Run's pass had no place).
4. The older work workbench (`servers/workbench-work/work_progress.py` `render_task_about`, JL 261022: "给 task 也来一个
   这种 report"): a Task's pop-out report with its Runs by role, each with its finish time and one-line result, and its
   figures Runs' charts. s57 keeps the role groups and the one-line result, moves finish times to Work, and adds the
   thing itself.


## (e) Alternatives weighed

1. **View list** (asked, Q1). A · one view, the Task's type, with charts and audits inside it (pick: one output
   contract, one button; JL 261030, one clean thing of one type). B · one view per type its Runs make (`Data` ·
   `Display` when a figures Run draws charts). Not offered: a fixed `Result` button (s57's first Design A drew it; it
   would be the one page whose button is not a type, against s51-D01).
2. **Which Runs** (asked, Q2, the face's red open point). A · every current Run, one row each, make Runs first (pick:
   a replaced Run is pruned, so each current Run is its own cut, a fold or a window). B · only the newest make Run,
   whole. C · the newest make Run whole, every other Run one line. "The newest Run" alone was refined to "the newest
   make Run": the newest folder may be an audit or a chart.
3. **A hard Run's row** (asked, Q3). A · its headline and its first table, small (pick: the number and its table at a
   glance). B · its `RUN-REPORT.md` whole, in place. C · its headline only. Every option opens the rest from tags.
4. **A soft Run's row** (asked, Q4). A · the thing it wrote, as it reads now; its pass opens from its version word
   (pick: check the thing itself; how it was made is Work's). B · its newest pass. C · both.
5. **The MindMap** (asked, Q5). A · the Task's Runs by role, each boxed with what it found (pick: one look, every
   Run's finding). B · its result's content, each report's sections boxed with their first sentence (as a draft
   Task's map is its paper content).
6. **A read sign** (weighed, not asked): `⬜ unread` in orange until a person writes `✅ read` in the face's
   `#### READING · current` table (haipipe-task `ref/task-page.md`). Not picked: no Task in use keeps a READING table
   (the research Task read for structure has none); r01 Q6 asked for one word, the current version; the focus page
   writes nothing yet (Phase A, read only). Revisit when Report gets a sign.
7. **Status as a Report view** (not asked): decided, it moves to Work (r01 Q6).
8. **Report shares Work's view list** (weighed, not asked), as the paper Board does (s33-D01): not here, since the work
   Report is by type (s51-D01) and Work's list is s58's to propose.
9. **Collection Runs as rows** (decided here): no; their Result is a person's answers, shown in Interactions and on
   Work rows (b16 t01 r04 Q6).
10. **Role order** (decided here): make first, trial last, against the older order trial first (JL 261020): the
    Report checks what was made.
11. **Receipt facts on a row** (decided here): no; started, finished and status are Work's.
