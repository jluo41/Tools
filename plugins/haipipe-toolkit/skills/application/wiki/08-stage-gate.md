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

Ladder gate batching (stage-1 family, ladder restage R6)
---------------------------------------------------------

The evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice) batches its gates by venue depth -- approval is batched, never skipped, and every rung still gets its own ledger row:

```
light    ONE combined inline gate at 1d covering all four rungs;
         one approval writes four ledger rows
medium   combined gate at 1c (covers 1a-1c) + own gate at 1d
full     four individual gates, one per rung
```

Venue unpinned (the normal case -- the ladder is venue-FREE and runs before the pin): apply `light` batching provisionally; a later pin to a deeper venue re-opens only the GATE (re-present criteria at the deeper bar), not the content.

Within the ladder, a rung's CHECK routes like any gate: **approve** advances to the next rung (1c → 1d); **revise** reruns the same rung; upstream symptoms **loop back** (1c → 1a for stale/missing data, 1c → 1b for a wrong theme) per the loopback rule. Whatever the batching, the ladder EXITS to venue only through the 1d gate (JL invariant, 2026-07-09).

Rounds within a rung (breadth/depth contract, JL 2026-07-09): REVISE ends with a self-assessment -- did this round surface anything new? If yes, another DRAFT->PROBE->REVISE lap runs BEFORE CHECK (`[ROUND n]` in the rung's `_LOG`); CHECK fires only when a round comes up dry. Venue-scaled round depth: light -- one round suffices unless the rung self-assesses a blocker; medium -- loop-until-dry on 1c; full -- loop-until-dry on every rung. Mid-phase back-routing (`[ROUTE -> <rung>]`) files the upstream slot/card immediately and never waits for a gate -- rounds are internal; only CHECK involves the user. And the gate itself is a lens (JL 2026-07-09): at a GROW-loop rung's CHECK the user is asked which data topics are still missing; a `grow` verdict converts the answers to new slots + planned probes and re-opens DRAFT as [ROUND n+1] -- approve means saturated AND the user added nothing.

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
