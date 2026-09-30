# Workbench, Runs, and Skills

This repository uses **Workbench** for the page-level working surface. A
package may provide a Workbench without requiring a Board. When a Board is
present, it can link to that Workbench; the Board does not own its work.

## Design principle

```text
Page / real folder
└── Workbench
    └── Space
        └── View (the subspace within that Space)
            └── Run Type (one kind of bounded work)
                ├── declared Skills (one or more, with distinct roles)
                └── Run instances (zero or more, each with a Ticket and Result)
```

A Space and View organize the interface. Each Run Type has one home View so its
Runs have a predictable place in the panel. A Run Type may also be listed in
other Views of the same Space; the first View its catalogue line names is its
home. The panel is a projection of the Run Type catalogue and the Page's real
Run Tickets; it does not allocate work.

**Skills attach to a Run Type, not exclusively to a View.** A Run Type may
declare several Skills, and one Skill may guide several Run Types or Views.
A package may have one context Skill dedicated to each View, alongside shared
workflow, domain, and procedure Skills. Those shared Skills remain part of the
Run Type's declared set. A View's context Skill alone does not describe the
whole Run Type.

The number of Skills is not fixed. A Run Type should name one **primary Skill**
for its bounded procedure and supporting Skills with their roles and conditions
for use, rather than requiring a fixed number of slots. Mandatory execution
checks belong in the owning writer. The Run Type catalogue, a concrete Run's
bound guidance, and evidence of what an agent actually loaded are different
facts.

## How a catalogue line declares its Skills

The Page and Paper catalogues (`run-cards.md`) put one `🧩 SKILL` line after
each `🔘 BUTTON` line. The first Skill is the primary one; each supporting Skill
says its role in brackets:

```text
🔘 BUTTON   Section revise · Draft · ^run-section- · views revise
🧩 SKILL    haipipe-page-writing · haipipe-writing (prose style, when the person asks for a voice)
```

A line with one Skill needs nothing more. A supporting Skill with no role is a
gap to fill, not a second primary.

## Where a Run's Ticket and Result live

A concrete Run is one execution of a Run Type for a bounded target. Most Runs
keep both halves in the Page's own folder; other owners and Run Type kinds have
their own rules:

New Run Tickets should use readable `run-...` names on disk and in the panel.
The name identifies the operation and target; its Ticket binds exact input
versions. `run-corpus` and `run-labeling` can identify owner families, while a
concrete Run adds its operation and target. Short family codes and ordinal-only
IDs are legacy compatibility, not the naming pattern for new Run Types. The
Page Workbench already writes full names; the Paper Workbench displays full
names but still reads some older short IDs. Labeling now writes full
`run-labeling-<operation>-<MMDD>-<target>` names while reading historical short
IDs for compatibility. Source-owned Corpus Preparation writes full
`run-corpus-<operation>-<MMDD>-<target>` names.

| Run Type kind | Ticket | Result | example |
|---|---|---|---|
| own Run | `runs/<name>.md` or `.sh` | `results/<name>/` | `run-section-0920-c1-p1` |
| source-owned Run | `<source>/corpus-preparation/runs/<name>.yaml` | `<source>/corpus-preparation/results/<name>/` | `run-corpus-unit-materialize-0929-assistant-replies` |
| fixed Delivery Run | `runs/run-delivery-<lane>.sh`, rerun in place | the built files in `delivery/<lane>/` | `run-delivery-latex` |
| supporting Run | stays in the folder that owns it | stays with its owner | a Task Run `b01j09t02r01` on a Paper's Roadmap |
| prompt-only Run Type | none in this folder | none in this folder | Paper › Ideation › Generate ideas |

A supporting Run appears in the panel only as a reference, read from the Page's
Evidence Markdown (its `Supporting Runs:` lines); the panel never copies the
owner's Ticket or Result. A prompt-only Run Type copies a prompt that starts
work under another owner; its Runs are counted where that owner keeps them.

## What a run card may say about Skills

When a runtime records Skill provenance, it should bind the resolved Skill
identities and versions for that Run and distinguish **declared** Skills from
Skills actually loaded or invoked. A catalogue or panel can show declared
Skills; neither proves that a historical Run used them. Code workers and human
actors remain separate from Skills. On a run card this means:

1. A Run whose Ticket or receipt records a `skills:` line shows those, as the
   Skills it used.
2. A Run with no such line shows its Run Type's Skills labelled as declared,
   never as used.
3. A Run Type with no Run yet shows its declared Skills under `No runs yet.`,
   so a reader can see which Skill would do the work.

## Preparation is its own bounded work

When raw data needs parsing, cleaning, or conversion into working units,
commission that preparation as bounded work with its own outputs. In Labeling,
the `corpus-contract` Run consumes an accepted, versioned item set and freezes
its meaning and custody; it should not silently stand for the entire
preparation history. The [Labeling corpus preparation design](../plugins/subjective-label/CORPUS-PREPARATION.md)
specifies the upstream Runs, custody boundary, and multi-turn item contract.

## The Workbenches that follow this design

| Workbench | real folder | Spaces | Run Type catalogue |
|---|---|---|---|
| Page | a Page folder (`<page>/<page>.md`) | Draft · Evidence · Delivery | `plugins/haipipe-toolkit/skills/page/haipipe-page-workflow/ref/run-cards.md` |
| Paper | a paper folder (`board.md` with `dialect: paper`) | Ideation · Story · Sections · Delivery | `plugins/haipipe-toolkit/skills/paper/haipipe-paper-workflow/ref/run-cards.md` |
| Labeling | a Page's `labeling/` folder | Data · Labeling · Quality · Delivery | [Run Type–Skill table](../plugins/subjective-label/skills/label-building/ref/ref-space-mapping.md#run-type-skills) |

### Example: Labeling

The [Labeling Workbench diagram](../plugins/subjective-label/servers/workbench-labeling/studio/labeling-workbench-design.excalidraw)
shows Preparation before Contract, both Run owner folders, and full Ticket names.

In the current Labeling catalogue, the View Skill is primary; the shared
Workflow, side law, and side workflow are supporting guidance. Those View
Skills currently instruct an agent performing a Run to load all three
supporting Skills and the family entry Skill first. This is an invocation rule
of those Skills, not a rule that every UI read or code-worker call loads them.

| current Labeling binding | answers | example for `human-calibration` |
|---|---|---|
| primary View Skill | how to perform this Run | `subjective-label-rounds` |
| shared Workflow | which Run is eligible and which Route follows | `subjective-label-workflow` |
| side law | who may decide and what is forbidden | `label-building` |
| side workflow | how this side allocates and records its Runs | `label-building-workflow` |

`subjective-label` is the family entry, outside those four catalogue entries.
For future Run Types, state each supporting Skill's purpose and when it must be
loaded; do not fill four slots merely to make the table rectangular.

The `subjective-label` package has `Quality → Test` as one View. Its
`test-reserve` Run Type uses Building rules, while `test-gold-lock` uses
Scanning rules. Both appear in the same View, so the View cannot determine the
complete Skill set. The package's
[Run Type–Skill table](../plugins/subjective-label/skills/label-building/ref/ref-space-mapping.md#run-type-skills)
declares the specific bindings and implementation status.
