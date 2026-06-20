End-to-End Sandwich Run Example
===============================

Status: draft (2026-06-20)
Scope: one concrete project run through Narrative -> Probe -> Discovery/Task
       -> Probe -> Narrative.


Mental Model
============

This is the smallest useful full run:

```
Narrative-open
  Probe-open
    Discovery A
    Discovery B
    Task 1
    Task 2
    Task 3
  Probe-post
Narrative-post
```

Narrative asks, "what story are we trying to fill?"
Probe asks, "what claim would settle this gap?"
Discovery asks, "what does the outside world already know?"
Task asks, "what did our own execution show?"

The key rule: each layer references the next layer's artifacts. It does not
own or embed them.


Example User Request
====================

```
We think adaptive sampling improves rare phenotype detection.
Create a narrative, run the first probe, check prior art, run three evaluation
tasks, and tell me whether the story is ready.
```


Expected Project Tree
=====================

```
examples/ProjX-Phy-001-AdaptiveSampling/
|-- _haipipe/
|   |-- project.log.jsonl
|   |-- project.status.yaml
|   `-- project.site.md
|-- narratives/
|   `-- N001_adaptive-sampling/
|       |-- story.md
|       |-- claims.md
|       |-- ignite-log.md
|       `-- decision-tree.md
|-- probes/
|   `-- P001_rare-phenotype-lift/
|       |-- probe.yaml
|       |-- status.yaml
|       |-- site.md
|       |-- review.md
|       |-- INTEGRITY_AUDIT.md
|       `-- CLAIMS_FROM_RESULTS.md
|-- discoveries/
|   |-- D001_prior-art-adaptive-sampling/
|   |   |-- discovery.yaml
|   |   |-- status.yaml
|   |   |-- site.md
|   |   |-- sources.md
|   |   |-- notes.md
|   |   `-- verdict.md
|   `-- D002_benchmark-landscape-rare-phenotypes/
|       |-- discovery.yaml
|       |-- status.yaml
|       |-- site.md
|       |-- sources.md
|       |-- notes.md
|       `-- verdict.md
|-- tasks/
|   |-- T001_baseline-eval/
|   |   |-- workflow/
|   |   |-- configs/
|   |   |-- runs/
|   |   |-- results/
|   |   |-- status.yaml
|   |   `-- site.md
|   |-- T002_adaptive-eval/
|   |   |-- workflow/
|   |   |-- configs/
|   |   |-- runs/
|   |   |-- results/
|   |   |-- status.yaml
|   |   `-- site.md
|   `-- T003_ablation-eval/
|       |-- workflow/
|       |-- configs/
|       |-- runs/
|       |-- results/
|       |-- status.yaml
|       `-- site.md
|-- paper/
`-- applications/
```


Object Responsibilities
=======================

Narrative package:

```
narratives/N001_adaptive-sampling/
```

Owns the story:

- `story.md`: angle, audience, why the claim matters.
- `claims.md`: claim slots and gap ledger.
- `ignite-log.md`: round-level YES/NO decisions.
- `decision-tree.md`: eventual paper/application spine.

It references `P001_rare-phenotype-lift`; it does not read task metrics
directly unless debugging.

Probe package:

```
probes/P001_rare-phenotype-lift/
```

Owns the claim contract:

- What claim is being tested?
- What discoveries are required?
- What tasks are required?
- What completion gate closes the probe?
- What verdict follows from the evidence?

It references discoveries and tasks by ID/path; it does not contain them.

Discovery packages:

```
discoveries/D001_prior-art-adaptive-sampling/
discoveries/D002_benchmark-landscape-rare-phenotypes/
```

Own outside-world evidence:

- sources
- source notes
- prior-art or benchmark synthesis
- a compact verdict the probe can consume

Task packages:

```
tasks/T001_baseline-eval/
tasks/T002_adaptive-eval/
tasks/T003_ablation-eval/
```

Own inside-world execution:

- workflow plans
- code/config/run scripts
- runtime status
- metrics
- task report

Tasks do not decide whether the research claim is true. They only produce
execution evidence for Probe-post.


Single Project Log
==================

All orchestration events go to one append-only log:

```
_haipipe/project.log.jsonl
```

Example:

```jsonl
{"ts":"2026-06-20T09:00:00-04:00","event":"narrative.opened","narrative_id":"N001_adaptive-sampling","status":"exploring","summary":"Story angle created: adaptive sampling may improve rare phenotype detection."}
{"ts":"2026-06-20T09:12:00-04:00","event":"probe.opened","narrative_id":"N001_adaptive-sampling","probe_id":"P001_rare-phenotype-lift","status":"waiting_for_evidence","summary":"Probe opened for rare phenotype lift claim."}
{"ts":"2026-06-20T09:15:00-04:00","event":"discovery.started","probe_id":"P001_rare-phenotype-lift","discovery_id":"D001_prior-art-adaptive-sampling","role":"prior_art_check"}
{"ts":"2026-06-20T09:16:00-04:00","event":"discovery.started","probe_id":"P001_rare-phenotype-lift","discovery_id":"D002_benchmark-landscape-rare-phenotypes","role":"benchmark_landscape"}
{"ts":"2026-06-20T09:20:00-04:00","event":"task.started","probe_id":"P001_rare-phenotype-lift","task_id":"T001_baseline-eval","task_type":"eval"}
{"ts":"2026-06-20T09:21:00-04:00","event":"task.started","probe_id":"P001_rare-phenotype-lift","task_id":"T002_adaptive-eval","task_type":"eval"}
{"ts":"2026-06-20T09:22:00-04:00","event":"task.started","probe_id":"P001_rare-phenotype-lift","task_id":"T003_ablation-eval","task_type":"eval"}
{"ts":"2026-06-20T11:05:00-04:00","event":"discovery.completed","discovery_id":"D001_prior-art-adaptive-sampling","status":"ok","summary":"No exact prior art found; related active-learning methods noted."}
{"ts":"2026-06-20T11:20:00-04:00","event":"discovery.completed","discovery_id":"D002_benchmark-landscape-rare-phenotypes","status":"ok","summary":"Benchmark metrics and baseline expectations captured."}
{"ts":"2026-06-20T12:30:00-04:00","event":"task.completed","task_id":"T001_baseline-eval","status":"reported","summary":"Baseline metrics written."}
{"ts":"2026-06-20T12:42:00-04:00","event":"task.completed","task_id":"T002_adaptive-eval","status":"reported","summary":"Adaptive metrics written."}
{"ts":"2026-06-20T12:55:00-04:00","event":"task.completed","task_id":"T003_ablation-eval","status":"reported","summary":"Ablation metrics written."}
{"ts":"2026-06-20T13:10:00-04:00","event":"probe.closed","probe_id":"P001_rare-phenotype-lift","status":"closed","verdict":"supported_with_caveats","summary":"Adaptive sampling improves recall, but precision cost must be reported."}
{"ts":"2026-06-20T13:30:00-04:00","event":"narrative.posted","narrative_id":"N001_adaptive-sampling","status":"needs_next_probe","summary":"Main claim partly filled; next gap is precision tradeoff framing."}
```

Do not create `logs/` inside each narrative, probe, discovery, or task folder.
Local folders summarize state; `_haipipe/project.log.jsonl` records time.


Project Snapshot
================

`_haipipe/project.status.yaml` is a current snapshot, not a full event history:

```yaml
project_id: ProjX-Phy-001-AdaptiveSampling
updated_at: "2026-06-20T13:30:00-04:00"
active_narrative: N001_adaptive-sampling
status: needs_next_probe

narratives:
  N001_adaptive-sampling:
    status: needs_next_probe
    open_gaps:
      - precision_tradeoff

probes:
  P001_rare-phenotype-lift:
    status: closed
    verdict: supported_with_caveats
    narrative_id: N001_adaptive-sampling

discoveries:
  D001_prior-art-adaptive-sampling:
    status: ok
    probe_id: P001_rare-phenotype-lift
  D002_benchmark-landscape-rare-phenotypes:
    status: ok
    probe_id: P001_rare-phenotype-lift

tasks:
  T001_baseline-eval:
    status: reported
    probe_id: P001_rare-phenotype-lift
  T002_adaptive-eval:
    status: reported
    probe_id: P001_rare-phenotype-lift
  T003_ablation-eval:
    status: reported
    probe_id: P001_rare-phenotype-lift
```


Probe Contract Example
======================

`probes/P001_rare-phenotype-lift/probe.yaml` should make the references clear:

```yaml
id: P001_rare-phenotype-lift
status: waiting_for_evidence
narrative_id: N001_adaptive-sampling
claim: Adaptive sampling improves rare phenotype recall over the baseline.

evidence_plan:
  discoveries:
    - id: D001_prior-art-adaptive-sampling
      role: prior_art_check
      required: true
    - id: D002_benchmark-landscape-rare-phenotypes
      role: benchmark_landscape
      required: true
  tasks:
    - id: T001_baseline-eval
      type: eval
      required: true
    - id: T002_adaptive-eval
      type: eval
      required: true
    - id: T003_ablation-eval
      type: eval
      required: true

completion_gate:
  require_discovery_verdicts: true
  require_task_reports: true
  required_task_status: reported
```

After Probe-post:

```yaml
id: P001_rare-phenotype-lift
status: closed
verdict: supported_with_caveats
claim_result:
  summary: Adaptive sampling improves recall, but precision cost must be framed.
  supports_narrative_claim: partial
evidence_refs:
  discoveries:
    - discoveries/D001_prior-art-adaptive-sampling/verdict.md
    - discoveries/D002_benchmark-landscape-rare-phenotypes/verdict.md
  tasks:
    - tasks/T001_baseline-eval/results/main/metrics.json
    - tasks/T002_adaptive-eval/results/main/metrics.json
    - tasks/T003_ablation-eval/results/main/metrics.json
```


How To Read Progress
====================

Use three levels:

1. `_haipipe/project.site.md`
   Human dashboard: what is active, what is blocked, what closed recently.

2. `_haipipe/project.status.yaml`
   Machine-readable current state.

3. `_haipipe/project.log.jsonl`
   Append-only timeline for reconstructing exactly what happened.

Local `site.md` files answer local questions:

```
narratives/N001.../site.md   what story gap is open?
probes/P001.../site.md       what evidence is missing?
discoveries/D001.../site.md  what sources/verdict exist?
tasks/T001.../site.md        what run/report status exists?
```


End State
=========

A run is ready for handoff only when:

- Narrative has no blocking claim gaps.
- Required probes are closed.
- Probe verdicts are supported or explicitly caveated.
- Required discovery verdicts exist.
- Required task reports and metrics exist.
- `ignite-log.md` says YES.

Then the narrative can hand off to `paper/` or `application/`.
