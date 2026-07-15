1c-claims: <intervention name> (venue-free claim ledger + evidence campaign)
=============================================================================

Date: YYYY-MM-DD
Status: DRAFT
Ladder rung 1c: which claims generalize -- supported / weak / GAP -- and what evidence settles each.
This ledger plans what evidence to collect, commissions the work, and tracks results as they return.
(No Hypotheses section -- mechanism lives in seed/pitch; the theme space lives in 1b.)
How to use: copy to `<intervention>/0-lifecycle/1c-claims/1c-claims.md`, replace every `<...>`, delete unused sub-items (the DRAFT worker does this during the stage's DPRC).



Claims
------

Each claim is a short sub-item: the testable statement, theme tag, role, status, and which probe settles it.
Status vocabulary: `supported` / `weak` / `GAP`.
No inline study design -- the thinking lives in the Probes section.

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


Probes
------

Each probe is its own sub-item organized by PP number.
Full evidence plan: mode, route, claims, status, dependencies, what work to do.
Separated by `---` horizontal rules.

**PP01 - <title> - <status>**

Mode: <light | full>.
Route: <task | discovery>.
Claims: <which claims this settles>.
Status: <planned | dispatched | read | verdicted>.
<Dependencies, if any.>

<Full evidence plan, one sentence per line.>
Refutes-if: <the result that would FLIP the claim(s) this probe settles>.
Detail: `_PROBE/PP01_<slug>.md`

---

**PP02 - <title> - <status>**

Mode: <mode>.
Route: <route>.
Claims: <which claims>.
Status: <status>.

<Evidence plan.>
Detail: `_PROBE/PP02_<slug>.md`


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
