# Intervention Dashboard Contract

The Intervention Console (haipipe-application-enter) derives the
dashboard from disk. This document specifies what is read and how
the dashboard is rendered.

Modeled on paper/ref/paper-dashboard.md.


Derive-from-disk rules
========================

The Console reads the intervention folder and derives state. It
NEVER trusts STATUS.md alone — disk wins.


Stage frontier detection
==========================

```python
for stage in [0-seed, 1-rationale, 2-claims, 3-design, 4-variants, 5-delivery-plan]:
    path = f"0-lifecycle/{stage}.md"
    if not exists(path) or is_empty(path):
        frontier = stage
        break
else:
    frontier = "post-lifecycle"  # all stages complete
```


Open needs detection
=====================

```
Source                          Need type
───────────────────────         ──────────────
2-claims.md: status=GAP         claim gap → probe plan
2-claims.md: status=weak        weak claim → optional probe
1-probe-plans/: status=planned  unstarted probe
1-probe-plans/: status=dispatched  in-progress probe
4-variants.md: status=planned   undrafted variant
0-artifacts/REVIEW-*: verdict=revise   needs revision
1-rounds/latest: status=open    open round with todo
```


Dashboard rendering
====================

```
Intervention: <name>
Audience:     <from seed or audience profile>
Theory:       <one-sentence from rationale, or "(not yet written)")>

Lifecycle:  ✅ seed  ✅ rationale  ▶️ claims  ⬜ design  ⬜ variants  ⬜ delivery
Maturity:   <derived maturity>
Round:      <active round or "none">

Claims:     N total: M supported, P weak, Q GAP
Probes:     N planned, M dispatched, P returned
Artifacts:  N drafted, M reviewed, P deployed

Open needs:
  <id>  <type>   <description>   → <suggested route>

Next:
  <suggested command based on frontier and open needs>
```


Progress strip symbols
=======================

```
✅  stage file exists and has substantive content
▶️  current frontier (earliest incomplete stage)
⬜  not yet started (no file or empty)
⚠️  stage exists but has issues (GAPs in claims, review failures)
```


Session state file (.intervention-console.yaml)
==================================================

Written by the Console on entry. Read on re-entry to detect
changes since last session.

```yaml
intervention_root: <path>
entered_at: <ISO>
frontier_stage: <stage name>
maturity: <derived maturity>
open_needs:
  - {id: C02, type: GAP, route: "probe PP01"}
  - {id: V01, type: planned, route: "draft message"}
active_round: <vYYMMDD or null>
artifact_count:
  drafted: 0
  reviewed: 0
  deployed: 0
claims_summary:
  total: 5
  supported: 2
  weak: 1
  gap: 2
```
