Stage Gate Protocol
===================

A stage is only "done" when an EXPLICIT APPROVAL ACTION closes it. The system must never auto-advance silently. The approver is either the human (copilot mode, default) or a reviewer subagent standing in for the human (autopilot mode) -- but there is ALWAYS a judgment step.


Gate Modes
-----------

Mode lives in STATUS.md (`gate_mode: copilot | autopilot`, default copilot) and can be overridden per invocation (e.g. "run seed --autopilot").

```
🧑 copilot   (default)  the human reads the exit-criteria report, adds > JL: comments,
                        and explicitly confirms / restarts / accepts.
🤖 autopilot            a FRESH-CONTEXT reviewer subagent reads the stage artifact + the
                        exit-criteria report, leaves > REVIEWER: comments in the working doc,
                        and returns a verdict: approve | restart-from-<DRAFT|PROBE|REVISE> (+ reasons).
                        approve -> advance; the ledger records the agent as actor.
                        restart -> the named phase re-runs READING the > REVIEWER: comments,
                        then re-checks (same loop a human restart triggers).
                        HUMAN-ONLY items (e.g. Scholar bibtex verification -- agents never touch .bib)
                        are NOT silently passed: they are marked DEFERRED and accumulate in a human
                        queue the human clears at the next copilot touchpoint.
                        The human can REOPEN any agent-approved gate later; reopening resets that
                        stage's ledger row.
```


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
4. **APPROVAL** -- copilot: ASK "Stage <X> looks ready -- confirm to close and
   move to <next>?" and WAIT. autopilot: dispatch the reviewer subagent and
   take its verdict.
5. Only on **explicit approval** (human confirm, or reviewer approve): update
   STATUS.md current_layer to the next stage and write the ledger row with the
   actor.

In copilot mode the system **STOPS at Step 4 and WAITS**. In autopilot mode the reviewer's verdict IS the Step-4 action; a restart verdict loops back instead of advancing.


Stage Exit Invariant
--------------------

The CHECK phase is the ONLY door out of a stage. Its verdicts move in exactly two directions:

```
♻️ backward, WITHIN the stage    restart from DRAFT | PROBE | REVISE (a phase re-opens; never another stage)
✅ forward, ACROSS the gate      proceed (or accept-with-issues) -> current_layer advances to the next stage
```

Going BACK across stages (e.g. redoing seed while the frontier is section-edit) is NOT a CHECK outcome. That is a lifecycle loopback: re-enter the earlier stage directly (`/haipipe-paper seed`; 🔥 moves there, 🚀 stays at the frontier), and that stage runs its own DPRC cycle and its own CHECK gate.


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

STATUS.md carries a **Gate Ledger** -- one row per stage, with the APPROVAL ACTOR:

    | Stage | Approved | Actor | Date | Notes |
    |-------|----------|-------|------|-------|
    | seed | yes | JL | 2026-06-22 | question + motivations + claim shape settled |
    | claims | yes | reviewer-agent | 2026-06-22 | autopilot; 2 deferred human items in queue |
    | pitch | no | -- | -- | -- |

(Older ledgers with a `Confirmed` column read as Actor = human.) The stage strip's checkmark means "approved in the ledger", NOT "artifact exists on disk". A stage with an artifact on disk but no ledger approval is unapproved.


Autonomy Policy
---------------

- **Stage TRANSITION** = always an explicit approval ACTION (copilot: ask the human and pause; autopilot: reviewer subagent verdict).
- **Work WITHIN a stage** = can be autonomous (read, draft, compile, backfill).
- **Taste-bearing choices** (framing, emphasis, scope) = PAUSE to elicit
  (see 09-stage-illuminate.md).
- **Mechanical formatting** = autonomous.


Recovery
--------

If a paper reached a late stage without per-stage confirmations, the gate state
is UNCONFIRMED for all stages. A re-walk resets to seed and confirms each stage
one-by-one. Artifacts on disk are NOT deleted -- only the gate state resets.
