# Board skill set

The Board family turns one bounded work object into a readable, operable set
of Folder-backed Pages. It separates container, Page lifecycle, workbenches, and
sentence work so each rule has one owner.

## Ownership map

| Layer | Skill | Owns |
|---|---|---|
| Folder | `haipipe-folder` | neutral Page Face + Task Face contract |
| Board | `haipipe-board` | container, Groups, roster, build, serve, aggregate close |
| Page | `skills/page/haipipe-page` | readable frame, Folder-kind resolution, lifecycle entry |
| Page workflow | `skills/page/haipipe-page-workflow` | CONTEXT → OUTLINE → EVIDENCE → CONTENT → CHECK router |
| Workbench | `skills/page/haipipe-workbench` | workbench definition and roster law |
| Sentence | `skills/page/haipipe-sentence` | comment, edit, card, sentence-local record |
| Write routing | `haipipe-board-routing` | propose Board shape or route one anchored Page write |

Domain Page contracts live with their Folder or family owner. Task Pages are
owned by `haipipe-task`; Paper Pages by the Paper family. Insight and Design
are independent families: `haipipe-insight` owns InsightBoards and
`haipipe-workbench-design/ref/design-board.md` presents the Design family at Board grain.
Application is retired as their parent skill family. This folder does not
maintain a duplicate Page Type set.

## Page workflow

A Workflow is a list of Runs. Its definition is the Page owner's bounded
[Run Spec graph](../page/haipipe-page-workflow/ref/workflow-table.md);
actual instances retain their native identities and receipts. The table below
maps controller coordinates to workspaces; its rows do not count Runs.

| Controller coordinate | Skill | Primary work | Primary workspace |
|---:|---|---|---|
| context | `haipipe-page-context` | collect, resolve, freeze allowed context | off-stage Context record |
| structure | `haipipe-page-structure` | SHAPE bullets; SURVEY Evidence Items and Runs | Draft + Evidence Spaces |
| evidence | `haipipe-page-evidence` | LAND Supporting/Local Results; EMBED evidence | Evidence Space, then Draft Space |
| writing | `haipipe-page-writing` | WRITE from the approved plan and ready evidence | Page Content |
| check | `haipipe-page-check` | check one whole Page version | workflow receipt |

CONTEXT, OUTLINE, and EVIDENCE all use `haipipe-workbench-page` records.
CONTENT realizes them on the Page. CHECK evaluates the complete Page rather
than creating a second content surface.

## Run vocabulary

| Name | Identity | Owner |
|---|---|---|
| Page Writing Run | `rp-struct-NN`, `rp-scratch-NN_<target>`, `rp-sec-NN`, `rp-para-NN_Pxx[-Pyy]` | Page-owned bounded writing/structure target with feedback Steps and Versions |
| Task Run | native `rNN` or global run id | output-producing Task/Discovery family |
| Page Workflow Runtime execution | `workflow_runtime_id`, controller packet and receipt | `haipipe-page-workflow`; invoked by the `RUN` verb; coordinates actual Runs |

The Workflow Runtime envelope does not allocate an extra Run. Board hosts
these projections without renaming identities or becoming their authority.
The initial Structure Run is `rp-struct-01`; load
[Page Run families](../page/haipipe-page/ref/page-run-families.md) for RP/RE/RD
allocation. Historical compact `rp00_*`, `rpNN_pNN` and `prNN_*` records remain
readable compatibility input. New writers use the canonical typed IDs.
Serialized `run`, `cycle` and `next_cycle` fields are Run names and step names, not authorities.

## Public workbenches

| Workbench | Lane |
|---|---|
| `haipipe-workbench-page` | Context, Bullet, Evidence Item records; Run Space (Execution, Discovery, and Page Run tickets/results); LaTeX, Word, Slides, Render; Folder roster and meta-surface. Served by `servers/workbench-page` |
| `haipipe-workbench-studio` | Chat and Draw. Served by `servers/workbench-studio` |

Evidence VALUE, CITE, DISPLAY, and historical Page-link outcomes are typed
Evidence Items, not separate workbenches. Supporting Runs come from Execution or
Discovery; a Local Page Run turns their Results into one focal ready-to-use
Evidence Item.

## Source layout

```text
skills/
├── board/
│   ├── README.md + CHANGELOG.md
│   ├── haipipe-folder/
│   ├── haipipe-board/
│   ├── haipipe-board-routing/
│   ├── agents/
│   ├── haipipe-page/              compatibility links only
│   ├── haipipe-workbench@            compatibility symlink
│   ├── haipipe-sentence@          compatibility symlink
│   ├── page-workflows@            compatibility symlink
│   └── haipipe-workbench-page@       compatibility symlink
└── page/                           canonical Page family
    ├── haipipe-page/
    ├── haipipe-workbench/              lane · surface · writer · boundary, ref/roster.md
    ├── haipipe-workbench-page/         🧭 Outline · Run Space · Delivery · Folder
    ├── haipipe-workbench-studio/       🎨 Chat and Draw
    ├── haipipe-sentence/
    └── page-workflows/
```

The five Board-local Page entries are compatibility surfaces resolving into
canonical `skills/page/`. They are not second implementations or documentation
authorities; new links and imports should target `skills/page/` directly.

`haipipe-board/legacy/` contains only explicit compatibility readers and
one-time migration tools. It is not scanned as a current skill source. Retired
skills are deleted; Git history is their archive.

## Validation

```bash
python3 -m unittest discover -s haipipe-board/tests
python3 haipipe-board/cli/foldercontracts.py --check
```

The Folder-contract command is a cross-family integration audit and names the
owning external skill for every finding. Use repeatable `--workflow <name>`
arguments when validating one workflow's Folder owners in isolation.

Use `/workflow-table board` when a cross-skill workflow view is needed. Keep
test counts in command output and changelogs, not in this README.
