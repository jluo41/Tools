---
name: haipipe-experiment-result
description: "Post-run specialist of haipipe-experiment. Aggregates linked-run results into mean/std/paired-t/sign-test, writes claim sentence with caveats, and renders the project-level experiment-log.txt comparison table. Called by /haipipe-experiment orchestrator. Direct invocation works for result-scoped work."
argument-hint: [aggregate|claim|render] [experiment_id]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-experiment-result
=================================

Owns the POST-RUN half: read linked runs' results, compute statistics,
write claim, render the project comparison table.


Commands
--------

```
/haipipe-experiment result aggregate <ID>
  Read arms' runtime.yaml + metrics.json. Compute aggregation per spec.
  Fill the `result:` block in experiments/<ID>.yaml.

/haipipe-experiment result claim <ID>
  Read filled `result:` + `caveats:`. LLM writes final claim sentence
  into experiments/<ID>.yaml `claim:` field.

/haipipe-experiment result render [project-path]
  Render ALL experiments/*.yaml into diagram/experiment-log.txt
  (comparison-centric scoreboard).
```


Workflow — `aggregate`
-----------------------

```
Step 1: Load experiments/<ID>.yaml. Refuse if arms are empty.

Step 2: For each arm, for each linked run-path:
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

Step 5: Write result: block in experiments/<ID>.yaml (atomic).
        Set status field.

Step 6: Emit tail; suggest /result claim <ID> as next.
```


Workflow — `claim`
-------------------

```
Step 1: Load experiments/<ID>.yaml. Require result.status != pending.

Step 2: Run the caveats checklist
        (see ../ref/experiment-caveats-checklist.txt):
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

Step 4: Write claim: field in experiments/<ID>.yaml.

Step 5: Emit tail.
```


Workflow — `render`
--------------------

```
Step 1: Resolve project root.
Step 2: Glob experiments/*.yaml.
Step 3: For each, format into the per-entry template
        (../ref/experiment-entry-template.txt).
Step 4: Build the headline scoreboard (best per split per category).
Step 5: Compile the Caveats section (aggregate across experiments).
Step 6: Write diagram/experiment-log.txt (atomic; preserve manual
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
  - render with no experiments → empty file with a "no experiments yet" note


Risk profile
-------------

EDITS experiments/<ID>.yaml (fills result: + claim:). WRITES
diagram/experiment-log.txt (project-level). Does NOT touch tasks/ or runs/.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "02_lhm_vs_baseline aggregated: Δ=-0.68 p=0.018, status=confirmed"
artifacts: [experiments/02_lhm_vs_baseline/experiment.yaml, experiments/comparison.md]
next:      /haipipe-experiment review 02
```
