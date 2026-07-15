1-claims: <paper title> (venue-free claim/evidence inventory)
==============================================================

Date: YYYY-MM-DD
Status: DRAFT.
This ledger plans what evidence to collect, commissions the work, and tracks results as they return.


Hypotheses (venue-neutral)
--------------------------

Venue-neutral statements of what the paper tests.
The same H1 can become RQ1 for different venues -- that reframing happens in pitch, not here.

- **H1 (core).**
<hypothesis statement, one sentence per line.>

- **H2 (boundary).**
<hypothesis statement.>

- **H3 (mechanism).**
<hypothesis statement.>


Claims
------

Each claim is a short sub-item: the testable statement, current status, and which probe settles it.
Status vocabulary: `supported` / `weak` / `GAP`.
No inline study design -- the thinking lives in the Q-consumer section.

**C1 - <title> (H1, core) - <status>**

<Claim statement, one sentence per line.>
Evidence: -> PP<nn> (<short description>).

**C2 - <title> (H3, mechanism) - <status>**

<Claim statement.>
Evidence: -> PP<nn> (<short description>).

**C3 - <title> (H2, boundary) - <status>**

<Claim statement.>
Evidence: -> PP<nn> (<short description>).


Q-consumer
----------

The evidence questions this stage raises — one `##` per question: id, title, what it wants.
The route (task/discovery) and the approver (which claim reads the answer) are organized at APPROVE, into the probe file — not here.

## Q1 · <question title>
<what this question wants to know, one sentence per line.>
<which claim it is meant to settle, if that helps frame it.>

## Q2 · <question title>
<what it wants.>

<APPROVE adds each `→ 1-probes/PPNN_<topic>.md` pointer + derived state.>


Evidence Campaign
-----------------

```text
dispatch order         what it unblocks
─────────────────      ────────────────
PP<nn> first           <what it gates>
  -> PP<nn>            <what it informs>
  -> PP<nn>            <the main run>

PP   type        claims   status     settles
──   ────        ──────   ──────     ───────
01   <type>      <Cx>     <status>   <one-line description>
02   <type>      <Cx>     <status>   <one-line description>
```
