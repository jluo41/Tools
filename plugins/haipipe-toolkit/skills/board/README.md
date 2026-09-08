# Board skill set

The Board family turns one bounded work object into a readable, operable set
of Folder-backed Pages. It separates container, Page lifecycle, plugins, and
sentence work so each rule has one owner.

## Ownership map

| Layer | Skill | Owns |
|---|---|---|
| Folder | `haipipe-folder` | neutral Page Face + Task Face contract |
| Board | `haipipe-board` | container, Groups, roster, build, serve, aggregate close |
| Page | `haipipe-page` | readable frame, Folder-kind resolution, lifecycle entry |
| Page workflow | `haipipe-page-workflow` | CONTEXT → OUTLINE → EVIDENCE → CONTENT → CHECK router |
| Plugin | `haipipe-plugin` | plugin definition and roster law |
| Sentence | `haipipe-sentence` | comment, edit, card, sentence-local record |
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
board/
├── README.md
├── CHANGELOG.md
├── haipipe-folder/
├── haipipe-board/
├── haipipe-page/
├── haipipe-plugin/
├── haipipe-sentence/
├── haipipe-board-routing/
├── page-workflows/
│   ├── haipipe-page-workflow/
│   ├── haipipe-page-context/
│   ├── haipipe-page-outline/
│   ├── haipipe-page-evidence/
│   ├── haipipe-page-content/
│   ├── haipipe-page-check/
│   └── agents/
├── page-plugins/
│   ├── haipipe-plugin-outline/
│   ├── haipipe-plugin-studio/
│   ├── haipipe-plugin-runs/
│   ├── haipipe-plugin-delivery/
│   └── haipipe-plugin-folder/
└── agents/
```

`haipipe-board/legacy/` contains only explicit compatibility readers and
one-time migration tools. It is not scanned as a current skill source. Retired
skills are deleted; Git history is their archive.

## Validation

```bash
python3 haipipe-board/cli/foldercontracts.py --check
python3 -m unittest discover -s haipipe-board/tests
```

Use `/workflow-table board` when a cross-skill workflow view is needed. Keep
test counts in command output and changelogs, not in this README.
