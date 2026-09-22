---
name: haipipe-page-insight
description: >-
  Create or update a task-side Insight Page Folder for one research topic and
  data context. Each riNN Insight Run points to one reusable normal rNN Run,
  freezes a new dataset binding, and produces an independent versioned DIKW
  Result. Use for dataset or patient insight instances, RI binding, resumable
  checkpoints, shared Task analysis calls, and exact RI/result citations. Application
  InsightBoard rung pages remain owned by haipipe-insight-workflow.
metadata:
  version: "1.2.1"
  last_updated: "2026-09-21"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Origin → Instance and Scope → Insight Items → Synthesis → Reusable Findings"
  parent: haipipe-page
---

# /haipipe-page-insight · one topic instance, independently runnable items

An Insight Folder is one addressable research topic in an explicit data
context. Its same-stem Markdown file is the Page Face. Its **Insight Items**
are the questions and insight work performed inside that Page: one item owns
one `riNN` Insight Run binding and a history of immutable execution Results.
The RI ticket points to one normal `rNN` Run ticket/recipe and freezes the new
dataset binding; it never rewrites or impersonates that base R. An item is not
another Page Folder. The Page organizes the findings from its items.

Load `haipipe-page` and `haipipe-page-workflow` for the shared Page frame and
authoring controls. Read `ref/instance-items.md` for identity, schemas, runtime
structure, and citations; `ref/workflow-table.md` when planning or resuming;
`ref/task-calls.md` when invoking reusable analysis. Migration from the previous
single-question Page is described in `ref/migration.md`.

## Scope and ownership

The preferred public entry is `/haipipe-insight task "<topic>" [<board>]`.
It delegates here through the Task Insight route. `/haipipe-task insight
"<topic>" [<board>]` remains a compatibility alias with identical behavior.
Keep the public skill name and the family-owned path
`skills/insight/haipipe-page-insight`; no second Insight skill or parallel Page
frame is required. This remains the task-only Page Type during the shared
Folder-kind migration:

```yaml
page-type: insight
scope: task
insight-layout: items-v2
insight-instance: sms/patient-a-study
```

No `application:` or `serves:` belongs on this research Page. A patient is one
possible independent data context, not a universal row grain. The same Page
may declare several datasets when its topic is their comparison. A Board may
organize many such instances; the Application one-extract-per-Board law does
not force a new task-side Board for each patient.

Split a Folder when its topic or independently managed data context changes.
Add an item when another answerable question belongs to the same topic. Do
not split a Page merely because a question or finding has its own completion
state. Do not automatically turn each data row, patient, DIKW rung, figure,
tool call, or finding into a Run.

## R and RI are different Runs

```text
r01_description                    normal Task Run · reusable method/ticket
  ├── ri01_description             points to r01 + patient-a@snapshot-01
  │     └── @v001                  independent DIKW Result
  └── ri02_description             points to r01 + patient-b@snapshot-01
        └── @v001                  independent DIKW Result
```

`rNN` answers **what executable method is reused**. `riNN` answers **which
new frozen dataset is bound to that method for Insight work**. RI is a
first-class Level-4 Run with its own authored YAML Ticket, runtime receipt,
Result, status, and monotonic local counter. It remains in the Page's Task Runs
lane with `family: insight`; it does not create a third Page lane.

The RI relation is immutable:

```text
RI identity = base R ticket id + base ticket hash + dataset snapshot(s)
              + question + DIKW target + acceptance
```

A different dataset allocates a new `riNN`; it is never `rerun` or `v002` of
the old dataset. A retry of the exact frozen RI contract appends an attempt.
A corrected or newly reviewed DIKW publication over the same RI binding may
allocate the next `vNNN`, preserving all earlier Results. A changed base R,
question, target, or acceptance allocates a new RI and may record
`supersedes:`; it must not silently retarget an existing RI.

## The item is the unit of insight work

One item declares its question, base R, frozen datasets, target, expected
Result, and acceptance test. Its stable id is its `riNN_<stem>` ticket stem;
do not add a second `itemNN` namespace or an `items/<item>/` Folder hierarchy.
A proposed row has no actual Run until its RI ticket exists. The human label
may say “Item 1”; the address remains `ri01_description`. Historical
`items-v1` records whose item id is `rNN_<stem>` remain readable, but new work
must allocate RI.

Each execution may call shared Task capabilities, gather evidence, reason
through DIKW, and return positive, null, contradictory, or insufficient
evidence. A target is the depth to assess, not a promise to find a positive
effect. The target is declared per item; a legacy Page `insight-target:` is
only a migration default.

```text
Folder instance
  ri01_description@v001       r01 + dataset A → evidence → D/I/K/W/RF
  ri02_description@v001       r01 + dataset B → evidence → D/I/K/W/RF
  ri01_description@v002       later publication, preserves v001
```

An **Insight Item** is a domain work unit. An **Evidence Item** is a typed
VALUE/CITE/DISPLAY support unit in the shared Outline workspace. They are not
synonyms. An Insight Item may use several Evidence Items. Their producing and
local Runs retain their own targets and receipts; count them as dependencies,
not additional Insight Items. An item Run earns its identity through its own
DIKW Result; a dispatcher that only launches dependencies earns no extra Run.

## Page Face

Retain `Opening → Outline → Content → Aims`. The Content has five divisions:

1. **Origin**: why this research topic exists, without a preferred conclusion.
2. **Instance and Scope**: data context, versions, population/unit, window,
   exclusions, and shared analysis capabilities available to this instance.
3. **Insight Items**: one block per declared item, in stable id order. Each
   names its question, target, exact execution version, progress, and the
   D/I/K/W/RF rows actually supported by that Result. Link the evidence.
4. **Synthesis**: a reading across accepted item Results, including disagreement
   and limits. A new numerical derivation or independently reusable claim
   needs a commissioned item/supporting Task, not an unrecorded calculation.
5. **Reusable Findings**: a generated or explicitly version-bound index of
   accepted item findings. Each row carries the full instance/item/version/RF
   address. This index exports existing findings and creates none.

The item table is a read projection of `workflow/insight.yaml`, tickets, and
Result receipts. Use `scripts/insight_items.py table <folder>` to inspect it.
It is not a second handwritten status ledger. The generic Outline table still
projects the Page plan and typed Evidence Items; the item table summarizes
domain work. Neither replaces the other or adds a new universal Page section.

## Task Face and execution

The Task Face owns item intent, dependency dispatch, input freezing,
checkpoints, Result validation, and publication. Its workflow and Workflow activities × Run ownership
map live in `ref/workflow-table.md`; Page authoring still uses the shared Page
workflow. DIKW is inside each item Result, not four separate Application Folders.

Use the Insight instance dialect in `haipipe-run`: one `riNN` ticket points to
one normal R ticket and resolves to versioned execution addresses in this
instance. Record the full RI address; `r01` alone names only the reusable base
Run and is never the rebound dataset execution. A shared recipe, its normal R
execution, and an RI execution are three different identities.
`ref/task-calls.md` owns the binding protocol.

Shared Task code stays with the producing Task. The Insight supplies the data
manifest, allowed parameters, and output scope through a small local ticket.
It does not edit another patient's inputs or overwrite the producer's default
test execution. A call that a legacy launcher cannot parameterize must first
be adapted and verified; never silently run its default dataset.

Page numeric evidence keeps the existing single page-serving collection route
and named producing Run/Result bindings. Cross-Folder evidence enters through full
Supporting Run Results; each typed make-item still owes its local Evidence
Item Run. Load `haipipe-workbench-page/ref/item-table.md` when mapping those
dependencies. The new item dialect does not authorize direct raw-result
reading from a consuming Page or a second numeric computation path.

## DIKW Result and closure

Every item keeps the trace:

```text
named source/Run → D<n> → I<n> → K<n> → W<n> → RF<n> Reusable Finding
```

D observes dated evidence; I derives patterns from named D rows; K states
claims with strength, rivals, and boundary; W explains applicability and
unsafe inference; RF exports the finding without strengthening it. Row ids are
local to an exact item execution Result. Reusing `D1` in another item is legal
only because the full address disambiguates it.

The checkpoints record frozen inputs, ready evidence, checked reasoning, and
publication. They are resumable records, not additional Runs or automatic
human approval requests. Existing Page/Evidence human decisions remain owned
by their original contracts. A failed or insufficient-evidence Result is a
truthful outcome; it must not be published as an accepted finding.

Item acceptance is independent of sibling items. A completed item can be
reused while another is open. The Page closes only when its declared items
are terminal or explicitly held outside the current scope, its synthesis is
current, and Page CHECK passes. A new dataset/source snapshot allocates a
sibling RI. A changed base recipe, question, target, or acceptance also
allocates a new RI. Both preserve old Results and reopen only dependent
bindings; neither silently upgrades an existing Design citation to the latest
version.

## Handoff

A consumer selects an accepted finding by **instance + item + execution
version + RF id**, with its Result path and hash. The parent Page URL is
navigation, not the evidence address. Use `ref/instance-items.md` for the
portable reference packet and historical single-chain aliases.

RF is not a
Design Handoff. It remains unsigned, consumer-neutral evidence. An Application
registers its QW need and contextualizes the exact item RF in a local,
human-signed Wisdom Folder. The relevant item's Wisdom target and current
accepted Result are tested, not whole-Page completion; unrelated open items
do not block this bridge. An explicit no-answer cannot satisfy the bridge.

## Validation and files

- `scripts/insight_items.py bind <folder> --base-run <rNN> --base-ticket <path>
  --dataset <id@version> --stem <stem> --question <text> --target <rung>
  --expected <text> --acceptance <text>` allocates the next RI, freezes its
  goal/base/dataset binding, and leaves it planned with no final evidence input. It does not execute the base R or fabricate a Result.
- `scripts/insight_items.py freeze <folder> --item <ri> --version <vNNN>
  --evidence <packet.yaml>` validates completed supporting/local evidence and
  seals the interpretation input once. Revisions use the next explicit version.
- `scripts/insight_items.py check <folder>` validates manifests, R→RI binding,
  ticket/Result
  pairing, immutable execution identities, source hashes, checkpoints, DIKW
  references, and accepted finding addresses. It is a structural/provenance
  check, not independent scientific review.
- `scripts/insight_items.py table <folder>` returns one row per declared
  item; the current Result and checkpoint come from receipts.
- `ref/instance-items.md`: runtime schema and exact reference packet.
- `ref/workflow-table.md`: workflow, checkpoints, Workflow activities × Run ownership, reopening.
- `ref/task-calls.md`: reusable Task recipe and instance binding.
- `ref/migration.md`: old Page-to-item mapping and compatibility.
- `agents/openai.yaml`: existing discoverable entry, updated to item semantics.

The skill owns no patient dataset and executes no analysis merely because its
instructions were loaded.
