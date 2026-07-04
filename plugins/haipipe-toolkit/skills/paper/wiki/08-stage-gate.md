Stage Gate Protocol
===================

A stage is only "done" when the USER explicitly confirms it. The system must
never auto-advance to the next stage. This is the user-control mechanism for
the paper lifecycle.


Gate Protocol (per-stage loop)
------------------------------

0. **Illuminate + Elicit** -- surface taste-bearing choices before drafting
   (see 09-stage-illuminate.md).
1. **Produce** the stage artifact (markdown `<stage>.md` + `_LOG`; display
   produces `4-display.tex`).
2. **Review** the artifact content. Display only: compile the PDF (see
   13-tex-quality.md). Markdown stages have no compile step; their gate is
   content review.
3. **Present exit criteria** with per-item check/fail marks (see table below).
4. **ASK** "Stage <X> looks ready -- confirm to close and move to <next>?"
5. Only on **explicit user confirm**: update STATUS.md current_layer to the
   next stage.

The system **STOPS at Step 4 and WAITS**. No next-stage work until confirmed.


Per-Stage Exit Criteria
-----------------------

| Stage | Exit criteria |
|-----------|---------------------------------------------------------------|
| seed | Seed question stated? Motivations stated? Tentative claim shape stated? |
| claims | Every claim has status (supported/weak/GAP)? Each claim tied to an evidence source? GAP claims have delivery needs recorded? |
| venue | Shortlist ranked with per-venue rationale? Venue pinned in STATUS.md? |
| pitch | Hook section with >=2 candidate hooks? Surprise stated? Implication/so-what stated? Why-believe with evidence pointers? Editor's Chair Test passed? [primary] claim designated? |
| narrative | All claims carried in the arc? Claim-evidence matrix complete? Figure inventory present? Per-beat subagent review comments in small font? |
| display | Gallery README present? Every display unit has README + float.tex? Per-unit interrogation verdict present? 4-display.tex + PDF compiled and current? |
| section-edit | Every section has a scaffold (outline + _LOG + _CITATION_ + _VALUES_)? DRAFT-PROBE-REVISE-CHECK complete per section? Section checklists pass? |


Confirmation Ledger in STATUS.md
---------------------------------

STATUS.md carries a **Gate Ledger** -- one row per stage:

    | Stage | Confirmed | Date | Notes |
    |-------|-----------|------|-------|
    | seed | yes | 2026-06-22 | question + motivations + claim shape settled |
    | claims | yes | 2026-06-22 | ledger complete, 2 GAPs routed to probe |
    | pitch | no | -- | -- |

The stage strip's checkmark means "user-confirmed in the ledger", NOT "artifact
exists on disk". A stage with an artifact on disk but no ledger confirmation is
unconfirmed.


Autonomy Policy
---------------

- **Stage TRANSITION** = always PAUSE (ask before advancing).
- **Work WITHIN a stage** = can be autonomous (read, draft, compile, backfill).
- **Taste-bearing choices** (framing, emphasis, scope) = PAUSE to elicit
  (see 09-stage-illuminate.md).
- **Mechanical formatting** = autonomous.


Recovery
--------

If a paper reached a late stage without per-stage confirmations, the gate state
is UNCONFIRMED for all stages. A re-walk resets to seed and confirms each stage
one-by-one. Artifacts on disk are NOT deleted -- only the gate state resets.
