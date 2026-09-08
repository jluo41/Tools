---
name: haipipe-page-insight
description: >-
  Create or update a task-side Insight Page Folder for one research topic and
  data context. Its Insight Items are independently runnable questions; each
  produces a versioned DIKW result and reusable findings. Use for dataset or
  patient insight instances, item Runs, resumable checkpoints, shared Task
  analysis calls, and exact instance/item/result citations. Application
  InsightBoard rung pages remain owned by haipipe-insight-workflow.
metadata:
  version: "1.0.0"
  last_updated: "2026-09-08"
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
one local Run ticket and a history of immutable execution Results. An item is
not another Page Folder. The Page organizes the findings from its items.

Load `haipipe-page` and `haipipe-page-workflow` for the shared Page frame and
authoring controls. Read `ref/instance-items.md` for identity, schemas, runtime
structure, and citations; `ref/workflow-table.md` when planning or resuming;
`ref/task-calls.md` when invoking reusable analysis. Migration from the previous
single-question Page is described in `ref/migration.md`.

## Scope and ownership

`/haipipe-task insight "<topic>" [<board>]` creates or resumes this Folder.
Keep the public skill and installed path; no second Insight skill or parallel
Page frame is required. This remains the task-only Page Type during the
shared Folder-kind migration:

```yaml
page-type: insight
scope: task
insight-layout: items-v1
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

## The item is the unit of insight work

One item declares its question, frozen inputs, target, expected Result, and
acceptance test. Its stable id is its `rNN_<stem>` ticket stem; do not add a
second `itemNN` namespace or an `items/<item>/` Folder hierarchy. A proposed
row has no actual Run until its ticket exists. The human label may say
“Item 1”; the address remains `r01_description`.

Each execution may call shared Task capabilities, gather evidence, reason
through DIKW, and return positive, null, contradictory, or insufficient
evidence. A target is the depth to assess, not a promise to find a positive
effect. The target is declared per item; a legacy Page `insight-target:` is
only a migration default.

```text
Folder instance
  r01_description@v001       bounded question → evidence → D/I/K/W/RF
  r02_temporal-pattern@v001  bounded question → evidence → D/I/K/W/RF
  r01_description@v002       later execution, preserves v001
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
checkpoints, Result validation, and publication. Its workflow and Phase × Run
Map live in `ref/workflow-table.md`; Page authoring still uses the shared Page
workflow. DIKW is inside each item Result, not four new phase-owned Folders.

Use the Insight instance dialect in `haipipe-run`: one stable local ticket
resolves to versioned execution addresses in this instance. Record the full
address; `r01` alone is never a cross-Folder execution reference. A shared
recipe, a test execution of that recipe, and an instance execution are three
different identities. `ref/task-calls.md` owns the binding protocol.

Shared Task code stays with the producing Task. The Insight supplies the data
manifest, allowed parameters, and output scope through a small local ticket.
It does not edit another patient's inputs or overwrite the producer's default
test execution. A call that a legacy launcher cannot parameterize must first
be adapted and verified; never silently run its default dataset.

Page numeric evidence keeps the existing single page-serving collection route
and named producing Run/Result bindings. Cross-Folder evidence enters through full
Supporting Run Results; each typed make-item still owes its local Evidence
Item Run. Load `haipipe-plugin-outline/ref/item-table.md` when mapping those
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
current, and Page CHECK passes. A data/recipe/source change preserves old
Results and reopens only dependent bindings. It never rewrites history or
silently upgrades an existing Design citation to the latest version.

## Handoff

A consumer selects an accepted finding by **instance + item + execution
version + RF id**, with its Result path and hash. The parent Page URL is
navigation, not the evidence address. Use `ref/instance-items.md` for the
portable reference packet and historical single-chain aliases.

RF is not a
Design Handoff. It remains unsigned, consumer-neutral evidence. An Application
registers its I1 QW need and contextualizes the exact item RF in a local,
human-signed I5 Wisdom Folder. The relevant item's Wisdom target and current
accepted Result are tested, not whole-Page completion; unrelated open items
do not block this bridge. An explicit no-answer cannot satisfy the bridge.

## Validation and files

- `scripts/insight_items.py check <folder>` validates manifests, ticket/Result
  pairing, immutable execution identities, source hashes, checkpoints, DIKW
  references, and accepted finding addresses. It is a structural/provenance
  check, not independent scientific review.
- `scripts/insight_items.py table <folder>` returns one row per declared
  item; the current Result and checkpoint come from receipts.
- `ref/instance-items.md`: runtime schema and exact reference packet.
- `ref/workflow-table.md`: workflow, checkpoints, Phase × Run Map, reopening.
- `ref/task-calls.md`: reusable Task recipe and instance binding.
- `ref/migration.md`: old Page-to-item mapping and compatibility.
- `agents/openai.yaml`: existing discoverable entry, updated to item semantics.

The skill owns no patient dataset and executes no analysis merely because its
instructions were loaded.
