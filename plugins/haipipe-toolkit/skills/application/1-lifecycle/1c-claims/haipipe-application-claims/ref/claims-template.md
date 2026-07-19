1c-claims: <intervention name> (venue-free claim ledger + evidence campaign)
=============================================================================

Date: YYYY-MM-DD
Status: DRAFT
Ladder rung 1c: which claims generalize -- supported / weak / GAP -- and what evidence settles each.
This ledger plans what evidence to collect, commissions the work, and tracks results as they return.
(No Hypotheses section -- mechanism lives in seed/pitch; the theme space lives in 1b.)



Claims
------

Each claim is a short sub-item: the testable statement, theme tag, role, status, and which probe settles it.
Status vocabulary: `supported` / `weak` / `GAP`.
No inline study design -- the thinking lives in the Q-consumer section.

**C1 (T1, primary) - <title> - <status>**

<Claim statement, one sentence per line.>
Rival: <the strongest alternative explanation the probe must rule out>.
Evidence: -> PP<nn> (<short description>).

**C2 (T1, enabling) - <title> - <status>**

<Claim statement.>
Evidence: -> PP<nn> (<short description>).

**C3 (T2, assumption) - <title> - <status>**

<Claim statement.>
Evidence: -> PP<nn> (<short description>).


Declined hooks
--------------

Theme hooks considered and not committed as claims, one line each with a why; the reservoir the next round's DRAFT re-mines.
(May be empty.)

- T<n> hook "<clause>" -- <why declined, e.g. not testable with current data / superseded by C<n>>


Q-consumer
----------

<Evidence questions this stage raises. One ## Q-Claim-<n> block each.>

## Q-Claim-1 · <question title>

Ask: <what this question wants to know; one sentence per line.>

Why: <which claim(s) it settles, and the Refutes-if that would FLIP the claim.>
## Q-Claim-2 · <question title>

Ask: <what it wants.>

Why: <which claim it settles.>

Evidence Campaign
-----------------

```text
dispatch order         what it unblocks
─────────────────      ────────────────
PP<nn> first           <what it gates>
  -> PP<nn>            <what it informs>

PP   route       claims   status     settles
──   ─────       ──────   ──────     ───────
01   <route>     <Cx>     <status>   <one-line description>
02   <route>     <Cx>     <status>   <one-line description>
```
