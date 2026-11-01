# s54 · Job UI: Report · views proposal

for: b17.j03.t02-s54:theme_work.work_workbench_pages.job_page @ job_ui_report
form: `../../runs/r01_collect_job_report_views/` (three questions; my picks Q1 B, Q2 A, Q3 A); its previews are
written by `../../scripts/build_r01_previews.py`
date: 2026-10-31 · status: proposed, waiting on JL's answers

A work Job page's Report section (verb: check), on the focus page (`layout=focus&section=report`). A work Job makes
one sNN's delivery through its Tasks: `j01_work_ladder_contract` makes s01's three skill pieces (one per Task, named in
`s01-work-ladder/delivery/render.yaml`); `j03_work_workbench_pages` makes s04's three page pieces.

Applied, never re-asked (s51-D01 to D06, s52-D01, b16 t01 r04 and r07): the Report is MindMap first, then one view
per delivery type, never one per delivery's name; a delivery opens from the tags below its sNN; a delivery not made
yet shows its planned look, marked planned; each delivery carries one word, its current version; no Questions, so no
Findings, Answers or Questions view; where things stand lives in Work; one Interaction button wherever an item shows,
🙋 and orange when a form waits.


## (a) The view list

```text
button     opens   what it shows, one line
MindMap    first   how the Job is built: what it makes, its Tasks in order, each Task's Runs
<Type>             what the Job hands over: the delivery, then each piece and the Task that makes it
```

`<Type>` is one button per delivery type of what the Job makes, named by the type (Skill · UI · Code · Draft ·
Display · Data, the order of `frame.DELIVERY_TYPES`). A work Job makes one sNN's delivery, so it is one button:

```text
j01_work_ladder_contract    MindMap · Skill     (s01, Delivery type: skill)
j02_workbench_work_skill        MindMap · Skill     (s02, Delivery type: skill)
j03_work_workbench_pages    MindMap · UI        (s04, Delivery type: ui)
a Job that makes nothing    MindMap             (no type button: a section with nothing in it does not show)
```

Gone from today's `MindMap · Status`: Status (`overview["standing"]`, `status_now_html`); its rows live in Work ›
Tasks (s55; s52-D01). Never shown on a work Job: Findings, Answers, Questions (s51-D04), and Block UI · Job UI ·
Task UI (a theme Block's own views, from board.md `ui-block:`, `ui-job:`, `ui-task:`).

**What counts as "what the Job makes"** (Q2, my pick A): the Block's sNN whose `delivery/render.yaml` names a Run of
this Job in a piece's `by:` (s01 from j01, s02 from j02, s04 from j03). When no render.yaml names the Job, two
fallbacks in order: the sNN whose face `**For:**` says "made by `../<job>/`"; then an sNN named after the Job
(`sNN-jNN-<job>`, the shape research SPACEs use for a Job's own topic). The sNN that sit in the Job's Tasks (j03's
s51 to s59) are not listed as deliveries of their own: they show inside the piece their Task makes. Today's
`focus_page.work_root(topic)` maps an sNN to its Job by the same render.yaml `by:` first, then by the Job it sits in;
the list here uses only its first half.


## (b) Each view's subsections

### View 1 · MindMap (opens first)

Caption: "How it is built, as a map: what it makes, its Tasks, their Runs." Drawn by haipipe-mindmap's renderer
(`mmmap.draw`), as `focus_page.parts_mindmap` draws it today; every point open; each point a pill, a short title and
one plain paragraph box (the draft map's rule, b32 s42). Its branches, top to bottom:

1. **Root**: the Job's folder name, `j01_work_ladder_contract`. Reads the folder. Always there.
2. **Makes** (Q3, my pick A): one point per sNN the Job makes. Pill: its folder, `s01-work-ladder`; title: its short
   name, `work ladder`; box: its Topic's first sentence, "Delivers" and its `**For:**` (without "made by"), then its
   one word (`planned`, or `v<N>`). Reads `s01-work-ladder/s01-work-ladder.md` (`**Topic:**`, `**For:**`) and the
   newest `-v<N>` in `s01-work-ladder/delivery/`. Action: its label opens its drawing (`s01-work-ladder.excalidraw`,
   ✎), as the Block map's topics do. Empty: no Makes branch.
3. **One branch per Task**, in the Job face's `## Tasks` order: grey line, its folder `t01_skill_section`; title, its
   face's title `Write haipipe-work's ladder section`. Reads `j01_work_ladder_contract.md` (`## Tasks`) and
   `t01_skill_section/t01_skill_section.md` (line 1). Today the order is the folders' (`frame.children`, sorted).
4. **Under each Task, its own sNN first** (three at most): pill, its folder; title, its face title; box, Topic,
   Delivers and Still open, as the Block map draws a topic. Reads `tNN_<task>/sNN-*/sNN-*.md`. Empty: none drawn.
   Today none show: `parts_mindmap` looks for topics only in the Block folder, so j03's map has none of s51 to s59.
5. **Under each Task, its Runs**: pill, the card's status word (`queued`, `done`, `planned`, `waiting`); title, the
   Run's folder; box, its ticket's `ask:` line (no point without its sentence). A collection Run that waits on JL
   shows its pill orange. Reads `tNN/runs/<run>/run.yaml` (`status`) and `<run>/<run>.md` (`ask:`). Empty: a Task with
   no Runs shows its title alone. Today a Run point has no box.

Empty view: "Nothing to map yet." (no Tasks, no sNN). Actions: the map's own (pan; ▾ folds one point; a label opens
its drawing); nothing is edited on this page.

### View 2 · `<Type>` (Skill on j01, UI on j03)

Caption: "What this Job hands over." Two sections, a heading each; they fold by their heading, open by default
(haipipe-ui rule 4).

1. **The delivery**: the sNN's card, the same card the Block's Report (s51) and the Studio draw.
   - picture: its deck's first slide (`s01-work-ladder.slides.json` names `slides/idea-01-rungs-one-shape.png`), else
     its drawing `s01-work-ladder.png`; which one is s51's open question, and the Job follows it;
   - name: its address, `b17-s01:theme_work @ work_ladder` (`frame.topic_label`);
   - one line: its `**For:**` without "made by" (this page is the maker);
   - one word: its current version, the newest `-v<N>` in `delivery/` (haipipe-delivery's version rule,
     `frame.delivery_items`), else `planned` (s51-D03, D05);
   - tags below: Slide · Draw · Mind map · Work · Delivery (s51-D02), each a pop-out: `s01-work-ladder.slides.html`,
     `s01-work-ladder.excalidraw`, `s01-work-ladder.mindmap.md`, its Work (`work_root`: this Job), its Delivery
     (`topic_delivery`: its files, and where each piece goes); then Interaction when a collection Run's `for:` names
     it, "🙋 Interaction" in orange when one waits. Today s04's card is orange (`b17_theme_work/runs/
     r02_collect_interactions_page` waits); s01's is plain (`b17_theme_work/runs/r01_collect_theme_alignment` is planned).
   - reads: the sNN face (`**For:**`, `**Delivery type:**`, `**Tags:**`), `<sNN>.slides.json`, `delivery/`,
     `focus_page.card_interactions`. Empty: the view is absent.
2. **Its pieces, by Task** (Q1, my pick B): one row per piece in the sNN's `delivery/render.yaml`, in the Job face's
   `## Tasks` order; one item per row.
   - name: the words before the colon of its `code:` (`ladder-section`), with its one word: `planned` until its Run is
     done, then the delivery version that holds it;
   - made by: its Task and Run, from `by:` (`t01_skill_section · run-write-ladder-section`);
   - the piece itself, small, on the right: once made, the agreed copy in `delivery/` (a skill piece's text, a ui
     piece's screens, a code piece's output named in the Run's `writes:`); before, its planned look marked planned:
     where it lands (`writes:`, here haipipe-work `SKILL.md` › The work ladder) in the words of the ticket's `ask:`;
     on j03, a piece's three screens (block-page: s51 · s52 · s53), each opening its card in its Task's Studio;
   - tags: Open (the piece whole, in the pop-out) · Task (that Task's page) · Interaction when the Task holds a form.
   - reads: `delivery/render.yaml` (`pieces[].code`, `.by`), each Run's `run.yaml` (`target`, `status`, `writes`,
     `passes`), its ticket (`ask:`, `close:`), haipipe-studio's `render_delivery.py` state (`same`, `rendered`,
     `differs`, `not placed`).
   - empty: no render.yaml, so nothing says which Task makes which piece: one row per Task instead, its newest Run's
     result (the first file in its `result/`), else "no result yet".


## (c) What it leaves to the other cells

- s55 (Job UI: Work): the Task rows in order, each with its state and what waits, and their Runs (its open question);
  a waiting form's row, orange and first. The Report never repeats them as rows.
- s56 (Job UI: Studio): the sNN as topics to think in (groups, cards, talk and sketch), and whether a Job's Studio
  shows the Block sNN it makes (its open question).
- s57 (Task UI: Report): a Task's whole result. A piece row's Task tag lands there; its Open tag shows the same piece.
- s51 (Block UI: Report): the delivery card itself and its picture (its open question). A Job shows the same card.
- b17-s04 (what every work page shares): path, title, goal-line, right rail, the pop-out, and which section a Job
  opens on (Work today, haipipe-ui's level table).
- Owners outside j03: design_b02_workbench writes the code in `servers/workbench/focus_page.py`; haipipe-studio owns
  what render.yaml means (`render_delivery.py`); haipipe-delivery owns versions (`-v<N>`).


## (d) Compared with b16's s35 and today's real pages

**b16 s35, Version UI: Report** (a paper version is a Job; its Tasks are Sections). Its sketch: MindMap · Text ·
Status, open on Status, a row per Section saying which step waits; its form (`r01_collect_version_ui_report`,
waiting) asks whether Text is every Section's text in reader order (its pick) or the built PDF. Later decisions:
the version's views are Draft-Main · Draft-Appendix · Display-Main · Display-Appendix (s36-D02), Report is to share
that list (in progress, `r02_collect_version_ui_work/applied.md`), and on the Board the mind map is a section inside
each view (s32-D06).

```text
                     b16 s35, a paper version          s54, a work Job (proposed)
the Job makes        one manuscript, from Sections     one sNN's delivery, from its Tasks' pieces
views                bands, shared with Work           MindMap, then one per delivery type
MindMap              a section inside each view        its own view, first
Status               in the sketch; Work shows steps   gone; Work shows Task rows
each Task's result   Text: every Section, in order     pieces by Task, each small (Q1 B)
```

Same: a Job's Report shows the thing the Job makes, in its parts, in the order the Job makes them; b16's "every
Section's text, in reader order" is this cell's "each Task's piece". Differs, and why: the work theme keeps the
MindMap as a view and names views by delivery type (JL's work decisions, s51-D01); a work Job makes one delivery of
one type, so it needs no bands; Status goes because where things stand lives in Work (s52-D01).

**Today's pages.** On 5623, `j01_work_ladder_contract` › Report shows MindMap · Status; its map holds the root and
three Task branches, each with one `queued` Run point and no boxes; s01, which j01 makes, is not on it (it hangs at
the Block); Status lists the three Tasks, each 🔴 open, the rows Work already shows; the right rail is Report · Work ·
Interactions · Delivery · Files, and the page opens on Work. `j03_work_workbench_pages` › Report is the same two
views; its map lists each Task's Runs and none of s51 to s59. On 5599, a research SPACE's Job page (structure only)
shows the same MindMap · Status; its map lists its six Tasks; its sNN sits at the Block, named after the Job
(`sNN-jNN-<job>`), and nothing on the Job's Report says what it hands over. So: no view says what a Job hands over,
the map misses what the Job makes and the Tasks' own sNN, and Status repeats Work.


## (e) Alternatives weighed

1. **View list.** A · MindMap, then one view per delivery type it makes (pick: s51-D01 at every level, one rule). B ·
   MindMap alone, the delivery as a section under the map (not offered: it re-asks s51-D01). C · keep Status (not
   offered: s52-D01). D · a view per sNN name (not offered: s51-D01).
2. **Each Task's result** (Q1). A · the card only. B · the card, then one row per piece, by Task (pick). C · the card,
   then each Task's whole result. B, because a Job exists to make its delivery and its Tasks make the pieces: one
   screen says what is made and what is still planned, and the whole result is one click away (Open) and on the
   Task's own Report (s57). A leaves a Job's page one card, which the Block's Report already shows; C repeats every
   Task's Report and runs long.
3. **Which deliveries** (Q2). A · only what it makes, the Tasks' sNN inside its pieces (pick). B · also the Tasks' own
   sNN as cards (today's `work_root` rule). A, because each screen shows once, inside the page it belongs to; B lists
   ten flat cards on j03, nine of them s04's pieces again.
4. **The map's first branch** (Q3). A · Makes, then the Tasks (pick). B · Tasks and Runs only. A, because the map
   then says what the Job is for before how; the Skill view still shows the delivery itself, so the map keeps one
   line of it, not the card.
5. **How a Job finds what it makes** (decided here). render.yaml `by:` (pick: it already names each piece's Run, and
   `work_root` reads it). A new face field `makes: s01` (no: a second place to keep one link). The `**For:**` text and
   the `sNN-jNN-` name (fallbacks only: free text, and research SPACEs' naming).
6. **A Run point's box** (decided here). The ticket's `ask:` (pick: the draft map's rule, no point without its
   sentence). Today's empty point (no). The ticket's `close:` (no: it says when the Run is done, not what it does).
7. **A piece's word** (decided here). `planned`, then the version that holds it (pick: s51-D05, the current version).
   The Run's status (no: status rows live in Work). The render state, in place or changed (no: the Delivery pop-out's).
8. **A made piece's thing** (decided here). The agreed copy in `delivery/` (pick: the thing handed over). What sits at
   its target now (no: the Delivery pop-out's second part shows that). The Run's `result/` (fallback, a Job with no
   render.yaml).
9. **The card on a Job page** (decided here). The same card and tags as the Block's Report and the Studio (pick: one
   card everywhere). A larger Job-only card (no).


## The code change, named for design_b02_workbench

In `servers/workbench/focus_page.py`, after JL answers r01:

1. `render()`: at a work Job, no `overview["standing"]`; after `"mindmap"`, one view per delivery type of the sNN in
   `job_deliveries(job)`, keyed by the type, named Skill, UI, Code, Draft, Display or Data.
2. `job_deliveries(job, root)` (new): the Block sNN whose `delivery/render.yaml` `by:` starts with the Job's folder;
   then the two fallbacks in (a).
3. `parts_mindmap()` at a Job: a Makes branch first; Tasks in the face's `## Tasks` order; each Task's own sNN; each
   Run point's box from its ticket's `ask:`.
4. `type_view(job, topic, root)` (new): the card (`studio_html`'s row, the version word in place of the stage), then
   the piece rows from `render.yaml` and the Run cards.
5. `VIEW_WORDS`: "mindmap" at a Job, "How it is built, as a map: what it makes, its Tasks, their Runs."; each type
   view, "What this Job hands over."


## Files

- `s54-job-ui-report/result/views-proposal.md` (this cell): this proposal
- `runs/r01_collect_job_report_views/question_collection.md` (t02_job_page): the three questions
- `runs/r01_collect_job_report_views/option-q1-a.html` to `option-q3-b.html`: seven previews, generated
- `scripts/build_r01_previews.py` (t02_job_page): writes the previews from disk
