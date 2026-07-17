3-narrative: <intervention name> (arc structure, venue-GATED)
==============================================================

Date: YYYY-MM-DD
Status: DRAFT
Venue: <pinned venue>
Fires only if the pinned venue requires it (STATUS.md stages_skipped).
The arc leans only on claims meeting the venue's settlement bar; a load-bearing GAP claim cannot anchor a beat.
Arc rules come from 2-venue.md Artifact Principles; the beats compose the 1d advice (A entries).
How to use: copy to `<intervention>/0-lifecycle/3-narrative/3-narrative.md`, replace every `<...>`, delete unused sub-items (the DRAFT worker does this during the stage's DPRC).



Arc structure
-------------

<Venue-shaped. One numbered position per arc beat, each anchored.>

Sectioned venues (email/report -- linear arc):

1. <beat, e.g. context paragraph> <- A<n> / C<n> (<why this position>)
2. <beat, e.g. finding> <- C<n>, C<n>
3. <beat, e.g. recommendation> <- A<n>
4. <beat, e.g. next steps> <- (standard)

Drill-down venues (dashboard/ui-card -- levels instead of sequence):

Level 1: <summary layer> <- C<n>, C<n> (headline metrics)
Level 2: <detail layer> <- C<n> (supporting evidence)
Level 3: <action layer> <- A<n> (recommendations)


Claim -> arc mapping
--------------------

One line per load-bearing claim/advice: where it lands and what job it does there.

- C<n> -> <position> (<job in one clause>)
- A<n> -> <position> (<job>)


Q-consumer
----------

Narrative-level needs (rare): a beat exposing a NEW evidence gap raises a question here, routed back to 1c-claims — never gathered here.
One `##` per question: id, title, what it wants. The route and approver are organized at APPROVE, into the probe file — not here.

## Q1 · <question title>
<what it wants.>

<APPROVE adds each `→ 1-probes/PPNN_<topic>.md` pointer + derived state.>
