0-seed: <intervention name> (why this might work, venue-free)
==============================================================

Date: YYYY-MM-DD
Status: DRAFT
The earliest-stage contract: keeps the intervention possibility alive before evidence is mature.



Opportunity
-----------

<2-3 sentences: what gap exists, what behavior we want to change.>


Expected impact
---------------

<Directional estimate, e.g. "increase refill adherence by 5-15pp".>


Audience
--------

<Who receives this intervention: patient subset, clinician type. Specific, not "everyone".>


Channel hunch
-------------

<SMS, push, in-app UI, provider dashboard, email -- a HUNCH, not a pin;
the venue decision happens after the evidence ladder via /haipipe-application venue.>


Mechanism hypothesis
--------------------

<One sentence: why this audience + this content might respond.>


Q-consumer
----------

<!-- RULE: every question the draft raises, one `## Q-Seed-<n>` block each.
     · RAISE FREELY — as many questions as the draft needs; asking is cheap. When a sentence rests on something no existing question tests, PROPOSE A NEW ONE rather than leave it unanchored. No question shape is disqualified from being asked here.
     · DISPATCH NARROWLY — the GATE decides, per question, what goes out at seed: feasibility-shaped only (novelty, external-data-obtainability), which also gets an entry in `1-probes/`. Anything else stays here with `Answer: deferred -> CLAIMS` and a `[FORWARD -> CLAIMS]` pointer in `_LOG_0-seed.md` — no entry, no dispatch. (The token stays `CLAIMS` for grep-stability; rung 1a is what consumes it.)
     · STAGE-PREFIXED ID — `Q-Seed-<n>`. Each stage owns its own index (Q-Claim-<n>, Q-Pitch-<n>, …) so a cited id is never ambiguous across stages.
     · ANCHORED, not detached — every question spot-checks a SPECIFIC assertion above; cite its id inline in the sentence(s) it hangs on, e.g. [Q-Seed-1]. One question may be cited from several sentences — that is how it links to more than one place.
     · Description = what the question wants. Reason = every anchor it is cited from + why each matters if that assertion is wrong (the back-link). Probe = the pointer to the ENTRY that carries this question, `→ 1-probes/PP<nn> · QX<n>` (DISPATCHED questions only; a DEFERRED one writes `--`). Answer = empty in DRAFT; PROBE fills it from the answering QA file.
     · The loop closes at REVISE (not PROBE): the answer is woven back into every sentence that cites [Q-Seed-<n>], and the bracket is discharged. Born from content (DRAFT drops the bracket in), dies into content (REVISE discharges it). -->

## Q-Seed-<n> · <question title>
Description: <what the question wants to know — one sentence per line>
Reason: <which section(s) above cite this id, and why each matters if that assertion is wrong>
Probe: <→ 1-probes/PP<nn> · QX<n> for a DISPATCHED question; `--` for one the gate DEFERRED>
Answer: <empty in DRAFT — PROBE fills it from the answering QA file, anchored [source: PPnn]; a question the gate DEFERRED reads `deferred -> CLAIMS`; on a loopback redo, prior-cycle resolution + source>