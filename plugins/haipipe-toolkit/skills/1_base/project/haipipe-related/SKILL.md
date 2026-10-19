---
name: haipipe-related
description: >-
  Owns the Block's Related, shared across Block, Job and Task views: the one physical `related/`
  folder of a Block, where what came in from outside is kept once, as it came (meetings/,
  papers/, files/, emails/); its one table, `related/related.md` (kind · date · item · link ·
  feeds · group); its groups (a subfolder is a group of its files, the group cell adds more,
  `related/_groups.txt` keeps the button order); and the Related view folded inside the Studio.
  Use to add a meeting's notes, a paper, a file we were sent or an email and write its row, say
  which topics and reports an item feeds, or check that no Job or Task keeps its own related/.
  Trigger: related, related/, related.md, meeting notes, transcript, email, file we were sent,
  add a paper, /haipipe-related.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.3.1"
  last_updated: "2026-10-19"
  # version history: ./CHANGELOG.md
---

# /haipipe-related · what a Block sits beside

A Block keeps what came in from outside once, in its `related/`: a meeting's notes, a paper, a
file we were sent, an email, a repo or a dataset. It is Delivery's twin on the other side:
`related/` is what came in, `delivery/` what went out.

```text
haipipe-related   related/               came in     one per Block, read by every level
haipipe-studio    studio/sNN-<topic>/    think       one per Block, opened from every level
haipipe-report    reports/qNN_<topic>/   answer      every level its own
haipipe-delivery  delivery/              went out    one per Block, opened from every level
```

On a paper Board, `haipipe-paper-related` marks the closest papers in this table (`bears on` = `Closest: <type>`,
`key` ★) and reads them in `studio/s10-related-work-map/` and s11-s19; this skill still owns the table and the files.

Decided in b10 (Tools/blueprints/b10_project_workbench): s01-D27 and s01-D34 (the folder and its
table), s04-D01 to s04-D09. Its design topic is `studio/s04-related-workbench-skill/`.


The folder
----------

```text
<block>/related/
├── related.md          one row per item: kind · date · item · link · feeds · group
├── _groups.txt         the group buttons, in order (the workbench writes it)
├── meetings/           YYYY-MM-DD-HHMM <title>.md, notes or a transcript as it came
├── papers/             <author><year>.pdf, a free copy: open-licensed (private repo: also arXiv, PMC)
├── files/              what we were sent: a draft, a form, slides, as it came
└── emails/             YYYY-MM-DD-HHMM <subject>.eml, saved from the mail app
```

1. **Block only**: Jobs and Tasks keep no `related/`; they read the Block's.
2. **As it came**: what lands here is not edited again; notes about it go to a studio topic or a
   report.
3. **Made with its first item**: a subfolder exists once something is in it; any other
   subfolder name works too.
4. **Links, not copies**: a paper with no free copy, a repo, a dataset or a tool is only a row with
   its link; nothing else is copied into the SPACE. A paper row opens on its PDF when one is kept
   (JL 261013: "we want here to show the pdf attached"), so keep the free copy when there is one: an
   open-licensed version anywhere, and in a private repository an arXiv preprint or a PMC copy too.
   Check the PDF's first page carries the paper's title before its row links it.
5. **No private data**: an email or file holding patient or personal data does not land here.


The table: related.md
---------------------

```text
| kind    | date       | item                 | link                              | feeds     | group |
| meeting | 2026-10-10 | Workbench structure  | `meetings/2026-10-10-1800 ….md`   | s02 · s03 |       |
| email   | 2026-10-09 | IRB question         | `emails/2026-10-09-0900 ….eml`    | q01       | IRB   |
| paper   | 2024       | <author><year>       | https://doi.org/…                 | q02       |       |
```

1. **kind**: meeting · paper · file · email · repo · dataset · tool · project.
2. **link**: a path under `related/` in backticks, or a web address.
3. **feeds**: the studio topics (`sNN`) and reports (`qNN`) it feeds; a report cites the row the
   way it cites a Run.
4. **group**: extra groups, comma-separated; the subfolder is never written here.
5. **bears on** (a paper Board): what a paper bears on (the closest work, the background, an idea, a
   research question), comma-separated. Audience Report › Related Papers groups its cards by it;
   the Studio's groups stay the kinds.


Groups
------

An item's groups are its subfolder first, then its `group` cell (b10 s04-D08, JL 261011: "we have
the things like subfolders and can give them the group name"). A meeting in `meetings/` is in the
`meetings` group without any row edit; dragging it onto another group writes that name into its
cell. The subfolder group has no × and changes only when the file moves. A row kept as a web link has
no subfolder, so its `kind` stands in (JL 261013: the groups are "things like meeting, email,
paper"): the bar reads by what each item is. Untagged holds only a row with no subfolder, no kind and
an empty cell. `related/_groups.txt` keeps the buttons' order, as `studio/_groups.txt` does for the
topics. What a paper is about is not a Studio group: it goes in `bears on`.


Versions
--------

1. **Keep each version**: a second draft goes beside the first, its version in its name
   (`Proposal-v1.docx`, `Proposal-v2.docx`), never over it (b10 s04-D10, JL 261014).
2. **One item**: the workbench folds them by Delivery's rule (`frame.version_roots`), newest first,
   a row of versions, each opening its own preview.
3. **One row is enough**: the item keeps the row one of its versions has; a new version needs none.
4. **Two formats are not versions**: a `.docx` and its PDF print stay two items, each with its row.


On screen
---------

1. **Inside the Studio**: Related is the Studio's second folding part, under the topic cards; the
   top row stays `Guide · Studio | Block · Job · Task | Delivery` (s04-D05).
2. **One row per item**: opened, a row is the file itself: Markdown read in place (an Obsidian
   note's quote blocks folded), Word from its package, a deck drawn slide by slide, an email with
   its headers, a PDF, a page or a picture (s04-D06); versions of one thing are one row (s04-D10).
3. **The group bar**: Current · the groups · Untagged · + Group, the Studio's own (s04-D07).
4. **The code**: `servers/workbench/frame.py` (`related_items`, `related_view`, `studio_related`,
   `_related_preview`, `docx_preview`, `eml_preview`, `_related_set_groups`), and
   `servers/workbench/page_reader.py` (`markdown_document`) for a Markdown file that is no Page.


Add an item: run-add-related-<slug>
-----------------------------------

1. **Put the file**: as it came, in its subfolder; name it by date and title.
2. **Write its row**: kind, date, item, link (in backticks), feeds; group only if it needs more.
3. **Say what it feeds**: a meeting that raises a question becomes a Question in the Block's face
   and a `qNN` (haipipe-report); a thought it starts goes to a studio topic (haipipe-studio).
4. **Check**: open the Studio's Related; the item sits under its subfolder's group.

An email is saved from the mail app as `.eml` (Outlook and Apple Mail: File › Save As); a thread
pasted as text may be a `.md` instead.


Boundary
--------

| Owner | Owns |
|---|---|
| `haipipe-related` | the Block's `related/` folder, `related.md`, its groups, the Related view |
| `haipipe-paper` | a paper Board's `reference.bib`, built from its paper rows at Delivery |
| `haipipe-discovery` | a deep read of a paper: a discovery Task's Run, linked from its row |
| `table-papers` | the papers behind a workbench (Guide › Related Paper), not a Block's related/ |
| `haipipe-studio` | `studio/`: Related folds inside it, but its topics are no related items |
| `haipipe-delivery` | `delivery/`, the twin: what went out |


Files
-----

```text
haipipe-related/
├── SKILL.md
├── CHANGELOG.md
└── agents/openai.yaml
```
