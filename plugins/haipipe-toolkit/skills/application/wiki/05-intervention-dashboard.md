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
1-claims: status=GAP below settlement bar     claim gap → raise a question
1-claims: status=weak (load-bearing)          weak claim → optional question
1-probes/: section state=planned              question raised, never bound
1-probes/: section state=commissioned         answer in flight (OVERDUE past its eta = FAIL)
1-probes/: section state=answered             the QA file landed, nobody read it yet
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
Probes:     PP01-PP02 · 4 questions: 1 read, 1 answered, 1 commissioned, 1 planned
Artifacts:  0 drafted, 0 reviewed, 0 deployed
Round:      v260620 (open, 2 todo remaining)

Open needs:
  C02  GAP   "timing matters for refill"  → probe PP01 (commissioned)

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
