OKF Compatibility for insight
================================

This file defines the thin compatibility layer between haipipe's
`examples/<project>/insights/` knowledge base and Open Knowledge Format
(OKF)-style bundles.

The rule is deliberate:

```
haipipe DIKW schema is authoritative.
OKF is an export / interchange view.
```

Do not weaken the D/I/K/W boundaries to fit OKF. Add just enough metadata and
links so external agents, graph viewers, and Markdown catalog tooling can read
the insight base as a generic knowledge bundle.


Why this belongs here
=====================

insight already has the same useful substrate as OKF:

- Markdown files
- YAML frontmatter
- directory-level organization
- a derived `INDEX.md`
- machine-traversable `sources` / `ref_by`

The difference is scope. OKF is a generic catalog format. insight is a
research archive with strong semantics:

```
D = observation
I = pattern
K = belief
W = action
```

The compatibility layer lets consumers see "knowledge entries" without losing
the sharper haipipe meaning.


Frontmatter additions
=====================

Every new insight card SHOULD include these OKF-facing fields in addition to
the canonical DIKW fields:

```yaml
type:        Insight Data | Insight Information | Insight Knowledge | Insight Wisdom
title:       "<short human-readable title>"
description: "<one-sentence catalog description>"
```

These fields are OKF-facing only:

- `type` maps the DIKW layer to a generic concept type.
- `title` gives a stable label independent of the Markdown H1.
- `description` gives a skim-load summary for generic catalog readers.

The layer-specific fields remain load-bearing for haipipe:

```
D: headline
I: pattern / n_obs / direction
K: claim / confidence
W: rec / rec_type / cost
```

Note the `type` collision for W cards: W already uses `type` to mean
recommendation type (`next_experiment`, `paper_direction`, ...). To preserve
backward compatibility, existing W cards may keep that field. For new cards,
use:

```yaml
type:      Insight Wisdom
rec_type:  next_experiment | research_pivot | stop_doing | paper_direction
```

Consumers MUST accept legacy W cards where `type` is the recommendation enum
and infer `okf_type = Insight Wisdom` from `layer: W`.


ID links
========

The canonical graph stays in `sources` / `ref_by` as bare IDs:

```yaml
sources: [D01, D03]
ref_by:  [I02]
```

The OKF export resolves these IDs to Markdown links in the exported files and
to node/edge records in `graph.json`. Do not replace the canonical bare IDs in
source cards with Markdown links; bare IDs are easier for haipipe tools to
audit and rewrite.


Export command
==============

The orchestrator supports:

```bash
/haipipe-insight export-okf [project-path]
```

Implementation:

```bash
python3 plugins/haipipe-toolkit/skills/insight/scripts/export_okf.py \
  examples/<project>
```

Default output:

```text
examples/<project>/insights/okf/
├── index.md
├── graph.json
├── D_data/
├── I_information/
├── K_knowledge/
└── W_wisdom/
```

The export is derived state. It can be deleted and rebuilt. Source of truth
remains the original cards under `D_data/`, `I_information/`, `K_knowledge/`,
and `W_wisdom/`.


Validation level
================

`export-okf` is intentionally tolerant:

- If `title` is missing, infer it from the Markdown H1 or filename.
- If `description` is missing, infer it from the layer key field:
  `headline`, `pattern`, `claim`, or `rec`.
- If `type` is missing, infer it from `layer`.
- If a source/ref target is dangling, emit a warning and keep the raw ID.

The stricter gate remains `index-integrity-auditor-agent`.
