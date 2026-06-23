---
name: haipipe-insight-data
description: "D-level dataset-profile writer API of the haipipe-insight family. Files one named dataset's profile (what the dataset looks like: size, structure, composition, coverage) into insights/D_data/ from a approved by review task/probe/discover/lit source. NO code execution — pure markdown synthesis. NO p-value / CI (those are generalization → K). Prefer /haipipe-insight review; call this directly only with a complete source spec."
argument-hint: "[source_ref] [--dataset <name>] [--id D<NN>] [--project <path>] [--slug <slug>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-22"
  summary: "D-level dataset-profile writer API of the haipipe-insight family."
  changelog:
    - "2.0.0 (2026-06-22): recut to the in-sample model (JL). D = ONE named dataset's profile (require `dataset:`, no p/CI). A null/ns finding is no longer an 'inconclusive D' — it is a K (does not generalize)."
    - "1.1.0 (2026-06-20): repositioned as review-called writer API; source_ref may be task/probe/discover/lit."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-insight-data
====================================

D-level of the Insight base (D → I → K → W). Writes ONE named dataset's profile:
what the dataset looks like (size, structure, variable definitions, composition,
coverage, balance), from a approved by review, traceable source. Prefer
`/haipipe-insight review ...`; direct calls to this skill are the low-level
writer path when the caller already has a complete source spec.

**Invocation modes** (see `../../ref/invocation-modes.md`): interactive (a
human steers; a missing/ambiguous `source_ref` or `dataset` gets ASKed) OR
headless (a full spec → file the card silently, no ASK), chosen by input
completeness. Review apply or `card-creator-data-agent` calls this skill headless
during fan-out; agent + missing/unsettled source or no dataset → `status: blocked`
(never hang). End with the structured return block.

```
D — Data:         "what one dataset looks like"     ← THIS SKILL
I — Information:  "the pattern inside that dataset"
K — Knowledge:    "does it generalize, + confidence"
W — Wisdom:       "what to do, tuned to confidence"
```

This is the **boundary that distinguishes insight from task**:

```
task        EXECUTES (Python, metrics, GPU, run.sh)
insight     SYNTHESIZES (markdown, reads existing artifacts, NO code)
```


Input
-----

```
One source ref from `INSIGHT_REVIEW.yaml`, usually one of:
  task:<task-id-or-path>
  probe:<probe-id-or-path>
  discover:<note-id-or-path>
  lit:<citekey>

For probe sources:
examples/<project>/probes/<GROUP>_<group_slug>/<NN>_<slug>/probe.yaml
examples/<project>/probes/<GROUP>_<group_slug>/<NN>_<slug>/CLAIMS_FROM_RESULTS.md   (if any)
examples/<project>/probes/<GROUP>_<group_slug>/<NN>_<slug>/INTEGRITY_AUDIT.md       (if any)
examples/<project>/tasks/.../results/<run>/metrics.json             (optional;
                                                                     read for
                                                                     specific
                                                                     number
                                                                     quotes)
```


Output
------

```
examples/<project>/insights/D_data/D{NN}_<slug>.md
```

`NN` = next available 2-digit index across `D_data/`.


Hard rules
----------

- NO Python execution. NO writing `analysis.py`. NO running scripts.
- Pure markdown synthesis from already-existing source artifacts.
- D NAMES its dataset (`dataset:`) and describes only THAT dataset's profile:
  size, structure, variable definitions, composition, coverage, balance.
- NO p-value, NO CI, NO significance, NO `verdict:` on a D card. Those are
  generalization quantities and belong to K. A null / ns finding is NOT an
  "inconclusive D" — it is a K that says the pattern does NOT generalize (see
  `../../ref/dikw-boundaries.md` "Negative and uncertain K"). D stays purely the
  dataset description.
- Numbers cited (counts, shares, sizes) must reference an exact source:
  source ref + metric/table/key.
- If a number requires NEW computation, that belongs in task — invoke
  `/haipipe-task task-folder eval` to scaffold an evaluation task. Never
  compute inline here.
- The source must be settled (a task result, a probe with a settled run, a
  vetted discover/lit), traceable, and named with a namespaced `source_ref`;
  otherwise return `status: blocked`.
- D granularity is one important reusable observation, not one raw row, one
  seed, or a whole task dump. If the source only adds evidence to an existing
  D/I/K, prefer `merge` during review/apply (see
  `../../ref/card-granularity.md`).


Workflow
--------

```
Step 1: Parse args
  - <source_ref>        required (e.g. task:T.A01.02, probe:P.A01, lit:smith2024)
  - --project <path>    optional, else cwd-inferred
  - --slug <slug>       optional, else derived from source title

Step 2: Resolve paths
  - project root        from arg or cwd
  - source artifact     from source_ref namespace + review context
  - insight_dir         examples/<project>/insights/D_data/

Step 3: Validate source + resolve the dataset
  - Read the cited source artifact; identify the DATASET it profiles (set `dataset:`).
  - Accept any settled source (a task result, a probe with a settled run, a vetted
    discover/lit); refuse only unsettled sources (report the status). A null / ns
    finding is NOT recorded here — that is a K (does not generalize), not a D.
  - Check `../../ref/card-granularity.md`: block or merge if the candidate is
    too fine, too broad, or duplicates an active card.

Step 4: Pick output NN
  - If `--id D<NN>` was passed, USE IT verbatim (apply pre-assigns ids so parallel
    creators do not collide). Otherwise: NN = max existing + 1 (zero-padded). The
    auto path is safe ONLY for a single serial write, never for parallel fan-out.

Step 5: Compose entry (markdown, no Python)
  - Read the source artifact's dataset-profile fields (size, structure, composition)
  - Optionally read 1-3 linked run-paths' metrics.json (read-only) for
    exact count/share quotes (no p/CI)
  - Synthesize into the entry schema below

Step 6: Write
  - insights/D_data/D{NN}_<slug>.md (atomic write)
  - Update insights/INDEX.md (one line under D_data section)
```


Entry schema
------------

Canonical schema: **`../../ref/insight-md-schema.md`** (see "D layer" section).

Quick reminder for D entries:

```
frontmatter (≤ 16 lines):
  id, type=Insight Data, layer=D, title, description,
  tags, status, created, updated,
  dataset, source_id, headline,
  sources, ref_by

body sections (in order):
  ## Profile         (1-2 paragraphs, FACTS about the dataset — no interpretation)
  ## Numbers         (padded fixed-width table — counts/shares, NO p/CI — see below)
  ## Caveats         (bullet list, verbatim from the source where available)
  ## Change log      (created/merged/updated evidence trail)

length: ≤ 100 lines total
```

Numbers table MUST use padded fixed-width columns for visual consistency across all D cards. It holds DESCRIPTIVE quantities of the dataset only (counts, shares, sizes, coverage); NO p-value, NO CI:

```
| Metric                                | Value              | Source                         |
|---------------------------------------|--------------------|--------------------------------|
| <40 chars padded>                     | <20 chars padded>  | <32 chars padded>              |
```

Column headers: Metric (40), Value (20), Source (32).

The `headline` field in frontmatter is the one-line dataset profile
(e.g. `"VisitOsteo 1st-pair: N=1.2M encounters, 2015-2020 Medicare"`); detailed
counts go in the `## Numbers` table body section. No p-value in the headline.


Definition of done
-------------------

- [ ] `insights/D_data/D{NN}_<slug>.md` written, non-empty
- [ ] Every cited number traceable to the source artifact or a specific
      metrics/table key (no fabricated numbers)
- [ ] No interpretive claims (those are I / K level)
- [ ] `caveats` section non-empty if source probe had caveats
- [ ] `## Change log` records creation source or meaningful update
- [ ] NO Python file written, NO script executed
- [ ] `insights/INDEX.md` updated with the new entry's one-line stub


Disambiguation
---------------

- source_ref ambiguous (multiple matches) → ASK, list candidates
- source is unsettled (e.g. probe pending / exploratory, task not yet run) →
  REFUSE; report status; suggest waiting for a settled run.
- the candidate is a null / ns finding, not a dataset profile → route to
  /haipipe-insight-knowledge (it is a K: does not generalize), do not file a D
- slug collides with existing D*.md → bump NN; do not overwrite
- new computation needed → STOP; recommend
  `/haipipe-task task-folder eval` to scaffold an eval task


Risk profile
-------------

WRITES one new file under `examples/<project>/insights/D_data/`.
APPENDS one line to `insights/INDEX.md`. Read-only on everything else.
Never modifies probes/ or tasks/ contents.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "D03_<slug> dataset profile written for <dataset> from probe:P.A01"
artifacts: [insights/D_data/D{NN}_<slug>.md, insights/INDEX.md]
next:      /haipipe-insight-information to state the in-sample pattern in this dataset
```
