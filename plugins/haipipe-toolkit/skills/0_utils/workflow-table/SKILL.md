---
name: workflow-table
description: >-
  Design, audit, and render a cross-workflow table for a skill family. It fixes
  one row per executable Phase/Cycle, includes default Skill Coverage for the
  skills involved, separates authoritative L3 Task/Page content changes from
  L4 Run activity, and keeps Runs Overview and Human Actions as separate
  surfaces. Use when designing or reviewing Page, Task, Board, Discovery,
  Design, Labeling, or similar workflow contracts; not for ordinary data
  tables or a single-run status report.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.3.0"
  last_updated: "2026-09-01"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /workflow-table · the cross-workflow contract table

Use this skill when a workflow family needs one clear answer to:

```text
Where are we?       → Phase / Cycle
What does this row own? → purpose, input, gate, route
What L3 changes?    → authoritative Task/Page content
What L4 work?       → addressable Run profile and cardinality
Which skills are in play? → role, owner row, status, version, size, quality
What comes next?    → route and handoff
What must a person decide? → Human Action
```

The Workflow Table is an index and design contract. Its default report includes
a Skill Coverage projection so the workflow can show which skills it depends
on and whether those skills are current and exercised. It is not a giant
checklist, a concrete Run inventory, or a replacement for the phase skill that
owns the actual work.

## 🧭 Core model

Define the terms before filling a table:

- **L3 Task/Page content** is the authoritative work object: the plan, outline,
  task manifest, page content, decision record, or other durable content that
  the phase owns.
- **L4 Run** is one independently closable `Ticket → Result` attempt with its
  own target, inputs, acceptance gate, and receipt. A tool call, script,
  agent turn, retry inside one Run, or human tick is not automatically another
  Run.
- **Phase** owns semantic purpose, authority, entry conditions, and closure.
- **Cycle** is the executable unit within a Phase. Use one row for each
  distinct Phase/Cycle contract. A loop is a route unless the repeated cycle
  has a different owner, input, output, or closure boundary.
- **Part** is a reader-facing grouping only. It does not own execution or
  authorize a transition.
- **Skill Coverage** is one row per participating skill or contract. It records
  the skill's role, owning Phase/Cycle, source-backed status, exact version,
  measured `SKILL.md` line count, quality class or completeness finding, field
  evidence, and the smallest next action. A shared skill appears once even if
  several rows use it.

The governing separation is:

```text
Workflow row commissions or permits L4 Runs
                 ↓
L4 Run produces a Result
                 ↓
Phase validates and promotes the Result
                 ↓
authoritative L3 Task/Page content changes
```

Never write that a Run directly changed the authoritative L3 content unless
the owning contract explicitly makes that Run the promotion authority. In the
normal case, the Run produces a candidate or Result; the phase gate binds or
promotes it.

## 📋 The canonical Workflow Table

Every workflow family that has phases publishes this contract view. The
declaration and the rendered table use the same fields, even when a UI hides
some columns for compactness.

| Row ID | Part | Phase | Cycle | Purpose | Input / policy | L3 Task/Page content modified | L4 Run profile | Output | Exit gate | Next route | Human gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `<id>` | `<group>` | `<phase>` | `<cycle>` | `<why>` | `<frozen inputs and policy>` | `<authoritative content or none>` | `<family + operation + cardinality, or none>` | `<artifact/result>` | `<testable assertion>` | `<row id(s) or terminal>` | `<decision, record, or none>` |

Column rules:

- **Row ID** is stable and unique. Prefer `<part>.<phase>.<cycle>` or another
  explicit key that routes can reference mechanically.
- **Purpose** says what this row accomplishes, not how an agent happens to
  implement it.
- **Input / policy** names the versioned inputs, scope, and governing contract.
  Do not hide an input in prose or infer it from a sibling row.
- **L3 Task/Page content modified** names the exact logical content or path
  that is created, revised, bound, promoted, or explicitly left unchanged.
  Use `none` when the row is read-only or only produces a transient result.
- **L4 Run profile** states the permitted Run family, operation or target,
  and symbolic cardinality. Use `none` for planning, gates, and other rows
  with no addressable Runs. `0..N`, `exactly 1`, and formulae such as `N_make`
  are plans, not actual inventory.
- **Output** is the phase-level product, including a receipt or decision
  record when one is required.
- **Exit gate** must be checkable from named files, fields, receipts, or an
  explicitly named human decision. “Looks good” is not a gate.
- **Next route** lists valid destination Row IDs, including backward routes
  and terminal `CLOSE`. A route to a missing row is a contract error.
- **Human gate** records the decision reserved for a person. Use `none` when
  closure is mechanical. A human gate is not a Run merely because it is
  recorded in a Task Face.

For a compact runtime display, use:

| Part | Phase | Cycle | Status | L3 change | Active L4 Runs | Next | Human action |
|---|---|---|---|---|---|---|---|

Do not remove the full contract view from the owning skill. The compact view is
only a presentation projection.

## 🔀 Four synchronized surfaces

Keep different row grains in different surfaces:

| Surface | One row represents | Required |
|---|---|---|
| **Workflow Table** | One Phase/Cycle contract | Always for a phased workflow |
| **Runs Overview** | One logical L4 Run | When the workflow permits addressable Runs |
| **Human Actions** | One unresolved human decision | When the workflow has human gates |
| **Skill Coverage** | One participating skill or contract | Default; rendered last in every workflow report |

The default Runs Overview is:

| Run | Owner Phase/Cycle | Kind | Target | Depends On | Status | Result |
|---|---|---|---|---|---|---|
| `bNNjNNtNNrNN` | `<row id>` | `<Run family>` | `<target>` | `<Run ids or none>` | `<planned/runtime state>` | `<Result pointer or none>` |

One row is one L4 Run. Keep the Result on that row. Put the ticket, frozen
inputs, receipt, full Result, logs, acceptance, and `supersedes` details behind
the row rather than expanding the overview into a file tree.

The default Human Actions surface is:

| Gate | Owner Phase/Cycle | Trigger | Decision | State | Record |
|---|---|---|---|---|---|
| `<gate>` | `<row id>` | `<when it appears>` | `<what the person answers>` | `<open/signed/returned>` | `<path or receipt>` |

Do not turn every Run into a human checklist item. In a normal workflow, the
person sees only the decisions that authorize, route, or accept work. A failed
or held Run may expose a detail action, but it does not change the row grain.

## 🧩 Default Skill Coverage

Render Skill Coverage last in every `/workflow-table` design, audit, or show
operation, unless the user explicitly asks for a phase-only compact view. The
report order is therefore:

```text
Workflow Table → Runs Overview → Human Actions → Skill Coverage
```

This is where the skill review lives; do not bury it in an unstructured
appendix.

| Skill | Path | Role | Used by Phase/Cycle | Status | Version | `SKILL.md` lines | Quality / completeness | Field-test | Gap / next action |
|---|---|---|---|---|---|---:|---|---|---|
| `<skill-name>` | `<literal path>` | `<door/machine/contract/library/craft>` | `<row ids>` | `<status>` | `<version>` | `<wc -l>` | `<class/score or finding>` | `<receipt or ?>` | `<smallest repair or none>` |

Populate the fields from evidence, not from the visual impression of a skill:

- **Skill / Path** use the literal `name:` and on-disk `SKILL.md` path. A
  referenced skill that cannot be resolved gets its own `⬜ missing` row and a
  `HOLD` finding; do not silently omit it. If the source names only an
  unresolved dependency without giving its name or path, render an ordinal
  placeholder such as `<unresolved skill reference 1>` and mark the identity as
  user-declared/unresolved; never invent a plausible skill name or path.
- **Role** describes what the skill owns in this workflow: door, phase
  machine, artifact contract, library, or craft. If the workflow uses another
  vocabulary, name it and define it in the row.
- **Used by Phase/Cycle** lists stable Workflow Table Row IDs. A skill used by
  multiple rows still has one Skill Coverage row.
- **Status** is source-backed: `✅ structurally valid`, `🟡 incomplete`,
  `⚠ stale`, `❌ invalid`, `⬜ missing`, or `? unknown`. Do not infer status
  from age or line count alone.
- **Version** comes from the skill frontmatter. If it is absent, show `?` and
  report missing version as a finding; do not invent a semver.
- **Lines** comes from `wc -l <path>/SKILL.md`. It is a size fact, not a
  quality score. Character size may be added when the static quality method
  requires its class-median comparison.
- **Quality / completeness** records the static quality class and named finding
  from [`ref/skill-coverage.md`](ref/skill-coverage.md) (`DOOR`, `MACHINE`,
  `CONTRACT`, `LIBRARY`, or `CRAFT`). If the review has not assessed it, use
  `?` rather than scoring from memory.
- **Field-test** records a dated fresh-context receipt, a named field-test
  result, or `?`. Static structure and dynamic behavior are separate facts.
- **Gap / next action** names the smallest repair or validation event. `none`
  is valid only when the source and evidence support it.

For every row, keep a provenance note in the declaration or adjacent report:
`observed` (read from disk), `user-declared` (supplied by the requester),
`derived` (mechanically computed from observed facts), or `unresolved`. A
user-declared roster or dependency is useful input, but it is not proof that
the path, version, quality, or behavior exists. If a value is required for a
gate and its provenance is not observed, use `?`/`HOLD`.

`workflow-table` owns the inventory and static quality view; `field-test`
remains the behavior proof. Skill Coverage places both kinds of evidence beside
the workflow rows without pretending that static structure proves runtime
behavior.

## 📚 Workspace Run Catalogue

When a workspace has several kinds of work, keep a separate reference table
for the vocabulary of Runs. The catalogue has one row per Run type, not one row
per live instance and not one row per Workflow Table Phase/Cycle. It answers
“what can a Run be in this workspace?”; the Runs Overview answers “which actual
Run happened for this workflow?” See
[`ref/run-catalog.md`](ref/run-catalog.md) for the normalized shape and
examples.

The catalogue is a reference projection and may be linked from a workflow
report. The `ref/run-catalog.md` shipped beside this skill is a schema/example
reference unless a workflow explicitly declares it as its workspace catalogue;
it does not automatically make every example key a live workspace type. A
declared catalogue must have a resolved path and its own `run_catalog.runs`
rows. The catalogue does not supply current status, completed counts, or
receipts; those belong to concrete Runs Overview rows.

## ⚙️ L4 Run profile rules

Use the L4 column to describe work that can close independently:

```text
<Run family> · <operation> · <cardinality>
```

Examples:

```text
none
Execution · fit-model · 0..N
Discovery · source-analysis · N_subjects
Page · Evidence Item · exactly 1 per make-item
Page · Division Writing · one per ready division
```

Apply these distinctions:

| Situation | Workflow Table entry |
|---|---|
| A planning row identifies future work | `none; defines Run demand` |
| Several calls share one Ticket, target, and Result gate | One Run, not one Run per call |
| A phase has independently closable children | List the child Run family; do not mint an umbrella Run merely for the phase |
| A bare approval or signature | Human gate, not a Run |
| An actual execution attempt | A Run with an allocated identity and receipt |

When a workflow uses a neutral Run contract, load it before finalizing the
table. Its identity, Ticket/Result pairing, receipt, planned-versus-actual
counting, and audit rules remain the authority below this presentation layer.

## 🛠️ Design, render, or audit

### Design a new workflow table

1. Find the workflow head and its authoritative phase roster. If the roster is
   unavailable, report a named HOLD instead of inventing phases.
2. Read the relevant phase contracts and the neutral Run/Folder/Page/Task
   contracts when the workflow uses them. Use the phase contract for semantics;
   use this skill for the common table shape.
3. Build the skill chain and Skill Coverage rows. Apply the static inventory
   and quality method in [`ref/skill-coverage.md`](ref/skill-coverage.md), and
   use `field-test` receipts when available. Gather versions from frontmatter
   and line counts with `wc -l`; never use size as a proxy for quality. Mark
   each fact as observed, user-declared, derived, or unresolved; never invent
   an unnamed dependency's identity.
4. Draft one structured declaration per distinct Phase/Cycle. Set every field,
   including explicit `none` values.
5. Check the L3/L4 boundary: every L3 cell names authoritative content, and
   every non-`none` L4 cell names a closable Run family, target, operation, and
   cardinality.
6. Derive the Runs Overview and Human Actions surfaces only when their row
   grains exist. Do not copy planned Run counts into actual status.
7. Link Run profiles to a declared workspace Run Catalogue when one exists;
   label the bundled `ref/run-catalog.md` as template-only otherwise. Do not
   turn catalogue types into concrete Runs.
8. Validate the declaration, Skill Coverage, and routes using the rules in
   [`ref/workflow-table-schema.md`](ref/workflow-table-schema.md).
9. Render the contract table, Runs Overview, Human Actions, and Skill Coverage
   last, or all applicable surfaces according to the user's request. Add the
   Run Catalogue only as a linked reference when needed. Save an artifact only
   when the user names a path.

### Audit an existing workflow

Compare, in this order:

```text
authoritative phase roster
        ↓
phase contracts
        ↓
skill chain and Skill Coverage
        ↓
Workflow Table declarations/rendering
        ↓
Run Catalogue references
        ↓
Runs Overview and receipts
        ↓
Human Actions and gate records
```

Report missing, extra, duplicate, stale, or contradictory rows. A table that
looks complete but has no owning phase contract is not evidence of a complete
workflow.

### Write or update a table artifact

The default operation is read-only and returns the table in the reply. If the
user asks for a file, write only the named table/declaration artifact. Do not
silently rewrite phase skills, Task/Page content, Run tickets, or receipts.
Those mutations belong to their owning contracts and require the user's
request for that change.

## ✅ Validation gates

A Workflow Table is ready only when all of these hold:

- every authoritative Phase/Cycle has exactly one Row ID;
- every Row ID is unique and every route resolves to a Row ID or `CLOSE`;
- every row names its input/policy, output, and testable exit gate;
- the L3 column distinguishes authoritative content from transient Results;
- every non-`none` L4 profile states family, target/operation, cardinality, and
  the owning Run/phase contract;
- every participating or explicitly referenced skill has exactly one Skill
  Coverage row, with its literal path, version, line count, and evidence
  provenance shown or marked `?`;
- an unresolved dependency is represented without an invented name or path;
- every non-unknown quality claim is backed by the static quality method in
  `ref/skill-coverage.md`, and every field-test claim points to a receipt or
  named fresh-context test;
- every Run profile key resolves to a Run type in the workspace Run Catalogue
  when that catalogue is declared; a bundled schema/example reference is
  labelled template-only and cannot prove resolution;
- planned cardinality is not presented as receipt-backed actual inventory;
- every human gate appears in Human Actions with a decision and record;
- Runs Overview rows have an owner row, a valid identity/status, and a Result
  pointer when the Run is complete;
- compact phase Status values are backed by an explicit runtime state, receipt,
  or human record; otherwise use `planned`/`?` with its provenance rather than
  inferring a status from the table;
- no phase, step, tool call, script, Result file, or human tick is double-counted
  as an L4 Run;
- the rendered view agrees with the structured declaration.

If a check cannot be resolved from the available files, report the exact
missing input and stop at `HOLD`. Do not fill the cell with a plausible guess.

## 📚 Related contracts

- [`ref/workflow-table-schema.md`](ref/workflow-table-schema.md) contains the
  normalized declaration shape, field definitions, example rows, Skill
  Coverage fields, and audit rules.
- [`ref/skill-coverage.md`](ref/skill-coverage.md) defines evidence sources,
  status vocabulary, and the Skill Coverage projection.
- [`ref/run-catalog.md`](ref/run-catalog.md) defines workspace-level Run types
  and the boundary between a Run type and a concrete Run instance.
- `ref/skill-coverage.md` owns family inventory and static quality classes;
  `field-test` owns fresh-context behavior evidence when that skill is
  available.
- `haipipe-workflow` owns the broader IPO and Plan → Build → Execute → Report
  lifecycle when that skill is available.
- `haipipe-run` owns Level-4 identity, Ticket/Result pairing, receipts, and
  Run counting when that skill is available.
- The owning workflow and phase skills remain authoritative for domain meaning,
  gates, and actual file ownership.

## 📂 Files

```text
workflow-table/
├── SKILL.md                         this contract and operating method
├── CHANGELOG.md                     skill-scoped version history
├── agents/openai.yaml               UI metadata and invocation prompt
├── ref/workflow-table-schema.md     declaration, Skill Coverage, validation
├── ref/skill-coverage.md            evidence-backed skill inventory projection
└── ref/run-catalog.md               workspace Run-type reference projection
```
