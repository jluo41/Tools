# Intervention Dashboard Contract

The Intervention Console (haipipe-application-enter) derives the dashboard from disk. This document specifies what is read and how the dashboard is rendered. Modeled on `../../paper/wiki/05-paper-dashboard.md`.

Derive-from-disk rules
========================

The Console reads the intervention folder and derives state. It NEVER trusts STATUS.md alone — disk wins; STATUS.md drift is flagged.

Stage frontier detection
==========================

```python
spine = ["0-seed", "1-claims", "venue", "2-pitch", "3-narrative", "4-display", "5-section-edit"]
skipped = read_status_row("stages_skipped")          # written at venue pin
for stage in spine:
    if stage in skipped: continue                    # venue-skipped: passed over, never a gap
    if stage == "venue":
        if not status_has_venue(): frontier = "venue"; break
    elif not stage_doc_has_content(f"0-lifecycle/{stage}/{stage}.md") or not gate_confirmed(stage):
        frontier = stage; break
else:
    frontier = "draft" if no_artifact() else "review" if not_reviewed() else "deploy"
```

Open needs detection
=====================

```
Source                                        Need type
───────────────────────                       ──────────────
1-claims: status=GAP below settlement bar     claim gap → probe card
1-claims: status=weak (load-bearing)          weak claim → optional probe
1-probe-plans/README.md: planned              unstarted probe card
1-probe-plans/README.md: dispatched           in-progress probe (await TRANSLATE)
4-display: element without task ref           unmaterialized element
5-section-edit: DPRC phase incomplete         section work
0-artifacts/REVIEW-*: verdict=revise          artifact needs revision
1-rounds/latest: status=open                  open round with todo
```

Dashboard rendering
====================

Body order per `0-enter/haipipe-application-enter/SKILL.md` (Identity → About → Focus Strip → Current State → Stable → Open Needs → Loopback → Next → Artifacts Read). Compact shape:

```
Intervention: 03_refill_reminder
Venue:        sms · audience: patient · settlement: light
Theory:       <one sentence from 2-pitch, or "(pitch not yet written)">

stage:   seed ✅  claims 🔥🚀  venue ⬜  pitch ⬜  narrative --  display --  section-edit --  →  draft ⬜  →  review ⬜  →  deploy ⬜
phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜

Claims:     5 total: 2 supported, 1 weak, 2 GAP (bar: light — 1 load-bearing GAP open)
Probes:     2 planned, 1 dispatched, 0 verdicted
Artifacts:  0 drafted, 0 reviewed, 0 deployed
Round:      v260620 (open, 2 todo remaining)

Open needs:
  C02  GAP   "timing matters for refill"  → probe PP01 (dispatched)

Next:
  /haipipe-application probe run PP01
```

Strip symbols
==============

The stage line is rendered ONLY by `haipipe-application/stage-strip.sh` (🔥 active · 🚀 frontier · ✅ ledger-confirmed · ⬜ not started · `--` venue-skipped). Marker convention: haipipe-application/SKILL.md Closing Block, the single source of truth. The old ▶️ frontier symbol is retired.

Session state file (.intervention-console.yaml)
==================================================

Written by the Console on entry; a fresh session re-derives everything from disk.

```yaml
intervention_root: <path>
active_intervention: <name>
venue: <pinned venue or "">
current_layer: <frontier stage>
maturity: <derived maturity>
active_round: <vYYMMDD or null>
open_needs: <count>
updated: <YYMMDD>
```
