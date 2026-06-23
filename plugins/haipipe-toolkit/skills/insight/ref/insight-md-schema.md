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
type:      Insight Data | Insight Information | Insight Knowledge | Insight Wisdom
layer:     D | I | K | W
title:     "<short title for generic catalog readers>"
description: "<one-sentence OKF/catalog summary>"
tags:      [<list of cross-cutting topics>]
status:    active | stale | superseded | contested | acted_on
created:   YYYY-MM-DD                  # date only, not timestamp
updated:   YYYY-MM-DD

# (Layer-specific fields go HERE — see per-layer sections below)

sources:   [<internal card ids or external source refs>]   # machine-traversable
ref_by:    [<internal card ids or external caller refs>]   # auto-maintained

# Optional lifecycle fields:
# supersedes: [K02]
# superseded_by: K09
# merged_from: [task:T.A01.04, probe:P.0701_param_matched]
---
```

Conventions:
  - `id` letter matches layer: D=Data, I=Information, K=Knowledge, W=Wisdom
  - `type`, `title`, and `description` make the card OKF-compatible; they do
    not replace the layer-specific fields below
  - `tags` is a list, lowercase snake_case (e.g. `[film, conditioning, val]`)
  - `status` enum strict; default = `active`
  - `sources` and `ref_by` use structured refs, NOT prose
    - internal insight refs are bare IDs: `D01`, `I02`, `K03`, `W01`
    - external refs are namespaced: `task:T.A01.02`, `probe:P.0619_film_ood`,
      `lit:smith2024`, `discover:Dsc.03`, `narrative:N01.C2`, `app:ask:03`
  - Frontmatter total length target: ≤ 16 lines
  - Lifecycle fields are optional; use them only when status/evidence history
    requires machine-readable routing


Layer-specific frontmatter additions
======================================

D layer (Data) — describes ONE dataset
-----------------------

```yaml
dataset:   <dataset-name>              # REQUIRED. The dataset this D describes
                                       # e.g. VisitOsteo_1stPair_af14d
source_id: <source-ref>                # WHERE the profile came from
                                       # task:T.A01.02 for task-sourced D
                                       # lit:smith2024 for literature-sourced D
                                       # probe:P.A07 for probe-sourced D
headline:  "<one-line dataset profile>"  # e.g. "VisitOsteo 1st-pair: N=1.2M, 2015-2020 Medicare"
```

`dataset:` is required — a D card is a statement ABOUT one named dataset.
Naming convention: a single stable token, snake/Pascal joined by underscores,
specific enough that the I card for the same dataset reuses it VERBATIM (the
D↔I `dataset:` match depends on exact string equality). Include the
distinguishing facets the project slices on, e.g. `VisitOsteo_1stPair_af14d`
(cohort + sample + window). Do not write a prose phrase ("VisitOsteo 1stPair");
normalize to the token form.
`headline` is the quick-load profile; counts/shares go in the body `## Numbers`
table. D carries NO p-value, NO CI, NO significance: those are descriptions of
generalization and live at K (see `dikw-boundaries.md`).

Note on `source_id`: D cards cite the source artifact that produced the
profile. The legacy `exp_id` field name implied D came only from probes; that
was the old model. Current model: D/I describe one named dataset (in-sample),
while K records whether the pattern generalizes and W acts on it. For continuity,
`exp_id` is accepted as a deprecated alias for `source_id`; new cards use a
namespaced `source_id`.


I layer (Information) — a pattern IN one dataset
-------------------

```yaml
dataset:   <dataset-name>              # REQUIRED. Same dataset as the D it cites
pattern:   statistical_regularity | repeated_effect | paired_contrast | null_finding
direction: positive | negative | mixed | null
```

`dataset:` is required and must match the D card(s) in `sources:`. An I card is
an in-sample pattern within ONE dataset. It carries the estimate / direction /
magnitude / shape, but NO p-value, NO CI, NO confidence level — the moment a
claim asserts the pattern holds beyond the sample it is a K, not an I.


K layer (Knowledge) — does the pattern generalize
--------------------

```yaml
claim:      "<one-sentence generalization claim>"
confidence: high | medium | low | contested   # REQUIRED — strength of GENERALIZATION
claim_type: associational | causal            # REQUIRED — is it a causal claim?
```

`claim` is THE generalization belief in one line. K carries TWO orthogonal
qualifiers (do not conflate them):

- `confidence` (the GENERALIZATION axis): how sure are we the pattern holds beyond
  the sample. ALWAYS present (high/medium/low/contested); a low-confidence or
  negative ("does not generalize") K is still recorded.
- `claim_type` (the CAUSAL axis): is this a causal claim or only an association.
  Default `associational`. `causal` is allowed ONLY when the body
  `## Generalization basis` names a valid identification strategy (RCT, a strong/
  valid instrument, RDD, DiD with the parallel-trends check, etc.). A significant
  coefficient with a WEAK or invalid instrument stays `associational` — weak-IV is
  not identification. A high generalization `confidence` does NOT make a claim
  causal; the two axes are independent.

K has NO admission gate: it needs a generalization basis (the inferential
evidence: p / CI / robustness across subgroups, or a vetted external claim), not
a probe. The p-value / CI / significance / confidence appear HERE, in the body
`## Generalization basis`, never in D or I. Detail and scope go in body sections.


W layer (Wisdom) — act, tuned to K confidence
-----------------

```yaml
rec:       "<one-sentence action>"
rec_type:  next_experiment | research_pivot | stop_doing | paper_direction
cost:      cheap | medium | expensive
```

`rec` is THE action in one line. The body records which K it acts on, that K's
confidence at the time, and why that confidence justifies this risk posture
(bold for high-confidence K, conservative/hedged for low). Detail goes in body.

Legacy note: older W cards may use `type:` for the recommendation enum. New
cards should use `type: Insight Wisdom` plus `rec_type:` so the card remains
OKF-compatible while preserving the recommendation subtype.


Body sections (per layer, in this order)
=========================================

D layer
--------

```markdown
# D{NN}: <one-line dataset-profile title>

## Profile
<1-2 paragraphs of FACTS about the dataset — composition, how it was built — no interpretation, no inference>

## Numbers
| Metric                                | Value              | Source                         |
|---------------------------------------|--------------------|--------------------------------|
| ...                                   | ...                | ...                            |

## Caveats
- <bulleted, verbatim from the source caveats[]>

## Change log
- <YYYY-MM-DD> — created from <source-ref>.
```

The D `## Numbers` table holds DESCRIPTIVE quantities of the dataset only (counts,
shares, sizes, coverage). NO p-value, NO CI, NO significance — those are
generalization quantities and belong to K.

Table formatting: use padded fixed-width columns so all D cards render as a clean grid. Column headers are `Metric` (40 chars), `Value` (20 chars), `Source` (32 chars). Pad every cell to its column width with trailing spaces.

Length budget: 30-50 body lines.


I layer
--------

```markdown
# I{NN}: <one-line title>

## Pattern statement
<the in-sample regularity in 1-3 sentences; THIS dataset only>

## Evidence
| Source | Metric / Split                 | Δ or Value         | Direction  |
|--------|--------------------------------|--------------------|------------|
| D01    | ...                            | ...                | ...        |

## Counter-evidence
<in-sample entries that should show the pattern but don't, OR "none found" with rationale>

## Change log
- <YYYY-MM-DD> — created from <D ids>.
```

The I `## Evidence` table holds the in-sample estimate / direction / magnitude only. NO p-value, NO CI, NO confidence — asserting the pattern holds beyond the sample is a K. Table formatting: padded fixed-width columns consistent with D-layer tables. Column headers are `Source` (8 chars), `Metric / Split` (32 chars), `Δ or Value` (20 chars), `Direction` (12 chars).

Length budget: 30-60 body lines.


K layer
--------

```markdown
# K{NN}: <one-line generalization claim>

## Claim
<1-2 paragraphs: does the in-sample pattern hold beyond the sample? state it fully, with scope>

## Generalization basis
- <the inferential evidence that lets this generalize: p-value / CI / significance,
   AND any robustness across subgroups/cohorts/time. p and CI appear HERE, not in I.>
- <cite the I entries whose pattern is being generalized>

## Counter-evidence
- <honestly list contradicting findings or "none found" with reason>

## Confidence rationale
<why high/medium/low/contested — statistical-only (weaker) vs robust-across-subgroups
 (stronger); be specific about what would change confidence>

## Scope
<where/when this belief holds; one paragraph>

## Change log
- <YYYY-MM-DD> — created from <source-ref>.
- <YYYY-MM-DD> — merged <source-ref>; confidence changed <old> -> <new>.
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
 the literal /haipipe-probe plan new ... command.>

## Risk posture
<which K this acts on, that K's confidence at the time, and WHY that confidence
 justifies this boldness: high-confidence K → bold; low-confidence K →
 conservative / hedged / "do not yet do X" / gather more first. This is the
 provenance that lets a later reader audit the decision.>

## Why now
<one paragraph: what makes this timely; which K entries trigger it>

## Decay condition
- <conditions under which this recommendation should be downgraded>

## Change log
- <YYYY-MM-DD> — created from <K ids>.
```

Length budget: 30-60 body lines.


Length budgets (summary)
=========================

```
Frontmatter:    13-16 lines (universal: 11, layer-specific: 2-4, sources/ref_by: 2-3)
Body:           30-80 lines depending on layer
Total entry:    ≤ 100 lines for most; never exceed 200

Skim load all entries: <frontmatter only>
  100 entries × 16 lines = 1600 lines ← fast load
```


Concrete example (W-layer)
============================

```markdown
---
id:        W01
type:      Insight Wisdom
layer:     W
title:     "Param-matched FiLM re-test"
description: "Action recommendation to isolate FiLM conditioning from scale."
tags:      [film, conditioning, next_experiment]
status:    active
created:   2026-05-23
updated:   2026-05-23

rec:       "Run param-matched FiLM re-test to isolate conditioning from scale"
rec_type:  next_experiment
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
  - `sources` field accepts structured refs only:
      - internal insight card ids: D01, I02, K03, W01
      - external source refs: task:T.A01.02, probe:P.A07,
        discover:Dsc.03, lit:smith2024, narrative:N01.C2, app:ask:03
  - D cards name a `dataset:` and cite one settled source via `source_id`;
    descriptive only (no p-value / CI / significance)
  - I cards name a `dataset:` matching their cited D card(s); in-sample pattern
    only (no p-value / CI / confidence)
  - K cards state a generalization claim with an explicit `confidence` (high /
    medium / low / contested, never omitted), cite the I card(s) they generalize,
    and give a generalization basis (p / CI / robustness, or a vetted external
    claim) in the body. NO probe is required. Negative / low-confidence K are valid.
  - W cards cite >=1 K card and record the risk posture justified by that K's
    confidence
  - `ref_by` consistent: if K03 lists `ref_by: [W01]`, W01 MUST list
    `sources: [K03]` (auto-maintained)
  - Lifecycle conforms to `ref/card-lifecycle.md`:
      - same reusable unit + new evidence should merge/update, not duplicate
      - superseded cards stay in place and link to replacements
      - meaningful updates append `## Change log`
  - Granularity conforms to `ref/card-granularity.md`:
      - one card = one reusable knowledge unit
      - not a raw row / seed / log line
      - not a whole report / full topic / multi-claim essay
      - duplicate evidence should merge into an existing card
  - No `</`-style HTML, no `[[wikilink]]` — pure standard markdown
  - Length: target ≤ 160 lines; absolute max ≤ 200 lines

Loading order: see `ref/insight-context-loading.md`.
