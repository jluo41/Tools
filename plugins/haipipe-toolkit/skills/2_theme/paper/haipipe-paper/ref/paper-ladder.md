Paper ladder: the paper theme's Board · version · Task · Run
=============================================================

(JL 261007, designed in Tools/blueprints/b16_theme_paper: s11 Board, s12 version, s13 Section, s21 skills and Runs;
Q01 and Q04, and Q05 for this file; was paper-structure.md.) A paper sits on the shared ladder: one Board per
paper, one Job per version (one send to one venue), one Task per Section, the Abstract or a letter, and the Runs
that make and check them. Each level has the six Spaces of the base workbench (Description · Idea Studio ·
Audience Report | Work Details | Runs · Delivery); the paper workbench fills them
(servers/workbench-paper/paper_theme.py). `scripts/paper_ladder.py` makes each folder.

Read this reference when creating, naming or auditing a paper folder. `haipipe-paper` keeps only the routing in
its entrypoint; the Page, Story, Venue, comments and assembly owners stay authoritative for their own records.


The tree
--------

```text
paper/Paper-<Slug>/                  Board: one paper
├── board.md                         its face (haipipe-board): board-kind: paper-board · dialect: paper ·
│                                    story-current · spine · close ·
│                                    ## Pages (### J01 · j01_v<MMDD>_<desk>, its Tasks) · ## Questions (group: <topic>)
├── studio/                          Idea Studio: the paper's thinking, one topic per folder
│   ├── s01-ideation/                the ideas, ranked, admitted and eliminated (haipipe-paper-ideation)
│   ├── sNN-story-<desk>-<idea>/     a telling (haipipe-paper-story): identity · pitch · stakes · roadmaps;
│   │                                feeds: its Questions; an earlier telling is an ended topic
│   └── sNN-<topic>/                 any other topic: its drawings and its builder
├── reports/qNN_<question>/          Audience Report: one per research question (Answer · Evidence · Limits · Next)
├── runs/run-<type>-<target>/        a soft Run (haipipe-run, soft_run.py): run.yaml · its ticket .md · passes/pNN-<MMDD>/
├── venues/<venue>/                  call.md (dates, limits, format, review rules) · kit/ (haipipe-paper-venue)
├── related/related.md               the related work, one row per card; read rNN ↗ a discovery deep read
├── delivery/                        the Board's own (reference.bib); each version builds its own paper
└── j01_v<MMDD>_<desk>/              Job: one version, one send to one venue, named for the day it is sent
    ├── j01_v<MMDD>_<desk>.md        its face (haipipe-job): send · desk · venue · state · tells · from · goal ·
    │                                close · responds-to (the comments report it answers) · ## Tasks (in order) ·
    │                                ## Narrative (one row per Section; the compile order) · ## Questions
    ├── studio/ · reports/ · runs/   the version's own topics, Questions (the standing J1-J5 first) and Runs
    │   └── reports/qNN_<kind>-<MMDD>/   a comments batch: page-type: comments, in the version that answers it
    │                                (haipipe-paper-comments); feedback/ · meeting/ · sent/ inside
    ├── t00_abstract/                Task: the Abstract
    ├── t0N_<title>/                 Task: a Main Section, in reading order (t01-t19)
    ├── t2N_<title>/                 Task: an Appendix Section, A = t21 (t20-t29)
    ├── t3N_<title>/                 Task: a letter (t30-t39): t31_cover-letter · t32_response
    │   ├── tNN_<title>.md           its face: task-kind: page · page-type: section · the reader contract · story-row
    │   ├── draft/ · studio/ · reports/   its writing, its drawings, its own Questions
    │   └── runs/ · results/ · delivery/  the Page workflow's Runs and Results; delivery/latex/ is the fragment
    └── delivery/                    the generated paper of this version
        ├── paper-build.toml         [pages] main = appendix = "..": the version folder
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
never ahead of it (haipipe-board, haipipe-job): `paper_ladder.py` writes faces only. `answers:` on a face names a
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
- `reports/` and `studio/` are level folders, not Page groups: board.md lists neither. A report answers one
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
declared build config. Generated Word and PDF files, frozen sends and old desk-room copies are never wording or
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
└── delivery/                        → jNN_v<N>_<desk>/delivery/
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
