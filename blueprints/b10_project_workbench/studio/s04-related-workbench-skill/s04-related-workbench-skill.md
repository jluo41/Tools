s04 · Related: its workbench and its skill
==========================================

New on 261011 (JL: "how should I make the s02 studio, s03 delivery, and s04 related, and s05 report,
and s06 run"). The numbers follow the screen: the top row's Studio and Delivery are s02 · s03, Related,
folded inside the Studio, is s04, the work row's Report and Runs are s05 · s06. s04 was once
s04-studio-and-report, merged into s02 on 261010; its old decisions are s02-D22 to D30 since 261011,
so the ids here start at s04-D01 and every id names the topic it lives in.

**Tags:** `Structure` · `UI`

**Stage:** shaping

**Topic:** the Related seen from both sides: its workbench (the Studio's second folding part, under
the topic cards, since 261011; was Description › Related) and its skill (`/haipipe-related`, made
261011, s04-D09). What comes in from outside (a meeting, a paper, a file we were sent, an email, a repo
or dataset)
is kept once, at the Block, in its one `related/`, one row each in `related/related.md`; the studio
topics and reports it feeds read it from there. It is Delivery's twin on the other side: `related/`
is what came in, `delivery/` what went out.

**Feeds:** `reports/` q07_workbench_mapping · q08_workbench_base


Files
-----

```text
s04-related-workbench-skill/
├── s04-related-workbench-skill.md            this face
├── s04-related-workbench-skill.excalidraw    two frames: the idea (sources, related/, table, screen); In Tools
├── s04-related-workbench-skill.png           its preview
├── .s04-related-workbench-skill.seed.json    generated snapshot for preserving marks
└── build_s04_related_workbench_skill.py      the builder, the same shape as s03's
example: ../../related/ (b10's own: related.md and meetings/)
```


In Tools
--------

Where its skill and code sit, under `Tools/plugins/haipipe-toolkit/`. The drawing's "In Tools" frame
reads the same off the disk on every build: the skill's folder as it is, its version, and each
function looked up in its file (JL 261011: "show what are the skills related folders in the Tools").

```text
skills/1_base/project/
├── haipipe-studio/     s02 Studio
├── haipipe-delivery/   s03 Delivery
├── haipipe-related/    s04 Related    ◀ this topic
├── haipipe-report/     s05 Report
└── haipipe-run/        s06 Run
servers/workbench/frame.py         related_items · _related_folder · related_view · studio_related
                                   _related_preview · docx_preview · eml_preview · _related_set_groups
servers/workbench/page_reader.py   markdown_document, a .md that is no Page
```


Decided
-------

s04-D01 · A Block keeps one `related/`, shared by its Jobs and Tasks, for what came in from outside:
    `meetings/` (notes or a transcript, `YYYY-MM-DD-HHMM <title>.md`), `papers/` (open-licensed PDFs
    only), `files/` (what we were sent: a draft, a form, slides), `emails/` (since s04-D08), each made
    with its first item, and one table, `related.md` (kind · date · item · link · feeds · group; `group`
    since s04-D07; kind meeting · paper · file · email · repo · dataset · tool · project). A repo,
    dataset, tool or project is only a row with its link. Carries b10 s01-D27 and s01-D34 on (JL
    261011: "to put the meeting, and related papers, etc. or some source materials"; "maybe we just
    use the related").
s04-D02 · What lands in `related/` is read only: it is not edited again; notes about it go to a
    studio topic or a report. A deep read of a paper is a discovery Task's Run, linked from its row;
    a paper Board builds `reference.bib` from its paper rows at Delivery (s01-D21, D27).
s04-D03 · Related and the reports: a row's `feeds` names the reports (`qNN`) and topics (`sNN`) it
    feeds; a report cites the row the way it cites a Run; a meeting that raises a question becomes a
    Question in the Block's face and a `qNN`. Flow: related (in) → studio (think) → Jobs and Tasks
    (work) → reports (answer) → delivery (out) (JL 261011: "how it will related to the reports?").
s04-D04 · The paper theme's Audience Report › Related Papers shows the paper rows only: meeting and
    file rows are left out (`NOT_PAPERS` in servers/workbench-paper/paper_theme.py, 261011).
s04-D05 · Related folds inside the Studio as its second part, under the topic cards; the top row stays
    Guide · Studio | Block · Job · Task | Delivery (JL 261011: "put the related as the second collapse
    part in the box of the studio items", "I might just want to keep Guide, Studio | Block, Job, Task |
    Delivery"). Folded by default; a `space=Related` link (or an older Description › Related one)
    opens the Studio with it unfolded. Not in the Guide: the Guide is the family's docs, the same in
    every Block, and related/ is this Block's own. Not a studio group: a topic group tags sNN topics, and a
    related row is no topic (it has its own groups, s04-D07). `frame.studio_related` (servers/workbench/frame.py); it was a top-row tab
    for an hour on 261011 (b16 session), and "after Delivery" (s01-D34) is dropped.
s04-D06 · The Related view draws one folding row per `related.md` row. An opened row is the file
    itself: a Word file through `/_board/workbench?view=docx&path=<file>` (text, tables, pictures and
    its comments in the margin), a PDF, Markdown, HTML or text file in a frame, a picture as a
    picture. No kind buttons; every theme shows this one view, and the paper's question cards stay
    in Report › Related Papers (s04-D04). JL 261011: "could we preview the word here?". Built by the
    b16 session (`frame.related_view`, `frame.docx_preview`). Its first grouping, by the `related/`
    subfolder a file sits in, was replaced the same day by s04-D07. A Markdown file that is no Page
    (a meeting's notes, `related.md` itself) opened on "Not a Page" (JL 261011, a screenshot); the
    reader `/_board/page` now shows any such `.md` as plain Markdown, its Obsidian quote blocks
    folded (`page_reader.markdown_document`).
s04-D07 · Related uses the Studio's group bar: Current · the groups · Untagged · + Group, as the topic
    cards above it do. A group is a name in the row's `group` cell, comma-separated like a topic's
    **Tags:** line; `related/_groups.txt` keeps the buttons' order (drag one sideways), as
    `studio/_groups.txt` does for topics. The subfolders only keep the files (until s04-D08 the same
    day: a subfolder is a group). A file no row names yet sat under Untagged ("no row yet"); dragging
    it onto a group writes its row, and a table with no
    `group` column gets one then. JL 261011 (relayed by the b02_aid_ai and sNN sessions): "🎯Current 0
    / Untagged 4 / + Group, for the studio". Built by the sNN session: `frame.related_items`,
    `_related_set_groups`, `group_list`, `studio_group_op(kind="related")`; workbench 1.15.1.
s04-D08 · A subfolder of `related/` is a group of its files, and `emails/` is one more subfolder (JL
    261011, on a screenshot of the meeting under Untagged: "this one is by default should be the
    Meeting, why you make it to be the untagged"; "we have the things like subfolders and can give
    them the group name"; "the related can have /emails as well"). An item's groups are its
    subfolder first (`meetings/…` → meetings, read off its link), then its `group` cell; the folder's
    group is never written in the cell, has no × on its chip, and changes only when the file moves,
    as a topic's **Type:** line does in the Studio. Untagged keeps only items with no subfolder and an
    empty cell (a web link). An email is saved from the mail app as it came,
    `emails/YYYY-MM-DD-HHMM <subject>.eml`, kind `email`; opened, it shows From · To · Cc · Date ·
    Subject, its text and its attachments by name (`frame.eml_preview`, `/_board/workbench?view=eml`),
    an HTML-only body in a sandboxed frame so nothing in it runs. An email holding patient or
    personal data does not land here. Code: `frame._related_folder`, `related_items`,
    `_related_set_groups`, `_group_parts(fixed=)`.
s04-D09 · `/haipipe-related` is a skill of its own, `skills/1_base/project/haipipe-related/` (0.1.0),
    beside haipipe-studio, haipipe-delivery, haipipe-report and haipipe-run: one skill per shared
    Block shelf (studio/, related/, delivery/) and per level part (reports/, runs/). Not a part of
    haipipe-block (the Block face) or haipipe-project (the Project root): related/ has its own folder,
    table, groups and view, as delivery/ does. JL 261011: "for the s04, do we need a haipipe-related
    skill for it? and where it should be in the Tools?". The workbench's `run-add-related-<slug>`
    button names it; haipipe-studio and haipipe-delivery point to it.


Open
----

1. Settled 261011 by s04-D05: Related folds inside the Studio, under the topic cards.
2. Settled 261011 by s04-D09: `/haipipe-related`, its own skill in `skills/1_base/project/`.
3. A Job's own inputs (a site visit's notes): its Job folder, or the Block's `related/` with
   `feeds: jNN`? An email now goes to `related/emails/` (s04-D08), its row naming the Job it feeds.
4. The Project root's `external/` (pinned upstream code and data, s01-D06): rows here that point to it,
   or kept apart?

(write here, or mark the drawing in red)
