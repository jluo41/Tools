Insight Entry Schema — Canonical Spec
======================================

Authoritative shape for every entry under `examples/<project>/insights/`.
All four layer skills (haipipe-insight-data / -information / -knowledge /
-wisdom) write entries that conform to this schema. The loading strategy
(see `insight-context-loading.md`) depends on this shape being stable.


Universal frontmatter (every entry, every layer)
=================================================

```yaml
---
id:        <Layer><NN>                # e.g. D01, I02, K03, W01
layer:     D | I | K | W
tags:      [<list of cross-cutting topics>]
status:    active | stale | superseded
created:   YYYY-MM-DD                  # date only, not timestamp
updated:   YYYY-MM-DD

# (Layer-specific fields go HERE — see per-layer sections below)

sources:   [<entries this derives from>]   # machine-traversable
ref_by:    [<entries that cite this>]      # auto-maintained
---
```

Conventions:
  - `id` letter matches layer: D=Data, I=Information, K=Knowledge, W=Wisdom
  - `tags` is a list, lowercase snake_case (e.g. `[film, conditioning, val]`)
  - `status` enum strict; default = `active`
  - `sources` and `ref_by` use bare IDs (e.g. `[D01, D03]`), NOT prose
  - Frontmatter total length target: ≤ 13 lines


Layer-specific frontmatter additions
======================================

D layer (Data)
-----------------------

```yaml
source_id: <task-id|exp-id>            # WHERE this observation came from
                                       # task id (e.g. T1, "regression_v2") for
                                       # C_task-sourced D cards
                                       # probe source ref (e.g. P.A07) for
                                       # D_probe-sourced D cards (rare)
headline:  "<one-line number summary>" # e.g. "val: FiLM Δ -0.98 ± 0.27 mg/dL (p=0.018, n=3)"
```

`headline` is the quick-load summary; specific numbers go in body's
`## Numbers` table.

Note on `source_id`: D and I cards almost always come from C_task
results (a regression / display / individual-query task). The legacy
`exp_id` field name implied D came from probes — that was the
old model. New model: D + I = C_task lens, K + W = D_probe lens.
For continuity, `exp_id` is accepted as a deprecated alias for
`source_id` when present; new cards should use `source_id`.


I layer (Information)
-------------------

```yaml
pattern:   statistical_regularity | repeated_effect | paired_contrast | null_finding
n_obs:     <int>                        # number of D entries supporting
direction: positive | negative | mixed | null
```


K layer (Knowledge)
--------------------

```yaml
claim:      "<one-sentence belief>"
confidence: high | medium | low | contested
```

`claim` is THE belief in one line. Detail and scope go in body sections.


W layer (Wisdom)
-----------------

```yaml
rec:       "<one-sentence action>"
type:      next_experiment | research_pivot | stop_doing | paper_direction
cost:      cheap | medium | expensive
```

`rec` is THE action in one line. Detail goes in body.


Body sections (per layer, in this order)
=========================================

D layer
--------

```markdown
# D{NN}: <one-line title>

## Observation
<1-2 paragraphs of FACTS only — no interpretation>

## Numbers
| Metric                                | Value              | CI (95%)                        | Source                         |
|---------------------------------------|--------------------|---------------------------------|--------------------------------|
| ...                                   | ...                | ...                             | ...                            |

## Caveats
- <bulleted, verbatim from probe.yaml caveats[]>
```

Table formatting: use padded fixed-width columns so all D cards render as a clean grid. Column headers are `Metric` (40 chars), `Value` (20 chars), `CI (95%)` (33 chars), `Source` (32 chars). Pad every cell to its column width with trailing spaces. Use `—` for missing CI values, not `--`.

Length budget: 30-50 body lines.


I layer
--------

```markdown
# I{NN}: <one-line title>

## Pattern statement
<the invariant in 1-3 sentences>

## Evidence
| Source | Metric / Split                 | Δ or Value         | Direction  |
|--------|--------------------------------|--------------------|------------|
| D01    | ...                            | ...                | ...        |

## Counter-evidence
<entries that should show the pattern but don't, OR "none found" with rationale>
```

Table formatting: use padded fixed-width columns consistent with D-layer tables. Column headers are `Source` (8 chars), `Metric / Split` (32 chars), `Δ or Value` (20 chars), `Direction` (12 chars).

Length budget: 30-60 body lines.


K layer
--------

```markdown
# K{NN}: <one-line title>

## Claim
<1-2 paragraphs: the belief stated fully, with scope qualification>

## Supporting evidence
- <bulleted; cite I entries with their key numbers>

## Counter-evidence
- <honestly list contradicting findings or "none found" with reason>

## Confidence rationale
<why high/medium/low/contested — be specific about what would change confidence>

## Scope
<where/when this belief holds; one paragraph>
```

Length budget: 40-80 body lines.


W layer
--------

```markdown
# W{NN}: <one-line title>

## Recommendation
<1-2 paragraphs: concrete action, sufficient detail to execute>

## How to act
<exact command / decision / next step. For triggering probes:
 the literal /haipipe-probe design new ... command.>

## Why now
<one paragraph: what makes this timely; which K entries trigger it>

## Decay condition
- <conditions under which this recommendation should be downgraded>
```

Length budget: 30-60 body lines.


Length budgets (summary)
=========================

```
Frontmatter:    10-13 lines (universal: 8, layer-specific: 2-4, sources/ref_by: 2-3)
Body:           30-80 lines depending on layer
Total entry:    ≤ 100 lines for most; never exceed 200

Skim load all entries: <frontmatter only>
  100 entries × 12 lines = 1200 lines ← fast load
```


Concrete example (W-layer)
============================

```markdown
---
id:        W01
layer:     W
tags:      [film, conditioning, next_experiment]
status:    active
created:   2026-05-23
updated:   2026-05-23

rec:       "Run param-matched FiLM re-test to isolate conditioning from scale"
type:      next_experiment
cost:      medium

sources:   [K03]
ref_by:    []
---

# W01: Param-matched FiLM re-test

## Recommendation

Scaffold a new probe with:
- baseline arm:  current arch + 5% width reduction → match FiLM params
- film_pm arm:   FiLM on the size-reduced baseline
- film_orig arm: FiLM on original arch (control)

N=3 seeds each. Eval on val / test-id / test-od.

## How to act

```
/haipipe-probe design new 12 \
    --title "Param-matched FiLM re-test" \
    --hypothesis "FiLM in-dist benefit survives param-matching"
/haipipe-probe bridge 12
```

## Why now

K03 is the strongest belief on patient-conditioning architecture, but
its scale-confound caveat blocks any clean paper claim. Resolving it
gates further FiLM work and main figure 3.

## Decay condition

- Another lab publishes a param-matched FiLM result first
- OR project pivots away from patient-feature conditioning
- OR K03 is downgraded by new contradicting evidence (I02 fails to replicate)
```


Validation rules (any layer)
=============================

  - YAML frontmatter parses (yaml.safe_load)
  - `id` letter matches `layer` (D, I, K, W)
  - `sources` field accepts:
      - D / I cards: task ids (e.g. T1, T2) — points into the
        plan's task_batch; the task's results/ folder is the
        evidence anchor
      - K / W cards: probe source refs (e.g. P.A07) — points into the
        plan's probe_batch; probe.yaml is the evidence
        anchor (status MUST be `confirmed`)
      - Strategic W cards: a list of K ids (e.g. [K01, K03, K05])
        instead of a single E; mark `type: strategic` in body
  - `ref_by` consistent: if K03 lists `ref_by: [W01]`, W01 MUST list
    `sources: [K03]` (auto-maintained)
  - No `</`-style HTML, no `[[wikilink]]` — pure standard markdown
  - Length: total file ≤ 200 lines

Loading order: see `ref/insight-context-loading.md`.
