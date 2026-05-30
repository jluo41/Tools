---
name: haipipe-insight-data
description: "D-level observations specialist of the haipipe-insight family. Reads CONFIRMED probe claims from D_probe and synthesizes markdown observation entries into insights/D_data/. NO code execution — pure markdown synthesis. Use when running D-phase via /haipipe-application ask, or directly /haipipe-insight-data <probe-id>. Trigger: D-level, observations, what did we observe, raw findings from probes."
argument-hint: "[experiment_id] [--project <path>] [--slug <slug>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-insight-data
====================================

D-level of the Insight base (D → I → K → W). Reads CONFIRMED probe
claims and writes markdown observation entries.

```
D — Data:         "what we observed"          ← THIS SKILL
I — Information:      "what patterns emerged across observations"
K — Knowledge:    "what we now believe is true"
W — Wisdom:       "what we should do next"
```

This is the **boundary that distinguishes E_insight from C_task**:

```
C_task        EXECUTES (Python, metrics, GPU, run.sh)
E_insight     SYNTHESIZES (markdown, reads existing artifacts, NO code)
```


Input
-----

```
examples/<project>/probes/<NN>_<slug>/probe.yaml          (REQUIRED)
examples/<project>/probes/<NN>_<slug>/CLAIMS_FROM_RESULTS.md   (if any)
examples/<project>/probes/<NN>_<slug>/INTEGRITY_AUDIT.md       (if any)
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
- Pure markdown synthesis from already-existing probe artifacts.
- Numbers cited must reference exact source: probe ID + metric key.
- If a number requires NEW computation, that belongs in C_task — invoke
  `/haipipe-task task-folder eval` to scaffold an evaluation task. Never
  compute inline here.
- Source probe MUST have `result.status == confirmed`. Pending /
  inconclusive / refuted are refused.


Workflow
--------

```
Step 1: Parse args
  - <experiment_id>     required (e.g. 02 or 02_lhm_vs_baseline)
  - --project <path>    optional, else cwd-inferred
  - --slug <slug>       optional, else derived from probe title

Step 2: Resolve paths
  - project root        from arg or cwd
  - experiment_dir      examples/<project>/probes/<NN>_<slug>/
  - insight_dir         examples/<project>/insights/D_data/

Step 3: Validate source
  - Read probe.yaml
  - Refuse if result.status != confirmed (report which status it has)
  - Note presence of CLAIMS_FROM_RESULTS.md and INTEGRITY_AUDIT.md

Step 4: Pick output NN
  - List existing insights/D_data/D*.md
  - NN = max existing + 1 (zero-padded to 2 digits)

Step 5: Compose entry (markdown, no Python)
  - Read probe.yaml hypothesis / claim / result fields
  - Optionally read 1-3 linked run-paths' metrics.json (read-only) for
    exact number quotes
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
frontmatter (≤ 13 lines):
  id, layer=D, tags, status, created, updated,
  exp_id, headline,
  sources, ref_by

body sections (in order):
  ## Observation     (1-2 paragraphs, FACTS only — no interpretation)
  ## Numbers         (table: Metric / Value / Split / Source)
  ## Caveats         (bullet list, verbatim from probe.yaml caveats[])

length: ≤ 100 lines total
```

The `headline` field in frontmatter is the one-line number summary
(e.g. `"val: FiLM Δ -0.98 ± 0.27 mg/dL (p=0.018, n=3)"`); detailed
numbers go in the `## Numbers` table body section.


Definition of done
-------------------

- [ ] `insights/D_data/D{NN}_<slug>.md` written, non-empty
- [ ] Every cited number traceable to probe.yaml or a specific
      metrics.json key (no fabricated numbers)
- [ ] No interpretive claims (those are I / K level)
- [ ] `caveats` section non-empty if source probe had caveats
- [ ] NO Python file written, NO script executed
- [ ] `insights/INDEX.md` updated with the new entry's one-line stub


Disambiguation
---------------

- experiment_id ambiguous (multiple matches) → ASK, list candidates
- source probe.result.status != confirmed → REFUSE; report status;
  suggest waiting or using a sibling skill once promoted to confirmed
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
summary:   "D03_<slug> written from probe <NN>_<slug>"
artifacts: [insights/D_data/D{NN}_<slug>.md, insights/INDEX.md]
next:      /haipipe-insight-information to extract cross-observation patterns
```
