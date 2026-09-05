---
name: haipipe-folder
description: >-
  The neutral Folder contract shared by Board pages, workflow artifacts, and
  executable task units. Every Folder has a Page Face for reading and judgment
  and a Task Face for intent, work, progress, and closure; a domain workflow
  phase or a declared canonical family skill owns both faces and selects
  optional plugins such as Outline or Runs.
  Use when defining a Folder kind, authoring a workflow-phase skill, deciding
  whether something is a page or a task, filling a Phase × Run Map, or routing a legacy page-type.
  Trigger: folder contract, page face, task face, folder kind, phase-owned
  configuration, workflow phase, /haipipe-folder.
metadata:
  version: "0.5.1"
  last_updated: "2026-09-05"
---

# /haipipe-folder · one work object, two faces

A Folder is the addressable unit of work. It is not a Page with a Task
attached, and it is not a Task with documentation attached. It owns two
orthogonal faces:

```text
                         Folder kind
                 owned by one phase or family
                    /                    \
       Page Face  /                      \  Task Face
  read · express · judge             intend · do · track · close
```

`primary_face` says which face is the normal entry, never which face exists.
A page-primary Folder still owes executable closure. A task-primary Folder
still owes a readable account of what it is, what happened, and what remains.
Either face may be physically minimal when the phase has no work for it.

## Ownership

One domain workflow phase normally owns the Folder kind. A stable base Folder
whose kind is itself the family work unit may instead be owned by one declared
canonical family skill. Ownership always includes both faces, the plugin
profile, the gate, and the handoff. The four altitudes are:

```text
door       invariants and user verbs across the family
workflow   order, frontier, dispatch, receipts, and stop rules
phase      one Folder kind: Page Face + Task Face + plugins + closure
plugin     reusable storage/surface/writer/boundary capability
```

### Stable address, phase-owned identity

A workflow may grow one physical Folder through several sequential phase
identities. That is an **in-place transition**, not several Folders pretending
to be one. The address stays stable; exactly one `folder-kind` is current; and
`workflow/phase.yaml` records the current phase plus an append-only transition
history. The gate that closes phase A changes the identity to phase B only when
B's input packet exists. A return edge records another transition instead of
rewinding or erasing history.

```yaml
current:
  phase: D2
  folder-kind: design-unit
history:
  - {from: D1, to: D2, gate: GD1, at: 2026-08-31}
```

`workflow/` is control material, not product material. A purity law such as
“a proposed Card has no realization beside it” may permit `workflow/phase.yaml`
without treating the Folder as realized. The phase contract must say so, and
its checker must distinguish control metadata from produced artifacts.

Use in-place evolution only when every phase concerns the same work object. If
the subject, independent closure, or address changes, mint another Folder and
bind it through the owning workflow plus explicit Context/Evidence addresses.
A cross-Folder phase such as a round audit still owes a
small addressable receipt Folder; it must not masquerade as an unrecorded verb.

Do not create a separate `haipipe-page-for-<kind>` when `<kind>` is already a
workflow phase. Put the Page Face in that phase skill. Do not create a private
lifecycle in the phase: Page work uses `haipipe-page-workflow`; executable
work uses the owning domain/task workflow.

The same anti-duplication rule applies to a canonical family owner. When a
stable Folder kind is already the family's work unit and has no meaningful
domain-phase identity, the family skill owns both faces directly. Do not mint a
fake workflow or phase, and do not add a parallel Page-Type skill merely to
carry its Page Face.

## Runtime shape

A Folder may materialize only the lanes its owner selects:

```text
<folder>/
├── <stem>.md             Page Face · what a reader opens
├── outline/              human plan and decision record, when selected
├── workflow/             machine intent/progress/receipts, when selected
├── evidence/             evidence lanes selected by the phase
├── delivery/             outward projections selected by the phase
├── studio/               human authoring room selected by the phase
├── scripts/config/       optional reusable implementation material
├── runs/                 authored Run tickets; the only execution door
└── results/              Folder-local paired Results, when this dialect owns them
```

Absence is meaningful. An owner that selects no addressable Runs does not
scaffold empty runtime lanes. When the first Run opens, its authored ticket and
generated Result acquire one logical address. Resolve the Result by dialect:

```text
Folder-local     <folder>/runs/<run>.sh ↔ <folder>/results/<run>/
Job-backed Task  <job>/<task>/runs/<run>.sh ↔ <job>/results/<task>/<run>/
```

The second form keeps generated output at the Job without weakening the Task
Folder's identity; do not copy it under the Page. `scripts/`, config, and
notebooks are conditional supporting projections. `haipipe-plugin-runs` is the
optional presenter over the logical Run spine. It does not replace the
universal Task Face or own Execute, lifecycle, or closure authority.
`haipipe-run` owns the shared Level-4 identity, pairing, receipt, lifecycle, and
audit invariants beneath both physical dialects.

## 🪞 Table projection · not a third Folder face

A Table is a read projection over one or both Folder faces. It can show a plan
and the current display/runtime state in the same row, but it does not become a
third authority beside the Page Face and Task Face:

| Table | Row grain | Plan source | Display source | Current status |
|---|---|---|---|---|
| **Workflow Table** | Phase/Cycle | workflow declaration | compact Runs and human state | exists |
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

## Phase skill contract

Every new phase-owned Folder skill declares these metadata rows:

```yaml
metadata:
  workflow: haipipe-<family>-workflow
  phase: I4
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

The owning workflow publishes the complete Phase × Run Map defined by
`haipipe-run`. This phase must make its row executable:

- when the row lists Run operations, add `### Run Profile` inside `## Task
  Face` with ALLOWED, TARGET, TICKET, INPUTS, WORKER, RESULT, ACCEPT,
  PROMOTION, and REOPEN;
- make the profile's operations and cardinality agree exactly with the
  workflow row;
- when the row says `none`, omit empty `runs/`, `results/`, and Runs-presenter
  lanes rather than manufacturing work;
- keep the phase gate in `## Gate and Closure`; a human tick or phase receipt
  does not become a Run merely because the Task Face records it.

The workflow map is the index, this phase profile is the executable detail,
and runtime receipts are actual inventory. A disagreement is a structural
error, never a license to infer missing Runs.

`page_ruling` tells the shared Page Workflow whether CHECK owes an owner-level
person decision. `domain-gate` reuses the phase's named human gate receipt;
`local` names a distinct Page-Face ruling in the phase contract; `none` means
closure is mechanical apart from any selected plugin ticks.

Run the structural gate after adding or revising a phase:

```bash
python3 ../haipipe-board/cli/foldercontracts.py --check
```

## Canonical family-owner contract

A canonical family owner is the narrow exception for a stable base Folder kind
that is itself the family's durable work unit rather than one phase of a domain
workflow. It declares:

```yaml
metadata:
  folder_owner: canonical
  folder_kind: task
  primary_face: task       # page | task
  page_ruling: local       # none | domain-gate | local
  legacy_page_type: task   # optional compatibility key
```

It does not declare `workflow:` or `phase:` and does not manufacture
`workflow/phase.yaml`. The canonical family skill must own both faces, the
family lifecycle, selected plugins, cross-face closure, and any handoff. Its
Page Face still runs through `haipipe-page-workflow`; its executable work runs
through the family lifecycle. Page routing resolves the canonical owner by
`folder_kind`, while `legacy_page_type` may point old `page-type:` values to
the same owner.

Use this form only when no domain workflow phase can truthfully name the Folder
identity. A phase-varying Folder remains phase-owned.

## Plugin selection

A Folder owner selects plugins; plugins never decide the owner. Record each selected
plugin as required, optional, or forbidden and state why. Cross-Folder input
does not require a separate binding plugin: bounded informational context is
named by source address in the Context Workspace; evidence is bound through an
Evidence Item's full Supporting Run id or frozen Local Input address. There is
no separate Task plugin. `PageX` is read-only migration history and must not be
selected, scaffolded, or written for a new Folder.

## Compatibility

During migration, a runtime Folder may still carry `page-type:`. Resolution is:

```text
workflow/phase.yaml current.folder-kind: authoritative in-place identity
folder-kind:       fixed phase- or canonical-family-owned identity in Page frontmatter
page-type:         legacy lookup through owner metadata
filename/base      families that have not migrated yet
```

When `workflow/phase.yaml` exists, a missing/invalid `current` block or a
conflicting Markdown `folder-kind:` is a named routing error. Falling back
would let a stale Page Face silently select the wrong phase after D1→D2→D3.

Compatibility keys do not own semantics. `legacy_page_type` points the old key
at the phase or canonical family skill that now owns its Page Face. Never write a new
Application `page-type:` merely because the checker still accepts the key.

## Closing checks

- One workflow phase owns the Folder kind and both faces; or, for one stable
  family work unit with no phase identity, one declared canonical family skill
  owns the Folder kind and both faces.
- An in-place phase transition preserves one address, one current kind, and an
  append-only phase history.
- The two faces name the same subject, version, and closure boundary.
- Every selected plugin has a purpose; empty capability folders do not exist.
- Cross-Folder inputs use Context source addresses or Evidence Item
  Supporting/Local Run bindings, never PageX or a private task-link lane.
- Runs, when present, launch only through `runs/`, resolve one paired Result by
  Folder dialect, and write only declared output.
- The workflow's Phase × Run row and this phase's Run Profile agree on
  operations and symbolic cardinality; planned counts remain distinct from
  receipt-backed actual inventory.
- The phase's gate and handoff are testable from named files.
- Any table projection names its plan and display sources and remains
  regenerable/read-only; it does not become a third Folder face or closure
  authority.

## Files

- `../haipipe-board/src/folder_contract.py` discovers and validates phase contracts.
- `../haipipe-board/cli/foldercontracts.py` is the executable inventory/gate.
- `../haipipe-page/SKILL.md` owns the shared Page frame and Page workflow entry.
- `../haipipe-plugin/SKILL.md` owns reusable plugin mechanics.
- `../../run/haipipe-run/SKILL.md` owns the neutral Level-4 Run contract.
