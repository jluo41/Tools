Stage Gate Protocol (application)
==================================

A stage is only "done" when it is EXPLICITLY approved. The system must never auto-advance. This is the user-control mechanism for the intervention lifecycle. Application rewrite of the paper protocol (`../../paper/wiki/08-stage-gate.md`); the venue scales the gate's DEPTH, never its existence.

Gate Protocol (per-stage loop)
------------------------------

1. **Produce** the stage artifact through DRAFT → PROBE → REVISE (2-phase/ workers). The PROBE phase ends with a VERIFY step: `check-probe-cards.sh` FAILs cards left `planned|dispatched|failed`, dangling refs, and `harvest: OWED` lane debts.
2. **Present exit criteria** with per-item check/fail marks (per-stage table: `2-phase/3-check/haipipe-application-check/SKILL.md`).
3. **ASK** "Stage <X> looks ready -- confirm to close and move to <next>?"
4. Only on **explicit approval**: write the Gate Ledger row and update STATUS.md `current_layer` to the next non-skipped stage.

The system **STOPS at step 3 and WAITS**. No next-stage work until approved.

Venue-scaled depth
------------------

```
simple venues (sms/push/reminder)      INLINE gate: exit criteria as one short
                                       checklist in the reply; user's "ok" approves
medium venues (checklist/email)        INLINE by default; full report on request
complex venues (dashboard/ui-card/     FULL gate: complete CHECK report (criteria +
report)                                evidence spot-checks + flags) before the ask
```

Depth changes the REPORT, not the rule: every stage still ends with an explicit approval and a ledger row.

Mechanical teeth
-----------------

The gate is not prose-only. Before the ask, the check worker (`2-phase/3-check/haipipe-application-check`) runs two deterministic checkers, and any FAIL blocks the gate from going green:

- `check-probe-cards.sh` (re-run of the probe worker's VERIFY step): a `status: planned` card or a `harvest: OWED` lane at the gate means a probe that never ran — FAIL.
- `checks.sh` (markdown-safe deterministic checks): em-dash (❌ house rule), AI-voice tells, TODO/FIXME, bibtex-in-markdown.

Findings are seeded as `> CHECK:` threads in the STAGE DOCS only; `0-artifacts/*.md` stay clean because the artifact IS the deliverable text — artifact-level findings go to the Gate Ledger `Notes` column instead (JL ruling 2026-07-07).

Confirmation Ledger in STATUS.md
---------------------------------

STATUS.md carries a **Gate Ledger** -- one row per stage:

    | Stage | Confirmed | Date | By | Notes |
    |-------|-----------|------|----|-------|
    | seed | yes | 2026-07-06 | JL | kill criteria set |
    | claims | yes | 2026-07-06 | JL | settlement: light met |
    | pitch | no | -- | -- | -- |

`By` records who approved: the human (copilot mode, the default) or `persona:<preset>` (unattended runs only -- attendance modes and persona presets live with the check worker). The stage strip's ✅ means "confirmed in the ledger", NOT "artifact exists on disk". A stage with a doc but no ledger row is unconfirmed. Venue-skipped stages never get ledger rows (they render `--` in the strip).

Autonomy Policy
---------------

- **Stage TRANSITION** = always PAUSE (ask before advancing).
- **Work WITHIN a stage** = can be autonomous (read, draft, buffer probe cards, backfill).
- **Taste-bearing choices** (framing, emphasis, scope, venue pick) = PAUSE to elicit.
- **Mechanical formatting** = autonomous.
- **Evidence dispatch** = the PROBE phase worker is the only door; a stage never reads discoveries/, tasks/, or legacy probes/ inline, and never dispatches discovery/task orchestrator agents itself.

Recovery
--------

If an intervention reached a late stage without per-stage confirmations, the gate state is UNCONFIRMED for all stages. A re-walk resets to seed and confirms each non-skipped stage one-by-one. Artifacts on disk are NOT deleted -- only the gate state resets.
