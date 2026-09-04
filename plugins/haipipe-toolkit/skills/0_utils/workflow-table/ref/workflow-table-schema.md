# Workflow Table schema and validation reference

This reference is loaded by `/workflow-table` when a structured declaration,
cross-family audit, or generated rendering needs more precision than the
entrypoint provides.

## 1. Normalized declaration

The recommended source of truth is one workflow declaration with one row per
distinct Phase/Cycle. YAML is illustrative; an existing workflow may use
another machine-readable format if it preserves the same fields.

```yaml
workflow_table:
  id: <workflow-family-id>
  title: <human-readable workflow name>
  owner: <workflow-head skill or contract>
  skill_coverage:
    - skill: <literal skill name>
      path: <literal path to SKILL.md>
      role: <door | machine | contract | library | craft>
      used_by: [<stable row ids>]
      provenance:
        kind: <observed | user-declared | derived | unresolved>
        source: <path, prompt, receipt, or "?">
      status: <source-backed status>
      version: <frontmatter version or "?">
      skill_md_lines: <integer or "?">
      quality:
        class: <DOOR | MACHINE | CONTRACT | LIBRARY | CRAFT | "?">
        score_or_finding: <named score/finding or "?">
        source: <workflow-table Skill Coverage evidence or "?">
      field_test:
        status: <receipt-backed result or "?">
        source: <fresh-context receipt/path or "?">
      gap: <smallest repair or "none">
  run_catalog:
    mode: <declared | template-only | none>
    ref: <workspace catalogue path or "none">
    keys: [<catalog Run keys used by this workflow>]
  rows:
    - id: <stable-row-id>
      part: <reader-facing grouping>
      phase: <semantic phase>
      cycle: <executable cycle>
      runtime_status:
        value: <planned | ready | active | blocked | accepted | returned | closed | "?">
        source: <phase state, receipt, decision record, or "design-time">
      purpose: <one sentence>
      input_policy:
        - <versioned input, scope, or governing policy>
      l3_content_modified:
        - <authoritative Task/Page content or none>
      l4_run_profile:
        families: []                 # [] means no addressable Runs
        operations: []               # e.g. fit-model, source-analysis
        target: <target grammar or none>
        cardinality: "0"             # symbolic until runtime allocates work
        owner_contract: <Run contract or none>
      skill_chain:
        - <workflow skill>
        - <phase skill>
      output:
        - <phase-level artifact, Result binding, receipt, or decision>
      exit_gate:
        kind: machine                 # machine | human | mixed
        assertion: <testable completion assertion>
        record: <path, field, receipt, or none>
      next_route:
        - <another row id or CLOSE>
      human_gate:
        kind: none                    # none | approval | decision | acceptance
        question: <what the person decides or none>
        record: <signature/decision path or none>
```

The declaration is intentionally explicit. `families: []`, `cardinality: "0"`,
and `human_gate.kind: none` mean different things from omitted fields:

| Value | Meaning |
|---|---|
| `families: []` | This row permits no addressable L4 Run |
| `cardinality: "0"` | No Run is expected for this row |
| `human_gate.kind: none` | Closure has no person decision |
| `next_route: [CLOSE]` | The row may terminate the workflow |
| omitted/unknown | The declaration is incomplete and should be held |

`skill_coverage` is a projection of the workflow's skill chain, not a second
phase roster. It has one row per literal participating or explicitly
referenced skill. `used_by` points back to `rows[].id`; a shared skill is listed
once. The values have distinct evidence sources:

| Field | Source of truth | If unavailable |
|---|---|---|
| `skill`, `path`, `version` | resolved `SKILL.md` frontmatter and literal path | `?` plus a named finding; unresolved path is `⬜ missing` |
| `skill_md_lines` | `wc -l <path>/SKILL.md` | `?`, never an estimate |
| `quality` | the static quality method in `ref/skill-coverage.md` and named evidence | `?`; do not score from length or memory |
| `field_test` | dated fresh-context/field-test receipt | `?`; static validity is not behavior proof |
| `status` | the above evidence and explicit audit finding | `? unknown` |
| `provenance` | how the identity/fact entered the report | `unresolved` when the source does not resolve |

The five quality classes are ownership labels, not a maturity ranking:
`DOOR`, `MACHINE`, `CONTRACT`, `LIBRARY`, and `CRAFT`. A line count is a size
fact only. A workflow may report a completeness gap in `quality.score_or_finding`
or `gap`, but must name the missing evidence or rule.

`run_catalog` points to a workspace reference table of Run types. Its `keys`
are vocabulary references, not allocated Run IDs and not completed counts. A
concrete Run still needs its own Runs Overview row, Ticket, Result, and receipt.
`mode: declared` requires a resolved workspace catalogue artifact containing
`run_catalog.runs`; `mode: template-only` means the bundled schema/examples are
being used for vocabulary guidance and cannot prove that a key exists in this
workspace. `mode: none` is explicit absence.

`rows[].runtime_status` is a runtime overlay, not a replacement for the
Phase/Cycle contract. `planned` is legal for design-time demand; all other
values need the named phase state, receipt, or decision record in `source`.
When no state is known, use `?`, not a visually inferred status.

Do not use `none`, `person`, or another vague placeholder to hide a missing
route, missing input, or impossible work request. Use a named `HOLD` finding.

## 2. Required field semantics

### Identity fields

`workflow_table.id` identifies the workflow family, not a live Run. `rows[].id`
is the stable key used by routes, audits, and cross-surface ownership. Two rows
may have the same display label only when their IDs and closure boundaries are
different; otherwise they are duplicate rows.

### L3 field

`l3_content_modified` contains logical authorities, not incidental files:

```yaml
l3_content_modified:
  - outline/<page>-outline-v4.md
  - outline/<page>-evidence-items.md
```

For a phase that consumes a Result but does not yet promote it:

```yaml
l3_content_modified:
  - none; reads the landed Result and writes no authoritative content
```

The field may name a new version of an existing L3 artifact. It should not
pretend that a generated Run Result is already the authoritative Page/Task
content. The normal promotion chain is:

```text
Run Result → phase acceptance → bind/promote → L3 content version
```

### L4 field

`l4_run_profile` describes planned capability, not actual inventory. A
non-empty profile should answer four questions:

1. Which Run family is allowed?
2. What operation or target does the Run own?
3. How many Runs may the row commission, symbolically?
4. Which contract defines the Ticket, Result, and close gate?

Examples:

```yaml
# Planning only
l4_run_profile:
  families: []
  operations: []
  target: none
  cardinality: "0"
  owner_contract: none

# One logical Run per ready division
l4_run_profile:
  families: ["Page · Division Writing"]
  operations: ["write-division"]
  target: "C<NN>"
  cardinality: "N_ready_divisions"
  owner_contract: haipipe-run
```

If a row has several Run families, list them separately rather than collapsing
them into a vague “N Runs” cell:

```yaml
l4_run_profile:
  families: [Execution, Discovery]
  operations: [reuse, rerun, new-run, new-task]
  target: "supporting evidence item"
  cardinality: "sum(S_i)"
  owner_contract: haipipe-run
```

The actual count comes only from allocated Run identities and valid receipts.
Never convert `N_ready_divisions` or `sum(S_i)` into “12 completed” without
receipt-backed inventory.

### Gate and route fields

`exit_gate.assertion` is a condition a reviewer or checker can evaluate. The
gate may be machine, human, or mixed, but its evidence must be named. A human
gate should be repeated in the Human Actions surface, not left only in a
sentence in the Workflow Table.

`next_route` is a directed edge list. Backward routes are valid and should be
visible:

```yaml
next_route:
  - draft.write
  - outline.survey
  - outline.shape
```

An unresolved finding is not a new phase by itself. Route it to the row that
owns the correction. Use a new row only when the correction has its own
independent purpose and closure.

## 3. Worked cross-domain rows

These examples show the grammar, not a universal phase roster. The owning
workflow must supply its own names and semantics.

### Page-style workflow

| Row ID | Part | Phase | Cycle | L3 Task/Page content modified | L4 Run profile | Exit gate | Human gate |
|---|---|---|---|---|---|---|---|
| `outline.shape` | Outline | OUTLINE | SHAPE | outline plan + typed item expectations | none | every item has target, expected Result, and acceptance | approve outline |
| `outline.survey` | Outline | OUTLINE | SURVEY | item table: route, Local Input, Local Run plan, decision | none; defines demand | every item graph is valid and decided | make / defer / drop |
| `evidence.land` | Outline | EVIDENCE | LAND | item table gains allocated Run IDs and Result pointers | Supporting Execution/Discovery `0..N` + one local item Run per make-item | every make-item has a valid local Result | none |
| `evidence.embed` | Outline | EVIDENCE | EMBED | outline v<N+1> gains folded answers and bindings | none | every required Result is folded | none |
| `draft.write` | Draft | DRAFT | WRITE | Page Content divisions after promotion | Page · Division Writing, one per ready division | built candidate passes internal checks | none |
| `draft.check` | Draft | CHECK | CHECK | acceptance/feedback record; never producer prose | none by default | Page accepted or routed backward | accept or give feedback |

The Page example demonstrates the key distinction:

```text
LAND / WRITE Run → candidate or typed Result
                → phase gate
                → L3 item/outline/Page content update
```

### Generic task-style workflow

| Row ID | Part | Phase | Cycle | L3 Task content modified | L4 Run profile | Exit gate | Human gate |
|---|---|---|---|---|---|---|---|
| `task.plan` | Task | PLAN | PLAN | task manifest and acceptance contract | none | inputs, scope, and close condition are frozen | approve scope when required |
| `task.execute` | Task | EXECUTE | RUN | progress/receipt links only | Execution `0..N` | every commissioned Run has a truthful receipt | none |
| `task.report` | Task | REPORT | PROMOTE | report and promoted outputs | none | report reconciles planned and actual inventory | accept report when required |

The task-style example does not imply that every task has exactly three rows.
It shows how the L3 and L4 columns stay separate across domains.

## 4. Rendering projections

The same declaration may render into four synchronized surfaces without
changing row meaning. The default report order is:

```text
Workflow Table → Runs Overview → Human Actions → Skill Coverage
```

### Full contract view

Use for skill designers and reviewers:

```text
ID · Part · Phase · Cycle · Purpose · Input/policy · L3 modified ·
L4 profile · Skill chain · Output · Exit gate · Next route · Human gate
```

### Runs Overview / runtime view

Use for a person following progress. Keep planned demand separate from actual
receipt-backed inventory:

```text
Part · Phase · Cycle · Status · L3 change · active L4 Runs · Next · Human action
```

`Status` comes from `rows[].runtime_status` and its named phase-state, receipt,
or decision source. It is not a replacement for the exit gate.

### Human Actions view

Use for decisions reserved for a person:

```text
Gate · Owner Phase/Cycle · Trigger · Decision · State · Record
```

Every human gate in the Workflow Table should appear here once. A Human Action
is not a Run.

### Catalogue view

Use when the workflow introduces a Run family not already explained in the
workspace reference:

```text
Run key · Family · Run for · Common operations · Target · Inputs · Result ·
Close gate · Owner contract · Not a Run when
```

The bundled `ref/run-catalog.md` is a template/example reference. A workflow
must label it `template-only` unless a separate, resolved workspace artifact is
explicitly declared as the live catalogue.

### Run detail view

Use after a person opens one Runs Overview row:

```text
Run ID · owner row · Ticket · target · frozen inputs · dependencies ·
runtime receipt · Result · acceptance · logs/errors · supersedes
```

Do not put this detail into every Workflow Table cell.

### Skill Coverage view

Render last in every default design, audit, and “show me the workflow” report.
Include the provenance note for any user-declared or unresolved identity:

```text
Skill · Path · Role · Used by Phase/Cycle · Status · Version · SKILL.md lines ·
Quality/completeness · Field-test · Gap/next action
```

## 5. Audit rules

Run the following checks in order:

| Check | Failure finding |
|---|---|
| Roster coverage | declared phase/cycle has no row, or row has no owner |
| Skill coverage | participating or referenced skill has no unique coverage row, or a coverage row has no owning Workflow Table Row ID |
| Skill evidence | version, line count, quality, or field-test claim has no source or is inferred from size |
| Provenance | user-declared or unresolved identity is presented as observed, or an unnamed missing dependency is invented |
| Identity | duplicate/missing Row ID |
| Route closure | route points to an unknown row or omits a terminal/hold route |
| Input completeness | required input or policy is omitted or only implied |
| L3 truth | transient Result, log, or command is claimed as authoritative L3 content |
| L4 truth | step, tool call, human gate, or Result file is counted as a Run |
| Run profile | non-empty Run profile lacks family, target/operation, cardinality, or owner contract |
| Run catalogue | declared Run family has no matching catalogue key, or a type row is mistaken for a live Run |
| Runtime status | compact Status has no phase-state/receipt/decision source or is inferred from the plan |
| Gate testability | exit gate cannot be checked from named evidence |
| Human mirror | human gate is absent from Human Actions or has no record |
| Inventory truth | planned cardinality is presented as actual completed work |
| Projection agreement | rendered table differs from structured declaration |

Report each finding with the row ID, the source file, and the smallest repair
needed. Do not repair a domain phase contract from this utility unless the user
explicitly asks for that mutation.

## 6. Minimal conformance checklist

```text
[ ] one row per distinct Phase/Cycle
[ ] stable unique Row IDs
[ ] L3 authoritative content named or explicitly none
[ ] L4 family/operation/target/cardinality named or explicitly none
[ ] inputs and policy named
[ ] output and testable exit gate named
[ ] routes resolve, including loops and CLOSE/HOLD
[ ] one Skill Coverage row per participating/referenced skill
[ ] skill path, version, line count, quality provenance, and field evidence are exact or `?`
[ ] user-declared, derived, observed, and unresolved provenance is explicit
[ ] Run profile keys resolve to Run Catalogue types when a catalogue is declared
[ ] template-only catalogue references are not presented as workspace facts
[ ] Runs Overview keeps one row per L4 Run
[ ] Human Actions keeps one row per human decision
[ ] actual inventory comes from Tickets and receipts
[ ] rendered projection matches the declaration
```
