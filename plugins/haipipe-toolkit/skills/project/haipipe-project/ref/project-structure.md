# Project Container Contract · haipipe-project/v1

This reference owns the root of `examples/<project>/` only. Load a child
world's Skill for everything below that root.

## Identity

A Project is one durable question, product, or research program that benefits
from one boundary for execution, evidence, interpretation, and delivery.

Use a stable readable id such as:

```text
Proj32-CGM-Event-Pred
```

The id is an address, not metadata. Do not infer repository topology, execution
model, or project profile from spelling.

Every active Project carries:

```text
README.md       human entry: mission, boundary, current shape, entry points
project.yaml    machine entry: identity, profile, Git mode, state, migration debt
```

## Manifest schema

Required fields:

```yaml
schema: haipipe-project/v1
id: Proj32-CGM-Event-Pred
profile: research                 # research | software | hybrid
git_mode: workspace              # workspace | submodule
state: active                    # active | paused | archived
mission: "Predict glucose from CGM plus event context."
```

Optional root-migration disclosure:

```yaml
migration:
  status: needed                 # needed | planned
  legacy_paths:
    - paper
    - applications
    - results
  note: "Paths are preserved until owner-specific migration is approved."
```

`migration` records debt; it does not waive the canonical contract or claim a
move has happened. Omit it when the Project root is clean.

## Canonical root

```text
examples/<project>/
├── README.md             REQUIRED
├── project.yaml          REQUIRED
│
├── tasks/                LAZY · internal computational executor
├── discoveries/          LAZY · external-evidence executor
├── diagram/              LAZY · Project story and Board/view surfaces
├── papers/               LAZY · academic consumers
├── insights/             LAZY · Insight Prototypes (Blocks) and Instances
├── designs/              LAZY · Design boards and Design Folders
└── external/             LAZY · read-only upstream repositories/assets
```

LAZY means “create on first use,” not “missing capability.” Empty directories
are not a useful contract because Git cannot preserve them without placeholders.

New work always uses plural `papers/`. Existing `paper/` paths, especially
submodules, are legacy debt and are not renamed without an explicit migration.

## Worlds and flow

```text
external/ ──▶ discoveries/ ──┐
                             ├──▶ insights/ (Prototype ──▶ Instance) ──▶ papers/
tasks/ ──────────────────────┘                                      └──▶ designs/
```

| Root | Role | Owner and boundary |
|---|---|---|
| `tasks/` | computational evidence bank | `haipipe-task`; Block → Job → Task → Run |
| `discoveries/` | external-evidence bank | `haipipe-discovery`; its current BJTR contract |
| `diagram/` | navigation and interpretation surfaces | Project story plus project-level Boards and meetings |
| `papers/` | academic consumer | `haipipe-paper`; may contain nested submodules |
| `insights/` | a Prototype (Block: questions, scripts, studio) and one Instance per dataset (runs, results, pages) | `haipipe-insight`; see `insights/` below |
| `designs/` | Design boards, reading signed Insight handoffs | `haipipe-design` |
| `external/` | upstream dependency | pinned/read-only here; analysis belongs in Discovery or Task |

Insight is a world of its own (JL 261001); a Task-side Insight Page stays on
its Task Board. Reusable findings flow to Paper and Design through their
contracts. Raw Task Results never move to the Project root; an Instance's light
results live in its question folders, heavy output in `ProjectResult`.

## Profiles

Profiles answer what kind of root this is. They do not alter child-world
contracts.

| Profile | Root-owned code allowed | Intended use |
|---|---|---|
| `research` | no | execution code belongs to Job/Task; shared SPACE libraries remain external to the Project |
| `software` | yes | the Project itself is a package/product repository; conventional `src/`, `tests/`, and build files are valid |
| `hybrid` | yes | a software artifact plus research Tasks/Discoveries/Papers; Tasks call the package instead of duplicating it |

For `software` and `hybrid`, conventional root directories such as `src/`,
`tests/`, `scripts/`, `configs/`, and `docs/` are profile-owned. Generated
`results/` remains forbidden at the Project root in every profile.

## Git modes

| Git mode | Meaning |
|---|---|
| `workspace` | files are tracked by the containing SPACE repository |
| `submodule` | the Project has its own repository and is linked under `examples/` |

Repository topology is observable and declared. Never route on `Proj...` versus
`Project-...`. Papers may be nested submodules regardless of Project spelling.

## `external/`

`external/` is optional and has one narrow meaning: upstream material whose
identity and history are owned elsewhere. Prefer a pinned submodule or another
resolvable origin. Do not develop project-owned code there. If the Project
modifies an upstream codebase as its product, that code belongs to the
software/hybrid profile instead.

Heavy data remains outside the repository in configured stores. `external/`
may contain metadata or a code/reference checkout, not an uncontrolled data
dump.

## `diagram/`

`diagram/` is no longer restricted to two static ASCII files. It may contain:

```text
diagram/
├── project/       mission, boundary, architecture, durable decisions
├── boards/        project-level Task/Insights and other Board surfaces
└── meetings/      optional meeting records tied to this Project
```

Existing flat Board folders remain readable. New work may adopt these zones
incrementally; no routine update moves an active Board.

Block-local `board.md` remains under its owning `tasks/bNN_.../` Block and does
not move to the Project diagram tree.

## `insights/`

An Insight topic is two boards (JL 261003). The Prototype is Block level: the
topic's design, its partitions and one folder per question with that question's
own script, plus the Block's `studio/`. It holds no data. An Instance reads one
dataset through one Prototype; a new dataset is a new Instance, a new subject
with a different input a new Prototype.

```text
insights/
├── Prototype-Insight-<Topic>/      the Block: the design, no data
│   ├── board.md                    board-kind: insight-prototype
│   ├── 0-Meta/                     meta.md · partitions.md · thresholds.yaml
│   ├── 1-Data/ … 4-Wisdom/         one folder per question: its file and scripts/
│   └── studio/                     the Block's studio: question-map.excalidraw
│                                   (generated) and hand sketches
├── Instance-Insight-<Dataset>/     one extract read through one Prototype:
│                                   script copies, runs, results, the pages
└── <Dataset>-InsightBoard/         older register-kind board, until carried over
```

- **The Prototype is the Block.** Inside it there is no B-J-T-R: the rung is the
  Job, the question folder the Task, an Instance's partition run the Run.
- **The studio lives at Block level.** `studio/` sits beside the Prototype's
  `board.md`; `question-map.excalidraw` is generated from the question files
  and never edited, and each hand sketch is its own file. An Instance has no
  studio of its own; the workbench shows its Prototype's.
- **Older boards.** A register-kind `<Dataset>-InsightBoard/` keeps its layout
  until it is carried over into a Prototype; it is not migration debt.

The internals belong to `haipipe-insight` (`ref/prototype-contract.md`); a
Project audit checks only that `insights/` holds these folder kinds.

## Root prohibitions and debt

Never create these as new root structures:

- `results/`: generated output belongs to a Job or consumer-owned store.
- `applications/`: legacy since 261001; Insight boards go to `insights/`, Design
  boards to `designs/` (old ones under each world's `_old/`).
- `probes/`: use the current Page evidence contract.
- `_old/`, `cc-archive/`: archive inside the owning world, or preserve only as
  declared migration debt.
- `tasks.old/`: temporary migration name only; durable history belongs under
  `tasks/_legacy/` after explicit migration.

For a research profile, root `src/`, `scripts/`, `configs/`, `tests/`, and
`docs/` are also debt until reclassified or moved. For software/hybrid they are
valid profile-owned structure.

## Structure ownership

| Scope | Authority |
|---|---|
| Project root, manifest, profile, Git mode, `external/` boundary | `haipipe-project` |
| `tasks/` internals | `haipipe-task` + `haipipe-run` |
| `discoveries/` internals | `haipipe-discovery` |
| Board/Page internals | `haipipe-board`, `haipipe-page`, owning workflow |
| `papers/` internals | `haipipe-paper` |
| `insights/` internals | `haipipe-insight` |
| `designs/` internals | `haipipe-design` |

An audit at this layer checks only Project-root truth. It must not claim that a
child world is internally compliant without invoking that world's checker.
