Paper ladder: the paper theme's Board · version · Task · Run
=============================================================

Delivery storage (JL 261010)
---------------------------

Only the Block owns a physical `delivery/` directory. Job, Task and Report
outputs retain their source identity under it: `delivery/jNN_<job>/`,
`delivery/jNN_<job>/tNN_<task>/<lane>/`, and
`delivery/reports/qNN_<report>/<lane>/`. The Block's own output uses
`delivery/<lane>/`. Job and Task Delivery views select their source subtree
and link to the whole Block Delivery; they never create local delivery folders.
Runs and Results remain with their source. Every writer and reader uses the
shared `haipipe-draft/src/common.py` Delivery helpers. Standalone Pages without
a Block keep their own output root; an orphan jNN/tNN must acquire a Block.

In this skill, a Page's or Job's `delivery/<lane>/` means its source subtree
inside Block Delivery. Old local lanes are read-only migration inputs. Rebuild
from source before removing generated output; preserve a hand-owned fragment
when the source cannot reproduce it. A storage migration grants no acceptance,
release, send or submission approval.



(JL 261007, designed in Tools/blueprints/b16_theme_paper: s11 Board, s12 version, s13 Section, s21 skills and Runs;
Q01 and Q04, and Q05 for this file; was paper-structure.md.) A paper sits on the shared ladder: one Board per
paper, one Job per version (one send to one venue), one Task per Section, the Abstract or a letter, and the Runs
that make and check them. On screen every level shows the shared frame's two rows (b10_project_workbench s02,
s01, s04-D05): the top row `Guide · Studio | Paper Board · Version ▾ · Section ▾ | Delivery`, whose Studio
(with Related folded under its topic cards) and Delivery are the Board's alone and open the same from every
level; and each level's own work row, `Description | Report | Work | Runs`. The paper workbench fills them (servers/workbench-paper/paper_theme.py).
`scripts/paper_ladder.py` makes each folder.

Read this reference when creating, naming or auditing a paper folder. `haipipe-paper` keeps only the routing in
its entrypoint; the Page, Story, Venue, comments and assembly owners stay authoritative for their own records.


The tree
--------

```text
paper/Paper-<Slug>/                  Board: one paper
├── board.md                         its face (haipipe-block): board-kind: paper-board · dialect: paper ·
│                                    story-current · spine · close ·
│                                    ## Pages (### J01 · j01_v<MMDD>_<desk>, its Tasks) · ## Questions (group: <topic>)
├── studio/                          Studio, the Board's only: the paper's thinking, one topic per folder; each
│                                    face has **Tags:** and **Stage:** (haipipe-studio topic contract)
│   ├── s01-ideation/                the ideas, ranked, admitted and eliminated (haipipe-paper-ideation)
│   ├── sNN-story-<desk>-<idea>/     a telling (haipipe-paper-story): identity · pitch · stakes · roadmaps;
│   │                                feeds: its Questions; an earlier telling is an ended topic
│   └── sNN-<topic>/                 any other topic: its drawings and its builder
├── reports/qNN_<question>/          Audience Report: one per research question (Answer · Evidence · Limits · Next)
├── runs/run-<type>-<target>/        a soft Run (haipipe-run, soft_run.py): run.yaml · its ticket .md · passes/pNN-<MMDD>/
├── venues/<venue>/                  call.md (dates, limits, format, review rules) · kit/ (haipipe-paper-venue)
├── related/                         what came in, kept once as it came, read only (/haipipe-related; b10
│                                    s04-D01, D02): related.md, one row per item (kind · date · item · link ·
│                                    feeds · group; a paper row adds key · venue · why here · read ↗ its
│                                    discovery deep read) · meetings/ · papers/ · files/ · emails/ (an .eml as
│                                    it came, b10 s04-D09) · any subfolder. A row's groups on the Studio's bar:
│                                    its subfolder first, then its group cell, comma-separated, a paper's
│                                    research questions among them (b10 s04-D07, D08)
├── delivery/                        Block-owned: jNN_<version>/ manuscript and Task outputs
└── j01_v<MMDD>_<desk>/              Job: one version, one send to one venue, named for the day it is sent
    ├── j01_v<MMDD>_<desk>.md        its face (haipipe-job): send · desk · venue · state · tells · from · goal ·
    │                                close · responds-to (the comments report it answers) · ## Tasks (in order) ·
    │                                ## Narrative (one row per Section; the compile order) · ## Questions
    ├── reports/ · runs/             the version's own Questions (the standing J1-J5 first) and Runs; its
    │                                drawings are Board topics (studio/sNN-<topic>/, b10 s09-D01)
    │   └── reports/qNN_<kind>-<MMDD>/   a comments batch: page-type: comments, in the version that answers it
    │                                (haipipe-paper-comments); feedback/ · sent/ inside; a meeting's
    │                                notes sit once in the Board's related/meetings/ (b10 s04-D01)
    ├── t00_abstract/                Task: the Abstract
    ├── t0N_<title>/                 Task: a Main Section, in reading order (t01-t19)
    ├── t2N_<title>/                 Task: an Appendix Section, A = t21 (t20-t29)
    ├── t3N_<title>/                 Task: a letter (t30-t39): t31_cover-letter · t32_response
    │   ├── tNN_<title>.md           its face: task-kind: page · page-type: section · the reader contract · story-row
    │   ├── draft/ · reports/        its writing and its own Questions (no studio/: the Board's)
    │   └── runs/ · results/              Page workflow; outputs in Block delivery/jNN/tNN/
    └── (no delivery here)          generated paper in Block delivery/jNN_<version>/
        ├── paper-build.toml         [pages] main = appendix = "../../jNN_<version>"
        └── latex/ · word/           generated, never edited
```

The next send (a revision, or another venue) is a new version, `j02_v<MMDD>_<desk>/`, made by `paper_ladder.py
next`: it starts from the one it follows (each Section's own writing copied, never its Runs, Results or build)
and answers that version's comments.


Each level
----------

```text
level     folder                    face                       made by                       its Runs
Board     Paper-<Slug>/             board.md                   paper_ladder.py board         runs/run-<type>-<target>/
version   jNN_v<MMDD>_<desk>/       jNN_v<MMDD>_<desk>.md      paper_ladder.py version|next  runs/run-<type>-<target>/
Task      tNN_<title>/              tNN_<title>.md             paper_ladder.py task          the Page workflow's (page.py open-run)
Run       runs/run-<type>-<target>/  run.yaml · ticket          paper_ladder.py run           passes/pNN-<MMDD>/ inside
```

A Space folder (`studio/`, `reports/`, `runs/`, `venues/`, `related/`, `delivery/`) comes with its first item,
never ahead of it (haipipe-block, haipipe-job): `paper_ladder.py` writes faces only. `studio/`, `related/` and
`delivery/` exist only at the Board; every level keeps its own `reports/` and `runs/` (b10 s09-D01, D02, D05). `answers:` on a face names a
Question id it answers (haipipe-report); a version that answers a comments report says `responds-to:` instead.

Every Run is `run-<type>-<target>`, with no date (JL 261007). Where a paper button does a base button's job it
makes the base Run (run-face-*, run-add-<jNN>, run-add-<tNN>, run-draw-<sNN>, run-ask-<qNN>, run-report-<qNN>,
run-figures-<qNN>, run-check-<qNN>, run-delivery-<target>; haipipe-run `ref/run-types-by-space.md`). A Board's or a version's Run is a folder in the shared Run
contract's shape (`haipipe-run`); a Section's Runs are the Page engine's, one ticket `runs/run-<kind>-<slug>.md` each. The run types of each level and Space, with the
skill, agent and sign of each, are `haipipe-paper-workflow/ref/run-cards.md`. Only a supporting Run of another
theme keeps its hard `rNN_` name, in its own work or discovery Task.


Naming and routing invariants
-----------------------------

- A version is `jNN_v<MMDD>_<desk>`: its series number, the day it is sent, its desk (JL 261007: "just use MMDD").
- A Task is named by series (JL 261007: "no more S-xxx"): `t00_abstract`; `t0N_<title>` for the Main Sections in
  reading order; `t2N_<title>` for the Appendix (A = t21); `t3N_<title>` for letters (t31 cover letter, t32
  response). The number band says the part; the title is lowercase-kebab.
- A comments batch is not a Task: it is a report of type comments, `reports/qNN_<kind>-<MMDD>/`, in the version
  that answers it (JL 261007).
- Group headings in board.md name their folder: `### J01 · j01_v<MMDD>_<desk>`, not a display title. The Paper
  Workbench binds the token after `·` to disk.
- A Section's story-row is its row in its version face's `## Narrative`; the row is recognized only when the
  Section's stem is its first table cell.
- Compile order is read only from the version face's `<!-- haipipe:compile-order:start -->` / `end` markers with
  `- ` ids.
- `reports/` (every level) and `studio/` (the Board only) are level folders, not Page groups: board.md lists
  neither. A report answers one
  Question in the shape `haipipe-question` gives every board's questions (`state:`, `answers:`,
  `answer-status:`, an Opening whose first paragraph is the answer, then Answer · Evidence · Limits · Next, and a
  `page.toml`). A research question's report is the G2 record.
- Task Roadmap work lives in the work theme's Task folders. The paper records the evidence need and consumes the
  accepted Result; it never executes the Task.


Source and delivery law
-----------------------

Section Tasks own the manuscript wording and their Page-local Evidence Results. Each Section's
`delivery/latex/<stem>.tex` body fragment is the version build's input. `haipipe-paper-assemble` regenerates the
version's `delivery/` from those fragments, the version face's compile order, the accepted display assets and the
declared build config, into the Board's `delivery/jNN_<version>/`. Generated Word and PDF files, frozen sends and old desk-room copies are never wording or
evidence sources.

Assembly may run early, but its manifest stays `DRAFT` until the intended Sections have current outlines,
evidence, display previews, Page delivery and Page CHECK closure. A send freezes the current build in the
comments report's `sent/`; the answering build is frozen in `released/`.


Older layouts
-------------

Two older layouts are still read by the Paper Workbench, and the carry-over scripts move a Board onto the ladder
once (`haipipe-paper/scripts/carry_over/`, each with a dry run, a record and an exact rollback):

```text
Paper-<Slug>/
├── board.md                         paper-root: .
├── A1-Story/  (or j00_story/)       → studio/ topics and reports/ Questions        topics_paper.py
├── Ba-<desk>-Main/                  → jNN_v<N>_<desk>/  (S-<desk>-Main-<N>-<Title>)  migrate_paper.py
├── Bb-<desk>-Appendix/              → jNN_v<N>_<desk>/  (S-<desk>-Appendix-<L>-<Title>)
├── Bc-<desk>-Round/                 → jNN_v<N>_<desk>/  (RD<NN> feedback Rounds)
└── delivery/                        → stays at Block; rebuild each version in delivery/jNN_v<N>_<desk>/
then: rename_tasks.py <board> --date MMDD   the version dated, S-… → t0N_/t2N_, RD<NN>-… → reports/qNN_<kind>-<MMDD>/
```

`migrate_paper.py` moves folders and keeps names; `rename_tasks.py` then renames each Page once (folder, face, plan
files, every source line that names it), recording the old names, so a receipt written before still resolves
through the record. Roll back newest first. The older `S-<desk>-…`, `RD<NN>-…` and dated `run-<kind>-<MMDD>-<slug>`
names stay readable; `page.py run-names` drops a dated Run's day.


Migration boundary
------------------

The former S01-S10 runtime, old desk-room layouts, SD/SA/NA aliases and shadow Page names are historical inputs.
Migrate active Pages in place, keep Story, Section, claim, Evidence and Run identities, and never edit a frozen
send or generated delivery by hand.
