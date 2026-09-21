---
name: haipipe-folder
description: >-
  The neutral Folder contract shared by Board pages, workflow artifacts, and
  executable task units. Every Folder has a Page Face for reading and judgment
  and a Task Face for intent, work, progress, and closure; a declared resource owner or canonical family skill owns both faces and selects
  optional plugins such as Outline or Runs.
  Use when defining a Folder kind, authoring a Folder owner skill, deciding
  whether something is a page or a task, binding Run Specs to Folder resources, or routing a legacy page-type.
  Trigger: folder contract, page face, task face, folder kind, Folder ownership, Run Spec, /haipipe-folder.
metadata:
  version: "0.7.1"
  last_updated: "2026-09-20"
---

# /haipipe-folder · one work object, two faces

A Folder is the addressable unit of work. It is not a Page with a Task
attached, and it is not a Task with documentation attached. It owns two
orthogonal faces:

For `folder-kind: task`, **Task Folder = Page Folder = `tNN_<task>/`**. The
two phrases select different faces of one address; they do not name nested or
sibling directories. Its parent `jNN_<job>/` is a Job container, never a Task
Folder.

```text
                         Folder kind
                 owned by one resource/family skill
                    /                    \
       Page Face  /                      \  Task Face
  read · express · judge             intend · do · track · close
```

`primary_face` says which face is the normal entry, never which face exists.
A page-primary Folder still owes executable closure. A task-primary Folder
still owes a readable account of what it is, what happened, and what remains.
Either face may be physically minimal when the owner has no work for it.

## Ownership

One declared resource or canonical family skill owns the Folder kind, both
faces, selected plugins, closure and handoff. Its workflow declares the graph
of bounded Run Specs. A Folder kind is resource identity; workflow progress is
recorded on Runs and their dependencies.

```text
door         family invariants and user verbs
workflow     Run Specs, dependencies/routes, dispatch, receipts, completion
Folder owner Page Face + Task Face + resource closure + plugins + handoff
native Run   Ticket + bounded target + worker + Result + receipt
plugin       reusable storage/presentation/writer capability
```

### Stable address and resource identity

New fixed-kind Folders declare `folder-kind:` on their Page. If a separately
governed identity record is needed, use `workflow/folder.yaml`:

```yaml
schema: haipipe.folder-identity/v1
current:
  folder-kind: knowledge
history:
  - {from: information, to: knowledge, reason: <explicit-resource-change>, at: <timestamp>}
```

This record has no execution position or progress field. A Run completing does
not automatically change the Folder kind. A resource-kind change requires an
explicit owner action with resolved inputs and an append-only identity receipt.
Keep the Page `folder-kind:` consistent. If subject, address or independent
closure changes, create another Folder and bind exact Context/Evidence inputs.
Insight's Meta/Question/DIKW Folders normally retain their separate identities;
Design retains one `folder-kind: design` with native Design Runs.

A Page Face belongs to the Folder owner. Do not create a duplicate
`haipipe-page-for-<kind>` when the owner already supplies that face. Page work
uses `haipipe-page-workflow`; executable work uses declared native Run owners.
`workflow/` holds control records and does not imply a product or allocated Run.

## Runtime shape

A Folder may materialize only the lanes its owner selects:

```text
<folder>/
├── <stem>.md             Page Face · what a reader opens
├── outline/              human plan and decision record, when selected
├── workflow/             machine intent/progress/receipts, when selected
├── evidence/             evidence lanes selected by the owner
├── delivery/             outward projections selected by the owner
├── studio/               human authoring room selected by the owner
├── scripts/config/       optional reusable implementation material
├── runs/                 authored Run tickets; the only execution door
└── results/              Folder-local paired Results, when this dialect owns them
```

Absence is meaningful. An owner that selects no addressable Runs does not
scaffold empty runtime lanes. When the first Run opens, its authored ticket and
generated Result acquire one logical address. Resolve the Ticket format and
Result location from the owning Run Profile. These are shell-dialect examples:

```text
Folder-local     <folder>/runs/<run>.sh ↔ <folder>/results/<run>/
Job-backed Task  <job>/<task>/runs/<run>.sh ↔ $OUTPUT_ROOT/<task>/results/<run>/
```

Page Writing uses Markdown Tickets (`runs/rp-*.md`) under the
[interactive writing profile](../../page/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md).
Design uses YAML Tickets (`runs/rdNN_<operation>_<slug>.yaml`) under
[haipipe-design-workflow](../../design/haipipe-design-workflow/SKILL.md).
Neither requires a shell wrapper merely to count as a Run.

The Task owner resolves `$OUTPUT_ROOT` from its declared store or the Job.
Existing records in older `results/<task>/` stores retain their resolver;
do not copy or relocate them to imitate another dialect. `scripts/`, config, and
notebooks are conditional supporting projections. `haipipe-plugin-runs` is the
optional presenter over the logical Run spine. It does not replace the
universal Task Face or own Execute, lifecycle, or closure authority.
`haipipe-run` owns the shared Level-4 identity, pairing, receipt, lifecycle, and
audit invariants beneath these physical dialects.

## 🪞 Table projection · not a third Folder face

A Table is a read projection over one or both Folder faces. It can show a plan
and the current display/runtime state in the same row, but it does not become a
third authority beside the Page Face and Task Face:

| Table | Row grain | Plan source | Display source | Current status |
|---|---|---|---|---|
| **Workflow Table** | bounded Run Spec | frozen workflow declaration | actual native Runs and their control state | exists |
| **Task Tables** | Task folder | task-page `develops:` / `input:` / `output:` | tree, code, tickets, receipts, stores | exists as `/task-table` |
| **Board Tables** | one Board Page/Page Folder | Page/Outline + cross-lane intent | Folder lanes, Tasks, Runs, Results, evidence | not implemented; future sibling |

The current Folder already exposes parts of the future Board view, but as
separate surfaces:

- `haipipe-plugin-folder` / `folderstat.py` is the live **display inventory**:
  one row per material lane, with counts, age, and narrow staleness.
- Page `Outline` is the **plan/evidence projection** for the current Page
  workflow.
- `haipipe-plugin-runs` is the **runtime projection** over Tickets, Results,
  and receipts.

These are not yet a unified `Board Table`. Do not add a `board-table/` Folder
lane, copy plan fields into `folderstat`, or call the Folder inventory a Board
Table until that sibling contract defines its row grain, source authority, and
write boundary.

## Folder owner skill contract

Every new workflow-associated Folder owner skill declares these metadata rows:

```yaml
metadata:
  workflow: haipipe-<family>-workflow
  folder_kind: knowledge
  primary_face: page       # page | task
  page_ruling: none        # none | domain-gate | local
  legacy_page_type: knowledge   # optional compatibility key
```

It then carries these sections in this order:

```text
## Position
## Folder Kind
## Input
## Page Face
## Task Face
## Plugins
## Gate and Closure
## Handoff
## Files
```

The Page Face specifies reader promise, outline/grammar, judgment boundary,
and reopening conditions. The Task Face specifies the work, writer, progress
record, execution boundary, and terminal states. Closure is one cross-face
assertion: neither face may report closed while the other still owes a
load-bearing artifact or decision.

The owning workflow publishes a Run Spec list and its dependency/Route graph
under `haipipe-run`. The
Folder contract binds the work it actually commissions:

- Declare a Run Profile in `## Task Face`, or link the exact shared profile,
  naming target, Ticket, inputs, worker, Result, acceptance, promotion and
  reopening behavior for each selected operation.
- Match the workflow's Spec targets, native identities and cardinalities.
- With no commissioned Run, omit empty `runs/`, `results/` and presenter lanes.
- Keep resource closure in `## Gate and Closure`. A register edit, Page CHECK,
  human tick or control receipt does not itself allocate a Run.

The Run Spec graph is the execution definition, the Folder profile binds its
resources, and native receipts establish actual inventory. Record resource
controls without synthetic Run ids.

`page_ruling` tells the shared Page Workflow whether CHECK owes an owner-level
person decision. `domain-gate` reuses the owner's named human gate receipt;
`local` names a distinct Page-Face ruling in the Folder contract; `none` means
closure is mechanical apart from any selected plugin ticks.

Run the structural gate after adding or revising a Folder owner:

```bash
python3 ../haipipe-board/cli/foldercontracts.py --check
```

## Canonical family-owner contract

A family whose durable work unit is one stable Folder may declare ownership
directly, without a separate workflow-associated Folder skill:

```yaml
metadata:
  folder_owner: canonical
  folder_kind: task
  primary_face: task       # page | task
  page_ruling: local       # none | domain-gate | local
  legacy_page_type: task   # optional compatibility key
```

The skill owns both faces, selected plugins, cross-face closure and handoff.
Its Page Face uses `haipipe-page-workflow`; execution uses the family's Run
Specs and native workers. No extra lifecycle object or identity record is
required. Both owner forms resolve by `folder_kind`; `legacy_page_type` is
only a read alias for old Pages.

## Plugin selection

A Folder owner selects plugins; plugins never decide the owner. Record each selected
plugin as required, optional, or forbidden and state why. Cross-Folder input
does not require a separate binding plugin: bounded informational context is
named by source address in the off-stage Context record; evidence is bound through an
Evidence Item's full Supporting Run id or frozen Local Input address. There is
no separate Task plugin. `PageX` is read-only migration history and must not be
selected, scaffolded, or written for a new Folder.

## Compatibility

Resolution uses one resource owner:

```text
workflow/folder.yaml current.folder-kind   canonical identity record, if present
workflow/phase.yaml current.folder-kind    read-only import only if canonical absent
Page folder-kind                          fixed resource identity
Page page-type                            legacy owner lookup
filename/base                             families without a declared kind
```

Malformed selected identity or a conflicting Page `folder-kind:` is a routing
error; never guess from another source. A valid canonical record supersedes
legacy bytes. Only the old file's Folder kind is imported; its phase field and
transition history create no execution authority. New writers emit no Phase
field. On an authorized identity edit, write the canonical record and retain
old bytes as history. Remove the read adapter only after supported legacy
records are inventoried/migrated; see the Insight workflow migration reference.

Compatibility keys do not own semantics. `legacy_page_type` points at the
current resource owner. New domain Pages write `folder-kind:`.

## Closing checks

- One declared resource/family skill owns each Folder kind and both faces.
- Resource identity is separate from Run progress and dependency state.
- Both faces name the same subject, version and closure boundary.
- Each selected plugin has a purpose; empty capability folders do not exist.
- Cross-Folder inputs use exact Context source addresses or Evidence Item
  Supporting/Local Run bindings.
- Runs launch through native Tickets, pair one declared Result and receipt,
  and write only their declared output.
- Folder Run Profiles match workflow Specs; actual counts come from receipts.
- Resource gates and handoffs are testable from named files.
- Table projections name their authoritative sources and remain read-only.

## Files

- `../haipipe-board/src/folder_contract.py` discovers and validates Folder owner contracts.
- `../haipipe-board/cli/foldercontracts.py` is the executable inventory/gate.
- `../../page/haipipe-page/SKILL.md` owns the shared Page frame and Page workflow entry.
- `../../page/haipipe-plugin/SKILL.md` owns reusable plugin mechanics.
- `../../run/haipipe-run/SKILL.md` owns the neutral Level-4 Run contract.
