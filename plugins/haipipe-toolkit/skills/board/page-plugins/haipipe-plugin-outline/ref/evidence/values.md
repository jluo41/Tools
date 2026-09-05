# VALUE Results · one checked quantity ready for one Page use

Read this reference from `haipipe-plugin-outline` when an Evidence Item is
`VALUE`, or when Evidence Workspace must explain a number's provenance. The
Outline plugin owns only the workspace and presentation. The Page EVIDENCE
phase owns LAND/EMBED; the local Run owns the Result.

## 🎯 Ready-evidence contract

A VALUE item has an immutable typed id and one focal payload:

```text
E01-VALUE-adjusted-effect
Expected: VALUE · estimate, interval, unit, population, and model label
Acceptance: recomputes from named Supporting Results; aggregate only
```

The local Result must contain exactly what SHAPE's `Expected` and `Acceptance`
fields require. A bare number, an unlabeled interval, or a number copied from
another Page is not a ready VALUE Result.

## 🔗 One graph, two Run layers

```text
Supporting Runs  0..N  Execution and/or Discovery
                         ↓ validated Results
Local Input        1    frozen Result paths + hashes + governed local sources
                         ↓
Local Run          1    Page · Evidence Item
                         ↓
VALUE Result       1    checked quantity + meaning + provenance
                         ↓
EMBED                    Answered: binding on the target Bullet
```

SURVEY plans and classifies the graph; it creates no Ticket. LAND validates or
executes the Supporting Runs, freezes one Local Input, allocates/executes the
one local Run, and binds its Result. EMBED interprets the accepted Result in
the next outline version. CONTENT may then use it in prose.

## 📦 Result shape

The local Result lives under the Page Folder's paired `results/` tree, never in
a separate value plugin:

```yaml
item: E01-VALUE-adjusted-effect
run: pj01t01r01
type: VALUE
status: complete
payload:
  estimate: 9.34
  interval: [7.81, 10.87]
  unit: MME per visit
  population: eligible visits, primary specification
  model: adjusted OLS
provenance:
  supporting_results:
    - run: b01j02t03r04
      result: tasks/.../results/r04_.../result.yaml
      sha256: <64-hex>
  local_input: results/r01_.../input.yaml#<sha256>
acceptance:
  recomputed: true
  aggregate_only: true
  checks: [estimate-present, interval-ordered, unit-present, population-present]
```

The exact payload may vary with the item contract, but `item`, full Run id,
type, status, provenance, and observable acceptance checks never disappear.
Raw rows and PHI never enter this Result.

## 🧭 Workspace and writing join

Evidence Workspace derives one row per VALUE item:

```text
Item                          Supporting Runs   Local Run       State    Result
E01-VALUE-adjusted-effect     1 Execution       pj01t01r01      ready    9.34 [7.81, 10.87] MME/visit
```

Clicking the item exposes the full Expected/Acceptance contract, Supporting
Run and Result paths, frozen Local Input, local Run receipt, and payload. The
overview stays compact; it never invents a second Status record.

The Bullet and later Page prose cite the Evidence Item id and local Result/Run
identity. This gives a two-way join:

```text
unsourced   prose has a quantity but no VALUE item/local Result
unused      accepted VALUE Result is folded nowhere
bound       Result → item → Bullet → Content all resolve
```

## 🚧 Boundaries and legacy input

- No `value/` plugin or folder exists.
- No new Probe card or `PP<NN>.v<n>` id is created for VALUE work.
- A related Page link is context, not evidence.
- Cross-Folder quantities enter through named Supporting Run Results.
- A Page-local governed static source may enter only through the frozen Local
  Input exception in the item-table contract.
- Legacy Probe `## Values` records and `PP<NN>.v<n>` references are read-only
  migration input. SURVEY converts their evidentiary source to a Supporting
  Result or governed Local Input; new work receives an `E<NN>-VALUE-<slug>` id
  and one local VALUE Run/Result.

The common item and graph laws are in `../item-table.md`; LAND/EMBED authority
is in `haipipe-page-evidence`. This reference owns no scripts or writer.
