---
name: haipipe-insight-data
description: "D-level observations specialist of the haipipe-insight family. Reads CONFIRMED probe claims from probe and synthesizes markdown observation entries into insights/D_data/. NO code execution — pure markdown synthesis. Use when running D-phase via /haipipe-application ask, or directly /haipipe-insight-data <probe-ref>. Trigger: D-level, observations, what did we observe, raw findings from probes."
argument-hint: "[probe_ref] [--project <path>] [--slug <slug>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
  summary: "D-level observations specialist of the haipipe-insight family."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-insight-data
====================================

D-level of the Insight base (D → I → K → W). Reads CONFIRMED probe
claims and writes markdown observation entries.

**Invocation modes** (see `../../ref/invocation-modes.md`): interactive (a
human steers; a missing/ambiguous `probe_ref` gets ASKed) OR headless (a full
spec → file the card silently, no ASK), chosen by input completeness.
`card-creator-data-agent` calls this skill headless during fan-out; agent +
missing/unconfirmed source → `status: blocked` (never hang). End with the
structured return block.

```
D — Data:         "what we observed"          ← THIS SKILL
I — Information:      "what patterns emerged across observations"
K — Knowledge:    "what we now believe is true"
W — Wisdom:       "what we should do next"
```

This is the **boundary that distinguishes insight from task**:

```
task        EXECUTES (Python, metrics, GPU, run.sh)
insight     SYNTHESIZES (markdown, reads existing artifacts, NO code)
```


Input
-----

```
examples/<project>/probes/<GROUP>_<group_slug>/<NN>_<slug>/probe.yaml          (REQUIRED)
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
- Pure markdown synthesis from already-existing probe artifacts.
- Numbers cited must reference exact source: probe ID + metric key.
- If a number requires NEW computation, that belongs in task — invoke
  `/haipipe-task task-folder eval` to scaffold an evaluation task. Never
  compute inline here.
- Source probe MUST have `result.status` in {confirmed, refuted, inconclusive}.
  Only `pending` / `exploratory` are refused (no settled run). A `refuted` or
  `inconclusive` probe is a controlled comparison with real numbers → a valid D
  observation. An inconclusive D MUST set frontmatter `verdict: inconclusive`
  and its headline must state the null (e.g. "Δ … CI straddles 0") so a reader
  never mistakes a null for an effect.


Workflow
--------

```
Step 1: Parse args
  - <probe_ref>         required (e.g. P.A01, A01, or A/01_lhm_vs_baseline)
  - --project <path>    optional, else cwd-inferred
  - --slug <slug>       optional, else derived from probe title

Step 2: Resolve paths
  - project root        from arg or cwd
  - probe_dir           examples/<project>/probes/<GROUP>_<group_slug>/<NN>_<slug>/
  - insight_dir         examples/<project>/insights/D_data/

Step 3: Validate source
  - Read probe.yaml
  - Accept result.status in {confirmed, refuted, inconclusive}; refuse only
    pending / exploratory (report which status it has). Inconclusive D cards
    must carry `verdict: inconclusive` + a null-stating headline.
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
frontmatter (≤ 16 lines):
  id, type=Insight Data, layer=D, title, description,
  tags, status, created, updated,
  source_id, headline,
  sources, ref_by

body sections (in order):
  ## Observation     (1-2 paragraphs, FACTS only — no interpretation)
  ## Numbers         (padded fixed-width table — see below)
  ## Caveats         (bullet list, verbatim from probe.yaml caveats[])

length: ≤ 100 lines total
```

Numbers table MUST use padded fixed-width columns for visual consistency across all D cards:

```
| Metric                                | Value              | CI (95%)                        | Source                         |
|---------------------------------------|--------------------|---------------------------------|--------------------------------|
| <40 chars padded>                     | <20 chars padded>  | <33 chars padded>               | <32 chars padded>              |
```

Use `—` (em-dash) for missing CI values, not `--`. Column headers: Metric (40), Value (20), CI (33), Source (32).

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

- probe_ref ambiguous (multiple matches) → ASK, list candidates
- source probe.result.status is pending / exploratory → REFUSE; report status;
  suggest waiting for a settled run. confirmed / refuted / inconclusive are all
  accepted (inconclusive files a `verdict: inconclusive` D card).
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
summary:   "D03_<slug> written from probe P.A01"
artifacts: [insights/D_data/D{NN}_<slug>.md, insights/INDEX.md]
next:      /haipipe-insight-information to extract cross-observation patterns
```
