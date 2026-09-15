# Skill Coverage projection

Skill Coverage is the dependency/audit view of a Workflow × Workspace table.
One row represents one literal skill referenced by a Cell's `owner_skill` or
`worker_skill_chain`.

```text
Run Spec × member Workspace ──is──> Cell
Cell skill bindings ──used_by_cells──> Skill Coverage row
```

Skill is not an axis. A shared skill appears once and lists every Cell it
serves. A missing referenced skill also gets one row and blocks the Workflow.

## Rendered view

| Skill | Path | Role | Used by Cell(s) | Status | Version | Lines | Quality | Field-test | Gap |
|---|---|---|---|---|---|---:|---|---|---|
| `haipipe-run` | `../../../run/haipipe-run/SKILL.md` | contract | `generate@create`, `generate@runtime`, `adopt@runtime` | `?` | `?` | `?` | `?` | `?` | inspect current contract |

Use exact Cell coordinates, not only a Run Spec label or Workspace name.

## Normalized row

```yaml
skill_coverage:
  - skill: <literal skill name>
    path: <literal path to SKILL.md>
    role: <door | machine | contract | library | craft>
    used_by_cells: [<run-spec-id>@<workspace-id>]
    provenance:
      kind: <observed | user-declared | derived | unresolved>
      source: <Cell declaration, path, receipt, or "?">
    status: <status vocabulary>
    version: <frontmatter version or "?">
    skill_md_lines: <integer or "?">
    quality:
      class: <DOOR | MACHINE | CONTRACT | LIBRARY | CRAFT | "?">
      score_or_finding: <named finding or "?">
      source: <evidence or "?">
    field_test:
      status: <receipt-backed result or "?">
      source: <receipt/path or "?">
    gap: <smallest repair or none>
```

## Evidence rules

| Provenance | Meaning |
|---|---|
| `observed` | read from a resolved Cell, skill file, or receipt |
| `user-declared` | supplied by the requester but not independently resolved |
| `derived` | mechanically computed from observed facts |
| `unresolved` | referenced identity/path cannot be resolved |

Never invent a missing name/path. Use an ordinal unresolved placeholder and a
`HOLD` finding when identity is unknown.

| Field | Required evidence |
|---|---|
| Skill/path/version | resolved `SKILL.md` frontmatter and literal path |
| Used by Cell(s) | Cell owner/worker bindings |
| Lines | `wc -l` on the resolved file |
| Quality | source-backed static review for the ownership class |
| Field-test | dated fresh-context behavior receipt |
| Status | explicit evidence and finding |

Unknown is `?`, never an inferred pass.

## Ownership classes

| Class | Test |
|---|---|
| `DOOR` | routes intent to the correct owner |
| `MACHINE` | owns a Run Spec graph, Gates, Routes, and terminal rules |
| `CONTRACT` | owns one artifact/identity shape and close rule |
| `LIBRARY` | owns reusable assets consumed by named Runs/Gates |
| `CRAFT` | owns a bounded transform without Workflow authority |

For each class, record `✓`, `◐`, `✗`, `—`, or `?` with a source. Line count is
only a size signal, not quality.

## Status vocabulary

| Status | Meaning |
|---|---|
| `✅ structurally valid` | required structure and checks pass |
| `🟡 incomplete` | a required field/surface is missing |
| `⚠ stale` | declaration no longer matches current Workflow/Workspace |
| `❌ invalid` | validation fails and blocks use |
| `⬜ missing` | referenced skill cannot be resolved |
| `? unknown` | evidence is insufficient |

## Audit procedure

1. Read the Plugin/work object's plural Workspace roster.
2. Read the Workflow's Run Spec graph.
3. Resolve every Cell's owner/worker skill bindings.
4. Deduplicate by literal name/path while preserving all `used_by_cells`.
5. Read each skill frontmatter and gather exact version/line count.
6. Apply the source-backed quality class questions.
7. Load fresh-context field-test evidence when behavior is claimed.
8. Render one row per skill and mark unresolved values explicitly.

This projection is read-only. It reports the owning file for a gap and never
silently edits that skill.
