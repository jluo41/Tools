---
status: fixed (structure-claims v1.1.0: status col + per-claim detail + no-planned)
created: 2026-06-22
context: haipipe-paper-structure-claims + the live ledger Paper-Personality-Opioid-MedJournal/0-lifecycle/2-claims/2-claims.tex
fixed_in: ""
---
ok feedback for claims， also very thin，how do you think we can provide more evidence? from discovery or from tasks?

Diagnosis (after reading the skill):
- The live 2-claims.tex does NOT follow the claims skill's own canonical format. Skill mandates columns: ID | Claim | Status (supported/weak/GAP) | Evidence Source / Open Need, with the source being a real ref (probe verdict path / task contract / discover question) and a delivery need emitted for every weak/GAP row. The live ledger instead uses ID | Claim | Evidence Anchor | Limitation, has NO status column, and every anchor is aspirational ("planned Table 1 / eFigure 1") rather than a real source. By the skill's own rules every row is currently GAP.
- Even when filled per the skill, the ledger is still thin: a "supported" row only points to a probe verdict path. It does not carry the quantified result (effect size / CI / N), a robustness note, or an outside-literature anchor (consistent-with / contradicts prior work). So a reader cannot see how strong each claim is or how it sits against the field.

Suggested fix direction (skill):
- Enforce the Status column + real Source ref; flag aspirational anchors ("planned ...") as GAP, not as evidence.
- Enrich the row schema so a claim carries: status, quantified result, caveat, outside-literature anchor, display ref. A verdict pointer alone is not enough to make the ledger non-thin.
- Add a done-rubric (parallel to the pitch quality-gate gap) so a claim is not "done" until it has status + a real source + (for supported) a quantified result.

Design question resolution (discovery vs tasks):
- Empirical claims C1-C4 (effect, margin, threshold, subgroup) get their teeth from TASKS (run the regression on CMS data; outputs likely already exist in Z01/Z02) -> then a PROBE judges whether the result supports the claim -> backfill verdict + number into the ledger. Tasks are primary here.
- C5 (measurement / discriminant validity, "trait != generic sentiment") needs DISCOVERY (the established way to demonstrate discriminant validity + prior work on review sentiment vs traits) AND a task (compute the check).
- DISCOVERY is the secondary layer for ALL claims: an outside-literature anchor that says whether each finding is consistent with or surprising against prior work. That is what turns a bare number into a defensible claim.
- Net: tasks -> probe for the numbers; discovery for framing/validity/novelty. Not either/or.

Fix:
