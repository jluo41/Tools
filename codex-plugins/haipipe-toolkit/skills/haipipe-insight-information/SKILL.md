---
name: haipipe-insight-information
description: "I-level patterns specialist of the haipipe-insight family. Reads a dataset's D_data profile + its in-sample results and files ONE in-sample pattern (an association/direction/magnitude/shape) WITHIN that one named dataset into insights/I_information/. NO code execution — pure markdown synthesis. NO p-value / CI (those are generalization → K). Use via /haipipe-insight review/apply, /haipipe-application ask, or directly /haipipe-insight-information. Trigger: I-level, in-sample pattern, what pattern is in this dataset."
argument-hint: "[--project <path>] [--dataset <name>] [--id I<NN>] [--scope <D-ids>] [--slug <slug>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-22"
  summary: "I-level in-sample-pattern specialist of the haipipe-insight family."
  changelog:
    - "2.0.0 (2026-06-22): recut to the in-sample model (JL). I = a pattern INSIDE ONE named dataset, cites that dataset's D (no >=2-D gate), carries no p/CI. Cross-dataset regularities now belong to K (robust generalization)."
    - "1.1.0 (2026-06-20): clarified cross-D granularity; one reusable pattern per card."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-insight-information
================================

I-level of the Insight base (D → I → K → W). Files ONE **in-sample pattern**: an
association / direction / magnitude / shape found WITHIN one named dataset. It
reads that dataset's `D_data/D*.md` profile and the in-sample result (the model
estimate), and states the pattern descriptively. It does NOT claim the pattern
generalizes — that leap, with its p-value / CI / confidence, is a K.
Each I card holds ONE reusable pattern for ONE dataset. If a candidate is a whole
topic summary, split it; if it duplicates an active I card, merge evidence
instead (see `../../ref/card-granularity.md`).

**Invocation modes** (see `../../ref/invocation-modes.md`): interactive (a
human steers; the triage ASK runs) OR headless (`--dataset` + the D id(s) +
`--auto` → file silently), chosen by input completeness.
`card-creator-information-agent` calls this skill headless during fan-out; agent
+ no dataset / no D for it → `status: blocked` (never hang). End with the
structured return block.

```
D — Data:         "what one dataset looks like"     (input)
I — Information:  "the pattern inside that dataset"  ← THIS SKILL
K — Knowledge:    "does it generalize, + confidence"
W — Wisdom:       "what to do, tuned to confidence"
```


Input
-----

```
examples/<project>/insights/D_data/D*.md   (REQUIRED: the D card(s) for ONE dataset)
the in-sample result for that dataset       (the model estimate / direction; read-only)
```


Output
------

```
examples/<project>/insights/I_information/I{NN}_<slug>.md
```


Hard rules
----------

- NO Python execution. The in-sample pattern is extracted by **reading** the
  dataset's D profile and the model estimate — not by running statistics.
- NO p-value, NO CI, NO confidence on an I card. The estimate / direction /
  magnitude / shape are descriptive of THIS sample. The moment a claim asserts
  the pattern holds beyond the sample, it is a K, not an I.
- The I card NAMES its dataset (`dataset:`) and cites the D card(s) profiling that
  same dataset. It does NOT need ≥2 D — one dataset, its profile, its pattern.
- A cross-dataset regularity (the same pattern recurring across cohorts) is NOT an
  I; it is robust generalization and belongs to a K. Do not file it here.
- A card holds one reusable pattern for one dataset. Broad summaries split;
  reinforcing evidence for an existing pattern merges.


Workflow
--------

```
Step 1: Parse args
  - --project <path>          optional, else cwd-inferred
  - --scope <D01,D02,...>     optional; restrict to specific D entries
  - --slug <slug>             optional, descriptive name for the pattern

Step 2: Resolve paths
  - project root              from arg or cwd
  - d_dir                     examples/<project>/insights/D_data/
  - i_dir                     examples/<project>/insights/I_information/

Step 3: Read the dataset's D + in-sample result
  - Read the D card(s) profiling the target dataset
  - Read the in-sample estimate (coefficient / direction / magnitude / shape)
  - State the pattern descriptively for THIS dataset (no p/CI)

Step 4: Triage patterns (interactive default; --auto skips ASK)
  - Present candidate patterns ranked by evidence-strength
  - User picks which to materialize (or --slug forces one)

Step 5: Pick output NN
  - If `--id I<NN>` was passed, USE IT verbatim (apply pre-assigns ids for
    parallel safety). Otherwise NN = max existing + 1 (serial writes only).

Step 6: Compose entry (markdown only)
  - Per the entry schema below

Step 7: Write
  - insights/I_information/I{NN}_<slug>.md (atomic)
  - Update insights/INDEX.md
  - Back-link: append "linked patterns: I{NN}" to each cited D entry's
    Cross-references section
```


Entry schema
------------

Canonical schema: **`../../ref/insight-md-schema.md`** (see "I layer" section).

Quick reminder for I entries:

```
frontmatter (≤ 16 lines):
  id, type=Insight Information, layer=I, title, description,
  tags, status, created, updated,
  dataset, pattern, direction,
  sources, ref_by

body sections (in order):
  ## Pattern statement   (1-3 sentences: the in-sample pattern in THIS dataset)
  ## Evidence            (table: Source / Metric / Δ or Value / Direction — NO p/CI)
  ## Counter-evidence    (in-sample null/reversed cases; "none found" + reason if so)

length: ≤ 120 lines total
```

The `pattern` enum is one of: `statistical_regularity | repeated_effect
| paired_contrast | null_finding`. `direction` is the in-sample direction within
the named dataset.


Definition of done
-------------------

- [ ] `insights/I_information/I{NN}_<slug>.md` written, non-empty
- [ ] `dataset:` present; cites the D card(s) for that same dataset
- [ ] Evidence table is in-sample (estimate / direction); NO p-value / CI / confidence
- [ ] Non-confirming evidence section honestly populated (or "none found"
      stated explicitly with rationale)
- [ ] `## Change log` records creation source or meaningful update
- [ ] NO Python file written, NO script executed
- [ ] Back-link added to each cited D entry's Cross-references section
- [ ] `insights/INDEX.md` updated


Disambiguation
---------------

- no D card for the target dataset → REFUSE; suggest running
  /haipipe-insight-data to profile the dataset first
- the claim asserts the pattern holds beyond the sample (has a p-value / CI /
  confidence) → that is a K, not an I; route to /haipipe-insight-knowledge
- new statistical computation needed → STOP; recommend task eval
  scaffolding


Risk profile
-------------

WRITES one new file under `insights/I_information/`. APPENDS to
`insights/INDEX.md`. APPENDS one back-link line to each cited D entry.
Read-only on probes/ and tasks/.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "I02_<slug> written for dataset <name> from [D01]"
artifacts: [insights/I_information/I{NN}_<slug>.md, insights/INDEX.md,
            <back-linked D entries>]
next:      /haipipe-insight-knowledge to ask whether this pattern generalizes (→ K + confidence)
```
