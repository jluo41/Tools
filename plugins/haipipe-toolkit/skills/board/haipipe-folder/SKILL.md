---
name: haipipe-folder
description: >-
  The neutral Folder contract shared by Board pages, workflow artifacts, and
  executable task units. Every Folder has a Page Face for reading and judgment
  and a Task Face for intent, work, progress, and closure; a domain workflow
  phase owns both faces and selects optional plugins such as PageX or Runs.
  Use when defining a Folder kind, authoring a workflow-phase skill, deciding
  whether something is a page or a task, or routing a legacy page-type.
  Trigger: folder contract, page face, task face, folder kind, phase-owned
  configuration, workflow phase, /haipipe-folder.
metadata:
  version: "0.3.0"
  last_updated: "2026-09-01"
---

# /haipipe-folder · one work object, two faces

A Folder is the addressable unit of work. It is not a Page with a Task
attached, and it is not a Task with documentation attached. It owns two
orthogonal faces:

```text
                         Folder kind
                   owned by one workflow phase
                    /                    \
       Page Face  /                      \  Task Face
  read · express · judge             intend · do · track · close
```

`primary_face` says which face is the normal entry, never which face exists.
A page-primary Folder still owes executable closure. A task-primary Folder
still owes a readable account of what it is, what happened, and what remains.
Either face may be physically minimal when the phase has no work for it.

## Ownership

The domain workflow phase owns the Folder kind. Ownership includes both faces,
its plugin profile, its gate, and its handoff. The four altitudes are:

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
bind it through PageX. A cross-Folder phase such as a round audit still owes a
small addressable receipt Folder; it must not masquerade as an unrecorded verb.

Do not create a separate `haipipe-page-for-<kind>` when `<kind>` is already a
workflow phase. Put the Page Face in that phase skill. Do not create a private
lifecycle in the phase: Page work uses `haipipe-page-workflow`; executable
work uses the owning domain/task workflow.

## Runtime shape

A Folder may materialize only the lanes its phase selects:

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

Absence is meaningful. A phase that selects no addressable Runs does not
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

`page_ruling` tells the shared Page Workflow whether CHECK owes an owner-level
person decision. `domain-gate` reuses the phase's named human gate receipt;
`local` names a distinct Page-Face ruling in the phase contract; `none` means
closure is mechanical apart from any selected plugin ticks.

Run the structural gate after adding or revising a phase:

```bash
python3 ../haipipe-board/cli/foldercontracts.py --check
```

## Plugin selection

A phase selects plugins; plugins never decide the phase. Record each selected
plugin as required, optional, or forbidden and state why. `PageX` is the one
cross-Folder binding surface, including links to executable Task Folders.
There is no separate Task plugin. A PageX Folder card reads live
plan/report/QA status when its target exposes those files.

## Compatibility

During migration, a runtime Folder may still carry `page-type:`. Resolution is:

```text
workflow/phase.yaml current.folder-kind: authoritative in-place identity
folder-kind:       fixed phase-owned identity in Page frontmatter
page-type:         legacy lookup through phase metadata
filename/base      families that have not migrated yet
```

When `workflow/phase.yaml` exists, a missing/invalid `current` block or a
conflicting Markdown `folder-kind:` is a named routing error. Falling back
would let a stale Page Face silently select the wrong phase after D1→D2→D3.

Compatibility keys do not own semantics. `legacy_page_type` points the old key
at the phase skill that now owns its Page Face. Never write a new
Application `page-type:` merely because the checker still accepts the key.

## Closing checks

- One workflow phase owns the Folder kind and both faces.
- An in-place phase transition preserves one address, one current kind, and an
  append-only phase history.
- The two faces name the same subject, version, and closure boundary.
- Every selected plugin has a purpose; empty capability folders do not exist.
- Cross-Folder inputs bind through PageX, never a private task-link lane.
- Runs, when present, launch only through `runs/`, resolve one paired Result by
  Folder dialect, and write only declared output.
- The phase's gate and handoff are testable from named files.

## Files

- `../haipipe-board/src/folder_contract.py` discovers and validates phase contracts.
- `../haipipe-board/cli/foldercontracts.py` is the executable inventory/gate.
- `../haipipe-page/SKILL.md` owns the shared Page frame and Page workflow entry.
- `../haipipe-plugin/SKILL.md` owns reusable plugin mechanics.
