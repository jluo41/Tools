---
name: haipipe-application-enter
description: "Intervention Console. Derives current state from disk (0-lifecycle/ stages, 1-probe-plans/, 0-artifacts/, 1-rounds/), renders an open-needs dashboard with lifecycle frontier, maturity, stable assets, claim/evidence gaps, and next commands. Records session state in .intervention-console.yaml. Routes free-form follow-up through the lifecycle. Modeled on haipipe-paper-enter. Trigger: enter, status, dashboard, intervention status, /haipipe-application enter."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-06-22"
  summary: "Intervention Console — derive-from-disk dashboard + lifecycle router."
  changelog:
    - "1.0.0 (2026-06-22): initial version modeled on paper-enter."
---

Skill: haipipe-application-enter (Intervention Console)
========================================================

Derive-from-disk, context-aware entry point for one intervention.

```
/haipipe-application enter <intervention-path>
/haipipe-application status [intervention-path]
```


What the Console does
======================

1. **Resolve** intervention root by walking up for STATUS.md,
   0-lifecycle/, or 0-artifacts/.

2. **Derive** current state from disk (not stored status):
   - Each lifecycle stage file existence and content
   - Claim ledger GAP/weak/supported counts
   - Probe plans buffered vs dispatched
   - Artifact variants drafted
   - Round status (open/closed)

3. **Render** a tight dashboard:

   ```
   Intervention: 03_refill_reminder
   Audience:     patient
   Theory:       timing-aware refill SMS increases adherence by 8-12pp
   
   Lifecycle:  ✅ seed  ✅ rationale  ▶️ claims  ⬜ design  ⬜ variants  ⬜ delivery
   Maturity:   claim-ledger
   Round:      v260620 (open, 2 todo remaining)
   
   Open needs:
     C02  GAP   "timing matters for refill"  → probe PP01 (dispatched, pending)
     C04  weak  "tone affects click-through" → no probe planned
   
   Artifacts:  0 drafted, 0 reviewed
   
   Next:
     /haipipe-application claims    (resolve GAPs before advancing)
     /haipipe-application round     (triage v260620 todo)
   ```

4. **Record** session state in `.intervention-console.yaml`.

5. **Route** free-form follow-up input through the lifecycle dispatcher.


Lifecycle progress strip
=========================

```
✅  stage artifact exists and has content
▶️  current frontier (earliest incomplete stage)
⬜  not yet started
⚠️  stage exists but has GAPs or issues
```


Maturity (derived, not declared)
=================================

```
prospect       0-seed exists, no further obligations
rationale      1-rationale exists
claim-ledger   2-claims exists with explicit C-slots
designed       3-design exists
variants-map   4-variants exists
delivery-plan  5-delivery-plan exists
drafted        0-artifacts/ has at least one artifact
reviewed       review pass completed
deployed       artifact shipped to channel
iterating      post-deploy round open with A/B results
```


Console session state (.intervention-console.yaml)
====================================================

```yaml
intervention_root: <path>
entered_at: <ISO>
frontier_stage: claims
maturity: claim-ledger
open_needs: [{id: C02, status: GAP, route: "probe PP01"}, ...]
active_round: v260620
artifact_count: {drafted: 0, reviewed: 0, deployed: 0}
```


Routing follow-up input
=========================

After rendering the dashboard, the Console stays active and routes
free-form user input:

```
"resolve the timing claim"       → /haipipe-application claims
"draft an SMS"                   → /haipipe-application draft message
"what's in round v260620?"       → /haipipe-application round
"show probe PP01 status"         → /haipipe-probe status PP01
"advance to design"              → /haipipe-application design
```


Risk profile
=============

READ-ONLY on intervention artifacts. Writes only
`.intervention-console.yaml` (session state, not content).


Specialist tail
================

```
status:    ok | not_found
summary:   "<intervention name> at <maturity>; frontier = <stage>; N open needs"
artifacts: [.intervention-console.yaml]
next:      <suggested lifecycle command>
```
