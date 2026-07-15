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
------

Each probe is its own sub-item organized by PP number.
Full evidence plan: type, claims, status, dependencies, what work to do.
Separated by `---` horizontal rules.

**PP01 - <title> - <state>**

Type: <task | discovery>.
Claims: <which claims this settles>.
State: <planned | commissioned | answered | read>   (DERIVED from the probe file, never asserted)
<Dependencies, if any.>

<Full evidence plan, one sentence per line.>
<What the work produces.>
<Design decisions to settle.>
Detail: `1-probes/PP01_<topic>.md` (the question's SECTION)

---

**PP02 - <title> - <status>**

Type: <task | discovery>.
Claims: <which claims>.
Status: <status>.

<Evidence plan.>
Detail: `1-probes/PP02_<topic>.md` (the question's SECTION)


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
