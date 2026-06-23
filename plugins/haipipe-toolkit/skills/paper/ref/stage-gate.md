Stage Gate Protocol
===================

A stage is only "done" when the USER explicitly confirms it. The system must
never auto-advance to the next stage. This is the user-control mechanism for
the paper lifecycle.


Gate Protocol (per-stage loop)
------------------------------

0. **Illuminate + Elicit** -- surface taste-bearing choices before drafting
   (see ref/stage-illuminate.md).
1. **Produce** the stage artifact (.tex).
2. **Compile** the stage PDF (see ref/tex-quality.md).
3. **Present exit criteria** with per-item check/fail marks (see table below).
4. **ASK** "Stage <X> looks ready -- confirm to close and move to <next>?"
5. Only on **explicit user confirm**: update STATUS.md current_layer to the
   next stage.

The system **STOPS at Step 4 and WAITS**. No next-stage work until confirmed.


Per-Stage Exit Criteria
-----------------------

| Stage | Exit criteria |
|-----------|---------------------------------------------------------------|
| seed | Seed question stated? Promotion gate defined? Kill criteria defined? At least one evidence path named? |
| pitch | Hook section with >=2 candidate hooks? Surprise stated? Implication/so-what stated? Why-believe with evidence pointers? PDF compiled and current? |
| claims | PRIMARY claim designated? Venue coupling block present? Every claim has status (supported/weak/GAP)? GAP claims have delivery needs recorded? |
| narrative | All claims carried in the arc? Claim-evidence matrix complete? Figure inventory present? Per-beat subagent review comments in small font? |
| display | Gallery README present? Every display unit has README + float.tex? Per-unit interrogation verdict present? Preview PDFs compiled? |
| minimap | Every section/paragraph has a job? Every supported claim anchored in >=1 slot? Every display referenced in >=1 slot? PDF compiled and current? |


Confirmation Ledger in STATUS.md
---------------------------------

STATUS.md carries a **Gate Ledger** -- one row per stage:

    | Stage | Confirmed | Date | Notes |
    |-------|-----------|------|-------|
    | seed | yes | 2026-06-22 | promotion gate met |
    | pitch | yes | 2026-06-22 | 3 hook candidates, A selected |
    | claims | no | -- | -- |

The stage strip's checkmark means "user-confirmed in the ledger", NOT "artifact
exists on disk". A stage with a .tex but no ledger confirmation is unconfirmed.


Autonomy Policy
---------------

- **Stage TRANSITION** = always PAUSE (ask before advancing).
- **Work WITHIN a stage** = can be autonomous (read, draft, compile, backfill).
- **Taste-bearing choices** (framing, emphasis, scope) = PAUSE to elicit
  (see ref/stage-illuminate.md).
- **Mechanical formatting** = autonomous.


Recovery
--------

If a paper reached a late stage without per-stage confirmations, the gate state
is UNCONFIRMED for all stages. A re-walk resets to seed and confirms each stage
one-by-one. Artifacts on disk are NOT deleted -- only the gate state resets.
