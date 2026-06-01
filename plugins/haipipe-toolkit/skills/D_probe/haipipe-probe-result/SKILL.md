---
name: haipipe-probe-result
description: "Post-run specialist of haipipe-probe. Aggregates linked-run results into mean/std/paired-t/sign-test, writes claim sentence with caveats, and renders the project-level probe-log.txt comparison table. Called by /haipipe-probe orchestrator. Direct invocation works for result-scoped work."
argument-hint: "[aggregate|claim|render] [probe_ref]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.2.0"
  last_updated: "2026-06-01"
  summary: "Post-run specialist of haipipe-probe."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-06-01): update probe path examples and glob rules for active/archive `MM-NN_slug` layout."
    - "1.2.0 (2026-06-01): switch probe folder + ref examples to date-based `MMDD` / `P.MMDD`."
---

Skill: haipipe-probe-result
=================================

Owns the POST-RUN half: read linked runs' results, compute statistics,
write claim, render the project comparison table.


Commands
--------

```
/haipipe-probe result aggregate <probe>
  Read arms' runtime.yaml + metrics.json. Compute aggregation per spec.
  Fill the `result:` block in probes/<MMDD>_<slug>/probe.yaml.

/haipipe-probe result claim <probe>
  Read filled `result:` + `caveats:`. LLM writes final claim sentence
  into probes/<MMDD>_<slug>/probe.yaml `claim:` field.

/haipipe-probe result render [project-path]
  Render all active probes/*/probe.yaml plus archived
  probes/*-archive/*/probe.yaml into diagram/probe-log.txt
  (comparison-centric scoreboard).
```


Workflow — `aggregate`
-----------------------

```
Step 1: Resolve and load probes/<MMDD>_<slug>/probe.yaml. Refuse if arms are empty.

Step 2: For each arm, for each linked run-path in arms.<arm>.runs:
  - Read <run-path>/results/<NAME>/runtime.yaml; require status=ok.
  - Read <run-path>/results/<NAME>/{metrics,summary,aggregated}.json.
  - Extract metric value matching aggregation.metric.
  - Collect array of metric values per arm.

Step 3: Compute statistics per aggregation.statistic:
  - mean_std: per-arm mean ± std
  - mean_std_paired_t: + paired-t between baseline and treatment arms
                       (require equal N, sort by seed for pairing)
  - sign_test: count of seeds where Δ has the same sign

Step 4: Determine status:
  - confirmed: p < 0.05 AND Δ in claim direction
  - inconclusive: p >= 0.05 OR Δ small (<0.5 noise floor)
  - refuted: Δ in OPPOSITE direction with p < 0.05
  - pending: missing data (insufficient runs / failed runs)

Step 5: Write result: block in probe.yaml (atomic).
        Set status field.

Step 6: Emit tail; suggest /result claim <probe> as next.
```


Workflow — `claim`
-------------------

```
Step 1: Resolve and load probe.yaml. Require result.status != pending.

Step 2: Run the caveats checklist
        (see ../ref/probe-caveats-checklist.txt):
  For each YES item, ensure it's in caveats: list.
  Halt if any unchecked.

Step 3: LLM composes claim sentence from:
  - claim_target (intended)
  - result (actual numbers)
  - caveats (modifiers / qualifiers)

  Format:
  ```
  <Treatment> <direction> <baseline> by <Δ ± std> on <metric/split>
  (statistical: <test> p=<X>, N=<seeds>). <caveat headline>.
  ```

Step 4: Write claim: field in probe.yaml.

Step 5: Emit tail.
```


Workflow — `render`
--------------------

```
Step 1: Resolve project root.
Step 2: Glob active probes/*/probe.yaml and archived probes/*-archive/*/probe.yaml.
Step 3: For each, format into the per-entry template
        (../ref/probe-entry-template.txt).
Step 4: Build the headline scoreboard (best per split per category).
Step 5: Compile the Caveats section (aggregate across probes).
Step 6: Write diagram/probe-log.txt (atomic; preserve manual
        "Where artifacts live" section if present).
```


Claim sentence — examples (template-good)
------------------------------------------

```
✅ LHM-A beats baseline by 0.68 ± 0.27 MAE on test-id
   (paired-t p=0.018, N=3 seeds; sign 3/3). Confound: +20% params.

⚠️ Event-channel arch yields no measurable Δ vs baseline on test-id
   (Δ=+0.05 ± 0.30 MAE; p=0.71; N=3). Treat as null.

❓ Single-seed transformer beats baseline by 0.4 MAE on test-id;
   need N≥3 paired runs to confirm.
```


Disambiguation
---------------

  - aggregate before any runs are ok → refuse, report missing/failed runs
  - claim before aggregate → refuse; redirect
  - render with no probes → empty file with a "no probes yet" note


Risk profile
-------------

EDITS probes/<MMDD>_<slug>/probe.yaml (fills result: + claim:). WRITES
diagram/probe-log.txt (project-level). Does NOT touch tasks/ or runs/.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "P.0601 framing_loss-aversion aggregated: Δ=-0.68 p=0.018, status=confirmed"
artifacts: [probes/0601_framing_loss-aversion/probe.yaml, probes/comparison.md]
next:      /haipipe-probe review P.0601
```
