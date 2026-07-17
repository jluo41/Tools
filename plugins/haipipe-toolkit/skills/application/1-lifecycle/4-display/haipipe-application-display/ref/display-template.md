4-display: <intervention name> (content elements + unit jobs, venue-GATED)
===========================================================================

Date: YYYY-MM-DD
Status: DRAFT
Venue: <pinned venue>
Fires only if the pinned venue requires it (STATUS.md stages_skipped).
Every unit carries FOUR required fields -- Type, Claim, Job, Data source.
The Job field is the minimap absorption: one sentence on what this unit must make the reader see/do.
Unit materialization is raised as a SECTION in the flat probe pool `1-probes/PPNN_<topic>.md` and, uniquely among stages, commissioned by this stage through the PROBE phase to a task; this doc plans and links.
How to use: copy to `<intervention>/0-lifecycle/4-display/4-display.md`, replace every `<...>`, delete unused sub-items (the DRAFT worker does this during the stage's DPRC).



Display units
-------------

One **U<nn>** per unit. Element types come from the venue profile (metric-card, line-chart, table, ...).

**U01 - <element name, e.g. KPI Card: Refill Rate>**

Type: <element type>.
Claim: C<n> (via A<n> where an advice entry drives it).
Job: <one sentence: what the reader must see/do because of this unit>.
Content: <what it shows, one line>.
Data source: <task ref, e.g. tasks/X01_<slug>/results/...> · Status: <planned | commissioned (PP<nn>) | landed>.

**U02 - <element name>**

Type: <type>.
Claim: C<n>.
Job: <job sentence>.
Content: <content>.
Data source: <ref> · Status: <planned | commissioned (PP<nn>) | landed>.


Unit -> section mapping (sectioned venues)
------------------------------------------

- U01 -> <section> (<why there>)
- U02 -> <section>


Q-consumer
----------

Materialization needs — one `##` per question: id, which unit it materializes, what it needs.
Uniquely, this stage commissions these to a task through its PROBE phase; the display lane LINKs what landed. The route and approver are organized at APPROVE, into the probe file — not here.

## Q1 · materialize U<nn> — <what the unit needs>
<what it wants.>

<APPROVE adds each `→ 1-probes/PPNN_<topic>.md` pointer + derived state.>
