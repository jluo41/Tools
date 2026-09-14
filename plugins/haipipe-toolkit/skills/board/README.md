# Board skill set

The Board family turns one bounded work object into a readable, operable set
of Folder-backed Pages. It separates container, Page lifecycle, plugins, and
sentence work so each rule has one owner.

## Ownership map

| Layer | Skill | Owns |
|---|---|---|
| Folder | `haipipe-folder` | neutral Page Face + Task Face contract |
| Board | `haipipe-board` | container, Groups, roster, build, serve, aggregate close |
| Page | `skills/page/haipipe-page` | readable frame, Folder-kind resolution, lifecycle entry |
| Page workflow | `skills/page/page-workflows/haipipe-page-workflow` | CONTEXT → OUTLINE → EVIDENCE → CONTENT → CHECK router |
| Plugin | `skills/page/haipipe-plugin` | plugin definition and roster law |
| Sentence | `skills/page/haipipe-sentence` | comment, edit, card, sentence-local record |
| Write routing | `haipipe-board-routing` | propose Board shape or route one anchored Page write |

Domain Page Types live with the workflow that owns them. Task Pages are owned
by `haipipe-task`; Paper Pages by the Paper family; Application Pages by the
Application family. This folder does not maintain a duplicate Page Type set.

## Page workflow

| Phase | Skill | Primary work | Primary workspace |
|---:|---|---|---|
| 00 CONTEXT | `haipipe-page-context` | collect, resolve, freeze allowed context | Context Workspace |
| 01 OUTLINE | `haipipe-page-outline` | SHAPE bullets; SURVEY Evidence Items and Runs | Bullet + Evidence Workspaces |
| 02 EVIDENCE | `haipipe-page-evidence` | LAND Supporting/Local Results; EMBED evidence | Evidence, then Bullet Workspace |
| 03 CONTENT | `haipipe-page-content` | WRITE from the approved plan and ready evidence | Page Content |
| 04 CHECK | `haipipe-page-check` | check one whole Page version | workflow receipt |

CONTEXT, OUTLINE, and EVIDENCE all use `haipipe-plugin-outline` records.
CONTENT realizes them on the Page. CHECK evaluates the complete Page rather
than creating a second content surface.

## Run vocabulary

| Name | Identity | Owner |
|---|---|---|
| Page Run | `rp00_mermaid-structure`, then `rpNN_pNN[-pNN]` from `rp01` | Page-owned human-feedback Version/Step history |
| Task Run | native `rNN` or global run id | output-producing Task/Discovery family |
| Page workflow pass | phase-controller packet + receipt | `haipipe-page-workflow`; invoked by the `RUN` verb |

A Page workflow pass is not a Page Run. Board may host and present all three,
but it never renames their identities or becomes their source authority.
Historical `prNN_*` Page Runs remain readable migration records; new Page Runs
use `rpNN` so `PR` remains unambiguous shorthand for Pull Request.

## Public plugins

| Plugin | Lane |
|---|---|
| `haipipe-plugin-outline` | Context, Bullet, Evidence Item records |
| `haipipe-plugin-studio` | Chat and Draw |
| `haipipe-plugin-runs` | Execution, Discovery, and Page Run tickets/results |
| `haipipe-plugin-delivery` | LaTeX, Word, Slides, Render |
| `haipipe-plugin-folder` | Folder roster and meta-surface |

Evidence VALUE, CITE, DISPLAY, and historical Page-link outcomes are typed
Evidence Items, not separate plugins. Supporting Runs come from Execution or
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
│   ├── haipipe-plugin@            compatibility symlink
│   ├── haipipe-sentence@          compatibility symlink
│   ├── page-workflows@            compatibility symlink
│   └── page-plugins@              compatibility symlink
└── page/                           canonical Page family
    ├── haipipe-page/
    ├── haipipe-plugin/
    ├── haipipe-sentence/
    ├── page-workflows/
    └── page-plugins/
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
arguments when validating one owner's phase family in isolation.

Use `/workflow-table board` when a cross-skill workflow view is needed. Keep
test counts in command output and changelogs, not in this README.
