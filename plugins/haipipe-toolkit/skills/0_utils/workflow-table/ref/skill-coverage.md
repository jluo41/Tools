# Skill Coverage projection

This reference defines the default skill-review table emitted by
`/workflow-table`. It is the workflow's dependency view: one row per
participating or explicitly referenced skill, with evidence placed beside the
Phase/Cycle rows that use it.

## 1. Row grain

One row represents one literal skill or contract identified in the workflow's
skill chain. It does not represent a phase, a Run, a tool call, or a sentence in
a skill description.

```text
Workflow Table row(s) ──used_by──> one Skill Coverage row
Skill Coverage row ──evidence──> source files, inspection, field-test receipt
```

A shared skill appears once and lists all of its `used_by` Row IDs. A skill
named by the workflow but missing on disk also gets a row: its status is
`⬜ missing`, its version and line count are `?`, and the workflow is `HOLD`
until the missing dependency is resolved or explicitly removed by its owner.

## 2. Canonical rendered view

| Skill | Path | Role | Used by Phase/Cycle | Status | Version | `SKILL.md` lines | Quality / completeness | Field-test | Gap / next action |
|---|---|---|---|---|---|---:|---|---|---|
| `haipipe-page` | `skills/.../haipipe-page/SKILL.md` | contract | `draft.write`, `draft.check` | `✅ structurally valid` | `0.8.0` | `248` | `CONTRACT; 7/8, ◐ receipt-duty` | `✅ FT-2026-08-31` | `add page receipt sentence` |
| `haipipe-run` | `skills/.../haipipe-run/SKILL.md` | contract | `evidence.land` | `? unknown` | `?` | `?` | `?` | `?` | `run inspection before release` |

The table is compact enough to show alongside the Workflow Table. If a review
needs detail, expand the `Quality / completeness` and `Field-test` cells with
the source path and command; do not move the evidence into an unlinked prose
appendix.

## 3. Provenance and evidence rules

Keep the basis of every identity and status visible in the declaration or in a
small note adjacent to the table:

| Provenance kind | Meaning |
|---|---|
| `observed` | read directly from a resolved file or receipt |
| `user-declared` | supplied by the requester but not independently resolved |
| `derived` | mechanically computed from observed facts, such as `wc -l` |
| `unresolved` | a name/path was referenced but cannot be resolved |

Never invent a missing skill's literal name or path. If the requester says that
one dependency is missing but does not identify it, use an ordinal placeholder
such as `<unresolved skill reference 1>`, set provenance to `unresolved`, and
record the missing identity as a `HOLD` finding. A user-declared roster is not
evidence that the named skill exists.

| Column | Required evidence | Legal unknown |
|---|---|---|
| Skill | the literal `name:` in a resolved `SKILL.md` | no; unresolved names are `⬜ missing` |
| Path | the literal on-disk path used for the inspection | no for a present skill |
| Role | the ownership law read from the skill and its workflow use | `?` only when ownership cannot be resolved |
| Used by Phase/Cycle | stable Workflow Table Row IDs | no; an unowned skill is a coverage finding |
| Status | structure/audit result, with the source named when not obvious | `? unknown` |
| Version | frontmatter `metadata.version` or equivalent declared version | `?` plus missing-version finding |
| `SKILL.md` lines | `wc -l <path>/SKILL.md` | `?` when the path cannot be read |
| Quality / completeness | this reference's static quality method, including class and named partial/failing property | `?`; never infer from line count |
| Field-test | dated fresh-context receipt or named field-test result | `?`; no receipt means unproven, not failed |
| Gap / next action | smallest concrete repair, inspection, or field-test event | `none` only when the evidence supports closure |

This reference owns the family inventory and the five ownership classes:
`DOOR`, `MACHINE`, `CONTRACT`, `LIBRARY`, and `CRAFT`. Use `field-test` as the
source for cold behavior evidence. Workflow Table records the static finding
and the behavior evidence separately; it does not score a skill from memory.

Classify by what the skill owns:

| Class | Ownership test | Minimum quality questions |
|---|---|---|
| `DOOR` | routes intent to the member that owns it | Do routes resolve, stay current, and answer when the skill should be picked? |
| `MACHINE` | owns phases, gates, and transitions | Are phases/gates named, closable, receipt-owned, and exercised where evidence exists? |
| `CONTRACT` | owns one artifact's persistent shape and close rule | Is the grain clear, vocabulary addressable, each field legal, the receipt duty named, and the closing check testable? |
| `LIBRARY` | owns reusable assets consumed by a journey | Is the asset neutral, versioned, refreshed on its own clock, and consumed by a named gate? |
| `CRAFT` | owns a bounded transform without lifecycle authority | Is the scope bounded, the output diffable/reversible, and the neighboring owner explicit? |

Record each applicable question as `✓`, `◐`, `✗`, or `—` and name the source
line or missing repair. Use `?` when the review has not gathered the evidence;
never turn an unperformed review into a positive score. This is the static
quality method used by the Skill Coverage table.

`SKILL.md` lines are a useful size signal for the table, but size is not
quality. When a full static quality review is available, its character size and
class-median comparison may be linked in the cell or receipt; the line-count
column remains the simple mechanical count requested by the workflow view.

A fresh-context validation required by repository skill-development practice
is not automatically a `field-test` receipt. It may be listed as a separate
validation source, but the Field-test cell remains `?` until the `field-test`
ledger/commission/settlement evidence exists.

## 4. Status vocabulary

Use one of these values, with a source-backed explanation for every non-unknown
finding:

| Status | Meaning |
|---|---|
| `✅ structurally valid` | required files/frontmatter/declared shape are present and checks pass |
| `🟡 incomplete` | the skill exists but a required field, rule, or declared surface is missing |
| `⚠ stale` | the skill is present but its declaration, version/date, routes, or evidence no longer matches the workspace |
| `❌ invalid` | a validation or contract check fails in a way that blocks use |
| `⬜ missing` | the workflow references a skill that cannot be resolved on disk |
| `? unknown` | the available evidence is insufficient to classify the state |

Do not promote `? unknown` to `✅` because the skill has many lines or a recent
date. Do not call a skill `❌ invalid` merely because it has no field-test; use
`?` or `🟡 incomplete` according to the missing contract requirement.

## 5. Normalized row

The source declaration can be embedded under `workflow_table.skill_coverage`:

```yaml
skill_coverage:
  - skill: <literal skill name>
    path: <literal path to SKILL.md>
    role: <door | machine | contract | library | craft>
    used_by:
      - <stable workflow row id>
    provenance:
      kind: <observed | user-declared | derived | unresolved>
      source: <path, prompt, receipt, or "?">
    status: <status vocabulary value>
    version: <frontmatter version or "?">
    skill_md_lines: <integer or "?">
    quality:
      class: <DOOR | MACHINE | CONTRACT | LIBRARY | CRAFT | "?">
      score_or_finding: <named property score/finding or "?">
      source: <workflow-table Skill Coverage evidence or "?">
    field_test:
      status: <receipt-backed result or "?">
      source: <fresh-context receipt/path or "?">
    gap: <smallest repair or "none">
```

The rendered table and this declaration must agree. A field intentionally not
known at design time is written as `?` and remains an explicit validation
finding; omitted fields are incomplete declarations.

## 6. Audit procedure

1. Read the workflow head and authoritative Phase/Cycle roster.
2. Resolve every `skill_chain` name and deduplicate by literal skill name/path;
   preserve an ordinal unresolved placeholder when the source leaves an
   identity unspecified.
3. Read each resolved `SKILL.md` frontmatter; gather version and date.
4. Run `wc -l` for each `SKILL.md` and record the command-backed count.
5. Apply the static quality method above when a quality claim is needed; name
   the source lines or missing property rather than relying on memory.
6. Load `field-test` evidence when behavior/exercise is claimed.
7. Render one row per skill and link each row to its Workflow Table Row IDs;
   include provenance when a fact came from the requester or a derivation.
8. Mark missing or unproven values explicitly and stop the workflow at `HOLD`
   when the missing dependency or evidence is required for the next gate.

This projection is read-only by default. It reports the file that owns a gap;
it does not rewrite that skill, its version, or its field-test receipt.
